# R0.73N | Fixed-member finite-strain stability and the family-transfer obstruction

**Status:** continuum proof and independent analytic, adversarial, symmetry,
compactness, and bounded literature audits PASS; finite diagnostic validated
pre-seal but not yet final release evidence; source-commit binding, final
seal, formal figure, and public release PENDING

**Date:** 2026-08-31 (Asia/Shanghai)

**Public title (zh):** R0.73N｜固定成员有限应变稳定性与族转移障碍

## 1. Direct result

R0.73N closes a specific attempted inference from R0.73M. It does not turn
the R0.73M family-level departure into instability of one background. It
proves the opposite statement needed for that route: every fixed finite member
of the explicit family has a positive full-three-dimensional \(H^3\)
stability tube.

On the normalized standard three-torus, with viscosity one and zero forcing,
consider the mean-zero divergence-free trajectory

\[
 \overline U_\Lambda(t,y)
 =\left(0,0,-\Lambda e^{-4t}\sin2y
 +{\Lambda\over2}e^{-16t}\sin4y\right),
 \qquad 0<\Lambda<\infty.
 \tag{1.1}
\]

For every fixed \(\Lambda\), the internal continuum proof establishes forward
synchronized \((H^3,H^3)\) stability from the fixed initial time \(t_0=0\).
This is a fixed-trajectory extension of the FPS norm-quantifier pattern, not
an FPS theorem for a nonstationary orbit, not orbital stability, and not a
claim uniform over all starting times.

The decisive route correction is:

> The amplification in R0.73M becomes unbounded only while the marked
> background changes with \(\Lambda\). At each individual marked background,
> the local chordal moduli are finite and the full-three-dimensional \(H^3\)
> synchronized stability radius is positive.

## 2. Four topology statements that must remain separate

| Phase space and topology | Initial smallness | Observed distance | Global solution requirement | R0.73N state |
|---|---|---|---|---|
| full 3D synchronized \((H^3,H^3)\) | \(H^3\) | \(H^3\) | proved inside the fixed-member tube | **CLOSED** |
| full 3D custom \(H^3\)-in/\(L^2\)-out | \(H^3\) | \(L^2\) | inherited from the \(H^3\) tube | **CLOSED AS COROLLARY** |
| planar synchronized \((H^3_{\rm pl},L^2_{\rm pl})\) | genuinely \(L^2_{\rm pl}\) only, with \(H^3_{\rm pl}\) regularity | \(L^2_{\rm pl}\) | global by two-dimensional regularity | **CLOSED** |
| full 3D FPS \((H^3,L^2)\) | genuinely \(L^2\) only, with arbitrary \(H^3\) size | \(L^2\) | would require global \(H^3\) continuation | **OPEN** |

The second row must not be renamed as the fourth. In the FPS convention,
\((H^3,L^2)\) means that the datum is \(H^3\)-regular but small only in
\(L^2\); R0.73N does not prove that full-three-dimensional statement.

## 3. Exact relative-energy estimate

Let \(V\) be any strong solution of the same equation on \([0,T]\), and set
\(w=V-\overline U_\Lambda\). The perturbation equation gives the exact
relative-energy identity

\[
 {1\over2}{d\over dt}\|w\|_2^2+\|\nabla w\|_2^2
 =-\int_{\mathbb T^3}(\partial_yF_\Lambda)w_2w_3\,dx,
 \tag{3.1}
\]

where \(F_\Lambda\) is the third component of (1.1). Since

\[
 {1\over2}\|\partial_yF_\Lambda(t)\|_\infty
 \le \Lambda(e^{-4t}+e^{-16t}),
\]

Gronwall yields

\[
 \boxed{
 \|w(T)\|_2\le e^{\Lambda j(T)}\|w(0)\|_2,}
 \qquad
 j(T)={1-e^{-4T}\over4}+{1-e^{-16T}\over16}.
 \tag{3.2}
\]

Because \(j(T)\uparrow5/16\),

\[
 \sup_{0\le t<T_{\max}}\|w(t)\|_2
 \le e^{5\Lambda/16}\|w(0)\|_2
 \tag{3.3}
\]

on every common strong lifespan. Equation (3.3) is all-time only when the
comparison solution is known to be global: in the invariant planar subsystem
or inside the full-three-dimensional tube proved below.

## 4. The genuine planar \(L^2\)-small theorem

The subspace

\[
 \mathcal S_{2D}
 =\{(0,v_2(y,z),v_3(y,z)):
 \partial_yv_2+\partial_zv_3=0\}
 \tag{4.1}
\]

