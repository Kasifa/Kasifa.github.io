#!/usr/bin/env python3
"""Generate the deterministic R0.72R release from the public R0.72Q endpoint.

The script is intentionally publication-only: its fail-closed preflight checks
the sealed certificate, the formal figure package, and byte-identical public
figure copies before mutating any HTML or manifest.  It is not executed at the
R0.72R source-freeze stage.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from generate_r072o_release import (
    assert_clean,
    digest,
    once,
    required,
    section,
    verify_flat_hash_ledger,
)
from generate_r072p_release import assert_mathjax_clean


ROOT = Path(os.environ.get("R072R_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_RELATIVE = "figures/r072r-caustic-free-core/fig-r072r-caustic-free-core"
FIGURE_ID = "fig-r072r-caustic-free-core"
CERTIFICATE_RELATIVE = "research/certificates/r072r"


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72R · FOUR-REAL-DIMENSIONAL CORE · BEYOND THE OLD CONE</div>
        <h1>旧加权锥不是 caustic；<br>一个四实维紧致安全核已经越过它</h1>
        <p class="lead">在 complex 1:2:3 coefficient space 中，显式 polydisc \(K=\{|z_2-3/20|\le1/100,\ |z_3|\le1/1000\}\) 的全部初始 profile 都满足 \(Q_2(0)\ge14/25>1/2\)，却沿整个声明热路径始终恰有两个临界点。实际 shear 在 \(0\le y\le1\) 具有统一 \((r,\mathfrak C_0,\mathfrak C_1)=(\pi/48,144,240)\)；同一 cell window 上，固定 commensurate 1:2:3 triangular affine-row propagator 得到系数一致的 full-superposition enhanced-dissipation corollary。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72R 四实维 caustic-free core 完成</span><strong>explicit compact core beyond the old cone: CLOSED</strong><p>版本 v0.72R · 2026-08-28</p><p>four-real-dimensional compact polydisc: CLOSED</p><p>strict exit margin \(Q_2(0)-1/2\ge3/50\): CLOSED</p><p>two critical points on the full heat path: CLOSED</p><p>physical \((r,C_0,C_1)=(\pi/48,144,240)\) on \(0\le y\le1\): CLOSED</p><p>complete four-dimensional caustic stratification: OPEN</p><p>general 3D / Clay problem: OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r"""      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>旧条件是充分锥，不是退化墙</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · EXPLICIT 4D CORE</strong><p>紧致 polydisc \(K\subset\mathbb C^2\cong\mathbb R^4\) 有非空内部，并整体位于 R0.72Q 的 \(Q_2\le1/2\) 锥外。</p></div>
            <div class="verdict-card true"><strong>THEOREM · HEAT-PATH SHAPE</strong><p>每条声明热路径始终只有两个临界点；在 \(0\le y\le1\) 取 \((r,C_0,C_1)=(\pi/48,144,240)\)。</p></div>
            <div class="verdict-card true"><strong>COROLLARY · FULL SUPERPOSITION ED</strong><p>在 \(0\le y\le1\) 的 cell window 内，固定 commensurate 1:2:3 triangular affine-row propagator 对 \(K\) 内系数具有统一 enhanced-dissipation 常数。</p></div>
            <div class="verdict-card false"><strong>OPEN · GLOBAL CAUSTIC</strong><p>没有分类整个四维 caustic、全部 complement components 或 wall-crossing dynamics。</p></div>
          </div>
        </section>

        <section id="core"><div class="section-no">01 / Explicit compact core</div><h2>安全核是四实维 polydisc，不是一条相位线</h2>
          <div class="equation result">\[
          K=\left\{(z_2,z_3)\in\mathbb C^2:
          \left|z_2-\frac3{20}\right|\le\frac1{100},\quad
          |z_3|\le\frac1{1000}\right\},
          \]</div>
          <div class="equation result">\[
          W(y,\phi)=e^{-y}\cos\phi+\operatorname{Re}\!\left(
          z_2e^{-4y}e^{2i\phi}+z_3e^{-9y}e^{3i\phi}\right).
          \]</div>
          <p>这里第一谐波已由平移与归一化固定；\((z_2,z_3)\) 仍保留四个真实自由度。安全结论覆盖整个紧致集合，而不是有限样点。</p>
        </section>

        <section id="cone"><div class="section-no">02 / Cone exit and heat crossing</div><h2>每个初值严格越过旧锥，随后只穿过充分条件边界</h2>
          <div class="equation result">\[
          4|z_2|+9|z_3|\ge\frac{14}{25}=\frac12+\frac3{50}.
          \]</div>
          <p>沿归一化热路径，\(Q_2(y)=4|z_2|e^{-3y}+9|z_3|e^{-8y}\) 严格下降，且 \(Q_2(1)&lt;20489/256000&lt;1/2\)。所以每条路径恰穿过旧边界一次，而临界点仍统一非退化；这次 crossing 不是 caustic。</p>
        </section>

        <section id="critical"><div class="section-no">03 / Two-critical-point theorem</div><h2>中心因式分解与小扰动预算给出全局计数</h2>
          <p>以 \(F_y^0=\cos\phi+(3/20)e^{-3y}\cos2\phi\) 为中心，扰动满足</p>
          <div class="equation result">\[
          \|h_y'\|_\infty\le\frac{23}{1000},\qquad
          \|h_y''\|_\infty\le\frac{49}{1000},\qquad
          \|h_y'''\|_\infty\le\frac{107}{1000}.
          \]</div>
          <p>中心 slope 写成 \(-(\sin\phi)(1+4c(y)\cos\phi)\)，第二因子至少为 \(2/5\)。在 \(\ell=\pi/48\) 的边界，保留精确正 margin \(3047/1536000\)；大盒内严格单调，盒外由 slope 排除。因此临界点恰有两个，分别落在 \(0\) 与 \(\pi\) 的 \(\pi/48\) 邻域。</p>
        </section>

        <section id="shape"><div class="section-no">04 / Physical shape contract</div><h2>root localization 被转换成实际 shear 的统一常数</h2>
          <div class="equation result">\[
          \boxed{N_{\rm crit}=2,\qquad r=\frac\pi{48},\qquad
          \mathfrak C_0=144,\qquad\mathfrak C_1=240,\qquad0\le y\le1.}
          \]</div>
          <p>归一化 profile 的临界 tube 内有 Hessian 下界 \(1/4\)，tube 外有 away-gradient 下界 \(1/80\)。乘回 \(e^{-y}\) 后使用 \(e^{-1}>1/3\)，得到正式物理常数；它们没有被外推到 \(y\to\infty\)。</p>
        </section>

        <section id="ed"><div class="section-no">05 / Family-uniform enhanced dissipation</div><h2>固定 commensurate 1:2:3 triangular affine row 保留全部交叉项</h2>
          <p>四个空间导数上界可取 \(1161/1000,1323/1000,1649/1000,2307/1000\)；若 \(W^{3,\infty}\) 采用四项和范数，可取 \(C_{\rm sh}=161/25\)。slow-reference 充分门槛为 \(\eta\le(3/7)^4=81/2401\)；完整阈值仍包含 Coble–He proof dependency \(\eta_{\rm CH}\)。Coble–He 输入使用 \(0\le t\le\eta^{-1}\)，对应 cell window \(0\le y\le1\)。</p>
          <div class="equation result">\[
          E(y)\le C_Re^{-c_R\sqrt{\varepsilon_c}\,y}E(0),\qquad0\le y\le1,
          \qquad\int_0^1E(y)\,dy\le C_R\varepsilon_c^{-1/2}E(0).
          \]</div>
          <p>常数对 \((z_2,z_3)\in K\)、\(R\)、\(\varepsilon_c\) 和 row datum 一致，但依赖声明的 fixed-pattern reduction。<strong>third-carrier amplitude floor:</strong> 若第三 carrier 被计为 active，物理比较仍需固定 \(|z_3|\ge\beta_->0\)；没有 \(\beta_-\downarrow0\) 的一致性。</p>
        </section>

        <section id="incidence"><div class="section-no">06 / Exact degeneracy incidence</div><h2>四维墙由实 unit-circle incidence 表达，而非复判别式替代</h2>
          <div class="equation result">\[
          z_3=(A+iB)e^{-3i\phi},\qquad
          z_2=e^{-2i\phi}\left[-\frac{\cos\phi+9A}{4}
          -\frac{i(\sin\phi+3B)}2\right].
          \]</div>
          <p>等价地，若 \(u=e^{i\phi}\)，则实 caustic 满足存在 \(|u|=1\) 使 \(D(u)=D'(u)=0\)。沿 incidence，\(f'''=3(5B-\sin\phi)\)、\(f''''=3(15A-\cos\phi)\)。这些公式给出墙的可审计坐标，但没有完成其 self-intersections、singular strata 或 complement components 的全局分类。</p>
        </section>

        <section id="slice"><div class="section-no">07 / Exact real slice</div><h2>代数判别式必须再施加 unit-circle 可实现区间</h2>
          <div class="equation result">\[
          \operatorname{Disc}_uD=-64(4a-9b-1)^3(4a+9b+1)^3
          (a^2+9b^2-3b)^2.
          \]</div>
          <p>实 caustic 包含两条 endpoint lines，以及 \(a^2=3b(1-3b)\) 上 \(1/15\le b\le1/3\) 的 internal arc。遗漏这个区间会把 unit circle 外的重复根误报为真实退化墙；本节也不把这张二维切片冒充四维分类。</p>
        </section>

        <section id="certificate"><div class="section-no">08 / Independent exact audit</div><h2>Python rational 与 JavaScript BigInt 双路核验有限代数骨架</h2>
          <p>两路独立重建 cone-exit margin、perturbation budgets、shape margins、slow-time identity、incidence identities 与 real-slice factorization；comparator 要求 canonical payload 精确相等。证书不替代连续单调性证明、Coble–He 定理或完整 caustic decomposition。</p>
        </section>

        <section id="literature"><div class="section-no">09 / Literature boundary</div><h2>Arnol'd 已给一般 caustic 与 degree-three chamber 拓扑；本站只主张定量安全核</h2>
          <p><a href="https://doi.org/10.1070/RM2001v056n06ABEH000452">Arnol'd (2001)</a> 给出 \(A\cos\phi+B\sin\phi+g(\phi)\) 的一般 caustic 公式和 generic cusp geometry；<a href="https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_8">Arnol'd (1997)</a> 已研究 maximal-real-critical degree-three regions 的拓扑。存在 degree-three chamber 不是本站的新发现。</p>
          <p><a href="https://doi.org/10.1016/j.aim.2023.109275">Voorhaar</a> 给出 Laurent-polynomial Morse discriminant 的复代数背景；<a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He</a> 给出时变非退化 shear 的半群输入。限定一手检索没有定位到这里的精确 rational polydisc、对所有 \(y\ge0\) 的 normalized root-localization margins 与 \(0\le y\le1\) 上 fixed-pattern commensurate 1:2:3 triangular affine-row ED corollary 的组合陈述；这不构成新颖性或优先权证明。</p>
        </section>

        <section id="figure"><div class="section-no">10 / Journal figure</div><h2>正式附图在实系数切片上区分旧充分锥、\(K\) 的实迹与真实 unit-circle caustic</h2>
          <p><img src="/assets/r072r/fig-r072r-caustic-free-core.svg" alt="R0.72R four-real-dimensional caustic-free core beyond the old sufficient cone"></p>
          <p><a href="/assets/r072r/fig-r072r-caustic-free-core.pdf">下载 PDF</a> · <a href="/assets/r072r/fig-r072r-caustic-free-core.png">下载 PNG</a> · <a href="/assets/r072r/fig-r072r-caustic-free-core.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">11 / Research value</div><h2>这是从 phase-uniform 内锥到显式非锥安全核的严格扩张</h2>
          <p>在本站这条研究路线中，R0.72R 给出一个整体处于旧 jet-safety cone 外的四实维系数集：对所有 \(y\ge0\) 具有统一 root localization；在 \(0\le y\le1\) 上具有 physical shape margins、heat-path ledger 与 fixed-pattern commensurate 1:2:3 triangular affine-row full-superposition ED corollary。它可作为特殊 triangular mechanism 论文中的定量 lemma，也为逼近真实 caustic 提供有证书的起点。</p>
          <p>对 Clay 问题的直接价值仍低：第一谐波归一化、有限 commensurate pattern、affine-row invariance、triangular 2.5D reduction 与非退化 critical-point 条件仍远离任意三维初值。</p>
        </section>

        <section id="scope"><div class="section-no">12 / Scope boundary</div><h2>caustic-free compact core 不等于完整四维 caustic classification</h2>
          <p>没有证明整个 \(\mathbb C^2\cong\mathbb R^4\) coefficient space 的 caustic stratification、全部临界点计数胞腔、\(K\) 的最大性、穿越 \(A_2/A_3\) 墙的非自治 ED、任意时变相位、增长 carrier ceiling、一般三维 continuation、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="next"><div class="section-no">13 / Next gate</div><h2>R0.72S：从安全核推进到声明的 wall stratum</h2>
          <p>下一节先在一个明确紧系数盒上分离 generic \(A_2\)、\(A_3\) 与更高余维 strata，再构造逼近或穿越其中一个 stratum 的热路径；完整全局 chamber 分类继续单列，除非获得完备 semialgebraic certificate。</p>
        </section>

        <section id="reproduce"><div class="section-no">14 / Reproduction</div><h2>报告、文献边界、独立审计、精确证书与正式附图包</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072r_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072r_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072r_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072r_independent_audit.md">独立数学审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072r">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072r-caustic-free-core/fig-r072r-caustic-free-core">正式附图包</a> · <a href="/notes/r0-72r.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72r.html">累计回顾</a> · <a href="/recap-r0-61-r0-72r.pdf">累计回顾 PDF</a></p>
        </section>
      </article>"""


HOME_NEXT = '''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72S</span><span class="tree-state current">下一检查点</span></div>
              <h3>approach a declared caustic stratum</h3>
              <p>在明确紧系数盒上分离 generic A2、A3 与更高余维 strata，并研究一条逼近或穿越指定 wall 的热路径。</p>
            </article>'''


HOME_R_CARD = r'''          <div class="task-one" id="r072r" data-release="r072r" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72R · 2026-08-28</p>
            <h3>旧加权锥外的四实维 caustic-free core 已经闭合</h3>
            <p>显式 \(K=\{|z_2-3/20|\le1/100,\ |z_3|\le1/1000\}\) 整体满足 \(Q_2(0)\ge14/25\)，却沿声明热路径对所有 \(y\ge0\) 始终恰有两个临界点；实际 shear 在 \(0\le y\le1\) 可取 \((r,C_0,C_1)=(\pi/48,144,240)\)。</p>
            <p>每条路径都恰穿过旧 \(Q_2=1/2\) 充分条件边界一次而保持统一非退化。该 crossing 不是 caustic；R0.72R 只证明紧致安全核，不声称完成整个四维 caustic 或胞腔分类。</p>
            <p><strong>结论边界：</strong>&nbsp;family-uniform ED 仍属于固定 commensurate 1:2:3 triangular affine-row class，并只在 \(0\le y\le1\) 的 cell window 使用；wall crossing、任意时变相位与一般三维问题未证明。</p>
            <p><a href="/notes/r0-72r.html"><strong>阅读 R0.72R 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72r.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072r/fig-r072r-caustic-free-core.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072r">查看精确证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072r_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072r-caustic-free-core/fig-r072r-caustic-free-core">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72r.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72r.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72S：</strong>&nbsp;从安全核推进到声明的 wall stratum。</p>
          </div>'''


def validate_inputs() -> None:
    required_inputs = (
        "research/r072r_report-source.md",
        "research/r072r_literature_audit.md",
        "research/r072r_gap_matrix.md",
        "research/r072r_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md",
        f"{CERTIFICATE_RELATIVE}/crosscheck.json",
        f"{FIGURE_RELATIVE}/manifest.json",
        "public/notes/r0-72q.html",
        "public/recap-r0-61-r0-72q.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72R release input: {relative}")

    report = (ROOT / "research/r072r_report-source.md").read_text(encoding="utf-8")
    for token in (
        "|z_2-\\frac3{20}\\right|\\le\\frac1{100}",
        "=\\frac{14}{25}",
        "=\\frac12+\\frac3{50}",
        "N_{\\rm crit}=2",
        "r=\\frac\\pi{48}",
        "\\mathfrak C_0=144",
        "\\mathfrak C_1=240",
        "complete four-dimensional caustic stratification is not claimed",
        "R0.72S",
    ):
        if token not in report:
            raise RuntimeError(f"R0.72R report missing claim-boundary token: {token}")
    literature = (ROOT / "research/r072r_literature_audit.md").read_text(encoding="utf-8")
    for token in ("Arnol'd", "Coble", "Voorhaar", "not a novelty or priority certificate"):
        if token not in literature:
            raise RuntimeError(f"R0.72R literature audit missing boundary token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72R certificate")
    verify_flat_hash_ledger(figure, "R0.72R figure")
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if (
        crosscheck.get("status") != "passed"
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or not all(value is True for value in crosscheck.get("checks", {}).values())
    ):
        raise RuntimeError("R0.72R crosscheck is not a formal all-passed seal")

    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    publication = manifest.get("publication", {})
    if (
        manifest.get("release") != "R0.72R"
        or manifest.get("figureId") != FIGURE_ID
        or manifest.get("status") != "formal"
        or manifest.get("qa", {}).get("status") != "passed"
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
        or publication.get("publicCopiesComplete") is not True
        or publication.get("directory") != "public/assets/r072r"
        or publication.get("stem") != FIGURE_ID
    ):
        raise RuntimeError("R0.72R figure manifest is not a complete formal seal")
    validator = ROOT / "research/validate_figure_package.py"
    completed = subprocess.run(
        [sys.executable, str(validator), str(figure)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0 or json.loads(completed.stdout).get("errors") != []:
        raise RuntimeError("R0.72R strict figure validation failed")
    expected_public = []
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = ROOT / publication["directory"] / f"{publication['stem']}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72R public {suffix} is absent or not byte-identical")
        expected_public.append(str(public.relative_to(ROOT)))
    if sorted(row.get("path") for row in publication.get("assets", [])) != sorted(expected_public):
        raise RuntimeError("R0.72R manifest does not enumerate the exact public assets")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72q.html").read_text(encoding="utf-8")
    replacements = (
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72R：旧加权充分锥外的显式四实维 caustic-free core、0≤y≤1 的统一 shape contract，以及 K 上 fixed-pattern commensurate 1:2:3 triangular affine-row full-superposition ED corollary。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72R｜旧锥外的四实维 caustic-free core">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="一个整体越过 Q2≤1/2 旧充分锥的显式 polydisc，仍沿热路径保持两个临界点。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072r/fig-r072r-caustic-free-core.png">'),
        (r'<title>.*?</title>', '<title>R0.72R｜旧锥外的四实维 caustic-free core</title>'),
    )
    for index, (pattern, value) in enumerate(replacements):
        html = section(html, pattern, value, f"R note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.30", "/i18n-en.js?v=1.31", "R note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#core">安全核</a><a href="#cone">旧锥 crossing</a><a href="#critical">临界点</a><a href="#shape">shape</a><a href="#ed">ED</a><a href="#incidence">incidence</a><a href="#slice">实切片</a><a href="#certificate">证书</a><a href="#literature">文献边界</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#scope">边界</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "R note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "R note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 直接判断</a></li><li><a href="#core">01 · 四实维安全核</a></li><li><a href="#cone">02 · 旧锥 crossing</a></li><li><a href="#critical">03 · 临界点计数</a></li><li><a href="#shape">04 · shape contract</a></li><li><a href="#ed">05 · family-uniform ED</a></li><li><a href="#incidence">06 · caustic incidence</a></li><li><a href="#slice">07 · 实系数切片</a></li><li><a href="#certificate">08 · 独立证书</a></li><li><a href="#literature">09 · 文献边界</a></li><li><a href="#figure">10 · 正式附图</a></li><li><a href="#value">11 · 研究价值</a></li><li><a href="#scope">12 · 主张边界</a></li><li><a href="#next">13 · R0.72S</a></li><li><a href="#reproduce">14 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "R note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "R note article")
    footer = '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72R · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>'
    html = section(html, r'<footer>.*?</footer>', footer, "R note footer")
    assert_clean(html, "R0.72R note")
    assert_mathjax_clean(html, "R0.72R note")
    (PUBLIC / "notes/r0-72r.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72q.html").read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.30", "/i18n-en.js?v=1.31"),
        ("R0.61–R0.72Q", "R0.61–R0.72R"),
        ("R0.61 到 R0.72Q 的 107 个研究节点", "R0.61 到 R0.72R 的 108 个研究节点"),
        ("收录节点：107", "收录节点：108"),
        ("回顾截止时公开笔记：167", "回顾截止时公开笔记：168"),
        ("回顾截止节点：R0.72Q", "回顾截止节点：R0.72R"),
        ("02 · 107 节完整索引", "02 · 108 节完整索引"),
        ("<strong>107</strong><span>R0.61–R0.72R 研究节点</span>", "<strong>108</strong><span>R0.61–R0.72R 研究节点</span>"),
        ("<strong>69</strong><span>R0.70A–R0.72Q 已公开版本</span>", "<strong>70</strong><span>R0.70A–R0.72R 已公开版本</span>"),
        ("<strong>45</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>46</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("后面的 107 个节点", "后面的 108 个节点"),
        ("R0.70A–R0.72Q 的 69 个版本已经公开；其中 45 个", "R0.70A–R0.72R 的 70 个版本已经公开；其中 46 个"),
        ("R0.61–R0.72R 的 107 节公开笔记", "R0.61–R0.72R 的 108 节公开笔记"),
        ("/recap-r0-61-r0-72q.pdf", "/recap-r0-61-r0-72r.pdf"),
    ):
        html = required(html, old, new, f"R recap {old}")
    html = section(html, r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72R 的 108 个节点；最新一节闭合旧加权锥外的四实维 caustic-free core。">', "R recap description")
    html = section(html, r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="二十八个阶段、108 个节点：从约化递推到旧充分锥外的四实维安全核。">', "R recap og description")
    html = section(html, r'<title>.*?</title>', '<title>R0.61–R0.72R｜R0.60 之后的研究回顾</title>', "R recap title")
    phase = r'''            <article class="phase"><h3>R0.72L–R0.72R · strong-coupling、物理回填与 caustic-free coefficient geometry</h3>
              <p>R0.72L 保留 actual ledger；R0.72M 给出零扩散 action-poor reference，R0.72N 排除声明耗散一载波链上的该安全分支。R0.72O 完成物理回填，R0.72P 在 fixed real-collinear static-phase 1:2 正类上关闭完整传播门，R0.72Q 再闭合 fixed-\(M\) arbitrary-static-phase、\(Q_2\le1/2\) 的 shape gate。</p>
              <p>R0.72R 证明该 \(Q_2\) 条件只是一条充分锥：显式四实维 polydisc \(K\) 整体满足 \(Q_2(0)\ge14/25>1/2\)，却沿每条声明热路径对所有 \(y\ge0\) 始终恰有两个临界点；在 \(0\le y\le1\) 上，物理 shear 具有 shape constants \((\pi/48,144,240)\)，且声明的 fixed-pattern 1:2:3 triangular affine-row propagator 具有 coefficient-uniform full-superposition ED corollary。</p>
              <p>每条热路径恰穿过旧 \(Q_2=1/2\) 边界一次而不退化。R0.72R 只给一个 caustic-free compact core；完整四维 caustic stratification、wall crossing、任意时变相位与一般三维问题仍开放。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/notes/r0-72m.html">R0.72M</a><a href="/notes/r0-72n.html">R0.72N</a><a href="/notes/r0-72o.html">R0.72O</a><a href="/notes/r0-72p.html">R0.72P</a><a href="/notes/r0-72q.html">R0.72Q</a><a href="/notes/r0-72r.html">R0.72R</a><a href="/assets/r072r/fig-r072r-caustic-free-core.pdf">R0.72R 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072r">R0.72R 证书</a></div></article>'''
    html = section(html, r'            <article class="phase"><h3>R0\.72L–R0\.72Q .*?</article>', phase, "R recap phase")
    node_q = '            <span class="node-ref"><a href="/notes/r0-72q.html">R0.72Q</a><span class="node-state kind-closed">闭</span></span>\n'
    node_r = '            <span class="node-ref"><a href="/notes/r0-72r.html">R0.72R</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_q, node_q + node_r, "R recap node")
    retained = r'''            <li>R0.72R 的 four-real-dimensional caustic-free core：整个 \(K\) 严格位于旧 \(Q_2\le1/2\) 充分锥外，沿声明热路径对所有 \(y\ge0\) 仍恰有两个临界点；在 \(0\le y\le1\) 上，物理 shear 具有 shape constants \((\pi/48,144,240)\)，且声明的 fixed-pattern commensurate 1:2:3 triangular affine-row propagator 具有 coefficient-uniform ED corollary。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "R recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>旧安全锥已被严格越过，真实 caustic wall 仍是下一道边界</h2><p>截至 R0.72R，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 108 个节点或 70 个公开版本解释成 Clay 问题完成比例。</p><p>新的严格增量是一个非空四实维紧致系数核：它整体位于 R0.72Q 加权锥外，具有 \(y\ge0\) 的全热路径 root localization，并在 \(0\le y\le1\) 具有物理 shape contract 和 fixed-pattern commensurate 1:2:3 triangular affine-row family-uniform ED。</p></section>''', "R recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72S 从安全核推进到声明的 caustic stratum</h2><p>先在明确紧系数盒上分离 generic \(A_2\)、\(A_3\) 与更高余维 strata，再研究一条逼近或穿越指定 wall 的热路径。</p></section>''', "R recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72R 的 70 节已公开；46 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。</p><p>R0.72R 证明的是固定 first harmonic、commensurate 1:2:3、triangular affine-row class 中的显式 caustic-free compact core，不是整个 \(\mathbb C^2\) coefficient space 的 chamber classification。caustic crossing、任意时变相位、增长 carrier ceiling 与 Clay 正式问题保持开放。</p></section>''', "R recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72q.html">保留 R0.72Q 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72r.html">打开最新节点 R0.72R</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072r">查看 R0.72R 精确证书</a> · <a href="/assets/r072r/fig-r072r-caustic-free-core.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72r.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72q.pdf">上一版累计回顾 PDF</a></p><p>完整节点索引保留 R0.69W、R0.70A 以后每个公开版本及其原始编号；状态标签只描述证据类型。</p></section>''', "R recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72R 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "R recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 108 or len(set(links)) != 108:
        raise RuntimeError(f"recap node index expected 108 unique links, got {len(links)}/{len(set(links))}")
    assert_clean(html, "R0.72R recap")
    assert_mathjax_clean(html, "R0.72R recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72r.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.30"', 'data-site-version="1.31"'),
        ("/i18n-en.js?v=1.30", "/i18n-en.js?v=1.31"),
        ("/site-refresh.js?v=1.30", "/site-refresh.js?v=1.31"),
        ("<strong>v1.30</strong>网页版本", "<strong>v1.31</strong>网页版本"),
        ("<strong>167</strong>公开研究笔记", "<strong>168</strong>公开研究笔记"),
        ("<strong>R0.72Q</strong>最新研究节点", "<strong>R0.72R</strong>最新研究节点"),
        ("<strong>caustic geometry beyond the dominant-first-harmonic cone</strong>当前方向", "<strong>caustic-wall stratification and nonautonomous crossing</strong>当前方向"),
        ("Research topology · R0.1–R0.72Q", "Research topology · R0.1–R0.72R"),
        ("R0.70A–R0.72Q：69 节已公开，45 节完整封存", "R0.70A–R0.72R：70 节已公开，46 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72Q</span>', '<span class="route-range">R0.69P–R0.72R</span>'),
        ('aria-label="R0.69P–R0.72Q"', 'aria-label="R0.69P–R0.72R"'),
        ("展开 77 篇公开笔记", "展开 78 篇公开笔记"),
        ("本站 R0.69P–R0.72L 路线", "本站 R0.69P–R0.72R 路线"),
        ("下一步 R0.72Q：</strong>", "阶段后续 R0.72Q（已完成）：</strong>"),
        ("下一步 R0.72R：</strong>", "阶段后续 R0.72R（已完成）：</strong>"),
        ("综述 v1.30 · 2026-08-28", "综述 v1.31 · 2026-08-28"),
        ("上次综述 v1.29 · 2026-08-27", "上次综述 v1.30 · 2026-08-28"),
        ("/recap-r0-61-r0-72q.html", "/recap-r0-61-r0-72r.html"),
        ("/recap-r0-61-r0-72q.pdf", "/recap-r0-61-r0-72r.pdf"),
    ):
        html = required(html, old, new, f"R home {old}")
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72R 已闭合旧 Q2≤1/2 锥外的四实维 caustic-free core；下一关是指定 caustic stratum 的逼近或穿越。</span></div>', "R home focus")
    link_q = '<a class="milestone" href="/notes/r0-72q.html">R0.72Q</a>'
    html = once(html, link_q, link_q + '\n                  <a class="milestone" href="/notes/r0-72r.html">R0.72R</a>', "R home route link")
    route_r = r'''              <p>R0.72R 严格离开旧加权锥：显式四实维 polydisc 整体满足 \(Q_2(0)\ge14/25>1/2\)，沿声明热路径对所有 \(y\ge0\) 保持恰好两个临界点；物理 shape constants \((\pi/48,144,240)\) 与 fixed-pattern commensurate 1:2:3 triangular affine-row family-uniform ED 只在 \(0\le y\le1\) 的 cell window 使用。每条路径穿过 \(Q_2=1/2\) 时仍统一非退化；旧边界因此不是 caustic。这里只证明 caustic-free compact core，不作完整四维 chamber 分类。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_r + '              <details class="tree-notes" open>', "R home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "R home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72R · 2026-08-28</p>
            <h3>R0.60 recap 之后的累计回顾收录 108 个节点；全站现有 168 篇公开研究笔记</h3>
            <p>累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72R 的完整逐节点索引。R0.72R 给出旧加权锥外的四实维 caustic-free core、对所有 \(y\ge0\) 的全热路径 root localization，以及 \(0\le y\le1\) 上的物理 shape contract 与 fixed-pattern commensurate 1:2:3 triangular affine-row coefficient-uniform full-superposition ED。</p>
            <p>R0.70A–R0.72R 共 70 个版本已公开；46 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;旧充分锥已被越过；完整四维 caustic stratification、wall crossing 与一般三维问题仍开放。</p>
            <p><a href="/recap-r0-61-r0-72r.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72r.pdf">下载同步 PDF</a></p>
          </div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "R home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_R_CARD + '\n        </section>\n\n      </article>', "R home card")
    if html.count('data-release="r072r"') != 1:
        raise RuntimeError("home must contain exactly one R0.72R card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72R">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 78:
        raise RuntimeError("home current-route index must contain 78 note links")
    assert_clean(html, "R0.72R home")
    assert_mathjax_clean(html, "R0.72R home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.30", "/i18n-en.js?v=1.31"),
        ("资料截止 2026-08-27", "资料截止 2026-08-28"),
        ("资料截止：2026-08-27", "资料截止：2026-08-28"),
        ("本站 R0.69P–R0.72Q 只列为研究笔记", "本站 R0.69P–R0.72R 只列为研究笔记"),
        ("/recap-r0-61-r0-72q.html", "/recap-r0-61-r0-72r.html"),
        ("文献综述 v1.30 · 2026-08-28", "文献综述 v1.31 · 2026-08-28"),
        ("累计回顾与 107 节索引", "累计回顾与 108 节索引"),
        ("打开 107 节完整索引", "打开 108 节完整索引"),
    ):
        html = required(html, old, new, f"R literature {old}")
    overview_old = r'''R0.72O 将该 cubic 回填物理账本，得到 \(\varepsilon^{11/6}\) numerator 与 \(R^{4/3}L_{R,\varepsilon}^2\) window；多载波只在带统一常数的 full-superposition ED 假设下条件成立。一般 Navier–Stokes 正则性仍开放。'''
    overview_new = r'''R0.72O 将该 cubic 回填物理账本，得到 \(\varepsilon^{11/6}\) numerator 与 \(R^{4/3}L_{R,\varepsilon}^2\) window；多载波只在带统一常数的 full-superposition ED 假设下条件成立。R0.72P 在 fixed real-collinear static-phase 1:2 正类上关闭完整传播门，R0.72Q 再证明 fixed-\(M\)、arbitrary-static-phase、\(Q_2\le1/2\) 的 two-critical-point shape gate，并给出精确 1:2 caustic。R0.72R 构造整体位于旧加权锥外的四实维 rational polydisc，闭合对所有 \(y\ge0\) 的全热路径 root localization，并在 \(0\le y\le1\) 闭合物理 \((\pi/48,144,240)\) shape contract 与 coefficient-uniform fixed-pattern commensurate 1:2:3 triangular affine-row enhanced dissipation；完整四维 caustic stratification 未完成。一般 Navier–Stokes 正则性仍开放。'''
    html = once(html, overview_old, overview_new, "R literature route overview")
    old_open = '<div class="route-step pause"><header><b>开放接口 · R0.72R</b><strong>leave the dominant-first-harmonic cone</strong></header><p>研究受控 1:2:3 caustic 或逼近退化墙的 profile，定位 uniform shape contract 的新边界。</p></div>'
    new_steps = r'''<div class="route-step closed"><header><b>R0.72R</b><strong>four-real-dimensional caustic-free core beyond the old cone</strong></header><p>显式 rational polydisc 整体满足 \(Q_2(0)\ge14/25>1/2\)，沿热路径对所有 \(y\ge0\) 保持两个临界点；在 \(0\le y\le1\) 的 cell window 内具有 physical shape constants \((\pi/48,144,240)\)。旧锥 crossing 不是 caustic。<a href="/notes/r0-72r.html">研究笔记</a> <a href="/recap-r0-61-r0-72r.html">当前累计回顾</a> <a href="#r072r-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72S</b><strong>approach a declared caustic stratum</strong></header><p>在明确紧系数盒上分离 generic \(A_2\)、\(A_3\) 与更高余维 strata，并研究逼近或穿越指定 wall 的热路径。</p></div>'''
    html = once(html, old_open, new_steps, "R literature route")
    boundary = r'''

          <h3 id="r072r-boundary">R0.72R 的四实维安全核与 caustic 文献边界</h3>
          <p><a href="https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_8">Arnol'd (1997)</a> 已研究实三角多项式 maximal-real-critical regions 的拓扑，degree three 的这类区域并非本站新发现。<a href="https://doi.org/10.1070/RM2001v056n06ABEH000452">Arnol'd (2001)</a> 给出 \(A\cos\phi+B\sin\phi+g(\phi)\) 的一般 caustic 公式和 generic cusp geometry。R0.72R 的严格增量只是在 fixed-first-harmonic 四实维切片中给出一个显式 rational compact core，以及在 \(0\le y\le1\) 上支持 fixed-pattern commensurate \(1{:}2{:}3\) triangular affine-row ED 的统一 margins。</p>
          <p><a href="https://doi.org/10.1016/j.aim.2023.109275">Voorhaar</a> 研究 univariate Laurent polynomial 的 caustic 与 Morse discriminant；complex discriminant 不能替代本站的 real self-inversive unit-circle incidence。<a href="https://doi.org/10.4310/CMS.2024.v22.n6.a10">Coble–He</a> 提供时变非退化 shear 的 semigroup input；polydisc、对所有 \(y\ge0\) 的 normalized root-localization margins、\(0\le y\le1\) 的 physical shape constants 与同窗 heat-path ledger，是本站为上述固定类供给的 family-uniform inputs。</p>
          <p><a href="https://doi.org/10.1007/s00205-017-1099-y">Bedrossian–Coti Zelati</a> 与 <a href="https://doi.org/10.1016/j.jfa.2022.109522">Albritton–Beekie–Novack</a> 给出 stationary degenerate critical points 的较慢 ED benchmarks；它们不等价于非自治 caustic crossing theorem，也说明 caustic 不是 ED 失败墙。</p>
          <div class="boundary"><strong>R0.72R 的主张边界</strong><p>证明的是 \(K\subset\mathbb C^2\cong\mathbb R^4\) 位于一个 nondegenerate complement component 内的 compact core；complement component 本身是开集，不能把 \(K\) 称为完整紧致胞腔。临界点计数对所有 \(y\ge0\) 成立；physical shape contract 与 fixed-pattern commensurate 1:2:3 triangular affine-row ED 只在 \(0\le y\le1\) 的 cell window 使用。没有完成整个四维 caustic 的 \(A_2/A_3\) stratification、全部 component count、\(K\) 的最大性或 wall-crossing ED。限定一手检索没有定位到该精确 polydisc 与全热路径定量组合，但不构成新颖性或优先权证明。</p></div>'''
    match = re.search(r'(<h3 id="r072q-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("R literature boundary: expected one R0.72Q boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "R literature boundary")
    references = '''            <li id="ref-105">V. I. Arnol'd. <a href="https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_8"><em>Topological Classification of Real Trigonometric Polynomials and Cyclic Serpents Polyhedron</em></a>. In <em>The Arnold–Gelfand Mathematical Seminars</em>, Birkhäuser (1997).</li>
            <li id="ref-106">V. I. Arnol'd. <a href="https://doi.org/10.1070/RM2001v056n06ABEH000452"><em>Astroidal Geometry of Hypocycloids and the Hessian Topology of Hyperbolic Polynomials</em></a>. Russian Math. Surveys 56 (2001), 1019–1083.</li>
            <li id="ref-107">A. Voorhaar. <a href="https://doi.org/10.1016/j.aim.2023.109275"><em>The Newton Polytope of the Morse Discriminant of a Univariate Polynomial</em></a>. Adv. Math. 432 (2023), 109275.</li>
'''
    html = once(html, "          </ol>\n          <p class=\"source-note\">资料截止：2026-08-28。", references + "          </ol>\n          <p class=\"source-note\">资料截止：2026-08-28。", "R literature references")
    assert_clean(html, "R0.72R literature")
    assert_mathjax_clean(html, "R0.72R literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    notes = len(list((PUBLIC / "notes").glob("*.html")))
    if notes != 168:
        raise RuntimeError(f"expected 168 public HTML notes after R0.72R, got {notes}")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    expected = {
        "latestCompletedRelease": "r072q",
        "siteVersion": "1.30",
        "publicHtmlNoteCount": 167,
        "postR060RecapNodeCount": 107,
        "nextRelease": "r072r",
        "latestReleaseGate": "tests/r072q-phase-robust-shape-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072q-release.test.mjs",
        "postR070APublishedReleaseCount": 69,
        "postR070AFormalSealedReleaseCount": 45,
        "legacyFormalFigureBacklogCount": 24,
    }
    for key, value in expected.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72Q: {key}")
    stage = release.get("nextReleaseSourceStage", {})
    expected_stage = {
        "release": "r072r",
        "stage": "source-freeze",
        "publicationStatus": "pending-formal-certificate-figure-and-publication",
        "publicCountersAdvanced": False,
        "report": "research/r072r_report-source.md",
        "independentAudit": "research/r072r_independent_audit.md",
        "producer": "research/r072r_exact_audit.py",
        "independentProducer": "research/r072r_independent_audit.mjs",
        "comparator": "research/r072r_compare_audits.py",
        "certificateDirectory": "research/certificates/r072r",
        "figureDirectory": FIGURE_RELATIVE,
        "generator": "scripts/generate_r072r_release.py",
        "translationScript": "scripts/add-r072r-translations.mjs",
        "releaseGate": "tests/r072r-caustic-free-core-gate.test.mjs",
        "publicationTest": "tests/r072r-release.test.mjs",
    }
    if stage != expected_stage:
        raise RuntimeError("R0.72R source-stage manifest contract is missing or stale")
    release.update({
        "latestCompletedRelease": "r072r",
        "siteVersion": "1.31",
        "publicHtmlNoteCount": 168,
        "postR060RecapNodeCount": 108,
        "nextRelease": "r072s",
        "latestReleaseGate": "tests/r072r-caustic-free-core-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072r-release.test.mjs",
        "postR070APublishedReleaseCount": 70,
        "postR070AFormalSealedReleaseCount": 46,
    })
    del release["nextReleaseSourceStage"]
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if site.get("latestRelease") != "R0.72Q" or site.get("publicHtmlNoteCount") != 167:
        raise RuntimeError("site-version is not at R0.72Q")
    site.update({"version": "1.31", "latestRelease": "R0.72R", "publicHtmlNoteCount": 168, "publishedDate": "2026-08-28"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") != "r072q" or inventory.get("legacyFormalFigureBacklogCount") != 24:
        raise RuntimeError("formal archive inventory is not at R0.72Q")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072q" or "r072r" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72Q")
        inventory[key].append("r072r")
    inventory.update({"latestPublishedRelease": "r072r", "publishedReleaseCount": 70, "formalSealedReleaseCount": 46})
    if len(inventory["publishedReleases"]) != 70 or len(inventory["formalSealedReleases"]) != 46:
        raise RuntimeError("formal archive count mismatch after R0.72R")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in (
        "research-review.html",
        "literature-review.html",
        "notes/r0-72r.html",
        "recap-r0-61-r0-72r.html",
    ):
        assert_clean((PUBLIC / relative).read_text(encoding="utf-8"), relative)
    print(json.dumps({
        "release": "R0.72R",
        "siteVersion": "1.31",
        "notes": 168,
        "recapNodes": 108,
        "published": 70,
        "formalSealed": 46,
        "legacyBacklog": 24,
        "phases": 28,
        "routeNotes": 78,
        "next": "R0.72S",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
