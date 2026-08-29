# R0.73F problem freeze: a moving-profile dichotomy on a fixed physical window

**Frozen:** 2026-08-30  
**Parent release:** R0.73E  
**One permitted row:** \(\gamma=1/2\), \(\beta=\xi=0\), first for
\(s=+1\) and then for \(s=-1\) by complex conjugation  
**Evidence target:** an exact evolution-family theorem; finite Fourier
calculations remain diagnostic only

## 1. Input inherited from R0.73E

On \(H=L^2(\mathbb T_{2\pi})\), let

\[
 L=-\partial_x^2+\frac14,
 \qquad
 \widetilde B_\varepsilon(d)=\widetilde A(d)-\varepsilon L,
 \qquad
 D(\widetilde B_\varepsilon(d))=H^2_{\rm per},
 \tag{1.1}
\]

where \(\varepsilon=|\Lambda|^{-1}\) and

\[
 W(d,x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x.
 \tag{1.2}
\]

The exact profile drift is bounded on \(H\) and satisfies

\[
 \|\widetilde A(d)-\widetilde A(0)\|
 \le C_A d,
 \qquad C_A=\frac{49}{4}.
 \tag{1.3}
\]

At \(d=0\), R0.73E proved a complete top-cluster relative dichotomy.  There
are numbers

\[
 0<b<c<a
 \tag{1.4}
\]

and, for all sufficiently small \(\varepsilon>0\), a finite-rank top Riesz
projection \(P_\varepsilon\), with \(Q_\varepsilon=I-P_\varepsilon\), such
that

\[
 \|e^{t\widetilde B_\varepsilon(0)}Q_\varepsilon\|
 \le K e^{bt},
 \qquad
 \|e^{-t\widetilde B_\varepsilon(0)}P_\varepsilon\|
 \le K e^{-ct},
 \qquad t\ge0,
 \tag{1.5}
\]

with one \(K\) independent of small \(\varepsilon\).  No simplicity or
rightmost-branch identification is assumed.

Choose once and for all

\[
 b<\alpha<c,
 \qquad
 \nu=\min\{\alpha-b,c-\alpha\}>0,
 \tag{1.6}
\]

and put

\[
 C_\varepsilon=\widetilde B_\varepsilon(0)-\alpha I.
 \tag{1.7}
\]

Then \(C_\varepsilon\) has an \(\varepsilon\)-uniform exponential
dichotomy: \(Q_\varepsilon H\) is forward stable and
\(P_\varepsilon H\) is backward stable, both with rate \(\nu\).

## 2. The decisive distinction

A pointwise spectral gap for every frozen generator is not enough to control a
nonautonomous evolution.  R0.73F may use the stronger input (1.5), which is a
family-uniform semigroup dichotomy with a common prefactor.  It must also use
the smallness of the whole bounded perturbation on a short physical window,
not only the slow derivative of that perturbation.

In fast time \(\theta=|\Lambda|d\), the exact moving equation is

\[
 q'(\theta)=
 \left[\widetilde B_\varepsilon(0)+D_\varepsilon(\theta)\right]q(\theta),
 \qquad
 D_\varepsilon(\theta)
 =\widetilde A(\varepsilon\theta)-\widetilde A(0).
 \tag{2.1}
\]

For \(0\le \theta\le d_0/\varepsilon\),

\[
 \sup_\theta\|D_\varepsilon(\theta)\|\le C_A d_0.
 \tag{2.2}
\]

Thus a sufficiently small but \(\varepsilon\)-independent \(d_0>0\) places
the complete moving interval inside the roughness radius of the frozen
dichotomy.  The interval may have fast length \(d_0/\varepsilon\); the
roughness theorem is uniform in that length.

## 3. Exact theorem contract F1: bounded-perturbation roughness

The section must prove, or cite with every hypothesis checked, the following
Banach-space lemma.

Let \(C\) generate an exponentially bounded semigroup on a Banach space and
suppose it has a dichotomy projection \(P\) satisfying

\[
 \|e^{tC}(I-P)\|\le K e^{-\nu t},
 \qquad
 \|e^{-tC}P\|\le K e^{-\nu t},
 \qquad t\ge0.
 \tag{3.1}
\]

There is \(\rho_0=\rho_0(K,\nu)>0\) such that every norm-continuous
\(D:\mathbb R\to\mathcal B(H)\) with
\(\sup_t\|D(t)\|<\rho_0\) generates an exponentially bounded evolution
family \(V_D(t,s)\) having a dichotomy

\[
 \|V_D(t,s)Q_D(s)\|\le K_1e^{-\nu_1(t-s)},
 \qquad t\ge s,
 \tag{3.2}
\]

and

\[
 \|V_D(s,t)P_D(t)\|\le K_1e^{-\nu_1(t-s)},
 \qquad t\ge s.
 \tag{3.3}
\]

Here \(P_D(t)=I-Q_D(t)\) is the unstable projection, the evolution restricted
to its range is invertible, and \(K_1,\nu_1>0\) depend only on the frozen
constants and the selected roughness radius.  When \(P\) has finite nonzero
rank, \(P_D(t)\) must have the same rank.

The proof must cover the present noninvertible parabolic stable evolution.  It
may not assume a two-sided group on all of \(H\).

## 4. Exact theorem contract F2: instantaneous spectral strip and contour

The same sufficiently small \(d_0\) must give all instantaneous generators
\(\widetilde B_\varepsilon(d)\), \(0\le d\le d_0\), one common spectral
strip around the shift \(\alpha\), with an \(m\)-dimensional unstable part.
One fixed finite contour must define the complete unstable Riesz projection

\[
 P_\varepsilon^{\rm inst}(d)
 =\frac1{2\pi i}\int_\Gamma
 (z-\widetilde B_\varepsilon(d))^{-1}\,dz,
 \tag{4.1}
\]

with

\[
 \sup_{\substack{0<\varepsilon<\varepsilon_0\\0\le d\le d_0}}
 \left(
 \|P_\varepsilon^{\rm inst}(d)\|
 +\|\partial_dP_\varepsilon^{\rm inst}(d)\|
 \right)<\infty.
 \tag{4.2}
\]

This is a statement in \(\mathcal B(H)\).  No unscaled \(H^2\) graph-norm
transport may be inferred from it.

## 5. Exact theorem contract F3: moving-profile evolution dichotomy

Extend \(D_\varepsilon\) from
\([0,d_0/\varepsilon]\) to all of \(\mathbb R\) by constants at the two
endpoints.  Choose \(d_0>0\) so that

\[
 C_A d_0<\rho_0(K,\nu).
 \tag{5.1}
\]

Apply F1 to

\[
 C_\varepsilon+D_\varepsilon(\theta)
 =\widetilde B_\varepsilon(\varepsilon\theta)-\alpha I.
 \tag{5.2}
\]

The resulting projections \(P_\varepsilon^{\rm mov}(\theta)\) must have the
same positive finite rank as the frozen top projection.  For
\(0\le s\le t\le d_0/\varepsilon\), the unshifted exact evolution
\(U_\varepsilon(t,s)\) must satisfy

\[
 \left\|
 \left(U_\varepsilon(t,s)|_{P_\varepsilon^{\rm mov}(s)H}\right)^{-1}
 P_\varepsilon^{\rm mov}(t)
 \right\|
 \le K_1e^{-(\alpha+\nu_1)(t-s)}.
 \tag{5.3}
\]

Equation (5.3) is the required moving-profile unstable-bundle estimate.  The
projection is a dynamical dichotomy projection.  It need not equal the
instantaneous frozen Riesz projection at \(d=\varepsilon t\).

## 6. Exact theorem contract F4: fixed-window exponential lower law

Let

\[
 G_{1/2}(\Lambda;D)
 =\sup_{0\le d\le D}
 \|U_{1/2,\Lambda}(d,0)\|_{\mathcal K_{1/4}\to\mathcal K_{1/4}}.
 \tag{6.1}
\]

For a fixed observation window \(D>0\), put

\[
 d_D=\min\{D,d_0\},
 \qquad T_{\varepsilon,D}=d_D/\varepsilon.
 \tag{6.2}
\]

Choose a unit vector
\(v\in P_\varepsilon^{\rm mov}(0)H\).  Invertibility on the moving unstable
bundle and (5.3) must give

\[
 \|U_\varepsilon(T_{\varepsilon,D},0)v\|
 \ge K_1^{-1}
 \exp\left((\alpha+\nu_1)\frac{d_D}{\varepsilon}\right).
 \tag{6.3}
\]

After the exact kinetic-space isometry, the invariant \(\xi=0\) OS--Squire
embedding, and complex conjugation for the two signs, the final statement must
be

\[
 \boxed{
 G_{1/2}(\Lambda;D)
 \ge K_1^{-1}
 \exp\left(\kappa_D|\Lambda|\right),
 \qquad
 \kappa_D=(\alpha+\nu_1)\min\{D,d_0\}>0,
 }
 \tag{6.4}
\]

for every fixed \(D>0\) and all sufficiently large \(|\Lambda|\), for both
signs of \(\Lambda\).

## 7. Mandatory adversarial checks

The final proof and audit must explicitly reject both invalid shortcuts:

1. pointwise frozen spectral separation without a uniform resolvent or
   semigroup prefactor;
2. pointwise positive frozen spectral abscissa without a uniform dynamical
   unstable bundle.

At least one exact finite-dimensional counterexample or cited theorem must be
included for each failure.  These counterexamples delimit the proof; they are
not evidence about the Fourier row itself.

## 8. Claim boundary

Even if F1--F4 close, the result concerns one exact linear Fourier row and a
family of background shears whose amplitude \(|\Lambda|\) tends to infinity.
It does not prove any of the following:

- that the certified inviscid eigenvalue \(\sigma_*\) is simple or rightmost;
- a complete all-row OS--Squire \(A_2\) direct-sum closure or a matching
  fixed-window lower bound across all rows;
- nonlinear control of mode convolution;
- finite-time singularity formation for one Navier--Stokes solution;
- failure of global regularity, or the Clay problem.

The next nonlinear gate may use (6.4) only after converting this family-level
linear amplification into a closed nonlinear instability statement with a
specified topology and remainder estimate.
