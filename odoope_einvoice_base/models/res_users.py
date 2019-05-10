# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
import logging

from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.exceptions import AccessDenied, AccessError, UserError, ValidationError
from odoo.osv import expression
from odoo.service.db import check_super
from odoo.tools import partition

_logger = logging.getLogger(__name__)

class Users(models.Model):
    _inherit = "res.users"
    
    shop_ids = fields.Many2many('einvoice.shop', 'einvoice_shop_users_rel', 'user_id', 'shop_id', string='Shops')
