from odoo import models, fields, api
import re
from datetime import datetime, date, timedelta

record = []


class baocaoWizard(models.TransientModel):
    _name = 'baocao.wizard'

    team_ids = fields.Many2many('crm.team')
    select_month = fields.Selection(
        [('thang1', 'Tháng 1'), ('thang2', 'Tháng 2'), ('thang3', 'Tháng 3'), ('thang4', 'Tháng 4'),
         ('thang5', 'Tháng 5'), ('thang6', 'Tháng 6'), ('thang7', 'Tháng 7'), ('thang8', 'Tháng 8'),
         ('thang9', 'Tháng 9'), ('thang10', 'Tháng 10'), ('thang11', 'Tháng 11'),
         ('thang12', 'Tháng 12')], default='thang1')

    def get_detail_report(self):
        if self.select_month:
            x = re.sub(r'\D', '', self.select_month)
            current_year = date.today().year - 2000
            date_begin = datetime.strptime("01" + x + str(current_year), '%d%m%y')
            date_end = (date_begin + timedelta(days=31)).replace(day=1) - timedelta(days=1)

            action = self.env['ir.actions.act_window']._for_xml_id('crm-sales.bao_cao_tree_action')
            if self.team_ids:
                action['domain'] = [('create_date', '>', date_begin), ('create_date', '<=', date_end),
                                    ('team_id', 'in', self.team_ids.ids)]
            else:
                action['domain'] = [('create_date', '>', date_begin), ('create_date', '<=', date_end)]
            return action

    def get_target_report(self):

        if self.select_month:
            month = re.sub(r'\D', '', self.select_month)
            current_year = date.today().year - 2000
            time = datetime.strptime("01" + month + str(current_year), '%d%m%y')
            date_begin = datetime.strptime("01" + month + str(current_year), '%d%m%y')
            date_end = (date_begin + timedelta(days=31)).replace(day=1) - timedelta(days=1)
            action = self.env['ir.actions.act_window']._for_xml_id('crm-sales.bao_cao_chi_tieu_tree_action')

            teams = self.env['crm.team'].sudo().search([('id', 'in', self.team_ids.ids)])

            if teams:
                # print(teams.ids)
                for team in teams:
                    total = 0
                    list_so = self.env['sale.order'].search(
                        [('team_id', '=', team.id),
                         ('create_date', '>', date_begin),
                         ('create_date', '<=', date_end)])
                    # print(date_begin)
                    team_id_revenue = self.env['crm.team'].search([('id', '=', team.id)])

                    sell = []
                    diff = 0
                    target_revenue = 0
                    for seller in list_so:
                        if seller.state == 'sale':
                            total += seller.amount_total
                    rec = self.env['target.report'].search([('team_sale', '=', team.name), ('date_end', '=', date_end),
                                                            ('date_begin', '=', date_begin)])
                    if rec:
                        continue
                    elif month == '1':
                        diff = total - team_id_revenue.thang1
                        target_revenue = team_id_revenue.thang1
                    elif month == '2':
                        diff = total - team_id_revenue.thang2
                        target_revenue = team_id_revenue.thang2
                    elif month == '3':
                        diff = total - team_id_revenue.thang3
                        target_revenue = team_id_revenue.thang3
                    elif month == '4':
                        diff = total - team_id_revenue.thang4
                        target_revenue = team_id_revenue.thang4
                    elif month == '5':
                        diff = total - team_id_revenue.thang5
                        target_revenue = team_id_revenue.thang5
                    elif month == '1':
                        diff = total - team_id_revenue.thang1
                        target_revenue = team_id_revenue.thang1
                    elif month == '6':
                        diff = total - team_id_revenue.thang6
                        target_revenue = team_id_revenue.thang6
                    elif month == '7':
                        diff = total - team_id_revenue.thang7
                        target_revenue = team_id_revenue.thang7
                    elif month == '8':
                        diff = total - team_id_revenue.thang8
                        target_revenue = team_id_revenue.thang8
                    elif month == '9':
                        diff = total - team_id_revenue.thang9
                        target_revenue = team_id_revenue.thang9
                    elif month == '10':
                        diff = total - team_id_revenue.thang10
                        target_revenue = team_id_revenue.thang10
                    elif month == '11':
                        diff = total - team_id_revenue.thang11
                        target_revenue = team_id_revenue.thang11
                    elif month == '12':
                        diff = total - team_id_revenue.thang12
                        target_revenue = team_id_revenue.thang12
                    sell = self.env['target.report'].create({'revenue': total, 'team_sale': team.id,
                                                             'revenue_target': target_revenue,
                                                             'diff_revenue_and_month_target': diff,
                                                             'date_end': date_end, 'date_begin': date_begin})

                action['domain'] = [('team_sale', 'in', teams.ids), ('date_begin', '=', time)]
            else:
                action['domain'] = []

            return action
