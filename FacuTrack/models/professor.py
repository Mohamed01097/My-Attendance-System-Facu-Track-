from odoo import models, fields
import random, datetime


class Professor(models.Model):
    _name = 'facu_track.prof'
    _description = 'Faculty Professor'
    _rec_name = 'name'

    name = fields.Char(required=True)
    code = fields.Char(string='Professor Code', required=True)
    dept_id = fields.Many2one('facu_track.dept', string='Department', required=True)
    course_ids = fields.One2many('facu_track.course', 'prof_id', string="Course")
    email = fields.Char("Email")

    # def test(self):
    #     course_ids = self.env['facu_track.course'].search([])
    #     students = self.env['facu_track.student'].search([])
    #     for student in students:
    #         if course_ids:
    #             student.course_id = random.choice(course_ids.ids)

    # def test_date(self):
    #     students = self.env['facu_track.student'].search([])
    #     for student in students:
    #         random_datetime = self.generate_random_datetime()
    #         student.date = random_datetime

    # @staticmethod
    # def generate_random_datetime():
    #     start_datetime = datetime.datetime(2023, 1, 1)
    #     end_datetime = datetime.datetime(2023, 12, 31)
    #
    #     time_range = (end_datetime - start_datetime).total_seconds()
    #     random_seconds = random.randint(0, int(time_range))
    #     random_datetime = start_datetime + datetime.timedelta(seconds=random_seconds)
    #
    #     return random_datetime

    # def test_courses(self):
    #     students = self.env['facu_track.student'].search([('course_id', '=', self.id)])
    #     courses = self.env['facu_track.course'].search([])
    #     for rec in courses:
    #         rec.student_ids = students
