#!/usr/bin/env python3
"""CSS inventory metric + no-regression ratchet for the kk-aurora theme.

Step 0 of ``docs/current-state/AURORA-STYLESHEET-REBUILD-PLAN.md`` §3. This is
the durable version of the throwaway scripts described in that plan's §0.1: it
emits the §1.1 stylesheet table as machine-readable JSON and gates CI on the two
numbers that regressed silently between 2026-07-19 and 1.4.3 — front-end CSS
**line count** and **``!important`` count**.

Parsing is deliberately *not* reimplemented. Rule/selector structure comes from
``scripts/css_coverage_audit.py`` (PR #468), which already solved seven
false-positive traps documented in ``docs/current-state/archive/CSS-DEADCODE-OVERLAP-AUDIT.md``.
This module adds three things on top: raw-vs-code-only counting, git-revision
sourcing, and CSS-nesting awareness for the selector census.

Counting rules that matter
--------------------------

``!important`` is counted twice, and the difference is load-bearing:

* ``important_raw``  — every occurrence of the literal, comments included.
* ``important_code`` — occurrences after ``/* … */`` is blanked out.

They differ by exactly one today: ``assets/css/revive-port.css`` carries a
section comment reading *"Those rules used !important black panes behind type"*.
A raw grep therefore reports 161 across the front-end + editor sheets where only
160 are real declarations. **The ratchet gates on ``important_code``.** Verify
the case with::

    python3 scripts/css_inventory.py --explain-important-comments

Usage
-----

::

    python3 scripts/css_inventory.py                      # §1.1 markdown table
    python3 scripts/css_inventory.py --format json        # machine-readable
    python3 scripts/css_inventory.py --rev 0064b4e        # measure a git revision
    python3 scripts/css_inventory.py --check              # ratchet vs .css-budget.json
    python3 scripts/css_inventory.py --freeze             # lower the budget
    python3 scripts/css_inventory.py --coverage --fetch-routes  # live-route coverage

The ratchet
-----------

``.css-budget.json`` at the repo root holds the ceiling. ``--check`` fails when a
gated metric is **above** the budget (a regression) *and* when it is **below**
(a stale budget that must be tightened, which is what makes this a ratchet
rather than a cap). Lowering the budget is one unceremonious command::

    make css-inventory-freeze

Raising it is not. ``--freeze`` refuses to write a higher number without
``--waiver-issue`` and ``--waiver-reason``, and appends a dated, permanent waiver
record to ``.css-budget.json``. ``--check --base-ref <ref>`` then re-validates
that every raise between the base ref and HEAD is covered by a waiver that is
**new in this diff** and whose ``to`` value matches the new budget. Hand-editing
the number, or reusing an old waiver, fails CI.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import css_coverage_audit as cca  # noqa: E402  (local sibling module)

REPO_ROOT = Path(__file__).resolve().parents[1]
BUDGET_PATH = REPO_ROOT / ".css-budget.json"

# Enqueue order, front end first, editor-only sheet last. Mirrors
# css_coverage_audit.CSS_FILES so the two tools can never diverge on scope.
ALL_FILES = [str(p.relative_to(cca.REPO_ROOT)) for p in cca.CSS_FILES]
EDITOR_ONLY = {"theme/kk-aurora/assets/css/editor.css"}
FRONT_END_FILES = [f for f in ALL_FILES if f not in EDITOR_ONLY]

# Metrics the CI ratchet gates on. Everything else in the report is diagnostic.
GATED_METRICS = ("front_end_lines", "front_end_important")

COMMENT_RE = re.compile(r"/\*.*?\*/", re.S)
AT_BLOCK_RE = re.compile(r"@[-\w]+[^{};]*\{")
MEDIA_BLOCK_RE = re.compile(r"@media([^{]*)\{")
VAR_USE_RE = re.compile(r"var\(")
PX_RE = re.compile(r"\d(?:\.\d+)?px\b")

# 13 live routes plus a synthetic 404 probe, chosen for *template* variety
# rather than volume: front page, several FSE page templates, the posts archive,
# a category archive, a single post, and the 404 template. Issue #472 asks for
# >= 10 routes; the plan's §1.5 heuristic used 10 page routes only and therefore
# never exercised the single-post or archive templates.
DEFAULT_ROUTES = [
    "/",
    "/about/",
    "/speaking/",
    "/services/",
    "/work/",
    "/photography/",
    "/publications/",
    "/events/",
    "/testimonials/",
    "/contact/",
    "/blog/",
    "/category/ai-creatives/",
    "/2003/10/14/testing-testing-1-2-1-2-3-4/",
    "/kk-inventory-404-probe/",  # expected 404 — exercises templates/404.html
]
LIVE_ORIGIN = "https://kriskrug.co"


# --------------------------------------------------------------------------
# Sourcing: working tree or a git revision
# --------------------------------------------------------------------------


def _git(*args: str) -> str:
    return subprocess.run(
        ["git", "-C", str(REPO_ROOT), *args],
        capture_output=True,
        text=True,
        check=True,
    ).stdout


def load_sources(rev: str | None) -> dict[str, str]:
    """Return ``{relative_path: text}`` from the working tree or a git rev."""
    out: dict[str, str] = {}
    for rel in ALL_FILES:
        if rev:
            try:
                out[rel] = _git("show", f"{rev}:{rel}")
            except subprocess.CalledProcessError:
                continue  # file did not exist at that revision
        else:
            p = REPO_ROOT / rel
            if p.exists():
                out[rel] = p.read_text(encoding="utf-8")
    return out


def blank_comments(text: str) -> str:
    """Blank ``/* … */`` to equal-length whitespace, preserving line numbers."""
    return COMMENT_RE.sub(
        lambda m: re.sub(r"[^\n]", " ", m.group(0)), text
    )


# --------------------------------------------------------------------------
# Per-file metrics — the plan's §1.1 columns
# --------------------------------------------------------------------------


def file_metrics(text: str) -> dict:
    code = blank_comments(text)
    braces = code.count("{")
    at_blocks = len(AT_BLOCK_RE.findall(code))
    return {
        "bytes": len(text.encode("utf-8")),
        "lines": len(text.splitlines()),
        # Plan §0.1 method: every "{" minus every at-rule "{".
        "rule_blocks": braces - at_blocks,
        "at_rule_blocks": at_blocks,
        "media_blocks": len(MEDIA_BLOCK_RE.findall(code)),
        "important_raw": text.count("!important"),
        "important_code": code.count("!important"),
        "custom_prop_decls": len(cca.CUSTOM_PROP_RE.findall(code)),
        "var_uses": len(VAR_USE_RE.findall(code)),
        "hex_literals": len(cca.HEX_COLOR_RE.findall(code)),
        "px_literals": len(PX_RE.findall(code)),
    }


# --------------------------------------------------------------------------
# Selector census (nesting-aware) and breakpoint census
# --------------------------------------------------------------------------


def _nested_selectors(body: str) -> list[str]:
    """Selector preludes of blocks nested *inside* a rule body (CSS nesting).

    ``css_coverage_audit.parse_css`` indexes top-level and at-rule-nested rules
    but treats a nested ``&:hover { … }`` as part of its parent's body. Those
    blocks are real selectors and the rebuild has to account for them, so they
    are recovered here rather than by patching the audited parser.
    """
    out: list[str] = []
    buf: list[str] = []
    i, n = 0, len(body)
    while i < n:
        ch = body[i]
        if ch == "{":
            prelude = re.sub(r"\s+", " ", "".join(buf).strip())
            depth, j = 1, i + 1
            while j < n and depth:
                if body[j] == "{":
                    depth += 1
                elif body[j] == "}":
                    depth -= 1
                j += 1
            if prelude and not prelude.startswith("@"):
                out.append(prelude)
                out.extend(_nested_selectors(body[i + 1 : j - 1]))
            i, buf = j, []
            continue
        if ch == "}":
            buf = []
            i += 1
            continue
        buf.append(ch)
        i += 1
    return out


def _materialise(sources: dict[str, str], tmp: Path) -> dict[str, Path]:
    """Write sources to a temp tree so the audited path-based parser can read them."""
    paths: dict[str, Path] = {}
    for rel, text in sources.items():
        p = tmp / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text, encoding="utf-8")
        paths[rel] = p
    return paths


def structural_census(sources: dict[str, str], scope: list[str]) -> dict:
    """Selector duplication, custom properties and breakpoints over ``scope``."""
    selectors: dict[str, list[str]] = {}
    props: dict[str, list[str]] = {}
    conditions: dict[str, list[str]] = {}

    with tempfile.TemporaryDirectory() as td:
        paths = _materialise({k: v for k, v in sources.items() if k in scope}, Path(td))
        for rel in scope:
            if rel not in paths:
                continue
            rules, code = cca.parse_css(paths[rel])
            for rule in rules:
                for part in rule.selector_parts:
                    selectors.setdefault(re.sub(r"\s+", " ", part).strip(), []).append(rel)
                for nested in _nested_selectors(rule.body):
                    for part in nested.split(","):
                        part = part.strip()
                        if part:
                            selectors.setdefault(part, []).append(rel)
            for m in cca.CUSTOM_PROP_RE.finditer(code):
                props.setdefault(m.group(1), []).append(rel)
            for m in MEDIA_BLOCK_RE.finditer(code):
                conditions.setdefault(re.sub(r"\s+", " ", m.group(1)).strip(), []).append(rel)

    widths: dict[str, set[str]] = {"min-width": set(), "max-width": set()}
    for cond in conditions:
        for m in re.finditer(r"(min|max)-width:\s*([\d.]+)px", cond):
            widths[f"{m.group(1)}-width"].add(m.group(2))

    duplicated = {s: v for s, v in selectors.items() if len(v) > 1}
    cross_file = {s: sorted(set(v)) for s, v in selectors.items() if len(set(v)) > 1}

    return {
        "distinct_selectors": len(selectors),
        "selectors_declared_more_than_once": len(duplicated),
        "redundant_declarations": sum(len(v) - 1 for v in selectors.values()),
        "selectors_in_more_than_one_file": len(cross_file),
        "worst_offenders": [
            {"selector": s, "declarations": len(v), "files": sorted(set(v))}
            for s, v in sorted(duplicated.items(), key=lambda kv: -len(kv[1]))[:20]
        ],
        "cross_file_selectors": cross_file,
        "distinct_custom_props": len(props),
        "custom_props_by_namespace": _namespace_breakdown(props),
        "distinct_media_conditions": len(conditions),
        "media_conditions": sorted(conditions),
        "distinct_breakpoint_widths": sum(len(v) for v in widths.values()),
        "breakpoint_widths": {k: sorted(v, key=float) for k, v in widths.items()},
    }


def _namespace_breakdown(props: dict[str, list[str]]) -> dict[str, int]:
    buckets: dict[str, int] = {}
    for name in props:
        stem = name[2:]
        prefix = stem.split("-")[0]
        key = f"--{prefix}-*" if "-" in stem else "--bare"
        buckets[key] = buckets.get(key, 0) + 1
    return dict(sorted(buckets.items(), key=lambda kv: -kv[1]))


# --------------------------------------------------------------------------
# Inventory
# --------------------------------------------------------------------------


def inventory(rev: str | None = None) -> dict:
    sources = load_sources(rev)
    if not sources:
        raise SystemExit(f"error: no kk-aurora CSS found at {rev or 'the working tree'}")

    per_file = {rel: file_metrics(text) for rel, text in sources.items()}

    def total(keys: list[str]) -> dict:
        agg: dict[str, int] = {}
        for rel in keys:
            for k, v in per_file.get(rel, {}).items():
                agg[k] = agg.get(k, 0) + v
        return agg

    all_totals = total(list(per_file))
    fe_totals = total([f for f in FRONT_END_FILES if f in per_file])

    return {
        "schema": 1,
        "rev": rev or "worktree",
        "theme_version": _theme_version(sources),
        "files": per_file,
        "totals": all_totals,
        "front_end_totals": fe_totals,
        # The two numbers CI gates on, hoisted so nothing has to know the shape.
        "metrics": {
            "front_end_lines": fe_totals.get("lines", 0),
            "front_end_important": fe_totals.get("important_code", 0),
        },
        "informational": {
            "all_files_lines": all_totals.get("lines", 0),
            "all_files_important_code": all_totals.get("important_code", 0),
            "all_files_important_raw": all_totals.get("important_raw", 0),
            "front_end_important_raw": fe_totals.get("important_raw", 0),
        },
        "structure": structural_census(sources, FRONT_END_FILES),
        "important_in_comments": important_comment_sites(sources),
    }


def _theme_version(sources: dict[str, str]) -> str:
    head = sources.get("theme/kk-aurora/style.css", "")[:2000]
    m = re.search(r"^Version:\s*(\S+)", head, re.M)
    return m.group(1) if m else "unknown"


def important_comment_sites(sources: dict[str, str]) -> list[dict]:
    """Every ``!important`` that sits inside a comment — the raw/code delta."""
    sites: list[dict] = []
    for rel, text in sources.items():
        for m in COMMENT_RE.finditer(text):
            block = m.group(0)
            if "!important" not in block:
                continue
            base = text.count("\n", 0, m.start()) + 1
            for offset, line in enumerate(block.splitlines()):
                if "!important" in line:
                    sites.append(
                        {
                            "file": rel,
                            "line": base + offset,
                            "text": line.strip(),
                            "counted": False,
                        }
                    )
    return sites


# --------------------------------------------------------------------------
# Budget / ratchet
# --------------------------------------------------------------------------


def load_budget(rev: str | None = None) -> dict | None:
    if rev:
        try:
            return json.loads(_git("show", f"{rev}:.css-budget.json"))
        except (subprocess.CalledProcessError, json.JSONDecodeError):
            return None
    if not BUDGET_PATH.exists():
        return None
    return json.loads(BUDGET_PATH.read_text(encoding="utf-8"))


def _waiver_key(w: dict) -> tuple:
    return (w.get("date"), w.get("metric"), w.get("from"), w.get("to"), w.get("issue"))


def check(base_ref: str | None, summary_path: str | None) -> int:
    """Ratchet. Returns a process exit code; prints exactly why it failed."""
    data = inventory(None)
    budget = load_budget()
    errors: list[str] = []
    notes: list[str] = []

    if budget is None:
        print(
            "FAIL: .css-budget.json is missing. Create it with:\n"
            "        make css-inventory-freeze",
            file=sys.stderr,
        )
        return 1

    limits = budget.get("metrics", {})
    base = inventory(base_ref) if base_ref else None
    base_budget = load_budget(base_ref) if base_ref else None

    for metric in GATED_METRICS:
        measured = data["metrics"][metric]
        allowed = limits.get(metric)
        if allowed is None:
            errors.append(f"{metric}: no budget recorded in .css-budget.json")
            continue
        if measured > allowed:
            errors.append(
                f"{metric}: {measured} exceeds the committed budget of {allowed} "
                f"(+{measured - allowed}). {_blame(metric, data, base)}"
            )
        elif measured < allowed:
            errors.append(
                f"{metric}: {measured} is BELOW the committed budget of {allowed} "
                f"(-{allowed - measured}). The budget is stale — a ratchet only "
                f"holds if wins are locked in. Run: make css-inventory-freeze"
            )
        else:
            notes.append(f"{metric}: {measured} == budget {allowed}")

    # Escape-hatch validation: a raised budget must carry a waiver added in this
    # same diff, matching the new value, with a non-empty issue and reason.
    if base_budget is not None:
        old_waivers = {_waiver_key(w) for w in base_budget.get("waivers", [])}
        new_waivers = [
            w for w in budget.get("waivers", []) if _waiver_key(w) not in old_waivers
        ]
        for metric in GATED_METRICS:
            was = base_budget.get("metrics", {}).get(metric)
            now = limits.get(metric)
            if was is None or now is None or now <= was:
                continue
            match = [
                w
                for w in new_waivers
                if w.get("metric") == metric
                and w.get("to") == now
                and str(w.get("issue", "")).strip()
                and str(w.get("reason", "")).strip()
            ]
            if not match:
                errors.append(
                    f"{metric}: budget raised {was} -> {now} without a waiver. "
                    f"Raising the budget requires:\n"
                    f"        make css-inventory-freeze "
                    f"WAIVER_ISSUE='#123' WAIVER_REASON='why this rule must exist'\n"
                    f"      which appends a dated, reviewable record to .css-budget.json. "
                    f"Hand-editing the number is not an escape hatch."
                )
            else:
                notes.append(
                    f"WAIVED: {metric} {was} -> {now} "
                    f"({match[0]['issue']}: {match[0]['reason']})"
                )

    title = "CSS inventory ratchet"
    lines = [f"### {title}", ""]
    lines.append(f"Theme `{data['theme_version']}` — measured on the PR head.")
    lines.append("")
    lines.append("| Metric | Measured | Budget |")
    lines.append("|---|---:|---:|")
    for metric in GATED_METRICS:
        lines.append(
            f"| `{metric}` | {data['metrics'][metric]} | {limits.get(metric, '—')} |"
        )
    if notes:
        lines += ["", *[f"- {n}" for n in notes]]
    if errors:
        lines += ["", "**Failures**", *[f"- {e}" for e in errors]]

    report = "\n".join(lines)
    print(report)
    if summary_path:
        with open(summary_path, "a", encoding="utf-8") as fh:
            fh.write(report + "\n")

    if errors:
        print("", file=sys.stderr)
        for e in errors:
            print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


def _blame(metric: str, data: dict, base: dict | None) -> str:
    """Name the offending file(s) so the fix is obvious."""
    key = "lines" if metric.endswith("lines") else "important_code"
    if base is None:
        worst = sorted(
            ((r, m[key]) for r, m in data["files"].items() if r in FRONT_END_FILES),
            key=lambda kv: -kv[1],
        )[:3]
        return "Largest contributors: " + ", ".join(f"{r} ({n})" for r, n in worst)
    deltas = []
    for rel in FRONT_END_FILES:
        now = data["files"].get(rel, {}).get(key, 0)
        was = base["files"].get(rel, {}).get(key, 0)
        if now != was:
            deltas.append(f"{rel} {was} -> {now} ({now - was:+d})")
    return ("Changed since base: " + "; ".join(deltas)) if deltas else ""


def freeze(waiver_issue: str | None, waiver_reason: str | None) -> int:
    data = inventory(None)
    budget = load_budget() or {
        "$comment": (
            "CSS regression ratchet for theme/kk-aurora. Generated by "
            "scripts/css_inventory.py; see docs/current-state/"
            "AURORA-STYLESHEET-REBUILD-PLAN.md §3 step 0. Lowering these numbers "
            "is free (make css-inventory-freeze). Raising one requires "
            "WAIVER_ISSUE and WAIVER_REASON and leaves a permanent record below."
        ),
        "metrics": {},
        "waivers": [],
    }
    old = budget.get("metrics", {})
    raises = [
        (m, old[m], data["metrics"][m])
        for m in GATED_METRICS
        if m in old and data["metrics"][m] > old[m]
    ]
    if raises and not (waiver_issue and waiver_reason):
        for m, was, now in raises:
            print(
                f"REFUSED: {m} would rise {was} -> {now} (+{now - was}).",
                file=sys.stderr,
            )
        print(
            "\nThe ratchet does not raise silently. If this increase is genuinely "
            "necessary, re-run with an issue and a reason:\n"
            "    make css-inventory-freeze WAIVER_ISSUE='#123' "
            "WAIVER_REASON='new component X needs N lines'\n"
            "That writes a dated waiver into .css-budget.json which shows up in "
            "the PR diff and which CI cross-checks.",
            file=sys.stderr,
        )
        return 1

    today = _dt.date.today().isoformat()
    for m, was, now in raises:
        budget.setdefault("waivers", []).append(
            {
                "date": today,
                "metric": m,
                "from": was,
                "to": now,
                "issue": waiver_issue,
                "reason": waiver_reason,
                "theme_version": data["theme_version"],
            }
        )
    budget["metrics"] = dict(data["metrics"])
    budget["measured_at"] = today
    budget["theme_version"] = data["theme_version"]
    budget["informational"] = data["informational"]
    BUDGET_PATH.write_text(
        json.dumps(budget, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(f"wrote {BUDGET_PATH.relative_to(REPO_ROOT)}: {budget['metrics']}")
    for m, was, now in raises:
        print(f"  WAIVED {m}: {was} -> {now} ({waiver_issue}: {waiver_reason})")
    return 0


# --------------------------------------------------------------------------
# Live-route coverage (replaces the 53% dead-class heuristic)
# --------------------------------------------------------------------------


def fetch_routes(routes: list[str], dest: Path) -> list[dict]:
    """Read-only GETs of public routes. No credentials, no writes to the site."""
    import urllib.error
    import urllib.request

    dest.mkdir(parents=True, exist_ok=True)
    results = []
    for route in routes:
        url = LIVE_ORIGIN + route
        req = urllib.request.Request(
            url, headers={"User-Agent": "kriskrug-wp css-inventory (read-only)"}
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                body = resp.read().decode("utf-8", "ignore")
                status = resp.status
        except urllib.error.HTTPError as e:  # 404 probe is expected
            body = e.read().decode("utf-8", "ignore")
            status = e.code
        except Exception as e:  # noqa: BLE001 - network failure is reportable, not fatal
            results.append({"route": route, "status": None, "error": str(e)})
            continue
        name = (route.strip("/").replace("/", "_") or "home") + ".html"
        (dest / name).write_text(body, encoding="utf-8")
        results.append({"route": route, "status": status, "bytes": len(body)})
    return results


def coverage_report(corpus_dir: Path, routes: list[dict] | None) -> dict:
    data = cca.analyse(corpus_dir)
    theme_prefixes = ("aurora-", "kk-", "kkm-", "revive-", "is-aurora")
    authored = [
        f
        for f in data["findings"]
        if f.name.startswith(theme_prefixes)
    ]
    # css_coverage_audit only returns classes with NO markup match, so recount
    # the denominator from the CSS itself.
    total_authored = _count_authored_classes()
    by_conf: dict[str, list[str]] = {"high": [], "medium": [], "low": []}
    for f in authored:
        by_conf[f.confidence].append(f.name)
    return {
        "routes_fetched": routes,
        "route_count": len([r for r in (routes or []) if r.get("status")]),
        "routes_http_200": len([r for r in (routes or []) if r.get("status") == 200]),
        "live_pages_in_corpus": data["corpus"]["live_files"],
        "authored_classes_total": total_authored,
        "unmatched_authored": len(authored),
        "unmatched_pct": round(100 * len(authored) / max(1, total_authored), 1),
        "high_confidence_dead": sorted(by_conf["high"]),
        "high_confidence_dead_count": len(by_conf["high"]),
        "high_confidence_dead_pct": round(
            100 * len(by_conf["high"]) / max(1, total_authored), 1
        ),
        "needs_eyeballs_medium": sorted(by_conf["medium"]),
        "protected_low": len(by_conf["low"]),
        "removable_rule_blocks": len(data["removable"]),
        "removable_bytes": sum(r["bytes"] for r in data["removable"]),
    }


def _count_authored_classes() -> int:
    theme_prefixes = ("aurora-", "kk-", "kkm-", "revive-", "is-aurora")
    names: set[str] = set()
    for rel in FRONT_END_FILES:
        p = REPO_ROOT / rel
        if not p.exists():
            continue
        code = blank_comments(p.read_text(encoding="utf-8"))
        for name in cca.CLASS_IN_SELECTOR_RE.findall(code):
            if name.startswith(theme_prefixes):
                names.add(name)
    return len(names)


# --------------------------------------------------------------------------
# Reporting
# --------------------------------------------------------------------------


def report_markdown(data: dict) -> str:
    out: list[str] = []
    w = out.append
    w(f"## Stylesheet inventory — kk-aurora {data['theme_version']} (`{data['rev']}`)\n")
    cols = [
        ("Bytes", "bytes"),
        ("Lines", "lines"),
        ("Rule blocks", "rule_blocks"),
        ("At-rule blocks", "at_rule_blocks"),
        ("`@media`", "media_blocks"),
        ("`!important`", "important_code"),
        ("Custom-prop decls", "custom_prop_decls"),
        ("`var()` uses", "var_uses"),
        ("Hex literals", "hex_literals"),
        ("`px` literals", "px_literals"),
    ]
    w("| File | " + " | ".join(c[0] for c in cols) + " |")
    w("|---|" + "---:|" * len(cols))
    for rel, m in data["files"].items():
        label = rel.replace("theme/kk-aurora/", "")
        if rel in EDITOR_ONLY:
            label += " (editor only)"
        w(f"| `{label}` | " + " | ".join(f"{m[c[1]]:,}" for c in cols) + " |")
    t, fe = data["totals"], data["front_end_totals"]
    w("| **Total** | " + " | ".join(f"**{t[c[1]]:,}**" for c in cols) + " |")
    w(
        "| **Front-end subtotal** | "
        + " | ".join(f"**{fe[c[1]]:,}**" for c in cols)
        + " |"
    )
    w("")
    inf = data["informational"]
    w(
        f"`!important` raw / code-only — all {len(ALL_FILES)} sheets: "
        f"**{inf['all_files_important_raw']} raw**, **{inf['all_files_important_code']} code-only**; "
        f"front-end {len(FRONT_END_FILES)}: **{inf['front_end_important_raw']} raw**, "
        f"**{data['metrics']['front_end_important']} code-only**. "
        f"The delta is comment text, listed below.\n"
    )

    if data["important_in_comments"]:
        w("### `!important` inside comments (never counted as declarations)\n")
        for s in data["important_in_comments"]:
            w(f"- `{s['file']}:{s['line']}` — `{s['text']}`")
        w("")

    s = data["structure"]
    w(f"### Selector duplication (front-end {len(FRONT_END_FILES)}, nesting-aware)\n")
    w("| Metric | Value |")
    w("|---|---:|")
    w(f"| Distinct selectors (comma-split) | {s['distinct_selectors']:,} |")
    w(f"| Selectors declared more than once | {s['selectors_declared_more_than_once']:,} |")
    w(f"| Redundant declarations | {s['redundant_declarations']:,} |")
    w(f"| Selectors in more than one file | {s['selectors_in_more_than_one_file']:,} |")
    w(f"| Distinct custom-property names | {s['distinct_custom_props']:,} |")
    w("")
    w("Worst offenders: " + ", ".join(
        f"`{o['selector']}` ({o['declarations']}x)" for o in s["worst_offenders"][:8]
    ) + "\n")

    w("### Breakpoint census\n")
    w(f"{s['distinct_media_conditions']} distinct `@media` conditions; "
      f"{s['distinct_breakpoint_widths']} distinct width values.\n")
    w("| Direction | Values (px) |")
    w("|---|---|")
    for k, v in s["breakpoint_widths"].items():
        w(f"| `{k}` | {', '.join(v) or '—'} |")
    w("")
    return "\n".join(out)


def report_coverage_markdown(cov: dict) -> str:
    out = ["## Live-route CSS coverage\n"]
    out.append(
        f"{cov['live_pages_in_corpus']} saved public pages in the corpus "
        f"({cov['route_count']} routes fetched this run, "
        f"{cov.get('routes_http_200', 0)} HTTP 200).\n"
    )
    out.append("| Metric | Value |")
    out.append("|---|---:|")
    out.append(f"| Theme-authored classes in front-end CSS | {cov['authored_classes_total']} |")
    out.append(f"| Unmatched in any rendered markup | {cov['unmatched_authored']} ({cov['unmatched_pct']}%) |")
    out.append(f"| High-confidence dead (safe candidates) | {cov['high_confidence_dead_count']} ({cov['high_confidence_dead_pct']}%) |")
    out.append(f"| Medium — needs eyeballs | {len(cov['needs_eyeballs_medium'])} |")
    out.append(f"| Protected (WP/JS/PHP/editor) | {cov['protected_low']} |")
    out.append(f"| Fully-removable rule blocks | {cov['removable_rule_blocks']} ({cov['removable_bytes']:,} bytes) |")
    out.append("")
    if cov["routes_fetched"]:
        out.append("| Route | HTTP | Bytes |")
        out.append("|---|---:|---:|")
        for r in cov["routes_fetched"]:
            out.append(f"| `{r['route']}` | {r.get('status') or r.get('error')} | {r.get('bytes', 0):,} |")
        out.append("")
    return "\n".join(out)


# --------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description=__doc__.split("\n")[0],
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    ap.add_argument("--rev", help="measure a git revision instead of the working tree")
    ap.add_argument("--output", help="write to this path instead of stdout")

    ap.add_argument("--check", action="store_true", help="run the CI ratchet")
    ap.add_argument("--base-ref", help="base revision the PR branches from (for --check)")
    ap.add_argument(
        "--github-summary",
        action="store_true",
        help="also append the ratchet table to $GITHUB_STEP_SUMMARY",
    )

    ap.add_argument("--freeze", action="store_true", help="write .css-budget.json")
    ap.add_argument("--waiver-issue", help="issue reference authorising a budget raise")
    ap.add_argument("--waiver-reason", help="why the budget must rise")

    ap.add_argument("--coverage", action="store_true", help="live-route coverage report")
    ap.add_argument("--live-corpus", help="directory of saved public HTML")
    ap.add_argument(
        "--fetch-routes",
        action="store_true",
        help=f"fetch {len(DEFAULT_ROUTES)} public routes read-only into a temp corpus",
    )
    ap.add_argument(
        "--record",
        action="store_true",
        help="write the coverage summary into .css-budget.json (small; not gated)",
    )
    ap.add_argument(
        "--explain-important-comments",
        action="store_true",
        help="show every !important that sits inside a comment (raw vs code-only delta)",
    )
    args = ap.parse_args(argv)

    if args.explain_important_comments:
        data = inventory(args.rev)
        sites = data["important_in_comments"]
        print(
            f"raw={data['informational']['all_files_important_raw']} "
            f"code={data['informational']['all_files_important_code']} "
            f"delta={len(sites)}"
        )
        for s in sites:
            print(f"  {s['file']}:{s['line']}: {s['text']}   -> NOT counted")
        return 0

    if args.freeze:
        return freeze(args.waiver_issue, args.waiver_reason)

    if args.check:
        summary = os.environ.get("GITHUB_STEP_SUMMARY") if args.github_summary else None
        return check(args.base_ref, summary)

    if args.coverage:
        with tempfile.TemporaryDirectory() as td:
            routes = None
            if args.fetch_routes:
                routes = fetch_routes(DEFAULT_ROUTES, Path(td))
                corpus = Path(td)
            elif args.live_corpus:
                corpus = Path(args.live_corpus)
            else:
                ap.error("--coverage needs --fetch-routes or --live-corpus DIR")
            cov = coverage_report(corpus, routes)
        if args.record:
            budget = load_budget() or {"metrics": {}, "waivers": []}
            budget["coverage"] = {
                "measured_at": _dt.date.today().isoformat(),
                "theme_version": inventory(None)["theme_version"],
                "routes": [r["route"] for r in (cov["routes_fetched"] or [])],
                "routes_http_200": cov.get("routes_http_200", 0),
                "authored_classes_total": cov["authored_classes_total"],
                "unmatched_authored": cov["unmatched_authored"],
                "unmatched_pct": cov["unmatched_pct"],
                "high_confidence_dead_count": cov["high_confidence_dead_count"],
                "high_confidence_dead_pct": cov["high_confidence_dead_pct"],
                "high_confidence_dead": cov["high_confidence_dead"],
                "removable_rule_blocks": cov["removable_rule_blocks"],
                "removable_bytes": cov["removable_bytes"],
            }
            BUDGET_PATH.write_text(
                json.dumps(budget, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
            )
            print(f"recorded coverage in {BUDGET_PATH.relative_to(REPO_ROOT)}")
        text = json.dumps(cov, indent=2) if args.format == "json" else report_coverage_markdown(cov)
    else:
        data = inventory(args.rev)
        text = json.dumps(data, indent=2) if args.format == "json" else report_markdown(data)

    if args.output:
        Path(args.output).write_text(text + "\n", encoding="utf-8")
        print(f"wrote {args.output}")
    else:
        print(text)
    return 0


if __name__ == "__main__":
    sys.exit(main())
