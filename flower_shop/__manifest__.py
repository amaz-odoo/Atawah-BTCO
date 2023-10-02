# -*- coding: utf-8 -*-
{
    'name': "Sally's Flower Shop",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,
    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '16.0.0.0.0',
    'depends': ["website_sale", "stock", "base_geolocalize"],
    'data': [
        # data
        'data/res_groups.xml',
        'data/ir_actions_server.xml',
        'data/ir_config_parameter.xml',
        'data/ir_cron.xml',
        # views
        'views/flower_views.xml',
        'views/product_views.xml',
        'views/sale_order_views.xml',
        'views/stock_production_lot_views.xml',
        'views/templates.xml',
        'views/stock_warehouse_views.xml',
        'views/flower_water_views.xml',
        # reports
        'reports/paperformat.xml',
        'reports/flower_sale_order_views.xml',
        # menuitems
        'views/menu_items.xml',
        # security
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
    'license': 'OEEL-1',
}
