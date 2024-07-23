from odoo import models, api

class AccountMove(models.Model):
    _inherit = 'account.move'

    def preview_invoice(self):
        for move in self:
            move.invoice_line_ids._compute_free_units()
        return super(AccountMove, self).preview_invoice()
