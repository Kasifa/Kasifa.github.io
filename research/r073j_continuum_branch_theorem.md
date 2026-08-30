# R0.73J continuum spectral-branch theorem

**Status:** theorem assembled from sealed analytic and interval inputs; final
release still requires the remaining publication gates  
**Parameter window:** \(0\le d\le D_*=1/450\)  
**Operator row:** \((\beta,\xi,\gamma)=(0,0,1/2)\)

## 1. The statement

Let

\[
 W_d(x)=-\frac12e^{-d}\sin x+\frac14e^{-4d}\sin2x,
 \qquad L=-\partial_x^2+\frac14,
 \tag{1.1}
\]

and let \(X\simeq H^{-1}_{\rm per}(\mathbb T)\) have inner product

\[
 \langle q_1,q_2\rangle_X
 =4\langle L^{-1}q_1,q_2\rangle_{L^2}.
 \tag{1.2}
\]

Define

\[
 A_X(d)=-\frac i2\left(M_{W_d}+M_{W_d''}L^{-1}\right).
 \tag{1.3}
\]

The analytic proof and the two validated interval certificates imply the
following theorem.

### Theorem R0.73J

There is a real-analytic function

\[
 \lambda_0:[0,1/450]\longrightarrow(167/1000,173/1000)
 \tag{1.4}
\]

such that, for every \(d\in[0,1/450]\):

1. \(\lambda_0(d)\) is a real, algebraically simple eigenvalue of
   \(A_X(d)\);
2. it is the only spectral point with real part greater than \(11/100\);
3. every other spectral point satisfies
   \[
   \operatorname{Re}z\le\frac{11}{100};
   \tag{1.5}
   \]
4. the real-part gap is therefore strictly greater than \(57/1000\), and in
   particular admits the conservative uniform value
   \[
   g_*=\frac1{20};
   \tag{1.6}
   \]
5. normalized right and kinetic-adjoint eigenvectors \(h_d,\ell_d\in X\)
   can be chosen with
   \[
   \frac{|\langle\ell_d,h_d\rangle_X|}
   {\|\ell_d\|_X\|h_d\|_X}>0.5853>\frac12;
   \tag{1.7}
   \]
6. the fixed bounded functional
   \[
   \mathfrak a(h)=(L^{-1}h)(0)
   \tag{1.8}
   \]
   is nonzero on the selected right eigenvector throughout the branch.

The word *spectral branch* in this statement refers to the discrete spectrum
of the infinite-dimensional operator.  It does not mean continuous spectrum.

## 2. Analytic inputs

The source snapshot
`research/r073j_analytic_proof.md`, SHA-256
`81061d6f77e97fca33dafa0643820ab3860ae02b4042fe742eac1d91f1f108f0`,
proves the following facts.

1. The Fredholm essential spectrum is
   \[
   \sigma_{\rm ess}(A_X(d))
   =-\frac i2\operatorname{Ran}W_d\subset i\mathbb R.
   \tag{2.1}
   \]
   Every right-half-plane spectral point is therefore an isolated eigenvalue
   of finite algebraic multiplicity.
2. Generalized right-half-plane root spaces in \(X\) and in the ordinary
   \(L^2\) realization coincide by a Sobolev bootstrap.
3. With
   \[
   T(d,\lambda)=-\partial_x^2+\frac14+
   \frac{W_d''}{W_d-2i\lambda},
   \tag{2.2}
   \]
   the exact factorization
   \[
   (\lambda-A_2(d))L
   =M_{\lambda+iW_d/2}T(d,\lambda)
   \tag{2.3}
   \]
   and the periodic BVP/IVP block equivalence imply
   \[
   \operatorname{ord}_{\lambda_*}E(d,\lambda)
   =\operatorname{algmult}_{A_X(d)}(\lambda_*).
   \tag{2.4}
   \]
4. Reflection followed by conjugation gives
   \[
   E(d,\bar\lambda)=\overline{E(d,\lambda)}.
   \tag{2.5}
   \]
5. Every right-half-plane eigenvalue obeys the analytic Howard bound
   \[
   |\lambda|\le\frac{3\sqrt3}{16}<\frac{13}{40}.
   \tag{2.6}
   \]

