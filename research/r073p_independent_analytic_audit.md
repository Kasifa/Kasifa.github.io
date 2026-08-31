# R0.73P independent analytic audit

**Release verdict:** **FORMAL PASS after one documented repair round.**

**Scope:** continuum mathematics and theorem/source quantifiers only.  This
audit does not certify the later formula-diagnostic package, formal figure,
HTML/PDF synchronization, novelty, priority, or any Clay conclusion.

## 1. Files read independently

- `research/r073p_problem_freeze.md`
- `research/r073p_critical_frequency_proof.md`
- `research/r073p_delayed_synchronization_proof.md`
- `research/r073p_literature_audit.md`
- the primary manuscripts of Burczak--Zajączkowski,
  Marín-Rubio--Robinson--Sadowski, and Hoang--Martinez

The reviewer was asked to reconstruct the energy exponents, time quantifiers,
frequency powers, and Sobolev derivative counts rather than merely compare
conclusions.

## 2. First-pass findings and repairs

The first readback found two release-blocking presentation defects, not a
failure of the core theorem.

1. The critical proof had not written the exact conversion between the
   Burczak--Zajączkowski Fourier norm and the released normalized-Haar
   Stokes norm.  The repaired proof now fixes
   \(\mathbb T^3=[0,2\pi]^3\), \(d\mu=(2\pi)^{-3}dx\), copies
   \(K_2^c,K_3^c,K_4^c\), and uses
   \(K_3'=(2\pi)^6K_3^c\).  It also reproduces the theorem's dissipation
   estimate and separates inherited strong regularity from uniqueness.
2. The draft token `backwardPropagationOfRegularity=FALSE` could be mistaken
   for a counterexample to backward regularity.  It was replaced by
   `backwardRegularityInference=NOT_AVAILABLE`: a smooth tail supplies no
   such inference, but no falsehood theorem is claimed.

The same pass requested four smaller repairs: isolate \(M=0\), choose the
small \(H^1\) time in the intersection of the energy-admissible full-measure
sets, define \(Q_{>N}\) and the inherited R0.73O radius, and make the
all-starting-time quantifier explicit.  All were incorporated.

## 3. Relative-energy check

With

\[
 E=\|v-u\|_2^2,\qquad D=|v-u|_1^2,
 \qquad a=\|\nabla u\|_\infty,
\]

the integrated weak--strong inequality is

\[
 {1\over2}E'+D\le aE.
\]

Since \(D\ge E\), the squared norm has exponent
\(-2(t-t_0)+2\int_{t_0}^ta\), hence the released norm estimate has exactly

\[
 \|v(t)-u(t)\|_2
 \le e^{\int_{t_0}^ta}e^{-(t-t_0)}
 \|v(t_0)-u(t_0)\|_2.
\]

No factor of two is missing.  The estimate applies to every Leray--Hopf
comparison selection because the other side is the fixed global strong
reference.

**Decision:** **PASS.**

## 4. Published critical-radius normalization

The paper's coefficient norm on \(Q_{2\pi}\) is exactly the release norm,
whereas its physical Lebesgue gradient satisfies

\[
 \|\nabla u\|_{L^2(dx)}^4=(2\pi)^6|u|_1^4.
\]

For fixed positive
\(\bar\nu,\varepsilon_1,\varepsilon_2\) with
\(\bar\nu+\varepsilon_1+\varepsilon_2<1\), the repaired proof therefore
uses the literal sufficient radius

\[
 R_{\rm BZ}[u]
 ={\bar\nu\over K_2^c}
 \exp\!\left[-{1\over2}K_3^c(2\pi)^6
 \mathcal A_c[u]\right].
\]

The finite orbit action bounds every tail action, so the same radius works
for every finite terminal time and every starting time.  Applying the
published theorem to one global Leray solution and then using critical
uniqueness gives a single global critical solution.

**Decision:** **PASS AS A CLASSICAL COROLLARY.**

## 5. Critical synchronization and H3 persistence

The independently checked bootstrap is

\[
 X'+c_0Y\le C_0|u|_1^4X+C_1XY,
 \qquad X=|w|_{1/2}^2,\quad Y=|w|_{3/2}^2.
\]

After fixing \(C_1\eta\le c_0/2\), the first-exit argument and
\(Y\ge X\) give the released exponential rate; the squared-norm rate
\(c_0/2\) becomes \(c_0/4\) in the norm.  Moreover

\[
 L^\infty H^{1/2}\cap L^2H^{3/2}
 \subset L^4H^1\subset L^4L^6,
\]

and \((4,6)\) satisfies the Serrin equality.  Local \(H^3\) persistence and
weak--strong uniqueness therefore upgrade an \(H^3\) datum inside the
critical tube to a global \(H^3\) solution.

**Decision:** **PASS; the robustness input and persistence route are
classical.**

## 6. Frequency-transfer check

For \(P_{\le N}w_0=w_0\), Parseval gives

\[
 |w_0|_{1/2}\le N^{1/2}\|w_0\|_2,
 \qquad |w_0|_3\le N^3\|w_0\|_2.
\]

Thus the critical and direct R0.73O sufficient gates are respectively
\(R_{1/2}N^{-1/2}\) and \(R_3N^{-3}\).  A single normalized divergence-free
Fourier shear mode attains both norm exponents.  Because that witness is
itself smooth, the audit accepts sharpness only for norm transfer and rejects
any inference of PDE necessity or instability.

The mixed \(L^2+H^s\) and low/high critical-tail inequalities were also
recomputed and are exact.

**Decision:** **PASS AS EXACT COROLLARIES.**

## 7. Uniform eventual regularity and delayed difference ladder

For \(M=0\), energy gives the zero solution directly.  For \(M>0\), the
energy decay and one-unit averaging window produce an energy-admissible
small \(H^1\) time before

\[
 T_{\rm reg}(M)=\bigl(\log(M/\eta_*)\bigr)_++2.
\]

Two more windows produce the common small-\(H^3\) upper time

\[
 T_3(M)=\bigl(\log(M/\eta_*)\bigr)_++4.
\]

The individual entry times may depend on the Leray selection, but their
upper bounds do not.  This quantifier is compatible with Hoang--Martinez
Theorem 2.4; the two numerical start times are not identified.

After \(T_3(M)\), the derivative counts at levels zero through three give

\[
 F_m'+F_{m+1}\le0,\qquad m=0,1,2,3.
\]

Three unit windows transfer the early relative \(L^2\) estimate to \(H^3\),
and the fourth inequality gives

\[
 |v(t)-u(t)|_3
 \le K_u e^{-\frac12(t-T_3(M)-3)}|v_0-u_0|_0,
 \qquad t\ge T_3(M)+3.
\]

This is one-sided against a fixed global strong reference.  It does not
compare two arbitrary weak selections during the unknown early interval.

**Decision:** **PASS.**

## 8. Exact release boundary

The independent audit approves the following and no stronger statements.

```text
allTimeWeakL2RelativeStability=CLOSED_AFTER_AUDIT
globalCriticalH12OrbitStability=CLOSED_AS_CLASSICAL_COROLLARY
criticalH12Synchronization=CLOSED_AFTER_AUDIT
criticalToGlobalH3Propagation=CLOSED_AS_CLASSICAL_COROLLARY
bandLimitedL2ThresholdNMinusHalf=CLOSED_AS_COROLLARY
mixedL2HsThreshold=CLOSED_AS_COROLLARY
lowHighCriticalTailCertificate=CLOSED_AS_COROLLARY
uniformEventualRegularityOnL2Ball=CLOSED_AFTER_AUDIT
uniformEventualSmallH3Entry=CLOSED_AFTER_AUDIT
oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT
normTransferNMinusHalfSharp=CLOSED
PDEDynamicalNMinusHalfSharp=NOT_CLAIMED
arbitraryLerayPairLipschitzSemigroup=NOT_PROVED
uniformL2OnlyStrongThreshold=OPEN_COLLISION_SENSITIVE
earlyWeakIntervalRegularity=OPEN
backwardRegularityInference=NOT_AVAILABLE
arbitraryThreeDimensionalGlobalRegularity=OPEN
clayConclusion=OPEN
noveltyOrPriorityClaim=FORBIDDEN
```

The exact public label remains **NOT CLAY**.
