# check_json_consistency.py — Specification Notes

## Purpose
Checks `src/draft-wullink-rpp-json.md` for consistency between JSON examples and JSON schemas.

## Source file
`src/draft-wullink-rpp-json.md` — a Mmark/IETF Internet-Draft in Markdown.

## Three named top-level chapters (by `# Heading` level)

| Chapter title                  | Content type                                              |
|-------------------------------|-----------------------------------------------------------|
| `JSON Representation Rules`   | JSON snippets (invalid/partial JSON) — listed, not validated |
| `JSON Schema Definitions`     | JSON Schema definitions — validated                       |
| `Examples`                    | Full JSON object examples — validated                     |

Any ` ```json ` block outside these three chapters is flagged as "other".

---

## Section 2 — JSON Schema Definitions

### Sub-chapter classification

Each schema block belongs to a level-2 sub-chapter of `JSON Schema Definitions`.
The sub-chapter determines what `@type` rules apply:

| Sub-chapter                   | `@type` rule | Example coverage required      |
|------------------------------|--------------|-------------------------------|
| `Common Data Types Schemas`  | **forbidden** — error if present | none (no `@type`, no example check) |
| `Component Objects Schemas`  | **required** — error if missing  | nested (at any depth in any example) |
| `Process Object Schemas`     | **required** — error if missing  | top-level example required     |
| `Domain Name Data Object`    | **required** — error if missing  | top-level example required     |
| `Contact Data Object`        | **required** — error if missing  | top-level example required     |
| `Host Data Object`           | **required** — error if missing  | top-level example required     |
| `Organisation Data Object`   | **required** — error if missing  | top-level example required     |

### Rules checked per schema block
- Must be valid JSON
- Must contain `$defs` with **exactly one** named definition
- `@type` rule per sub-chapter (see table above):
  - `forbidden`: `@type` property MUST NOT appear in the definition — **error** if present
  - `required`: `@type` property MUST appear with `"type": "string"` and a `"const"` value — **error** if missing or malformed
    - Deep check (default, disable with `--no-deep-type-check`): if `@type` is not in top-level `properties`, the script traverses `allOf`/`anyOf`/`oneOf` and follows `$ref` pointers to locate it:
      - `allOf`: at least one branch must define/constrain `@type`
      - `anyOf`/`oneOf`: **all** branches must define/constrain `@type`
      - `$ref`: followed into the combined `$defs` (cycle-safe)
- All `$ref: #/$defs/<name>` pointers are checked against the combined `$defs` map — **error** if unresolved
- Schema must be a valid JSON Schema (draft 2020-12) — `check_schema()` is called
- Cross-references are resolved by merging all schemas into one combined `$defs` map

---

## Section 3 — Examples

### Rules checked per example block
- Must be valid JSON
- Must have a top-level `"@type"` property — **error** if missing
- Must have at least one matching schema (matched by `@type` value == schema's `@type` const) — **error** if none found
- Schemas with unresolved `$ref`s are skipped for validation (already flagged in section 2); if all matching schemas are skipped, validation is marked as not possible
- Must validate against at least one matching schema — **error** if all fail; **warning** if some fail but at least one passes

---

## Section 4 — Typed schemas without examples

For each schema with a `@type` const, example coverage is checked according to the sub-chapter rule (see table above):

- **Top-level required** (Process Objects, Data Objects): the `@type` value must appear as the top-level `"@type"` of at least one example — **error** if missing
- **Nested sufficient** (Component Objects): the `@type` value must appear at any depth in any example — **warning** if missing

---

## Running the script
```bash
# From project root, using the bundled venv:
.scripts/.venv/bin/python .scripts/check_json_consistency.py

# Quiet mode — suppress OK/info lines; >> location markers always shown:
.scripts/.venv/bin/python .scripts/check_json_consistency.py -q

# Disable deep @type traversal via allOf/anyOf/oneOf/$ref:
.scripts/.venv/bin/python .scripts/check_json_consistency.py --no-deep-type-check

# Custom file path:
.scripts/.venv/bin/python .scripts/check_json_consistency.py path/to/file.md
```

## Dependencies
- Python 3.10+
- `jsonschema` 4.x (installed in `.scripts/.venv`)

## Exit codes
- `0` — no errors (warnings may still be present)
- `1` — one or more errors found
