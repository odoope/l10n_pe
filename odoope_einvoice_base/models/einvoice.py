# -*- coding: utf-8 -*-
from odoo import models, fields, api

class einvoice_catalog_01(models.Model):
    _name = "einvoice.catalog.01"
    _description = 'Codigo de Tipo de documento'

    code = fields.Char(string='Code', size=4, index=True, required=True)
    name = fields.Char(string='Description', size=128, index=True, required=True)
    label = fields.Char(string='Label to print', size=256)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result

class einvoice_catalog_05(models.Model):
    _name = "einvoice.catalog.05"
    _description = 'Codigo de Tipo de tributo'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)
    un_5153 = fields.Char(string='UN/ECE 5153-Duty or tax or fee type name code', size=5)
    un_5103 = fields.Char(string='UN/ECE 5305-Duty or tax or fee category code', size=1)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result

class einvoice_catalog_06(models.Model):
    _name = "einvoice.catalog.06"
    _description = 'Tipo de documento de Identidad'

    code = fields.Char(string='Code', size=4, index=True, required=True)
    name = fields.Char(string='Description', size=128, index=True, required=True)
    default = fields.Char(string='Valor por defecto', size=128)
    
    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result
        
class einvoice_catalog_07(models.Model):
    _name = "einvoice.catalog.07"
    _description = 'Codigos de Tipo de Afectacion del IGV'

    code = fields.Char(string='Code', size=4, index=True, required=True)
    name = fields.Char(string='Description', size=128, index=True, required=True)
    no_onerosa = fields.Boolean(string='No onerosa')
    type = fields.Selection([('gravado','Gravado'),('exonerado','Exonerado'),('inafecto','Inafecto')],string='Tipo')
    
    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result

class einvoice_catalog_08(models.Model):
    _name = "einvoice.catalog.08"
    _description = 'Codigos de Tipo de Afectacion del IGV'

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

class einvoice_catalog_09(models.Model):
    _name = "einvoice.catalog.09"
    _description = 'Codigos de Tipo de Nota de Credito Electronica'

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

class einvoice_catalog_10(models.Model):
    _name = "einvoice.catalog.10"
    _description = 'Codigos de Tipo de Nota de Debito Electronica'

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


class einvoice_catalog_11(models.Model):
    _name = "einvoice.catalog.11"
    _description = 'Codigo de Tipo de Valor de Venta'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_12(models.Model):
    _name = "einvoice.catalog.12"
    _description = 'Codigos -Documentos Relacionados Tributarios'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_14(models.Model):
    _name = "einvoice.catalog.14"
    _description = 'Codigos - Otros Conceptos Tributarios'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_15(models.Model):
    _name = "einvoice.catalog.15"
    _description = 'Codigos-Elementos Adicionales en la Factura Electrónica '

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Valor', size=256, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_16(models.Model):
    _name = "einvoice.catalog.16"
    _description = 'Codigos - Tipo de Precio de Venta Unitario'

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

class einvoice_catalog_17(models.Model):
    _name = "einvoice.catalog.17"
    _description = 'Codigos -Tipo de Operacion'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result

class einvoice_catalog_18(models.Model):
    _name = "einvoice.catalog.18"
    _description = 'Codigos - Modalidad de  Traslado'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_19(models.Model):
    _name = "einvoice.catalog.19"
    _description = 'Codigos de Estado de Item'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_20(models.Model):
    _name = "einvoice.catalog.20"
    _description = 'Codigos - Motivo de Traslado'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result

class einvoice_catalog_21(models.Model):
    _name = "einvoice.catalog.21"
    _description = 'Codigos-Documentos Relacionados '

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_22(models.Model):
    _name = "einvoice.catalog.22"
    _description = 'Codigos- Regimenes de Percepcion'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)
    rate = fields.Char(string='Tasa', size=10, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_23(models.Model):
    _name = "einvoice.catalog.23"
    _description = 'Codigos- Regimenes de Retencion'

    code = fields.Char(string='Codigo', size=4, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)


    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_24(models.Model):
    _name = "einvoice.catalog.24"
    _description = 'Codigos- Recibo Electronico por Servicios Publicos'

    rate_code = fields.Char(string='Codigo tarifa', size=4, index=True, required=True)
    code = fields.Char(string='Codigo',  index=True, required=True)
    name = fields.Char(string='Servicio', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_25(models.Model):
    _name = "einvoice.catalog.25"
    _description = 'Codigos - Producto SUNAT'

    code = fields.Char(string='Code', size=12, index=True, required=True)
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
    
    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('code', '=ilike', name.split('-')[0] + '%'), ('name', operator, name)]
            if operator in expression.NEGATIVE_TERM_OPERATORS:
                domain = ['&', '!'] + domain[1:]
        ids = self._search(expression.AND([domain, args]), limit=limit, access_rights_uid=name_get_uid)
        return self.browse(ids).name_get()


class einvoice_catalog_51(models.Model):
    _name = "einvoice.catalog.51"
    _description = 'Codigo de  Tipo de Factura'

    code = fields.Char(string='Codigo', size=12, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_52(models.Model):
    _name = "einvoice.catalog.52"
    _description = 'Codigos de Leyendas'

    code = fields.Char(string='Codigo', size=12, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_53(models.Model):
    _name = "einvoice.catalog.53"
    _description = 'Codigos de Cargos o Descuentos'

    code = fields.Char(string='Codigo', size=12, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_54(models.Model):
    _name = "einvoice.catalog.54"
    _description = 'Codigos de Bienes y Servicio Sujetos a Detraccion'

    code = fields.Char(string='Codigo', size=12, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result



class einvoice_catalog_55(models.Model):
    _name = "einvoice.catalog.55"
    _description = 'Codigo de identificacion del Item'

    code = fields.Char(string='Codigo', size=12, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result



class einvoice_catalog_56(models.Model):
    _name = "einvoice.catalog.56"
    _description = 'Codigo de Tipo de Servicio Publico'

    code = fields.Char(string='Codigo', size=12, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result



class einvoice_catalog_57(models.Model):
    _name = "einvoice.catalog.57"
    _description = 'Codigo de Tipo de Servicio Publicos-Telecomunicaciones'

    code = fields.Char(string='Codigo', size=12, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result


class einvoice_catalog_58(models.Model):
    _name = "einvoice.catalog.58"
    _description = 'Codigo de Tipo de Medidor-Recibo de Luz'

    code = fields.Char(string='Codigo', size=12, index=True, required=True)
    name = fields.Char(string='Descripcion', size=128, index=True, required=True)

    @api.multi
    @api.depends('code', 'name')
    def name_get(self):
        result = []
        for table in self:
            l_name = table.code and table.code + ' - ' or ''
            l_name +=  table.name
            result.append((table.id, l_name ))
        return result
