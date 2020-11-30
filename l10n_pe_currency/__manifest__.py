# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2019-TODAY OPeru.
#    Author      :  Grupo Odoo S.A.C. (<http://www.operu.pe>)
#
#    This program is copyright property of the author mentioned above.
#    You can`t redistribute it and/or modify it.
#
###############################################################################

{
    'name' : 'Tipo de cambio Peru',
    'version' : '1.0',
    'author' : 'OPeru',
    'category' : 'Generic Modules/Base',
    'summary': 'Permite ingresar tipo de cambio en formato peruano.',
    'license': 'AGPL-3',
    'contributors': [
        'Leonidas Pezo <leonidas@operu.pe>',
    ],
    'description' : """
Registro de tpo de cambio
-----------------------

Registra el tipo de cambio al estilo peruano:

ANTES:
 S/. 1 = S/. 1
   $ 1 = S/. 0.30769

AHORA
 S/. 1 = S/. 1
   $ 1 = S/. 3.25

    """,
    'website': 'http://www.operu.pe/contabilidad',
    'depends' : ['account'],
    'data': [
        'views/res_currency_view.xml',
        'data/res_currency_data.xml',
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
    "sequence": 2,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
