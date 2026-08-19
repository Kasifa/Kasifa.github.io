# R0.57 — A coherent fixed-output packet and the failure of signed normal-channel decay

## 1. Scope and literature boundary

R0.56 isolated one scale-critical obstruction in the Fourier--Leray symbol:
the polarization normal to a frequency-triad plane has pointwise gain one.
The remaining question was whether keeping the signs of many such interactions
before summation could recover a square-function gain at a fixed low output.

This note answers that question negatively in the smallest natural setting.  I
construct, for every integer \(L\geq1\), a real-valued divergence-free Fourier
polynomial with \(L\) high-frequency pairs.  All pairs lie in one dyadic shell
and in two shrinking antipodal angular caps.  They generate the same low mode,
their normal outputs are parallel and have the same phase, and every exchanged
term vanishes.  The resulting fixed-output bilinear estimate attains its exact
constant one.

Coherent high-frequency pairs producing a common low mode are classical.  In
particular, the norm-inflation construction of Bourgain and Pavlović uses
wave-vector pairs whose difference is a fixed low frequency; related
high-to-low transfer constructions appear in later ill-posedness work.  I do
**not** claim that the coherence mechanism is new.  The narrower statement
proved here is its exact alignment with the R0.56 normal channel, including:

1. the sharp fixed-output \(\ell^2\times\ell^2\) operator norm;
2. an all-index real and divergence-free equality packet in one shell and
   shrinking angular caps;
3. persistence under exchange symmetrization and instantaneous heat evolution;
4. an exact single-mode energy-flux saturation.

References used for this boundary are:

- J. Bourgain and N. Pavlović, *Ill-posedness of the Navier--Stokes equations
  in a critical space in 3D*, Journal of Functional Analysis 255 (2008),
  2233--2247, <https://arxiv.org/abs/0807.0882>.
- A. Cheskidov and M. Dai, *Norm inflation for generalized Navier--Stokes
  equations*, Indiana University Mathematics Journal 63 (2014), 869--884,
  <https://arxiv.org/abs/1212.3801>.

Nothing in this note proves or disproves global regularity for the
three-dimensional Navier--Stokes equations.  It rules out one proposed source
of decay and identifies what the next estimate must use.

## 2. The fixed-output operator has norm at most one

On the three-dimensional torus, let \(U=(U_p)\) and \(V=(V_q)\) be finitely
supported divergence-free Fourier sequences.  Thus

\[
 p\cdot U_p=0,\qquad q\cdot V_q=0.
\tag{2.1}
\]

For a fixed nonzero output \(k\in\mathbb Z^3\), define the normalized ordered
Fourier--Leray operator

\[
 \mathfrak B_k(U,V)
 =\frac1{|k|}P_k\sum_{p+q=k}(q\cdot U_p)V_q,
 \qquad
 P_k=I-\widehat k\otimes\widehat k.
\tag{2.2}
\]

Let

\[
 \|U\|_{2,k}^2=\sum_{p+q=k}|U_p|^2,
 \qquad
 \|V\|_{2,k}^2=\sum_{p+q=k}|V_q|^2.
\tag{2.3}
\]

### Theorem 1 — sharp fixed-output bound

For every finite divergence-free pair,

\[
 \boxed{
 |\mathfrak B_k(U,V)|\leq \|U\|_{2,k}\|V\|_{2,k}.
 }
\tag{2.4}
\]

The constant one is exact, even after restricting both input blocks to one
high-frequency dyadic shell and to shrinking antipodal angular caps while
\(|k|/|p|\to0\).

### Proof of the upper bound

Since \(q=k-p\) and \(p\cdot U_p=0\),

\[
 q\cdot U_p=k\cdot U_p.
\tag{2.5}
\]

The Leray projector is an orthogonal contraction, so

\[
 \begin{aligned}
 |\mathfrak B_k(U,V)|
 &\leq \sum_{p+q=k}
   \frac{|k\cdot U_p|}{|k|}|V_q|\\
 &\leq \sum_{p+q=k}|U_p||V_q|\\
 &\leq \|U\|_{2,k}\|V\|_{2,k}.
 \end{aligned}
\tag{2.6}
\]

Only the last line uses Cauchy--Schwarz.  The construction below attains
equality in every line simultaneously. \(\square\)

