# -*- coding: utf-8 -*-
# Part of Jet. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from datetime import timedelta
from odoo.exceptions import ValidationError
class estate_property_offer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _order = "price desc"

    price = fields.Float('Price', required=True)
    status = fields.Selection(
        string='Status' ,
        selection=[('accepted','Accepted'), ('refused','Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True, ondelete='cascade')
    validity = fields.Integer('Validity', default = 7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline')
    property_type_id = fields.Many2one(related="property_id.property_type_id" , store=True) # 作為統計連結按鈕使用 #

    _sql_constraints = [
        ('check_price3','CHECK(price >= 0)','The price must be positive.')
    ]

    @api.depends('create_date','validity')
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + timedelta(days=offer.validity)
            else:
                offer.date_deadline = fields.Datetime.today() + timedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            if offer.date_deadline and offer.create_date:
                offer.validity = (offer.date_deadline - offer.create_date.date()).days
            else:
                offer.validity = 0

    def action_accept(self):
        if self.status == 'accepted':
            return
        self.write({'status': 'accepted'})
        # Consider using `write` on the related record or a dedicated method
        self.property_id.write({'selling_price': self.price})
        self.property_id.write({'buyer_id': self.partner_id.id})

    def action_refuse(self):
        if self.status == 'refused':
            return
        self.write({'status': 'refused'})

    # def create(self, vals):
    #     if 'price' in vals and 'property_id' in vals:
    #         property = self.env['estate.property'].browse(vals['property_id'])
    #     # 直接在這裡檢查 best_price
    #         if property.best_price and vals['price'] <= property.best_price:
    #             raise ValidationError('The offer price cannot be lower than or equal to the best offer price.')

    # # 其他 create 方法的邏輯
    #     return super(estate_property_offer, self).create(vals)
    
    def create(self, vals):
        # 檢查是否提供 price 和 property_id
        if 'price' in vals and 'property_id' in vals:
            property = self.env['estate.property'].browse(vals['property_id'])
            property._compute_best_offer()

            # 檢查是否為最高報價
            if property.best_price and vals['price'] <= property.best_price:
                raise ValidationError("新的報價必須高於現有的最佳報價。")

            # 如果是新的最佳報價，則更新 property 的狀態和最佳價格
            if property.best_price is None or vals['price'] > property.best_price:
                property.write({'state': 'offer_received', 'best_price': vals['price']})

        # 呼叫父類別的 create 方法，完成記錄的建立
        return super(estate_property_offer, self).create(vals)