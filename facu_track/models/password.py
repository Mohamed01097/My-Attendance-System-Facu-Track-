from odoo import fields, models, api,_
from odoo.exceptions import ValidationError

class Paasword(models.TransientModel):
    _name = 'facu_track.password'

    new_password = fields.Char(string="New Password")
    def change_password(self):
        self.env.user.password = self.new_password
