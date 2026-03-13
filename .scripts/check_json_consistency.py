#!/usr/bin/env python3
"""
check_json_consistency.py

Checks src/draft-wullink-rpp-json.md for consistency of JSON examples and schemas.

Usage:
    python3 check_json_consistency.py [path/to/draft-wullink-rpp-json.md]

See .scripts/check_json_consistency_spec.md for specification notes.
"""

import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Optional

try:
    import jsonschema
    from jsonschema import Draft202012Validator
    from jsonschema.exceptions import SchemaError, ValidationError
except ImportError:
    print("ERROR: jsonschema not installed. Run: pip install jsonschema")
    sys.exit(1)

try:
    import referencing
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012
    HAS_REFERENCING = True
except ImportError:
    HAS_REFERENCING = False


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class JsonBlock:
    """Represents a ```json ... ``` block found in the markdown."""
    line_start: int
    line_end: int
    raw: str
    chapter_path: list  # list[str]
    caption: str        # last non-empty non-fence line before the block


@dataclass
class SchemaEntry:
    block: JsonBlock
    def_name: str             # name inside $defs (or "<missing>" etc)
    type_const: Optional[str] # value of @type const, or None
    schema: dict              # the parsed schema JSON object
    subchapter: str           # level-2 section name within JSON Schema Definitions


@dataclass
class ExampleEntry:
    block: JsonBlock
    section: str              # section title path
    caption: str
    obj: Optional[dict]       # None if JSON parsing failed
    type_value: Optional[str] # value of top-level @type


# ---------------------------------------------------------------------------
# Markdown parsing
# ---------------------------------------------------------------------------

TOP_LEVEL_CHAPTER_JSON_REPRESENTATION_RULES = "JSON Representation Rules"
TOP_LEVEL_CHAPTER_JSON_SCHEMA_DEFINITIONS   = "JSON Schema Definitions"
TOP_LEVEL_CHAPTER_EXAMPLES                  = "Examples"

# Sub-chapters of JSON Schema Definitions and their @type requirements.
# "forbidden" = @type MUST NOT be present (error if present)
# "required"  = @type MUST be present with a const value (error if missing)
SCHEMA_SUBCHAPTER_TYPE_RULES: dict[str, str] = {
    "Common Data Types Schemas": "forbidden",
    "Component Objects Schemas": "required",
    "Process Object Schemas":    "required",
    "Domain Name Data Object":   "required",
    "Contact Data Object":       "required",
    "Host Data Object":          "required",
    "Organisation Data Object":  "required",
}

# Which subchapters require a top-level example (the @type must appear as the
# top-level "@type" of an example object).  All other "required" subchapters
# only need the @type to appear somewhere (at any depth) in any example.
SCHEMA_SUBCHAPTER_NEEDS_TOPLEVEL_EXAMPLE: set[str] = {
    "Process Object Schemas",
    "Domain Name Data Object",
    "Contact Data Object",
    "Host Data Object",
    "Organisation Data Object",
}


