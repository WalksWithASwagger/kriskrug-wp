"""Contract for the /ai-policy/ page payload (#885).

The payload is policy.md, approved by Kris on 2026-11-12, converted to body-only
Aurora HTML. These checks hold it to that source word for word and to the
release gate in #886, in both states page-meta.json can record. While
publish_approval is null the body keeps its placeholders. Once it is recorded,
the body must be the final one: the approval date and no pending wording.
"""

from __future__ import annotations

import difflib
import hashlib
import json
import re
import sys
import unittest
from datetime import date, timedelta
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
PACK = ROOT / "content/source-packs/ai-policy-2026"
META_PATH = PACK / "page-meta.json"
ROBOTS_PATH = ROOT / "fixes/robots.txt"

sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "scripts/notion-to-wp"))
from content_architecture_deploy import retired_class_tokens  # noqa: E402
from cp1252_text import UnstorableText, plain_meta_text, storable_payload  # noqa: E402

# content-architecture-2026/module-spec.md, "Allowed Vocabulary".
AURORA_CLASSES = frozenset(
    {
        "aurora-page-lead",
        "aurora-section-kicker",
        "aurora-display-heading",
        "aurora-card-grid",
        "aurora-card",
        "aurora-media-card",
        "aurora-proof-section",
        "aurora-proof-grid",
        "aurora-proof-module",
        "aurora-button",
    }
)
ALLOWED_HOSTS = frozenset(
    {
        "kriskrug.co",
        "larakroekerinteractive.com",
        "www.ap.org",
        "www.theguardian.com",
        "www.wired.com",
        "www.canada.ca",
        "mangrove-web.com",
        "www.agreatidea.com",
        "buffer.com",
    }
)
FORBIDDEN_TAGS = frozenset(
    {
        "h1",
        "style",
        "script",
        "noscript",
        "iframe",
        "img",
        "svg",
        "picture",
        "canvas",
        "video",
        "audio",
        "object",
        "embed",
        "form",
        "input",
        "button",
        "table",
        "link",
        "meta",
        "base",
    }
)
PRIVATE_PATTERNS = (
    r"localhost",
    r"127\.0\.0\.1",
    r"\.local\b",
    r"\.test\b",
    r"file:",
    r"/Users/",
    r"/private/",
    r"/tmp/",
    r"notion\.so",
    r"notionusercontent",
    r"wp-admin",
    r"wp-json",
    r"[?&]preview=",
    r"[?&]page_id=",
    r"staging",
    r"docs\.google",
    r"drive\.google",
    r"dropbox",
)
GENERIC_LINK_TEXT = frozenset(
    {"here", "click here", "this", "link", "read more", "more"}
)
# chr() keeps these characters out of the source, where formatters and the voice
# rule would otherwise see a literal em dash.
EM_DASH_CHAR = chr(0x2014)
NON_CP1252_CHAR = chr(0x2192)
EM_DASH = re.compile(rf"{EM_DASH_CHAR}|&mdash;|&#0*8212;?|&#x0*2014;?", re.IGNORECASE)
# WordPress's wptexturize turns "---" and a spaced "--" into an em dash on the
# public page, so plain hyphens can ship one that never appears in the file.
DOUBLE_HYPHEN = "--"
BLOCK_TAGS = frozenset(
    {
        "p",
        "li",
        "ul",
        "ol",
        "h2",
        "h3",
        "h4",
        "section",
        "aside",
        "div",
        "blockquote",
        "article",
    }
)

