# R0.70H independent internal audit

> **Audit date:** 2026-08-24
>
> **Final status:** PASS after correction
>
> **Scope:** work-critical core-moment normalization, variable-ratio Abel
> indices, fixed-time scale variation, nested parabolic windows, filtered
> vorticity-moment identities, the R0.70F initial-face pressure test, bounded
> literature attribution, and certificate claim boundaries. This is an
> internal adversarial audit assembled from three independent audit lanes; it
> is not external peer review.

## 1. Audit disposition

The first draft contained four material algebraic or quantifier errors. A
separate PDE/certificate audit also required the polynomial regression to use
an actual velocity--vorticity pair and required the finite-regression boundary
to be stated explicitly. The corrected report and producer close all of these
points.

| audit area | original finding | correction | final status |
|---|---|---|---|
| variable-ratio transport | the convention $r_{k+1}=\rho_k r_k$ was combined with the shifted formula $\lambda_k=\rho_k^{n+2}$ | replaced it by $\lambda_k=(r_k/r_{k-1})^{n+2}=\rho_{k-1}^{n+2}$, so the Abel interior factor is $\lambda_{k+1}=\rho_k^{n+2}$ | PASS |
| spacetime work normalization | $c_k(t)$ was factored out of a time integral and the parabolic $r_k^{-2}$ factor was lost | retained the product inside the integral and introduced $\mathcal N_k=r_k^{-2}\mathbf1_{I_k}m_k$ | PASS |
| spacetime Abel increment and dual weight | the unweighted instantaneous increment was used as the coordinate for the R0.70F spacetime work | expanded the actual $\mathcal N$-increment, obtaining the overlap factor $\rho_k^n$ and the Cauchy--Schwarz weight $r_k^{-3}$ | PASS |
| scale-chain quantifier | the proof used $\sum r_k\lesssim r_0$ without declaring a one-sided chain | restricted the estimate to $0\le k\le N$, uniformly in $N$, or $k\in\mathbb N_0$ | PASS |
| filtered PDE regression | separate divergence-free polynomial fields would not by themselves certify a velocity--vorticity identity | the producer now uses $\Omega=\nabla\times U$, checks both divergences and the curl relation, and treats the calculation as a pointwise divergence identity | PASS |
| finite certificate scope | finite exact loops risked being read as proofs for arbitrary length or compact geometry | separated analytic proofs from finite regressions and listed every non-computer-proved step | PASS |
| R0.70F transfer | instantaneous pressure-test factors risked being confused with spacetime overlap factors | restricted $\rho^{n+2}$ recurrence to the instantaneous initial-face pairing and retained the no-common-top-time boundary | PASS |

The final PASS applies to the corrected `research/r070h_report-source.md`,
`research/r070h_core_moment_audit.py`, and the archived R0.70H certificate. It
does not upgrade the report to a journal theorem or external peer review.

## 2. Critical normalization audit

For

\[
 M_k^{(n)}
 =\int \chi_k(x)(x-x_0)^{\otimes n}\otimes
       \Omega_k(x)\otimes\Omega_k(x)\,dx,
 \qquad n=0,1,
\]

the length dimension is $n-1$. A degree-$n$ strain coefficient has
dimension $-(n+2)$. The corrected critical coordinates are therefore

\[
 c_k^{(n)}=r_k^{n+2}P_k^{(n)},
 \qquad
 m_k^{(n)}=r_k^{1-n}M_k^{(n)}.
\]

They satisfy the exact instantaneous identity

\[
 r_k^3P_k^{(n)}:M_k^{(n)}
 =c_k^{(n)}:m_k^{(n)}.
\]

In particular,

\[
 m_k^{(0)}=r_kM_k^{(0)},
 \qquad
 m_k^{(1)}=M_k^{(1)}.
\]