def parse_markdown(md_path: Path):
    """
    Parse the markdown file and return:
      - snippets:       JsonBlock list  (in "JSON Representation Rules")
      - schema_entries: SchemaEntry list (in "JSON Schema Definitions")
      - example_entries: ExampleEntry list (in "Examples")
      - other_blocks:   JsonBlock list  (everywhere else)
    """
    lines = md_path.read_text(encoding="utf-8").splitlines()
    heading_re = re.compile(r'^(#{1,6})\s+(.*?)\s*$')

    # Pass 1: build a per-line chapter-path array
    chapter_paths = []
    heading_stack = []  # list of (level, title)
    for line in lines:
        m = heading_re.match(line)
        if m:
            level = len(m.group(1))
            title = re.sub(r'^[.#]+\s*', '', m.group(2)).strip()
            while heading_stack and heading_stack[-1][0] >= level:
                heading_stack.pop()
            heading_stack.append((level, title))
        chapter_paths.append([t for _, t in heading_stack])

    # Pass 2: collect ```json ... ``` blocks
    blocks: list[JsonBlock] = []
    i = 0
    while i < len(lines):
        if lines[i].strip() == '```json':
            block_start = i
            block_lines = []
            i += 1
            while i < len(lines) and lines[i].strip() != '```':
                block_lines.append(lines[i])
                i += 1
            raw = "\n".join(block_lines)

            # Caption: last non-empty, non-heading, non-fence line before block
            caption = ""
            for j in range(block_start - 1, -1, -1):
                s = lines[j].strip()
                if s and not s.startswith('#') and not s.startswith('```'):
                    caption = s
                    break

            blocks.append(JsonBlock(
                line_start=block_start + 1,  # 1-based
                line_end=i + 1,
                raw=raw,
                chapter_path=chapter_paths[block_start][:],
                caption=caption,
            ))
        i += 1

    # Classify blocks
    snippets: list[JsonBlock]         = []
    schema_entries: list[SchemaEntry] = []
    example_entries: list[ExampleEntry] = []
    other_blocks: list[JsonBlock]     = []

    for blk in blocks:
        tlc = blk.chapter_path[0] if blk.chapter_path else ""

        if tlc == TOP_LEVEL_CHAPTER_JSON_REPRESENTATION_RULES:
            snippets.append(blk)

        elif tlc == TOP_LEVEL_CHAPTER_JSON_SCHEMA_DEFINITIONS:
            entry = _try_parse_schema(blk)
            schema_entries.append(entry)

        elif tlc == TOP_LEVEL_CHAPTER_EXAMPLES:
            section = " > ".join(blk.chapter_path[1:]) if len(blk.chapter_path) > 1 else ""
            example_entries.append(_parse_example(blk, section))

        else:
            other_blocks.append(blk)

    return snippets, schema_entries, example_entries, other_blocks


def _try_parse_schema(blk: JsonBlock) -> SchemaEntry:
    # Determine subchapter: level-2 heading within "JSON Schema Definitions"
    subchapter = blk.chapter_path[1] if len(blk.chapter_path) > 1 else ""

    try:
        obj = json.loads(blk.raw)
    except json.JSONDecodeError as e:
        return SchemaEntry(block=blk, def_name=f"<JSON parse error: {e}>",
                           type_const=None, schema={}, subchapter=subchapter)

    defs = obj.get("$defs", {})
    if not isinstance(defs, dict) or len(defs) != 1:
        return SchemaEntry(block=blk,
                           def_name=f"<$defs has {len(defs) if isinstance(defs,dict) else 'non-object'} entries>",
                           type_const=None, schema=obj, subchapter=subchapter)

    def_name = next(iter(defs))
    defn = defs[def_name]
    type_const = None
    props = defn.get("properties", {}) if isinstance(defn, dict) else {}
    if "@type" in props and isinstance(props["@type"], dict):
        type_const = props["@type"].get("const")

    return SchemaEntry(block=blk, def_name=def_name, type_const=type_const,
                       schema=obj, subchapter=subchapter)


def _parse_example(blk: JsonBlock, section: str) -> ExampleEntry:
    try:
        obj = json.loads(blk.raw)
    except json.JSONDecodeError:
        obj = None
    type_value = obj.get("@type") if isinstance(obj, dict) else None
    return ExampleEntry(block=blk, section=section, caption=blk.caption,
                        obj=obj, type_value=type_value)


# ---------------------------------------------------------------------------
# Schema validation helpers
# ---------------------------------------------------------------------------

def build_combined_schema(schema_entries: list) -> dict:
    """
    Merge all $defs from every schema entry into one combined document.
    This lets cross-references ($ref: #/$defs/foo) resolve across schemas.
    """
    combined: dict = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$defs": {}
    }
    for entry in schema_entries:
        defs = entry.schema.get("$defs", {})
        if isinstance(defs, dict):
            combined["$defs"].update(defs)
    return combined


def make_validator(schema_fragment: dict, combined_schema: dict) -> Draft202012Validator:
    """
    Build a Draft202012Validator for `schema_fragment` with access to all
    $defs from `combined_schema` for resolving $ref pointers.
    """
    # Embed the combined $defs into the schema fragment so all cross-refs resolve.
    # We must not mutate the originals, so merge into a fresh dict.
    merged = dict(schema_fragment)
    merged_defs = dict(combined_schema.get("$defs", {}))
    # The schema_fragment's own $defs take priority (override)
    merged_defs.update(schema_fragment.get("$defs", {}))
    merged["$defs"] = merged_defs
    merged["unevaluatedProperties"] = False
    merged["$schema"] = "https://json-schema.org/draft/2020-12/schema"

    return Draft202012Validator(merged)


