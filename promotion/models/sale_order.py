from odoo import models, fields, api
import logging

from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    free_units = fields.Integer(compute='_compute_free_units', store=True)

    @api.depends('product_uom_qty', 'product_id', 'order_id.date_order')
    def _compute_free_units(self):
        for line in self:
            free_units = 0
            if not line.product_id or not line.order_id.date_order:
                line.free_units = free_units
                continue

            promotions = self.env['promotion.promotion'].search([
                ('start_date', '<=', line.order_id.date_order),
                ('end_date', '>=', line.order_id.date_order),
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


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def preview_sale_order(self):
        for order in self:
            order.order_line._compute_free_units()
        return super(SaleOrder, self).preview_sale_order()

    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        self._create_free_units_stock_moves()
        return res

    def _create_free_units_stock_moves(self):
        for order in self:
            for line in order.order_line:
                if line.free_units > 0:
                    self._create_stock_move_for_free_units(line)

    def _create_stock_move_for_free_units(self, line):
        stock_location_id = self.env['stock.location'].search([('usage', '=', 'internal')], limit=1).id
        stock_move_obj = self.env['stock.move']

        move_vals = {
            'name': line.name,
            'product_id': line.product_id.id,
            'product_uom_qty': line.free_units,
            'product_uom': line.product_uom.id,
            'location_id': stock_location_id,
            'location_dest_id': line.order_id.partner_shipping_id.property_stock_customer.id,
            'sale_line_id': line.id,
        }
        stock_move = stock_move_obj.create(move_vals)
        stock_move._action_confirm()
        stock_move._action_assign()
        stock_move._action_done()

    @api.model
    def create(self, vals):
        order = super(SaleOrder, self).create(vals)
        for line in order.order_line:
            line._compute_free_units()
        return order

    def action_confirm(self):
        self._check_stock_availability()
        res = super(SaleOrder, self).action_confirm()
        self._create_free_units_stock_moves()
        return res

    def _check_stock_availability(self):
        for order in self:
            for line in order.order_line:
                available_qty = line.product_id.qty_available
                required_qty = line.product_uom_qty + line.free_units
                if available_qty < required_qty:
                    raise UserError(
                        f"Not enough stock for {line.product_id.name}. Available: {available_qty}, Required: {required_qty}")