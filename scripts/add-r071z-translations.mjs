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
001 ||| Open the complete 90-note index
002 ||| The Dyson–Phillips expansion is an infinite sequence of iterated integrals; finite-dimensional zero counting cannot be applied without a finite closure or stability of the complex-domain tail zeros.
003 ||| The scattered-zero Sobolev inequality pays a fill-distance cost and does not provide a discrete all-root slope-mass estimate.
004 ||| The time-analyticity results provide only qualitative isolation of zeros. These sources are adjacent frameworks; they do not imply this section's BV lemma, combined dissipative row, or mixed-window cancellation. No claim of novelty, priority, or NSE regularity is made here.
005 ||| These sources provide analytic or nonautonomous evolution frameworks, but bounded time dependence alone does not yield the second-order time control required here.
006 ||| For complex-valued \(g\in W^{2,1}(I)\), R0.71Z directly proves a BV zero-slope-mass lemma: after listing the distinct zeros in the interval in order, \(\sum_m|g'(\tau_m)|^2\) is controlled by the first zero slope, \(\|g'\|_\infty\), and \(\int_I|g''|\), with no dependence on the number or spacing of the zeros. Applying it to the weighted target coordinate of the exact triangular real-shear system, then using the exact \(\ell^2\) contraction of the skew coupling, the target-row identity, and the combined dissipative row, gives a complete all-root slope-mass theorem. The zeros remain in the original observation window while the payment window extends leftward to launch; the common factor in \(\mathcal R_Y\) then cancels against the launch Parseval floor and gives the bound \(C\nu^{-2}\eta^{4/3}(1+\eta)M^{-2}\). No matched background floor, root-time floor, or growing-dimensional root count is required.
007 ||| A complex \(W^{2,1}\)/BV zero lemma bypasses root counting; exact triangular real-shear dissipation pays the complete root-slope mass. A launch-inclusive mixed window then gives the normalized bound \(C\nu^{-2}\eta^{4/3}(1+\eta)M^{-2}\), without a matched background or root-time floors.
008 ||| Test the critical regime as \(\eta\) grows with the carrier count, while treating the \(A_0\to0\) shrinking observation layer separately from a fixed positive launch.
009 ||| The conclusion covers only the declared triangular real-shear class, distinct integer carriers, a fixed target, and a positive launch. It proves neither a critical estimate for general NSE nor a result for strong coupling or a shrinking observation layer. The six filters below remain unchanged.
010 ||| Open interface · R0.72A
011 ||| cumulative recap and 90-note index
012 ||| Literature review · sources checked through 2026-08-27
013 ||| Literature review v1.12 · 2026-08-27
014 ||| Published theorems are listed as established results, 2026 preprints are marked separately, and this site's R0.69P–R0.71Z material is classified only as research notes. Calculations and notes are not extrapolated into regularity theorems.
015 ||| control only a fixed finite-dimensional ECT space;
016 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U gives the conditional-incidence, genuine-internal-entry, second-time-jet, and finite-recurrence boundaries. R0.71V–W separates the fixed zero-level trace and rules out the data-uniform complete first-row ledger. R0.71X reaches the one-third endpoint inside a fixed-dimensional small-coupling family; R0.71Y treats selected roots; R0.71Z gives an all-root slope-mass bound in the same exact triangular real-shear class and removes the matched background and root-time floors through a launch-inclusive mixed window. General Navier–Stokes regularity remains open.
017 ||| Sources checked through 2026-08-27. Later changes in publication status, versions, or official assessments will be recorded here while preserving the original evidence labels.
018 ||| all-root slope mass and mixed-window floor-free closure
019 ||| Giga et al.
020 ||| Primary-source boundary for R0.71Z
021 ||| What R0.71Z closes and where its boundary lies
022 ||| \(A_{0,M}\to0\), sparse or non-unit phases, and non-triangular geometry are recorded separately instead of combining several unclosed mechanisms into one conclusion.
023 ||| \(Q\) uses only \(F_{\pm r_l}\), with exact coefficients containing \(-2\nu d^2r_l^2\mp2\nu dr_lK_y/q\). One factor of \(r_l\) is paid by shear heat decay and the other by \(-\langle D_qF,F\rangle\), giving
024 ||| \(V_z'\) and \(V_z(D_q+\lambda_0)\) must be estimated together
025 ||| 02 · BV sampling
026 ||| 03 · Target row
027 ||| 04 · All-root theorem
028 ||| 07 · \(M^{-2}\) scale
029 ||| 08 · Double certificate
030 ||| Version v0.71Z · 2026-08-27
031 ||| No root counting:
032 ||| gives complete all-root \(M^{-2}\) suppression. At large coupling, the nonvanishing diagnostic of this upper bound is \(\delta_{\rm obs}\asymp M^{6/7}\); it is not a strong-coupling exact-root construction.
033 ||| The Dyson–Phillips expansion is an infinite iterated-integral series and does not directly inherit a uniform zero count.
034 ||| The ECT result concerns a fixed finite-dimensional kernel;
035 ||| The scattered-zero Sobolev inequality pays for fill distance and does not give the discrete derivative mass used here.
036 ||| First, quadratically many extra roots no longer matter because the slope mass is summed directly. Second, the matched floor is unnecessary because the launch-inclusive \(\mathcal R_Y\) automatically converts the root denominators into a single \(\sup Y\) retention factor.
037 ||| On a payment interval \(K\) containing every counted root, the common factor \(1/\mathcal R_Y(K)\) can be distributed linearly through the atom sum:
038 ||| The figure separates the lattice cost, all-root envelope, strong-coupling diagnostic, and retention
039 ||| High-precision algebra and an independent finite-matrix reconstruction have different roles
040 ||| Roots are still counted in \(I=[a,b]\); only the payment interval extends to launch
041 ||| Observation coupling is \(\delta_{\rm obs}=|\delta|\Omega\), where \(\Omega=\sup_{x\ge A_0}\|V_z(x)\|\).
042 ||| Combining the BV lemma, target-row estimate, and \(\|F\|_2\le\sqrt M\), every finite subset of roots satisfies
043 ||| Neither computation is DNS, and neither constructs a growing-dimensional exact-root family. The analytic proof carries the continuum theorem.
044 ||| Let \(h=P_0V_zF\). The target integrating factor \(g=e^{\lambda_0(x-A)}F_0\) satisfies
045 ||| Target row
046 ||| The squared slope mass of all exact roots is independent of the root count
047 ||| All roots
048 ||| The complete ledger absorbs the slope mass of all roots with an \(M^{-2}\) factor
049 ||| If \(K=[\sigma_q,b]\) contains launch, then \(\sup_KY\ge Y(\sigma_q)\gtrsim q^2(S^2K_s+P^2K_v)\). Thus the normalized ledger no longer requires a matched persistent background or a separate floor at every root time.
050 ||| If the complex scalar \(g\in W^{2,1}(a,b)\) satisfies \(g(\tau_m)=0\), then
051 ||| Restricting the interval to \(I\) when computing \(\Lambda_1\) makes an additional retention factor unavoidable
052 ||| Real \(z_l\) makes \(V_z\) skew-adjoint and \(D_q\) self-adjoint nonpositive. Therefore
053 ||| Real shear gives exact contraction and turns one derivative into a dissipation budget
054 ||| provide parabolic evolution frameworks, but bounded time dependence alone does not imply \(H_t^2\).
055 ||| Figure R0.71Z-1. A: the exact \(M/K_s\) factor decays as \(M^{-2}\). B: for bounded \(\delta_{\rm obs}\), the complete all-root envelope is \(M^{-2}\); the old selected-root \(M^{-1}\) rate appears only as a neutral reference. C: bounded, \(M^{1/2}\), and critical \(M^{6/7}\) coupling laws. D: fixed-window heat retention vanishes exponentially, whereas launch-inclusive retention is 1. The figure contains only analytic and certificate data, not DNS.
056 ||| Next object: strong coupling / shrinking layer
057 ||| The next section first asks whether, as \(\delta_{\rm obs}\) approaches the \(M^{6/7}\) scale, exact roots, the full nonlinear rotational charge, and an IFT / Dyson certificate can all be retained simultaneously.
058 ||| Apply \(\mathcal R_Y\) first, then take the viscous baseline
059 ||| The bounded primary-source search found no theorem of the same form; this is not a claim of originality, priority, or nonexistence.
060 ||| Between adjacent zeros, the average derivative over the interval is exactly zero
061 ||| Research note R0.71Z · ALL ROOTS · BV SAMPLING · MIXED WINDOW
062 ||| Research note R0.71Z: in the declared real-shear triangular Fourier-lattice class, bounded-variation sampling controls the slope mass of all target roots, while a complete ledger containing launch removes the rootwise enstrophy floor; this is not a general three-dimensional regularity theorem.
063 ||| Ruled out:
064 ||| Taking the supremum over all finite subsets then handles the complete zero set; no zero-count theorem is needed first.
065 ||| escape through quadratic extra roots or a matched background alone, within the same declared class.
066 ||| This is a complete all-root upper bound for the declared exact triangular class, not a general 3D NSE endpoint.
067 ||| This is a rigorous mechanism-exclusion result, but it covers only the exact triangular 2.5D class. It neither reduces the set of possible singular mechanisms in general three dimensions nor gives a continuation criterion.
068 ||| This step avoids the global \(\|D_qF\|_2\) and an unnecessary second spectral moment.
069 ||| The proof, literature record, double certificate, and journal-figure package are all retained
070 ||| The proof uses only \(\int_{\tau_{m-1}}^{\tau_m}g'=0\) and one integration by parts. The constant is independent of root count, minimum gap, and fill distance, and it does not use a vector-valued Rolle theorem.
071 ||| support time analyticity but do not provide an \(M^{-2}\) all-root payment.
072 ||| Status · R0.71Z completed
073 ||| The amplitude ratio is still maximized at \(S^2K_s/(P^2K_v)=3\). Then use
074 ||| Under bounded observation coupling, the complete all-root endpoint ratio is at most C M^(-2) delta_obs^(4/3)(1+delta_obs).
075 ||| The Decimal producer and the independent binary64 / finite-matrix certificate both pass separately. The former checks \(M^{-2}\), \(M^{6/7}\), the optimizer, the floor identity, and retention; the latter reconstructs the shift matrices, the \(Q\) row, dissipative payment, and the complex BV zero sampler.
076 ||| complete all-root squared-slope mass in the declared triangular class; launch-inclusive mixed-window floor cancellation; \(M^{-2}\) endpoint suppression under bounded coupling.
077 ||| Exact heat shear gives \(\theta_I\asymp e^{-2\nu d^2R^2A_0}\to0\). This disproves only automatic retention; it is not a complete counterexample with a nonzero target atom.
078 ||| Finite ECT, maximal regularity, and time analyticity cannot replace this section's estimate
079 ||| The pre-observation layer may contain other roots, and they are not controlled by \(\Omega=\sup_{x\ge A_0}\|V_z(x)\|\). Therefore this section does not enlarge the root set from \(I\) to \(K\).
080 ||| The quadratic extra-root escape is closed in the declared bounded-coupling triangular class
081 ||| The two specific gaps in R0.71Y close simultaneously in the same declared class
082 ||| R0.71Y controls only selected roots, leaving two interfaces: \(R\gtrsim M^2\) extra roots and a matched root-time floor. This section instead studies the complete squared-slope mass. For real shear, unit-modulus launch phases, a fixed target, and \(A_0>0\), bounded-variation sampling, exact \(\ell^2\) contraction, and the dissipative target row give \(G_{\rm all}^{\rm ex}\le C M\Omega^2(1+\delta_{\rm obs})\). Roots remain counted in the original observation interval, but the payment interval for \(\Lambda_1\) contains launch; \(\mathcal R_Y\) then replaces the rootwise denominators by \(\sup Y\). Hence the complete ratio is \(O(M^{-2})\) under bounded coupling.
083 ||| R0.71Z · 2026-08-27 · Personal mathematics research log
084 ||| R0.71Z all-root inverse-square suppression in M, strong-coupling diagnostic, and fixed-window enstrophy retention
085 ||| R0.71Z | All-root slope mass and the launch-inclusive ledger
086 ||| Raw root count is not the right object. R0.71U already shows that a finite recurrence can have arbitrarily many roots. This section instead sums each exact root's squared slope; multiple roots and accumulation-type zero roots have zero slope and contribute no atom mass.
087 ||| a raw zero-count theorem, universal endpoint, continuation criterion, finite-time singularity, global regularity, originality, or priority conclusion.
088 ||| strong coupling, \(A_0\to0\), non-unit or sparse phases, complex shear, a non-diagonal target, and different geometry.
089 ||| For unit phases, \(K_s\gtrsim M^3\) suppresses the complete ratio by \(M^{-2}\)
090 ||| 02 · Complete 90-note index
091 ||| Open latest node R0.71Z
092 ||| Recap endpoint: R0.71Z
093 ||| Public notes at recap endpoint: 150
094 ||| As of R0.71Z there is no new unconditional continuation criterion, no reduction of the full class of potential singular solutions, and no proof of finite-time breakdown. The 90 nodes cannot be interpreted as a percentage of the Millennium problem completed.
095 ||| Cumulative recap · R0.61–R0.71Z · 2026-08-27
096 ||| Seventeen phases and 90 nodes: from reduced recurrence and the post-R0.70A dynamic route through the fixed-zero ledger and the family-internal one-third endpoint, then to bounded-coupling all-root suppression.
097 ||| Nodes included: 90
098 ||| In parallel, treat the \(A_{0,M}\to0\) shrinking observation layer separately from fixed-window retention. If launch cannot enter the payment interval, \(\theta_I^{-1}\) must remain explicit; any substitute must be paid by the true dynamics or a new ledger quantity.
099 ||| The next finite task analyzes whether exact trajectories can approach the all-root upper envelope as \(\delta_{\rm obs}\) grows with carrier dimension. The current upper bound has a nonvanishing diagnostic at \(\delta_{\rm obs}\asymp M^{6/7}\), but this is not a root construction.
100 ||| Both the selected-root and all-root interfaces of the small-coupling triangular route are closed; the general problem remains open
101 ||| This closes two interfaces only in the declared model class, not a general NSE complete-atom theorem. Strong coupling, an observation layer shrinking with dimension, non-triangular feedback, sparse or non-unit phases, and different geometry remain open; fixed-window retention can also vanish exponentially.
102 ||| This page follows the R0.00–R0.60 phase recap and organizes the 90 research nodes from R0.61 through R0.71Z. It records chronologically what each segment actually proved, which proposals were ruled out by a specific counterexample or scale analysis, and which assumptions have not been derived from the Navier–Stokes equations.
103 ||| The R0.00–R0.60 material remains in the preceding phase recap. R0.60 concluded that the full Fourier–Leray structure and higher-order calculations could continue, but still did not control a critical quantity for general three-dimensional solutions. The following 90 nodes advance along that gap; every completed release from R0.70A onward remains in the route and index.
104 ||| Post-R0.60 research recap: a chronological organization of 90 research nodes from R0.61 through R0.71Z; the latest section uses BV sampling to close the all-root slope mass in the declared real-shear triangular class and removes the rootwise enstrophy floor through a launch-inclusive ledger.
105 ||| Public notes from R0.61–R0.71Z: 90 sections
106 ||| R0.61–R0.71Z recap · 2026-08-27
107 ||| R0.61–R0.71Z research nodes
108 ||| R0.61–R0.71Z | Post-R0.60 research recap
109 ||| R0.71U gives a zero-count-independent all-shell second-time-jet theorem and finite prescribed recurrence. R0.71V turns the first-row ledger into Leray–Hopf right-rooted excursion-height packing and separates the level integral from the fixed zero-level atom. R0.71W rules out the data-uniform complete first-row bound, and R0.71X completes the roots and reaches the \(D^{1/3}\) endpoint inside a fixed-dimensional small-coupling family. R0.71Y proves that the selected growing-root ratio is at most \(C\nu^{-2}\delta_{\rm obs}^{4/3}/N\) under bounded observation coupling. R0.71Z stops counting roots: a BV zero-slope lemma for complex \(W^{2,1}\) functions, exact contraction of the real-shear triangular system, and a dissipative target row directly control the squared-slope mass of all exact roots. Extending the payment interval to launch lets \(\mathcal R_Y\) remove the rootwise enstrophy floor and gives the complete ratio \(C\nu^{-2}M^{-2}\delta_{\rm obs}^{4/3}(1+\delta_{\rm obs})\). It vanishes as \(M^{-2}\) under bounded coupling; the conclusion covers only the declared triangular class.
110 ||| R0.71U–R0.71Z · second-time jet, complete first row, and the all-root boundary
111 ||| R0.71X reaches the \(D^{1/3}\) endpoint inside a fixed-dimensional small-coupling family, and R0.71Y rules out a gain from selected growing roots alone. R0.71Z further shows that, in the same real-shear triangular system, the complete squared-slope mass can be paid directly without counting roots; a launch-inclusive mixed window also removes the matched root-time floors. Under bounded coupling, the normalized complete ratio is at most \(C\nu^{-2}M^{-2}\delta_{\rm obs}^{4/3}(1+\delta_{\rm obs})\).
112 ||| R0.71Z's complete all-root closure: the zero-slope mass of a complex \(W^{2,1}\) function is controlled by the first slope and \(\|g'\|_\infty\int|g''|\). In the declared real-shear triangular system, exact contraction, target-row variation, and viscous payment give an all-root estimate independent of the root count. Once the payment interval contains launch, \(\mathcal R_Y\) replaces the rootwise denominators by one \(\sup Y\), yielding \(M^{-2}\) suppression under bounded coupling. Fixed-observation-window retention can vanish exponentially; strong coupling and a shrinking layer remain open.
113 ||| R0.71Z figure
114 ||| R0.71Z certificates
115 ||| R0.72A tests strong coupling and a shrinking observation layer
116 ||| From the family-internal one-third endpoint to complete all-root suppression
117 ||| For the declared real-shear exact triangular Fourier-lattice evolution, no uniform raw-root-count bound is attempted. A complex scalar bounded-variation zero lemma reduces the squared slopes on any finite root subset to the first slope and one total-variation term. After \(V_z'\) and \(V_z(D_q+\lambda_0)\) are combined in the target row, exact contraction and the dissipation identity give \[ \sum_{F_0(\tau)=0}|F_0'(\tau)|^2 \le e^{2\lambda_0L}(4+C_\kappa\delta_{\rm obs}) \delta_{\rm obs}^2M. \] Taking the supremum handles the complete zero set, so the constant has no root-count, minimum-gap, fill-distance, or second-spectral-moment cost.
118 ||| Roots are still counted only in the original observation interval \(I=[a,b]\), while the payment interval becomes the launch-inclusive \(K=[\sigma_q,b]\). First distribute the common \(1/\mathcal R_Y(K)\) through the atom sum, then use launch enstrophy to obtain \(\sup_KY\gtrsim q^2(S^2K_s+P^2K_v)\), eliminating the rootwise matched-background floor. For unit phases, \(K_s\gtrsim M^3\) finally gives \[ \frac{\mathcal J_{\rm all}(I)}{D^{1/3}\Lambda_1(K)} \le C\nu^{-2} \frac{\delta_{\rm obs}^{4/3}(1+\delta_{\rm obs})}{M^2}. \]
119 ||| annulus exclusion → source-core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → shared-response first-order channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation → bounded-coupling selected-root \(N^{-1}\) suppression → BV all-root slope-mass closure → launch-inclusive mixed-window floor cancellation → bounded-coupling complete-root \(M^{-2}\) suppression
120 ||| Test whether strong coupling and a shrinking observation layer can simultaneously preserve exact roots, the complete nonlinear rotational charge, and certifiable IFT / Dyson control.
121 ||| Test whether strong observation coupling and a shrinking observation layer can simultaneously preserve exact roots, the complete nonlinear rotational charge, and certifiable IFT / Dyson control.
122 ||| After the static annular families are rigorously excluded, the route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–V separates the second-time jet, Leray-paid excursion, and fixed zero-level trace. R0.71W rules out the data-independent complete first-row ledger, R0.71X reaches the \(D^{1/3}\) endpoint inside a fixed-dimensional small-coupling family, and R0.71Y proves that the selected growing-root ratio decays as \(N^{-1}\) under bounded observation coupling. R0.71Z uses bounded-variation zero sampling to control the squared-slope mass of all exact roots directly and a mixed payment window containing launch to remove the rootwise matched enstrophy floor; the complete ratio is suppressed by \(M^{-2}\) in the declared triangular class. Strong coupling and a shrinking observation layer remain open.
123 ||| Cumulative recap R0.61–R0.71Z · 2026-08-27
124 ||| There is still no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71Z proves that the complete all-root squared-slope mass is independent of the root count in the declared real-shear, unit-phase exact triangular class; a payment window containing launch also removes the rootwise matched enstrophy floor and gives the endpoint upper bound \(CM^{-2}\delta_{\rm obs}^{4/3}(1+\delta_{\rm obs})\) under bounded coupling. This is a rigorous mechanism exclusion inside a model class, not a general NSE regularity result.
125 ||| The slope mass of all roots can be paid uniformly, and a rootwise enstrophy floor is no longer needed
126 ||| Previous review v1.11 · 2026-08-26
127 ||| A systematic review places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019–2026, and this site's R0.69P–R0.71Z route in one view. The historical R0.61–R0.69O nodes remain in the cumulative recap.
128 ||| Next step R0.72A:
129 ||| Research note R0.71Z · 2026-08-27
130 ||| First test whether, as \(\delta_{\rm obs}\) approaches the \(M^{6/7}\) scale, exact roots, the full nonlinear rotational charge, and an IFT / Dyson certificate can all be retained simultaneously; treat \(A_{0,M}\to0\) as an independent boundary.
131 ||| Read research note R0.71Z →
132 ||| Expand 60 public notes
133 ||| This is a complete all-root, mixed-window floor-free upper bound inside the declared exact triangular 2.5D class. It gives no raw zero-count theorem and is not a general three-dimensional Navier–Stokes endpoint, continuation criterion, finite-time singularity, or global-regularity result; strong coupling, a shrinking observation layer, non-unit phases, and different geometry remain open.
134 ||| Review v1.12 · 2026-08-27
135 ||| Bounded-variation sampling controls the complete all-root slope mass; a launch-inclusive mixed window removes the rootwise matched floor.
136 ||| The post-R0.60 route has seventeen segments: reduced Picard analysis and the shear boundary; transverse perturbations; local pressure budgets; signed physical annuli; moving labels and source-core duality; defect tensors and finite observations; full-frame covariance; the constant-projection boundary; positive output and the material-heat tent; projected-Lamb heat volume; local heat packing and the critical-trace obstruction; and positive-entry temporal packing, conditional Jensen/incidence, packet/Bessel analysis, internal-entry scaling, the second-time jet, finite recurrence, Leray-paid excursions, the fixed-zero boundary, the complete first-row data-uniform no-go, fixed-small-coupling one-third internal saturation, bounded-coupling selected-root suppression, BV all-root slope-mass closure, and launch-inclusive mixed-window floor cancellation. R0.70A–R0.71Z contains 52 completed releases.
137 ||| The cumulative recap after the R0.60 recap contains 90 nodes; the full site now has 150 public research notes
138 ||| R0.70A–R0.71Z completed releases
139 ||| R0.71Z completed:
`;

const englishRows = translationRows
  .trim()
  .split("\n")
  .map((row, index) => {
    const expected = String(index + 1).padStart(3, "0") + " ||| ";
    if (!row.startsWith(expected)) {
      throw new Error("unexpected R0.71Z translation row " + (index + 1));
    }
    return row.slice(expected.length);
  });

const currentWithoutBatch = current.filter(
  (entry) => !/^r071z\d+$/.test(entry.id),
);
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.71Z batch");
}

const missingFileOrder = [
  "literature-review.html",
  "notes/r0-71z.html",
  "recap-r0-61-r0-71z.html",
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
  missing.length !== 139 ||
  englishRows.length !== missing.length ||
  missingHash !== "17a87e0bbdbc2e172434035fa58ae8f67ad0ccaae5f4816d296b9b4c4c0ee5ad"
) {
  throw new Error(
    "R0.71Z translation source drift: missing=" +
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
    id: "r071z" + String(index + 1).padStart(3, "0"),
    en,
  };
});

for (const relative of [
  "research-review.html",
  "literature-review.html",
  "recap-r0-61-r0-71z.html",
  "notes/r0-71z.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.12')) {
    throw new Error(relative + ": expected i18n cache version v1.12");
  }
}

for (const relative of [
  "recap-r0-61-r0-71y.html",
  "notes/r0-71y.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.11')) {
    throw new Error(relative + ": expected historical i18n cache version v1.11");
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
      missingHash,
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
