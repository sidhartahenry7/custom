from odoo import models, fields, api, _

class Employee(models.Model):
    _inherit = "hr.employee"
    tanggal_masuk = fields.Date('Tanggal Masuk', default=fields.Date.context_today, help='Please fill the date')
    tanggal_keluar = fields.Date('Tanggal Keluar', help='Please fill the date')

    _sql_constraints = [('cek_tanggal_keluar', 'CHECK(tanggal_keluar>tanggal_masuk)', _('Tanggal Keluar harus setelah tanggal masuk!'))]