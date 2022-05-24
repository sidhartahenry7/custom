from odoo import models, fields, api, _

class _peminjaman(models.Model):
    _name = 'perpus.peminjaman'
    _description = 'class untuk data peminjaman'

    name = fields.Char('ID Peminjaman', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    date = fields.Date('Tanggal Peminjaman', default=fields.Date.context_today, readonly=True, help='Please fill the date',
                       states={'draft': [('readonly', False)]})
    jumlah = fields.Integer('Jumlah Peminjaman', compute="_compute_jumlah", store=True, recursive=True)
    total = fields.Integer('Total Bayar', compute="_compute_total", store=True, recursive=True)

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    detail_peminjaman_ids = fields.One2many('perpus.detail_peminjaman', 'peminjaman_id', string='Detail Peminjaman')

    anggota_id = fields.Many2one('perpus.anggota', string='Nama Anggota', readonly=True, ondelete='cascade',
                                 states={'draft': [('readonly', False)]},
                                 domain="[('state', '=', 'confirmed')]")

    admin_id = fields.Many2one('perpus.admin', string='Nama Admin', readonly=True, ondelete='cascade',
                               states={'draft': [('readonly', False)]},
                               domain="[('state', '=', 'confirmed')]")

    _sql_constraints = [('name_unik', 'unique(name)', _('ID peminjaman must be unique!'))]

    @api.depends('detail_peminjaman_ids.sub_total')
    def _compute_total(self):
        for _peminjaman in self:
            val = {
                "total": 0,
            }
            for rec in _peminjaman.detail_peminjaman_ids:
                val["total"] += rec.sub_total
            _peminjaman.update(val)

    @api.depends('detail_peminjaman_ids.buku_id')
    def _compute_jumlah(self):
        for _peminjaman in self:
            val = {
                "jumlah": 0,
            }
            for rec in _peminjaman.detail_peminjaman_ids:
                val["jumlah"] += len(rec.buku_id)
            _peminjaman.update(val)

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'
