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

{
    'name' : 'Factura electronica - Base',
    'version' : '2.0.0',
    'author' : 'Odoo Peru',
    'category' : 'Accounting & Finance',
    'summary': 'Tablas y requisitos mínimos para la factura electrónica.',
    'license': 'LGPL-3',
    'contributors': [
        'Leonidas Pezo <leonidas@odooperu.pe>',
    ],
    'description' : """
Factura electronica - Base.
====================================

Tablas:
--------------------------------------------
    * Tablas requeridas por la Factura electrónica

    """,
    'website': 'http://www.odooperu.pe/contabilidad',
    'depends' : ['base','account','odoope_ruc_validation'],
    'data': [
        'wizard/einvoice_ose_views.xml',
        'views/einvoice_views.xml',
        'views/account_views.xml',
        'views/account_invoice_view.xml',
        'views/product_product_views.xml',        
        'views/res_users_view.xml',
        'views/shop_views.xml',
        'data/einvoice_data.xml',
        'data/account_data.xml',        
        'views/res_config_settings_views.xml',
        'security/einvoice_base_security.xml',
        'security/ir.model.access.csv',
    ],
    'qweb' : [

    ],
    'demo': [
        
    ],
    'test': [
        
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'auto_install': False,
    "sequence": 1,
    'post_init_hook': '_create_shop',
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
