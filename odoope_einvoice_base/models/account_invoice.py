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

class AccountInvoice(models.Model): 
    
    _inherit = 'account.invoice'      
    
    amount_base = fields.Monetary(string='Subtotal',store=True, readonly=True, compute='_compute_amount', track_visibility='always', help='Total without discounts and taxes')
    amount_discount = fields.Monetary(string='Discount', store=True, readonly=True, compute='_compute_amount',track_visibility='always')
    credit_note_type = fields.Many2one('einvoice.catalog.09', string='Credit note type', help='Catalog 09: Type of Credit note')
    debit_note_type = fields.Many2one('einvoice.catalog.10', string='Debit note type', help='Catalog 10: Type of Debit note')      
    edocument_type = fields.Many2one('einvoice.catalog.01', string='Electronic document type', help='Catalog 01: Type of electronic document')    
    einv_amount_base = fields.Monetary(string='Base Amount', store=True, readonly=True, compute='_compute_amount', track_visibility='always', help='Total with discounts and before taxes')
    einv_amount_exonerated = fields.Monetary(string='Exonerated  Amount', store=True, compute='_compute_amount', track_visibility='always')
    einv_amount_free = fields.Monetary(string='Free Amount', store=True, compute='_compute_amount', track_visibility='always')
    einv_amount_unaffected = fields.Monetary(string='Unaffected Amount', store=True, compute='_compute_amount', track_visibility='always')
    einv_amount_igv = fields.Monetary(string='IGV Amount', store=True, compute='_compute_amount', track_visibility='always')
    einv_amount_others = fields.Monetary(string='Other charges', store=True, compute='_compute_amount', track_visibility='always')    
    einv_amount_untaxed = fields.Monetary(string='Total before taxes', store=True, compute='_compute_amount', track_visibility='always', help='Total before taxes, all discounts included')   
    einv_serie = fields.Char(string='E-invoice Serie', compute='_get_einvoice_number', store=True)
    einv_number = fields.Integer(string='E-invoice Number', compute='_get_einvoice_number', store=True)
    global_discount = fields.Monetary(string='Global discount', store=True, readonly=True, compute='_compute_amount',track_visibility='always')       
    igv_percent = fields.Integer(string="Percentage IGV", compute='_get_percentage_igv')
    origin_document_id = fields.Many2one('account.invoice', string='Origin document', help='Used for Credit an debit note')
    origin_document_serie = fields.Char(string='Document serie', help='Used for Credit an debit note')
    origin_document_number = fields.Char(string='Document number', help='Used for Credit an debit note')
    picking_number = fields.Char(string='Picking number')
    sent_ose = fields.Boolean(string='Sent to OSE')
    shop_id = fields.Many2one('einvoice.shop', string='Shop', related='journal_id.shop_id', store=True)
    
    # Onchange created for getting the default edocument type from the journal
    @api.onchange('journal_id')
    def onchange_edocument_type(self):        
        if self.journal_id:
            self.edocument_type = self.journal_id.edocument_type
    
    @api.one
    @api.depends('invoice_line_ids.price_subtotal', 'invoice_line_ids.price_base', 'tax_line_ids.amount',
                 'currency_id', 'company_id', 'date_invoice', 'type')
    def _compute_amount(self):
        sign = self.type in ['in_refund', 'out_refund'] and -1 or 1
        super(AccountInvoice, self)._compute_amount()
        self.global_discount = sum(line.price_base for line in self.invoice_line_ids.filtered(lambda r: r.price_base * sign < 0)) * sign * -1
        self.amount_discount = sum((line.price_base * line.discount)/100 for line in self.invoice_line_ids.filtered(lambda r: r.free_product == False))
        self.amount_base = sum(line.price_base for line in self.invoice_line_ids.filtered(lambda r: r.price_total > 0))
        #~ E-invoice amounts
        self.einv_amount_free = sum(line.amount_free for line in self.invoice_line_ids)
        self.einv_amount_base = sum(line.base for line in self.tax_line_ids.filtered(lambda r: r.einv_type_tax in ('igv','isc')))
        self.einv_amount_exonerated = sum(line.base for line in self.tax_line_ids.filtered(lambda r: r.einv_type_tax == 'exonerated'))
        self.einv_amount_unaffected = sum(line.base for line in self.tax_line_ids.filtered(lambda r: r.einv_type_tax == 'unaffected'))
        self.einv_amount_igv = sum(line.amount_total for line in self.tax_line_ids.filtered(lambda r: r.einv_type_tax == 'igv'))
        self.einv_amount_others = sum(line.amount_total for line in self.tax_line_ids.filtered(lambda r: r.einv_type_tax == 'others'))
        self.einv_amount_untaxed = self.einv_amount_base - self.einv_amount_free 
    
    @api.multi
    @api.depends('move_id.name','move_name')
    def _get_einvoice_number(self):
        for inv in self:
            if inv.move_name and inv.type in ['out_invoice','out_refund']:
                inv_number = inv.move_name.split('-')
                if len(inv_number) == 2:
                     inv.einv_serie = inv_number[0]
                     inv.einv_number = inv_number[1]
        return True
    
    @api.depends('tax_line_ids')
    def _get_percentage_igv(self):
        for inv in self:
            igv = 0.0
            if inv.tax_line_ids:
                for tax in inv.tax_line_ids.filtered(lambda r: r.einv_type_tax == 'igv' and r.tax_id.amount_type == 'percent'):
                    igv = int(tax.tax_id.amount)
            inv.igv_percent = igv
        return True
    
    @api.onchange('origin_document_id')
    def onchange_origin_document(self):        
        if self.origin_document_id:
            if self.type == 'out_refund':
                self.origin_document_serie = self.origin_document_id.einv_serie
                self.origin_document_number = self.origin_document_id.einv_number
            else:
                if self.origin_document_id and self.origin_document_id.reference:
                    reference = self.origin_document_id.reference
                    if len(reference.split('-')) == 2:
                        self.origin_document_serie = self.origin_document_id.reference.split('-')[0]
                        self.origin_document_number = self.origin_document_id.reference.split('-')[1]
                    
    def _prepare_tax_line_vals(self, line, tax):
        #~ Adding Type of tax IGV, ISC and others
        vals = super(AccountInvoice, self)._prepare_tax_line_vals(line, tax)
        vals.update({'einv_type_tax':self.env['account.tax'].browse(tax['id']).einv_type_tax})
        return vals    
        
