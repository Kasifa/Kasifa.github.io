# R0.74A — independent audit of the localized \(\mathcal K_D\) size lemma

**Audit date:** 2026-09-01

**Audited source:** `research/r074a_localized_kd_size_lemma.md`

**Canonical comparisons:** `research/r073x_exterior_tail_freeze.md` and
`research/r073z_finiteness_obstruction_and_repair.md`

**Audit mode:** independent analytic reconstruction; no change to the main
proof

**Verdict:** `PASS`

The current source passes the requested analytic gate.  Two issues found
during review -- a missing addition sign in the displayed four-block theorem
and an incomplete inheritance of the pressure-corollary hypotheses -- are
already corrected in the audited source.  No unresolved mathematical blocker
remains within the claim class stated by the note.

---

## 1. Clock and local-energy quantifiers — `PASS`

The note keeps the two clocks distinct:

\[
 I_R^{\rm std}=(t_0-R^2,t_0),\qquad
 I_R^\nu=(t_0-R^2/\nu,t_0).
\]

The same symbol \(\square\in\{{\rm std},\nu\}\) occurs on every left- and
right-hand side.  The hypothesis

\[
 I_{4R}^\square\Subset(0,T)
\]

is now explicit, and the energy-class assumption is imposed on
\(I_{4R}^\square\), not merely on \(I_R^\square\).  Therefore
\(\mathcal E^\square(z_0,4R)\) is defined and finite under the stated
hypotheses, and

\[
 A_c+B_c\le 4\mathcal E^\square(z_0,4R)
\]

follows from both the spatial inclusion \(B_{2R}\subset B_{4R}\) and the
matching-clock inclusion \(I_R^\square\subset I_{4R}^\square\).  No standard
clock is silently substituted for the viscosity-adapted clock.

---

## 2. Exterior-gradient alias and finiteness — `PASS`

The definition

\[
 \mathcal G_{\nabla,{\rm ext}}^{1,\square}
 =\frac{\nu}{R}\int_{I_R^\square}
   \sum_{m\ge1}\gamma_m(\theta)
   \int_{A_m(R)}|\nabla\widetilde u|^2
\]

is term-for-term the R0.73X definition (7.2) of
\(\mathcal D_{\rm ext}^\square\).  The identity in (2.5a) is therefore an
exact alias, not a comparison and not a new tail.  Only
\(\mathcal U_{\rm ext}^{\infty,\square}\) is new.

The cell-count estimate
\(O(1+(2^mR)^3)\), together with the super-geometric Gaussian weight, proves
finiteness of both tails for every fixed \(R>0\) and \(0<\theta\le1\) at the
stated periodic energy level.  This is pointwise finiteness of the selected
tails, not a uniform local estimate.

---

## 3. Positive four-block estimate — `PASS`

The decomposition used in (3.2) is correctly described as a positive
majorization of uncentered moments.  It is not presented as a false exact
core/exterior covariance identity.

Writing

\[
 U_\gamma(t)=\sum_m\gamma_m\int_{A_m}|\widetilde u|^2,
 \qquad
 G_\gamma(t)=\sum_m\gamma_m\int_{A_m}|\nabla\widetilde u|^2,
\]

the kernel bounds give \(U_e\le CR^{-3}U_\gamma\) and
\(G_e\le CR^{-3}G_\gamma\).  Reconstructing the four integrations from the
prefactor \(\nu/R^2\) in \(\mathcal K_D\) gives:

| block | spatial/scale input | resulting dimensionless payment | verdict |
| --- | --- | --- | --- |
| core--core | \(s^{-3/4}\|u\|_{2,B_{2R}}\|\nabla u\|_{2,B_{2R}}^2\), with \(\int_0^{\theta R^2}s^{-3/4}ds=4\theta^{1/4}R^{1/2}\) | \(C\theta^{1/4}A_c^{1/2}B_c\) | `PASS` |
| core--exterior | \(R^{-3/2}U_\gamma^{1/2}\int_{B_{2R}}|\nabla u|^2\), integrated over a scale interval of length \(\theta R^2\) | \(C\theta B_c(\mathcal U_{\rm ext}^{\infty,\square})^{1/2}\) | `PASS` |
| exterior--core | \(s^{-3/4}G_\gamma\|u\|_{2,B_{2R}}\) | \(C\theta^{1/4}A_c^{1/2}\mathcal D_{\rm ext}^\square\) | `PASS` |
| exterior--exterior | \(R^{-3/2}G_\gamma U_\gamma^{1/2}\), integrated over a scale interval of length \(\theta R^2\) | \(C\theta(\mathcal U_{\rm ext}^{\infty,\square})^{1/2}\mathcal D_{\rm ext}^\square\) | `PASS` |

