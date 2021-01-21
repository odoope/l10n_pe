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

    ruc_validation = fields.Boolean(string="Ruc Validation", related='company_id.ruc_validation',readonly=False)
    dni_validation = fields.Boolean(string="Dni Validation", related='company_id.dni_validation',readonly=False)
    