# The title line becomes the WordPress title (the template's only H1). Of the
# review note, only its first sentence leaves the body. The scope sentence is
# #883's architecture decision, and no ruling from Kris removes it.
TITLE_LINE = "# How I Use AI (And Where I Draw the Line)"
REVIEW_PREFIX = "Draft for Kris Krüg's review. "
SCOPE_PENDING = (
    "This is a proposed public transparency statement, not legal terms, a "
    "privacy policy, or a client contract."
)
SCOPE_FINAL = SCOPE_PENDING.replace("a proposed public", "a public")
REVIEW_NOTE = f"> {REVIEW_PREFIX}{SCOPE_PENDING}"
DATE_TOKEN = "YYYY-MM-DD"
PENDING_PREFIX = "Pending Kris Krüg's review and approval:"
PENDING_HEADING = "Proposed AI-assistance disclosure"
FINAL_HEADING = "AI-assistance disclosure"
PENDING_WORDING = re.compile(r"pending|proposed", re.IGNORECASE)
PENDING_ONLY_TEXT = (
    DATE_TOKEN,
    "Pending Kris Krüg",
    "Proposed AI-assistance",
    "proposed public transparency",
)
# Stands in for Kris's approval only while page-meta.json records none. Once it
# records one, the tests use that date instead.
SIMULATED_APPROVAL = {"date": "2031-01-01", "record": "simulated in tests"}
CRAWLER_CLAIM = (
    "My public site is intentionally open to search and AI crawlers for discovery "
    "and citation."
)
CRAWLER_WORD = re.compile(
    r"\bcrawl(?:er|ers|ing)?\b|\bbots?\b|\bscrap(?:e|er|ers|ing)\b"
)
BLOCKING_WORD = re.compile(
    r"\b(?:block(?:s|ed|ing)?|disallow(?:s|ed)?|opts? out|opted out|not allowed|"
    r"forbid(?:s|den)?|ban(?:s|ned)?|keeps? out|shut out)\b"
)
AI_CRAWLER_AGENTS = frozenset(
    {
        "*",
        "oai-searchbot",
        "gptbot",
        "chatgpt-user",
        "claudebot",
        "claude-user",
        "claude-searchbot",
        "perplexitybot",
        "perplexity-user",
        "google-extended",
        "applebot-extended",
        "ccbot",
        "amazonbot",
        "cohere-ai",
        "bytespider",
    }
)
MAX_PARAGRAPH_WORDS = 80
MAX_HEADING_CHARS = 60


