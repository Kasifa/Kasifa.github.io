# R0.74S Step 3 — exact signed decomposition on the actual padded collars

## 0. Result and boundary

R0.74S Step 2 binds every selected terminal net-upcrossing family to the
actual stopped work

\[
 W_R^M
 =\frac1R\int\eta_R\widetilde{\mathcal W}_R^M\cdot
   \sum_{k\in A(t)}\gamma_k\nabla\psi_k^R.
\]

This note computes that spatial row without replacing the frozen padded
cutoffs by an ideal partition.  The result is stricter than the Step-1
no-gain model:

1. all inner and outer transition-gradient supports are pairwise disjoint
   on the Euclidean lift;
2. hence adjacent padded collars have no pointwise internal-face
   cancellation at all;
3. for each active shell block, the signed work splits exactly into a root
   collar, an outer collar, an internal weight-drop row, and a two-sided
   collar-mismatch row; and
4. the present \(L^1\) work ledger supplies no uniform modulus comparing
   the two sides of a shared boundary.

Thus the next positive theorem must be a dynamical signed bridge across two
disjoint collars.  Coefficient algebra, overlap, and \(L^1\) translation
continuity do not provide it.  The bridge remains **OPEN**.
**NOT CLAY.**

## 1. Exact derivative supports of the frozen shell cutoff

Put

\[
 r_k:=2^kR,\qquad \delta:=\frac R8,\qquad
 \psi_k^R(y)
 =\vartheta\!\left(\frac{|y|-r_k}{\delta}\right)
  \vartheta\!\left(\frac{r_{k+1}-|y|}{\delta}\right),
\tag{S.39}
\]

