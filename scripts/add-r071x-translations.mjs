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
001 ||| 02 · Complete 88-section index
002 ||| Open latest node R0.71X
003 ||| In the multiblock extension, the energy proxy \(\varepsilon_N=P\sqrt{K_{v,N}}/q^2\) is not the exact operator IFT parameter \(\delta_{\mathrm{op},N}=(P/q^2)\sup_x\lVert V_{z,N}(x)\rVert\). Both growing \(N\) and strong coupling remain open; atomProxy in the numerical figure is also not the multiplier-locked \(J_*\), and \(\delta=1/128\) has not been quantified as a continuum IFT radius.
004 ||| Recap endpoint: R0.71X
005 ||| Public notes at recap endpoint: 148
006 ||| As of R0.71X there is no new unconditional continuation criterion, no reduction of the full class of potential singular solutions, and no proof of finite-time breakdown. The 88 nodes cannot be interpreted as a percentage of the Millennium problem completed.
007 ||| Cumulative recap · R0.61–R0.71X · 2026-08-26
008 ||| The declared triangular family has reached its internal one-third boundary
009 ||| Seventeen phases and 88 nodes: from reduced recurrence to the fixed-zero ledger and then endpoint saturation at the one-third power of D within a fixed-small-coupling triangular family; growing dimension and general regularity remain open.
010 ||| Nodes included: 88
011 ||| The next finite task makes the growth of ECT root separation, the uniform IFT radius, and the operator norm with block number explicit and checkable; it also establishes a weighted slope-energy / observability gate to test whether the complete atom sum can be paid by data of the same scale.
012 ||| This page follows the R0.00–R0.60 phase recap and organizes the 88 research nodes from R0.61 through R0.71X. It records chronologically what each segment actually proved, which proposals were ruled out by a specific counterexample or scale analysis, and which assumptions have not been derived from the Navier–Stokes equations.
013 ||| The R0.00–R0.60 material remains in the preceding phase recap. R0.60 concluded that the full Fourier–Leray structure and higher-order calculations could continue, but still did not control a critical quantity for general three-dimensional solutions. The following 88 nodes advance along that gap.
014 ||| Post-R0.60 research recap: a chronological organization of 88 research nodes from R0.61 through R0.71X; the latest section completes the prescribed real roots and precisely saturates the one-third power of D within a fixed-small-coupling triangular family, while preserving the boundaries around the general problem and growing dimension.
015 ||| Public notes from R0.61–R0.71X: 88 sections
016 ||| R0.61–R0.71X recap · 2026-08-26
017 ||| R0.61–R0.71X research nodes
018 ||| R0.61–R0.71X | Post-R0.60 research recap
019 ||| R0.70A–R0.71X completed releases
020 ||| R0.71U gives a zero-count-independent all-shell second-time-jet theorem and finite prescribed recurrence. R0.71V turns the first-row ledger into Leray–Hopf right-rooted excursion-height packing and separates the level integral from the fixed zero-level atom. R0.71W uses amplitude doping to rule out a data-uniform first-row bound with a fixed \(\nu^2\) baseline and complete projected rotational charge, while leaving the \(D^{1/3}\) endpoint open. R0.71X fixes sufficiently small \(\delta\) and takes \(A=\delta q^2\) inside the uniform IFT neighborhood: ECT zero counting, compact \(C^1\) separation, and a half-line integrating factor together prove that the only real-time target roots are the two declared simple roots. The family satisfies \(D\asymp\delta^2q^6\), complete \(\mathcal J\asymp\delta^2q^2\), and \(\nu^2\le\Lambda_1\le C(\nu^2+\delta^2)\), so \(\mathcal J/(D^{1/3}\Lambda_1)\asymp\delta^{4/3}\). For fixed \(\delta\), the ratio diverges for \(\beta<1/3\), saturates for \(\beta=1/3\), and decays for \(\beta>1/3\).
021 ||| R0.71U–R0.71X · second-time jet, complete first row, and the one-third boundary
022 ||| R0.71W rules out the data-uniform complete first-row bound. R0.71X completes all real-time roots inside the uniform IFT neighborhood for fixed sufficiently small \(\delta\), and puts the complete atom, data size, and first-row payment on the same scale, producing a finite nonzero ratio at \(D^{1/3}\). This is internal saturation for a fixed-dimensional declared triangular family, not a universal endpoint for a general initial-data class.
023 ||| R0.71X figure
024 ||| With fixed sufficiently small \(\delta\) and \(A=\delta q^2\) inside the uniform IFT neighborhood, R0.71X uses ECT, compact \(C^1\) separation, and a half-line integrating factor to complete the real-time target-root ledger. It also proves \(D\asymp\delta^2q^6\), complete \(\mathcal J\asymp\delta^2q^2\), \(\nu^2\le\Lambda_1\le C(\nu^2+\delta^2)\), and \(\mathcal J/(D^{1/3}\Lambda_1)\asymp\delta^{4/3}\). This is internal saturation in the declared fixed-dimensional triangular family, not a universal endpoint or regularity theorem.
025 ||| R0.71X certificates
026 ||| R0.71Y quantifies growing-dimensional ECT/IFT and the weighted observability gate
027 ||| The strong-coupling Bessel route is retained as a later candidate and is not mixed into R0.71Y. A positive estimate must state the growing-dimensional constants explicitly; a negative conclusion must retain the exact operator parameter and complete-atom convention.
028 ||| From the complete first-row no-go to the family-internal one-third endpoint
029 ||| Fixed sufficiently small coupling, the complete root set, and declared-family internal saturation of \(D^{1/3}\Lambda_1\) are closed.
030 ||| Fix sufficiently small \(0<\delta\le\delta_*\) and take \(\mathscr A_{q,\delta}=\delta q^2\). The uniform IFT branch persists. The ECT zero budget, compact \(C^1\) separation, and a half-line integrating factor together prove that the positive target roots in the declared interval are exactly the prescribed \(N\) simple roots.
031 ||| Fixed small coupling reaches the one-third endpoint within the declared triangular family
032 ||| annulus exclusion → source-core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → shared-response first-order channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment–projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go → fixed-small-coupling one-third internal saturation
033 ||| After the static annular families are rigorously excluded, the route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71U–V separates the second-time jet, Leray-paid excursion, and fixed zero-level trace. R0.71W rules out the data-independent complete first-row ledger. R0.71X then fixes sufficiently small \(\delta\), completes all real-time target roots, and proves that the complete atom sum saturates \(D^{1/3}\Lambda_1\) within the declared exact triangular family; the general endpoint, growing dimension, and strong coupling remain open.
034 ||| Cumulative recap R0.61–R0.71X · 2026-08-26
035 ||| Quantify the growing-dimensional ECT / IFT constants and test whether weighted slope-energy and complete-atom observability close at the same scale.
036 ||| Quantify growing-dimensional ECT / IFT and test the weighted slope-energy / observability gate.
037 ||| Quantify root separation, the operator IFT radius, and weighted slope-energy / observability; retain strong-coupling Bessel as a later candidate.
038 ||| There is still no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71X proves complete roots inside the uniform IFT branch for fixed sufficiently small \(\delta\), and obtains \(D\asymp\delta^2q^6\), complete \(\mathcal J\asymp\delta^2q^2\), and \(\mathcal J/(D^{1/3}\Lambda_1)\asymp\delta^{4/3}\). This is only internal saturation within the declared fixed-dimensional triangular family.
039 ||| Previous review v1.09 · 2026-08-26
040 ||| The complete scales are \[ D_{q,\delta}\asymp\delta^2q^6,\qquad \mathcal J_{q,\delta}\asymp\delta^2q^2,\qquad \nu^2\le\Lambda_1\le C(\nu^2+\delta^2), \] so \(\mathcal J/(D^{1/3}\Lambda_1)\asymp\delta^{4/3}\). For fixed \(\delta\), the ratio diverges for \(\beta<1/3\), saturates for \(\beta=1/3\), and decays for \(\beta>1/3\).
041 ||| A systematic review places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019–2026, and this site's R0.69P–R0.71X route in one view. The historical R0.61–R0.69O nodes remain in the cumulative recap.
042 ||| Next step R0.71Y:
043 ||| Research note R0.71X · 2026-08-26
044 ||| Read research note R0.71X →
045 ||| Expand 58 public notes
046 ||| This is fixed-dimensional declared triangular family internal saturation, not a universal endpoint, bounded-data continuation, finite-time singularity, or global-regularity conclusion. The multiblock energy proxy is not the exact operator IFT parameter; growing \(N\) and strong coupling remain open.
047 ||| Review v1.10 · 2026-08-26
048 ||| The post-R0.60 route has seventeen segments: reduced Picard analysis and the shear boundary; transverse perturbations; local pressure budgets; signed physical annuli; moving labels and source-core duality; defect tensors and finite observations; full-frame covariance; the constant-projection boundary; positive output and the material-heat tent; projected-Lamb heat volume; local heat packing and the critical-trace obstruction; and positive-entry temporal packing, conditional Jensen/incidence, packet/Bessel analysis, internal-entry scaling, the second-time jet, finite recurrence, Leray-paid excursions, the fixed-zero boundary, the complete first-row data-uniform no-go, and fixed-small-coupling one-third internal saturation. R0.70A–R0.71X contains 50 completed releases.
049 ||| The cumulative recap after the R0.60 recap contains 88 nodes; the full site now has 148 public research notes
050 ||| R0.71X completed:
051 ||| treats time analyticity. The bounded primary-source search located no directly coincident fixed temporal zero-slope complete atom theorem; this is bounded non-collision, not a claim of originality, priority, or nonexistence.
052 ||| treat spatial level / trace,
053 ||| Open the complete 88-section index
054 ||| 's one-third exponent concerns time integrability of higher spatial derivatives.
055 ||| give projected-Lamb identities;
056 ||| give a whole-space cubic enstrophy ODE and small-data threshold;
057 ||| Open interface · R0.71Y
058 ||| cumulative recap and 88-section index
059 ||| Quantify ECT / IFT constants and weighted slope-energy / observability; retain strong-coupling Bessel as a later candidate.
060 ||| Literature review v1.10 · 2026-08-26
061 ||| Published theorems are listed as known results, 2026 preprints are marked separately, and this site's R0.69P–R0.71X material is classified only as research notes. Calculations and notes are not extrapolated into regularity theorems.
062 ||| study extreme enstrophy growth;
063 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U gives the conditional-incidence, genuine-internal-entry, second-time-jet, and finite-recurrence boundaries. R0.71V–W separates the fixed zero-level trace and rules out the data-uniform complete first-row ledger. R0.71X completes the roots at fixed sufficiently small coupling and obtains one-third saturation within the declared triangular family. Growing dimension and general regularity remain open.
064 ||| Primary-source boundary for R0.71X
065 ||| R0.71X fixes sufficiently small \(\delta\) and takes \(A=\delta q^2\) inside the R0.71W uniform IFT neighborhood. The ECT multiplicity bound, compact \(C^1\) separation, and a half-line integrating factor give complete real-time target roots; the exact scales give \(\mathcal J/(D^{1/3}\Lambda_1)\asymp\delta^{4/3}\). This is fixed-dimensional declared triangular family internal saturation, not a universal endpoint or regularity theorem. The multiblock energy proxy \(\varepsilon_N\) is not the exact \(\delta_{\mathrm{op},N}\). R0.71Y quantifies only growing-dimensional ECT / IFT and the weighted observability gate. The six filters below remain unchanged.
066 ||| What R0.71X closes and what R0.71Y alone tests
067 ||| Take \(A=\delta q^2\) inside the uniform IFT. ECT, compact \(C^1\), and a half-line integrating factor give complete roots; \(D\asymp\delta^2q^6\), complete \(\mathcal J\asymp\delta^2q^2\), and \(\nu^2\le\Lambda_1\le C(\nu^2+\delta^2)\).
068 ||| The ratio diverges for \(\beta<1/3\), stays of constant order for \(\beta=1/3\), and is absorbed for \(\beta>1/3\). This trichotomy resolves only the data-power sensitivity of this family; it does not prove that \(D^{1/3}\Lambda_1\) pays for an arbitrary solution.
069 ||| \(\Lambda_1\) retains both the viscous baseline and the full-frequency rotational charge
070 ||| 01 · Endpoint theorem
071 ||| 02 · Fixed small coupling
072 ||| 03 · Complete root set
073 ||| 04 · Exact scales
074 ||| 05 · Complete ledger
075 ||| 06 · Exponent trichotomy
076 ||| 07 · Multiblock boundary
077 ||| 08 · Three audits
078 ||| The 9/9, 8/8, and 10/10 checks verify finite algebraic and numerical layers; the analytic proof still carries the continuum theorem.
079 ||| The 90-digit Decimal producer passes 9/9, the independent binary64 reconstruction passes 8/8, and the nonlinear retained-coset calculation passes 10/10. The last check verifies root residuals, the powers of \(q\), the \(\delta^{4/3}\) collapse, truncation stability, and the finite tail sign.
080 ||| Version v0.71X · 2026-08-26
081 ||| The report, literature, certificates, and formal figure package are all preserved
082 ||| This section returns to the exact triangular 2.5D invariant class of R0.71W, fixes the rescaled coupling at sufficiently small \(\delta>0\), and takes \(\mathscr A_{q,\delta}=\delta q^2\). The uniform IFT remains applicable. The complete real-time target root set consists exactly of the prescribed \(N\) simple roots, the complete atom sum satisfies \(\mathcal J_{q,\delta}\asymp\delta^2q^2\), and the initial-data quantity satisfies \(D_{q,\delta}\asymp\delta^2q^6\). Thus the family saturates the \(D^{1/3}\Lambda_1\) scale but does not provide a universal endpoint estimate.
083 ||| is not the multiplier-locked \(J_*\). The numerical choice \(\delta=1/128\) has also not been proved to lie inside a quantified continuum IFT radius; the analytic theorem states only that a sufficiently small \(\delta_*\) exists.
084 ||| treat spatial level/trace;
085 ||| There exist \(0<\delta_*<\delta_0\) and \(q_0\) such that every \(0<\delta\le\delta_*\) and all sufficiently large admissible \(q\) produce an exact triangular NSE solution that is smooth, unforced, and global forward from the launch time, and
086 ||| 's \(H_2^{1/3}\in L_t^1\) is a time-integrability exponent for higher spatial derivatives, not the initial-data power in this section.
087 ||| The three behaviors below, at, and above \(1/3\) separate completely
088 ||| The endpoint is attained within an exact smooth family, but the general payment problem remains fully open
089 ||| For every fixed \(0<\delta\le\delta_*\),
090 ||| Multiblock
091 ||| The multiblock audit distinguishes the energy proxy from the true multiplication-operator parameter in the IFT:
092 ||| Multiblock and open-route matrix
093 ||| Figure, data, manifest, validation, and source-code package
094 ||| The figure separates the powers of \(q\), the endpoint plateau, and the \(\delta^{4/3}\) collapse
095 ||| This family satisfies \(1\le\mathcal R_Y\le C\), and the complete rotational term is at most \(C\delta^2\). Thus \(\Lambda_1\) retains the fixed \(\nu^2\) term and does not replace the full-frequency charge with a selected-shell proxy.
096 ||| give projected Lamb identities;
097 ||| gives time analyticity but no theorem paying the fixed temporal zero-slope sum with \(D\). The bounded primary-source search located no direct coincidence; this is not a claim of originality, priority, or nonexistence.
098 ||| give a whole-space cubic enstrophy ODE, explicit lifespan, and small-data threshold;
099 ||| Root set
100 ||| After \(\delta\) is fixed, the complete atom sum retains a nondegenerate endpoint coefficient
101 ||| For fixed \(N\), the selected-root route is still limited by collective coupling. Growing \(N(q)\) requires a quantitative ECT inverse, a uniform IFT radius, weighted slope-energy, and complete observability; the strong-coupling Bessel route also remains only a later candidate.
102 ||| Summing over fixed \(N\) does not change the powers. The endpoint coefficient can also be written as three normalized factors with uniform upper and lower bounds, multiplied by \(\delta^{4/3}\), so this is more than formal power counting.
103 ||| fixed sufficiently small \(\delta\) on the declared uniform-IFT branch; the prescribed roots form the complete real-time target zero set; two-sided scales for \(D\), \(\mathcal J\), and \(\Lambda_1\); family-internal \(D^{1/3}\Lambda_1\) saturation and the \(\beta\) trichotomy.
104 ||| Fixed sufficiently small coupling reaches the one-third scale,
105 ||| On each fixed compact interval, \(\|H_{q,\delta}-\Gamma\|_{C^1}\le\varepsilon_q+C\delta\). The derivative sign persists in root neighborhoods, while the real part remains separated from zero on the complement. On the half-line, an integrating factor is applied to \(e^{\lambda_qx}H_{q,\delta}\); the interaction kernel is integrable with no \(\lambda_q^{-1}\) loss, and its limit approaches the nonzero \(\Gamma_\infty\). Therefore the real-time target roots in the declared interval are exactly the prescribed \(N\) roots.
106 ||| Fixed-dimensional small-coupling analysis produces no gain beyond the endpoint
107 ||| The limiting target \(\Gamma\) is a constant plus \(N+1\) distinct decaying exponentials. A generalized Rolle induction proves that such a nonzero exponential polynomial has at most \(N+1\) real roots counted with multiplicity. The known roots \(0,\tau_1,\ldots,\tau_N\) exhaust the budget, so all are simple and \(\Gamma_\infty\ne0\).
108 ||| a continuation criterion, bounded-data no-go, finite-time singularity, or global regularity.
109 ||| The conclusion belongs only to the declared triangular family
110 ||| The analytic proof and three finite computations carry different responsibilities
111 ||| Not obtained:
112 ||| Still open:
113 ||| It does not turn the general singularity problem into a conclusion. The next informative threshold is whether growing-dimensional roots or stronger coupling can change this boundary after paying the exact operator norm and complete slope energy.
114 ||| Figure R0.71X-1. Finite retained-coset data show \(D\) scaling approximately as \(q^6\) and the complete two-root atomProxy approximately as \(q^2\); an independent high-precision ledger shows the plateau of atomProxy divided by \(D^{1/3}\) and its \(\delta^{4/3}\) collapse. atomProxy is not \(J_*\), \(\delta=1/128\) is not a certified continuum IFT radius, and the figure is reproducible corroboration only.
115 ||| In the figure and retained-coset JSON,
116 ||| The complete prescribed-root atom sum reaches the D^(1/3) Lambda1 scale; root completeness is proved by ECT, compact-interval C1 separation, and a half-line integrating factor.
117 ||| The one-third powers, spatial traces, and time analyticity in the literature do not directly provide the ledger in this section
118 ||| The physical amplitude is of order \(q^2\), while the small quantity remains the fixed rescaled coupling
119 ||| Next object: growing-dimensional ECT / IFT
120 ||| The next section first quantifies the exponential-Chebyshev inverse, coefficient curve, and IFT radius as \(N\) grows, and then places weighted slope-energy and full-charge observability in the same ledger. Only if all of these quantities close together can \(\varepsilon_N^{4/3}\mathcal Q_N\) be interpreted.
121 ||| Research note R0.71X · FIXED SMALL COUPLING · ONE-THIRD ENDPOINT
122 ||| Research note R0.71X: an exact triangular 2.5D family with fixed sufficiently small coupling reaches the one-third power of D over the complete real-time root set; this is family-internal endpoint saturation, not a universal estimate or regularity theorem.
123 ||| The implicit constants may depend on the fixed geometry, viscosity, observation interval, and \(\delta_*\), but not on \(q\) and \(\delta\) within the declared range.
124 ||| On the Fourier lattice with \(x=q^2(t-\sigma_q)\), the evolution becomes
125 ||| This is not a solution of the three-dimensional Navier–Stokes global-regularity problem, nor an upper bound by \(D^{1/3}\) for all triangular solutions.
126 ||| Exponent
127 ||| Status · R0.71X completed
128 ||| The ECT zero budget, compact-interval separation, and half-line tail jointly exclude additional roots
129 ||| exact / independent / retained-coset certificates
130 ||| growing-dimensional ECT/IFT, weighted slope-energy/observability, strong coupling, all triangular solutions, or a universal endpoint estimate for general three-dimensional solutions.
131 ||| Parseval, root slopes, and enstrophy give two independent powers of \(q\)
132 ||| The persistent background gives two-sided bounds for \(D\) and \(Y\), while exact multiplier normalization at the roots gives
133 ||| The uniform IFT of R0.71W allows fixed sufficiently small \(\delta\); it does not require \(\delta_q\to0\). After taking \(\mathscr A_{q,\delta}=\delta q^2\), the complete atom sum and \(D^{1/3}\Lambda_1\) have the same order. This is an internal saturation theorem for a fixed-dimensional local-IFT triangular family.
134 ||| The subcritical family from R0.71W can be advanced to an exact family-internal endpoint
135 ||| R0.71W already gives a local IFT radius uniform in \(q\). Whenever \(0<\delta\le\delta_*\) is fixed and \(\delta_*\) is sufficiently small, the coefficient curve \(z_q(\delta)\) and simple-slope lower bound persist. The coefficient-one value \(\delta=1\) is not forced into the local branch.
136 ||| R0.71W approaches \(1/3\) only from below. This section proves that a fixed sufficiently small prefactor already lies on the same uniform IFT branch and completes the real-time root set. Thus \(1/3\) is no longer only an extrapolated exponent, but a saturation law with a nondegenerate coefficient in the declared family.
137 ||| R0.71X · 2026-08-26 · Personal mathematics research log
138 ||| R0.71X fixed-small-coupling endpoint scales, one-third plateau, and delta-to-the-four-thirds collapse
139 ||| R0.71X | Fixed small coupling and the one-third endpoint
140 ||| R0.71Y tests growing-dimensional ECT / IFT and weighted observability
141 ||| The strong-coupling Bessel/enhanced-dissipation construction is retained as a later candidate and is not treated in advance as an established mechanism for R0.71Y.
`;

const englishRows = translationRows
  .trim()
  .split("\n")
  .map((row, index) => {
    const expected = String(index + 1).padStart(3, "0") + " ||| ";
    if (!row.startsWith(expected)) {
      throw new Error("unexpected R0.71X translation row " + (index + 1));
    }
    return row.slice(expected.length);
  });

const currentWithoutBatch = current.filter((entry) => !/^r071x\d+$/.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.71X batch");
}

const missingPriority = [
  "recap-r0-61-r0-71x.html",
  "research-review.html",
  "literature-review.html",
  "notes/r0-71x.html",
];
function priority(entry) {
  const value = missingPriority.findIndex((file) => entry.files.includes(file));
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
  missing.length !== 141 ||
  englishRows.length !== missing.length ||
  missingHash !== "c9bb591961261d4fea029621bc895191f92eb5bccdbbbf20da4e17dc08cba89d"
) {
  throw new Error(
    "R0.71X translation source drift: missing=" +
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
    id: "r071x" + String(index + 1).padStart(3, "0"),
    en,
  };
});

for (const relative of [
  "research-review.html",
  "literature-review.html",
  "recap-r0-61-r0-71x.html",
  "notes/r0-71x.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.10')) {
    throw new Error(relative + ": expected i18n cache version v1.10");
  }
}
for (const relative of [
  "recap-r0-61-r0-71w.html",
  "notes/r0-71w.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.09')) {
    throw new Error(relative + ": expected historical i18n cache version v1.09");
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
