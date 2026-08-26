import { createHash } from "node:crypto";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const source = await collectSiteStrings(publicDirectory);
const current = JSON.parse(await readFile(translationPath, "utf8"));

const translationRows = String.raw`
001 ||| Open the complete 89-note index
002 ||| give exponential-sum sampling bounds,
003 ||| record observation-time and gap costs in the moment method,
004 ||| Test the all-root count, quadratic extra-root proliferation, and the floor-free complete ledger; keep strong coupling and \(A_0\to0\) separate.
005 ||| Open interface · R0.71Z
006 ||| cumulative recap and 89-note index
007 ||| quantify the node and dimension losses in positive-real Vandermonde inverses.
008 ||| distinguishes ordinary conditioning from structured total-nonnegative computation. None of these sources gives the NSE root-coordinate identity, matched-background ledger, \(N^{-1}\) payment, or all-root count in this section; the bounded search makes no claim of originality, priority, or nonexistence.
009 ||| shows that a certified IFT radius depends on the inverse Jacobian and Lipschitz data,
010 ||| Literature review v1.11 · 2026-08-26
011 ||| Published theorems are listed as established results, 2026 preprints are marked separately, and this site's R0.69P–R0.71Y material is classified only as research notes. Calculations and notes are not extrapolated into regularity theorems.
012 ||| support finite-dimensional Chebyshev / total-positivity nondegeneracy;
013 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U gives the conditional-incidence, genuine-internal-entry, second-time-jet, and finite-recurrence boundaries. R0.71V–W separates the fixed zero-level trace and rules out the data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint inside a fixed-dimensional small-coupling family; R0.71Y proves that the selected growing-root ratio decays as \(N^{-1}\) under bounded observation coupling. The all-root problem and general regularity remain open.
014 ||| Exact \(\ell^2\) contraction, the root-coordinate identity, full floors, and the carrier-lattice cost give \(\mathcal J_N^{\rm sel}/(D_N^{1/3}\Lambda_1)\le C\nu^{-2}\delta_{\rm obs,N}^{4/3}/N\).
015 ||| R0.71Y does not first seek a growing-dimensional ECT inverse. It uses diagonal heat cancellation and active-sector \(\ell^2\) contraction at exact roots. For real shear, unit phases, a fixed target, and full data/root-time floors, the selected ratio is bounded by \(C\nu^{-2}\delta_{\rm obs}^{4/3}/N\). Under bounded observation coupling, the selected prescribed-root gain vanishes; nonvanishing requires coupling at least of order \(N^{3/4}\). The general \(R/M\) bound only shows that bounded-coupling escape needs at least \(R\gtrsim M^2\); it does not give an all-root count. R0.71Z examines only the total-root and floor-free interface. The six filters below remain unchanged.
016 ||| Primary-source boundary for R0.71Y
017 ||| What R0.71Y closes and what R0.71Z alone tests
018 ||| 01 · Exact setting
019 ||| 02 · Root slopes
020 ||| 03 · Sampling theorem
021 ||| 04 · Carrier cost
022 ||| 05 · R0.71X correction
023 ||| 06 · Root separation
024 ||| 07 · Additional roots
025 ||| 08 · ECT conditioning
026 ||| 09 · Two audit layers
027 ||| The 90-digit Decimal producer passes 13/13, covering the amplitude optimizer, multiplier bound, \(N^{-1}\) and \(N^{-2}\) envelopes, critical \(N^{3/4}\) coupling, the heat-weighted correction, and the equal-grid inverse lower bound.
028 ||| place the inverse Jacobian and Lipschitz data in the certified IFT radius;
029 ||| Version v0.71Y · 2026-08-26
030 ||| This section examines the growing-dimensional route left by R0.71X. For \(M=2N+1\) unit-modulus carrier phases, real shear, a fixed target, and full data and root-time enstrophy floors, the \(\ell^2\) contraction and root-coordinate identity of the exact triangular evolution give \(\mathcal J_N^{\rm sel}/(D_N^{1/3}\Lambda_1)\le C\nu^{-2}\delta_{\rm obs,N}^{4/3}/N\). Thus uniformly bounded observation coupling cannot preserve the prescribed-root gain. The result controls selected exact roots, not all nonlinear roots.
031 ||| In parallel, test whether the matched background can be removed or replaced automatically by a weak-solution / full-ledger quantity. Strong coupling, \(A_0\to0\), and different geometries remain separate interfaces.
032 ||| Cost
033 ||| The theorem uses real shear, unit carrier phases, and the full growing cost
034 ||| The independent NumPy/SciPy finite-matrix reconstruction passes 12/12: zero skew defect, semigroup contraction, root slope, multiplier, optimized envelope, separated bound, determinant factorization, and inverse lower bound all pass. These are finite algebraic corroborations, not DNS, and they do not construct a growing exact-root family.
035 ||| Additional roots
036 ||| Nonvanishing requires \(\delta_{\rm obs}\gtrsim N^{3/4}\); under the general \(R/M\) ledger, bounded-coupling escape requires at least \(R\gtrsim M^2\).
037 ||| The figure shows only analytic bounds, certificate envelopes, and a conditioning lower bound
038 ||| give exponential-sum sampling inequalities;
039 ||| Root separation improves the bound from \(N^{-1}\) to \(1/(h_NN^2)\)
040 ||| Observation coupling, Dyson exposure, and the IFT certificate must be kept separate
041 ||| Distinct positive integers and unit phases force
042 ||| Suppose, independently of \(q,N,S,P,z\), that constants \(c_D,c_Y>0\) satisfy \(D_N\ge c_Dq^2E_N\), and each counted root satisfies \(Y_N(t_{m,q})\ge c_Yq^2E_N\). Then
043 ||| Separation
044 ||| The result closes the selected prescribed-root gain inside the uniformly small Dyson/IFT corridor, and also every sampled-root family growing at most linearly under bounded coupling. It does not control the unknown set of all nonlinear roots.
045 ||| The analytic chain and two independent computational layers were checked separately
046 ||| Open-route matrix
047 ||| quantify the time and gap costs in the moment method;
048 ||| Let \(M=2N+1\), choose pairwise distinct positive integers \(r_1,\ldots,r_M\), and give each of the \(M\) nonzero launch-vector coefficients unit modulus. The scaled active sector satisfies
049 ||| There is no uniform unweighted lower bound by \(\|z\|_2\). The fixed-dimensional endpoint theorem in R0.71X did not use this incorrect comparison, so that theorem is unaffected.
050 ||| Suppose \(F_0(\tau_m)=0\), and define
051 ||| Let \(h_N\) be the minimum separation between the scaled roots and the left boundary, and put \(W_N^2=\sum_l|z_l|^2e^{-2\nu d^2r_l^2A_0}\). The exact finite-\(q\) estimate is
052 ||| Setting
053 ||| Real shear makes \(V_z(x)\) skew-adjoint, while \(D_q\) is self-adjoint and nonpositive, so
054 ||| show that positive-real Vandermonde inverses pay node and dimension losses.
055 ||| explains why structured total-nonnegative computation must be distinguished from an ordinary condition number.
056 ||| Conditioning
057 ||| Conditional consequence:
058 ||| Figure R0.71Y-1. A: the exact lattice factor \(NM/K_s\) decays as \(N^{-1}\). B: at fixed \(\delta_{\rm obs}=1/8\), the no-separation envelope is \(N^{-1}\); a fixed root gap gives \(N^{-2}\), while \(h=N^{-1}\) returns to \(N^{-1}\). C: for canonical rates and \(h=N^{-3}\), the \(\log_{10}\) equal-grid inverse lower bound rises from 1.806 at \(N=4\) to 49.029 at \(N=64\). The figure contains no DNS or growing-root simulation and does not treat the conditioning lower bound as an upper bound for the nonlinear IFT radius.
059 ||| After full payment, the selected-root endpoint ratio is at most \(N^{-1}\)
060 ||| Next object: total-root / floor-free ledger
061 ||| The next section first asks whether all real roots of the exact triangular nonlinear target coordinate can be counted uniformly using carrier dimension, observation coupling, and observation-layer geometry. If not, it will seek a reproducible candidate with at least quadratic root proliferation.
062 ||| Slope
063 ||| Correction
064 ||| Research note R0.71Y · GROWING ROOTS · OPERATOR SAMPLING
065 ||| Research note R0.71Y: under the declared triangular Fourier-lattice family and full data/root-time enstrophy floors, growing dimension cannot rescue the selected-root endpoint gain under bounded observation coupling; this is not an all-root theorem or a general regularity result.
066 ||| General \(M\) carriers and \(R\) sampled roots yield only a conditional payment
067 ||| Thus bounded \(\delta_{\rm obs,N}\) gives a vanishing selected ratio. Nonvanishing requires at least \(\delta_{\rm obs,N}\gtrsim N^{3/4}\), while divergence requires \(\delta_{\rm obs,N}/N^{3/4}\to\infty\). The bound \(\Lambda_1\ge\nu^2\) retains the full viscous baseline; the full-frequency rotational charge only increases the denominator.
068 ||| Since \(D_q\) is diagonal, the heat term vanishes in the root coordinate. The physical-time slope is exactly
069 ||| Under bounded observation coupling,
070 ||| Hence the exact nonlinear sampled-slope mass satisfies \(G_N^{\rm ex}\le NM\Omega_N^2\). There is no Gronwall exponent and no ECT determinant or inverse-Jacobian constant.
071 ||| the endpoint gain from prescribed growing roots vanishes as \(N^{-1}\)
072 ||| At an exact root, the observation-layer operator directly controls the target slope
073 ||| In the declared real-shear, fixed-target, unit-phase, matched-floor triangular setting, any selected \(N\) exact roots satisfy the upper bound \(C\nu^{-2}\delta_{\rm obs}^{4/3}/N\); under bounded coupling the ratio vanishes.
074 ||| The \(N^3\) carrier-lattice cost dominates the worst-case \(N^2\) sampling sum
075 ||| Growing dimension alone cannot rescue the small-coupling prescribed-root mechanism of R0.71W
076 ||| This narrows the later search to more specific exceptions: quadratic extra-root proliferation, a floor-free or sparse-phase ledger, strong observation coupling, an \(A_{0,N}\to0\) short pulse, non-unit phases, or different geometry. It does not shrink the class of potential singular solutions in general three dimensions.
077 ||| This is a definite route-closing result, not a partial solution of the Millennium problem
078 ||| These primary sources do not give the NSE root-coordinate identity, matched-background ledger, \(N^{-1}\) payment, or all-root count in this section. The bounded search makes no claim of originality, priority, or nonexistence.
079 ||| Status · R0.71Y completed
080 ||| all-root count, floor-free / sparse-phase / non-unit-phase cases, strong coupling, \(A_{0,N}\to0\), quadratic extra roots, and different geometries.
081 ||| Under bounded coupling, any extra-root escape needs at least \(R\gtrsim M^2\). But this section does not prove an upper bound on the number of all nonlinear target zeros, so this conditional conclusion is not a complete all-root theorem.
082 ||| Canonical \(r_l=l\) with \(hN^2\to0\) produces rapid inverse growth. This is a conditioning squeeze, not an upper bound on the true nonlinear IFT branch radius.
083 ||| ECT still determines whether exact roots can be constructed stably, but it does not enter the upper-bound proof
084 ||| The ECT inverse is not a prerequisite for this upper bound. At an exact root, the diagonal heat coordinate vanishes, and the target slope is one coordinate of the shear multiplication operator acting on the active scalar. The full evolution is also an \(\ell^2\) contraction. Therefore the selected slopes can be settled directly without computing the interpolation inverse.
085 ||| The ECT, Vandermonde, and quantitative-IFT literature supports only its respective stated layers
086 ||| For equal-grid roots \(\tau_m=mh\), let \(x_l=e^{-2\nu d^2hr_l^2}\). The integrated-response matrix factors exactly into cumulative-sum, Vandermonde, and diagonal factors, so
087 ||| Fixed \(h_N\) gives \(N^{-2}\), while quasi-uniform \(h_N\asymp N^{-1}\) returns to \(N^{-1}\). If the first root lies on \(A_0\), only this \(h_N^{-1}\) corollary degenerates; the original weighted-kernel form remains valid.
088 ||| The Fourier multiplier upper bound gives \(\Omega_N^2/K_{v,N}\le2\pi^2K_z^2/3\). Optimizing the scalar/shear amplitude ratio gives the extremum at \(S^2K_s/(P^2K_v)=3\). These three steps yield the \(N^{-1}\) bound above.
089 ||| The launch-to-root Dyson size is \(\eta_{\rm Dyson,N}=(P/q^2)\int_0^{\tau_N}\|V_z(x)\|dx\). A complete quantitative IFT certificate also pays the inverse Jacobian and derivative-Lipschitz constant. For fixed \(A_0>0\), only the audited one-way control \(\delta_{\rm obs,N}\le C_{A_0,\nu,d}\eta_{\rm Dyson,N}\) holds; the reverse fails, and the constant degenerates when \(A_{0,N}\to0\).
090 ||| The matched background must pay the entire growing cost \(E_N=S^2K_{s,N}+P^2K_{v,N}\); the old fixed-\(N\) background cannot be reused for free.
091 ||| R0.71X shows that a fixed-dimensional small-coupling family can attain the \(D^{1/3}\) endpoint. R0.71Y proves that merely increasing the prescribed roots and carrier dimension instead produces \(N^{-1}\) suppression after paying the exact observation operator, full lattice cost, and matched floor. ECT conditioning is no longer a prerequisite for deciding the selected-root gain.
092 ||| One lower comparison in the R0.71X route matrix needs correction. Because the operator supremum begins at \(A_0>0\), the correct lower bound is heat weighted:
093 ||| R0.71Y · 2026-08-26 · Personal mathematics research log
094 ||| R0.71Y growing-root operator sampling: lattice cost, selected-root envelopes, and the equal-grid inverse lower bound
095 ||| R0.71Y | Operator-sampling suppression for growing-root families
096 ||| The selected exact-root atom sum is at most C delta_obs^(4/3)/N; nonvanishing requires delta_obs to grow at least as N^(3/4).
097 ||| a universal endpoint, continuation criterion, finite-time singularity, global regularity, originality, or priority conclusion.
098 ||| 02 · Complete 89-note index
099 ||| In parallel, test whether the matched background can be removed or replaced automatically by a weak-solution / full-ledger quantity. Strong coupling, \(A_0\to0\), non-unit phases, and different geometries remain separate interfaces.
100 ||| Open latest node R0.71Y
101 ||| Recap endpoint: R0.71Y
102 ||| Public notes at recap endpoint: 149
103 ||| As of R0.71Y there is no new unconditional continuation criterion, no reduction of the full class of potential singular solutions, and no proof of finite-time breakdown. The 89 nodes cannot be interpreted as a percentage of the Millennium problem completed.
104 ||| Cumulative recap · R0.61–R0.71Y · 2026-08-26
105 ||| Seventeen phases and 89 nodes: from reduced recurrence and the post-R0.70A dynamic route through the fixed-zero ledger and the family-internal one-third endpoint, then to bounded-coupling selected-root suppression.
106 ||| Nodes included: 89
107 ||| The next finite task first asks whether all real roots of the exact triangular nonlinear target coordinate can be counted uniformly using carrier dimension, observation coupling, and observation-layer geometry. If not, it will seek a reproducible candidate with at least quadratic extra-root proliferation.
108 ||| The small-coupling prescribed-growing-root route is closed; the all-root and general problems remain open
109 ||| This is not a complete all-root no-go. Under bounded coupling, an extra-root escape may still require at least quadratic proliferation \(R\gtrsim M^2\); the floor-free, sparse/non-unit-phase, strong-coupling, \(A_{0,N}\to0\), and different-geometry cases are also not closed.
110 ||| This page follows the R0.00–R0.60 phase recap and organizes the 89 research nodes from R0.61 through R0.71Y. It records chronologically what each segment actually proved, which proposals were ruled out by a specific counterexample or scale analysis, and which assumptions have not been derived from the Navier–Stokes equations.
111 ||| The R0.00–R0.60 material remains in the preceding phase recap. R0.60 concluded that the full Fourier–Leray structure and higher-order calculations could continue, but still did not control a critical quantity for general three-dimensional solutions. The following 89 nodes advance along that gap; every completed release from R0.70A onward remains in the route and index.
112 ||| Post-R0.60 research recap: a chronological organization of 89 research nodes from R0.61 through R0.71Y; the latest section proves that the selected growing-root endpoint ratio decays as the inverse of N under bounded observation coupling, while preserving the all-root and general-regularity boundaries.
113 ||| Public notes from R0.61–R0.71Y: 89 sections
114 ||| R0.61–R0.71Y recap · 2026-08-26
115 ||| R0.61–R0.71Y research nodes
116 ||| R0.61–R0.71Y | Post-R0.60 research recap
117 ||| R0.71U gives a zero-count-independent all-shell second-time-jet theorem and finite prescribed recurrence. R0.71V turns the first-row ledger into Leray–Hopf right-rooted excursion-height packing and separates the level integral from the fixed zero-level atom. R0.71W rules out the data-uniform complete first-row bound, and R0.71X completes the root set and reaches the \(D^{1/3}\) endpoint inside a fixed-dimensional small-coupling family. R0.71Y then grows \(M=2N+1\) unit carriers and selected exact roots: exact \(\ell^2\) contraction, the root-coordinate identity, \(K_s\gtrsim N^3\), and full floors give \(\mathcal J_N^{\rm sel}/(D_N^{1/3}\Lambda_1)\le C\nu^{-2}\delta_{\rm obs,N}^{4/3}/N\). Under bounded coupling the selected ratio vanishes; nonvanishing requires at least \(\delta_{\rm obs,N}\gtrsim N^{3/4}\). The general \(R/M\) ledger only says that escape needs at least \(R\gtrsim M^2\); it does not give an all-root count.
118 ||| R0.71U–R0.71Y · second-time jet, complete first row, and the growing-root boundary
119 ||| R0.71X reaches the \(D^{1/3}\) endpoint inside a fixed-dimensional small-coupling family. R0.71Y shows that if only unit carriers and selected prescribed roots are increased, and the full lattice cost, matched enstrophy floors, and exact observation operator are paid, the normalized endpoint ratio is at most \(C\delta_{\rm obs}^{4/3}/N\). Thus growing dimension alone does not produce the proposed gain.
120 ||| R0.71Y's growing-root operator-sampling theorem: under real shear, a fixed target, unit phases, and full data/root-time floors, selected exact roots satisfy \(\mathcal J_N^{\rm sel}/(D_N^{1/3}\Lambda_1)\le C\nu^{-2}\delta_{\rm obs,N}^{4/3}/N\). Under bounded coupling the selected ratio vanishes, and the fixed-gap estimate improves to \(C\delta_{\rm obs}^{4/3}/(h_NN^2)\). The section also corrects the unweighted lower comparison in the R0.71X route matrix: the correct lower bound is heat weighted; observation coupling, Dyson exposure, and the complete IFT certificate are distinct.
121 ||| R0.71Y figure
122 ||| R0.71Y certificates
123 ||| R0.71Z tests the total-root count and floor-free complete ledger
124 ||| From the family-internal one-third endpoint to selected growing-root suppression
125 ||| The theorem controls selected exact roots only and assumes real shear, unit phases, a fixed target, and matched floors. It is not an all-root theorem, universal endpoint, continuation criterion, finite-time singularity, or global-regularity result; the floor-free, strong-coupling, \(A_{0,N}\to0\), non-unit-phase, and different-geometry cases remain open.
126 ||| For \(M=2N+1\) unit-modulus carrier phases, real shear, and a fixed target, the exact triangular Fourier-lattice evolution is an \(\ell^2\) contraction. At every selected exact root the diagonal heat coordinate vanishes, and the target slope is exactly one coordinate of the shear multiplication operator acting on the active scalar.
127 ||| annulus exclusion → source-core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → shared-response first-order channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression
128 ||| Test the total-root count and floor-free complete ledger.
129 ||| Test whether all nonlinear target roots can be counted uniformly, and whether the matched enstrophy floor can be removed or paid automatically by the complete ledger.
130 ||| After the static annular families are rigorously excluded, the route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–V separates the second-time jet, Leray-paid excursion, and fixed zero-level trace. R0.71W rules out the data-independent complete first-row ledger, and R0.71X reaches the \(D^{1/3}\) endpoint inside a fixed-dimensional small-coupling family. R0.71Y uses exact \(\ell^2\) contraction, the root-coordinate identity, and the carrier-lattice cost to prove that the selected growing-root ratio decays as \(N^{-1}\) under bounded observation coupling; the all-root, floor-free, and strong-coupling routes remain open.
131 ||| Cumulative recap R0.61–R0.71Y · 2026-08-26
132 ||| There is still no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71Y proves that in the declared unit-phase, matched-floor triangular setting, the selected growing-root ratio is at most \(C\nu^{-2}\delta_{\rm obs}^{4/3}/N\). This is a route-closing theorem, not an all-root theorem or a general regularity result.
133 ||| Previous review v1.10 · 2026-08-26
134 ||| A systematic review places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019–2026, and this site's R0.69P–R0.71Y route in one view. The historical R0.61–R0.69O nodes remain in the cumulative recap.
135 ||| Next step R0.71Z:
136 ||| First test whether all nonlinear target roots can be counted using carrier dimension and observation coupling, then test whether the matched floor can be removed; treat strong coupling and \(A_0\to0\) separately.
137 ||| Research note R0.71Y · 2026-08-26
138 ||| Read research note R0.71Y →
139 ||| Growing dimension cannot rescue the prescribed-root endpoint gain under bounded coupling
140 ||| Expand 59 public notes
141 ||| Review v1.11 · 2026-08-26
142 ||| Under bounded observation coupling, the selected growing-root endpoint ratio vanishes as \(N^{-1}\).
143 ||| The full data/root-time enstrophy floors, Fourier multiplier upper bound, amplitude optimization, and unavoidable lattice cost \(K_s\gtrsim N^3\) give \[ \frac{\mathcal J_N^{\rm sel}}{D_N^{1/3}\Lambda_1} \le C\nu^{-2}\frac{\delta_{\rm obs,N}^{4/3}}N. \] Under bounded \(\delta_{\rm obs,N}\) the selected ratio vanishes; nonvanishing requires at least \(\delta_{\rm obs,N}\gtrsim N^{3/4}\). For general \(M\) carriers and \(R\) sampled roots, the bound is \(CR\delta_{\rm obs}^{4/3}/M^2\), so bounded-coupling escape requires at least quadratic root proliferation.
144 ||| The post-R0.60 route has seventeen segments: reduced Picard analysis and the shear boundary; transverse perturbations; local pressure budgets; signed physical annuli; moving labels and source-core duality; defect tensors and finite observations; full-frame covariance; the constant-projection boundary; positive output and the material-heat tent; projected-Lamb heat volume; local heat packing and the critical-trace obstruction; and positive-entry temporal packing, conditional Jensen/incidence, packet/Bessel analysis, internal-entry scaling, the second-time jet, finite recurrence, Leray-paid excursions, the fixed-zero boundary, the complete first-row data-uniform no-go, fixed-small-coupling one-third internal saturation, and bounded-coupling selected-root suppression. R0.70A–R0.71Y contains 51 completed releases.
145 ||| The cumulative recap after the R0.60 recap contains 89 nodes; the full site now has 149 public research notes
146 ||| R0.70A–R0.71Y completed releases
147 ||| The R0.71X route matrix's unweighted operator lower bound is also corrected to a heat-weighted lower bound. Observation coupling, launch-to-root Dyson exposure, and the complete quantitative IFT certificate are distinct; for fixed \(A_0>0\), only the one-way control \(\delta_{\rm obs}\le C\eta_{\rm Dyson}\) holds.
148 ||| R0.71Y completed:
`;

