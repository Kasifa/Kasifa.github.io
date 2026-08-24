# R0.70A pilot — non-explicit robustness around scale ratio four

## 1. Status and claim boundary

This pilot starts from the current repository state, not from the earlier pause
record.  Before the new R0.70A files were added, the worktree was clean at

```text
155b21437337d69f42938699f0afcdd9e820f56c
```

and the published R0.69W certificate remained source-locked to producer commit

```text
2b3141a333d3dea0c4b7a241c11f9adbca31d1b4.
```

R0.69W proves the strict sign obstruction at the single scale ratio
\(\rho=4\), where \(\varepsilon=1/\rho=1/4\).  This note proves two new
*existence* statements:

1. the same two-annulus obstruction holds on some open interval
   \((4-\eta,4+\eta)\), uniformly in the amplitude;
2. for initial data in a closed subinterval of that ratio interval, the
   obstruction persists for a common short time along the corresponding smooth
   Navier--Stokes solutions.

Neither \(\eta\) nor the common time is made explicit here.  A separate coarse
single-worker calculation diagnoses what an explicit ratio certificate would
require.  It does not certify numerical endpoints for the open interval.

## 2. The fixed-ratio family and the two-annulus observable

Let

\[
 U_\varepsilon(x)=\varepsilon U_1(x/\varepsilon),
 \qquad
 u_{a,\rho}=aU_1+(1-a)U_{1/\rho},
 \qquad 0\leq a\leq1,
 \tag{2.1}
\]

with the exact R0.69W cutoff and physical annular functionals
\(\mathcal A_j\).  Define

\[
 G(a,\rho)
 =\min\{\mathcal A_0(u_{a,\rho}),
          \mathcal A_{-2}(u_{a,\rho})\}.
 \tag{2.2}
\]

The minimum is essential.  At \(a=0\), the exact amplitude factor makes
\(\mathcal A_0=0\); continuity of \(\mathcal A_0\) alone therefore cannot
produce a uniform negative margin on the closed amplitude interval.  R0.69W
uses \(j=-2\) precisely at that endpoint.

## 3. An explicit uniform margin at \(\rho=4\)

At ratio four the exact analytic amplitude law established in the R0.69V/W
derivation is

\[
 \mathcal A_0(u_{a,4})
 =a(c_1+c_2a+c_3a^2).
 \tag{3.1}
\]

Use the certified upper endpoints

\[
\begin{aligned}
 c_1^U&=-0.0008440552534174868,\\
 c_2^U&= \phantom{-}0.004933596141229829,\\
 c_3^U&=-0.12489333880250154.
\end{aligned}
\tag{3.2}
\]

Put \(a_*=1/64\) and

\[
 f(a)=a(c_1^U+c_2^Ua+c_3^Ua^2).
 \tag{3.3}
\]

