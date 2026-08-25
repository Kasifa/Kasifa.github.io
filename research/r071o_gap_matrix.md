# R0.71O gap matrix — soft denominator faces and the unpaid fixed-partition sum

## 0. Claim boundary

This matrix separates six evidence classes:

1. **exact theorem**;
2. **independent numerical corroboration**;
3. **abstract functional separation**;
4. **genuine NSE one-sided initial jet**;
5. **conditional implication**;
6. **open claim**.

The starting observable is

\[
 R_\varepsilon=\sqrt{d+\varepsilon},\qquad
 z_\varepsilon=\frac{B}{\sqrt YR_\varepsilon},\qquad
 a_\varepsilon=(z_\varepsilon^+)^2
 =\frac{(B^+)^2}{Y(d+\varepsilon)},
 \tag{0.1}
\]

for one fixed real-even scalar multiplier, one fixed real smooth cutoff, and a
classical zero-mean periodic Navier--Stokes solution.  The soft formulas require
\(Y>0\).  The hard direction additionally requires \(d>0\).

The exact producer is `research/r071o_exact_audit.py`.  The standalone checker
is `research/r071o_independent_audit.py`; it imports neither the producer nor
earlier release code.  Numerical rows corroborate, but do not prove, the exact
rows.  Nothing here proves a uniform NSE face sum, a continuation criterion,
a singularity, global regularity, originality, priority, or a solution of the
Millennium problem.

## 1. Classification matrix

