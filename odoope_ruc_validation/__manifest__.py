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
    'name' : 'Validador de RUC - Peru',
    'version' : '14.0.1.0.0',
    'author' : 'OPeru',
    'category' : 'Generic Modules/Base',
    'summary': 'RUC validator - PERU',
    'license': 'LGPL-3',
    'contributors': [
        'Enrique Huayas <enrique@operu.pe>',
        'Leonidas Pezo <leonidas@operu.pe>',
    ],
    'description' : """
Validador RUC
-----------------------
Clientes y Proveedores:
-----------------------
    * Nuevo campo "tipo de documento"
    * Validacion RUC
Dependencias:
-------------
$ sudo pip3 install beautifulsoup4

    """,
    'depends': ['l10n_latam_base','l10n_pe'],
    'data': [
        'views/res_partner_view.xml',
        'views/res_config_settings_views.xml',
        'views/res_company_views.xml',
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
    'support': 'modulos@operu.pe',
    'installable': True,
    'auto_install': False,
    "sequence": 1,

    'post_init_hook': '_odoope_ruc_validation_init',
}
