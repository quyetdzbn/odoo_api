# -*- coding: utf-8 -*-
from datetime import timedelta

from odoo import models, fields, api


class InheritDepartment(models.Model):
    _inherit = 'hr.department'
    _description = 'extend department'

    spending_limit_month = fields.Float()
    actual_spending = fields.Float(compute='compute_actual_spending')
    revenue_difference = fields.Float(compute='compute_revenue_difference')

    def compute_revenue_difference(self):
        for rec in self:
            if rec.spending_limit_month and rec.actual_spending:
                rec.revenue_difference = rec.actual_spending - rec.spending_limit_month
            else:
                rec.revenue_difference = 0

    def compute_actual_spending(self):
        for rec in self:
            days = self.env['purchase.order'].sudo().search([('department', '=', rec.name)])
            rec.actual_spending = 0
            total = 0
            for seller in days:
                # print(seller.date_order)
                if seller.date_order:
                    date_begin = seller.date_order.replace(day=1)
                    date_end = (seller.date_order.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(
                        days=1)

                    demo = self.env['purchase.order'].sudo().search(
                        [('state', '=', 'purchase'), ('department', '=', rec.name),
                         ('create_date', '>', date_begin),
                         ('create_date', '<=', date_end)])
                    check = 1

            if check == 1:
                for sel in demo:
                    total += sel.amount_total
                rec.actual_spending = total
            check = 0
