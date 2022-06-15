from odoo import models, fields, api, _

class ResPartner(models.Model):
    _inherit = 'res.partner'
    poin = fields.Integer("Poin", compute="_compute_poin", store=True, default=0)
    transaksi_ids = fields.One2many('tokobaju.transaksi', 'membership_id', string="Transaksi")

    @api.depends('transaksi_ids.state')
    def _compute_poin(self):
        for ResPartner in self:
            val = {'poin': 0}
            for rec in ResPartner.transaksi_ids.filtered(lambda i: i.state == 'confirmed'):
                if rec.poin_dipakai == True:
                    if rec.sub_total_transaksi >= val['poin']:
                        val['poin'] = rec.poin_tertambah
                    else:
                        val['poin'] = val['poin'] - rec.sub_total_transaksi + rec.poin_tertambah
                else:
                    val['poin'] += rec.poin_tertambah
            ResPartner.update(val)