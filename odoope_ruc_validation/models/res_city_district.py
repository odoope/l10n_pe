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

class L10nPeResCityDistrict(models.Model):
    _inherit = 'l10n_pe.res.city.district'
    _rec_name = 'complete_name'

    complete_name = fields.Char("Full District Name", compute='_compute_complete_name')

    def name_get(self):
        res = []
        for district in self:
            if district.city_id:
                complete_name = '%s / %s ' % (district.name, district.city_id.name)
            else:
                complete_name = district.name
            res.append((district.id, complete_name))

        return res
        
    @api.depends('name', 'city_id.complete_name')
    def _compute_complete_name(self):
        for district in self:
            if district.city_id:
                district.complete_name = '%s / %s ' % (district.name, district.city_id.complete_name)
            else:
                district.complete_name = district.name