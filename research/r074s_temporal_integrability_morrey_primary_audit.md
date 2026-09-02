# R0.74S Step 13 — primary analytic audit

## 0. Verdict

The note
`research/r074s_temporal_integrability_morrey_threshold.md` is audited
against the frozen R0.74P/R/S definitions and ledgers.

**Verdict: PASS, subject to the exact scope recorded below.**

The audit supports three new proved statements:

1. a fixed-solution, fixed-scale
   \(\ell^1(L_t^{4/3})\) bound for the physical shell-flux rates and the
   resulting \(\delta^{1/4}\) terminal-window modulus;
2. the exact temporal optimization ceiling and its smooth abstract
   saturation models; and
3. the payment-dependent moving-Morrey implication and the critical
   eight-ary tree obstruction.

It does not support a uniform \(P_R^M\)-bound for the temporal coefficient,
the geometric hypothesis (S.328), a PDE realization of either abstract
countermodel, S.280, S.288, S.303, Q.12, Q.1, or regularity.

## 1. Frozen source bindings

| Input | Role checked |
|---|---|
| `research/r074p_temporal_observable_triage.md` | Canonical physical-flux primitive, pressure-gauge cancellation, absolute \(L_t^1\) ledger, and AC representatives. |
| `research/r074r_arbitrary_clock_extraction_gate.md` | Shell-dependent cubic payment and the persistence/ancestor boundary. |
| `research/r074s_shared_budget_terminal_trace_obstruction.md` | Step 11 residual split, linear selected-excess ledger, pure high-Rayleigh scalar row (S.267), and the fixed-\(N\) target. |
| `research/r074s_terminal_window_morrey_packing.md` | Common-window reduction (S.273)--(S.280), moving-tube cover (S.289)--(S.294), and inherited heat-shear screen. |

Only consequences explicitly rederived in the Step 13 note are treated as
new.  The upstream PDE identities and estimates remain inherited results.

## 2. Dimensionless window and norm order

| Item | Audit | Verdict |
|---|---|---|
| (S.307) | Under \(t=s_R+R^2\sigma\), \(dt=R^2d\sigma\), so \(h_k=R^2|\dot F_k|\) preserves the window integral. | PASS |
| (S.308) | Truncating \((\vartheta-\delta,\vartheta)\) by \((0,4)\) is exactly the clipped terminal window in (S.273). | PASS |
| (S.309) | The shell set is chosen outside the sum of time norms.  It is therefore common to every time in the window. | PASS |
| Norm order | The proof uses \(\inf_S\sum_{k\notin S}\|h_k\|_p\), not \(\|\mathcal S_N(h(t))\|_p\).  The latter would permit a time-dependent exceptional set and is not substituted. | PASS |

## 3. Energy-class temporal estimate

### 3.1 Velocity and pressure

The periodic energy class gives

\[
 v_R\in L_t^\infty L_x^2\cap L_t^2H_x^1.
\]

Spatial interpolation followed by temporal Hölder gives
\(v_R\in L_t^4L_x^3\).  With the mean-zero periodic pressure gauge,

\[
 \|\pi_R-\overline\pi_R\|_{3/2}
 \le C\|v_R\otimes v_R\|_{3/2}
 \le C\|v_R\|_3^2,
\]

so the pressure-velocity product has the same temporal \(L^{4/3}\) class
as \(\|v_R\|_3^3\).  Both exponents lie strictly inside the strong
Calderón--Zygmund range.  No \(L^1\) or \(L^\infty\) Riesz-transform
endpoint is used.

### 3.2 Drift and cutoff sum

For fixed \(R\), convolution gives

\[
 |a_R(t)|\le CR^{-3/2}\|v_R(t)\|_2.
\]

The inherited derivative bound and
\(\sum_k2^{3k}\gamma_k<\infty\) give

\[
 \sum_k\gamma_k|\nabla\Psi_k^R|\le CR^{-1}
\]

on the frozen range \(R<\pi/16\).  Thus the drift rate is in
\(L_t^\infty\), with a coefficient depending on the global kinetic energy
at that scale.

### 3.3 Scale cancellation

Let \(E_I=Re_R\), \(D_I=Rd_R\), and
\(|\mathcal T_R|=4R^2\).  The periodic interpolation estimate gives

\[
 \int_{\mathcal T_R}\|v_R(t)\|_3^4dt
 \le CE_I(D_I+E_I).
\]

The physical-flux derivative contributes \(R^{-2}\).  Consequently,

\[
 \left\|\sum_k|\dot F_{k,R}^{\rm cub}|
       +\sum_k|\dot F_{k,R}^{\rm pr}|\right\|_{4/3}
 \le CR^{-1/2}[e_R(e_R+d_R)]^{3/4},
\]

