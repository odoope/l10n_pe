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

from odoo import api, fields, models, _

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    l10n_pe_ruc_validation = fields.Boolean(string="RUC Validation", related='company_id.l10n_pe_ruc_validation', readonly=False)
    l10n_pe_dni_validation = fields.Boolean(string="DNI Validation", related='company_id.l10n_pe_dni_validation', readonly=False)
    
