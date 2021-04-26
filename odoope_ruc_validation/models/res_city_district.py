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

    def name_get(self):
        res = []
        for district in self:
            if district.city_id:
                display_name = '%s (%s)' % (district.name, district.city_id.name)
            else:
                display_name = district.name
            res.append((district.id, display_name))
        return res
