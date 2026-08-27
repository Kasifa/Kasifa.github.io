#!/usr/bin/env python3
"""Generate the deterministic R0.72I GitHub Pages release from site v1.21."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def replace_pattern(text: str, pattern: str, new: str, label: str) -> str:
    updated, count = re.subn(pattern, lambda _match: new, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return updated


def build_recap() -> None:
    source = PUBLIC / "recap-r0-61-r0-72h.html"
    target = PUBLIC / "recap-r0-61-r0-72i.html"
    html = source.read_text(encoding="utf-8")
    replacements = [
        ("R0.61–R0.72H｜R0.60 之后的研究回顾", "R0.61–R0.72I｜R0.60 之后的研究回顾"),
        ("R0.61 到 R0.72H 的 98 个研究节点", "R0.61 到 R0.72I 的 99 个研究节点"),
        ("二十四个阶段、98 个节点", "二十五个阶段、99 个节点"),
        ("最新一节在有限多载波系统中封闭 mixed row，并证明 action-only 版本失效。", "最新一节分离了失败的正项吸收与真实完整根账本，并在全奇载波族上证明后者统一衰减。"),
        ("finite multi-carrier mixed-row 行级封闭", "physical absorption no-go 与 odd-carrier repair"),
        ("/i18n-en.js?v=1.21", "/i18n-en.js?v=1.22"),
        ("累计回顾 · R0.61–R0.72H", "累计回顾 · R0.61–R0.72I"),
        ("<strong>R0.61–R0.72H</strong>", "<strong>R0.61–R0.72I</strong>"),
        ("收录节点：98", "收录节点：99"),
        ("回顾截止时公开笔记：158", "回顾截止时公开笔记：159"),
        ("回顾截止节点：R0.72H", "回顾截止节点：R0.72I"),
        ("01 · 二十四个研究阶段", "01 · 二十五个研究阶段"),
        ("02 · 98 节完整索引", "02 · 99 节完整索引"),
        ("<strong>98</strong><span>R0.61–R0.72H 研究节点</span>", "<strong>99</strong><span>R0.61–R0.72I 研究节点</span>"),
        ("<strong>60</strong><span>R0.70A–R0.72H 已公开版本</span>", "<strong>61</strong><span>R0.70A–R0.72I 已公开版本</span>"),
        ("<strong>36</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>37</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("<strong>24</strong><span>按问题划分的研究阶段</span>", "<strong>25</strong><span>按问题划分的研究阶段</span>"),
        ("后面的 98 个节点", "后面的 99 个节点"),
        ("R0.70A–R0.72H 的 60 个版本已经公开；其中 36 个", "R0.70A–R0.72I 的 61 个版本已经公开；其中 37 个"),
        ("R0.60 之后的路线分成二十四个阶段", "R0.60 之后的路线分成二十五个阶段"),
        ("R0.61–R0.72H 的 98 节公开笔记", "R0.61–R0.72I 的 99 节公开笔记"),
    ]
    for old, new in replacements:
        if old not in html:
            raise RuntimeError(f"recap missing: {old}")
        html = html.replace(old, new)

    phase_h_end = '<div class="links"><a href="/notes/r0-72h.html">R0.72H</a><a href="/figures/r0-72h-mixed-row-payment.pdf">R0.72H 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072h">R0.72H 证书</a></div></article>'
    phase_i = r'''
            <article class="phase"><h3>R0.72I · 物理吸收失败与全奇载波修复</h3>
              <p>我把 R0.72H 的四个正项逐一换回物理量。取全奇 Rudin–Shapiro 载波与 \(\delta=M\) 时，前三项都能支付；分离的 \(B_AQ_*\) 项却比 \(D^{1/3}\Lambda_{1,*}\) 多出 \(M^{1/2}\log M\)。因此固定 corollary 不能靠逐项吸收闭合。</p>
              <p>这个发散来自上界，不是真实根账本的下界。保留 joint heat exposure，或直接利用 \(V\) 翻转奇偶格点，可得 \(G_{\rm all}^{\rm ex}\asymp M^2\)。完整物理比值在整个 \(0&lt;g\le\gamma_0M^{3/2}\) 窗口内至多为 \(CM^{-4/9}(\log M)^{-2/3}\)，所以同一族不是 critical-log 候选的反例。</p>
              <div class="links"><a href="/notes/r0-72i.html">R0.72I</a><a href="/figures/r0-72i-physical-absorption.pdf">R0.72I 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072i">R0.72I 证书</a></div></article>'''
    html = replace_once(html, phase_h_end, phase_h_end + phase_i, "recap I phase")

    node_h = '            <span class="node-ref"><a href="/notes/r0-72h.html">R0.72H</a><span class="node-state kind-closed">闭</span></span>\n'
    node_i = '            <span class="node-ref"><a href="/notes/r0-72i.html">R0.72I</a><span class="node-state kind-closed">闭</span></span>\n'
    html = replace_once(html, node_h, node_h + node_i, "recap I node")

    retained = r"""            <li>R0.72I 的 physical-absorption audit：在 \(\delta=M\) 的全奇 Rudin–Shapiro 族上，R0.72H 的分离 \(B_AQ_*\) 正项归一化后按 \(M^{1/2}\log M\) 发散，所以 fixed termwise absorption 路线失效。joint exposure 与 odd-carrier parity 两条解析路线却给出真实 \(G_{\rm all}^{\rm ex}\asymp M^2\)，完整物理归一化比在整个 perturbative coupling window 内统一趋零。这是否定证明路线，不是否定候选不等式。</li>
