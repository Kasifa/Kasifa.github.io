#!/usr/bin/env python3
"""Publish the queued R0.74B--R0.74F note-only releases.

This script consumes frozen research artifacts without editing them.  It owns
only the complete Chinese reader-facing notes, figure mirrors, route/index
accounting and release metadata.  The R0.73X recap stays byte-identical.
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
SITE_VERSION = PUBLIC / "site-version.json"
MANIFEST = ROOT / "research/release-manifest.json"
INVENTORY = ROOT / "research/formal-archive-inventory.json"
RECAP_HTML = PUBLIC / "recap-r0-61-r0-73x.html"
RECAP_PDF = PUBLIC / "recap-r0-61-r0-73x.pdf"
RECAP_HASHES = {
    RECAP_HTML: "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776",
    RECAP_PDF: "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa",
}
VERSION = "1.72"


@dataclass(frozen=True)
class Release:
    code: str
    slug: str
    title: str
    subtitle: str
    figure_dir: str
    figure_slug: str
    status_lines: tuple[str, ...]
    sections: tuple[tuple[str, str, str], ...]
    evidence_links: tuple[tuple[str, str], ...]
    card: str
    next_gate: str
    literature_boundary: str


def eq(value: str) -> str:
    return f'<div class="equation">\\[{value}\\]</div>'


RELEASES = (
    Release(
        code="R0.74B",
        slug="r074b",
        title="R0.74B｜缓冲环带闭合：Gaussian 外部尾项由倍半径付款",
        subtitle="原权重保留不变；严格更早的时间层和 2R 外部账本闭合正尺度尾项",
        figure_dir="fig-r074b-buffered-tail-closure",
        figure_slug="fig-r074b-buffered-tail-closure",
        status_lines=(
            "缓冲 Caccioppoli 估计：PROVED",
            "有限证书与图件：FINITE",
            "大付款纯 2/3 次闭合：OPEN",
            "不构成 Clay 问题解答：NOT CLAY",
        ),
        sections=(
            ("01", "冻结对象与适用范围", r"""
<p>本节处理 R0.74A 留下的两个二次外部尾项。对标准时间钟和黏度时间钟分别令</p>
<div class="equation">\[\kappa_{\rm std}=1,\quad \kappa_\nu=\nu,\qquad
I_\rho^\square=(t_0-\rho^2/\kappa_\square,t_0).\]</div>
<p>假设 \(0&lt;R&lt;\pi/16\)、\(0&lt;\theta\le1\)、\(I_{8R}^\square\Subset(0,T)\)，并取周期 suitable weak solution。所有比较都在同一时间钟内完成；半径 \(8R\) 的局部能量支付半径 \(2R\) 压力分解产生的内区项。</p>
<div class="equation">\[\mathcal U_{\rm ext}^{\infty,\square}
=\mathop{\rm ess\,sup}_{I_R^\square}R^{-1}U_\gamma(t),\qquad
\mathcal D_{\rm ext}^{\square}
=\nu R^{-1}\int_{I_R^\square}G_\gamma(t)\,dt.\]</div>
<p>结论是正尺度 size estimate，不是零尺度正则性判据。</p>"""),
            ("02", "倍半径移位为什么消除权重损失", r"""
<p>关键不是把相邻 Gaussian 权重粗暴比较，而是使用精确环带恒等式</p>
<div class="equation">\[A_k(R)=A_{k-1}(2R),\qquad k\ge2.\]</div>
<p>目标半径 \(R\) 的外移邻居在半径 \(2R\) 处保留同一权重；内移邻居获得更大的权重。前两个环带单独落入 \(B_{4R}\) 和最内层 \(2R\) 环带，因此作为 core 行显式保留。固定半径下错误使用 \(\gamma_m\lesssim\gamma_{m+1}\) 会造成超指数损失。</p>"""),
            ("03", "suitable local energy 的加权求和", r"""
<p>我在每个提升环带上放置非负 cutoff，并在 \(I_{2R}^\square\) 左端加入严格时间缓冲。先对有限个环带应用 suitable local energy inequality，再乘 \(\gamma_m/R\) 求和，最后用单调收敛取极限。压力常数由无散条件严格消失，局部压力、谐和压力、前两个内壳和所有周期复制项均显式计入。</p>
<p>二次 cutoff 行由加权 Hölder 和 \(\mathcal E(z_0,8R)\) 支付；三次速度/压力 flux 行由 \(\mathcal A_{\rm ext}(z_0,2R;\theta)\) 支付。证明不调用时间端点值。</p>"""),
            ("04", "缓冲尾项主定理", r"""
<p>定义完整的大半径付款</p>
<div class="equation">\[P^\square=\mathcal E^\square(z_0,8R)^{3/2}
+\mathcal A_{\rm ext}^\square(z_0,2R;\theta).\]</div>
<p><strong>PROVED。</strong>对两种时间钟分别有</p>
<div class="equation">\[\mathcal U_{\rm ext}^{\infty,\square}
+\mathcal D_{\rm ext}^{\square}
\le C_{\nu,\square}\big[(P^\square)^{2/3}+P^\square\big].\]</div>
<p>把它代回 R0.74A 的四块分解得到</p>
<div class="equation">\[\mathcal K_D^\square
\le C_{\nu,\square}\theta^{1/4}
\big[P^\square+(P^\square)^{3/2}\big].\]</div>
<p>当 \(P^\square\le1\) 时，二次尾由 \(C(P^\square)^{2/3}\) 控制，\(\mathcal K_D^\square\le C\theta^{1/4}P^\square\)。这仍只是小付款 size corollary，并未证明吸收。</p>"""),
            ("05", "压力界面也随倍半径移动", r"""
<p>压力 gauge 在半径 \(R\) 与 \(2R\) 处不能被默认视为相同。局部 Calderón--Zygmund、谐和压力估计和 Jensen 不等式共同给出 gauge difference 的显式付款。由此得到</p>
<div class="equation">\[\mathcal A_{\rm ext}^\square(z_0,R;\theta)
\le C_{\nu,\square}P^\square.\]</div>
<p>因此 R0.74A 的 compact-cutoff 压力行与 \(\mathcal K_D\) 可由同一个 \(P^\square+(P^\square)^{3/2}\) 支付。这里没有把 pressure nonlocality 藏入“低阶误差”。</p>"""),
            ("06", "同一时间窗的不可行性结论", r"""
