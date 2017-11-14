# -*- coding: utf-8 -*-
###############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2009-TODAY Odoo Peru(<http://www.odooperu.pe>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Lesser General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Lesser General Public License for more details.
#
#    You should have received a copy of the GNU Lesser General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################

import datetime
from lxml import etree
import math
import pytz
from PIL import Image

from odoo import models, fields, api

class res_partner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    state_id = fields.Many2one('res.country.state', 'Departamento')
    province_id = fields.Many2one('res.country.state', 'Provincia')
    district_id = fields.Many2one('res.country.state', 'Distrito')
        
    # Funcion reemplazada para considerar los nuevos campos en el onchange
    @api.model
    def _address_fields(self):
        """ Returns the list of address fields that are synced from the parent
        when the `use_parent_address` flag is set. """
        #~ return list(ADDRESS_FIELDS)
        address_fields = ('street', 'street2', 'zip', 'city', 'state_id', 'country_id','province_id','district_id')
        return list(address_fields)
    
    # Onchange para actualizar el codigo de distrito
    @api.onchange('district_id')
    def onchange_district(self):
        if self.district_id:
            state = self.district_id.code
            self.zip = state
    
    @api.multi
    def _display_address(self, without_company=False):

        '''
        The purpose of this function is to build and return an address formatted accordingly to the
        standards of the country where it belongs.

        :param address: browse record of the res.partner to format
        :returns: the address formatted in a display that fit its country habits (or the default ones
            if not country is specified)
        :rtype: string
        '''
        # get the information that will be injected into the display format
        # get the address format
        address_format = self.country_id.address_format or \
              "%(street)s\n%(street2)s\n%(state_name)s-%(province_name)s-%(district_code)s %(zip)s\n%(country_name)s"
        args = {
            'district_code': self.district_id.code or '',
            'district_name': self.district_id.name or '',
            'province_code': self.province_id.code or '',
            'province_name': self.province_id.name or '',
            'state_code': self.state_id.code or '',
            'state_name': self.state_id.name or '',
            'country_code': self.country_id.code or '',
            'country_name': self.country_id.name or '',
            'company_name': self.parent_name or '',
        }
        for field in self._address_fields():
            args[field] = getattr(self, field) or ''
        if without_company:
            args['company_name'] = ''
        elif self.commercial_company_name:
            address_format = '%(company_name)s\n' + address_format
        return address_format % args
