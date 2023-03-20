from odoo import api, fields, models


class SaleOrderTags(models.Model):
    _inherit = "sale.order"

    invoice_tag_ids = fields.Many2many(
        "crm.tag",
        "sale_order_invoice_crm_tag_rel",
        string="Invoice tags",
        compute="_compute_sale_order_tags",
        store=True,
    )

    @api.depends("order_line.invoice_lines", "order_line.invoice_lines.move_id.state")
    def _compute_sale_order_tags(self):
        invoice_tag = self.env.ref("sale_order_tags_data.crm_invoice_tag", False)
        partial_refund_tag = self.env.ref("sale_order_tags_data.crm_partial_refund_tag", False)
        full_refund_tag = self.env.ref("sale_order_tags_data.crm_full_refund_tag", False)

        for rec in self:
            res_tags = []
            amount_total_invoiced = sum(
                [
                    invoice.amount_total
                    for invoice in rec.order_line.invoice_lines.move_id.filtered(
                        lambda r: r.move_type == "out_invoice" and r.state == "posted"
                    )
                ]
            )

            amount_total_refunded = sum(
                [
                    invoice.amount_total
                    for invoice in rec.order_line.invoice_lines.move_id.filtered(
                        lambda r: r.move_type == "out_refund" and r.state == "posted"
                    )
                ]
            )

            # Add invoice tag
            if amount_total_invoiced:
                res_tags.append(invoice_tag.id)

            # Refund tags
            if amount_total_invoiced and amount_total_refunded:
                # Add full refund tag if amount_total_invoice and amount_total_refunded have the same value.
                if amount_total_refunded == amount_total_invoiced:
                    res_tags.append(full_refund_tag.id)
                else:
                    # Partial refund tag
                    if amount_total_refunded:
                        res_tags.append(partial_refund_tag.id)
            rec.invoice_tag_ids = [(6, 0, res_tags)]
