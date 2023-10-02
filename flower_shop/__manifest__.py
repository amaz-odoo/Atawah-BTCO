# -*- coding: utf-8 -*-
{
    'name': "Sally Flower Shop",
    'summary': """Sally's Flower shop contains many types of flowers""",
    'description': """ 
         Sally's Flower Shop - 
         Sally runs a flower shop. She wants to use Odoo in order to run her daily tasks smoothly. 
         This store grows its own flowers in a garden nearby. These flowers have a set of different attributes.
        """,

    'author': "HalimaHamood",
    'website': "https://www.yourcompany.com",
    'category': 'Uncategorized',
    'version': '0.1',
    'depends': ['base', 'sale', 'mail', 'website', 'website_sale', 'stock'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
        'views/flower.xml',
        'views/product.xml',
        'views/flower_product.xml',
        'views/templates.xml',
        'views/tracking_water.xml',
        'views/weather_data.xml',
        'reports/flower_sale_order_views.xml',
        'data/groups.xml',
        'data/action.xml',
        'data/weather_api.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
