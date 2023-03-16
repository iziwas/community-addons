""" Héritage de sale.order pour ajouter le calcul des tags """
import logging

from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = "sale.order"

    invoice_tag_ids = fields.Many2many(
        "crm.tag",
        "sale_order_invoice_crm_tag_rel",
        string="Invoice tags",
        compute="_compute_sale_order_tags",
        store=True
    )

    @api.depends('order_line.invoice_lines', 'order_line.invoice_lines.move_id.state')
    def _compute_sale_order_tags(self):
        facture_tag = self.env.ref("sale_order_tags.crm_tag_facture")
        avoir_partiel_tag = self.env.ref("sale_order_tags.crm_tag_avoir_partiel")
        avoir_integral_tag = self.env.ref("sale_order_tags.crm_tag_avoir_integral")

        for rec in self:
            res_tags = []
            amount_total_invoiced = sum(
                [
                    invoice.amount_total
                    for invoice in rec.order_line.invoice_lines.move_id.filtered(
                        lambda r: r.move_type == "out_invoice" and r.state == 'posted'
                    )
                ]
            )

            amount_total_refunded = sum(
                [
                    invoice.amount_total
                    for invoice in rec.order_line.invoice_lines.move_id.filtered(
                        lambda r: r.move_type == "out_refund" and r.state == 'posted'
                    )
                ]
            )

            # Ajout du tag `facture
            if amount_total_invoiced:
                res_tags.append(facture_tag.id)

            # Gestion des tags `avoir
            if amount_total_invoiced and amount_total_refunded:
                # Ajout du tag `avoir integral`
                if amount_total_refunded == amount_total_invoiced:
                    res_tags.append(avoir_integral_tag.id)
                else:
                    # Ajout du tag `avoir partiel`
                    if amount_total_refunded:
                        res_tags.append(avoir_partiel_tag.id)
            rec.invoice_tag_ids = [(6, 0, res_tags)]
