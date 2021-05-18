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

import json
from urllib.parse import urlencode
import requests
from odoo import _, api, fields, models
from odoo.addons.odoope_ruc_validation.models import sunatconstants
from odoo.exceptions import Warning,UserError
import urllib
from bs4 import BeautifulSoup as BS

class ResPartner(models.Model):
    _inherit = 'res.partner'

    registration_name = fields.Char('Registration Name', size=128, index=True, )
    catalog_06_id = fields.Many2one('einvoice.catalog.06','Tipo Doc.', index=True)
    state = fields.Selection([('habido','Habido'),('nhabido','No Habido')],'State')
    alert_warning_vat= fields.Boolean(string="Alert warning vat", default=False)

    @api.onchange('vat','catalog_06_id')
    def onchange_vat(self):
        res = {}
        self.name = False
        self.registration_name =False
        self.street = False
        if self.vat: 
            vat_isdigit = self.vat.isdigit()
            if self.catalog_06_id and self.catalog_06_id.code == '6':
                if vat_isdigit == False or len(self.vat)!=11:
                    res['warning'] = {'title': _('Warning'), 'message': _('The Ruc must be 11 characters long.')}
                else:
                    company = self.env.user.company_id
                    if company.l10n_pe_ruc_validation == True:
                        self.conexion_sunat()
            elif self.catalog_06_id and self.catalog_06_id.code == '1':
                if len(self.vat) != 8 :
                    res['warning'] = {'title': _('Warning'), 'message': _('The Dni must be 8 characters long.')}
                else:
                    company = self.env.user.company_id
                    if company.l10n_pe_dni_validation == True:
                        self.get_data_dni()
        if res:
            return res

    @api.one
    def conexion_sunat(self):
        result = self.l10n_pe_ruc_connection(self.vat)
        if result:
            self.alert_warning_vat=False
            self.company_type = 'company'
            self.name = str(result['razon_social']).strip()
            self.registration_name =str(result['nombre_comercial'] or result['razon_social']).strip() 
            self.street = result['domicilio']
            if result['condicion_contribuyente'] == 'HABIDO':
                self.state = 'habido'
            else:
                self.state = 'nhabido'
            if result['value']:
                self.district_id = result['value']['district_id']
                self.province_id = result['value']['province_id'] 
                self.state_id = result['value']['state_id'] 
                self.country_id = result['value']['country_id']
    def get_data_dni(self):
        result = self.l10n_pe_dni_connection(self.vat)
        if result:
            self.alert_warning_vat = False
            self.name = str(result['nombre'] or '').strip()
            self.company_type = 'person'

    @api.model
    def get_data_ruc(self,ruc):
        #  ====Session para las consultas ====
        session = requests.Session()
        # ====Link de Consultas ====           
        url_sunat = "https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias"
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        data = {}
        try:
            url_numRnd = session.get('https://e-consultaruc.sunat.gob.pe/cl-ti-itmrconsruc/jcrS00Alias?accion=consPorRazonSoc&razSoc=BVA%20FOODS', headers=headers,timeout=12).content
            html_content = BS(url_numRnd, 'html.parser')
            content_form = html_content.find_all('form')
            numRnd = content_form[0].find_all('input')[3].get('value')
            data_ruc = {'accion':'consPorRuc','nroRuc':ruc,'numRnd':numRnd,'actReturn':'1','modo':'1'}
            html_doc = session.post(url=url_sunat,data=data_ruc,headers=headers,timeout=(15,20))
            html_info = BS(html_doc.content, 'html.parser')
            div_info = html_info.find_all("div", {"class": "list-group"})
            div_p_info = div_info[0].find_all("p", {"class": "list-group-item-text"})
            div_h4_info = div_info[0].find_all("h4", {"class": "list-group-item-heading"})
            sunat_cons = None
            if ruc[0] == '1':
                sunat_cons = sunatconstants.PersonaNaturalConstant    
                
            elif ruc[0] == '2':
                sunat_cons = sunatconstants.PersonaJuridicaConstant
            # ====Agregar datos en el Diccionario ====
            number_ruc = (div_h4_info[sunat_cons.number_ruc.value].contents[0])
            data['ruc'] = number_ruc.split('-')[0]
            data['razon_social'] = number_ruc.split('-')[1]
            data['tipo_contribuyente']= (div_p_info[sunat_cons.type_of_taxpayer.value].contents[0])
            # ====Estado del Contribuyente====
            data['estado'] = (div_p_info[sunat_cons.taxpayer_state.value].contents[0])
            data['condicion_contribuyente'] = (div_p_info[sunat_cons.contributing_condition.value].contents[0]).replace('\r', '') \
            .replace('\n', '').strip()
            data['nombre_comercial'] = (div_p_info[sunat_cons.commercial_name.value].contents[0]).replace('-','').strip()
            # ====Buscar Distrito====
            domicilio = (div_p_info[sunat_cons.tax_residence.value].contents[0])
            district = " ".join(domicilio.split("-")[-1].split()) 
            province = " ".join(domicilio.split("-")[-2].split())
            direccion = " ".join(domicilio.split())
            direccion = " ".join(domicilio.split("-")[0:-2])
            ditrict_obj = self.env['res.country.state']
            prov_ids = ditrict_obj.search([('name', '=', province),('province_id', '=', False),('state_id', '!=', False)])
            dist_id = ditrict_obj.search([('name', '=', district),
                                                ('province_id', '!=', False),
                                                ('state_id', '!=', False),
                                                ('province_id', 'in', [x.id for x in prov_ids])], limit=1)
            vals={}
            if dist_id:
                vals['district_id'] = dist_id.id
                vals['province_id'] = dist_id.province_id.id
                vals['state_id'] = dist_id.state_id.id
                vals['country_id'] = dist_id.country_id.id
            data['value']=vals    
            data['domicilio']  = direccion.strip()

        except Exception:
            self.alert_warning_vat=True
            data = False                
        return data
    
    @api.model     
    def l10n_pe_ruc_connection(self, ruc):
        data = {}
        if self.env.user.company_id.l10n_pe_api_ruc_connection == 'sunat':
            data = self.get_data_ruc(ruc)
        return data 
    
    @api.model
    def reniec_connection(self, dni):
        session = requests.Session()
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        url_reniec = 'https://api.reniec.cloud/dni/{dni}'
        data = {}
        try:
            response= session.get(url=url_reniec.format(dni=dni),verify = False,headers=headers).text
            values_response = response.replace('&Ntilde;','Ñ')
            result = json.loads(values_response)
            data['nombre'] = (result['nombres'] + " " +result['apellido_paterno'] + " " + result['apellido_materno'])
        except Exception:
            self.alert_warning_vat = True
            data = False 
        return data

    @api.model
    def jne_connection(self,dni):
        session = requests.Session()
        headers = requests.utils.default_headers()
        headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        headers['Content-Type'] = 'application/json;chartset=utf-8'
        headers['Requestverificationtoken'] = 'Dmfiv1Unnsv8I9EoXEzbyQExSD8Q1UY7viyyf_347vRCfO-1xGFvDddaxDAlvm0cZ8XgAKTaWclVFnnsGgoy4aLlBGB5m-E8rGw_ymEcCig1:eq4At-H2zqgXPrPnoiDGFZH0Fdx5a-1UiyVaR4nQlCvYZzAhzmvWxLwkUk6-yORYrBBxEnoG5sm-Hkiyc91so6-nHHxIeLee5p700KE47Cw1'
        url_reniec = 'https://aplicaciones007.jne.gob.pe/srop_publico/Consulta/api/AfiliadoApi/GetNombresCiudadano'
        dni_value = {"CODDNI":dni}
        data = {}
        try:
            response = session.post(url=url_reniec,json=dni_value,headers=headers,timeout=(15)).text
            values_response = response.replace('|',' ')
            result = json.loads(values_response)
            data['nombre'] = result['data']
        except Exception :
            self.alert_warning_vat = True
            data = False 
        return data 

    @api.model     
    def free_api_connection(self, dni):
        url = 'https://dni.optimizeperu.com/api/prod/persons/{dni}'.format(dni=dni)
        headers = {'authorization': 'token 48b5594ab9a37a8c3581e5e71ed89c7538a36f11'}
        data = {}
        try:
            r = requests.get(url, headers=headers,timeout=(15))
            result = r.json()
            name = result.get('first_name') +" "+ result.get('last_name') + " " + result.get('name')
            data['nombre'] = name
        except Exception :
            self.alert_warning_vat = True
            data = False 
        return data  

    @api.model     
    def facturacion_electronica_dni_connection(self, dni):
        url = 'https://www.facturacionelectronica.us/facturacion/controller/ws_consulta_rucdni_v2.php'
        params = {
            'usuario': '10447915125',
            'password': '985511933',
            'documento': 'DNI',
            'nro_documento': dni
        }
        data = {}
        try:
            r = requests.get(url, params, timeout=(15))
            result = r.json()
            name = result.get('result').get('Paterno') +" "+ result.get('result').get('Materno') + " " + result.get('result').get('Nombre')
            data['nombre'] = name
        except Exception :
            self.alert_warning_vat = True
            data = False 

        return data

    @api.model     
    def l10n_pe_dni_connection(self, dni):
        data = {}
        company = self.env.user.company_id
        if self.env.user.company_id.l10n_pe_api_dni_connection == 'jne':
            data = self.jne_connection(dni)
        elif company.l10n_pe_api_dni_connection == 'facturacion_electronica':
            data = self.facturacion_electronica_dni_connection(dni)
        elif company.l10n_pe_api_dni_connection == 'free_api':
            data = self.free_api_connection(dni)
        else:
            data = False   
        return data   

    @api.onchange('district_id')
    def _onchange_district_id(self):
        if self.district_id and self.district_id.province_id:
            self.province_id = self.district_id.province_id

    @api.onchange('province_id')
    def _onchange_province_id(self):
        if self.province_id and self.province_id.state_id:
            self.state_id = self.province_id.state_id
        res = {}
        res['domain'] = {}
        res['domain']['district_id'] = []
        if self.province_id:
            res['domain']['district_id'] += [('province_id','=',self.province_id.id)]
        return res

    @api.onchange('state_id')
    def _onchange_state_id(self):
        if self.state_id and self.state_id.country_id:
            self.country_id = self.state_id.country_id
        res = {}
        res['domain'] = {}
        res['domain']['province_id'] = []
        if self.state_id:
            res['domain']['province_id'] += [('state_id','=',self.state_id.id)]
        return res