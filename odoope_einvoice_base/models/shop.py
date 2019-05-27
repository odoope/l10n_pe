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
    
    
