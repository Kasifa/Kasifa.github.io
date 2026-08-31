# R0.73Q bilingual dictionary and public-claim boundary

**Status:** canonical terminology for synchronized HTML/PDF rendering

**Release title:** R0.73Q | A critical heat-flow tube beyond the
\(H^{1/2}\) entrance

**Public title (zh):** R0.73Q｜越过 \(H^{1/2}\) 入口的临界热流稳定管

**Next release:** R0.73R

This dictionary fixes the public vocabulary for one fixed a priori global
periodic \(H^3\) orbit.  It does not turn that hypothesis into a theorem for
arbitrary data, promote a finite-index Besov argument to an unrestricted
\(BMO^{-1}\) result, or claim novelty or priority.

## 1. Mathematical terms

| English | Chinese | Required meaning |
| --- | --- | --- |
| a priori global reference orbit | 先验全局参考轨道 | A fixed unforced solution already known to lie in \(C([0,\infty);H^3_{\sigma,0})\cap L^2_{\rm loc}([0,\infty);H^4_{\sigma,0})\). R0.73Q does not prove this hypothesis for arbitrary data. |
| heat-flow trace norm | 热流迹范数 | The concrete caloric-extension norm \(\|f\|_{\mathfrak X}:=\|e^{t\Delta}f\|_{L^4((0,\infty);L^6(\mathbb T^3))}\), equivalent on mean-zero periodic distributions to \(\dot B^{-1/2}_{6,4}\). It is not a spatial boundary trace. |
| critical Besov tube | 临界 Besov 稳定管 | The sufficient neighborhood \(\|v_0-u(t_0)\|_{\mathfrak X}<\rho_{\mathfrak X}[u]\), with smooth \(H^3\) input and uniqueness in the resulting mild/Serrin strong class. |
| finite reference action | 有限参考轨道作用量 | \(M[u]=\|u\|_{L^4(0,\infty;L^6)}<\infty\), inherited from the R0.73P orbit estimate. The stability constants may depend on this fixed orbit. |
| uniform all-restart radius | 对全部重启时刻统一的稳定半径 | One positive \(\rho_{\mathfrak X}[u]\) works for every \(t_0\ge0\). It is uniform in restart time, not uniform over all reference orbits or all \(L^2\) data. |
| periodic Oseen--HLS closure | 周期 Oseen--HLS 闭合 | The causal bilinear estimate \(\|\mathcal B(a,b)\|_{L^4_tL^6_x}\le C_B\|a\|_{L^4_tL^6_x}\|b\|_{L^4_tL^6_x}\), proved with the periodic Oseen kernel and the strong map \(I_{1/4}:L^2_t\to L^4_t\). |
| linearized Volterra inverse | 线性化 Volterra 逆算子 | The inverse of \(I+\mathcal L_{U_{t_0}}\) on \(L^4_tL^6_x\), constructed by a finite causal action partition. Its explicit upper bound \(K[u]\) is finite and restart-uniform, not optimized. |
| Serrin continuation bridge | Serrin 延拓桥 | The full \(L^4_tL^6_x\) bound prevents finite-time breakdown for the already smooth input and propagates the \(H^3\) branch. It is not rough-data uniqueness outside the Serrin/mild class. |
| strict domain enlargement by union | 由并集实现的稳定域严格扩大 | The safe comparison is \(\mathcal D_Q[u]=B_{H^{1/2}}(R_{1/2}[u])\cup B_{\mathfrak X}(\rho_{\mathfrak X}[u])\supsetneq B_{H^{1/2}}(R_{1/2}[u])\). The two independently proved radii are not numerically ordered. |
| structured high-frequency entrance | 结构化高频入口 | The smooth shear family \(w_N=N^{-1/4}e_2\sin(Nx_1)\) satisfies \(\|w_N\|_2\to0\), \(\|w_N\|_{\mathfrak X}\to0\), and \(|w_N|_{1/2}\to\infty\). It certifies one controlled entrance, not an arbitrary \(L^2\)-ball. |
| bare Kato supremum | 裸 Kato 上确界范数 | The incomplete quantity \(\sup_{t>0}t^{1/4}\|w(t)\|_6\), without the local Carleson/tent-space component of the Koch--Tataru norm. |
| endpoint no-go | 端点不可闭合 | The exact failure of the proposed cross-term estimate from only \(u\in L^4_tL^6_x\), because it would require the false endpoint map \(I_{1/4}:L^4_t\to L^\infty_t\). This blocks one proof route only. |
| Koch--Tataru class | Koch--Tataru 解类 | The critical path space containing both a time-weighted \(L^\infty_x\) term and a local parabolic-cylinder Carleson \(L^2\) term. It must not be replaced by the bare Kato supremum. |
| nonperturbative \(BMO^{-1}\) non-uniqueness | 非扰动型 \(BMO^{-1}\) 数据的非唯一性 | The existence of periodic \(BMO^{-1}\) data with two distinct global finite-\(X_{KT}\) solutions, smooth for positive time. Remark 1.3 says the construction is not perturbative around zero; this is not a quantitative lower bound on the datum norm, does not say every such datum is non-unique, and does not contradict small-data uniqueness. |
| finite-index endpoint stop | 有限指标端点止步 | R0.73Q stops at the periodic \(\dot B^{-1/2}_{6,4}\) heat-flow/Serrin level and makes no unrestricted endpoint uniqueness claim. |
| classical collision | 经典文献碰撞 | Whole-space critical Besov orbit stability, whole-space \(BMO^{-1}\) openness around suitable global solutions, and broader periodic anisotropic domains already exist in the literature. |

