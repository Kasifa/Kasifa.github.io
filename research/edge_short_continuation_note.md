# R0.36: a certified short recentering step inside the R0.31 polydisc

## Status and boundary

R0.35 proves that the raw active fixed-point map is unbounded on a
same-radius Wiener ball.  It also proves the outer-to-half-radius estimate

\[
 \|\Phi(f)-\Phi(g)\|_{\rho/2}
 \le \frac{121}{48}
 (\|f\|_\rho+\|g\|_\rho)\|f-g\|_\rho.
\tag{0.1}
\]

This note shows how to use that loss correctly after moving the Taylor
center.  The local equation is conjugated back to the origin, not rewritten
with a false local charge projector.  An exact rational short step is then
certified wholly inside the R0.31 domain.

The operator theorem and the tail enclosure below are all-order statements.
The degree-40 polynomial, the five projector checks, and the
degree-2-through-8 Jacobian inverse are finite exact regressions.  The step
does not leave the R0.31 polydisc, reach the R0.32 Padé candidate, or imply
regularity or singularity for the three-dimensional Navier--Stokes equation.

## 1. Translation between Wiener algebras

For a center \(c=(c_Z,c_W)\), write

\[
 (\tau_cf)(\zeta,\omega)=f(c_Z+\zeta,c_W+\omega).
\tag{1.1}
\]

Let \(\mathcal A_{r_Z,r_W}\) be the weighted Wiener algebra used in R0.35.
The binomial theorem gives the exact operator estimate

\[
 \boxed{
 \|\tau_cf\|_{r_Z,r_W}
 \le
 \|f\|_{|c_Z|+r_Z,\,|c_W|+r_W}.
 }
\tag{1.2}
\]

Indeed, the weighted coefficient sum of
\((c_Z+\zeta)^n(c_W+\omega)^k\) is exactly
\((|c_Z|+r_Z)^n(|c_W|+r_W)^k\).  Applying the same argument to translation
by \(-c\) gives

\[
 \|\tau_c^{-1}g\|_{S_Z,S_W}
 \le
 \|g\|_{|c_Z|+S_Z,\,|c_W|+S_W}.
\tag{1.3}
\]

These inequalities do not require a finite Taylor cutoff.

## 2. The conjugated two-radius theorem

Let

\[
 \Phi_c=\tau_c\Phi\tau_c^{-1}
\tag{2.1}
\]

be the correctly recentered nonlinear map.  Use local outer radii
\(\mathsf R_i\) and inner radii \(\mathsf r_i\), and define

\[
 S_i=\mathsf R_i-|c_i|,
 \qquad
 s_i=\mathsf r_i+|c_i|,
 \qquad
 \lambda=\max_i\frac{s_i}{S_i}.
\tag{2.2}
\]

The necessary separation is

\[
 \mathsf R_i>2|c_i|+\mathsf r_i,
\tag{2.3}
\]

which is the same affine-orbit margin found in R0.35.

For \(0<\lambda<1\), put

\[
 M_j(\lambda)=\sup_{n\ge0}n^j\lambda^n.
\tag{2.4}
\]

The origin calculation behind R0.35 works at any radius ratio:

\[
 \|\Phi(f)-\Phi(g)\|_s
 \le C(\lambda)(\|f\|_S+\|g\|_S)\|f-g\|_S,
\tag{2.5}
\]

where

\[
 \boxed{
 C(\lambda)=\frac{11}{3}M_1(\lambda)
 \left(M_2(\lambda)+M_1(\lambda)^2\right).
 }
\tag{2.6}
\]

The nonzero-charge branch contributes
\(3M_1(M_2+M_1^2)\).  The charge-zero branch contributes
\(\frac23M_1(M_2+M_1^2)\); the factor \(1/3\) is the norm of
\(\mathcal L^{-1}\) on nonconstant charge-zero monomials.  The remaining
inverses have norm at most one on their respective sectors.

Combining (1.2), (1.3), and (2.5) proves the local theorem

\[
 \boxed{
 \|\Phi_c(f)-\Phi_c(g)\|_{\mathsf r}
 \le C(\lambda)
 (\|f\|_{\mathsf R}+\|g\|_{\mathsf R})
 \|f-g\|_{\mathsf R}.
 }
\tag{2.7}
\]

This proof carries the entire operator back to the origin.  It therefore
uses the correct global charge projector automatically.

## 3. An exact step along the negative fixed-charge axis

Let

\[
 \rho_*=\frac4{81}
\tag{3.1}
\]

be the R0.31 certified common radius.  Choose

\[
 \delta=\frac{\rho_*}{7}=\frac4{567},
 \qquad
 c=(\delta,-\delta),
\tag{3.2}
\]

and take isotropic local radii

\[
 \mathsf r=\delta,
 \qquad
 \mathsf R=5\delta.
\tag{3.3}
\]

The complete outer local disc lies in the origin polydisc because

\[
 |c_i|+\mathsf R=6\delta=\frac67\rho_*<\rho_*.
\tag{3.4}
\]

The affine charge orbit of the inner local disc lies in the outer one because

\[
 \mathsf r+2\delta=3\delta<5\delta=\mathsf R.
\tag{3.5}
\]

After conjugation,

\[
 S=\mathsf R-\delta=4\delta,
 \qquad
 s=\mathsf r+\delta=2\delta,
 \qquad
 \lambda=\frac12.
\tag{3.6}
\]

