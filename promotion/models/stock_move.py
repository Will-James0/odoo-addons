from odoo import models, fields, api

class StockMove(models.Model):
    _inherit = 'stock.move'

    free_units = fields.Integer('Free Units')

    @api.model
    def create(self, vals):
        # Calculez les unités gratuites ici si nécessaire
        if 'product_id' in vals and 'product_uom_qty' in vals:
            product_id = vals['product_id']
            product_qty = vals['product_uom_qty']
            promotions = self.env['promotion.promotion'].search([
                ('start_date', '<=', fields.Date.today()),
                ('end_date', '>=', fields.Date.today()),
                ('product_ids', 'in', product_id)
            ])
            free_units = 0
            for promo in promotions:
                for tier in promo.tier_ids:
                    if isinstance(product_qty, int) and product_qty >= tier.quantity:
                        free_units = max(free_units, tier.free_units)
            vals['free_units'] = free_units
        return super(StockMove, self).create(vals)

    @api.depends('product_uom_qty', 'free_units')
    def _compute_total_qty(self):
        for move in self:
            move.total_qty = move.product_uom_qty + move.free_units

    total_qty = fields.Float(compute='_compute_total_qty', string='Total Quantity')
