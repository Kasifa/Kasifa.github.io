# R0.74R — independent audit of the terminal-window lobe theorem

Date: 2026-09-02

## 1. Frozen inputs

This audit is bound to the following exact bytes:

- analytic note, `research/r074r_persistent_lobe_cubic_packing.md`:
  `e7f151048e85d95133f8c6414849c0fe9dc40cc48b7a12666b7e21496ddb99b5`;
- problem freeze, `research/r074r_problem_freeze.md`:
  `cf20265b02f163da7c866f41e1109d19f5d0a1bbb45a8a53adfcb799816360cd`;
- certificate generator, `scripts/r074r_persistent_lobe_certificate.py`:
  `bfb0078ea71eb6eefc8a02c97a4cc9d1234ab1475a80a19c49c566eefb0ef645`;
- certificate JSON, `research/r074r_persistent_lobe_certificate.json`:
  `504a54a7061346c689401205099cf2c7c3178fabb936cb3449826b3c122b31af`;
- certificate report, `research/r074r_persistent_lobe_certificate_report.md`:
  `f41274b2d2eca0db6fd002854b3720aa9bbb8eb5963c9a7ae8ae5deb18ded40d`.

Two independent read-only audit lines were used: one for the algebra,
clock direction, and measure/Hölder gate; the other for theorem scope,
claim boundaries, tag continuity, and certificate binding.  Earlier audit
rounds against the superseded pointwise-floor version do not count toward
this verdict.

## 2. Verdict

**PASS.  No mathematical or claim-boundary blocker remains for this
frozen terminal-window theorem.**

The result proved analytically is

\[
 (P_R^M)^{2/3}
 \ge2^{2/3}(2L)^{-1/3}e^{\kappa_2L^2}
       \sum_{\ell=2}^NE_\ell,
 \qquad
 \kappa_2=\frac{8831}{1905120}>0.
\]

If \(S>0\) and \((P_R^M)^{2/3}\le MS\), it follows that

\[
 \frac{\sum_{\ell=2}^NE_\ell}{S}
 \le2^{-2/3}M(2L)^{1/3}e^{-\kappa_2L^2},
\]

and hence

\[
 \left\|\frac{\mathbf E}{S}-\mathbf e_1\right\|_{\ell^1}
 \le2^{1/3}M(2L)^{1/3}e^{-\kappa_2L^2}.
\]

Thus the conclusion is first-shell concentration, not merely concentration
on an unspecified coordinate.

## 3. Audit ledger

1. **Geometry and measurability — PASS.**  The moving lobe cylinders are
   explicitly defined, Lebesgue measurable, and pairwise disjoint because
   their hard-shell indices are distinct.
2. **Clock detection — PASS.**  For each target separately,
   \(E_\ell\le\sup_JK_{k_\ell,R}\le v_{k_\ell,R}\), so
   \(Y_{2,R}^{\rm sf}\ge Q\).  Maximizing times may differ by shell; no
   common time slice is used.
3. **Spacetime Hölder — PASS.**  The identities
   \(|\mathcal O_{\ell,+}|=L_\ell R^6/16\) and
   \(\int_{\mathcal O_{\ell,+}}|u|^2
   =2R^4\Gamma_\ell^{-1}E_\ell\) give the exact coefficient
   \(2\sqrt2\,R\Gamma_\ell^{-5/4}L_\ell^{-1/2}\).
4. **Weighted packing — PASS.**  Weighted Hölder has equality precisely on
   \(E_\ell=C d_\ell^{-2}\), and
   \(\sum_{\ell=2}^Nd_\ell^{-2}
   \le2\Gamma_2^{5/2}L_2\) has no factor depending on \(N\).
5. **Exact exponents — PASS.**  The finite ledger confirms
   \(\kappa_1=-769/1905120<0\) and
   \(\kappa_2=8831/1905120>0\).
6. **Route implication — PASS WITH ITS STATED HYPOTHESIS.**  If signed
   cumulative flux is separately proved comparable to \(S\), then
   \(Y_2=o(S)\) gives \(E_1=o(S)\), while
   \((P_R^M)^{2/3}=o(S)\) gives
   \(\sum_{\ell\ge2}E_\ell=o(S)\), contradicting
   \(S=E_1+\sum_{\ell\ge2}E_\ell\).
7. **Finite certificate — PASS.**  The deterministic generator reports
   21/21 exact-arithmetic checks, a passing exponent ledger, and 22/22
   structural checks.  A deliberate mutation of the frozen definition of
   \(U\) was detected by the fail-closed sentinel check.  Repeated runs were
   byte-identical.

## 4. Boundary

The theorem assumes realized kinetic lobe mass averaged on one fixed
terminal window.  It does not extract such mass from an arbitrary large
terminal clock.  Endpoint-only spikes, accumulated viscous or defect
dissipation, earlier positive variation, and source/flux effects remain
outside the theorem.

The signed cumulative flux lower bound, a full square-function upper bound,
the arbitrary-clock stopping-time/dissipation alternative, the fixed-scale
inequality (Q.1), regularity, singularity formation, and the Clay Millennium
problem remain **OPEN**.  **NOT CLAY.**
