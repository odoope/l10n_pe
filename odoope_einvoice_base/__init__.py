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

from . import models
from . import wizard

from odoo import api, SUPERUSER_ID

def _create_shop(cr, registry):
    """ This hook is used to add a shop on existing companies
    when module l10n_pe is installed.
    """
    env = api.Environment(cr, SUPERUSER_ID, {})
    company_ids = env['res.company'].search([])
    company_with_shop = env['einvoice.shop'].search([]).mapped('company_id')
    company_without_shop = company_ids - company_with_shop
    for company in company_without_shop:
        # Getting internal users
        user_ids = env['res.users'].search([('company_id', '=', company.id),('share','=',False)]).ids
        print('Usuarios de compañia', user_ids)
        shop_id = env['einvoice.shop'].create({
            'name': '%s %s' % (company.name, company.id),
            'code': '0000',
            'company_id': company.id,
            'partner_id': company.partner_id.id,
            'user_ids': [(6, 0, user_ids)],
        })

        # Assigning shop to the sale journals
        sale_journal_ids = env['account.journal'].search([('company_id','=',company.id),('type','=','sale')])
        for journal in sale_journal_ids:
            journal.write({'shop_id': shop_id.id})
    