const englishRows = translationRows
  .trim()
  .split("\n")
  .map((row, index) => {
    const expected = String(index + 1).padStart(3, "0") + " ||| ";
    if (!row.startsWith(expected)) {
      throw new Error("unexpected R0.71Y translation row " + (index + 1));
    }
    return row.slice(expected.length);
  });

const currentWithoutBatch = current.filter(
  (entry) => !/^r071y\d+$/.test(entry.id),
);
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.71Y batch");
}

const missingFileOrder = [
  "literature-review.html",
  "notes/r0-71y.html",
  "recap-r0-61-r0-71y.html",
  "research-review.html",
];
function priority(entry) {
  const value = missingFileOrder.indexOf(entry.files[0]);
  return value < 0 ? 9 : value;
}
const missing = source
  .filter((entry) => !currentByChinese.has(entry.zh))
  .sort(
    (left, right) =>
      priority(left) - priority(right) ||
      left.zh.localeCompare(right.zh, "zh-CN"),
  );
const missingHash = createHash("sha256")
  .update(JSON.stringify(missing.map((entry) => entry.zh)))
  .digest("hex");
if (
  missing.length !== 148 ||
  englishRows.length !== missing.length ||
  missingHash !== "86be89fde3229204b536184f62bae84775cbea8a24687fa3578981a001ee6505"
) {
  throw new Error(
    "R0.71Y translation source drift: missing=" +
      missing.length +
      " rows=" +
      englishRows.length +
      " hash=" +
      missingHash,
  );
}

