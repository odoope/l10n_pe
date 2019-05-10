# -*- coding: utf-8 -*-

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
    
    edocument_credit = fields.Many2one('einvoice.catalog.01', string='Credit document type', help='Catalog 01: Type of electronic document for Credit Note', default=lambda self: self._default_credit_edocument())
    edocument_debit = fields.Many2one('einvoice.catalog.01', string='Debit document type', help='Catalog 01: Type of electronic document for Debit Note', default=lambda self: self._default_debit_edocument())
    edocument_type = fields.Many2one('einvoice.catalog.01', string='Electronic document type', help='Catalog 01: Type of electronic document')
    label_to_print = fields.Char(string='Label to print', size=256)
    shop_id = fields.Many2one('einvoice.shop', string='Shop')
    
    @api.onchange('edocument_type')
    def onchange_edocument_type(self):
        if self.edocument_type:
            self.label_to_print = self.edocument_type.label or self.edocument_type.name
    
class AccountTax(models.Model):
    _inherit = 'account.tax'
    
    einv_type_tax = fields.Selection([('igv','IGV'),('isc','ISC'),('exonerated','Exonerated'),('unaffected','Unaffected'),('other','Others')], 
            string="Tax type",default='igv')
    