<p>精确耗散 shear</p>
<div class="equation">\[u_N(t,x)=A e^{-\nu N^2(t-t_-)}\sin(Nx_2)e_1,\qquad p_N=0\]</div>
<p>满足 \(\mathcal U_{\rm ext}^{\infty}\asymp A^2\)、\(\mathcal D_{\rm ext}\asymp A^2\)，而同窗积分三次付款是 \(O(A^3N^{-2})\)。所以只用同一时间窗的三次账本，不能以频率无关常数控制二次端点。这里的“不可行性”只排除这一条明确估计；它不排除所有缓冲、入口二次付款或其他结构。</p>"""),
            ("07", "证据分层与文献边界", """
<p><strong>PROVED：</strong>倍半径权重移位、两种时间钟的严格缓冲、局部能量求和、压力 gauge 转移、尾项闭合与同窗三次付款反例均为解析证明。</p>
<p><strong>FINITE：</strong>固定正尺度下各尾有限；有限算术证书和期刊图只复算常数、索引与公式，不承担 suitable-weak PDE 证明。</p>
<p><strong>BOUNDED LITERATURE AUDIT：</strong>局部能量、压力分解和 Gaussian 热核估计都有经典先例；限定检索不构成原创性或优先权证明。</p>"""),
            ("08", "仍然开放", """
<ul><li>对任意大付款删除主估计中的 \(+P\)；</li><li>付款的尺度一致小性、吸收、弱稳定与下半连续性；</li><li>quotient 后的下界、epsilon regularity 与任意三维正则性。</li></ul>
<p><strong>NOT CLAY：</strong>本节不证明奇点不存在，也不构造奇点；它不构成 Clay 千禧年问题的解答或部分解答。</p>"""),
        ),
        evidence_links=(
            ("规范解析证明", "research/r074b_buffered_tail_closure.md"),
            ("独立解析审计", "research/r074b_independent_audit.md"),
            ("一手文献边界", "research/r074b_primary_literature_audit.md"),
            ("有限证书报告", "research/r074b_buffered_tail_certificate_report.md"),
            ("机器可读证书", "research/r074b_buffered_tail_certificate.json"),
            ("证书脚本", "scripts/r074b_buffered_tail_certificate.py"),
        ),
        card="倍半径环带与严格更早时间层闭合了 Gaussian 二次外部尾；任意大付款仍保留 \(+P\)，同窗三次付款单独不足。",
        next_gate="构造或排除固定中心大付款端点；先检查运输造成的瞬时外环带质量。",
        literature_boundary="经典 local energy、pressure splitting 与 heat-kernel 工具分别归入既有文献；组合检索仅为有界 non-hit，不作新颖性或优先权声明。",
    ),
    Release(
        code="R0.74C",
        slug="r074c",
        title="R0.74C｜平流剪切阻断固定中心的大付款端点",
        subtitle="精确光滑周期 NSE 解族使固定中心的纯 2/3 次付款比无界",
        figure_dir="fig-r074c-advected-shear-obstruction",
        figure_slug="fig-r074c-advected-shear-obstruction",
        status_lines=(
            "固定中心端点反例：PROVED",
            "有限指数账本：FINITE",
            "随流/均值修复：OPEN",
            "不构成 Clay 问题解答：NOT CLAY",
        ),
        sections=(
            ("01", "冻结问题与结论", r"""
<p>本节只测试 R0.74B 的固定中心、大付款纯 \(2/3\) 次估计。固定 \(\nu=\theta=1\)，令 \(t_0=65R^2\)，并保留</p>
<div class="equation">\[X_R=\mathcal U_{\rm ext}^{\infty}+\mathcal D_{\rm ext},\qquad
P_R=\mathcal E(z_0,8R)^{3/2}+\mathcal A_{\rm ext}(z_0,2R;1).\]</div>
<p><strong>PROVED。</strong></p>
<div class="equation">\[\sup_{0<R<\pi/16,\ (u,p)\ {\rm smooth\ periodic\ NSE}}
\frac{X_R}{P_R^{2/3}}=\infty.\]</div>
<p>所以 R0.74B 中的 \(+P\) 不能直接删除。该结论没有判断 \(+P\) 是否最优，也没有处理随流坐标。</p>"""),
            ("02", "精确平流 shear 解族", r"""
<p>令 \(K_\tau^{\rm per}\) 为一维周期热核，\(M_m=3\,2^{m-1}\)，\(q_m=M_mR\)，并取</p>
<div class="equation">\[F_R(t,x_2)=R^2\partial_2K_{t+R^2}^{\rm per}(x_2-q(t)),
\qquad u=A F_R e_1+V_me_2,\qquad p=0.\]</div>
<p>由于 \(\partial_tF_R+V_m\partial_2F_R=\partial_2^2F_R\)，该场是完整时间区间上的精确、光滑、无外力周期 NSE 解。shear 分量空间均值为零。自由参数 \(A\) 属于这一正交 shear 子类，不是对任意 NSE 解做非法振幅缩放。</p>"""),
            ("03", "终端外环带的下界", r"""
<p>最终热核条带在正时间区间内穿过目标环带。中心核在一段长度为 \(cR/|V_m|\asymp R^3\) 的时间内保持统一点态下界；横向截面给出正测度。原始权重为 \(e^{-M_m^2/288}\)，因此</p>
<div class="equation">\[\mathcal U_{\rm ext}^{\infty}
\ge cA^2M_m^2R^2e^{-M_m^2/288}.\]</div>
<p>这里使用 essential supremum，不依赖单一终端时刻。</p>"""),
            ("04", "完整付款账本", r"""
<p>早期局部球只看见 Gaussian 泄漏和常速背景。所有周期复制、局部压力 gauge、谐和压力和混合 \(A\)-\(V_m\) 项都被保留。统一上界为</p>
<div class="equation">\[P_R^{2/3}\le C\left[
R^{-2}+A^2R^2\Pi_m e^{-M_m^2/264}
+A^2R^{8/3}M_m^{-2/3}\right],\qquad \Pi_m=(1+M_m)^8.\]</div>
<p>严格指数差 \(1/264-1/288=1/3168\) 是局部泄漏与终端条带分离的关键。</p>"""),
            ("05", "三条比值同时发散", r"""
<p>选择</p>
<div class="equation">\[R_m=e^{-M_m^2/96},\qquad
\mathfrak a_m=R_m^{-2}e^{M_m^2/576}.\]</div>
<p>目标下界分别压过背景行、局部 Gaussian 泄漏行和外部三次行，因而</p>
<div class="equation">\[\frac{X_{R_m}}{P_{R_m}^{2/3}}\longrightarrow\infty.\]</div>
<p>机制是短驻留时间的 endpoint transport：大常速把更强的正交 shear 穿过固定观察环带，而早期核心只看见远处热尾。</p>"""),
            ("06", "结论只针对固定中心", """
