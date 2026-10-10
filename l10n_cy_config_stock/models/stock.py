# Copyright 2026 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import models

# Мостът: скриването на l10n_cy* полетата в чужда фирма — само там,
# където има модула (l10n_*_config зависи само от account).


class StockPicking(models.Model):
    _inherit = ["stock.picking", "l10n.cy.config.mixin"]
    _name = "stock.picking"
