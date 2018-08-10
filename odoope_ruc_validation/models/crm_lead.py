from odoo import models,fields,api
from odoo.exceptions import Warning
import requests

def get_data_doc_number(tipo_doc, numero_doc, format='json'):
    user, password = 'demorest', 'demo1234'
    url = 'http://py-devs.com/api'
    url = '%s/%s/%s' % (url, tipo_doc, str(numero_doc))
    res = {'error': True, 'message': None, 'data': {}}
    try:
        response = requests.get(url, auth=(user, password))
    except requests.exceptions.ConnectionError as e:
        res['message'] = 'Error en la conexion'
        return res

    if response.status_code == 200:
        res['error'] = False
        res['data'] = response.json()
    else:
        try:
            res['message'] = response.json()['detail']
        except Exception as e:
            res['error'] = True
    return res
class CrmLead(models.Model):
    _name = "crm.lead"
    _inherit = "crm.lead"
    catalog_06_id = fields.Many2one('einvoice.catalog.06',string="Tipo Doc")
    vat = fields.Char("Ingrese Numero")
    state_id = fields.Many2one('res.country.state', 'Departamento')
    province_id = fields.Many2one('res.country.state', 'Provincia')
    district_id = fields.Many2one('res.country.state', 'Distrito')
    
    
    @api.onchange('catalog_06_id','vat')    
    def vat_change(self):
        self.update_document()

    @api.onchange('district_id')
    def onchange_district(self):
        if self.district_id:
            state = self.district_id.code
            self.zip = state
            
    @api.one
    def update_document(self):
    
        if not self.vat:
            return False
        if self.catalog_06_id and self.catalog_06_id.code == '1':
           #Valida DNI
            if self.vat and len(self.vat) != 8:
                raise Warning('El Dni debe tener 8 caracteres')
            else:
                d = get_data_doc_number(
                    'dni', self.vat, format='json')
                if not d['error']:
                    d = d['data']
                    self.contact_name = '%s %s %s' % (d['nombres'],
                                               d['ape_paterno'],
                                               d['ape_materno'])

        elif self.catalog_06_id and self.catalog_06_id.code == '6':
            # Valida RUC
            if self.vat and len(self.vat) != 11:
                raise Warning('El Ruc debe tener 11 caracteres')
            else:
                d = get_data_doc_number(
                    'ruc', self.vat, format='json')
                if d['error']:
                    return True
                d = d['data']
                print(d)
                #~ Busca el distrito
                ditrict_obj = self.env['res.country.state']
                prov_ids = ditrict_obj.search([('name', '=', d['provincia']),
                                               ('province_id', '=', False),
                                               ('state_id', '!=', False)])
                dist_id = ditrict_obj.search([('name', '=', d['distrito']),
                                              ('province_id', '!=', False),
                                              ('state_id', '!=', False),
                                              ('province_id', 'in', [x.id for x in prov_ids])], limit=1)
                if dist_id:
                    self.district_id = dist_id.id
                    self.province_id = dist_id.province_id.id
                    self.state_id = dist_id.state_id.id
                    self.country_id = dist_id.country_id.id
                        
                # Si es HABIDO, caso contrario es NO HABIDO
                tstate = d['condicion_contribuyente']
                if tstate == 'HABIDO':
                    tstate = 'habido'
                else:
                    tstate = 'nhabido'
                self.state = tstate
                            
                self.partner_name = d['nombre_comercial'] != '-' and d['nombre_comercial'] or d['nombre']
                self.registration_name = d['nombre']
                self.street = d['domicilio_fiscal']
                self.vat_subjected = True
                self.is_company = True
        else:
            True
