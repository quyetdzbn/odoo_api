from odoo import models, fields, api
from odoo.exceptions import ValidationError


class B(models.Model):
    _name = 'limit_order_staff'
    _description = 'new'

    staff = fields.Many2one('res.users')
    limit_order = fields.Integer()