All powers of \(R\) and \(\nu\) cancel.  The first and third rows have the
integrable endpoint factor \(\theta^{1/4}\); the second and fourth rows have
\(\theta\).  The corrected display (4.2) is the sum of exactly these four
terms.

---

## 4. The \(3/2\)-homogeneous merge in (4.4) — `PASS`

Because \(0<\theta\le1\), (4.2) factors as

\[
 C\theta^{1/4}
 \left(A_c^{1/2}+(\mathcal U_{\rm ext}^{\infty,\square})^{1/2}\right)
 \left(B_c+\mathcal D_{\rm ext}^\square\right).
\]

For nonnegative \(a,b,c,d\),

\[
 (a^{1/2}+b^{1/2})(c+d)
 \le C(a+b+c+d)^{3/2}.
\]

Combining this inequality with
\(A_c+B_c\le4\mathcal E^\square(z_0,4R)\) yields exactly

\[
 \mathcal K_D^\square
 \le C\theta^{1/4}
 \left[\mathcal E^\square
 +\mathcal U_{\rm ext}^{\infty,\square}
 +\mathcal D_{\rm ext}^\square\right]^{3/2}.
\]

The exponent is consistent with cubic amplitude homogeneity and with
Navier--Stokes scaling.  No quotient coercivity is inferred from this upper
bound.

---

## 5. Pressure-cutoff corollary (4.17) — `PASS`

The current corollary explicitly adds the hypotheses needed by R0.73X:
\((u,p)\) is a periodic suitable weak solution on
\(\mathbb T^3\times(0,T)\), \(p\in L^{3/2}_{t,x}\), and the common
pressure-tail quantifiers hold.  It also repeats the measurable-scale and
cutoff conditions.

R0.73X (5.7) states

\[
 \frac1R\int_{I_R^\square}\int_{B_R}
 |Q_{s(t)}\cdot\nabla\eta_R|
 \le C_{\theta,C_\eta}\left[
 R^{-2}\int_{I_R^\square}\int_{B_{4R}}|u|^3
 +\mathcal A_{\rm ext}^\square\right].
\]

R0.73X (6.2) pays the local row by
\(C_\nu(\mathcal E^\square(z_0,4R))^{3/2}\).  Adding this to (4.4), and
enlarging the nonnegative bracket, gives (4.17) with precisely

\[
 \left[\mathcal E^\square+
 \mathcal U_{\rm ext}^{\infty,\square}+
 \mathcal D_{\rm ext}^\square\right]^{3/2}
 +\mathcal A_{\rm ext}^\square.
\]

Thus (4.17) faithfully inherits, rather than replaces, the older pressure
and harmonic payment.  In particular, it does not claim that the two
quadratic tails control a general pressure covariance.

---

## 6. Exterior high-frequency packet — `PASS`

For \(B_*\Subset A_2(R)\) disjoint from \(B_{4R}\), the construction

\[
 b_N=\frac{\varepsilon_N}{N}\phi\sin(Ny_1)e_3,
 \qquad w_N=\nabla\times b_N
\]

is smooth, periodic after chart extension, divergence free, and supported
outside \(B_{4R}\).  Its leading oscillatory derivative gives

\[
 \|w_N\|_2+\|w_N\|_3\asymp\varepsilon_N,
 \qquad \|\nabla w_N\|_2\asymp\varepsilon_NN.
\]

The associated periodic Poisson pressure
\(p_N=\mathcal R_i\mathcal R_j(w_{N,i}w_{N,j})\) satisfies the displayed
Poisson equation and
\(\|p_N\|_{3/2}\le C\varepsilon_N^2\) by periodic
Calderon--Zygmund theory.  Hence, on a fixed time interval,

