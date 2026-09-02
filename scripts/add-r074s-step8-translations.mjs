#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074s8";

const english = [
  "Return to fixed best-N, terminal-dependent exceptions, and pay the tail with sqrt(N)Y2; do not attempt another no-exception supremum.",
  "Review v1.87 · 2026-09-02",
  "No-exception stopped work and full terminal positive flux differ only by the already-paid B_Q; a smooth exact family rigorously refutes the universal quadratic bound. S.38 is retained, and the next step turns to fixed best-N terminal exceptions. NOT CLAY.",
  "R0.74S rigorously excludes the no-exception stopped-work quadratic bound; the conditional implication S.38 remains valid. The next threshold is fixed best-N, terminal-dependent exceptions with a sqrt(N)Y2 tail payment, not another repair of the same universal supremum.",
  "R0.74S: No-go for the no-exception stopped-work quadratic bound",
  "R0.74S｜No-go for the no-exception stopped-work quadratic bound",
  "W_up and full flux differ only by the already-paid B_Q; a smooth exact family rigorously refutes the universal quadratic bound. Next: fixed best-N exceptions. NOT CLAY.",
  "W_up and full terminal flux differ only by the already-paid B_Q; a smooth exact family makes W_up/(P_R^M)^(2/3)→∞. S.38 is retained, and the next step turns to fixed best-N exceptions. NOT CLAY.",
  "Return to R0.74Q's terminal-dependent exception quantifier and pay the tail with sqrt(N)Y2.",
  "Literature review v1.87 · 2026-09-02",
  "B_Q-accurate equivalence for no-exception stopped work and an exact-NSE no-go",
  "PROVED: the S.163–S.196 excess interface and stopped-work bridge; |W_up−C_full|≤B_Q; K_full−B_Q≤W_up≤K_full+B_Q. REFUTED: the universal no-exception antecedent W_up≲(P_R^M)^(2/3). RETAINED: the conditional implication S.38. FINITE: final Python 16/16, 19/19, 75/75, and 20/20; Ruby 14/14 groups, 22/22 exact, 61/61 structural, 14/14 source mutations, 10/10 artifact mutations, and 6/6 report checks. OPEN: fixed best-N terminal exceptions, a quadratic bound for the Jordan envelope, Q.1, and regularity.",
  "S.163–S.196 establish the total-Rayleigh excess interface; S.197–S.198 prove that W_up and full terminal flux differ only by the already-paid B_Q; S.199 uses a smooth exact family to rigorously refute the universal no-exception quadratic bound. The conditional implication S.38 is retained.",
  "Step 8 uses the inherited suitable-weak measures, Q-variation, padded-shell cubic payment, Step 2 gate, and R0.74O/P smooth exact family; it claims no novelty, priority, or general regularity.",
  "Research-note master index · v1.87 · 2026-09-02",
  "No-go for the no-exception stopped-work quadratic bound",
  String.raw`: fixed best-\(N_0\), terminal-dependent exception estimate with the exceptional tail paid by \(\sqrt{N_0}Y_{2,R}^{\rm sf}\); a quadratic/square-function/finite-exception bound for the Jordan envelope; existence of smooth NSE approximations; the R0.74R extraction hypotheses; unconditional fixed-scale (Q.1), scale contraction, prescribed-centre packing, and regularity.`,
  String.raw`: \(X=0\) for the exact shear; lower semicontinuity of the selected excess sum; \(X\le\mathfrak W_{\rm up}\); a narrowing of the Step 2 gate by Step 8; hard-terminal mass convergence; or any novelty, priority, singularity, or Clay conclusion.`,
  ": the S.163--S.196 three-measure excess interface, one-sixth trichotomy, two paid branches, lower semicontinuity, fixed-scale finiteness, terminal-flux domination, and stopped-work bridge; the S.197--S.198 no-exception two-sided equivalence; and the S.199 smooth exact-family refutation.",
  String.raw`. This does not refute the conditional algebra of S.38, S.196, estimates with terminal exceptions paid by \(Y_{2,R}^{\rm sf}\), or (Q.1).`,
  String.raw`The \(\beta\)-branch satisfies \(\sum_{\mathcal I_\beta}T_k\le C_\beta(P_R^M)^{2/3}\), while the selected excess branch satisfies \(T_k\le6x_k\). Therefore`,
  String.raw`The \(\beta\)-branch is paid by the inherited quadratic \(Q\)-variation ledger. For the kinetic branch, set \(\delta_\tau=|J_\tau|/R^2<4\); Jensen gives`,
  String.raw`\(\mathfrak W_{\rm up}\) and full terminal positive flux differ only by the already-paid \(B_Q\); a smooth exact family makes \(\mathfrak W_{\rm up}/(P_R^M)^{2/3}\to\infty\).`,
  String.raw`\(\sigma\) is the parabolically normalized kinetic-energy measure, \(\nu\) is the total dissipation measure combining viscous and anomalous defect, and \(\beta\) is the total-variation measure of the canonical \(Q\)-primitive. The interval \(J_\tau\) is open at the terminal endpoint, consistently with the inherited completed-clock convention \((s_R,\tau)\), so a dissipation atom at \(t=\tau\) is not counted again. The frozen cutoff and its derivatives vanish on a common neighbourhood of \(s_R\), so no mass escapes through the left endpoint.`,
  String.raw`\(x\) first evaluates the signed mass on the full terminal interval and then takes its scalar positive part; \(X\) is the positive-measure mass in the Jordan decomposition and retains local positive excess cancelled by netting across distinct time intervals. Hahn decomposition, Radon-measure regularity, and Urysohn approximation give`,
  "18. Three time measures and the open-terminal convention",
  "19 / Complete text",
  "19. Scalar excess and the Jordan envelope",
  "20 / Complete text",
  "20. The one-sixth priority trichotomy and two paid branches",
  "21 / Complete text",
  "21. Selected/global excess ledger and comparison with Step 7",
  "22 / Complete text",
  "22. Exact shear, lower semicontinuity, and the boundary of the smooth formula",
  "23 / Complete text",
  "23. Fixed-scale finiteness and terminal-flux domination",
  "24 / Complete text",
  "24. The selected excess enters the Step 2 gate",
  "25 / Complete text",
  "25. Equivalence of no-exception stopped work and full terminal flux",
  "26 / Complete text",
  "27 / Complete text",
  "27. Stress tests, certificates, and the next threshold",
  "28 / Complete text",
  "rigorously",
  String.raw`This step also retains six stress tests: the Jordan formula fully detects an interior atom; excess subtracts the already-paid dissipation when \(\nu=\beta\); a high-frequency divergence-free functional family excludes a cubic bound for \(x\) or \(X\) based only on incompressibility/cutoff/Holder; temporal cancellation of a signed density proves that \(X\) can be strictly larger than \(x\); mass escaping to the hard terminal endpoint shows that only lower semicontinuity can be claimed; and \(Q_n=n^{-1}\sin(nt)\) shows that uniform convergence of primitives cannot replace convergence of \(\dot Q_n\) that is strong in \(L^1\). The PDE-identity boundary of each stress test is retained explicitly.`,
  String.raw`This rigorously refutes the universal no-exception quadratic bound. S.38 remains a valid conditional implication; what is disproved is the antecedent required to turn it into an unconditional theorem. The next viable route must return to fixed best-\(N\), terminal-dependent exception sets and pay the tail with \(\sqrt N,Y_{2,R}^{\rm sf}\).`,
  String.raw`The coefficient one in the second inequality is sharp by the single-shell scalar stress \(K=0,Q=-B,F=B\). Thus the Step 2 no-exception observable is equivalent, within the already-paid quadratic error \(B_Q\), to full-cutoff positive cumulative flux; it is not a smaller signed-depletion quantity.`,
  String.raw`Define \(\mathscr L(\boldsymbol\lambda)=\sum_k2^{3k}\gamma_k\lambda_k^3\). If \(\mathscr L<\infty\), finite-shell Holder followed by monotone convergence gives`,
  "Define the all-shell interface",
  String.raw`Define the already-paid \(Q\)-variation, full terminal-clock supremum, and full positive cumulative flux:`,
  String.raw`For a Borel set \(A\subset\mathcal T_R\), define`,
  String.raw`For a dissipation-dominated shell, write \(T_k=K_{k,R}(\tau)>0\) and \(D_{k,R}(\tau)\ge T_k/2\). Test in priority order`,
  String.raw`For the inherited heat shear, Step 7 proved \(F_k=0\), hence \(K_k=Q_k\). If \(T_k=K_k(\tau)>0\), then`,
  String.raw`For any admissible stopped family in S.37, subtract the work directly from full flux at the same terminal time. The \(K_k\) terms in the start and omitted-shell parts are nonnegative, and the remaining \(Q\)-differences total at most \(B_Q\). Conversely, at a common good terminal time, use a common zero stop for finite shell sets with \(K_k(\tau)>0\) and \(F_k(\tau)>0\), then take the monotone limit. If an omitted shell has \(K_k=0<F_k\), then \(F_k=-Q_k\), whose total is still at most \(B_Q\). Therefore S.197--S.198 give`,
  "For the same high/low-Rayleigh split as in Step 7, each shell satisfies",
  String.raw`Fix the periodic suitable-weak Version-M geometry of R0.74P--R0.74R: unit viscosity, scale \(R\), terminal-anchored path \(X_R\), nondecreasing time cutoff \(\eta_R\), padded-shell cutoff \(\Psi_k^R\), and weights \(\gamma_k\). Write`,
  String.raw`Fix a positive deterministic profile \(\boldsymbol\lambda=(\lambda_k)\), and set`,
  String.raw`Return to fixed best-\(N\), terminal-dependent exceptions, and pay the tail with \(\sqrt N\,Y_{2,R}^{\rm sf}\); do not attempt another no-exception supremum.`,
  "still",
  String.raw`still excludes only scalar completed-clock algebra and unweighted genealogy; the new Step 8 no-go is instead supplied by an inherited genuine smooth exact NSE family and rigorously excludes the universal no-exception stopped-work quadratic bound. A fixed best-\(N\) terminal-exception estimate, the R0.74R extraction inputs, the fixed-scale inequality, scale contraction, regularity, and singularity formation remain`,
  String.raw`Combining the two paid \(\beta\) and kinetic branches, S.196 gives`,
  "Analytic identities and a scale no-go from an inherited smooth exact NSE family; not DNS or evidence of singularity or regularity.",
  "The two excess levels are",
  "Explicitly",
  "Universal no-exception quadratic bound: REFUTED",
  "Taking the finite-family supremum gives",
  String.raw`If \(\boldsymbol\delta_{k,R}\) is the weighted time pushforward of anomalous dissipation, then`,
  "If the solution itself is smooth, the defect measure vanishes and",
  "If both tests fail, then",
  "Using the inherited R0.74O/P smooth periodic exact family, one has",
  String.raw`Therefore \(x_k>T_k/6\). This is the literal trichotomy of S.170--S.171: every positive dissipation-dominated clock is either paid by \(\beta\) by at least one sixth, has enough kinetic time mass, or enters the selected excess class.`,
  String.raw`It therefore enters the \(\beta\)-priority branch and is not a counterexample to the excess theorem; no claim is made here that its Jordan envelope \(X_k\) vanishes.`,
  String.raw`The next step will not attempt another no-exception supremum. The only frozen direction is to return to the fixed best-\(N\), terminal-dependent exceptions of R0.74Q (Q.7)--(Q.12), retaining payment by \(\sqrt N,Y_{2,R}^{\rm sf}\).`,
  String.raw`A linear \(CP_R^M\) bound, when \(P_R^M>1\), is not a quadratic \((P_R^M)^{2/3}\) bound.`,
  String.raw`Alternatively, select only the exact-family target shell: its terminal clock is \(\gtrsim T_*\), its full \(Q\)-variation is \(O(T_*/K_*)\), and the common zero stop gives stopped work \(\gtrsim T_*\). This witness is a genuine smooth, periodic, mean-zero, unforced, pressure-free NSE solution family.`,
  String.raw`Thus \(0\le x\le X\), and`,
  "Therefore the universal antecedent",
  String.raw`The signed-measure order \(\alpha\le\nu\) gives \(\alpha^+\le\nu\). Tonelli, the inherited \(\Theta_R=\sum_k\gamma_k\Psi_k^R\) \(C^2\)-convergence, and local finiteness give`,
  String.raw`Because the additive \(Q\)-error in S.198 is only \(O((P_{R_j}^{M,*})^{2/3})\), S.199 yields`,
  "Combining this with the inherited padded-shell cubic estimate gives",
  String.raw`In the common initial interval where \(\eta_R=\eta_R'=0\), choose a common good time \(\sigma_0\). Every shell satisfies \(K_k(\sigma_0)=Q_k(\sigma_0)=F_k(\sigma_0)=0\). If \(x_k(\tau)>0\), then \(K_k(\tau)>0\), so this common zero start satisfies the strict upcrossing condition of Step 2. For every finite nonempty \(G\subset\{k:x_k(\tau)>0\}\),`,
  String.raw`At an inherited local-energy good terminal time, \(\nu_{k,R}(J_\tau)=D_{k,R}(\tau)\), while \(\beta_{k,R}(J_\tau)=\operatorname{TV}_{J_\tau}Q_{k,R}\). These are the exact measure identities S.163--S.166.`,
  String.raw`On the priority-selected excess class, \(\beta_k<T_k/6\) and \(|Q_k(\tau)|\le\beta_k\), hence`,
  String.raw`In the fixed-scale Version-M topology of R0.74P, if \(u_n\to u\) strongly in \(L^3\), \(\nabla u_n\rightharpoonup\nabla u\) in \(L^2\), and \(p_n\rightharpoonup p\) in \(L^{3/2}\), then on each fixed shell \(\nu_n\rightharpoonup^*\nu\) locally, while \(\sigma_n\to\sigma\) and \(\beta_n\to\beta\) in total variation. Open-set Portmanteau and the Jordan continuous-test formula respectively give`,
  String.raw`This is fixed-scale total-dissipation finiteness, not a quadratic bound uniform in \(R\).`,
  "This dominates the old raw residual shell by shell, but because the two steps use different priority partitions, the Step 8 global sum cannot be claimed to be numerically smaller than the Step 7 prioritized residual.",
  "This proves that the selected defect/high-Rayleigh scalar residual is not a new independent obstruction but a subledger of the existing stopped-work ledger. Yet Step 2 already permits a common zero start, so it does not narrow the no-exception supremum.",
  String.raw`Only when a smooth periodic NSE sequence satisfying the stated topology is supplied separately may one take \(\liminf\) of these smooth formulas. This section does not claim that every suitable weak solution admits such smooth approximants.`,
  String.raw`The terminal trichotomy uses the smaller \(x\); \(X\) is for localization and weak-limit stability, not a smaller terminal upper bound.`,
  "The final Step 8 primary certificate passes 16/16 exact, 19/19 finite, 75/75 structural, and 20/20 negative mutations. The independent Ruby audit passes 14/14 groups, 22/22 exact rows, 61/61 structural, 14/14 source mutations, 10/10 artifact mutations, and 6/6 report checks. The main-text SHA-256 is `0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab`. Finite certificates support implementation reproducibility; they do not replace the measure/PDE analysis.",
  "Final Step 8: Python 16/16 exact, 19/19 finite, 75/75 structural, and 20/20 mutations; Ruby 14/14 groups, 22/22 exact, 61/61 structural, 14/14 source mutations, 10/10 artifact mutations, and 6/6 report checks. Finite certificates do not replace the analytic proof.",
  String.raw`The canonical primitives vanish at \(s_R\), so \(\beta_k(J_\tau)\ge|Q_k(\tau)|\). The completed-clock identity gives`,
  "Excess bridge, B_Q-accurate equivalence, and exact-family no-go",
  String.raw`Finite-shell Fatou followed by monotone convergence gives all-shell lower semicontinuity of \(\mathfrak x_{1,R}\) and \(\mathcal X_{1,R}\). This holds only in the inherited topology at fixed \(R\) and provides no cross-scale compactness.`,
  "Quadratic bound for the Jordan envelope: OPEN",
  "B_Q-accurate equivalence of no-exception stopped work and full terminal flux, plus a smooth exact-family no-go",
  "R0.74S Steps 1--6 separately sealed one-sided ball completion, the terminal Abel identity, four-channel circular recombination, and the abstract scalar no-go for unweighted genealogy; Step 7 then paid the low-Rayleigh dissipation branch. Step 8 subtracts the remaining total-Rayleigh excess at measure level and reaudits the Step 2 no-exception stopped-work gate.",
  "Conditional implication S.38: RETAINED",
  String.raw`The selected inequality may therefore be relaxed by adding \(6\mathfrak x_{1,R}\), and then further by adding \(6\mathcal X_{1,R}\). The global sums include shells already paid by \(\beta\); \(X\) also retains local positive excess cancelled in the terminal signed mass.`,
  "Step 7 main text",
  "Step 8 independent audit",
  "Step 8 machine-certificate JSON",
  String.raw`Step 8 introduces scalar excess \(x\) and the Jordan envelope \(X\), proving that the selected defect/high-Rayleigh residual is a subledger of the existing stopped-work ledger. More importantly, S.197--S.198 prove that the no-exception stopped-work supremum \(\mathfrak W_{\rm up}\), full terminal clock, and full positive cumulative flux differ only by \(B_Q\), which the quadratic ledger already pays. The R0.74O/P smooth exact family then gives`,
  "Step 8 certificate report",
  "Step 8 primary audit",
  "Step 8 final analytic main text",
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
  assert.equal(rows.length, english.length, "R0.74S Step 8 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74S Step 8 English translation drift");
} else {
  assert.equal(missingBefore.length, english.length, "R0.74S Step 8 source-string count drift");
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

process.stdout.write(`${JSON.stringify({ release: "R0.74S Step 8", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
