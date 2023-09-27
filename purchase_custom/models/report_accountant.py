from pkg_resources import _

from odoo import models, fields, api


class ReportAccountant(models.Model):
    _name = 'report.accountant'
    _description = 'report'

    department = fields.Many2one('hr.department')
    spending_limit_month = fields.Float()
    actual_spending = fields.Float()
    revenue_difference = fields.Float()
    date_end = fields.Datetime()
    date_begin = fields.Datetime()

