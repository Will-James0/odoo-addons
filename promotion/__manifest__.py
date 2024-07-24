# -*- coding: utf-8 -*-
{
    'name': "Promotion Module",

    'summary': """
        Manage promotions and discounts
    """,

    'description': """
        Module to manage promotions with multiple tiers and specific product applicability.
    """,

    'author': "will",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Sales',
    'version': '1.0',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale', 'account', 'product', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/promotion_views.xml',
        'views/account_move_views.xml',
        'views/product_views.xml',
        'views/sale_order.xml',
        'views/sale_order_portal.xml',
        'views/account_report.xml',
    ],

    'installable': True,
    'application': False,

    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
