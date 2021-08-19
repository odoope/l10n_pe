# -*- coding: utf-8 -*-
from odoo import http, _
from odoo.http import request
from odoo.addons.iap.tools import iap_tools
from odoo.exceptions import UserError


class Main(http.Controller):
    @http.route('/get_info_data', type='json', auth="public")
    def get_info_data(self, account_token, doc_number, company_name, phone, email, cover_image, number):
        service_key = request.env['ir.config_parameter'].sudo().get_param('iap.validation_service_key', False)
        if not service_key:
            return {
                'status': 'service is not active'
            }
        credits_to_reserve = 1
        data = {}
        with iap_tools.iap_charge(request.env, service_key, account_token, credits_to_reserve):
            data = request.env['validation.info'].sudo()._partners_data_by_doc(doc_number, company_name, phone, email, cover_image, number)
            if data['status'] == 'not found':
                raise UserError(_('The RUC or DNI number to consult does not exist. Please try again.'))
        return data