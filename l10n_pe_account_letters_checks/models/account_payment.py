# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountPayment(models.Model):
    _inherit = 'account.payment'

    paid_state = fields.Selection([
        ('no', 'No Paid'),
        ('paid', 'Paid')
    ], string="Paid State", compute='_compute_paid_state')

    @api.depends('internal_payment_type', 'reconciled_statements_count')
    def _compute_paid_state(self):
        for rec in self:
            rec.paid_state = 'no'
            if rec.internal_payment_type != 'other' and rec.reconciled_statements_count != 0:
                rec.paid_state = 'paid'