is exactly invariant. Every \(H^3_{\rm pl}\) datum in it produces a global
two-dimensional strong solution. Hence, for any \(\epsilon>0\),

\[
 \|w(0)\|_2<\epsilon e^{-5\Lambda/16}
 \quad\Longrightarrow\quad
 \sup_{t\ge0}\|w(t)\|_2<\epsilon.
 \tag{4.2}
\]

The smallness assumption in (4.2) is genuinely \(L^2\), not \(H^3\). This
is planar synchronized \((H^3_{\rm pl},L^2_{\rm pl})\) stability, with the
regularity and distance norms playing the FPS roles but with a fixed
nonstationary trajectory rather than an equilibrium.

## 5. Positive full-three-dimensional \(H^3\) tube

Use the normalized Bessel-potential norm and set

\[
 X(t)=\|w(t)\|_{H^3}^2,
 \qquad
 Y(t)=\|\nabla w(t)\|_{H^3}^2.
\]

Mean zero gives \(X\le Y\). Periodic Kato--Ponce/Moser estimates and the
top-order transport cancellations give a universal \(C_3\ge1\) such that

\[
 {1\over2}X'(t)+Y(t)
 \le C_3\|\overline U_\Lambda(t)\|_{H^4}X(t)
 +C_3X(t)^{1/2}Y(t).
 \tag{5.1}
\]

The two heat modes satisfy

\[
 A_{4,\Lambda}:=\int_0^\infty
 \|\overline U_\Lambda(t)\|_{H^4}\,dt
 \le {489\over32\sqrt2}\Lambda.
 \tag{5.2}
\]

Taking

\[
 r_3={1\over4C_3},
 \qquad
 R_\Lambda=r_3e^{-C_3A_{4,\Lambda}},
 \tag{5.3}
\]

the bootstrap closes for every datum satisfying
\(\|w(0)\|_{H^3}<R_\Lambda\). Strong continuation then gives a unique global
solution and

\[
 \boxed{
 \sup_{t\ge0}\|w(t)\|_{H^3}
 \le e^{C_3A_{4,\Lambda}}\|w(0)\|_{H^3}.}
 \tag{5.4}
\]

For every \(\epsilon>0\), one sufficient synchronized-stability radius is

\[
 \delta_\Lambda(\epsilon)
 =\min\{R_\Lambda,\epsilon e^{-C_3A_{4,\Lambda}}\}.
 \tag{5.5}
\]

The radius may become exponentially small as \(\Lambda\) grows, but it is
strictly positive for every fixed finite member. It is a sufficient radius,
not an optimal threshold.

Equation (5.4) also gives the custom full-three-dimensional
\(H^3\)-in/\(L^2\)-out corollary through \(\|w\|_2\le\|w\|_{H^3}\). It does
not close full-three-dimensional FPS \((H^3,L^2)\) stability.

## 6. What R0.73M actually implies for the flow map

For a fixed observation time \(T\), let

\[
 \mathcal D_T=\{u_0\in H^3_{\sigma,0}:
 \text{the unique strong solution from }u_0
 \text{ exists on }[0,T]\}
 \tag{6.1}
\]

and let \(S_T:\mathcal D_T\to H^3_{\sigma,0}\) be the time-\(T\) state map.
The local chordal moduli below are localized by \(H^3\) neighborhoods; the
superscript \(2\to2\) records only the norms in its quotient.

Precisely,

\[
 \mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T)
 :=\limsup_{r\downarrow0}
 \sup_{\substack{h\in C^\infty_{\sigma,0},\ 0<\|h\|_{H^3}<r\\
 \overline U_\Lambda(0)+h\in\mathcal D_T}}
 {\|S_T(\overline U_\Lambda(0)+h)
 -S_T(\overline U_\Lambda(0))\|_2\over\|h\|_2}.
 \tag{6.2}
\]

The modulus \(\mathfrak L_{\Lambda,\mathrm{loc}}^{3\to2}(T)\) uses the same
formula with \(\|h\|_{H^3}\) in the denominator.

At

\[
 D_*={1\over450},
 \qquad T_*={1\over1800},
 \qquad
 \mathcal A_*=\int_0^{D_*}\lambda_0(d)\,\mathrm d d,
\]

R0.73M and the energy upper bound imply, for every sufficiently large
\(\Lambda\),

\[
 \boxed{
 c_*e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{2\to2}(T_*)
 \le e^{\Lambda j_*}.}
 \tag{6.3}
\]

The launch estimate \(\|\phi_\Lambda\|_{H^3}\le C_H\Lambda^2\) gives the
mixed-topology bracket

