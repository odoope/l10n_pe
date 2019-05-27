# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009-TODAY Odoo Peru(<http://www.odooperu.pe>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import time
import math

from odoo.osv import expression
from odoo.tools.float_utils import float_round as round
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT
from odoo.exceptions import UserError, ValidationError
from odoo import api, fields, models, _

class AccountJournal(models.Model):
    _inherit = "account.journal"
    
    @api.model
    def _default_credit_edocument(self):
        return self.env['einvoice.catalog.01'].search([('code','in',['07','87','97'])], limit=1)
        
    @api.model
    def _default_debit_edocument(self):
        return self.env['einvoice.catalog.01'].search([('code','in',['08','88','98'])], limit=1)
    
    edocument_credit = fields.Many2one('einvoice.catalog.01', string='Credit document type', help='Catalog 01: Type of electronic document for Credit Note', default=_default_credit_edocument)
    edocument_debit = fields.Many2one('einvoice.catalog.01', string='Debit document type', help='Catalog 01: Type of electronic document for Debit Note', default=_default_debit_edocument)
    edocument_type = fields.Many2one('einvoice.catalog.01', string='Electronic document type', help='Catalog 01: Type of electronic document')
    shop_id = fields.Many2one('einvoice.shop', string='Shop')
    
class AccountTax(models.Model):
    _inherit = 'account.tax'
    
    einv_type_tax = fields.Selection([('igv','IGV'),('isc','ISC'),('exonerated','Exonerated'),('unaffected','Unaffected'),('other','Others')], 
            string="Tax type",default='igv')
    
