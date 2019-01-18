# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import math
import re
import time
try:
    from num2words import num2words
except ImportError:
    logging.getLogger(__name__).warning("The num2words python library is not installed, l10n_mx_edi features won't be fully available.")
    num2words = None

from odoo import api, fields, models, tools, _

TYPES = [('purchase','Compra'),('sale','Venta')]

class Currency(models.Model):
    _inherit = "res.currency"
    
    rate_pe = fields.Float(compute='_compute_current_rate_pe', string='Cambio del dia', digits=(12, 4),
                        help='Tipo de cambio del dia en formato peruano.')
    type = fields.Selection(TYPES,string='Tipo',default='sale')
    
    #~ Tipo de cambio PE ctual
    @api.multi
    def _compute_current_rate_pe(self):
        date = self._context.get('date') or fields.Date.today()
        company_id = self._context.get('company_id') or self.env['res.users']._get_company().id
        # the subquery selects the last rate before 'date' for the given currency/company
        query = """SELECT c.id, (SELECT r.rate_pe FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name <= %s
                                    AND (r.company_id IS NULL OR r.company_id = %s)
                               ORDER BY r.company_id, r.name DESC
                                  LIMIT 1) AS rate_pe
                   FROM res_currency c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, company_id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        for currency in self:
            currency.rate_pe = currency_rates.get(currency.id) or 1.0
    
    #~ Replace the original label for Amount to text
    @api.multi
    def amount_to_text(self, amount):
        self.ensure_one()
        def _num2words(number, lang):
            try:
                return num2words(number, lang=lang).title()
            except NotImplementedError:
                return num2words(number, lang='en').title()

        if num2words is None:
            logging.getLogger(__name__).warning("The library 'num2words' is missing, cannot render textual amounts.")
            return ""

        formatted = "%.{0}f".format(self.decimal_places) % amount
        parts = formatted.partition('.')
        integer_value = int(parts[0])
        fractional_value = int(parts[2] or 0)
        if fractional_value == 0:
            fractional_value = '00'

        lang_code = self.env.context.get('lang') or self.env.user.lang
        lang = self.env['res.lang'].search([('code', '=', lang_code)])
        amount_words = tools.ustr('{amt_value}').format(
                        amt_value=_num2words(integer_value, lang=lang.iso_code)
                        )
        #~ For decimals
        amount_words += ' ' + _('con') + tools.ustr(' {amt_value}/100 {amt_word}').format(
                    amt_value= fractional_value,
                    amt_word=self.currency_unit_label,
                    )
        return amount_words
        
    #~ Agrega tipo de moneda en nombre
    @api.multi
    def name_get(self):
        return [(currency.id, tools.ustr(currency.name + ' - ' + dict(TYPES)[currency.type])) for currency in self]
    

class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    _description = "Currency Rate"

    rate_pe = fields.Float(string='Cambio',digits=(12, 4), help='Tipo de cambio en formato peruano. Ejm: 3.25 si $1 = S/. 3.25')
    type = fields.Selection(related="currency_id.type", store=True)
    
    @api.onchange('rate_pe')
    def onchange_rate_pe(self):
        if self.rate_pe > 0:
            self.rate = 1 / self.rate_pe
       
