# Copyright 2026 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
from lxml import etree

from odoo.tests import TransactionCase, tagged


@tagged("post_install", "-at_install")
class TestL10nCyHideMarked(TransactionCase):
    """Скриване по име на кипърското в изгледите на фирма, която не е кипърска."""

    def _hide(self, arch, view_type="form"):
        doc = etree.fromstring(arch)
        self.env["res.partner"]._l10n_cy_hide_marked(doc, view_type)
        return doc

    def test_both_markers_start_the_name(self):
        doc = self._hide(
            '<form><field name="name"/><div name="l10n_cy_box"/>'
            '<div name="aade_box"/><group id="my_l10n_cy"/></form>'
        )
        self.assertEqual(doc.find("div[@name='l10n_cy_box']").get("invisible"), "True")
        self.assertIsNone(doc.find("div[@name='aade_box']").get("invisible"))
        self.assertIsNone(doc.find("group").get("invisible"))
        self.assertIsNone(doc.find("field").get("invisible"))

    def test_required_field_keeps_itself_and_its_container(self):
        self.patch(self.env["res.partner"]._fields["name"], "required", True)
        doc = self._hide('<form><group name="l10n_cy_group"><field name="name"/></group></form>')
        self.assertIsNone(doc.find("group").get("invisible"))

    def test_cypriot_company_detection(self):
        cy = self.env["res.company"].create({"name": "CY", "country_id": self.env.ref("base.cy").id})
        bg = self.env["res.company"].create({"name": "BG", "country_id": self.env.ref("base.bg").id})
        self.assertTrue(cy._l10n_cy_is_cypriot())
        self.assertFalse(bg._l10n_cy_is_cypriot())

    def test_get_view_hides_only_outside_cyprus(self):
        cy = self.env["res.company"].create({"name": "CY", "country_id": self.env.ref("base.cy").id})
        bg = self.env["res.company"].create({"name": "BG", "country_id": self.env.ref("base.bg").id})
        view = self.env["ir.ui.view"].create({
            "name": "test l10n_cy", "model": "res.partner", "type": "form",
            "arch": '<form><group name="l10n_cy_test"><field name="ref"/></group></form>',
        })
        def arch_for(company):
            Partner = self.env["res.partner"].with_company(company).with_context(allowed_company_ids=[company.id])
            return etree.fromstring(Partner.get_view(view.id, "form")["arch"])
        self.assertIsNone(arch_for(cy).find(".//group[@name='l10n_cy_test']").get("invisible"))
        self.assertEqual(arch_for(bg).find(".//group[@name='l10n_cy_test']").get("invisible"), "True")
