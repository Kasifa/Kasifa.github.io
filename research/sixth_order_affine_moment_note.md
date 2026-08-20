# R0.67B — The exact mass-plus-affine lift and the \(C^{1,1}\) spectral gap

## Claim boundary

R0.67A proved that one reachable scalar of the zero-time sixth-order cycle
has a strictly negative dominant coefficient at the root

\[
 402.425429345624<\mu<402.4254293456256.
\tag{0.1}
\]

The missing analytic issue was that the absolute spatial transfer grows by
\(65536\) per four-bit block.  A zero-mass Lipschitz estimate would therefore
cost \(65536/16=4096>\mu\).  This note proves that the correct finite lift
contains the mass and all four free first moments.  After this lift, the
remainder annihilates every affine function and contracts at the second-order
scale

\[
 \frac{65536}{16^2}=256<\mu.
\tag{0.2}
\]

Thus the finite affine lift and the resolvent on the zero-affine remainder
are now rigorous.  The sign of the complete heat-weighted five-simplex
projection is still open.  No conclusion about all Picard orders, norm
inflation, singularity, or global regularity is made here.

## 1. Four free spatial coordinates

Every complete sixth-order path satisfies

\[
 A+B+C-D-E=Q.
\tag{1.1}
\]

Take \(A,B,C,D\) as free indices and recover

\[
 E=A+B+C-D-Q.
\tag{1.2}
\]

At the end of a four-bit block put \(M_r=16^r\) and

\[
 x_1=\frac A{M_r},\quad
 x_2=\frac B{M_r},\quad
 x_3=\frac C{M_r},\quad
 x_4=\frac D{M_r}.
\tag{1.3}
\]

The discrete state remains

\[
 (s,\boldsymbol\sigma,k)\in
 \{0,1\}\times\{0,1\}^5\times\{-2,-1,0,1,2\},
 \qquad 2\cdot32\cdot5=320.
\tag{1.4}
\]

For every state \(i\), let \(\nu_i\) be its signed measure on the four-cube.
Define its mass and first moments by

\[
 m_i=\int1\,d\nu_i,
 \qquad
 \ell_{j,i}=\int x_j\,d\nu_i,
 \quad 1\le j\le4.
\tag{1.5}
\]

## 2. Exact integer moment transport

Let \(W\) be the 320 by 320 signed mass matrix for the word \(0100\).  Every
affine branch has the form

\[
 x\longmapsto\frac{x+e}{16},
 \qquad e\in\{0,1,\ldots,15\}^4.
\tag{2.1}
\]

For \(1\le j\le4\), aggregate the signed branch shift \(e_j\) into the
integer matrix \(E_j\).  Direct integration of (2.1) gives the complete
finite lift

\[
 \boxed{
 m'=Wm,
 \qquad
 \ell'_j=\frac1{16}\bigl(W\ell_j+E_jm\bigr),
 \quad 1\le j\le4.}
\tag{2.2}
\]

This is a 1600-dimensional block-triangular operator \(L\).  The audit builds
the five matrices by exact integer arithmetic.  Its mass matrix agrees
byte-for-byte with R0.67A.  The four shift-matrix SHA-256 digests are

\[
\begin{array}{c|c}
A&\mathrm{7b0da1bf689415f353952213a3700fc5c423960d7af960898844e0640ffa5c3a}\\
B&\mathrm{395c5d12784a24279ad72947b4d0448a5bc616ad3054b5bfdc08e2274a668ae8}\\
C&\mathrm{e66efdbb7fce3e0251b8651dc5b912858be73f5a26a80d490bbb3085647a5679}\\
D&\mathrm{e7c387f17ebedf4611999a6df27102751494bdd08261590c17bc1cae98f9f271}.
\end{array}
\tag{2.3}
\]

As an independent check, the script directly constructs the five
Rudin--Shapiro polynomials, reverses the two negative carriers, weights each
of the first four factors by its original index, and performs exact
convolution.  All 320 masses and all \(4\times320\) first moments agree with
(2.2) through six binary levels.  At level six, the largest absolute mass is
\(6142\) and the largest absolute first moment is \(331330\).

## 3. The canonical finite lift

Let \(e_j\) be the \(j\)-th coordinate vector in the four-cube.  State by
state define

\[
 J(m,\ell)
 =\left(m-\sum_{j=1}^4\ell_j\right)\delta_0
  +\sum_{j=1}^4\ell_j\delta_{e_j}.
\tag{3.1}
\]

If \(\mathcal M\) extracts mass and the four first moments, then

\[
 \mathcal M J=I.
\tag{3.2}
\]

Let \(\mathcal P\) be the full signed affine transfer on vector measures.
Because affine maps close exactly on affine functions, (2.2) is equivalently

\[
 \mathcal M\mathcal P=L\mathcal M.
\tag{3.3}
\]

Consequently the finite-lift defect

\[
 R=\mathcal PJ-JL
\tag{3.4}
\]

satisfies

\[
 \mathcal M R=0.
\tag{3.5}
\]

Thus every component of \(Rv\) annihilates \(1,x_1,x_2,x_3,x_4\).  This is
the exact property that the zero-mass lift of R0.66 could not provide for the
sixth-order cycle.

## 4. Exact finite spectrum

