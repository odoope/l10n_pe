# -*- coding: utf-8 -*-
from odoo import models, fields


class ConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    validation_service_key = fields.Char("Validation service key", config_parameter='iap.validation_service_key')
