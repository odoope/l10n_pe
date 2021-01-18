# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import json
import logging
import math
import re
import time
import datetime
import requests

from odoo import api, fields, models, tools, _
from odoo.exceptions import Warning, UserError
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT


class Currency(models.Model):
    _inherit = "res.currency"
    _description = "Currency"
    
    rate_pe = fields.Float(compute='_compute_current_rate_pe', string='Peruvian format', digits=(12, 3),
                        help='Currency rate in peruvian format.')
    
    def _get_rates_pe(self, company, date):
        self.env['res.currency.rate'].flush(['rate_pe', 'currency_id', 'company_id', 'name'])
        query = """SELECT c.id,
                          COALESCE((SELECT r.rate_pe FROM res_currency_rate r
                                  WHERE r.currency_id = c.id AND r.name <= %s
                                    AND (r.company_id IS NULL OR r.company_id = %s)
                               ORDER BY r.company_id, r.name DESC
                                  LIMIT 1), 1.0) AS rate_pe
                   FROM res_currency c
                   WHERE c.id IN %s"""
        self._cr.execute(query, (date, company.id, tuple(self.ids)))
        currency_rates = dict(self._cr.fetchall())
        return currency_rates

    @api.depends('rate_ids.rate')
    def _compute_current_rate_pe(self):
        date = self._context.get('date') or fields.Date.today()
        company = self.env['res.company'].browse(self._context.get('company_id')) or self.env.company
        # the subquery selects the last rate before 'date' for the given currency/company
        currency_rates = self._get_rates_pe(company, date)
        for currency in self:
            currency.rate_pe = currency_rates.get(currency.id) or 1.0
    
    # TODO: Get currency rate from BCRP
    # def get_current_rate_pe(self, date=False):
    #     """PEN currency rate from 'Banco Central de Reserva del Peru'
    #     """
    #     if not date:
    #         date = fields.Date.today()
    #         print('today: ', date)
    #     for currency in self:
    #         if currency.name == 'USD':
    #             # Code for Sale / SUNAT
    #             code_ws = 'PD04640PD'
    #             # The current currency rate from BCRP is always one day before
    #             date_str = (date - datetime.timedelta(days=1)).strftime('%Y-%m-%d')
    #             url= "https://estadisticas.bcrp.gob.pe/estadisticas/series/api/%s/json/%s/%s/ing" % (code_ws, date_str, date_str)
    #             try:
    #                 res = requests.get(url)
    #                 res.raise_for_status()
    #                 data = res.json()
    #                 date_rate = datetime.datetime.strptime(data['periods'][0]['name'], '%d.%b.%y').strftime(DEFAULT_SERVER_DATE_FORMAT)
    #                 rate_pe = float(data['periods'][0]['values'][0])                    
    #                 for company in self.env['res.company'].search([]).filtered(lambda r: r.currency_id.name == 'PEN'):
    #                     vals = {
    #                         'company_id': company.id,
    #                         'currency_id': currency.id,
    #                         'name': date_rate,
    #                         'rate_pe': rate_pe,                            
    #                     }
    #                     rate_line = self.env['res.currency.rate'].search([ ('company_id','=',company.id),('currency_id','=',currency.id),('name','=',date_rate)], limit=1)
    #                     if rate_line:
    #                         rate_line.write(vals)
    #                     else:
    #                         rate_line = self.env['res.currency.rate'].create(vals)
    #                     rate_line.onchange_rate_pe()
    #             except:
    #                 return True
    #     return True

class CurrencyRate(models.Model):
    _inherit = "res.currency.rate"
    _description = "Currency Rate"

    rate_pe = fields.Float(string='Change type',digits=(12, 3), default=1.0, help='Currency rate in peruvian format. Ex: 3.25 when $1 = S/. 3.25')
    
    @api.onchange('rate_pe')
    def onchange_rate_pe(self):
        if self.rate_pe > 0:
            self.rate = 1 / self.rate_pe
        else:
            raise UserError(_('The amount must be greater than zero'))
        