\[
 \boxed{
 {c_*\over C_H}\Lambda^{-2}e^{\Lambda\mathcal A_*}
 \le\mathfrak L_{\Lambda,\mathrm{loc}}^{3\to2}(T_*)
 \le e^{\Lambda j_*}.}
 \tag{6.4}
\]

The exponents are compatible because

\[
 j_*>{359\over324000}>{173\over450000}>\mathcal A_*.
 \tag{6.5}
\]

The first strict inequality follows analytically from
\(1-e^{-x}>x-x^2/2\); it is not inferred from decimal evaluation. Equations
(6.3)--(6.4) do not identify a sharp exponent or a prefactor limit.

At any fixed \(0<\rho\le\rho_0\), the R0.73M marked pairs satisfy

\[
 \|h_{\Lambda,\rho}\|_{H^3}
 \le C_H\rho\Lambda^2e^{-\Lambda\mathcal A_*}\longrightarrow0,
\]

while their time-\(T_*\) output separation is at least \(c_*\rho\). Define

\[
 \mathcal E_\rho=
 \{\overline U_\Lambda(0),
 \overline U_\Lambda(0)+h_{\Lambda,\rho}:\Lambda\ge\Lambda_0\}
 \subset\mathcal D_{T_*}.
 \tag{6.6}
\]

The single Navier--Stokes flow map \(S_{T_*}\) fails to be uniformly continuous
from \(H^3\) to \(L^2\) on this explicit unbounded planar set of marked pairs.
Equivalently, the pointed maps fail to be equicontinuous across the family.
Every individual marked basepoint still has a finite local modulus.

This is one flow map at different basepoints, not a different solution map for
each \(\Lambda\).

## 7. The quantifier obstruction

R0.73M has the form

\[
 \exists\rho_0,c_*,\Lambda_0\quad
 \forall\Lambda\ge\Lambda_0\quad
 \forall\rho\in(0,\rho_0],
 \tag{7.1}
\]

where the base is \(\overline U_\Lambda\). With \(\rho\) fixed,
\(\Lambda\to\infty\) makes the selected input tend to zero and retains an
order-\(\rho\) endpoint, but it also changes the background.

Fix instead one admissible \(\Lambda^\sharp\ge\Lambda_0\). When
\(\rho\downarrow0\), the input tends to zero and the relative upper bound
forces the actual endpoint distance to zero. Sections 3--5 give a positive
stability radius for every fixed \(\Lambda>0\), including members below the
R0.73M threshold. Hence the family-level quantifiers cannot be exchanged for
arbitrarily small \(H^3\) input and fixed \(L^2\) escape at one member.

## 8. Why exact symmetry and compactness do not transfer the family

The registered candidates fail for explicit algebraic reasons.

| Candidate | What it preserves or changes | Decision for this route |
|---|---|---|
| pure amplitude multiplication | preserves the shear only because its self-advection vanishes; changes perturbed nonlinear dynamics | not a neighborhood symmetry |
| time translation | must match heat rates \(4\) and \(16\) simultaneously | only the zero shift preserves both modes |
| spatial translation or Galilean change | changes phase or adds a zero mode | cannot change \(\Lambda\) |
| parabolic scaling | changes torus representation, Fourier rows, time, and \(H^3\) size unless scale is one | no fixed-torus conjugacy |
| original-time compactness | \(\|\overline U_\Lambda(0)\|_2^2=5\Lambda^2/8\) | no bounded Sobolev subsequence |
| time-shift compactness | every bounded limit loses the second harmonic | loses the certified mechanism |
| smooth infinite-block embedding | fixed smooth heat shears retain finite integrated \(H^4\) size | remains inside the finite-strain tube class |

This audit closes only the registered transfer routes. A different forced,
nondecaying, infinite-strain, or otherwise structurally different background
would require a new problem and a new theorem.

## 9. Literature position

The bounded two-wave source audit fixes three boundaries.

1. Friedlander--Pavlović--Shvydkoy define the \((X,Z)\) norm roles for a
   fixed equilibrium and prove an autonomous spectral-to-nonlinear theorem;
   they do not prove the present nonstationary synchronized theorem.
2. Grenier-type constructions, Couette threshold results, and classical
   non-normal transient growth show that parameter-dependent large gain is a
   meaningful phenomenon, but do not exchange a varying-background family
   for one fixed member.
3. Heat-evolving and periodic-shear stability or frozen-spectrum results are
   neighboring comparisons with different geometry, hypotheses, or
   conclusions. They are not provenance for the internal R0.73N tube.

Primary links and exact support classes are recorded in
`r073n_literature_audit.md` and `r073n_claim_source_ledger.md`. The strongest
permitted absence statement is:

