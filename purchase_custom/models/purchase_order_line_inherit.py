from random import random
import random

from odoo import models, fields, api


class InheritPurchaseOrder(models.Model):
    _inherit = 'purchase.order.line'
    _description = 'extend purchase order line'
    # 'res.partner'
    recommended_supplier = fields.Many2one('res.partner')

    @api.onchange('product_id')
    def auto_update(self):
        for rec in self:
            rec.recommended_supplier = 1
            if rec.product_id.seller_ids:
                min_price = rec.product_id.seller_ids[0].price
                min_delivery_lead_time = rec.product_id.seller_ids[0].delay
                list_recommended_supplier = []

                for seller in rec.product_id.seller_ids:
                    if min_price >= seller.price:
                        min_price = seller.price
                        if min_delivery_lead_time >= seller.delay:
                            min_delivery_lead_time = seller.delay
                            # print(seller.delay, seller.name.name)
                count = 0
                for sell in rec.product_id.seller_ids:
                    if sell.delay == min_delivery_lead_time and min_price == sell.price:
                        count += 1
                        list_recommended_supplier.append(sell.name)

                if count == 1:
                    rec.recommended_supplier = list_recommended_supplier[0]
                else:
                    rec.recommended_supplier = random.choice(list_recommended_supplier)

