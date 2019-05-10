from odoo import api, fields, models

class ProductTemplate(models.Model):
        _name = 'product.template'
        _inherit = 'product.template'

        igv_type = fields.Many2one("einvoice.catalog.07", string='IGV type')
        product_code_sunat = fields.Many2one("einvoice.catalog.25", string='Product code SUNAT')
