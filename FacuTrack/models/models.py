# -*- coding: utf-8 -*-

# from odoo import helper_files, fields, api


# class facu_track(helper_files.Model):
#     _name = 'facu_track.facu_track'
#     _description = 'facu_track.facu_track'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
