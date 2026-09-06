#!/usr/bin/env python3
"""Generate the deterministic, latest-first public research-note index."""

from __future__ import annotations

import argparse
import html
import json
import re
import sys
from collections import defaultdict
from dataclasses import dataclass
from html.parser import HTMLParser
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
NOTES = PUBLIC / "notes"
OUTPUT = NOTES / "index.html"
NOTE_NAME = re.compile(r"^r0-(\d+)[a-z0-9]*\.html$")
RECAP_NAME = re.compile(r"^recap-r0-61-r0-(\d+)[a-z0-9]*\.html$")
INDEPENDENT_CHAPTERS = {
    "clay-b-two-scale-20260905": "CB.1",
    "clay-b-signed-scale-20260905": "CB.2",
    "clay-b-physical-adjoint-20260906": "CB.3",
    "clay-b-window-localisation-20260906": "CB.4",
    "clay-b-plateau-history-20260906": "CB.5",
    "clay-b-concentration-limits-20260906": "CB.6",
    "clay-b-pressure-geometry-20260906": "CB.7",
    "clay-b-pressure-quotient-20260906": "CB.8",
}


class TitleParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.parts: list[str] = []

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data: str) -> None:
        if self.in_title:
            self.parts.append(data)

    @property
    def title(self) -> str:
        return " ".join("".join(self.parts).split())


@dataclass(frozen=True)
class Note:
    slug: str
    code: str
    title: str
    major: int
    has_pdf: bool


def natural_key(value: str) -> tuple[int | str, ...]:
    """Return a stable natural key for identifiers such as 68b2fgh."""

    return tuple(
        int(part) if part.isdigit() else part
        for part in re.findall(r"\d+|[a-z]+", value.lower())
    )


def note_files() -> list[Path]:
    files = [path for path in NOTES.glob("r0-*.html") if NOTE_NAME.fullmatch(path.name)]
    if not files:
        raise RuntimeError("no public r0-*.html research notes found")
    return sorted(
        files,
        key=lambda path: natural_key(path.stem.removeprefix("r0-")),
        reverse=True,
    )


def parse_note(path: Path) -> Note:
    parser = TitleParser()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.close()
    if "｜" not in parser.title:
        raise RuntimeError(f"{path.name}: expected CODE｜TITLE document title")
    code, title = (part.strip() for part in parser.title.split("｜", 1))
    if not code.startswith("R0.") or not title:
        raise RuntimeError(f"{path.name}: malformed document title {parser.title!r}")
    match = NOTE_NAME.fullmatch(path.name)
    assert match is not None
    slug = path.stem
    return Note(
        slug=slug,
        code=code,
        title=title,
        major=int(match.group(1)),
        has_pdf=path.with_suffix(".pdf").is_file(),
    )


def release_to_slug(release: str) -> str:
    match = re.fullmatch(r"r0(\d{2})([a-z])", release)
    if match is None:
        raise RuntimeError("release manifest has malformed latestRecapRelease")
    return f"r0-{match.group(1)}{match.group(2)}"


def latest_recap_href() -> str:
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    site = json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8"))
    declared = manifest.get("latestRecapRelease")
    if not isinstance(declared, str):
        raise RuntimeError("release manifest must declare latestRecapRelease")
    public_code = declared.replace(
        "r0", "R0.", 1,
    ).upper()
    if site.get("latestRecapRelease") != public_code:
        raise RuntimeError("site-version latestRecapRelease disagrees with release manifest")
    expected = PUBLIC / f"recap-r0-61-{release_to_slug(declared)}.html"
    recaps = [
        path
        for path in PUBLIC.glob("recap-r0-61-r0-*.html")
        if RECAP_NAME.fullmatch(path.name)
    ]
    if not expected.is_file() or expected.is_symlink() or not recaps:
        raise RuntimeError("declared recap endpoint is not a regular public HTML file")
    latest = max(
        recaps,
        key=lambda path: natural_key(path.stem.removeprefix("recap-r0-61-r0-")),
    )
    if latest != expected:
        raise RuntimeError("maximum recap filename disagrees with declared milestone endpoint")
    return "/" + expected.name


