from odoo import models, fields, api, _

class _admin(models.Model):
    _name = 'perpus.admin'
    _description = 'class untuk data admin'

    name = fields.Char('Nama Admin', size=64, required=True, index=True, readonly=True,
                       states={'draft': [('readonly', False)]})
    id_admin = fields.Char('ID Admin', size=64, required=True, index=True, readonly=True,
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

    _sql_constraints = [('id_unik', 'unique(id_admin)', _('ID admin must be unique!'))]

    def action_confirmed(self):
        self.state = 'confirmed'

    def action_canceled(self):
        self.state = 'canceled'

    def action_settodraft(self):
        self.state = 'draft'