> No single source in the recorded bounded search supplies the R0.73N
> fixed-member theorem and family-transfer obstruction as a black box.

This is not an exhaustive classification and carries no novelty, first-result,
or priority claim.

## 10. Evidence ledger

| Evidence layer | State | Exact support |
|---|---|---|
| fixed-time relative \(L^2\) bound | CLOSED | direct nonlinear integration by parts and Gronwall |
| finite all-time strain envelope | CLOSED | exact two-mode heat formula |
| planar synchronized \((H^3_{\rm pl},L^2_{\rm pl})\) stability | CLOSED | planar invariance, global 2D regularity, and relative \(L^2\) bound |
| full-3D synchronized \((H^3,H^3)\) stability | CLOSED | periodic commutator estimate, finite \(H^4\) integral, bootstrap, and continuation |
| custom full-3D \(H^3\)-in/\(L^2\)-out | CLOSED AS COROLLARY | \(H^3\) theorem plus \(H^3\hookrightarrow L^2\) |
| full-3D FPS \((H^3,L^2)\) stability | **OPEN** | no theorem for arbitrary \(H^3\)-regular data small only in \(L^2\) |
| pointed family sensitivity and marked-set nonuniform continuity | CLOSED | sealed R0.73M lower theorem plus R0.73N upper estimate |
| registered symmetry and compactness transfer routes | CLOSED AS OBSTRUCTION | direct transformation and Sobolev/Fourier bookkeeping |
| independent analytic audit | PASS | complete rederivation of estimates, quantifiers, moduli, and transformations |
| adversarial audit | PASS | factor-of-two, lifespan, topology, bootstrap, modulus, and same-map attacks |
| bounded literature boundary | PASS | two-wave primary-source audit and internal claim-boundary reconciliation |
| finite diagnostic | VALIDATED PRE-SEAL; RELEASE PENDING | primary and independent checks pass, but source-commit binding and final seal are incomplete |
| formal figure | **PENDING** | no formal figure package is asserted yet |
| public release | **PENDING** | downstream rendering and publication gates remain |

## 11. Validated pre-seal finite diagnostic

The current R0.73N diagnostic package has passed its primary and independent
checks as a theorem-relevant error-detection layer. It remains pre-seal:
`sourceCommitAssigned=false` and `finalSeal=false`, so it is not yet final
release evidence. Its current checks cover:

- the exact normalized strain envelope \(e^{-4t}+e^{-16t}\), including its
  equality witness;
- the closed form for \(j(T)\) and \(j(\infty)=5/16\);
- the high-precision value
  \(j_*=0.0011080324480805907920035217032737848\ldots\);
- the exact strict rational chain in (6.5);
- illustrative exponent-factor curves across the marked background family.

The bound \(\mathcal A_*<173/450000\) is inherited from the sealed R0.73M
continuum theorem and is not recomputed by the finite package.

The pre-seal source-data file has exactly 605 rows: 241 strain samples, 243
cumulative samples, and 121 marked-basepoint samples. The primary validation
and the independent Decimal/Fraction reconstruction both report
`allChecksPass=true`; the latter evaluates six sentinel times without
importing the primary producer. These are pre-seal observations until the
parent release binds the final source commit and completes the final seal.

These facts are finite checks, not proof of the continuum energy inequality,
the \(H^3\) stability tube, the inherited action interval, a sharp flow-map
modulus, or any open statement.

## 12. Formal figure placeholder

**Status:** `PENDING`

No formal R0.73N figure package, frozen figure identifier, caption, file
inventory, or visual QA result is claimed in this source. A later figure may
visualize the exact strain envelope, cumulative \(j(T)\), and the lower/upper
pointed exponent factors only after its source-data binding and publication QA
are completed. Until then, the diagnostic CSV is not to be described as a
released journal figure.

## 13. Public release copy (zh)

### Title

R0.73N｜固定成员有限应变稳定性与族转移障碍

### Lead

R0.73N 对 R0.73M 的“变背景族能否转化为单个固定背景不稳定性”作出否定
判定。对显式无外力双谐波背景族中的每个固定有限 \(\Lambda\)，直接能量、
交换子与延拓估计给出一个正的全三维同步 \((H^3,H^3)\) 稳定管；R0.73M
所捕捉的是跨无界标记背景族的非一致指向放大，而不是任一固定成员处的
Lyapunov 不稳定性。

### Home

