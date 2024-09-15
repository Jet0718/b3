# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name': 'Real Estate',
    'version': '17.0.0.2',
    'category': 'Category',
    'author': "BWCS PMO",
    'license': "LGPL-3", 
    'sequence': 15,
    'summary': 'Real Estate managements',
    'description': "This is a Estate Management Module 01.01",
    'website': '',
    'depends': ['base','resource'],
    'data': [
        'security/ir.model.access.csv',
        'views/estate_property_type_view.xml',
        'views/estate_property_tag_view.xml',
        'views/estate_property_view.xml',
        'views/estate_menu.xml',
        'views/estate_property_offer_view.xml',
    ]
    #'application': True,
}