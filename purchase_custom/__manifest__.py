# -*- coding: utf-8 -*-
{
    'name': "PurchaseCustom",

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
    'depends': ['base','hr','purchase'],

    # always loaded
    'data': [
        'security/group.xml',
        'data/department.xml',
        'security/ir.model.access.csv',
        'views/hr_department_view_inherit.xml',
        'views/purchase_views_inherit.xml',
        'views/order_limit_configuration_view.xml',
        'wizard/report_to_accountant_view.xml',
        'wizard/popup_raise_incorrect.xml',
        'wizard/report_to_accountant_wizard.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
