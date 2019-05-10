# -*- coding: utf-8 -*-

from datetime import date, datetime, timedelta
from odoo.fields import Date, Datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    shop_ids = fields.One2many('einvoice.shop','company_id', string='Shops')
