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
    'name': 'RUC validator',
    'version': '0.3',
    'author': 'OPeru',
    'category': 'Generic Modules',
    'summary': 'RUC validator.',
    'description': ''' RUC validator.''',
    'depends': ['l10n_latam_base','l10n_pe'],
    'data': [ 
        'views/res_partner_view.xml',      
    ],
    'installable': True,
    'license': 'OPL-1',
    'support': 'soporte@operu.pe',
    'sequence': 1,
}

