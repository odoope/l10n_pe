# -*- coding: utf-8 -*-
{
    'name': "IAP Validation RUC and DNI service",
    'summary': "Get partners Validation information by RUC and DNI number",
    'author' : 'OPeru',
    'category' : 'Generic Modules/Base',
    'license': 'LGPL-3',
    'contributors': [
        'Angel Rodriguez <angel@operu.pe>',
        'Leonidas Pezo <leonidas@operu.pe>',
    ],

    'version': '14.0.1.0.0',
    'depends': ['iap', 'web', 'base_setup'],
    'data': [
        'security/ir.model.access.csv',
        'views/validation_info_views.xml',
        'views/res_config_settings.xml',
    ]
}
