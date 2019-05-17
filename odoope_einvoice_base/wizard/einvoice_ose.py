# -*- coding: utf-8 -*-
from odoo import tools
from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError

class EinvoiceOseInstall(models.TransientModel):
    _name = 'einvoice.ose.install'
    _description = 'Install E-invoice by OSE'
    
    @api.model
    def _get_message(self):
        content_html = '''
                <section class="jumbotron text-center bg-primary">
                    <div class="container pb32 pt32">
                        <h1 class="jumbotron-heading">{company}</h1>
                        <p class="lead text-muted">
                            Get full book information with cover image just by the ISBN number.
                        </p>
                        <span class="badge badge-warning" style="font-size: 30px;">
                            20% Off
                        </span>
                    </div>
                </section>
                <div class="container">
                    <div class="row">
                        <div class="col">
                            <div class="card mb-3">
                                <div class="card-header">
                                    <i class="fa fa-database"/> Large books database
                                </div>
                                <div class="card-body">
                                    <p class="card-text">
                                        We have largest book databse. It contains more
                                        then 2500000+ books.
                                    </p>
                                </div>
                            </div>
                        </div>
                        <div class="col">
                            <div class="card mb-3">
                                <div class="card-header">
                                    <i class="fa fa-image"/>
                                    With cover image
                                </div>
                                <div class="card-body">
                                    <p class="card-text">
                                        More then 95% of our books having high quality
                                        book cover images.
                                    </p>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
                '''
        html = tools.ustr(content_html).format(
                company = self.env.user.company_id.name,
                )
        return html

    message = fields.Html(string='Message', default=_get_message)
    