def schema_find_type_const(defn: dict, all_defs: dict, _seen: Optional[set] = None) -> Optional[str]:
    """
    Return the '@type' const value if `defn` defines or constrains an "@type" property,
    considering:
    - Direct "properties": {"@type": ...} at the top level of defn
    - allOf: at least one branch defines/constrains "@type" (or is a $ref that does)
    - anyOf / oneOf: all branches define/constrain "@type" (or are $ref that do)
    - $ref: follows the reference into all_defs (cycle-safe)

    Returns None if no @type const is found. This is used when `--deep-type-check` is active.
    """
    if _seen is None:
        _seen = set()
    if not isinstance(defn, dict):
        return None

    # Follow $ref
    ref = defn.get("$ref")
    if ref:
        m = re.match(r'^#/\$defs/(.+)$', ref)
        if m:
            name = m.group(1)
            if name in _seen:
                return None  # cycle guard
            target = all_defs.get(name)
            if target:
                return schema_find_type_const(target, all_defs, _seen | {name})
        return None

    # Direct properties
    props = defn.get("properties", {})
    if isinstance(props, dict) and "@type" in props:
        tp = props["@type"]
        return tp.get("const") if isinstance(tp, dict) else None

    # allOf: return const from the first branch that has one
    all_of = defn.get("allOf")
    if isinstance(all_of, list) and all_of:
        for branch in all_of:
            val = schema_find_type_const(branch, all_defs, _seen)
            if val is not None:
                return val

    # anyOf / oneOf: return const only if all branches agree on the same value
    for keyword in ("anyOf", "oneOf"):
        branches = defn.get(keyword)
        if isinstance(branches, list) and branches:
            values = [schema_find_type_const(b, all_defs, _seen) for b in branches]
            unique = {v for v in values if v is not None}
            if len(unique) == 1:
                return unique.pop()

    return None


def collect_nested_types(obj) -> set:
    """Recursively collect all "@type" string values found at any depth in obj."""
    found = set()
    if isinstance(obj, dict):
        v = obj.get("@type")
        if isinstance(v, str):
            found.add(v)
        for val in obj.values():
            found |= collect_nested_types(val)
    elif isinstance(obj, list):
        for item in obj:
            found |= collect_nested_types(item)
    return found


def find_unresolved_refs(schema_obj: dict, available_defs: set) -> list:
    """
    Walk the schema recursively and collect any $ref values pointing to
    #/$defs/<name> where <name> is not in available_defs.
    Returns list of (ref_string, path).
    """
    missing = []

    def walk(node, path=""):
        if isinstance(node, dict):
            if "$ref" in node:
                ref = node["$ref"]
                m = re.match(r'^#/\$defs/(.+)$', ref)
                if m:
                    name = m.group(1)
                    if name not in available_defs:
                        missing.append((ref, path))
            for k, v in node.items():
                walk(v, f"{path}/{k}")
        elif isinstance(node, list):
            for idx, item in enumerate(node):
                walk(item, f"{path}/{idx}")

    walk(schema_obj)
    return missing


# ---------------------------------------------------------------------------
# Output helpers
# ---------------------------------------------------------------------------

RESET = "\033[0m"
BOLD  = "\033[1m"
RED   = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
CYAN  = "\033[36m"
DIM   = "\033[2m"


def _col():
    return sys.stdout.isatty()


def c(text, code):
    return f"{code}{text}{RESET}" if _col() else text


_quiet = False
_very_quiet = False


def section_hdr(title: str):
    print()
    print(c("=" * 72, BOLD))
    print(c(f"  {title}", BOLD + CYAN))
    print(c("=" * 72, BOLD))


def ok(msg: str):
    if not _quiet:
        print(c("  OK  ", GREEN) + " " + msg)


def loc(msg: str):
    """Always-visible neutral location marker (item header). Never suppressed by -q or -vq."""
    print(c("  >>  ", CYAN) + " " + msg)


def warn(msg: str):
    if not _very_quiet:
        print(c(" WARN ", YELLOW) + " " + msg)

def err(msg: str):  print(c("  ERR ", RED)    + " " + msg)


