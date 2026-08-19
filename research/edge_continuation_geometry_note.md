# R0.35: charge-projection geometry and the obstruction to naive recentering

## Status and boundary

R0.31 proves that the reduced edge fields are analytic on the common
polydisc

\[
 |Z|,|W|<\frac4{81}.
\]

R0.32 then finds a stable finite Padé candidate near \(R=-0.7495\) for two
fixed-charge transport series.  R0.34 shows that no finite Taylor background
through the certified degrees repairs the failed positive-measure
representation.  The next mathematical issue is therefore analytic
continuation, not another finite fit.

This note proves that the most direct continuation design is invalid.  The
charge-zero projector is tied to the original origin and does not commute
with translation.  More strongly, the nonlinear active fixed-point map is
unbounded on a same-radius Wiener ball.  A correct estimate needs a scale of
analytic spaces; an explicit outer-to-half-radius bound is proved below.

These are all-order statements for the reduced edge equation.  The numerical
comparison with the R0.32 candidate remains a finite diagnostic.  No
singularity of the original generating functions and no regularity or
singularity statement for three-dimensional Navier--Stokes is proved.

## 1. The charge circle action

Let

\[
 X=Z\partial_Z,\qquad Y=W\partial_W,\qquad
 \mathcal L=X+Y,\qquad \mathcal Q=2Y-X,
\]

and

\[
 \{f,g\}=(Xf)(Yg)-(Yf)(Xg).
\]

The active scalar satisfies

\[
 (\mathcal L-1)a
 =(I-\Pi_0)\mathcal Q^{-1}\{a,\mathcal Qa\}
 +\Pi_0\mathcal L^{-1}\{a,\mathcal La\}.
\tag{1.1}
\]

For the monomial \(Z^nW^k\), the integer charge is

\[
 q=2k-n.
\]

Define the weighted circle action

\[
 \gamma_\theta(Z,W)=(e^{-i\theta}Z,e^{2i\theta}W).
\tag{1.2}
\]

Then

\[
 (Z^nW^k)\circ\gamma_\theta=e^{iq\theta}Z^nW^k.
\]

### Theorem 1: charge projection is Fourier projection

Whenever the circle orbit stays in the analytic domain,

\[
 \boxed{
 \Pi_q f(Z,W)=\frac1{2\pi}\int_0^{2\pi}
 e^{-iq\theta}f(e^{-i\theta}Z,e^{2i\theta}W)\,d\theta .
 }
\tag{1.3}
\]

The proof is termwise Fourier orthogonality.  On the weighted Wiener algebra

\[
 \mathcal A_{\rho_Z,\rho_W}
 =\left\{f=\sum_{n,k\ge0}f_{n,k}Z^nW^k:
 \|f\|_\rho=\sum_{n,k\ge0}|f_{n,k}|\rho_Z^n\rho_W^k<\infty\right\},
\tag{1.4}
\]

coefficient deletion immediately gives

\[
 \|\Pi_qf\|_\rho\le \|f\|_\rho.
\tag{1.5}
\]

The algebra is adapted to multiplication because
\(\|fg\|_\rho\le\|f\|_\rho\|g\|_\rho\).

## 2. Exact geometry of fixed-charge extraction

Use

\[
 R=Z^2W,\qquad \Xi=Z^{-1},\qquad
 Z=\Xi^{-1},\qquad W=R\Xi^2.
\tag{2.1}
\]

For a fixed integer charge \(q\),

\[
 F_q(R)=[\Xi^q]F(R,\Xi)
 =\frac1{2\pi i}\oint
 F(\Xi^{-1},R\Xi^2)\Xi^{-q-1}\,d\Xi.
\tag{2.2}
\]

Suppose \(F\) is represented by an absolutely convergent Taylor series on
\(|Z|<\rho_Z,|W|<\rho_W\).  A circular \(\Xi\)-contour of radius \(s\) lies
inside that polydisc exactly when

\[
 \frac1{\rho_Z}<s<\sqrt{\frac{\rho_W}{|R|}}.
\tag{2.3}
\]

### Theorem 2: polydisc-to-fixed-charge domain

The interval in (2.3) is nonempty exactly when

\[
 \boxed{|R|<\rho_Z^2\rho_W.}
\tag{2.4}
\]

For an isotropic polydisc \(\rho_Z=\rho_W=\rho\), this becomes
\(|R|<\rho^3\).  The exponent three in R0.32 is therefore not an artifact of
the coefficient majorant.  It is the exact geometry of the fixed-charge
contour.

At fixed \(|R|\), the smallest isotropic bivariate radius met by any such
contour is

\[
 \min_{s>0}\max(s^{-1},|R|s^2)=|R|^{1/3},
 \qquad s=|R|^{-1/3}.
\tag{2.5}
\]

