"""Boundary validation for the single Events catalog and its enrichment sources."""

from __future__ import annotations

from datetime import date, datetime
from ipaddress import ip_address
from urllib.parse import urlsplit

PUBLIC_STATUSES = frozenset({"confirmed", "scaffold"})
PRIVATE_STATUSES = frozenset(
    {"unconfirmed", "proposed", "unverified", "placeholder", "draft", "hidden", "omit"}
)
DOC_KINDS = ("recap", "photos", "video")


def normalize_status(value: object) -> str:
    status = value.strip().lower() if isinstance(value, str) else ""
    return status if status in PUBLIC_STATUSES | PRIVATE_STATUSES else "unconfirmed"


def public_status(event: dict) -> bool:
    return normalize_status(event.get("status")) in PUBLIC_STATUSES


def documentation_url(value: object, *, canonical_recap: bool = False) -> str:
    if not isinstance(value, str) or any(c.isspace() or c in '<>"\\' for c in value):
        raise ValueError("Documentation links must be absolute public HTTPS URLs")
    parts = urlsplit(value)
    host = parts.hostname or ""
    if (
        parts.scheme != "https"
        or not host
        or parts.username is not None
        or parts.password is not None
        or parts.port not in (None, 443)
        or host == "localhost"
        or host.endswith((".localhost", ".local"))
        or "." not in host
    ):
        raise ValueError("Documentation links must be absolute public HTTPS URLs")
    try:
        address = ip_address(host)
    except ValueError:
        address = None
    if address is not None and not address.is_global:
        raise ValueError("Documentation links cannot use a private address")
    if canonical_recap and host != "kriskrug.co":
        raise ValueError("recap_url must be an absolute HTTPS link on kriskrug.co")
    return value


def normalize_docs(event: dict) -> dict[str, list[str]]:
    raw = event.get("docs") or {}
    if not isinstance(raw, dict) or set(raw) - set(DOC_KINDS):
        raise ValueError("docs must contain only recap, photos and video slots")
    docs = {}
    for kind in DOC_KINDS:
        links = raw.get(kind) or []
        if isinstance(links, str):
            links = [links]
        if not isinstance(links, list):
            raise ValueError(f"docs.{kind} must be a URL or list of URLs")
        docs[kind] = list(dict.fromkeys(documentation_url(link) for link in links))
    if event.get("recap_url"):
        legacy = documentation_url(event["recap_url"], canonical_recap=True)
        docs["recap"] = [legacy] + [link for link in docs["recap"] if link != legacy]
    return docs


def validate_dates(event: dict) -> None:
    start = event.get("date")
    end = event.get("end")
    start_date = date.fromisoformat(str(start)) if start else None
    end_date = None
    if end:
        text = str(end)
        if "T" in text:
            instant = datetime.fromisoformat(text)
            if instant.tzinfo is None:
                raise ValueError("Event end timestamps require a timezone")
            end_date = instant.date()
        else:
            end_date = date.fromisoformat(text)
    if start_date and end_date and end_date < start_date:
        raise ValueError("Event end date precedes its start date")
    if public_status(event) and not start_date and not end_date:
        if event["status"] != "scaffold" or event.get("bucket_hint") != "past":
            raise ValueError(
                "Public events need a date; only historical scaffolds may omit it"
            )


def normalize_contract(event: dict) -> dict:
    normalized = dict(event)
    normalized["status"] = normalize_status(event.get("status"))
    validate_dates(normalized)
    normalized["docs"] = normalize_docs(event)
    return normalized


def index_events(events: list[dict], source: str) -> dict[str, dict]:
    indexed = {}
    for event in events:
        ident = event.get("id")
        if not isinstance(ident, str) or not ident:
            raise SystemExit(f"{source}: event without an id")
        if ident in indexed:
            raise SystemExit(f"{source}: duplicate event id '{ident}'")
        indexed[ident] = event
    return indexed


def merge_event(base: dict, overlay: dict) -> dict:
    merged = dict(base)
    for key, value in overlay.items():
        if value in (None, "", [], {}):
            continue
        if key == "status" and not public_status(base) and public_status(overlay):
            # Enrichment cannot grant permission withheld by the authoritative row.
            continue
        if key in {"image", "docs"}:
            nested = dict(merged.get(key) or {})
            for field, entry in value.items():
                if entry not in (None, "", [], {}):
                    nested[field] = entry
            merged[key] = nested
        else:
            merged[key] = value
    return merged


def validate_editions(events: list[dict]) -> None:
    claimed = {}
    for event in events:
        edition = event.get("edition")
        if edition is None:
            continue
        if isinstance(edition, bool) or not isinstance(edition, int) or edition < 1:
            raise ValueError(f"{event['id']}: edition must be a positive integer")
        if edition in claimed:
            raise ValueError(
                f"Meetup edition {edition} has two identities: {claimed[edition]}, {event['id']}"
            )
        claimed[edition] = event["id"]