def entry(note: Note) -> str:
    code = html.escape(note.code)
    title = html.escape(note.title)
    html_href = f"/notes/{note.slug}.html"
    if note.has_pdf:
        pdf = (
            f'<a class="file-link pdf" href="/notes/{note.slug}.pdf" '
            f'aria-label="Download {code} PDF">PDF</a>'
        )
    else:
        pdf = (
            f'<span class="file-link missing" data-pdf-missing="{note.slug}">'
            "PDF 未生成 · 历史笔记</span>"
        )
    return f'''          <li class="note-entry" data-note="{note.slug}">
            <article>
              <div class="entry-copy">
                <p class="note-code">{code}</p>
                <h3>{title}</h3>
              </div>
              <nav class="entry-files" aria-label="{code} files">
                <a class="file-link html" href="{html_href}" aria-label="Read {code} HTML">HTML</a>
                {pdf}
              </nav>
            </article>
          </li>'''


def independent_section(site: dict[str, object]) -> str:
    count = site.get("publicIndependentNoteCount", 0)
    if count == 0:
        return ""
    declared_html = site.get("latestIndependentResearchHtml")
    declared_pdf = site.get("latestIndependentResearchPdf")
    declared_id = site.get("latestIndependentNote")
    if not isinstance(declared_html, str) or not re.fullmatch(
        r"/notes/[a-z0-9]+(?:-[a-z0-9]+)*\.html", declared_html
    ):
        raise RuntimeError("malformed latestIndependentResearchHtml")
    if declared_pdf is not None and (
        not isinstance(declared_pdf, str)
        or declared_pdf != declared_html.removesuffix(".html") + ".pdf"
    ):
        raise RuntimeError("latest independent PDF must be null or match its HTML path")
    if not isinstance(declared_id, str):
        raise RuntimeError("latest independent identifier is missing")

    paths = list(NOTES.glob("clay-b-*.html"))
    if len(paths) != count:
        raise RuntimeError("publicIndependentNoteCount disagrees with the HTML inventory")
    if {path.stem for path in paths} != set(INDEPENDENT_CHAPTERS):
        raise RuntimeError("Clay-B chapter map disagrees with the HTML inventory")
    paths.sort(key=lambda path: int(INDEPENDENT_CHAPTERS[path.stem].split(".", 1)[1]), reverse=True)
    ordered_chapters = sorted(
        INDEPENDENT_CHAPTERS.values(), key=lambda chapter: int(chapter.split(".", 1)[1])
    )
    chapter_range = f"{ordered_chapters[0]}–{ordered_chapters[-1]}"

    rows = []
    for index, path in enumerate(paths):
        if not path.is_file() or path.is_symlink():
            raise RuntimeError("independent HTML must be a regular file")
        parser = TitleParser()
        parser.feed(path.read_text(encoding="utf-8"))
        parser.close()
        title = html.escape(parser.title)
        if not title:
            raise RuntimeError("independent note title is missing")
        slug = path.stem
        chapter = INDEPENDENT_CHAPTERS[slug]
        topic, date = slug.removeprefix("clay-b-").rsplit("-", 1)
        display_id = f"ClayB-{''.join(part.title() for part in topic.split('-'))}-{date}"
        href = f"/notes/{slug}.html"
        if index == 0:
            if href != declared_html or display_id != declared_id:
                raise RuntimeError("latest independent note metadata disagrees with its file")
            if (path.with_suffix(".pdf").is_file()) != isinstance(declared_pdf, str):
                raise RuntimeError("latest independent PDF metadata disagrees with inventory")
        pdf_path = path.with_suffix(".pdf")
        if pdf_path.is_file() and not pdf_path.is_symlink():
            pdf = f'<a class="file-link pdf" href="/notes/{slug}.pdf" aria-label="Download {display_id} PDF">PDF</a>'
        elif pdf_path.exists():
            raise RuntimeError("independent PDF must be a regular file")
        else:
            pdf = '<span class="file-link missing">按政策不生成 PDF</span>'
        rows.append(
            f'<li class="note-entry independent-entry" data-note="{slug}"><article>'
            f'<div class="entry-copy"><p class="note-code">{chapter} · {html.escape(display_id)}</p><h3>{title}</h3></div>'
            f'<nav class="entry-files" aria-label="{html.escape(display_id)} files">'
            f'<a class="file-link html" href="{href}" aria-label="Read {html.escape(display_id)} HTML">HTML</a>{pdf}'
            '</nav></article></li>'
        )

    return f'''      <section class="release-group independent-release-group" aria-labelledby="series-independent"><header class="group-header"><div><p>INDEPENDENT CLAY-B NOTES · {chapter_range}</p><h2 id="series-independent">Clay-B</h2></div><span>{count} NOTES</span></header><ol class="note-list">{"".join(rows)}</ol><p class="index-note">{chapter_range} 是 Clay-B 路线的独立章节号，不占用 R0 主序列编号，也不改变 R0.76L 的当前端点。自 ClayB-SignedScale-20260905 起，新发布只生成 HTML；既有 PDF 保留不动。</p></section>'''


