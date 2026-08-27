import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const defaultRoot = resolve(import.meta.dirname, "..");
const root = resolve(process.env.R072M_RELEASE_ROOT ?? defaultRoot);
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const snapshotPath = resolve(
  root,
  "scripts/i18n-snapshots/r072m-missing.json",
);
const checkOnly = process.argv.includes("--check-only");

const englishRows = String.raw`
Open the complete 103-note index
's triad analysis shows that transfer depends on the exact geometry and polarization;
establish shear enhanced-dissipation semigroup estimates, but these results do not directly give the project-specific cubic variation with an absolute value in this section. The Bessel recurrence, fixed-order asymptotics, and uniform Airy control in the turning region use
The analytic theorems cover the scalar superlevel set and the stated one-carrier zero-diffusion reference. Removing the relative diagonal heat is not a dissipative PDE reduction; the two finite dissipative curves are only convergence diagnostics. A bounded search does not establish novelty or priority.
Open interface · R0.72N
Cumulative recap and 103-note index
's result shows that a truncated triad can differ from exact evolution. R0.72M therefore retains the complete infinite convolution lattice and does not treat a three-mode orbit as a PDE subsystem.
Literature review v1.26 · 2026-08-27
I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72M on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.
Prove \(\mathcal C_{\rm diss}=O(a^2\log(1+\sigma))\), or prove \(\sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})\).
__DERIVE_LITERATURE_ROUTE__
R0.72M boundary for the full-lattice reference and enhanced dissipation
Claim boundary for R0.72M
The scalar cubic superlevel set is an explicit middle open interval; the complete one-carrier zero-diffusion reference has a Bessel solution, action-poor placement, and the true-cubic law \((16/\pi^2)a^2\log\sigma\).
00 · Direct decision
01 · Exact danger window
02 · Complete lattice
03 · Complete action
05 · Branch placement
06 · Two-route audit
Version v0.72M · 2026-08-27
Report, two-route certificates, formal figure, and cumulative recap
This section does not treat the zero-diffusion reference chain as a dissipative PDE, does not extrapolate continuum asymptotics from finite diagnostics, and does not complete arbitrary strong coupling, multiple carriers, multiscale physical absorption, a finite-time singularity, or a global-smoothness proof. The Clay Millennium Problem remains unsolved.
The reference model uses the complete infinite lattice, not a three-mode closure
After restoring the inherited \(\Theta\asymp\sigma^2\), \(x_{\rm fr}\asymp\sigma^{4/3}\log\sigma\). The target row alone gives a positive signal with the same exponent, but it cannot replace \(q(s)\) or its constant.
The second identity places the reference enstrophy contrast at \(K_{\rm fr}\asymp\sigma^2\) for the fixed geometry.
For \(f_1(0)=2^{-1/2}\) and \(f_{-1}(0)=-2^{-1/2}\), the generating function or the Bessel propagator gives
Branch placement
The figure separates the analytic theorem, reference asymptotics, and finite dissipative diagnostics
give shear enhanced-dissipation semigroup results, but do not directly control the project-specific cubic variation with an absolute value in this section. This site states conclusions only to the extent supported by the current report and certificates and does not claim priority from a bounded search.
For the fixed one-carrier geometry, \(x/H\asymp\sigma^{-2/3}\log\sigma\) and \(Vx/K\asymp\sigma^{-1/3}\log\sigma\), so the reference chain lies below the danger window.
The dissipative curves show only that two finite discretizations agree on the stated grids. They do not prove \(\mathcal C_{\rm diss}=O(\log\sigma)\).
The value is to replace “is the action large enough?” with a decidable interval
The analytic formulas and finite diagnostics use two independent numerical routes
The absolute cubic variation grows only logarithmically
The zero-diffusion reference chain retains the complete infinite lattice and the \(e^{-y}\) coupling envelope. For the stated antisymmetric launch, the exact solution is \(f_n(s)=\sqrt2J_n'(2s)\).
Let \(Bf=(f_{n-1}-f_{n+1})_n\), and define
Let \(T(x)=\min\{U,Vx\}/(K+x)\) and \(H=U/V\). When \(A<U/(K+H)\), \(T(x)>A\) is equivalent to \(\frac{AK}{V-A}<x<\frac UA-K\); otherwise the superlevel set is empty.
Choose a one-carrier mode orthogonal to the target frequency and write \(\mu=q_*^2/R^2>0\). After removing the relative diagonal heat, retain the complete coupling chain
Removing \(-n^2f_n\) is a benchmark operation, not an exact reduction of the dissipative equation. Finite numerical curves do not replace a uniform analytic estimate.
The formula requires \(0<A<U/(K+H)\). With an inherited floor \(x\ge Z\), intersect it with \([Z,\infty)\). The function \(T\) rises to the left of \(H\) and falls to its right. Thus too little action and a sufficiently large denominator are both safe branches; only the middle interval can make this scalar term large.
's result shows that a truncated triad can differ from exact evolution. The Bessel wave here occupies the complete lattice.
's analysis shows that triad transfer depends on geometry and polarization;
The complete Fourier-lattice Bessel benchmark, action-poor placement, and the open boundary for the dissipative chain.
The complete superlevel set can be written endpoint by endpoint
Complete lattice
The complete one-carrier reference chain lies below the window
Danger window
The dangerous term appears only in the middle action window;
I first rewrite the R0.72L scalar cubic remainder as an exact superlevel interval, then solve a one-carrier zero-diffusion reference chain on the complete infinite Fourier lattice. The Bessel solution gives the vorticity scale \(\sigma^2\), the lifted action \(\sigma^{4/3}\log\sigma\), and the true-cubic leading term \((16/\pi^2)a^2\log\sigma\). This reference chain belongs to the action-poor branch; the analogous uniform estimate for the dissipative chain remains unproved.
The next section checks two provable targets in parallel: prove \(\mathcal C_{\rm diss}(\sigma)\lesssim a^2[1+\log(1+\sigma)]\) directly, or prove \(\sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})\). The former bypasses the scalar window; the latter places the action below it.
Write \(u(s)=f_1(s)=\sqrt2J_1'(2s)\). After restoring the carrier envelope and target heat, the reference true-cubic mass is exactly
Research note R0.72M · EXACT DANGER WINDOW · FULL-LATTICE PHASE MIXING
Research note R0.72M: the exact scalar-cubic action danger window, with the Bessel action and logarithmic true-cubic benchmark proved on the complete one-carrier lattice.
Therefore the R0.72L optimization over all \(x\ge Z\) is not sharp for this family. This conclusion locates only one exact reference family; it does not show that every extreme-coupling solution is action-poor.
In the ledger with \(p=1\) and fixed \(R=R_0\), \(U\asymp\sigma^{7/3}\), \(V\asymp\sigma^{1/3}\), and \(H\asymp\sigma^2\). Hence
The original \(Vx\) branch already pays for this reference family
This still does not establish a general dissipative theorem or imply \(L_t^\infty L_x^3\) or another continuation criterion for general three-dimensional flows. Its current value for the Clay problem is to screen mechanisms and narrow the next proof target, not to solve the original problem.
Stationary phase, the Airy transition region, and tail estimates give \(q(s)\lesssim(1+s)^{-1}\). Therefore
Status · R0.72M theorem complete
The large-parameter expansion of the Bessel derivative and the oscillatory absolute-value average give the sharp leading term
The independent route instead uses the Bessel recurrence, angular FFT Parseval, independent quadrature, and a finite-chain Cayley split. The crosscheck applies separate accuracy gates to quantities with the same name.
The negative-norm action must include the complete lattice, not a single target row
The producer uses differentiated Bessel functions, Gauss quadrature, and Fourier phase splitting to check the exact window, Bessel moment, action scaling, frozen cubic, and finite dissipative diagnostic.
The R0.72L bad term is not monotone in the action
R0.72M corrects the loss caused by optimizing the previous section over the full range of \(x\), and gives a sharp benchmark on the complete infinite lattice. It shows that at least one genuine phase-mixing geometry does not trigger the scalar danger window and that the raw \(O(\sigma)\) cubic bound is very lossy for this reference model.
R0.72M｜Exact action danger window
R0.72N: return to the dissipative chain with \(-n^2f_n\)
Triad geometry, enhanced dissipation, and the cubic action here are not the same conclusion
02 · Complete 103-note index
Retain the R0.72L historical recap
Check \(\mathcal C_{\rm diss}\lesssim a^2[1+\log(1+\sigma)]\) and \(\sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})\) in parallel.
View the R0.72M two-route certificates
Open the latest node R0.72M
Twenty-eight phases and 103 nodes: from reduced recurrences and temporal-trace ledgers through the critical-log candidate and strong-coupling window to the complete one-carrier reference chain.
Recap endpoint: R0.72M
Public notes at recap endpoint: 163
As of R0.72M, there is no new unconditional continuation criterion, no reduction of the set of all possible singular solutions, and no proof of finite-time breakdown. The 103 nodes or 65 public releases cannot be interpreted as a completion percentage for the Millennium Problem.
Cumulative recap · R0.61–R0.72M · 2026-08-27
The zero-diffusion reference lies on the action-poor branch, but it is not the dissipative chain with \(-n^2f_n\). A uniform logarithmic-cubic or action-poor theorem for the latter remains open.
The former pays for the true cubic directly; the latter proves that the action lies below the danger window. The multiscale Schur ledger remains a parallel interface.
Nodes included: 103
The complete one-carrier zero-diffusion reference chain has a Bessel solution, \(K_{\rm fr}\asymp\sigma^2\), \(x_{\rm fr}\asymp\sigma^{4/3}\log\sigma\), and \(\mathcal C_{\rm fr}=(16/\pi^2)a^2\log\sigma+O(a^2)\). It lies on the action-poor branch; the dissipative chain with diagonal heat remains open.
The new rigorous results are the exact scalar superlevel theorem, the complete-infinite-lattice Bessel reference, the complete-action asymptotic, and the sharp cubic coefficient \(16/\pi^2\).
This page follows the phase recap for R0.00–R0.60 and organizes the research nodes from R0.61 through R0.72M, 103 in total. I record chronologically what each segment actually proves, which proposals are excluded by concrete counterexamples or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations. Node status describes the type of evidence and does not misstate release archiving as completion of a phase objective.
The material from R0.00–R0.60 remains in the previous phase recap. The conclusion at R0.60 is that the complete Fourier–Leray structure and higher-order computations can continue, but the critical quantity for general three-dimensional solutions is not yet controlled. The subsequent 103 nodes advance along this gap; the releases from R0.70A–R0.72M, 65 in total, are public, and 41 satisfy the current formal-figure complete-archive contract, while still including conditional theorems, counterexamples, finite diagnostics, and open gaps.
Research recap after R0.60: complete coverage from R0.61 through R0.72M, totaling 103 research nodes; the latest section gives the exact action danger window and the complete one-carrier phase-mixing benchmark.
Public research notes from R0.61–R0.72M: 103
R0.61–R0.72M recap · 2026-08-27
R0.61–R0.72M research nodes
R0.61–R0.72M｜Research recap after R0.60
The HTML/PDF releases and research sources from R0.70A–R0.72M, 65 in total, are on the public route. Under the current formal-figure contract, 41 releases are fully archived; 24 earlier releases remain on the auditable legacy-backfill list.
Published releases from R0.70A–R0.72M
R0.72L retains the actual enstrophy contrast \(K\) and actual action \(x\) in the complete-root denominator, advancing the closure to a moderate strong-coupling window growing with \(R\). R0.72M then determines all superlevel intervals of the scalar cubic exactly.
R0.72L–R0.72M · Moderate strong-coupling window and exact action screen
The R0.72M analytic theorem is limited to the scalar ledger and the stated complete one-carrier zero-diffusion reference. Finite dissipative diagnostics are not a continuum theorem; the official Clay problem remains open.
R0.72M exact danger-window theorem and full-lattice reference: the superlevel set of \(\min\{U,Vx\}/(K+x)\) is an explicit middle open interval; the complete one-carrier zero-diffusion chain has \(f_n(s)=\sqrt2J_n'(2s)\), gradient moment \(1+s^2\), lifted action \(\asymp\sigma^{4/3}\log\sigma\), and true-cubic leading term \((16/\pi^2)a^2\log\sigma\). This reference belongs to the action-poor branch; the dissipative theorem remains open.
R0.72M figure
R0.72M certificates
R0.72N returns to the dissipative one-carrier chain
The scalar danger window is exact; the dissipative chain remains the next gate
From the moderate strong-coupling window to the exact action screen
__DERIVE_ROUTE_PATH__
Return to the complete dissipative chain with \(-n^2f_n\), and prove a logarithmic true-cubic bound or the action-poor inequality \(\sigma^{1/3}x_{\rm diss}=o(K_{\rm diss})\).
__DERIVE_HOME_ROUTE__
Cumulative recap R0.61–R0.72M · 2026-08-27
The cumulative recap retains twenty-eight problem phases and completely covers R0.61–R0.72M. R0.72M rewrites the extreme-strong scalar remainder as an exact action danger window and uses the complete one-carrier Bessel reference to prove action-poor placement and the sharp logarithmic cubic law. Across R0.70A–R0.72M, 65 releases are public; 41 satisfy the current formal-figure complete-archive contract, while 24 older figure archives remain on the backfill list.
The zero-diffusion reference is not a dissipative PDE; general three-dimensional regularity remains open.
The zero-diffusion reference chain lies below the danger window; a uniform cubic/action theorem for the dissipative one-carrier chain and multiscale physical absorption remain open.
Previous review v1.25 · 2026-08-27
I determine every superlevel set of \(T(x)=\min\{U,Vx\}/(K+x)\) exactly and obtain \(f_n(s)=\sqrt2J_n'(2s)\) on the complete infinite Fourier lattice. The reference chain has gradient moment \(1+s^2\) and lifted action of order \(\sigma^{4/3}\log\sigma\).
Next R0.72N:
Research note R0.72M · 2026-08-27
Read the R0.72M research note →
Expand 73 public notes
Prove a logarithmic cubic bound or an action-poor inequality for the dissipative one-carrier chain.
Review v1.26 · 2026-08-27
The cumulative recap after R0.60 contains 103 nodes; the site now has 163 public research notes
R0.70A–R0.72M: 65 published, 41 fully archived
R0.72M rewrites the scalar cubic remainder as an exact action danger window and proves action-poor placement and a logarithmic true-cubic law on the complete one-carrier Bessel reference; the dissipative one-carrier theorem remains open.
R0.72M complete:
The reference true-cubic mass satisfies \(\mathcal C_{\rm fr}=(16/\pi^2)a^2\log\sigma+O(a^2)\), and \(Vx_{\rm fr}/K_{\rm fr}\to0\). The two finite audits agree; the dissipative curves are diagnostics only.
The scalar cubic is dangerous only in a middle action window; the complete one-carrier reference chain lies below it
The scalar danger window and the full-lattice zero-diffusion reference are closed; the dissipative one-carrier theorem moves to R0.72N.
`
  .trim()
  .split("\n")
  .filter((row) => row.length > 0);

