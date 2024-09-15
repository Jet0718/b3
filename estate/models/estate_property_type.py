# -*- coding: utf-8 -*-
# Part of Jet. See LICENSE file for full copyright and licensing details.

from odoo import api,fields, models

class estate_property_type(models.Model):
    _name = "estate.property.type"
    _description = "Estate Property Type"
    _order = "name"

    sequence = fields.Integer('Sequence', default = 1, help = '作為排序使用')
    name = fields.Char('Name', required=True)
    property_ids = fields.One2many("estate.property","property_type_id", string="Properties")
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id', string='Offers')
    offer_count = fields.Integer(compute="_compute_offers_count")
    _sql_constraints = [('check_name_unique','UNIQUE(name)','The Name must be unique.')]

    @api.depends("offer_ids")
    def _compute_offers_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
