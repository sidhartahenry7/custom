from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _produk(models.Model):
    _name = 'tokobaju.produk'
    _description = 'class untuk data produk'

    name = fields.Char('Nama Produk', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    id_produk = fields.Char('ID Produk', size=64, required=True, index=True, readonly=True, default='new',
                              states={})
    ukuran = fields.Char('Size', size=64, required=True, index=True, readonly=True,
                          states={'draft': [('readonly', False)]})
    warna = fields.Char('Color', size=64, required=True, index=True, readonly=True,
                         states={'draft': [('readonly', False)]})
    quantity = fields.Integer('Quantity', size=64, required=True, index=True, readonly=True,
                              states={'draft': [('readonly', False)]})
    harga = fields.Integer('Harga', size=64, required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})

    kategori_id = fields.Many2one('tokobaju.kategori', string='Kategori', readonly=True, ondelete="cascade",
                                    states={'draft': [('readonly', False)]},
                                    domain="[('state', '=', 'confirmed')]")

    brand_id = fields.Many2one('tokobaju.brand', string='Brand', readonly=True, ondelete="cascade",
                                  states={'draft': [('readonly', False)]},
                                  domain="[('state', '=', 'confirmed')]")

    detail_transaksi_ids = fields.One2many('tokobaju.detail_transaksi', 'produk_id', string="Detail Transaksi")
    sisa_quantity = fields.Integer("Quantity Saat Ini", compute="_compute_quantity", store=True, default=0)

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('cek_harga', 'CHECK (harga>=0)', 'Harga tidak boleh minus'),
                        ('cek_quantity', 'CHECK (quantity>=0)', 'Quantity produk tidak boleh minus')]

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "tokobaju.produk")])
        if not seq:
            raise UserError(_("tokobaju.produk sequence not found, please create tokobaju.produk sequence"))
        for val in vals_list:
            val['id_produk'] = seq.next_by_id()
        return super(_produk, self).create(vals_list)

    @api.depends('quantity', 'detail_transaksi_ids', 'detail_transaksi_ids.quantity')
    def _compute_quantity(self):
        for _produk in self.filtered(lambda i: i.state == 'confirmed'):
            val = {'sisa_quantity': _produk.quantity}
            for rec in _produk.detail_transaksi_ids.filtered(lambda s: s.state == 'confirmed'):
                val['sisa_quantity'] -= rec.quantity
            _produk.update(val)