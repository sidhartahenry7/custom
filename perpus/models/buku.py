from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _buku(models.Model):
    _name = 'perpus.buku'
    _description = 'class untuk data buku'

    name = fields.Char('Nama Buku', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    id_buku = fields.Char('ID Buku', size=64, required=True, index=True, readonly=True, default='new',
                          states={})
    kode_isbn = fields.Char('Kode ISBN', size=64, required=True, index=True, readonly=True,
                          states={'draft': [('readonly', False)]})
    penulis = fields.Char('Penulis', size=64, required=True, index=True, readonly=True,
                          states={'draft': [('readonly', False)]})
    penerbit = fields.Char('Penerbit', size=64, required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})
    tahun_terbit = fields.Char('Tahun Terbit', size=64, required=True, index=True, readonly=True,
                               states={'draft': [('readonly', False)]})
    quantity = fields.Integer('Quantity', size=64, required=True, index=True, readonly=True,
                              states={'draft': [('readonly', False)]})

    harga = fields.Integer('Harga', size=64, required=True, index=True, readonly=True,
                           states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('id_unik', 'unique(id_buku)', _('ID Buku must be unique!')),
                        ('cek_harga', 'CHECK (harga>=0)', 'Harga tidak boleh minus'),
                        ('cek_quantity', 'CHECK (quantity>=0)', 'Quantity buku tidak boleh minus')]

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "perpus.buku")])
        if not seq:
            raise UserError(_("perpus.buku sequence not found, please create perpus.buku sequence"))
        for val in vals_list:
            val['id_buku'] = seq.next_by_id()
        return super(_buku, self).create(vals_list)