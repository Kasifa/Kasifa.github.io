#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074s7";

const english = [
  "The low-Rayleigh dissipation clocks are simultaneously paid by (P_R^M)^(2/3); the high-Rayleigh and anomalous-defect residuals remain open. NOT CLAY.",
  "The low-Rayleigh clocks are simultaneously paid by (P_R^M)^(2/3); high-Rayleigh and anomalous defect remain open. NOT CLAY.",
  "The low-Rayleigh class of dissipation-dominated clocks has parabolic kinetic time mass and is simultaneously paid by (P_R^M)^(2/3); the high-Rayleigh and anomalous-defect residuals remain open. NOT CLAY.",
  "Test only a PDE payment or a uniform finite-exception theorem for the high-Rayleigh viscous residual and the anomalous-defect residual.",
  "Review v1.86 · 2026-09-02",
  "abstract scalar no-go → dissipation trichotomy → low-Rayleigh kinetic mass → all-shell quadratic payment → two open residuals",
  "R0.74S rigorously pays the low-Rayleigh class of dissipation-dominated clocks; the remaining terms are the high-Rayleigh viscous residual and the anomalous-defect residual. The next threshold is a PDE payment or a uniform finite-exception theorem, not another scalar clock identity.",
  "R0.74S: The low-Rayleigh dissipation branch is paid",
  "R0.74S｜Quadratic payment for the low-Rayleigh dissipation branch",
  "R0.74S｜Low-Rayleigh dissipation branch paid",
  "Parabolic kinetic mass and quadratic payment for the low-Rayleigh dissipation branch",
  "The dissipation-dominated clocks split exactly into defect, high-Rayleigh, and low-Rayleigh classes; the low class is simultaneously paid by (P_R^M)^(2/3). The Step 6 abstract scalar no-go is retained in its original scope.",
  "Literature review v1.86 · 2026-09-02",
  "The next step tests only a PDE payment or a uniform finite-exception theorem for the two residuals; the conditional interface must not be presented as a completed conclusion.",
  "high-Rayleigh and anomalous-defect residuals",
  "PROVED: the one-eighth/one-eighth/one-quarter trichotomy for dissipation-dominated clocks; low-Rayleigh kinetic mass, Jensen, and the all-shell (P_R^M)^(2/3) payment; and the exact residual ledger. CONDITIONAL ONLY: if a future theorem uniformly controls the number of high-Rayleigh and defect exceptions, the square function pays the remaining clocks. FINITE: Step 7 Python 16/16, 8/8, 52/52, and 9/9; Ruby 6/6 groups, 31/31, and 9/9, with a passing cross-check. OPEN: high-Rayleigh, anomalous defect, Q.1, regularity, and singularities. The Step 6 abstract scalar no-go still excludes only unweighted genealogy.",
  "Step 7 uses the inherited suitable-weak dissipation split and padded-shell cubic payment; it states no general regularity theorem and claims no novelty or priority.",
  "Quadratic payment for the low-Rayleigh dissipation branch",
  "Research-note master index · v1.86 · 2026-09-02",
  "; this step proves no uniform finite-exception bound and does not derive (Q.1).",
  ". This step gives only their exact residual ledger and the",
  String.raw`. The inherited smooth high-frequency shear shows that high-Rayleigh time sets can occur, but that shear is itself paid by the existing \(Q\)-ledger and is not a counterexample to the theorem.`,
  "10. Exact local-dissipation split and Rayleigh time sets",
  "11. The one-eighth, one-eighth, one-quarter trichotomy",
  "12. All-shell low-Rayleigh quadratic payment",
  "13. Unclosed residuals and the conditional finite-exception interface",
  "14. High-frequency shear diagnostic and strict boundary",
  "15 / Complete text",
  "15. Certificate and independent audit",
  "16 / Complete text",
  "16. Decision and next threshold",
  "17 / Complete text",
  "17. Inherited boundaries",
  "18 / Complete text",
  "The one-eighth/one-eighth/one-quarter priority trichotomy;",
  String.raw`Restrict the R0.74R padded-shell cubic payment to each shell's own \(L_{k,R}\):`,
  String.raw`After setting the representatives to zero on their common null set, both rows are measurable. At a good terminal time \(\tau\), the dissipation clock splits exactly as`,
  "Retain the suitable-weak total local-dissipation measure from R0.74P",
  "This step first splits the local-dissipation clock exactly into viscous dissipation and anomalous defect, then applies the following priority trichotomy: anomalous defect carries at least one eighth of the terminal clock; high-Rayleigh viscous dissipation carries at least one eighth; otherwise low-Rayleigh viscous dissipation carries more than one quarter. Parabolically normalized kinetic time mass, Jensen's inequality, and the inherited padded-shell cubic payment then give the third class",
  String.raw`The constant sequence \(\lambda_k=1\) is admissible; \(\lambda_k=\gamma_k^{-\alpha}\) is admissible for \(0\le\alpha<1/3\); and the near-critical sequence`,
  "The earlier",
  String.raw`But this shear has flux clock \(F_{k,R}=0\), hence \(K_{k,R}=Q_{k,R}\), and its completed clocks are already paid by the inherited \(Q\)-variation ledger. It shows only that the high-Rayleigh time set is nonempty; it is not a counterexample to the low-Rayleigh theorem or the completed-clock estimate, and it does not automatically place the shell in the priority class \(\mathcal I_{\rm hi}\).`,
  String.raw`When the denominator and \(\eta_R\) are positive, this is equivalent to the cutoff-weighted ratio`,
  String.raw`Low-Rayleigh kinetic time mass, Jensen conversion, and all-shell \((P_R^M)^{2/3}\) payment;`,
  "Parabolic kinetic mass, all-shell quadratic payment, and the unclosed residuals of the low-Rayleigh dissipation branch",
  "Low-Rayleigh all-shell payment: PROVED",
  String.raw`For a dissipation-dominated shell, write \(T_k=K_{k,R}(\tau)>0\) and \(D_{k,R}(\tau)\ge T_k/2\). Define the defect, high, and low classes in priority order:`,
  "For each shell, define the kinetic and viscous density rows",
  "Anomalous-defect residual: OPEN",
  "The high-Rayleigh and anomalous-defect branches remain",
  "High-Rayleigh residual: OPEN",
  "Smooth high-frequency shear diagnostic: inherited from R0.73Y and R0.74B, PROVED in its stated scope.",
  String.raw`gives \(\mathscr L=2^{-3\varepsilon}/(1-2^{-3\varepsilon})\). At the critical value \(\varepsilon=0\), every summand equals 1 and the series diverges. This is only the sequence-space boundary of the argument, not a Rayleigh profile automatically obeyed by arbitrary solutions.`,
  "Exact dissipation split: PROVED",
  "Dissipation trichotomy, low-Rayleigh payment, and open residuals",
  String.raw`The dissipation-dominated clocks split exactly into defect, high-Rayleigh, and low-Rayleigh classes; the low class has parabolic kinetic time mass and is simultaneously paid by \((P_R^M)^{2/3}\).`,
  "The complete residual ledger for the dissipation-dominated family is",
  "Machine certificate JSON",
  "The inherited smooth periodic shear",
  "continues to exclude only scalar completed-clock algebra and unweighted genealogy; it is not a PDE/NSE counterexample. Unconditional stopped-work estimates, the universal persistence input of R0.74R, the fixed-scale inequality, scale contraction, regularity, and singularity formation remain",
  "Combining spatial Holder with the preceding section first gives the per-shell estimate",
  String.raw`Let \(\delta_{k,R}=|L_{k,R}|/R^2\). The frozen time window gives only \(0<\delta_{k,R}\le4\), but this already suffices for Jensen to give`,
  String.raw`satisfies \(\rho_{k,R}^{(N)}/(R^2N^2)\to1\) for a fixed cutoff. Thus, for a fixed threshold and sufficiently high frequency, the high-Rayleigh time set can occur at every active time; this residual cannot simply be deleted.`,
  "The exact viscous/defect dissipation split and measurable low/high-Rayleigh time sets;",
  String.raw`where \(m_{k,R}\) is the anomalous-defect part. Given a positive sequence \(\boldsymbol\lambda=(\lambda_k)\), define directly`,
  "The remaining low-Rayleigh class satisfies the exact strict inequalities",
  String.raw`A thinner time set does not damage this step: at fixed kinetic time mass it increases the \(L_t^{3/2}\) row. What is proved is integrated mass, not uniform time thickness.`,
  "Priority trichotomy: PROVED",
  String.raw`The primary definition does not divide; when the denominator vanishes both rows vanish, so there is no \(0/0\) convention.`,
  String.raw`then Cauchy--Schwarz immediately bounds the remaining clocks by \(\sqrt{N_D}Y_{2,R}^{\rm sf}\). This is a`,
  "No exceptional shell and no new signed cancellation are needed here. The conclusion is a rigorous simultaneous quadratic payment over all shells, but only for the low-Rayleigh dissipation branch; it does not give a uniform positive measure for the low-Rayleigh time set.",
  String.raw`This inequality hides no additional \(\ell^1\) clock remainder, but it also does not control the last two terms. If a future PDE theorem proves`,
  "Test only a PDE payment or a uniform finite-exception theorem for the high-Rayleigh viscous residual and the anomalous-defect residual; do not present the conditional interface as a completed conclusion.",
  String.raw`Whenever \(\mathscr L(\boldsymbol\lambda)<\infty\), cross-shell Holder and the inherited nonnegative payment give`,
  "Chinese reader source",
  "The admissible/critical Rayleigh-profile boundary, exact residual ledger, and conditional finite-exception implication.",
  "R0.74S Steps 1--6 separately sealed one-sided ball completion, the terminal Abel identity, four-channel circular recombination, and the abstract scalar no-go for unweighted genealogy. Step 7 returns to the dissipation-dominated branch of the R0.74R trichotomy and proves a new positive result.",
  "Dynamical control of root/outer/weight-drop, the high-Rayleigh/defect residuals, the R0.74R persistence hypotheses, the unconditional fixed-scale inequality (Q.1), scale contraction, regularity, singularity formation, and the Clay problem all remain",
  "Shell-dependent cubic payment and padded-shell Holder: inherited from R0.74R, PROVED;",
  "Step 6 main text",
  "Step 7 independent audit",
  "Step 7 analytic main text",
  "Step 7 rigorously proves simultaneous quadratic payment for the low-Rayleigh dissipation branch, the exact residual ledger, and the conditional finite-exception implication. The high-Rayleigh branch, anomalous-defect branch, stopped-work depletion, arbitrary-clock extraction, (Q.1), scale contraction, and regularity remain",
  "Step 7 has closed the low-Rayleigh part of the dissipation-dominated family. The next step should test only whether PDE structure pays the high-Rayleigh viscous residual and anomalous-defect residual, or proves a uniform finite-exception theorem; the conditional interface must not be stated as a completed theorem.",
  "Step 7 primary audit",
  "The Step 7 primary certificate passes 16/16 exact, 8/8 finite, 52/52 structural, and 9/9 negative mutations. The independent Ruby path passes 6/6 groups, 31/31 structural, and 9/9 adversarial mutations, and agrees with the producer cross-check. The main-text SHA-256 is `e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3`.",
  "Step 7: Python 16/16 exact, 8/8 finite, 52/52 structural, and 9/9 mutations; Ruby 6/6 groups, 31/31 structural, and 9/9 adversarial, with a passing producer cross-check. Finite certificates do not replace the analytic proof.",
  "Suitable-weak dissipation measure and completed shell clocks: inherited from R0.74P, PROVED;",
];

process.chdir(root);
const [source, translationOrderSource, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings("./public"),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);
const baseCurrent = checkOnly ? current : current.filter((row) => !rowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missingBefore = source.filter((entry) => !currentByZh.has(entry.zh));
const missingInTranslationOrder = translationOrderSource.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missingBefore.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => rowPattern.test(row.id));
  assert.equal(rows.length, english.length, "R0.74S Step 7 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74S Step 7 English translation drift");
} else {
  assert.equal(missingBefore.length, english.length, "R0.74S Step 7 source-string count drift");
  const sourceByZh = new Map(missingBefore.map((entry) => [entry.zh, entry]));
  const additions = missingInTranslationOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = english[index];
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), `protected token drift ${index + 1}: ${entry.zh}`);
    return { id: `${prefix}${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...baseCurrent, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({ release: "R0.74S Step 7", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