The triangular form (2.2) gives the spectrum without forming a dense 1600 by
1600 characteristic polynomial:

\[
 \operatorname{spec}L
 =\operatorname{spec}W
 \cup\frac1{16}\operatorname{spec}W
 \cup\frac1{16}\operatorname{spec}W
 \cup\frac1{16}\operatorname{spec}W
 \cup\frac1{16}\operatorname{spec}W.
\tag{4.1}
\]

R0.67A gave

\[
 \chi_{W|\operatorname{im}W}(x)
 =x^5(x-256)^5q_4(x)^4q_{10}(x),
\tag{4.2}
\]

where \(q_4\) has one root \(\mu\) in (0.1), its other roots lie in
\((-208,-192),(48,64),(128,144)\), and the ten roots of \(q_{10}\) satisfy
\(|z|<300\) by ten exact Schur transforms.  Moreover

\[
 \frac{\rho(W)}{16}<\frac{416}{16}=26.
\tag{4.3}
\]

Therefore the non-dominant finite spectral part and the first-moment blocks
obey the strict enclosure

\[
 \boxed{\rho_{\rm finite,other}<300<\mu.}
\tag{4.4}
\]

The factor \(q_4^4\) in (4.2) is retained: this note does not replace the full
dominant spectral subspace by a fictitious simple eigenvalue.  The reachable
scalar from R0.67A has a simple \(q_4\) denominator, but the full 320-state
operator has the multiplicities displayed in (4.2).

## 5. The zero-affine \(C^{1,1}\) contraction

Give every state the positive weight determined only by its carry,

\[
 w_k=(16,83441,631131,471851,28561),
 \qquad k=-2,-1,0,1,2.
\tag{5.1}
\]

The pathwise absolute four-bit transfer satisfies exactly

\[
 A_{\rm abs}w=65536w.
\tag{5.2}
\]

Let \(\mathcal B_0\) be the vector measures whose every component annihilates
all affine functions.  On \(\mathcal B_0\), use the weighted dual seminorm

\[
 \|\zeta\|_{(C^{1,1})^*,w}
 =\max_i\frac1{w_i}
 \sup_{\operatorname{Lip}(\nabla f)\le1}
 \left|\int f\,d\zeta_i\right|.
\tag{5.3}
\]

Affine terms in \(f((x+e)/16)\) vanish against \(\zeta_i\).  The remaining
Taylor difference has gradient-Lipschitz constant reduced by \(16^{-2}\).
Combining this with (5.2) proves

\[
 \boxed{
 \|\mathcal P\zeta\|_{(C^{1,1})^*,w}
 \le256\|\zeta\|_{(C^{1,1})^*,w},
 \qquad \zeta\in\mathcal B_0.}
\tag{5.4}
\]

Since \(\mu>402>256\), the resolvent exists on this remainder space and

\[
 (\mu-\mathcal P|_{\mathcal B_0})^{-1}
 =\sum_{n=0}^{\infty}\mu^{-n-1}
  (\mathcal P|_{\mathcal B_0})^n,
\tag{5.5}
\]

with the explicit bound

\[
 \left\|(\mu-\mathcal P|_{\mathcal B_0})^{-1}\right\|
 \le\frac1{\mu-256}.
\tag{5.6}
\]

Equations (4.3)--(5.6) give the full hierarchy

\[
 \boxed{26<256<300<\mu.}
\tag{5.7}
\]

## 6. Lifting the dominant finite subspace

Let \(v\) lie in the finite \(\mu\)-eigenspace of \(L\).  By (3.5), \(Rv\)
belongs to \(\mathcal B_0\).  Define

\[
 \eta_v=(\mu-\mathcal P|_{\mathcal B_0})^{-1}Rv,
 \qquad
 \rho_v=Jv+\eta_v.
\tag{6.1}
\]

Then

\[
 \mathcal P\rho_v=\mu\rho_v,
 \qquad
 \mathcal M\rho_v=v.
\tag{6.2}
\]

Thus the finite dominant subspace lifts to genuine eigen-distributions of the
full affine operator.  This closes the structural gap between the R0.67A mass
mode and an analytic heat observable.

It does not determine the scalar

\[
 C_{6,\mathrm{heat}}
 =\rho_v(F_{\theta_\infty}),
\tag{6.3}
\]

because the complete five-simplex heat kernel \(F_{\theta_\infty}\) can still
be orthogonal to the lifted dominant subspace.  Proving a strict interval for
(6.3) is the remaining R0.67 task.

## 7. Reproducibility

Run the exact audit with

    python3 research/sixth_order_affine_moment_audit.py \
      --output /tmp/r067b-affine-moment-audit.json \
      --max-direct-level 6 \
      --progress

The audit uses integer matrices and exact rational comparisons.  Floating
point is used only for human-readable decimal displays.  Its current thirteen
checks all pass.

The exact conclusion is limited to:

1. the 1600-dimensional mass-plus-four-first-moment lift (2.2);
2. its independent direct-convolution verification;
3. the spectral separation (4.4);
4. the zero-affine contraction and resolvent (5.4)--(5.6);
5. the eigen-distribution lifting formula (6.1).

The complete heat-projection sign, all higher even orders, and the full
Navier--Stokes regularity problem remain open.
