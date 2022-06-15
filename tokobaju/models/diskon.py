from odoo import models, fields, api, _
from odoo.exceptions import UserError

class _diskon(models.Model):
    _name = 'tokobaju.diskon'
    _description = 'class untuk data diskon'

    name = fields.Char('Event Diskon', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})

    id_diskon = fields.Char('ID Diskon', size=64, required=True, index=True, readonly=True, default='new',
                              states={})

    tanggal_mulai = fields.Date('Tanggal Mulai', default=fields.Date.context_today, readonly=True,
                       help='Please fill the date',
                       states={'draft': [('readonly', False)]})

    tanggal_berakhir = fields.Date('Tanggal Berakhir', default=fields.Date.context_today, readonly=True,
                                help='Please fill the date',
                                states={'draft': [('readonly', False)]})

    jumlah_diskon = fields.Float(string="Diskon (%)", digits='Discount', default=0.0)

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('cek_diskon', 'CHECK (jumlah_diskon>=0)', 'Diskon tidak boleh minus'),
                        ('cek_tanggal_berakhir', 'CHECK(tanggal_berakhir>=tanggal_mulai)', _('Tanggal Diskon berakhir harus setelah tanggal mulai!'))]

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'

    @api.model_create_multi
    def create(self, vals_list):
        seq = self.env['ir.sequence'].search([("code", "=", "tokobaju.diskon")])
        if not seq:
            raise UserError(_("tokobaju.diskon sequence not found, please create tokobaju.diskon sequence"))
        for val in vals_list:
            val['id_diskon'] = seq.next_by_id()
        return super(_diskon, self).create(vals_list)