# -*- coding: utf-8 -*-

from odoo import models, fields, api, _

class AccountMove(models.Model):
    _inherit = 'account.move'

    internal_payment_type = fields.Selection(related='journal_id.internal_payment_type')

    def action_register_payment(self):
        if len(self.ids) == 1:
            vals = {
                'name': _('Register Payment'),
                'res_model': 'account.payment.register',
                'view_mode': 'form',
                'context': {
                    'active_model': 'account.move',
                    'active_ids': self.ids,
                },
                'target': 'new',
                'type': 'ir.actions.act_window',
            }
            if self.move_type == 'out_invoice':
                view_id = self.env.ref('l10n_pe_account_letters_checks.view_account_payment_register_form_receivable').id
                vals['view_id'] = view_id
                return vals
            if self.move_type == 'in_invoice':
                view_id = self.env.ref('l10n_pe_account_letters_checks.view_account_payment_register_form_payable').id
                vals['view_id'] = view_id
                return vals
        return super(AccountMove, self).action_register_payment()