function same(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

const translated = missing.map((entry, index) => {
  const en = englishRows[index];
  if (!same(extractProtectedTokens(entry.zh), extractProtectedTokens(en))) {
    throw new Error(
      "protected-token mismatch at row " +
        String(index + 1) +
        ": " +
        entry.zh,
    );
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("blank or Chinese-containing translation: " + entry.zh);
  }
  if (/\b(?:we|our|ours|us)\b/i.test(en)) {
    throw new Error("first-person plural voice: " + entry.zh);
  }
  return {
    ...entry,
    id: "r071y" + String(index + 1).padStart(3, "0"),
    en,
  };
});

for (const relative of [
  "research-review.html",
  "literature-review.html",
  "recap-r0-61-r0-71y.html",
  "notes/r0-71y.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.11')) {
    throw new Error(relative + ": expected i18n cache version v1.11");
  }
}
for (const relative of [
  "recap-r0-61-r0-71x.html",
  "notes/r0-71x.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.10')) {
    throw new Error(relative + ": expected historical i18n cache version v1.10");
  }
}

const merged = [...currentWithoutBatch, ...translated];
if (new Set(merged.map((entry) => entry.zh)).size !== merged.length) {
  throw new Error("translation merge produced duplicate Chinese keys");
}
if (new Set(merged.map((entry) => entry.id)).size !== merged.length) {
  throw new Error("translation merge produced duplicate IDs");
}

await writeFile(translationPath, JSON.stringify(merged, null, 2) + "\n");
console.log(
  JSON.stringify(
    {
      source: source.length,
      existingWithoutBatch: currentWithoutBatch.length,
      activeMissingBefore: missing.length,
      added: translated.length,
      firstId: translated.at(0)?.id,
      lastId: translated.at(-1)?.id,
      total: merged.length,
      protectedTokenMismatches: 0,
      englishWithChinese: 0,
      firstPersonPlural: 0,
    },
    null,
    2,
  ),
);