This work-critical normalization is distinct from the coordinates
$r_k^{-3/2}M_k^{(0)}$ and $r_k^{-5/2}M_k^{(1)}$, which are dual to a
different source coefficient square function. The audit found no permissible
way to substitute one normalization for the other without retaining the
corresponding scale weight.

## 3. Variable-ratio Abel audit

The scale convention is

\[
 r_{k+1}=\rho_k r_k.
\]

Consequently the exact source transport is

\[
 h_k^{(n)}
 =c_k^{(n)}-\lambda_k^{(n)}c_{k-1}^{(n)},
 \qquad
 \lambda_k^{(n)}
 =\left(\frac{r_k}{r_{k-1}}\right)^{n+2}
 =\rho_{k-1}^{n+2}.
\]

Finite componentwise summation by parts gives

\[
\begin{aligned}
 \sum_{k=a}^b h_k^{(n)}:m_k^{(n)}
 ={}&c_b^{(n)}:m_b^{(n)}
 -\lambda_a^{(n)}c_{a-1}^{(n)}:m_a^{(n)}\\
 &+\sum_{k=a}^{b-1}c_k^{(n)}:
 \left(m_k^{(n)}-\lambda_{k+1}^{(n)}m_{k+1}^{(n)}\right).
\end{aligned}
\]

Thus the instantaneous pairing-covariant increment is exactly

\[
 \mathfrak D_k^{\rm pair}m^{(n)}
 =m_k^{(n)}-\rho_k^{n+2}m_{k+1}^{(n)}.
\]

This differs from the geometric normalization increment

\[
 m_{k+1}^{(n)}-\rho_k^{1-n}m_k^{(n)}.
\]

For a constant-ratio chain, the instantaneous pairing factors are
$\rho^2$ and $\rho^3$ for degrees zero and one. The producer now contains
both generic variable-coefficient Abel regressions and nonconstant-radius
index-map checks; the constant-ratio tests alone would not have detected the
original shift.

## 4. Fixed-time estimate and one-sided-chain boundary

Let $D_k=\Omega_{k+1}-\Omega_k$. Under the explicit multiplier assumption

\[
 \sup_{\xi\ne0}\sum_k
 \left|\widehat\varphi(\ell_{k+1}\xi)
       -\widehat\varphi(\ell_k\xi)\right|^2<\infty,
\]

Plancherel gives

\[
 \sum_k\|D_k\|_2^2\lesssim\|\omega\|_2^2,
 \qquad
 \sup_k\|\Omega_k\|_2\lesssim\|\omega\|_2.
\]

The cutoff, normalization, and filter-field terms then obey the corrected
one-sided estimate

\[
 \sum_k|m_{k+1}^{(n)}-m_k^{(n)}|
 +\sum_k|m_k^{(n)}|
 \lesssim r_0\|\omega\|_2^2,
 \qquad n=0,1.
\]

The proof uses

\[
 \sum_{k\ge0}r_k\lesssim r_0,
 \qquad
 \sum_{k\ge0}r_k^2\lesssim r_0^2.
\]

It is therefore stated only for a finite chain $0\le k\le N$, uniformly in
$N$, or a one-sided fine-scale chain $k\in\mathbb N_0$. It is false as
written on an unrestricted two-sided scale chain. Time integration against
Leray dissipation gives an auxiliary common-time
$L_t^1(\ell_k^1)$ estimate for these unweighted instantaneous moments. It is
not a bound for the actual parabolic work coordinate below.

## 5. Spacetime work, nested windows, and the negative dual weight

For time-dependent coefficients, the exact work identity is

\[
 \boxed{
 r_k\int_{I_k}P_k^{(n)}(t):M_k^{(n)}(t)\,dt
 =r_k^{-2}\int_{I_k}c_k^{(n)}(t):m_k^{(n)}(t)\,dt.}
\]

The coefficient $c_k(t)$ cannot be extracted from the integral unless it is
constant on $I_k$. The parabolic moment average

\[
 \bar m_k^{(n)}=r_k^{-2}\int_{I_k}m_k^{(n)}(t)\,dt
\]

