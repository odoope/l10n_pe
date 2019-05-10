# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo.fields import Date, Datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError

class EinvoiceShop(models.Model):
    _name = 'einvoice.shop'
    _description = 'Shops'
    
    name = fields.Char('Name', required=True)
    code = fields.Char('SUNAT Code', size=4, required=True, help='Code from SUNAT')
    company_id = fields.Many2one('res.company', 'Company', default=lambda self: self.env.user.company_id.id, index=1, required=True)
    journal_ids = fields.One2many('account.journal','shop_id', string='Journals', help='Select the from the journal configuration')
    partner_id = fields.Many2one('res.partner','Address')
    send_email = fields.Boolean(string='Send invoice by Email',help='Send email automatically when the invoice is sent')    
    user_ids = fields.Many2many('res.users', 'einvoice_shop_users_rel', 'shop_id', 'user_id', string='Users')
    
    