The independent line-by-line audit is
`research/r073j_analytic_audit.md`, SHA-256
`f134d4a828ed0f91c62899a41e9640b8e5ed211f375a4a92913e76a1f537de5e`.

## 3. Contour certificate

Let

\[
 \Omega=\left\{\frac{11}{100}<\operatorname{Re}\lambda<\frac{19}{50},
 \quad |\operatorname{Im}\lambda|<\frac{19}{50}\right\},
 \tag{3.1}
\]

and

\[
 B_{\rm loc}=\left\{|\lambda-17/100|<3/1000\right\}.
 \tag{3.2}
\]

The file `experiments/r073j/contour_certificate.json`, SHA-256
`60c770beaf0dc9a3da99ba6ab7bff234b506aa7d8bc72a0aad7b55471b571a38`,
records a validated Arb/Acb calculation with source digest
`736ebbcdad0f0897a1be100352aec7163f0483a1f323e6a4f1466dd43d7353f8`.
Its decisive outputs are:

\[
 \inf_{\substack{0\le d\le1/450\\
                  \lambda\in\partial\Omega}}
 |E(d,\lambda)|>5.49948,
 \tag{3.3}
\]

\[
 \inf_{\substack{0\le d\le1/450\\
                  \lambda\in\partial B_{\rm loc}}}
 |E(d,\lambda)|>0.164355,
 \tag{3.4}
\]

and exact rational-polygon windings

\[
 \operatorname{wind}E(0,\partial\Omega)
 =\operatorname{wind}E(0,\partial B_{\rm loc})=1.
 \tag{3.5}
\]

The primary range method uses outward-rounded interval Clenshaw evaluation
on a complete dyadic real-box cover.  The independent post-processing file
`experiments/r073j/independent_validation.json`, SHA-256
`203b7af48933cdb49c0a0b59751c0b0435cf26ae48ea01e08f203900ad554d57`,
uses a separate direct two-dimensional DCT and the reverse Clenshaw axis
order.  It independently obtains both windings equal to one and the global
and local lower bounds (5.49739\ldots) and (0.164339\ldots).  It shares
the raw ODE grid and is classified accordingly; it is not described as a
fully independent ODE proof.

## 4. Zero count, reality, simplicity, and the gap

The Evans function is jointly continuous in real \(d\) and holomorphic in
\(\lambda\) on the two contour interiors.  Equations (3.3)--(3.5), homotopy
in \(d\), and the argument principle give exactly one zero counted with
order in each of \(\Omega\) and \(B_{\rm loc}\), for every
\(d\in[0,1/450]\).

The local disk is contained in the global rectangle.  Consequently its zero
is the global zero.  Both regions are invariant under conjugation.  If the
single zero were nonreal, (2.5) would supply its distinct conjugate and the
count would be at least two.  The zero is therefore real.  A total zero order
of one makes it a simple Evans zero; (2.4) makes the kinetic eigenvalue
algebraically simple.

The analytic implicit-function theorem supplies a local real-analytic branch
at every \(d\).  Uniqueness in the fixed local disk glues these local branches
into the function in (1.4).

The Howard disk (2.6) lies strictly inside the top, bottom, and right sides of
\(\Omega\).  It follows that every right-half-plane spectral point with real
part greater than \(11/100\) lies in \(\Omega\).  The global count therefore
excludes every such point except \(\lambda_0(d)\).  The essential spectrum is
on the imaginary axis.  Equations (1.4) and (1.5) now give

\[
 \operatorname{Re}\lambda_0(d)
 -\sup\operatorname{Re}\bigl(\sigma(A_X(d))\setminus\{\lambda_0(d)\}\bigr)
 >\frac{167}{1000}-\frac{11}{100}
 =\frac{57}{1000}>\frac1{20}.
 \tag{4.1}
\]

## 5. Kinetic overlap and phase anchor

The source snapshot
`research/r073j_overlap_analytic_proof.md`, SHA-256
`89c94e9d3ab9cd892f4f20ff8d2a3932b3f5fef6e82135ea2e64f39148c42f02`,
constructs plus/minus holomorphic substitutes for every conjugated quantity
used on the real parameter rectangle.  At an Evans zero, let

