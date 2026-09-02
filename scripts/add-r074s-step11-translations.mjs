#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074sstep11";

const english = [
  "Prove or refute short terminal anti-concentration S.261 and uniform selected-excess packing S.269 separately, then test S.272 with the added fixed budget.",
  "The budget infimal convolution is exact; the short-branch terminal trace and scalar-excess uniform packing remain open. Existing multi-packet exact families do not rule out fixed positive N. NOT CLAY.",
  "The shared budget is exact; short terminal trace and selected-excess packing remain OPEN. NOT CLAY.",
  "Previous-stage structure figure",
  "Review v1.90 · 2026-09-03",
  "R0.74S Step 11 writes the shared exception budget as an exact infimal convolution. The next threshold is to prove short terminal anti-concentration S.261 and selected-excess packing S.269 separately, then combine them as S.272.",
  "R0.74S: Shared best-N budget and the terminal-trace obstruction",
  "R0.74S｜Shared best-N budget and the terminal-trace obstruction",
  "Prove or refute S.261 and S.269 separately, then test S.272 with the added fixed budget.",
  "Shared best-N budget and the terminal-trace obstruction",
  "Literature review v1.90 · 2026-09-03",
  "PROVED: the exact shared-budget infimal convolution; short inverse-duration, nested-tent, and positive-depth control; the critical s² Carleson logarithmic obstruction at coefficient level; excess/residual best-N constants 1/5 and 3; fixed-solution nonuniform tightness; and the N+1-target falsification test. ABSTRACT STRESS TESTS: not NSE counterexamples. FINITE: Python 14/14 exact, 7/7 finite, 34/34 structural, and 7/7 mutations; Ruby 7/7 groups, 206,891 cases, and 59/59 note checks. OPEN: S.261, S.269, S.272, S.243, Q.12, Q.1, and regularity. Existing multi-packet exact families do not refute fixed positive N. The prior no-go remains.",
  "R0.74S Step 11 public boundary",
  "S.249 gives the exact shared-budget infimal convolution; S.253–S.259 give short inverse-duration, nested-tent, and positive-depth control; S.262–S.265 give the excess/residual constants 1/5 and 3 and nonuniform compactness. S.261, S.269, and S.272 remain open.",
  "Step 11 audits the shared budget, terminal trace, and selected-excess packing on top of the inherited paid/residual partition; it claims no novelty, priority, or new PDE packing theorem.",
  "Shared best-N budget and the terminal-trace obstruction",
  "Research-note master index · v1.90 · 2026-09-03",
  String.raw`; they rule out derivations using only scalar \(\ell^1/\ell^2\) ledgers and do not refute (S.243). The exact minimal target is`,
  String.raw`: the shared-budget identity and domain consequence (S.249)--(S.251); the inverse-duration estimate (S.253)--(S.254); the normalized-depth, dyadic, and layer-cake identities (S.255)--(S.256); the coefficient-level critical Carleson failure (S.257); the nested-tent and positive-depth estimates (S.258)--(S.259); the scalar-excess/residual equivalence (S.262)--(S.263); the ancestry, linear ledger, and fixed-solution compactness statements (S.264)--(S.265); and the conditional implications from (S.261), (S.269), (S.270), and (S.272).`,
  String.raw`: the duplicate-budget fixture (S.252); the critical Carleson sequence and nested tower (S.257), (S.260); the ancestry-localization witnesses (S.266)--(S.267); and the flat selected-excess tower (S.268).`,
  String.raw`: continuity or measurability of moving masks, last-exit selectors, top-\(N\) sets, or adaptive budget splits; commutation of terminal supremum and branch-budget minimum; use of CKN-type singular-set estimates to count these shell residuals; persistence of terminal ancestry on the last-exit interval; exhaustiveness of the bounded literature search; novelty or priority; or a solution of the Navier--Stokes Millennium problem.`,
  String.raw`: terminal anti-concentration (S.261); uniform selected-excess packing (S.269); either branch estimate in (S.272); a fixed universal \(N_0\); Step 10 (S.243), Q.12, Q.1, scale contraction, prescribed-centre packing, and regularity; and a new exact multi-packet family satisfying (S.270) without prohibitive full payment.`,
  ". No claim of novelty, priority, singularity, regularity, or a Millennium-problem conclusion is made.",
  String.raw`The implication from (S.261) and (S.259) is proved: it would close the short branch. The boxed hypothesis itself is unproved; it asks the PDE to prevent a nonquadratic fraction of the tail from being generated entirely in the final \(\delta_*R^2\) time units.`,
  "(S.266)--(S.268) are all",
  "46. Step 11 question and four conclusions",
  "47 / Complete text",
  "47. Two residual vectors and the shared-budget identity",
  "48 / Complete text",
  "48. The short-branch inverse-duration ledger",
  "49 / Complete text",
  "49. Normalized depth and the critical Carleson log gap",
  "50 / Complete text",
  "50. What the nested tent controls and what it does not",
  "51 / Complete text",
  "51. The first new PDE threshold for the short branch",
  "52 / Complete text",
  "52. Exact best-N equivalence of scalar excess and residual",
  "53 / Complete text",
  String.raw`53. Fixed-solution tightness is not a uniform \(N\)`,
  "54 / Complete text",
  "54. Ancestry cannot be pushed back to the last-exit interval",
  "55 / Complete text",
  "56 / Complete text",
  "56. The combined open theorem",
  "57 / Complete text",
  "57. Step 11 claim boundary and dual audit",
  "58 / Complete text",
  String.raw`Retain all Step 10 definitions. At a fixed good terminal \(\tau\), set \(T_k=K_{k,R}(\tau)\), \(\ell_k=\ell^K_{k,2/3}(\tau)\), and \(d_k=(\tau-\ell_k)/R^2\), and split the residual into two disjointly supported vectors`,
  String.raw`Retain the Step 8 scalar excess \(x_k=[D_{k,R}(\tau)-\beta_{k,R}(J_\tau)-2\lambda_k\sigma_{k,R}(J_\tau)]_+\), and put \(x_k^{\rm sel}=\mathbf1_{\mathcal I_x}x_k\). The failed priority tests and terminal clock identity give the literal coordinate comparison`,
  String.raw`A more natural target than the raw inverse-duration moment is amplitude-sensitive terminal anti-concentration: find fixed, solution- and scale-independent \(N_{\rm sh}\), \(0<\delta_*<4\), \(0\le\theta_*<1\), and \(C_{\rm nc}<\infty\), such that every good terminal admits one set \(S_\tau\), \(\#S_\tau\le N_{\rm sh}\), satisfying`,
  "not an NSE counterexample",
  "not an NSE solution",
  "The constants are sharp at the scalar-constraint level. Optimizing the same exceptional set gives",
  "Apply finite-shell Holder to the same exceptional set, then invoke the shell-dependent-time-set estimate only once, to obtain",
  String.raw`For the atomic measure \(\mu_\tau=\sum_{k\in\mathcal H_\tau}w_k\delta_{h_k}\), Tonelli gives the exact layer-cake identity:`,
  "Prove or refute short terminal anti-concentration (S.261) and uniform selected-excess packing (S.269) separately, then test (S.272) with one shared fixed budget after adding the counts.",
  "Exact recombination of the shared best-N budget; the short-branch terminal trace and scalar-excess uniform packing remain open",
  String.raw`continues to exclude only scalar completed-clock algebra and unweighted genealogy; the Step 8 no-go is supplied by an inherited genuine smooth exact NSE family; and the Step 9 no-gain shows that canonical stops do not compress by themselves. Step 10 proves that the four paid classes together use only one \(6B_Q\) ledger and one \(C_5\) cubic ledger, leaving exactly one residual gate on \(\mathcal R_{\rm sh}\cup\mathcal R_x\) with a shared best-\(N\) budget. Step 11 further proves the discrete infimal convolution of the shared budget; the short branch gains inverse-duration and nested-tent control but still lacks the depth-zero terminal trace; and the scalar-excess branch is equivalent to residual best-\(N\) with literal constants \(1/5\) and \(3\). Fixed-solution tail tightness cannot replace a fixed \(N_0\) independent of solution and scale. Existing multi-packet exact families also do not rule out any fixed positive \(N\). S.261, S.269, S.272, S.243, Q.12, Q.1, scale contraction, regularity, and singularity formation remain`,
  String.raw`Two best-\(N\) branch theorems give a combined best-\(2N\), not best-\(N\). The fixture \(a=(M,0),b=(0,M)\) gives`,
  "Two exact rational scalar clocks isolate the forbidden shortcut. The pure-defect row satisfies",
  String.raw`The shared best-\(N\) budget for the two residual mechanisms is an exact infimal convolution; the short branch still lacks a terminal trace, while the scalar-excess branch still lacks uniform packing.`,
  String.raw`Both show that full-history ancestry cannot be retrospectively restricted to \(J^{\rm LE}\). Repeating the pure-defect row gives`,
  String.raw`On both branches, \(T_k/6<r_k<T_k/2\le v_{k,R}/2\). For \(z\in\ell^1_+\), write \(\mathcal S_N(z)=\inf_{\#S\le N}\sum_{k\notin S}z_k\). If \(a,b\) have disjoint supports, then`,
  String.raw`Let \(\mathcal H_\tau=\mathcal R_{\rm sh}(\tau)\), \(a_k=2^{3k}\gamma_k\), and \(p_k=p_{k,R}^{u,\eta}(J_k^{\rm LE})\). Non-\(D\) persistence and the inherited cubic estimate give`,
  String.raw`Let \(\mathscr A_0=\sum_k2^{3k}\gamma_k<\infty\). For every \(0<\delta<4\),`,
  String.raw`If (S.272) holds, then (S.251), with \(N_0=N_{\rm sh}+N_x\), proves Step 10 (S.243), and conditionally yields R0.74Q (Q.12) and fixed-scale (Q.1). The implication is proved; the antecedent remains`,
  String.raw`To refute a fixed \(N\), a new smooth exact family must supply \(N+1\) distinct target shells such that`,
  "Thus the nonnegative cubic payment overwhelms its clock lower scale; it establishes neither (S.270) nor a refutation of fixed positive exception count. This is a quantitative obstruction to existing designs, not a no-go for every multi-packet architecture.",
  String.raw`Thus every residual surviving to a fixed positive backward depth already has quadratic control; all unresolved mass may concentrate at \(d_k\downarrow0\). An \(L^{3/2}\)-in-time tent bound has no depth-zero terminal trace.`,
  String.raw`It exactly shows that duplicate \(N\)-budgets silently double the total budget.`,
  "The next PDE stage retains two work packages: test short terminal trace through (S.261), and test selected-excess packing through (S.269) while separating anomalous measure from high-Rayleigh viscous mass. Any adversarial exact family must first pass (S.270), not merely display several terminal lobes.",
  "The existing common-shear multi-packet construction creates distinct terminal lobes but also proves the exterior cubic lower bound",
  "Existing smooth exact families refute only the zero-exception route. The cubic cost of current multi-packet designs is too large to refute any fixed positive exception count.",
  "Strict nesting alone also cannot help: a continuous clock/payment tower can have nested intervals and a small cubic integral while still satisfying",
  String.raw`In backward time \(s=(\tau-t)/R^2\), define \(M_I(s)=\sum_{k\in I,d_k>s}r_k^{\rm sh}\) and \(V_I(s)=\sum_{k\in I,d_k>s}a_k\). All last-exit intervals share the terminal endpoint, so their indicator is exactly \(\mathbf1_{\{s<d_k\}}\). Weighted Holder, (R.214), and (R.211) give`,
  String.raw`Thus the \(\mathcal R_x\) gate has been reduced exactly but not closed.`,
  String.raw`Hence \(\mu_\tau((0,s])\lesssim s^{2+\varepsilon}\) is sufficient, but critical exponent two is not. With fixed profile \(\lambda_k=1\), \(w_k=2^{3k}\gamma_k\), and \(h_k=w_k^{1/2}\), one may have \(\mu((0,s])\le2s^2\) while`,
  "Thus the short-branch gap is terminal anti-concentration, not interval overlap; the excess-branch gap is uniform weighted packing, not ancestry classification. Both remain",
  String.raw`By (S.263), this is equivalent up to literal constants to the \(\mathcal R_x\) residual gate.`,
  String.raw`On the short branch define \(h_k=d_k\lambda_k^{3/2}\in(0,1)\) and \(w_k=a_k\lambda_k^3\). Let \(\mathcal H_j=\{2^{-j-1}\le h_k<2^{-j}\}\) and \(W_j=\sum_{k\in\mathcal H_j}w_k\). Then`,
  String.raw`This is the logarithmic obstruction at the critical \(s^2\) Carleson endpoint. It is a coefficient/clock stress test,`,
  String.raw`Equality generally fails here because supremum and finite minimum do not commute; the optimal budget split and top-\(N\) shells may depend on \(\tau\). If the two branches close with fixed \(N_{\rm sh},N_x\), put \(N_0=N_{\rm sh}+N_x\). Then`,
  "This is an abstract continuous clock/payment witness,",
  "This is a pointwise equality. Taking the terminal supremum gives only the domain-safe inequality:",
  "This is the inherited Step 10 structure figure. Step 11 is an analytic reduction and introduces no new figure; terminal trace and selected-excess packing remain open.",
  String.raw`This is genuine nonuniform compactness, but what is missing is exactly a uniform \(N\), independent of solution and scale, with an \(O(A_R)\) rate; the two statements must not be conflated.`,
  String.raw`These are only linear ledgers when \(P_R^M>1\), so Markov counting cannot produce a universal quadratic best-\(N\) tail. On the other hand, since \(r_k^x\le v_{k,R}/2\) and \(v_R\in\ell^1\), for each fixed solution, fixed \(R\), and \(\varepsilon>0\), one can choose a dependent \(N=N(u,R,\varepsilon)\) such that`,
  String.raw`This is only a sufficient interface, not an estimate on \(\mathfrak D_N^{\rm sh}\); it identifies the remaining debt exactly as inverse-square duration.`,
  "The primary certificate passes 14/14 exact, 7/7 finite, 34/34 structural, and 7/7 negative mutations. The independent Ruby audit passes 7/7 groups, 206,891 cases, 6/6 artifact locks, 7/7 dependency locks, and 59/59 note checks; the canonical stdout SHA-256 is `506440647a0a9b5be9d65ded24762b6eb6f6ce8cf054473a0ac04bf8835a1ffb`. These finite certificates support implementation reproducibility only and do not replace the inherited local-energy/PDE analysis.",
  "Status · R0.74S STEP 11",
  "The final combined theorem is",
  String.raw`The combined residual is the exact discrete infimal convolution of the two branch best-\(N\) tails. The branches may be studied separately, but exception counts must be added; two fixed finite counts still suffice for the final goal of some fixed \(N_0\).`,
  "excess constants: 1/5 and 3",
  "F / Previous-stage structure figure",
  "The pure high-Rayleigh row satisfies",
  String.raw`R0.74S Steps 1--10 separately sealed one-sided ball completion, the terminal Abel identity, four-channel circular recombination, the abstract scalar no-go for unweighted genealogy, the low-Rayleigh payment, the no-exception exact-family no-go, the canonical last exit, and the paid/residual six-class partition. Step 11 does not repeat that partition; it answers exactly how the two residual mechanisms share one best-\(N\) budget and advances each branch to its first missing PDE threshold.`,
  "S.248–S.272: PROVED and OPEN claims separated",
  String.raw`On the scalar-excess branch, the stopped residual and Step 8 priority-selected excess are equivalent in best-\(N\) with literal constants \(1/5\) and \(3\). The inherited theory gives only linear summability and fixed-solution tightness, not a solution- and scale-independent count.`,
  String.raw`The short non-\(D\) branch gains the sharp inverse-duration coefficient, a nested-tent integral, and control at every positive backward depth; the depth-zero terminal trace remains missing, and the critical \(s^2\) Carleson endpoint has a logarithmic divergence.`,
  String.raw`Step 10 forces these target shells into the combined residual eventually, so \(\mathcal S_N(r)/A_R\to\infty\). The existing R0.74O/P single-packet family passes this test only for \(N=0\): one positive exception may delete its only large coordinate.`,
  String.raw`Step 10 reduced the full-terminal clock estimate to one combined best-\(N\) tail on two disjoint residual mechanisms. Step 11 does not prove that tail estimate; it determines exactly how the branches recombine, how far their current estimates go, and which new PDE statement would close the short branch.`,
  "Step 10 paid-branch deletion and residual gate",
  "Step 11 independent audit",
  "Step 11 machine-certificate JSON",
  "Step 11 analytic main text, certificates, and independent audit",
  "Step 11 certificate report",
  "Step 11 primary audit",
  "Step 11 final analytic main text",
  "Step 11: Python 14/14 exact, 7/7 finite, 34/34 structural, and 7/7 mutations; Ruby 7/7 groups, 206,891 cases, 6/6 artifact locks, 7/7 dependency locks, and 59/59 note checks. Finite certificates do not replace the inherited local-energy/PDE analysis.",
  String.raw`The Step 8 ancestor vector \(b_k=\mathbf1_{\mathcal I_x}[m_{k,R}+\int_{H_{k,R}}g_{k,R}]\) satisfies`,
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
  assert.equal(rows.length, english.length, "R0.74S Step 11 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74S Step 11 English translation drift");
} else {
  assert.equal(missingBefore.length, english.length, "R0.74S Step 11 source-string count drift");
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

process.stdout.write(`${JSON.stringify({ release: "R0.74S Step 11", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
