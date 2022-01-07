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

from odoo import _, api, fields, models
import requests
import json
from zipfile import ZipFile
from bs4 import BeautifulSoup
from io import BytesIO
from odoo.exceptions import Warning, UserError
from odoo.addons.iap.tools import iap_tools
class ResPartner(models.Model):
    _inherit = 'res.partner'

    def _default_country(self):
        return self.env.company.country_id.id

    country_id = fields.Many2one(default=_default_country)
    commercial_name = fields.Char(string="Commercial Name")
    state = fields.Selection([('habido','Habido'),('nhabido','No Habido')], string="State")
    alert_warning_vat= fields.Boolean(string="Alert warning vat", default=False)

    @api.onchange('vat','l10n_latam_identification_type_id')
    def onchange_vat(self):
        res = {}
        self.name = False
        self.commercial_name = False
        self.street = False
        if self.vat: 
            if self.l10n_latam_identification_type_id.l10n_pe_vat_code == '6':
                if len(self.vat) != 11 :
                    res['warning'] = {'title': _('Warning'), 'message': _('The Ruc must be 11 characters long.')}
                else:
                    company = self.env['res.company'].browse(self.env.company.id) 
                    if company.l10n_pe_ruc_validation == True:
                        self.get_data_ruc()
            elif self.l10n_latam_identification_type_id.l10n_pe_vat_code == '1':
                if len(self.vat) != 8 :
                    res['warning'] = {'title': _('Warning'), 'message': _('The Dni must be 8 characters long.')}
                else:
                    company = self.env['res.company'].browse(self.env.company.id)
                    if company.l10n_pe_dni_validation == True:
                        self.get_data_dni()
        if res:
            return res

    def get_data_ruc(self):
        result = self.l10n_pe_ruc_connection(self.vat)
        if result:
            self.alert_warning_vat = False
            self.company_type = 'company'
            self.name = str(result['business_name']).strip()
            self.commercial_name = str(result['commercial_name'] or result['business_name']).strip()
            self.street = str(result['residence']).strip()
            if result['contributing_condition'] == 'HABIDO':
                self.state = 'habido'
            else:
                self.state = 'nhabido'
            if result['value']:
                self.l10n_pe_district = result['value']['district_id']
                self.city_id = result['value']['city_id'] 
                self.state_id = result['value']['state_id'] 
                # self.country_id = result['value']['country_id']
    def get_data_dni(self):
        result = self.l10n_pe_dni_connection(self.vat)
        if result:
            self.alert_warning_vat = False
            self.name = str(result['nombre'] or '').strip()
            self.company_type = 'person'
    
    def fetch_ruc_data(self, vat_number):
        data = {}
        self.ensure_one()
        user_token = self.env['iap.account'].get('validation_ruc')
        company = self.env.company
        params = {
            'account_token': user_token.account_token,
            'doc_number': vat_number,
            'company_name': company.name,
            'phone': company.phone,
            'email': company.email,
            'cover_image': company.logo,
            'number': company.vat
        }
        service_endpoint = 'http://localhost:8069'
        result = iap_tools.iap_jsonrpc(service_endpoint + '/get_info_data', params=params)
        if result.get('status') == 'found' and len(vat_number) != 8:
            data = self.ruc_connection(result)
        if result.get('status') == 'found' and len(vat_number) != 11:
            data = self.dni_connection(result)
        return data       
        
    @api.model
    def ruc_connection(self, result):
        data = {}
        try:
            data['ruc'] = result.get('ruc')
            data['business_name'] = result.get('nombre_o_razon_social')
            data['estado'] = result.get('estado_del_contribuyente')
            data['contributing_condition'] = result.get('condicion_de_domicilio')
            data['commercial_name'] = result.get('nombre_o_razon_social')
            provincia = result.get('provincia').title()
            distrito = result.get('distrito').title()
            prov_ids = self.env['res.city'].search([('name', '=', provincia),('state_id','!=',False)])
            dist_id = self.env['l10n_pe.res.city.district'].search([('name', '=',distrito ),('city_id', 'in', [x.id for x in prov_ids])], limit=1)
            dist_short_id = self.env['l10n_pe.res.city.district'].search([('name', '=', result.get('distrito'))], limit=1)
            if dist_id:
                l10n_pe_district = dist_id
            else:
                l10n_pe_district = dist_short_id

            vals = {}
            if l10n_pe_district:
                vals['district_id'] = l10n_pe_district.id
                vals['city_id'] = l10n_pe_district.city_id.id
                vals['state_id'] = l10n_pe_district.city_id.state_id.id
                vals['country_id'] = l10n_pe_district.city_id.state_id.country_id.id
            data['value'] = vals
            data['residence']  = result.get('direccion')
        except Exception:
            self.alert_warning_vat = True
            data = False
        return data


    @api.model     
    def l10n_pe_ruc_connection(self, vat_number):
        data = {}
        if self.env.company.l10n_pe_api_ruc_connection == 'consul_ruc_api':  
            data = self.fetch_ruc_data(vat_number)
        return data
    
    @api.model
    def dni_connection(self, result):
        data = {}
        try:
            name = result.get('nombre_completo')
            data['nombre'] = name
        except Exception:
            self.alert_warning_vat = True
            data = False
        return data

    @api.model     
    def l10n_pe_dni_connection(self, vat_number):
        data = {}
        if self.env.company.l10n_pe_api_dni_connection == 'consul_dni_api':
            data = self.fetch_ruc_data(vat_number)
        return data   

    @api.onchange('l10n_pe_district')
    def _onchange_l10n_pe_district(self):
        if self.l10n_pe_district and self.l10n_pe_district.city_id:
            self.city_id = self.l10n_pe_district.city_id

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id and self.city_id.state_id:
            self.state_id = self.city_id.state_id
        res = {}
        res['domain'] = {}
        res['domain']['l10n_pe_district'] = []
        if self.city_id:
            res['domain']['l10n_pe_district'] += [('city_id','=',self.city_id.id)]
        return res

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id and self.state_id.country_id:
            self.country_id = self.state_id.country_id
        res = {}
        res['domain'] = {}
        res['domain']['city_id'] = []
        if self.state_id:
            res['domain']['city_id'] += [('state_id','=',self.state_id.id)]
        return res