class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"
    
    def _get_igv_type(self):
        return self.env['einvoice.catalog.07'].search([('code','=','10')], limit=1)
        
    amount_discount = fields.Monetary(string='Amount discount before taxes', readonly=True, compute='_compute_price')
    amount_free = fields.Monetary(string='Amount free', readonly=True, compute='_compute_price')
    free_product = fields.Boolean('Free', compute='_compute_price', store=True, default=False)
    igv_type = fields.Many2one('einvoice.catalog.07', string="Type of IGV", default=_get_igv_type)
    igv_amount = fields.Monetary(string='IGV amount',readonly=True, compute='_compute_price', help="Total IGV amount")
    price_base = fields.Monetary(string='Subtotal without discounts', readonly=True, compute='_compute_price', help="Total amount without discounts and taxes")
    price_total = fields.Monetary(string='Amount (with Taxes)',
        store=True, readonly=True, compute='_compute_price', help="Total amount with taxes")
    price_unit_excluded = fields.Monetary(string='Price unit excluded', readonly=True, compute='_compute_price', help="Price unit without taxes")
    price_unit_included = fields.Monetary(string='Price unit IGV included', readonly=True, compute='_compute_price', help="Price unit with IGV included")
        
    @api.one
    @api.depends('price_unit', 'discount', 'invoice_line_tax_ids', 'quantity',
        'product_id', 'invoice_id.partner_id', 'invoice_id.currency_id', 'invoice_id.company_id',
        'invoice_id.date_invoice', 'invoice_id.date')
    def _compute_price(self):
        '''
        return price_base = price_subtotal whitout discounts
        '''
        super(AccountInvoiceLine, self)._compute_price()      
        if self.display_type == False:
            currency = self.invoice_id and self.invoice_id.currency_id or None
            price = self.price_unit        
            # without all taxes
            taxes = False
            if self.invoice_line_tax_ids:
                taxes = self.invoice_line_tax_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
            if self.quantity == 0:
                raise UserError('The quantity cannot be 0')
            else:
                self.price_unit_excluded = price_unit_excluded_signed = taxes['total_excluded']/self.quantity if taxes else price
                self.price_base = price_base_signed = taxes['total_excluded'] if taxes else self.quantity * price 
            #~ With IGV taxes
            igv_taxes = False
            igv_taxes_ids = self.invoice_line_tax_ids.filtered(lambda r: r.einv_type_tax == 'igv')
            if igv_taxes_ids:
                igv_taxes = igv_taxes_ids.compute_all(price, currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
            self.price_unit_included = price_unit_included_signed = igv_taxes['total_included']/self.quantity if igv_taxes else price
            #~ IGV amount after discount
            if igv_taxes_ids:
                igv_taxes_discount = igv_taxes_ids.compute_all(price * (1 - (self.discount or 0.0) / 100.0), currency, self.quantity, product=self.product_id, partner=self.invoice_id.partner_id)
                self.igv_amount = sum( r['amount'] for r in igv_taxes_discount['taxes'])        
            
            self.price_total = taxes['total_included'] if taxes else self.price_subtotal
            sign = self.invoice_id.type in ['in_refund', 'out_refund'] and -1 or 1
            self.price_base = price_base_signed * sign       
            self.price_unit_excluded = price_unit_excluded_signed * sign       
            self.price_unit_included = price_unit_included_signed * sign    
            #~ Discount line
            #~ Free amount
            if self.discount >= 100.0:  
                self.igv_amount = 0.0   # When the product is free, igv = 0
                self.amount_discount = 0.0  # Although the product has 100% discount, the amount of discount in a free product is 0 
                self.igv_type = self.env['einvoice.catalog.07'].search([('code','=','15')], limit=1)
                self.free_product = True
                self.amount_free = self.price_unit_excluded * self.quantity
            else:
                self.amount_discount = (self.price_unit_excluded * self.discount * self.quantity) / 100
                self.igv_amount = abs(self.igv_amount) > 0.01 and abs(self.igv_amount) or 0.02 # The IGV must be > 0.01, i't mandatory in Odoofact
                self.igv_type = self.env['einvoice.catalog.07'].search([('code','=','10')], limit=1)
                self.free_product = False
    

    @api.onchange('igv_type')
    def onchange_igv_type(self):
        if self.igv_type:
            company_id = self.company_id or self.env.user.company_id
            taxes = self.env['account.tax'].search([('company_id','=',company_id.id)])
            if self.igv_type.type == 'gravado':
                taxes = taxes.filtered(lambda r: r.einv_type_tax == 'igv')[0]
            elif self.igv_type.type == 'inafecto':
                taxes = taxes.filtered(lambda r: r.einv_type_tax == 'unaffected')[0]
            else:
                taxes = taxes.filtered(lambda r: r.einv_type_tax == 'exonerated')[0]
            self.invoice_line_tax_ids = self.invoice_id.fiscal_position_id.map_tax(taxes, self.product_id, self.invoice_id.partner_id)
              
class AccountInvoiceTax(models.Model):
    _inherit = "account.invoice.tax"
    
    einv_type_tax = fields.Selection(related='tax_id.einv_type_tax', string="Tax type")
