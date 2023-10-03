# -*- coding: utf-8 -*-
{
    'name': "Sally's Flower Shop",
    'version': '1.0',
    'summary': 'Manage flowers and gardening tasks for Sally\'s Flower Shop',
    'description': """
        This module allows Sally to manage her flower shop's inventory and gardening tasks.
    """,
    'author': 'Your Name',
    'category': 'Tools',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/tree_view.xml',
        'views/form_view.xml',
        'views/menu_item.xml',
    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}
