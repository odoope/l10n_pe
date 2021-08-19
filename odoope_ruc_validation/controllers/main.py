from odoo.http import request, route, Controller


class BannerController(Controller):
    @route('/credit_status', type='json', auth='user')
    def credit_status(self):
        credit = request.env['iap.account'].get_credits('validation_ruc')
        credit_url = request.env['iap.account'].get_credits_url('validation_ruc')
        return {
            'html': request.env['ir.ui.view']._render_template('odoope_ruc_validation.credit_banner', {'credit': credit, 'credit_url': credit_url})
        }