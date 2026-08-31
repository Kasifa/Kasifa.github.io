# R0.73O independent analytic audit

**Audit date:** 2026-08-31
**Audited drafts:** r073o_global_orbit_stability_proof.md and
r073o_forced_kolmogorov_contrast.md
**Method:** independent rederivation of every energy and scaling step, direct
inspection of the available FPS and Mucha theorem texts, and an independently
assembled Fourier diagnostic for the Kolmogorov eigenproblem
**Release verdict:** **FORMAL PASS after two documented repair rounds.** The
unforced global-orbit theorem passes analytically. The initial forced draft
failed at the one-sided spectral and invariant-subspace interfaces; Sections
6--7 record the repairs and the final independent readback that supersedes
those initial failure findings.

No statement in this audit is a novelty or priority claim.

## 1. Executive gate table

| ID | Interface | Verdict | Required action |
|---|---|---|---|
| G1 | $H^1\to H^2\to H^3$ energy ladder | **PASS** | Retain the specialized estimates and state that the identities hold a.e. by smoothing/Galerkin approximation. |
| G2 | eventual entry into a small $H^1$ ball | **PASS** | No mathematical change. |
| G3 | finite $\int_0^\infty |u|_4\,dt$ | **PASS** | No mathematical change. |
| G4 | $H^3$ perturbation inequality | **PASS, exposition fix** | Expand the commutator/product derivation so no hidden $H^4$ norm of $w$ is suspected. |
| G5 | bootstrap, continuation, exponential rate | **PASS** | No mathematical change. |
| G6 | one radius for every $t_0\ge0$ | **PASS** | Distinguish the $A^{3/2}$-norm radius from the equivalent standard-$H^3$ radius. |
| F1 | equilibrium, vorticity sign, $N=10,m=7$ scaling | **PASS** | Keep the exact calculation. |
| F2 | certified $R_c$ implies positive spectrum at $R=3.012$ | **PASS after Sections 6--7** | The revised proof uses an Ilyin anchor, complete imaginary-axis exclusion, a uniform spectral rectangle, and Riesz-rank continuation. |
| F3 | FPS transfer to planar $H^3$-small data | **PASS after repair** | FPS is applied on the invariant two-dimensional torus with $n=2,p=2,q=4$, then extended constantly in $z$. |
| F4 | planar global smoothness and fixed $L^2$ escape | **PASS** | The fixed norm conversion and planar global regularity are explicit. |
| M1 | Mucha 2001/2008 collision boundary | **PASS only with current caveat** | Do not transfer the explicit 2008 norm dependence to the unread 2001 theorem. |

## 2. Unforced global-orbit proof

### 2.1 The $H^1$, $H^2$, and $H^3$ ladder — PASS

On the mean-zero standard torus, $A=-\Delta$ on solenoidal fields and
$|z|_{m+1}\ge |z|_m$. The nonlinear estimates have the correct derivative
count:

\[
 |(B(u,u),Au)|
 \le C\|u\|_6\|\nabla u\|_3\|Au\|_2
 \le C|u|_1^{3/2}|u|_2^{3/2},
\]

\[
 \|B(u,u)\|_{H^1}\le C|u|_2^2,
 \qquad
 \|B(u,u)\|_{H^2}\le C|u|_3^2.
\]

Testing at Stokes levels one, two, and three and using

\[
 |u|_2^2\le |u|_1|u|_3,
 \qquad
 |u|_3^2\le |u|_2|u|_4
\]

gives

\[
\begin{aligned}
 \tfrac12 (|u|_1^2)' + |u|_2^2
 &\le C_1|u|_1^{3/2}|u|_2^{3/2},\\
 \tfrac12 (|u|_2^2)' + |u|_3^2
 &\le C_2|u|_1|u|_3^2,\\
 \tfrac12 (|u|_3^2)' + |u|_4^2
 &\le C_3|u|_2|u|_4^2.
\end{aligned}
\]

