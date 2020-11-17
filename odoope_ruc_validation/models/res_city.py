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

from odoo import fields, models, api

class City(models.Model):
    _inherit = "res.city"
    _rec_name = 'complete_name'

    complete_name = fields.Char("Full City Name", compute='_compute_complete_name')

    def name_get(self):
        res = []
        for city in self:
            if city.state_id:
                complete_name = '%s / %s ' % (city.name, city.state_id.name)
            else:
                complete_name = city.name
            res.append((city.id, complete_name))
        return res
        
    @api.depends('name', 'state_id.name')
    def _compute_complete_name(self):
        for city in self:
            if city.state_id:
                city.complete_name = '%s / %s ' % (city.name, city.state_id.name)
            else:
                city.complete_name = city.name