from odoo import models, fields, api, _
from odoo.exceptions import UserError


class _transaksi(models.Model):
    _name = 'tokobaju.transaksi'
    _description = 'class untuk data transaksi'

    name = fields.Char('ID Transaksi', size=64, required=True, index=True, readonly=True, default='new',
                       states={})

    date = fields.Date('Tanggal Transaksi', default=fields.Date.context_today, readonly=True,
                       help='Please fill the date',
                       states={'draft': [('readonly', False)]})

    jumlah = fields.Integer('Jumlah Item', compute="_compute_jumlah", store=True, recursive=True)

    sub_total_transaksi = fields.Integer('Sub Total Bayar', compute="_compute_sub_total_transaksi", store=True,
                                         recursive=True)

    total = fields.Integer('Total Bayar', compute="_compute_total", store=True, recursive=True)

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    detail_transaksi_ids = fields.One2many('tokobaju.detail_transaksi', 'transaksi_id', string='Detail transaksi')

    employee_id = fields.Many2one('hr.employee', 'Employee', index=True, readonly=True,
                                    states={'draft': [('readonly', False)]})

    membership_id = fields.Many2one('res.partner', 'Membership', index=True, readonly=True,
                                    states={'draft': [('readonly', False)]})

    poin_sekarang = fields.Integer("Poin Saat Ini", compute="_compute_poin_now", store=True, recursive=True)
    poin_dipakai = fields.Boolean('Pakai Poin', default=False, readonly=True, states={'draft': [('readonly', False)]})
    poin_tertambah = fields.Integer('Poin Tertambah', compute="_compute_poin", store=True, recursive=True)

    # _sql_constraints = [('cek_periode_berakhir', 'CHECK (detail_transaksi_ids.diskon_id.tanggal_berakhir>=date)',
    #                      'Periode diskon telah lewat'),
    #                     ('cek_periode_mulai', 'CHECK (detail_transaksi_ids.diskon_id.tanggal_mulai<=date)',
    #                      'Periode diskon belum dimulai')]

    @api.depends('detail_transaksi_ids.produk_id', 'detail_transaksi_ids.quantity')
    def _compute_jumlah(self):
        for _transaksi in self:
            val = {
                "jumlah": 0,
            }
            for rec in _transaksi.detail_transaksi_ids:
                val["jumlah"] += rec.quantity
            _transaksi.update(val)

    @api.depends('detail_transaksi_ids.sub_total_item')
    def _compute_sub_total_transaksi(self):
        for _transaksi in self:
            val = {
                "sub_total_transaksi": 0,
            }
            for rec in _transaksi.detail_transaksi_ids:
                val["sub_total_transaksi"] += rec.sub_total_item
            _transaksi.update(val)

    @api.depends('sub_total_transaksi', 'membership_id')
    def _compute_poin(self):
        for _transaksi in self:
            val = {
                "poin_tertambah": 0,
            }
            val["poin_tertambah"] = 0.05 * self.sub_total_transaksi
            _transaksi.update(val)

    @api.depends('membership_id')
    def _compute_poin_now(self):
        for _transaksi in self:
            val = {
                "poin_sekarang": self.membership_id.poin,
            }
            _transaksi.update(val)

    @api.depends('sub_total_transaksi', 'poin_dipakai')
    def _compute_total(self):
        for _transaksi in self:
            val = {
                "total": 0,
            }
            for rec in self:
                if rec.poin_dipakai:
                    if rec.sub_total_transaksi > rec.poin_sekarang:
                        val["total"] += rec.sub_total_transaksi - rec.poin_sekarang
                    else:
                        val["total"] = 0
                else:
                    val["total"] = self.sub_total_transaksi
            _transaksi.update(val)

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "tokobaju.transaksi")])
        if not seq:
            raise UserError(_("tokobaju.transaksi sequence not found, please create tokobaju.transaksi sequence"))
        for val in vals_list:
            val['name'] = seq.next_by_id()
        return super(_transaksi, self).create(vals_list)

    def action_wiz_tokobaju(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Wizard Tokobaju Transaksi'),
            'res_model': 'wiz.tokobaju.transaksi',
            'view_mode': 'form',
            'target': 'new',
            'context': {'active_id': self.id},
        }