def render(notes: list[Note]) -> str:
    site = json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8"))
    if site.get("publicHtmlNoteCount") != len(notes):
        raise RuntimeError(
            "site-version publicHtmlNoteCount does not match r0-*.html inventory"
        )
    if site.get("latestRelease") != notes[0].code:
        raise RuntimeError("site-version latestRelease does not match newest note")

    pdf_count = sum(note.has_pdf for note in notes)
    html_only_count = len(notes) - pdf_count
    groups: dict[int, list[Note]] = defaultdict(list)
    for note in notes:
        groups[note.major].append(note)

    sections = []
    for major in sorted(groups, reverse=True):
        rows = "\n".join(entry(note) for note in groups[major])
        sections.append(f'''      <section class="release-group" aria-labelledby="series-{major}">
        <header class="group-header">
          <div><p>SERIES</p><h2 id="series-{major}">R0.{major}</h2></div>
          <span><span>{len(groups[major])}</span> <span>篇</span></span>
        </header>
        <ol class="note-list">
{rows}
        </ol>
      </section>''')

    recap_href = latest_recap_href()
    recap_label = (
        "累计回顾"
        if site.get("latestRecapRelease") == notes[0].code
        else "上一大里程碑 recap"
    )
    version = html.escape(str(site["version"]))
    published_date = html.escape(str(site["publishedDate"]))
    latest = html.escape(notes[0].code)
    content = "\n\n".join(sections)
    independent = independent_section(site)
    if independent:
        content = independent + "\n\n" + content
    return f'''<!doctype html>
<html lang="zh-CN" data-site-version="{version}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>研究笔记总索引｜三维 Navier–Stokes 全局正则性问题</title>
  <meta name="description" content="按版本倒序排列的三维 Navier–Stokes 研究笔记总索引；HTML 全覆盖，PDF 只链接实际存在的文件。">
  <link rel="canonical" href="https://kasifa.github.io/notes/">
  <meta property="og:title" content="研究笔记总索引">
  <meta property="og:description" content="{len(notes)} 篇公开研究笔记，最新节点 {latest}。">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://kasifa.github.io/notes/">
  <link rel="icon" href="/favicon.svg" type="image/svg+xml">
  <link rel="stylesheet" href="/bilingual.css">
  <script defer src="/i18n-en.js?v={version}"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="/site-refresh.js?v={version}"></script>
  <style>
    :root {{
      color-scheme: light dark;
      --paper: #f2eddf;
      --paper-raised: #faf6ea;
      --ink: #241f1a;
      --muted: #6c6257;
      --line: #958979;
      --accent: #a43f2c;
      --accent-soft: #ead6bb;
      --shadow: rgba(50, 39, 27, .12);
    }}
    @media (prefers-color-scheme: dark) {{
      :root {{
        --paper: #181714;
        --paper-raised: #22201c;
        --ink: #ece3d1;
        --muted: #b9ad9b;
        --line: #665d52;
        --accent: #e08a68;
        --accent-soft: #3e3026;
        --shadow: rgba(0, 0, 0, .28);
      }}
    }}
    * {{ box-sizing: border-box; }}
    html {{ background: var(--paper); scroll-behavior: smooth; }}
    body {{
      margin: 0;
      color: var(--ink);
      background:
        linear-gradient(rgba(120, 102, 79, .045) 1px, transparent 1px) 0 0 / 100% 28px,
        var(--paper);
      font-family: Georgia, "Songti SC", "Noto Serif CJK SC", serif;
      line-height: 1.55;
    }}
    a {{ color: inherit; }}
    a:focus-visible {{ outline: 3px double var(--accent); outline-offset: 3px; }}
    .skip-link {{
      position: fixed;
      top: 8px;
      left: 8px;
      z-index: 20;
      padding: 8px 12px;
      color: var(--paper-raised);
      background: var(--ink);
      transform: translateY(-160%);
    }}
    .skip-link:focus {{ transform: none; }}
    .masthead {{ border-top: 6px solid var(--ink); border-bottom: 1px solid var(--line); }}
    .masthead-inner, main, .footer-inner {{ width: min(1080px, calc(100% - 32px)); margin: 0 auto; }}
    .masthead-inner {{
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 18px;
      min-height: 58px;
    }}
    .brand {{ font-weight: 700; text-decoration: none; }}
    .masthead nav {{ display: flex; flex-wrap: wrap; gap: 16px; }}
    .masthead nav a {{
      color: var(--muted);
      font: 700 11px/1.3 "SFMono-Regular", Consolas, monospace;
      letter-spacing: .04em;
      text-decoration: none;
      text-transform: uppercase;
    }}
    .masthead nav a:hover {{ color: var(--accent); }}
    .hero {{ padding: clamp(58px, 10vw, 112px) 0 52px; }}
    .eyebrow, .note-code, .group-header p {{
      margin: 0;
      color: var(--accent);
      font: 700 11px/1.4 "SFMono-Regular", Consolas, monospace;
      letter-spacing: .09em;
      text-transform: uppercase;
    }}
    h1 {{
      max-width: 820px;
      margin: 14px 0 20px;
      font-size: clamp(42px, 8vw, 84px);
      font-weight: 600;
      letter-spacing: -.045em;
      line-height: .98;
    }}
    .lead {{ max-width: 760px; margin: 0; color: var(--muted); font-size: 18px; }}
    .stats {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      margin: 38px 0 0;
      border: 1px solid var(--line);
      background: var(--paper-raised);
      box-shadow: 7px 7px 0 var(--shadow);
    }}
    .stat {{ padding: 17px 18px; border-right: 1px solid var(--line); }}
    .stat:last-child {{ border-right: 0; }}
    .stat strong {{ display: block; font: 700 24px/1.1 "SFMono-Regular", Consolas, monospace; }}
    .stat span {{ color: var(--muted); font-size: 12px; }}
    .index-note {{
      margin: 22px 0 0;
      padding-left: 14px;
      border-left: 4px double var(--accent);
      color: var(--muted);
      font-size: 14px;
    }}
    main {{ padding-bottom: 84px; }}
    .release-group {{ margin-top: 50px; }}
    .group-header {{
      display: flex;
      align-items: end;
      justify-content: space-between;
      gap: 16px;
      padding-bottom: 10px;
      border-bottom: 4px double var(--ink);
    }}
    .group-header h2 {{ margin: 1px 0 0; font-size: 34px; line-height: 1; }}
    .group-header span {{ color: var(--muted); font: 700 12px/1.3 "SFMono-Regular", Consolas, monospace; }}
    .note-list {{ margin: 0; padding: 0; list-style: none; }}
    .note-entry {{ border-bottom: 1px solid var(--line); }}
    .note-entry article {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) auto;
      gap: 24px;
      align-items: center;
      padding: 18px 0;
    }}
    .note-entry h3 {{ margin: 5px 0 0; font-size: clamp(17px, 2.4vw, 22px); font-weight: 600; line-height: 1.3; }}
    .entry-files {{ display: flex; flex-wrap: wrap; justify-content: flex-end; gap: 8px; }}
    .file-link {{
      display: inline-flex;
      align-items: center;
      min-height: 32px;
      padding: 5px 9px;
      border: 1px solid var(--line);
      background: var(--paper-raised);
      font: 700 10px/1.25 "SFMono-Regular", Consolas, monospace;
      letter-spacing: .05em;
      text-decoration: none;
      text-transform: uppercase;
    }}
    a.file-link:hover {{ border-color: var(--accent); color: var(--accent); }}
    .file-link.html {{ border: 3px double var(--accent); padding: 3px 7px; }}
    .file-link.missing {{ color: var(--muted); background: transparent; text-transform: none; }}
    footer {{ border-top: 1px solid var(--line); }}
    .footer-inner {{
      display: flex;
      justify-content: space-between;
      gap: 24px;
      padding: 26px 0 38px;
      color: var(--muted);
      font-size: 13px;
    }}
    @media (max-width: 720px) {{
      .masthead-inner, .footer-inner {{ align-items: flex-start; flex-direction: column; padding-top: 14px; padding-bottom: 14px; }}
      .stats {{ grid-template-columns: 1fr 1fr; }}
      .stat:nth-child(2) {{ border-right: 0; }}
      .stat:nth-child(-n+2) {{ border-bottom: 1px solid var(--line); }}
      .note-entry article {{ grid-template-columns: 1fr; gap: 12px; }}
      .entry-files {{ justify-content: flex-start; }}
    }}
    @media print {{
      :root {{ color-scheme: light; --paper: white; --paper-raised: white; --ink: black; --muted: #444; --line: #777; --accent: #333; --shadow: transparent; }}
      .masthead, .entry-files {{ display: none; }}
      .hero {{ padding-top: 30px; }}
      .release-group, .note-entry {{ break-inside: avoid; }}
    }}
  </style>
</head>
<body>
  <a class="skip-link" href="#content">跳到正文</a>
  <header class="masthead">
    <div class="masthead-inner">
      <a class="brand" href="/">ν · Navier–Stokes 研究记录</a>
      <nav aria-label="页面导航"><a href="/">研究主页</a><a href="{recap_href}">{recap_label}</a></nav>
    </div>
  </header>
  <main id="content">
    <header class="hero">
      <p class="eyebrow">Research notes · complete index · latest first</p>
      <h1>研究笔记总索引</h1>
      <p class="lead">全部公开研究笔记按版本倒序排列。HTML 全部保留；PDF 只在实际文件存在时提供下载。</p>
      <div class="stats" aria-label="索引统计">
        <div class="stat"><strong>{len(notes)}</strong><span>公开 HTML 笔记</span></div>
        <div class="stat"><strong>{pdf_count}</strong><span>同步 PDF</span></div>
        <div class="stat"><strong>{html_only_count}</strong><span>历史 HTML-only 笔记</span></div>
        <div class="stat"><strong>{latest}</strong><span>最新研究节点</span></div>
      </div>
      <p class="index-note">索引页本身不计入研究笔记总数。{html_only_count} 篇早期笔记尚无同名 PDF，页面明确标为历史 HTML-only，不生成失效下载链接。</p>
    </header>

{content}
  </main>
  <footer>
    <div class="footer-inner"><span>研究笔记总索引 · v{version} · {published_date}</span><span>最新节点 {latest} · 持续修订</span></div>
  </footer>
</body>
</html>
'''


def main() -> None:
    cli = argparse.ArgumentParser()
    cli.add_argument(
        "--check",
        action="store_true",
        help="fail if public/notes/index.html is absent or stale",
    )
    args = cli.parse_args()

    notes = [parse_note(path) for path in note_files()]
    rendered = render(notes)
    if args.check:
        if not OUTPUT.is_file() or OUTPUT.read_text(encoding="utf-8") != rendered:
            print("public/notes/index.html is missing or stale", file=sys.stderr)
            raise SystemExit(1)
        status = "current"
    else:
        OUTPUT.write_text(rendered, encoding="utf-8")
        status = "written"

    pdf_count = sum(note.has_pdf for note in notes)
    print(
        json.dumps(
            {
                "schemaVersion": "research-note-index-v1",
                "status": status,
                "htmlNotes": len(notes),
                "pdfNotes": pdf_count,
                "htmlOnlyNotes": len(notes) - pdf_count,
                "latest": notes[0].code,
                "oldest": notes[-1].code,
                "output": str(OUTPUT.relative_to(ROOT)),
            },
            ensure_ascii=False,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
