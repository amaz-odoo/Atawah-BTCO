# -*- coding: utf-8 -*-
{
    'name': "FlowerShop",

    'summary': """
     Odoo FlowerShop Excersize""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale_management','stock','website_sale','base_geolocalize'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/main_views.xml',
        'views/product.xml',
        'views/stock_lot.xml',
        'reports/flower_sale_order_views.xml',
        'data/res_groups.xml',
        'views/stock_warehouse.xml',
        #'data/ir_sequence.xml',
        'views/web_flower.xml',
        # 'data/ir_config_parameter.xml',
        #Tried part7 (as a comment) but That things was New!
    ],

}
