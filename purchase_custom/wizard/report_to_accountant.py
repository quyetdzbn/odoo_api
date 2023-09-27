import re
from datetime import datetime, date, timedelta

from odoo import models, fields, api


class ReportToAccountant(models.TransientModel):
    _name = 'report.to.accountant'

    select_month = fields.Selection(
        [('thang1', 'Tháng 1'), ('thang2', 'Tháng 2'), ('thang3', 'Tháng 3'), ('thang4', 'Tháng 4'),
         ('thang5', 'Tháng 5'), ('thang6', 'Tháng 6'), ('thang7', 'Tháng 7'), ('thang8', 'Tháng 8'),
         ('thang9', 'Tháng 9'), ('thang10', 'Tháng 10'), ('thang11', 'Tháng 11'),
         ('thang12', 'Tháng 12')], default='thang1')
    department_ids = fields.Many2many('hr.department')

    def get_data(self):
        if self.select_month:
            month = re.sub(r'\D', '', self.select_month)
            current_year = date.today().year - 2000
            time = datetime.strptime("01" + month + str(current_year), '%d%m%y')
            date_begin = datetime.strptime("01" + month + str(current_year), '%d%m%y')
            date_end = (date_begin + timedelta(days=31)).replace(day=1)

            action = self.env['ir.actions.act_window']._for_xml_id('purchase_custom.report_to_accountant_action_wizard')

            departments = self.env['hr.department'].sudo().search([('id', 'in', self.department_ids.ids)])
            if departments:
                for department in departments:
                    total = 0

                    department_id_revenue = self.env['hr.department'].search([('id', '=', department.id)])

                    list_po = self.env['purchase.order'].search(
                        [('department', '=', department.id),
                         ('create_date', '>', date_begin),
                         ('create_date', '<=', date_end)])

                    for rec in list_po:
                        if rec.state == 'purchase':
                            total += rec.amount_total
                    rec = self.env['report.accountant'].search(
                        [('department', '=', department.id), ('date_end', '=', date_end),
                         ('date_begin', '=', date_begin)])
                    if rec:
                        continue
                    else:
                        diff = total - department_id_revenue.spending_limit_month
                        seller = self.env['report.accountant'].create(
                            {'actual_spending': total, 'department': department.id,
                             'spending_limit_month': department_id_revenue.spending_limit_month,
                             'revenue_difference': diff,
                             'date_end': date_end, 'date_begin': date_begin})

                action['domain'] = [('date_begin', '=', time),
                                    ('department', 'in', departments.ids)]
            else:
                action['domain'] = []
            return action
