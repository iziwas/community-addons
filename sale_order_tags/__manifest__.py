# -*- coding: utf-8 -*-
{
    "name": "Sale Order Tags",
    "category": "Sales/Sales",
    "version": "14.0.1.0.0",
    "description": """
Sale Order Tags
===============
Tools to add automatically tags if account.invoice is paid or not
    """,
    "depends": ["sale"],
    "data": [
        "data/crm_tag.xml",
        "views/sale_order.xml",
        "views/crm_tag.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "license": "LGPL-3",
}
