from odoo import models, fields, api, _

class _detail_peminjaman(models.Model):
    _name = 'perpus.detail_peminjaman'
    _description = 'class untuk data detail peminjaman'

    date = fields.Date('Tanggal Pengembalian', default=fields.Date.context_today, readonly=True, help='Please fill the date',
                       states={'draft': [('readonly', False)]})
    biaya_denda = fields.Integer('Biaya Denda', compute="_compute_biaya_denda", store=True, recursive=True)

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    peminjaman_id = fields.Many2one('perpus.peminjaman', string='Peminjaman', readonly=True, ondelete="cascade",
                                    states={'draft': [('readonly', False)]},
                                    domain="[('state', '=', 'confirmed')]")

    buku_id = fields.Many2one('perpus.buku', string='Judul Buku', readonly=True, ondelete='cascade',
                              states={'draft': [('readonly', False)]},
                              domain="[('state', '=', 'confirmed')]")

    date_pinjam = fields.Date("Tanggal Peminjaman", related='peminjaman_id.date')

    harga = fields.Integer("Harga Per Hari", related='buku_id.harga')

    biaya_pinjam = fields.Integer('Biaya Peminjaman', compute="_compute_biaya_pinjam", store=True, recursive=True)

    count_days = fields.Integer("Jumlah Hari", compute="_compute_count_days", store=True, recursive=True)

    count_days_telat = fields.Integer("Jumlah Hari Terlambat", compute="_compute_count_days_telat", store=True, recursive=True)

    biaya_telat = fields.Integer('Biaya Keterlambatan', compute="_compute_biaya_telat", store=True, recursive=True)

    status_cacat = fields.Selection([('yes', 'Yes'),
                                     ('no', 'No')], 'Buku Cacat', required=True, readonly=True, default='no',
                                      states={'draft': [('readonly', False)]})

    sub_total = fields.Integer('Sub Total', compute="_compute_sub_total", store=True, recursive=True)

    _sql_constraints = [('cek_tanggal', 'CHECK(count_days>0)', _('Tanggal Kembali harus setelah tanggal pinjam!'))]

    @api.depends('date_pinjam', 'date')
    def _compute_count_days(self):
        if self.date_pinjam and self.date:
            for rec in self:
                count_days = (int((rec.date - rec.date_pinjam).days) + 1)
                rec.count_days = count_days

    @api.depends('harga','count_days')
    def _compute_biaya_pinjam(self):
        for _detail_peminjaman in self:
            val = {
                "biaya_pinjam": 0,
            }
            for rec in self:
                val["biaya_pinjam"] = rec.count_days * rec.harga
            _detail_peminjaman.update(val)

    @api.depends('count_days')
    def _compute_count_days_telat(self):
        if self.count_days:
            for rec in self:
                if self.count_days > 7:
                    count_days_telat = rec.count_days - 7
                else:
                    count_days_telat = 0
                rec.count_days_telat = count_days_telat

    @api.depends('harga', 'count_days_telat')
    def _compute_biaya_telat(self):
        for _detail_peminjaman in self:
            val = {
                "biaya_telat": 0,
            }
            for rec in self:
                val["biaya_telat"] = rec.count_days_telat * (rec.harga*0.1)
            _detail_peminjaman.update(val)

    @api.depends('status_cacat')
    def _compute_biaya_denda(self):
        for _detail_peminjaman in self:
            val = {
                "biaya_denda": 0,
            }
            for rec in self:
                if rec.status_cacat == "yes":
                    val["biaya_denda"] = rec.harga*100
                else:
                    val["biaya_denda"] = 0
            _detail_peminjaman.update(val)

    @api.depends('biaya_pinjam', 'biaya_telat', 'biaya_denda')
    def _compute_sub_total(self):
        for _detail_peminjaman in self:
            val = {
                "sub_total": 0,
            }
            for rec in self:
                val["sub_total"] = rec.biaya_pinjam + rec.biaya_telat + rec.biaya_denda
            _detail_peminjaman.update(val)

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'