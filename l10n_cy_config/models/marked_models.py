# Copyright 2026 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from odoo import models

# основните модели, на които кипърски модули биха сложили полета (l10n_cy).
# В Odoo 19 _inherit със списък без _name дава модел по името на класа —
# затова _name е изрично навсякъде.


class AccountMove(models.Model):
    _inherit = ["account.move", "l10n.cy.config.mixin"]
    _name = "account.move"


class AccountJournal(models.Model):
    _inherit = ["account.journal", "l10n.cy.config.mixin"]
    _name = "account.journal"


class AccountAccount(models.Model):
    _inherit = ["account.account", "l10n.cy.config.mixin"]
    _name = "account.account"


class AccountFiscalPosition(models.Model):
    _inherit = ["account.fiscal.position", "l10n.cy.config.mixin"]
    _name = "account.fiscal.position"


class AccountBankStatementLine(models.Model):
    _inherit = ["account.bank.statement.line", "l10n.cy.config.mixin"]
    _name = "account.bank.statement.line"


class ResPartner(models.Model):
    _inherit = ["res.partner", "l10n.cy.config.mixin"]
    _name = "res.partner"


class ResUsers(models.Model):
    _inherit = ["res.users", "l10n.cy.config.mixin"]
    _name = "res.users"


class ResCompanyMarked(models.Model):
    _inherit = ["res.company", "l10n.cy.config.mixin"]
    _name = "res.company"


class ResConfigSettings(models.TransientModel):
    _inherit = ["res.config.settings", "l10n.cy.config.mixin"]
    _name = "res.config.settings"