There is no circular use of the desired $L^1_tH^4$ conclusion. The assumed
$L^2_{\rm loc}H^4$ regularity justifies the top identity a.e.; smooth
approximation supplies the standard limiting argument.

### 2.2 Late smallness and decay — PASS

The energy equality gives

\[
 \int_0^\infty |u(t)|_1^2\,dt<\infty.
\]

Continuity in $H^3$ supplies $T_1$ with $|u(T_1)|_1<\eta$. Young's
inequality gives

\[
 \tfrac12(|u|_1^2)'+\tfrac12|u|_2^2
 \le K_1|u|_1^6.
\]

If $K_1\eta^4\le1/4$, then on the $\eta$-ball the right-hand side is at
most $\frac14|u|_2^2$. The ball is forward invariant, and Poincare gives
exponential $H^1$ decay. The second ladder inequality gives exponential
$H^2$ decay. A finite $T_2$ then satisfies
$C_3|u(T_2)|_2\le1/2$, and the third inequality gives exponential $H^3$
decay. Every quantifier in this bootstrap is valid.

### 2.3 Finite accumulated $H^4$ action — PASS

For $t\ge T_2$, put $Q=|u|_3^2$ and $W=|u|_4^2$. The draft has

\[
 Q'+W\le0,
 \qquad W\ge Q.
\]

For $0<\beta<1$,

\[
 \frac d{dt}\big(e^{\beta(t-T_2)}Q\big)
 +(1-\beta)e^{\beta(t-T_2)}W\le0.
\]

Consequently,

\[
 \int_{T_2}^\infty |u(t)|_4\,dt
 \le \frac{|u(T_2)|_3}{\sqrt{\beta(1-\beta)}}.
\]

On $[0,T_2]$, Cauchy--Schwarz and $L^2_{\rm loc}H^4$ close the finite
interval. This proves the claimed action without finite-dimensional input.

### 2.4 The $H^3$ perturbation energy — PASS, exposition fix required

For $w=v-u$, a multi-index or Kato--Ponce expansion at order three gives

\[
\begin{aligned}
 |\langle \Lambda^3(u\cdot\nabla w),\Lambda^3w\rangle|
 &\le C\|u\|_{H^3}\|w\|_{H^3}^2,\\
 |\langle \Lambda^3(w\cdot\nabla u),\Lambda^3w\rangle|
 &\le C\|u\|_{H^4}\|w\|_{H^3}^2,\\
 |\langle \Lambda^3(w\cdot\nabla w),\Lambda^3w\rangle|
 &\le C\|w\|_{H^3}^3.
\end{aligned}
\]

The leading term $u\cdot\nabla\Lambda^3w$ cancels by incompressibility.
Mean-zero norm equivalence and Poincare give
$\|u\|_{H^3}\lesssim |u|_4$, while $X=|w|_3^2\le Y=|w|_4^2$.
Therefore

\[
 \tfrac12X'+Y
 \le C_*|u|_4X+C_*X^{1/2}Y.
\]

The inequality is correct. The current schematic $A^{3/2}B$ display should
be expanded as above because, read literally at the endpoint regularity, it
can look as if $B(u,w)\in H^3$ were used without transport cancellation.

### 2.5 Bootstrap, continuation, and all starting times — PASS

On $X^{1/2}\le(2C_*)^{-1}$, absorption gives

\[
 X'+Y\le2C_*|u|_4X.
\]

Hence

\[
 X(t)^{1/2}
 \le e^{C_*\int_{t_0}^t|u(s)|_4ds}X(t_0)^{1/2}.
\]

The radius

\[
 R_A[u]=(4C_*)^{-1}e^{-C_*\mathcal A_4[u]}
\]

strictly improves the bootstrap bound from $(2C_*)^{-1}$ to
$(4C_*)^{-1}$. Since $Y\ge X$, the retained dissipation yields

