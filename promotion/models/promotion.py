from odoo import models, fields

class Promotion(models.Model):
    _name = 'promotion.promotion'
    _description = 'Promotion'

    name = fields.Char('Promotion Name', required=True)
    start_date = fields.Date('Start Date', required=True)
    end_date = fields.Date('End Date', required=True)
    tier_ids = fields.One2many('promotion.tier', 'promotion_id', string='Tiers')
    product_ids = fields.Many2many('product.product', string='Applicable Products')