where \(\vartheta=0\) on \((-\infty,-1]\),
\(\vartheta=1\) on \([0,\infty)\), and \(\vartheta'\ge0\).
For \(y\ne0\), write \(\widehat y=y/|y|\).  On the support of either
derivative, the other cutoff factor is exactly one.  Therefore

\[
 \boxed{
 \nabla\psi_k^R(y)
 =\delta^{-1}\left[
  \vartheta'\!\left(\frac{|y|-r_k}{\delta}\right)
  -\vartheta'\!\left(\frac{r_{k+1}-|y|}{\delta}\right)
 \right]\widehat y.}
\tag{S.40}
\]

For every boundary radius \(r_m\), define the two open collars

\[
 C_m^-:=\{r_m-\delta<|y|<r_m\},
 \qquad
 C_m^+:=\{r_m<|y|<r_m+\delta\}.
\tag{S.41}
\]

The inner derivative of shell \(k\) is supported in \(C_k^-\), whereas
its outer derivative is supported in \(C_{k+1}^+\).  These two collars lie
on opposite sides of the hard boundary.  Moreover,

\[
 r_{m+1}-r_m=2^mR>2\delta\qquad(m\ge1),
\tag{S.42}
\]

so the entire collection
\(\{C_m^-,C_m^+:m\ge1\}\) is pairwise disjoint up to null boundary spheres.
Consequently, for every finite \(A\subset\mathbb N\),

\[
 \boxed{
 \left|\sum_{k\in A}\gamma_k\nabla\psi_k^R(y)\right|
 =\sum_{k\in A}\gamma_k|\nabla\psi_k^R(y)|
 \quad\hbox{for a.e. }y\in\mathbb R^3.}
\tag{S.43}
\]

Equation (S.43) is a statement about gradient coefficients, not about the
sign of the velocity--pressure work paired with them.

## 2. Oriented work on the two sides of one hard boundary

Let \(\widetilde{\mathcal W}_R^M\) be the periodic Euclidean lift of

\[
 \mathcal W_R^M
 =\frac12|v_R|^2(v_R-a_R)+(\pi_R-c_R)v_R.
\tag{S.44}
\]

Define the oriented collar-work traces

\[
\begin{aligned}
 J_{m,R}^-(t)
 &:=
 \delta^{-1}\int_{C_m^-}
 \widetilde{\mathcal W}_R^M(t,y)\cdot\widehat y\,
 \vartheta'\!\left(\frac{|y|-r_m}{\delta}\right)\,dy,\\
 J_{m,R}^+(t)
 &:=
 \delta^{-1}\int_{C_m^+}
 \widetilde{\mathcal W}_R^M(t,y)\cdot\widehat y\,
 \vartheta'\!\left(\frac{r_m-|y|}{\delta}\right)\,dy.
\end{aligned}
\tag{S.45}
\]

Unfolding the periodized cutoff and using (S.40) gives the exact shell row

\[
 \boxed{
 \int_{\mathbb T^3}
 \mathcal W_R^M(t,y)\cdot\nabla\Psi_k^R(y)\,dy
 =J_{k,R}^-(t)-J_{k+1,R}^+(t).}
\tag{S.46}
\]

There is no regular trace on the hard sphere in (S.45).  Both terms are
ordinary weighted collar integrals of an \(L^1\) work density.

## 3. Active shell blocks

For a stopped family from R0.74S Step 2, let

\[
 A(t)=\{k\in I:\sigma_k<t\le\tau\}.
\tag{S.47}
\]

Away from the finitely many stopping times, write its maximal block
decomposition as

\[
 A(t)=\bigcup_{\nu=1}^{N(t)}
 [p_\nu(t),q_\nu(t)]_{\mathbb Z}.
\tag{S.48}
\]

On one block \([p,q]_{\mathbb Z}\), (S.46) gives

\[
\begin{aligned}
 \sum_{k=p}^{q}\gamma_k(J_{k,R}^--J_{k+1,R}^+)
 ={}&\gamma_pJ_{p,R}^-
     -\gamma_qJ_{q+1,R}^+\\
 &+\sum_{m=p+1}^{q}
   \bigl[\gamma_mJ_{m,R}^-
         -\gamma_{m-1}J_{m,R}^+\bigr].
\end{aligned}
\tag{S.49}
\]

Each internal shared-boundary pair has the exact decomposition

\[
\boxed{
 \gamma_mJ_{m,R}^--\gamma_{m-1}J_{m,R}^+
 =-(\gamma_{m-1}-\gamma_m)J_{m,R}^+
   +\gamma_m(J_{m,R}^--J_{m,R}^+).}
\tag{S.50}
\]

The first term is the frozen weight-drop row.  The second is the bridge
mismatch between the two disjoint sides of the same hard boundary.

## 4. Complete stopped-work decomposition

Define, at every non-stopping time,

\[
\begin{aligned}
 \mathcal R_R(t)
 &:=\sum_{\nu=1}^{N(t)}
      \gamma_{p_\nu}J_{p_\nu,R}^-,\\
 \mathcal L_R(t)
 &:=\sum_{\nu=1}^{N(t)}
      \gamma_{q_\nu}J_{q_\nu+1,R}^+,\\
 \mathcal G_R(t)
 &:=-\sum_{\nu=1}^{N(t)}
    \sum_{m=p_\nu+1}^{q_\nu}
      (\gamma_{m-1}-\gamma_m)J_{m,R}^+,\\
 \mathcal M_R(t)
 &:=\sum_{\nu=1}^{N(t)}
    \sum_{m=p_\nu+1}^{q_\nu}
      \gamma_m(J_{m,R}^--J_{m,R}^+).
\end{aligned}
\tag{S.51}
\]

Here \(\mathcal R_R\) is the collection of block-root collars,
\(\mathcal L_R\) is the collection of block-outer collars,
\(\mathcal G_R\) is the internal weight-drop work, and
\(\mathcal M_R\) is the two-sided collar mismatch.  Equations
(S.31), (S.46), (S.49), and (S.50) imply

\[
 \boxed{
 W_R^M(\tau;I,\boldsymbol\sigma)
 =\frac1R\int_{s_R}^{\tau}\eta_R(t)
 \bigl[
  \mathcal R_R(t)-\mathcal L_R(t)
  +\mathcal G_R(t)+\mathcal M_R(t)
 \bigr]\,dt.}
\tag{S.52}
\]

This is an exact identity.  The labels root and outer describe geometry,
not a predetermined sign: each term can represent supply, leakage, forward
work, or backscatter depending on
\(\widetilde{\mathcal W}_R^M\cdot\widehat y\).

## 5. Why neither adjacency nor equal radial work closes the sum

The weight gap from R0.74S Step 1 gives

\[
 \gamma_{m-1}-\gamma_m\ge\frac3{35}\gamma_{m-1}.
\tag{S.53}
\]

Even if a separate theorem gave the exact bridge equality
\(J_{m,R}^-=J_{m,R}^+\), the internal pair in (S.50) would remain

\[
 -(\gamma_{m-1}-\gamma_m)J_{m,R}^+,
\tag{S.54}
\]

which is a fixed fraction of the more heavily weighted collar work.
Therefore a bridge estimate alone is insufficient; the sign of the
weight-drop work must also be retained.

Conversely, the existing integrability gives no uniform bridge modulus.
Choose a no-winding collar with \(r_m+\delta<\pi/2\), and a smooth periodic
vector work density whose principal lift is supported where
\(\vartheta'((r_m-|y|)/\delta)>0\) inside \(C_m^+\), aligned with
\(\widehat y\), and normalized so \(J_m^+=1\).  No other periodic copy
meets \(C_m^-\), so \(J_m^-=0\).  A density supported in \(C_m^-\) reverses
the example.  The \(L^1\) norm can be kept uniformly bounded under the
corresponding scaled construction.  Thus bounded \(L^1\) work alone cannot force
\(J_{m,R}^--J_{m,R}^+\) to be small uniformly over solutions and scales.

This is a functional \(L^1\) witness, not a Navier--Stokes work density.
It does not rule out a dynamical bridge estimate.

## 6. Positive-channel gate

For a time-integrated signed quantity \(H\), write \([H]_+=\max(H,0)\).
Equation (S.52) gives

\[
\begin{aligned}
 [W_R^M]_+
 \le{}&
 \left[\frac1R\int\eta_R\mathcal R_R\right]_+
 +\left[-\frac1R\int\eta_R\mathcal L_R\right]_+\\
 &+\left[\frac1R\int\eta_R\mathcal G_R\right]_+
 +\left[\frac1R\int\eta_R\mathcal M_R\right]_+.
\end{aligned}
\tag{S.55}
\]

Hence a sufficient large-payment theorem would control the four positive
cumulative channels on the right by \(CA_R\), either separately or through
cancellation retained before the final positive part.  Taking pointwise
absolute values instead returns only \(CP_R^M\) by R0.74S Step 2.

The split is useful because it distinguishes four logically different
requirements:

- component-root supply;
- sign of outer leakage/backscatter;
- sign of the super-Gaussian weight-drop work; and
- a dynamical bridge between the two disjoint collars.

## 7. Kinetic, pressure, and moving-frame drift rows

For a vector field \(G\) on the Euclidean lift, let
\(\mathcal T_{m,R}^{\pm}[G]\) denote the two linear collar functionals in
(S.45).  Decompose

\[
\begin{aligned}
 \widetilde{\mathcal W}_R^M
 &=\mathcal W_{\rm kin}+\mathcal W_{\rm pr}+\mathcal W_{\rm drift},\\
 \mathcal W_{\rm kin}
 &:=\frac12|\widetilde v_R|^2\widetilde v_R,\\
 \mathcal W_{\rm pr}
 &:=(\widetilde\pi_R-c_R)\widetilde v_R,\\
 \mathcal W_{\rm drift}
 &:=-\frac12|\widetilde v_R|^2a_R.
\end{aligned}
\tag{S.56}
\]

Then, for \(\diamond\in\{-,+\}\),

\[
 \boxed{
 J_{m,R}^{\diamond}
 =J_{m,R}^{{\rm kin},\diamond}
  +J_{m,R}^{{\rm pr},\diamond}
  +J_{m,R}^{{\rm drift},\diamond},
 \qquad
 J_{m,R}^{\alpha,\diamond}
 :=\mathcal T_{m,R}^{\diamond}[\mathcal W_\alpha].}
\tag{S.57}
\]

By linearity, every geometric channel
\(\mathcal C\in\{\mathcal R,\mathcal L,\mathcal G,\mathcal M\}\) has the
same physical split

\[
 \boxed{
 \mathcal C_R
 =\mathcal C_R^{\rm kin}
  +\mathcal C_R^{\rm pr}
  +\mathcal C_R^{\rm drift}.}
\tag{S.58}
\]

After absolute values, the coefficient accounting in (S.49)--(S.51)
counts each active collar by at most its original shell weight.  The
pressure gauge cancellation, R0.74P pressure product bound, and the
Version-M drift estimate therefore give

\[
\boxed{
 \frac1R\int_{s_R}^{\tau}\eta_R
 \sum_{\mathcal C\in\{\mathcal R,\mathcal L,\mathcal G,\mathcal M\}}
 \sum_{\alpha\in\{{\rm kin},{\rm pr},{\rm drift}\}}
 |\mathcal C_R^\alpha(t)|\,dt
 \le CP_R^M.}
\tag{S.59}
\]

This is again linear in \(P_R^M\).  Any large-payment improvement must use
sign correlation between physical rows or between geometric channels; the
local/harmonic pressure split and moving-frame drift estimates do not
produce the missing \(2/3\) power after they are made absolute.

## 8. Exact boundary and next decision

The following are **PROVED**:

- the exact derivative formula and disjoint-support geometry
  (S.40)--(S.43);
- the unfolded two-sided collar representation (S.45)--(S.46);
- the active-block and internal-pair decompositions
  (S.49)--(S.52);
- persistence of the internal weight-drop row even under exact bridge
  equality; and
- failure of a uniform collar bridge from \(L^1\) integrability alone.

The following remain **OPEN**:

- a Navier--Stokes sign or depletion estimate for the four channels in
  (S.55);
- a uniform bridge estimate using additional local energy, dissipation, or
  pressure structure;
- quadratic payment or finite-exception control of the dissipation branch;
- the R0.74R persistence packing;
- (Q.1), scale contraction, prescribed-centre scale packing, regularity,
  singularity formation, and the Clay problem.

The next falsification gate should test the strongest plausible bridge
obtainable from the available \(L_t^\infty L_x^2\cap L_t^2H_x^1\),
\(L^3\), and pressure \(L^{3/2}\) ledgers.  It must keep the
weight-drop term separate: proving only
\(J_m^-\approx J_m^+\) cannot close (S.55).  **NOT CLAY.**

## 9. Inherited source ledger

| Use in this note | Frozen source | Status |
|---|---|---|
| Exact padded cutoff formula and transition profile | R0.74E (4.12b)--(4.12d) | **INHERITED / PROVED** |
| Periodization and unfolding | R0.74H (2.3)--(2.7) | **INHERITED / PROVED** |
| Version-M velocity--pressure--drift work vector | R0.74P (2.9); R0.74S (S.29) | **INHERITED / PROVED** |
| Stopped-work identity | R0.74S Step 2 (S.26)--(S.31) | **INHERITED / PROVED** |
| Uniform adjacent weight gap | R0.74S Step 1 (S.2)--(S.3) | **INHERITED / PROVED** |

No novelty or priority claim is made.