is a valid auxiliary coordinate, but the work is not generally
$c_k:\bar m_k$.

For $I_k=(t_0-r_k^2,t_0)$, define the actual spacetime coordinate

\[
 \mathcal N_k^{(n)}(t)
 =r_k^{-2}\mathbf1_{I_k}(t)m_k^{(n)}(t).
\]

The corrected Abel increment is

\[
\begin{aligned}
 \mathcal N_k^{(n)}-\lambda_{k+1}^{(n)}\mathcal N_{k+1}^{(n)}
 ={}&r_k^{-2}\mathbf1_{I_{k+1}}
 \left(m_k^{(n)}-\rho_k^n m_{k+1}^{(n)}\right)\\
 &+r_k^{-2}\mathbf1_{I_k\setminus I_{k+1}}m_k^{(n)}.
\end{aligned}
\]

The fine-window factors are therefore $1$ for degree zero and $\rho_k$
for degree one. They are not the instantaneous factors $\rho_k^2$ and
$\rho_k^3$.

If the source estimate is measured in
$L_t^2\ell_k^2(r_k^{-1})$, direct Cauchy--Schwarz requires

\[
 \int\sum_k r_k
 \left|\mathcal N_k-\lambda_{k+1}\mathcal N_{k+1}\right|^2dt.
\]

Because the fine window and discarded slab are disjoint, this equals

\[
\begin{aligned}
 \int\sum_k r_k^{-3}\bigg[
 &\mathbf1_{I_{k+1}}
 |m_k^{(n)}-\rho_k^n m_{k+1}^{(n)}|^2\\
 &+\mathbf1_{I_k\setminus I_{k+1}}|m_k^{(n)}|^2
 \bigg]dt.
\end{aligned}
\]

The producer checks the elementary weight identity

\[
 r_k(r_k^{-2})^2=r_k^{-3}.
\]

No estimate for this negative-weight expression is proved. The fixed-time
variation estimate omits $r_k^{-2}$ and cannot be promoted to this bound by
changing only a time exponent.

## 6. Filtered vorticity and pointwise-divergence audit

With

\[
 C_{ai}=\tau_{ai}^{\omega u}-\tau_{ai}^{u\omega},
\]

the filtered vorticity equation has the sign

\[
 \partial_t\Omega_i+U_a\partial_a\Omega_i
 =\Omega_a\partial_aU_i+\nu\Delta\Omega_i
 +\partial_aC_{ai}.
\]

After integration by parts, the trace commutator term is therefore

\[
 -\int C_{ai}\,\partial_a(\phi\Omega_i),
\]

and the resolved stretching term is

\[
 \int\phi\,S(U):\Omega\otimes\Omega.
\]

The signs in the corrected report agree with these identities. The producer
uses a polynomial pair satisfying

\[
 \nabla\cdot U=0,
 \qquad
 \Omega=\nabla\times U,
 \qquad
 \nabla\cdot\Omega=0.
\]

Its weights are noncompact polynomials. Accordingly, the computer check is a
pointwise divergence-law regression, not a boundary-free integrated theorem.
The smooth filtered identities in the report still require the usual
mollification and limiting argument before any minimal Leray formulation;
the report does not claim that extension as a new result.

## 7. R0.70F pressure-test boundary

For the compact interlaced family at the initial face and fixed center
$x_0=0$,

\[
 b_n=\frac{1-\Lambda^{-4n}}{1-\Lambda^{-4}},
\]

and the work-critical moments are

\[
 m_n^{(0)}=C_0b_n^2e_1^{\otimes2},
 \qquad
 m_n^{(1)}=C_1b_n^2e_1^{\otimes3}.
\]

Their ordinary variation is uniformly bounded. For the instantaneous
normalized pairing $r_n^3P_n:M_n=c_n:m_n$, the factors are

\[
 \lambda_0=\rho^2=\Lambda^{-4},
 \qquad
 \lambda_1=\rho^3=\Lambda^{-6},
\]