The high-cut R0.32 finite candidate hull implies a balanced radius between
approximately

\[
 0.9083313136751\quad\text{and}\quad0.9083582427090.
\tag{2.6}
\]

This is between \(18.3937\) and \(18.3943\) times the R0.31 radius
\(4/81\).  In the \(R\)-plane, the candidate modulus is more than 6223 times
the proved fixed-charge radius \((4/81)^3\).  These ratios quantify the
continuation distance.  They do not certify that the candidate is a
singularity or that a singularity-free path reaches it.

## 3. Translation does not preserve the recurrence

Let a germ be recentered at \(c=(z_0,w_0)\):

\[
 (\tau_cf)(\zeta,\omega)=f(z_0+\zeta,w_0+\omega).
\tag{3.1}
\]

If \(f(Z,W)=Z\), then \(\Pi_0f=0\), but

\[
 \Pi_0^{\rm local}(\tau_cf)=z_0.
\tag{3.2}
\]

If \(f(Z,W)=W\), the same calculation gives \(w_0\).  Hence

\[
 \boxed{\Pi_0^{\rm local}\tau_c\ne\tau_c\Pi_0
 \quad\text{for every }c\ne(0,0).}
\tag{3.3}
\]

The Euler fields also change:

\[
 X_c=(z_0+\zeta)\partial_\zeta,\qquad
 Y_c=(w_0+\omega)\partial_\omega.
\tag{3.4}
\]

The correct conjugated projector is not diagonal in the local Taylor
coefficients.  It is

\[
 \begin{aligned}
 (\Pi_q^cg)(\zeta,\omega)
 =\frac1{2\pi}\int_0^{2\pi}e^{-iq\theta}
 g(&e^{-i\theta}(z_0+\zeta)-z_0,\\
   &e^{2i\theta}(w_0+\omega)-w_0)\,d\theta .
 \end{aligned}
\tag{3.5}
\]

Thus a small Taylor disk around \(c\) does not by itself contain the data
needed for the global charge projection.  A sufficient local containment
condition from an inner polydisc \((r_Z,r_W)\) to an outer one
\((R_Z,R_W)\) is

\[
 R_Z>r_Z+2|z_0|,\qquad R_W>r_W+2|w_0|.
\tag{3.6}
\]

This is often much larger than an ordinary adjacent-disk step.  A correct
algorithm must carry the conjugated nonlocal operator or use domains
saturated by the charge circle action.

## 4. Same-radius unboundedness

Write the quadratic fixed-point map associated with (1.1) as

\[
 \Phi(f)=(\mathcal L-1)^{-1}\left[
 (I-\Pi_0)\mathcal Q^{-1}\{f,\mathcal Qf\}
 +\Pi_0\mathcal L^{-1}\{f,\mathcal Lf\}\right].
\tag{4.1}
\]

For arbitrary positive \(\rho_Z,\rho_W\), take

\[
 f_N=\frac12\left(\rho_Z^{-N}Z^N+\rho_W^{-N}W^N\right).
\tag{4.2}
\]

Then \(\|f_N\|_\rho=1\).  The mixed output has charge \(N\), so only the
nonzero-charge branch contributes.  Direct calculation gives

\[
 \{f_N,\mathcal Qf_N\}
 =3N^3\left(\frac{\rho_Z^{-N}Z^N}{2}\right)
        \left(\frac{\rho_W^{-N}W^N}{2}\right).
\]

After the \(\mathcal Q^{-1}\) and \((\mathcal L-1)^{-1}\) multipliers,

\[
 \boxed{
 \|\Phi(f_N)\|_\rho=\frac{3N^2}{4(2N-1)}\longrightarrow\infty.
 }
\tag{4.3}
\]

### Theorem 3: no same-radius Wiener bound

The quadratic map \(\Phi\) is not bounded on the unit ball of any
\(\mathcal A_{\rho_Z,\rho_W}\).  Therefore a proof that treats (4.1) as a
bounded same-radius fixed-point equation in this Wiener norm cannot work.
This does not rule out a stronger norm, a smoothing reformulation, or a
scale-of-spaces argument.

## 5. A valid outer-to-half-radius bound

The radius loss repairs the derivative problem.  For \(n\ge0\),

\[
 \sup_n\frac{n}{2^n}=\frac12,
 \qquad
 \sup_n\frac{n^2}{2^n}=\frac98.
\tag{5.1}
\]

Hence, with \(\rho/2=(\rho_Z/2,\rho_W/2)\),

\[
 \|Xf\|_{\rho/2},\|Yf\|_{\rho/2}\le\frac12\|f\|_\rho,
\tag{5.2}
\]

