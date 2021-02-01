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
from odoo.addons.odoope_ruc_validation.models import sunatconstants
import requests
from bs4 import BeautifulSoup
from odoo.exceptions import Warning, UserError
class ResPartner(models.Model):
    _inherit = 'res.partner'

    commercial_name = fields.Char(string="Commercial Name")
    state = fields.Selection([('habido','Habido'),('nhabido','No Habido')],'State')
    alert_warning_vat= fields.Boolean(string="Alert warning vat", default=False)

    @api.onchange('vat','l10n_latam_identification_type_id')
    def onchange_vat(self):
        res = {}
        self.name = False
        self.commercial_name =False
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
        result = self.sunat_connection(self.vat)
        if result:
            self.alert_warning_vat=False
            self.company_type = 'company'
            self.name = result['business_name']
            self.commercial_name =result['commercial_name'] or result['business_name']
            self.street = result['residence']
            if result['contributing_condition'] == 'HABIDO':
                self.state = 'habido'
            else:
                self.state = 'nhabido'
            if result['value']:
                self.l10n_pe_district = result['value']['district_id']
                self.city_id = result['value']['city_id'] 
                self.state_id = result['value']['state_id'] 
                self.country_id = result['value']['country_id']
    def get_data_dni(self):
        result = self.reniec_connection(self.vat)
        if result:
            self.alert_warning_vat=False
            self.name= result['nombre'] or ''
            self.company_type = 'person'

    @api.model
    def sunat_connection(self,ruc):
        session = requests.Session()
        url_sunat = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36' 
        data = {}
        try:
            captcha_data = session.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/captcha?accion=random', headers=headers).text
            data_ruc = {'accion':'consPorRuc','nroRuc':ruc,'numRnd':str(captcha_data)}
            html_doc = session.post(url=url_sunat,data=data_ruc,headers=headers)
            html_info = BeautifulSoup(html_doc.content, 'html.parser')
            table_info = html_info.find_all('tr')
            sunat_cons = None
            if ruc[0] == '1':
                sunat_cons = sunatconstants.PersonaNaturalConstant    
                
            elif ruc[0] == '2':
                sunat_cons = sunatconstants.PersonaJuridicaConstant

            number_ruc = (table_info[sunat_cons.number_ruc.value].find_all("td"))[1].contents[0]
            data['ruc'] = number_ruc.split('-')[0]
            data['business_name'] = number_ruc.split('-')[1]
            data['type_of_taxpayer']= (table_info[sunat_cons.type_of_taxpayer.value].find_all("td"))[1].contents[0]
            data['estado'] = (table_info[sunat_cons.taxpayer_state.value].find_all("td"))[1].contents[0]
            data['contributing_condition'] = (table_info[sunat_cons.contributing_condition.value].find_all("td"))[1].contents[0].replace('\r', '') \
            .replace('\n', '').strip()
            data['commercial_name'] = (table_info[sunat_cons.commercial_name.value].find_all("td"))[1].contents[0].replace('-','').strip()    

            residence = (table_info[sunat_cons.tax_residence.value].find_all("td"))[1].contents[0]
            district = (" ".join(residence.split("-")[-1].split())).title()
            province = (" ".join(residence.split("-")[-2].split())).title()
            address = " ".join(residence.split())
            address = " ".join(residence.split("-")[0:-2])	
            prov_ids = self.env['res.city'].search([('name', '=', province),('state_id','!=',False)])
            dist_id = self.env['l10n_pe.res.city.district'].search([('name', '=', district),('city_id', 'in', [x.id for x in prov_ids])], limit=1)
            dist_short_id = self.env['l10n_pe.res.city.district'].search([('name', '=', district)], limit=1)
            if dist_id:
                l10n_pe_district = dist_id
            else:
                l10n_pe_district = dist_short_id  
    
            vals={}
            if l10n_pe_district:
                vals['district_id'] = l10n_pe_district.id
                vals['city_id'] = l10n_pe_district.city_id.id
                vals['state_id'] = l10n_pe_district.city_id.state_id.id
                vals['country_id'] = l10n_pe_district.city_id.state_id.country_id.id
            data['value'] = vals    
            data['residence']  = address

        except Exception:
            self.alert_warning_vat=True
            data = False                    
        return data
    
    @api.model
    def reniec_connection(self,dni):
        session = requests.Session()
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        url_reniec = 'https://api.reniec.cloud/dni/{dni}'
        data = {}
        try:
            result= session.get(url=url_reniec.format(dni=dni),verify = False,headers=headers).json()
            data['nombre'] = (result['nombres'] + " " +result['apellido_paterno'] + " " + result['apellido_materno'])
        except Exception :
            self.alert_warning_vat=True
            data = False 
        return data 

       
    @api.onchange('l10n_pe_district')
    def _onchange_l10n_pe_district(self):
        if self.l10n_pe_district and self.l10n_pe_district.city_id:
            self.city_id = self.l10n_pe_district.city_id

    @api.onchange('city_id')
    def _onchange_city_id(self):
        if self.city_id and self.city_id.state_id:
            self.state_id = self.city_id.state_id
    
    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id and self.state_id.country_id:
            self.country_id = self.state_id.country_id