<p>该解族的常速背景可以被 Galilean 移动消去。若所有球和环带随全局均值移动，当前反例退化为不平流的耗散条带。因此，本节只排除冻结的 fixed-centre endpoint；均值减除、随流中心或显式入口 flux 的修复仍需单独证明。</p>"""),
            ("07", "证据与文献边界", """
<p><strong>PROVED：</strong>精确 NSE 解、热核上下界、全周期复制、压力 gauge、完整付款和三比值发散均为解析证明。</p>
<p><strong>FINITE：</strong>每个序列成员能量和付款有限；有限证书只核对指数、阈值和算术。</p>
<p><strong>BOUNDED LITERATURE AUDIT：</strong>平流 shear、周期热核、Galilean 变换和压力分解均有直接先例；限定检索不是新颖性证明。</p>"""),
            ("08", "开放边界", """
<ul><li>固定中心估计中大付款的最优替代指数；</li><li>随均值移动后的纯 \(P^{2/3}\) 闭合；</li><li>外部尾的弱稳定、吸收和 epsilon regularity。</li></ul>
<p><strong>NOT CLAY：</strong>这是一个正尺度估计的反例，不是 blow-up 解，也不是一般三维全局正则性结论。</p>"""),
        ),
        evidence_links=(
            ("规范解析证明", "research/r074c_advected_shear_large_payment_obstruction.md"),
            ("独立解析审计", "research/r074c_independent_audit.md"),
            ("一手文献边界", "research/r074c_primary_literature_audit.md"),
            ("有限证书报告", "research/r074c_advected_shear_certificate_report.md"),
            ("机器可读证书", "research/r074c_advected_shear_certificate.json"),
            ("证书脚本", "scripts/r074c_advected_shear_certificate.py"),
        ),
        card="一个精确平流 shear 解族使固定中心 \(X_R/P_R^{2/3}\) 无界；它只排除固定中心端点，随流或均值修复仍开放。",
        next_gate="先减去全局均值并移动观察中心，检查局部 coherent transport 是否仍能穿过外环带。",
        literature_boundary="周期热核、advected shear、Galilean 变换与 local pressure splitting 都有直接先例；本节不作 first/novel/priority 表述。",
    ),
    Release(
        code="R0.74D",
        slug="r074d",
        title="R0.74D｜零总均值仍不能修复固定中心运输缺口",
        subtitle="局部 coherent transport 穿过全局均值/Galilean 修复，Version-A 比值仍无界",
        figure_dir="fig-r074d-zero-mean-local-transport-obstruction",
        figure_slug="fig-r074d-zero-mean-local-transport-obstruction",
        status_lines=(
            "零均值运输障碍：PROVED",
            "有限证书 111/111：FINITE",
            "局部随流坐标：OPEN",
            "不构成 Clay 问题解答：NOT CLAY",
        ),
        sections=(
            ("01", "Version-A 问题", r"""
<p>R0.74C 的常速背景可被全局 Galilean 变换消去。本节因此冻结更强的 Version-A：先减去全局空间均值，再按该常数移动中心。令</p>
<div class="equation">\[X_R^A=\mathcal U_{\rm ext}^{\infty,A}+\mathcal D_{\rm ext}^{A},\qquad
P_R^A=\mathcal E^A(z_0,8R)^{3/2}+\mathcal A_{\rm ext}^{A}(z_0,2R;1).\]</div>
<p><strong>PROVED。</strong></p>
<div class="equation">\[\sup_{0<R<\pi/16,\ (u,p)\ {\rm smooth\ periodic\ NSE},\ \bar u=0}
\frac{X_R^A}{(P_R^A)^{2/3}}=\infty.\]</div>
"""),
            ("02", "零总均值精确见证", r"""
<p>见证是光滑周期 2D3C 解</p>
<div class="equation">\[u(t,x)=\bigl(AF(t,x_2,x_3),\ B_Re^{-t}\cos x_3,\ 0\bigr),\qquad p=0,\]</div>
<div class="equation">\[\partial_tF+B_Re^{-t}\cos x_3\,\partial_2F
=(\partial_2^2+\partial_3^2)F.\]</div>
<p>两个速度分量的全局空间均值都严格为零，所以 Version-A 的均值减除与常量平移在该族上就是恒等操作。障碍来自局部相干运输，不是隐藏的常速漂移。</p>"""),
            ("03", "终端目标与参数序列", r"""
<p>取</p>
<div class="equation">\[M_m=3\,2^{m-1},\qquad R_m=e^{-M_m^2/96},\qquad
\mathfrak a_m=R_m^{-2}e^{M_m^2/576}.\]</div>
<p>正确时间序的 Feynman--Kac 表示给出目标存活；残余位移的符号产生单边 Gaussian 泄漏，另一侧由全局 \(L^2/L^3\) 收缩支付。目标下界为</p>
<div class="equation">\[L_m=c\mathfrak a_m^2M_mR_m^2e^{-M_m^2/288}=cM_mR_m^{-2}.\]</div>
"""),
            ("04", "三行付款同时被压过", r"""
<p>完整付款保持背景、局部泄漏和谐和外部三行。严格指数差仍为</p>
<div class="equation">\[\frac1{264}-\frac1{288}=\frac1{3168}>0.\]</div>
<p>目标分别相对 \(R_m^{-2}\)、\(\mathfrak a_m^2R_m^2\Pi_m e^{-M_m^2/264}\) 与 \(\mathfrak a_m^2R_m^{8/3}M_m^{-4/3}\) 发散，从而证明 Version-A 比值无界。</p>"""),
            ("05", "这一结论排除了什么", """
<p>全局均值减除只处理常量漂移；它不能跟踪尺度相关的局部速度。本节因此排除“只减常数均值并作常量 Galilean 平移即可恢复纯大付款端点”这一明确方案。它不排除局部平均、mollified trajectory、skewed cylinder 或显式入口 flux。</p>"""),
            ("06", "有限证书的严格边界", """
<p><strong>FINITE：</strong>确定性证书报告 111/111 PASS；独立有限审计核对参数恒等式、指数差、三比值签名和一个有限可行性见证。它不证明随机表示、Gaussian 泄漏、Calderón--Zygmund/Jensen、无穷极限或任何 Clay 结论。</p>
<p>期刊图 validator 为 40/40 PASS；图是解析账本示意，不是 DNS、仿真或数值证明。</p>"""),
            ("07", "有界文献审计", """
<p><strong>BOUNDED LITERATURE AUDIT：</strong>2D3C/passive-scalar 子类、衰减正弦 shear、torus mean 的 Galilean 去除、mollified trajectories、flow-following cylinders 和 harmonic pressure splitting 均有直接先例。限定检索未找到完整定量组合，但这不是新颖性或优先权证明。</p>"""),
            ("08", "开放边界", """