\[
 |w(t)|_3\le
 e^{C_*\mathcal A_4[u]}e^{-(t-t_0)/2}|w(t_0)|_3.
\]

A bounded $H^3$ norm on every finite interval invokes the standard local
continuation alternative, so $v$ is global. Finally,

\[
 \int_{t_0}^\infty |u(s)|_4ds\le\mathcal A_4[u]
\]

is independent of $t_0$. Thus one radius works for every starting time.
The numerical value $R_A[u]$ is a radius in the homogeneous Stokes norm;
norm equivalence gives a positive, generally rescaled, radius in the usual
inhomogeneous $H^3$ norm. The prose should not identify those numeric radii.

**Unforced theorem decision:** **PASS after exposition-only edits.** It is a
conditional stability theorem around an already-global orbit, not a
continuation criterion for arbitrary local data and not an $L^2$-only input
theorem.

## 3. Forced Kolmogorov contrast

### 3.1 Equilibrium and vorticity sign — PASS

For

\[
 U=(A\sin Ny,0),
 \qquad w=(\psi_y,-\psi_x),
\]

the scalar vorticities are $\Omega=-AN\cos Ny$ and
$\zeta=-\Delta\psi$. Linearizing

\[
 \partial_t\omega+u\cdot\nabla\omega
 =\nu\Delta\omega+\operatorname{curl}f
\]

gives

\[
 \partial_t(-\Delta\psi)
 +A\sin Ny\,\partial_x(-\Delta\psi)
 -AN^2\sin Ny\,\partial_x\psi
 =-\nu\Delta^2\psi.
\]

After multiplication by $-1$ and insertion of $e^{\lambda t}$, this is

\[
 \lambda\Delta\phi-\nu\Delta^2\phi
 +A\sin Ny(\Delta+N^2)\partial_x\phi=0.
\]

Thus the signs agree with Nagatou's stream-function convention. The direct
steady calculation $(U\cdot\nabla)U=0$ and $-\Delta U=N^2U=f$ also passes.

### 3.2 Geometry and nondimensionalization — PASS

With $X=Nx$, $Y=Ny$,

\[
 \sigma=\frac{\lambda}{AN},
 \qquad R=\frac{A}{\nu N},
\]

division by $AN^3$ gives

\[
 \sigma\Delta_{X,Y}\phi-\frac1R\Delta_{X,Y}^2\phi
 +\sin Y(\Delta_{X,Y}+I)\partial_X\phi=0.
\]

The physical subspace

\[
 e^{i7x}\sum_{k\in\mathbb Z}c_ke^{i10ky}
\]

has nondimensional $X$-wave number $\alpha=m/N=7/10$. Although $X=Nx$
traverses several copies of Nagatou's rectangle, its period
$2\pi/\alpha=20\pi/7$ divides the physical $X$-period $20\pi$ exactly.
This is a standard-cube embedding, not an aspect-ratio approximation. Also

\[
 R=30.12/10=3.012,
 \qquad
 \lambda=AN\sigma=301.2\sigma.
\]

### 3.3 Initial neutral-enclosure audit — FAIL, superseded by Sections 6--7

Nagatou directly supports the eigenproblem, exchange-of-stability statement,
and enclosure

\[
 R_c\in[3.011528364444,3.011528364446]
 \quad(\alpha=0.7).
\]

The paper verifies a zero eigenvalue at a locally unique Reynolds number.
The quoted exchange-of-stability proposition says only

\[
 \Re\sigma\ge0\Longrightarrow\sigma\in\mathbb R.
\]

It does **not** by itself say on which side of $R_c$ the real eigenvalue is
positive, nor rule out tangency at zero. Thus the current inference

\[
 \text{exchange of stability}+3.012>R_c
 \Longrightarrow \sigma>0
\]

has a missing logical edge.

One of the following closes it:

