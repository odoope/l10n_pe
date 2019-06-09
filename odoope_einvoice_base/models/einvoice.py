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

from odoo import models, fields, api

class EinvoiceCatalogTmpl(models.Model):
    _name = 'einvoice.catalog.tmpl'
    _description = 'Catalog Template'

    code = fields.Char(string='Code', size=4, index=True, required=True)
    name = fields.Char(string='Description', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result

class EinvoiceCatalog01(models.Model):
    _name = 'einvoice.catalog.01'
    _description = 'Codigo de Tipo de documento'
    _inherit = 'einvoice.catalog.tmpl'

    label = fields.Char(string='Label to print', size=256)

class EinvoiceCatalog05(models.Model):
    _name = "einvoice.catalog.05"
    _description = 'Codigo de Tipo de tributo'
    _inherit = 'einvoice.catalog.tmpl'

    un_5153 = fields.Char(string='UN/ECE 5153-Duty or tax or fee type name code', size=5)
    un_5103 = fields.Char(string='UN/ECE 5305-Duty or tax or fee category code', size=1)

class EinvoiceCatalog06(models.Model):
    _name = "einvoice.catalog.06"
    _description = 'Tipo de documento de Identidad'
    _inherit = 'einvoice.catalog.tmpl'

    default = fields.Char(string='Default value', size=128)
        
class EinvoiceCatalog07(models.Model):
    _name = "einvoice.catalog.07"
    _description = 'Codigos de Tipo de Afectacion del IGV'
    _inherit = 'einvoice.catalog.tmpl'

    no_onerosa = fields.Boolean(string='No onerosa')
    type = fields.Selection([('gravado','Gravado'),('exonerado','Exonerado'),('inafecto','Inafecto')],string='Tipo')
    
class EinvoiceCatalog08(models.Model):
    _name = "einvoice.catalog.08"
    _description = 'Codigos de Tipo de Afectacion del IGV'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog09(models.Model):
    _name = "einvoice.catalog.09"
    _description = 'Codigos de Tipo de Nota de Credito Electronica'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog10(models.Model):
    _name = "einvoice.catalog.10"
    _description = 'Codigos de Tipo de Nota de Debito Electronica'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog11(models.Model):
    _name = "einvoice.catalog.11"
    _description = 'Codigo de Tipo de Valor de Venta'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog12(models.Model):
    _name = "einvoice.catalog.12"
    _description = 'Codigos -Documentos Relacionados Tributarios'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog14(models.Model):
    _name = "einvoice.catalog.14"
    _description = 'Codigos - Otros Conceptos Tributarios'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog15(models.Model):
    _name = "einvoice.catalog.15"
    _description = 'Codigos-Elementos Adicionales en la Factura Electrónica '
    _inherit = 'einvoice.catalog.tmpl'

    name = fields.Char(string='Value', size=256, index=True, required=True)

class EinvoiceCatalog16(models.Model):
    _name = "einvoice.catalog.16"
    _description = 'Codigos - Tipo de Precio de Venta Unitario'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog17(models.Model):
    _name = "einvoice.catalog.17"
    _description = 'Codigos -Tipo de Operacion'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog18(models.Model):
    _name = "einvoice.catalog.18"
    _description = 'Codigos - Modalidad de  Traslado'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog19(models.Model):
    _name = "einvoice.catalog.19"
    _description = 'Codigos de Estado de Item'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog20(models.Model):
    _name = "einvoice.catalog.20"
    _description = 'Codigos - Motivo de Traslado'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog21(models.Model):
    _name = "einvoice.catalog.21"
    _description = 'Codigos-Documentos Relacionados '
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog22(models.Model):
    _name = "einvoice.catalog.22"
    _description = 'Codigos- Regimenes de Percepcion'
    _inherit = 'einvoice.catalog.tmpl'

    rate = fields.Char(string='Tasa', size=10, index=True, required=True)

class EinvoiceCatalog23(models.Model):
    _name = "einvoice.catalog.23"
    _description = 'Codigos- Regimenes de Retencion'
    _inherit = 'einvoice.catalog.tmpl'

class EinvoiceCatalog24(models.Model):
    _name = "einvoice.catalog.24"
    _description = 'Codigos- Recibo Electronico por Servicios Publicos'
    _inherit = 'einvoice.catalog.tmpl'

    name = fields.Char(string='Service', size=128, index=True, required=True)
    rate_code = fields.Char(string='Rate code', size=4, index=True, required=True)
    
class EinvoiceCatalog25(models.Model):
    _name = "einvoice.catalog.25"
    _description = 'Codigos - Producto SUNAT'
    _inherit = 'einvoice.catalog.tmpl'

    code = fields.Char(string='Code', size=12, index=True, required=True)

class EinvoiceCatalog51(models.Model):
    _name = "einvoice.catalog.51"
    _description = 'Codigo de  Tipo de Factura'
    _inherit = 'einvoice.catalog.tmpl'

    code = fields.Char(string='Code', size=12, index=True, required=True)

class EinvoiceCatalog52(models.Model):
    _name = "einvoice.catalog.52"
    _description = 'Codigos de Leyendas'
    _inherit = 'einvoice.catalog.tmpl'

    code = fields.Char(string='Code', size=12, index=True, required=True)

class EinvoiceCatalog53(models.Model):
    _name = "einvoice.catalog.53"
    _description = 'Codigos de Cargos o Descuentos'
    _inherit = 'einvoice.catalog.tmpl'

    code = fields.Char(string='Code', size=12, index=True, required=True)

class EinvoiceCatalog54(models.Model):
    _name = "einvoice.catalog.54"
    _description = 'Codigos de Bienes y Servicio Sujetos a Detraccion'
    _inherit = 'einvoice.catalog.tmpl'

    code = fields.Char(string='Code', size=12, index=True, required=True)

class EinvoiceCatalog55(models.Model):
    _name = "einvoice.catalog.55"
    _description = 'Codigo de identificacion del Item'
    _inherit = 'einvoice.catalog.tmpl'

    code = fields.Char(string='Code', size=12, index=True, required=True)

class EinvoiceCatalog56(models.Model):
    _name = "einvoice.catalog.56"
    _description = 'Codigo de Tipo de Servicio Publico'
    _inherit = 'einvoice.catalog.tmpl'

    code = fields.Char(string='Code', size=12, index=True, required=True)

class EinvoiceCatalog57(models.Model):
    _name = "einvoice.catalog.57"
    _description = 'Codigo de Tipo de Servicio Publicos-Telecomunicaciones'
    _inherit = 'einvoice.catalog.tmpl'

    code = fields.Char(string='Code', size=12, index=True, required=True)
    
class EinvoiceCatalog58(models.Model):
    _name = "einvoice.catalog.58"
    _description = 'Codigo de Tipo de Medidor-Recibo de Luz'
    _inherit = 'einvoice.catalog.tmpl'

    code = fields.Char(string='Code', size=12, index=True, required=True)