while
\[
 \left\|\sum_k|\dot F_{k,R}^{\rm dr}|\right\|_\infty
 \le CR^{-2}e_R^{3/2}.
\]
The window factors are

\[
 (\delta R^2)^{1/4}R^{-1/2}=\delta^{1/4},
 \qquad
 (\delta R^2)R^{-2}=\delta.
\]

This verifies (S.310)--(S.313).  The use of global torus energies
\(e_R,d_R\), rather than the local payment \(P_R^M\), is explicit and is
why the estimate is nonuniform for the intended gate.

### 3.4 Endpoint wording

For energy-admissible pairs
\(2/q+3/r=3/2\), three spatial factors satisfying
\(\sum_i1/r_i=1\) obey \(\sum_i1/q_i=3/4\).  Hence the direct triple-product
argument has time exponent \(4/3\).  The note correctly calls this the
endpoint of the direct energy-interpolation argument, not the strongest
integrability that any additional PDE hypothesis could ever yield.

## 4. General \(p\) optimization

For \(a_p=1-1/p\), Hölder gives the exact common-set inequality

\[
 \mathcal V^F_{N,R}\le\delta^{a_p}\mathfrak H^F_{p,N,R}.
\]

Under the explicitly conditional comparison
\(\mathfrak H^F_{p,N,R}\le C_HP^\beta\), balancing with
\(C_{\rm deep}\delta^{-2/3}P^{2/3}\) gives

\[
 \delta\asymp P^{-(\beta-2/3)/(a_p+2/3)},
 \qquad
 E_{p,\beta}={2\over3}{a_p+\beta\over a_p+2/3}.
\]

The difference

\[
 E_{p,\beta}-{2\over3}
 ={2\over3}{\beta-2/3\over a_p+2/3}
\]

has the asserted sign.  In the linear case,

\[
 \delta_p\asymp P^{-p/(5p-3)},
 \qquad
 E_p={2(2p-1)\over5p-3}.
\]

The values \(E_1=1\), \(E_{4/3}=10/11\), and
\(E_\infty=4/5\) are correct.  The \(p=1\) case is handled separately
because it has no positive window power.  The capped-window alternative in
(S.322) correctly adds an \(A_R\) term.

**Boundary:** minimizing this particular upper bound proves a ceiling for
the stated two-term method.  It does not prove that Navier--Stokes solutions
must saturate the bound.  The note preserves that distinction.

## 5. Temporal witnesses

For \(M=N+1\), the fixed-profile family (S.323) has one common smooth bump
in all \(M\) coordinates.  Its \(\ell^1(L^p)\) norm is
\(H\|\phi\|_p\), and deleting \(N\) equal coordinates leaves exactly
\(H/M\).  With payment proportional to \(H\), the normalized tail grows
like \(H^{1/3}\).

For the adaptive \(p=4/3\) family, take \(P\ge1\), a nonnegative
\(\rho\in C_c^\infty((-1,0))\), and
\(d=P^{-4/11}\).  With \(c_\rho=\int\rho>0\), the scaling gives

\[
 \sum_k\|h_k\|_{4/3}=P,
 \qquad
 \sum_k\|h_k\|_1=c_\rho P^{10/11},
 \qquad
 P^{2/3}d^{-2/3}=P^{10/11}.
\]

The remaining best-\(N\) mass is
\(c_\rho P^{10/11}/(N+1)\).  Assigning every coordinate the abstract
depth \(d\) and residual equal to its full \(L^1\) mass also checks the
combined ledger for every window: \(\delta\ge d\) captures the full bump,
while \(0<\delta<d\) gives
\(P^{2/3}\delta^{-2/3}\ge P^{2/3}d^{-2/3}=P^{10/11}\).
Both constructions are smooth rate vectors with AC primitives.  Neither is
labeled as an NSE solution.

## 6. Moving-Morrey envelope

The Step 12 moving-tube cover is pointwise in \((u,R,\tau)\); uniformity of
\(M\) and \(L\) was needed only to make its final constant uniform.
Replacing them by \(M_R(\tau),L_R(\tau)\) therefore gives (S.326)--(S.327).

The two payment regimes in Proposition 5.1 are exact:

- for \(P\le1\), the inherited linear cap gives \(P\le P^{2/3}\);
- for \(P\ge1\), (S.328) gives
  \(B_R\le C(1+P^{2/3})\le2CP^{2/3}\).

Thus (S.328) is a weaker sufficient interface than separate solution-
independent bounds on \(M_R\) and \(L_R\).  It is not proved for the bare
suitable-weak class.