## 2. Required public tokens

```text
periodicOseenHLS=CLOSED_AFTER_AUDIT
linearizedVolterraInverse=CLOSED_AFTER_AUDIT
uniformAllRestartRadius=CLOSED_AFTER_AUDIT
H3SerrinBridge=CLOSED_AFTER_AUDIT
periodicHeatFlowTube=CLOSED_AFTER_AUDIT
strictExtensionByUnion=CLOSED
heatFlowBallContainsEntirePublishedH12Ball=NOT_PROVED
bareKatoSupFromL4L6=BLOCKED_BY_ENDPOINT
fullKochTataruTheory=NOT_REFUTED
uniformL2Only=OPEN
nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
formulaDiagnosticValidation=PASS
formulaDiagnosticPackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
NOT CLAY
```

The literal public meaning of the endpoint token is also:
`nonperturbative BMO^-1 uniqueness=FALSE_IN_GENERAL`.  The release policy is
`novelty forbidden`.

## 3. Evidence-state vocabulary

| Token | Required interpretation |
| --- | --- |
| `CLOSED_AFTER_AUDIT` | The stated periodic analytic implication has passed the internal proof and independent readback in its declared topology and solution class. It is not a novelty label. |
| `CLOSED` | The set-theoretic union and strictness witness are complete under the two already proved tube theorems. |
| `BLOCKED_BY_ENDPOINT` | The bare \(L^4_t\to L^\infty_t\) fractional-integration route fails exactly; fuller endpoint theories are not refuted. |
| `OPEN` | No theorem is asserted. In particular, arbitrary \(L^2\)-small smooth perturbations remain outside the proved entrance unless the heat-flow condition is supplied. |
| `FALSE_IN_GENERAL` | A counterexample rules out unrestricted uniqueness in general; it does not classify every datum. |
| `FORBIDDEN` | No originality, priority, or first-proof wording is admissible. |
| provenance tokens | `sourceCommitAssigned=TRUE`, `finalSeal=TRUE`, and `formalFigurePackage=PASS` bind the finite packages to the recorded immutable source.  They do not enlarge the analytic theorem. |

## 4. Forbidden renderings

- Do not translate `critical` as “决定性的”; here it means
  scaling-critical.
- Do not call the heat-flow trace a boundary trace or a pointwise-in-time
  norm.
- Do not state that the radius is universal.  It depends on the fixed a
  priori global orbit through its finite \(L^4_tL^6_x\) action.
