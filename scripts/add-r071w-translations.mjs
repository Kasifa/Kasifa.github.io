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
001 ||| 02 · Complete 87-section index
002 ||| The boundary is equally clear: the initial energy/enstrophy \(D_q\asymp q^{2\alpha+2}\) of the construction is unbounded. For every fixed \(\beta<1/3\), it rules out the \(D^\beta\) prefactor, but not \(D^{1/3}\), stronger data dependence, a persistence condition, a time-regularity charge, or a different observable.
003 ||| Open latest node R0.71W
004 ||| Recap endpoint: R0.71W
005 ||| Public notes at recap endpoint: 147
006 ||| As of R0.71W there is no new unconditional continuation criterion, no reduction of the full class of potential singular solutions, and no proof of finite-time breakdown. The 87 nodes cannot be interpreted as a percentage of the Millennium problem completed.
007 ||| Cumulative recap · R0.61–R0.71W · 2026-08-26
008 ||| Seventeen phases and 87 nodes: from reduced recurrence to conditional incidence, the second-time jet, Leray-paid excursions, and finally an amplitude-doped exact 2.5D data-uniform complete first-row no-go; initial-data dependence remains open.
009 ||| Nodes included: 87
010 ||| The data-uniform complete first-row route is closed; data-dependent payment is the next boundary
011 ||| The next finite task compares exact atom scaling and data-dependent energy/enstrophy payments on the same scale, to determine whether \(1/3\) is a feature of the triangular amplitude-doping family or a more general structural boundary.
012 ||| This page follows the R0.00–R0.60 phase recap and organizes the 87 research nodes from R0.61 through R0.71W. I record chronologically what each segment actually proved, which proposals were ruled out by a specific counterexample or scale analysis, and which assumptions have not been derived from the Navier–Stokes equations.
013 ||| A positive estimate must specify a bounded-data class or data prefactor; a negative conclusion must use the same data convention. R0.71X still claims no continuation, singularity exclusion, or global regularity.
014 ||| The R0.00–R0.60 material remains in the preceding phase recap. R0.60 concluded that the full Fourier–Leray structure and higher-order calculations could continue, but still did not control a critical quantity for general three-dimensional solutions. The following 87 nodes advance along that gap.
015 ||| Post-R0.60 research recap: a chronological organization of 87 research nodes from R0.61 through R0.71W, recording the full route from reduced recurrence, projected-Lamb heat volume, and temporal packing to Leray-paid excursions, the fixed-zero boundary, and the data-uniform complete first-row no-go.
016 ||| Public notes from R0.61–R0.71W: 87 sections
017 ||| R0.61–R0.71W recap · 2026-08-26
018 ||| R0.61–R0.71W research nodes
019 ||| R0.61–R0.71W | Post-R0.60 research recap
020 ||| R0.70A–R0.71W completed releases
021 ||| R0.71U gives a zero-count-independent all-shell second-time-jet theorem and finite prescribed recurrence. R0.71V turns the first-row ledger into Leray–Hopf right-rooted excursion-height packing and separates the level integral from the fixed zero-level atom. R0.71W takes \(\mathscr A_q=q^\alpha\), \(1<\alpha<2\), uses a uniform rescaled IFT to retain the prescribed \(m=2\) simple root, and proves \(J_{*,2,q}\asymp\mathscr A_q^2/q^2\to\infty\), \(\mathcal R_Y=O(1)\), and a normalized full projected rotational charge \(O(\mathscr A_q^2/q^4)\to0\). Hence the complete first-row ledger with the fixed \(\nu^2\) baseline also has no data-independent bound. The initial data size \(D_q\asymp\mathscr A_q^2q^2\) is unbounded, so the \(D^{1/3}\) endpoint and general data-dependent estimates remain open.
022 ||| R0.71U–R0.71W · second-time jet, fixed-zero boundary, and complete first-row no-go
023 ||| R0.71U–V first separates the root atom, second-time tax, Leray-paid excursion, and fixed zero-level trace. R0.71W then retains the fixed \(\nu^2\) baseline, enstrophy ratio, and complete projected rotational charge, yet the prescribed \(m=2\) atom still diverges relative to the complete first-row ledger. This is a data-uniform no-go, not a selected-shell omission or an abstract path test.
024 ||| R0.71W provides an amplitude-doped exact triangular 2.5D sequence, a uniform rescaled Fourier-lattice IFT, the prescribed \(m=2\) exact simple root, \(Y_q\asymp\mathscr A_q^2q^2\), a full-frequency projected rotational charge bound, and a data-uniform complete first-row no-go. The initial data size is unbounded; it rules out only \(D^\beta\) with \(\beta<1/3\), not \(D^{1/3}\) or stronger data dependence.
025 ||| R0.71W figure
026 ||| R0.71W certificates
027 ||| R0.71X tests the \(D^{1/3}\) endpoint and a scale-compatible charge
028 ||| Compare the amplitude-doped fixed-zero atom with a data-dependent energy/enstrophy charge and test whether the \(D^{1/3}\) endpoint can pay.
029 ||| Compare exact atom scaling with \(D^{1/3}\) or a stronger scale-compatible energy/enstrophy payment.
030 ||| View independent audit
031 ||| View three audit certificates
032 ||| The initial data size \(D_q\asymp\mathscr A_q^2q^2=q^{2\alpha+2}\) is unbounded. For every fixed \(\beta<1/3\), this family rules out the \(D^\beta\) prefactor, but not \(D^{1/3}\), stronger data dependence, or a different charge.
033 ||| From the signed-annulus obstruction to a complete first-row data-uniform no-go
034 ||| annulus exclusion → source-core ledger → covariance spectral stratification → all-frequency conditional bridge → response-slope chord gain → shared-response first-order channel → constant-projection sign obstruction → unweighted scale-packing obstruction → signed positive-output coefficient → nonnegative refinement defect → viscous sign creation → material-heat tent critical obstruction → projected-Lamb heat-volume closure → local heat packing → critical bottom trace → sign-only residence counterexample → relative superlevel set → projective heat curvature → soft denominator faces → two-power gap → joint one-sided creation → zero-entry 2D3C volume gap → all-shell positive defect → broad-parent full-frame gap → fixed matched-cell heat gap → exact viscous fusion → increment-projective bridge → signed second-jet boundary → soft-denominator face boundary → spatial entry batching → temporal-packing boundary → complex-time anchor / truncation / cover boundary → parabolic-incidence rho=0 / rho=2 boundary → signed-packet scale / Bessel boundary → genuine internal-entry scaling no-go → outgoing occupation boundary → classical second-time-jet packing → exact finite recurrence → Leray-paid excursion → fixed-zero selected-singleton first-row obstruction → amplitude-doped complete first-row data-uniform no-go
035 ||| Test the \(D^{1/3}\) endpoint and a scale-compatible energy/enstrophy charge.
036 ||| After the static annular families are rigorously excluded, the route turns to covariance-rank stratification and the all-frequency projection bridge. R0.71A–T establishes projected-Lamb heat volume, localization, and the temporal-packing boundary. R0.71U–V separates the second-time jet, Leray-paid excursion, and fixed zero-level trace. The amplitude-doped exact triangular 2.5D sequence in R0.71W retains the complete \(\nu^2\) baseline, enstrophy ratio, and projected rotational charge, yet still rules out a data-independent complete first-row ledger; initial-data dependence remains open.
037 ||| Cumulative recap R0.61–R0.71W · 2026-08-26
038 ||| There is still no new unconditional continuation criterion and no construction of a finite-time singularity. R0.71W rules out a data-independent complete first-row ledger: the prescribed \(m=2\) atom diverges, the enstrophy ratio is bounded, and the normalized full rotational charge vanishes. Initial energy/enstrophy is unbounded, so \(D^{1/3}\) and general data-dependent estimates remain open.
039 ||| Previous review v1.08 · 2026-08-26
040 ||| I also prepared a systematic review that places classical theory, five main literature strands, the candidate-blowup exclusion tree, progress from 2019—2026, and this site's R0.69P–R0.71W route in one view. The historical R0.61–R0.69O nodes remain in the cumulative recap.
041 ||| Next step R0.71X:
042 ||| Research note R0.71W · 2026-08-26
043 ||| Read research note R0.71W →
044 ||| In the exact triangular 2.5D class, take \[ \mathscr A_q=q^\alpha,\qquad 1<\alpha<2,\qquad \delta_q=\mathscr A_q/q^2\to0. \] The uniform rescaled IFT retains the fixed target, fixed macroscopic time window, and prescribed \(m=2\) simple root. The target coefficient of filtered \(C_{*,t}\) differs from \(a_t\) only by fixed nonzero factors.
045 ||| Expand 57 public notes
046 ||| This is a data-uniform route-pruning theorem, not a bounded-data no-go, continuation, finite-time singularity, or global-regularity conclusion; the finite truncated-coset calculation is corroboration only.
047 ||| Review v1.09 · 2026-08-26
048 ||| Amplitude doping rules out the data-uniform complete first-row ledger
049 ||| Amplitude doping rules out the data-uniform first-row ledger with the complete \(\nu^2\) baseline and projected rotational charge.
050 ||| Full nonlinear estimates give \[ J_{*,2,q}\asymp\mathscr A_q^2/q^2\to\infty,\qquad \mathcal R_{Y_q}=O(1),\qquad \ell^{-1}\!\int_I\frac{\|\mathbb P(u_q\times\omega_q)\|_{\dot H^{-1}}^2}{Y_q}\,dt =O(\mathscr A_q^2/q^4)\to0. \] Hence the complete first-row ledger with the fixed \(\nu^2\) baseline also has no data-independent bound.
051 ||| The post-R0.60 route has seventeen segments: reduced Picard analysis and the shear boundary; transverse perturbations; local pressure budgets; signed physical annuli; moving labels and source-core duality; defect tensors and finite observations; full-frame covariance; the constant-projection boundary; positive output and the material-heat tent; projected-Lamb heat volume; local heat packing and the critical-trace obstruction; and positive-entry temporal packing, conditional Jensen/incidence, packet/Bessel analysis, internal-entry scaling, the second-time jet, finite recurrence, Leray-paid excursions, the fixed-zero boundary, and the complete first-row data-uniform no-go. R0.70A–R0.71W contains 49 completed releases.
052 ||| The cumulative recap after the R0.60 recap contains 87 nodes; the full site now has 147 public research notes
053 ||| R0.71W completed:
054 ||| Compare exact atom scaling with \(D^{1/3}\) or a stronger scale-compatible payment.
055 ||| Open the complete 87-section index
056 ||| give the Chebyshev-system interpolation background. The uniform rescaled IFT and complete rotational estimate are proved directly here. The bounded audit located no data-uniform fixed-zero complete first-row theorem; this is not a claim of originality, priority, or nonexistence.
057 ||| Open interface · R0.71X
058 ||| cumulative recap and 87-section index
059 ||| Literature review v1.09 · 2026-08-26
060 ||| I list published theorems as known results, mark 2026 preprints separately, and classify this site's R0.69P–R0.71W material only as research notes. I do not extrapolate calculations or notes into regularity theorems.
061 ||| support the weak-energy and semigroup framework;
062 ||| . R0.69P–R0.71P reaches the positive-entry temporal-packing boundary; R0.71Q–U gives the conditional-incidence, genuine-internal-entry, second-time-jet, and finite-recurrence boundaries. R0.71V separates the Leray-paid excursion from the fixed zero-level trace. The amplitude-doped exact 2.5D sequence in R0.71W further rules out a data-independent complete first-row ledger; initial-data dependence remains open. None of the retained results is a global-regularity conclusion.
063 ||| An amplitude-doped exact triangular 2.5D sequence satisfies \(J_{*,2,q}\to\infty\) and \(\mathcal R_Y=O(1)\), while the normalized full projected rotational charge tends to zero. The initial data size is unbounded.
064 ||| Compact-shell AC representatives and weighted Cauchy–Schwarz give right-rooted scale-zero excursion packing; the area formula, sine test, and fixed-target genuine 2.5D sequence rule out selected-first-row fixed-zero sampling.
065 ||| The data-uniform complete first-row ledger fails
066 ||| R0.71W retains the fixed target, fixed macroscopic window, enstrophy ratio, \(\nu^2\) baseline, and complete projected rotational charge. An amplitude-doped exact triangular 2.5D sequence still makes the prescribed \(m=2\) atom diverge relative to the complete first-row ledger, so the data-uniform estimate fails. The initial energy/enstrophy is unbounded; the construction rules out only \(D^\beta\) with \(\beta<1/3\), not \(D^{1/3}\), stronger data dependence, or a structurally different payment. R0.71X tests only the data-dependent one-third boundary. I continue to use the six filters below.
067 ||| Primary-source boundary for R0.71W
068 ||| What R0.71W closes and what R0.71X alone tests
069 ||| \(D_q\) is self-adjoint and dissipative on a common weighted \(\ell^2\) domain, while \(V_z(x)\) is uniformly bounded and strongly continuous. The Dyson expansion retaining every intervening semigroup has a factorial majorant; uniform \(C^2\) control of the divided target map and two Chebyshev blocks give a quantitative implicit-function theorem. This yields bounded parameters \(z_q(\delta_q)\), the prescribed exact roots, and a uniform simple-slope lower bound.
070 ||| \(f_z\) still satisfies advection-diffusion; \(f_y\) only gains the \(v_yf_z\) source. A direct energy estimate gives
071 ||| 01 · Complete ledger
072 ||| 02 · Exact 2.5D class
073 ||| 03 · Amplitude doping
074 ||| 04 · Uniform IFT
075 ||| 05 · Root slope and atom
076 ||| 07 · Rotational term
077 ||| 08 · No-go theorem
078 ||| 09 · Data dependence
079 ||| 11 · Computational audit
080 ||| 12 · Journal figure
081 ||| 2.5D class
082 ||| Version v0.71W · 2026-08-26
083 ||| The report, literature audit, three computational audits, and journal figure package are all preserved
084 ||| This section constructs an amplitude-doped smooth unforced NSE sequence in the exact triangular 2.5D invariant class. The fixed target, fixed macroscopic time window, and prescribed \(m=2\) root remain unchanged; the fixed-shell atom diverges, the enstrophy ratio is bounded, and the complete projected rotational charge tends to zero. Thus even the complete first-row ledger with the fixed \(\nu^2\) baseline cannot control every smooth solution with a data-independent constant. The price is unbounded initial energy/enstrophy.
085 ||| The initial energy/enstrophy of this sequence is unbounded, so the result cannot be extrapolated into a bounded-data no-go.
086 ||| Standard sources support weak energy, 2D3C, and semigroup tools, not the fixed zero-level estimate in this section
087 ||| No uniform constant depending only on the fixed geometry, viscosity, and interval exists
088 ||| Initial-data dependence remains an open boundary
089 ||| The price is initial energy/enstrophy growing as \(q^{2\alpha+2}\)
090 ||| For every \(1<\alpha<2\), there is an exact smooth global unforced 3D NSE sequence for which the prescribed \(m=2\) fixed-shell atom diverges relative to the complete first-row Leray ledger. The conclusion rules out only a data-independent constant; it does not rule out sufficiently strong initial-data dependence.
091 ||| The figure compares the atom, complete-ledger proxy, and nonlinear coset audit
092 ||| This estimate retains all diagonal, off-diagonal, and target-complement interactions; it is not a selected-shell proxy.
093 ||| The high-precision producer, independent binary64 reconstruction, and truncated coset provide separate checks
094 ||| give the Chebyshev-system background. The quantitative rescaled IFT and complete charge estimate are proved directly in the report.
095 ||| provide the weak-energy and semigroup framework;
096 ||| Construction
097 ||| The fixed baseline and complete rotational charge do not rescue the data-uniform first-row estimate
098 ||| Fix the target \(k_*=(0,K_y,K_z)\), annular multiplier, macroscopic interval, and two rescaled root times. Take auxiliary frequencies \(n_l=d r_lq\), and set
099 ||| The fixed-shell atom diverges, the enstrophy ratio is bounded, and the complete projected rotational charge vanishes; the price is unbounded initial data.
100 ||| The following two-sided enstrophy bound turns this into \(J_{*,m,q}\asymp\mathscr A_q^2/q^2\). Only the prescribed \(m=2\) atom is needed; no accumulation of many zeros is required.
101 ||| Its vorticity is \(\omega=(v_y,f_z,-f_y)\), and
102 ||| Take the periodic solution
103 ||| As \(\alpha\uparrow2\), the exponent approaches \(1/3\) from below. For every fixed \(\beta<1/3\), the family therefore rules out the \(D^\beta\) payment, but not the endpoint \(D^{1/3}\), stronger data dependence, or a structurally different charge. Shrinking the observation window to \(q^{-2}\) cannot replace the background because \(\ell^{-1}\) restores \(q^2\).
104 ||| Failure of every estimate with arbitrary initial-data dependence; sharpness of \(D^{1/3}\); failure of the R0.71U second-time theorem; a weak zero trace; single-trajectory infinite recurrence; continuation, finite-time singularity, or global regularity.
105 ||| Data boundary
106 ||| Data boundary:
107 ||| The numerical component is finite-dimensional corroboration, not DNS, and does not carry uniform Dyson convergence, the IFT remainder, nonlinear enstrophy bounds, or the continuum proof.
108 ||| Thus no data-independent \(C_*\) can uniformly control the positive fixed-shell atoms of every smooth unforced solution by \(C_*\Lambda_1\). A singleton shell and the prescribed \(m=2\) root already fail. This conclusion does not negate the R0.71U second-time-jet theorem.
109 ||| A uniform radius produces two exact simple roots
110 ||| Figure R0.71W. The analytic scaling and two independent certificates give an atom at \(q^{+1}\), normalized rotational charge at \(q^{-1}\), and atom-to-complete-ledger ratio at \(q^{+1}\) for the \(\alpha=3/2\) instance; the nonlinear truncated-coset calculation separately checks the opposite scalings of the atom and retained full-coset rotational charge. The figure is reproducible corroboration only and does not replace the analytic no-go theorem.
111 ||| The complete first-row data-uniform ledger fails,
112 ||| The data-uniform complete first-row candidate is closed; data dependence becomes the next testable boundary
113 ||| The next step compares a data-dependent energy/enstrophy charge with exact atom scaling, to determine whether \(1/3\) is a feature of this triangular family or a more general structural boundary. Any positive estimate must be stated for a bounded-data class or with an explicit data prefactor.
114 ||| Next object: data-dependent \(1/3\) boundary
115 ||| The bounded search located no data-uniform fixed-zero quadratic-trace complete first-row Leray estimate. This is not a claim of originality, priority, or nonexistence.
116 ||| A small rescaled coupling and a growing physical amplitude can coexist
117 ||| Rotational term
118 ||| The pressure gradient separates exactly, leaving only one rotational component
119 ||| Research note R0.71W · AMPLITUDE DOPING · COMPLETE FIRST-ROW LEDGER
120 ||| Research note R0.71W: an amplitude-doped exact triangular 2.5D NSE sequence rules out a data-independent complete first-row Leray ledger; initial-data dependence and the one-third endpoint remain open.
121 ||| The research value is precise route pruning: replacing the R0.71U second-time row requires sufficiently strong initial-data dependence, a persistence/noncollapse trace, more time regularity, or a different observable. By itself, this result does not advance the general singularity question toward a conclusion.
122 ||| With \(x=q^2(t-\sigma_q)\) and the Fourier coset \(k_y=K_y+dqr\), write the active scalar as \(f^{\rm act}=\mathscr A_qF_q\). The evolution becomes
123 ||| On a fixed interval \(I\), set \(Y=\|\omega\|_2^2\) and \(L=\mathbb P(u\times\omega)\), and write
124 ||| This is not a solution to the Millennium problem. This section provides no continuation criterion, finite-time singularity, or global regularity.
125 ||| This is an exact invariant class of the original three-dimensional incompressible NSE, not a modified equation or forced model.
126 ||| The slope of the prescribed \(m=2\) filtered coefficient is of order \(\mathscr A_q^2\)
127 ||| Status · R0.71W completed
128 ||| The background gives the lower bound; component equations give an upper bound without exponential loss
129 ||| The background has no \(z\)-derivative and therefore does not enter \(L=(-vf_z,0,0)\). The complete heat-mode shear satisfies \(\int\|v\|_\infty^2dt\le C\mathscr A_q^2/q^2\). Combining \(Y_q\gtrsim\mathscr A_q^2q^2\) with \(\|f_z\|_2\lesssim\mathscr A_q\) gives
130 ||| exact / independent / truncated-coset certificates
131 ||| The exact and independent certificates both check the powers of \(\delta_q\), the atom, the rotational upper bound, atom/ledger ratio, and enstrophy. The finite nonlinear truncated-coset audit checks the exact root residual, the opposite scalings of the atom and retained full-coset \(\dot H^{-1}\) charge, and truncation stability.
132 ||| The target coefficient of filtered \(C_{*,t}\) differs from \(a_t\) only by fixed nonzero multiplier/eigenshell factors; hence at the prescribed root
133 ||| Finite-response and truncated-coset outputs check only finite data and scaling; they do not carry the analytic proof.
134 ||| The full-frequency \(\dot H^{-1}\) payment tends to zero
135 ||| The bounded-data diagonal from R0.71V is absorbed by the fixed \(\nu^2\) term. This section must therefore make the atom grow, keep \(\mathcal R_Y\) bounded, and control the complete rather than selected-shell rotational charge.
136 ||| The complete first-row object left open by R0.71V
137 ||| R0.71V could not exclude the fixed \(\nu^2\) baseline and complete projected rotational term. This section retains both and still obtains divergence, so selected-shell omission, an abstract time path, and pressure are not the causes of this no-go.
138 ||| R0.71W · 2026-08-26 · Personal mathematics research log
139 ||| R0.71W amplitude-doped sequence: fixed-shell atom, complete first-row ledger proxy, rotational term, and truncated-coset stability
140 ||| R0.71W | Amplitude doping and the complete first-row ledger boundary
141 ||| R0.71X tests the \(D^{1/3}\) endpoint and a scale-compatible payment
142 ||| The seed, shear, and a \(z\)-independent background outside the target annulus are doped together; the background coefficient is \(B_q=b_0\mathscr A_qq\). The small quantity is the rescaled coupling \(\delta_q\), not the physical shear amplitude.
143 ||| uniform rescaled Fourier-lattice IFT; exact prescribed roots; root slope \(\asymp\mathscr A_q^2\); \(Y_q\asymp\mathscr A_q^2q^2\); complete projected rotational charge bound; data-uniform complete first-row no-go.
`;

const englishRows = translationRows
  .trim()
  .split("\n")
  .map((row, index) => {
    const expected = String(index + 1).padStart(3, "0") + " ||| ";
    if (!row.startsWith(expected)) {
      throw new Error("unexpected R0.71W translation row " + (index + 1));
    }
    return row.slice(expected.length);
  });

const currentWithoutBatch = current.filter((entry) => !/^r071w\d+$/.test(entry.id));
const currentByChinese = new Map(
  currentWithoutBatch.map((entry) => [entry.zh, entry]),
);
if (currentByChinese.size !== currentWithoutBatch.length) {
  throw new Error("duplicate Chinese keys outside the R0.71W batch");
}

const missingPriority = [
  "recap-r0-61-r0-71w.html",
  "research-review.html",
  "literature-review.html",
  "notes/r0-71w.html",
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
  missing.length !== 143 ||
  englishRows.length !== missing.length ||
  missingHash !== "75af50293cfb54298e101f21f19f22e8f21361c9ff0dc997c4b02a8fafb2692a"
) {
  throw new Error(
    "R0.71W translation source drift: missing=" +
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
    id: "r071w" + String(index + 1).padStart(3, "0"),
    en,
  };
});

for (const relative of [
  "research-review.html",
  "literature-review.html",
  "recap-r0-61-r0-71w.html",
  "notes/r0-71w.html",
]) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.09')) {
    throw new Error(relative + ": expected i18n cache version v1.09");
  }
}
const previous = await readFile(
  resolve(publicDirectory, "notes/r0-71v.html"),
  "utf8",
);
if (!previous.includes('/i18n-en.js?v=1.08')) {
  throw new Error("notes/r0-71v.html: expected historical i18n cache version v1.08");
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
