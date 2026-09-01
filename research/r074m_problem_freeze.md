# R0.74M problem freeze — quantitative expulsion at the nearest inward collar

## Status at freeze

This file freezes the exact question which was open at the start of
R0.74M.  It does not assert the expulsion estimate.  A later proof or
negative result must address the object below without replacing the true
packet by a free heat packet and without discarding periodic windings.

R0.74L proved the normalized-bridge majorant at the target-shell collar.
R0.74M treats only the complete \(k=j-1\) row of the annular derivative.
The remaining shell synthesis, the full R0.74K signed condition, the
matching upper bounds for \(\mathfrak C_j\) or \(X_j\), every universal
endpoint estimate, and three-dimensional Navier--Stokes regularity remain
outside this freeze.  **NOT CLAY.**

## 1. Inherited exact family

Retain

\[
 \lambda=\frac{63}{32},\qquad c_h=\frac{15}{16},\qquad
 \beta=\frac{\sqrt{31}}{16},\qquad \rho=\frac1{320},
\]

\[
 L_j=\lambda2^j,\qquad R_j=e^{-\rho L_j^2},\qquad
 r_j=L_jR_j,\qquad h_j=c_hr_j,
 \qquad q_j=\beta r_j,
\tag{F.1}
\]

and write \(R=R_j\), \(L=L_j\), \(h=h_j\), \(B=B_j\), and
\(Q=Q_j\).  The calibrated path satisfies

\[
 Q(R^2)=-\frac12,\qquad Q(65R^2)=q_j,qquad
 \frac1{128R^2}\le B\le\frac1{64R^2}
\tag{F.2}
\]

for all sufficiently large \(j\).  The time window and its fixed
scale-consistent cutoff are

\[
 s_R=61R^2,\qquad I_{2R}=(61R^2,65R^2),\qquad
 I_R=(64R^2,65R^2),\qquad 0\le\eta_R\le1.
\tag{F.3}
\]

The velocity family is

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),\qquad
 F_j=F_j^++F_j^-,
\tag{F.4}
\]

with

\[
 F_j^-(t,x_2,x_3)=-F_j^+(t,-x_2,-x_3).
\tag{F.5}
\]

The shell weights obey

\[
 \frac{\Gamma_{j-1}}{\Gamma_j}
 =e^{G_1L^2},\qquad G_1=\frac2{1323}.
\tag{F.6}
\]

## 2. The complete nearest-inward row

Let

\[
 \psi_k^R(x)=
 \vartheta\!\left(\frac{|x|-2^kR}{R/8}\right)
 \vartheta\!\left(\frac{2^{k+1}R-|x|}{R/8}\right),
\tag{F.7}
\]

where the inherited \(\vartheta\in C^\infty(\mathbb R;[0,1])\) is
nondecreasing, zero on \(( -\infty,-1]\), and one on \([0,\infty)\).
The complete \(k=j-1\) row is

\[
\boxed{
 \mathcal J_{j,j-1}(\tau)
 :=\Gamma_{j-1}\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}
 \theta_j(t,x_3)\,\widetilde F_j(t,x_2,x_3)^2
 \partial_2\psi_{j-1}^R(x)\,dx\,dt .}
\tag{F.8}
\]

The tilde records the periodic lift.  The compact Euclidean cutoff and
every periodic copy of the field must both remain visible.  The associated
physical flux component is

\[
 \mathfrak F_j^{(j-1)}(\tau)
 =\frac{\mathfrak a_j^2B_j}{2R_j}\,
 \mathcal J_{j,j-1}(\tau).
\tag{F.9}
\]

### Primary R0.74M question

Does there exist \(C<\infty\), independent of \(j\), such that for every
sufficiently large \(j\),

\[
\boxed{
 \sup_{\tau\in I_R}
 [\mathcal J_{j,j-1}(\tau)]_+
 \le C\Gamma_jLR^5?}
\tag{F.10}
\]

This is a one-sided estimate for the original signed row.  It is neither an
absolute estimate for the full annular sum nor a claim about every shell.

## 3. Safe one-packet majorant

Put

\[
 w(t,x)=\eta_R(t)\theta_j(t,x_3)
 \partial_2\psi_{j-1}^R(x).
\tag{F.11}
\]

Both \(\theta_j\) and \(\partial_2\psi_{j-1}^R\) change sign under full
inversion, so \(w(t,-x)=w(t,x)\).  Hence (F.5) and
\(|a+b|^2\le2(|a|^2+|b|^2)\) give the cancellation-free reduction

