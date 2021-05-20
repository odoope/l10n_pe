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
    'name' : 'Letras y Cheques',
    'version' : '14.0.1.0.0',
    'author' : 'Grupo Odoo SAC',
    'category' : 'Acounting',
    'summary': 'Permite registrar Letras y Cheques',
    'license': 'AGPL-3',
    'contributors': [
        'Leonidas Pezo <leonidas@operu.pe>',
    ],
    'description' : """
    Registro de Letras y Cheques como pagos de Factura
    """,
    'website': 'http://www.operu.pe/contabilidad',
    'depends' : ['account'],
    'data': [
        'views/account_journal_views.xml',
        'views/account_payment_views.xml',
    ],
    'installable': True,
    "sequence": 2,
}