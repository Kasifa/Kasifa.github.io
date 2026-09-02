#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074sstep16";

// Local, direct translations in deterministic collectSiteStrings order.
// Protected TeX and URL tokens are copied byte-for-byte by withProtected.
const summaries = [
  "99 sections fully sealed",
  "Current endpoint R0.74S Step 16",
  "The fixed-frame Bernoulli flux cancels exactly, while the Version-M moving cutoff leaves a drift; S.342 is FALSE for every p>1, and the critical S.444 and S.407 remain OPEN. NOT CLAY.",
  "If separately launched, analyze only OPEN S.444, OPEN S.407, or another explicit new PDE input; do not keep assuming the now-FALSE S.342 or claim that Q.1 or regularity is solved. This release contains only R0.74S Step 16.",
  "Research note R0.74S Step 16 · 2026-09-03",
  "Review v1.95 · 2026-09-03",
  "R0.70A–R0.74S · 124 sections published",
  "R0.74S follow-up research interface",
  "R0.74S Step 16 uses a smooth Taylor 1923 exact solution to refute S.342 for every p>1; the critical S.444, S.407, Q.12, Q.1, and regularity remain OPEN.",
  "R0.74S: Taylor 1923 vortex, moving drift, and the critical time endpoint",
  "R0.74S｜Taylor 1923 vortex, moving drift, and the critical time endpoint",
  "Step 16 formal analytic schematic",
  "For the smooth Taylor 1923 exact solution the fixed-frame Bernoulli flux is zero, but the Version-M moving drift makes S.342 FALSE for every p>1; the critical S.444 and S.407 remain OPEN. NOT CLAY.",
  "The smooth Taylor 1923 exact solution has fixed-frame flux cancellation but nonzero Version-M moving drift; S.342 is FALSE for every p>1, while S.444, S.407, Q.1, and regularity remain OPEN. NOT CLAY.",
  "If separately launched, analyze OPEN S.444, OPEN S.407, or another explicit new PDE input; do not keep assuming FALSE S.342.",
  "Literature review v1.95 · 2026-09-03",
  "PROVED: the exact solution, fixed-frame Bernoulli cancellation, Version-M moving drift, and amplitude scaling in S.417–S.443. FALSE: for every p>1 and finite N and C, suitable R, z0, and A refute S.342. CRITICAL OPEN: at p=1, H scales like A squared while payment scales like A cubed, so S.444 is undecided. FINITE: the primary certificate passes 7/7 groups (2,207 cases), the independent Ruby certificate passes 9/9 groups (2,839 cases), and all 11 external negative probes fail as expected; the finite certificate does not machine-prove continuum payment. OPEN: S.444, S.407, Q.12, Q.1, scale contraction, and regularity.",
  "R0.74S Step 16 public boundary",
  "S.417–S.443 use the smooth exact periodic Taylor 1923 solution to establish fixed-frame Bernoulli cancellation and Version-M moving drift, and to refute S.342 for every p>1; S.444, S.407, Q.12, and Q.1 remain open.",
  "Step 16 uses the smooth exact NSE family given by the Taylor 1923 bi-periodic decaying vortex; Taylor–Green 1937 appears only as historical background. Only results supported by the frozen evidence are stated, with no novelty or priority claim.",
  "Taylor 1923 vortex, moving drift, and the critical time endpoint",
  "Research-note master index · v1.95 · 2026-09-03",
  ", and may no longer be listed as an open candidate.",
  ", Wolf local pressure decomposition, Dascaliuc--Grujić physical-scale flux locality, the Koch--Tataru critical Carleson-type norm, and Yang skewed-cylinder maximal estimates",
  ": the direct hybrid terminal-flux gate, selected-crown estimate S.407, S.375, S.288, S.303, S.272, Step 10 S.243, Q.12, Q.1, scale contraction, regularity, singularity formation, and the Millennium problem.",
  ": the smooth exact NSE identities in S.417--S.420; the radial mollifier and terminal path in S.421--S.423; fixed-frame Bernoulli cancellation and the moving-drift identity in S.424--S.425; simultaneous positivity on any N+1 physical shells in S.426--S.432; the temporal-tail lower bounds and complete-payment upper bound in S.433--S.437; the quantifier-level refutation of S.342 in S.438; and the critical L1-in-time amplitude saturation at fixed N and R in S.439--S.443.",
  ". Continue to keep",
  ". They do not provide a theorem combining this project-specific terminal mollified trajectory, periodized physical annuli, fixed shell deletion before the time norm, and the Version-M payment.",
  ". Modern exact-flow background also includes the work of Chai--Wu--Fang on",
  ". Step 15 S.386--S.387 includes p=1; if S.444 is used as an antecedent, the same reasoning in S.389--S.391 still pays the full hybrid residual. The p>1 time-window gain from Step 13 may no longer be used.",
  "(1923). Taylor--Green 1937 is cited only for historical context; see",
  "(2020) and the work of Antuono on",
  "(2020). These classical fields, the generalized-Beltrami mechanism, and exponential decay are not novelty claims.",
  "The proposed universal critical endpoint estimate is",
  "The exact quantifier-level refutation for every supercritical p is",
  "106. Step 16: a smooth exact solution refutes every p>1 quadratic temporal-tail estimate",
  "107 / Complete text",
  "107. The Taylor 1923 bi-periodic decaying vortex is a smooth exact solution in the three-dimensional periodic class",
  "108 / Complete text",
  "108. Fixed-frame Bernoulli flux cancels exactly; Version-M leaves only moving drift",
  "109 / Complete text",
  "109. One radial Fourier multiplier activates any N+1 physical annuli simultaneously",
  "110 / Complete text",
  "110. The common-deletion temporal tail fails quantifier by quantifier for p>1",
  "111 / Complete text",
  "111. More general payment powers and time anti-concentration exponents are also constrained",
  "112 / Complete text",
  "112. The critical p=1 case only saturates amplitude scaling, and the new S.444 remains OPEN",
  "113 / Complete text",
  "113. The exact ABC family provides an independent algebraic screen, not a second required theorem",
  "114 / Complete text",
  "114. Primary sources support only the classical background, not this project-specific refutation",
  "115 / Complete text",
  "115. Claim ledger, finite certificates, and the only allowed next route",
  "116 / Complete text",
  "Integrating S.432 over a terminal block of length delta over A and again applying the pigeonhole principle to N+1 shells gives the reverse amplitude lower bound",
  "The newly stated S.444 remains",
  "This release contains only R0.74S Step 16 and stops here. Any separately launched follow-up may analyze only OPEN S.444, OPEN S.407, or another explicit new PDE input; the now-FALSE S.342 must not be assumed, and Q.1, regularity, or the Millennium problem must not be presented as theorems.",
  "As R decreases to zero, mu_R tends to one. Taking R sufficiently small gives one half at most mu_R at most one. With x_*=(pi/4,0,0) as the endpoint, the Version-M trajectory and moving field satisfy",
  "equal-parameter ABC field",
  "The frozen even radial mollifier gives the same real multiplier on every square-root-of-two frequency mode of W",
  "The frozen audit performed only a bounded collision search. Failure to find a theorem or counterexample with the same quantifiers is not exhaustiveness and does not establish novelty or priority. The proof of S.438 uses the displayed direct substitution and payment comparison, not the absence of a literature match.",
  "For p=infinity,",
  "For the shell cutoff, write",
  "For every A>0 this is a smooth, exact, periodic, mean-zero, unforced three-dimensional incompressible NSE solution. It is independent of x3 and is therefore a two-dimensional smooth screen embedded in the three-dimensional solution class. Amplitude is freely variable because this particular W is both a steady Euler field and a Laplace eigenfield; this is not a general NSE amplitude symmetry.",
  "For every k, S.428 still holds and the absolute value of c_k,R is at most m_k,R. Along the characteristic use",
  "Nearby analytic background also includes Caffarelli--Kohn--Nirenberg suitable-weak partial regularity",
  "More generally, on the same dimensionless terminal block, suppose",
  "Fix t0>0 and set",
  "Combining S.435--S.436 gives",
  "The conclusion is strict: for every p>1, every finite deletion budget N, and every proposed constant C, one can choose admissible R and z0 and a sufficiently large amplitude A so that S.342 fails. Therefore S.342 must be labeled",
  "Exact-solution analytic schematic · not simulation / DNS · NO DGX",
  "Radial symmetry and product-to-sum identities give",
  "The historical source is G. I. Taylor,",
  "Let q_+=(2,2,0) and define",
  "The route correction is explicit: S.342 may no longer be used as a proof antecedent because it is false even for smooth periodic exact solutions. The short-flux route can next analyze only the critical L1-in-time tail S.444, retaining signed moving-drift cancellation and the common deletion set. The terminal-crown route may still proceed through the separate open coercivity estimate S.407.",
  "satisfies curl U=U and Laplacian U=-U. Hence the stated exponentially decaying velocity and mean-zero pressure form another smooth periodic exact solution. At xi_*=0,",
  "where c_p,N,R>0 is independent of A. On the other hand, every nonnegative row of the complete payment must enter the comparison. At fixed R, translation does not change pointwise amplitude; local energy, exterior velocity and pressure, fixed gauge, and the algebraic harmonic row are each at most O_R(A squared) or O_R(A cubed). Therefore",
  "where g0 is positive.",
  "Taking local-energy good times approaching t0, the endpoint term of the buffered local energy also gives",
  "After deleting at most N=M-1 indices, at least one of the first M positive coordinates remains. Thus",
  "The order cannot be exchanged: the opponent first fixes p, N, and C; then take M=N+1, choose an admissible R, and finally send A to infinity. R may depend on N because S.342 requires one finite N to work uniformly over all admissible scales.",
  "The velocity modes have frequency length one, while nonconstant modes of the squared speed have frequency length square root two. The radial multiplier, small-R shell positivity, and O(A inverse) trajectory residence again produce the A^(3-1/p) obstruction.",
  "Therefore, at fixed N and R,",
  "In particular, in the bare class, quadratic payment power beta=2/3 permits no positive time anti-concentration exponent alpha.",
  "The same family gives a sharper exponent boundary. If for some fixed p between one and infinity there is",
  "Uniqueness gives xi2=xi3=0, and",
  "First fix any finite deletion budget N>=0 and put M=N+1. Then choose R so that",
  "Choose a fixed small delta>0. For sufficiently large A the terminal physical-time block lies in I_R, and the trajectory stays between pi/8 and pi/4. Hence the first N+1 shells simultaneously satisfy",
  "Retain the dimensionless density from Step 13",
  "Thus the exact quantifier-level negation of S.342 is",
  "The critical endpoint S.444, together with S.407, Q.12, Q.1, regularity, and the Millennium problem, remains OPEN. NOT CLAY. The range in which S.342 is FALSE is exactly",
  "The shell-mass bound and summability of the weighted coefficients give",
  "On the three-dimensional torus define",
  "In the frozen Version-M setting, this step",
  "then the scaling of interval length and integrated density forces",
  "then necessarily",
  "This refutation concerns only the supercritical temporal-tail statement S.342. It does not refute the direct hybrid terminal-flux gate or the critical p=1 candidate S.444, and it neither proves nor refutes S.407, S.375, Q.12, Q.1, scale contraction, regularity, singularity formation, or the Navier--Stokes Millennium problem. No singular solution appears here.",
  "Here 1/infinity=0. Thus payment power 2/3 is amplitude-compatible only at p=1; every p>1 requires a strictly larger payment power unless an extra factor is added.",
  "Here the all-copy sum in the exterior G row converges by super-Gaussian shell weights, while the harmonic H row uses the frozen order-minus-four algebraic kernel. These two convergence mechanisms must not be conflated.",
  "This is the key distinction of the step. Zero fixed-frame Bernoulli flux does not mean the frozen moving observable has no flux: a cutoff moving with nonconstant local velocity creates an explicit drift, and that term cannot be removed from the Version-M flux.",
  "This is generated from exact-solution formulas and frozen evidence as an",
  "These are N+1 distinct physical annuli in moving spatial coordinates, not Fourier-shell indices. Along xi2=0,",
  "Thus the entire support of each of the first M physical shell cutoffs has the required phase bound, and hence",
  "This is only an independent exact-family screen of the mechanism. The Taylor family proof does not depend on it, and it need not be promoted to a second theorem. For ABC historical context see Dombre et al.,",
  "This is only saturation of the amplitude exponent. It supplies neither universal N1 and C nor a proof of the new candidate below:",
  "Direct differentiation gives",
  "The primary certificate passes 7/7 finite groups, 2,207 cases, 7/7 structural groups, and 3/3 dependency locks. The independent Ruby verifier passes 9/9 groups and 2,839 independent cases and locks the main text, both audits, both implementations, the primary certificate JSON, and the certificate report. Eleven external negative probes all fail as expected. The finite programs check exact Fourier identities, pigeonhole arguments, representative support and path inequalities, amplitude exponents, hashes, structure, and claim labels; they do not machine-prove arbitrary-mollifier continuity, the continuous payment estimate, S.444, S.407, regularity, or the Clay problem.",
  "Status · R0.74S STEP 16",
  "Changing variables cancels mu_R exactly and removes one amplitude factor. Hence",
  "The Bernoulli function satisfies divergence of B_W W equal to zero. Therefore the kinetic and physical-pressure shell fluxes in fixed coordinates cancel exactly after periodic integration by parts; the time-dependent pressure gauge also integrates to zero by incompressibility. The full Version-M formula leaves only moving-cutoff drift:",
  "R0.74S / follow-up research interface",
  "The exact field in S.417 is the Taylor 1923 bi-periodic decaying vortex. Modern numerical literature sometimes calls it the two-dimensional Taylor--Green vortex, but it is not conflated here with the fully three-dimensional Taylor--Green 1937 datum.",
  "The dimensionless time length in S.432 is delta/(A R squared). Therefore, for 1<p<infinity,",
  "S.444 remains",
  "Step 15 shows that if a common-deletion temporal flux tail holds, the same deletion set pays both branches of the combined terminal residual. Step 16 tests the p>1 time integrability additionally required by the Step 13 candidate S.342. The test object is neither a numerical approximation nor a singular solution, but the translation and amplitude family of the Taylor 1923 bi-periodic decaying vortex.",
  "Step 16 Chinese reader source",
  "Step 16 main text, certificate, and dual audit",
  "Step 16: the primary certificate passes 7/7 groups (2,207 cases), the independent Ruby certificate passes 9/9 groups (2,839 cases), and all 11 external negative probes fail as expected. Finite certificates verify algebra, counts, and boundary labels; they do not replace an analytic proof of continuum payment.",
  "The Taylor 1923 bi-periodic decaying vortex gives a smooth, exact, periodic, unforced three-dimensional NSE solution family: the fixed-frame Bernoulli flux cancels exactly, while the Version-M moving cutoff leaves a nonzero drift.",
  "The Taylor 1923 bi-periodic decaying vortex exposes Version-M moving-cutoff drift; S.342 is false for every p>1, while the critical S.444 remains open",
  "Taylor 1923 exact vortex: fixed-frame cancellation, moving drift, and amplitude split",
  "The Taylor planar field satisfies",
  "Taylor moving-frame main text",
];

