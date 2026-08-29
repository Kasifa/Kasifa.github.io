# R0.73B independent analytic audit: Bloch carrier and physical kinetic finite transients

**Date:** 2026-08-29

**Role:** independent re-derivation of
`research/r073b_report-source.md` and
`research/r073b_kinetic_form_proof.md`.

**Decision:** **ANALYTIC PASS AFTER REQUIRED SCOPE AND PROOF EDITS.**  The
Bloch cancellation, transformed signs, physical-energy factor, heat
primitive, direct-sum constant, shear-form limit, trial-plane threshold, and
fixed-\(c\) divergence were independently recovered.  The release source has
been amended for the endpoint multiplicity, homogeneous-forcing scope,
infinite tail estimate, mild-solution domain, and fixed-\(c\) continuity
lemma.  This audit is not a numerical certificate or release authorization.

No literature assertion is used in the mathematical decisions below.

---

## 0. Decision ledger

| Item | Decision | Independent conclusion |
|---|---|---|
| Bloch zero-lattice cancellation | PASS | both integrations by parts and the \(+2i\beta\) sign are exact |
| physical orientation factor | PASS WITH SCOPE | \(|2c\beta/g|\le|\Lambda|\) regularizes homogeneous coupling; forcing still pays \(g^{-1}\Pi_0F_q\) |
| hybrid \(X_g\) transient constants | PASS | \(C_c=4e^{-d}+43e^{-4d}/8\), \(C_\Lambda=e^{-d}+e^{-4d}\) |
| Bloch endpoint language | REQUIRED EDIT APPLIED | \(\beta=-1/2\) is included and has a tied lowest eigenvalue; the chosen carrier is not unique there |
| physical kinetic energy identity | PASS | no missing factor two; valid in primitive components including exceptional rows |
| forced row estimate | PASS WITH HYPOTHESIS | use physical projected \(F_j\in L^1_{\rm loc}L^2\) |
| infinite direct sum | PASS | finite partial sums plus monotone convergence; continuous Bloch uses a direct integral |
| OS shear operator and Fourier matrix | PASS | self-adjoint banded operator with exact carrier block |
| low-gap shear coefficient | PASS AFTER TAIL EDIT | carrier column converges in \(\ell^2\), mean-zero block is \(O(\sqrt\mu)\) in operator norm |
| carrier--tangent growth witness | PASS WITH TERMINOLOGY | two directions, not two Fourier modes; assume \(\Lambda\ne0\) |
| fixed-\(c\) \(\mu^{-1/2}\) lower bound | PASS AFTER CONTINUITY EDIT | regular evolution converges on compact intervals and a four-mode projection stays nonzero |
| enhanced dissipation / nonlinear / Clay | NOT PROVED | none follows from the viscous-rate linear energy theorem |

---

## 1. Bloch carrier identity and homogeneous (X_g) theorem

Let

\[
 \mathcal L=-\partial_x^2-2i\beta\partial_x+g,
 \qquad g=\beta^2+\xi^2+\gamma^2,
 \qquad c=\gamma\Lambda.
 \tag{1.1}
\]

For \(q=gh+r\), \(h=\Pi_0\mathcal L^{-1}q\),
\(r=Q_0q\), and \(s_r=\mathcal L^{-1}r\),

\[
 r=-s_{r,xx}-2i\beta s_{r,x}+gs_r.
 \tag{1.2}
\]

Periodic integration by parts gives

\[
 \Pi_0(-Ws_{r,xx})=-\Pi_0(W_{xx}s_r),
 \qquad
 \Pi_0(-2i\beta Ws_{r,x})=2i\beta\Pi_0(W_xs_r).
 \tag{1.3}
\]

Thus

\[
 \boxed{
 \Pi_0(Wr+W_{xx}\mathcal L^{-1}r)
 =g\Pi_0(W\mathcal L^{-1}r)
 +2i\beta\Pi_0(W_x\mathcal L^{-1}r).}
 \tag{1.4}
\]

Multiplying the second term by \(-ic/g\) indeed produces the positive
coefficient \(+2c\beta/g\).  Moreover

\[
 \left|\frac{2c\beta}{g}\right|
 =|\Lambda|\frac{2|\gamma\beta|}{
 \beta^2+\xi^2+\gamma^2}
 \le|\Lambda|.
 \tag{1.5}
\]

This removes the inverse gap only from the homogeneous coupling.  The exact
transformed forcing remains \(g^{-1}\Pi_0F_q\), so the audited \(X_g\)
propagator theorem assumes \(F_q=0\) and \(\mu>0\).

With

\[
 \ell=(1-|\beta|)^2+\mu,
 \qquad X_g=|h|^2+\|r\|_2^2,
 \tag{1.6}
\]

the exact coefficient ledger in the report yields, for \(0<g\le1\),

\[
 \frac12X_g'
 \le\left[-g+|c|\left(4e^{-d}+\frac{43}{8}e^{-4d}\right)
 +|\Lambda|(e^{-d}+e^{-4d})\right]X_g.
 \tag{1.7}
\]