1. quote an exact Meshalkin--Sinai/continued-fraction theorem in the same
   normalization stating that the basic flow is spectrally stable for
   $R<R_c(\alpha)$ and has a positive real eigenvalue for every
   $R>R_c(\alpha)$; or
2. certify simplicity plus a strictly positive enclosure for
   $\partial_R\sigma(R_c)$, together with an analytic continuation enclosure
   reaching $R=3.012$.

Watanabe's later prose that the basic flow “loses stability” at this critical
value is strong corroboration, but the release theorem should expose the exact
one-sided theorem instead of making the exchange proposition carry more than
it states.

An independent, non-rigorous Fourier diagnostic supports the intended sign.
For $\kappa_j^2=\alpha^2+j^2$, the truncated matrix was

\[
 \sigma c_j=-\frac{\kappa_j^2}{R}c_j
 +\frac{\alpha}{2\kappa_j^2}
 \left[(1-\kappa_{j-1}^2)c_{j-1}
 -(1-\kappa_{j+1}^2)c_{j+1}\right].
\]

For cutoffs $10,20,40,80,120$, the rightmost eigenvalue at $R=3.012$
agrees to the displayed precision:

\[
 \sigma_{\max}\approx3.732723642\times10^{-5},
 \qquad
 \lambda_{\max}\approx1.124296361\times10^{-2}.
\]

At $R=3.011$ it is approximately
$-4.182951063\times10^{-5}$, and at the midpoint of the certified interval
it is $O(10^{-13})$. This checks the signs and scaling factors, but it has no
interval tail bound and is **diagnostic only**.

### 3.4 Initial FPS audit — FAIL as written, repaired in Sections 6--7

FPS Theorem 2.2 says that right-half-plane $L^p$ spectrum implies
$(L^q,L^p)$ nonlinear instability for $q>\max\{p,n\}$. The finite-domain
proof selects an eigenvalue with maximal positive real part in the phase space
on which the theorem is applied. If it is applied directly to the full
three-dimensional operator with $n=3$, the selected rightmost eigenfunction
need not be planar. One planar positive eigenfunction does not justify the
next sentence that scalar multiples of that planar eigenfunction are the FPS
witnesses in the full-space proof.

The correction is exact:

1. apply FPS on the invariant two-dimensional torus, with
   $n=2,p=2,q=4$; the positive Kolmogorov eigenvalue belongs to that
   operator and $4>\max\{2,2\}$;
2. use the finite-domain construction $v_0=\epsilon\phi$ to obtain smooth
   planar data tending to zero in every fixed smooth norm and a fixed 2D
   $L^2$ escape;
3. extend the force, equilibrium, data, and solutions constantly in $z$.

For the standard $2\pi$-periodic $z$ direction, unnormalized norms obey

\[
 \|g(x,y)\|_{L^2(\mathbb T^3)}
 =(2\pi)^{1/2}\|g\|_{L^2(\mathbb T^2)},
\]

with an analogous fixed factor for $H^3$. Small input and fixed escape
survive the embedding. Classical 2D periodic regularity makes every witness
global and smooth; strong uniqueness identifies it with the planar 3D
solution. After this repair, the full-phase-space instability statement is
valid even though the witnessing subspace is planar.

**Initial forced-theorem decision:** **FAIL CLOSED until F2 and F3 are
repaired.** Neither issue challenged the exact equilibrium or scaling. The
repairs and the superseding final decision appear in Sections 6--7.

## 4. Mucha 2001/2008 collision boundary

### 4.1 What is directly checked — PASS

The accessible Mucha 2008 Theorem 1.2 explicitly assumes that

\[
 \|v_0\|_{L^2}
 \quad\text{is sufficiently small compared with}\quad
 \|v_0\|_{B^{2-2/q}_{p,q}}.
\]

