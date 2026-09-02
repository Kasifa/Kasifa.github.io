#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { collectSiteStrings, containsChinese, extractProtectedTokens } from './i18n-lib.mjs';

const root = resolve(import.meta.dirname, '..');
const translationPath = resolve(root, 'translations/en.json');
const publicRoot = resolve(root, 'public');
const checkOnly = process.argv.includes('--check-only');
const prefix = 'r074sstep14';

// Local direct translations in deterministic collectSiteStrings order. Inline
// TeX tokens are appended unchanged by the builder, keeping formulas identical
// while the surrounding reader prose is translated here.
const summaries = [
  'Current endpoint R0.74S Step 14',
  'If launched separately, continue only with the PDE-level jump--corona payment in S.375 or another explicitly new structure; this release stops at R0.74S Step 14.',
  'The same-weight outer collar and no-gain critical threshold are proved; the first-jump skeleton is separated from the unpaid corona. S.358 and S.376 remain CONDITIONAL, while S.342 and S.375 remain OPEN. NOT CLAY.',
  'The same-weight outer collar, critical density cancellation, and first-jump skeleton are fixed; the aligned spike and critical corona are abstract method obstructions, and S.375 remains OPEN. NOT CLAY.',
  'The outer collar lies exactly in the same-weight payment annulus, and the critical density threshold gives no gain; the jump skeleton contracts, but the full corona still depends on OPEN S.375. The abstract obstructions are not NSE counterexamples. NOT CLAY.',
  'Research note R0.74S Step 14 · 2026-09-03',
  'Review v1.93 · 2026-09-03',
  'R0.74S Step 14 fixes the same-weight outer-collar alignment and critical density cancellation; S.358 and S.376 remain conditional, while S.342, S.375, and the upstream PDE gates remain OPEN.',
  'R0.74S: Outer-collar alignment and the jump--corona obstruction',
  'R0.74S｜Outer-collar alignment and the jump--corona obstruction',
  'R0.74T follow-up research',
  'Step 14 formal analytic schematic',
  'If launched separately, test the PDE-level jump--corona payment in S.375 or another explicitly new structure.',
  'Outer-collar alignment and the jump--corona obstruction',
  'Literature review v1.93 · 2026-09-03',
  'PROVED: the shell-scale flux, collar geometry, incidence algebra, threshold cancellation, jump skeleton, and heat-shear identities in S.343–S.352, S.356–S.357, S.359–S.368, and S.371–S.374. CONDITIONAL: S.358 depends on the budgets in S.356–S.357; S.376 depends on OPEN S.375. ABSTRACT METHOD OBSTRUCTION: S.353–S.355 and S.370 are not NSE counterexamples. FINITE: Python passes 12/12 exact, 9/9 finite groups (74,287 cases), 37/37 structural, 3/3 dependency, and 49/49 negative checks; Ruby passes 7/7 groups, 82,788 cases, 68/68 note checks, and 99 negative cases. OPEN: S.342, S.375, S.288, S.303, S.272, Q.12, Q.1, and regularity.',
  'R0.74S Step 14 public boundary',
  'S.343–S.374 fix the shell-scale flux, same-weight outer-collar alignment, critical density cancellation, first-jump skeleton, and heat-shear screen; S.358 and S.376 remain conditional, while S.342 and S.375 remain open.',
  'Step 14 proves the same-weight outer-collar alignment, critical density cancellation, and first-jump contraction under its stated hypotheses; the aligned spike and critical corona are only abstract method obstructions, with no novelty or priority claim.',
  'Research-note master index · v1.93 · 2026-09-03',
  ', and does not refute the PDE target S.342; it proves only that S.342 cannot follow from S.348, outer-shell deletion, and the super-Gaussian coefficients alone.',
  ', not a Navier--Stokes counterexample.',
  '; only the algebraic arrow from it to the ancestor gate has been proved.',
  '; it does not assert that the signed outer flux is actually large. After deleting any fixed number of inner shells, infinitely many aligned outer faces still remain.',
  '; it does not realize the whole tree as clocks of one Navier--Stokes solution.',
  ': the common-deletion temporal estimate S.342, including uniform outer-collar anti-concentration; the PDE shell-selective jump--corona lemma S.375, especially the top-boundary, low-transition-corona, and moving-drift charges; the ancestor gate S.288, combined gate S.303, Step 11 S.272, Q.12, and Q.1; and scale contraction, regularity, singularity formation, and the Millennium problem.',
  ': density pigeonholing combined with critical cubic duality returns only total measure mass. If the available estimate of the total mass depends only linearly on payment, optimizing the density level remains linear.',
  ': the shell-scale pressure decomposition and four-channel signed flux identity in S.343--S.347; the inherited componentwise payment and fixed-solution tail boundary in S.348--S.349; the collar inclusions, inner-face gain, and outer-face alignment in S.350--S.352; the incidence Holder theorem and exact cubic duality in S.356--S.359, with the conclusion conditional on the displayed budgets; the scale-invariant measure, 32-child scaling, first-root bounds, critical factorization, and threshold cancellation in S.360--S.365; the first-jump sparsity and strict Dini coefficient in S.366--S.368; the failure of a nonuniform strict factor in S.369; bounded fine-scale shell incidence in S.371; and the heat-shear mass split and zero-flux identities in S.372--S.374.',
  '. This step does not prove scale contraction, regularity, singularity formation, or the Navier--Stokes Millennium problem. No DNS or DGX was used.',
  '. It requires universal constants, a universal deletion count, and one common shell set, so that every solution, scale, and good terminal admits nonnegative top, corona, jump, and payment rows satisfying the displayed budgets.',
  'The scaling factor is forced by Navier--Stokes scaling because dissipation has length dimension one. Halving the radius of a parabolic dyadic cell gives eight spatial children and four temporal children:',
  '83. Step 14: Outer-collar alignment and the jump--corona obstruction',
  '84 / Complete text',
  '84. Exact four-channel flux decomposition',
  '85 / Complete text',
  '85. The outer face and payment weight align exactly',
  '86 / Complete text',
  '86. Exact coefficient-cube interface',
  '87 / Complete text',
  '87. Scale-invariant parabolic measure and density roots',
  '88 / Complete text',
  '88. Density jumps are sparse, but the low-transition corona is unpaid',
  '89 / Complete text',
  '89. Shell incidence and the missing analytic charge',
  '90 / Complete text',
  '90. Exact heat shear: a narrow no-go for the raw tree',
  '91 / Complete text',
  '92 / Complete text',
  '92. Step 14 route decision',
  '93 / Complete text',
  '93. Bounded primary-source boundary',
  '94 / Complete text',
  '94. Step 14 claim ledger and finite certificate',
  '95 / Complete text',
  'This step has eight conclusions. The physical shell-flux derivative has an exact four-channel signed split into local cubic, local pressure, shell-scale harmonic pressure, and moving-frame drift; after taking absolute values channel by channel, the inherited estimate supplies only a linear payment. The outer derivative collar lies in the doubled-radius payment annulus with the same weight; the super-Gaussian ratio helps only the inner collar, with no gain on infinitely many outer collars. A smooth coordinate construction therefore proves that the aligned weighted ledger alone cannot imply any higher-integrability common-deletion tail; this is an',
  'The advance is a strict method boundary: super-Gaussian weights do not improve the aligned outer flux face, the density threshold does not improve the critical cubic payment power, and density jumps leave a corona uncontrolled by the current PDE ledger; the next positive statement is isolated exactly as the open lemma S.375.',
  'This release stops at R0.74S Step 14. If launched separately, subsequent work may test only the PDE-level jump--corona payment in S.375 or another explicitly new structure; the conditional interfaces S.358 and S.376 must not be presented as theorems.',
  'This route decision does not change the frozen target or its quantifiers.',
  'Use the half-open convention to preserve exact additivity of boundary atoms. First density roots are the maximal cells where the density first crosses the selected level; they form an antichain and satisfy the displayed bounds.',
  'But the level parameter cancels exactly in the cubic Holder product:',
  'As the bump width tends to zero, the right-hand side diverges, so one may arrange',
  ' statement; it supplies neither uniform higher temporal integrability nor a sublinear payment power. There is also a tail valid only for a fixed solution and fixed scale. Let',
  'The frozen main-text SHA-256 is `c843284d68c0d7d441214b0b3e67e97ca4c5ebda5f527a957eb6e9bdc07f55f9`. The Python certificate passes 12/12 exact checks, 9/9 finite groups, 74,287 finite rational cases, 3/3 dependencies, 37/37 structural checks, and 49/49 negative mutations. The independent Ruby verifier passes 7/7 groups, 82,788 cases, 6/6 artifact locks, 2/2 dependency locks, 68/68 note checks, 1/1 primary-artifact group, and 2/2 negative groups. The programs check exact algebra, fixtures, upstream hashes, equation numbering, selected formula bindings, and claim wording; they do not machine-prove analytic PDE estimates, open gates, regularity, or the Millennium problem.',
  'For each fixed maximum scale, the index tail tends to zero, but the energy bracket has no available uniform bound. Thus S.349 is not a uniform-in-scale payment theorem.',
  'More generally, if the coefficient cube is a power of the radius, then',
  'Fix a strict density-jump factor and a tree node of positive mass. The first proper descendants whose density crosses that relative factor are disjoint, so',
  'Fix a higher time exponent, deletion count, starting index, target constant, and payment. Choose one more distinct shell than can be deleted and use a smooth unit-mass bump near an interior terminal. Set',
  'A candidate PDE construction must first unfold every nonnegative collar row to the Euclidean lift, then cover all lifted shell supports by a countable locally finite comoving parabolic forest from a fixed finite family of shifted grids. Each top cell chooses a density level, takes first roots, and iterates first relative jumps. Incidence refers to one unperiodized lifted support.',
  'Analytic schematic · not simulation or DNS · NO DGX',
  'Let the lifted total local-dissipation measure and lifted mollified path define the following scale-invariant measure in dimensionless comoving coordinates:',
  'Let one common finite shell set be deleted and let the remaining shell--node pairs form a countable incidence multiset. Assume',
  'Use rescaled time and the nonnegative dimensionless majorants of the four vector integrands. Then',
  'Its gradient is supported only in the two collars:',
  'The first two inner collars lie in the core. For later shells, the target-to-payment ratio on the inner face is',
  'However, the moving velocity is independent of the first coordinate, the path velocity is parallel to it, and periodic integration gives',
  'If S.375 holds, substitute its top and corona rows into S.356--S.358 to obtain',
  'If one node is incident to many shells, one cannot count only distinct-node coefficients; incidence multiplicity must be controlled uniformly, or the repeated cubic sum and repeated payment in S.357 must be proved directly.',
  'are the aligned smooth coordinate rates in S.353--S.355 and the S.370 critical eight-ary corona embedding inherited from the Step 13 ledger model.',
  'The needed property is uniform Dini summability, not pointwise strictness. In the Step 13 critical-corona model, a 32-child tree retains one temporal child and all eight spatial children. Density decreases strictly along each branch, yet the retained coefficient cube stays critical:',
  'The same deleted shell set must serve both defect and high-Rayleigh ancestors and cannot move between levels or payment channels. All constants are uniform. Payment traverses the full incidence multiset, including periodic copies, overlaps, and repeated shell uses. The top row contains pre-crossing cells and top-boundary terms; the corona row contains moving-frame drift and every node unreached by the jump skeleton.',
  'Outer-collar alignment, critical threshold, and the jump--corona boundary',
  'Same-weight outer-collar alignment, no gain at the critical density threshold, the jump skeleton, and the unpaid corona; S.375 remains open',
  'The outer derivative collar aligns exactly with the same-weight payment annulus, the critical-level parameter cancels completely, and the first-jump skeleton contracts under the stated hypotheses.',
  'Assign nonnegative payment to every node occurrence, count repeated incidences repeatedly, and use the stated zero and infinity conventions. If',
  'The following statement for the bare periodic suitable-weak class is',
  'Thus a deep critical dissipation tree need not create any physical shell-flux tail. This exact family refutes neither S.342 nor S.375 and does not realize the abstract ancestor failure in S.370; its completed clocks are paid by the quadratic local-energy channel.',
  'On the periodic torus, take a positive amplitude, a positive integer depth, and a dyadic frequency:',
  'In comoving coordinates, after unfolding every nonnegative periodized integral, the collar family is stationary. A lifted cell at the stated physical resolution meets at most two shell indices:',
  'In distributions, the pressure remainder and its fixed-gauge form are harmonic on the shell-scale ball; Weyl lemma supplies smooth representatives. The gauge constant does not change flux. For almost every time, unfolding the cutoff gives',
  'In the standard dyadic spatial grid, once the generation is finer than the wavelength, each child interval contains an integer number of squared-cosine periods; density is constant in the other directions, so',
  'the Holder inequality on the incidence multiset gives',
  'Here the coefficient is the Step 13 incidence coefficient, not the root factor in S.363. This example is an',
  'The prefactor becomes a bare weighted constant only after the cutoff-gradient estimate. Calderon--Zygmund, Young, the fixed-gauge pressure majorant, local cubic estimate, and Jensen--Young drift estimate together give',
  'This is an',
  'This geometry is favorable, but the transported local-energy test still produces Version-M drift, whose absolute estimate appears only in the linear payment S.348. Finite shell incidence alone cannot place drift or the low-transition corona in the quadratic budget; whenever a cell is reused, its payment must also be counted repeatedly as in S.357.',
  'These are smooth nonnegative scalar rates, not fluxes generated by one velocity and pressure. S.355 is an',
  'This is only a collision boundary, not a novelty or priority claim, and not an exhaustive literature review.',
  'Iterating only along first-jump descendants gives the uniform Dini sum:',
  'Status · R0.74S STEP 14',
  'The final inclusion must track the shell radius. A pressure remainder constructed only at one fixed radius is not harmonic on every outer shell. Use the displayed shell-scale localization while retaining the fixed frozen gauge, and define',
  'The aligned spike and critical corona are only ABSTRACT METHOD OBSTRUCTIONS; S.358 and S.376 remain CONDITIONAL, while S.342 and S.375 remain OPEN. NOT CLAY.',
  'The aligned weighted payment equals the prescribed total exactly. After deleting all but one of the coordinates, one identical target coordinate remains:',
  'CKN suitable-weak local energy, epsilon regularity, and parabolic singular-set size do not supply the repeated-mass, incidence, or low-transition-corona budgets in S.375. Nearby trajectory, critical-space, partial-regularity, and pressure-sensitive estimates likewise do not produce the required common-deletion shell tail or payment-additive corona charge.',
  'The doubled-radius exterior-payment annuli are the displayed radial regions. The collars satisfy',
  'On the Euclidean lift, the frozen cutoff is',
  'The positive algebra for the excess branch is complete in S.358. The next task is the PDE content of S.375, beginning with the low-transition corona and top-boundary row; density thresholds and jump sparsity can be used only after repeated incidence payments are fully recorded. Exact-family screening must be shell selective: high Fourier frequency, a deep raw dissipation tree, or a large Rayleigh ratio is insufficient because physical flux may vanish or the completed clock may already be paid by the quadratic channel.',
  'The correct excess-branch interface is a cubic coefficient sum over the shell-incidence multiset, with payment counted at the same multiplicity. First density crossings are sparse, but the level parameter cancels exactly at the cubic endpoint. First relative jumps have a strict Dini coefficient, yet the low-transition corona between jumps remains unpaid. Exact heat shear shows that a deep critical mass tree can coexist with zero physical shell flux; this is only a narrow screen, not an NSE counterexample. The remaining positive task is isolated as a shell-selective jump--corona lemma, which is an',
  'implication: the algebra is proved, while the PDE construction in S.356--S.357 is not. With the displayed factorization, the final term is exactly the cubic coefficient sum. Its exponent is exact because',
  'measure-tree facts, but they control only the jump skeleton. Between jumps, the low-transition corona has only a bounded relative density; no inherited local-energy inequality puts all its shell contributions into the quadratic row of S.357. A strict factor at each level is also insufficient:',
  'The outer face has no analogous gain:',
  'R0.74T / Follow-up research',
  'The root mass has the exact critical factorization:',
  'S.348 is a',
  'S.350--S.352 concern the specific method that first takes absolute values on every outer collar and then compares with nonnegative exterior payment; they form a',
  'S.365 is a',
  'S.366--S.368 are',
  'Consequently S.376 closes the ancestor gate S.288 conditionally. The Holder arrow is proved; the missing mathematics is a PDE estimate that pays the top and low-transition corona at quadratic scale while preserving shell incidence and payment additivity.',
  'The supports of shells two indices apart have the stated radial separation, so double incidence can occur only at a shared hard boundary of adjacent padded shells. S.371 applies to one unfolded Euclidean support, not a torus cell and all periodized copies. Larger cells must be subdivided to this resolution.',
  'The short branch will not continue by taking absolute values channel by channel in S.345 and applying only the existing nonnegative payment. The outer-face coefficients align exactly, and the smooth spike in S.353--S.355 saturates that information. The next acceptable input must be signed local-energy cancellation on outer collars or a PDE temporal anti-concentration theorem uniform after one common finite shell deletion. The target S.342 remains',
  'statements are: S.358 depends on the exact incidence budgets in S.356--S.357; S.376 depends on the open shell-selective jump--corona lemma S.375.',
  'Comparing the bounded primary-source screens in Steps 12--13 with the two interfaces here found no cited theorem having the common-deletion flux-tail quantifiers of S.342 or the shell-selective jump--corona quantifiers of S.375.',
  'Step 13 split possible repairs leading to quadratic payment into two branches: a common-deletion temporal tail for the short branch and a strict cubic Dini--Carleson charge for full-history ancestors in the excess branch. Step 14 tests both interfaces against the actual cutoff geometry and the scale of total local dissipation. Continue to write',
  'Step 13 S.342, the ancestor gate S.288, combined gate S.303, Step 11 S.272, Q.12, and Q.1 all remain',
  'Step 14',
  'Step 14 independent audit',
  'Step 14 machine-certificate JSON',
  'In the frozen setting, Step 14',
  'Step 14 certificate report',
  'Step 14 Chinese reader source',
  'Step 14 primary audit',
  'Step 14 analytic main text, certificate, and dual audit',
  'Step 14 final analytic main text',
  'Step 14: Python passes 12/12 exact, 9/9 finite groups (74,287 cases), 37/37 structural, 3/3 dependency, and 49/49 negative checks; Ruby passes 7/7 groups, 82,788 cases, 6/6 artifact locks, 2/2 dependency locks, 68/68 note checks, 1/1 primary-artifact group, and 2/2 negative groups (99 cases). Finite certificates do not replace the analytic proof.',
];

