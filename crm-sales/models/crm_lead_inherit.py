# -*- coding: utf-8 -*-

from odoo import models, fields, api
import sys


class crmsales(models.Model):
    _inherit = 'crm.lead'
    _description = 'extend crm sale'

    Doanh_thu_toi_thieu = fields.Char()
    Doanh_thu_thuc_te = fields.Float(compute='compute_has_tax')
    Doanh_thu = fields.Float(compute='compute_not_tax')
    Chi_tieu_doanh_thu_id = fields.Integer(compute='tinh_chi_tieu')
    luachon = fields.Selection([('thang1', 'thang1'), ('thang2', 'thang2'), ('thang3', 'thang3'), ('thang4', 'thang4'),
                                ('thang5', 'thang5'), ('thang6', 'thang6'), ('thang7', 'thang7'), ('thang8', 'thang8'),
                                ('thang9', 'thang9'), ('thang10', 'thang10'), ('thang11', 'thang11'),
                                ('thang12', 'thang12')], default='thang1')
    team_member_ids = fields.Many2many('res.users', 'rel_team_crm', 'user_id', 'crm_id',
                                       compute='check_user')  # team_id vaf member_id deu thuoc many2many
    revenue_difference = fields.Float(compute='compute_revenue_difference')

    #chênh lệch doanh thu thực tế so với chỉ tiêu tháng hiện tại
    def compute_revenue_difference(self):
        for rec in self:
            if rec.Doanh_thu_thuc_te and rec.Chi_tieu_doanh_thu_id:
                rec.revenue_difference = rec.Doanh_thu_thuc_te - rec.Chi_tieu_doanh_thu_id
            else:
                rec.revenue_difference = 0

    def check_user(self):
        if self.user_has_groups('crm-sales.group_manager_sales'):
            test = self.env['res.users'].sudo().search([('id', '!=', False)])
            self.sudo().team_member_ids = [(6, 0, test.ids)]
        elif self.env.user.id == self.team_id.user_id.id:
            self.sudo().team_member_ids = [(6, 0, self.team_id.member_ids.ids + [self.team_id.user_id.id])]
        else:
            self.sudo().team_member_ids = [(6, 0, self.team_id.member_ids.ids)]

    @api.depends('order_ids')
    def compute_has_tax(self):
        for rec in self:
            total = 0
            # print(rec.order_ids)
            if rec.order_ids:
                for order in rec.order_ids:
                    if order.state == 'sale':
                        total += order.amount_total
            rec.Doanh_thu_thuc_te = total

    @api.depends('order_ids')
    def compute_not_tax(self):
        for rec in self:
            total = 0
            if rec.order_ids:
                for order in rec.order_ids:
                    if order.state == 'sale':
                        total += order.amount_untaxed
            rec.Doanh_thu = total

    @api.depends('team_id')
    def tinh_chi_tieu(self):
        for rec in self:
            rec.Chi_tieu_doanh_thu_id = 0
            if rec.team_id:
                if rec.create_date.month == 1:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang1
                elif rec.create_date.month == 2:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang2
                elif rec.create_date.month == 3:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang3
                elif rec.create_date.month == 4:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang4
                elif rec.create_date.month == 5:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang5
                elif rec.create_date.month == 6:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang6
                elif rec.create_date.month == 7:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang7
                elif rec.create_date.month == 8:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang8
                elif rec.create_date.month == 9:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang9
                elif rec.create_date.month == 10:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang10
                elif rec.create_date.month == 11:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang11
                elif rec.create_date.month == 12:
                    rec.Chi_tieu_doanh_thu_id = rec.team_id.thang12