\[
 [\mathcal J_{j,j-1}(\tau)]_+
 \le4\Gamma_{j-1}\int_{s_R}^{\tau}\!\!\int_{\mathbb R^3}
 [w(t,x)]_+|F_j^+(t,x_2,x_3)|^2\,dx\,dt.
\tag{F.12}
\]

Define the positive chord and its two-variable periodization by

\[
 D^-(t,x_2,x_3)
 :=\int_{\mathbb R}
 [\theta_j(t,x_3)\partial_2\psi_{j-1}^R
 (x_1,x_2,x_3)]_+\,dx_1,
\tag{F.13}
\]

\[
 \overline D^-(t,\bar x_2,\bar x_3)
 :=\sum_{n_2,n_3\in\mathbb Z}
 D^-(t,x_2+2\pi n_2,x_3+2\pi n_3).
\tag{F.14}
\]

For the positive packet, the exact normalized bridge formula is

\[
 F_j^+(t,Q(t)+z,h+y)
 =R^3K_T(y)\mathbb E_{t,y}^{\rm br}
 \partial K_T(z+\mathfrak S_t^y),
 \qquad T=R^2+t,
\tag{F.15}
\]

where

\[
 \mathfrak S_t^y
 =B\int_0^t[\theta_j(t-s,h)-\theta_j(t-s,h+Y_s^y)]\,ds.
\tag{F.16}
\]

Jensen, exact periodic unfolding, and the R0.74L common-forward-law
identity reduce (F.12) to the nonnegative sufficient quantity

\[
\begin{aligned}
 \mathcal A^-_{j,j-1}(\tau)
 :={}&\Gamma_{j-1}R^6\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb T}|\partial K_T(u)|^2\\
 &\times\mathbb E^{\rm fw}\!\left[
 K_T(X_t)\overline D^-
 (t,q_\omega(t)+u,h+X_t)
 \right]du\,dt,
\end{aligned}
\tag{F.17}
\]

with

\[
 q_\omega(t)=Q(t)-\mathfrak S_t^{\leftarrow}[X],\qquad
 \mathfrak S_t^{\leftarrow}[X]
 =B\int_0^t[\theta_j(s,h)-\theta_j(s,h+X_s)]\,ds.
\tag{F.18}
\]

Thus the stronger target

\[
\boxed{
 \sup_{\tau\in I_R}\mathcal A^-_{j,j-1}(\tau)
 \le C\Gamma_jLR^5}
\tag{F.19}
\]

is sufficient for (F.10).  Formula (F.17) retains the correlation between
the shear lag and the radial window.

## 4. Frozen proof-or-refutation route

The first route to test is a final-segment expulsion lemma under the common
forward law.  On the support of \(\overline D^-\), the vertical endpoint is
inside the padded \(j-1\) shell:

\[
 |h+X_t|_{\rm lift}
 \le\left(\frac{32}{63}L+\frac18\right)R.
\tag{F.20}
\]

Take a final time segment of length \(R^2/64\).  The candidate mechanism is:

1. except on a Brownian modulus event of probability \(e^{-cL^2}\), the
   last segment remains within \(LR/16\) of its inward endpoint;
2. on that event the path lies in \(|h+X_s|\le(3/5)LR\), where a fixed
   negative interval of the initial shear gives a lower caloric defect;
3. integration of that defect produces a positive displacement much larger
   than \(LR\), because its exponent is strictly smaller than \(\rho\);
4. the horizontal heat derivative is then evaluated super-Gaussianly far
   from its centre; and
5. the exceptional modulus event must itself pay both one factor \(R\) and
   the weight ratio \(e^{-G_1L^2}\).

These are proof obligations, not results at freeze.  A failed pathwise
lower bound does not refute (F.10): continuous fast-return paths exist and
must be handled probabilistically.  Likewise, nonnegativity or monotonicity
of an abstract displacement alone cannot repair the known free-heat
exponent deficit.

## 5. Exclusions and completion gate

R0.74M may be promoted only after all of the following are present.

1. A proof of (F.19), or an explicit negative result locating the first
   false implication and the strongest surviving signed statement.
2. Exact treatment of the full \(j-1\) cutoff derivative, both packet signs,
   the cross term, the fixed time cutoff, and all periodic windings.
3. A finite exact-arithmetic or interval certificate for every calibrated
   exponent and geometric comparison used in the proof.
4. An independent mathematical reconstruction which is not the authoring
   pass.
5. A bounded primary-source collision audit, reported only as a finite
   hit or non-hit and never as a novelty or priority proof.
6. A journal-ready formal figure package: source data, SVG, vector PDF,
   600-dpi PNG, manifest, and visual QA.
7. A frozen handoff to the independent Codex task titled **发布任务**.

The recap is not updated at this section boundary.  Publication is a
separate transaction after the research gate closes.
