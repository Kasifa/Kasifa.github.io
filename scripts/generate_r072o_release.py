#!/usr/bin/env python3
"""Generate the deterministic R0.72O GitHub Pages release from site v1.27."""

from __future__ import annotations

import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(os.environ.get("R072O_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def verify_flat_hash_ledger(directory: Path, label: str) -> None:
    ledger = directory / "SHA256SUMS"
    if not ledger.is_file():
        raise RuntimeError(f"{label}: missing SHA256SUMS")
    rows = ledger.read_text(encoding="utf-8").splitlines()
    names: list[str] = []
    for row in rows:
        match = re.fullmatch(r"([0-9a-f]{64})  ([^/\\\r\n]+)", row)
        if match is None:
            raise RuntimeError(f"{label}: malformed SHA256SUMS row: {row!r}")
        expected, name = match.groups()
        target = directory / name
        if not target.is_file() or target.is_symlink():
            raise RuntimeError(f"{label}: invalid ledger target: {name}")
        if digest(target) != expected:
            raise RuntimeError(f"{label}: SHA256 mismatch: {name}")
        names.append(name)
    if names != sorted(set(names)):
        raise RuntimeError(f"{label}: SHA256SUMS must be unique and sorted")
    entries = []
    for path in directory.iterdir():
        if path.name in {"SHA256SUMS", ".DS_Store"}:
            continue
        if not path.is_file() or path.is_symlink():
            raise RuntimeError(f"{label}: unexpected non-file artifact: {path.name}")
        entries.append(path.name)
    if names != sorted(entries):
        raise RuntimeError(f"{label}: SHA256SUMS does not cover exact package bytes")


def once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return text.replace(old, new, 1)


def required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise RuntimeError(f"{label}: missing {old}")
    return text.replace(old, new)


def section(text: str, pattern: str, new: str, label: str) -> str:
    updated, count = re.subn(pattern, lambda _match: new, text, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one match, found {count}")
    return updated


def assert_clean(text: str, label: str) -> None:
    bad = [
        (index, ord(character))
        for index, character in enumerate(text)
        if ord(character) < 32 and character not in "\t\n\r"
    ]
    if bad:
        raise RuntimeError(f"{label}: forbidden control characters {bad[:8]}")
    for phrase in ("我们", "攻关", "主攻", "研究纪律", "杀死错误想法", "突破"):
        if phrase in text:
            raise RuntimeError(f"{label}: discouraged public phrase {phrase}")


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72O · PHYSICAL REINSERTION · SUPERPOSITION INTERFACE</div>
        <h1>次线性 cubic 已回填物理账本；<br>一载波窗口加倍，多载波仍有独立门槛</h1>
        <p class="lead">R0.72N 的一载波 enhanced-dissipation cubic 在 exact-root correction 后仍满足 \(\mathcal C_\times\lesssim a^2\varepsilon^{1/2}\)。把它严格放回 R0.72L 的物理归一化后，正确 numerator 是 \(\varepsilon^{11/6}\)，强耦合窗口推进到 \(\varepsilon\lesssim R^{4/3}L_{R,\varepsilon}^2\)。多载波公式只有在带统一常数的 full-superposition integrated enhanced dissipation 下成立；common-band support 与逐载波估计都不能替代这个假设。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72O 定理与条件接口完成</span><strong>one-carrier reinsertion closed; superposition gate open</strong><p>版本 v0.72O · 2026-08-27</p><p>one-carrier exact correction: CLOSED</p><p>physical numerator \(\varepsilon^{11/6}\): CLOSED</p><p>growing-geometry strong window: CLOSED</p><p>fixed-geometry arbitrary coupling: OPEN</p><p>multi-carrier full-superposition ED: CONDITIONAL</p><p>一般三维正则性：OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r"""      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>一载波物理回填已经闭合，多载波结论仍严格带条件</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>THEOREM · CORRECTED ONE-CARRIER CUBIC</strong><p>对 R0.72L–N 的 fixed-background、row-aligned、phase-aligned、exact-root-corrected 一载波族，\(\mathcal C_\times\lesssim a^2\varepsilon^{1/2}\)。</p></div>
            <div class="verdict-card true"><strong>THEOREM · PHYSICAL REINSERTION</strong><p>物理 lift 给 \(U_{\rm ED}^{(1)}=\varepsilon^{11/6}\)，并把 strong window 推进到 \(\sqrt\varepsilon\lesssim R^{2/3}L_{R,\varepsilon}\)。</p></div>
            <div class="verdict-card false"><strong>CONDITIONAL · MULTI-CARRIER</strong><p>若完整叠加满足 integrated enhanced dissipation，且常数对比较的参数与几何族一致，则 \(U_{\rm ED}=\varepsilon^{11/6}p^{4/3}\)；当前 common-band 假设本身不推出该传播估计。</p></div>
            <div class="verdict-card false"><strong>OPEN · FIXED GEOMETRY</strong><p>窗口上沿只给统一有界，little-o 子区间才衰减；固定 \(R\) 下任意强耦合仍未闭合。</p></div>
          </div>
        </section>

        <section id="identification"><div class="section-no">01 / Exact identification</div><h2>correction 前的 antisymmetric launch 上，raw cubic 与 R0.72N 耗散量完全相同</h2>
          <p>对 correction 前的 antisymmetric one-carrier launch，\(h=P_0V_wF\)、\(b=P_0V_w^2F\)。以 \(y=R^2x\) 重标度后，R0.72L 的完整 cubic row 精确变成</p>
          <div class="equation result">\[
            \mathcal C_\times=4a^2\int_0^1\varepsilon e^{-(3+2\mu)y}
            |f_1(f_0-f_2)|\,dy=\mathcal C_{\rm diss}.
          \]</div>
          <p>exact-root correction 加入 \(\widetilde G=G+\zeta e_0\)。Coble–He 半群估计对任意 \(L^2\) 初值成立，固定坐标泛函有统一范数，所以 correction 不破坏</p>
          <div class="equation result">\[
            \boxed{\mathcal C_\times(\widetilde G)\lesssim a^2\varepsilon^{1/2}.}
          \]</div>
        </section>

        <section id="reinsertion"><div class="section-no">02 / Physical reinsertion</div><h2>平方根 raw exponent 经过物理 lift 后变成 \(11/6\)</h2>
          <p>一载波满足 \(g=\varepsilon R^2\)、\(\Theta\asymp g^2/(a^2R^2)\) 与 \(D^{1/3}\asymp g^{2/3}R^{2/3}\)。因此</p>
          <div class="equation result">\[
            \frac{\Theta(a^2\varepsilon^{1/2})}{D^{1/3}}
            \asymp\boxed{\varepsilon^{11/6}}.
          \]</div>
          <p>这里不能把 raw \(\varepsilon^{1/2}\) 直接写进 normalized ledger；\(11/6\) 才是物理 numerator 的正确指数。</p>
        </section>

        <section id="ledger"><div class="section-no">03 / Corrected ledger</div><h2>新分支与原有两条 cubic 分支共同进入完整账本</h2>
          <div class="equation result">\[
          \frac{\mathcal J_{\rm all}}{D^{1/3}\Lambda_{1,*}}
          \le C\!\left[
          \frac{\varepsilon^{4/3}}{K+x}
          +\varepsilon^{1/3}R^{-1/3}L_R^{-1/2}\frac{\sqrt x}{K+x}
          +\frac{\min\{\varepsilon^{7/3},\varepsilon^{1/3}Rx,
          \varepsilon^{11/6}\}}{K+x}\right].
          \]</div>
          <p>exact-root launch 仍给 action floor
          \(x\ge Z\gtrsim\varepsilon^2R^{2/3}(1+\varepsilon)^{-2/3}L_{R,\varepsilon}\)。</p>
        </section>

        <section id="window"><div class="section-no">04 / Strong-coupling window</div><h2>一载波 paid window 同时加倍 \(R\) 幂和 logarithm 幂</h2>
          <p>对 \(\varepsilon\ge1\)，完整比值满足</p>
          <div class="equation result">\[
          \frac{\mathcal J_{\rm all}}{D^{1/3}\Lambda_{1,*}}
          \lesssim
          \frac1{R^{2/3}L_{R,\varepsilon}}
          +\frac{\varepsilon^{-1/3}}{R^{2/3}(L_RL_{R,\varepsilon})^{1/2}}
          +\frac{\varepsilon^{1/2}}{R^{2/3}L_{R,\varepsilon}}.
          \]</div>
          <div class="equation result">\[
            \boxed{\sqrt\varepsilon\lesssim R^{2/3}L_{R,\varepsilon}},
            \qquad
            \boxed{\varepsilon\lesssim R^{4/3}L_{R,\varepsilon}^{\,2}}.
          \]</div>
          <p>沿固定 polynomial coupling，\(L_{R,\varepsilon}\asymp1+\log R\)。上沿只给 \(O(1)\)；little-o 版本才使比值趋零。</p>
        </section>

        <section id="fixed"><div class="section-no">05 / Fixed-geometry boundary</div><h2>次线性 raw cubic 仍没有支付固定几何上的任意强耦合</h2>
          <div class="equation result">\[
            \frac{\varepsilon^{11/6}}{K+x}
            \lesssim\frac{\varepsilon^{1/2}}{\log\varepsilon}
            \qquad(R\ \text{fixed}).
          \]</div>
          <p>这个已证上包络不衰减。因此 R0.72O 扩大的是 growing-geometry strong window，不是 fixed-geometry closure。</p>
        </section>

        <section id="superposition"><div class="section-no">06 / Full-superposition implication</div><h2>交叉项可以整体支付，但前提必须作用于完整叠加</h2>
          <p>令 \(p=\sqrt N/B\)。若完整多载波传播满足</p>
          <div class="equation result">\[
            \int_0^1E(y)\,dy\le C_{\rm ED}\varepsilon^{-1/2}E(0),
            \qquad E(1)\le C_{\rm ED}e^{-c_{\rm ED}\sqrt\varepsilon}E(0),
          \]</div>
          <p>这里 \(C_{\rm ED}\) 与 \(c_{\rm ED}\) 必须对所比较的 \(N,p,R,\varepsilon\) 和声明的载波几何族一致；否则只得到逐点蕴含，不能得到统一尺度律。</p>
          <p>则不展开 carrierwise triples，直接由算子范数得到</p>
          <div class="equation result">\[
            \mathcal C_\times\lesssim a^2N^2\varepsilon^{1/2},
            \quad U_{\rm ED}=\varepsilon^{11/6}p^{4/3},
            \quad \sqrt\varepsilon\lesssim p^{2/3}R^{2/3}L_{R,\varepsilon}.
          \]</div>
          <p>这是带统一常数假设的条件蕴含，不是当前 common-band class 的无条件定理。</p>
        </section>

        <section id="gate"><div class="section-no">07 / Cross-term gate</div><h2>逐载波求和与 common-band support 都不足</h2>
          <p>R0.72J 的 triangle-rich coherent block 有 \(3R(R+1)\) 个有序 signed Schur triples，并达到 \(\mathcal C_{\times,R}\asymp a^2N^2\)。因此把 \(N\) 个 one-carrier costs 相加会漏掉真实 cross cubics。</p>
          <p>形状门也不能由频带自动推出。两载波剪切</p>
          <div class="equation result">\[
            U_R(\theta)=\sin(R\theta)-\frac{R}{R+1}\sin((R+1)\theta)
          \]</div>
          <p>在 \(\theta=0\) 满足 \(U_R'(0)=U_R''(0)=0\)、\(U_R'''(0)=R(2R+1)\ne0\)。组合剪切具有退化临界点，不能直接调用 Coble–He 的统一非退化定理。</p>
        </section>

        <section id="literature"><div class="section-no">08 / Literature boundary</div><h2>published theorem 与项目新推论保持分开</h2>
          <p><a href="https://arxiv.org/html/2309.15738">Coble–He, Theorem 1.2</a> 给足够小 \(\nu\) 下非退化时变剪切的 modewise \(e^{-c\nu^{1/2}|k|^{1/2}t}\) 衰减；本站再用 \(L^2\) 收缩补齐剩余紧参数区间。原论文不陈述这里的 cubic、物理回填或多载波结论。</p>
          <p><a href="https://doi.org/10.1112/jlms.12782">Coti Zelati–Gallay</a> 证明静态剪切的 rate 随临界点退化阶改变，支持保留 shape parameter；Couette 与 Kolmogorov 的非线性稳定理论只提供 flow-specific 方法先例。限定检索没有找到基于 \((R,N,B,p)\) 的 black-box full-superposition theorem，也不构成新颖性或优先权证明。</p>
        </section>

        <section id="figure"><div class="section-no">09 / Journal figure</div><h2>附图只展示已证明的指数账本与条件分界</h2>
          <p><img src="/assets/r072o/fig-r072o-physical-reinsertion.svg" alt="R0.72O physical reinsertion and full-superposition interface formal figure"></p>
          <p><a href="/assets/r072o/fig-r072o-physical-reinsertion.pdf">下载 PDF</a> · <a href="/assets/r072o/fig-r072o-physical-reinsertion.png">下载 PNG</a> · <a href="/assets/r072o/fig-r072o-physical-reinsertion.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">10 / Research value</div><h2>物理付款不再停在 raw exponent，多载波缺口也被精确定位</h2>
          <p>R0.72O 把 R0.72N 的 continuum enhanced-dissipation corollary 完整送入 normalized physical ledger，得到此前没有的 \(R^{4/3}(\log R)^2\) strong window。与此同时，剩余困难不再是简单 carrier counting，而是组合剪切的统一 shape control 或等价的 full-superposition flux estimate。</p>
          <p>这仍是特殊 triangular 2.5D family 中的机制定理，不是一般三维 continuation criterion。</p>
        </section>

        <section id="next"><div class="section-no">11 / Next gate</div><h2>R0.72P：先处理有统一 Morse margin 的有限 carrier pattern</h2>
          <p>下一节直接证明 full-superposition integrated ED，或证明更弱但足够的 rowwise flux estimate。第一个诚实正类应固定有限 carrier pattern，并把临界点数、Morse margin 与 shape neighborhoods 写成显式参数。</p>
        </section>

        <section id="claims"><div class="section-no">12 / Claim boundary</div><h2>一般 Navier–Stokes 问题仍未解决</h2>
          <p>本节没有从 common-band assumptions 推出 full-superposition ED，没有证明 logarithmic one-carrier cubic、fixed-geometry arbitrary coupling、multiscale physical absorption、任意三维继续性、有限时奇性或全局光滑性。Clay 千禧年问题仍未解决。</p>
        </section>

        <section id="reproduce"><div class="section-no">13 / Reproduction</div><h2>报告、审计、证书与正式附图包</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072o_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072o_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072o_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072o_independent_audit.md">独立数学审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072o">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072o-physical-reinsertion/fig-r072o-physical-reinsertion">正式附图包</a> · <a href="/notes/r0-72o.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72o.html">累计回顾</a> · <a href="/recap-r0-61-r0-72o.pdf">累计回顾 PDF</a></p>
        </section>
      </article>"""


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72P</span><span class="tree-state current">下一检查点</span></div>
              <h3>full-superposition enhanced dissipation with explicit shape control</h3>
              <p>先固定有限 carrier pattern 与统一 Morse margin，证明完整叠加的 integrated enhanced dissipation 或 rowwise cubic flux estimate。</p>
            </article>'''


HOME_RECAP = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72O · 2026-08-27</p>
            <h3>R0.60 recap 之后的累计回顾收录 105 个节点；全站现有 165 篇公开研究笔记</h3>
            <p>累计回顾保持二十八个问题阶段，并给出 R0.61–R0.72O 的完整逐节点索引。R0.72O 把一载波 true cubic 严格回填物理账本，将 strong window 推进到 \(\varepsilon\lesssim R^{4/3}L_{R,\varepsilon}^2\)；多载波只在带统一常数的 full-superposition ED 假设下得到条件窗口。</p>
            <p>R0.70A–R0.72O 共 67 个版本已公开；43 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;一载波 growing-geometry payment 已闭合；fixed geometry 与 multi-carrier propagation 仍开放。</p>
            <p><a href="/recap-r0-61-r0-72o.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72o.pdf">下载同步 PDF</a></p>
          </div>'''


HOME_O_CARD = r'''          <div class="task-one" id="r072o" data-release="r072o" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72O · 2026-08-27</p>
            <h3>物理 numerator 是 \(\varepsilon^{11/6}\)；多载波需要完整传播定理</h3>
            <p>一载波 exact-root correction 后仍有 \(\mathcal C_\times\lesssim a^2\sqrt\varepsilon\)。物理回填给 \(U_{\rm ED}^{(1)}=\varepsilon^{11/6}\)，并将 paid window 推进到 \(\sqrt\varepsilon\lesssim R^{2/3}L_{R,\varepsilon}\)。</p>
            <p>若 full superposition 满足 integrated enhanced dissipation，且常数对比较的参数与几何族一致，则 \(U_{\rm ED}=\varepsilon^{11/6}p^{4/3}\)。common-band support 不能保证统一非退化临界点；逐载波求和还会遗漏真实 \(N^2\) cross cubics。</p>
            <p><strong>结论边界：</strong>&nbsp;conditional multi-carrier implication 不是无条件 superposition theorem；fixed-geometry arbitrary coupling 与一般三维正则性仍开放。</p>
            <p><a href="/notes/r0-72o.html"><strong>阅读 R0.72O 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72o.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072o/fig-r072o-physical-reinsertion.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072o">查看精确证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072o_report-source.md">查看完整数学报告</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072o_literature_audit.md">查看文献边界审计</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072o-physical-reinsertion/fig-r072o-physical-reinsertion">查看正式附图包</a> ·
              <a href="/recap-r0-61-r0-72o.html">阅读累计回顾</a> ·
              <a href="/recap-r0-61-r0-72o.pdf">下载累计回顾 PDF</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72P：</strong>&nbsp;在显式 uniform Morse margin 下证明 full-superposition gate。</p>
          </div>'''


def validate_inputs() -> None:
    for relative in (
        "research/r072o_report-source.md",
        "research/r072o_literature_audit.md",
        "research/r072o_gap_matrix.md",
        "research/r072o_independent_audit.md",
        "research/certificates/r072o/README.md",
        "research/certificates/r072o/SHA256SUMS",
        "research/certificates/r072o/crosscheck.json",
        "research/certificates/r072o/producer-config.json",
        "research/certificates/r072o/independent-config.json",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72O release input: {relative}")

    certificate = ROOT / "research/certificates/r072o"
    verify_flat_hash_ledger(certificate, "R0.72O certificate")
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if crosscheck.get("status") != "passed":
        raise RuntimeError("R0.72O certificate crosscheck is not passed")
    producer = json.loads((certificate / "producer-config.json").read_text(encoding="utf-8"))
    independent = json.loads((certificate / "independent-config.json").read_text(encoding="utf-8"))
    source_commit = producer.get("gitCommit")
    if (
        re.fullmatch(r"[0-9a-f]{40}", str(source_commit or "")) is None
        or independent.get("gitCommit") != source_commit
    ):
        raise RuntimeError("R0.72O dual audits do not record one full source commit")

    figure = (
        ROOT
        / "figures/r072o-physical-reinsertion/fig-r072o-physical-reinsertion"
    )
    for name in (
        "manifest.json",
        "SHA256SUMS",
        "validation.json",
        "figure.pdf",
        "figure.svg",
        "figure.png",
    ):
        if not (figure / name).is_file():
            raise RuntimeError(f"missing formal R0.72O figure artifact: {name}")
    verify_flat_hash_ledger(figure, "R0.72O figure")
    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    if (
        manifest.get("release") != "R0.72O"
        or manifest.get("figureId") != "fig-r072o-physical-reinsertion"
        or manifest.get("status") != "formal"
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
        or manifest.get("publication", {}).get("publicCopiesComplete") is not True
        or manifest.get("git", {}).get("sourceCommit") != source_commit
        or re.fullmatch(
            r"[0-9a-f]{40}",
            str(manifest.get("git", {}).get("certificateCommit") or ""),
        )
        is None
    ):
        raise RuntimeError("R0.72O figure manifest is not a lineage-complete formal seal")

    validator = ROOT / "research/validate_figure_package.py"
    if not validator.is_file():
        raise RuntimeError("missing strict figure-package validator")
    completed = subprocess.run(
        [sys.executable, str(validator), str(figure)],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            "R0.72O strict figure validation failed: "
            + (completed.stdout or completed.stderr).strip()
        )
    validation = json.loads(completed.stdout)
    if validation.get("errors") != []:
        raise RuntimeError(f"R0.72O strict figure errors: {validation['errors']}")

    publication = manifest["publication"]
    expected_public = []
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = ROOT / publication["directory"] / f"{publication['stem']}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72O public {suffix} is absent or not byte-identical")
        expected_public.append(str(public.relative_to(ROOT)))
    recorded_public = sorted(
        row.get("path") for row in publication.get("assets", []) if isinstance(row, dict)
    )
    if recorded_public != sorted(expected_public):
        raise RuntimeError("R0.72O figure manifest does not enumerate exact public assets")


def build_note() -> None:
    html = (PUBLIC / "notes" / "r0-72n.html").read_text(encoding="utf-8")
    replacements = [
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72O：一载波次线性 cubic 的物理回填、加倍的 strong window 与条件性的多载波接口。">', "description"),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72O｜物理回填与多载波传播门槛">', "og title"),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="物理 numerator ε^(11/6)、一载波 growing-geometry window 与 full-superposition enhanced-dissipation gate。">', "og description"),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072o/fig-r072o-physical-reinsertion.png">', "og image"),
        (r'<title>.*?</title>', '<title>R0.72O｜物理回填与多载波传播门槛</title>', "title"),
    ]
    for pattern, value, label in replacements:
        html = section(html, pattern, value, f"note {label}")
    html = required(html, "/i18n-en.js?v=1.27", "/i18n-en.js?v=1.28", "note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#identification">识别</a><a href="#reinsertion">回填</a><a href="#ledger">账本</a><a href="#window">窗口</a><a href="#fixed">固定几何</a><a href="#superposition">叠加</a><a href="#gate">交叉项</a><a href="#literature">文献边界</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#claims">边界</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · 直接判断</a></li><li><a href="#identification">01 · raw cubic 识别</a></li><li><a href="#reinsertion">02 · 物理回填</a></li><li><a href="#ledger">03 · 完整账本</a></li><li><a href="#window">04 · strong window</a></li><li><a href="#fixed">05 · fixed geometry</a></li><li><a href="#superposition">06 · full superposition</a></li><li><a href="#gate">07 · cross-term gate</a></li><li><a href="#literature">08 · 文献边界</a></li><li><a href="#figure">09 · 正式附图</a></li><li><a href="#value">10 · 研究价值</a></li><li><a href="#next">11 · R0.72P</a></li><li><a href="#claims">12 · 主张边界</a></li><li><a href="#reproduce">13 · 复现入口</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72O · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>', "note footer")
    assert_clean(html, "R0.72O note")
    (PUBLIC / "notes" / "r0-72o.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72n.html").read_text(encoding="utf-8")
    changes = [
        ("/i18n-en.js?v=1.27", "/i18n-en.js?v=1.28"),
        ("R0.61–R0.72N", "R0.61–R0.72O"),
        ("R0.61 到 R0.72N 的 104 个研究节点", "R0.61 到 R0.72O 的 105 个研究节点"),
        ("收录节点：104", "收录节点：105"),
        ("回顾截止时公开笔记：164", "回顾截止时公开笔记：165"),
        ("回顾截止节点：R0.72N", "回顾截止节点：R0.72O"),
        ("02 · 104 节完整索引", "02 · 105 节完整索引"),
        ("<strong>104</strong><span>R0.61–R0.72O 研究节点</span>", "<strong>105</strong><span>R0.61–R0.72O 研究节点</span>"),
        ("<strong>66</strong><span>R0.70A–R0.72N 已公开版本</span>", "<strong>67</strong><span>R0.70A–R0.72O 已公开版本</span>"),
        ("<strong>42</strong><span>当前 formal-figure 合同下完整封存</span>", "<strong>43</strong><span>当前 formal-figure 合同下完整封存</span>"),
        ("后面的 104 个节点", "后面的 105 个节点"),
        ("R0.70A–R0.72N 的 66 个版本已经公开；其中 42 个", "R0.70A–R0.72O 的 67 个版本已经公开；其中 43 个"),
        ("R0.61–R0.72O 的 104 节公开笔记", "R0.61–R0.72O 的 105 节公开笔记"),
        ("/recap-r0-61-r0-72n.pdf", "/recap-r0-61-r0-72o.pdf"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"recap {old}")
    html = section(html, r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72O 的 105 个研究节点；最新一节完成一载波物理回填并隔离多载波传播门槛。">', "recap description")
    html = section(html, r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="二十八个阶段、105 个节点：从约化递推到一载波 physical reinsertion 与 full-superposition gate。">', "recap og description")
    html = section(html, r'<title>.*?</title>', '<title>R0.61–R0.72O｜R0.60 之后的研究回顾</title>', "recap title")

    old_phase = r'''            <article class="phase"><h3>R0.72L–R0.72N · strong-coupling screen 与耗散决策</h3>
              <p>R0.72L 保留 actual \(K\) 与 \(x\)，R0.72M 把 scalar danger window 精确化。R0.72N 回到完整耗散一载波链，证明 \(K_\sigma\lesssim1+\sigma^{2/3}\) 而 \(x_\sigma\gtrsim\sigma^{4/3}\log\sigma\)，从而排除声明 launch 上的 action-poor route。</p>
              <p>Coble–He 的时变剪切 \(L^2\) 衰减经坐标投影和时间积分给本站 corollary \(\mathcal C_{\rm diss}\lesssim a^2\sqrt\sigma\)。logarithmic sharpen、多载波稳定性和物理账本回填仍开放。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/notes/r0-72m.html">R0.72M</a><a href="/notes/r0-72n.html">R0.72N</a><a href="/assets/r072n/fig-r072n-dissipative-carrier.pdf">R0.72N 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072n">R0.72N 证书</a></div></article>'''
    new_phase = r'''            <article class="phase"><h3>R0.72L–R0.72O · strong-coupling screen、耗散决策与物理回填</h3>
              <p>R0.72L 保留 actual \(K\) 与 \(x\)，R0.72M 精确化 danger window，R0.72N 在完整耗散链上排除 action-poor route 并得到一载波 \(O(a^2\sqrt\varepsilon)\) cubic。</p>
              <p>R0.72O 将该 cubic 严格回填 normalized physical ledger，得到 \(U_{\rm ED}^{(1)}=\varepsilon^{11/6}\) 和 \(\varepsilon\lesssim R^{4/3}L_{R,\varepsilon}^2\) 的 growing-geometry window。多载波公式只在 full-superposition integrated ED 及其统一常数假设下成立；common-band support 不能自动保证统一 Morse margin。</p>
              <div class="links"><a href="/notes/r0-72l.html">R0.72L</a><a href="/notes/r0-72m.html">R0.72M</a><a href="/notes/r0-72n.html">R0.72N</a><a href="/notes/r0-72o.html">R0.72O</a><a href="/assets/r072o/fig-r072o-physical-reinsertion.pdf">R0.72O 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072o">R0.72O 证书</a></div></article>'''
    html = once(html, old_phase, new_phase, "recap O phase")
    node_n = '            <span class="node-ref"><a href="/notes/r0-72n.html">R0.72N</a><span class="node-state kind-closed">闭</span></span>\n'
    node_o = '            <span class="node-ref"><a href="/notes/r0-72o.html">R0.72O</a><span class="node-state kind-conditional">条件</span></span>\n'
    html = once(html, node_n, node_n + node_o, "recap O node")
    retained_o = r'''            <li>R0.72O 的 physical-reinsertion theorem：exact-root correction 后 \(\mathcal C_\times\lesssim a^2\sqrt\varepsilon\)；物理 numerator 为 \(\varepsilon^{11/6}\)，一载波 paid window 为 \(\sqrt\varepsilon\lesssim R^{2/3}L_{R,\varepsilon}\)。多载波只有在带统一常数的 full-superposition integrated ED 下得到条件推广；逐载波求和与 common-band support 都不足。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained_o + "          </ul>\n          <p>这些结果可以分别整理成", "recap retained O")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>一载波物理回填完成，多载波缺口已经变成明确传播命题</h2>
          <p>截至 R0.72O，没有新的无条件继续性判据，没有缩小所有潜在奇性解的集合，也没有证明有限时破裂。不能把 105 个节点或 67 个公开版本解释成对千禧年问题完成了某个比例。</p>
          <p>新的严格结果是 \(\varepsilon^{11/6}\) physical numerator、加倍的 growing-geometry strong window，以及带统一常数的 full-superposition ED 对多载波 cubic 的条件蕴含。</p>
          <p>组合剪切可能出现退化临界点；因此下一步必须显式控制 Morse margin 或直接证明 rowwise flux，不能把 one-carrier theorem 逐模相加。</p>
        </section>''', "recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72P 直接处理 full-superposition gate</h2>
          <p>先固定有限 carrier pattern，给临界点数、Morse margin 与 shape neighborhoods 统一参数，证明 integrated enhanced dissipation。</p>
          <p>若完整半群过强，则直接证明足够闭合物理账本的 rowwise cubic flux estimate。</p>
        </section>''', "recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2>
          <p>R0.70A–R0.72O 的 67 节 HTML/PDF 与研究源稿列入公开路线。按当前 formal-figure 合同，43 节完整封存；24 节较早版本仍列入可审计的旧档回补清单。</p>
          <p>R0.72O 的无条件部分只覆盖声明的一载波 exact-corrected triangular family。多载波公式明确依赖常数对参数与几何族一致的 full-superposition ED；限定检索没有找到可替代该 gate 的 black-box theorem，Clay 正式问题仍然开放。</p>
        </section>''', "recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2>
          <p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72n.html">保留 R0.72N 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72o.html">打开最新节点 R0.72O</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072o">查看 R0.72O 精确证书</a> · <a href="/assets/r072o/fig-r072o-physical-reinsertion.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72o.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-72n.pdf">上一版累计回顾 PDF</a></p>
          <p>完整节点索引保留 R0.69W、R0.70A 以后每个公开版本及其原始编号；状态标签只描述证据类型。</p>
        </section>''', "recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72O 回顾 · 2026-08-27<br><a href="/">返回研究主页</a></div></footer>', "recap footer")

    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 105 or len(set(links)) != 105:
        raise RuntimeError(f"recap node index: expected 105 unique links, got {len(links)}/{len(set(links))}")
    expected = ["r0-69w"]
    expected += [f"r0-70{chr(code)}" for code in range(ord("a"), ord("z") + 1)]
    expected += [f"r0-71{chr(code)}" for code in range(ord("a"), ord("z") + 1)]
    expected += [f"r0-72{chr(code)}" for code in range(ord("a"), ord("o") + 1)]
    missing = [slug for slug in expected if slug not in links]
    if missing:
        raise RuntimeError(f"recap node index missing required releases: {missing}")
    assert_clean(html, "R0.72O recap")
    (PUBLIC / "recap-r0-61-r0-72o.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    changes = [
        ('data-site-version="1.27"', 'data-site-version="1.28"'),
        ("/i18n-en.js?v=1.27", "/i18n-en.js?v=1.28"),
        ("/site-refresh.js?v=1.27", "/site-refresh.js?v=1.28"),
        ("<strong>v1.27</strong>网页版本", "<strong>v1.28</strong>网页版本"),
        ("<strong>164</strong>公开研究笔记", "<strong>165</strong>公开研究笔记"),
        ("<strong>R0.72N</strong>最新研究节点", "<strong>R0.72O</strong>最新研究节点"),
        ("<strong>one-carrier physical reinsertion and multi-carrier stability</strong>当前方向", "<strong>full-superposition enhanced dissipation with shape control</strong>当前方向"),
        ("Research topology · R0.1–R0.72N", "Research topology · R0.1–R0.72O"),
        ("R0.70A–R0.72N：66 节已公开，42 节完整封存", "R0.70A–R0.72O：67 节已公开，43 节完整封存"),
        ("<span class=\"route-range\">R0.69P–R0.72N</span>", "<span class=\"route-range\">R0.69P–R0.72O</span>"),
        ('aria-label="R0.69P–R0.72N"', 'aria-label="R0.69P–R0.72O"'),
        ("展开 74 篇公开笔记", "展开 75 篇公开笔记"),
        ("综述 v1.27 · 2026-08-27", "综述 v1.28 · 2026-08-27"),
        ("上次综述 v1.26 · 2026-08-27", "上次综述 v1.27 · 2026-08-27"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"home {old}")
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', r'<div class="summary-item"><strong>我目前关注</strong><span>R0.72O 已把一载波 enhanced-dissipation cubic 回填物理账本，并得到 \(\varepsilon\lesssim R^{4/3}L_{R,\varepsilon}^2\) 的 growing-geometry window；下一关是带显式 shape control 的 full-superposition propagation。</span></div>', "home summary")
    html = once(html, "从 exact action screen 走到 dissipative one-carrier decision", "从 dissipative one-carrier decision 走到 physical reinsertion", "home route title")
    old_end = r'''R0.72N 回到耗散链，证明 action-poor route 对声明 launch 失效；再把 Coble–He 的时变剪切衰减转成本站的 \(O(a^2\sqrt\sigma)\) cubic corollary。</p>'''
    new_end = r'''R0.72N 回到耗散链，证明 action-poor route 对声明 launch 失效；再把 Coble–He 的时变剪切衰减转成本站的 \(O(a^2\sqrt\sigma)\) cubic corollary。R0.72O 将该结果回填 normalized physical ledger，得到 \(\varepsilon^{11/6}\) numerator 与加倍的 growing-geometry window，并把多载波问题隔离为 full-superposition ED gate。</p>'''
    html = once(html, old_end, new_end, "home route O prose")
    html = once(html, "→ dissipative one-carrier decision → physical reinsertion and multi-carrier gate</p>", "→ dissipative one-carrier decision → physical reinsertion → full-superposition ED gate</p>", "home path O")
    nav_n = '                  <a class="milestone" href="/notes/r0-72n.html">R0.72N</a>\n'
    html = once(html, nav_n, nav_n + '                  <a class="milestone" href="/notes/r0-72o.html">R0.72O</a>\n', "home O route link")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "home next")
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', HOME_RECAP, "home recap")
    old_tail = r'''            <p><strong style="color:var(--gold)">下一步 R0.72O：</strong>&nbsp;回填 normalized physical ledger，并检查多载波 cross terms。</p>
          </div>
        </section>'''
    new_tail = r'''            <p><strong style="color:var(--gold)">R0.72O 已完成：</strong>&nbsp;一载波 physical reinsertion 与 growing-geometry strong window 已闭合；full-superposition propagation 保持开放。</p>
          </div>

''' + HOME_O_CARD + r'''
        </section>'''
    html = once(html, old_tail, new_tail, "home O card")
    html = required(html, "/recap-r0-61-r0-72n.html", "/recap-r0-61-r0-72o.html", "home recap HTML endpoint")
    html = required(html, "/recap-r0-61-r0-72n.pdf", "/recap-r0-61-r0-72o.pdf", "home recap PDF endpoint")
    assert_clean(html, "R0.72O home")
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    changes = [
        ("/i18n-en.js?v=1.27", "/i18n-en.js?v=1.28"),
        ("文献综述 v1.27 · 2026-08-27", "文献综述 v1.28 · 2026-08-27"),
        ("本站 R0.69P–R0.72N 只列为研究笔记", "本站 R0.69P–R0.72O 只列为研究笔记"),
        ("累计回顾与 104 节索引", "累计回顾与 105 节索引"),
        ("打开 104 节完整索引", "打开 105 节完整索引"),
        ("/recap-r0-61-r0-72n.html", "/recap-r0-61-r0-72o.html"),
    ]
    for old, new in changes:
        html = required(html, old, new, f"literature {old}")
    old_route = r'''R0.72N 在完整耗散链上排除声明 launch 的 action-poor route，并由 Coble–He 时变剪切衰减推出本站 corollary \(\mathcal C_{\rm diss}\lesssim a^2\sqrt\sigma\)；logarithmic rate 与多载波仍开放。一般 Navier–Stokes 正则性仍开放。</p>'''
    new_route = r'''R0.72N 在完整耗散链上排除声明 launch 的 action-poor route，并由 Coble–He 时变剪切衰减推出本站 corollary \(\mathcal C_{\rm diss}\lesssim a^2\sqrt\sigma\)。R0.72O 将该 cubic 回填物理账本，得到 \(\varepsilon^{11/6}\) numerator 与 \(R^{4/3}L_{R,\varepsilon}^2\) window；多载波只在带统一常数的 full-superposition ED 假设下条件成立。一般 Navier–Stokes 正则性仍开放。</p>'''
    html = once(html, old_route, new_route, "literature O route")
    old_open = r'''              <div class="route-step pause"><header><b>开放接口 · R0.72O</b><strong>physical reinsertion and multi-carrier stability</strong></header><p>把一载波次线性 cubic 回填 normalized physical ledger，并检查多载波 cross terms 是否保留 \(\sigma^{1/2}\) 增益。</p></div>'''
    new_open = r'''              <div class="route-step closed"><header><b>R0.72O</b><strong>physical reinsertion and conditional superposition interface</strong></header><p>一载波 physical numerator 为 \(\varepsilon^{11/6}\)，growing-geometry window 推进到 \(\sqrt\varepsilon\lesssim R^{2/3}L_{R,\varepsilon}\)；多载波公式依赖常数对比较族一致的 full-superposition ED。<a href="/notes/r0-72o.html">研究笔记</a> <a href="/recap-r0-61-r0-72o.html">当前累计回顾</a> <a href="#r072o-boundary">方法边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72P</b><strong>full-superposition ED with explicit shape control</strong></header><p>在固定有限 carrier pattern 与 uniform Morse margin 下证明 integrated ED，或直接证明 rowwise cubic flux estimate。</p></div>'''
    html = once(html, old_open, new_open, "literature O cards")
    n_boundary = r'''          <div class="boundary"><strong>R0.72N 的主张边界</strong><p>action-poor no-go 只覆盖声明的 fixed-band、row-aligned、one-carrier launch；\(O(a^2\log\sigma)\) 仍是有限诊断支持的开放 sharpen。matching asymptotic、多载波、multiscale physical absorption 和一般三维继续性均未闭合；限定检索不构成新颖性或优先权证明。</p></div>'''
    o_boundary = r'''

          <h3 id="r072o-boundary">R0.72O 的物理回填与多载波文献边界</h3>
          <p><a href="https://arxiv.org/html/2309.15738">Coble–He, Theorem 1.2</a> 的常数在统一非退化 shape parameters 下不依赖 \(\nu\) 与 horizontal mode。本站一载波 profile 直接核对这些参数，再把 semigroup decay 转成 corrected cubic 和 physical ledger；后两步不是原论文定理。</p>
          <p><a href="https://doi.org/10.1112/jlms.12782">Coti Zelati–Gallay</a> 说明 stationary-shear exponent 随临界点退化阶改变。Couette 与 Kolmogorov 的 nonlinear thresholds 是 flow-specific 方法先例，不是当前 common-band class 的 black-box theorem。</p>
          <div class="boundary"><strong>R0.72O 的主张边界</strong><p>线性 horizontal solution modes 可在同一 \(x\)-independent shear 下用 Parseval 叠加；这里的多个 carriers 进入 shear coefficient 与 cubic cross terms，不能逐载波 tensorize。common-band support 不能保证组合 shear 的 uniform Morse margin。多载波窗口明确依赖常数对参数与几何族一致的 full-superposition ED；限定检索不构成新颖性或优先权证明。</p></div>'''
    html = once(html, n_boundary, n_boundary + o_boundary, "literature O boundary")
    assert_clean(html, "R0.72O literature")
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    note_count = len(list((PUBLIC / "notes").glob("*.html")))
    if note_count != 165:
        raise RuntimeError(f"expected 165 public HTML notes, found {note_count}")
    release_path = ROOT / "research" / "release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    release.update({
        "latestCompletedRelease": "r072o", "siteVersion": "1.28",
        "publicHtmlNoteCount": note_count, "postR060RecapNodeCount": 105,
        "nextRelease": "r072p", "latestReleaseGate": "tests/r072o-physical-reinsertion-gate.test.mjs",
        "postR070APublishedReleaseCount": 67, "postR070AFormalSealedReleaseCount": 43,
        "legacyFormalFigureBacklogCount": 24,
    })
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    site.update({"version": "1.28", "latestRelease": "R0.72O", "publicHtmlNoteCount": note_count, "publishedDate": "2026-08-27"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research" / "formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    inventory.update({"latestPublishedRelease": "r072o", "publishedReleaseCount": 67, "formalSealedReleaseCount": 43, "legacyFormalFigureBacklogCount": 24})
    for key in ("publishedReleases", "formalSealedReleases"):
        if "r072o" not in inventory[key]:
            inventory[key].append("r072o")
    if len(inventory["legacyFormalFigureBacklog"]) != 24:
        raise RuntimeError("legacy formal-figure backlog changed unexpectedly")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ("research-review.html", "literature-review.html", "notes/r0-72o.html", "recap-r0-61-r0-72o.html"):
        assert_clean((PUBLIC / relative).read_text(encoding="utf-8"), relative)
    print(json.dumps({
        "release": "R0.72O", "siteVersion": "1.28", "notes": 165,
        "recapNodes": 105, "published": 67, "formalSealed": 43,
        "legacyBacklog": 24, "phases": 28, "next": "R0.72P",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
