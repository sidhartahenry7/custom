from odoo import models, fields, api, _

class _anggota(models.Model):
    _name = 'perpus.anggota'
    _description = 'class untuk data anggota'

    name = fields.Many2one('res.users', 'Nama Anggota', readonly=True, default=lambda self: self.env.user,
                           states={'draft': [('readonly', False)]})
    id_anggota = fields.Char('ID Anggota', size=64, required=True, index=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    email = fields.Char('E-mail', size=64, required=True, index=True, readonly=True,
                        states={'draft': [('readonly', False)]})
    alamat = fields.Char('Alamat', size=64, required=True, index=True, readonly=True,
                         states={'draft': [('readonly', False)]})
    no_telp = fields.Char('No. Telepon', size=64, required=True, index=True, readonly=True,
                          states={'draft': [('readonly', False)]})

    state = fields.Selection([('draft', 'Draft'),
                              ('confirmed', 'Confirmed'),
                              ('canceled', 'Canceled')], 'State', required=True, readonly=True, default='draft')

    _sql_constraints = [('id_unik', 'unique(id_anggota)', _('ID Anggota must be unique!'))]

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'