Thus that exact theorem does not provide one $L^2$ threshold uniform over
arbitrarily large trace norms. Its text also says that similar earlier
considerations covered the torus and $\mathbb R^3$ in
$W^{2,1}_{p,p}$-spaces.

### 4.2 What is not directly checked — retain the caveat

The full Mucha 2001 theorem text was unavailable in the audited source cache.
Its publisher abstract says only that the perturbation's $W^{2,1}_r$ norm is
controlled when the initial perturbation is sufficiently small in $L^2$.
An abstract does not specify whether the threshold is uniform over the
regular input class or depends on its high norm.

Mucha 2008 is evidence for the dependence pattern of its own stated method;
it is not a logical substitute for the exact quantifiers of the unread 2001
theorem. The following wording passes:

> No exact theorem statement checked in this bounded audit establishes a
> uniform $L^2$-only threshold over arbitrary regular perturbations; Mucha
> 2001 remains the closest unresolved collision because its full theorem
> quantifiers were not inspected.

The following stronger language fails:

- “Mucha 2001's threshold depends on the $H^3$ or trace norm”;
- “the literature contains no uniform $L^2$-only theorem”;
- “Mucha 2008 resolves the exact Mucha 2001 quantifiers.”

This source-access caveat does not affect the internal validity of the
unforced $H^3$-tube theorem. It affects only collision, novelty, and the
status of the uniform FPS $(H^3,L^2)$ cell.

## 5. Required revisions before the analytic gate could pass

1. In the unforced proof, replace the schematic background estimates by the
   explicit transport-commutator bounds in Section 2.4 and state the
   standard-$H^3$ radius with its norm-equivalence factor.
2. In the forced proof, add a theorem-grade supercritical-side result in the
   exact Nagatou normalization; do not infer it from exchange of stability
   alone.
3. Change the FPS invocation from $n=3$ to the invariant planar problem with
   $n=2,p=2,q=4$, then embed the global solutions in $\mathbb T^3$.
4. Label finite eigenvalues as nondimensional $\sigma$; if physical time is
   plotted, multiply by $AN=301.2$.
5. Keep Mucha 2001 COLLISION-SENSITIVE until its exact theorem is read; use
   Mucha 2008 only for its own explicit dependence statement.

Items 1--5 were incorporated and independently read back in Sections 6--7.
The final forced conclusion uses theorem-grade spectral continuation rather
than the floating-point sign check.

## 6. Post-remediation audit --- 2026-08-31

This section audits only Sections 4--5 of the revised forced Kolmogorov-flow
draft. It supersedes the earlier F2--F3 failure findings to the extent stated
below.

### 6.1 One-sided positive-spectrum chain --- PASS after precision edits

The mathematical chain is sound. Ilyin supplies a finite high-\(R\) anchor
with nonzero right-half-plane spectrum. On a compact parameter interval, the
common-domain elliptic family has compact resolvent and continuous Riesz
projections; Nagatou Proposition 2.1 implies that an eigenvalue on the
imaginary axis must be real, hence it excludes every nonzero imaginary-axis
crossing. At zero, the Matsuda--Miyatake recurrence and Proposition 1 give
the complete mode test: for \(\alpha=0.7\), the \(|m|=1\) block is neutral
only at \(\lambda(0.7)=R_c\), while \(|m|\geq2\) has
\(\beta=|m|\alpha\geq1\) and admits no nonzero neutral sequence. Therefore
the right-half-plane Riesz rank present at the Ilyin anchor cannot vanish on
\((R_c,R_H]\), and \(R=3.012>R_c\) has positive real spectrum.

The following exact edits are nevertheless required before the present prose
earns an unconditional publication PASS.

1. **Ilyin normalization.** State the theorem directly at \(L=2\pi\):
   \(f=(\Lambda\nu^2\sin x_2,0)\),
   \(U=(\Lambda\nu\sin x_2,0)\), and hence \(R=\Lambda\).
   The current general-\(L\) sentence omits the Laplacian scaling factors and,
   as written, its displayed force and equilibrium do not satisfy the steady
   equation for arbitrary \(L\).