## 3. An all-index coherent equality packet

Fix

\[
 k=e_2=(0,1,0).
\tag{3.1}
\]

For an integer \(L\geq1\) and \(N=L,\ldots,2L-1\), set

\[
 p_N=(N,0,0),
 \qquad
 q_N=(-N,1,0)=k-p_N.
\tag{3.2}
\]

Choose real coefficients \(c_N\), and define two input blocks by

\[
 U_{p_N}=c_Ne_2,
 \qquad
 V_{q_N}=c_Ne_3.
\tag{3.3}
\]

Both blocks are divergence free.  Moreover,

\[
 q_N\cdot U_{p_N}=c_N,
 \qquad
 P_ke_3=e_3,
\tag{3.4}
\]

and hence

\[
 \boxed{
 \mathfrak B_k(U,V)=\left(\sum_{N=L}^{2L-1}c_N^2\right)e_3.
 }
\tag{3.5}
\]

At the same time,

\[
 \|U\|_{2,k}\|V\|_{2,k}
 =\sum_{N=L}^{2L-1}c_N^2.
\tag{3.6}
\]

Thus (2.4) is an equality for every coefficient sequence, not only for equal
amplitudes.

The localization becomes stronger as \(L\) grows:

\[
 L\leq |p_N|,|q_N|<2L,
 \qquad
 \frac{|k|}{\min(|p_N|,|q_N|)}\leq\frac1L,
\tag{3.7}
\]

and

\[
 \widehat p_N=e_1,
 \qquad
 \angle(\widehat q_N,-e_1)=\arctan(1/N)\leq\arctan(1/L).
\tag{3.8}
\]

So both blocks are in the same dyadic shell.  One angular cap has zero radius
and the other shrinks to the antipodal direction.  Nevertheless the ratio in
(2.4) remains exactly one.

Geometrically, every triad lies in the \(e_1e_2\)-plane and has the same
normal \(e_3\).  The left polarization \(e_2\) is the R0.56 tangent
polarization \(t_{p_N}\), while the right polarization \(e_3\) is the normal
polarization.  Hence each pair uses precisely the constant-one channel.

## 4. Reality, absence of cross collisions, and exchange symmetrization

Define one Fourier field \(w\) by

\[
 \widehat w(p_N)=c_Ne_2,
 \qquad
 \widehat w(q_N)=c_Ne_3,
\tag{4.1}
\]

and impose reality through

\[
 \widehat w(-m)=\overline{\widehat w(m)}.
\tag{4.2}
\]

The coefficients in (4.1) are real, so \(w\) is a real-valued,
divergence-free trigonometric polynomial.

There are no unintended contributions to the output \(k\).  The support has
second coordinates \(0,1,0,-1\).  A supported pair summing to \(k\) must use
one mode with second coordinate zero and one with second coordinate one.  The
first-coordinate equation then forces exactly \(p_N+q_N=k\) with the same
index \(N\).  Thus the only ordered pairs are

\[
 (p_N,q_N),\qquad(q_N,p_N).
\tag{4.3}
\]

The exchanged interaction vanishes exactly:

\[
 p_N\cdot \widehat w(q_N)=p_N\cdot(c_Ne_3)=0.
\tag{4.4}
\]

Consequently the full self-interaction at output \(k\) is

\[
 \boxed{
 \frac1{|k|}P_k\sum_{p+q=k}
 (q\cdot\widehat w(p))\widehat w(q)
 =\left(\sum_{N=L}^{2L-1}c_N^2\right)e_3.
 }
\tag{4.5}
\]

Exchange symmetrization therefore gives no cancellation for this packet.

## 5. No-go theorem for shell- or cap-decaying constants

### Theorem 2 — signed fixed-output aggregation has no geometric decay

Suppose a fixed-output estimate for the normal channel has the form

\[
 |\mathfrak B_k(U,V)|
 \leq C(\rho,\theta)\|U\|_{2,k}\|V\|_{2,k},
\tag{5.1}
\]

whenever both blocks lie in one high-frequency shell,
\(|k|/\min(|p|,|q|)\leq\rho\), and the blocks lie in antipodal caps of
aperture at most \(\theta\).  Then