\[
 h=L\phi,
 \qquad
 p=\frac{\bar\phi}{W_d+2i\lambda_0(d)},
 \qquad
 \ell=Lp.
 \tag{5.1}
\]

Then \(A_Xh=\lambda_0h\), \(A_X^*\ell=\lambda_0\ell\), and

\[
 \frac{|\langle\ell,h\rangle_X|}
 {\|\ell\|_X\|h\|_X}
 =\frac{|N|}{\sqrt{E_rE_p}},
 \tag{5.2}
\]

where

\[
 N=-\int_{\mathbb T}
 \frac{W_d''\phi^2}{(W_d-2i\lambda_0)^2}\,dx.
 \tag{5.3}
\]

The file `experiments/r073j/overlap_certificate.json`, SHA-256
`12e1505cacb807d83a611b96d5b928bd4302c9faef16030566d3e178234180ab`,
validates the complete rectangle

\[
 0\le d\le1/450,
 \qquad 167/1000\le\lambda\le173/1000.
 \tag{5.4}
\]

Its midpoint-Bernstein ranges, direct Chebyshev coefficient-residual bounds,
and analytic interpolation remainders give

\[
 |M_{12}|>1.84154,
 \qquad
 \frac{|N|}{\sqrt{E_rE_p}}>0.585343.
 \tag{5.5}
\]

The first inequality fixes a nonzero selected solution.  Since
\(L^{-1}:X\to H^1_{\rm per}\) and one-dimensional point evaluation is bounded
on \(H^1\), (1.8) is a fixed bounded functional on \(X\).  On the selected
vector \(h=L\phi\),

\[
 \mathfrak a(h)=\phi(0)=M_{12}\ne0.
 \tag{5.6}
\]

The second inequality is invariant under rescaling and proves (1.7) after
normalization.

## 6. Independent numerical audits

The contour post-processing audit and the overlap post-processing audit use
independent implementations but share the frozen raw Arb/Acb grids.  This
distinction is part of the evidence, not a footnote.

The overlap audit
`experiments/r073j/independent_overlap_validation.json` reconstructs all
\(4\times841=3364\) tensor-grid balls with a direct DCT, ranges a complete
\(3\times4\) dyadic cover by a cell-centre plus Chebyshev-derivative
Lipschitz method, and rechecks all 128 primary midpoint--Bernstein cells.  It
obtains the independent lower bound

\[
 \frac{|N|}{\sqrt{E_rE_p}}>0.5850094448>\frac12.
 \tag{6.1}
\]

The initial direct natural-parameter-box ODE audit is preserved in
`experiments/r073j/natural_box_validation.json`.  It used 120 decimal digits,
Taylor order 14, and 2048/1024 ODE steps without importing the primary ODE
implementation.  Seventy-six of 83 boxes passed at their frozen widths; seven
were *inconclusive because of interval wrapping*.  None failed a denominator
or Picard-tube condition.  The preserved depth-two refinement resolved only
one of those seven parent boxes.  A subsequent complete adaptive refinement,
recorded in `experiments/r073j/natural_box_refinement_deep.json`, split every
remaining failed branch through depth five.  Its 2,896 final leaves all pass,
with minimum Evans lower bound greater than \(0.00714950\), so all 83 selected
natural boxes are now covered directly or by passing leaves.  This spot audit
is still corroborative only: 83 selected boxes do not replace the complete
parameter-uniform contour cover.

## 7. Evidence boundary

The theorem uses validated computation as a proof input.  The raw contour
grid contains 21,632 Arb/Acb ODE points, and the overlap grid contains 841.
The package preserves the configurations, source ledgers, checkpoints,
progress logs, resource logs, rejected wrapping methods, replacement
analyses, and independent post-processing.

This theorem does not establish any of the following:

- uniform persistence of a viscous rank-one branch;
- a two-sided selected-gain action or bounded prefactor;
- a nonselfadjoint adiabatic remainder for the moving operator;
- a prescribed exponential seed on a fixed background;
- transverse three-dimensional nonlinear closure;
- finite-time singularity or the Clay problem.

Those statements remain separate later gates.
