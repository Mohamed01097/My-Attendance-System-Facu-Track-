from odoo import models, fields, api


class Department(models.Model):
    _name = 'facu_track.dept'
    _rec_name = 'code'
    _description = 'Faculty Department'

    name = fields.Selection([
        ('cs', 'Computer Science'),
        ('it', 'Information Technology'),
        ('is', 'Information Systems'),
        ('mm', 'Multimedia')
    ], string='Department Name', required=True)
    code = fields.Char(string='Department Code')
    student_ids = fields.One2many('facu_track.student','dept_id',string="Students")
    prof_ids = fields.One2many('facu_track.prof','dept_id',string="Professors")








