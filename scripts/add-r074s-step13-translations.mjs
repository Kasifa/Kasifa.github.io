#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074sstep13";

// Local, direct translations in the deterministic order returned by
// collectSiteStrings. TeX spans are preserved byte-for-byte.
const english = [
  "Current endpoint R0.74S Step 13",
  "The fixed-solution time modulus is proved; the current linear-payment route falls strictly short of the 2/3 target. The Morrey/Dini conclusions remain conditional, and the abstract witnesses are not NSE counterexamples. NOT CLAY.",
  "The fixed-solution time modulus is proved; the linear-payment ceiling, two-cap 2/3 threshold, and critical cubic tree are now fixed exactly. The PDE gates remain OPEN. NOT CLAY.",
  "The fixed-solution time modulus is proved; the linear-payment method ceiling, two-cap 2/3 threshold, and critical cubic tree are now fixed exactly. The PDE gates remain OPEN. NOT CLAY.",
  "If started separately, test the PDE incidence/strict cubic Dini gain, S.342, and bare-class S.328; this release does not start Step 14.",
  "Not started",
  "Research note R0.74S Step 13 · 2026-09-03",
  "Formal analytic schematic",
  "Review v1.92 · 2026-09-03",
  "R0.74S Step 13 fixes the linear-payment temporal-exponent ceiling and the Morrey 2/3/cubic Dini thresholds; S.328 and S.340 remain conditional, while S.342 and the PDE packing gates remain OPEN.",
  "R0.74S: Temporal-integrability ceiling and combined Morrey threshold",
  "R0.74S｜Temporal-integrability ceiling and combined Morrey threshold",
  "Step 13 formal analytic schematic",
  "Step 14 / R0.74T follow-up interface",
  "Not started in this release",
  "If started separately: test the PDE incidence/strict cubic Dini gain, S.342, and bare-class S.328.",
  "Temporal-integrability ceiling and combined Morrey threshold",
  "Literature review v1.92 · 2026-09-03",
  "PROVED: fixed-solution ell1(L_t^(4/3)), the delta^(1/4) common-window modulus, general Holder algebra, the exact ceiling under explicit S.316, the payment-dependent Morrey implication, heat-shear identities, the conditional incidence theorem, and cubic duality. ABSTRACT: the smooth saturation, two-cap, and eight-ary trees are not NSE counterexamples. FINITE: Python passes 31/31 exact, 11/11 finite, 22/22 structural, 4/4 dependency, and 32/32 negative checks; Ruby passes 9/9 groups, 72,027 cases, and 32/32 note checks. OPEN: the uniform H-tail, S.342, bare S.328, PDE incidence/Dini gain, S.280, S.288, S.303, Q.12, Q.1, and regularity.",
  "R0.74S Step 13 public boundary",
  "S.307–S.325 give the fixed-solution time modulus, exact linear-payment ceiling, and abstract saturation; S.326–S.341 give the conditional Morrey inference, two-cap 2/3 threshold, heat-shear screen, and critical cubic-tree/Dini interface. S.342 and the PDE gates remain open.",
  "Step 13 proves the fixed-solution time modulus and fixes the thresholds of the current linear-payment method, two-cap Morrey argument, and cubic tree exactly; it does not present abstract boundary tests as NSE counterexamples or claim novelty or priority.",
  "Research-note master index · v1.92 · 2026-09-03",
  ", not a simulation, DNS, or NSE counterexample, and not evidence for regularity or a Clay result.",
  String.raw`: a uniform payment bound for \(\mathfrak H^F_{4/3,N,R}\); the quadratic shell-selective estimate S.342; PDE incidence data and a strict cubic Dini-Carleson gain for S.340; the payment-dependent moving-tube estimate S.328 for the bare suitable-weak class; the universal gates S.280, S.288, and S.303; Step 11 S.272; Q.12 and Q.1; and scale contraction, regularity, singularity formation, and the Navier--Stokes Millennium problem.`,
  ": obtains pressure-sensitive local-energy and epsilon-regularity criteria from scale-integrated inputs; it does not supply the coefficient in S.316 or S.328.",
  String.raw`: quantifies a dissipation-energy pigeonhole and proves logarithmically improved partial regularity; its annular levels and constants depend on natural local energies and do not give a common-terminal fixed-physical-shell best-\(N\) flux estimate.`,
  String.raw`: uses a Carleson-type spacetime norm in the critical small-data \(BMO^{-1}\) class; it does not derive a Carleson estimate from \(P_R^M\) for every bare suitable weak solution.`,
  ": obtains reverse Holder improvement under uniformly bounded scaled local kinetic energy; that is precisely additional information absent from the bare payment ledger.",
  String.raw`: the dimensionless/common-deletion representation S.307--S.309; fixed-solution \(\ell^1(L_t^{4/3})\) finiteness and the \(\delta^{1/4}\) common-window bound S.310--S.313; the general Holder bound S.314--S.315; exact optimization algebra S.317--S.322 under explicit S.316; the smooth all-\(p\) abstract saturation witness S.323--S.325; the payment-dependent Morrey implication S.326--S.330 under the explicit geometric envelope S.328; sharpness of the two-cap inference in S.331; exact heat-shear identities S.332--S.334; the critical eight-ary abstract countermodel S.335--S.339; and the conditional incidence-charging theorem, exact cubic duality, and Dini-subcritical criterion S.340--S.341.`,
  ": the synchronized temporal family S.323--S.325; the subsequent adaptive smooth rate/depth family; the equal-coordinate two-cap family S.331; and the eight-ary critical ancestor tree S.335--S.339.",
  ". This step does not prove Q.12, Q.1, scale contraction, regularity, singularity formation, or the Millennium problem; it uses neither DNS nor DGX.",
  String.raw`At \(p=1\) there is no positive window power, and the linear term remains \(P\). In S.320, as \(p\to\infty\), the exponent increases monotonically toward \(4/5\), still above the target \(2/3\).`,
  "72. Step 13: Temporal-integrability ceiling and combined Morrey threshold",
  "73 / Complete text",
  "73. Dimensionless flux density and the common deletion order",
  "74 / Complete text",
  String.raw`74. The fixed-solution \(L_t^{4/3}\) fact`,
  "75 / Complete text",
  "75. General temporal exponents and exact optimization",
  "76 / Complete text",
  String.raw`76. Smooth all-\(p\) abstract saturation witness`,
  "77 / Complete text",
  "77. Exact scalar threshold for the moving-tube route",
  "78 / Complete text",
  "78. Why dynamic high frequency alone cannot attack the flux gate",
  "79 / Complete text",
  "79. Bounded primary-literature boundary",
  "80 / Complete text",
  "80. Critical eight-ary abstract countermodel",
  "81 / Complete text",
  "81. Conditional incidence theorem and cubic Dini interface",
  "82 / Complete text",
  "82. Step 13 route decision and claim ledger",
  "83 / Complete text",
  String.raw`Scale the pure high-Rayleigh scalar row in Step 11 S.267 by \(s_v\):`,
  "Retain all settings from R0.74S Step 12. Let",
  String.raw`This step has five conclusions. First, for each fixed periodic suitable weak solution and fixed scale, the physical shell-flux density has a summable \(\ell^1(L_t^{4/3})\) envelope; this follows from the energy-class interpolation \(u\in L_t^4L_x^3\), the periodic Calderon--Zygmund pressure estimate, and the fixed-scale mollified-drift bound. Second, a common terminal window of dimensionless length \(\delta\) consequently gains \(\delta^{1/4}\); a general \(L_t^p\) shell-tail estimate gains \(\delta^{1-1/p}\), but the entire window may delete only one common shell set. Third, that time gain does not repair the payment exponent: even if one additionally assumes that the relevant \(\ell^1(L_t^p)\) tail depends linearly on \(P_R^M\), balancing it with the positive-depth term gives only \(P^{2(2p-1)/(5p-3)}\); the energy-class value is \(P^{10/11}\), and even \(p=\infty\) gives only \(P^{4/5}\), all short of \(P^{2/3}\). Fourth, a smooth \((N+1)\)-coordinate witness shows that arbitrarily high scalar temporal regularity together with payment-linear amplitude cannot by itself imply the fixed-window best-\(N\) gate; this is an abstract vector witness, not a Navier--Stokes solution. Fifth, Step 12's separate uniform Morrey/path assumptions can be weakened to a combined cover coefficient growing at most like \(1+(P_R^M)^{2/3}\); \(2/3\) is the exact threshold for an argument using only the two scalar caps, but is not claimed necessary for other PDE proofs.`,
  "The advance is a fixed-solution algebraic terminal modulus, the exact temporal-integrability ceiling of the current two-term method, a weaker combined Morrey interface for the excess branch, and a critical-tree obstruction identifying strict cubic Dini decay as the next conditional packing interface.",
  "This publication stops at Step 13. If started separately, the next targets are a PDE-level incidence/Dini gain, S.342, and bare-class S.328; the conditional interface must not be presented as a theorem.",
  String.raw`and extend every derivative by zero outside \(\mathcal T_R\). Define`,
  String.raw`Use the mean-zero periodic pressure gauge. Shellwise gauge cancellation permits this gauge in the signed derivative of \(F_{k,R}\). The energy class and spatial interpolation give`,
  String.raw`Therefore, for every terminal and \(0<\delta<4\),`,
  String.raw`There is an exact sufficient substitute. Suppose every terminal has a shell set \(E_\tau\), \(\#E_\tau\le N_b\), nonnegative \(q_k\), tree payments \(p_\nu\), coefficients \(c_\nu\), and incidences \(\nu\rightsquigarrow k\), such that outside \(E_\tau\)`,
  String.raw`When \(P\ge1\), \(\beta>2/3\), and the optimizer lies in \((0,4)\), the balancing scale is`,
  String.raw`When the denominator is nonzero, equality is attained by \(p_\nu=c_\nu^3/\sum_\omega c_\omega^3\). Turning the tree inequality into the incidence coefficient bound in S.340 still requires three uniform inputs:`,
  "Define the combined cover coefficient",
  String.raw`For nonnegative shell densities in \(\ell^1(L^p(0,4))\), the same proof gives`,
  String.raw`For \(1\le p\le\infty\) and integer \(N\ge0\), define the common-deletion temporal tail`,
  String.raw`For each fixed periodic suitable weak solution in the frozen class and each fixed \(R>0\), let`,
  "Direct optimization of the coefficient actually proved by Proposition 2.1 gives the fixed-solution estimate",
  String.raw`For an argument that knows only the two scalar caps in S.327, the exponent threshold is sharp. If \(\theta>2/3\), fix \(N\), set \(M=N+1\), and for large \(P\) take \(M\) equal coordinates with total mass \(T_P=\min\{C_0P,C_BP^\theta\}\), setting \(x_k^{\rm sel}=b_k=T_P/M\). Then`,
  String.raw`Interpret \(r=2\) separately as \(q(2)=\infty\). For admissible factors whose three spatial Holder reciprocals sum to one,`,
  "Not simulation / DNS · NO DGX",
  "The nonnegative child factors satisfy the uniform Dini product sum",
  String.raw`Fix \(N\ge0\), set \(M=N+1\), take \(0<\delta_0<4\) and nonnegative \(\phi\in C_c^\infty((-\delta_0,0))\) with \(\int\phi=1\), and choose a terminal \(\vartheta_0\) so that the translated support lies in \((0,4)\). For \(H>0\), define`,
  String.raw`Fixed-scale convolution maps \(L_x^2\) into \(L_x^\infty\), so \(|a_R(t)|\le C_R\|v_R(t)\|_2\). The inherited cutoff bound and super-Gaussian shell weights give \(\sum_{k\ge1}\gamma_k(1+2^{3k}R^3)<\infty\). Taking absolute values only after changing the pressure gauge, R0.74P (2.9) gives`,
  String.raw`The fixed-solution \(\ell^1(L_t^{4/3})\) and \(\delta^{1/4}\) common-window modulus are proved; the exact exponent ceiling of the current linear-payment route remains strictly above \(2/3\).`,
  "Fixed-solution time modulus, linear-payment method ceiling, combined Morrey threshold, and critical cubic tree; the PDE gates remain open",
  String.raw`Fix an integer \(m\ge1\), set \(L=m^3\), and take a complete eight-ary tree with depths \(0\le d\le L-1\). At depth \(d\), for each node \(v\), define`,
  String.raw`Thus the temporal exponent is still \(4/3\). The symmetric pressure choice first places \(v_R\otimes v_R\) in the strong Calderon--Zygmund range \(L_x^{3/2}\); neither the \(L^1\) weak endpoint nor the \(L^\infty\)-to-BMO endpoint is used.`,
  String.raw`There is also a smooth abstract witness saturating the adaptive \(p=4/3\) balance. For \(P\ge1\), choose \(0\le\rho\in C_c^\infty((-1,0))\) with \(\|\rho\|_{4/3}=1\), and set`,
  String.raw`This closes the selected-excess gate. \(M_R\) and \(L_R\) may each be nonuniform provided their weighted cover cost grows no faster than the quadratic payment scale.`,
  "Next test whether a bounded-branching ancestor tree together with the existing linear and square ledgers forces extra packing. At the critical tree exponent, it does not.",
  String.raw`The optimistic linear case \(\beta=1\) gives`,
  "The payment power produced jointly by the two terms is",
  String.raw`Let the bracket in S.313 at \(t=t(\sigma)\) be \(\mathcal B_R(\sigma)\). What is actually used is`,
  String.raw`Every coordinate is at most \(m^{-2}\). After deleting any fixed \(N\) coordinates, there remains`,
  String.raw`Every node lies strictly in the abstract \(\mathcal I_x\) branch, with pure high-Rayleigh ancestry. Summing by levels gives`,
  String.raw`Every primitive is smooth and increasing, and for every \(1\le p\le\infty\),`,
  String.raw`Every fixed node is counted in at most \(M_{\rm inc}\) incidences;`,
  String.raw`Its dissipation-to-cubic ratio grows like \(n^2/A\), but the canonical physical-flux primitive is zero and the completed clock satisfies \(K=Q\). Thus high Fourier frequency and a high Rayleigh ratio do not by themselves create a short physical-shell flux tail; here \(k\) indexes physical moving annuli, not Fourier shells. This screen does not extend to a zero-flux theorem for arbitrary dynamic high-frequency fields.`,
  String.raw`Here \(L_t^\infty L_x^2\cap L_t^2H_x^1\subset L_t^4L_x^3\), while the periodic Calderon--Zygmund estimate is`,
  "The second term is the strong square-Carleson bound; the third is asserted only for nonterminal nodes and is at exact critical equality: eight children each receive half the coefficient, conserving the coefficient cube.",
  String.raw`If the abstract payment is normalized by \(P_H\asymp H\), then`,
  "The cube is the exact dual exponent, not a convenient choice. For every finite nonnegative coefficient vector,",
  String.raw`Together the three inputs give \(\sum_{\rm incidences}c_\nu^3\le M_{\rm inc}C_{\rm root}C_D\), supplying the \(C_c\) required by S.340. Uniform \(\theta_d\le\theta<1\) is a simple special case. The critical tree in S.335 has \(\theta_d=1\), and its finite-depth Dini constant grows like \(L=m^3\), so it cannot supply a uniform coefficient bound.`,
  String.raw`After deleting \(N=M-1\) coordinates, exactly \(c_\rho P^{10/11}/M\) remains. Assign each coordinate an abstract depth \(d_{k,P}=d\) and residual \(r_{k,P}=c_\rho P^{10/11}/M\). If \(\delta\ge d\), the common terminal window charges the full residual; if \(0<\delta<d\), the coordinate lies in the deep class and`,
  "Previous milestone recap (through R0.74O, 157 sections, unchanged)",
  "Temporal-integrability ceiling, Morrey 2/3 threshold, and critical cubic tree",
  String.raw`Thus the linear total ledger, vanishing global square ledger, bounded branching, square-Carleson subtree estimate, and critical child decay still do not imply S.288. Stopping one ancestor cannot count as deleting one shell exception while all its descendants are deleted for free; the best-\(N\) functional deletes individual shell coordinates.`,
  "In particular,",
  String.raw`The full scaling calculation uses \(\sum_k\gamma_k|\nabla\Psi_k^R|\le CR^{-1}\) and the periodic interpolation inequality`,
  "A bounded search found no theorem with the quantifiers needed in Step 13 that directly supplies a uniform temporal tail or S.328.",
  String.raw`Choose \(\vartheta_0\) so that \(\vartheta_0+d\,\operatorname{supp}\rho\subset(0,4)\), and define`,
  String.raw`Thus Step 12's separate assumptions \(M_R\le M\) and \(L_R\le L\) are stronger than algebraic closure requires.`,
  String.raw`Hence, up to the fixed constant \(c_\rho\), \(10/11\) is sharp for the abstract combination of a linear \(\ell^1(L^{4/3})\) rate bound, the inherited linear \(L^1\) ledger, depth allowance, and a fixed deletion budget. It remains only a method-level countermodel, not an NSE realization.`,
  String.raw`This is therefore an \(\ell^1(L^{4/3})\) estimate, not an illicit exchange with \(L^{4/3}(\ell^1)\). The exponent \(4/3\) is the endpoint supplied by direct energy-class interpolation for the spatial cubic integral; additional PDE hypotheses may still yield higher temporal integrability.`,
  String.raw`Thus whenever the temporal coefficient grows faster than \(P^{2/3}\), no \(p\), including \(p=\infty\), removes the exponent loss. Conversely, within this two-term argument, \(\beta\le2/3\) is sufficient in the large-payment regime; the small-payment regime follows from \(P\le P^{2/3}\) and the inherited linear ledger.`,
  String.raw`Since \(|\mathcal T_R|=4R^2\), the \(L_t^{4/3}\) norm of the cubic/pressure part is at most \(CR^{-1/2}[e_R(e_R+d_R)]^{3/4}\), and the \(L_t^\infty\) norm of the drift part is at most \(CR^{-2}e_R^{3/2}\). Under the change of variables in S.307, the former gains \(R^{1/2}\) and the latter \(R^2\), proving S.310; applying Holder to a fixed deletion set in S.308 gives S.311.`,
  "The finite certificate passes 31/31 exact, 11/11 finite, 4/4 dependency, 22/22 structural, and 32/32 negative-mutation checks; the independent Ruby verifier passes 9/9 groups, 72,027 exact cases, 6/6 artifact locks, 4/4 dependency locks, 32/32 note checks, 1/1 primary-artifact group, and 2/2 negative groups. They check algebra, finite fixtures, hashes, structure, and claim wording; they do not machine-prove PDE estimates, open packing gates, the Morrey hypothesis, an NSE realization of an abstract model, regularity, or the Millennium problem.",
  "Allow the Step 12 quantities to depend on the solution, scale, and terminal:",
  String.raw`On the \(2\pi\)-periodic torus, take \(A>0\), \(T>0\), and an integer \(n\ge1\):`,
  "At the balancing depth,",
  "Proposition 2.1 then proves",
  "The common-window coordinate in S.273 is exactly",
  String.raw`Using Holder with exponents \(3\) and \(3/2\) on the incidence set gives`,
  String.raw`This witness has a fixed smooth time profile and belongs to every temporal \(L^p\) space. It proves only a logical boundary: temporal regularity plus a scalar linear-amplitude bound does not contain S.280. It is not a velocity field, pressure, suitable weak solution, or NSE counterexample.`,
  String.raw`This tree is a strict abstract ledger model. Its nodes are not jointly realized as physical moving annuli of one solution; it does not satisfy the coupled Navier--Stokes dynamics, pressure, diffusion, cross-cubic payment, periodic incidence, or \(K=Q+F\) for one common velocity field. It is not an NSE counterexample.`,
  String.raw`Here \(A_R\) covers the case in which the formal optimizer exceeds the allowed window length. Only the still-unproved estimate \(\mathfrak H^F_{4/3,N,R}\lesssim P\) would make the mixed term \(P^{10/11}\). This is a ceiling for this upper-bound method, not a lower bound attained by every NSE solution.`,
  String.raw`This is an abstract sequence countermodel to the two-cap inference, not a dissipation measure or NSE solution. A proof using more PDE structure could still succeed when \(\theta>2/3\).`,
  String.raw`This is an unforced smooth Navier--Stokes solution: it is divergence free, \((u^{(n)}\!\cdot\nabla)u^{(n)}=0\), and satisfies the heat equation. The mollified path velocity is parallel to \(e_1\), while the moving velocity is independent of \(y_1\), so for every periodic shell cutoff,`,
  "This is generated from exact formulas and frozen evidence as an",
  String.raw`These scalar rows are compatible with the inherited linear clock/variation ledgers and zero \(Q\)-variation, and satisfy`,
  "This is only a collision check, not a novelty or priority claim. The quantitative temporal/Morrey gains in neighboring literature all carry extra scale information, smallness, or energy-dependent constants and cannot prove S.280, S.288, or S.328.",
  String.raw`The proof uses only two payment regimes: when \(P_R^M\le1\), use the linear side of S.327 and \(P_R^M\le(P_R^M)^{2/3}\); when \(P_R^M\ge1\), use S.328 and \(1\le(P_R^M)^{2/3}\). In particular,`,
  String.raw`Only to test this method, additionally assume that some fixed \(p\in(1,\infty]\), \(N\), \(\beta>0\), and \(C_H\) satisfy uniformly over the solution, scale, and terminal`,
  String.raw`Whenever these quantities are finite, Step 12 S.291--S.293 holds pointwise for each \((u,R,\tau)\), giving`,
  "Status · R0.74S STEP 13",
  String.raw`The final equality follows from periodic integration in \(y_1\). Thus every \(f_{k,R}\) and \(\mathcal V^F_{N,R}\) for this exact family vanishes. Meanwhile, on \([0,T]\),`,
  "Energy-admissible pairs satisfy",
  "F / Formal analytic schematic",
  "The Morrey and Dini interfaces remain CONDITIONAL; the PDE gates remain OPEN. NOT CLAY.",
  "NEXT / Not started in this release",
  String.raw`Proposition 5.1 is a conditional payment-dependent Morrey envelope: suppose one universal \(C_B\) satisfies, for every solution and scale,`,
  String.raw`the root family satisfies \(\sum_{v\in{\rm roots}}c_v^3\le C_{\rm root}\);`,
  "The order in S.309 cannot be exchanged: the shell set is selected outside the time norm, so the entire window uses one deletion set. A pointwise moving minimizing shell set does not control the common-window functional here.",
  String.raw`The finite coefficient in S.310 may depend on the solution and \(R\); this step does not prove uniform control of it by \(P_R^M\).`,
  "Combining S.315 with S.275 gives",
  String.raw`The deletion set in S.342 is fixed in time; a pointwise moving exceptional set is insufficient. Second, the excess branch should attack the weaker combined envelope S.328 instead of separately requiring universal bounds on \(M_R\) and \(L_R\); provided the product remains at the quadratic payment scale, a longer path can be offset by a smaller cylinder-density coefficient. Third, pure high-frequency heat shear is not a counterexample candidate for the physical-window gate; a later exact-family search must create physical annular separation while passing the \(Q\), cubic, pressure, and drift ledgers.`,
  "Step 12 writes the short last-exit residual as absolute physical-flux variation in one common terminal window and proves a selected-excess estimate under uniform moving-tube Morrey and path-length hypotheses. Step 13 tests how far ordinary temporal integrability can move the short gate and finds the exact scalar threshold for the excess gate when the Morrey coefficient is allowed to grow with payment.",
  "Step 13 independent audit",
  "Step 13 machine-certificate JSON",
  "Step 13 rules out two invalid directions. First, higher scalar time regularity of the aggregate flux density is insufficient; the next sufficient input for the short branch must be shell selective:",
  "Step 13 certificate report",
  "Step 13 Chinese reader source",
  "Step 13 primary audit",
  "Step 13 analytic main text, certificate, and dual audit",
  "Step 13 final analytic main text",
  "Step 13: Python passes 31/31 exact, 11/11 finite, 22/22 structural, 4/4 dependency, and 32/32 negative checks; Ruby passes 9/9 groups, 72,027 cases, 6/6 artifact locks, 4/4 dependency locks, 32/32 note checks, 19 primary-audit cases, and 43 negative cases. Finite certificates do not replace the analytic proof.",
  "The universal terminal-window gate S.280, universal ancestor gate S.288, and combined target S.303 remain",
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
  assert.equal(rows.length, english.length, "R0.74S Step 13 translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74S Step 13 English translation drift");
} else {
  assert.equal(missing.length, english.length, "R0.74S Step 13 source-string count drift");
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

process.stdout.write(`${JSON.stringify({ release: "R0.74S Step 13", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
