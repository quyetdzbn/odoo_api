from datetime import timedelta

from odoo import models, fields


class inheritCrm(models.Model):
    _inherit = 'crm.team'
    _description = 'extend crm team'

    thang1 = fields.Integer()
    thang2 = fields.Integer()
    thang3 = fields.Integer()
    thang4 = fields.Integer()
    thang5 = fields.Integer()
    thang6 = fields.Integer()
    thang7 = fields.Integer()
    thang8 = fields.Integer()
    thang9 = fields.Integer()
    thang10 = fields.Integer()
    thang11 = fields.Integer()
    thang12 = fields.Integer()
    luachon_id = fields.Selection(
        [('thang1', 'thang1'), ('thang2', 'thang2'), ('thang3', 'thang3'), ('thang4', 'thang4'),
         ('thang5', 'thang5'), ('thang6', 'thang6'), ('thang7', 'thang7'), ('thang8', 'thang8'),
         ('thang9', 'thang9'), ('thang10', 'thang10'), ('thang11', 'thang11'),
         ('thang12', 'thang12')], default='thang1')

    # team_id = fields.Char()

    revenue = fields.Float(compute='compute_revenue')
    revenue_target = fields.Float()

    def compute_revenue(self):
        for rec in self:
            # print(rec.name)
            days = self.env['sale.order'].sudo().search([('team_id', '=', rec.name)])
            rec.revenue = 0
            total = 0
            check = 0
            for seller in days:
                # print(seller.date_order)
                if seller.date_order:
                    date_begin = seller.date_order.replace(day=1)
                    date_end = (seller.date_order.replace(day=1) + timedelta(days=31)).replace(day=1) - timedelta(
                        days=1)

                    demo = self.env['sale.order'].sudo().search(
                        [('state', '=', 'sale'), ('team_id', '=', rec.name),
                         ('create_date', '>', date_begin),
                         ('create_date', '<=', date_end)])
                    check = 1

            print(demo)
            if check == 1:
                # print(demo)
                for sell in demo:
                    print(sell.amount_total)
                    total += sell.amount_total
                rec.revenue = total


