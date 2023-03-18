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
    "depends": ["sale", "sale_order_tags_data"],
    "data": [
        "views/sale_order_tags.xml",
    ],
    "installable": True,
    "auto_install": False,
    "application": True,
    "license": "LGPL-3",
}