The constants were independently reproduced term by term.  Gronwall and
the square root of (X_g) give exactly the exponent displayed in the report.

The representative cell \([-1/2,1/2)\) includes \(\beta=-1/2\).  At that
fiber the (n=0,1) eigenvalues tie.  The coordinate (h) remains exact but
must be described as the selected zero-lattice carrier, not the unique slow
mode.  At \(\mu=0,\beta\ne0\), (1.4) remains algebraically meaningful, but
the complete velocity divergence constraint forces (v=0); the nontrivial
hybrid physical theorem is therefore stated for \(\mu>0\).

---

## 2. Complete primitive-component kinetic theorem

For a complete divergence-free row, the primitive velocity equation gives

\[
 \frac12\frac d{dd}\|u\|_2^2
 +\|A_\beta u\|_2^2+\mu\|u\|_2^2
 =-\Lambda\operatorname{Re}\langle W_xv,u_3\rangle
 +\operatorname{Re}\langle F,u\rangle.
 \tag{2.1}
\]

Since (v) and (u_3) are physical components,

\[
 |\langle W_xv,u_3\rangle|
 \le\frac12\|W_x\|_\infty\|u\|_2^2.
 \tag{2.2}
\]

The exact heat profile satisfies

\[
 W_x=-\frac12e^{-d}\cos x+\frac12e^{-4d}\cos2x.
 \tag{2.3}
\]

At (x=\pi) both terms have the same sign, hence

\[
 \|W_x(d)\|_\infty=\frac12(e^{-d}+e^{-4d}),
 \tag{2.4}
\]

\[
 K(s,d)=\int_s^d\|W_x(\tau)\|_\infty d\tau
 =\frac12(e^{-s}-e^{-d})
 +\frac18(e^{-4s}-e^{-4d}).
 \tag{2.5}
\]

Therefore

\[
 \boxed{
 \|U_j(d,s)\|_{L^2_u\to L^2_u}
 \le e^{-g_j(d-s)+|\Lambda|K(s,d)/2}.}
 \tag{2.6}
\]

The coefficient \(|\Lambda|/2\) in the norm differential is correct: the
(1/2) in the energy identity and the square root introduce no missing
factor.  The theorem remains valid at (g_j=0), where it gives finite
transient without strict decay.

For \(\mu>0\), the exact OS--Squire recovery identity is

\[
 \|u\|_2^2=\mu^{-1}
 \left(\|\mathcal L^{-1/2}q\|_2^2+\|\eta\|_2^2\right).
 \tag{2.7}
\]

At \(\mu=0\), primitive components rather than (2.7) cover the exceptional
rows.  The proof starts with smooth divergence-free data and projected
forcing, then passes to (L^2) mild solutions by density.  Applying (2.6)
to finite row sums and using monotone convergence proves the infinite
discrete direct sum with no row-count factor.  In a continuous Bloch model,
the same step is an orthogonal direct integral.

---

## 3. Best OS shear-form coefficient

On \(\beta=\xi=0\), define

\[
 S=-i\left(W_x\partial_x+\frac12W_{xx}\right),
 \qquad
 T_\mu=\sqrt\mu\mathcal L_\mu^{-1/2}
 S\mathcal L_\mu^{-1/2}.
 \tag{3.1}
\]

The operator (S) is self-adjoint, and

\[
 \rho_\mu=\|T_\mu\|,
 \qquad
 (T_\mu)_{kn}=\sqrt\mu\,
 \frac{(k+n)\widehat{W_x}(k-n)}
 {2\sqrt{(k^2+\mu)(n^2+\mu)}}.
 \tag{3.2}
\]

In the decomposition \(\mathbb Ce_0\oplus Q_0L^2\),

\[
 T_\mu=
 \begin{pmatrix}0&a_\mu^*\\a_\mu&B_\mu\end{pmatrix},
 \qquad
 (a_\mu)_k=\frac{k}{2\sqrt{k^2+\mu}}\widehat{W_x}(k).
 \tag{3.3}
\]

The exact carrier norm is

\[
 \|a_\mu\|_{\ell^2}^2
 =\frac{e^{-2d}}{32(1+\mu)}
 +\frac{e^{-8d}}{8(4+\mu)},
 \tag{3.4}
\]

while the entire infinite mean-zero block obeys

\[
 \|B_\mu\|
 \le\delta_\mu
 :=\|W_x\|_\infty\sqrt{\frac\mu{1+\mu}}.
 \tag{3.5}
\]

Hence (a_\mu\to a_0) in \(\ell^2\), (B_\mu\to0) in operator norm,
and

\[
 \boxed{
 \rho_\mu(d)\longrightarrow
 \frac12\|W_x(d)\|_2
 =\frac{\sqrt{e^{-2d}+e^{-8d}}}{4\sqrt2}.}
 \tag{3.6}
\]

The finite-(\mu\) block estimate is

