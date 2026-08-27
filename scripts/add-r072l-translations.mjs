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
const snapshotPath = resolve(
  root,
  "scripts/i18n-snapshots/r072l-missing.json",
);
const checkOnly = process.argv.includes("--check-only");

const englishRows = String.raw`
Retain the actual \(K=\mathcal R_Y\) and \(x=\Theta Q_*\), and establish a local action floor for the constructed family with a fixed background, phase alignment, row alignment, and an exact correction. The ledger is uniformly bounded at the upper edge of the window and decays only in the little-o subwindow.
Open the complete 102-note index
's \(L_t^\infty L_x^3\) endpoint remains the external continuation baseline, but the present ledger has not been shown to imply it.
's averaged Navier–Stokes blowup shows that generic cancellation and harmonic estimates cannot replace the structure of the original equations; it is not genuine NSE blowup.
's large-critical-data smooth nonuniqueness lies in the infinite-energy, non-Leray–Hopf regime and is not a Clay counterexample.
's logarithmic Prodi–Serrin improvement is not the temporal critical-log action used here.
's small-\(BMO^{-1}\) theory cannot be identified with \(\varepsilon\) here;
Open interface · R0.72M
Cumulative recap and 102-note index
Quantify full-lattice enstrophy, all-time action, or improved cubic mixing to pay the \(\varepsilon^{7/3}p^{4/3}\) remainder; retain the multiscale Schur ledger as a parallel interface.
emphasizes that triad transfer depends on exact Fourier geometry;
shows that 2D3C is an exact PDE structure;
shows that isolated triad truncation and exact evolution can differ substantially. The three-mode Galerkin countertheorem is therefore stated separately from the full-lattice non-embedding proposition.
Literature review v1.25 · 2026-08-27
I list published theorems as known results, mark 2026 preprints separately, and list R0.69P–R0.72L on this site only as research notes. I do not extrapolate computations or notes into regularity theorems.
The bounded search found no direct predecessor for the project formula or the \(p^{2/3}R^{2/3}(1+\log R)\) window, but this does not prove novelty or priority. The local floor applies only to the constructed family with a fixed background, phase alignment, row alignment, and an exact correction; the upper edge gives only \(O(1)\), decay requires the little-o subwindow, and the Galerkin result is not a full-Fourier-lattice conclusion.
__DERIVE_LITERATURE_ROUTE__
R0.72L boundary for strong coupling, 2D3C, and Galerkin truncation
Claim boundary for R0.72L
\(\Lambda_{1,*}\) contains at least \(K+x\)
01 · Strong-coupling parameter
02 · Unified ledger
03 · Physical denominator
04 · Local exact root
05 · Moderate strong-coupling window
06 · Galerkin boundary
07 · Multiscale interface
08 · Two-route audit
Version v0.72L · 2026-08-27
This section does not close arbitrary strong coupling or complete multiscale physical absorption, and it gives no continuation criterion, finite-time singularity, or global-smoothness proof for general three-dimensional flows. The Clay Millennium Problem remains unsolved.
Parameter
Beyond this window, a full-lattice enstrophy/action lower bound or a stronger cubic-mixing estimate is still missing.
From fixed smallness to a strong-coupling range that grows with frequency
The single-carrier three-mode projected ODE has \(\theta_y=\sigma e^{-y}-\tfrac12\sin2\theta\). The root count, root-slope mass, and cubic row can therefore all grow linearly in \(\sigma\). This countertheorem is rigorous for the projected ODE.
For \(1\lesssim\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\), the complete physical ledger is uniformly bounded; it decays only in the little-o subwindow.
When \(B\asymp\sqrt N\), the window reaches \(R^{2/3}\log R\); in the most coherent case \(B\asymp N\) with \(N\asymp R\), it still reaches \(R^{1/3}\log R\).
The independent route rederives the inequality directions in the root/action lift, the local correction, and the little-o boundary; it explicitly forbids describing the upper-edge \(O(1)\) bound as decay.
For a phase-aligned, row-aligned launch with a fixed background, set \(\Omega=R^2+gB\) and \(\tau=c_*/\Omega\). Over this interval, both the heat change and the coupling exposure are \(O(c_*)\). A one-coordinate linear correction in the target coordinate gives
For the stated phase-aligned, row-aligned, exactly corrected family, an exact root is produced and the target row is retained at \(\tau=c_*/(R^2+gB)\); this action floor allows the common-band global exposure scale \(\varepsilon\) to be arbitrarily large.
Multiscale
The common-band scale invariant and its one-sided exposure comparison are
The fixed decoupled background gives \(\inf_IY\gtrsim E_{\rm phys}\), so each root atom is at most \(C\Theta|h|^2\). The target Fourier sector gives the action lower bound, while \(\inf Y\le Y(0)\lesssim E_{\rm phys}\). These two directions cannot be interchanged, but together they give
The kernel \(R_jR_k/(R_j^2+R_k^2)\lesssim2^{-|j-k|}\) makes the constant independent of the shell count. The explicit shell moments have not yet been absorbed unconditionally by one global \(D^{1/3}\Lambda_{1,*}\).
The extreme-coupling gap can now be written exactly
The value is an enlarged rigorous closure range and one explicit next remainder
Local root
Set \(K=\mathcal R_Y(I)\), \(x=\Theta Q_*^I\), and \(L_R=1+\log R\), and define
The powers, window, and Galerkin boundary are checked separately
Strong-coupling window
When the global exposure scale is large, one coupling-time window is still small
If \(K\gtrsim\varepsilon^{7/3}p^{4/3}\), the enstrophy contrast alone pays for the strongest cubic term. This is only a sufficient branch; the section does not prove that cascade dynamics must force such growth of \(K\).
The three-mode truncation grows linearly, but it loses higher shells on the first coupling time
The producer certificate reconstructs \(U_0,W,U,V,H,Z\) term by term, scans the normalized contributions inside and outside the window, and numerically checks the projected polar ODE.
The Galerkin orbit therefore creates \(O(1)\) outer-shell mass before many rotations occur. It is not the full Fourier lattice and cannot serve as a counterexample to the full triangular PDE.
Moderate strong-coupling closure, a local action floor, and the Galerkin non-embedding boundary on the full Fourier lattice.
For every \(\varepsilon=gB/R^2>0\), the complete-root ledger on the full Fourier lattice has a uniform upper bound retaining the actual \(K\) and \(x\).
The full convolution has no nonzero finite Fourier-support invariant subspace. For \(u_R=(e_R+e_{-R})/\sqrt2\),
The complete ledger retains the actual enstrophy contrast and action
I retain the actual enstrophy contrast \(K=\mathcal R_Y\) and actual critical-log action \(x=\Theta Q_*\) in the denominator and construct an exact target root on a local window of length \((R^2+gB)^{-1}\). The complete complex-root ledger therefore moves from \(gB/R^2\ll1\) into a moderate strong-coupling range that grows with \(R\). The upper edge is only uniformly bounded; decay holds only in the little-o subwindow.
I obtain a window genuinely beyond the perturbative range without claiming arbitrary strong coupling is solved
Physical quantity
The next step is to prove that enstrophy contrast, all-time action, or true cubic mixing pays at least one \(\varepsilon^{7/3}p^{4/3}\) term. A finite Galerkin orbit cannot replace the full convolution chain.
Small coupling is not the true common-band boundary;
Research note R0.72L · MODERATE STRONG COUPLING · ENSTROPHY-AWARE LEDGER
Research note R0.72L: retaining the actual enstrophy contrast and critical-log action extends the complete-root ledger to a moderate strong-coupling window that grows with R and isolates the extreme strong remainder.
Thus \(Q_*^I\gtrsim a^2N^2\Omega^{-2/3}[1+\log(2+\Omega)]\), and
In this range, the first-root and mixed-row terms vanish, while the cubic term remains \(O(1)\) at the upper edge. If \(\varepsilon=o(p^{2/3}R^{2/3}(1+\log R))\), all three terms vanish.
This floor belongs only to the exactly corrected family with a fixed background and aligned phase and row; it is not a conclusion for arbitrary initial data.
This upper bound combines R0.72K complete-root sampling, the R0.72H mixed row, and the R0.72J hybrid cubic minimum. It does not require \(\varepsilon\ll1\), but in strong coupling it provides only a one-sided root lift and cannot be written as a two-sided equivalence.
Only the one-sided comparison from the upper bound on \(\|V_w(x)\|\) is used; no reverse estimate is assumed, and the actual Duhamel exposure can be smaller. Simultaneously rescaling the shear coefficient and \(\delta\) does not change the dynamics, so bare \(\delta\) cannot define strong coupling. Here \(B\) records multiplier coherence, and distinct integer carriers give \(p\gtrsim R^{-1/2}\).
This remains a stress test of a proof mechanism inside a special exact 2.5D class. It directly advances the Clay problem only if the ledger can be connected to \(L_t^\infty L_x^3\) or another continuation criterion for general three-dimensional solutions.
The formal figure separates the new window, the three payments, and Galerkin leakage
Status · R0.72L theorem complete
The dyadic Schur estimate removes the extra shell-count factor
The small-coupling hypothesis in R0.72K is not the true endpoint of the common-band route. R0.72L proves that the complete root ledger enters a strong-coupling interval that grows with \(R\), while isolating the first unpaid term in the more extreme region.
R0.72L | Small coupling is not the true boundary
R0.72M: quantify the full-lattice cascade at extreme strong coupling
Strong coupling is defined by the common-band exposure scale
01 · Twenty-eight research phases
02 · Complete 102-note index
Retain the R0.72K historical recap
View the R0.72L two-route certificates
The upper edge guarantees only an \(O(1)\) normalized ledger. Decay holds only when \(\varepsilon=o(p^{2/3}R^{2/3}(1+\log R))\); extreme strong coupling and multiscale physical absorption remain open.
Open the latest node R0.72L
Twenty-eight phases and 102 nodes: from reduced recurrences and temporal-trace ledgers through the critical-log candidate to moderate strong-coupling closure.
Recap endpoint: R0.72L
Public notes at recap endpoint: 162
As of R0.72L, there is no new unconditional continuation criterion, no reduction of the set of all possible singular solutions, and no proof of finite-time breakdown. The 102 nodes or 64 public releases cannot be interpreted as a completion percentage for the Millennium Problem.
Cumulative recap · R0.61–R0.72L · 2026-08-27
Nodes included: 102
I retain the actual enstrophy contrast \(K\) and actual action \(x\) in the complete-root denominator, obtaining a full-lattice upper bound valid for every \(\varepsilon=gB/R^2>0\). For the constructed family with a fixed background, phase alignment, row alignment, and an exact correction, the local exact root also gives \(x\ge Z\).
The next step is to prove that enstrophy contrast, all-time action, or improved cubic mixing pays at least one \(\varepsilon^{7/3}p^{4/3}\) term.
Small coupling is no longer the common-band boundary, but extreme strong coupling is still unpaid
The new rigorous results are a coupling-uniform enstrophy-aware upper bound, a local action floor allowing an arbitrarily large global exposure scale, and a moderate strong-coupling closure that grows with \(R\).
This advances the closure to \(1\lesssim\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\). The upper edge gives only \(O(1)\), and only the little-o subwindow decays. Linear growth in the three-mode Galerkin model does not embed in the full lattice; extreme strong coupling remains open.
This page follows the phase recap for R0.00–R0.60 and organizes the research nodes from R0.61 through R0.72L, 102 in total. I record chronologically what each segment actually proves, which proposals are excluded by concrete counterexamples or scaling analysis, and which conditions have not been derived from the Navier–Stokes equations. Node status describes the type of evidence and does not misstate release archiving as completion of a phase objective.
A finite Galerkin model cannot replace the full convolution chain; retain the separated-heat-window multiscale Schur ledger as a parallel interface.
The material from R0.00–R0.60 remains in the previous phase recap. The conclusion at R0.60 is that the full Fourier–Leray structure and higher-order computations can continue, but the critical quantity for general three-dimensional solutions is not yet controlled. The subsequent 102 nodes advance along this gap; from R0.70A–R0.72L, 64 releases are public, and 40 satisfy the current formal-figure complete-archive contract, while still including conditional theorems, counterexamples, finite diagnostics, and open gaps.
The route after R0.60 has twenty-eight phases
Research recap after R0.60: complete coverage from R0.61 through R0.72L, totaling 102 research nodes; the latest section advances the common band into a moderate strong-coupling window that grows with R.
Public notes from R0.61–R0.72L: 102
R0.61–R0.72L recap · 2026-08-27
R0.61–R0.72L research nodes
R0.61–R0.72L | Research recap after R0.60
From R0.70A–R0.72L, the 64 HTML/PDF releases and research sources are on the public route. Under the current formal-figure contract, 40 releases are fully archived; 24 earlier releases remain on the auditable legacy-backfill list.
Published releases from R0.70A–R0.72L
R0.72L · Moderate strong-coupling closure and the extreme-coupling remainder
R0.72L enstrophy-aware strong window: the complete-root upper bound retains \(K=\mathcal R_Y\) and \(x=\Theta Q_*\) at every coupling strength; for the constructed family with a fixed background, phase alignment, row alignment, and an exact correction, \(x\ge Z\) advances the common-band closure to \(\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\). The upper edge is only uniformly bounded, the little-o subwindow decays, and extreme strong coupling remains open.
R0.72L figure
R0.72L is limited to the exact finite triangular common-band class; the local floor also requires a fixed background, phase alignment, row alignment, and an exact correction. It closes neither extreme strong coupling, multiscale physical payment, nor global smoothness for general three-dimensional Navier–Stokes; the official Clay problem remains open.
R0.72L certificates
R0.72M quantifies the full-lattice cascade at extreme strong coupling
With actual enstrophy and action retained, small coupling is no longer the common-band boundary
From complete complex-root closure to a moderate strong-coupling window
For every \(\varepsilon=gB/R^2>0\), I obtain a full-lattice complete-root upper bound retaining \(K=\mathcal R_Y\) and \(x=\Theta Q_*\). For a launch with a fixed background, phase alignment, and row alignment, the local exact correction produces an exact root at \(\tau=c_*/(R^2+gB)\) and gives \(x\ge Z\).
__DERIVE_ROUTE_PATH__
__DERIVE_HOME_ROUTE__
Cumulative recap R0.61–R0.72L · 2026-08-27
The cumulative recap now has twenty-eight problem phases and completely covers R0.61–R0.72L. It retains the critical-log, mixed/cubic, and complex-root route from R0.72E–K and adds the enstrophy-aware moderate strong-coupling closure of R0.72L. Across R0.70A–R0.72L, 64 releases are public; 40 satisfy the current formal-figure complete-archive contract, while 24 older figure archives remain on the backfill list.
Quantify the full-lattice cascade/enstrophy/action alternative at extreme strong coupling.
Quantify full-lattice enstrophy contrast, all-time action, or improved cubic mixing to pay the R0.72L remainder \(\varepsilon^{7/3}p^{4/3}\); retain the multiscale Schur ledger as a parallel interface.
Previous review v1.24 · 2026-08-27
__DERIVE_HOME_CALLOUT__
Next R0.72M:
Research note R0.72L · 2026-08-27
The ledger is uniformly bounded for \(1\lesssim\varepsilon\lesssim p^{2/3}R^{2/3}(1+\log R)\); it decays only in the little-o subwindow. The linear bad family in the Galerkin model does not embed in the full Fourier lattice.
Read the R0.72L research note →
Expand 72 public notes
Review v1.25 · 2026-08-27
The common band now extends beyond fixed-small coupling; the upper edge gives only \(O(1)\), decay holds only in the little-o subwindow, and the extreme strong remainder and multiscale physical absorption remain open.
The complete-root ledger enters a moderate strong-coupling window growing with \(R\); the extreme strong remainder is isolated explicitly.
Extreme strong coupling, multiscale physical absorption, and general three-dimensional regularity remain open.
The cumulative recap after R0.60 contains 102 nodes; the site now has 162 public research notes
R0.70A–R0.72L: 64 published, 40 fully archived
R0.72L retains the actual enstrophy contrast and critical-log action and extends the common-band complete-root ledger to a moderate strong-coupling window growing with \(R\); the extreme strong remainder remains open.
R0.72L complete:
`
  .trim()
  .split("\n");

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
  "notes/r0-72l.html",
  "recap-r0-61-r0-72l.html",
  "research-review.html",
];
for (const relative of expectedFiles) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.25')) {
    throw new Error(relative + ": expected i18n cache version v1.25");
  }
}