def info(msg: str):
    if not _quiet:
        print(c("  --  ", DIM) + " " + msg)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def run_checks(md_path: Path, deep_type_check: bool = True) -> int:
    print(f"\nChecking: {md_path}")
    snippets, schema_entries, example_entries, other_blocks = parse_markdown(md_path)

    total_errors   = 0
    total_warnings = 0

    # ==================================================================
    # 1. Snippets
    # ==================================================================
    section_hdr("1. JSON Snippets in 'JSON Representation Rules'")
    info(f"Found {len(snippets)} snippet(s) — validated as JSON or JSON object fragment")
    for blk in snippets:
        path_str = " > ".join(blk.chapter_path)
        loc(f"Line {blk.line_start:4d}: [{path_str}]")
        info(f"            caption: {blk.caption[:80]}")
        # Remove brevity placeholder lines ("...") before validating
        cleaned = "\n".join(
            line for line in blk.raw.splitlines()
            if line.strip() != "..."
        )
        # Try as-is first
        try:
            json.loads(cleaned)
            ok(f"  -> Valid JSON")
        except json.JSONDecodeError:
            # Try wrapped in { } to allow object fragments (key-value pairs)
            try:
                json.loads("{" + cleaned + "}")
                ok(f"  -> Valid JSON object fragment (valid when wrapped in {{ }})")
            except json.JSONDecodeError as e:
                err(f"  -> INVALID: not valid JSON and not a valid JSON object fragment: {e}")
                total_errors += 1

    # ==================================================================
    # 2. JSON Schema Definitions
    # ==================================================================
    section_hdr("2. JSON Schema Definitions")
    info(f"Found {len(schema_entries)} schema block(s)")

    combined = build_combined_schema(schema_entries)
    available_defs = set(combined.get("$defs", {}).keys())

    schemas_by_type: dict[str, list[SchemaEntry]] = {}
    # Track which def_names have unresolved refs (to suppress cascade errors in examples)
    defs_with_unresolved_refs: set[str] = set()

    for entry in schema_entries:
        path_str = " > ".join(entry.block.chapter_path)
        label = f"Line {entry.block.line_start:4d} [{path_str}]"

        # --- valid JSON? ---
        if not entry.schema:
            err(f"{label}: {entry.def_name}")
            total_errors += 1
            continue

        # --- exactly one $defs? ---
        defs = entry.schema.get("$defs", {})
        if not isinstance(defs, dict) or len(defs) != 1:
            if entry.def_name.startswith("<"):
                err(f"{label}: {entry.def_name}")
                total_errors += 1
            else:
                warn(f"{label}: '$defs' has {len(defs)} entries (expected 1): {list(defs.keys())}")
                total_warnings += 1
        else:
            loc(f"{label}")
            info(f"            $defs entry: '{entry.def_name}'")

        # --- @type const — rules depend on subchapter ---
        def_body  = defs.get(entry.def_name, {}) if isinstance(defs, dict) else {}
        props     = def_body.get("properties", {}) if isinstance(def_body, dict) else {}
        type_rule = SCHEMA_SUBCHAPTER_TYPE_RULES.get(entry.subchapter, "required")
        has_type  = "@type" in props

        if type_rule == "forbidden":
            if has_type:
                err(f"  -> '{entry.def_name}': '@type' MUST NOT be present in '{entry.subchapter}' schemas")
                total_errors += 1
            else:
                ok(f"  -> '{entry.def_name}': no '@type' — correct for '{entry.subchapter}'")
        else:  # "required"
            if not has_type:
                # Deep check: look inside allOf/anyOf/oneOf and follow $refs
                deep_type_const = schema_find_type_const(
                        def_body, combined.get("$defs", {})) if deep_type_check else None
                if deep_type_const is not None:
                    entry.type_const = deep_type_const
                    ok(f"  -> '{entry.def_name}': '@type' found via allOf/anyOf/oneOf/$ref (deep check)")
                else:
                    err(f"  -> '{entry.def_name}': '@type' is required in '{entry.subchapter}' schemas but is missing"
                        + ("" if deep_type_check else " (deep check disabled)"))
                    total_errors += 1
            else:
                tp = props["@type"]
                if not isinstance(tp, dict):
                    err(f"  -> '{entry.def_name}': '@type' property is not an object")
                    total_errors += 1
                else:
                    if tp.get("type") != "string":
                        err(f"  -> '{entry.def_name}': '@type' does not have \"type\": \"string\"")
                        total_errors += 1
                    if "const" not in tp:
                        err(f"  -> '{entry.def_name}': '@type' has no 'const' value")
                        total_errors += 1
                    else:
                        ok(f"  -> '{entry.def_name}': @type const = '{entry.type_const}'")

        # --- unresolved $refs in this schema? ---
        unresolved = find_unresolved_refs(entry.schema, available_defs)
        for ref, path in unresolved:
            err(f"  -> '{entry.def_name}': unresolved $ref '{ref}' at {path}")
            total_errors += 1
        if unresolved:
            defs_with_unresolved_refs.add(entry.def_name)

        # --- schema is valid JSON Schema? ---
        try:
            Draft202012Validator.check_schema(entry.schema)
            ok(f"  -> '{entry.def_name}': is a valid JSON Schema")
        except SchemaError as e:
            err(f"  -> '{entry.def_name}': schema error: {e.message}")
            total_errors += 1

        # index by type const
        if entry.type_const:
            schemas_by_type.setdefault(entry.type_const, []).append(entry)

    # ==================================================================
    # 3. Examples
    # ==================================================================
    section_hdr("3. Examples")
    info(f"Found {len(example_entries)} example(s)")

    types_with_examples: set[str] = set()        # top-level @type values
    types_with_nested_examples: set[str] = set() # @type values anywhere in any example

    for ex in example_entries:
        label = (f"Line {ex.block.line_start:4d} "
                 f"[{ex.section}] \"{ex.caption[:55]}\"")

        # 3a. Valid JSON?
        loc(f"{label}")
        if ex.obj is None:
            err(f"  -> INVALID JSON")
            total_errors += 1
            continue

        # 3b. @type present?
        if ex.type_value is None:
            err(f"  -> Missing top-level '@type' property")
            total_errors += 1
            continue
        ok(f"  -> @type = '{ex.type_value}'")
        types_with_examples.add(ex.type_value)
        types_with_nested_examples |= collect_nested_types(ex.obj)

        # 3c. Matching schema?
        matching = schemas_by_type.get(ex.type_value, [])
        if not matching:
            err(f"  -> No JSON Schema found for @type='{ex.type_value}'")
            total_errors += 1
            continue
        ok(f"  -> {len(matching)} schema(s) found for @type='{ex.type_value}'")

        # 3d. Validate against each matching schema
        any_pass = False
        failing: list[tuple[str, list[str]]] = []
        skipped_due_to_broken_refs: list[str] = []
        for se in matching:
            if se.def_name in defs_with_unresolved_refs:
                skipped_due_to_broken_refs.append(se.def_name)
                continue
            def_body = se.schema.get("$defs", {}).get(se.def_name, {})
            try:
                v = make_validator(def_body, combined)
                errors_found = sorted(v.iter_errors(ex.obj), key=lambda e: e.path)
                if errors_found:
                    msgs = [e.message for e in errors_found]
                    failing.append((se.def_name, msgs))
                else:
                    any_pass = True
                    ok(f"  -> Validates OK against '{se.def_name}' (line {se.block.line_start})")
            except Exception as exc:
                # Truncate potentially very long exception messages (e.g. PointerToNowhere dumps schema)
                msg = str(exc)
                if len(msg) > 200:
                    msg = msg[:200] + " …[truncated]"
                failing.append((se.def_name, [f"Validator error: {msg}"]))

        for sn in skipped_due_to_broken_refs:
            warn(f"  -> Skipped validation against '{sn}' — schema has unresolved $refs (see section 2)")

        all_skipped = bool(skipped_due_to_broken_refs) and not failing and not any_pass

        if all_skipped:
            # All schemas were skipped — can't conclude pass or fail
            warn(f"  -> All matching schemas skipped due to unresolved $refs — validation not possible")
            total_warnings += 1
        elif not any_pass:
            err(f"  -> Example does NOT validate against any schema for @type='{ex.type_value}'")
            total_errors += 1
            for def_name, msgs in failing:
                err(f"     Schema '{def_name}':")
                for m in msgs[:5]:
                    err(f"       - {m}")
                if len(msgs) > 5:
                    err(f"       ... and {len(msgs) - 5} more")
        elif any_pass and failing:
            warn(f"  -> Failed {len(failing)} schema(s) but passed at least one — acceptable")
            for def_name, msgs in failing:
                warn(f"     Failing schema '{def_name}':")
                for m in msgs[:3]:
                    warn(f"       - {m}")
                if len(msgs) > 3:
                    warn(f"       ... and {len(msgs) - 3} more")

    # ==================================================================
    # 4. Typed schemas without examples
    # ==================================================================
    section_hdr("4. Typed schemas without any example")
    any_missing = False
    for type_const, entries in sorted(schemas_by_type.items()):
        for se in entries:
            needs_toplevel = se.subchapter in SCHEMA_SUBCHAPTER_NEEDS_TOPLEVEL_EXAMPLE
            if needs_toplevel:
                if type_const not in types_with_examples:
                    err(f"  Line {se.block.line_start:4d} '{se.def_name}': "
                        f"no top-level example found for @type='{type_const}'")
                    total_errors += 1
                    any_missing = True
                else:
                    ok(f"  '{se.def_name}' (@type='{type_const}'): top-level example present")
            else:
                if type_const not in types_with_nested_examples:
                    warn(f"  Line {se.block.line_start:4d} '{se.def_name}': "
                         f"no example found (at any depth) for @type='{type_const}'")
                    total_warnings += 1
                    any_missing = True
                else:
                    ok(f"  '{se.def_name}' (@type='{type_const}'): example present (nested)")
    if not any_missing:
        ok("All typed schemas have at least one example")

    # ==================================================================
    # 5. Other JSON blocks
    # ==================================================================
    section_hdr("5. Other JSON blocks  (outside the three named sections)")
    if not other_blocks:
        ok("No JSON blocks found outside the three named sections")
    else:
        warn(f"Found {len(other_blocks)} JSON block(s) outside named sections:")
        for blk in other_blocks:
            path_str = " > ".join(blk.chapter_path) if blk.chapter_path else "<no chapter>"
            try:
                json.loads(blk.raw)
                validity = "valid JSON"
            except json.JSONDecodeError as e:
                validity = f"INVALID JSON ({e})"
            warn(f"  Line {blk.line_start:4d}: [{path_str}]")
            warn(f"             caption: \"{blk.caption[:60]}\" — {validity}")
        total_warnings += len(other_blocks)

    # ==================================================================
    # Summary
    # ==================================================================
    section_hdr("Summary")
    print(f"  Snippets (validated):      {len(snippets)}")
    print(f"  Schema definitions:        {len(schema_entries)}")
    print(f"  Examples:                  {len(example_entries)}")
    print(f"  Other JSON blocks:         {len(other_blocks)}")
    print()
    if total_errors == 0 and total_warnings == 0:
        print(c("  All checks passed with no errors or warnings.", GREEN + BOLD))
    else:
        if total_errors > 0:
            print(c(f"  ERRORS:   {total_errors}", RED + BOLD))
        if total_warnings > 0:
            print(c(f"  WARNINGS: {total_warnings}", YELLOW + BOLD))
    print()

    return total_errors


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Check JSON examples and schemas in the RPP JSON Internet-Draft.")
    parser.add_argument("file", nargs="?",
                        help="Path to the markdown file (default: src/draft-wullink-rpp-json.md)")
    parser.add_argument("-q", "--quiet", action="store_true",
                        help="Suppress OK and informational output; show only warnings and errors")
    parser.add_argument("-vq", "--very-quiet", action="store_true",
                        help="Suppress OK, info, and warnings; keep section headers, >> context lines, and errors")
    parser.add_argument("--no-deep-type-check", action="store_true",
                        help="Disable deep @type detection via allOf/anyOf/oneOf/$ref traversal "
                             "(by default the deep check is performed)")
    args = parser.parse_args()

    if args.quiet:
        _quiet = True
    if args.very_quiet:
        _quiet = True
        _very_quiet = True

    md = Path(args.file) if args.file else Path(__file__).parent.parent / "src" / "draft-wullink-rpp-json.md"

    if not md.exists():
        print(f"ERROR: File not found: {md}", file=sys.stderr)
        sys.exit(1)

    sys.exit(1 if run_checks(md, deep_type_check=not args.no_deep_type_check) > 0 else 0)
