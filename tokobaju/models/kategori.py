from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _kategori(models.Model):
    _name = 'tokobaju.kategori'
    _description = 'class untuk data kategori'

    name = fields.Char('Nama Kategori', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})

    id_kategori = fields.Char('ID Kategori', size=64, required=True, index=True, readonly=True, default='new', states={})

    produk_ids = fields.One2many('tokobaju.produk', 'kategori_id', string='ID Produk')

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
        seq = self.env['ir.sequence'].search([("code", "=", "tokobaju.kategori")])
        if not seq:
            raise UserError(_("tokobaju.kategori sequence not found, please create tokobaju.kategori sequence"))
        for val in vals_list:
            val['id_kategori'] = seq.next_by_id()
        return super(_kategori, self).create(vals_list)