<ul><li>跟随局部或 mollified velocity 的 cylinder；</li><li>尺度依赖局部均值减除与保留 signed entrance flux 的估计；</li><li>transport-aware 大付款修复、吸收和 epsilon regularity。</li></ul>
<p><strong>NOT CLAY：</strong>见证位于经典全局光滑 2D3C 子空间；本节没有 blow-up、奇点或一般三维定理。</p>"""),
        ),
        evidence_links=(
            ("问题门", "research/r074d_zero_mean_local_transport_gate.md"),
            ("规范解析证明", "research/r074d_zero_mean_local_transport_obstruction.md"),
            ("独立解析审计", "research/r074d_independent_audit.md"),
            ("独立有限审计", "research/r074d_finite_certificate_independent_audit.md"),
            ("一手文献边界", "research/r074d_primary_literature_audit.md"),
            ("有限证书报告", "research/r074d_zero_mean_transport_certificate_report.md"),
            ("机器可读证书", "research/r074d_zero_mean_transport_certificate.json"),
        ),
        card="精确零总均值 2D3C 解族仍使 Version-A 比值无界；常量均值/Galilean 修复不足，下一步必须进入局部随流坐标。",
        next_gate="严格写出局部 mollified trajectory 的移动/减法方程，并检查旧反例是否被新付款吸收。",
        literature_boundary="2D3C、time-dependent shear、Galilean mean removal、mollified trajectories 与 pressure splitting 均有 prior art；bounded non-hit 不是 novelty proof。",
    ),
    Release(
        code="R0.74E",
        slug="r074e",
        title="R0.74E｜局部随流坐标：旧反例被支付，外环新门槛通过",
        subtitle="局部 frame 代数闭合；旧 R0.74D 族被中和；新奇对称双流只通过有限指数关",
        figure_dir="fig-r074e-outer-annulus-frame-gate",
        figure_slug="fig-r074e-outer-annulus-frame-gate",
        status_lines=(
            "局部 frame 代数：PROVED",
            "旧族中和：PROVED",
            "新双流指数门 13/13：FINITE",
            "双包存活与完整账本：OPEN",
            "不构成 Clay 问题解答：NOT CLAY",
        ),
        sections=(
            ("01", "两种局部 frame 不等价", r"""
