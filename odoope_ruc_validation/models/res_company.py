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

from datetime import date, datetime, timedelta

from odoo import models, fields, api, _
from odoo.fields import Date, Datetime
from odoo.exceptions import ValidationError, UserError, AccessError

class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_pe_ruc_validation = fields.Boolean(string="RUC Validation")
    l10n_pe_dni_validation = fields.Boolean(string="DNI Validation")
    l10n_pe_api_dni_connection = fields.Selection([('consul_dni_api','CONSULTA DNI API')], string='Api DNI Connection', default='consul_dni_api')
    l10n_pe_api_ruc_connection = fields.Selection([('consul_ruc_api','CONSULTA RUC API')], string='Api RUC Connection', default='consul_ruc_api')

    @api.onchange('country_id')
    def _onchange_country_id(self):
        super(ResCompany, self)._onchange_country_id()
        if self.country_id and self.country_id.code == 'PE':
            self.l10n_pe_ruc_validation = True
            self.l10n_pe_dni_validation = True
        else:
            self.l10n_pe_ruc_validation = False
            self.l10n_pe_dni_validation = False