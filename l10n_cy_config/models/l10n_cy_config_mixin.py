# Copyright 2026 Rosen Vladimirov
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl).
import re

from lxml import etree

from odoo import api, fields, models


class L10nCyConfigMixin(models.AbstractModel):
    """Скриване по име на кипърското в изгледа на фирма, която не е кипърска.

    Правилата са като в l10n_bg_config: маркерът ЗАПОЧВА с един от префиксите;
    поле — по името му, всеки друг елемент — по id или name; задължителните
    полета (required) и контейнерът с такова поле на същия запис не се гасят.
    """

    _name = "l10n.cy.config.mixin"
    _description = "Mixin hiding Cypriot-only elements for non-Cypriot companies"

    _l10n_cy_markers = ("l10n_cy",)

    is_l10n_cy_record = fields.Boolean(
        string="Is Cypriot Record",
        compute="_compute_is_l10n_cy_record",
    )

    @api.depends_context("company")
    def _compute_is_l10n_cy_record(self):
        has_company = "company_id" in self._fields
        for record in self:
            company = (has_company and record.company_id) or record.env.company
            record.is_l10n_cy_record = company._l10n_cy_is_cypriot()

    @api.model
    def get_view(self, view_id=None, view_type="form", **options):
        result = super().get_view(view_id=view_id, view_type=view_type, **options)
        if self.env.company._l10n_cy_is_cypriot():
            return result
        doc = etree.fromstring(result["arch"])
        if self._l10n_cy_hide_marked(doc, view_type):
            result["arch"] = etree.tostring(doc)
        return result

    @api.model
    def fields_get(self, allfields=None, attributes=None):
        """Справките на не-кипърска фирма не предлагат маркираните полета.

        „Групиране по → собствено“, полето в „Добави филтър“ и мерките на
        pivot/graph идват от fields_get, не от изгледа — get_view не ги
        стига. Полетата остават в отговора (формите и списъците ги искат),
        само им се свалят флаговете, по които клиентът ги предлага.
        """
        result = super().fields_get(allfields=allfields, attributes=attributes)
        if not self.env.company._l10n_cy_is_cypriot():
            self._l10n_cy_unoffer_marked(result)
        return result

    def _l10n_cy_unoffer_marked(self, descriptions):
        for name, desc in descriptions.items():
            if not self._l10n_cy_is_marked(name):
                continue
            for flag in ("groupable", "searchable"):
                if flag in desc:
                    desc[flag] = False
            if "aggregator" in desc:
                desc["aggregator"] = None

    def _l10n_cy_is_marked(self, value):
        return bool(value) and value.startswith(self._l10n_cy_markers)

    def _l10n_cy_node_model(self, node):
        chain = [
            anc.get("name")
            for anc in reversed(list(node.iterancestors()))
            if anc.tag == "field" and anc.get("name")
        ]
        model = self._name
        for name in chain:
            field = self.env[model]._fields.get(name)
            if not field or not field.comodel_name:
                return None
            model = field.comodel_name
        return model

    def _l10n_cy_field_required(self, node):
        if node.get("required") in ("1", "True", "true"):
            return True
        model = self._l10n_cy_node_model(node)
        field = model and self.env[model]._fields.get(node.get("name"))
        return bool(field and field.required)

    def _l10n_cy_hide_marked(self, doc, view_type):
        """Скрива маркираните възли в doc; връща True, ако нещо е променено."""
        changed = False
        if view_type == "search":
            token = re.compile(r"""['"](%s)""" % "|".join(self._l10n_cy_markers))
            for node in doc.iter("field", "filter"):
                if (
                    self._l10n_cy_is_marked(node.get("name"))
                    or token.search(node.get("domain") or "")
                    or token.search(node.get("context") or "")
                ):
                    node.set("invisible", "True")
                    changed = True
            return changed

        hidden_fields = set()
        for node in doc.iter():
            if not isinstance(node.tag, str) or node is doc:
                continue
            if node.tag == "field":
                if not self._l10n_cy_is_marked(node.get("name")) or self._l10n_cy_field_required(node):
                    continue
                in_list = view_type == "list" or any(anc.tag == "list" for anc in node.iterancestors())
                node.set("column_invisible" if in_list else "invisible", "True")
                hidden_fields.add(node.get("name"))
                changed = True
            elif node.tag != "label" and (
                self._l10n_cy_is_marked(node.get("id")) or self._l10n_cy_is_marked(node.get("name"))
            ):
                # само задължително поле на СЪЩИЯ запис пази контейнера
                if any(
                    not any(anc.tag == "field" for anc in f.iterancestors())
                    and self._l10n_cy_field_required(f)
                    for f in node.iter("field")
                ):
                    continue
                node.set("invisible", "True")
                changed = True
        for label in doc.iter("label"):
            if label.get("for") in hidden_fields:
                label.set("invisible", "True")
                changed = True
        return changed