本节必须同时保留四条不同结论：全三维同步 \((H^3,H^3)\) 稳定性已经
闭合；全三维 \(H^3\)-输入/\(L^2\)-输出只是前者的自定义推论；平面不变
子系统内的同步 \((H^3_{\rm pl},L^2_{\rm pl})\) 稳定性具有真正的 \(L^2\)
初值小性；全三维 FPS \((H^3,L^2)\) 稳定性仍为 OPEN。这里的同步比较
固定从 \(t_0=0\) 出发，不允许轨道相移，也不声称对所有起始时刻一致。

### Recap

R0.73M 证明：当 \(\Lambda\to\infty\) 且背景随之改变时，按完整作用量
缩小的平面扰动可以在固定时刻保持固定阶输出。R0.73N 补上固定成员审计：
任意共存强解满足有限累积应变控制；平面扰动全局满足 \(L^2\) 稳定估计；
足够小的全三维 \(H^3\) 扰动落在正的全局强解稳定管内。因此，R0.73M
中的量词顺序不能交换为一个固定背景上的任意小输入、固定距离逃逸。

### Literature

有界两轮原始来源检索核对了 FPS 的范数量词、自治谱不稳定转移、Grenier
型参数族构造、Couette 阈值与瞬态增长、热演化剪切流和周期衰减流。检索
中没有一篇来源可以作为 R0.73N 固定成员定理与族转移障碍的黑箱证明。
这一表述只针对已记录的检索范围，不是穷尽性、首创性或优先权声明。

### Next

下一发布步骤是先把已经通过内部校验的预封存有限诊断绑定到最终核心源提交，
完成 final seal，再制作正式附图并完成图注、源数据绑定、视觉 QA 与公开页面
检查；在这些门禁完成前，有限诊断发布证据、正式附图和公开发布均为 PENDING。
若继续数学研究，应为强迫、非衰减或无限累积应变等结构不同的固定背景重新
冻结问题，而不能把 R0.73M 的现有背景族直接重新标记。

## 14. Exact public boundary

The public note may state:

> Every fixed member of the explicit unforced two-harmonic family has a
> positive full-three-dimensional forward synchronized \((H^3,H^3)\)
> stability tube from \(t_0=0\). R0.73M instead detects nonuniform pointed
> amplification across an unbounded family of marked backgrounds. The
> varying-background theorem therefore cannot be converted into instability
> of one member by the audited quantifier, symmetry, or compactness routes.

It must also state all of the following:

- the full-3D \(H^3\)-in/\(L^2\)-out statement is a custom corollary;
- the planar \((H^3_{\rm pl},L^2_{\rm pl})\) theorem has genuine \(L^2\)
  initial smallness but applies only in the invariant planar subsystem;
- full-three-dimensional FPS \((H^3,L^2)\) stability remains OPEN;
- the stability radius and both local-modulus exponent bounds are not claimed
  sharp;
- the same autonomous Navier--Stokes flow map is evaluated at different
  marked basepoints;
- the obstruction is specific to the registered R0.73M transfer routes;
- finite diagnostics do not certify continuum claims;
- arbitrary-background behavior, transverse critical-norm growth,
  finite-time singularity, and the Clay problem remain OPEN.

The exact public boundary label is `NOT CLAY`.

The public note must not say that R0.73M proves fixed-member Lyapunov
instability, that large finite amplification is instability, that the
full-three-dimensional FPS \((H^3,L^2)\) problem is closed, or that the bounded
source audit establishes novelty or priority.

## 15. Canonical machine-readable boundary

```text
fixedTimeRelativeL2LipschitzBound=CLOSED
finiteAllTimeStrainEnvelope=CLOSED
fixedMemberPlanarL2SynchronizedStability=CLOSED
fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED
fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY
familyFlowMapNonuniformMarkedBasepointSensitivity=CLOSED
familyDepartureImpliesFixedMemberInstability=FALSE_AS_INFERENCE
singleR073mMemberH3SmallL2FixedDistanceEscape=FALSE
amplitudeOnlyIdentificationIsNSSymmetry=FALSE
timeTranslationIdentifiesLambdaFamily=FALSE
parabolicScalingIdentifiesLambdaFamilyOnFixedTorus=FALSE
fullThreeDimensionalFPSH3L2Stability=OPEN
optimalFixedMemberStabilityRadius=OPEN
sharpFamilyLipschitzExponent=OPEN
arbitraryFixedBackgroundInstability=OPEN
transverseCriticalNormGrowth=OPEN
finiteTimeSingularity=OPEN
Clay=OPEN
finiteDiagnosticValidation=VALIDATED_PRESEAL
finiteDiagnosticPackage=PENDING
sourceCommitAssigned=FALSE
finalSeal=FALSE
formalFigurePackage=PENDING
publicRelease=PENDING
```
