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

from . import models

from odoo import api, SUPERUSER_ID, _

def _update_company(env):
    """ This hook is used to set True the RUC/DNI validation
    when module odoope_ruc_validation is installed.
    """
    company_ids = env['res.company'].search([]).filtered(lambda r: r.country_id.code == 'PE')
    company_ids.write({
                        'l10n_pe_ruc_validation': True,
                        'l10n_pe_dni_validation': True})

def _odoope_ruc_validation_init(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _update_company(env)