<p>令终端轨迹满足 \(\dot X_R=u_R(t,X_R)\)。只移动、不减去轨迹速度时，移动场 \(v_R\) 满足</p>
<div class="equation">\[\partial_tv_R-\Delta v_R+(v_R-a_R)\cdot\nabla v_R+\nabla\pi_R=0.\]</div>
<p>移动并减去 \(a_R=\dot X_R\) 时，\(w_R\) 满足</p>
<div class="equation">\[\partial_tw_R-\Delta w_R+w_R\cdot\nabla w_R+\nabla\pi_R=-a_R'.\]</div>
<p>加速度 \(-a_R'\) 不能被藏入周期 torus pressure。匹配 mollifier 在半径 \(R\) 上精确消掉它的测试矩，但 \(2R\)、\(8R\) 或不匹配 sharp cutoff 不会自动消失。</p>"""),
            ("02", "旧 R0.74D 反例族被完整中和", r"""
<p>局部轨迹在整个付款时间窗内跟随旧 packet，始终位于 \(q_m+O(R^2)\)。因此旧的 kinematic target 转入 algebraic harmonic payment。对该显式族的每一个成员，两个局部 frame 版本均满足</p>
<div class="equation">\[X_R^M\le C(P_R^M)^{2/3},\qquad
X_R^F\le C(P_R^F)^{2/3}.\]</div>
<p>这是 familywise neutralization，不是任意解端点定理。</p>"""),
            ("03", "新奇对称成对双流", r"""
<p>为避免局部中心跟随单个 packet，新构造采用成对奇对称流。冻结参数为</p>
<div class="equation">\[\lambda=\frac{63}{32},\quad c_h=\frac{15}{16},\quad
\alpha=\frac{14}{15},\quad \beta^2=\frac{31}{256},\quad
c_R=\frac1{320},\quad \kappa=16.\]</div>
<p>场是精确、光滑、周期、零均值、无外力 NSE 解；全反演奇性和偶 mollifier 给出</p>
<div class="equation">\[X_{R_j}(t)\equiv0,\qquad a_{R_j}(t)=a_{R_j}'(t)=0.\]</div>
<p>这只固定局部 frame；还没有证明被输运的 passive packets 在终端存活。</p>"""),
            ("04", "非空指数窗口", r"""
<p>有限算术门验证</p>
<div class="equation">\[\frac4{1323}<\frac1{320}<\frac{49}{14625},\qquad
\frac{75}{22528}>\frac1{320}>\frac8{3969}.\]</div>
<p>第一条给出非空半径指数窗；第二条说明横向泄漏指数同时压过 \(R_j^{-1}\) 前因子和 annular weight。新严格间隙是</p>
<div class="equation">\[\frac{75}{22528}-\frac1{320}=\frac{23}{112640}>0.\]</div>
"""),
            ("05", "两个被拒绝的窄机制", """
<p>高频单 cosine 被排除的是“统一 scale-\(R\) 扰动 packet 机制”，不是所有单模构造。对称 midpoint 双 bump 在直接充分估计 \(c_R&gt;1/192\) 与 \(c_R&lt;1/266240\) 下窗口为空；这也不是 plateau 构造的普适不可能性定理。</p>"""),
            ("06", "有限层不等于解析存活", """
<p><strong>FINITE：</strong>证书 13/13 PASS，图件 validator 42/42 PASS。它们只核对参数、指数窗、几何兼容与图件档案；不证明 Feynman--Kac survival、buffered leakage、压力复制项或完整付款比。</p>"""),
            ("07", "证据与文献边界", """
<p><strong>PROVED：</strong>局部 frame 方程、匹配 mollifier 消去、旧族中和、奇对称中心锁定和参考路径校准均为解析结论。</p>
<p><strong>BOUNDED LITERATURE AUDIT：</strong>mollified trajectories、flow-following cylinders、2D3C passive scalar 与 shear dispersion 都有经典或近期先例；这里不作“第一”或优先权表述。</p>"""),
            ("08", "开放边界", """
<ul><li>两 packet 的 Feynman--Kac 存活；</li><li>有限指数比较之外的解析泄漏；</li><li>完整 \(E/G_u/G_p/H_u\) transition、packet、mixed 与 periodic-copy 账本；</li><li>一个同时闭合 Version-M/F 比值的振幅。</li></ul>
<p><strong>NOT CLAY：</strong>本节没有 epsilon regularity、奇点或任意三维全局结论。</p>"""),
        ),
        evidence_links=(
            ("规范研究报告", "research/r074e_local_mollified_frame_gate.md"),
            ("局部 frame 独立审计", "research/r074e_local_frame_independent_audit.md"),
            ("有限门独立审计", "research/r074e_finite_gate_independent_audit.md"),
            ("有限证书报告", "research/r074e_outer_annulus_exponent_certificate_report.md"),
            ("机器可读证书", "research/r074e_outer_annulus_exponent_certificate.json"),
            ("证书脚本", "scripts/r074e_outer_annulus_exponent_certificate.py"),
        ),
        card="局部 mollified frame 完整支付旧 R0.74D 族；新的奇对称双流精确锁定中心并通过 13/13 指数门，但 packet survival 仍开放。",
        next_gate="保留全部周期 winding，证明或否定两 packet 在终端外环带的正测度存活。",
        literature_boundary="mollified trajectories、flow-following geometry、2D3C passive scalar 与 shear dispersion 均有先例；有限检索不承担 novelty。",
    ),
    Release(
        code="R0.74F",
        slug="r074f",
        title="R0.74F｜奇对称局部坐标中的双包存活：周期桥估计闭合",
        subtitle="局部中心严格锁定；保留所有 winding 的 Brownian bridge 给出冻结端点正下界",
        figure_dir="fig-r074f-two-packet-survival-gates",
        figure_slug="fig-r074f-two-packet-survival-gates",
        status_lines=(
            "双包存活定理：PROVED",
            "两份独立解析审计：PASS",
            "有限证书 30/30：FINITE",
            "完整 denominator / amplitude：OPEN",
            "不构成 Clay 问题解答：NOT CLAY",
        ),
        sections=(
            ("01", "冻结参数与精确解族", r"""
<p>保留 R0.74E 的参数</p>
<div class="equation">\[\lambda=\frac{63}{32},\quad c_h=\frac{15}{16},\quad
\alpha=\frac{14}{15},\quad \beta=\frac{\sqrt{31}}{16},\quad
c_R=\frac1{320},\quad \kappa=16.\]</div>
<p>令 \(L_j=\lambda2^j\)、\(R_j=e^{-c_RL_j^2}\)、\(r_j=L_jR_j\)。本节构造精确、光滑、周期、零均值、无外力 2D3C 解</p>
<div class="equation">\[u_j=(\mathfrak a_jF_j,b_j,0),\qquad p_j=0.\]</div>
"""),
            ("02", "奇对称性严格锁定局部中心", r"""
<p>全反演奇性与偶匹配 mollifier 使选定局部轨迹、速度与加速度全部消失：</p>
<div class="equation">\[X_{R_j}(t)\equiv0,\qquad a_{R_j}(t)=a_{R_j}'(t)=0.\]</div>
<p>因此 frame 本身没有漂移误差，packet 是否存活成为纯解析问题，而不是坐标选择问题。</p>"""),
            ("03", "正 packet 的反向 Feynman--Kac 表示", """
<p>证明把终端 packet 值写成时间反向随机表示。周期流形上的 Brownian path 不能只保留中央复制；所有 winding 都必须纳入。正 packet 的主桥事件、drift shift 和横向扩散分别估计，负 packet 则用严格的相反侧指数抑制。</p>
<p>这里的随机表示只服务于解析下界，没有 Monte Carlo、DNS 或经验拟合。</p>"""),
            ("04", "完整周期 Brownian bridge 门", """
<p>桥恒等式按整数 winding 精确求和。主 winding 的正概率由固定 tube 事件控制；其他 winding 不是删除，而是进入统一可求和上界。累计 drift-shift 小于冻结终端 lobe 的几何余量；反向 packet 的到达概率带有更强指数。</p>
<p>终端 lobe 在指定 dyadic annulus 内具有正测度，这把路径概率下界转成确定性的 \(L^2\) 外环带下界。</p>"""),
            ("05", "双包存活主定理", r"""
<p><strong>PROVED。</strong>对每个 \(\mathfrak a_j&gt;0\) 以及所有充分大的 \(j\)，</p>
<div class="equation">\[\boxed{
X_{R_j}^M=X_{R_j}^F
\ge c\,\mathfrak a_j^2L_jR_j^2
e^{-c_\gamma L_j^2},\qquad c_\gamma=\frac8{3969}.}\]</div>
<p>有限算术门从 \(j=13\) 开始，但解析定理有多个渐近估计，所以公开量词保留“充分大”，不把 \(j=13\) 偷换成全部解析步骤的统一阈值。</p>"""),
            ("06", "两份独立解析审计", """
<p>周期桥审计逐行复核全 winding 恒等式、drift shift 与 bridge tube 概率；双包存活审计独立复核 packet 符号、终端几何和最终指数。两份审计绑定同一最终主报告 SHA；状态提升前后的主体 1--6 节经字节比较保持一致。</p>"""),
            ("07", "有限证书与图件边界", """
<p><strong>FINITE：</strong>算术证书 30/30 PASS，只核对有理恒等式、指数余量、离散阈值和条件 annular geometry。图 validator 50/50 PASS，SVG/PDF/600 dpi PNG、灰度和最终尺寸均通过。</p>
<p>图上明确写明：有限兼容性不能认证解析 bridge 或 packet survival；图不是 DNS、仿真或数值证明。</p>"""),
            ("08", "文献与开放边界", """
<p><strong>BOUNDED LITERATURE AUDIT：</strong>Feynman--Kac、Brownian bridge、2D3C passive scalar、shear dispersion 和 mollified trajectory 各有直接先例。限定检索未定位同一组合定理，但这不是 priority/novelty proof。</p>
<ul><li>半径 \(8R_j\) 上所有速度/梯度分量的 buffered local-energy 上界；</li><li>transition、background、packet、mixed \(G_u\)、pressure gauge 与 all-copy \(H_u\) 行；</li><li>一个闭合完整 denominator 的振幅 \(\mathfrak a_j\)；</li><li>任意 NSE 解的端点与所有正则性后果。</li></ul>
<p><strong>NOT CLAY：</strong>双包存活下界不是 global regularity、blow-up 或 Clay 问题的部分完成。</p>"""),
        ),
        evidence_links=(
            ("规范解析证明", "research/r074f_two_packet_survival.md"),
            ("周期桥独立审计", "research/r074f_periodic_bridge_independent_audit.md"),
            ("存活定理独立审计", "research/r074f_two_packet_survival_independent_audit.md"),
            ("一手文献边界", "research/r074f_primary_literature_boundary.md"),
            ("有限证书报告", "research/r074f_two_packet_survival_certificate_report.md"),
            ("机器可读证书", "research/r074f_two_packet_survival_certificate.json"),
            ("证书脚本", "scripts/r074f_two_packet_survival_certificate.py"),
            ("冻结清单", "research/r074f_freeze_manifest.json"),
        ),
        card="奇对称性把局部中心钉在原点；保留全部 winding 的周期 Brownian bridge 证明两 packet 在终端外环带仍有正测度存活。完整 denominator 仍开放。",
        next_gate="补齐 buffered local energy、完整 \(G_u/G_p/H_u\) 与 all-copy 账本，再决定是否存在统一闭合振幅。",
        literature_boundary="Feynman--Kac、Brownian bridge、2D3C passive scalar、shear dispersion 与 mollified trajectory 均有直接先例；bounded search 不证明新颖性或优先权。",
    ),
)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value, encoding="utf-8")


