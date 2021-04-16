# -*- coding: utf-8 -*-
from odoo import fields, models, api
from odoo.exceptions import ValidationError
import datetime


class Patient(models.Model):
    _inherit = 'res.partner'

    @api.model
    def create(self, vals_list):
        res = super(Patient, self).create(vals_list)
        return res


