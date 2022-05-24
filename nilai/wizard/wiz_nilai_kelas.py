from odoo import models, fields, api, _

class wizkelas(models.TransientModel):
    _name = 'wiz.nilai.kelas'
    _description = 'class untuk menyimpan data kelas dan nilai'

    kelas_id = fields.Many2one('nilai.kelas', String='Kelas')

    semester = fields.Selection(related='kelas_id.semester')
    tahun = fields.Char(related='kelas_id.tahun')

    mk_id = fields.Many2one(related='kelas_id.mk_id')

    line_ids = fields.One2many('wiz.nilai.kelas.lines', 'wiz_header_id', string='Nilai')

    @api.model
    def default_get(self,fields_list):  # ini adalah common method, semacam constructor, akan dijalankan saat create object. Ini akan meng-overwrite default_get dari parent
        res = super(wizkelas, self).default_get(fields_list)
        # res  merupakan dictionary beserta value yang akan diisi, yang sudah diproses di super class (untuk create record baru)
        res['kelas_id'] = self.env.context['active_id']
        return res

    @api.onchange('kelas_id')
    def onchange_kelas_id(self):
        if not self.kelas_id:
            return
        vals = []
        line_ids = self.env['wiz.nilai.kelas.lines']
        for rec in self.kelas_id.line_ids:
            line_ids += self.env['wiz.nilai.kelas.lines'].new({
                'wiz_header_id': self.id,
                'mhs_id': rec.mhs_id.id,
                'ref_kelas_lines_id': rec.id
            })
            # cara membuat record baru di m2m atau o2m
        self.line_ids = line_ids

    def action_confirm(self):
        for rec in self.line_ids:
            rec.ref_kelas_lines_id.grade = rec.grade


class kelas_lines_wiz(models.TransientModel):
    _name = 'wiz.nilai.kelas.lines'
    _description = 'class untuk menyimpan data nilai suatu kelas'

    wiz_header_id = fields.Many2one('wiz.nilai.kelas', string='Kelas')
    mhs_id = fields.Many2one('nilai.mahasiswa', string='Mahasiswa', ondelete="restrict")
    ref_kelas_lines_id = fields.Many2one('nilai.kelas.lines')
    grade = fields.Selection([('A', 'A'),
                              ('B+', 'B+'),
                              ('B', 'B'),
                              ('C+', 'C+'),
                              ('C', 'C'),
                              ('D', 'D'),
                              ('E', 'E')])

