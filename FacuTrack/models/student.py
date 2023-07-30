# -*- coding: utf-8 -*-
from odoo import models, fields, api
import random
from datetime import datetime
import geocoder


class Student(models.Model):
    _name = 'facu_track.student'
    _description = 'facu_track.student'
    _order = 'name'

    name = fields.Char(required=True)
    code = fields.Char(required=True, string="Student Code")
    group = fields.Integer(required=True)
    dept_id = fields.Many2one('facu_track.dept', string="Department",readonly=True)
    course_id = fields.Many2one('facu_track.course', string="course",readonly=True)
    location_id = fields.Many2one('facu_track.course', string="Location")
    date = fields.Char(string="Time Of Attend",readonly=True)
    prof_id = fields.Many2one('facu_track.prof', string="Professor", related='course_id.prof_id')
    latitude = fields.Float(readonly=True)
    longitude = fields.Float(readonly=True)
    location_checked = fields.Boolean()
    attendance_confirmed = fields.Boolean()
    clear_location = fields.Boolean(default=False)



