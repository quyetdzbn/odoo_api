from datetime import timedelta

from odoo import models, fields, api


class TargetReport(models.Model):
    _name = "target.report"
    _description = 'target report'

    revenue = fields.Float()
    revenue_target = fields.Float()
    team_sale = fields.Many2one('crm.team')
    date_end = fields.Datetime()
    date_begin = fields.Datetime()
    diff_revenue_and_month_target = fields.Float()
    # team_sale = fields.Selection(related='link.team_id')
