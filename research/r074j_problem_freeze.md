# R0.74J problem freeze — matching complete payment on the explicit family

## 0. Decision

R0.74J will not claim a new cross-scale containment theorem.  Yang already
proved quantitative comparison and containment for admissible skewed
cylinders, and Vasseur--Yang already used this geometry in the
suitable-weak Navier--Stokes setting.  Nor will this release claim that finite
total energy produces a good scale at a prescribed possible singular point.
The available partial-regularity and hollow-shell results do not supply that
implication.

The selected task is an internal analytic gap left open in R0.74I:

> determine the true complete-payment scale of the exact R0.74F--H
> two-packet family.

The proof target is a matching lower bound for a quantity whose upper bound
was frozen in R0.74G.  The lower bound will use only the background shear on
one fixed annulus.  It is independent of the passive-packet amplitude and of
the unspecified shape of the saturation inside its transition interval.

This is a theorem about one explicit smooth family.  It is not a regularity
theorem for arbitrary solutions and it does not solve the Navier--Stokes
Millennium problem.  **NOT CLAY.**

---

## 1. Frozen inherited objects

Use exactly the R0.74F--H family and notation analysed in R0.74I:

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),\qquad p_j=0,
\]

\[
 L_j=\frac{63}{32}2^j,\qquad
 R_j=e^{-L_j^2/320},\qquad
 B_jR_j^2\longrightarrow\frac1{128},
\]

with
\(\mathfrak a_j=B_j(\gamma_j^{\rm tar})^{-1/2}\) and
\(\gamma_j^{\rm tar}=e^{-(8/3969)L_j^2}\), and retain the exact identities

\[
 \frac8{3969}L_j^2=\frac{4^{j-1}}{32},
 \qquad \gamma_j^{\rm tar}=e^{-4^{j-1}/32}=\Gamma_j.
\]

This is one numerical weight sequence with two roles: \(j\) is the family
index in the target amplitude, whereas \(k\) is the payment-shell index in
\(\Gamma_k\).  Retain the exact identities

\[
 P_j:=P_{R_j}^M=P_{R_j}^F,
 \qquad X_{R_j}=a_{R_j}=a_{R_j}'=0.
\]

Set the terminal spacetime point

\[
 z_{0,j}:=(65R_j^2,0).
\]

At payment radius \(2R\), the nonnegative velocity-cubic payment row is

\[
 \mathcal G_u
 =(2R)^{-2}\int_{I_{2R}}\int_{\mathbb R^3}
 W_{2R}(x)|u(t,x)|^3\,dx\,dt,
\]

where

\[
 I_{2R}=(61R^2,65R^2),\qquad
 W_{2R}=\sum_{k\ge1}\Gamma_k1_{A_k(2R)},\qquad
 \Gamma_k=e^{-4^{k-1}/32}.
\]

R0.74G supplies the inherited upper bound

\[
 P_j\le C B_j^3R_j^3.
\]

---

## 2. Frozen theorem target

For every sufficiently large \(j\), prove

\[
 \boxed{
 \mathcal G_u(z_{0,j},2R_j;1)
 \ge 8e^{-8}B_j^3R_j^3.}
\tag{T1}
\]

Since every row in \(P_j\) is nonnegative, (T1) and the inherited upper
bound imply

\[
 \boxed{
 8e^{-8}B_j^3R_j^3
 \le P_j\le C B_j^3R_j^3.}
\tag{T2}
\]

Consequently,

\[
 \boxed{
 \lim_{j\to\infty}\frac{\log P_j}{L_j^2}
 =\frac3{320}.}
\tag{T3}
\]

Write the proof region as the payment interval times a spatial box:

\[
 Q_R=\{|x_1|<R,\ |x_2|<R,\ 80R<x_3<96R\},
 \qquad \mathcal Q_R:=I_{2R}\times Q_R.
\tag{T4}
\]

For sufficiently small \(R\), its spatial part lies in
\(A_5(2R)=\{64R\le|x|<128R\}\), so the weight is exactly
\(\Gamma_5=e^{-8}\).  The shear plateau and the periodic heat-kernel tail
must give

\[
 \theta_j(t,x_3)\ge\frac12\qquad\hbox{on }\mathcal Q_{R_j}.
\tag{T5}
\]

Then \(|u_j|^3\ge B_j^3|\theta_j|^3\),
\(|Q_R|=64R^3\), \(|\mathcal Q_R|=256R^5\), and the exact
normalization yields (T1).

---

## 3. Proof obligations

The analytic note must close all of the following obligations.

1. **Plateau geometry.**  From
   \(\delta_R=\arcsin(16R)\le32R\), verify that every
   \(x_3\in(80R,96R)\) has circular distance at least \(48R\) from the
   defect set of the positive plateau, after imposing one explicit
   sufficiently-small-\(R\) condition.
2. **Caloric persistence.**  Impose \(R\le1/200\), use the periodic
   Brownian representation with variance \(2t\), and prove by Chebyshev that
   \(1-\theta\le65/576<1/2\).  No monotonicity of the transition profile may
   be assumed.  The sharper Gaussian-tail estimate is optional and is not
   needed by the frozen proof.
3. **Shell geometry.**  Verify the entire rectangular spatial box lies in
   \(A_5(2R)\), including the two transverse coordinates.
4. **Exact ledger arithmetic.**  Check \(\Gamma_5=e^{-8}\), the time length
   \(4R^2\), the spatial volume \(64R^3\), the cubic factor \(2^{-3}\),
   and the normalization \((2R)^{-2}\), giving the coefficient
   \(8e^{-8}\).
5. **Complete-payment passage.**  Record explicitly that \(\mathcal G_u\)
   is a nonnegative row of both complete payments and that Versions M and F
   coincide on the family.
6. **Asymptotic passage.**  Combine (T2) with
   \(B_jR_j^2\to1/128\) and \(R_j=e^{-L_j^2/320}\) to prove (T3).
7. **Historical correction.**  State that R0.74J supersedes only the
   `unproved matching family bound` sentence in R0.74I.  The R0.74I frozen
   file remains an immutable record of what was known at that release.

---

## 4. Required audits and finite checks

Before release freeze, require:

- one independent analytic audit of the periodic heat-tail and plateau
  argument;
- one independent adversarial audit of shell membership, normalization,
  and the complete-payment implication;
- an exact certificate, independently reconstructed in a second language,
  for all rational shell, volume, exponent, and logarithmic-rate fields;
- a formal SVG/PDF/600-dpi PNG figure package that visualizes the fifth-shell
  proof box and the old versus sharpened logarithmic window;
- a primary-literature boundary and claim-to-source ledger;
- a bilingual notation dictionary, synchronized HTML/PDF, source-rebind
  audit, freeze manifest, and publication handoff.

The finite certificate will not be described as proof of the heat equation,
the inherited R0.74G upper bound, or any continuum theorem.

---

## 5. Exclusions

R0.74J will not claim any of the following.

- A universal square-root-log endpoint upper estimate.
- An upper bound of order \(B_j^2L_jR_j^2\) for \(X_j\) or
  \(\mathfrak C_j\).
- A payment-to-Yang-admissibility theorem.
- A good-scale theorem at a prescribed possible singular point.
- Existence or nonexistence of a singular suitable weak solution.
- Novelty or publication priority after only a bounded collision search.
- Global smoothness or resolution of the Millennium problem.

**NOT CLAY.**
