#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074sstep10";

const english = [
  "Study the short non-D, Q-small packing in R_sh and the anomalous-defect / high-Rayleigh ancestry in R_x separately, then test S.243 with one shared fixed-N0 exception budget.",
  "The exact six-class partition places four paid branches under one Q ledger and one cubic ledger; R_sh and R_x share one residual best-N gate, while S.243 remains open. NOT CLAY.",
  "Four paid branches use one Q ledger and one cubic ledger; two residual classes share one best-N gate. S.243 OPEN. NOT CLAY.",
  "Review v1.89 · 2026-09-03",
  "R0.74S Step 10 removes four already-paid branches, leaving only the short non-D, Q-small mechanism and scalar-excess ancestry. The next threshold is to prove S.243 with one shared fixed-N0 budget.",
  "R0.74S: The residual best-N gate after paid-branch deletion",
  "R0.74S｜The residual best-N gate after paid-branch deletion",
  "Study R_sh and R_x separately, then recombine them with one shared fixed-N0 exception budget.",
  "The residual best-N gate after paid-branch deletion",
  "Literature review v1.89 · 2026-09-03",
  "PROVED: a D-first exact six-class partition; P_beta/P_Q share one 6B_Q ledger; P_sigma/P_LE share one C5 ledger; T/6<r<T/2 on R_sh/R_x; a domain-safe best-N reduction; and the plateau and small-payment corollaries. REFUTED / RULED OUT: an extra low-Rayleigh residual, duplicate full ledgers, two N-budgets, automatic terminal-D last-exit persistence, and fixed-N compression from last-exit algebra alone. FINITE: Python 12/12 exact, 10/10 finite, 79/79 structural, and 47/47 mutations; Ruby 9/9 groups, 65,681 cases, 21/21 contract mutations, 13/13 report checks, and 15/15 audit bindings. OPEN: S.243, PDE packing of the two residual mechanisms, Q.12, Q.1, and regularity. The prior no-go remains.",
  "R0.74S Step 10 public boundary",
  "S.223–S.231 give the D-first six-class partition and single Q/cubic payments; S.232–S.240 prove T/6<r<T/2 on the two residual classes and establish the domain-safe best-N equivalence. The fixed-N PDE packing statement S.243 remains open.",
  "Step 10 performs exact branch deletion using the inherited completed clocks, last exits, and local-energy payments; it claims no novelty, priority, or new PDE packing theorem.",
  "Research-note master index · v1.89 · 2026-09-03",
  String.raw`: the canonical \(2/3\)-last exit and fixed profile in (S.223)--(S.224); the exact six-class partition in (S.225); Step 7/8 compatibility in (S.226); the single \(6B_Q\) and single \(C_5\) payments in (S.227)--(S.231); the positive residual and \(T/6<r<T/2\) in (S.232)--(S.234); the fixed-good-terminal/domain-safe best-\(N\) reductions in (S.235)--(S.240); and the plateau corollary and small-payment fallback in (S.241)--(S.242).`,
  String.raw`: \(\mathcal I_x\) can arise only from anomalous-defect or high-Rayleigh shells, and its full-history \(Q\)-variation and kinetic mass are below the Step 8 thresholds. The remaining defect/high-Rayleigh mass requires genuine packing; terminal \(D\)-dominance cannot be converted for free into a payment on the last-exit interval.`,
  String.raw`: an extra low-Rayleigh residual class; the need to charge a complete \(Q\) or cubic ledger twice; separate sets of \(N\) exceptions for the two residual mechanisms; automatic localization of terminal \(D\)-dominance to the last-exit interval; and fixed-\(N\) shell compression from last-exit algebra alone.`,
  String.raw`: a fixed residual estimate (S.243) with \(N_0\) independent of the solution and scale; PDE packing of \(\mathcal R_{\rm sh}\) and \(\mathcal R_x\); full Q.12, Q.1, the R0.74R extraction hypotheses, scale contraction, prescribed-centre packing, and regularity.`,
  String.raw`: the positive stopped flux is comparable to \(T_k\), yet it is generated on a terminal interval shorter than \(R^2\lambda_k^{-3/2}\). A new theorem must use cross-shell PDE information such as spatial crowding, overlap, or a Carleson-type constraint; an ordinary \(\ell^2\) sequence inequality cannot close the gate.`,
  String.raw`: terminal continuity, measurability, or lower semicontinuity of the last-exit selector, branch masks, or residual path; that \(\ell_k\) is a good time; that an infinite last-exit family is an admissible local-energy test; that the Step 8 classes can be redefined on \(J_k^{\rm LE}\); equality of the plateau and full domains; optimization of \(\boldsymbol\lambda\); that the scalar fixtures are NSE solutions; or any novelty, priority, singularity formation, regularity, or Clay conclusion.`,
  String.raw`: the R0.74P canonical clocks, variation ledgers, and \(\ell^1\)-terminal continuity; the R0.74Q fixed-\(N\) reduction; the R0.74R shell-dependent cubic payment; the Step 7 Rayleigh trichotomy; the Step 8 full-history \(\beta/\sigma/x\) partition; and the Step 9 last-exit identity and finite good-stop closure.`,
  String.raw`The \(\ell^2\) bound alone does not imply a fixed-\(N\) \(\ell^1\) tail bound; the final term also has only linear scale when \(P_R^M\) is large.`,
  String.raw`\(\mathcal P_Q\) means absolute-\(Q\)-large, not positive-sign \(Q\). The Step 7 low-Rayleigh branch cannot create a seventh class:`,
  String.raw`\(\mathcal R_x\) and \(\mathcal R_{\rm sh}\) must be combined before taking one best-\(N\) infimum; allowing \(N\) exceptions separately would silently increase the total budget to \(2N\).`,
  String.raw`\[ \boxed{ \text{OPEN: there exist fixed }N_0<\infty,C_{\rm res}<\infty, \text{ such that } \mathfrak R_{N_0,R}^{\boldsymbol\lambda}(\mathcal T_R) \le C_{\rm res}A_R \text{ uniformly for every }R\text{ and solution}.} \tag{S.243} \]`,
  "36. Step 10 question and result",
  "37 / Complete text",
  "37. Canonical 2/3-last exit and fixed profile",
  "38 / Complete text",
  "38. D-first six-class partition and genealogy",
  "39 / Complete text",
  "39. One Q ledger and one cubic ledger",
  "40 / Complete text",
  "40. Residual vector and sharp comparison",
  "41 / Complete text",
  "41. Best-N reduction after paid-branch deletion",
  "42 / Complete text",
  "42. Plateau corollary, full gate, and fallback",
  "43 / Complete text",
  "43. Sharpness, exception budget, and D-persistence no-go",
  "44 / Complete text",
  "44. Route decision",
  "45 / Complete text",
  "45. Step 10 claim boundary and dual audit",
  "46 / Complete text",
  "Combine the inherited plateau reduction with (S.238):",
  String.raw`Bounding the two branches separately by the complete global ledger would charge \(C_5\) twice; this step does not do so.`,
  String.raw`Retain the periodic suitable-weak Version-M setting, the full clock interval \(\mathcal T_R=(s_R,t_0)\), the plateau interval \(I_R\), the good-time set \(\mathcal G_R\), and`,
  String.raw`This step proves an exact reduction. It does not prove that there is a fixed \(N_0\), independent of the solution and scale, for which the residual tail has a quadratic bound; nor does it prove Q.12, Q.1, regularity, or a Clay conclusion.`,
  "The answer is an exact six-class partition. The four paid classes together require only",
  "Define the residual stopped-flux vector",
  String.raw`For \(\mathcal D\in\{I_R,\mathcal T_R\}\), define the good-terminal residual gate`,
  String.raw`For \(\mathcal P_\beta\), Step 8 gives \(T_k\le6\beta_k(J_\tau)\); for \(\mathcal P_Q\), the definition gives \(T_k\le6|\Delta Q_k|\). The two classes lie in disjoint \(D\) and non-\(D\) shell sets, so sum first and then enlarge to the complete variation ledger:`,
  String.raw`For \(\mathcal P_\sigma\), use \(J_\tau\); for \(\mathcal P_{\rm LE}\), use its corresponding \(J_k^{\rm LE}\). Apply finite-shell Holder on their union, then invoke the shell-dependent-time-set estimate (R.211) only once to obtain`,
  String.raw`For a nonnegative \(\ell^1\) vector, define`,
  String.raw`For every common exceptional set \(S\), the four paid classes and the residual comparison give`,
  String.raw`Conversely, coordinatewise \(r\le K/2\) and the same exceptional set give`,
  String.raw`Study the short non-\(D\), \(Q\)-small packing and the anomalous-defect / high-Rayleigh scalar-excess ancestry separately, then recombine them with one shared fixed-\(N_0\) exception budget and test (S.243).`,
  String.raw`Fix \(\tau\in\mathcal G_R\cap\mathcal T_R\). If \(T_k=K_{k,R}(\tau)>0\), take the last time satisfying \(K\le2T_k/3\), denoted by \(\ell_k\), and write`,
  String.raw`Fix a positive deterministic profile \(\boldsymbol\lambda\), independent of \(R,\tau\), and the solution, satisfying`,
  String.raw`Let \(\mathcal I_{\rm pay}\) be the union of the four paid classes and \(\mathcal I_{\rm res}=\mathcal R_{\rm sh}\cup\mathcal R_x\) the union of the two residual classes. Then`,
  String.raw`continues to exclude only scalar completed-clock algebra and unweighted genealogy; the Step 8 no-go comes from an inherited genuine smooth exact NSE family, and the Step 9 no-gain shows that canonical stops alone do not compress. Step 10 proves that the four paid classes together use only one \(6B_Q\) ledger and one \(C_5\) cubic ledger. The remainder on \(\mathcal R_{\rm sh}\cup\mathcal R_x\) is exactly the shared best-\(N\) residual gate, with \(T_k/6<r_k<T_k/2\). This is a domain-safe reduction, not a residual packing theorem. The estimate (S.243) with fixed \(N_0\) independent of scale and solution, Q.12, Q.1, scale contraction, regularity, and singularity formation remain`,
  String.raw`Absolute \(F\)-variation gives the linear fallback:`,
  String.raw`Of the seven \(B_Q\) units, six come from the paid partition and one from the terminal \(K\)-to-flux reduction. This formula holds only on the plateau domain, not for full-terminal Q.12.`,
  String.raw`The \(Q\) row is charged only once as \(6B_Q\), while \(\mathcal P_\sigma\) and \(\mathcal P_{\rm LE}\) are combined before Holder and charged only once by the \(C_5\) cubic ledger. The two remaining residual mechanisms are the short non-\(D\), \(Q\)-small class \(\mathcal R_{\rm sh}\), and the Step 8 scalar-excess class \(\mathcal R_x=\mathcal I_x\). They share one best-\(N\) exception budget and may not each delete \(N\) coordinates.`,
  "After extending by zero globally,",
  String.raw`Every candidate estimate must pass (S.245)--(S.247) and retain the inherited R0.74O/P exact-family boundary: that exact family only refutes the no-exception gate and does not prove that \(N_0=1\) is sufficient.`,
  String.raw`If (S.243) holds, then (S.238) gives full Q.12, and inherited Q.9 then gives Q.1. A residual bound proved only on \(I_R\) can give plateau Q.1 directly, but it cannot be upgraded to full Q.12.`,
  String.raw`If \(k\in\mathcal P_{\rm LE}\), then \(D_k(t)\le D_k(\tau)<T_k/2\) and \(K_k(t)>2T_k/3\) imply, for almost every good time on the last-exit interval,`,
  String.raw`If \(T_k=0\), set \(\ell_k=\tau\), \(d_k=0\), and the residual coordinate to zero. The time \(\ell_k\) need not be good; only continuity of \(K_k\) is used.`,
  "After paid-branch deletion, the complete clock tail reduces exactly to one best-N gate shared by two residual mechanisms; S.243 remains open",
  String.raw`Four paid branches use one \(Q\) ledger and one cubic ledger; the two remaining mechanisms share one residual best-\(N\) gate.`,
  String.raw`The need for one shared exception budget follows from \(T_1=T_2=3\) and \(r_1=r_2=1\):`,
  "Paid-branch deletion, two residual mechanisms, and one shared best-N gate",
  "The six-class partition, single-ledger payment, and domain-safe reduction are complete; the PDE packing statement S.243 remains open and is not DNS or evidence of singularity or regularity.",
  String.raw`Thus the small-payment regime is closed. When \(P_R^M>1\), the linear fallback still misses the target by \((P_R^M)^{1/3}\). The genuinely open full-domain statement is`,
  String.raw`Therefore, for fixed \(N_0\) independent of the solution and scale,`,
  String.raw`Thus, from \(|\Delta Q|<T/6\) alone, the coefficient six and the upper bound one half are limiting-sharp; equality \(|\Delta Q|=T/6\) belongs to the paid class \(\mathcal P_Q\). These are clock-algebra tests, not NSE solutions.`,
  "Take a limit through the same sets approaching the residual infimum to obtain the fixed-good-terminal theorem",
  String.raw`The right-hand expression is invalid because it spends one exception on each residual label. A fixed \(N\) also cannot be replaced by a truncation-dependent budget:`,
  String.raw`On \(\mathcal R_{\rm sh}\), \(|\Delta Q_k|<T_k/6\) holds by definition; on \(\mathcal R_x=\mathcal I_x\), the failed Step 8 \(\beta\)-test gives the same strict bound. Together with \(\Delta F=T/3-\Delta Q\), both residual classes satisfy`,
  String.raw`At the abstract continuous-clock level, take \(T=1\), \(0<\varepsilon<1/6\), and set`,
  String.raw`Among positive-terminal shells, use \(d_k\gtreqless\lambda_k^{-3/2}\), \(|\Delta Q_k|\gtreqless T_k/6\), and \(D_{k,R}(\tau)\gtreqless T_k/2\) to split into long/short, \(Q+\)/\(Q-\), and \(D\)/non-\(D\). Equality is assigned to the long, absolute-\(Q\)-large, and \(D\)-dominated sides.`,
  "This equivalence removes the known payments but does not turn the residual gate into a theorem; it identifies exactly where new PDE information is still required.",
  String.raw`Here \(\mathcal I_\beta,\mathcal I_\sigma,\mathcal I_x\) remain defined on the complete \(J_\tau=(s_R,\tau)\) and cannot be rewritten on the last-exit interval. Define, in D-first priority order,`,
  String.raw`At the possibly non-good time \(\ell_k\), no value of \(E_k,D_k\) is taken. Combining this with the inherited padded-shell estimate gives`,
  String.raw`This is a genealogy and no-double-charge conclusion, not a new payment for \(\mathcal I_x\); it may still come from the anomalous-defect or high-Rayleigh branch.`,
  String.raw`This strictly rules out inserting \(\mathcal I_D\) directly into the long non-\(D\) persistence proof; the Step 8 full-history trichotomy must remain. The witness is still only a continuous-clock stress test.`,
  String.raw`The correct coefficient is one \(6B_Q\), not two \(6B_Q\).`,
  String.raw`Use only the terminal \(K\)-vector's inherited \(\ell^1\)-continuity to extend the left-hand side from dense good times to all terminal times; do not use continuity of the residual path, selector, or masks:`,
  "The primary certificate passes 12/12 exact, 10/10 finite, 79/79 structural, and 47/47 negative mutations. The independent Ruby audit passes 9/9 groups, 65,681 cases, 21/21 contract mutations, 13/13 report checks, and 15/15 audit bindings; the deterministic stdout SHA-256 is `4877dc3a0de2c2f605641736c7355672f0a7a68cb97a37849d4a7c28495e8bbd`. The main-text SHA-256 is `9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c`. Finite certificates do not replace the inherited local-energy/PDE analysis.",
  "Status · R0.74S STEP 10",
  String.raw`Finally, terminal \(D\)-dominance cannot be localized for free into last-exit persistence. Take the explicit rational piecewise-linear clock with \(R^2=1,s_R=0,\tau=2,T=1\), last exit \(\ell=1/4\), and \(D(t)=3/5\) constant on the later segment; then`,
  "Paid-branch deletion has reached its natural endpoint. The next PDE stage should study the two residual mechanisms separately, but must ultimately recombine them with one shared exception budget:",
  String.raw`R0.74S Steps 1--6 separately sealed one-sided ball completion, the terminal Abel identity, four-channel circular recombination, and the abstract scalar no-go for unweighted genealogy; Step 7 paid the low-Rayleigh dissipation branch, Step 8 strictly refuted the universal no-exception stopped-work quadratic bound, and Step 9 proved that the canonical last exit is only an exact representation of the fixed best-\(N\) terminal tail. Step 10 further removes every shell already paid by the \(Q\)-variation or velocity-cubic ledger and locates the two genuinely remaining residual mechanisms.`,
  "Step 10 independent audit",
  "Step 10 machine-certificate JSON",
  "Step 10 certificate report",
  "Step 10 primary audit",
  "Step 10 final analytic main text",
  "Step 10: Python 12/12 exact, 10/10 finite, 79/79 structural, and 47/47 mutations; Ruby 9/9 groups, 65,681 cases, 21/21 contract mutations, 13/13 report checks, and 15/15 audit bindings. Finite certificates do not replace the inherited local-energy/PDE analysis.",
  "The Step 8 full-history priority partition remains unchanged:",
  String.raw`Step 9 showed that the canonical last exit only represents the R0.74Q best-\(N\) terminal tail and does not compress it by itself. Step 10 asks a narrower question: after deleting every shell already paid by the quadratic \(Q\)-variation ledger or velocity-cubic ledger, what remains of the canonical \(2/3\)-last-exit tail?`,
  "Step 9 main text",
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
  assert.equal(rows.length, english.length, "R0.74S Step 10 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74S Step 10 English translation drift");
} else {
  assert.equal(missingBefore.length, english.length, "R0.74S Step 10 source-string count drift");
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

process.stdout.write(`${JSON.stringify({ release: "R0.74S Step 10", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
