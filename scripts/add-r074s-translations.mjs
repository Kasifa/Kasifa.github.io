#!/usr/bin/env node

import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const delegated = spawnSync(
  process.execPath,
  [resolve(root, "scripts/add-r074s-step16-translations.mjs"), ...process.argv.slice(2)],
  { cwd: root, encoding: "utf8" },
);
process.stdout.write(delegated.stdout || "");
process.stderr.write(delegated.stderr || "");
process.exit(delegated.status ?? 1);

const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const translationRoute = "LOCAL_DIRECT_NO_DGX";
const dgxUsed = false;
const checkOnly = process.argv.includes("--check-only");

// Deterministic direct translations in collectSiteStrings order. Mathematical
// tokens are preserved byte-for-byte from their Chinese source strings.
const english = [
  "Master index of 221 research notes",
  "98 sections fully sealed",
  "View the R0.74S homepage card",
  "Window-mass contraction → arbitrary-clock trichotomy → one-sided ball completion → terminal Abel identity → abstract ℓ¹/ℓ² no-go",
  "Current endpoint R0.74S",
  "Test cross-channel dynamical sign relations, or prove uniformly finite complexity of the stopped block genealogy; do not add more clocks of the same positive type.",
  "The exact Abel identity gives only ℓ¹; an abstract clock tower rules out obtaining ℓ² compression from positivity and linearity alone. This is not a PDE/NSE counterexample. NOT CLAY.",
  "Jump to the R0.74S homepage card →",
  "Research note R0.74S · 2026-09-02",
  "One-sided ball completion and the terminal Abel identity give only ℓ¹; an abstract clock tower rules out obtaining ℓ² compression from positivity, linearity, and the tower identity alone. This is not a PDE/NSE counterexample. NOT CLAY.",
  "Read the latest R0.74S research note →",
  "Expand 131 public notes",
  "Review v1.85 · 2026-09-02",
  "The ball-clock and Abel identities are proved; an abstract clock tower gives an ℓ¹/ℓ² no-go. This is not a PDE/NSE counterexample. NOT CLAY.",
  "The cumulative review after the R0.60 recap contains 157 nodes; the site now has 221 public research notes",
  "R0.70A–R0.74S · 123 sections published",
  "R0.70A–R0.74S: 123 sections published, 98 fully sealed",
  "R0.74S proves that one-sided ball completion leaves only an ℓ¹ debt and uses an abstract smooth clock tower to rule out the route from positivity, linearity, and tower identities alone to matching ℓ² compression; cross-channel dynamical signs and finite genealogy remain open.",
  "R0.74S: One-sided ball clocks and the ℓ¹/ℓ² no-go",
  "R0.74S｜Why does a one-sided ball clock still leave an ℓ¹ debt?",
  "R0.74S｜One-sided ball clocks and the ℓ¹ debt",
  "R0.74T next interface",
  "This section is an internal algebraic route audit built on the existing suitable-weak local-energy and shell-clock framework. It claims neither a new Navier--Stokes theorem from an abstract tower nor novelty or priority.",
  "Open interface · R0.74T",
  "Cross-channel dynamical signs or finite genealogy",
  "The three stopped channels, quadratic ball ledger, and terminal Abel identity are proved; an abstract clock tower rules out deriving matching ℓ² compression from scalar positivity, linearity, and tower identities alone. It is not a PDE/NSE counterexample.",
  "Literature review v1.85 · 2026-09-02",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74S only as research notes. I do not extrapolate computations or notes into regularity theorems.",
  "The next step will not add another positive completion of the same type; it must retain the dynamical relations among root, outer, and weight-drop channels.",
  "One-sided ball-clock Abel identity and the ℓ¹/ℓ² no-go",
  "Claim boundary",
  "PROVED: one-sided ball clocks, stopped orientations, quadratic ledger, and terminal Abel identity. FINITE: 5/5, 7/7, 55/55, and 4/4. NO-GO: only the independent mechanism using scalar positivity, cutoff linearity, and tower identities is excluded; the witness is not a velocity, pressure, dissipation measure, or NSE solution. OPEN: cross-channel dynamical signs, finite genealogy, Q.1, regularity, and singularities.",
  "R0.74S public boundary",
  "R0.74S literature and claim boundary",
  "221 public research notes, with R0.74S as the latest node.",
  "Research-note master index · v1.85 · 2026-09-02",
  "Why does a one-sided ball clock still leave an ℓ¹ debt?",
  "Latest node R0.74S · continuously revised",
  "; the witness is not a velocity field, pressure field, dissipation measure, or Navier--Stokes solution and cannot be presented as a PDE/NSE counterexample.",
  "0. What this step establishes",
  "1. Two compactly supported one-sided ball cutoffs",
  "3. From collar to ball still requires only quadratic payment",
  "4. Time orientations of the three signed channels",
  "4/4 negative sign-mutation checks.",
  "5. The Abel identity for terminal weight-drop",
  "5/5 exact ledger rows;",
  "5/5 exact, 7/7 finite, 55/55 structural, and 4/4 negative mutations; the finite certificate does not replace the analytic proof.",
  "55/55 structural checks;",
  "6. An abstract clock tower sharply saturates this loss",
  "7. Certificate and independent audit",
  "7/7 finite checks;",
  "8. Decision and next threshold",
  "9. Inherited boundaries",
  String.raw`Retain \(r_m=2^mR\), \(\delta=R/8\), and the frozen transition function \(\vartheta\), and define`,
  "This section contains no numerical simulation, DNS, or DGX.",
  "This section has",
  "This section proves three points:",
  "This section closes only one independent algebraic route: completing every remaining signed face separately into a positive ball clock and then taking absolute values or terminal values term by term cannot produce a matching square-function estimate from positivity, linearity, and the tower identity.",
  String.raw`The scalar positive-clock \(\ell^1/\ell^2\) obstruction.`,
  "The asymmetry is exact: root remains at the initial stop, outer remains at the merge, and weight-drop remains at the terminal time. Positivity does not automatically erase these values.",
  "cannot by itself close the matching square function. This witness has no spatial operator or PDE realization, so it does not exclude a theorem that genuinely uses the Navier--Stokes equation, cross-channel signs, or finite genealogy.",
  "No novelty, priority, regularity, or Millennium-problem conclusion is claimed.",
  "Do not add another positive completion of the same type; next test only cross-channel dynamical sign relations or uniformly finite complexity of the stopped block genealogy.",
  String.raw`Replacing the collar by a ball creates no additional low-order loss; all quadratic cutoff rows are still paid by \(A_R=(P_R^M)^{2/3}\);`,
  String.raw`The frozen weights satisfy \(\sum_{k\ge j}\gamma_k\le(35/3)\gamma_j\). Splitting the lifted ball into the central ball, hard boundary collar, and padded-shell interior gives the pointwise packing`,
  String.raw`For any nonnegative compactly supported lifted cutoff \(\phi\) and its periodization \(\Phi\), define the four rows of endpoint energy, dissipation, quadratic source, and flux`,
  String.raw`The sum of the corresponding absolute Laplacians, multiplied by \(R^2\), obeys the same control. The dangerous outer collar \(C_j^+\) carries \(\gamma_{j-1}\), paid by \(\operatorname{supp}\psi_{j-1}^R\); it must not be replaced incorrectly by \(\gamma_j\). The central ball is paid separately by`,
  String.raw`For fixed \(R,t\), the periodized ball clock grows at most like \(1+2^{3M}\), while \(\gamma_M=\exp(-4^{M-1}/32)\), so \(\gamma_MB_M\to0\). Passing to the limit and restoring \(m=1\) gives`,
  String.raw`Fix the stopped family \((\tau,I,\boldsymbol\sigma)\) from Step 2. For \(k\in I\), let \(\rho_k\) be the predecessor merge/terminal time and \(\lambda_k\) the successor merge/terminal time; an internal boundary becomes active at \(\widehat\sigma_m=\max(\sigma_{m-1},\sigma_m)\).`,
  "Analytic main text, certificate, and independent audit",
  "Exact integration gives:",
  String.raw`Both are smooth, radial, compactly supported, and valued in \([0,1]\). Checking the four radial regions divided by \(r_m-\delta,r_m,r_m+\delta\) gives`,
  String.raw`Let \(\mathsf B_{m,R}^{\pm}\) be their periodizations. Both radial gradients carry a negative sign, so the work vector in R0.74S Step 3 satisfies`,
  String.raw`Every term is nonnegative. Therefore, for every finite \(H\subset\{2,3,\ldots\}\),`,
  String.raw`The remaining ball tower is defined recursively by monotone differences. At the purely scalar level set \(\mathscr E=\mathscr K\), \(\mathscr D=\mathscr Q=0\), and \(\mathscr F=\mathscr K\); every completed-clock and linear tower identity then holds term by term.`,
  String.raw`Take any \(N\ge1\) and a smooth monotone function \(h\) with \(h(s_R)=0\) and \(h(\tau)=1\). Set`,
  "Deterministic analytic figure; not DNS, simulation, a PDE/NSE counterexample, a singularity, or regularity evidence.",
  "A viable next step must retain cross-channel dynamical relations, such as the sign coupling between root supply and an inactive inner shell, outer leakage and a later merge, or weight-drop and negative work/backscatter before taking positive parts. Another possibility is to prove uniformly finite complexity of the stopped block genealogy.",
  "Three stopped orientations: PROVED",
  "All three signed channels have exact stopped ball-clock representations, but their time orientations differ;",
  String.raw`Three families of quadratic \(\mathscr Q\) payments;`,
  String.raw`Consequently there is no universal constant \(C\) derivable only from the scalar algebra above such that`,
  "Literature and priority boundary",
  "No simulation / NO DGX",
  "Unconditional stopped-work estimates, a cross-channel dynamical sign theorem, R0.74R's universal persistence input, the fixed-scale inequality, scale contraction, regularity, and singularity formation remain",
  "Linearity and the cutoff-difference identities above give",
  String.raw`Write \(\mathscr K_R=\mathscr Q_R+\mathscr F_R\). The suitable-weak local-energy calculation in R0.74P gives canonical absolutely continuous representatives`,
  "Research note R0.74S · complete Chinese version",
  String.raw`One-sided ball completion gives exact stopped clocks and an Abel identity, but leaves only an \(\ell^1\) ledger. An abstract clock tower proves that positivity, linearity, and the tower identity alone cannot yield matching \(\ell^2\) compression.`,
  "One-sided ball cutoff and flux-sign identity;",
  "One-sided ball cutoffs: PROVED",
  "One-sided ball-clock reduction, terminal Abel identity, and the remaining ℓ¹ debt",
  "One-sided ball clocks, exact Abel identity, and the remaining debt",
  String.raw`Thus ball completion creates no new low-order loss; the real issue is the remaining terminal \(\mathscr K\)-clock.`,
  String.raw`Using \(\mathscr F=\mathscr K-\mathscr Q\), \(\mathscr K\ge0\), and quadratic payment leaves only`,
  "By the ball tower, the middle term is exactly",
  String.raw`The finite coverage includes 312 rational cutoff values, 228 derivative samples, 1024 stopped configurations including tied stops, 82,432 Boolean activation comparisons, every finite Abel endpoint for \(M=2,\ldots,8\), and the abstract tower for \(N=1,\ldots,24\) at five rational times. Independent recomputation in two temporary directories produces byte-identical JSON and Markdown reports.`,
  String.raw`At a good time \(t\), write \(B_m=\mathscr K_{m,R}^+(t)\). Finite summation by parts gives`,
  String.raw`At the terminal time, the positive variations of the first \(N\) shells all equal 1, so`,
  "This sign determines that the later root and outer rows retain different endpoints; absolute values must not be taken at this stage.",
  "This is the no-go in this section:",
  String.raw`This is a genuine monotone ball tower, but monotonicity alone only makes the residual nonnegative; it does not turn it from \(\ell^1\) into \(\ell^2\).`,
  String.raw`This is a correct finite \(\ell^1\) estimate, but it supplies no square-function compression. Substituting it into the weight-drop row returns only the already-known large payment ledger.`,
  "These are",
  "certificates that validate only formula implementations and sign sentinels; they do not machine-prove cutoff smoothness, periodization/unfolding, the suitable local-energy calculation, infinite-support estimates, or a PDE realization of the abstract witness. The analytic proof and finite certificate remain separate.",
  "paid by. After combination,",
  "Primary audit",
  "Status · R0.74S",
  String.raw`Finally, a smooth abstract clock tower makes the ball-clock debt equal to \(N\), while the square function is only \(\sqrt N\). Therefore completed-clock positivity, cutoff linearity, and tower identities alone cannot yield the required \(\ell^2\) compression. This is an`,
  "Final analytic main text",
  "The final deterministic certificate passes:",
  "actual collar traces and the four-channel split: inherited from R0.74S Step 3, PROVED;",
  "frozen adjacent-weight tail: inherited from R0.74S Step 1, PROVED.",
  "R0.74R split the difficulty for an arbitrary completed clock into accumulated dissipation, a true kinetic-energy window, and recent positive variation. R0.74S tests the most natural repair: stop every active shell at its last upcrossing, complete the remaining root, outer, and weight-drop signed channels with one-sided ball cutoffs, and then use positivity and neighbouring shells to eliminate the boundary.",
  "Exact stopped time orientations of root, outer, and weight-drop;",
  "Dynamical control of root/outer/weight-drop, the dissipation-dominated branch, the R0.74R persistence hypotheses, the unconditional fixed-scale inequality (Q.1), scale contraction, regularity, singularity formation, and the Clay problem all remain",
  "stopped-family activation: inherited from R0.74S Step 2, PROVED;",
  "suitable-weak completed-clock operator: inherited from R0.74P, PROVED;",
  "terminal weight-drop Abel identity;",
  String.raw`The terminal weight-drop ball clocks satisfy an exact Abel identity, but its right-hand side is the complete \(\ell^1\) shell residual, not a matching square function.`,
  String.raw`thin boundary clock and \(K_m^\partial\le K_m\): inherited from R0.74S Step 4, PROVED;`,
  String.raw`weighted \(S_2\) and doubled-radius support ledger: inherited from R0.74H, PROVED;`,
];

process.chdir(root);
const [source, translationOrderSource, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings("./public"),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
// The original R0.74S release owns exactly the three-digit r074sNNN range.
// Later step-specific prefixes (for example r074s7NNN) must not be folded into
// this historical self-check.
const baseRowPattern = /^r074s\d{3}$/;
const baseCurrent = checkOnly ? current : current.filter((row) => !baseRowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missingBefore = source.filter((entry) => !currentByZh.has(entry.zh));
const missingInTranslationOrder = translationOrderSource.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missingBefore.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => baseRowPattern.test(row.id));
  assert.equal(rows.length, english.length, "R0.74S translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74S English translation drift");
} else {
  assert.equal(missingBefore.length, english.length, "R0.74S source-string count drift");
  const sourceByZh = new Map(missingBefore.map((entry) => [entry.zh, entry]));
  const additions = missingInTranslationOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = english[index];
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), `protected token drift ${index + 1}: ${entry.zh}`);
    return { id: `r074s${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...baseCurrent, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({ release: "R0.74S", translationPath: translationRoute, dgxUsed, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
