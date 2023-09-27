from datetime import date, datetime, timedelta

from odoo import models, fields, api


class CronjobDataReport(models.Model):
    _name = 'cronjob.data.report'
    _description = 'create cronjob'
    crm_report = fields.Many2many('target.report')
    purchase_report = fields.Many2many('report.accountant')
    date_end = fields.Datetime()
    date_begin = fields.Datetime()

    # gui dc email
    # cho doan code vao cronjob
    @api.model
    def atu_post_cronjob(self):
        time = date.today()
        month = time.month
        date_begin = (time.replace(day=1))
        date_end = (date_begin + timedelta(days=31)).replace(day=1) - timedelta(days=1)
        teams = self.env['crm.team'].sudo().search([('id', '!=', False)])
        purchase_list = []
        crm_list = []
        crm_list_report = []
        if teams:
            # print(teams.ids)
            for team in teams:
                total = 0
                diff = 0
                # print(team.name)
                list_so = self.env['sale.order'].search(
                    [('team_id', '=', team.id),
                     ('create_date', '>', date_begin),
                     ('create_date', '<=', date_end)])
                team_id_revenue = self.env['crm.team'].search([('id', '=', team.id)])

                for seller in list_so:
                    if seller.state == 'sale':
                        total += seller.amount_total
                if month == 2:
                    diff = total - team_id_revenue.thang2
                elif month == 3:
                    diff = total - team_id_revenue.thang3
                elif month == 4:
                    diff = total - team_id_revenue.thang4
                elif month == 5:
                    diff = total - team_id_revenue.thang5
                elif month == 6:
                    diff = total - team_id_revenue.thang6
                elif month == 7:
                    diff = total - team_id_revenue.thang7
                elif month == 8:
                    diff = total - team_id_revenue.thang8
                elif month == 9:
                    diff = total - team_id_revenue.thang9
                elif month == 10:
                    diff = total - team_id_revenue.thang10
                elif month == 11:
                    diff = total - team_id_revenue.thang11
                elif month == 12:
                    diff = total - team_id_revenue.thang12

                crm_list.append({"team": team.id,
                                 "actual_revenue": total,
                                 "diff_actual_target": diff,
                                 "date_end": date_end,
                                 "date_begin": date_begin})
            # print(crm_list)

            for rec in crm_list:
                check = self.env['target.report'].search(
                    [('team_sale', '=', rec['team']), ('date_end', '=', rec['date_end']),
                     ('date_begin', '=', rec['date_begin'])])
                if check:
                    continue
                else:
                    self.env['target.report'].create(
                        {"team_sale": rec['team'],
                         "revenue": rec['actual_revenue'],
                         "diff_revenue_and_month_target": rec['diff_actual_target'],
                         "date_end": rec['date_end'],
                         "date_begin": rec['date_begin']
                         })

            for rec in self.env['target.report'].search([('create_date', '>=', date_begin), ('create_date', '<=', date_end)]):
                crm_list_report.append(rec.id)

        departments = self.env['hr.department'].sudo().search([('id', '!=', False)])
        if departments:
            for department in departments:
                total = 0
                # print(department.name)
                department_id_revenue = self.env['hr.department'].search([('id', '=', department.id)])

                list_po = self.env['purchase.order'].search(
                    [('department', '=', department.id),
                     ('create_date', '>', date_begin),
                     ('create_date', '<=', date_end)])

                for rec in list_po:
                    if rec.state == 'purchase':
                        total += rec.amount_total
                purchase_list.append({"department_id": department.id,
                                      "actual_spending": total,
                                      "diff_actual_limit": total - department_id_revenue.spending_limit_month,
                                      "date_end": date_end,
                                      "date_begin": date_begin
                                      })
            for rec in purchase_list:
                check = self.env['report.accountant'].search(
                    [('department', '=', rec['department_id']), ('date_end', '=', rec['date_end']),
                     ('date_begin', '=', rec['date_begin'])])
                if check:
                    continue
                else:
                    self.env['report.accountant'].create(
                        {"department": rec['department_id'],
                         "actual_spending": rec['actual_spending'],
                         "revenue_difference": rec['diff_actual_limit'],
                         "date_end": rec['date_end'],
                         "date_begin": rec['date_begin']
                         })
            purchase_list_report = []
            for rec in self.env['report.accountant'].search(
                    [('create_date', '>=', date_begin), ('create_date', '<=', date_end)]):
                purchase_list_report.append(rec.id)

            check_purchase_report_crm_report = self.search(
                [('purchase_report', '!=', False), ('crm_report', '!=', False),('create_date', '>=', date_begin),
                 ('create_date', '<=', date_end)])
            if not check_purchase_report_crm_report:
                self.create({"crm_report": [(6, 0, crm_list_report)],
                            "purchase_report": [(6, 0, purchase_list_report)], "date_end": date_end,
                             "date_begin": date_begin})

        record = self.env['cronjob.data.report'].search([('create_date', '<=', date_end), ('create_date', '>=', date_begin)])[-1]
        group = self.env.ref('purchase_custom.group_accountant')
        for user in group.users:
            email_values = {
                'email_cc': False,
                'auto_delete': True,
                'recipient_ids': [],
                'partner_ids': [],
                'scheduled_date': False,
                # 'email_from': 'mailto:nguyendanhbinhgiang@gmail.com',
                'email_to': 'mailto:' + user.partner_id.email,
            }
            mail_template = self.env.ref('crm-sales.mail_template_mobile_merge_request')
            mail_template.send_mail(record.id, force_send=True, raise_exception=True, email_values=email_values)
