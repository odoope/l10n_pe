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
from odoo.fields import Date, Datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError, AccessError

class ResCompany(models.Model):
    _inherit = 'res.company'

    l10n_pe_ruc_validation = fields.Boolean(string="RUC Validation")
    l10n_pe_dni_validation = fields.Boolean(string="DNI Validation")
    l10n_pe_api_dni_connection = fields.Selection([('jne','JNE') ,('facturacion_electronica','Facturacion Electronica DNI'),('free_api','Free Api')], string='Api DNI Connection', default='jne')
    l10n_pe_api_ruc_connection = fields.Selection([('sunat','Sunat')], string='Api RUC Connection', default='sunat')
    @api.onchange('country_id')
    def _onchange_country_id(self):
        super(ResCompany, self)._onchange_country_id()
        if self.country_id and self.country_id.code == 'PE':
            self.l10n_pe_ruc_validation = True
            self.l10n_pe_dni_validation = True
        else:
            self.l10n_pe_ruc_validation = False
            self.l10n_pe_dni_validation = False