function withProtected(summary, source) {
  const tokens = extractProtectedTokens(source);
  return tokens.length === 0 ? summary : `${summary} ${tokens.join(' ')}`;
}

process.chdir(root);
const [source, order, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings('./public'),
  readFile(translationPath, 'utf8').then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);
const baseCurrent = checkOnly ? current : current.filter((row) => !rowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missing = source.filter((entry) => !currentByZh.has(entry.zh));
const missingOrder = order.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missing.length, 0, 'site still has untranslated Chinese strings');
  const rows = current.filter((row) => rowPattern.test(row.id));
  assert.equal(rows.length, summaries.length, 'R0.74S Step 14 translation count drift');
  assert.deepEqual(rows.map((row) => row.en), rows.map((row, index) => withProtected(summaries[index], row.zh)), 'R0.74S Step 14 English translation drift');
} else {
  assert.equal(missing.length, summaries.length, 'R0.74S Step 14 source-string count drift');
  const sourceByZh = new Map(missing.map((entry) => [entry.zh, entry]));
  const additions = missingOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = withProtected(summaries[index], entry.zh);
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), `protected token drift ${index + 1}: ${entry.zh}`);
    return { id: `${prefix}${String(index + 1).padStart(3, '0')}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...baseCurrent, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({ release: 'R0.74S Step 14', translationPath: 'LOCAL_DIRECT_NO_DGX', dgxUsed: false, checked: summaries.length, applied: !checkOnly }, null, 2)}\n`);
