#!/usr/bin/env python3
"""Publish the R0.74S analytic package without changing frozen mathematics."""

from __future__ import annotations

import hashlib, html, json, re, shutil, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "1.92"
RELEASE = "r074s"
CODE = "R0.74S"
TITLE = "R0.74S｜时间可积性上限与组合 Morrey 阈值"
FIGURE_ID = "fig-r074s-temporal-morrey-threshold"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-74o.html": "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2",
    PUBLIC / "recap-r0-61-r0-74o.pdf": "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076",
}


def sha256(target: Path) -> str:
    return hashlib.sha256(target.read_bytes()).hexdigest()


def write_text(target: Path, value: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def write_json(target: Path, value: object) -> None:
    write_text(target, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replace_once_or_present(value: str, old: str, new: str, label: str) -> str:
    if new in value:
        return value
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def assert_recap() -> None:
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected recap drift: {target.relative_to(ROOT)}")


def verify_sources() -> None:
    expected = {
        "research/r074s_one_sided_ball_clock_no_gain.md": "178c3431f808fa0bb7c8bbf116bd2fdf8c7335eea75e93ba11f51d7eeba7f1af",
        "research/r074s_one_sided_ball_clock_certificate.json": "1afcea511445b75c05da034130c4f1719f4b129c1df496ba5b3f65025ff57219",
        "research/r074s_one_sided_ball_clock_primary_audit.md": "83093d667b0f0ac0af919651c4dd45f87e60b8d2ebde59017f8abdfbd33041b9",
        "research/r074s_one_sided_ball_clock_independent_audit.md": "5ee63f78699891801151171f7fa68e103e52b04d2cc07b20ce48c1d3dd31b209",
        "research/r074s_cross_channel_recombination_no_gain.md": "c24d3673a5e3315777b47fa9751f8546a7df99538b6b22df7566ceb8fdce2e03",
        "scripts/r074s_cross_channel_recombination_certificate.py": "88644cdb311987755777fb951d1eb2ce5e0bdf0e6b829399832def0d9c54cb7c",
        "scripts/r074s_cross_channel_recombination_certificate_independent.rb": "cd5d7afadbaa9a257681f82d9e373777ac735c7675359310fb3a6efffc10ecef",
        "research/r074s_cross_channel_recombination_certificate.json": "5cd6ce5ba59586154c39cdfc5904eec4894dd51370d0cb02c0cd51bff58f4a63",
        "research/r074s_cross_channel_recombination_certificate_report.md": "548a68ca6ae82ea5f18e22504ee41da507569da4c283dbb8506f24b384aba189",
        "research/r074s_dissipation_rayleigh_gate.md": "e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3",
        "research/r074s_dissipation_rayleigh_primary_audit.md": "304bc2b87b9eb97d4f46d8bc4a77da3b1f11e2c37e95e20956504bb4681b2175",
        "research/r074s_dissipation_rayleigh_independent_audit.md": "efc30eb21e8d4e125d4b189455d4419bca9b5d1f1effeb265edba1cdf4a48233",
        "scripts/r074s_dissipation_rayleigh_certificate.py": "61bb1322151b66fc0cf780d2dfc15e0e06dde9a6cc59cc192be1b8c9e8d5e76a",
        "scripts/r074s_dissipation_rayleigh_certificate_independent.rb": "a4ce5bb0d3f20f549e70b7196487fd9540a5ff7be658d4cd52573d65f1a77ff3",
        "research/r074s_dissipation_rayleigh_certificate.json": "4f26fefe25ec92cdae86c2a45f384d0ed87ab3afe83a7d9ef7829ff829be6be1",
        "research/r074s_dissipation_rayleigh_certificate_report.md": "5c566f53e378c9f3fba2a690c3962051142ac00990c1177548b9ae3e956b14cb",
        "research/r074s_defect_relaxed_total_rayleigh_excess.md": "0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab",
        "research/r074s_defect_relaxed_total_rayleigh_primary_audit.md": "dbcba5ea68899faf74e4d38c232c58fdd3a71f1b2dcefb1eb007fcf102cd4f73",
        "research/r074s_defect_relaxed_total_rayleigh_independent_audit.md": "d7cb626b07b735b6ef19c8ca20fff670795e32768f3224a756901b230183d875",
        "scripts/r074s_defect_relaxed_total_rayleigh_certificate.py": "18735df5a8eff96167ef6314dad04150636c800c276e2fcffc7cbd8177fce9cf",
        "scripts/r074s_defect_relaxed_total_rayleigh_certificate_independent.rb": "b18b0a0b9937b106c5879a9e28996dd6892ab53f19decb7bca4db38c70a11343",
        "research/r074s_defect_relaxed_total_rayleigh_certificate.json": "3639edbccfddd97781805ed121fc91407771b9bf051ffefae5a17ad80087c69c",
        "research/r074s_defect_relaxed_total_rayleigh_certificate_report.md": "3a6d1e263daa7041edc4083a76c38af44f4fbcd7d2efc8f57592eecbd19ec55a",
        "research/r074s_best_n_last_exit_equivalence.md": "85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd",
        "research/r074s_best_n_last_exit_primary_audit.md": "0d326d0b77e499c36aa10fac64db66d4c40e6f0599640df65c915ca8de5f58d1",
        "research/r074s_best_n_last_exit_independent_audit.md": "e67b0f6cfcfa15f8e0b7f4f96670e10a843aabd753dd25d7ce5684e6c993a634",
        "scripts/r074s_best_n_last_exit_certificate.py": "0f04b79049ecd92c4a366ad9916fc8b6da9220b2f5baee34726aef2d4feaee65",
        "scripts/r074s_best_n_last_exit_certificate_independent.rb": "d9c0674b79bc532c10366d317ccb10550f0bfd2a825127e87a4ef24633d3ae66",
        "research/r074s_best_n_last_exit_certificate.json": "26ee76d969d3aec5eec55d9fa981bce195538cc3e2464fc0ece2c46b7c4accf0",
        "research/r074s_best_n_last_exit_certificate_report.md": "1108b72113d84b90ebc5570c2c7b4bfaa1ccdc299525c557979b564109ab6481",
        "research/r074s_paid_branch_last_exit_residual.md": "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c",
        "research/r074s_paid_branch_last_exit_primary_audit.md": "cf7bbfcb01a5389878a2a9f65ffa0e083863f8f6478986bc10110cfd24e6446c",
        "research/r074s_paid_branch_last_exit_independent_audit.md": "cb33dd2a1fed8a58f285bdb3e7a053480c40b06a899d1a1bd3a18549b6b8125a",
        "scripts/r074s_paid_branch_last_exit_certificate.py": "2763b3fa575ce723a400b6c7e5654d0a64c8a9db470d79097dc5a77769a365a9",
        "research/r074s_paid_branch_last_exit_certificate.json": "8f37a8ce4d6513406297e6ce1e676ceaafa39776723bba839074120f206314de",
        "research/r074s_paid_branch_last_exit_certificate_report.md": "6e25a07a417f96907e5e17da6b561830b75aa1a44d0b4b13fa56107dc31e4a5f",
        "scripts/r074s_paid_branch_last_exit_certificate_independent.rb": "15b77560f41aa22d00447821be501ab5d3c992afa1001063c3ce986f2e9938c9",
        "research/r074s_shared_budget_terminal_trace_obstruction.md": "fd022de342b935e3e6e5fe0231f6b08ab9494e2bd38e23da15de6807f14d4693",
        "research/r074s_shared_budget_terminal_trace_primary_audit.md": "d8bf38f4337af366cd450a50622f7105b8925db37cd87c09ce839fe129a058d5",
        "research/r074s_shared_budget_terminal_trace_independent_audit.md": "cfabe4b389c31b7ddeab755f51db8cf7daa88875add33621b0722b4487520f65",
        "scripts/r074s_shared_budget_terminal_trace_certificate.py": "a397d27943fca4d4a487038b5c14956667c7d36b3be5eb069262d2593f8ad2de",
        "research/r074s_shared_budget_terminal_trace_certificate.json": "ea5c9f13ba412703995b2875a26c84fa20779457399ffa9117871b65fafaf8d0",
        "research/r074s_shared_budget_terminal_trace_certificate_report.md": "6e86813ab2b001a8f357af42d952a9104ba70859b32441148ad5cd3ab283ffc4",
        "scripts/r074s_shared_budget_terminal_trace_certificate_independent.rb": "b8309f6bf23d0c75b09c39814e1452e6890a8de712f2974ffbda003a53d7a154",
        "research/r074s_terminal_window_morrey_packing.md": "03d1ae1fffd22d59ccb5bae7d860e3bd9bb9ab2f9e5dd7aafbee43b19153f84f",
        "research/r074s_terminal_window_morrey_primary_audit.md": "77397f923a20cb51382031bc4a8da82944190d4273aca8c316864e053e4c9396",
        "research/r074s_terminal_window_morrey_independent_audit.md": "148a75ca1ed9fdba3d8e0df3d1681f0e3fa4997df76960498faf64ffab9b9c95",
        "scripts/r074s_terminal_window_morrey_certificate.py": "90529ecfd080d3554fc45b63f5734a86f8736834cd6a65365c03fc82fb927a5a",
        "research/r074s_terminal_window_morrey_certificate.json": "741cb443b35a447df112d8078b79150eb21d5de308c4835219e0aa54f5e5b9d6",
        "research/r074s_terminal_window_morrey_certificate_report.md": "e9d5ebee782751b2cad17a4b7a78829ee7c4da6b6d7b828a9d5bb8faadba36ad",
        "scripts/r074s_terminal_window_morrey_certificate_independent.rb": "9c34db7d87b7074febdf5cad4cf437c28be6747017002d45479b024b5a815741",
        "research/r074s_temporal_integrability_morrey_certificate.json": "095e8a7a0ba378ff2178a166cbed81e1f132be055d37165c945020a26466e330",
        "research/r074s_temporal_integrability_morrey_certificate_report.md": "c464af1617391beda5b077e13066629203d408519ab32ee89b2115475346fe2b",
        "research/r074s_temporal_integrability_morrey_independent_audit.md": "332bf2a5b4503b9456bc76b1067bc44cb2d788e37fa7f2e34f10211a700e7ce3",
        "research/r074s_temporal_integrability_morrey_primary_audit.md": "5910f46c0dd401d3766343d75ae3e68bdecb9d8416615fd8feb74d0f560adefd",
        "research/r074s_temporal_integrability_morrey_threshold.md": "d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de",
        "scripts/r074s_temporal_integrability_morrey_certificate.py": "eb313260c16431c1379d1b77a508b8bb7740ac713c014126c08e44bc2d0cfafb",
        "scripts/r074s_temporal_integrability_morrey_certificate_independent.rb": "520d52deb1ba56fb46f841e0856bd8eb14ec5dd4961c90dd3b9ec240f88c9720",
    }
    for relative, expected_hash in expected.items():
        if sha256(ROOT / relative) != expected_hash:
            raise RuntimeError(f"frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r074s_one_sided_ball_clock_certificate.json").read_text(encoding="utf-8"))
    if certificate["summary"] != {"exact_passed": 5, "exact_total": 5, "finite_passed": 7, "finite_total": 7, "negative_passed": 4, "negative_total": 4, "result": "PASS", "structural_passed": 55, "structural_total": 55}:
        raise RuntimeError("R0.74S certificate boundary drift")
    step6 = json.loads((ROOT / "research/r074s_cross_channel_recombination_certificate.json").read_text(encoding="utf-8"))
    if step6["summary"] != {"exact_passed": 4, "exact_total": 4, "finite_passed": 8, "finite_total": 8, "structural_passed": 58, "structural_total": 58, "negative_passed": 10, "negative_total": 10, "result": "PASS"}:
        raise RuntimeError("R0.74S Step 6 certificate boundary drift")
    step7 = json.loads((ROOT / "research/r074s_dissipation_rayleigh_certificate.json").read_text(encoding="utf-8"))
    if step7["summary"] != {"exact_passed": 16, "exact_total": 16, "finite_passed": 8, "finite_total": 8, "negative_mutations_passed": 9, "negative_mutations_total": 9, "structural_passed": 52, "structural_total": 52}:
        raise RuntimeError("R0.74S Step 7 certificate boundary drift")
    step8 = json.loads((ROOT / "research/r074s_defect_relaxed_total_rayleigh_certificate.json").read_text(encoding="utf-8"))
    if step8["summary"] != {"exact_passed": 16, "exact_total": 16, "finite_passed": 19, "finite_total": 19, "negative_mutations_passed": 20, "negative_mutations_total": 20, "structural_passed": 75, "structural_total": 75}:
        raise RuntimeError("R0.74S Step 8 final certificate boundary drift")
    step9 = json.loads((ROOT / "research/r074s_best_n_last_exit_certificate.json").read_text(encoding="utf-8"))
    if step9["summary"] != {"exact_passed": 9, "exact_total": 9, "finite_passed": 8, "finite_total": 8, "structural_passed": 57, "structural_total": 57, "negative_mutations_passed": 18, "negative_mutations_total": 18}:
        raise RuntimeError("R0.74S Step 9 certificate boundary drift")
    step10 = json.loads((ROOT / "research/r074s_paid_branch_last_exit_certificate.json").read_text(encoding="utf-8"))
    if step10["summary"] != {"exact_total": 12, "exact_passed": 12, "finite_total": 10, "finite_passed": 10, "structural_total": 79, "structural_passed": 79, "negative_mutations_total": 47, "negative_mutations_passed": 47}:
        raise RuntimeError("R0.74S Step 10 certificate boundary drift")
    step11 = json.loads((ROOT / "research/r074s_shared_budget_terminal_trace_certificate.json").read_text(encoding="utf-8"))
    if step11["summary"] != {"all_pass": True, "exact_passed": 14, "exact_total": 14, "finite_passed": 7, "finite_total": 7, "negative_passed": 7, "negative_total": 7, "structural_passed": 34, "structural_total": 34}:
        raise RuntimeError("R0.74S Step 11 certificate boundary drift")
    step12 = json.loads((ROOT / "research/r074s_terminal_window_morrey_certificate.json").read_text(encoding="utf-8"))
    if step12["summary"] != {"all_pass": True, "exact_passed": 16, "exact_total": 16, "finite_passed": 12, "finite_total": 12, "negative_passed": 11, "negative_total": 11, "structural_passed": 51, "structural_total": 51}:
        raise RuntimeError("R0.74S Step 12 certificate boundary drift")
    step13 = json.loads((ROOT / "research/r074s_temporal_integrability_morrey_certificate.json").read_text(encoding="utf-8"))
    if step13["overall_pass"] is not True or step13["summary"] != {"dependency_passed": 4, "dependency_total": 4, "exact_passed": 31, "exact_total": 31, "finite_passed": 11, "finite_total": 11, "negative_passed": 32, "negative_total": 32, "structural_passed": 22, "structural_total": 22}:
        raise RuntimeError("R0.74S Step 13 certificate boundary drift")


def inline_markup(value: str) -> str:
    value = html.escape(" ".join(value.split()))
    value = re.sub(r"\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2">\1</a>', value)
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", value)


def report_body() -> str:
    source = "\n\n".join([
        (ROOT / "research/r074s_report-source.md").read_text(encoding="utf-8").strip(),
        (ROOT / "research/r074s_step13_report-source.md").read_text(encoding="utf-8").strip(),
    ])
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 0
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                output.append("</section>")
            section_index += 1
            output.append(f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{inline_markup(lines[0][3:])}</h2>')
            section_open = True
            continue
        if lines[0].startswith("### "):
            output.append(f"<h3>{inline_markup(lines[0][4:])}</h3>")
            continue
        stripped = block.strip()
        if stripped.startswith(r"\[") and stripped.endswith(r"\]"):
            output.append(f'<div class="equation">{html.escape(stripped)}</div>')
            continue
        if all(line.startswith("- ") or line.startswith("  ") for line in lines):
            items, current = [], ""
            for line in lines:
                if line.startswith("- "):
                    if current:
                        items.append(current)
                    current = line[2:]
                else:
                    current += " " + line.strip()
            if current:
                items.append(current)
            output.append("<ul>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ul>")
            continue
        output.append(f"<p>{inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    return "\n".join(output)


def render_note() -> str:
    return f'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{TITLE}</title><meta name="description" content="固定解时间模量、线性 payment 方法上限、组合 Morrey 阈值与 critical cubic tree；PDE gates 仍开放">
<link rel="canonical" href="https://kasifa.github.io/notes/r0-74s.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.72 Georgia,"Songti SC","Noto Serif SC",serif}}.top{{border-top:5px solid var(--ink);border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}}.top a{{font-weight:700;text-decoration:none}}main{{width:min(940px,90vw);margin:auto}}.hero{{padding:54px 0 30px;border-bottom:1px solid var(--line)}}.hero-inner{{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,290px);gap:2rem}}.hero-inner>div:first-child>p strong{{margin-left:.25em}}h1{{font-size:clamp(2rem,5.7vw,3.8rem);line-height:1.08;margin:.35em 0}}h2{{margin:2.5rem 0 1rem;color:var(--rule);font-size:1.55rem}}.stamp,.section-no,.label{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.07em;text-transform:uppercase}}.stamp{{border:1px solid var(--line);padding:1rem;background:var(--raised)}}article{{padding:14px 0 72px}}section{{padding-bottom:.5rem;border-bottom:1px dotted var(--line)}}p,li{{overflow-wrap:anywhere}}.equation{{overflow:auto;background:var(--raised);padding:13px 15px;border-left:4px solid var(--rule);margin:1rem 0}}.labels{{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}}.label{{border:1px solid var(--line);padding:.28rem .55rem;background:var(--raised)}}a{{color:var(--rule)}}.files{{line-height:2}}.note{{color:var(--muted);font-size:.94rem}}picture img{{display:block;width:100%;height:auto}}@media(max-width:720px){{body{{font-size:15px}}.hero-inner{{grid-template-columns:1fr}}main,article,section{{min-width:0}}.top{{font-size:13px}}.equation mjx-container[display="true"]{{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}.top{{display:none}}body{{background:#fff;font-size:9.3pt;line-height:1.5}}main{{width:auto}}.hero{{padding-top:0}}.hero-inner{{grid-template-columns:1fr 220px}}h2{{margin:1.7rem 0 .6rem;break-after:avoid}}#figure{{break-before:page}}a{{color:inherit;text-decoration:none}}a[href]::after{{content:none!important}}.equation,.stamp{{break-inside:avoid}}}}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.74S · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.74S · 完整中文版本</div><h1>{TITLE}</h1><p>固定解的 \\(\\ell^1(L_t^{{4/3}})\\) 与 \\(\\delta^{{1/4}}\\) common-window modulus 已证；当前 linear-payment 路线的精确指数上限仍严格高于 \\(2/3\\)。 <strong>Morrey 与 Dini 接口保持 CONDITIONAL；PDE gates 仍 OPEN. NOT CLAY.</strong></p><div class="labels"><span class="label">PROVED FIXED-SOLUTION</span><span class="label">METHOD CEILING</span><span class="label">CONDITIONAL MORREY</span><span class="label">ABSTRACT TREE</span><span class="label">OPEN PDE GATES</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.74S STEP 13</strong><p>S.307–S.342：PROVED / CONDITIONAL / ABSTRACT / OPEN</p><p>fixed-solution sum：PROVED</p><p>common window：\\(\\delta^{{1/4}}\\)</p><p>linear ceiling：\\(&gt;2/3\\)</p><p>two-cap threshold：\\(2/3\\)</p><p>critical tree：ABSTRACT</p><p>S.328 / S.340：CONDITIONAL</p><p>S.342：OPEN</p><p>regularity：OPEN</p><p>非 simulation / DNS · NO DGX</p></div></div></header><article>
{report_body()}
<section id="figure"><div class="section-no">F / 正式解析示意图</div><h2>时间可积性上限、Morrey 2/3 阈值与 critical cubic tree</h2><picture><source srcset="/assets/r074s/{FIGURE_ID}.svg" type="image/svg+xml"><img src="/assets/r074s/{FIGURE_ID}.png" alt="R0.74S Step 13 analytic schematic of temporal and packing thresholds"></picture><p><a href="/assets/r074s/{FIGURE_ID}.pdf">矢量 PDF</a> · <a href="/assets/r074s/{FIGURE_ID}.png">600 dpi PNG</a> · <a href="/assets/r074s/{FIGURE_ID}.svg">SVG</a> · <a href="/figures/r074s/{FIGURE_ID}/source-data.csv">exact source data</a> · <a href="/figures/r074s/{FIGURE_ID}/manifest.json">manifest</a> · <a href="/figures/r074s/{FIGURE_ID}/qa-report.md">视觉 QA</a></p><p class="note">这是由精确公式与冻结证据生成的 <strong>analytic schematic</strong>，不是 simulation、DNS 或 NSE counterexample，也不是 regularity / Clay 证据。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 13 主文、证书与双重审计</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_temporal_integrability_morrey_threshold.md">Step 13 最终解析主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_temporal_integrability_morrey_primary_audit.md">Step 13 主审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_temporal_integrability_morrey_independent_audit.md">Step 13 独立审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_temporal_integrability_morrey_certificate.json">Step 13 机器证书 JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_temporal_integrability_morrey_certificate_report.md">Step 13 证书报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_claim_state_update.md">主张边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_literature_boundary.md">文献边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r074s_step13_report-source.md">Step 13 中文 reader source</a></p><p><a href="/notes/r0-74s.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-74o.html">上一大里程碑 recap（截止 R0.74O，157 节，未改动）</a> · <a href="/recap-r0-61-r0-74o.pdf">PDF</a></p><p class="note">Step 13：Python 31/31 exact、11/11 finite、22/22 structural、4/4 dependency、32/32 negative；Ruby 9/9 groups、72,027 cases、6/6 artifact locks、4/4 dependency locks、32/32 note checks、19 primary-audit cases、43 negative cases。有限证书不替代 analytic proof。</p></section>
<section id="next"><div class="section-no">NEXT / 本次不启动</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">Step 14 / R0.74T</h2><p style="margin:.15rem 0">本次发布到 Step 13 即停止。后续若另行启动，目标仍是 PDE-level incidence / Dini gain、S.342 与 bare-class S.328；不得把 conditional interface 写成 theorem。</p></section></article></main></body></html>'''


def copy_figures() -> None:
    source = ROOT / "figures/r074s" / FIGURE_ID
    for target in (PUBLIC / "figures/r074s" / FIGURE_ID, ROOT / "research/figures/r074s" / FIGURE_ID):
        if target.exists():
            shutil.rmtree(target)
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(source, target)
    assets = PUBLIC / "assets/r074s"
    assets.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "pdf", "png"):
        shutil.copy2(source / f"figure.{extension}", assets / f"{FIGURE_ID}.{extension}")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    pairs = (
        ('data-site-version="1.91"', 'data-site-version="1.92"', "home version"),
        ('/i18n-en.js?v=1.91', '/i18n-en.js?v=1.92', "home i18n"),
        ('/site-refresh.js?v=1.91.1', '/site-refresh.js?v=1.92.1', "home refresh"),
        ('<strong>v1.91</strong>网页版本', '<strong>v1.92</strong>网页版本', "home stat version"),
        ('<h3>R0.74S：终端公共窗口与 conditional Morrey packing</h3>', '<h3>R0.74S：时间可积性上限与组合 Morrey 阈值</h3>', "current route title"),
        ('<p class="tree-current-summary">short branch 已归约为连续的 common terminal window；excess branch 在统一 critical Morrey/path-length 假设下闭合。S.280、S.288、S.303 仍 OPEN。NOT CLAY。</p>', '<p class="tree-current-summary">固定解的时间模量已证；当前 linear-payment 路线严格达不到 2/3 目标。Morrey / Dini 结论保持 conditional，abstract witnesses 不是 NSE counterexamples。NOT CLAY。</p>', "current route summary"),
        ('<p class="tree-path">common terminal window → all-threshold layer cake → conditional moving-tube Morrey → universal gates remain open</p>', '<p class="tree-path">fixed-solution time sum → exact method ceiling → two-cap 2/3 threshold → critical cubic tree → PDE gates open</p>', "current route path"),
        ('综述 v1.91 · 2026-09-03', '综述 v1.92 · 2026-09-03', "footer"),
    )
    for old, new, label in pairs:
        page = replace_once_or_present(page, old, new, label)
    page, count = re.subn(r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.74S Step 13 已锁定 linear-payment 时间指数上限与 Morrey 2/3 / cubic Dini 阈值；S.328、S.340 仍 conditional，S.342 与 PDE packing gates 仍 OPEN。</span></div>', page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("home focus replacement failed")
    latest = '''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74S · 2026-09-03 · STEP 13</p><h2 class="route-map-title" id="latest-release-title">R0.74S｜时间可积性上限与组合 Morrey 阈值</h2><p class="route-map-intro">固定解时间模量已证；线性 payment 方法上限、two-cap 2/3 阈值与 critical cubic tree 已精确锁定。PDE gates 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74s.pdf">阅读最新 R0.74S 研究笔记 →</a><a href="/assets/r074s/fig-r074s-temporal-morrey-threshold.pdf">Step 13 正式解析示意图</a><a href="/recap-r0-61-r0-74o.html">最新大里程碑 recap（R0.61–R0.74O，157 节）</a><a href="/notes/">221 篇研究笔记总索引</a><a href="#r074s">查看首页 R0.74S 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74S · 123 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>98 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74S Step 13</span></div></div></section>'''
    page, count = re.subn(r'<section class="route-overview latest-release-spotlight" id="latest-release".*?</section>', lambda _: latest, page, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError("latest spotlight replacement failed")
    page = replace_once_or_present(page, '<a class="milestone" href="/notes/r0-74r.html">R0.74R</a>', '<a class="milestone" href="/notes/r0-74r.html">R0.74R</a>\n<a class="milestone" href="/notes/r0-74s.html">R0.74S</a>', "milestone")
    old_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74T</span><span class="tree-state current">下一检查点</span></div><h3>R0.74T 下一接口</h3><p>分别证明或反驳 common-window gate S.280 与 ancestor gate S.288，再检验 S.303；conditional Morrey theorem 不等于 bare suitable-weak closure。</p></article></div>'
    new_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74T</span><span class="tree-state current">未启动</span></div><h3>Step 14 / R0.74T 后续接口</h3><p>若另行启动：检验 PDE incidence / strict cubic Dini gain、S.342 与 bare-class S.328；本次发布不启动 Step 14。</p></article></div>'
    page = replace_once_or_present(page, old_next, new_next, "next route")
    page = replace_once_or_present(page, 'terminal-window convex packing / arbitrary-clock triage / no-exception no-go → common window → conditional Morrey packing → universal gates open</p>', 'terminal-window convex packing / arbitrary-clock triage / no-exception no-go → time-integrability ceiling → Morrey / cubic Dini thresholds → PDE gates open</p>', "path tail")
    card = '''          <div class="task-one" id="r074s" data-release="r074s" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.74S Step 13 · 2026-09-03</p><h3>R0.74S｜时间可积性上限与组合 Morrey 阈值</h3><p>固定解的时间模量已证；linear-payment ceiling、two-cap 2/3 threshold 与 critical cubic tree 已精确锁定。PDE gates 仍 OPEN。NOT CLAY.</p><p><a href="/notes/r0-74s.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-74s.pdf">PDF</a> · <a href="/assets/r074s/fig-r074s-temporal-morrey-threshold.pdf">正式解析示意图</a></p></div>\n'''
    page = re.sub(r'^[ \t]*<div class="task-one" id="r074s" data-release="r074s"[\s\S]*?</div>\n?', "", page, flags=re.M)
    anchor = '          <div class="task-one" id="r074r"'
    if anchor not in page:
        raise RuntimeError("home R card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.91"', 'data-site-version="1.92"', "lit version"), ('/i18n-en.js?v=1.91', '/i18n-en.js?v=1.92', "lit i18n"), ('文献综述 v1.91 · 2026-09-03', '文献综述 v1.92 · 2026-09-03', "lit footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    old = '<div class="route-step kept"><header><b>R0.74S</b><strong>终端公共窗口与 conditional Morrey packing</strong></header><p>S.273–S.280 把 short trace 归约为连续 common-window / all-threshold gate；S.285–S.300 给出 honest budget sum、conditional moving-tube Morrey theorem 与 mixed-norm benchmark。S.280、S.288、S.303 仍开放。<a href="/notes/r0-74s.html">研究笔记</a> <a href="#r074s-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74T</b><strong>universal window / ancestor packing</strong></header><p>分别证明或反驳 S.280 与 S.288，再检验 combined target S.303。</p></div>'
    new = '<div class="route-step kept"><header><b>R0.74S</b><strong>时间可积性上限与组合 Morrey 阈值</strong></header><p>S.307–S.325 给出 fixed-solution 时间模量、linear-payment exact ceiling 与 abstract saturation；S.326–S.341 给出 conditional Morrey inference、two-cap 2/3 threshold、heat-shear screen 与 critical cubic tree / Dini interface。S.342 与 PDE gates 仍开放。<a href="/notes/r0-74s.html">研究笔记</a> <a href="#r074s-boundary">主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.74T</b><strong>本次未启动</strong></header><p>若另行启动：检验 PDE incidence / strict cubic Dini gain、S.342 与 bare-class S.328。</p></div>'
    if new not in page and '<header><b>后续接口 · R0.74T</b>' in page:
        page = page.replace('<header><b>后续接口 · R0.74T</b>', '<header><b>开放接口 · R0.74T</b>', 1)
    else:
        page = replace_once_or_present(page, old, new, "literature route")
    boundary = '<h3 id="r074s-boundary">R0.74S 的文献与主张边界</h3><p>Step 13 证明 fixed-solution 时间模量并精确锁定当前 linear-payment 方法、two-cap Morrey 与 cubic tree 的阈值；不把 abstract boundary tests 写成 NSE counterexamples，也不声称 novelty 或 priority。</p><div class="boundary"><strong>R0.74S Step 13 公开边界</strong><p>PROVED：fixed-solution ell1(L_t^(4/3))、delta^(1/4) common-window modulus、general Holder algebra、explicit S.316 下的 exact ceiling、payment-dependent Morrey implication、heat-shear identities、conditional incidence theorem 与 cubic duality。ABSTRACT：smooth saturation、two-cap 与 eight-ary tree 不是 NSE counterexamples。FINITE：Python 31/31 exact、11/11 finite、22/22 structural、4/4 dependency、32/32 negative；Ruby 9/9 groups、72,027 cases、32/32 note checks。OPEN：uniform H-tail、S.342、bare S.328、PDE incidence / Dini gain、S.280、S.288、S.303、Q.12、Q.1 与正则性。 <strong>NOT CLAY.</strong> <a href="/notes/r0-74s.html">阅读完整中文笔记</a>。</p></div>\n'
    page = re.sub(r'<h3 id="r074s-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\n?', "", page)
    anchor = '        <section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_notes_index() -> None:
    target = PUBLIC / "notes/index.html"
    page = target.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.91"', 'data-site-version="1.92"', "index version"), ('/i18n-en.js?v=1.91', '/i18n-en.js?v=1.92', "index i18n"), ('/site-refresh.js?v=1.91', '/site-refresh.js?v=1.92', "index refresh"), ('研究笔记总索引 · v1.91 · 2026-09-03', '研究笔记总索引 · v1.92 · 2026-09-03', "index footer"),
    ):
        page = replace_once_or_present(page, old, new, label)
    entry = '''          <li class="note-entry" data-note="r0-74s"><article><div class="entry-copy"><p class="note-code">R0.74S · STEP 13</p><h3>时间可积性上限与组合 Morrey 阈值</h3></div><nav class="entry-files" aria-label="R0.74S files"><a class="file-link html" href="/notes/r0-74s.html" aria-label="Read R0.74S HTML">HTML</a><a class="file-link pdf" href="/notes/r0-74s.pdf" aria-label="Download R0.74S PDF">PDF</a></nav></article></li>\n'''
    anchor = '          <li class="note-entry" data-note="r0-74r">'
    page, existing = re.subn(r'\s*<li class="note-entry" data-note="r0-74s">[\s\S]*?</li>\n?', "\n" + entry, page, count=1)
    if existing == 0:
        if anchor not in page:
            raise RuntimeError("index R anchor missing")
        page = page.replace(anchor, entry + anchor, 1)
    write_text(target, page)


def route_post_r060_count(page: str) -> int:
    start = page.index('<section class="route-overview"')
    end = page.index('<div class="page-shell">', start)
    slugs = re.findall(r'href="/notes/(r0-[^"]+)\.html"', page[start:end])
    return len(slugs) - slugs.index("r0-61")


def update_accounting() -> None:
    html_count = sum(" 2.html" not in path.name for path in (PUBLIC / "notes").glob("r0-*.html"))
    pdf_count = sum(" 2.pdf" not in path.name for path in (PUBLIC / "notes").glob("r0-*.pdf")) + (0 if (PUBLIC / "notes/r0-74s.pdf").exists() else 1)
    post_r060 = route_post_r060_count(HOME.read_text(encoding="utf-8"))
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {"schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE, "latestPublishedResearchHtml": "/notes/r0-74s.html", "latestPublishedResearchPdf": "/notes/r0-74s.pdf", "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157, "latestRecapRelease": "R0.74O", "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03"})
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    for key in ("publishedReleases", "formalSealedReleases"):
        if RELEASE not in inventory[key]:
            inventory[key].append(RELEASE)
    inventory["latestPublishedRelease"] = RELEASE
    inventory["publishedReleaseCount"] = len(inventory["publishedReleases"])
    inventory["formalSealedReleaseCount"] = len(inventory["formalSealedReleases"])
    inventory["formalFigureExemptReleaseCount"] = len(inventory.get("formalFigureExemptReleases", []))
    write_json(inventory_target, inventory)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({"latestCompletedRelease": RELEASE, "siteVersion": VERSION, "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count, "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 157, "nextRelease": "r074t", "latestPublishedResearchHtml": "/notes/r0-74s.html", "latestPublishedResearchPdf": "/notes/r0-74s.pdf", "latestReleaseGate": "tests/r074s-ball-clock-gate.test.mjs", "latestReleasePublicationTest": "tests/r074s-release.test.mjs", "postR070APublishedReleaseCount": inventory["publishedReleaseCount"], "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"], "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"], "latestRecapRelease": "r074o", "latestRecapHtml": "/recap-r0-61-r0-74o.html", "latestRecapPdf": "/recap-r0-61-r0-74o.pdf", "latestReleaseTranslationScript": "scripts/add-r074s-translations.mjs", "latestReleasePdfBinder": "scripts/bind-r074s-pdf.mjs", "recapPolicy": "MILESTONE_ONLY"})
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_sources()
    assert_recap()
    write_text(PUBLIC / "notes/r0-74s.html", render_note())
    if "--note-only" not in sys.argv:
        copy_figures(); update_home(); update_literature(); update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    assert_recap()
    print(json.dumps({"status": "generated", "latestRelease": CODE, "siteVersion": VERSION, "recapPreserved": True, "formalFigure": FIGURE_ID, "simulation": False, "dgxUsed": False}, ensure_ascii=False))


if __name__ == "__main__":
    main()
