# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import math
import re
import time

from odoo import api, fields, models, tools, _

TYPES = [('purchase','Compra'),('sale','Venta')]

class Currency(models.Model):
    _inherit = "res.currency"
    _description = "Currency"
    
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
    
    #~ Agrega tipo de moneda en nombre
    @api.multi
    def name_get(self):
        return [(currency.id, tools.ustr(currency.name + ' - ' + dict(TYPES)[currency.type])) for currency in self]
    
    _sql_constraints = [
        ('unique_name', 'unique (name,type)', 'Solo puede existir una moneda con el mismo tipo de cambio!'),
        ('rounding_gt_zero', 'CHECK (rounding>0)', 'The rounding factor must be greater than 0!')
    ]

class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    _description = "Currency Rate"

    rate_pe = fields.Float(string='Cambio',digits=(12, 4), help='Tipo de cambio en formato peruano. Ejm: 3.25 si $1 = S/. 3.25')
    type = fields.Selection(related="currency_id.type", store=True)
    
    @api.onchange('rate_pe')
    def onchange_rate_pe(self):
        if self.rate_pe > 0:
            self.rate = 1 / self.rate_pe
