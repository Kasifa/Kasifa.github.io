# R0.71Q claim--evidence matrix

**Audit date:** 2026-08-26  
**Release boundary:** finite quantitative complex-time/Jensen audit only

| ID | Claim | Evidence | Status | Exact boundary |
|---|---|---|---|---|
| Q1 | R0.71P leaves a distinct entry-time counting measure after simultaneous spatial batching. | `research/r071p_report-source.md`, Theorem 5.1 and certificates. | inherited, unconditional | Does not replace counting measure by Lebesgue time. |
| Q2 | A Hilbert-valued analytic observable on (D(t_*,R)) satisfies the Jensen count with radius, upper norm, and a nonzero center anchor. | Jensen formula plus complex Hahn--Banach; R0.71Q (2.2). | proved, classical | Scalar projection may add zeros and counts multiplicity. |
| Q3 | Temam's lobe contains (D(T/4,T/64)). | Rational inequalities (3.6)--(3.7); exact certificate `temamLobeDisk`; 200,000-point independent probe. | proved | Conservative inclusion, not an optimal inradius. |
| Q4 | The local complex-time scale is (T_1(R)=K_\nu(1+R^2)^{-2}). | Temam Chapter 7, formulas (7.8)--(7.12), restarted at a classical time. | known theorem | (R) is a strong (V=H^1) norm, not Leray energy alone. |
| Q5 | A fixed shell--cell observable has a finite complex (L^2) upper bound on the inner disk. | Temam (7.17) and boundedness of (mathcal O_\alpha:D(A)\to L^2); R0.71Q (3.8)--(3.10). | proved, conditional finite | Operator norm may grow with shell/cell; no all-frame claim. |
| Q6 | A finite owned cover gives the anchor-taxed weighted packing formula (4.6). | Exact pointwise Borel ownership, integer componentwise Jensen capacities, the empty-cell convention (H_m=0), and the R0.71P time-slice batch envelope. | proved, conditional finite | The left endpoint atom is owned inside an open inner disk, the right endpoint is excluded, and the bound pays (R_o,M_\alpha,a_{\alpha m},J,H_m) plus the component sum. |
| Q7 | A direct sum does not detect the union of component zero sets. | (oplus_\alpha C_\alpha=0) iff every component is zero. | proved, elementary | A scalarized product contains the union and may add projection zeros; a finite tensor product has exactly the union at vector level. Both retain the product-anchor and summed log taxes. |
| Q8 | Fixed analytic radius and fixed complex upper norm do not bound distinct real zeros. | Rational finite Blaschke products (B_N), exact and independent certificates. | proved, abstract analytic | Not an NSE trajectory. |
| Q9 | The Jensen anchor logarithm is asymptotically sharp. | (N\le\log(1/|B_N(0)|)/\log2\le N+1/\log2). | proved | Sharp for the scalar multiplicity count up to an additive constant. |
| Q10 | The same family yields unbounded positive-entry count, not only unsigned zeros. | (widetilde C_N=B_N^2e), (F=e), (Y=1): every even-order zero has (A_+=1). | proved, abstract analytic | Not a repeated-face NSE construction. |
| Q11 | Uniform per-component radius, norm, and anchor do not control the zero-set union independently of truncation. | (g_q(z)=z-b_q), (b_q\in(1/4,1/2)); exact union certificate. | proved, abstract analytic | Shows a component tax, not that NSE realizes the family. |
| Q12 | Uniform local radius ratio and relative anchor do not pay the number of windows. | (C_N=(\sin(\pi Nz)/(\pi N))^2e) with (N) owned cells and uniform (M_m/a_m). | proved, abstract analytic | Global complex growth can absorb, but cannot remove, the cost. |
| Q13 | Leray's (L_t^1Y) budget does not imply an inverse-window ((1+Y)^2) budget. | Exact triangular pulse (Y_N=N(1-Nt)_+): (int Y_N=1/2), (int Y_N^2=N/3). | proved, budget separation | Pulse is not asserted to be NSE enstrophy. |
| Q14 | Total enstrophy cannot give a positive lower bound for every filtered observable at a prescribed time. | R0.71P smooth NSE initial jet has (Y(0)=1), (C_\alpha(0)=0), (C_{\alpha,t}(0)\ne0). | proved at one NSE initial jet | Does not prove many interior NSE zeros. |
| Q15 | A zero count alone does not pay the weighted target. | Formula (4.6) still requires (H_m=\sup_{K_m}\mathcal H) for nonempty ownership cells, with (H_m=0) on empty cells. | proved, logical | No conversion from atomic sampling to a Leray-time integral follows. |
| Q16 | The checked primary literature supplies no lower filtered-observable anchor or all-filter temporal packing theorem. | Two bounded source waves in `research/r071q_literature_audit.md`. | bounded negative finding | Not a nonexistence, originality, or priority claim. |
| Q17 | R0.71Q proves a uniform NSE zero count, continuation criterion, or global regularity. | No supporting theorem or certificate. | **not proved** | Explicitly excluded from every public claim. |

## Decision gate

The direct analytic route would close only after all of the following were
paid uniformly as (K\uparrow T^*) and (Lambda\uparrow\Lambda_\infty):

1. a noncollapsing complex-time cover;
2. summable complex-growth bounds;
3. quantitative nonzero anchors or a substitute nondegeneracy law;
4. a component-union coupling estimate;
5. a pointwise or otherwise event-adapted payment of (mathcal H).

None is supplied by the present Leray budget.  The branch is therefore kept
as a finite conditional theorem and classified as closed-as-a-method at
R0.71Q.