- Do not remove the hypothesis that the comparison datum is in
  \(H^3_{\sigma,0}\), or extend uniqueness beyond the constructed
  mild/Serrin strong branch.
- Do not claim that the new heat-flow ball contains the entire numerical
  \(H^{1/2}\) ball from R0.73P.  Only the union supports the published strict
  set inclusion.
- Do not turn the high-frequency shear sequence into an unrestricted
  \(L^2\)-only theorem, a singularity witness, or a PDE-optimality claim.
- Do not say that the endpoint no-go disproves Koch--Tataru bilinear theory
  or \(BMO^{-1}\) stability.  It blocks only the bare Kato-sup estimate from
  the sole \(L^4_tL^6_x\) action.
- Use `nonperturbative around zero`, not a quantitative `large-norm`
  threshold, for the \(BMO^{-1}\) non-uniqueness boundary; do not use that
  result against classical small-data uniqueness.
- Do not import whole-space scaling theorems verbatim as periodic theorems.
- Do not describe the periodic packaging as new, first, sharp, optimal, or
  priority-bearing.  The admissible label is an audited internal synthesis
  with direct classical collisions.
- Do not mark the source commit, final seal, formal figure package, or public
  release as complete before the corresponding provenance record exists.
- Do not state that R0.73Q solves, nearly solves, or materially settles the
  Clay global-regularity problem.

## 5. Public one-sentence boundary

**Chinese:** R0.73Q 对每条已先验全局存在的无强迫周期 \(H^3\) 参考轨道，
在具体的 \(L^4_tL^6_x\) 热流迹范数中给出一个对全部重启时刻统一的稳定管，
并以结构化高频剪切模证明其与旧 \(H^{1/2}\) 管的并集严格扩大稳定域；任意
\(L^2\)-only 入口仍开放，非扰动型 \(BMO^{-1}\) 唯一性一般为假，且这不是 Clay
结论。

**English:** For each fixed a priori global unforced periodic \(H^3\) orbit,
R0.73Q gives one heat-flow-trace stability tube valid at every restart time
and uses structured high-frequency shear modes to show that its union with
the earlier \(H^{1/2}\) tube strictly enlarges the stable domain; the
unrestricted \(L^2\)-only entrance remains open, unrestricted
nonperturbative \(BMO^{-1}\) uniqueness is false in general, and this is not
a Clay conclusion.

## 6. Literature and claim boundary

The admissible literature statement is that the underlying critical
stability mechanism has direct predecessors: Gallagher--Iftimie--Planchon
give whole-space stability around a priori global solutions in critical
Besov spaces; Iftimie's theorems plus an elementary Fourier-weight
comparison give broader periodic anisotropic domains around two-dimensional
components; and the Auscher--Dubois--Tchamitchian publisher abstract reports
whole-space \(BMO^{-1}\)-topology openness for the corresponding Cauchy-data
set.  Coiculescu--Palasek rule out unrestricted nonperturbative periodic
\(BMO^{-1}\) uniqueness.

The permitted value statement is narrower: the section records a
self-contained fixed-torus estimate, one explicit restart-uniform inverse
bound, and an exact smooth high-frequency entrance.  These facts support a
careful periodic synthesis; they do not support a novelty or priority claim.

## 7. Publication provenance

The 19-file formula certificate and the 25-file formal figure package are
sealed to immutable source commit
`cb9511c3af08a4beb0b31284e96e2a9c47a23d04`.  The package commits are
`a0b00c0ef7f425443c88445a5284381469ce4046` and
`6da152412e36c647449675cb3cfaf3c4dab4542f`, respectively.  These labels
certify byte identity and the declared validation scope; they do not enlarge
the continuum theorem.

```text
formulaDiagnosticValidation=PASS
formulaDiagnosticPackage=CLOSED
sourceCommitAssigned=TRUE
finalSeal=TRUE
formalFigurePackage=PASS
publicReleaseContent=READY
```

## 8. Synchronized title

```text
R0.73Q | A critical heat-flow tube beyond the H^{1/2} entrance
R0.73Q｜越过 H^{1/2} 入口的临界热流稳定管
```