Thus

\[
 C(\lambda)=\frac{121}{48}
\tag{3.7}
\]

exactly, with no extra radius estimate.

At the center, the fixed-charge coordinate is

\[
 R_{\rm ch}=Z^2W=-\delta^3
 =-\frac{64}{182284263}.
\tag{3.8}
\]

Its modulus is \(1/343\) of the R0.31 fixed-charge radius
\(\rho_*^3=64/531441\).  This is a deliberately short regression step in the
relevant negative direction, not progress to the distant R0.32 candidate.

## 4. An all-order inclusion around the degree-40 polynomial

Let

\[
 a=\sum_{L\ge1}a_L,\qquad
 p_N=\tau_c\sum_{L=1}^N a_L.
\tag{4.1}
\]

R0.31 proves

\[
 \|a_L\|_1\le\frac{2K^{L-1}}{L^3},
 \qquad K=\frac{81}{4}.
\tag{4.2}
\]

For \(0<x<1\), define the rational tail

\[
 E_N(x)=\frac2K
 \frac{x^{N+1}}{(N+1)^3(1-x)}.
\tag{4.3}
\]

Since \(L^{-3}\le(N+1)^{-3}\) for \(L>N\), (4.2) and the geometric series
give

\[
 \|\,\tau_c a-p_N\,\|_{\mathsf R}
 \le E_N(6/7),
\qquad
 \|\,\tau_c a-p_N\,\|_{\mathsf r}
 \le E_N(2/7).
\tag{4.4}
\]

The complete outer norm satisfies

\[
 \|\tau_ca\|_{\mathsf R}
 \le \frac2K\frac{6/7}{1-6/7}
 =\frac{16}{27}.
\tag{4.5}
\]

Consequently, with

\[
 F_c(p)=p-\tau_ca_1-\Phi_c(p),
\tag{4.6}
\]

the exact solution identity and (2.7) imply

\[
 \boxed{
 \|F_c(p_N)\|_{\mathsf r}
 \le
 E_N(2/7)
 \frac{121}{48}
 \left(\frac{32}{27}+E_N(6/7)\right)E_N(6/7).
 }
\tag{4.7}
\]

For \(N=40\), every quantity in (4.4)--(4.7) is an exact rational number.
The audit stores the full fractions, decimal views, digit counts, and
SHA-256 digests.  The inclusion (4.4) is all-order: the finite recurrence is
used to define the center polynomial, while the uncomputed tail is covered
by (4.2).

## 5. Finite exact operator and inverse regressions

The audit reconstructs the normalized active recurrence through degree 40
over GMP rationals.  It then checks, without floating-point decisions:

1. the origin residual vanishes through degree 40;
2. translating to \(c\) and back recovers every coefficient exactly;
3. \(X_c=(\delta+\zeta)\partial_\zeta\) and
   \(Y_c=(-\delta+\omega)\partial_\omega\) agree with conjugation;
4. the local bracket and five charge projectors agree with
   \(\tau_c(\cdot)\tau_c^{-1}\);
5. the complete finite nonlinear residual agrees by both routes;
6. its exact inner Wiener norm lies below the all-order bound (4.7).

For an inverse regression, let \(H_8\) be the polynomial perturbations of
origin total degrees 2 through 8.  The projected Jacobian

\[
 J_8=P_8(I-D\Phi(a^{[40]}))|_{H_8}
\tag{5.1}
\]

is unit lower triangular in increasing total degree.  Its exact inverse is
constructed by forward substitution and checked on both sides.  Translation
conjugates this inverse to \(\tau_cH_8\).

This 42-dimensional inverse is finite.  It does not control the infinite
tail and is not a Newton--Kantorovich existence proof outside R0.31.

## 6. What the certificate establishes

The positive result is a first correct recentering certificate:

- the local projector is the conjugated global projector;
- the affine charge orbit stays inside a declared outer domain;
- the derivative loss is paid by two explicit radii;
- the exact translated polynomial has an all-order tail enclosure;
- a small structural Jacobian block has an exact two-sided inverse.

The exact solution inside the final inclusion ball is already guaranteed by
R0.31.  Therefore R0.36 validates the recentering architecture, but it does
not yet establish an independent restart beyond the previously known domain.

The next step is to replace the finite inverse regression by a computable
infinite inverse bound on a nested analytic scale.  Only then can a short
step crossing the R0.31 boundary be attempted.

## Reproduction

Run research/edge_short_continuation_audit.py with the pinned R0.31 and
R0.35 certificate hashes.  The formal run records an append-only progress
log and a process-tree resource log.  No random seed or floating-point sign
test is used.

## References

1. R0.31, *An improved common analytic domain for the canonical edge
   system*.  This supplies (4.2) and the certified radius \(\rho_*\).
2. R0.35, *Charge-projection geometry and the obstruction to naive
   recentering*.  This supplies the conjugated projector and the
   outer-to-half-radius constant.
3. Roberto Castelli, Marcio Gameiro, and Jean-Philippe Lessard,
   [“Rigorous numerics for ill-posed PDEs: periodic orbits in the Boussinesq
   equation”](https://arxiv.org/abs/1509.08648).  Its radii-polynomial
   workflow is a reference for the later infinite-inverse stage; no theorem
   from that paper is invoked here.
