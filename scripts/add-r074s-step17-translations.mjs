#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074sstep17";

// Local direct translations in deterministic collectSiteStrings order.
// withProtected appends every TeX, code, release, and URL token byte-for-byte.
const summaries = [
  "01 / Retained historical trunk", // 1
  "02 / Transition from P to R", // 2
  "03 / Decisive correction", // 3
  "04 / What remains valid", // 4
  "05 / Evidence levels", // 5
  "From the scalar no-go to a signed endpoint functional", // 6
  "From augmented-observable triage to terminal-clock extraction", // 7
  "Fixed positive-order windows miss the signal; the defect-completed shell clock is stable under fixed-scale suitable-weak limits, while the matching square-function bound remains open.", // 8
  "Keep analytic results, finite recomputation, figures, and the literature boundary separate", // 9
  "Earlier nodes progressed from projected-Lamb heat volume, local heat packing, exact shear, and spectral branches to suitable-weak moving tubes, complete payment, all-shell synthesis, and the free-passive-amplitude scalar-payment-only no-go. R0.74O proves only that frozen scalar payment is insufficient; it does not select the temporal functional that closes the route or change the open regularity and Clay status.", // 10
  "Seventeen steps audited positive clocks, terminal windows, common deletion, crowns, and temporal tails, until the exact Taylor family exposed the fundamental obstruction to absolute variation.", // 11
  "Previous milestone recap", // 12
  "The four-panel figure is an exact-field deterministic rendering, not DNS or a numerical NSE simulation.", // 13
  "On the same recurrent family, signed range and positive excursion remain quadratic. The Jordan identity separates total variation into the terminal endpoint and twice the backtracking debt; absolute value repeatedly charges every orbit, while a Step 15 terminal hybrid coordinate needs only a signed increment between two times.", // 14
  "Convex payment forces first-shell concentration; the dissipation, kinetic-window, and recent-positive-variation trichotomy holds for every completed clock, while persistence packing remains open.", // 15
  "The next sufficient input is the fixed-deletion positive excursion in open S.472, or equivalently up to already-paid Q-variation a simultaneous maximal-height clock estimate. The weaker direct hybrid last-exit gate also remains open. This no-go does not close terminal-crown coercivity, Q.12, Q.1, scale contraction, or regularity. The next interface has not been launched.", // 16
  "A bounded primary-source audit does not prove novelty, priority, or exhaustiveness.", // 17
  "Read R0.74S Step 17", // 18
  "This is the third cumulative recap after R0.60. It covers 161 nodes and 221 public notes, preserves the R0.61–R0.74O recap byte-for-byte, and adds the four nodes R0.74P–R0.74S. Within R0.74S the recap is updated only once for this major route correction.", // 19
  "closed-orbit recurrence, cubic absolute tail, cubic complete payment, quadratic signed excursion, and the BV and completed-clock comparisons.", // 20
  "The Python certificate has 4,325 cases and the independent Ruby audit has 294 exact assertions plus mutation, path, and reproducibility checks; these do not replace the continuum proof.", // 21
  "A 161-node cumulative recap from R0.61 through R0.74S: the split between the Step 16 quadratic separatrix and Step 17 cubic recurrence, and the new fixed-deletion simultaneous-height interface", // 22
  "The R0.61–R0.74O proofs, counterexamples, and open boundaries retain their original quantifiers", // 23
  "All nodes from R0.61 through R0.74S", // 24
  "R0.61–R0.74S major route-correction recap｜From the scalar no-go to a signed endpoint functional", // 25
  "R0.74P｜Temporal-observable triage", // 26
  "R0.74Q｜Effective shells and cubic payment", // 27
  "R0.74R｜Arbitrary-clock extraction gate", // 28
  "R0.74S｜From clocks to signed flux", // 29
  "S.342, S.444, and every power-only absolute temporal tail with exponent below one.", // 30
  "S.472, the direct hybrid gate, S.407, Q.12, Q.1, and regularity remain open; no singularity or Millennium conclusion is claimed.", // 31
  "signed excursion remains quadratic; the target moves to fixed-deletion hybrid or simultaneous height", // 32
  "Step 16's quadratic law is correct; the error was extrapolating a special separatrix to a universal endpoint", // 33
  "Step 16 chooses a terminal centre on a nonrecurrent invariant line. The trajectory crosses the key phase only once, so the critical absolute variation is quadratic while payment is cubic in that terminal setting. This proves exponent compatibility only, not the universally quantified status of S.444.", // 34
  "Step 17 moves to a regular closed streamline of the same smooth Taylor exact solution. A fixed physical window contains linearly many returns; absolute variation accumulates cubically and complete payment remains cubic. Hence every power-only absolute tail with p at least one and beta below one fails, including S.444.", // 35
  "The terminal best-N reduction holds; a common-shear multipacket can activate all target shells simultaneously, but the outermost genuine velocity-cubic payment blocks the construction.", // 36
  "Closed-orbit recurrence makes absolute variation and payment cubic, so S.444 and every power-only tail with beta below one are false; signed excursion remains quadratic. S.472, the direct hybrid gate, S.407, Q.1, and regularity remain open. NOT CLAY.", // 37
  "Current endpoint R0.74S Step 17", // 38
  "Journal-grade four-panel figure", // 39
  "If separately launched, study open S.472, fixed-deletion simultaneous height, direct hybrid last-exit increments, open S.407, or another explicit PDE input; do not restore the false S.342 or S.444. This release contains only R0.74S Step 17.", // 40
  "Closed-orbit recurrence in the same smooth Taylor exact solution makes absolute variation and complete payment cubic. Thus S.444 and all power-only tails with beta below one are false, while signed excursion remains quadratic; S.472, the direct hybrid gate, and S.407 remain open. NOT CLAY.", // 41
  "Closed-streamline recurrence raises absolute variation from the quadratic Step 16 special path to cubic size, while signed excursion remains quadratic; S.444 is therefore false. S.472, the direct hybrid gate, and S.407 remain open. NOT CLAY.", // 42
  "Research note R0.74S Step 17 · 2026-09-03", // 43
  "Read the complete R0.61–R0.74S cumulative recap →", // 44
  "Major route-correction recap R0.61–R0.74S · 2026-09-03", // 45
  "Review v1.96 · 2026-09-03", // 46
  "Latest major route-correction recap (R0.61–R0.74S, 161 sections)", // 47
  "The cumulative recap after R0.60 contains 161 nodes; the site has 221 public research notes", // 48
  "R0.74S Step 17 refutes every power-only absolute temporal tail with beta below one, including S.444. The target moves to fixed-deletion positive excursion or simultaneous height, or to direct hybrid increments. S.407, Q.12, Q.1, and regularity remain open.", // 49
  "R0.74S: Closed-streamline recurrence and the absolute temporal-tail no-go", // 50
  "R0.74S｜Closed-streamline recurrence refutes every sublinear absolute temporal tail", // 51
  "S.342 and S.444 are both false. The next target is fixed-deletion positive excursion or simultaneous height, or direct hybrid increments. S.407, Q.12, Q.1, regularity, and Clay remain open.", // 52
  "The special Step 16 separatrix sees only quadratic size; Step 17 uses recurrence on a closed orbit of the same Taylor exact solution to raise absolute temporal variation to cubic size while signed excursion remains quadratic.", // 53
  "Step 17 journal-grade four-panel figure", // 54
  "Closed-streamline recurrence and the absolute temporal-tail no-go", // 55
  "Literature review v1.96 · 2026-09-03", // 56
  "Study open S.472, fixed-deletion simultaneous height, direct hybrid increments, or open S.407; do not restore false S.342 or S.444.", // 57
  "Read the route-correction recap", // 58
  "PROVED: the closed-orbit recurrence, cubic absolute tail and complete payment, quadratic signed excursion, and completed-clock comparison in S.445–S.475. FALSE: every power-only absolute temporal tail with p at least one and beta below one, including S.444. FINITE: the Python certificate passes 12/12 groups and 4,325 cases; independent Ruby passes 7/7 exact groups and 294 assertions, together with every mutation, path, and reproducibility check. OPEN: S.472, the direct hybrid gate, S.407, Q.12, Q.1, scale contraction, and regularity. The figure is an analytic exact-field visualization, not DNS or a numerical NSE simulation.", // 59
  "R0.74S Step 17 literature and claim boundary", // 60
  "R0.74S Step 17 public boundary", // 61
  "The special Step 16 separatrix gives quadratic size; on a regular closed streamline of the same smooth Taylor exact solution, Step 17 proves cubic absolute variation and complete payment but quadratic signed excursion. Thus S.342, S.444, and every power-only tail with beta below one are false.", // 62
  "Step 17 still uses Taylor's bi-periodic decaying vortex. Closed-streamline recurrence, the Version-M path, physical-shell deletion, and payment comparison follow by direct substitution rather than historical attribution. The cited skewed-cylinder, signed averaged-flux, local-pressure, and signed local-balance results do not control absolute recurrent backtracking debt. The bounded audit makes no novelty, priority, or exhaustiveness claim.", // 63
  "Closed-streamline recurrence refutes every sublinear absolute temporal tail", // 64
  "Research-note master index · v1.96 · 2026-09-03", // 65
  "; the signed quadratic range, BV/backtracking identity, positive-excursion implication, and completed-clock comparison.", // 66
  ": the direct hybrid gate, terminal-crown coercivity S.407, Q.12, Q.1, scale contraction, and regularity.", // 67
  ": the regular closed streamline and recurrence lemma; simultaneous activation of arbitrary N+1 physical shells; the exact recurrent Version-M path and flux identity; the cubic absolute temporal tail for every p at least one; complete cubic payment; and failure of every power-only absolute tail with beta below one, especially", // 68
  ": the S.472 fixed-deletion positive-excursion or simultaneous-height estimate. Continue to keep", // 69
  ". It is stronger in quantifiers than the direct Step 15 gate; the weaker direct hybrid terminal-flux gate also remains open, and a future proof need not establish S.472 first.", // 70
  "← Previous section: R0.74R terminal windows and the arbitrary-clock extraction gate", // 71
  "116. Route correction: closed-streamline recurrence raises absolute temporal variation from quadratic to cubic size", // 72
  "117 / Full text", // 73
  "117. A regular closed streamline in the same Taylor exact family", // 74
  "118 / Full text", // 75
  "118. Any N+1 physical annuli activate simultaneously and the Version-M centre returns linearly many times", // 76
  "119 / Full text", // 77
  "119. The absolute temporal tail is cubic for every p at least one", // 78
  "120 / Full text", // 79
  "120. Complete Version-M payment remains cubic, so every beta below one fails", // 80
  "121 / Full text", // 81
  "121. Signed forward excursion remains only quadratic", // 82
  "122 / Full text", // 83
  "122. BV/Jordan decomposition identifies recurrent backtracking debt exactly", // 84
  "123 / Full text", // 85
  "123. The correct successor target is fixed-deletion positive excursion or simultaneous height", // 86
  "124 / Full text", // 87
  "124. Triple audit, two-language certificates, and a journal-grade four-panel figure", // 88
  "125 / Full text", // 89
  "125. Claim ledger and the strict next interface", // 90
  "126 / Full text", // 91
  "Combine this with S.459. Use the payment upper bound for nonnegative beta and the lower bound for negative beta, obtaining", // 92
  "For the completed nonnegative clocks, with already-paid Q-variation, S.473–S.475 show that S.444 is a positive-variation packing statement, whereas the correct successor needs only maximal simultaneous height or positive-excursion packing.", // 93
  "This release contains only R0.74S Step 17 and stops here. A separately launched follow-up may study open S.472, fixed-deletion simultaneous height, direct hybrid last-exit increments, open S.407, or another explicit PDE input. It must not assume the false S.342 or S.444 or present Q.12, Q.1, regularity, or the Millennium problem as a theorem.", // 94
  "This step", // 95
  "Closed-streamline recurrence: signed excursion versus absolute temporal variation", // 96
  "Define the forward ordered excursion and common-deletion tail", // 97
  "After integration by parts, the endpoint and cutoff/damping terms have only quadratic amplitude scale, hence", // 98
  "The fixed-frame kinetic and physical-pressure Bernoulli fluxes still cancel exactly, and the pressure gauge cancels shellwise; the complete Version-M expression leaves only moving-cutoff drift:", // 99
  "Let g be squared speed along the orbit and q its derivative. Two points on the same orbit have squared speeds one-half and three-quarters, so q is nonzero; for every p at least one, each sufficiently long phase interval contains linearly many complete periods:", // 100
  "Analytic visualization · not simulation or DNS · NO DGX", // 101
  "The quantifiers cannot be exchanged: the opponent first fixes p, N, beta, and C; then choose M=N+1, an admissible R and z0, and finally a sufficiently large amplitude. The p=1, beta=2/3 case refutes S.444 exactly. A power-only absolute temporal tail needs payment exponent at least one.", // 102
  "With the displayed pressure, decay factor, velocity, and pressure amplitude, direct divergence, Laplacian, and Euler identities make this a smooth, periodic, mean-zero, unforced exact three-dimensional NSE solution for every positive amplitude.", // 103
  "Let the positive and negative variations and their minimum be as displayed. The common zero start and Jordan decomposition give", // 104
  "The route decision cannot be reversed: no later proof may use S.342, S.444, or a power-only absolute tail with beta below one. The next temporal task is signed positive excursion, fixed-deletion simultaneous height, or the Step 15 hybrid last-exit increments directly; the terminal-crown route remains independently available.", // 105
  "Every Step 15 hybrid coordinate is an increment of the same shell flux between two times, hence", // 106
  "Take the one-half level branch of the stream function in the positive cell. Its two explicit graphs form a compact regular oval; the velocity has no zero and is tangent to it. The orbit from the chosen base point therefore has a finite period:", // 107
  "Previous section and next interface", // 108
  "All four panels come from the exact Taylor family, the closed-orbit ODE, and frozen formulas by deterministic rendering. This is not DNS, a numerical Navier--Stokes simulation, or regularity or Clay evidence.", // 109
  "The same smooth Taylor 1923 exact solution produces linearly many returns on a regular closed streamline: absolute temporal variation accumulates cubically, while signed positive excursion remains quadratic.", // 110
  "Closed-streamline recurrence in the same Taylor smooth exact solution makes absolute temporal variation cubic and refutes every power-only tail with beta below one, including S.444; signed excursion remains quadratic", // 111
  "The same formula also shows what absolute value destroys. Because the time derivative of g along the phase has the displayed form,", // 112
  "The lower bound is a continuum analytic statement; the finite certificate checks only exact identities, counts, deletion quantifiers, and exponent bookkeeping.", // 113
  "Next interface: R0.74T not started →", // 114
  "First fix any finite deletion budget N, set M=N+1, and only then choose a sufficiently small admissible R. The Step 16 Fourier-multiplier and support/cosine argument makes the first M physical-shell coefficients positive.", // 115
  "Translation along a compact orbit does not change the amplitudes of fixed smooth profiles. Local energy, exterior velocity and pressure, quadratic-cutoff, and harmonic rows are at most quadratic or cubic; the super-Gaussian all-copy sum and order-minus-four harmonic sum remain summable. Good times approaching the endpoint give a positive quadratic buffered-energy trace whose three-halves power gives the payment lower bound. Hence", // 116
  "Choose two ordered times on one correctly oriented period where squared speed rises from one-half to three-quarters. Each of the first N+1 coordinates then has a positive quadratic excursion. Thus signed range and positive excursion are quadratic, while absolute variation is cubic.", // 117
  "Research note R0.74S · Step 17 complete Chinese version", // 118
  "Thus S.472, the universal fixed-deletion positive-excursion estimate aligned with the signed endpoint problem, remains", // 119
  "As amplitude grows, the centre completes linearly many closed-orbit returns in a fixed physical-time window. This differs from the single separatrix passage in Step 16.", // 120
  "Therefore every power-only absolute tail with p at least one and beta below one is false, including S.444; S.472, the direct hybrid gate, S.407, Q.12, Q.1, and regularity remain open. NOT CLAY.", // 121
  "On the terminal interval the cutoff equals one. Changing variables to phase and using periodic averaging gives a cubic norm for every finite p, while one complete period gives the same scale at infinity. Deleting at most N=M-1 shells leaves one of the first M positive coordinates. Therefore for every p from one to infinity,", // 122
  "On the terminal interval, the phase length is", // 123
  "At p=1 the dimensionless normalization cancels exactly:", // 124
  "On the recurrent orbit, terminal endpoints and signed range are quadratic, but the backtracking debt is cubic on every active shell. S.444 charges every up-and-down traversal, while the signed terminal problem does not need this repeated debt.", // 125
  "On the present exact family,", // 126
  "This is not DNS or a numerical Navier--Stokes simulation. The displayed orbit and curves are deterministic analytic visualizations of exact formulas. The example is globally smooth; S.472, the direct hybrid gate, S.407, Q.12, Q.1, scale contraction, and regularity remain open.", // 127
  "The formal four-panel figure shows the regular closed streamline, one orbit period of squared speed, separation of signed cancellation from absolute debt over four returns, and the slope-two versus slope-three amplitude classes. The figure, caption, source data, plot and validation scripts, manifest, and QA are public. It is an analytic exact-field visualization, not DNS or a numerical NSE simulation.", // 128
  "Major route-correction recap (R0.61–R0.74S, 161 sections)", // 129
  "Status · R0.74S STEP 17", // 130
  "The final conclusion is that for every p from one to infinity, every finite deletion budget, and every beta below one, the power-only absolute temporal tail fails. The p=1, beta=2/3 case is exactly the quantifier combination that refutes S.444, so", // 131
  "F / Journal-grade four-panel figure", // 132
  "NAV / Adjacent research nodes", // 133
  "The primary analytic audit checks the closed-orbit topology, periodic averaging, dimensionless time normalization, complete payment, fixed deletion, signed integration by parts, and completed-clock inequalities in S.445–S.475. The independent adversarial audit retains and closes five repairs. The literature audit checks the sources and non-implication boundaries for Taylor, Yang, Dascaliuc--Grujić, Wolf, and Duchon--Robert. The bounded search makes no novelty or priority claim.", // 134
  "Python reproduction script", // 135
  "Python certificate JSON", // 136
  "The primary Python certificate passes 12/12 finite groups, 4,325 cases, 11/11 structural checks, and 2/2 dependency locks. The independent Ruby implementation does not invoke Python: 7/7 exact groups with 294 assertions, 4/4 artifact locks, 20/20 semantic checks, 32/32 negative mutations, 3/3 artifact-path substitutions, and 14/14 reproducibility assertions all pass.", // 137
  "R0.74T / signed endpoint functional interface", // 138
  "Recurrent-streamline main text", // 139
  "Independent Ruby report", // 140
  "Independent Ruby script", // 141
  "S.444 is FALSE", // 142
  "Step 16 uses a terminal centre on a nonrecurrent separatrix of the same Taylor 1923 smooth exact solution. The trajectory crosses the key phase once, so absolute flux variation is quadratic. That calculation is correct for this special terminal setting but cannot decide a statement quantified over all terminal settings.", // 143
  "Step 17 moves the endpoint to a regular closed streamline of the same solution. In a fixed physical-time window, the Version-M centre completes linearly many returns; instantaneous flux density is cubic. Signed increments cancel between circuits, while absolute temporal variation counts every circuit.", // 144
  "Step 17 Chinese reader source", // 145
  "Step 17 main text, three audits, and two-language certificates", // 146
  "Step 17: Python passes 12/12 finite groups and 4,325 cases, 11/11 structural checks, and 2/2 dependency locks; independent Ruby passes 7/7 exact groups with 294 assertions, 4/4 artifact locks, 20/20 semantic checks, 32/32 statement and environment mutations, 3/3 path substitutions, and 14/14 reproducibility assertions. Finite certificates do not replace the continuum proof.", // 147
  "The terminally anchored Version-M path is exactly", // 148
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
  assert.equal(rows.length, summaries.length, "R0.74S Step 17 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74S Step 17 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.74S Step 17 source-string count drift");
  const sourceByZh = new Map(missing.map((entry) => [entry.zh, entry]));
  const additions = missingOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, "absolute source entry missing " + orderedEntry.zh);
    const en = withProtected(summaries[index], entry.zh);
    assert.ok(!containsChinese(en), "Chinese remains in translation " + (index + 1));
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), "protected token drift " + (index + 1));
    return { id: prefix + String(index + 1).padStart(3, "0"), ...entry, en };
  });
  await writeFile(translationPath, JSON.stringify([...baseCurrent, ...additions], null, 2) + "\n");
}

process.stdout.write(JSON.stringify({
  release: "R0.74S Step 17",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2) + "\n");
