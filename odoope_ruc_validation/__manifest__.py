# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009-TODAY Odoo Peru(<http://www.odooperu.pe>).
#    
#    This module builds on a alexcuellar module at https://github.com/alexcuellar/l10n_pe_doc_validation
#    Este módulo esta basado en el módulo de Alex Cuellar en https://github.com/alexcuellar/l10n_pe_doc_validation
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
    'name' : 'Validador RUC/DNI',
    'version' : '1.2.2',
    'author' : 'Odoo Peru',
    'category' : 'Generic Modules/Base',
    'summary': 'Valida RUC y DNI.',
    'license': 'AGPL-3',
    'contributors': [
        'Leonidas Pezo <leonidas@odooperu.pe>',
    ],
    'description' : """
Validador RUC y DNI
-----------------------

Clientes y Proveedores:
-----------------------
    * Nuevo campo "tipo de documento"
    * Validacion RUC y DNI

Dependencias:
-------------
$ sudo apt-get install tesseract-ocr tesseract-ocr-eng python-imaging python-pip python-bs4
$ sudo pip install pytesseract

Créditos:
---------
Este módulo esta basado en el módulo de Alex Cuellar en https://github.com/alexcuellar/l10n_pe_doc_validation

    """,
    'website': 'http://odooperu.pe/page/contabilidad',
    'depends' : ['account','odoope_einvoice_base','odoope_toponyms'],
    'data': [
        'views/res_partner_view.xml',
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
    'application': True,
    "sequence": 1,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
