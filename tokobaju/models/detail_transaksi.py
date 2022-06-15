from odoo import models, fields, api, _

class _detail_transaksi(models.Model):
    _name = 'tokobaju.detail_transaksi'
    _description = 'class untuk data detail transaksi'

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    transaksi_id = fields.Many2one('tokobaju.transaksi', string='Transaksi', readonly=True, ondelete="cascade",
                                    states={'draft': [('readonly', False)]},
                                    domain="[('state', '=', 'confirmed')]")

    produk_id = fields.Many2one('tokobaju.produk', string='Nama Produk', readonly=True, ondelete='cascade',
                                states={'draft': [('readonly', False)]},
                                domain="[('state', '=', 'confirmed')]")

    diskon_id = fields.Many2one('tokobaju.diskon', string='Diskon', readonly=True, ondelete="cascade",
                                   states={'draft': [('readonly', False)]},
                                   domain="[('state', '=', 'confirmed')]")

    ukuran = fields.Char("Size", related='produk_id.ukuran')

    harga = fields.Integer("Harga", related='produk_id.harga')

    quantity = fields.Integer(string="Quantity", recursive=True)

    diskon = fields.Float("Discount Event (10%)", related='diskon_id.jumlah_diskon')

    diskon2 = fields.Float(string="Diskon (%)", digits='Discount', default=0.0)

    sub_total_item = fields.Integer('Sub Total', compute="_compute_sub_total_item", store=True, recursive=True)

    # tanggal_hari_ini = fields.Date('Tanggal Hari Ini', default=fields.Date.context_today, readonly=True)
    #
    # _sql_constraints = [('cek_periode_berakhir', 'CHECK (diskon_id.tanggal_berakhir>=tanggal_hari ini)', 'Periode diskon telah lewat'),
    #                     ('cek_periode_mulai', 'CHECK (diskon_id.tanggal_mulai<=tanggal_hari ini)', 'Periode diskon belum dimulai')]

    @api.depends('quantity', 'diskon_id', 'diskon2')
    def _compute_sub_total_item(self):
        for _detail_transaksi in self:
            val = {
                "sub_total_item": 0,
            }
            for rec in self:
                val["sub_total_item"] += rec.harga * (1 - (rec.diskon2 or 0.0) / 100.0) * rec.quantity
                val["sub_total_item"] = val["sub_total_item"] * (1 - (rec.diskon or 0.0) / 100.0)
            _detail_transaksi.update(val)

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'