2. **What is continued.** Replace “positive spectral count” by “the total
   algebraic multiplicity of spectrum in \(\{\Re z>0\}\), equivalently the
   rank of the corresponding Riesz projection.” Ilyin's count of distinct
   eigenvalues is sufficient to make that rank nonzero at \(R_H\), but a
   count of distinct eigenvalues need not remain constant under collisions
   inside the open right half-plane.
3. **Compact-interval spectral confinement.** Add that the common-domain
   analytic elliptic family has a uniform high-frequency sectorial bound on
   \([3.012,R_H]\). This prevents relevant eigenvalues from escaping through
   infinity and makes the Riesz-rank continuation argument complete.
4. **All Fourier sectors.** Matsuda--Miyatake formulate their recurrence in
   an inversion-even/cosine sector. Explicitly add that translation symmetry
   gives the identical inversion-odd/sine copy, negative \(m\) are conjugate
   copies, and the \(m=0\), \(\sigma=0\) equation is
   \(-R^{-1}\Delta^2\phi=0\), whose only periodic stream functions are gauge
   constants removed by normalization. Only after these observations does
   the zero-crossing exclusion cover the full planar phase space.

The identity \(R_c=\lambda(0.7)\) follows from the identical zero recurrence
and Matsuda--Miyatake uniqueness; Watanabe is useful corroboration but is not
needed as an additional logical premise. With edits 1--4, the conclusion
“the operator at \(R=3.012\) has at least one positive real eigenvalue” is
**PASS**. Without them, the chain is substantively correct but its written
normalization and full-sector/Riesz-projection justification remain
**CONDITIONAL PASS**, not CLOSED.

### 6.2 FPS in two dimensions and constant extension --- PASS

The revised order is correct. Applying Friedlander--Pavlović--Shvydkoy on
the invariant planar problem with \(n=2,p=2,q=4\) satisfies
\(q>\max\{p,n\}\). The smooth unstable eigenfunction may be scaled so the
initial data tend to zero in each prescribed fixed Sobolev norm while the
theorem retains a fixed \(L^2\) escape. Constant extension in \(z\) multiplies
the unnormalized \(L^2\) norm and the standard derivative-sum \(H^3\) norm by
\((2\pi)^{1/2}\) (or by the corresponding fixed factor under normalized
measure), so smallness and fixed escape both survive. Invariance of the
planar subspace, global two-dimensional smoothness, and strong uniqueness
then give global smooth three-dimensional witnesses.

For maximal precision, read “tending to zero in every fixed Sobolev norm” as
“for each fixed Sobolev index \(s\), tending to zero in \(H^s\).” This is a
wording clarification, not a mathematical defect. Section 5 is therefore
**PASS**.

## 7. Post-remediation final audit --- 2026-08-31

This is an independent readback of the further-revised Sections 4--5.  The
four qualifications in Section 6.1 have now been repaired.

### 7.1 Source normalization and anchor --- PASS

The Ilyin theorem is now specialized before parameters are identified:
\(L=2\pi\), \(f=(\Lambda\nu^2\sin x_2,0)\),
\(\bar U=(\Lambda\nu\sin x_2,0)\), forcing wave number \(N=1\), and hence
\(R=A/(\nu N)=\Lambda\).  No unsupported general-\(L\) formula remains.
Ilyin is used only to assert that the right-half-plane spectral subspace is
nonzero at one finite \(R_H\), not to continue his count of distinct
eigenvalues.  This is exactly the permissible use of that source.

### 7.2 Operator continuation --- PASS

The velocity operator is placed on one fixed complex, divergence-free,
mean-zero Hilbert space with common domain \(H^2\cap H\).  The displayed
relative-bound-zero estimate makes \(R\mapsto\mathcal A_R\) a type-(A)
analytic family.  The uniform large-real-\(\mu\) resolvent factorization on
compact \(R\)-intervals establishes compact resolvent and norm-resolvent
continuity.