The turning point of \(f'\) is

\[
 -\frac{c_2^U}{3c_3^U}
 =0.013167492060382572\ldots<a_*,
 \tag{3.4}
\]

and direct outward-endpoint arithmetic gives

\[
 f'(a_*)=-0.000781354987384793076\ldots<0.
 \tag{3.5}
\]

Consequently \(f\) is decreasing on \([a_*,1]\), and

\[
 \mathcal A_0(u_{a,4})
 \leq f(a)\leq f(a_*)
 =-0.0000124603023672554718658\ldots.
 \tag{3.6}
\]

Treating the displayed decimal coefficient endpoints as exact rationals gives

\[
 -f(a_*)
 =\frac{4082991879702273021}
        {327680000000000000000000}
 >\delta_*,
 \qquad
 \delta_*:=\frac{1246030236725547}{10^{20}}
 =1.246030236725547\times10^{-5}.
 \tag{3.7}
\]

For the second annulus, let \(d_k^U\) be the four certified upper
coefficient endpoints:

\[
 (d_0^U,d_1^U,d_2^U,d_3^U)
 =(-0.0019148502803584854,
 0.04610227421275272,
 0.08451552157038326,
 0.8605177243885085).
 \tag{3.8}
\]

The upper polynomial \(g(a)=\sum_{k=0}^3d_k^Ua^k\) is increasing for
\(a\geq0\), and

\[
 g(a_*)
 =-0.00117058595891558310866\ldots<0.
 \tag{3.9}
\]

Thus \([0,a_*]\) is controlled by \(\mathcal A_{-2}\), while
\([a_*,1]\) is controlled by \(\mathcal A_0\).  In particular,

\[
 \boxed{
 \max_{0\leq a\leq1}G(a,4)
 \leq-\delta_*,
 \qquad
 \delta_*=1.246030236725547\times10^{-5}.}
 \tag{3.10}
\]

This fixed-ratio uniform margin combines the exact factor in (3.1), which
removes the constant term analytically, with archived outward endpoints for
the remaining coefficients.  The raw JSON enclosure for the numerically
integrated constant coefficient is not used as an exact zero.  The result is
stronger than the pointwise statement
\(G(a,4)<0\), and it does not use the coarse R0.70A calculation below.

## 4. Continuity of the annular coefficients in \(\rho\)

The vorticity of the inner profile satisfies

\[
 \omega_\rho(x)=\omega_1(\rho x),
 \qquad
 \partial_\rho\omega_\rho(x)
 =x\cdot\nabla\omega_1(\rho x).
 \tag{4.1}
\]

Hence \(\rho\mapsto U_{1/\rho}\) is smooth into \(H^m(\mathbb R^3)\)
for every fixed integer \(m\), on every compact ratio interval contained in
\((0,\infty)\).  The amplitude dependence is affine.

For fixed \(j\), write the two-increment identity schematically as

\[
 \mathcal A_j(\omega)
 =\iint K_j(z)
 (\widehat z\cdot\delta_z\omega(x))
 (\widehat z\cdot(\omega(x)\times\delta_z\omega(x)))
 \,dx\,dz,
 \tag{4.2}
\]

where \(K_j\) is supported on a fixed compact annulus away from zero and lies
in \(L^1_z\).  In particular,

\[
 |\mathcal A_j(\omega)|
 \leq C_j\|\omega\|_\infty\|\omega\|_2^2,
 \tag{4.3}
\]

and expanding the difference of two cubic expressions gives continuity on
bounded subsets of \(H^3\) for the vorticity, hence on \(H^4\) for the
velocity.  It follows that every amplitude coefficient and
\(G(a,\rho)\) are jointly continuous in \((a,\rho)\).

The same argument also shows that the coefficients are differentiable in
\(\rho\): differentiate the trilinear form once and replace, in turn, each
inner-profile slot by (4.1).  This proves existence of a finite local
Lipschitz constant, but does not give its numerical value.

## 5. Non-explicit open-interval theorem

Choose any compact preliminary ratio interval containing four, for example
\([3,5]\).  Joint continuity makes \(G\) uniformly continuous on
\([0,1]\times[3,5]\).  Combining this with (3.10), there exists
\(\eta>0\) such that

\[
 |\rho-4|<\eta
 \quad\Longrightarrow\quad
 |G(a,\rho)-G(a,4)|<\frac{\delta_*}{2}
 \quad\hbox{for every }a\in[0,1].
 \tag{5.1}
\]

Therefore

\[
 \boxed{
 G(a,\rho)\leq-\frac{\delta_*}{2}<0
 \quad
 (0\leq a\leq1,\ |\rho-4|<\eta).}
 \tag{5.2}
\]

This is a rigorous robustness theorem on an open scale-ratio interval.  It is
non-explicit: the proof supplies neither a decimal lower bound for \(\eta\)
nor certified endpoints such as \(3.9<\rho<4.1\).  Compactness must not be
reported as an explicit interval computation.

## 6. Uniform short-time persistence along true solutions

Fix \(\nu>0\) and consider Navier--Stokes on \(\mathbb R^3\).  Let
\(J\Subset(4-\eta,4+\eta)\) be a closed ratio interval.  The initial-data map

\[
 (a,\rho)\longmapsto u_{a,\rho}
 \tag{6.1}
\]

has compact image in \(H^4\), and in particular has a uniform \(H^4\) bound.
Standard local well-posedness for the three-dimensional Navier--Stokes
equation therefore gives a common time \(T>0\), solutions in
\(C([0,T];H^4)\cap L^2(0,T;H^5)\), and a solution map continuous from this
compact initial-data family into \(C([0,T];H^4)\).  By (4.2)--(4.3),

\[
 (t,a,\rho)\longmapsto
 \min\{\mathcal A_0(u^{a,\rho}(t)),
       \mathcal A_{-2}(u^{a,\rho}(t))\}
 \tag{6.2}
\]

is continuous.  Uniform continuity and (5.2) then yield a common
\(0<\tau\leq T\) for which

\[
 \min\{\mathcal A_0(u^{a,\rho}(t)),
       \mathcal A_{-2}(u^{a,\rho}(t))\}<0
 \quad
 (0\leq t\leq\tau,\ a\in[0,1],\ \rho\in J).
 \tag{6.3}
\]

The evolved solution is not asserted to remain in the two-scale ansatz.  This
is only short-time stability of a strict initial sign obstruction.  It is not
a dynamically generated depletion estimate, does not control a critical norm,
and does not advance global regularity by itself.

## 7. Low-cost fixed-ratio pilot

The independent script
`research/r070a_scale_ratio_robustness.py` reuses the R0.69W integrator in
memory, sets \(\varepsilon=1/\rho\) to a positive rational value, and rebuilds
the radial cells.  It never overwrites the R0.69W certificate.  The resulting
diagnostic JSON is archived at
`research/certificates/r070a-pilot/result.json` together with its claim boundary
and SHA-256 digest.

The unmodified program output is retained as `raw-result.json`.  The exact byte
state of the script used for that original run and the exact one-off
post-processing command were not retained.  The current script is a
rerun-compatible companion, and an automated fieldwise comparison proves that
post-processing left every rigorous interval unchanged; nevertheless this
pilot is not an end-to-end replayable producer archive.

The first pilot used one local worker, raw-moment P14, 64 cutoff cells,
distance-moment P14, four core cells, eight plateau cells, eight cells in each
transition, and 128-bit Arb endpoints.  Each ratio had 28 radial cells.  Five
ratios required approximately 334.5 seconds in total on the local machine.

The following are **midpoints of extremely wide fixed-ratio intervals**, not
certified coefficient values:

| \(\rho\) | \(c_1\) midpoint | \(c_2\) midpoint | \(c_3\) midpoint | discriminant from coefficient midpoints | endpoint midpoint |
| ---: | ---: | ---: | ---: | ---: | ---: |
| 3.8 | -0.0024559525 | 0.0053672703 | -0.1297958331 | -0.0012462820 | -0.0016736917 |
| 3.9 | -0.0022400637 | 0.0048656210 | -0.1295073170 | -0.0011367443 | -0.0018764455 |
| 4.0 | -0.0020494171 | 0.0044249027 | -0.1292544223 | -0.0010400051 | -0.0019827541 |
| 4.1 | -0.0018803927 | 0.0040363866 | -0.1290321079 | -0.0009542317 | -0.0020189244 |
| 4.2 | -0.0017299773 | 0.0036927331 | -0.1288362142 | -0.0008778986 | -0.0020030707 |

The midpoint secants are smooth.  Across the four consecutive subintervals of
length \(0.1\), the largest observed absolute slopes per unit \(\rho\) were
approximately

\[
 (0.00216,\ 0.00502,\ 0.00289,\ 0.00110,\ 0.00203)
 \tag{7.1}
\]

for \((c_1,c_2,c_3,\Delta,\mathcal A_{-2}(u_0))\), respectively.  These are
not derivative bounds.

More importantly, the coarse interval widths at \(\rho=4\) were approximately

\[
 1.90\times10^4,\quad4.07\times10^4,\quad3.64\times10^4,
 \quad2.22\times10^9,\quad2.30\times10^2.
 \tag{7.2}
\]

Thus none of the coarse fixed-ratio sign decisions passed.  This is useful
failure evidence: merely evaluating several fixed ratios with a very coarse
Taylor grid cannot produce an explicit robustness certificate.  The smooth
midpoint trend makes

\[
 \boxed{3.9<\rho<4.1}
 \tag{7.3}
\]

a conservative interval **candidate for the next certification attempt**, not
a theorem.

## 8. The next explicit certification gate

No DGX run is justified yet.  An explicit interval should first be attacked by
one of two equivalent local calculations:

1. certify bounds for \(\partial_\rho c_1\),
   \(\partial_\rho c_2\), \(\partial_\rho c_3\), and the four
   \(j=-2\) coefficient derivatives on \(3.9\leq\rho\leq4.1\); or
2. propagate \(\rho\) itself as an interval after transforming the inner
   transition to the fixed coordinate \(R=\rho r\), and directly enclose the
   two rectangles
   \([0,1/64]\times[3.9,4.1]\) and
   \([1/64,1]\times[3.9,4.1]\).

The first method has a transparent acceptance threshold.  If certified
Lipschitz bounds are \(L_k\), widen every fixed-ratio coefficient by
\(0.1L_k\), then repeat the two monotonicity checks (3.5) and (3.9).  The
calculation passes only if the \(\mathcal A_0\) upper envelope remains
decreasing and below zero on \([1/64,1]\), while the \(\mathcal A_{-2}\)
upper envelope remains below zero on \([0,1/64]\).

The existing pilot should not be refined by brute force until this
ratio-derivative formulation passes a small-grid width decomposition.  Only if
the derivative or bivariate intervals are already sign-compatible but their
remainder widths are too large should the calculation be split across the DGX.

## 9. Decision

R0.70A already has a rigorous qualitative conclusion: R0.69W is stable on an
unspecified open ratio interval and for a uniform short time along the
associated smooth solutions.  The archived coefficient endpoints also give
the explicit fixed-ratio amplitude margin (3.10).

What remains open is quantitative, not topological: certify a decimal ratio
interval.  The local coarse run failed at that task by many orders of
magnitude, so the next step is an analytic \(\rho\)-derivative or bivariate
interval implementation, not a high-resolution fixed-ratio sweep.
