# -*- coding: utf-8 -*-

import datetime
import re

from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class Education(models.Model):
    _name = 'student.education'
    _description = 'student.education'
    _rec_name = 'degree_name'

    # degree = fields.Many2one('student.information', string="Degree")
    degree_name = fields.Char(string="Degree")
    institute = fields.Char(string="Institute", required=True)
    # education_id = fields.Many2one('student.information')

    # order_id = fields.Many2one('sale.order', string='Order Reference', required=True, ondelete='cascade', index=True,
    #                          copy=False)
    education_id = fields.Many2one('student.information', string="Education Id", required=True, ondelete='cascade',
                                   index=True, copy=False)
    # institute = fields.Char(string="Institute")

    @api.model
    def year_selection(self):
        year = 1900
        year_list = []
        while year != int(datetime.date.today().year + 1):
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    pass_out_year = fields.Selection(year_selection, string='Pass-out Year')
    year_difference = fields.Integer(compute='_compute_difference', string="Difference of Year")

    @api.depends('pass_out_year')
    def _compute_difference(self):
        if self.pass_out_year:
            today = datetime.date.today().year
            self.year_difference = today - int(self.pass_out_year)
        else:
            self.year_difference = 0.0