def squash(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def has_em_dash(value: str) -> bool:
    return bool(EM_DASH.search(value)) or DOUBLE_HYPHEN in value


class PayloadDoc(HTMLParser):
    """Reading-order view of the payload: what remains with CSS switched off."""

    def __init__(self, html: str):
        super().__init__(convert_charrefs=True)
        self.elements: list[tuple[str, dict[str, str]]] = []
        self.headings: list[tuple[int, str, str]] = []
        self.links: list[tuple[str, str, dict[str, str]]] = []
        self.items: list[str] = []
        self.paragraphs: list[str] = []
        self.strong: list[str] = []
        self._chunks: list[str] = []
        self._open: list[tuple[str, dict[str, str], list[str]]] = []
        self.feed(html)
        self.close()

    def handle_starttag(self, tag, attrs):
        attrs = {name: value or "" for name, value in attrs}
        self.elements.append((tag, attrs))
        if tag in BLOCK_TAGS:
            self._chunks.append(" ")
        if re.fullmatch(r"h[1-6]", tag) or tag in {"a", "li", "p", "strong"}:
            self._open.append((tag, attrs, []))

    def handle_endtag(self, tag):
        if tag in BLOCK_TAGS:
            self._chunks.append(" ")
        for index in range(len(self._open) - 1, -1, -1):
            if self._open[index][0] != tag:
                continue
            _, attrs, parts = self._open.pop(index)
            text = squash("".join(parts))
            if tag == "a":
                self.links.append((attrs.get("href", ""), text, attrs))
            elif tag == "li":
                self.items.append(text)
            elif tag == "p":
                self.paragraphs.append(text)
            elif tag == "strong":
                self.strong.append(text)
            else:
                self.headings.append((int(tag[1]), text, attrs.get("id", "")))
            break

    def handle_data(self, data):
        self._chunks.append(data)
        for _, _, parts in self._open:
            parts.append(data)

    @property
    def text(self) -> str:
        return squash("".join(self._chunks))


def policy_lines(policy_md: str) -> list[str]:
    return [
        f"> {SCOPE_PENDING}" if line == REVIEW_NOTE else line
        for line in policy_md.splitlines()
        if line != TITLE_LINE
    ]


def markdown_inline_text(line: str) -> str:
    line = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", line)
    return line.replace("**", "").replace("`", "")


def policy_body_text(policy_md: str) -> str:
    kept = []
    for line in policy_lines(policy_md):
        line = re.sub(r"^(?:#{2,6} |> |- )", "", line)
        kept.append(markdown_inline_text(line))
    return squash(" ".join(kept))


def policy_headings(policy_md: str) -> list[tuple[int, str]]:
    found = []
    for line in policy_lines(policy_md):
        match = re.match(r"^(#{2,6}) (.+)$", line)
        if match:
            found.append((len(match.group(1)), markdown_inline_text(match.group(2))))
    return found


def policy_links(policy_md: str) -> list[tuple[str, str]]:
    return [
        (url, text) for text, url in re.findall(r"\[([^\]]+)\]\(([^)]+)\)", policy_md)
    ]


def policy_list_items(policy_md: str) -> list[str]:
    return [
        markdown_inline_text(line[2:])
        for line in policy_lines(policy_md)
        if line.startswith("- ")
    ]


def comparable(text: str) -> str:
    """Neutralize the four spans the publish step is allowed to change."""
    text = re.sub(
        r"Last updated: (?:YYYY-MM-DD|\d{4}-\d{2}-\d{2})", "Last updated: <date>", text
    )
    text = text.replace(f"{PENDING_PREFIX} ", "")
    text = text.replace(SCOPE_PENDING, SCOPE_FINAL)
    return text.replace(PENDING_HEADING, FINAL_HEADING)


def first_difference(expected: str, actual: str) -> str:
    want, got = expected.split(), actual.split()
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(
        a=want, b=got, autojunk=False
    ).get_opcodes():
        if tag != "equal":
            return f"policy.md has {' '.join(want[i1 : i2 + 3])!r}, payload has {' '.join(got[j1 : j2 + 3])!r}"
    return "texts differ only in whitespace"


def audit(html: str, meta: dict, policy_md: str) -> list[str]:
    """Every way the payload breaks its contract, as 'category: detail' strings."""
    failures: list[str] = []
    doc = PayloadDoc(html)
    text = doc.text

    for tag, attrs in doc.elements:
        if tag in FORBIDDEN_TAGS:
            failures.append(f"{tag}: <{tag}> is not allowed in the body")
        for name in attrs:
            if name == "style":
                failures.append(f"style: inline style on <{tag}>")
            elif name.startswith("on"):
                failures.append(f"script: event handler {name} on <{tag}>")
        for token in attrs.get("class", "").split():
            if token not in AURORA_CLASSES:
                failures.append(f"class: {token!r} is not an Aurora content primitive")
    failures.extend(f"class: retired {token!r}" for token in retired_class_tokens(html))
    if re.search(r"<style\b", html, re.IGNORECASE):
        failures.append("style: <style> block")

    for pattern in PRIVATE_PATTERNS:
        if re.search(pattern, html, re.IGNORECASE):
            failures.append(f"private-url: matched {pattern!r}")
    for href, label, attrs in doc.links:
        parts = urlsplit(href)
        if parts.scheme != "https" or parts.hostname not in ALLOWED_HOSTS:
            failures.append(f"link: {href!r} is not https on an allowed host")
        if attrs.get("target") and "noopener" not in attrs.get("rel", "").split():
            failures.append(f"link: {href!r} opens a new context without rel=noopener")
        if label.lower() in GENERIC_LINK_TEXT or label.startswith(
            ("http://", "https://")
        ):
            failures.append(f"link: {href!r} has non-descriptive text {label!r}")

    # The raw pass covers attributes. The parsed pass covers every entity form
    # and skips the block comments, which legitimately contain "--".
    if EM_DASH.search(html) or has_em_dash(text):
        failures.append(
            "em-dash: the payload has an em dash, or a '--' WordPress turns into one"
        )
    if has_em_dash(policy_md):
        failures.append("em-dash: policy.md has an em dash or a '--'")
    try:
        sent = storable_payload({"title": meta["title"], "content": html})
    except UnstorableText as exc:
        failures.append(f"cp1252: {exc}")
    else:
        if sent["content"] != html:
            failures.append(
                "cp1252: payload needs numeric references; store them in the file"
            )

    levels = [level for level, _, _ in doc.headings]
    if levels[:1] != [2]:
        failures.append("headings: the body must open at h2 below the template h1")
    for previous, current in zip(levels, levels[1:]):
        if current > previous + 1:
            failures.append(f"headings: h{previous} jumps to h{current}")
    ids = [heading_id for _, _, heading_id in doc.headings]
    if not all(
        re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", heading_id) for heading_id in ids
    ):
        failures.append("headings: every heading needs a lowercase slug id")
    if len(set(ids)) != len(ids):
        failures.append("headings: heading ids repeat")

    expected = comparable(policy_body_text(policy_md))
    if comparable(text) != expected:
        failures.append(f"drift: {first_difference(expected, comparable(text))}")
    if [(level, comparable(label)) for level, label, _ in doc.headings] != [
        (level, comparable(label)) for level, label in policy_headings(policy_md)
    ]:
        failures.append("drift: headings differ from policy.md")
    if [(href, label) for href, label, _ in doc.links] != policy_links(policy_md):
        failures.append("drift: links differ from policy.md")
    if doc.items != policy_list_items(policy_md):
        failures.append("drift: list items differ from policy.md")

    if CRAWLER_CLAIM not in text:
        failures.append("crawler: the open-crawler statement is missing")
    for sentence in re.split(r"(?<=[.!?])\s+", text):
        lowered = sentence.lower()
        if CRAWLER_WORD.search(lowered) and BLOCKING_WORD.search(lowered):
            failures.append(f"crawler: says crawlers are blocked: {sentence[:80]!r}")

    updated = re.findall(r"Last updated: (\S+)", text)
    approval = meta.get("publish_approval")
    if len(updated) != 1:
        failures.append(f"date: expected one 'Last updated' line, found {len(updated)}")
    disclosure_heads = [
        label
        for _, label, _ in doc.headings
        if label in (PENDING_HEADING, FINAL_HEADING)
    ]
    if len(disclosure_heads) != 1:
        failures.append(
            "approval: expected exactly one AI-assistance disclosure heading"
        )
    if approval is None:
        if updated and updated[0] != DATE_TOKEN:
            failures.append(
                f"date: 'Last updated' is filled ({updated[0]}) before publish approval"
            )
        if (
            disclosure_heads != [PENDING_HEADING]
            or f"{PENDING_PREFIX} AI assisted" not in text
            or SCOPE_PENDING not in text
        ):
            failures.append(
                "approval: the body reads as approved but page-meta.json records none"
            )
    else:
        if updated and updated[0] != approval["date"]:
            failures.append(
                f"date: 'Last updated' is {updated[0]}, "
                f"publish approval is dated {approval['date']}"
            )
        if disclosure_heads != [FINAL_HEADING] or PENDING_WORDING.search(text):
            failures.append("approval: pending wording survived publish approval")
        for marker in meta["publish_absent_markers"]:
            if marker in html or marker in text:
                failures.append(
                    f"absent: {marker!r} is still in the body after publish approval"
                )
    if "remains accountable for it." not in text:
        failures.append("approval: disclosure no longer says Kris remains accountable")

    for marker in meta.get("readback_markers", []):
        if marker not in html:
            failures.append(f"marker: {marker!r} missing")
    return failures


def publish_edit_pairs(meta: dict) -> list[tuple[str, str]]:
    publish_date = meta["publish_approval"]["date"]
    return [
        (edit["find"], edit["replace"].format(publish_date=publish_date))
        for edit in meta["publish_edits"]
    ]


def apply_publish_edits(html: str, meta: dict) -> str:
    for pending, final in publish_edit_pairs(meta):
        html = html.replace(pending, final)
    return html


def revert_publish_edits(html: str, meta: dict) -> str:
    for pending, final in publish_edit_pairs(meta):
        html = html.replace(final, pending)
    return html


def robots_groups(robots: str) -> list[tuple[list[str], list[tuple[str, str]]]]:
    groups: list[tuple[list[str], list[tuple[str, str]]]] = []
    agents: list[str] = []
    rules: list[tuple[str, str]] = []
    for raw in robots.splitlines():
        field, _, value = raw.split("#", 1)[0].partition(":")
        field, value = field.strip().lower(), value.strip()
        if field == "user-agent":
            if rules:
                groups.append((agents, rules))
                agents, rules = [], []
            agents.append(value.lower())
        elif field in {"allow", "disallow"}:
            rules.append((field, value))
    if agents:
        groups.append((agents, rules))
    return groups


def robots_blocks_ai(robots: str) -> list[str]:
    blocked = []
    for agents, rules in robots_groups(robots):
        covered = sorted(set(agents) & AI_CRAWLER_AGENTS)
        if covered and any(
            field == "disallow" and value in {"/", "/*"} for field, value in rules
        ):
            blocked.append(
                f"crawler: robots.txt disallows the whole site for {', '.join(covered)}"
            )
    return blocked


class AiPolicyPayloadTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.meta = json.loads(META_PATH.read_text(encoding="utf-8"))
        cls.payload_path = PACK / cls.meta["payload"]
        cls.html = cls.payload_path.read_text(encoding="utf-8")
        cls.policy = (PACK / cls.meta["source"]["policy"]).read_text(encoding="utf-8")
        cls.doc = PayloadDoc(cls.html)
        # Both gate states are built from whichever one is committed, so the
        # suite runs the same way before and after publish approval.
        if cls.meta["publish_approval"] is None:
            cls.pending_html, cls.pending_meta = cls.html, cls.meta
            cls.released_meta = {
                **cls.meta,
                "status_target": "publish",
                "publish_approval": SIMULATED_APPROVAL,
            }
            cls.released_html = apply_publish_edits(cls.html, cls.released_meta)
        else:
            cls.released_html, cls.released_meta = cls.html, cls.meta
            cls.pending_meta = {
                **cls.meta,
                "status_target": "draft",
                "publish_approval": None,
            }
            cls.pending_html = revert_publish_edits(cls.html, cls.meta)
        cls.publish_date = cls.released_meta["publish_approval"]["date"]

    def assertFailsWith(self, category, html=None, meta=None, policy=None):
        failures = audit(
            self.html if html is None else html,
            meta or self.meta,
            self.policy if policy is None else policy,
        )
        self.assertTrue(
            any(failure.startswith(f"{category}:") for failure in failures),
            f"expected a {category!r} failure, got {failures}",
        )

    def test_payload_meets_its_contract(self):
        self.assertEqual([], audit(self.html, self.meta, self.policy))

    def test_payload_is_one_gutenberg_html_block(self):
        stripped = self.html.strip()
        self.assertTrue(
            stripped.startswith("<!-- wp:html -->\n<!-- ai-policy-2026:page -->")
        )
        self.assertTrue(stripped.endswith("<!-- /wp:html -->"))
        self.assertEqual(1, self.html.count("<!-- wp:"))

    def test_source_is_the_reviewed_policy(self):
        for key in ("policy", "source_matrix"):
            data = (PACK / self.meta["source"][key]).read_bytes()
            self.assertEqual(
                self.meta["source"][f"{key}_sha256"],
                hashlib.sha256(data).hexdigest(),
                key,
            )
        lines = self.policy.splitlines()
        self.assertEqual(1, lines.count(TITLE_LINE))
        self.assertEqual(1, lines.count(REVIEW_NOTE))
        self.assertNotIn(REVIEW_PREFIX.strip(), self.doc.text)
        self.assertEqual(
            1,
            self.doc.text.count(
                "not legal terms, a privacy policy, or a client contract."
            ),
        )

    def test_metadata_contract(self):
        meta = self.meta
        self.assertEqual("ai-policy", meta["slug"])
        self.assertEqual(TITLE_LINE[2:], meta["title"])
        self.assertEqual("https://kriskrug.co/ai-policy/", meta["canonical_url"])
        self.assertEqual("wp-payloads/ai-policy.html", meta["payload"])
        self.assertIn(meta["status_target"], {"draft", "publish"})
        if meta["publish_approval"] is None:
            self.assertEqual("draft", meta["status_target"])
        else:
            self.assertRegex(meta["publish_approval"]["date"], r"^\d{4}-\d{2}-\d{2}$")
            date.fromisoformat(meta["publish_approval"]["date"])
            self.assertTrue(meta["publish_approval"]["record"].strip())
        wordpress_id = meta["wordpress_id"]
        self.assertTrue(
            wordpress_id is None or (type(wordpress_id) is int and wordpress_id > 0)
        )
        if meta["status_target"] == "publish":
            self.assertIsNotNone(wordpress_id)
        self.assertEqual(
            {"comment_status": "closed", "ping_status": "closed"},
            {key: meta[key] for key in ("comment_status", "ping_status")},
        )
        self.assertTrue(meta["readback_markers"])
        self.assertLessEqual(
            set(PENDING_ONLY_TEXT), set(meta["publish_absent_markers"])
        )
        self.assertFalse(
            set(meta["readback_markers"]) & set(meta["publish_absent_markers"])
        )

    def test_draft_record_does_not_overclaim_parity(self):
        draft = self.meta["wordpress_draft"]
        payload = self.payload_path.read_bytes()
        same = (
            hashlib.sha256(payload).hexdigest() == draft["content_sha256"]
            and len(payload) == draft["content_bytes"]
        )
        self.assertEqual(same, draft["matches_payload"])

    def test_metadata_copy_is_storable_and_plain(self):
        meta = self.meta
        title = meta["meta"]["jetpack_seo_html_title"]
        description = meta["meta"]["advanced_seo_description"]
        for field, value in (
            ("title", meta["title"]),
            ("excerpt", meta["excerpt"]),
            ("seo title", title),
            ("seo description", description),
        ):
            self.assertTrue(value.strip(), field)
            self.assertFalse(has_em_dash(value), f"{field} has an em dash")
        self.assertEqual(title, plain_meta_text(title, "jetpack_seo_html_title"))
        self.assertEqual(
            description, plain_meta_text(description, "advanced_seo_description")
        )
        storable = {"title": meta["title"], "excerpt": meta["excerpt"]}
        self.assertEqual(storable, storable_payload(storable))
        self.assertLessEqual(len(title), 60)
        self.assertGreaterEqual(len(description), 120)
        self.assertLessEqual(len(description), 160)

    def test_reads_in_order_without_css(self):
        text = self.doc.text
        approval = self.meta["publish_approval"]
        scope, updated = (
            (SCOPE_PENDING, DATE_TOKEN)
            if approval is None
            else (SCOPE_FINAL, approval["date"])
        )
        self.assertTrue(
            text.startswith(
                f"{scope} Last updated: {updated} "
                "The short version: Both Hands Full I use AI a lot."
            ),
            text[:200],
        )
        self.assertTrue(
            text.endswith("approved the final version and remains accountable for it.")
        )
        order = [label for _, label, _ in self.doc.headings]
        self.assertLess(
            order.index("What I will not fake"), order.index("I own what ships")
        )
        self.assertEqual(12, len(self.doc.items))

    def test_refusal_lines_are_text(self):
        text = self.doc.text
        for line in (
            "I will not use AI to invent:",
            "a person, quote, interview, source, testimonial, or credential;",
            "evidence that an event happened or that a real person was present;",
            "I will not put generated words in a collaborator's mouth.",
            "I will not let a photorealistic crowd function as proof of a gathering.",
            "The refusal lines around fake people, fake evidence, stolen voice, and hidden accountability",
        ):
            self.assertIn(line, text)

    def test_mobile_scan_density(self):
        for _, label, _ in self.doc.headings:
            self.assertLessEqual(len(label), MAX_HEADING_CHARS, label)
        for paragraph in self.doc.paragraphs:
            self.assertLessEqual(
                len(paragraph.split()), MAX_PARAGRAPH_WORDS, paragraph[:60]
            )

    def test_sources_and_contact_path_are_linked(self):
        hrefs = [href for href, _, _ in self.doc.links]
        self.assertEqual(9, len(hrefs))
        self.assertEqual("https://kriskrug.co/contact/", hrefs[-1])
        self.assertEqual(ALLOWED_HOSTS, {urlsplit(href).hostname for href in hrefs})

    def test_crawler_claim_matches_robots_txt(self):
        robots = ROBOTS_PATH.read_text(encoding="utf-8")
        self.assertIn(CRAWLER_CLAIM, self.doc.text)
        self.assertEqual([], robots_blocks_ai(robots))
        self.assertIn(
            "gptbot", {agent for agents, _ in robots_groups(robots) for agent in agents}
        )

    def test_crawler_check_catches_a_blocking_robots_txt(self):
        robots = ROBOTS_PATH.read_text(encoding="utf-8").replace(
            "Allow: /\n", "Disallow: /\n"
        )
        self.assertTrue(robots_blocks_ai(robots))

    def test_committed_body_matches_the_recorded_gate_state(self):
        approval = self.meta["publish_approval"]
        text = self.doc.text
        if approval is None:
            self.assertEqual("draft", self.meta["status_target"])
            self.assertIn(f"Last updated: {DATE_TOKEN}", text)
            self.assertIn(SCOPE_PENDING, text)
            for edit in self.meta["publish_edits"]:
                self.assertEqual(1, self.html.count(edit["find"]), edit["find"])
        else:
            self.assertIn(f"Last updated: {approval['date']}", text)
            self.assertIn(SCOPE_FINAL, text)
            for leftover in (DATE_TOKEN, "Pending", "Proposed"):
                self.assertNotIn(leftover, self.html)
                self.assertNotIn(leftover, text)
            self.assertIsNone(PENDING_WORDING.search(text))
            for pending, final in publish_edit_pairs(self.meta):
                self.assertEqual(0, self.html.count(pending), pending)
                self.assertEqual(1, self.html.count(final), final)

    def test_gate_states_convert_both_ways(self):
        # An empty replacement could not be found again in the final page, and
        # the pending page could then not be rebuilt once approval is recorded.
        for pending, final in publish_edit_pairs(self.released_meta):
            self.assertTrue(final, pending)
            self.assertEqual(1, self.pending_html.count(pending), pending)
            self.assertEqual(1, self.released_html.count(final), final)
            self.assertEqual(0, self.released_html.count(pending), pending)
        self.assertEqual(
            self.released_html,
            apply_publish_edits(self.pending_html, self.released_meta),
        )
        self.assertEqual(
            self.pending_html,
            revert_publish_edits(self.released_html, self.released_meta),
        )
        for marker in self.meta["publish_absent_markers"]:
            self.assertIn(marker, self.pending_html)
            self.assertNotIn(marker, self.released_html)

    def test_pending_page_passes_and_refuses_an_early_release(self):
        html, meta = self.pending_html, self.pending_meta
        self.assertEqual([], audit(html, meta, self.policy))
        cases = (
            (
                "date",
                "date filled early",
                html.replace(
                    f"Last updated: {DATE_TOKEN}", f"Last updated: {self.publish_date}"
                ),
            ),
            (
                "approval",
                "pending prefix removed",
                html.replace(f"<strong>{PENDING_PREFIX}</strong> ", ""),
            ),
            (
                "approval",
                "heading renamed",
                html.replace(PENDING_HEADING, FINAL_HEADING),
            ),
            (
                "approval",
                "scope sentence no longer proposed",
                html.replace(SCOPE_PENDING, SCOPE_FINAL),
            ),
            ("approval", "final body without approval", self.released_html),
        )
        for category, name, mutated in cases:
            with self.subTest(name):
                self.assertNotEqual(html, mutated, "mutation did not apply")
                self.assertFailsWith(category, html=mutated, meta=meta)

    def test_released_page_passes_and_refuses_pending_leftovers(self):
        html, meta = self.released_html, self.released_meta
        self.assertEqual([], audit(html, meta, self.policy))
        self.assertIn(f"Last updated: {self.publish_date}", PayloadDoc(html).text)
        another_date = (
            date.fromisoformat(self.publish_date) + timedelta(days=1)
        ).isoformat()
        disclosure = "<p>AI assisted with research"
        cases = (
            (
                "date",
                "not the approval date",
                html.replace(self.publish_date, another_date),
            ),
            (
                "date",
                "placeholder date left",
                html.replace(self.publish_date, DATE_TOKEN),
            ),
            (
                "approval",
                "pending heading left",
                html.replace(f">{FINAL_HEADING}<", f">{PENDING_HEADING}<"),
            ),
            (
                "approval",
                "pending prefix left",
                html.replace(
                    disclosure,
                    f"<p><strong>{PENDING_PREFIX}</strong> AI assisted with research",
                ),
            ),
            (
                "approval",
                "scope sentence still proposed",
                html.replace(SCOPE_FINAL, SCOPE_PENDING),
            ),
            ("approval", "no edit applied", self.pending_html),
            (
                "absent",
                "marker spelled with an entity",
                html.replace(
                    disclosure, "<p>Pending Kris Kr&uuml;g: AI assisted with research"
                ),
            ),
        )
        for category, name, mutated in cases:
            with self.subTest(name):
                self.assertNotEqual(html, mutated, "mutation did not apply")
                self.assertFailsWith(category, html=mutated, meta=meta)
        for pending, final in publish_edit_pairs(meta):
            with self.subTest(unapplied=pending):
                self.assertFailsWith(
                    "absent", html=html.replace(final, pending), meta=meta
                )

    def test_safety_mutations_are_rejected(self):
        lead = '<p class="aurora-page-lead">'
        contact = 'href="https://kriskrug.co/contact/"'
        mutations = {
            "h1": self.html.replace(
                "<!-- ai-policy-2026:page -->",
                "<!-- ai-policy-2026:page -->\n<h1>Policy</h1>",
            ),
            "style": self.html.replace(
                lead, '<p class="aurora-page-lead" style="color:#00e5ff">'
            ),
            "script": self.html.replace(
                "</section>", "<script>alert(1)</script></section>", 1
            ),
            "class": self.html.replace(lead, '<p class="kk-lead">'),
            "private-url": self.html.replace(
                contact, 'href="http://localhost:10003/contact/"'
            ),
            "link": self.html.replace(contact, 'href="https://example.com/contact/"'),
            "cp1252": self.html.replace(
                "I use AI a lot.</p>", f"I use AI a lot {NON_CP1252_CHAR}</p>"
            ),
            "drift": self.html.replace(
                "should be labelled near", "will always be labelled near"
            ),
            "crawler": self.html.replace(
                CRAWLER_CLAIM,
                "My public site blocks AI crawlers from discovery and citation.",
            ),
        }
        for category, html in mutations.items():
            with self.subTest(category=category):
                self.assertNotEqual(self.html, html, "mutation did not apply")
                self.assertFailsWith(category, html=html)
        for html in (
            self.html.replace(contact, 'href="https://www.notion.so/ai-policy-draft"'),
            self.html.replace(
                contact, 'href="https://kriskrug.co/?page_id=1&amp;preview=true"'
            ),
            self.html.replace(
                "the contact page</a>.",
                "the contact page</a>. Notes in /Users/someone/policy.md.",
            ),
        ):
            with self.subTest(category="private-url"):
                self.assertFailsWith("private-url", html=html)

    def test_scope_sentence_cannot_be_dropped_silently(self):
        without = self.html.replace(f"<p>{SCOPE_PENDING}</p>\n", "").replace(
            f"<p>{SCOPE_FINAL}</p>\n", ""
        )
        self.assertNotEqual(self.html, without, "mutation did not apply")
        self.assertFailsWith("drift", html=without)
        self.assertFailsWith("marker", html=without)

    def test_em_dashes_are_rejected_in_every_form(self):
        target = "Useful does not mean clean."
        self.assertEqual(1, self.html.count(target))
        self.assertEqual(1, self.policy.count(target))
        for form in (
            EM_DASH_CHAR,
            "&mdash;",
            "&#8212;",
            "&#08212;",
            "&#8212",
            "&#x2014;",
            "&#X002014;",
            "--",
            "---",
            "&#45;&#45;",
        ):
            with self.subTest(payload=form):
                self.assertFailsWith(
                    "em-dash", html=self.html.replace(target, f"Useful {form} clean.")
                )
        attribute = self.html.replace(
            '<h2 id="cost">', f'<h2 id="cost" title="Cost {EM_DASH_CHAR} prompt">'
        )
        self.assertNotEqual(self.html, attribute, "mutation did not apply")
        self.assertFailsWith("em-dash", html=attribute)
        for form in (EM_DASH_CHAR, "&mdash;", "&#08212;", "--", "---"):
            with self.subTest(policy=form):
                self.assertFailsWith(
                    "em-dash",
                    policy=self.policy.replace(target, f"Useful {form} clean."),
                )


if __name__ == "__main__":
    unittest.main()
