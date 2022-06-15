from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _brand(models.Model):
    _name = 'tokobaju.brand'
    _description = 'class untuk data brand'

    name = fields.Char('Nama Brand', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})

    id_brand = fields.Char('ID Brand', size=64, required=True, index=True, readonly=True, default='new',
                              states={})

    perusahaan_id = fields.Many2one('res.partner', 'Perusahaan', index=True, readonly=True,
                                    states={'draft': [('readonly', False)]})

    produk_ids = fields.One2many('tokobaju.produk', 'brand_id', string='ID Produk')

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "tokobaju.brand")])
        if not seq:
            raise UserError(_("tokobaju.brand sequence not found, please create tokobaju.brand sequence"))
        for val in vals_list:
            val['id_brand'] = seq.next_by_id()
        return super(_brand, self).create(vals_list)