from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    free_units = fields.Integer(compute='_compute_free_units', store=True)

    @api.depends('product_uom_qty', 'product_id')
    def _compute_free_units(self):
        for line in self:
            free_units = 0
            if not line.product_id:
                line.free_units = free_units
                continue

            promotions = self.env['promotion.promotion'].search([
                ('start_date', '<=', fields.Date.today()),
                ('end_date', '>=', fields.Date.today()),
                ('product_ids', 'in', line.product_id.id)
            ])
            _logger.debug("Found promotions: %s", promotions)
            for promo in promotions:
                for tier in promo.tier_ids:
                    if line.product_uom_qty >= tier.quantity:
                        free_units = max(free_units, tier.free_units)
                        _logger.debug("Promotion %s applicable with free units %s", promo.name, free_units)
            line.free_units = free_units
            _logger.debug("Computed free units: %s", free_units)
