#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const translationRoute = "LOCAL_DIRECT_NO_DGX";
const dgxUsed = false;
const checkOnly = process.argv.includes("--check-only");

// Deterministic translations in collectSiteStrings order at the frozen R0.74P
// boundary. Mathematical tokens are copied byte-for-byte from the Chinese keys.
const english = [
  "Master index of 218 research notes",
  "96 sections fully sealed",
  "View the R0.74P homepage card",
  "Current endpoint R0.74P",
  "Every fixed positive-order window misses the target; energy oscillation reconstructs the endpoint; the defect-completed clock detects the target shell, but the complete matched square-function upper bound remains open.",
  "Jump to the R0.74P homepage card →",
  "Research note R0.74P · 2026-09-02",
  "Read the latest R0.74P research note →",
  "Expand 128 public notes",
  "Prove or disprove the PDE compression from the shellwise ℓ1 flux ledger to the matched ℓ2 clock, and test prescribed-centre scale packing.",
  "Review v1.82 · 2026-09-02",
  "The cumulative review after the R0.60 recap contains 157 nodes; the site now has 218 public research notes",
  "R0.70A–R0.74P · 120 sections published",
  "R0.70A–R0.74P: 120 sections published, 96 fully sealed",
  "R0.74P excludes every fixed positive-order temporal window, confirms that energy oscillation merely repackages the endpoint, and compresses the remaining gap to a PDE reduction from the shellwise ℓ1 flux ledger to the matched ℓ2 clock; the complete square-function upper bound, scale packing, and Clay remain open.",
  "R0.74P: Temporal-observable triage and the matched-clock boundary",
  "R0.74P｜Which temporal observables actually see the missing scale?",
  "R0.74Q next interface",
  "Every fixed positive-order window strictly misses the target; energy oscillation reconstructs the endpoint; the defect-completed clock is stable under suitable-weak limits at fixed scale, and the target shell reaches the target scale, while the complete matched square-function upper bound remains open.",
  "Open interface · R0.74Q",
  "Temporal-observable triage and the matched-clock boundary",
  "Literature review v1.82 · 2026-09-02",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74P only as research notes. I do not extrapolate computations or notes into regularity theorems.",
  "A bounded search of eight primary sources covers suitable weak solutions, local dissipation, moving cylinders, fixed physical-shell flux, spatial regularity intervals, and quantitative regularity epochs; Yu 2026 is an adjacent preprint on moving windows and scale-defect ledgers. No source replaces this section's shell-clock proof. A finite non-hit proves neither novelty, priority, search completeness, nor publishability.",
  "Effective shells, duration, scale packing, and contraction iteration at prescribed centres remain open.",
  "PDE compression from ℓ1 to matched ℓ2",
  "PROVED, INHERITED, FINITE, LITERATURE BOUNDARY, OPEN, and NOT CLAY are separated. The complete matched square-function upper bound, PDE compression, scale packing, contraction iteration, and arbitrary three-dimensional regularity remain open.",
  "R0.74P public boundary",
  "R0.74P literature and claim boundary",
  "218 public research notes, with R0.74P as the latest node.",
  "Which temporal observables actually see the missing scale?",
  "Research-note master index · v1.82 · 2026-09-02",
  "Latest node R0.74P · continuously revised",
  "01 / Complete text",
  "02 / Complete text",
  "03 / Complete text",
  "04 / Complete text",
  "05 / Complete text",
  "06 / Complete text",
  "07 / Complete text",
  "08 / Complete text",
  "09 / Complete text",
  "1. First route: why positive-order window mass must miss the scale",
  "10 / Complete text",
  "2. Second route: energy oscillation detects the scale but is not genuinely weaker",
  "20 validation records",
  "3. Third route: complete the shell clock with total local dissipation",
  String.raw`4. The closed \(\ell^1\) clock`,
  "5. Matched square function: target-shell detection, complete upper bound open",
  "52 exact-rational and finite-sequence checks; 147 envelope points and 5 rate rows in the figure.",
  "6. Fixed-scale weak stability is closed",
  "7. The one inequality that truly remains",
  "8. Research value of this section",
  "9. Evidence and boundaries",
  "This section contains no numerical Navier--Stokes simulation, constructs no singularity, excludes no singularity, and proves no global regularity for arbitrary smooth finite-energy initial data.",
  "and further obtain",
  String.raw`and prove that the new right-hand term is sufficiently small or summable along a nested scale sequence with a prescribed centre. The spatial regularity intervals and quantitative regularity epochs in Lei--Ren are chosen after inspecting the solution and do not automatically force a shrinking scale sequence through a prescribed spacetime centre. Yu 2026 studies adjacent moving parabolic-window chains, local-energy supply--tax ledgers, and scale-defect packages, but does not state the \(K=Q+F\) shell clock, temporal positive-variation BV, or the matched-shell \(\ell^2\) lower-semicontinuity theorem proved here.`,
  String.raw`Pure sequence inequalities cannot prove it. If \(v_1=\cdots=v_N=1\), then`,
  "Window mass, energy oscillation, and exterior dissipation have the corresponding lower-semicontinuity properties as well.",
  "But this is not the weaker mechanism I sought. It reconstructs the endpoint through the difference between the highest and lowest energy and explicitly restores the full exterior dissipation on the right. It is a stable and correct baseline, but it is already solved.",
  String.raw`When \(\sigma>1\), the second branch grows with \(x\); because \(x<1\), \(K_*^{-1}\) is approached only as \(x\uparrow1\) and is not attained on the admissible windows.`,
  "The core gap can now be written as",
  "Introduction",
  "Define the largest oscillation over all temporal window averages",
  String.raw`For fixed \(\sigma>0\), define`,
  String.raw`For each spatial shell, at a local-energy good time \(\tau<t_0\), first define`,
  String.raw`Taking the suprema separately in the three regimes \(0<\sigma<1\), \(\sigma=1\), and \(\sigma>1\) gives`,
  "Even if this inequality holds, regularity is not solved. The next interface still needs a genuine scale contraction, for example",
  "The conclusion is clear.",
  "The local energy inequality gives",
  String.raw`The shell weight is placed inside the clock, so at good times \(K_{k,R}=\gamma_k\widetilde K_{k,R}\). At all times, however, I do not use this measure formula as the definition. Instead I use the exact cumulative balance`,
  "Let the weighted energy be",
  "Every fixed positive-order window mass misses the target scale.",
  "Yet the target shell pays at least",
  "Target-shell two-sided scale: PROVED",
  "The energy-oscillation route is identified as an endpoint repackaging.",
  "Energy oscillation sees the target scale, but it essentially rewrites the original endpoint.",
  String.raw`Here \(Q\) is the quadratic cutoff primitive, \(F\) is the physical-flux primitive, and \(Q+F\) is chosen as the canonical absolutely continuous representative of \(K\) on \([s_R,t_0]\). It agrees with the preceding expression at every good time. The point is not merely to add a symbol, but to avoid taking a hard time section of the dissipation measure; weak-star convergence then need not cross a possible temporal atom.`,
  "Take the positive variation of the clock",
  "The defect-completed matched clock passes both necessary gates: target-shell detection and fixed-scale weak stability.",
  "Defect-completed clock: PROVED",
  String.raw`The defect-completed clock is stable under suitable-weak limits for fixed \(R\) and fixed terminal point; its target-shell component in the matched square function reaches exactly \(T_*\), but an upper bound for the complete square function is still unproved.`,
  "Deterministic analytic figure, not DNS, simulation, singularity evidence, or regularity evidence.",
  "If instead one uses the strongly weighted quantity that closes automatically by Cauchy--Schwarz",
  String.raw`If \(x=|J|/R^2\in(0,1)\), every window satisfies`,
  String.raw`If the complete exterior dissipation is restored, then of course \(X_R^\alpha\) can be controlled. On the exact solution family, for every sufficiently large \(j\), with constants uniform in \(j\), one indeed has`,
  "Rigorous triage of three candidate temporal observables",
  "Previous major-milestone recap (through R0.74O, 157 sections)",
  "The local energy balance for a suitable weak solution need not be an equality. Define the total local dissipation distribution",
  "The Navier--Stokes equation itself must therefore restrict the number, duration, or interaction of simultaneously effective shells. This could take the form of an effective-shell theorem, a scale-packing estimate, or another PDE mechanism connecting the positive variations.",
  String.raw`Both extremes are now known: the \(\ell^1\) ledger is too expensive, while applying \(\gamma_k^{-1/2}\) to the \(\ell^2\) quantity is also too expensive. The unweighted matched \(\ell^2\) quantity lies exactly in the middle where PDE structure is needed.`,
  "Thus what is missing is a structural quantity that distinguishes an average scale from a short-time concentration scale. R0.74P does not simply guess an answer; it screens three candidates in turn: positive-order temporal window mass, energy oscillation, and the defect-completed shell clock.",
  String.raw`It exceeds the target scale by an exponential factor. The finite certificate recomputes the exact ratio of this extra exponent to \(a=2m/3\) as`,
  "It also turns the failure from a vague lack of technique into a testable structural question: can the PDE be shown to allow only finitely many, or packably many, effective shells? This can either be proved or refuted by a new exact family, making it a serious next-stage research target.",
  "Figure package 20/20: FINITE",
  String.raw`Complete \(Y_2\) upper bound: OPEN`,
  "The complete absolute-value ledger gives",
  String.raw`The complete matched square-function upper bound, PDE compression from \(\ell^1\) to matched \(\ell^2\), prescribed-centre scale packing, contraction iteration, and global regularity.`,
  "Complete Chinese reader source",
  "Complete text, dual-implementation certificate, independent audit, and figure package",
  "I screened positive-order temporal windows, energy oscillation, and the defect-completed shell clock. Every fixed positive-order window strictly misses the target scale; energy oscillation merely repackages the endpoint; the defect-completed clock passes both the target-shell detection and fixed-scale suitable-weak stability gates, but the complete matched square-function upper bound remains",
  "The related literature supplies tools for suitable weak solutions, local dissipation, moving cylinders, fixed physical-shell flux, spatial regularity intervals, and quantitative regularity epochs; Yu 2026 is an adjacent preprint on moving windows and scale-defect ledgers. No source replaces the shell-clock proof here. A finite non-hit proves neither novelty nor priority.",
  "Checksums",
  "Research note R0.74P · complete Chinese version",
  "which is the original endpoint quantity.",
  String.raw`Therefore no slightly positive-order window mass can remain weaker than the endpoint and still detect \(T_*\) on this exact family. This is a strict no-go, not a numerical phenomenon.`,
  String.raw`On the target shell \(j\) of the R0.74O exact family, for every sufficiently large \(j\), with constants uniform in \(j\), I prove`,
  String.raw`Under Lin compactness on each compact subcylinder, at fixed radius \(R\), fixed terminal point, if`,
  String.raw`then the smooth trajectories converge uniformly, the moving fields converge in the corresponding strong and weak topologies, and the total dissipation measures converge locally weak-star. The cumulative primitives \(Q,F,K\) for each fixed shell converge uniformly on the closed time interval.`,
  String.raw`This turns the next step from a vague search for temporal information into a precise PDE problem: how can the shellwise \(\ell^1\) flux ledger be compressed into the matched \(\ell^2\) clock?`,
  String.raw`This quantity tries to reward high energy on short temporal windows while penalizing windows that are too short through \((|J|/R^2)^\sigma\). The problem is that the exact family also gives`,
  String.raw`Here the conclusion carrying \(\alpha\) is used only for the smooth exact family, with \(\alpha\in\{M,F\}\), \(z_M=v_R\), and \(z_F=v_R-a_R\). The theorem below for general periodic suitable weak solutions and all compactness conclusions are stated only in Version M, with fixed radius \(R\) and terminal point.`,
  String.raw`The quantifiers matter: for each fixed \(\sigma>0\), the statement holds for every sufficiently large \(j\), with constants uniform in \(j\); it is not uniform as \(\sigma\downarrow0\). Exactly at \(\sigma=0\), the window supremum reduces to`,
  "This is a theorem in Version M for periodic suitable weak solutions in the frozen local setting, but it does not complete the compression: the right side still retains the linear shellwise absolute-flux cost.",
  String.raw`This shows that the matched clock passes through the standard suitable-weak limit. It does not show that the clock is small as \(R\downarrow0\), and it gives no cross-scale compactness.`,
  "This section still does not solve the three-dimensional Navier--Stokes Millennium Problem.",
  String.raw`This is only a lower detection result: the target shell is not erased by square summation. It does not imply that the complete \(Y_{2,R}^{\rm sf}\) has an upper bound \(CT_*\), because the other shells remain.`,
  "The positive variation therefore satisfies",
  String.raw`Positive-order window no-go, the energy-oscillation identity, defect-completed balance, \(\ell^1\) closure, target-shell two-sided scale, and fixed-scale weak lower semicontinuity.`,
  "Rigorous triage of positive-order windows, energy oscillation, and the defect-completed shell clock; the target shell is detected while the complete matched square-function upper bound remains open",
  "Positive-order window miss: PROVED NO-GO",
  "The positive-order-window route is excluded by the exact family.",
  String.raw`The three lines in the formal figure plot only the decay-rate term \(-\min\{\sigma,1\}\log_{10}K_*\). The true upper bound also has an unknown additive intercept \(\log_{10}C\), which the figure and source data explicitly omit. The curves therefore show slopes and asymptotic rates, not absolute vertical values.`,
  String.raw`Prove or disprove the PDE compression from the shellwise \(\ell^1\) flux ledger to the matched \(\ell^2\) clock, and test prescribed-centre scale packing.`,
  "Certificate 52/52: FINITE",
  "Status · R0.74P",
  "The natural weakening is",
  "The Lebesgue differentiation theorem gives the exact identity",
  String.raw`The R0.74O smooth exact family and its \(P_*,X_*,\mathfrak C_*\) scales.`,
  "R0.74O already shows that the original complete scalar payment alone cannot yield the universal sublinear endpoint bound I had hoped for. Along that sequence of smooth, periodic, unforced exact solutions, write",
  "The value of R0.74P is not a quantifiable percentage of progress toward Clay, but the rigorous separation of three routes that are easy to conflate.",
];

process.chdir(root);
const [source, translationOrderSource, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings("./public"),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const currentByZh = new Map(current.map((entry) => [entry.zh, entry]));
const missingBefore = source.filter((entry) => !currentByZh.has(entry.zh));
const missingInTranslationOrder = translationOrderSource.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missingBefore.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => /^r074p\d+$/.test(row.id));
  assert.equal(rows.length, english.length, "R0.74P translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74P English translation drift");
} else {
  assert.equal(missingBefore.length, english.length, "R0.74P source-string count drift");
  const sourceByZh = new Map(missingBefore.map((entry) => [entry.zh, entry]));
  const additions = missingInTranslationOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = english[index];
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), `protected token drift ${index + 1}: ${entry.zh}`);
    return { id: `r074p${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...current, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({ release: "R0.74P", translationPath: translationRoute, dgxUsed, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