\[
 \|X^2f\|_{\rho/2},\|Y^2f\|_{\rho/2}\le\frac98\|f\|_\rho,
 \qquad
 \|XYf\|_{\rho/2}\le\frac14\|f\|_\rho.
\tag{5.3}
\]

Let \(B(f,g)\) be the bilinear polarization of (4.1), so that
\(\Phi(f)=B(f,f)\).  Equations (5.2)--(5.3) give

\[
 \|(I-\Pi_0)\mathcal Q^{-1}\{f,\mathcal Qg\}\|_{\rho/2}
 \le\frac{33}{16}\|f\|_\rho\|g\|_\rho.
\tag{5.4}
\]

On the nonconstant zero-charge sector, \(\mathcal L^{-1}\) has norm at most
\(1/3\), because \(q=0\) implies total degree \(3k\ge3\).  Therefore

\[
 \|\Pi_0\mathcal L^{-1}\{f,\mathcal Lg\}\|_{\rho/2}
 \le\frac{11}{24}\|f\|_\rho\|g\|_\rho.
\tag{5.5}
\]

Finally, \((\mathcal L-1)^{-1}\) has norm at most one on total degree at
least two.  Combining (5.4)--(5.5) proves

\[
 \boxed{
 \|B(f,g)\|_{\rho/2}
 \le\frac{121}{48}\|f\|_\rho\|g\|_\rho.
 }
\tag{5.6}
\]

Consequently,

\[
 \|\Phi(f)-\Phi(g)\|_{\rho/2}
 \le\frac{121}{48}(\|f\|_\rho+\|g\|_\rho)\|f-g\|_\rho.
\tag{5.7}
\]

### Theorem 4: the correct analytic scale begins with two radii

Equation (5.6) is an explicit, all-order outer-to-inner operator estimate.
It supplies one required component of a validated continuation proof.  It is
not yet such a proof: the current statement loses half the radius in one
nonlinear evaluation and does not invert the recentered global equation.

## 6. Consequence for the continuation design

Three proposals can now be classified precisely.

1. **Copy the origin recurrence at each new Taylor center.** Invalid by
   (3.3)--(3.5).
2. **Apply Banach contraction in one fixed Wiener radius.** Invalid for the
   raw quadratic map by (4.3).
3. **Use a charge-orbit-saturated analytic scale with outer/inner radii.**
   Structurally compatible with (1.3), (2.4), and (5.6), but it still needs a
   computable inverse or smoothing formulation and rigorous tail bounds.

The result has methodological value because it prevents a false validated
continuation certificate.  Its direct value for the Millennium Problem is
still small.  A long chain remains: construct a valid continuation domain,
decide whether a reduced-edge singularity exists, prove that it controls the
relevant asymptotic mechanism, and then connect that mechanism to a
three-dimensional PDE solution class.

## 7. Next theorem target

R0.36 should not start by launching a long numerical continuation.  It should
first choose between two mathematically valid formulations.

1. Build a scale-of-spaces Newton or radii-polynomial theorem whose domain is
   saturated under \(\gamma_\theta\), with explicit outer-to-inner losses.
2. Find an equivalent smoothing/integral equation that absorbs the two Euler
   derivatives and makes the nonlinear map bounded in one weighted sequence
   space.

The first acceptable computational test is a short certified step wholly
inside the R0.31 polydisc.  Its purpose is to verify the operator, projection,
tail, and inverse bounds.  Only after that local regression passes should a
chain toward negative \(R\) be attempted.

## Reproduction

The exact audit is implemented in
`research/edge_continuation_geometry_audit.py`.  It pins the R0.31 and R0.32
input hashes, checks the projector and translation identities, records the
same-radius witness sequence, proves the half-radius constant by exact
rational arithmetic, and computes exact rational enclosures for the
candidate-distance geometry.

## References

1. Robin Pemantle, Mark C. Wilson, and Stephen Melczer,
   [*Analytic Combinatorics in Several Variables*, second-edition
   manuscript](https://acsvproject.com/acsvbook/).  Multivariate Cauchy
   coefficient extraction and contour geometry provide the standard analytic
   background for (2.2); the specialized charge contour here is derived
   directly.
2. Roberto Castelli, Marcio Gameiro, and Jean-Philippe Lessard,
   [“Rigorous numerics for ill-posed PDEs: periodic orbits in the Boussinesq
   equation”](https://arxiv.org/abs/1509.08648).  This is a primary example of
   Newton--Kantorovich/radii-polynomial validation in a geometrically weighted
   \(\ell^1\) coefficient space.
3. Maxime Breden and Jean-Philippe Lessard,
   [“Polynomial interpolation and a priori bootstrap for computer-assisted
   proofs in nonlinear ODEs”](https://arxiv.org/abs/1704.03128).  Its
   smoothing Picard reformulation motivates the second R0.36 option; no
   theorem from that paper is assumed here.