For \(\theta>2/3\), the equal-coordinate sequence in (S.331), with
\(x=b\), satisfies both scalar caps but leaves a normalized fixed-\(N\)
tail growing as \(P^{\min\{1,\theta\}-2/3}\).  This proves sharpness only
for the two-scalar-cap inference.

## 7. Exact heat shear

The field in (S.332) is divergence free, has zero nonlinear term, and solves
the heat equation.  Translation along the \(e_1\) path leaves the moving
field independent of \(y_1\).  Periodic integration of
\(\partial_{y_1}\Psi_k^R\) therefore proves (S.333).

On the \(2\pi\)-torus,

\[
 \int_{\mathbb T^3}\cos^2(nx_2)dx=4\pi^3,
 \qquad
 \int_{\mathbb T^3}|\sin(nx_2)|^3dx={32\pi^2\over3}.
\]

Time integration gives exactly (S.334).  The family has high
dissipation-to-cubic ratio but zero physical-flux primitive.  The note does
not infer that arbitrary dynamic high-frequency fields have zero flux.

## 8. Critical tree and incidence charging

At every depth \(d\), the eight-ary tree has \(8^d\) nodes.  Thus each
level in (S.335) carries \(m^{-3}\) payment, \(m^{-2}\) ancestor mass, and
\(5/(3m^2)\) scalar-row scale.  There are \(L=m^3\) levels, proving
(S.337).

The subtree square series is

\[
 b_v^2\sum_{j\ge0}8^j64^{-j}={8\over7}b_v^2.
\]

The coefficient cube is critical because
\(8(1/2)^3=1\).  Since every coordinate is at most \(m^{-2}\), deletion of
\(N\) coordinates removes at most \(N/m^2\), proving (S.339).  The strict
Step 11 branch inequalities in (S.336) are numerically correct, and
\((3/5)s_v=b_v\).

For the conditional incidence theorem, Hölder with exponents \(3\) and
\(3/2\) gives

\[
 \sum_{\rm incidences}c_\nu p_\nu^{2/3}
 \le\left(\sum c_\nu^3\right)^{1/3}
     \left(\sum p_\nu\right)^{2/3}.
\]

This proves (S.340).  The dual identity (S.341) follows by equality at
\(p_\nu\propto c_\nu^3\).  To derive its incidence coefficient bound from
a tree, the note now requires all three missing uniformities: bounded total
root cube mass, bounded node-to-incidence multiplicity, and a Dini product
sum uniformly bounded over every starting depth.  These imply

\[
 \sum_{\rm incidences}c_\nu^3
 \le M_{\rm inc}C_{\rm root}C_D.
\]

The tree model has critical equality \(\theta_d=1\); its finite-depth Dini
constant grows like \(L=m^3\), so it cannot provide a uniform coefficient
bound.

**Boundary:** the tree nodes are not claimed to be the physical annular
coordinates of one solution.  The construction refutes only an inference
from the listed abstract ledgers and qualitative tree properties.

## 9. Literature and claim-boundary audit

The cited primary sources support the stated neighboring results:

- Lei--Ren quantifies a dissipation-energy pigeonhole and proves improved
  partial regularity, with natural local-energy dependence;
- Choe--Yang obtains reverse Hölder improvement under a uniformly bounded
  scaled local kinetic energy;
- Guevara--Phuc proves pressure-sensitive local-energy and epsilon-
  regularity criteria from scale-integrated hypotheses; and
- Koch--Tataru works in a critical small-data Carleson-type solution class.

None of those source descriptions is used as proof of (S.280), (S.288), or
(S.328).  The collision search is bounded and is not presented as a novelty
or priority search.

The main note contains explicit **PROVED**, **ABSTRACT BOUNDARY TESTS**,
**OPEN**, and **NOT CLAY** ledgers.  It does not use numerical simulation,
floating-point evidence, or DGX output.

## 10. Release recommendation

Release is recommended after all of the following mechanical gates pass:

1. sequential unique equation tags S.307--S.342;
2. exact rational checks for every exponent, branch threshold, tree sum,
   and two-regime implication;
3. a negative-mutation suite for the common deletion order, the
   \(4/3\) endpoint, the \(2/3\) Morrey threshold, the abstract/PDE
   boundary, and strict cubic subcriticality;
4. an independent verifier with locked hashes for the main note, primary
   certificate, this audit, and all upstream dependencies; and
5. the ordinary bilingual/PDF/GitHub Pages publication gates in the separate
   publication task.

Until all five items succeed, the result is research-frozen rather than a
completed public release.