\[
 \mathcal E^\square(z_0,4R)=0,
 \qquad \mathcal A_{\rm ext}^\square=O(\varepsilon_N^3).
\]

On every fixed scale band
\([\alpha R^2,\beta R^2]\), \(0<\alpha<\beta\le\theta\), the periodic heat
kernel has a strictly positive minimum.  The spatial means of a periodic curl
and of its gradient vanish, so the exact variance identities yield

\[
 k_s[w_N]\ge c\varepsilon_N^2,
 \qquad D_s[w_N]\ge c\varepsilon_N^2N^2
\]

uniformly for \(x\in B_R\) on that band.  Therefore
\(\mathcal K_D^\square[w_N]\ge c\varepsilon_N^3N^2\).  With
\(\varepsilon_N=N^{-2/3}\), the left side stays bounded below while the old
right side
\((\mathcal E^\square)^{3/2}+\mathcal A_{\rm ext}^\square\) tends to zero.

The conclusion is correctly restricted to arbitrary periodic energy-class
velocity/Poisson-pressure pairs.  The packet is not an unforced
Navier--Stokes trajectory and is not advertised as a suitable-weak NSE
counterexample.

---

## 7. Exterior time spike — `PASS`

For amplitude \(\delta^{-1/3}\) on a time interval of length \(\delta\),

\[
 \int|w_\delta|^3\asymp1,
 \qquad
 \mathop{\rm ess\,sup}_t\|w_\delta(t)\|_2^2
 \asymp\delta^{-2/3}.
\]

The pressure has quadratic amplitude.  Consequently its
\(L^{3/2}_{t,x}\) contribution, the Gaussian velocity contribution, and the
harmonic \(\Lambda_R^{3/2}\) contribution all scale like the time integral
of the amplitude cubed and remain bounded.  Meanwhile
\(\mathcal U_{\rm ext}^{\infty}\to\infty\).  This correctly demonstrates
that an integrated cubic tail does not supply the essential-time endpoint
used in (4.10).

The exact identities in (5.6) apply to the indicator model; smooth temporal
approximants retain the same powers with fixed comparison constants.  The
sequence has no uniform global \(L_t^\infty L_x^2\) bound, and the note states
this limitation explicitly.

---

## 8. Claim ledger — `PASS`

- `PROVED` is limited to the positive four-block majorization, its four
  estimates, the merged size bound, the inherited pressure interface, the
  larger-class obstruction, and scale invariance.
- `FINITE` is limited to finiteness of the two selected quadratic tails for
  each periodic energy-class field at fixed parameters.  It is not called a
  smaller-cylinder estimate.
- `OPEN` retains local control, smallness/absorption, a blow-up-stable
  replacement for the time supremum, NSE-specific closure, weak stability,
  any near-kernel quotient lower bound, and epsilon regularity.
- `NOT CLAY` explicitly disclaims compactness, epsilon regularity, smoothness,
  and global regularity.

These labels match the mathematics actually established.

---

## 9. Remaining boundary after audit

There is no remaining blocker for the stated R0.74A size lemma.  The exact
boundary is:

1. The theorem is an upper size estimate, not a coercive or absorbable
   inequality.
2. The newly introduced endpoint velocity tail and the reused gradient tail
   are finite, but are not controlled by data on one smaller cylinder.
3. The high-frequency packet excludes the old payment only in the larger
   energy-field/Poisson-pressure class; it does not exclude an
   equation-specific NSE repair.
4. The time spike separates integrated cubic control from a time supremum but
   is not uniform in global Leray energy.
5. The packet lower-bound constant is for fixed \(R,\alpha,\beta\) and the
   fixed torus; no scale-uniform coercive lower bound is proved.
6. The pressure corollary depends on the inherited R0.73X suitable-weak
   pressure decomposition and on \(\mathcal A_{\rm ext}^\square\); it is not
   a consequence of velocity energy alone.
7. Scaling invariance is understood in the standard local/rescaled-periodic
   convention, since arbitrary dilation does not preserve the normalized
   torus as the same global manifold.

**Final gate:** `R074A_INDEPENDENT_AUDIT_PASS`
