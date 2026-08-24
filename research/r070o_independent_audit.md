# R0.70O independent audit

**Audit status:** PASS

**Audit date:** 2026-08-25

**Mode:** independent, read-only mathematical, literature-boundary, and
reproducibility audit

## 1. Scope checked

- The best-plane and best-line Rayleigh--Ritz identities.
- The coercive, near-line, and near-plane spectral partition.
- Simple-spectrum eigenvalue, eigenvector, and projector evolution.
- Spatial projector differentiation and its spectral-gap constants.
- The smooth Bessel-filtered shear obstruction, including finite time.
- The compact-band dyadic Leray--Hopf endpoint example.
- Fixed-projection lower-frame reconstruction in (L^2) and
  \(\dot H^{-1/2}\).
- The distinction between periodic and whole-space direction criteria.
- The archived exact producer and its direct Fourier covariance check.

## 2. Spectral geometry

The three regions are mutually exclusive and exhaustive when

\[
 0<2\delta<\eta<\frac12.
 \tag{2.1}
\]

The near-line and near-plane gap estimates follow from exact nonnegative
slack identities and are therefore valid with the stated strictness:

\[
 \lambda_1-\lambda_2\geq(1-2\eta)E,
 \qquad
 \lambda_2-\lambda_3>(\eta-2\delta)E.
 \tag{2.2}
\]

The best-subspace formulas agree with Rayleigh--Ritz:

\[
 \min_{|n|=1}\int |n\cdot V|^2\,d\mu=\lambda_3,
 \qquad
 \min_{|\ell|=1}\int |P_{\ell^\perp}V|^2\,d\mu
 =\lambda_2+\lambda_3.
 \tag{2.3}
\]

The report correctly distinguishes relative spectral ratios from absolute
residual size.

## 3. Evolution and direction regularity

Starting from

\[
 \dot Q=\Sigma Q+Q\Sigma+F,
 \qquad \Sigma=\Sigma^{\mathsf T},\quad F=F^{\mathsf T},
 \tag{3.1}
\]

direct differentiation in a simple-spectrum eigenbasis confirms the reported
eigenvalue, eigenvector, and projector formulas.  The denominators use the
correct external spectral gaps.  The report also handles collision spectra,
rank boundaries, and cluster projectors at the correct level of generality.

The Frobenius constant in the spatial estimate is correct.  In the eigenbasis,

\[
 \|\partial_iP_1\|_F^2
 =2\sum_{b=2}^3
 \frac{|e_b^{\mathsf T}(\partial_iQ)e_1|^2}
      {(\lambda_1-\lambda_b)^2}
 \leq
 \frac{\|\partial_iQ\|_F^2}
      {(\lambda_1-\lambda_2)^2}.
 \tag{3.2}
\]

For a local unit lift (v),

\[
 \|\partial_iP_1\|_F=\sqrt2\,|\partial_iv|.
 \tag{3.3}
\]

This does not remove the separate global orientability issue.

## 4. Smooth dynamic obstruction

For the explicit Bessel-filtered shear, the divergence, zero nonlinear term,
heat evolution, vorticity, filtered covariance, and principal direction were
recomputed independently.  Requiring (N_q\geq2) rules out the only possible
frequency coincidence.

The infinite-time constants are

\[
 \|r_N\|_{L_t^2}
 =\frac{A(Ne_2)}{4\sqrt\nu},
 \qquad
 \|P_{e_3^\perp}\omega_N\|_{L_t^4L_x^2}
 =\frac1{2\nu^{1/4}}.
 \tag{4.1}
\]

For every fixed (T>0), with

\[
 \theta_{N,T}=1-e^{-4\nu N^2T},
 \tag{4.2}
\]

the finite-horizon computation gives the sharp identity

\[
 \frac{
 \|P_{e_3^\perp}\omega_N\|_{L^4(0,T;L^2)}^2}
 {\|r_N\|_{L^2(0,T)}}
 =\frac1{A(Ne_2)}
 \tag{4.3}
\]

whenever (A(Ne_2)>0).  Thus the example rules out a uniform quantitative
reconstruction estimate, or a modulus continuous at zero, under the stated
high-frequency-decay hypothesis.  It does not rule out all PDE-mediated
bridges.

The direct Fourier calculation for the archived (N=8) calibration also
recovers

\[
 Q(0)=\operatorname{diag}\!\left(
 \frac4{4225},0,\frac{4241}{8450}
 \right).
 \tag{4.4}
\]

## 5. Compact-band endpoint and lower-frame theorem

The compact-band dyadic example is a Leray--Hopf shear with initial datum in
(L^2\setminus H^1), observed rank-one covariance, and zero observed best-line
residual.  Tonelli's theorem and the diagonal terms give

\[
 \frac1{8\nu}\sum_{k,l}
 \frac{n_kn_l}{n_k^2+n_l^2}
 \geq\frac1{16\nu}\sum_k1
 =\infty.
 \tag{5.1}
\]

The fixed-projection reconstruction conditions are also correct.  Parseval
and a single-mode test give the stated necessity and sufficiency of

\[
 A(k)\geq a_0
 \tag{5.2}
\]

for (L^2) reconstruction, and

\[
 A(k)\geq a_0|k|^{-1}
 \tag{5.3}
\]

for \(\dot H^{-1/2}\) reconstruction.  The time bridge has the correct
constant (a_0^{-2}).

## 6. Literature and domain boundaries

The report's descriptions of Chae--Choe, Miller, and
Constantin--Fefferman agree with the checked primary sources.  In particular,
it preserves all of the following limitations:

1. The exact obstruction is periodic, while the cited Miller theorem is
   stated on \(\mathbb R^3\).  A periodic analogue must be cited or proved, or
   the bridge must be rebuilt on \(\mathbb R^3\), before that theorem can be
   invoked directly.
2. The smooth sequence excludes a uniform quantitative reconstruction; it
   does not exclude qualitative finiteness for each individual smooth
   solution.
3. The dyadic example gives qualitative failure only at a rough initial
   endpoint and does not contradict an (H^1)-data criterion.
4. The smooth obstruction is concentrated in an initial layer of order
   (N^{-2}) and does not disprove a positive-delay estimate whose constant
   may depend on the delay.
5. A finite filter family is not by itself enough for the no-go statement.
   The assumption (A(N_qe_2)\to0) is essential; an identity observation is
   excluded.

## 7. Reproducibility result

The producer reproduced byte-identically against the archived result.

SHA-256:

    33c8361bdfed507526aa948fc6c74d964292c79015949ba2c748190bd4ba1134

The regenerated and archived `result.json` files have the same hash.  The
independent audit also checked the newly added direct Bessel--Fourier
covariance integration rather than relying only on the closed-form matrix.

## 8. Claim boundary

The certified negative conclusion is narrow:

> A high-frequency-blind scalar Fourier-filter frame cannot, through its
> observed best-line residual alone, provide a uniform zero-continuous
> quantitative reconstruction of the unfiltered transverse critical
> vorticity norm.

The positive lower-frame theorem identifies the missing all-frequency
observability condition for a fixed projection.  The report does not claim a
new regularity criterion, a singular solution, global smoothness, or a
solution of the Millennium problem.

No remaining mathematical, literature-boundary, or reproducibility
correction is required for the audited R0.70O core claim.
