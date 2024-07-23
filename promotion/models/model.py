from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class AccountMoveLine(models.Model):
    _inherit = 'account.move.line'

    free_units = fields.Integer(compute='_compute_free_units', store=True)

    @api.depends('quantity', 'move_id.invoice_date', 'product_id')
    def _compute_free_units(self):
        for line in self:
            free_units = 0
            if not line.product_id or not line.move_id.invoice_date:
                line.free_units = free_units
                continue

            promotions = self.env['promotion.promotion'].search([
                ('start_date', '<=', line.move_id.invoice_date),
                ('end_date', '>=', line.move_id.invoice_date),
                ('product_ids', 'in', [line.product_id.id])
            ])
            _logger.debug("Found promotions: %s", promotions)
            for promo in promotions:
                for tier in promo.tier_ids:
                    if line.quantity and line.quantity >= tier.quantity:
                        free_units = max(free_units, tier.free_units)
                        _logger.debug("Promotion %s applicable with free units %s", promo.name, free_units)
            line.free_units = free_units
            _logger.debug("Computed free units: %s", free_units)
