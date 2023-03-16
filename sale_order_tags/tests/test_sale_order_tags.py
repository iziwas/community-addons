# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo.tests import Form, tagged
from odoo.addons.sale.tests.test_sale_refund import TestSaleToInvoice


@tagged('post_install', '-at_install', 'sale_order_tags')
class TestSaleOrderTags(TestSaleToInvoice):

    @classmethod
    def setUpClass(cls, chart_template_ref=None):
        super().setUpClass(chart_template_ref=chart_template_ref)
        cls.facture_tag = cls.env.ref('sale_order_tags.crm_tag_facture')
        cls.avoir_partiel_tag = cls.env.ref('sale_order_tags.crm_tag_avoir_partiel')
        cls.avoir_integral_tag = cls.env.ref('sale_order_tags.crm_tag_avoir_integral')

    def test_sale_order_invoice_tag(self):
        """
        Création d'une facture
            - Vérification que la facture ait bien le tag 'Facture'
            - Vérification sur le fait que les tags `avoir partiel` et `avoir total` soient absents
        """
        # Validate invoice
        self.invoice.action_post()
        self.assertTrue(self.facture_tag in self.sale_order.invoice_tag_ids, "Le tag `facture` devrait être présent.")
        self.assertTrue(
            self.avoir_partiel_tag not in self.sale_order.invoice_tag_ids,
            "Le tag `avoir partiel` doit être absent."
        )
        self.assertTrue(
            self.avoir_integral_tag not in self.sale_order.invoice_tag_ids,
            "Le tag `avoir intégral` doit être absent."
        )

    def test_sale_order_refund_tag(self):
        """
        Création d'une facture
            - Vérification que la facture possède le tag 'Facture'
            - Vérification que la facture n'ait pas le tag `avoir partiel`
            - Vérification que la facture possède le tag `avoir total`
        """
        self.test_refund_create()
        self.assertTrue(self.facture_tag in self.sale_order.invoice_tag_ids)
        self.assertTrue(self.avoir_partiel_tag not in self.sale_order.invoice_tag_ids)
        self.assertTrue(self.avoir_integral_tag in self.sale_order.invoice_tag_ids)

