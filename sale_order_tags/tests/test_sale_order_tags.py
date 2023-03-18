# -*- coding: utf-8 -*-
from odoo.addons.sale.tests.test_sale_refund import TestSaleToInvoice
from odoo.tests import Form, tagged


@tagged("post_install", "-at_install", "sale_order_tags")
class TestSaleOrderTags(TestSaleToInvoice):
    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.invoice_tag = cls.env.ref("sale_order_tags_data.crm_invoice_tag")
        cls.partial_refund_tag = cls.env.ref("sale_order_tags_data.crm_partial_refund_tag")
        cls.full_refund_tag = cls.env.ref("sale_order_tags_data.crm_full_refund_tag")

    def test_sale_order_invoice_tag(self):
        """
        Invoice posted
            - Check if the SO have `invoice tag`
            - Check if SO doesn't have `full refund` and `partial refund` tags
        """
        # Validate invoice
        self.invoice.action_post()
        self.assertTrue(
            self.invoice_tag in self.sale_order.invoice_tag_ids,
            "Invoice tag should be present in this SO.",
        )
        self.assertTrue(
            self.partial_refund_tag not in self.sale_order.invoice_tag_ids,
            "Partial refund tag shouldn't be present in this SO.",
        )
        self.assertTrue(
            self.full_refund_tag not in self.sale_order.invoice_tag_ids,
            "Full refund tag shouldn't be present in this SO.",
        )

    def test_sale_order_full_refund_tag(self):
        """
        Invoice posted
            - Check if the SO have `invoice tag`
            - Check if SO doesn't have `partial refund` tag
            - Check if SO have `full refund tag`
        """
        self.test_refund_create()
        self.assertTrue(self.invoice_tag in self.sale_order.invoice_tag_ids)
        self.assertTrue(self.partial_refund_tag not in self.sale_order.invoice_tag_ids)
        self.assertTrue(self.full_refund_tag in self.sale_order.invoice_tag_ids)

    def test_sale_order_partial_refund_tag(self):
        """
        Invoice posted
            - Check if the SO have `invoice tag`
            - Check if SO have `partial refund` tag
            - Check if SO doesn't have `full refund tag`
        """
        self.test_refund_modify()
        self.assertTrue(self.invoice_tag in self.sale_order.invoice_tag_ids)
        self.assertTrue(self.partial_refund_tag in self.sale_order.invoice_tag_ids)
        self.assertTrue(self.full_refund_tag not in self.sale_order.invoice_tag_ids)
