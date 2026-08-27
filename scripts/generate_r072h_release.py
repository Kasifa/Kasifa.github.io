#!/usr/bin/env python3
"""Generate the deterministic R0.72H web release from site v1.20."""

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
    source = PUBLIC / "recap-r0-61-r0-72g.html"
    target = PUBLIC / "recap-r0-61-r0-72h.html"
    html = source.read_text(encoding="utf-8")

    pairs = [
        ("R0.61–R0.72G｜R0.60 之后的研究回顾", "R0.61–R0.72H｜R0.60 之后的研究回顾"),
        ("R0.61 到 R0.72G 的 97 个研究节点", "R0.61 到 R0.72H 的 98 个研究节点"),
        ("二十三个阶段、97 个节点", "二十四个阶段、98 个节点"),
        ("最新一节在精确实单载波族上封闭完整根打包并证明 critical-log 尖锐饱和。", "最新一节在有限多载波系统中封闭 mixed row，并证明 action-only 版本失效。"),
        ("再到 critical-log complete-root 尖锐封闭。", "再到 finite multi-carrier mixed-row 行级封闭。"),
        ("/i18n-en.js?v=1.20", "/i18n-en.js?v=1.21"),
        ("累计回顾 · R0.61–R0.72G", "累计回顾 · R0.61–R0.72H"),
        ("<strong>R0.61–R0.72G</strong>", "<strong>R0.61–R0.72H</strong>"),
        ("收录节点：97", "收录节点：98"),
        ("回顾截止时公开笔记：157", "回顾截止时公开笔记：158"),
        ("回顾截止节点：R0.72G", "回顾截止节点：R0.72H"),
        ("01 · 二十三个研究阶段", "01 · 二十四个研究阶段"),
        ("02 · 97 节完整索引", "02 · 98 节完整索引"),
        ("<strong>97</strong><span>R0.61–R0.72G 研究节点</span>", "<strong>98</strong><span>R0.61–R0.72H 研究节点</span>"),
        ("<strong>59</strong><span>R0.70A–R0.72G 已公开版本</span>", "<strong>60</strong><span>R0.70A–R0.72H 已公开版本</span>"),
        ("<strong>35</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>36</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("<strong>23</strong><span>按问题划分的研究阶段</span>", "<strong>24</strong><span>按问题划分的研究阶段</span>"),
        ("后面的 97 个节点", "后面的 98 个节点"),
        ("R0.70A–R0.72G 的 59 个版本已经公开；其中 35 个", "R0.70A–R0.72H 的 60 个版本已经公开；其中 36 个"),
        ("R0.60 之后的路线分成二十三个阶段", "R0.60 之后的路线分成二十四个阶段"),
        ("R0.61–R0.72G 的 97 节公开笔记", "R0.61–R0.72H 的 98 节公开笔记"),
    ]
    for old, new in pairs:
        if old not in html:
            raise RuntimeError(f"recap missing {old[:30]}")
        html = html.replace(old, new)

    old_phase = """            <article class="phase"><h3>R0.72F–R0.72G · 临界对数候选与完整根封闭</h3>
              <p>R0.72F 对 \\(w_{\\beta,\\gamma}(s)=s^{-\\beta}[1+\\log(1/s)]^\\gamma\\) 分别计算 Leray payment 与 selected Bessel obstruction：能量支付要求 \\(\\beta&lt;1/2\\)，exact family 强制 \\(\\beta&gt;1/3\\)，或在端点取 \\(\\gamma\\ge1\\)。最小共同边界是 \\(w_*(s)=s^{-1/3}[1+\\log(1/s)]\\)。</p>
              <p>R0.72G 固定这个候选，不再预选根。在精确实单载波格点上，phase gauge、目标行恒等式与 Rolle–BV 归约给出不依赖根数和根间距的 \\(G_{\\rm all}\\lesssim\\log\\delta\\)；selected Bessel roots 给匹配下界。原始幅度序列上，完整物理 root ledger 与 \\(D^{1/3}\\Lambda_{1,*}\\) 同阶。下一障碍转到有限实多载波的 mixed row；一般三维传递仍开放。</p>
              <div class="links"><a href="/notes/r0-72f.html">R0.72F</a><a href="/notes/r0-72g.html">R0.72G</a><a href="/figures/r0-72g-complete-root-packing.pdf">R0.72G 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072g">R0.72G 证书</a></div></article>"""
    new_phase = old_phase + """
            <article class="phase"><h3>R0.72H · 有限多载波 mixed row 与尖锐矩</h3>
              <p>在有限共轭配对多载波三角形格点上，目标行坐标、对角耗散与 critical-log reciprocal envelope 给出
              \\(\\mathcal E_Q\\le6\\sqrt\\nu d|K_z|[\\lambda_0E_Am_*Q_*]^{1/2}\\)。常数不依赖载波数、位置或物理相位。</p>
              <p>全奇数 Rudin–Shapiro 族给 \\(\\mathcal E_Q\\asymp a^2M^2\\)、\\(Q_*\\asymp a^2M^{2/3}\\log M\\)、\\(m_*\\asymp a^2M^{7/3}/\\log M\\)：action-only payment 失效，而 moment-resolved 的 \\(M\\)-幂次被达到。兼容实目标的完整根 corollary 还需 \\(\\delta\\ne0\\)。下一关是把 \\(E_A,m_*,B_A,\\rho_A\\) 吸收到物理 \\(D^{1/3}\\Lambda_{1,*}\\)，不是继续增加载波计数。</p>
              <div class="links"><a href="/notes/r0-72h.html">R0.72H</a><a href="/figures/r0-72h-mixed-row-payment.pdf">R0.72H 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072h">R0.72H 证书</a></div></article>"""
    html = replace_once(html, old_phase, new_phase, "recap H phase")

    node_g = '            <span class="node-ref"><a href="/notes/r0-72g.html">R0.72G</a><span class="node-state kind-closed">闭</span></span>\n'
    node_h = '            <span class="node-ref"><a href="/notes/r0-72h.html">R0.72H</a><span class="node-state kind-closed">闭</span></span>\n'
    html = replace_once(html, node_g, node_g + node_h, "recap H node")

    retained = """            <li>R0.72H 的 finite-carrier mixed-row theorem：对有限共轭配对载波，\\(\\mathcal E_Q\\) 由 critical-log action、restart energy 与 reciprocal-weight shear moment 以载波数无关常数支付。全奇数 Rudin–Shapiro 族排除统一 action-only payment，并使 moment-resolved 的 \\(M\\)-幂次达到同阶。兼容实目标的 complete-root corollary 需 \\(\\delta\\ne0\\)；最终物理归一化吸收仍开放。</li>
"""
    html = replace_once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "recap retained H")

    value = """        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>多载波行级维数损失已排除，主障碍转到物理吸收</h2>
          <p>截至 R0.72H，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 98 个节点或 60 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>R0.72E 排除 unweighted candidate；R0.72F 选出 critical-log 最小修正；R0.72G 在 exact one-carrier ray 上封闭 complete roots。R0.72H 又证明 finite multi-carrier mixed row 不需要支付载波数损失，同时用全奇数 Rudin–Shapiro 族排除 action-only 版本。</p>
          <p>当前可以保留的是一个 row-level analytic theorem 和匹配的尺度反族。尚未完成的是把 \\(E_A,m_*,B_A,\\rho_A\\) 统一吸收到物理 \\(D^{1/3}\\Lambda_{1,*}\\)；这才决定该路线能否离开精确三角形模型。</p>
        </section>"""
    html = replace_pattern(html, r'        <section id="value">.*?</section>', value, "recap value")

    next_section = """        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72I 检查显式数据因子的物理吸收</h2>
          <p>下一步固定 R0.72H 的 mixed-row theorem，逐项比较 \\(E_A,m_*,B_A,\\rho_A\\) 与 physical energy、full-frequency rotational charge、critical-log action 和 restart geometry。</p>
          <p>有限关口是：证明这些量被统一的 \\(D^{1/3}\\Lambda_{1,*}\\) 支付，或构造满足完整物理归一化的 growing-carrier 反族。两者都不能完成时，就记录精确缺失的数据接口。</p>
        </section>"""
    html = replace_pattern(html, r'        <section id="next">.*?</section>', next_section, "recap next")

    claims = """        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2>
          <p>R0.70A–R0.72H 的 60 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，36 节完整封存；24 节较早版本仍缺 formal 状态或正式附图包，列入可审计的旧档回补清单。公开页存在不等于档案合同完整。</p>
          <p>R0.72H 的主定理限于有限载波三角形 2.5D row problem；compatible-real complete-root corollary 还要求 \\(\\delta\\ne0\\)。本回顾没有证明三维 Navier–Stokes 的全局光滑性或有限时破裂；Clay 正式问题仍然开放。</p>
        </section>"""
    html = replace_pattern(html, r'        <section id="claims">.*?</section>', claims, "recap claims")

    reproduce = """        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72g.html">保留 R0.72G 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72h.html">打开最新节点 R0.72H</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates">浏览机器可读证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072h">查看 R0.72H 双路证书</a> · <a href="/recap-r0-61-r0-72h.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72g.pdf">上一版累计回顾 PDF</a></p>
          <p>各已生成的 HTML、PDF、首页路线入口和首页进展入口按版本保留。正式附图同时保留源数据、绘图程序、环境、独立验证和校验和。</p>
        </section>"""
    html = replace_pattern(html, r'        <section id="reproduce">.*?</section>', reproduce, "recap reproduce")
    html = replace_once(html, "R0.61–R0.72G 回顾 · 2026-08-27", "R0.61–R0.72H 回顾 · 2026-08-27", "recap footer")
    target.write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    if 'data-site-version="1.21"' in html:
        return
    for old, new in [
        ('data-site-version="1.20"', 'data-site-version="1.21"'),
        ("/i18n-en.js?v=1.20", "/i18n-en.js?v=1.21"),
        ("/site-refresh.js?v=1.20", "/site-refresh.js?v=1.21"),
        ("/recap-r0-61-r0-72g", "/recap-r0-61-r0-72h"),
        ("<strong>v1.20</strong>网页版本", "<strong>v1.21</strong>网页版本"),
        ("<strong>157</strong>公开研究笔记", "<strong>158</strong>公开研究笔记"),
        ("<strong>R0.72G</strong>最新研究节点", "<strong>R0.72H</strong>最新研究节点"),
        ("<strong>finite real multi-carrier mixed-row payment</strong>当前方向", "<strong>physical absorption of mixed-row data factors</strong>当前方向"),
        ("Research topology · R0.1–R0.72G", "Research topology · R0.1–R0.72H"),
        ("R0.70A–R0.72G：59 节已公开，35 节完整封存", "R0.70A–R0.72H：60 节已公开，36 节完整封存"),
        ("R0.69P–R0.72G", "R0.69P–R0.72H"),
        ("展开 67 篇公开笔记", "展开 68 篇公开笔记"),
        ("综述 v1.20 · 2026-08-27", "综述 v1.21 · 2026-08-27"),
        ("上次综述 v1.19 · 2026-08-27", "上次综述 v1.20 · 2026-08-27"),
    ]:
        if old not in html:
            raise RuntimeError(f"home missing {old}")
        html = html.replace(old, new)

    html = replace_once(
        html,
        "R0.72G 已在精确实单载波族上封闭 complete-root trace packing，并证明 critical-log payment 尖锐；下一步只审有限实多载波的新 mixed row。",
        "R0.72H 已在有限共轭配对多载波系统中封闭 mixed row 的载波数无关支付，并证明 action-only 版本失效；下一步只审显式数据因子的物理归一化吸收。",
        "home summary",
    )
    html = replace_once(
        html,
        "从候选 payment 失效走到 critical-log complete-root 尖锐封闭",
        "从候选 payment 失效走到多载波 mixed-row 行级封闭",
        "home route title",
    )
    g_sentence = "R0.72G 固定这一候选，用实相位 gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量 \\(G_{\\rm all}\\asymp\\log\\delta\\)，并在原始幅度序列上得到 complete-root sharp saturation。</p>"
    h_sentence = "R0.72G 固定这一候选，用实相位 gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量 \\(G_{\\rm all}\\asymp\\log\\delta\\)，并在原始幅度序列上得到 complete-root sharp saturation。R0.72H 转入有限共轭配对多载波 mixed row，证明载波数无关的 moment-resolved 上界；全奇数 Rudin–Shapiro 族排除 action-only payment，并使所需 \\(M\\)-幂次达到同阶。</p>"
    html = replace_once(html, g_sentence, h_sentence, "home H route prose")
    html = replace_once(
        html,
        "complete-root Rolle–BV closure → sharp critical-log saturation</p>",
        "complete-root Rolle–BV closure → sharp critical-log saturation → carrier-free mixed-row payment → action-only no-go</p>",
        "home route path",
    )
    nav_g = '                  <a class="milestone" href="/notes/r0-72g.html">R0.72G</a>\n'
    nav_h = '                  <a class="milestone" href="/notes/r0-72h.html">R0.72H</a>\n'
    html = replace_once(html, nav_g, nav_g + nav_h, "home H nav")

    next_block = """            <article class="tree-node next">
              <div class="tree-node-head">
                <span class="route-range">NEXT · R0.72I</span>
                <span class="tree-state current">下一检查点</span>
              </div>
              <h3>physical absorption of the mixed-row data factors</h3>
              <p>固定 R0.72H 的载波数无关 row theorem，检查 \\(E_A,m_*,B_A,\\rho_A\\) 是否被 full physical energy、rotational charge、critical-log action 与 restart geometry 统一支付；否则构造完整归一化反族。</p>
            </article>"""
    html = replace_pattern(html, r'            <article class="tree-node next">.*?</article>', next_block, "home next")

    recap_card = """          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72H · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 98 个节点；全站现有 158 篇公开研究笔记</h3>
            <p>累计回顾现在分为二十四个问题阶段，完整覆盖 R0.61–R0.72H。R0.72E 排除 unweighted payment，R0.72F 选出 critical-log 修正，R0.72G 封闭 exact one-carrier complete roots，R0.72H 再封闭 finite multi-carrier mixed row，并排除 action-only 版本。R0.70A–R0.72H 共 60 个版本已公开；36 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;目前没有新的无条件继续性判据，也没有构造有限时奇性。下一障碍是显式 row-level 数据因子的物理归一化吸收。</p>
            <p><a href="/recap-r0-61-r0-72h.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72h.pdf">下载同步 PDF</a></p>
          </div>"""
    html = replace_pattern(
        html,
        r'          <div class="task-one" id="post-r060-recap".*?</div>',
        recap_card,
        "home recap card",
    )

    old_tail = """            <p><strong style="color:var(--gold)">下一步 R0.72H：</strong>&nbsp;处理有限实多载波的新 mixed row \\(\\mathcal E_Q=\\int|hQF|\\)，要求 dimension-free payment 或显式 growing-carrier 反族。</p>
          </div>
        </section>"""
    new_tail = """            <p><strong style="color:var(--gold)">R0.72H 已完成：</strong>&nbsp;finite conjugate-paired multi-carrier mixed row 具有载波数无关的 moment-resolved payment；action-only 版本被全奇数 Rudin–Shapiro 族排除。</p>
          </div>

          <div class="task-one" id="r072h" data-release="r072h" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72H · 2026-08-27</p>
            <h3>有限多载波 mixed row 没有维数损失，但 action 本身不够</h3>
            <p>对 \\(I=[A,A+X]\\)，定义 critical-log action \\(Q_*^I\\) 与 reciprocal-weight moment \\(m_*(A,X)\\)。目标行、对角耗散和同一热因子给</p>
            <p>\\[
              \\mathcal E_Q(I)\\le6\\sqrt\\nu d|K_z|[\\lambda_0E_A m_*(A,X)Q_*^I]^{1/2},
            \\]</p>
            <p>常数不依赖载波数、位置和物理相位。全奇数 Rudin–Shapiro 族满足 \\(\\mathcal E_Q\\asymp a^2M^2\\)、\\(Q_*\\asymp a^2M^{2/3}\\log M\\)、\\(m_*\\asymp a^2M^{7/3}/\\log M\\)，所以 action-only payment 发散，而 moment-resolved 的 \\(M\\)-幂次达到同阶。</p>
            <p><strong>结论边界：</strong>&nbsp;完整根 corollary 只在兼容实目标 gauge 且 \\(\\delta\\ne0\\) 时成立；物理 \\(D^{1/3}\\Lambda_{1,*}\\) 对 \\(E_A,m_*,B_A,\\rho_A\\) 的统一吸收仍未证明。本节不是一般三维 continuation theorem。</p>
            <p><a href="/notes/r0-72h.html"><strong>阅读 R0.72H 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72h.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/figures/r0-72h-mixed-row-payment.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072h">查看双路证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072h_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072h_literature_audit.md">查看文献审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072h_gap_matrix.md">查看主张—证据矩阵</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072h_independent_audit.md">查看独立逐式审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072h-mixed-row-payment/fig-r072h-mixed-row-payment">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72h.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72h.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72I：</strong>&nbsp;检查显式数据因子能否被完整 physical critical-log normalization 统一吸收，或构造 normalized growing-carrier 反族。</p>
          </div>
        </section>"""
    html = replace_once(html, old_tail, new_tail, "home H card")
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    if "/i18n-en.js?v=1.21" in html:
        return
    html = html.replace("/recap-r0-61-r0-72g", "/recap-r0-61-r0-72h")
    html = html.replace("/i18n-en.js?v=1.20", "/i18n-en.js?v=1.21")
    html = html.replace("文献综述 v1.20 · 2026-08-27", "文献综述 v1.21 · 2026-08-27")
    html = html.replace("本站 R0.69P–R0.72G 只列为研究笔记", "本站 R0.69P–R0.72H 只列为研究笔记")
    html = html.replace("累计回顾与 97 节索引", "累计回顾与 98 节索引")
    html = html.replace("打开 97 节完整索引", "打开 98 节完整索引")

    old_route_sentence = "R0.72G 在 exact real one-carrier lattice 上用 phase gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量恰为对数量级，并得到 critical-log complete-root sharp saturation。一般 Navier–Stokes 正则性仍开放。</p>"
    new_route_sentence = "R0.72G 在 exact real one-carrier lattice 上用 phase gauge、目标行恒等式与 Rolle–BV 归约证明完整根质量恰为对数量级，并得到 critical-log complete-root sharp saturation。R0.72H 在有限共轭配对多载波系统中证明 mixed row 的载波数无关 moment-resolved payment；全奇数 Rudin–Shapiro 族排除 action-only 版本，并使该 moment 所编码的载波幂次达到同阶。一般 Navier–Stokes 正则性仍开放。</p>"
    html = replace_once(html, old_route_sentence, new_route_sentence, "literature route deck")

    old_cards = """              <div class="route-step closed"><header><b>R0.72G</b><strong>exact one-carrier complete-root packing 与尖锐饱和</strong></header><p>实相位 gauge、目标行恒等式与 Rolle–BV 归约给 \\(G_{\\rm all}\\lesssim\\log\\delta\\)，selected Bessel roots 给匹配下界；原始幅度序列上 critical-log payment 对 complete roots 同阶。结论限于精确实单载波 ray。<a href="/notes/r0-72g.html">研究笔记</a> <a href="/recap-r0-61-r0-72h.html">当前累计回顾</a> <a href="#r072g-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72H</b><strong>finite real multi-carrier mixed-row payment</strong></header><p>处理 \\(\\mathcal E_Q=\\int|hQF|\\)，要求载波数无关的 critical-log payment，或构造显式 growing-carrier 反族。</p></div>"""
    new_cards = """              <div class="route-step closed"><header><b>R0.72G</b><strong>exact one-carrier complete-root packing 与尖锐饱和</strong></header><p>实相位 gauge、目标行恒等式与 Rolle–BV 归约给 \\(G_{\\rm all}\\lesssim\\log\\delta\\)，selected Bessel roots 给匹配下界；原始幅度序列上 critical-log payment 对 complete roots 同阶。结论限于精确实单载波 ray。<a href="/notes/r0-72g.html">研究笔记</a> <a href="/recap-r0-61-r0-72h.html">当前累计回顾</a> <a href="#r072g-boundary">方法边界</a></p></div>
              <div class="route-step closed"><header><b>R0.72H</b><strong>finite multi-carrier mixed-row payment 与 action-only no-go</strong></header><p>目标行、对角耗散和 reciprocal critical-log envelope 给载波数无关的 moment-resolved 上界。全奇数 Rudin–Shapiro 族排除 action-only payment，并达到所需 \\(M\\)-幂次；完整根 corollary 需 compatible real gauge 与 \\(\\delta\\ne0\\)。<a href="/notes/r0-72h.html">研究笔记</a> <a href="/recap-r0-61-r0-72h.html">当前累计回顾</a> <a href="#r072h-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72I</b><strong>physical absorption of row-level data factors</strong></header><p>检查 \\(E_A,m_*,B_A,\\rho_A\\) 是否被完整 physical critical-log normalization 统一支付，或构造 normalized growing-carrier 反族。</p></div>"""
    html = replace_once(html, old_cards, new_cards, "literature H cards")

    g_boundary = """          <div class="boundary"><strong>R0.72G 的主源边界</strong><p>本节真正使用的是 exact one-carrier lattice 的实相位 gauge、两个目标行恒等式与 Rolle–BV 归约；它们把根采样转成连续 negative-Sobolev action，不依赖解析零点计数。限定一手来源检索没有找到直接给出这条 complete temporal root-slope estimate 的定理；该判断是截至 2026-08-27 的 bounded non-collision check，不是原创性、优先权或穷尽性声明。</p></div>"""
    h_boundary = """

          <h3 id="r072h-boundary">R0.72H 的 non-autonomous mixed-row 边界</h3>
          <p><a href="#ref-96">Kato–Ponce</a> 控制空间交换子，不是时间系数导数 \\(V'\\)。<a href="#ref-97">Haak–Ouhabaz</a>、<a href="#ref-98">Trostorff–Waurick</a>与<a href="#ref-99">Kharou</a>提供 non-autonomous maximal regularity 或 observation admissibility，但不从内部 negative-Sobolev action 同时控制两个时变目标行。<a href="#ref-100">Carbonaro–Dragičević</a>、<a href="#ref-101">Morelato–Poggio</a>和<a href="#ref-102">Xu</a>的 bilinear 或 vector-valued heat-flow estimates 也没有 differentiated observation row。</p>
          <p><a href="#ref-103">Nazarov–Pisier–Treil–Volberg</a>说明一般 vector Carleson embedding 可出现有限维增长；这不是本节结构化 scalar heat row 的反定理。<a href="#ref-104">Stadje</a>的 BV indicatrix 和<a href="#ref-60">Narcowich–Ward–Wendland</a>的 scattered-zero inequality 也不控制内生单一时间零水平上的 squared slopes。</p>
          <div class="boundary"><strong>R0.72H 的主源边界</strong><p>本节没有调用一般 non-autonomous bilinear embedding，而是直接使用 scalar target coordinate、共同热因子、对角耗散和 reciprocal-weight moment。限定一手来源检索没有找到直接给出该 carrier-count-independent mixed-row estimate 的定理；这是截至 2026-08-27 的 bounded non-collision check，不是原创性、优先权或穷尽性声明。</p></div>"""
    html = replace_once(html, g_boundary, g_boundary + h_boundary, "literature H boundary")

    references = """            <li id="ref-96">T. Kato and G. Ponce. <a href="https://doi.org/10.1002/cpa.3160410704"><em>Commutator estimates and the Euler and Navier–Stokes equations</em></a>. Comm. Pure Appl. Math. 41 (1988).</li>
            <li id="ref-97">B. Haak and E. M. Ouhabaz. <a href="https://doi.org/10.1007/s00208-015-1199-7"><em>Maximal regularity for non-autonomous evolution equations</em></a>. Math. Ann. 363 (2015); <a href="https://arxiv.org/abs/1402.1136">arXiv</a>.</li>
            <li id="ref-98">S. Trostorff and M. Waurick. <a href="https://doi.org/10.1007/s00020-021-02645-5"><em>Maximal Regularity for Non-Autonomous Evolutionary Equations</em></a>. Integral Equations Operator Theory 93 (2021).</li>
            <li id="ref-99">Y. Kharou. <a href="https://doi.org/10.1007/s00233-022-10281-7"><em>On the admissibility of observation operators for evolution families</em></a>. Semigroup Forum 105 (2022).</li>
            <li id="ref-100">A. Carbonaro and O. Dragičević. <a href="https://doi.org/10.1007/s00526-020-01751-3"><em>Bilinear embedding for divergence-form operators with complex coefficients on irregular domains</em></a>. Calc. Var. 59 (2020).</li>
            <li id="ref-101">L. L. Morelato and A. Poggio. <a href="https://arxiv.org/abs/2605.14699"><em>Bilinear embedding for divergence-form operators with first-order terms and negative potentials</em></a>. Preprint (2026).</li>
            <li id="ref-102">Q. Xu. <a href="https://doi.org/10.4171/JEMS/1430"><em>Holomorphic functional calculus and vector-valued Littlewood–Paley–Stein theory for semigroups</em></a>. J. Eur. Math. Soc. (2025).</li>
            <li id="ref-103">F. Nazarov, G. Pisier, S. Treil and A. Volberg. <a href="https://doi.org/10.1515/crll.2002.004"><em>Sharp estimates in vector Carleson imbedding theorem and for vector paraproducts</em></a>. J. Reine Angew. Math. 542 (2002).</li>
            <li id="ref-104">W. Stadje. <a href="https://doi.org/10.1017/S0013091500017417"><em>On functions with derivative of bounded variation: An analogue of Banach's indicatrix theorem</em></a>. Proc. Edinburgh Math. Soc. 29 (1986).</li>
"""
    marker = "          </ol>\n          <p class=\"source-note\">资料截止"
    html = replace_once(html, marker, references + marker, "literature H references")
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    release_path = ROOT / "research" / "release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release.update(
        {
            "latestCompletedRelease": "r072h",
            "siteVersion": "1.21",
            "publicHtmlNoteCount": 158,
            "postR060RecapNodeCount": 98,
            "nextRelease": "r072i",
            "latestReleaseGate": "tests/r072h-mixed-row-payment-gate.test.mjs",
            "postR070APublishedReleaseCount": 60,
            "postR070AFormalSealedReleaseCount": 36,
            "legacyFormalFigureBacklogCount": 24,
        }
    )
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    site.update({"version": "1.21", "latestRelease": "R0.72H", "publicHtmlNoteCount": 158})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research" / "formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory.update(
        {
            "latestPublishedRelease": "r072h",
            "publishedReleaseCount": 60,
            "formalSealedReleaseCount": 36,
            "legacyFormalFigureBacklogCount": 24,
        }
    )
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r072h" not in inventory[key]:
            inventory[key].append("r072h")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    print("R0.72H release pages and manifests generated")


if __name__ == "__main__":
    main()