| Statement | Classification | Evidence | Exact scope | What it does not say |
|---|---|---|---|---|
| \((z_\varepsilon)_t=B_t/(\sqrt YR_\varepsilon)-\tfrac12z_\varepsilon(Y_t/Y+d_t/(d+\varepsilon))\) | exact theorem | quotient rule; report (2.2); exact producer `soft_identity` | fixed \(\varepsilon>0\), \(Y>0\), classical time derivatives | no uniform \(\varepsilon\downarrow0\) estimate |
| The N-style and I-style sources differ by \(\lambda\theta_\varepsilon z_\varepsilon\), where \(\theta_\varepsilon=\varepsilon/(d+\varepsilon)\) | exact theorem | report (1.2)--(1.4); exact symbolic simplification | same fixed-cell observable | the two conventions must not be interchanged termwise |
| On \(d>0\), \(z_\varepsilon=\sqrt{\sigma_\varepsilon}z\) and \(a_\varepsilon=\sigma_\varepsilon a\), with \(\sigma_\varepsilon=d/(d+\varepsilon)\) | exact theorem | report Theorem 3.1, (3.3)--(3.6) | each connected hard component | no hard direction at \(d=0\) |
| The exact N-style face source is \((\sigma_\varepsilon)_ta\) | exact theorem | differentiate \(a_\varepsilon=\sigma_\varepsilon a\); report (3.5) | cancellation-preserving joint source | no sign or total face payment after the shell--cell sum |
| An isolated finite-order zero has traces \(A_+=(b^+)^2/(Y_0q)\), \(A_-=(((-1)^mb)^+)^2/(Y_0q)\) | exact theorem | report Theorem 4.1, (4.1)--(4.5); exact inner profile \(s^{2m}/(1+s^{2m})\) | the classical \(C^1\) Taylor jet and derivative remainder stated in Theorem 4.1, \(q=\|c\|^2>0\), \(Y_0>0\) | flat, accumulating, interval, or leading-pairing-degenerate zeros are not covered |
| The signed, positive, negative, and total-variation atoms are respectively \((A_+-A_-)\delta_{t_0}\), \(A_+\delta_{t_0}\), \(A_-\delta_{t_0}\), and \((A_++A_-)\delta_{t_0}\) | exact theorem | report (4.6)--(4.10); unit mass of the inner derivative profile | atomic contribution of one shrinking soft layer | no uniform sum over zeros, cells, shells, or near a singular endpoint |
| When both traces are active, the relaxed soft-layer excess over hard signed-jump variation is \(2\min(A_+,A_-)\) | exact theorem | report (4.13); Jordan decomposition | one finite-order face | no claim that ordinary hard BV recovers the relaxed component ledger |
| The extra I-style radial damping has mass \(O(\varepsilon^{1/(2m)})\) and no finite-order face atom | exact theorem | report (4.9); rescaling \(\tau=\varepsilon^{1/(2m)}s\) | isolated finite-order zero, fixed \(\lambda\) | no estimate for a flat or accumulating zero set |
| The raw source and radial pieces have opposite logarithmic divergence, while only their joint form has a finite face-measure limit | exact theorem | report (4.14)--(4.18); exact producer `raw_split_cancellation` | one active finite-order half-face with the Taylor remainder needed to differentiate the jet | the two raw pieces are not separately uniformly bounded Radon-measure families and cannot be estimated separately before the limit |
| Adaptive quadrature reproduces the unit inner-profile mass and the finite radial-profile factor for zero orders \(m=1,\ldots,8\) | independent numerical corroboration | standalone SciPy quadrature in `inner_profiles` | declared tolerances and floating-point arithmetic | the exact \(\varepsilon^{1/(2m)}\) prefactor supplies the vanishing scale; this finite sample is not a proof for all orders |
| Adaptive quadrature reproduces the two divergent raw masses and their bounded joint increment | independent numerical corroboration | standalone `raw_split_cancellation` | declared \(\varepsilon\) values on one model half-face | finite samples do not establish the asymptotic theorem |
| Seven oscillatory paths reproduce face variation growing with zero count while ordinary quadratic budgets stay bounded | independent numerical corroboration | standalone `oscillatory_paths` | declared frequencies and diagonal soft scales | not an NSE trajectory and not a uniform theorem over paths |
| A standalone \(32^3\) FFT gives \(Y_0=1\), \(\|F_0\|_2^2=1/4\), \(\|G_0\|_2^2=1/2\), \(\|C_t(0)\|_2^2=1\), \(B_t(0)=1/2\), and right trace \(1/4\) | independent numerical corroboration | `nse_initial_face` in the independent checker | one declared trigonometric datum and radial multiplier | no time integration, interval sign certificate, or internal face count |
| The family \(C_N=N^{-1}\sin(Nt)e\), \(F_N=e\), \(Y_N=1\) has uniformly bounded ordinary \(W^{1,p}\)-in-time data and denominator mass tending to zero, but positive and negative face variations grow like \(N\) | abstract functional separation | exact formulas (6.1)--(6.11); symbolic producer | smooth Hilbert paths, fixed \(N\) then \(\varepsilon\downarrow0\), or a diagonal with \(N^2\varepsilon_N\to0\) | not generated by the coupled NSE observables \((F_j,C_Q,Y)\) |
| No universal functional inequality can pay relaxed face cost using only a right side bounded on the ordinary norms of (6.6)--(6.8) | abstract functional separation | previous family; report Theorem 6.1 | the specified abstract function-space budgets | does not rule out an NSE identity, zero-count term, inverse denominator, transversality, second derivative, directional BV, or the source itself |
| The smooth datum \(u_0=(0,\cos x_1,0)+(0,0,\cos x_2)\), with a multiplier vanishing at radius \(1\) and equal to one at radius \(\sqrt2\), has \(C(0)=0\) and right trace \(a(0+)=1/4\) | genuine NSE one-sided initial jet | exact Fourier convolution and local classical Taylor expansion; report (7.1)--(7.7) | one smooth one-sided initial entry face | no positive time step, internal face, large NSE face count, or failure of a summed bound |
| On a compact subinterval of a classical periodic strong interval, a fixed nontrivial analytic projection has finitely many isolated finite-order zeros | conditional implication | Temam Chapter 7, Theorem 7.1 and Remarks 7.1--7.2; analytic-function identity theorem | fixed projection not identically zero; compact interval strictly inside the strong interval | no uniform zero number, order, separation, or control up to a possible singular time |
| A proved bound on the weighted positive entries and positive joint source would feed the earlier one-sided BV reduction | conditional implication | R0.71I deterministic BV identity plus the atoms identified here | all endpoint conventions, shell--cell weights, and limiting passages retained | R0.71O does not prove the required bound |
| A bound that assumes a uniform zero count, transversality, inverse denominator, directional BV, or a continuation norm can control faces only conditionally | conditional implication | direct summation of the finite-order traces | the named extra hypothesis must be stated and verified separately | such an input is not supplied by Leray energy |
| Leray energy plus the R0.71L denominator-mass estimate pays the full fixed-partition face sum | open claim | no NSE estimate; abstract functional separation blocks the corresponding universal function-space implication | possible only through additional NSE-specific summed structure | not disproved as an equation-specific signed cancellation |
| A tight-frame identity cancels or pays \(\sum_{j,Q}\kappa_j^{-2}\sum_{t_0}A_{j,Q,+}(t_0)\) | open claim | none | fixed partition should be tested before refresh or moving cells | no all-cell/all-shell identity is presently available |
| Classical NSE admits an internal family with arbitrarily many unpaid denominator faces at bounded energy | open claim | none; the current NSE example has one initial entry only | would require a genuine coupled NSE construction | the abstract oscillatory family cannot be promoted to this claim |
| Flat zeros, accumulating zeros, or intervals on which \(C_Q=0\) admit the same finite-order atom formula | open claim | finite-order theorem does not apply | needs a component/stratification theorem or another compactness argument | smoothness alone is insufficient |
| Passage to infinitely many shells and cells and then to a putative singular endpoint | open claim | no uniform face summability or compactness theorem | finite truncations must first have a uniform measure bound | no Leray-level passage is justified |
| Refresh atoms and moving-cutoff contributions are controlled together with denominator faces | open claim | outside the fixed-cutoff release | requires separate jump and transport identities | R0.71O contains neither operation |
| Global regularity, finite-time singularity, or a new unconditional continuation criterion | open claim | none | Millennium problem | not reached by R0.71O |

