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

    def name_get(self):
        res = []
        for city in self:
            if city.state_id:
                display_name = '%s (%s)' % (city.name, city.state_id.name)
            else:
                display_name = city.name
            res.append((city.id, display_name))
        return res
