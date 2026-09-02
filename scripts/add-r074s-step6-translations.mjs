#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074sstep6";

// Deterministic direct translations in collectSiteStrings order. All protected
// mathematical and release-boundary tokens are preserved byte-for-byte.
const english = [
  "Test a PDE-paid quantity that sees block length or signed transport, prioritizing a return to the dissipation-dominated branch.",
  "The full signed recombination exactly returns the original increment; the three-channel recombination only concentrates the debt into a terminal ℓ¹ residual. The one-block scalar no-go is not a PDE/NSE counterexample. NOT CLAY.",
  "The full signed recombination is circular; the positive three-channel result still stops at a terminal ℓ¹ residual. The one-block scalar no-go is not a PDE/NSE counterexample. NOT CLAY.",
  "One-sided ball clock → four-channel circular recombination → three-channel terminal genealogy → abstract scalar no-go",
  "R0.74S proves that the four-channel signed recombination exactly returns the original stopped increments. After separating the mismatch, the three-channel recombination removes temporal debts, but the terminal term remains block root plus ℓ¹ residual. A one-block scalar family gives an N/√N no-go; PDE-weighted genealogy and dissipation payment remain open.",
  "R0.74S: Cross-channel recombination and terminal ℓ¹ debt",
  "R0.74S｜Cross-channel recombination and terminal ℓ¹ debt",
  "Four-channel circular recombination, three-channel terminal decomposition, and abstract scalar no-go",
  "The four-channel and genealogy identities use this project's frozen notation. No general NSE theorem, novelty, or priority is claimed here.",
  "The full signed recombination exactly returns the original stopped increments. After separating the mismatch, the three-channel recombination removes the start/merge temporal debts, but the terminal term remains one root-boundary per block plus the ℓ¹ mass of all nonnegative shell residuals. A one-block scalar family excludes compression by unweighted genealogy.",
  "Next, test a PDE-paid quantity that sees block length or signed transport, prioritizing a return to the dissipation-dominated branch.",
  "PDE-weighted genealogy or dissipation payment",
  "PROVED: the full signed recombination exactly returns the original stopped increments, so the linear route is circular; the three-channel decomposition removes every start/merge temporal debt and leaves block-root plus shell-residual ℓ¹ mass. NO-GO: a one-block, one-activation, zero-merger abstract scalar family excludes only matching payment of the work by unweighted component/epoch/merger count. FINITE: Step 6 Python 4/4, 8/8, 58/58, and 10/10; Ruby 9/9 and 8/8, with cross-check PASS. OPEN: PDE-weighted genealogy, Q.1, regularity, and singularities.",
  "Why does cross-channel recombination still leave a terminal ℓ¹ debt?",
  ", and is not a PDE counterexample.",
  "; PDE-weighted block length, dissipation payment, and cross-channel dynamical signs may still work.",
  "10. Certificate and independent audit",
  "11. Decision and next threshold",
  "12. Inherited boundaries",
  "7. Four-channel signed recombination exactly returns the original problem",
  "8. The positive three-channel result after separating the mismatch",
  "9. A one-block scalar family excludes unweighted genealogy compression",
  String.raw`This section closes two adjacent independent algebraic routes: separately estimating every positive completion gives only \(\ell^1\); retaining all signs and recombining linearly exactly returns the original unknown. Unweighted component/epoch/merger counts cannot repair the gap either.`,
  "One-block no-go: PROVED ABSTRACT",
  "An abstract scalar no-go from the one-block family and finite genealogy counts.",
  String.raw`For \(X\in\{E,D,Q,F,K\}\), combine the root, outer, weight-drop, and mismatch rows according to their stopped-time orientations into \(\mathfrak C_X\). The finite-block decomposition and cutoff linearity give`,
  String.raw`The quadratic \(Q\) row has already been paid by \(CA_R\), but the terminal upcrossing satisfies exactly`,
  "Cross-channel recombination, terminal ℓ¹ debt, and the abstract no-go",
  String.raw`Let \(\Omega_A^R\) be the genealogy cutoff obtained by subtracting the internal boundary bumps from the padded shells. Exact support geometry proves \(\Omega_A^R\ge0\), and the cutoff increases monotonically when a new shell is inserted. For the three-channel stopped work \(W_{R,3}^M\), every start and merge clock cancels, giving`,
  String.raw`Take \(I_N=\{1,\ldots,N\}\), activate every shell at the same time, set the boundary clocks to zero, let \(K_{k,R}=F_{k,R}=h\), \(Q=D=0\), and construct the ball clocks recursively from the tower identity. Every scalar completed-clock identity holds term by term, and`,
  "Any viable next step must add a PDE-paid quantity that sees block length or signed transport. One concrete entrance is to return to the dissipation-dominated branch and test whether a positive measure can pay for weighted genealogy.",
  String.raw`remains \(O(|I|)\), rather than a dimension-free square-function bound. This conclusion excludes only`,
  "The three-channel genealogy cutoff is nonnegative, insertion has the favorable sign, and the terminal block decomposition is exact;",
  "Three-channel genealogy: PROVED",
  "Four-channel circular recombination, three-channel genealogy terminal ℓ¹ debt, and abstract scalar no-go",
  String.raw`The four-channel signed recombination exactly returns the original stopped increments. After separating the mismatch, the three-channel recombination removes the temporal genealogy debt, but the terminal term remains root-boundary plus \(\ell^1\) residual.`,
  "Four-channel signed recombination exactly reconstructs the stopped increments, proving that this route is circular;",
  "Four-channel recombination: PROVED / CIRCULAR",
  String.raw`In particular, when \(X=F\), \(\mathfrak C_F=W_R^M\), while \(F=K-Q\) gives`,
  "Next, test only a PDE-paid quantity that sees block length or signed transport, prioritizing a return to the dissipation-dominated branch; do not retry linear recombination or unweighted genealogy.",
  String.raw`Thus component, epoch, or merger count alone cannot perform the \(\ell^1\to\ell^2\) compression. The exact finite genealogy count is`,
  "Therefore the full signed recombination does not reduce the difficult term; it exactly reconstructs the object to be controlled. This is",
  String.raw`Here \(\Phi_I=\mathscr K_R[\Omega_I^R]\). If the final block is \([a,b]_{\mathbb Z}\), write \(r_m=K_{m,R}-K_{m,R}^{\partial}\ge0\); then the terminal quantity has the exact nonnegative decomposition`,
  String.raw`This is the retained positive result: the three-channel recombination removes the temporal genealogy debt; the remaining obstruction is localized to each final block's root-boundary clock and complete \(\ell^1\) residual, rather than to the stopping times themselves.`,
  "Terminal ℓ¹ decomposition: PROVED",
  String.raw`Finally, a smooth abstract clock tower makes the stopped work equal to \(N\), while the square function equals only \(\sqrt N\), using one activation epoch, one active block, and zero mergers. Therefore completed-clock positivity, cutoff linearity, tower identities, and unweighted genealogy complexity alone cannot yield the required \(\ell^2\) compression. This is an`,
  "Step 5 analytic main text",
  "The final deterministic Step 5 certificate passes:",
  "Step 5: 5/5 exact, 7/7 finite, 55/55 structural, and 4/4 mutations. Step 6: Python 4/4 exact, 8/8 finite, 58/58 structural, and 10/10 mutations; Ruby 9/9 independent and 8/8 mutations. Finite certificates do not replace the analytic proof.",
  "Step 6 independent audit",
  "Step 6 analytic main text",
  String.raw`Step 6 retains all four channel signs for exact recombination. The result is not a new estimate: the complete root, outer, weight-drop, and mismatch rows exactly reconstruct the original stopped shell increment, so the linear route is circular. After separating the mismatch, the three-channel recombination does remove every start/merge temporal debt, but the terminal term is still exactly one root-boundary clock per final block plus the \(\ell^1\) mass of all nonnegative shell residuals.`,
  "Step 6 primary audit",
  "The Step 6 primary certificate additionally passes 4/4 exact, 8/8 finite, 58/58 structural, and 10/10 mutations. The independent Ruby implementation passes 9/9 independent and 8/8 mutations and agrees with the producer cross-check. All nine forged JSON classes are rejected.",
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
  assert.equal(rows.length, english.length, "R0.74S Step 6 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74S Step 6 English translation drift");
} else {
  assert.equal(missingBefore.length, english.length, "R0.74S Step 6 source-string count drift");
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

process.stdout.write(`${JSON.stringify({ release: "R0.74S Step 6", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
