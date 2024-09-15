# -*- coding: utf-8 -*-
# Part of Jet. See LICENSE file for full copyright and licensing details.

from odoo import fields, models
class estate_property_tag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate property tag"
    _order = "name"

    name = fields.Char('Name', required=True)
    color = fields.Integer('Color')
    _sql_constraints = [('check_name_unique','UNIQUE(name)','The Name must be unique.')]
