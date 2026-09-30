# Copyright 2026 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import models


class ResCompany(models.Model):
    _inherit = "res.company"

    def _l10n_cy_is_cypriot(self):
        """Кипърска фирма — по фискалната държава, иначе по държавата на фирмата."""
        self.ensure_one()
        country = self.account_fiscal_country_id or self.country_id
        return country.code == "CY"