\[
 \boxed{C(1/L,\arctan(1/L))\geq1}
\tag{5.2}
\]

for every integer \(L\geq1\).  In particular, no such estimate can have
\(C(\rho,\theta)<1\) along this sequence, let alone
\(C(\rho,\theta)\to0\) as \((\rho,\theta)\to(0,0)\).

### Proof

Insert the packet (3.2)--(3.3) into (5.1).  Equations (3.5)--(3.8) show that
the quotient of the two sides without \(C\) is exactly one at the stated
localization parameters. \(\square\)

The theorem does not say that phases never cancel.  They can.  It says that
sign retention alone cannot force cancellation uniformly over real
divergence-free data, because coherent admissible data attain equality.

## 6. Instantaneous heat evolution preserves equality

One might hope that the heat semigroup separates the two blocks before the
nonlinearity is estimated.  It does not improve this instantaneous
fixed-output inequality.

Let \(U(t)=e^{\nu t\Delta}U\) and \(V(t)=e^{\nu t\Delta}V\), where \(\nu>0\).
Since

\[
 |p_N|^2=N^2,
 \qquad
 |q_N|^2=N^2+1,
\tag{6.1}
\]

we obtain

\[
 \mathfrak B_k(U(t),V(t))
 =e^{-\nu t}
  \left(\sum_{N=L}^{2L-1}c_N^2e^{-2\nu N^2t}\right)e_3.
\tag{6.2}
\]

The product of the two time-dependent block norms is the same scalar:

\[
 \|U(t)\|_{2,k}\|V(t)\|_{2,k}
 =e^{-\nu t}\sum_{N=L}^{2L-1}c_N^2e^{-2\nu N^2t}.
\tag{6.3}
\]

Thus the ratio remains exactly one for every \(t\geq0\).  This statement is
only about applying the fixed-output estimate at one time.  The time-integrated
Duhamel operator contains additional denominators and is not resolved here.

## 7. Exact saturation of one-mode nonlinear energy input

Add the output coefficients

\[
 \widehat w(k)=-iCe_3,
 \qquad
 \widehat w(-k)=iCe_3,
 \qquad C>0.
\tag{7.1}
\]

They preserve reality and incompressibility and create no new pair summing to
\(k\).  With the Fourier convention

\[
 \partial_t\widehat w(k)\big|_{\rm nl}
 =-iP_k\sum_{p+q=k}(q\cdot\widehat w(p))\widehat w(q),
\tag{7.2}
\]

the instantaneous energy input into the mode \(k\) is

\[
 \begin{aligned}
 \operatorname{Re}\left[
  \overline{\widehat w(k)}\cdot
  \partial_t\widehat w(k)\big|_{\rm nl}
 \right]
 &=C\sum_{N=L}^{2L-1}c_N^2.
 \end{aligned}
\tag{7.3}
\]

It therefore saturates the product of the output amplitude and the two block
norms.  The conjugate mode \(-k\) gives the same input.  This does not conflict
with conservation of total kinetic energy by the Euler nonlinearity: other
output modes carry the balancing negative transfer.

## 8. Research decision and next test

R0.57 closes the option posed at the end of R0.56:

- a fixed output does not create orthogonality, because all normal vectors can
  be parallel;
- exchange antisymmetry does not help uniformly, because the reverse terms can
  vanish one by one;
- dyadic separation and arbitrarily narrow antipodal caps do not reduce the
  sharp \(\ell^2\times\ell^2\) constant;
- applying the heat semigroup to both input blocks before an instantaneous
  estimate still leaves an exact equality.

The result is useful as a rigorous no-go theorem inside this project, but its
standalone novelty is limited by the classical high-to-low coherence
mechanism.  It is not yet a high-level paper result and does not improve a
known regularity class.

The next state must use information absent from (5.1).  The smallest options
are:

1. estimate the **time-integrated Duhamel operator**, retaining its exact heat
   denominators rather than applying (2.4) at each time;
2. couple **many output frequencies** in a norm where their geometric
   arrangement matters;
3. combine the normal channel with a genuinely global constraint, such as a
   critical spacetime norm or a depletion condition that excludes coherent
   packets.

R0.58 should begin with option 1 because the packet above gives an exact test
family against which every proposed time-integrated gain can be checked.
