Hides Cypriot-only elements in the views of companies that are not Cypriot.

A field is hidden by its name, any other element (group, page, div, setting,
block, button, separator) by its `id` or `name`, when the value starts with
`l10n_cy`. Required fields stay visible, and so does a container holding a
required field of the same record.

A company is Cypriot when its fiscal country (or, failing that, its country) is
Cyprus. This is a user-interface filter, not an access right: RPC, exports and
reports still see the fields.
