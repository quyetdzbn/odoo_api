# -*- coding: utf-8 -*-
{
    'name': "crm-sales",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['crm', 'sale_crm'],

    # always loaded
    'data': [
        'security/group.xml',
        'security/ir.model.access.csv',
        'views/crm_team_inherit.xml',
        'views/crm_lead_views_inherit.xml',
        'views/sale_views_inherit.xml',
        'views/plan_sale_order_view.xml',
        'views/cron.xml',
        'wizard/detail_report_view.xml',
        'wizard/detail_report_wizard.xml',
        'wizard/target_report_view.xml',
        'wizard/target_report_wizard.xml',
        'data/cronjob_detail_report.xml',
        'data/email_send_to_accountant.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
