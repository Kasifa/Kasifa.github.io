#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074sstep12";

const english = [
  "Prove or refute the common-window gate S.280 and ancestor gate S.288 separately, then test S.303; the conditional Morrey theorem is not a closure for the bare suitable-weak class.",
  "The terminal-window reduction is closed; Morrey packing holds only under additional uniform hypotheses, while S.280 / S.288 / S.303 remain OPEN. NOT CLAY.",
  "The terminal-window reduction is closed; Morrey packing holds only under additional uniform hypotheses, while the universal gates remain OPEN. NOT CLAY.",
  "Review v1.91 · 2026-09-03",
  "R0.74S Step 12 reduces the short branch to the common-window gate S.280 and closes excess packing under additional uniform Morrey/path hypotheses; S.280, S.288, and S.303 remain OPEN in the bare class.",
  "R0.74S: Common terminal windows and conditional Morrey packing",
  "R0.74S｜Common terminal windows and conditional Morrey packing",
  "The short branch is reduced to a continuous common terminal window; the excess branch closes under uniform critical Morrey/path-length hypotheses. S.280, S.288, and S.303 remain OPEN. NOT CLAY.",
  "Step 10 historical structure figure",
  "Step 10 historical figure",
  "Prove or refute S.280 and S.288 separately, then test the combined target S.303.",
  "Literature review v1.91 · 2026-09-03",
  "Common terminal windows and conditional Morrey packing",
  "PROVED: terminal-window reduction, continuity, the best-N layer cake, the averaged P^(4/5) method boundary, honest ancestor-budget addition, the conditional moving-tube Morrey theorem, the mixed-norm benchmark, and the no-winding/occupation screen. ABSTRACT NO-GO: S.281 and S.301 are not NSE counterexamples. FINITE: Python 16/16 exact, 12/12 finite, 51/51 structural, and 11/11 mutations; Ruby 12/12 groups, 153,237 cases, and 39/39 note checks. OPEN: S.280, S.288, S.303, S.272, Q.12, Q.1, and regularity. The speed-only route is only kinematically screened; this is not a universal PDE no-go.",
  "R0.74S Step 12 public boundary",
  "S.273–S.280 reduce the short trace to a continuous common-window/all-threshold gate; S.285–S.300 give the honest budget sum, conditional moving-tube Morrey theorem, and mixed-norm benchmark. S.280, S.288, and S.303 remain open.",
  "Step 12 writes the short residual as a common terminal-window target and proves excess packing under additional uniform critical Morrey/path-length hypotheses; it claims neither a universal theorem from the bare suitable-weak ledger nor novelty or priority.",
  "Research-note master index · v1.91 · 2026-09-03",
  "Common terminal windows and conditional Morrey packing",
  String.raw`, and it does not identify the earlier packet deposit with the complete ancestor vector \(b\).`,
  "; the second is proved only under the additional uniform hypotheses of Sections 65/66.",
  String.raw`: the terminal variation-window reduction (S.274)--(S.275); continuity and the fixed-solution modulus (S.276)--(S.277); the best-\(N\) layer cake and all-threshold implication (S.278)--(S.279); the \(L_t^1\)-only abstract no-go and averaged \(P^{4/5}\) boundary (S.281)--(S.284); exception-budget recombination and conditional charging (S.285)--(S.287); the moving-tube cover and conditional critical-Morrey theorem (S.289)--(S.294); the mixed-norm sufficient benchmark (S.295)--(S.300); literal no-winding and the occupation lemma (S.304)--(S.305); and the abstract super-Gaussian filter (S.306).`,
  ": S.280, S.288, S.303, Step 11's S.272, Q.12, Q.1, scale contraction, regularity, and singularity. The constants in the conditional Morrey and mixed-norm conclusions depend on their additional uniform bounds; no novelty or priority is claimed. No DNS, floating-point asymptotics, or DGX.",
  String.raw`: the universal terminal-window gate S.280; the universal ancestor gate S.288; the combined S.303; Step 11 S.272; Q.12 and Q.1; a uniform critical Morrey/path estimate from the frozen payment alone; identification of an earlier moving-packet deposit with the complete \(b\); a universal shell count for the bare suitable-weak class; and scale contraction, regularity, singularity, and Clay.`,
  String.raw`. It proves only that AC plus the linear total-mass ledger cannot imply a uniform fixed-\(N\), \(P^{2/3}\)-scaled window estimate; this is a precise abstract no-go.`,
  String.raw`. Allowing \(M=M(u,R)\) or \(L=L(u,R)\) recovers only nonuniform fixed-solution finiteness and must not be presented as uniform packing for the bare suitable-weak class.`,
  "58. Step 12: Common terminal windows and conditional Morrey packing",
  "59 / Complete text",
  "59. Frozen setting and the common terminal window",
  "60 / Complete text",
  "61 / Complete text",
  "61. Terminal continuity and the missing uniform modulus",
  "62 / Complete text",
  "62. Layer cake: the exact all-threshold counting problem",
  "63 / Complete text",
  String.raw`63. The method boundary of the inherited \(L_t^1\) ledger`,
  "64 / Complete text",
  "64. The excess branch and honest exception accounting",
  "65 / Complete text",
  "66 / Complete text",
  "67 / Complete text",
  "67. Why partial regularity does not close the excess gate",
  "68 / Complete text",
  "69 / Complete text",
  "69. Route decision and combined target",
  "70 / Complete text",
  "70. Kinematic screen for accelerating one packet",
  "71 / Complete text",
  "71. Step 12 claim boundary and dual audit",
  "72 / Complete text",
  String.raw`Stopping greedily by elapsed time \(O(R^2)\) or accumulated path variation \(O(2^kR)\), one needs at most`,
  String.raw`Extend \(|\dot F_{k,R}|\) by zero outside \(\mathcal T_R\). For \(0<\delta<4\), define`,
  String.raw`Insert a smooth spacetime test equal to one into the distributional definition of \(\boldsymbol\mu\) to obtain`,
  "Retain all definitions from R0.74S Steps 10--11:",
  String.raw`There are six conclusions: the short residual is controlled by the absolute shell-flux variation in one common terminal window and the proved positive-depth cubic term; the new window functional is continuous in the terminal, but the fixed-solution modulus is not uniform over solutions and scales; the exact best-\(N\) layer-cake identity turns the question into shell counting at every threshold; the anomalous-defect and high-Rayleigh ancestors of the selected excess require honestly added exception budgets; a uniform critical Morrey coefficient for total local dissipation and a uniformly bounded lifted path length in units of \(R\) yield conditional Morrey packing through a moving-tube cover; and uniform acceleration of one inherited passive packet is kinematically screened and does not bypass the cubic obstruction.`,
  String.raw`For every \(\tau\in\mathcal G_R\cap\mathcal T_R\), retain \(r_k^{\rm sh}\), \(d_k=(\tau-\ell_k)/R^2\), and the inherited absolute-flux ledger`,
  "not a Navier--Stokes solution",
  "not an NSE defect measure",
  "not a universal PDE no-go",
  String.raw`After removing at most \(\eta R^2\) of terminal times,`,
  "Substitution into S.294 gives",
  String.raw`But this modulus depends on the solution and scale, while the positive-depth term in S.275 grows as \(\delta^{-2/3}A_R\); it therefore gives no universal estimate.`,
  "The frozen exact family makes no complete winding of the packet centre around the torus; the all-winding estimates in R0.74F concern periodic copies of the Brownian-bridge heat kernel, not packet-centre orbits.",
  String.raw`For \(z\in\ell^1_+\), define \(n_z(t)=\#\{k:z_k>t\}\). Deleting the largest \(N\) coordinates and applying Tonelli gives`,
  "Prove or refute the common-window gate S.280 and ancestor gate S.288 separately, then test the combined target S.303; do not present the conditional Morrey theorem as a theorem for the bare suitable-weak class.",
  String.raw`backward \(R\)-cylinders cover \(\mathcal U_{k,R}(\tau)\). Arc-length stopping cannot be replaced by endpoint displacement. Since \(\boldsymbol\mu=|\nabla u|^2dxdt+\boldsymbol D\) is one exact decomposition, adding the defect and restricted high-Rayleigh viscous parts pays the tube's total mass only once:`,
  String.raw`Fix \(N\), set \(M=N+1\), and place \(M\) synchronized AC spikes in the same terminal window to obtain`,
  String.raw`Assume common constants \(M,L<\infty\) for the entire restricted solution class, all scales, and all terminals:`,
  String.raw`may be supported on finitely many points while placing nonzero weighted mass in each of \(M\) moving annular tubes. It is only a measure countermodel to the implication "dimension gives packing automatically,"`,
  "The two ancestor vectors may overlap, but the union of their deletion sets gives",
  "Both antecedents remain",
  String.raw`Put \(\mathscr A_m=\sum_{k\ge1}2^{mk}\gamma_k<\infty\) (\(m=2,3\)); then`,
  String.raw`Let \(\widetilde{\boldsymbol\mu}\) be the periodic lift of the total local dissipation measure, let \(\widetilde X_R\) be the continuous lift of the mollified path, and define the full-history tube`,
  String.raw`Let \(g_R(t)=\sum_k|\dot F_{k,R}(t)|\in L^1(\mathcal T_R)\). If \(\tau_n\to\tau\), then`,
  String.raw`Let \(q\in[3,\infty]\), \(r\in[3,\infty)\), and \(\theta=3/r+2/q\), and assume at every target scale of the restricted class that`,
  String.raw`The remaining coordinates with \(d_k>\delta\) are controlled by Step 11 (S.259) using the same \(S\), so`,
  String.raw`If \(k\in\mathcal R_{\rm sh}(\tau)\) and \(d_k\le\delta\), then \(J_k^{\rm LE}\subset J_{\tau,\delta}\). Hence, for every \(S\subset\mathbb N\),`,
  String.raw`If a hypothetical monotone extension satisfies \(0<\beta B\le q'(t)\le B\), then for a measurable torus set \(J\), with \(D=q(T)-q(0)\) and \(m=\lfloor D/(2\pi)\rfloor\), change of variables gives the exact occupation bound`,
  String.raw`Suppose there is one shared exceptional set \(E_\tau\), \(\#E_\tau\le N_b\), and outside it \(b_k\le q_k+c_kp_k^{2/3}\), \(\sum q_k\le C_qA_R\), \(\sum p_k\le C_pP_R^M\), and \(\sum c_k^3\le C_c\). Then shellwise Holder gives`,
  String.raw`If the interior optimizer lies in \((0,4)\), balancing the two terms yields only`,
  String.raw`Thus \(\tau\mapsto\mathcal V^F_{N,R}(\tau,\delta)\) is continuous, and the supremum over good terminals equals that over all of \(\mathcal T_R\). For each fixed \((u,R)\), absolute continuity of the Lebesgue integral also gives`,
  "Thus uniform speed-up changes only a common prefactor, not the super-Gaussian shell ratio. This is a kinematic screen,",
  String.raw`Also \(|\dot X_R(t)|\le CR^{-3/r}\|u(t)\|_{L^r}\), so`,
  String.raw`A sufficient distributional theorem is therefore to find fixed \(N_F\) and one \(\Phi\in L^1(0,\infty)\), uniform over solutions, scales, and terminals, such that`,
  String.raw`The bounded literature search covered Caffarelli--Kohn--Nirenberg partial regularity, De Rosa--Drivas--Inversi on anomalous-dissipation support, Seregin's critical Morrey estimates, Barker's singular-point count under an additional weak-\(L^3\) bound, and Neustupa's singular-point \(L^3\) concentration. No theorem with exactly the quantifiers of S.280 or S.288 was found.`,
  String.raw`Combine this with the inherited linear cap \(\sum x_k^{\rm sel}\le C_0P_R^M\), choosing the stronger bound in the regions \(P_R^M\le1\) and \(P_R^M\ge1\), to obtain`,
  String.raw`On the Step 8 priority-selected set \(\mathcal I_x(\tau)\), define`,
  "This structural gain removes the last-exit selectors and branch masks from the new term, replacing them with a continuous functional on one fixed window.",
  "One common shell-deletion set is used for the entire window; it may not vary with time inside the integral.",
  String.raw`This is weaker than the required \(P^{2/3}\) scale and does not control the supremum terminal; it is the exact exponent boundary of this method, not a sharpness claim for NSE.`,
  "This is the inherited Step 10 structure figure, not a numerical result from Step 12. Step 12 is an analytic reduction and conditional theorem; no new figure or data have been fabricated.",
  "This is a vector-valued translated-spike witness,",
  "This is the genuinely proved",
  String.raw`These sources respectively control singular-set size, density under additional integrability, an assumed critical coefficient, or a singular-point count depending on an extra norm. None derives full-history high-Rayleigh annular best-\(N\) packing from the bare inherited ledger. The search marks the literature boundary; it is not a novelty or priority proof.`,
  String.raw`This is only a conditional sanity check: stronger regularity theory already covers critical strong-norm balls; when \(\theta>1\), finiteness of an individual solution's global mixed norm does not imply the scale-Morrey decay required by S.295. Nor is weak \(L^3\) inserted into the cubic row without a Lorentz endpoint argument.`,
  String.raw`A count at one threshold is insufficient; the critical \(A_R/t\) count still has a logarithmic divergence at the layer-cake endpoint. The clean short-branch target is`,
  "Exact terminal-window reduction; Morrey packing closes under additional uniform hypotheses, while the universal window and ancestor gates remain open",
  "The primary certificate passes 16/16 exact, 12/12 finite, 51/51 structural, and 11/11 mutations. The independent Ruby audit passes 12/12 groups, 153,237 exact cases, 6/6 artifact locks, 6/6 dependency locks, and 39/39 note checks; the two implementations independently seal the source and certificate boundary. Finite checks support only formula implementation and tamper detection; they do not replace the analytic proof.",
  "Status · R0.74S STEP 12",
  String.raw`CKN proves that the singular set has zero parabolic \(\mathcal H^1\)-measure. This is a support-size conclusion, not an upper bound on the mass density of \(\boldsymbol D\). Consider the abstract measure`,
  "The combined Step 12 target is",
  "The converse of epsilon regularity does not turn every large regular viscous mass into a singular point. Even a one-threshold singular-cylinder count would still need an integrable all-threshold mass distribution before it could imply S.288.",
  "F / Historical structure figure",
  "Fubini still gives the averaged-terminal statement:",
  String.raw`The high-Rayleigh ancestor belongs to \(|\nabla u|^2dxdt\) and may lie entirely in the regular set. Thus`,
  String.raw`The inherited R0.74F packet centre satisfies \(Q(t)=q_{\rm pre}+B\int_0^t\theta(s,h)ds\), \(|\theta|\le1\), and \(0<B\le(32R^2)^{-1}\), so`,
  String.raw`In the many-winding regime \(m\asymp BT\), the factor \(B\) from the number of visits cancels the inverse-speed residence time per visit, creating no exponential preference for outer dyadic shells. If \(z_\ell\le H2^{p\ell}\Gamma^{4^\ell}\) and \(q_N=2^p\Gamma^{3\cdot4^N}<1\), then`,
  "The mean-zero periodic pressure gauge and Calderon--Zygmund give",
  String.raw`After mixed Holder, every power of \(R\) cancels to one factor of \(R\):`,
  "The PDE must construct these objects while retaining full-history ancestry. The bare minimal statement remains",
  "S.273–S.306: PROVED / OPEN separated",
  "S.280 / S.288 / S.303 remain OPEN. NOT CLAY.",
  "S.280 is a sufficient replacement for S.261, not an equivalent reformulation; it is stronger, but its target is continuous, its window fixed, and it has no moving selector.",
  "The short branch is reduced to a continuous common terminal window; the selected-excess branch closes under uniform critical Morrey and path-length hypotheses.",
  String.raw`The short branch should directly attack the continuous common-window gate S.280, preferably through the all-threshold count S.279; scalar temporal \(L^1\), terminal averaging, or a critical one-threshold count without an endpoint gain has been proved insufficient. The excess branch should attack the shared ancestor charging S.287 or a uniform moving-tube coefficient sufficient for S.294; the defect and high-Rayleigh budgets must be added as in S.286.`,
  String.raw`Step 11 reduced the full-terminal clock estimate to two best-\(N\) tails: the short non-dissipation residual \(r^{\rm sh}\) and selected dissipation excess \(x^{\rm sel}\), equivalently \(r^x\). Step 12 does not prove either universal tail estimate; it rewrites both as cleaner PDE interfaces and proves one conditional packing theorem under additional uniform hypotheses.`,
  "Step 12 independent audit",
  "Step 12 machine-certificate JSON",
  "Step 12 certificate report",
  "Step 12 primary audit",
  "Step 12 analytic main text, certificates, and independent audit",
  "Step 12 final analytic main text",
  "Step 12: Python 16/16 exact, 12/12 finite, 51/51 structural, and 11/11 mutations; Ruby 12/12 groups, 153,237 exact cases, 6/6 artifact locks, 6/6 dependency locks, and 39/39 note checks. Finite certificates do not replace the analytic proof.",
];

process.chdir(root);
const [source, order, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings("./public"),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);
const baseCurrent = checkOnly ? current : current.filter((row) => !rowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missing = source.filter((entry) => !currentByZh.has(entry.zh));
const missingOrder = order.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missing.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => rowPattern.test(row.id));
  assert.equal(rows.length, english.length, "R0.74S Step 12 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74S Step 12 English translation drift");
} else {
  assert.equal(missing.length, english.length, "R0.74S Step 12 source-string count drift");
  const sourceByZh = new Map(missing.map((entry) => [entry.zh, entry]));
  const additions = missingOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = english[index];
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), `protected token drift ${index + 1}: ${entry.zh}`);
    return { id: `${prefix}${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...baseCurrent, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({ release: "R0.74S Step 12", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
