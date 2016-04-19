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

from openerp.osv import fields, osv

class CountryState(osv.osv):
    _inherit = 'res.country.state'
    _columns = {
        'code': fields.char('Country Code', size=9,
            help='The ISO country code in two chars.\n'
            'You can use this field for quick search.'),
        'state_id': fields.many2one('res.country.state', 'Departamento'),
        'province_id': fields.many2one('res.country.state', 'Provincia'),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

