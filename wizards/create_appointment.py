# -*- coding: utf-8 -*-

from odoo import models, fields, api


class CreateAppointment(models.TransientModel):
    _name = 'create.appointment'

    partner = fields.Many2one('res.partner', string="Patient")
    appointment_date = fields.Date(string="Appointment Date")
    doctor = fields.Many2one('hospital.doctor', string="Doctor")

    def create_appointment(self):
        vals = {
            'partner': self.partner.id,
            'appointment_date': self.appointment_date,
            'doctor': self.doctor.id,
        }
        self.env['hospital.appointment'].create(vals)

    def get_data(self):
        appointments = self.env['hospital.appointment'].search([])
        for rec in appointments:
            print(rec.id)