function numericTokens(value) {
  return [...value.matchAll(/\p{N}+(?:[.,]\p{N}+)*/gu)].map(
    (match) => match[0],
  );
}

function sameTokens(left, right) {
  return JSON.stringify(left) === JSON.stringify(right);
}

const expectedFiles = [
  "literature-review.html",
  "notes/r0-72m.html",
  "recap-r0-61-r0-72m.html",
  "research-review.html",
];
for (const relative of expectedFiles) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.26')) {
    throw new Error(relative + ": expected i18n cache version v1.26");
  }
}

const source = await collectSiteStrings(publicDirectory);
const translations = JSON.parse(await readFile(translationPath, "utf8"));
const batchId = /^r072m\d+$/;
const retained = translations.filter((entry) => !batchId.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72M batch");
}

const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
if (englishRows.length !== missing.length || missing.length !== 124) {
  throw new Error(
    `R0.72M English row count ${englishRows.length} does not match active missing set ${missing.length}`,
  );
}
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))];
if (!sameTokens(missingFiles, expectedFiles)) {
  throw new Error("Unexpected R0.72M source files: " + JSON.stringify(missingFiles));
}

function retainedEnglish(zh) {
  const entry = retainedByChinese.get(zh);
  if (!entry) {
    throw new Error("Missing retained translation derivation source: " + zh);
  }
  return entry.en;
}

