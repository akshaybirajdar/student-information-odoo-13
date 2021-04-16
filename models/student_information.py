# -*- coding: utf-8 -*-

import datetime
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class StudentInformation(models.Model):
    _name = 'student.information'
    _description = 'student.information'

    name = fields.Char(string="Registration", readonly=True, required=True, copy=False, default='New')

    student = fields.Many2one('res.partner', string="Student", required=True)
    email = fields.Char(string="Email Id")
    mobile = fields.Char(string="Mobile No")
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    # order_line = fields.One2many('sale.order.line', 'order_id', string='Order Lines',
    #                               states={'cancel': [('readonly', True)], 'done': [('readonly', True)]}, copy=True,
    #                               auto_join=True)

    education_line = fields.One2many('student.education', 'education_id', string='Education Line', auto_join=True)

    @api.onchange('mobile')
    def _onchange_mobile(self):
        for rec in self:
            if rec.mobile:
                pattern = re.compile(r'(?:0|\+?)\s?(?:\d\s?){9,11}$')
                if not pattern.match(self.mobile):
                    raise ValidationError("Invalid mobile number!")

    @api.onchange('email')
    def validate_mail(self):
        for rec in self:
            if rec.email:
                match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', self.email)
                if match == None:
                    raise ValidationError('Invalid Email Id!')

    @api.constrains('mobile')
    def _check_duplicate_mobile(self):
        for rec in self:
            mobiles = self.env['res.partner'].search([('id', '!=', rec.student.id), ('mobile', '=', rec.mobile)])
            print("Mobiles are", mobiles)
            for obj in mobiles:
                if obj.mobile:
                    print(obj, "  ", obj.mobile)
                    raise ValidationError("Duplicate Mobile Number.")

    @api.constrains('email')
    def _check_duplicate_email(self):
        for rec in self:
            emails = self.env['res.partner'].search([('id', '!=', rec.student.id), ('email', '=', rec.email)])
            for obj in emails:
                if obj.email:
                    raise ValidationError("Duplicate Email.")

    @api.model
    def year_selection(self):
        year = 1900
        year_list = []
        while year != int(datetime.date.today().year + 1):
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    state = fields.Selection([
        ('draft', "Draft"),
        ('approve', "Approved"),
        ('cancel', "Cancelled"),
    ], string="Status", readonly=True, default='draft')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('student_information_sequence') or 'New'
        result = super(StudentInformation, self).create(vals)
        return result

    def action_approve(self):
        for rec in self:
            rec.state = 'approve'

    def action_cancel(self):
        for rec in self:
            rec.state = 'cancel'

    def action_reset(self):
        for rec in self:
            rec.state = 'draft'