## 2. Exact finite-order face ledger

Let

\[
 C(t_0+\tau)=c\tau^m+O(|\tau|^{m+1}),\qquad
 C_t(t_0+\tau)=mc\tau^{m-1}+O(|\tau|^m),\qquad
 b=\langle F(t_0),c\rangle,\qquad
 q=\|c\|^2.
 \tag{2.1}
\]

On the inner scale

\[
 \delta_\varepsilon=(\varepsilon/q)^{1/(2m)},
 \qquad s=|\tau|/\delta_\varepsilon,
 \tag{2.2}
\]

the soft profile is

\[
 a_\varepsilon(t_0+\tau)
 =A_\pm\frac{s^{2m}}{1+s^{2m}}+o(1),
 \tag{2.3}
\]

and

\[
 \int_0^\infty
 \frac{2ms^{2m-1}}{(1+s^{2m})^2}\,ds=1.
 \tag{2.4}
\]

Thus a right departure contributes positive mass \(A_+\), while a left
approach contributes negative mass \(A_-\).  The endpoint convention matters:
distributional BV on an open interval does not charge its observation
endpoints, whereas the R0.71I component ledger explicitly charges one-sided
entry and exit traces.

## 3. Raw split: cancellation must precede the measure limit

On an active branch, write

\[
 (a_\varepsilon)_t+2\lambda a_\varepsilon
 =\mathsf S_\varepsilon+\mathsf R_\varepsilon,
 \tag{3.1}
\]

where

\[
 \mathsf S_\varepsilon
 =\frac{2B(B_t+\lambda B)}{Y(d+\varepsilon)}
 -a_\varepsilon\frac{Y_t}{Y},
 \qquad
 \mathsf R_\varepsilon
 =-\frac{B^2d_t}{Y(d+\varepsilon)^2}.
 \tag{3.2}
\]

For \(X=q r^{2m}\) on one active half-face and
\(\gamma^2=b^2/(Y_0q)\), the singular primitives are

\[
 \gamma^2\log\left(1+\frac X\varepsilon\right),
 \qquad
 -\gamma^2\left[
 \log\left(1+\frac X\varepsilon\right)
 -\frac X{X+\varepsilon}\right].
 \tag{3.3}
\]

Each raw piece has total mass growing like \(\gamma^2\log(1/\varepsilon)\),
with opposite signs.  Their sum is exactly

\[
 \gamma^2\frac X{X+\varepsilon}
 \longrightarrow\gamma^2.
 \tag{3.4}
\]

Therefore neither raw row is a separately compact measure family.  A valid
soft-limit argument must retain the cancellation-preserving factorization

\[
 2z_\varepsilon^+\mathcal J_\varepsilon^N
 =2\sigma_\varepsilon z^+\mathcal J
 +(\sigma_\varepsilon)_ta,
 \tag{3.5}
\]

or the full derivative (3.1) before taking positive parts, total variations,
or termwise estimates.

## 4. Functional separation versus NSE evidence

The oscillatory family proves a statement about possible inequalities between
ordinary Hilbert-path norms and face variation.  It is an exact abstract
separation, not an NSE counterexample.

The trigonometric NSE datum proves something different: one genuine smooth
NSE initial trace can leave a zero filtered denominator with positive one-sided
value.  It supplies existence of one admissible face, not an unbounded face
count and not a failure of the weighted fixed-partition sum.

These evidence classes cannot be combined into the stronger claim that NSE
creates arbitrarily many unpaid internal faces.

## 5. Next finite gate

The open fixed-partition quantity is

\[
 \sum_{j,Q}\kappa_j^{-2}
 \sum_{t_0\in Z_{j,Q}}A_{j,Q,+}(t_0).
 \tag{5.1}
\]

The next finite test may seek:

1. an exact tight-frame cancellation in the all-cell/all-shell sum;
2. a coarea or analytic-zero estimate with all constants explicit;
3. a genuine NSE separation for the summed quantity.

A bound that assumes the zero count, transversality, inverse denominator,
directional BV, the target source, or a known continuation norm is conditional.
Refresh and moving cutoffs remain outside this fixed-partition gate.