const source = await collectSiteStrings(publicDirectory);
const translations = JSON.parse(await readFile(translationPath, "utf8"));
const batchId = /^r072l\d+$/;
const retained = translations.filter((entry) => !batchId.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72L batch");
}

const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
if (englishRows.length !== missing.length || missing.length !== 136) {
  throw new Error(
    `R0.72L English row count ${englishRows.length} does not match active missing set ${missing.length}`,
  );
}
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))];
if (!sameTokens(missingFiles, expectedFiles)) {
  throw new Error("Unexpected R0.72L source files: " + JSON.stringify(missingFiles));
}

function retainedEnglish(zh) {
  const entry = retainedByChinese.get(zh);
  if (!entry) throw new Error("Missing retained translation derivation source: " + zh);
  return entry.en;
}

const literatureAddition =
  "R0.72L retains the actual enstrophy contrast and critical-log action and closes a moderate strong-coupling window growing with \\(R\\); the upper edge gives only \\(O(1)\\), and decay holds only in the little-o subwindow.";
const literatureLChinese =
  "R0.72L 保留实际 enstrophy contrast 与 critical-log action，闭合随 \\(R\\) 增长的 moderate strong-coupling window；窗口上沿只给 \\(O(1)\\)，little-o 子区间才衰减。";
const homeRouteAddition =
  "R0.72L retains the actual \\(K\\) and \\(x\\) and uses a local exact root/action floor to extend the closure to \\(\\varepsilon\\lesssim p^{2/3}R^{2/3}(1+\\log R)\\).";
