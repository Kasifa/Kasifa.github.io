# R0.74S Step 13 — independent adversarial audit

## 0. Frozen object and verdict

The audited note is
research/r074s_temporal_integrability_morrey_threshold.md, with frozen
SHA-256
d22a4e06b55325009b3d3930d0f8c0b96b4b4a7d3cdf1386a4158b0446e367de.

**Final verdict: PASS within the stated analytic and abstract scope.**

The first read-only pass returned FAIL because five quantifier or binding
defects could make otherwise correct calculations false as written.  The
main note was revised, and a second read-only pass checked every repair.
No audit agent edited the note or certificate sources.

## 1. Dimensionless rate and common-deletion order

The change \(t=s_R+R^2\sigma\) gives

\[
 \|R^2g(s_R+R^2\cdot)\|_{L^p_\sigma}
 =R^{2-2/p}\|g\|_{L^p_t}.
\]

Thus the powers are \(R^{1/2}\) at \(p=4/3\) and \(R^2\) at
\(p=\infty\).  The deletion set in (S.309) is chosen outside the sum of
time norms, so the argument uses one shell set on the whole terminal
window.  It does not substitute a time-dependent exceptional set.

For each shell, the time norm is applied first; the resulting norms are
then summed using the common coefficient envelope in (S.313):

\[
 \sum_k\|h_{k,R}\|_{4/3}
 \le C\left(\sum_k\gamma_k(1+2^{3k}R^3)\right)
       \|\mathcal B_R\|_{4/3}.
\]

Here \(\mathcal B_R(\sigma)\) is explicitly defined as the bracket in
(S.313), evaluated at \(t=t(\sigma)\).  This is a genuine
\(\ell^1(L^{4/3})\) estimate; no invalid interchange with
\(L^{4/3}(\ell^1)\) occurs.

## 2. Energy and pressure endpoint

The energy-class interpolation

\[
 v_R\in L_t^4L_x^3
\]

and the mean-zero periodic Calderón--Zygmund estimate place
\(\pi_R-\bar\pi_R\) in \(L_t^2L_x^{3/2}\).  The pressure-velocity product
and the cubic term therefore lie in \(L_t^{4/3}\).  The scale factors in
(S.310)--(S.313) cancel correctly on a window of length
\(\delta R^2\), giving the powers \(\delta^{1/4}\) and \(\delta\).

The admissible-pair formula is stated with \(2<r\le6\), while
\(q(2)=\infty\) is handled separately.  The note claims \(4/3\) only as
the endpoint supplied by direct energy interpolation.  It does not exclude
better integrability under additional PDE hypotheses.

## 3. Temporal optimization

For \(a_p=1-1/p\), balancing

\[
 C_H\delta^{a_p}P^\beta
 +C_{\rm deep}\delta^{-2/3}P^{2/3}
\]

gives

\[
 \delta_{p,\beta}\asymp
 P^{-(\beta-2/3)/(a_p+2/3)},
 \qquad
 E_{p,\beta}={2\over3}{a_p+\beta\over a_p+2/3}.
\]

The special values are exact:

\[
 p={4\over3}:\quad (\delta,E)=(P^{-4/11},10/11),
 \qquad
 p=\infty:\quad (\delta,E)=(P^{-1/5},4/5).
\]

These are ceilings for the stated two-term method under a hypothetical
linear payment bound.  They are not lower bounds attained by every
Navier--Stokes solution.

## 4. Smooth abstract witnesses

The fixed-profile construction has \(M=N+1\) equal coordinates, so deleting
\(N\) coordinates leaves exactly one.  Its conclusion concerns abstract
rate vectors and not a PDE realization.

The adaptive witness now has all required data:

- \(P\ge1\);
- \(0\le\rho\in C_c^\infty((-1,0))\),
  \(\|\rho\|_{4/3}=1\), and \(c_\rho=\int\rho>0\);
- \(d=P^{-4/11}\), abstract depths \(d_{k,P}=d\), and residuals
  \(r_{k,P}=c_\rho P^{10/11}/M\); and
- a terminal whose scaled support lies inside \((0,4)\).

For \(\delta\ge d\), the common window contains the whole bump.  For
\(0<\delta<d\),

\[
 c_\rho P^{10/11}
 \le c_\rho P^{2/3}\delta^{-2/3},
\]

with the tight boundary at \(\delta=d\).  Hence the abstract witness checks
the rate and depth ledgers simultaneously, rather than merely matching two
powers numerically.

## 5. Moving-Morrey threshold and heat shear

The two-cap countermodel now explicitly binds

\[
 x_k^{\rm sel}=b_k={T_P\over N+1}.
\]

This makes the failure for \(\theta>2/3\) a literal countermodel to the two
scalar hypotheses in (S.327).  It remains an abstract sequence, not a
dissipation measure or an NSE solution.

The heat-shear screen assumes \(A>0\) and \(T>0\).  Its nonlinear term
vanishes, periodic integration in \(y_1\) gives zero physical shell flux,
and the exact constants in (S.334) are correct.  High Fourier frequency is
therefore not by itself a physical-annulus flux mechanism.

## 6. Critical tree and cubic incidence theorem

For \(L=m^3\), level summation gives

\[
 \sum_vp_v=1,
 \qquad
 \sum_vb_v=m,
 \qquad
 \sum_vs_v={5m\over3},
 \qquad
 b_v=c_vp_v^{2/3}.
\]

The square ledger and subtree square-Carleson estimate are correct.  The
child-cube identity is now restricted to nonterminal nodes
\(0\le d(v)\le L-2\); it is not asserted at a leaf.  The scaled
high-Rayleigh row is bound through

\[
 \int_{H_v}g_v=b_v={3\over5}s_v,
\]

so it does not reuse the temporal density symbol \(h_{k,R}\).

The incidence theorem uses Hölder with exponents \(3\) and \(3/2\), and
the cubic duality formula is exact.  To turn a tree inequality into the
incidence-level coefficient bound, the note now assumes all three uniform
inputs:

1. bounded total root cube mass;
2. bounded coefficient-incidence multiplicity; and
3. a nonnegative coefficient-decay sequence whose Dini product sum is
   uniformly bounded over every starting depth.

They imply

\[
 \sum_{\rm incidences}c_\nu^3
 \le M_{\rm inc}C_{\rm root}C_D.
\]

The critical eight-ary model has \(\theta_d=1\), and its truncated Dini
constant grows like \(L=m^3\).  Finite depth alone therefore supplies no
uniform \(C_c\).

## 7. Mechanical and claim-boundary audit

- Equation tags are exactly S.307--S.342, sequential and unique.
- All display delimiters balance.
- The source is UTF-8 and has no NUL, carriage return, or trailing
  whitespace damage.
- The analytic note contains no DNS or DGX evidence.
- The fixed-solution temporal estimate is not promoted to a uniform payment
  estimate.
- The smooth rate families and the eight-ary tree remain labeled abstract,
  not NSE counterexamples.
- (S.328), (S.340), and (S.342) retain their conditional or open status.
- S.280, S.288, S.303, S.272, Q.12, Q.1, regularity, singularity formation,
  and the Millennium problem remain open.

The audit therefore supports freezing Step 13 as a rigorous method-screening
advance.  It does not certify a regularity theorem or a Clay solution.
**NOT CLAY.**
