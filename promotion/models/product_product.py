from odoo import models, fields

class ProductProduct(models.Model):
    _inherit = 'product.product'

    promotion_ids = fields.Many2many('promotion.promotion', string='Promotions')
