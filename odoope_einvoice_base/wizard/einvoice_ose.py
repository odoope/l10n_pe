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

from odoo import tools
from odoo import api, fields, models, _
from odoo.exceptions import UserError, ValidationError

class EinvoiceOseInstall(models.TransientModel):
    _name = 'einvoice.ose.install'
    _description = 'Install E-invoice by OSE'
    
    @api.model
    def _get_message(self):
        content_html = _('''
                <section class="jumbotron text-center bg-primary" style="padding: 4% 0% 4% 0%;top: 0;bottom: 0;right: 0;left: 0;width: 100%;height: 100%;background-image: linear-gradient(#875A7B, #62495B);">
                    <div class="container pb32 pt32" >
                        <h1 style="color:#FFFFFF" class="jumbotron-heading">{company}</h1>
                        <p class="lead text-muted" style="margin-bottom: 30px">
                            Obtenga el módulo Odoo para enviar sus comprobantes electrónicos a través de una OSE. 
                            </br>Fácil, económico y seguro.
                        </p>
                        <a style="text-align: center; background: #00A09D;width: 293px;padding: 12px;color: #fff !important;opacity: 1 !important;font-weight: 600;font-size: 18px; border-radius: 5px; margin: 15px 0 30px 0; -webkit-box-shadow: 0 10px 90px rgba(0, 0, 0, 0.08); box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08); color: #fff !important;" href="http://www.odoo.com/apps/modules/12.0/odoope_einvoice_ose/" target="_blank"><i class="fa fa-download" style="margin: 0px 8px"></i> Descarga
                                conexi&oacute;n a PSE/OSE</a>
                    </div>
                </section>
                <div class="container">
                    <div class="row">
                        <div class="col">
                            <div class="card mb-3">
                                <div class="card-header">
                                    <i class="fa fa-database"/> Factura electrónica vía PSE/OSE
                                </div>
                                <div class="card-body">
                                    <ul class="fa-ul">
                                        <li><span class="fa-li"><i class="fa fa-check-square"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Activación de cuenta en 24 horas.
                                        </li>
                                        <li><span class="fa-li"><i class="fa fa-check-square"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Certificación digital incluído</li>
                                        <li><span class="fa-li"><i class="fa fa-check-square"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Facturas, Boletas de Venta, Notas de Crédito, Débito y Anulaciones. </li>
                                        <li><span class="fa-li"><i class="fa fa-check-square"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Personalización con propio LOGOTIPO.</li>
                                        <li><span class="fa-li"><i class="fa fa-check-square"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Capacitación de uso</li>
                                        <li><span class="fa-li"><i class="fa fa-check-square"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Soporte por sistemas de Tickets y email.</li>
                                    </ul>
                                </div>
                            </div>
                        </div>
                        <div class="col">
                            <div class="card mb-3">
                                <div class="card-header">
                                    <i class="fa fa-gear"/>
                                    Integración con Odoo
                                </div>
                                <div class="card-body">
                                    <ul class="fa-ul">
                                        <li><span class="fa-li"><i class="fa fa-check"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Envía los comprobantes en tiempo real.
                                        </li>
                                        <li><span class="fa-li"><i class="fa fa-check"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Envío automático diario</li>
                                        <li><span class="fa-li"><i class="fa fa-check"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Consulta estado en SUNAT. </li>
                                        <li><span class="fa-li"><i class="fa fa-check"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Envía el comprobante por correo electrónico al cliente.</li>
                                        <li><span class="fa-li"><i class="fa fa-check"
                                                    style="font-size: 16px; color: #00A09D; margin-right: 22px;"></i></span>Disponible para Odoo v12</li>
                                    </ul>
                                    <div
                                        style="display: -moz-flex; display: -ms-flex; display: -o-flex; display: -webkit-box; display: -ms-flexbox; display: flex; -ms-flex-preferred-size: 1; flex-basis: 1;margin-top: 15px;">
                                        <div>
                                            <a
                                                style="border: 1px solid #ddd; display: -webkit-box; display: -ms-flexbox; display: flex; -webkit-box-align: center; -ms-flex-align: center; align-items: center; padding: 10px 15px;border-radius: 30px 30px 30px 0; -webkit-box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1); -webkit-box-pack: center; -ms-flex-pack: center; justify-content: center; margin-right: 20px;">
                                                <i class="fa fa-users"
                                                    style="display: inline-block; color: #47425d; font-size: 20px; margin-right: 15px;"></i>
                                                <p class="mb-0"
                                                    style="font-size: 12px; line-height: 1; -webkit-transition-duration: 500ms; -o-transition-duration: 500ms; transition-duration: 500ms;">
                                                    <span style="font-size: 10px; display: block;">compatible con</span> Odoo Community</p>
                                            </a>
                                        </div>
                                        <div>
                                            <a
                                                style="border: 1px solid #ddd; display: -webkit-box; display: -ms-flexbox; display: flex; -webkit-box-align: center; -ms-flex-align: center; align-items: center; padding: 10px 15px;border-radius: 30px 30px 30px 0; -webkit-box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1); box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1); -webkit-box-pack: center; -ms-flex-pack: center; justify-content: center; margin-right: 20px; background-color: #875A7B; color: #ffffff">
                                                <i class="fa fa-rocket"
                                                    style="display: inline-block; color: #ffffff; font-size: 20px; margin-right: 15px;"></i>
                                                <p class="mb-0"
                                                    style="font-size: 12px; line-height: 1; -webkit-transition-duration: 500ms; -o-transition-duration: 500ms; transition-duration: 500ms;">
                                                    <span style="font-size: 10px; display: block;">compatible con</span> Odoo Enterprise
                                                </p>
                                            </a>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                ''')
        html = tools.ustr(content_html).format(
                company = self.env.user.company_id.name,
                )
        return html

    message = fields.Html(string='Message', default=_get_message)
    