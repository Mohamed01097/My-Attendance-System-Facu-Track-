from odoo import models, fields, api, _
import random
import warnings
import os
import pandas as pd
from odoo.exceptions import MissingError, UserError, ValidationError, AccessError
from datetime import datetime, timedelta, date, time
from dateutil.relativedelta import relativedelta
from .my_location import GetUserlocation


class Course(models.Model):
    _name = 'facu_track.course'
    _description = 'Faculty Course'

    name = fields.Char(required=True, readonly=True)
    code = fields.Char(string='Course Code', required=True, readonly=True)
    prof_id = fields.Many2one('facu_track.prof', string='Professor', readonly=True)
    begining_time = fields.Datetime(string="Time Of Beginning", readonly=True)
    end_time = fields.Datetime(string="Time Of Finishing", readonly=True)
    student_ids = fields.One2many('facu_track.student', 'course_id', string='Students', readonly=True)
    location_ids = fields.One2many('facu_track.student', 'location_id', string='Location')
    number_of_student = fields.Integer(default=0, domain=lambda self: "[('groups_id', '=', 'facu_track_admins_group')]")
    state = fields.Selection(string='Status', required=True, copy=False, tracking=True, selection=[
        ('absent', 'Absent'),
        ('attend', 'Attended'),
    ], default='absent')
    clear_location = fields.Boolean(default=False)
    email = fields.Char(string="Email")
    color = fields.Char(string="Color")
    l10n_ke_cu_qrcode = fields.Char(string='CU QR Code', copy=False)

    def access_location(self):
        obj = GetUserlocation()
        user = self.env.user
        student_records = self.env['facu_track.student'].search([])
        user_id = self.env['facu_track.student'].search([('name', '=', user.name)], limit=1)

        for rec in self:
            if (len(rec.student_ids)):
                raise ValidationError("Your Attendance Successfuly Confirmed , You Can Exit Now")

        for student in student_records:
            if student.latitude and student.longitude:
                raise ValidationError("Your Location Already Checked")

        if user_id not in student_records:
            raise ValidationError("You are not a student")

        latitude, longitude = obj.check_user_location()[0], obj.check_user_location()[1]

        for student in student_records:
            student.latitude = latitude
            student.longitude = longitude

        self.location_ids |= (user_id)
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'warning',
                'title': _("Warning"),
                'message': "Don't Forget to Confirm Your Attendance Before You Exit!",
                'next': {
                    'type': 'ir.actions.act_window_close'
                },
            }
        }

    def confirm_attendance(self):
        obj = GetUserlocation()
        user = self.env.user
        user_id = self.env['facu_track.student'].search([('name', '=', user.name)], limit=1)
        date_time_now = datetime.now() + timedelta(hours=3)
        student_records = self.env['facu_track.student'].search([])

        try:
            for student in student_records:
                if not student.latitude or not student.longitude:
                    raise ValidationError("You Must Check Your Location")

            if not self.check_if_there_is_time_or_not():
                raise ValidationError(_("The time of the lecture is not found"))
            #
            if not self.check_lecture_time():
                raise ValidationError("You are not accepted")

            if not obj.check_if_range_available_or_not():
                raise ValidationError("You Are Not In The Available Range")
            #
            if user_id not in student_records:
                raise ValidationError("You are not found")

            self.student_ids |= (user_id)
            for student in self.student_ids:
                student.date = str(date_time_now.time())

            self.clear_student_location()

        except Exception as error:
            raise error

        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'type': 'success',
                'title': _("Successfuly Confirmed"),
                'message': "You confirm attendance Successfuly",
                'next': {
                    'type': 'ir.actions.act_window_close'
                },
            }
        }

    def check_lecture_time(self):
        date_time_now = datetime.now() + timedelta(hours=3)
        if self.begining_time <= date_time_now < self.end_time:
            return True
        else:
            return False

    def check_if_there_is_time_or_not(self):
        if not self.begining_time or not self.end_time:
            return False
        return True

    def empty_list(self):
        self.student_ids = [(5, 0, 0)]
        self.clear_student_location()

    def clear_student_location(self):
        self.location_ids = [(5, 0, 0)]
        students = self.env['facu_track.student']
        for rec in students.search([]):
            rec.latitude = 0.0
            rec.longitude = 0.0

    def set_date_time_now(self):
        now = datetime.now() + timedelta(hours=3)
        return now


class ResUser(models.Model):
    _inherit = 'res.users'

    def delete_users_from_group(self):
        for user in self.search([('id', '>', 2)]):
            if user.has_group("base.group_portal"):
                user.unlink()

    def add_to_group(self, group_xml_id):
        users = self.env['facu_track.prof'].search([('id', '=', 2)])
        group_id = self.env.ref(group_xml_id)
        group_id.users = [(4, user.id) for user in users]

    def call_add_to_group(self):
        self.add_to_group('facu_track.facu_track_profs_group')

    def remove_from_groups(self, user_ids, group_ids):
        users = self.browse(user_ids)

        for group_id in group_ids:
            users.write({'groups_id': [(3, group_id)]})

        return True

    def call_remove_from_all_groups(self):
        user_ids = self.search([('id', '=', 439)]).ids
        group_ids = self.env['res.groups'].search(
            [('id', 'in', [11, 25, 17, 45, 47, 8, 1, 57, 64, 42, 6, 24, 40, 39, 16, 26, 20, 5])]).ids
        res_users_model = self.env['res.users']
        res_users_model.remove_from_groups(user_ids, group_ids)
