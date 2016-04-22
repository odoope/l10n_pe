# -*- encoding: utf-8 -*-
##############################################################################
{
  'name' : 'Plan Contable Odoo Peru',
  'summary': 'Modulo con el plan contable actualizado',
  'version' : '1.0',
  'description' : """
  Peruvian OpenERP localization

  """,
  'author' : ['Odoo Peru'],
  'website' : 'http://odooperu.pe',
  'category' : 'Localization/Account Charts',
  "sequence": 1,
  'complexity' : 'easy',
  'license' : 'AGPL-3',
  'depends' : ['account_chart'],
   "data":[
	'account_tax_code.xml',
    'accounts.xml',
    'account_tax.xml',
    'accounts_wizard.xml',
	],
  'images': [
        'static/description/plan_contable_banner.png',
    ],
  'demo_xml': [ ],
  'init_xml' : [ ],
  'update_xml' : [ ],
  'installable' : True,
  'active': False,
  'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