"""
    html = replace_once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "recap retained I")

    value = r"""        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>一个正项分解被排除，但真实多载波账本没有随它发散</h2>
          <p>截至 R0.72I，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 99 个节点或 61 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>R0.72H 的 mixed-row theorem 本身保留。R0.72I 排除的是把 complete-root corollary 的四个正项逐项塞进 \(D^{1/3}\Lambda_{1,*}\) 的做法；其中 \(B_AQ_*\) 丢失了载波共同存在的短时间。</p>
          <p>同一全奇族的真实 complete ledger 已由 joint exposure 和 parity 两条路线封闭，并在完整 critical-log normalization 下统一衰减。当前障碍因此转到 mixed-parity carrier graph 的真实 cubic row，不是继续放大这个已经证伪的上界项。</p>
        </section>"""
    html = replace_pattern(html, r'        <section id="value">.*?</section>', value, "recap value")

    next_section = r"""        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72J 检查 mixed-parity 的真实 cubic interaction</h2>
          <p>下一步不再尝试吸收分离的 \(B_AQ_*\)。我会按载波的模二 residue graph 分解 \(V^2\) 返回目标行的路径，并直接估计 \(|\delta|\int|hP_0V^2F|\)。</p>
          <p>有限关口是：证明 action 与 joint exposure 的 hybrid payment，或构造 mixed-parity family 使真实 cubic row 在完整物理归一化后仍不消失。只有真实量可以决定候选，不再用发散的正上界代替它。</p>
        </section>"""
    html = replace_pattern(html, r'        <section id="next">.*?</section>', next_section, "recap next")

    claims = r"""        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2>
          <p>R0.70A–R0.72I 的 61 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，37 节完整封存；24 节较早版本仍缺 formal 状态或正式附图包，列入可审计的旧档回补清单。公开页存在不等于档案合同完整。</p>
          <p>R0.72I 的结论限于 exact finite triangular 2.5D class 和声明的 all-odd perturbative window。它没有证明 arbitrary-carrier physical inequality，也没有证明一般三维 Navier–Stokes 的全局光滑性或有限时破裂；Clay 正式问题仍然开放。</p>
        </section>"""
    html = replace_pattern(html, r'        <section id="claims">.*?</section>', claims, "recap claims")

    reproduce = r"""        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72h.html">保留 R0.72H 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72i.html">打开最新节点 R0.72I</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072i">查看 R0.72I 双路证书</a> · <a href="/figures/r0-72i-physical-absorption.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72i.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72h.pdf">上一版累计回顾 PDF</a></p>
          <p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>
        </section>"""
    html = replace_pattern(html, r'        <section id="reproduce">.*?</section>', reproduce, "recap reproduce")
    html = replace_once(html, "R0.61–R0.72H 回顾 · 2026-08-27", "R0.61–R0.72I 回顾 · 2026-08-27", "recap footer")
    target.write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    if 'data-site-version="1.22"' in html:
        # The first interrupted generation used ordinary Python strings for
        # TeX. Repair only the three resulting escape signatures, then keep
        # subsequent runs byte-stable.
        raw = path.read_bytes()
        repaired = raw.replace(b"\r" + b"ho", b"\\rho")
        repaired = repaired.replace(b"\r" + b"m", b"\\rm")
        repaired = repaired.replace(b"\x07" + b"symp", b"\\asymp")
        repaired = repaired.replace(b"\t" + b"o0", b"\\to0")
        if repaired != raw:
            path.write_bytes(repaired)
        return
    replacements = [
        ('data-site-version="1.21"', 'data-site-version="1.22"'),
        ("/i18n-en.js?v=1.21", "/i18n-en.js?v=1.22"),
        ("/site-refresh.js?v=1.21", "/site-refresh.js?v=1.22"),
        ("/recap-r0-61-r0-72h", "/recap-r0-61-r0-72i"),
        ("<strong>v1.21</strong>网页版本", "<strong>v1.22</strong>网页版本"),
        ("<strong>158</strong>公开研究笔记", "<strong>159</strong>公开研究笔记"),
        ("<strong>R0.72H</strong>最新研究节点", "<strong>R0.72I</strong>最新研究节点"),
        ("<strong>physical absorption of mixed-row data factors</strong>当前方向", "<strong>mixed-parity cubic interaction</strong>当前方向"),
        ("Research topology · R0.1–R0.72H", "Research topology · R0.1–R0.72I"),
        ("R0.70A–R0.72H：60 节已公开，36 节完整封存", "R0.70A–R0.72I：61 节已公开，37 节完整封存"),
        ("R0.69P–R0.72H", "R0.69P–R0.72I"),
        ("展开 68 篇公开笔记", "展开 69 篇公开笔记"),
        ("综述 v1.21 · 2026-08-27", "综述 v1.22 · 2026-08-27"),
        ("上次综述 v1.20 · 2026-08-27", "上次综述 v1.21 · 2026-08-27"),
    ]
    for old, new in replacements:
        if old not in html:
            raise RuntimeError(f"home missing: {old}")
        html = html.replace(old, new)

    html = replace_once(
        html,
        "R0.72H 已在有限共轭配对多载波系统中封闭 mixed row 的载波数无关支付，并证明 action-only 版本失效；下一步只审显式数据因子的物理归一化吸收。",
        "R0.72I 已证明分离的 B_AQ_* 正项不能逐项物理吸收，但同一全奇载波族的真实 complete ledger 在 critical-log normalization 下统一衰减；下一步只审 mixed-parity 的真实 cubic row。",
        "home summary",
    )
    html = replace_once(
        html,
        "从候选 payment 失效走到多载波 mixed-row 行级封闭",
        "从多载波 mixed-row 行级封闭走到物理吸收 no-go 与 parity repair",
        "home route title",
    )
    route_tail = "R0.72H 转入有限共轭配对多载波 mixed row，证明载波数无关的 moment-resolved 上界；全奇数 Rudin–Shapiro 族排除 action-only payment，并使所需 \\(M\\)-幂次达到同阶。</p>"
    route_new = "R0.72H 转入有限共轭配对多载波 mixed row，证明载波数无关的 moment-resolved 上界；全奇数 Rudin–Shapiro 族排除 action-only payment，并使所需 \\(M\\)-幂次达到同阶。R0.72I 逐项换回物理量，证明分离的 \\(B_AQ_*\\) 项不能统一吸收；joint exposure 与 odd-carrier parity 又证明真实 complete ledger 统一衰减。</p>"
    html = replace_once(html, route_tail, route_new, "home I route prose")
    html = replace_once(
        html,
        "complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go</p>",
        "complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go → termwise physical-absorption no-go → parity repair</p>",
        "home route path",
    )
    nav_h = '                  <a class="milestone" href="/notes/r0-72h.html">R0.72H</a>\n'
    nav_i = '                  <a class="milestone" href="/notes/r0-72i.html">R0.72I</a>\n'
    html = replace_once(html, nav_h, nav_h + nav_i, "home I nav")

    next_block = r"""            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72J</span><span class="tree-state current">下一检查点</span></div>
              <h3>mixed-parity cubic interaction</h3>
              <p>按 carrier residue graph 检查 \(P_0V^2F\) 返回目标行的真实路径，寻找 action 与 joint exposure 的 hybrid payment；若失败，就要求 mixed-parity 反族使真实 cubic row 而非其分离正上界存活。</p>
            </article>"""
    html = replace_pattern(html, r'            <article class="tree-node next">.*?</article>', next_block, "home next")

    recap_card = r"""          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72I · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 99 个节点；全站现有 159 篇公开研究笔记</h3>
            <p>累计回顾现在分为二十五个问题阶段，完整覆盖 R0.61–R0.72I。R0.72E 排除 unweighted payment，R0.72F 选出 critical-log 修正，R0.72G 封闭 one-carrier complete roots，R0.72H 封闭 finite multi-carrier mixed row，R0.72I 再分离失败的正项吸收与真实 parity-resolved ledger。R0.70A–R0.72I 共 61 个版本已公开；37 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;我排除了一个具体证明路线，但没有排除 physical critical-log candidate。下一障碍是 mixed-parity 的真实 cubic interaction。</p>
            <p><a href="/recap-r0-61-r0-72i.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72i.pdf">下载同步 PDF</a></p>
          </div>"""
    html = replace_pattern(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap_card, "home recap")

    old_tail = r"""            <p><strong style="color:var(--gold)">下一步 R0.72I：</strong>&nbsp;检查显式数据因子能否被完整 physical critical-log normalization 统一吸收，或构造 normalized growing-carrier 反族。</p>
          </div>
        </section>"""
    new_tail = r"""            <p><strong style="color:var(--gold)">R0.72I 已完成：</strong>&nbsp;分离的 \(B_AQ_*\) 正项不能逐项物理吸收；同一全奇族的真实 complete ledger 由 joint exposure 与 parity 修复并统一衰减。</p>
          </div>

          <div class="task-one" id="r072i" data-release="r072i" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72I · 2026-08-27</p>
            <h3>发散的是分离上界，不是真实完整根账本</h3>
            <p>取全奇 Rudin–Shapiro 载波和 \(\delta=M\)。R0.72H 的四个正项换回物理量后，前三项的归一化比都趋零；\(B_AQ_*\) 项却按 \(M^{1/2}\log M\) 发散。这严格排除了 fixed termwise absorption。</p>
            <p>保留 joint heat exposure，或直接利用 \(V\) 翻转奇偶格点，可得 \(G_{\rm all}^{\rm ex}\asymp M^2\)。完整物理比值在 \(0&lt;g\le\gamma_0M^{3/2}\) 内满足 \(CM^{-4/9}(\log M)^{-2/3}\to0\)。因此这个族不是候选 physical inequality 的反例。</p>
            <p><strong>结论边界：</strong>&nbsp;结论限于 exact triangular 2.5D all-odd class。arbitrary mixed-parity cubic row 与一般三维正则性仍然开放。</p>
            <p><a href="/notes/r0-72i.html"><strong>阅读 R0.72I 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72i.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-72i-physical-absorption.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072i">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072i_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072i_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072i_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072i_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072i-physical-absorption/fig-r072i-physical-absorption">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72i.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72i.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72J：</strong>&nbsp;检查 mixed-parity carrier graph 的真实 cubic interaction，寻找 hybrid payment 或 actual normalized counterfamily。</p>
          </div>
        </section>"""
    html = replace_once(html, old_tail, new_tail, "home I card")
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    if "/i18n-en.js?v=1.22" in html:
        return
    html = html.replace("/recap-r0-61-r0-72h", "/recap-r0-61-r0-72i")
    html = html.replace("/i18n-en.js?v=1.21", "/i18n-en.js?v=1.22")
    html = html.replace("文献综述 v1.21 · 2026-08-27", "文献综述 v1.22 · 2026-08-27")
    html = html.replace("本站 R0.69P–R0.72H 只列为研究笔记", "本站 R0.69P–R0.72I 只列为研究笔记")
    html = html.replace("累计回顾与 98 节索引", "累计回顾与 99 节索引")
    html = html.replace("打开 98 节完整索引", "打开 99 节完整索引")
    route_tail = "R0.72H 在有限共轭配对多载波系统中证明 mixed row 的载波数无关 moment-resolved payment；全奇数 Rudin–Shapiro 族排除 action-only 版本，并使该 moment 所编码的载波幂次达到同阶。一般 Navier–Stokes 正则性仍开放。</p>"
    route_new = "R0.72H 在有限共轭配对多载波系统中证明 mixed row 的载波数无关 moment-resolved payment；全奇数 Rudin–Shapiro 族排除 action-only 版本，并使该 moment 所编码的载波幂次达到同阶。R0.72I 证明分离的 \\(B_AQ_*\\) 正项不能逐项物理吸收，同时用 joint exposure 和 odd-carrier parity 证明真实 complete ledger 统一衰减。一般 Navier–Stokes 正则性仍开放。</p>"
    html = replace_once(html, route_tail, route_new, "literature I route")

    open_i = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72I</b><strong>physical absorption of row-level data factors</strong></header><p>检查 \(E_A,m_*,B_A,\rho_A\) 是否被完整 physical critical-log normalization 统一支付，或构造 normalized growing-carrier 反族。</p></div>'''
    closed_i = r'''              <div class="route-step closed"><header><b>R0.72I</b><strong>termwise physical-absorption no-go 与 odd-carrier repair</strong></header><p>全奇 \(\delta=M\) 族使分离 \(B_AQ_*\) 正项的 normalized ratio 按 \(M^{1/2}\log M\) 发散；joint exposure 与 parity refinement 却给真实 \(G_{\rm all}^{\rm ex}\asymp M^2\) 和统一衰减的 physical ratio。<a href="/notes/r0-72i.html">研究笔记</a> <a href="/recap-r0-61-r0-72i.html">当前累计回顾</a> <a href="#r072i-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72J</b><strong>mixed-parity cubic interaction</strong></header><p>直接检查 \(|\delta|\int|hP_0V^2F|\) 的 carrier graph、hybrid payment 与 actual normalized counterfamily。</p></div>'''
    html = replace_once(html, open_i, closed_i, "literature I cards")

    boundary_h = r'''          <div class="boundary"><strong>R0.72H 的主源边界</strong><p>本节没有调用一般 non-autonomous bilinear embedding，而是直接使用 scalar target coordinate、共同热因子、对角耗散和 reciprocal-weight moment。限定一手来源检索没有找到直接给出该 carrier-count-independent mixed-row estimate 的定理；这是截至 2026-08-27 的 bounded non-collision check，不是原创性、优先权或穷尽性声明。</p></div>'''
    boundary_i = r'''

          <h3 id="r072i-boundary">R0.72I 的 physical absorption 与 parity 边界</h3>
          <p><a href="https://math.berkeley.edu/~tataru/papers/nas.pdf">Koch–Tataru</a> 与 <a href="https://www.numdam.org/articles/10.24033/bsmf.2638/">Chemin–Planchon</a>处理临界 Carleson/Besov 空间，不把本站 solution-dependent Lamb action 直接变成 \(B_A\) payment。<a href="https://arxiv.org/abs/1102.3268">Haak–Ouhabaz</a> 的固定 observation admissibility 也不能消去时变 shear-row norm。</p>
          <p><a href="https://arxiv.org/abs/1505.00142">Lei–Lin–Zhou</a>与<a href="https://arxiv.org/abs/1303.1215">Biferale–Titi</a>的 helicity coercivity 需要 sign/sector 条件；arithmetic odd/even carrier parity 不是 helical sign。<a href="https://doi.org/10.1016/j.jfa.2020.108563">Dong–Zhang</a>的 time analyticity 不能支付 complete zero-slope sum。<a href="https://annals.math.princeton.edu/2017/185-2/p04">Bedrossian–Germain–Masmoudi</a>的 Couette threshold 与本节 arbitrary finite-carrier root sampling 量词不同。</p>
          <div class="boundary"><strong>R0.72I 的主源边界</strong><p>限定一手来源检索未发现同时给出 carrier-uniform \(B_A\) absorption、endogenous complete-root sampling 和 all-odd parity repair 的定理。本节只证明 exact triangular 2.5D class 内的 method obstruction 与 special-family repair；这是 bounded non-collision check，不是原创性、优先权或穷尽性声明。</p></div>'''
    html = replace_once(html, boundary_h, boundary_h + boundary_i, "literature I boundary")
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    note_count = len(list((PUBLIC / "notes").glob("*.html")))
    if note_count != 159:
        raise RuntimeError(f"expected 159 public HTML notes, found {note_count}")

    release_path = ROOT / "research" / "release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release.update({
        "latestCompletedRelease": "r072i",
        "siteVersion": "1.22",
        "publicHtmlNoteCount": note_count,
        "postR060RecapNodeCount": 99,
        "nextRelease": "r072j",
        "latestReleaseGate": "tests/r072i-physical-absorption-gate.test.mjs",
        "postR070APublishedReleaseCount": 61,
        "postR070AFormalSealedReleaseCount": 37,
        "legacyFormalFigureBacklogCount": 24,
    })
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    site.update({"version": "1.22", "latestRelease": "R0.72I", "publicHtmlNoteCount": note_count})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research" / "formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory.update({
        "latestPublishedRelease": "r072i",
        "publishedReleaseCount": 61,
        "formalSealedReleaseCount": 37,
        "legacyFormalFigureBacklogCount": 24,
    })
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r072i" not in inventory[key]:
            inventory[key].append("r072i")
    if len(inventory["legacyFormalFigureBacklog"]) != 24:
        raise RuntimeError("legacy formal-figure backlog changed unexpectedly")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    print(json.dumps({"release": "R0.72I", "siteVersion": "1.22", "notes": 159, "recapNodes": 99, "published": 61, "formalSealed": 37, "legacyBacklog": 24}, ensure_ascii=False))


if __name__ == "__main__":
    main()