and the pairing-covariant $\ell^1$ and square masses grow linearly in the
number of active scales. These are the instantaneous initial-face factors,
not the spacetime overlap factors in Section 5 of this audit.

The family has uniform velocity energy but no uniform initial-face vorticity
$L^2$ bound. It therefore does not contradict the dissipation-integrated
fixed-time estimate. It also does not produce recurrence on backward
cylinders with one common positive terminal time.

## 8. Fixed-source/filter and two-index boundaries

The source estimate transferred from R0.70G is valid for one fixed
source/filter family. If the source filter changes with the core index, the
same weighted estimate cannot simply be inserted into the Abel pairing.

R0.70H studies a single reindexed source--core scale chain. It does not
identify that chain with Yu's complete two-index moving-shell positive
packing, and taking a positive part does not preserve the signed Abel
identity. The surviving alternatives are a genuinely weighted parabolic
source--core embedding, a direct trilinear estimate, or an additional
sign/Carleson mechanism. None is proved here.

## 9. Certificate and finite-regression boundary

The archived producer was reproduced with

```sh
PYTHONDONTWRITEBYTECODE=1 \
  tmp/r068b-venv/bin/python research/r070h_core_moment_audit.py
```

All recorded Boolean checks returned `true`. The exact regressions cover:

- instantaneous and spacetime dimensional normalization;
- constant- and variable-coefficient finite Abel identities;
- ten nonconstant-radius index-map cases;
- scalar-contraction scale and nested-window ledgers;
- the $\rho_k^n$ spacetime overlap factors and $r_k^{-3}$ dual weight;
- one polynomial pointwise filtered-enstrophy divergence identity with
  $\Omega=\nabla\times U$;
- 66 finite R0.70F recurrence cases with
  $\Lambda\in\{2,4,8\}$ and $2\le N\le12$;
- representative component scale-weight geometric sums.

Finite regressions are not proofs for arbitrary sequence length. The general
Abel identities, lower bounds, and geometric-series estimates are proved
analytically in the report. The producer does not computer-prove the filter
multiplier hypothesis, the compact support geometry inherited from R0.70F,
full-field cross terms, the primary-source search, a Leray-class local
enstrophy Carleson estimate, nonlinear persistence, or a common-positive-time
construction.

## 10. Bounded literature-audit boundary

The literature lane audited eight nearby primary-source frameworks:

1. Caffarelli--Kohn--Nirenberg on suitable weak solutions and localized
   velocity energy;
2. Duchon--Robert on local energy balance and cubic defect;
3. Dascaliuc--Grujić (2011) on conditional physical-scale energy flux;
4. Dascaliuc--Grujić (2013) on conditional enstrophy-flux locality;
5. Fefferman--Stein on BMO--Carleson characterization;
6. Koch--Tataru on small-data $BMO^{-1}$ and the solution space $X$;
7. Jones--Seeger--Wright on linear jump and strong variation estimates;
8. Do--Muscalu--Thiele on bilinear Littlewood--Paley paraproduct variation.

No audited result supplies all of the fixed-center, changing-cutoff,
quadratic-moment, nested-time-window, negative-weight, and positive-work
features required here. This is a bounded eight-source search result. It is
not a proof that no relevant theorem exists elsewhere, and it must not be
quoted as a literature nonexistence theorem.

## 11. Final claim boundary

The corrected R0.70H report establishes exact normalization and Abel
identities, plus an explicitly conditional one-sided fixed-time variation
estimate. It identifies the actual spacetime dual quantity and shows why the
unweighted estimate does not control it.

It does not prove the $r_k^{-3}$-weighted parabolic estimate, a complete
source--core trilinear embedding, positive moving-shell packing, a
common-positive-terminal-time recurrence or exclusion, singularity
formation, large-data regularity, or a solution of the Millennium problem.
It also makes no claim that a missing theorem does not exist.
