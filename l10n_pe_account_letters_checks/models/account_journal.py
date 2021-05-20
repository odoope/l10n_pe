# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountJournal(models.Model):
    _inherit = 'account.journal'

    internal_payment_type = fields.Selection([
        ('other', 'Others'),
        ('lp', 'Letter Payable'),
        ('lr', 'Letter Receivable'),
        ('cp', 'Check Payable'),
        ('cr', 'Check Receivable')
    ], string="Internal Payment Type", default='other')