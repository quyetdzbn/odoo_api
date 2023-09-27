# -*- coding: utf-8 -*-
from odoo.http import request

from odoo import http, api, exceptions
import json

from odoo.addons.test_convert.tests.test_env import odoo

# {
#     "token":"odooneverdie" ,
#     "month" : 2
# }

class Main(http.Controller):
    @http.route('/api', methods=['POST'], type='json', auth="public")
    def report_result(self, **kwargs):
        # body
        data = request.jsonrequest
        if data['token'] != "odooneverdie":
            return {"error": "Invalid Token"}

        model_name = "cronjob.data.report"

        try:
            response = {}
            # recordset báo cáo hàng tháng
            crm_report_list = []
            purchase_report_list = []
            records = request.env[model_name].sudo().search([])
            for crm in records.crm_report:
                 if crm.create_date.month == data['month']:
                    crm_report_list.append({
                        "sale_team_name": crm.team_sale.name,
                        "real_revenue": crm.revenue,
                        "diff": crm.diff_revenue_and_month_target
                        })
                    response["sales"] = crm_report_list

            for purchase in records.purchase_report:
                if purchase.create_date.month == data['month']:
                    purchase_report_list.append({
                        "department_name": purchase.department.name,
                        "real_cost": purchase.actual_spending,
                        "diff": purchase.revenue_difference
                    })
                    response["purchases"] = purchase_report_list
    #
        except Exception as e:
            response = {
                "status": "error",
                "content": "not found"
            }
            raise e
        return response