const homeRouteLChinese =
  "R0.72L 保留 actual \\(K\\) 与 \\(x\\)，用 local exact root/action floor 把闭合区推进到 \\(\\varepsilon\\lesssim p^{2/3}R^{2/3}(1+\\log R)\\)。";

const translatedEntries = missing.map((entry, index) => {
  let en = englishRows[index];
  if (en === "__DERIVE_LITERATURE_ROUTE__") {
    const oldZh = entry.zh.replace(literatureLChinese, "");
    en = retainedEnglish(oldZh).replace(
      "General Navier–Stokes regularity remains open.",
      literatureAddition + " General Navier–Stokes regularity remains open.",
    );
  } else if (en === "__DERIVE_ROUTE_PATH__") {
    const suffix = " → moderate strong-coupling window → extreme remainder";
    en = retainedEnglish(entry.zh.slice(0, -suffix.length)) + suffix;
  } else if (en === "__DERIVE_HOME_ROUTE__") {
    const oldZh = entry.zh.replace(homeRouteLChinese, "");
    en = retainedEnglish(oldZh) + homeRouteAddition;
  } else if (en === "__DERIVE_HOME_CALLOUT__") {
    const oldZh = entry.zh.replaceAll("R0.72L", "R0.72K");
    en = retainedEnglish(oldZh).replaceAll("R0.72K", "R0.72L");
  }
  if (!en.trim() || containsChinese(en)) {
    throw new Error("Blank or Chinese-containing English for: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Collective English voice remains in: " + entry.zh);
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
    id: "r072l" + String(index + 1).padStart(3, "0"),
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

if (!checkOnly) {
  await writeFile(
    snapshotPath,
    JSON.stringify(
      missing.map(({ zh, count, files }) => ({ zh, count, files })),
      null,
      2,
    ) + "\n",
  );
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