def write_json(path: Path, value: object) -> None:
    write_text(path, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replace_once(value: str, old: str, new: str, label: str) -> str:
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def assert_recap() -> None:
    for path, expected in RECAP_HASHES.items():
        if sha256(path) != expected:
            raise RuntimeError(f"protected recap drift: {path.relative_to(ROOT)}")


def common_style() -> str:
    return """
:root{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}
@media(prefers-color-scheme:dark){:root{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}
*{box-sizing:border-box}html,body{max-width:100%;overflow-x:hidden}body{margin:0;background:var(--paper);color:var(--ink);font:17px/1.72 Georgia,"Songti SC","Noto Serif SC",serif}
.top{border-top:5px solid var(--ink);border-bottom:3px double var(--ink);padding:12px 5vw;display:flex;justify-content:space-between;gap:1rem}.top a{font-weight:700;text-decoration:none}
main{width:min(940px,90vw);margin:auto}.hero{padding:54px 0 30px;border-bottom:1px solid var(--line)}.hero-inner{display:grid;grid-template-columns:minmax(0,1fr) minmax(220px,290px);gap:2rem}
h1{font-size:clamp(2rem,5.7vw,3.8rem);line-height:1.08;margin:.35em 0}h2{margin:2.8rem 0 1rem;color:var(--rule);font-size:1.55rem}h3{color:var(--rule)}
.stamp,.section-no,.label{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.07em;text-transform:uppercase}.stamp{border:1px solid var(--line);padding:1rem;background:var(--raised)}
article{padding:14px 0 72px}section{padding-bottom:.5rem;border-bottom:1px dotted var(--line)}p,li{overflow-wrap:anywhere}.equation{overflow:auto;background:var(--raised);padding:13px 15px;border-left:4px solid var(--rule);margin:1rem 0}.callout{padding:1rem 1.2rem;background:var(--raised);border:1px solid var(--line)}
.labels{display:flex;flex-wrap:wrap;gap:.5rem;margin:1rem 0}.label{border:1px solid var(--line);padding:.28rem .55rem;background:var(--raised)}a{color:var(--rule)}img{max-width:100%;height:auto}.files{line-height:2}.figure-note{color:var(--muted);font-size:.94rem}
@media(max-width:720px){body{font-size:15px}.hero-inner{grid-template-columns:1fr}main,article,section{min-width:0}.top{font-size:13px}.equation mjx-container[display="true"]{display:block!important;width:100%!important;overflow-x:auto;overflow-y:hidden}}
@media print{:root{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}.top{display:none}body{background:#fff;font-size:10.2pt}main{width:auto}.hero{padding-top:0}.hero-inner{grid-template-columns:1fr 220px}a{color:inherit;text-decoration:none}section{break-inside:auto}.stamp{break-inside:avoid}.equation{break-inside:avoid}}
"""


def render_note(release: Release) -> str:
    status = "".join(f"<p>{line}</p>" for line in release.status_lines)
    labels = "".join(
        f'<span class="label">{label}</span>'
        for label in ("PROVED", "FINITE", "OPEN", "BOUNDED LITERATURE AUDIT", "NOT CLAY")
    )
    sections = "\n".join(
        f'<section id="s-{number}"><div class="section-no">{number} / 完整中文笔记</div><h2>{title}</h2>{body}</section>'
        for number, title, body in release.sections
    )
    repo = "https://github.com/Kasifa/Kasifa.github.io/blob/main/"
    evidence = " · ".join(f'<a href="{repo}{path}">{label}</a>' for label, path in release.evidence_links)
    figbase = f"/assets/{release.slug}/{release.figure_slug}"
    figrepo = f"https://github.com/Kasifa/Kasifa.github.io/tree/main/public/figures/{release.slug}/{release.figure_dir}"
    return f'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{release.title}</title><meta name="description" content="{release.subtitle}">
<link rel="canonical" href="https://kasifa.github.io/notes/{release.slug.replace('r074','r0-74')}.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\\\(","\\\\)"]],displayMath:[["\\\\[","\\\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script>
<script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script><style>{common_style()}</style></head>
<body><nav class="top"><a href="/research-review.html">研究首页</a><span>{release.code} · 2026-09-01</span></nav><main>
<header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 {release.code} · 完整中文版本</div><h1>{release.title}</h1><p>{release.subtitle}</p><div class="labels">{labels}</div><p>“NOT CLAY”表示本节不构成 Clay 千禧年问题的解答；“不可行性结论”只排除文中写明的具体估计或方法，不否定 Navier--Stokes 方程的其他路线。</p></div><div class="stamp"><strong>状态 · {release.code}</strong>{status}<p>LOCAL DIRECT / NO DGX</p></div></div></header>
<article>{sections}
<section id="figure"><div class="section-no">F / 期刊主图</div><h2>解析门槛与结论边界</h2>
<picture><source srcset="{figbase}.svg" type="image/svg+xml"><img src="{figbase}.png" alt="{release.code} analytic proof ledger and open-boundary figure"></picture>
<p><a href="{figbase}.pdf">下载矢量 PDF</a> · <a href="{figbase}.png">下载 600 dpi PNG</a> · <a href="{figbase}.svg">打开 SVG</a> · <a href="{figrepo}">源数据、caption 与 QA</a></p>
<p class="figure-note">主图是可复算的解析账本示意；它不是 DNS、NSE 时间仿真、奇点候选或有限采样证明。</p></section>
<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>证明、独立审计、证书与复现材料</h2><p class="files">{evidence}</p>
<p><a href="/notes/{release.slug.replace('r074','r0-74')}.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X）</a></p></section>
<section class="callout" id="next"><div class="section-no">NEXT / 下一门槛</div><h2>{'R0.74G' if release.slug == 'r074f' else '后续接口'}</h2><p>{release.next_gate}</p></section>
</article></main></body></html>'''


def copy_figures(release: Release) -> None:
    source = ROOT / f"research/figures/{release.slug}/{release.figure_dir}"
    if not source.is_dir():
        raise RuntimeError(f"missing frozen figure package: {source}")
    for target in (
        ROOT / f"figures/{release.slug}/{release.figure_dir}",
        PUBLIC / f"figures/{release.slug}/{release.figure_dir}",
    ):
        if target.exists():
            shutil.rmtree(target)
        shutil.copytree(source, target)
    asset_dir = PUBLIC / "assets" / release.slug
    asset_dir.mkdir(parents=True, exist_ok=True)
    for extension in ("svg", "pdf", "png"):
        shutil.copy2(source / f"figure.{extension}", asset_dir / f"{release.figure_slug}.{extension}")


def write_dictionaries() -> None:
    for release in RELEASES:
        lines = [
            f"# {release.code} bilingual publication dictionary",
            "",
            "The public note is authored completely in Chinese. This small dictionary fixes only recurring status terminology; it does not replace the Chinese note.",
            "",
            "| Chinese | English |",
            "|---|---|",
            "| 已证明 | PROVED |",
            "| 有限证书 | FINITE certificate |",
            "| 开放问题 | OPEN |",
            "| 有界文献审计 | BOUNDED LITERATURE AUDIT |",
            "| 不构成 Clay 问题解答 | NOT CLAY |",
            "| 不可行性结论 | no-go for the stated estimate only |",
            "",
            f"Chinese title: {release.title}",
            f"English working title: {release.code} publication boundary note",
            "",
        ]
        write_text(ROOT / f"research/{release.slug}_bilingual_dictionary.md", "\n".join(lines))


def card_html(release: Release) -> str:
    return f'''          <div class="task-one" id="{release.slug}" data-release="{release.slug}" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 {release.code} · 2026-09-01</p><h3>{release.title}</h3>
            <p>{release.card}</p>
            <p><strong>状态：</strong>PROVED / FINITE / OPEN / BOUNDED LITERATURE AUDIT / NOT CLAY。</p>
            <p><a href="/notes/{release.slug.replace('r074','r0-74')}.html"><strong>阅读 {release.code} 完整中文笔记 →</strong></a><br><a href="/notes/{release.slug.replace('r074','r0-74')}.pdf">下载同步 PDF</a> · <a href="/assets/{release.slug}/{release.figure_slug}.pdf">下载期刊附图 PDF</a> · <a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（截止 R0.73X）</a></p>
            <p><strong style="color:var(--gold)">下一接口：</strong>&nbsp;{release.next_gate}</p>
          </div>'''


def update_home() -> None:
    home = HOME.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.67"', f'data-site-version="{VERSION}"', "home site version"),
        ('/i18n-en.js?v=1.67', f'/i18n-en.js?v={VERSION}', "home i18n version"),
        ('/site-refresh.js?v=1.67.1', f'/site-refresh.js?v={VERSION}.1', "home refresh version"),
        ('<strong>v1.67</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', "home version stat"),
        ('<span><strong>203</strong>公开研究笔记</span>', '<span><strong>208</strong>公开研究笔记</span>', "home note count"),
        ('<span><strong>R0.74A</strong>最新研究节点</span>', '<span><strong>R0.74F</strong>最新研究节点</span>', "home latest stat"),
        ('Research topology · R0.1–R0.74A', 'Research topology · R0.1–R0.74F', "home topology label"),
        ('href="#r074a">跳到首页 R0.74A 卡片 →', 'href="#r074f">跳到首页 R0.74F 卡片 →', "home jump link"),
        ('href="#r070a">R0.70A–R0.74A：105 节已公开，81 节完整封存', 'href="#r070a">R0.70A–R0.74F：110 节已公开，86 节完整封存', "home progress link"),
        ('<span class="route-range">R0.69P–R0.74A</span>', '<span class="route-range">R0.69P–R0.74F</span>', "tree current range"),
        ('<h3>R0.74A：局部 K_D 付款已闭合</h3>', '<h3>R0.74F：双包存活已闭合，完整 denominator 仍开放</h3>', "tree current title"),
        ('<p class="tree-current-summary">core 由 local energy 支付，exterior 由显式 Gaussian tails 支付；尾项吸收与 epsilon regularity 仍开放。NOT CLAY。</p>', '<p class="tree-current-summary">奇对称局部 frame 锁定中心，周期 Brownian bridge 证明双包存活；完整付款账本与振幅闭合仍开放。NOT CLAY。</p>', "tree summary"),
        ('<p class="tree-path">production-only no-go → 正观测修复 → 局部 K_D 付款</p>', '<p class="tree-path">正观测修复 → 局部付款 → 固定中心运输障碍 → 局部 frame → 双包存活</p>', "tree short path"),
        ('<span>R0.72R–R0.74A：</span>', '<span>R0.72R–R0.74F：</span>', "tree detail range"),
        ('aria-label="R0.69P–R0.74A"', 'aria-label="R0.69P–R0.74F"', "tree link aria"),
        ('综述 v1.67 · 2026-09-01', f'综述 v{VERSION} · 2026-09-01', "home footer version"),
    ):
        home = replace_once(home, old, new, label)

    home = re.sub(
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.74F 已证明奇对称局部 frame 中的双包存活。下一步只补齐 buffered local energy、完整外部账本与振幅闭合；任意三维全局正则性和 Clay 仍为 OPEN。</span></div>',
        home, count=1, flags=re.S,
    )

    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.74F · 2026-09-01</p><h2 class="route-map-title" id="latest-release-title">R0.74F｜奇对称局部坐标中的双包存活</h2><p class="route-map-intro">周期 Brownian bridge 保留全部 winding，并给出终端外环带的正测度存活下界。完整 denominator 与 amplitude closure 仍开放。NOT CLAY。</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-74f.pdf">阅读最新 R0.74F 研究笔记 →</a><a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap（R0.61–R0.73X，140 节）</a><a href="/notes/">208 篇研究笔记总索引</a><a href="#r074f">查看首页 R0.74F 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.74F · 110 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>86 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.74F</span></div></div></section>'''
    home, n = re.subn(r'<section class="route-overview latest-release-spotlight".*?</section>', latest, home, count=1, flags=re.S)
    if n != 1:
        raise RuntimeError("latest release spotlight replacement failed")

    old_next = re.compile(r'<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0\.74B</span>.*?</article></div>', re.S)
    new_next = '<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.74G</span><span class="tree-state current">下一检查点</span></div><h3>R0.74G 下一接口</h3><p>补齐双包族的 buffered local energy、完整 transition/background/packet/mixed 与 all-copy 账本，并寻找一个同时闭合 denominator 的振幅；失败则记录精确 obstruction，不作正则性外推。</p></article></div>'
    home, n = old_next.subn(new_next, home, count=1)
    if n != 1:
        raise RuntimeError("next route card replacement failed")

    anchors = "\n".join(f'<a class="milestone" href="/notes/{r.slug.replace("r074","r0-74")}.html">{r.code}</a>' for r in RELEASES)
    home = replace_once(home, '<a class="milestone" href="/notes/r0-74a.html">R0.74A</a>', '<a class="milestone" href="/notes/r0-74a.html">R0.74A</a>\n                  ' + anchors, "route note links")

    cards = "\n".join(card_html(r) for r in reversed(RELEASES)) + "\n"
    home = replace_once(home, '<div class="task-one" id="r074a" data-release="r074a"', cards + '          <div class="task-one" id="r074a" data-release="r074a"', "home release cards")

    home = home.replace('R0.69P–R0.74A', 'R0.69P–R0.74F')
    home = home.replace('R0.70A–R0.74A', 'R0.70A–R0.74F')
    home = home.replace('R0.72R–R0.74A', 'R0.72R–R0.74F')
    home = home.replace('全站现有 203 篇公开研究笔记', '全站现有 208 篇公开研究笔记')
    write_text(HOME, home)


def literature_route_steps() -> str:
    rows = []
    for release in RELEASES:
        rows.append(
            f'<div class="route-step kept"><header><b>{release.code}</b><strong>{release.title.split("｜",1)[1]}</strong></header>'
            f'<p>{release.card} <a href="/notes/{release.slug.replace("r074","r0-74")}.html">研究笔记</a> '
            f'<a href="/recap-r0-61-r0-73x.html">上一大里程碑 recap</a> '
            f'<a href="#{release.slug}-boundary">文献边界</a></p></div>'
        )
    rows.append('<div class="route-step pause"><header><b>开放接口 · R0.74G</b><strong>完整 denominator 账本与振幅闭合</strong></header><p>补齐 R0.74F 双包族的 buffered local energy、transition/background/packet/mixed 与 all-copy 行；只有完整比值闭合后才讨论更强接口。</p></div>')
    return "".join(rows)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    for old, new, label in (
        ('data-site-version="1.67"', f'data-site-version="{VERSION}"', "literature version"),
        ('/i18n-en.js?v=1.67', f'/i18n-en.js?v={VERSION}', "literature i18n"),
        ('R0.69P–R0.74A 只列为研究笔记', 'R0.69P–R0.74F 只列为研究笔记', "literature intro range"),
        ('文献综述 v1.67 · 2026-09-01', f'文献综述 v{VERSION} · 2026-09-01', "literature footer"),
    ):
        page = replace_once(page, old, new, label)
    pause = re.compile(r'<div class="route-step pause"><header><b>开放接口 · R0\.74B</b>.*?</div>', re.S)
    page, n = pause.subn(literature_route_steps(), page, count=1)
    if n != 1:
        raise RuntimeError("literature route insertion failed")
    boundaries = "\n".join(
        f'<h3 id="{r.slug}-boundary">{r.code} 的文献与主张边界</h3><p>{r.literature_boundary}</p>'
        f'<div class="boundary"><strong>{r.code} 的公开边界</strong><p>PROVED、FINITE、OPEN、BOUNDED LITERATURE AUDIT 与 NOT CLAY 在研究笔记中逐项分开。'
        f'<a href="/notes/{r.slug.replace("r074","r0-74")}.html">阅读完整中文笔记</a>。</p></div>'
        for r in RELEASES
    )
    page = replace_once(page, '        <section id="references">', boundaries + '\n        <section id="references">', "literature boundaries")
    write_text(LITERATURE, page)


def update_accounting() -> None:
    site = {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": "R0.74F",
        "publicHtmlNoteCount": 208,
        "postR060PublishedNodeCount": 148,
        "postR060RecapNodeCount": 140,
        "latestRecapRelease": "R0.73X",
        "publicPdfNoteCount": 165,
        "publishedDate": "2026-09-01",
    }
    write_json(SITE_VERSION, site)
    write_text(ROOT / "VERSION", VERSION + "\n")

    inventory = json.loads(INVENTORY.read_text(encoding="utf-8"))
    for release in RELEASES:
        if release.slug not in inventory["publishedReleases"]:
            inventory["publishedReleases"].append(release.slug)
        if release.slug not in inventory["formalSealedReleases"]:
            inventory["formalSealedReleases"].append(release.slug)
    inventory["latestPublishedRelease"] = "r074f"
    inventory["publishedReleaseCount"] = len(inventory["publishedReleases"])
    inventory["formalSealedReleaseCount"] = len(inventory["formalSealedReleases"])
    write_json(INVENTORY, inventory)

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": "r074f",
        "siteVersion": VERSION,
        "publicHtmlNoteCount": 208,
        "publicPdfNoteCount": 165,
        "postR060PublishedNodeCount": 148,
        "postR060RecapNodeCount": 140,
        "nextRelease": "r074g",
        "latestReleaseGate": "tests/r074f-release.test.mjs",
        "latestReleasePublicationTest": "tests/r074f-release.test.mjs",
        "postR070APublishedReleaseCount": inventory["publishedReleaseCount"],
        "postR070AFormalSealedReleaseCount": inventory["formalSealedReleaseCount"],
        "latestRecapRelease": "r073x",
        "latestRecapHtml": "/recap-r0-61-r0-73x.html",
        "latestRecapPdf": "/recap-r0-61-r0-73x.pdf",
        "latestReleaseTranslationScript": "LOCAL_DIRECT_CHINESE_AUTHORING",
        "latestReleasePdfBinder": "scripts/bind-r074b-f-pdfs.mjs",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(INVENTORY),
    }
    write_json(MANIFEST, manifest)


def main() -> None:
    assert_recap()
    for release in RELEASES:
        copy_figures(release)
        note_slug = release.slug.replace("r074", "r0-74")
        write_text(PUBLIC / f"notes/{note_slug}.html", render_note(release))
    write_dictionaries()
    update_home()
    update_literature()
    update_accounting()
    assert_recap()
    print(json.dumps({
        "status": "generated",
        "latestRelease": "R0.74F",
        "notes": [release.code for release in RELEASES],
        "siteVersion": VERSION,
        "recapPreserved": True,
        "translationRoute": "LOCAL_DIRECT_NO_DGX",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
