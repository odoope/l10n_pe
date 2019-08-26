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
    'name' : 'Factura electronica - Datos Tabla 25',
    'version' : '1.0.1',
    'author' : 'Odoo Peru',
    'category' : 'Accounting & Finance',
    'summary': 'Datos de Tablas para la factura electrónica.',
    'license': 'AGPL-3',
    'contributors': [
        'Leonidas Pezo <leonidas@odooperu.pe>',
    ],
    'description' : """
Factura electronica - Datos tabla 25.
====================================

Tablas:
--------------------------------------------
    * Tablas requeridas por la Factura electrónica

    """,
    'website': 'http://www.odooperu.pe/contabilidad',
    'depends' : ['odoope_einvoice_base'],
    'data': [
        'data/einvoice_data_part1.xml',
        'data/einvoice_data_part2.xml',
        'data/einvoice_data_part3.xml',
        'data/einvoice_data_part4.xml',
        'data/einvoice_data_part5.xml',
    ],
    'qweb' : [

    ],
    'demo': [
        #'demo/account_demo.xml',
    ],
    'test': [
        #'test/account_test_users.yml',
    ],
    'images': [
        'static/description/banner.png',
    ],
    'installable': True,
    'auto_install': False,
    "sequence": 1,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