\[
 \rho_\mu\le
 \frac{\delta_\mu+
 \sqrt{\delta_\mu^2+4\|a_\mu\|^2}}2
 \le
 \frac{\delta_\mu+
 \sqrt{\delta_\mu^2+\|W_x\|_2^2}}2.
 \tag{3.7}
\]

Taking the minimum with \(\|W_x\|_\infty/2\) gives the report's explicit
bound.  Dominated convergence is available because that elementary majorant
is integrable, so

\[
 \lim_{\mu\downarrow0}\int_0^\infty\rho_\mu(d)\,dd
 =\frac1{4\sqrt2}\int_0^1\sqrt{1+y^6}\,dy
 =0.188106027072\ldots.
 \tag{3.8}
\]

This is a two-dimensional OS logarithmic coefficient, not the exact
nonautonomous propagator gain or a complete-row improved constant.

---

## 4. Carrier--tangent growth witness

Assume \(\Lambda\ne0\).  For the exact smooth divergence-free trial plane
in the report, let

\[
 A=\|W_x\|_2^2,
 \qquad D=A+\mu\|W\|_2^2,
 \qquad B=\|\mathcal L_\mu W\|_2^2.
 \tag{4.1}
\]

Its kinetic metric, dissipation, and shear form are

\[
 h^2+D\varepsilon^2,
 \qquad \mu h^2+B\varepsilon^2,
 \qquad |\Lambda|Ah\varepsilon.
 \tag{4.2}
\]

The largest instantaneous logarithmic growth of the norm is

\[
 \lambda_{\rm trial}
 =-\frac12\left(\mu+\frac BD\right)
 +\frac12\sqrt{\left(\mu-\frac BD\right)^2
 +\frac{\Lambda^2A^2}{D}},
 \tag{4.3}
\]

and

\[
 \boxed{\lambda_{\rm trial}>0
 \iff \Lambda^2A^2>4\mu B.}
 \tag{4.4}
\]

For each fixed nonzero \(\Lambda\), (4.4) holds at sufficiently small
\(\mu\), giving strict norm growth on a short future interval.  Thus a
prefactor-one kinetic contraction is false.  The witness is a two-direction
carrier--tangent plane with four nonzero Fourier harmonics, not literally a
two-mode Fourier truncation.  At finite \(\mu\), its vorticity tangent is
\(\sqrt\mu\mathcal L_\mu W\), only asymptotic to
\(-\sqrt\mu W_{xx}\).

---

## 5. Fixed-(c) long-wave lower bound

On \(X=\mathbb C\oplus Q_0L^2\), the regular heat semigroups and bounded
perturbations depend continuously on \(\mu\in[0,\mu_0]\).  Hence the
evolution family applied to the fixed initial datum \((h,r)=(1,0)\) is
strongly continuous in \(\mu\) on compact intervals.

For fixed \(c\ne0\), the limiting solution satisfies

\[
 P_{1,2}r_0(s+\tau)
 =-ic\tau W_{xx}(s)+O(\tau^2),
 \tag{5.1}
\]

where (P_{1,2}) projects onto modes \(\{\pm1,\pm2\}\).  Choose a fixed
small \(\tau_0\) for which the limit is nonzero.  Continuity gives

\[
 \|P_{1,2}r_\mu(s+\tau_0)\|_2\ge a_0>0
 \tag{5.2}
\]

for all sufficiently small \(\mu\).  On the projected modes and
\(0<\mu\le\mu_0\),

\[
 \|\mathcal L_\mu^{-1/2}P_{1,2}r\|_2
 \ge(4+\mu_0)^{-1/2}\|P_{1,2}r\|_2.
 \tag{5.3}
\]

The exact kinetic identity thus proves

\[
 \boxed{
 \|u(s+\tau_0)\|_2
 \ge\frac{a_0}{\sqrt{4+\mu_0}}\mu^{-1/2},
 \qquad \|u(s)\|_2=1.}
 \tag{5.4}
\]

Therefore fixed nonzero \(c\) cannot have a \(\mu\)-uniform physical kinetic
propagator.  This long-wave family varies the row parameter (or the physical
period); it is not a statement that the discrete nonzero frequencies of one
fixed periodic box converge continuously to zero.

---

## 6. Sealed analytic boundary

The independent audit authorizes the following analytic labels, subject to
the deterministic and publication gates:

- exact Bloch carrier cancellation and regular homogeneous coupling;
- homogeneous (X_g) finite transient for \(\mu>0\), \(0<g\le1\);
- complete primitive-component physical kinetic finite transient and forced
  Duhamel estimate;
- exact OS--Squire kinetic interpretation for \(\mu>0\), with exceptional
  rows covered in components;
- the viscous-rate orthogonal direct sum;
- the sharp two-dimensional OS shear coefficient and its low-gap limit;
- the carrier--tangent instantaneous-growth witness;
- the fixed-\(c\) \(\mu^{-1/2}\) counterexample.

It does not authorize a polynomially sharp \(\Lambda\) prefactor, an
enhanced-dissipation (A_2) direct sum, nonlinear stability, global
regularity, singularity formation, or the Clay claim.

