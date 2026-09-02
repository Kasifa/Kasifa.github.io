#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074s9";

const english = [
  "Define and audit the forced PDE residual tail after removing the Step 7 low-Rayleigh and Step 8 I_beta/I_sigma paid branches; pay at most N0 terminal-dependent exceptions by sqrt(N0)Z_R.",
  "Research note R0.74S · 2026-09-03",
  "Review v1.88 · 2026-09-03",
  "F-half-exit = 1/2 signed best-N tail; K-last-exit is equivalent within the sharp B_Q error. Canonical stops give no new quadratic compression. NOT CLAY.",
  "F-half-exit = 1/2 signed tail; K-last-exit differs only by the sharp B_Q. Canonical stops give no new quadratic compression. NOT CLAY.",
  "The F-half-exit is exactly one half of the signed best-N tail; the K-last-exit is equivalent only within the sharp B_Q. Canonical stops give no new quadratic compression. NOT CLAY.",
  "R0.74S Step 9 proves that canonical best-N last exits are exact representations of terminal tails, not new quadratic compression. The next threshold is the forced PDE residual tail after the Step 7/8 paid branches are removed.",
  "R0.74S: Canonical best-N last-exit equivalence and no-gain",
  "R0.74S｜Canonical best-N last-exit equivalence and no-gain",
  "After removing the Step 7 low-Rayleigh and Step 8 I_beta/I_sigma paid branches, define and audit the forced PDE residual tail.",
  "Literature review v1.88 · 2026-09-03",
  "Canonical best-N last-exit equivalence and no-gain",
  "PROVED: W_half=(1/2)S_N^F; W_theta^K and (1−theta)S_N^K differ only by the sharp B_Q; finite positive-terminal good-stop closure for theta<3/4; the distinction between full Q.12 and the weaker plateau restriction; and the no-gain equivalence for canonical last exits. FALSE: F-half-exits automatically satisfy S.25. RETAINED: the Step 8 no-exception no-go and the conditional implication S.38. FINITE: Python 9/9, 8/8, 57/57, and 18/18; Ruby 12/12 groups, 91,396/91,396 cases, 49/49 structural, 21/21 source mutations, 15/15 artifact mutations, and 6/6 report checks. OPEN: the forced PDE residual tail after paid branches, a fixed-N0 tail bound, Q.1, and regularity.",
  "R0.74S Step 9 public boundary",
  "S.200–S.207 give the exact signed half-exit representation; S.210–S.214 give the K-last-exit comparison with one sharp B_Q; S.218 proves that canonical stops are equivalent to the existing best-N tail and give no new quadratic compression.",
  "Step 9 constructs canonical last-exit representations in the inherited completed-clock algebra; it claims no novelty, priority, or new PDE packing theorem.",
  "Research-note master index · v1.88 · 2026-09-03",
  String.raw`, not a PDE tail estimate. A fixed best-\(N_0\) PDE bound, the R0.74R extraction inputs, the fixed-scale inequality, scale contraction, regularity, and singularity formation remain`,
  ", while the conditional implication S.38 remains",
  String.raw`: terminal-domain separation and best-\(N\) tails in (S.200)--(S.203); the exact signed half-exit representation in (S.204)--(S.207); the plateau reduction (S.208); the S.25 failure counterexample (S.209); the \(K\)-last-exit, sharp one-\(B_Q\) error, and finite good-stop closure for \(\theta<3/4\) in (S.210)--(S.215); the plateau reduction, \(F/K\) tail comparison, and no-gain equivalence in (S.216)--(S.218); and the quantifier, cancellation, plateau, and \(\theta=2/3\) stress tests in (S.219)--(S.222).`,
  String.raw`: a fixed \(N_0\), independent of the solution and scale, giving a quadratic bound for either best-\(N_0\) PDE tail in (S.218); the residual full tail after the paid branches; (Q.1), the R0.74R extraction hypotheses, scale contraction, prescribed-centre packing, and regularity.`,
  String.raw`: that F-half-exits satisfy S.25; that the canonical selector is continuous in the terminal time; that one infinite stopped cutoff is directly admissible as a local-energy test; that an arbitrary subset supremum may replace the forced full tail; that \(\sup\inf\) may be exchanged with \(\inf\sup\); that the plateau and full domains are equal; that one dominant packet proves \(N_0=1\); that the scalar stress tests are PDE solutions; or any novelty, priority, singularity formation, or Clay conclusion.`,
  ". Canonical last exits give no new quadratic compression; this is a rigorous conclusion in the completed-clock algebra:",
  String.raw`(S.219) uses the two terminal states \(x(\tau_1)=(1,0)\) and \(x(\tau_2)=(0,1)\) to prove`,
  String.raw`(S.220) uses \(F(\tau)=(1,-1)\) and \(N=0\) to show that the forced signed tail is zero, whereas an arbitrary subset supremum selects the positive coordinate and gives \(1/2\); the latter destroys the cancellation that must be retained.`,
  String.raw`(S.221) takes \(M>N\) simultaneous completed clocks with \(K_k=F_k=h\) and \(Q_k=0\). At the plateau terminal time,`,
  String.raw`\(\theta=2/3\) is compatible with the one-sixth rows of Step 8:`,
  String.raw`The \(F\)-half-exit is exactly one half of the signed best-\(N\) tail; the \(K\)-last-exit is equivalent only within one sharp \(B_Q\) error.`,
  String.raw`\(Q,F,K\) are continuous, start from zero, and satisfy \(K\ge0\); the inherited variation bounds and Step 8 finiteness make every infinite sum below absolutely convergent.`,
  "28. Step 9 result and terminal domains",
  "29 / Complete text",
  "29. Signed best-N tails and the correct quantifier order",
  "30 / Complete text",
  "30. F-half-exit: exactly one half",
  "31 / Complete text",
  "31. K-theta last exit and the sharp one-B_Q error",
  "32 / Complete text",
  "32. Equivalence with the existing R0.74Q gate: no-gain",
  "33 / Complete text",
  "33. Quantifier, cancellation, and full-history stress tests",
  "34 / Complete text",
  "34. Compatibility of theta=2/3 and the next PDE residual",
  "35 / Complete text",
  "35. Step 9 claim boundary and dual audit",
  "36 / Complete text",
  String.raw`But an F-half-exit generally does not satisfy the strict Step 2 S.25 upcrossing condition. In the exact counterexample \(F(t)=t\), \(K(t)=\min\{2t,1\}\), and \(\tau=1\), one has \(\ell^F=1/2\), but \(K(1)-K(1/2)=0\). Thus (S.209) rules out the inference that a canonical half-exit is automatically an S.25-admissible stop.`,
  String.raw`time \(\ell_k^F(\tau)\); when \(f_k=0\), define \(\ell_k^F(\tau)=\tau\), as in (S.204). Continuity immediately gives`,
  String.raw`Define and audit the forced PDE residual tail after removing the Step 7 low-Rayleigh and Step 8 \(\mathcal I_\beta/\mathcal I_\sigma\) paid branches; pay at most \(N_0\) terminal-dependent exceptions by \(\sqrt{N_0}Z_R\).`,
  String.raw`For \(0<\theta<1\) and \(T_k=K_{k,R}(\tau)>0\), let \(\ell_{k,\theta}^{K}(\tau)\) be the last time satisfying \(K_{k,R}(t)\le\theta T_k\); when \(T_k=0\), take \(\ell=\tau\). Since \(F=K-Q\),`,
  String.raw`For \(F\) and \(K\), taking \(\sup_\tau\) over the terminal domain gives \(\mathcal S_{N,R}^{F}(\mathcal D)\) and \(\mathcal S_{N,R}^{K}(\mathcal D)\), as in (S.203). Only the largest \(N\) positive coordinates can be deleted, so`,
  String.raw`For \(x\in\ell^1(\mathbb N;\mathbb R)\) and a fixed integer \(N\ge0\), define`,
  "For the plateau domain this gives",
  String.raw`Fix a terminal time \(\tau\), and write \(f_k=F_{k,R}(\tau)\). When \(f_k\ne0\), take the last`,
  "The inherited Step 8 no-exception gate remains",
  String.raw`still excludes only scalar completed-clock algebra and unweighted genealogy; the Step 8 no-go is supplied by an inherited genuine smooth exact NSE family. Step 9 further proves that the \(F\)-half-exit is exactly one half of the signed best-\(N\) tail and that the \(K\)-last-exit, within one sharp \(B_Q\) error, is equivalent to \((1-\theta)\) times the best-\(N\) clock tail. Thus canonical stops give no new quadratic compression; this is a rigorous`,
  String.raw`Here \(N\) is independent of the terminal time, scale, and solution, but the optimal exceptional set \(S_\tau\) may depend on \(\tau\). This is not the stronger \(\inf_S\sup_\tau\).`,
  String.raw`The complete nonexceptional-tail last-exit observable and the best-\(N\) clock tail satisfy`,
  String.raw`The error is one \(B_Q\), not two; coefficient \(1\) is attained by a scalar continuous clock and is therefore sharp. For \(0<\theta<3/4\), every positive-terminal shell has`,
  "Exact representations and a no-gain conclusion in completed-clock algebra; not new PDE packing, DNS, or evidence of singularity or regularity.",
  String.raw`Therefore, for \(R\) and the solution, take a fixed independent \(N_0\):`,
  String.raw`At a good terminal time, every finite positive-terminal shell family can therefore be approximated using the common dense good-time set and lies in the closure of S.37. This is only a finite-family, positive-terminal, good-terminal closure statement; it asserts neither continuity of the last-exit selector nor admissibility of one infinite temporally discontinuous cutoff in the local energy inequality. The strict margin vanishes at \(\theta=3/4\), so the endpoint is excluded.`,
  String.raw`In the complete nonexceptional signed tail, sum first and then take the positive part, \(\inf_S\), and \(\sup_\tau\), obtaining`,
  "This is the forced full signed tail: cancellation from negative coordinates cannot be replaced by an arbitrary finite-subset supremum. The correct quantifier order is",
  String.raw`This is the exact Step 9 no-gain/no-go: a last-exit quadratic bound is equivalent to the already-open best-\(N\) terminal-tail bound, so the canonical stop supplies no weaker intermediate theorem. When \(\mathcal D=\mathcal T_R\), this is exactly Q.12; when \(\mathcal D=I_R\), it is only the weaker plateau restriction.`,
  String.raw`This is an abstract continuous-clock stress test, not an NSE solution; it rigorously shows that last exits do not automatically turn an \(\ell^1\) tail into an \(\ell^2\) payment. If every level exit occurs before a proposed recent window, that window contains no usable exit at all; hence (S.210) must retain the full history from \(s_R\) to \(\tau\), unless another PDE theorem pays the earlier segment.`,
  String.raw`This is a compatibility parameter for the next PDE decomposition, not a global optimization theorem. The next genuinely new target is to define and audit the forced full PDE residual tail after removing the Step 7 low-Rayleigh branch and the Step 8 paid \(\mathcal I_\beta\) and \(\mathcal I_\sigma\) branches, allowing at most \(N_0\) terminal-dependent exceptions paid by \(\sqrt{N_0}Z_R\). That residual may still contain anomalous defect or high-Rayleigh dissipation; this step does not define it in advance as a favorable object.`,
  "Only this inequality is retained; equality of the two terminal domains is not claimed. Write",
  "The primary certificate passes 9/9 exact, 8/8 finite, 57/57 structural, and 18/18 mutations. The independent Ruby audit passes 12/12 groups, 91,396/91,396 finite cases, 49/49 structural, 21/21 source mutations, 15/15 artifact mutations, and 6/6 report checks. The main-text SHA-256 is `85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd`. Finite certificates support implementation reproducibility only; they do not replace the PDE analysis.",
  "Status · R0.74S STEP 9",
  "Exact equivalence between canonical best-N last exits and terminal tails, and the no-gain boundary in completed-clock algebra",
  "No-gain equivalence among the canonical half-exit, last-exit, and best-N tail",
  String.raw`R0.74S Steps 1--6 separately sealed one-sided ball completion, the terminal Abel identity, four-channel circular recombination, and the abstract scalar no-go for unweighted genealogy; Step 7 paid the low-Rayleigh dissipation branch, and Step 8 rigorously refuted the universal no-exception stopped-work quadratic bound. Step 9 returns to R0.74Q's correct quantifier order, with fixed best-\(N\) and terminal-dependent exceptional sets, and audits whether canonical last exits give any additional tail compression.`,
  String.raw`The signed \(F\)-tail and nonnegative \(K\)-tail differ by one \(B_Q\):`,
  "Step 8 main text",
  String.raw`Step 9 no longer repairs the no-exception gate refuted in Step 8; it returns to the fixed best-\(N\) terminal tail of R0.74Q. The plateau terminal domain \(I_R\) must be distinguished from the full clock interval \(\mathcal T_R=(s_R,t_0)\):`,
  "Step 9 independent audit",
  "Step 9 machine-certificate JSON",
  "Step 9 certificate report",
  "Step 9 primary audit",
  "Step 9 final analytic main text",
  "Step 9: Python 9/9 exact, 8/8 finite, 57/57 structural, and 18/18 mutations; Ruby 12/12 groups, 91,396/91,396 finite cases, 49/49 structural, 21/21 source mutations, 15/15 artifact mutations, and 6/6 report checks. Finite certificates do not replace the PDE analysis.",
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
  assert.equal(rows.length, english.length, "R0.74S Step 9 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74S Step 9 English translation drift");
} else {
  assert.equal(missingBefore.length, english.length, "R0.74S Step 9 source-string count drift");
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

process.stdout.write(`${JSON.stringify({ release: "R0.74S Step 9", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
