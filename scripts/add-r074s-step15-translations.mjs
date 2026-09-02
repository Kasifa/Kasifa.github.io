#!/usr/bin/env node

import assert from 'node:assert/strict';
import { readFile, writeFile } from 'node:fs/promises';
import { resolve } from 'node:path';
import { collectSiteStrings, containsChinese, extractProtectedTokens } from './i18n-lib.mjs';

const root = resolve(import.meta.dirname, '..');
const translationPath = resolve(root, 'translations/en.json');
const publicRoot = resolve(root, 'public');
const checkOnly = process.argv.includes('--check-only');
const prefix = 'r074sstep15';

// Local, direct translations in deterministic collectSiteStrings order. TeX
// tokens are copied byte-for-byte by withProtected rather than translated.
const summaries = [
  'Current endpoint R0.74S Step 15',
  'If separately launched, test only OPEN S.342, OPEN S.407, or another explicit new PDE input; this release contains only R0.74S Step 15.',
  'Same-deletion best-N equivalence and the depth-independent terminal-crown budget are fixed; S.342, S.407, Q.1, and regularity remain OPEN. NOT CLAY.',
  'Same-deletion best-N equivalence and the depth-independent terminal-crown budget are proved; full closure still depends on OPEN S.342 and OPEN S.407, and S.408 remains CONDITIONAL. NOT CLAY.',
  'One deletion set controls both residual branches, and terminal crowns give a depth-independent budget; full closure still depends separately on OPEN S.342 and OPEN S.407. The two stress tests are uncoupled. NOT CLAY.',
  'Research note R0.74S Step 15 · 2026-09-03',
  'Review v1.94 · 2026-09-03',
  'R0.74S Step 15 fixes same-deletion best-N equivalence and a depth-independent terminal-crown budget; S.408 remains conditional, while S.342, S.407, Q.1, and the upstream PDE gates remain OPEN.',
  'R0.74S: Hybrid-flux equivalence and the terminal-crown coercivity gap',
  'R0.74S｜Hybrid-flux equivalence and the terminal-crown coercivity gap',
  'Step 15 formal analytic schematic',
  'Hybrid-flux equivalence and the terminal-crown coercivity gap',
  'If separately launched, test OPEN S.342, OPEN S.407, or another explicit new PDE input.',
  'Literature review v1.94 · 2026-09-03',
  'PROVED: hybrid-coordinate comparison, same-deletion equivalence, signed common-window debt, terminal-crown ownership, and the depth-independent budget in S.377–S.406. CONDITIONAL: S.408 depends on OPEN S.407. ABSTRACT METHOD OBSTRUCTION: S.409–S.412 is not an NSE counterexample. FINITE: Python passes 5/5 dependency, 9/9 finite groups (3,941 cases), 45/45 structural, and 20/20 negative checks, with a separate Ruby implementation. OPEN: S.342, S.375, S.407, S.288, S.303, S.272, Q.12, Q.1, scale contraction, and regularity.',
  'R0.74S Step 15 public boundary',
  'S.377–S.416 fix same-deletion best-N equivalence, the start-clock overshoot debt, and a depth-independent terminal-crown budget; S.408 remains conditional, while S.342, S.407, Q.12, and Q.1 remain open.',
  'Step 15 proves same-deletion best-N equivalence between the hybrid-start flux and the residual, and a depth-independent coefficient budget for terminal crowns. The converse-Hölder flat-data family is only an abstract method obstruction; the periodic measure tree and scalar clock are uncoupled stress tests. No novelty or priority is claimed.',
  'Research-note master index · v1.94 · 2026-09-03',
  ', not a PDE counterexample to S.407.',
  ': the common-deletion temporal flux tail S.342, the selected-crown nonlinear payment S.407, and inherited S.375. Continue to write',
  ': S.288, S.303, S.272, Q.12, Q.1, scale contraction, regularity, singularity formation, and the Navier--Stokes Millennium problem.',
  ': the hybrid vector, sharp coordinate comparison, and same-deletion best-N equivalence in S.377--S.387; the conditional implication in S.388--S.391; the signed-window debt identity in S.392--S.395; the abstract sharpness checks in S.396--S.397; the ancestor submeasure, ownership, terminal crowns, and depth-independent coefficient content in S.398--S.404; the exact factorization and conditional Hölder closure in S.405--S.408; the converse-Hölder method obstruction in S.409--S.412; and the two separate stress tests in S.413--S.416.',
  ': bookkeeping for the top boundary and every low-transition crown is closed, but antecedent S.407 remains open.',
  '. The periodic positive-measure tree and the selected scalar clock pass only separate geometric and scalar stress tests; they are not coupled into one completed-clock/measure fixture and are not Navier--Stokes counterexamples.',
  '1. Prove S.342. By S.387--S.391, one common-deletion theorem with the same N_F closes the combined residual, eliminating the ancestor jump--corona route. 2. If the ancestor route is retained, S.404 supplies a depth-independent coefficient budget for every finite-depth terminal crown; the remaining PDE burden is the occurrence-level 3/2 coercivity in S.407. It must record top and stopping faces, pressure, moving drift, defect, and the infinite-jump remainder after the same shell deletion.',
  '100 / Complete text',
  '100. Shellwise ownership and terminal crowns',
  '101 / Complete text',
  '101. First roots, first jumps, and the depth-independent coefficient budget',
  '102 / Complete text',
  '102. Open nonlinear crown payment and conditional closure',
  '103 / Complete text',
  '103. Converse Hölder and the linear-payment method obstruction',
  '104 / Complete text',
  '104. Two uncoupled stress tests',
  '105 / Complete text',
  '105. Route decision, literature boundary, and certificate',
  '106 / Complete text',
  '95. Step 15: Hybrid-flux equivalence and the terminal-crown coercivity gap',
  '96 / Complete text',
  '96. Hybrid starts and one physical-flux vector',
  '97 / Complete text',
  '97. The same Q-variation diamond and best-N equivalence',
  '98 / Complete text',
  '98. One common-deletion temporal tail pays both branches',
  '99 / Complete text',
  '99. Start-clock debt in the signed common window',
  'Integrating the Step 14 four-channel identity over the hybrid active blocks gives',
  'Retain the dimensionless flux density from Step 13. Absolute continuity and S.377 give',
  'This step',
  'This step does not prove S.342, S.375, S.407, Q.12, Q.1, scale contraction, regularity, singularity formation, or the Millennium problem, and it makes no novelty or priority claim. The finite certificate checks algebra, combinatorics, hashes, structure, and boundary wording; it does not machine-prove an open PDE input.',
  'This release contains only R0.74S Step 15 and stops here. Any separately launched follow-up may test only OPEN S.342, OPEN S.407, or another explicit new PDE input; S.408 and Q.1 must not be presented as theorems.',
  'and the inherited terminal reduction yields',
  'Iterating the first proper kappa-jump descendants from every root gives',
  'Equivalently, if the cubic coefficient sum is controlled by a fixed constant, then',
  'Define the start-clock overshoot',
  'For each selected-excess index at the terminal, set',
  'For countable locally finite half-open forest-top occurrences, construct Borel ownership shell by shell:',
  'Define the canonical crown payment on the paid part',
  'For a selected ancestor, define a finite positive Borel submeasure. The frozen definition and cutoff domination give',
  'For the independent crown route, each terminal corona is compressed into a disjoint crown counted once, and its cubic coefficient budget is independent of stopping depth. This combinatorial fact does not supply the missing PDE coercivity: the selected-crown nonlinear payment S.407 remains',
  'For nonnegative rows, with total coefficient A and total payment P, the exact converse to Hölder is',
  'For the same arbitrary shell set of size at most N, sum first and then optimize to obtain',
  'Fix one Version-M suitable weak solution, scale R, and good terminal time. Retain',
  'A more direct but equally unproved interface is to establish a signed local-energy cancellation bound for the hybrid flux. By S.385 it differs from the Step 10 residual gate by only the literal factor 5. For shallow short intervals, S.395 shows that any signed common-window proof must also control the start-clock overshoot.',
  'Same-deletion best-N equivalence for the hybrid-start flux, the depth-independent terminal-crown budget, and the still-open S.342 and S.407',
  'Hybrid-flux equivalence and the terminal-crown interface',
  'The two Q-variation terms come from the same full-history variation measure, so they are not two independently saturable errors:',
  'Let the displayed quantity be the supremum over good terminals of the best-N hybrid-flux tail; then',
  'Each low-transition corona is counted as one crown, not once at every dyadic generation. Infinite-jump mass remains in the last finite-depth crown and cannot be dropped at the limit. The full crown--shell incidence multiset therefore satisfies',
  'Taking M=N_b+1 scalar copies gives',
  'Choose the canonical top level as mass divided by volume. First crossing roots satisfy',
  'The missing PDE statement is',
  'If S.400, S.405, and S.407 all hold, Hölder and S.404--S.406 give',
  'If the still-open Step 13 estimate is stated explicitly as the antecedent,',
  'satisfy a two-sided best-N equivalence; terminal crowns also supply a depth-independent coefficient budget.',
  'Thus signed synchronization replaces coordinatewise absolute increments by two same-deletion tasks: common-window cancellation and control of start-clock overshoot. This debt is an exact algebraic fact, but the witness remains only an abstract clock check.',
  'Thus it has no upward kappa-jump while retaining arbitrarily deep low-transition coronas; all periodic copies still enter the finite constant. Independently, rescale the Step 11 pure-defect scalar fixture to obtain',
  'Thus, with only linear payment, at least one of the normalized q-budget and cubic coefficient budget must diverge. This conclusion concerns formal nonnegative incidence data and is an',
  'Summing under the same deletion set gives',
  'same deletion set',
  'First choose one common shell exception set of size at most N_b, then use it for all tops, crowns, defect, and high-Rayleigh channels. Decompose the owned crown mass as',
  'The new hybrid-start physical-flux vector and the residual vector, on the',
  'Choose a common local-energy good time in the frozen initial interval so every shell clock vanishes there. Define',
  'Therefore the full hybrid-flux gate and full combined-residual gate are equivalent under the same terminal-dependent deletion budget, with constants 1/5 and 1. The abstract scalar-ledger rows in S.396 approach 1/5 and 3/7, proving sharpness under the stated scalar constraints; they are not NSE counterexamples.',
  'Hence the minimal signed common-window gate is',
  'Combining this with equality on the short branch gives',
  'Even if the forest, grids, levels, depth, and common exception set adapt after observing the data, the full repeated incidence multiset still satisfies the following: if q-budget and payment have the displayed orders, then for large H',
  'Direct optimization within the same diamond constraints of S.380 gives the sharp scalar constants',
  'In the standard grid, every retained child satisfies',
  'The entire time norm deletes one shell set before the terminal or branch is chosen, hence',
  'At any finite stopping depth, the top crown, nonterminal jump crowns, and terminal-depth crowns form an exact half-open partition:',
  'then the same N_F gives',
  'Repeating a top increases the top content accordingly; it is not hidden in a geometric constant.',
  'These two statements are PROVED, but full closure still depends separately on OPEN S.342 and OPEN S.407; S.408 is only CONDITIONAL. Q.1, regularity, and the Millennium problem remain OPEN. NOT CLAY.',
  'This permits a new PDE cancellation, but algebraic regrouping alone creates no gain. For a common terminal-window start, a shallow shell satisfies',
  'Status · R0.74S STEP 15',
  'Equality holds precisely when the payment rows are proportional to the coefficient rows. Fix any deletion budget, take one more distinct shell coordinate than can be deleted, and set',
  'Forest overlap therefore does not duplicate ancestor mass; adjacent-shell incidence, shifted-grid occurrence, periodic copy, and repeated top occurrence remain distinct. Define the incidence-weighted top content',
  'The frozen bounded collision check compares physical-space flux locality, skewed-cylinder maximal and covering estimates, reverse Hölder under extra local kinetic control, anomalous-dissipation support results, quantitative partial regularity, and Navier--Stokes inequality flexibility. None supplies the frozen quantifiers of S.342 or S.407. This is a finite collision check, not an exhaustive review or a novelty or priority claim.',
  'The frozen primary certificate passes 9/9 finite groups, 3,941 finite cases, 5/5 dependency, 45/45 structural, and 20/20 negative checks. The independent Ruby verifier reconstructs vectors, deletion sets, trees, crowns, and incidence rows, and locks both main texts, both implementations, the certificate, and report hashes. It checks finite algebra and combinatorics, not S.342, S.407, or any PDE realization. Both audits PASS within this boundary.',
  'hybrid-flux main text',
  'Last-exit maximality controls only the last-exit interval and cannot control an earlier common start. The abstract clock in S.397 gives',
  'The periodic positive-measure tree takes',
  'Proposition 3.1 is therefore an',
  'independent Ruby implementation',
  'S.377--S.379 are representation and sign conclusions, not a PDE bound on the hybrid vector.',
  'S.388--S.391 prove an implication, not S.342 or Q.1. Their route-level meaning is that if S.342 holds, it closes both short and selected-excess residuals without another exception budget or ancestor coefficient.',
  'The constant in S.404 is independent of depth, top count, and top levels. This closes the cubic coefficient side, not the payment estimate.',
  'S.407 requires a constant uniform over solution, scale, terminal, forest, top count, levels, and stopping depth. If the same frozen payment is used by multiple occurrences, it must be counted repeatedly in the sum. S.407 is not a consequence of the local-energy inequality proved here.',
  'S.413--S.414 test only measure geometry, while S.415--S.416 test only selected scalar-clock arithmetic. They share neither a completed-clock/measure identity nor a velocity-pressure Navier--Stokes realization. Their side-by-side display must not be described as a coupled counterexample.',
  'The selected excess is therefore a subcoordinate of that physical-flux vector:',
  'Step 14 separated the common-deletion short-branch flux tail S.342 from the excess-branch jump--corona input S.375. Step 15 proves an exact reduction not previously recorded: the short last-exit and selected-excess residuals fit one nonnegative stopped physical-flux vector and are coordinatewise equivalent to the full residual under the same best-N deletion set. Thus, if open S.342 is later proved, the same N_F pays both residual branches without another ancestor budget.',
  'Step 15 compresses the acceptable next input into two independent routes.',
  'Step 15 Chinese reader source',
  'Step 15 main texts, certificate, and dual audit',
  'Step 15: Python passes 5/5 dependency, 9/9 finite groups (3,941 cases), 45/45 structural, and 20/20 negative checks; Ruby supplies an independent certificate implementation. Finite certificates do not replace analytic proof.',
  'The terminal clock and last-exit identity are',
  'terminal-crown main text',
];

function withProtected(summary, source) {
  const tokens = extractProtectedTokens(source);
  return tokens.length === 0 ? summary : `${summary} ${tokens.join(' ')}`;
}

process.chdir(root);
const [source, order, current] = await Promise.all([
  collectSiteStrings(publicRoot), collectSiteStrings('./public'),
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
  assert.equal(rows.length, summaries.length, 'R0.74S Step 15 translation count drift');
  assert.deepEqual(rows.map((row) => row.en), rows.map((row, index) => withProtected(summaries[index], row.zh)), 'R0.74S Step 15 English translation drift');
} else {
  assert.equal(missing.length, summaries.length, 'R0.74S Step 15 source-string count drift');
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

process.stdout.write(`${JSON.stringify({ release: 'R0.74S Step 15', translationPath: 'LOCAL_DIRECT_NO_DGX', dgxUsed: false, checked: summaries.length, applied: !checkOnly }, null, 2)}\n`);