function withProtected(summary, source) {
  const tokens = extractProtectedTokens(source);
  return tokens.length === 0 ? summary : summary + " " + tokens.join(" ");
}

process.chdir(root);
const [source, order, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings("./public"),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp("^" + prefix + "\\d+$");
const baseCurrent = checkOnly ? current : current.filter((row) => !rowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missing = source.filter((entry) => !currentByZh.has(entry.zh));
const missingOrder = order.filter((entry) => !currentByZh.has(entry.zh));
const existingRows = current.filter((row) => rowPattern.test(row.id));

if (checkOnly) {
  assert.equal(missing.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => rowPattern.test(row.id));
  assert.equal(rows.length, summaries.length, "R0.74S Step 16 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74S Step 16 English translation drift",
  );
} else if (existingRows.length === summaries.length) {
  const refreshedRows = existingRows.map((row, index) => {
    const en = withProtected(summaries[index], row.zh);
    assert.ok(!containsChinese(en), "Chinese remains in translation " + (index + 1));
    assert.deepEqual(
      extractProtectedTokens(en),
      extractProtectedTokens(row.zh),
      "protected token drift " + (index + 1) + ": " + row.zh,
    );
    return { ...row, en };
  });
  await writeFile(translationPath, JSON.stringify([...baseCurrent, ...refreshedRows], null, 2) + "\n");
} else {
  assert.equal(missing.length, summaries.length, "R0.74S Step 16 source-string count drift");
  const sourceByZh = new Map(missing.map((entry) => [entry.zh, entry]));
  const additions = missingOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, "absolute source entry missing " + orderedEntry.zh);
    const en = withProtected(summaries[index], entry.zh);
    assert.ok(!containsChinese(en), "Chinese remains in translation " + (index + 1));
    assert.deepEqual(
      extractProtectedTokens(en),
      extractProtectedTokens(entry.zh),
      "protected token drift " + (index + 1) + ": " + entry.zh,
    );
    return { id: prefix + String(index + 1).padStart(3, "0"), ...entry, en };
  });
  await writeFile(translationPath, JSON.stringify([...baseCurrent, ...additions], null, 2) + "\n");
}

process.stdout.write(JSON.stringify({
  release: "R0.74S Step 16",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2) + "\n");
