#!/usr/bin/env python3
"""Fail-closed structural audit for the generated static public site.

Checks every public HTML file for missing local href/src targets, duplicate
ids, and missing same-site HTML fragments.  External URLs and schemes are
reported only by count and are not fetched here; live HTTP verification is a
separate release step.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit


LOCAL_ATTRS = {"a": "href", "img": "src", "script": "src", "link": "href", "source": "src"}
IGNORED_SCHEMES = {"http", "https", "mailto", "tel", "data", "javascript"}


@dataclass(frozen=True)
class Reference:
    tag: str
    value: str


class SiteParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.references: list[Reference] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        element_id = values.get("id")
        if element_id:
            self.ids.append(element_id)
        attribute = LOCAL_ATTRS.get(tag)
        if attribute and values.get(attribute):
            self.references.append(Reference(tag, values[attribute] or ""))


def resolve_target(public: Path, source: Path, raw: str) -> tuple[Path | None, str, bool]:
    parsed = urlsplit(raw)
    if parsed.scheme.lower() in IGNORED_SCHEMES or parsed.netloc:
        return None, parsed.fragment, True
    path_text = unquote(parsed.path)
    if not path_text:
        return source, parsed.fragment, False
    # The Pages workflow copies research-review.html to _site/index.html.
    # Resolve the source-tree root route against that canonical source file.
    if path_text == "/":
        return (public / "research-review.html").resolve(), parsed.fragment, False
    if path_text.startswith("/"):
        target = public / path_text.lstrip("/")
    else:
        target = source.parent / path_text
    if path_text.endswith("/"):
        target = target / "index.html"
    return target.resolve(), parsed.fragment, False


def parse_html(path: Path) -> SiteParser:
    parser = SiteParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    return parser


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    cli.add_argument("--json", action="store_true")
    cli.add_argument("--max-errors", type=int, default=50)
    args = cli.parse_args()

    root = args.root.resolve()
    public = root / "public"
    baseline_path = root / "release" / "structural-audit-baseline.json"
    baseline = json.loads(baseline_path.read_text(encoding="utf-8"))
    if baseline.get("schemaVersion") != "public-site-structural-audit-baseline-v1":
        raise SystemExit("unsupported structural-audit baseline schema")
    approved = {
        (item["kind"], source, item["target"])
        for item in baseline.get("approvedExistingIssues", [])
        for source in item.get("sources", [])
    }
    html_files = sorted(public.rglob("*.html"))
    if not html_files:
        raise SystemExit("no public HTML files found")

    parsed_by_path = {path.resolve(): parse_html(path) for path in html_files}
    errors: list[dict[str, str]] = []
    local_refs = 0
    external_refs = 0
    checked_fragments = 0

    for source, parser in parsed_by_path.items():
        duplicates = sorted(name for name, count in Counter(parser.ids).items() if count > 1)
        for duplicate in duplicates:
            errors.append({"kind": "duplicate-id", "source": str(source.relative_to(public)), "target": duplicate})

        for reference in parser.references:
            target, fragment, external = resolve_target(public, source, reference.value)
            if external:
                external_refs += 1
                continue
            local_refs += 1
            assert target is not None
            try:
                target.relative_to(public)
            except ValueError:
                errors.append({"kind": "escapes-public", "source": str(source.relative_to(public)), "target": reference.value})
                continue
            if not target.exists():
                errors.append({"kind": "missing-target", "source": str(source.relative_to(public)), "target": reference.value})
                continue
            if fragment and target.suffix.lower() in {".html", ".htm"}:
                checked_fragments += 1
                target_parser = parsed_by_path.get(target)
                if target_parser is None:
                    target_parser = parse_html(target)
                    parsed_by_path[target] = target_parser
                if fragment not in set(target_parser.ids):
                    errors.append({"kind": "missing-fragment", "source": str(source.relative_to(public)), "target": reference.value})

    baselined = [
        error for error in errors
        if (error["kind"], error["source"], error["target"]) in approved
    ]
    unexpected = [
        error for error in errors
        if (error["kind"], error["source"], error["target"]) not in approved
    ]
    observed = {(error["kind"], error["source"], error["target"]) for error in errors}
    stale_baseline = sorted(approved - observed)
    result = {
        "schemaVersion": "public-site-structural-audit-v1",
        "htmlFiles": len(html_files),
        "localReferences": local_refs,
        "externalReferencesNotFetched": external_refs,
        "checkedHtmlFragments": checked_fragments,
        "baselinedIssueCount": len(baselined),
        "staleBaselineCount": len(stale_baseline),
        "errorCount": len(unexpected),
        "errors": unexpected[: max(0, args.max_errors)],
        "status": "pass" if not unexpected else "fail",
    }
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result)
    if unexpected:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