The energy identity gives, for every eigenvalue with
\(\operatorname{Re}\zeta\geq0\),

\[
 0\leq\operatorname{Re}\zeta\leq1,\qquad
 |\operatorname{Im}\zeta|\leq\sqrt{R_H}+1.
\]

Thus all closed-right-half-plane spectrum lies in one compact rectangle,
uniformly on \([3.012,R_H]\); spectral escape through infinity is excluded.
Once the imaginary axis is shown to be free of spectrum, failure of a
uniform gap would produce convergent \(R_j,\zeta_j\) in that rectangle and,
by norm-resolvent continuity, an imaginary-axis spectral point at the limit.
The resulting \(\delta>0\) makes the single displayed contour valid for every
parameter.  Its Riesz projection varies continuously, so its finite rank,
equal to total algebraic multiplicity in the open right half-plane, is
constant.  The proof does not claim that the number of distinct eigenvalues
is invariant.  This closes the continuation argument.

### 7.3 Complete imaginary-axis exclusion --- PASS

Nagatou Proposition 2.1 reduces all possible imaginary-axis spectrum to
zero.  At zero, the revised Matsuda--Miyatake argument covers the complete
Fourier space:

- the cited cosine sector has the stated recurrence;
- \(x\)-translation supplies the identical sine sector;
- negative horizontal modes are conjugate copies;
- the \(m=0\) equation has only constant stream functions, which represent
  zero velocity and are removed as gauge.

For \(\alpha=0.7\), the only \(|m|=1\) neutral value is
\(R=\lambda(0.7)=R_c<3.012\), while every \(|m|\geq2\) has
\(\beta=|m|\alpha\geq1\) and no nonzero neutral sequence.  Therefore no
imaginary-axis eigenvalue exists for any \(R\in[3.012,R_H]\).  Together with
Sections 7.1--7.2, this proves
\(\operatorname{rank}\Pi_{3.012}>0\).  Nagatou then makes every eigenvalue in
the closed right half-plane real, so the conclusion is a positive **real**
eigenvalue, not merely an eigenvalue of positive real part.

### 7.4 FPS and constant extension --- PASS

The application \(n=2,p=2,q=4\) satisfies
\(q>\max\{p,n\}\) and is made first in the invariant planar system.  Scaling
the fixed smooth unstable eigenfunction gives arbitrarily small data in each
fixed Sobolev norm while FPS retains fixed \(L^2\) escape.  Constant
\(z\)-extension changes both \(H^3\) and \(L^2\) norms only by the stated
fixed measure factor.  Planar invariance, global two-dimensional regularity,
and strong uniqueness give global smooth three-dimensional solutions
realizing that escape.  No three-dimensional global-regularity assumption is
being smuggled into the argument.

### 7.5 Final decision and exact claim boundary

**FORMAL PASS.**  All six requested checks are now sufficient, and the
earlier forced-theorem FAIL/CLOSED qualifications are superseded for this
revised proof.

The proof permits the following exact conclusions:

1. at \(R=3.012\), the planar linearized Kolmogorov operator has at least one
   positive real eigenvalue of finite algebraic multiplicity and a smooth
   eigenfunction;
2. the same eigenpair belongs, by constant extension, to the full
   three-dimensional linearized operator;
3. the forced equilibrium has nonlinear instability witnessed by globally
   smooth planar solutions that start \(H^3\)-small and achieve a fixed
   \(L^2\) escape.

It does **not** establish algebraic simplicity of the positive eigenvalue,
an essentially three-dimensional unstable mode or mechanism, instability of
an unforced orbit, finite-time singularity, or any advance on the Clay
Navier--Stokes regularity problem.  The Fourier truncation remains diagnostic
only and is not part of the proof.