const literatureMChinese =
  "R0.72M 精确求出 scalar action danger window，并在完整一载波 zero-diffusion chain 上证明 Bessel action-poor benchmark 与 sharp logarithmic cubic law。";
const literatureMEnglish =
  "R0.72M determines the exact scalar action danger window and proves the Bessel action-poor benchmark and sharp logarithmic cubic law on the complete one-carrier zero-diffusion chain.";
const routeNewSuffix =
  " → moderate strong-coupling window → exact action danger window → dissipative one-carrier gate";
const routeOldSuffix =
  " → moderate strong-coupling window → extreme remainder";
const homeMChinese = String.raw`R0.72M 精确求出 scalar danger window，并在完整一载波 Bessel reference 上证明 action-poor placement 与 \((16/\pi^2)a^2\log\sigma\) cubic law。`;
const homeMEnglish = String.raw`R0.72M determines the exact scalar danger window and proves action-poor placement and the cubic law \((16/\pi^2)a^2\log\sigma\) on the complete one-carrier Bessel reference.`;

const translatedEntries = missing.map((entry, index) => {
  let en = englishRows[index];
  if (en === "__DERIVE_LITERATURE_ROUTE__") {
    const oldZh = entry.zh.replace(literatureMChinese, "");
    en = retainedEnglish(oldZh).replace(
      "General Navier–Stokes regularity remains open.",
      literatureMEnglish + " General Navier–Stokes regularity remains open.",
    );
  } else if (en === "__DERIVE_ROUTE_PATH__") {
    if (!entry.zh.endsWith(routeNewSuffix)) {
      throw new Error("Unexpected R0.72M route-path suffix");
    }
    const oldZh = entry.zh.slice(0, -routeNewSuffix.length) + routeOldSuffix;
    en = retainedEnglish(oldZh).replace(routeOldSuffix, routeNewSuffix);
  } else if (en === "__DERIVE_HOME_ROUTE__") {
    const oldZh = entry.zh.replace(homeMChinese, "");
    en = retainedEnglish(oldZh) + homeMEnglish;
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Blank or Chinese-containing English for: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Collective English voice remains in: " + entry.zh);
  }
  if (entry.zh.includes("我") && !/\bI\b/.test(en)) {
    throw new Error("First-person singular English is missing for: " + entry.zh);
  }
  if (!sameTokens(extractProtectedTokens(entry.zh), extractProtectedTokens(en))) {
    throw new Error(
      "Protected-token mismatch for:\n" +
        entry.zh +
        "\nZH " +
        JSON.stringify(extractProtectedTokens(entry.zh)) +
        "\nEN " +
        JSON.stringify(extractProtectedTokens(en)),
    );
  }
  if (!sameTokens(numericTokens(entry.zh), numericTokens(en))) {
    throw new Error(
      "Numeric-token mismatch for:\n" +
        entry.zh +
        "\nZH " +
        JSON.stringify(numericTokens(entry.zh)) +
        "\nEN " +
        JSON.stringify(numericTokens(en)),
    );
  }
  return {
    ...entry,
    id: "r072m" + String(index + 1).padStart(3, "0"),
    en,
  };
});

const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  const values = finalTranslations.map((entry) => entry[field]);
  if (new Set(values).size !== values.length) {
    throw new Error("Duplicate final translation " + field);
  }
}

const snapshot = missing.map(({ zh, count, files }) => ({ zh, count, files }));
if (checkOnly) {
  const currentSnapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
  if (JSON.stringify(currentSnapshot) !== JSON.stringify(snapshot)) {
    throw new Error("R0.72M missing-string snapshot is stale");
  }
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.72M translations/en.json batch is stale");
  }
} else {
  await writeFile(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");
  await writeFile(
    translationPath,
    JSON.stringify(finalTranslations, null, 2) + "\n",
  );
}

console.log(
  JSON.stringify({
    checkOnly,
    added: translatedEntries.length,
    total: finalTranslations.length,
    liveStrings: source.length,
    missingBefore: missing.length,
    missingAfter: 0,
    files: missingFiles,
  }),
);
