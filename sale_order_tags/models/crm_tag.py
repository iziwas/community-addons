from odoo import _, fields, models
from odoo.exceptions import UserError


class SaleOrderTagsData(models.Model):
    _inherit = "crm.tag"

    can_be_deleted = fields.Boolean("Can be deleted", default=True)

    def unlink(self):
        for rec in self:
            if not rec.can_be_deleted:
                raise UserError(_("This item can't be deleted."))
            super(SaleOrderTagsData, rec).unlink()
