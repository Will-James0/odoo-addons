from odoo import models, fields

class PromotionTier(models.Model):
    _name = 'promotion.tier'
    _description = 'Promotion Tier'

    quantity = fields.Integer('Quantity', required=True)
    free_units = fields.Integer('Free Units', required=True)
    promotion_id = fields.Many2one('promotion.promotion', string='Promotion', required=True, ondelete='cascade')