# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import Warning, UserError
import requests
import json

class ValidationInfo(models.Model):
    _name = 'validation.info'
    
    name = fields.Char('Company Name', required=True)
    validation_ips = fields.One2many('validation.info.lines', 'validation_ip', string='Validation Info Lines')
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    cover_image = fields.Binary('CompanyCover')
    number = fields.Char('Number')

    @api.model
    def _partners_data_by_doc(self, doc_number, company_name, phone, email, cover_image, number):
        headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36","Content-Type": "application/json;chartset=utf-8"}
        values_params = []
        try:
            url_ruc_api = 'https://ruc.com.pe/api/v1/consultas'
            if len(doc_number) != 11:
                values_params = {"dni":doc_number,"token": "fb187df3-fed7-4b16-8d72-72113718003b-23e4cbf3-49c7-4514-bc16-235e7c27c6cd"}
            if len(doc_number) != 8:
                values_params = {"ruc":doc_number,"token": "fb187df3-fed7-4b16-8d72-72113718003b-23e4cbf3-49c7-4514-bc16-235e7c27c6cd"}
            response = requests.post(url=url_ruc_api,json=values_params,headers=headers,timeout=(15)).content
            result = json.loads(response)
            if result.get('success', False):
                result['status'] = 'found'
                self._create_data_info(doc_number, company_name, phone, email, cover_image, number)
                return result
            raise UserError('Result success False ..')
        except Exception:
            return {
                'status': 'not found',
            }
            
    @api.model
    def _create_data_info(self, doc_number, company_name, phone, email, cover_image, number):
        company = self.search([('number', '=', number)], limit=1)
        values = {"number_consult":doc_number}
        if company:
            return company.write({
                    'name': company_name,
                    'phone': phone,
                    'email': email,
                    'cover_image': cover_image,
                    'validation_ips': [(0, 0, values)]
                })
        else:
            return self.create({
                    'name': company_name,
                    'phone': phone,
                    'email': email,
                    'cover_image': cover_image,
                    'number': number,
                    'validation_ips': [(0, 0, values)]
                })
            
class RucValidationInfoLine(models.Model):
    _name = 'validation.info.lines'
    
    validation_ip = fields.Many2one('validation.info', string='Info Lines')
    number_consult = fields.Char('Nº Consult')