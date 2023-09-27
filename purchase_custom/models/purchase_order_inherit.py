import re
from aifc import Error
from datetime import date

from AptUrl.Helpers import _

from odoo import models, fields, api
from datetime import datetime, timedelta

from odoo.exceptions import UserError


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order'
    _description = 'extend purchase order'

    department = fields.Many2one('hr.department')
    actual_spending = fields.Float(compute='compute_actual_spending')
    limit_spending_month = fields.Float(compute='compute_limit_spending_month')
    revenue_difference = fields.Float(compute='compute_revenue_difference')

    # chênh lệch chi tiêu thực tế với hạn mức
    def compute_revenue_difference(self):
        for rec in self:
            if rec.limit_spending_month and rec.actual_spending:
                rec.revenue_difference = rec.actual_spending - rec.limit_spending_month
            else:
                rec.revenue_difference = 0

    def compute_limit_spending_month(self):
        for rec in self:
            rec.limit_spending_month = rec.department.spending_limit_month

    def button_confirm(self):
        limit_order_user = 0
        # kiểm tra người tạo có tạo yêu cầu vượt quá hạn mức hay k, nếu có gây ra lỗi và gửi activity đến kế toán
        setting = self.env['order.limit.configuration'].search([])
        for rec in setting.link_to_b:
            if rec.staff == self.env.user:
                limit_order_user = rec.limit_order

        if self.amount_total > limit_order_user and not self.user_has_groups('purchase_custom.group_accountant'):
            group = self.env.ref('purchase_custom.group_accountant')
            for user in group.users:
                self.env['mail.activity'].sudo().create({
                    'summary': 'Xác nhận yêu cầu đặt hàng',
                    'res_id': self.id,
                    'res_model_id': self.env['ir.model']._get_id('purchase.order'),
                    'user_id': user.id,
                })
            return {
                'name': _('Lỗi'),
                'type': 'ir.actions.act_window',
                'view_mode': 'form',
                'res_model': 'report.to.accountant',
                'target': 'new'
            }
        return super(InheritPurchaseOrder, self).button_confirm()

    def compute_actual_spending(self):
        for rec in self:
            total = 0
            if rec.date_order:
                date_begin = rec.date_order.replace(day=1)
                date_end = (rec.date_order.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(days=1)

                demo = self.env['purchase.order'].sudo().search(
                    [('state', '=', 'purchase'), ('department', '=', rec.department.id),
                     ('create_date', '>', date_begin),
                     ('create_date', '<=', date_end), ])
                # print(demo)
                for seller in demo:
                    # print(seller.amount_total)
                    total += seller.amount_total
                rec.actual_spending = total
            else:
                rec.actual_spending = 1
