# -*- coding: utf-8 -*-
# Part of Jet. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero

class estate_property(models.Model):
    _name = "estate.property"
    _description = "Real Estate property"
    _order = "id desc"

    name = fields.Char('Name', required=True)
    description = fields.Text('Description', required=False)
    postcode = fields.Char('Postcode', required=False)
    date_availability = fields.Date(string='Date availability', copy=False, default=lambda self: fields.Datetime.today() + timedelta(days=90))
    expected_price = fields.Float('Expected Price')
    selling_price = fields.Float('Selling Price' , readonly=True, copy=False)
    bedrooms = fields.Integer('Bedrooms', default= 2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('east','東'), ('west','西'),('south','南'),('north','北')],
        help="Type is used to which orientation for garden"
    )
    active = fields.Boolean(string='Active', default=True, copy=False)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold','Sold'), ('canceled','Canceled')], 
        default='new', 
        copy=False
    )
    property_type_id = fields.Many2one('estate.property.type', string='Type')
    property_tag_ids = fields.Many2many('estate.property.tag', string='Tag')
    buyer_id = fields.Many2one('res.partner', string='Buyer', copy=False)
    user_id = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    offer_ids = fields.One2many('estate.property.offer','property_id', string='Offers')
    total_area = fields.Integer('Total Area', compute='_compute_total_area')
    best_price = fields.Float('Best Offer', compute='_compute_best_offer')
    #sequence = fields.Integer('Sequence', default=1, help="作為排序使用")

    _sql_constraints = [
        ('check_price3','CHECK(expected_price >= 0 AND selling_price >= 0)','The price of Expected and Selling must be positive.')
    ]

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for property in self:
            property.total_area = property.living_area + property.garden_area

    @api.depends('offer_ids')
    def _compute_best_offer(self):
        for property in self:
            property.best_price = max(property.offer_ids.mapped('price'), default=0.0)
            #property.state = 'offer_received'
            #property.write({'state': 'offer_received'})

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = None
            self.garden_orientation = None

    def action_set_lost(self):
        if self.state != 'sold':
            self.write({'state': 'canceled'})
        else:
            raise ValidationError('Sold properties cannot be canceled.')

    def action_set_sold(self):
        if self.state != 'canceled':
            self.write({'state': 'sold'})
        else:
            raise ValidationError('Canceled properties cannot be sold.')
        
    @api.constrains('expected_price','selling_price')
    def _check_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price,0):
                return
            elif float_compare(record.selling_price , record.expected_price * 0.9 , 1) < 0:
                raise ValidationError('The Selling Price must be greater than 90% of Expected price.')
    
    def unlink(self):
        for record in self:
            res = record.state not in ['new','canceled']
            if res:
                raise ValidationError("只能刪除狀態為new或canceled的記錄")
        return super(estate_property,self).unlink()

