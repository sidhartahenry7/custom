from odoo import models, fields, api, _

class wiz_transaksi(models.TransientModel):
    _name = 'wiz.tokobaju.transaksi'
    _description = 'class untuk menyimpan data transaksi dan detail transaksi'

    transaksi_id = fields.Many2one('tokobaju.transaksi', String='ID Transaksi')
    date = fields.Date(related='transaksi_id.date')

    detail_transaksi_ids = fields.One2many('wiz.tokobaju.detail_transaksi', 'wiz_header_id', string='Detail Transaksi')

    @api.model
    def default_get(self,fields_list):  # ini adalah common method, semacam constructor, akan dijalankan saat create object. Ini akan meng-overwrite default_get dari parent
        res = super(wiz_transaksi, self).default_get(fields_list)
        # res  merupakan dictionary beserta value yang akan diisi, yang sudah diproses di super class (untuk create record baru)
        res['transaksi_id'] = self.env.context['active_id']
        return res

    @api.onchange('transaksi_id')
    def onchange_transaksi_id(self):
        if not self.transaksi_id:
            return
        vals = []
        detail_transaksi_ids = self.env['wiz.tokobaju.detail_transaksi']
        for rec in self.transaksi_id.detail_transaksi_ids:
            detail_transaksi_ids += self.env['wiz.tokobaju.detail_transaksi'].new({
                'wiz_header_id': self.id,
                'produk_id': rec.produk_id.id,
                'ref_detail_transaksi_id': rec.id
            })
            # cara membuat record baru di m2m atau o2m
        self.detail_transaksi_ids = detail_transaksi_ids

    def action_confirm(self):
        for rec in self.detail_transaksi_ids:
            rec.ref_detail_transaksi_id.quantity = rec.quantity
            rec.ref_detail_transaksi_id.diskon_id = rec.diskon_id
            rec.ref_detail_transaksi_id.diskon2 = rec.diskon2


class detail_transaksi_wiz(models.TransientModel):
    _name = 'wiz.tokobaju.detail_transaksi'
    _description = 'class untuk data detail transaksi'

    wiz_header_id = fields.Many2one('wiz.tokobaju.transaksi', string='Transaksi')
    ref_detail_transaksi_id = fields.Many2one('tokobaju.detail_transaksi')

    # transaksi_id = fields.Many2one('tokobaju.transaksi', string='Transaksi', readonly=True, ondelete="cascade",
    #                                states={'draft': [('readonly', False)]},
    #                                domain="[('state', '=', 'confirmed')]")

    produk_id = fields.Many2one('tokobaju.produk', string='Nama Produk', ondelete='cascade')

    diskon_id = fields.Many2one('tokobaju.diskon', string='Diskon', readonly=False, ondelete="cascade")

    ukuran = fields.Char("Size", related='produk_id.ukuran')

    harga = fields.Integer("Harga", related='produk_id.harga')

    quantity = fields.Integer(string="Quantity")

    # diskon = fields.Float("Discount Event (10%)", related='diskon_id.jumlah_diskon')
    diskon2 = fields.Float(string="Diskon (%)", digits='Discount', default=0.0)


