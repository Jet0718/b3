# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'CRM Dashboard Inherit',
    'version': '17.0.0.2',
    'category': 'Category',
    'author': "BWCS PMO",
    'license': "LGPL-3", 
    'sequence': 15,
    'summary': 'CRM Dashboard Inherit',
    'description': "This is a CRM dashboard Inherit Module 01.01",
    'website': '',
    'depends': ['base','resource','crm'],
    'data': [
        # 'security/estate_group.xml',
        # 'security/ir.model.access.csv',
        # 'security/estate_security.xml',
        'views/crm_dashboard_action.xml',
        # 'views/estate_property_tag_view.xml',
        # 'views/estate_property_view.xml',
        # 'views/estate_menu.xml',
        # 'views/estate_property_offer_view.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'crm_dashboard/static/src/js/dashboard.js',
            'crm_dashboard/static/src/xml/dashboard.xml',
        ],
    },
    #'application': True,
}