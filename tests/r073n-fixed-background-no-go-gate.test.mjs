import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFile(resolve(root, relative), "utf8");

const paths = {
  freeze: "research/r073n_problem_freeze.md",
  proof: "research/r073n_fixed_background_no_go_proof.md",
  scaling: "research/r073n_scaling_obstruction.md",
  independent: "research/r073n_independent_analytic_audit.md",
  adversarial: "research/r073n_adversarial_audit.md",
  literature: "research/r073n_literature_audit.md",
  ledger: "research/r073n_claim_source_ledger.md",
  gap: "research/r073n_gap_matrix.md",
  dictionary: "research/r073n_bilingual_dictionary.md",
  report: "research/r073n_report-source.md",
};

const closedTokens = [
  "fixedTimeRelativeL2LipschitzBound=CLOSED",
  "finiteAllTimeStrainEnvelope=CLOSED",
  "fixedMemberPlanarL2SynchronizedStability=CLOSED",
  "fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED",
  "fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY",
  "familyFlowMapNonuniformMarkedBasepointSensitivity=CLOSED",
  "familyDepartureImpliesFixedMemberInstability=FALSE_AS_INFERENCE",
  "singleR073mMemberH3SmallL2FixedDistanceEscape=FALSE",
];

const openTokens = [
  "fullThreeDimensionalFPSH3L2Stability=OPEN",
  "optimalFixedMemberStabilityRadius=OPEN",
  "sharpFamilyLipschitzExponent=OPEN",
  "arbitraryFixedBackgroundInstability=OPEN",
  "transverseCriticalNormGrowth=OPEN",
  "finiteTimeSingularity=OPEN",
  "Clay=OPEN",
];

test("R0.73N continuum sources close only the synchronized finite-strain route", async () => {
  const values = Object.fromEntries(await Promise.all(
    Object.entries(paths).map(async ([name, path]) => [name, await read(path)]),
  ));

  assert.match(values.independent, /\*\*Verdict:\*\* \*\*MATHEMATICAL FINAL PASS\*\*/);
  assert.match(values.adversarial, /\*\*Verdict:\*\* \*\*PASS\*\*/);
  assert.match(values.literature, /claim-boundary reconciliation PASS/);
  assert.match(values.proof, /independent analytic and adversarial audits,\s+direct symmetry audit, and bounded literature audit PASS/);
  assert.match(values.scaling, /independent analytic and\s+adversarial audits PASS/);

  for (const token of [...closedTokens, ...openTokens]) {
    assert.ok(values.freeze.includes(token), "freeze boundary: " + token);
    assert.ok(values.proof.includes(token), "proof boundary: " + token);
    assert.ok(values.independent.includes(token), "independent boundary: " + token);
    assert.ok(values.dictionary.includes(token), "dictionary boundary: " + token);
    assert.ok(values.report.includes(token), "report boundary: " + token);
  }

  assert.match(values.ledger, /fullThreeDimensionalFPSH3L2Stability=OPEN/);
  assert.match(values.ledger,
    /fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED/);
  assert.match(values.ledger,
    /fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY/);
  assert.match(values.ledger, /fixedMemberPlanarL2SynchronizedStability=CLOSED/);
  assert.match(values.gap,
    /\| G10 \|[^\n]+\| \*\*OPEN\*\* \|/);
  assert.match(values.dictionary, /finiteDiagnosticValidation=PASS/);
  assert.match(values.dictionary, /finiteDiagnosticPackage=CLOSED/);
  assert.match(values.dictionary, /sourceCommitAssigned=TRUE/);
  assert.match(values.dictionary, /finalSeal=TRUE/);
  assert.match(values.report, /formalFigurePackage=PASS/);
  assert.match(values.report, /publicReleaseContent=READY/);

  const joined = Object.values(values).join("\n");
  assert.doesNotMatch(joined,
    /\(H\^3,H\^3\)[^\n]{0,80}hence[^\n]{0,80}FPS \\\(H\^3,L\^2\\\)/i);
  assert.doesNotMatch(joined, /family of (?:time-[^ ]+ )?solution maps/i);
  assert.doesNotMatch(joined, /\bR0\.73N (?:does|has) resolve[sd]? the Clay/i);
  assert.doesNotMatch(joined, /(?:first|unprecedented) result/i);
});

test("R0.73N exact strain and endpoint inequalities have the registered constants", async () => {
  const [freeze, proof, independent] = await Promise.all(
    [paths.freeze, paths.proof, paths.independent].map(read),
  );
  const sources = freeze + "\n" + proof + "\n" + independent;

  const D = 1 / 450;
  const T = D / 4;
  const jStar = (1 - Math.exp(-4 * T)) / 4
    + (1 - Math.exp(-16 * T)) / 16;
  const taylorLower = 359 / 324000;
  const actionUpper = 173 / 450000;

  assert.equal(T, 1 / 1800);
  assert.ok(jStar > taylorLower);
  assert.ok(taylorLower > actionUpper);
  assert.equal(173n * 324000n < 359n * 450000n, true);
  assert.equal(25n * 8n + 289n, 489n);

  for (const phrase of [
    "j(\\infty)=\\frac5{16}",
    "\\frac{489}{32\\sqrt2}\\Lambda",
    "\\frac{359}{324000}",
    "\\frac{173}{450000}",
    "T_*:=\\frac{D_*}{4}=\\frac1{1800}",
  ]) assert.ok(sources.includes(phrase), "registered formula: " + phrase);

  assert.match(proof,
    /\\sup_\{0\\le t<T_\{\\max\}\}\\\|w\(t\)\\\|_2\s+\\le e\^\{5\\Lambda\/16\}/);
  assert.match(proof,
    /R_\\Lambda:=r_3e\^\{-C_3A_\{4,\\Lambda\}\}/);
  assert.match(proof,
    /r_3:=\\frac1\{4C_3\}/);
});

test("R0.73N topology and pointed-flow definitions are fail-closed", async () => {
  const [freeze, proof, literature] = await Promise.all(
    [paths.freeze, paths.proof, paths.literature].map(read),
  );

  for (const source of [freeze, proof, literature]) {
    assert.match(source, /forward synchronized/);
    assert.match(source, /t_0=0/);
  }
  assert.ok(freeze.includes("not renamed FPS \\((H^3,L^2)\\) stability"));
  assert.ok(proof.includes("does not prove FPS \\((H^3,L^2)\\) stability"));
  assert.ok(literature.includes(
    "Full-three-dimensional FPS \\((H^3,L^2)\\) stability is **OPEN**",
  ));

  assert.match(freeze, /\\mathcal D_T:=\\\{u_0\\in H\^3_\{\\sigma,0\}/);
  assert.match(freeze, /\\overline U_\\Lambda\(0\)\+h\\in\\mathcal D_T/);
  assert.match(freeze, /neighborhood is still localized in \\\(H\^3\\\)/);
  assert.ok(freeze.includes("For every sufficiently\nlarge \\(\\Lambda\\)"));
  assert.match(freeze, /\\mathfrak L_\{\\Lambda,\\mathrm\{loc\}\}\^\{2\\to2\}/);
  assert.match(freeze, /\\mathfrak L_\{\\Lambda,\\mathrm\{loc\}\}\^\{3\\to2\}/);
  assert.match(freeze, /\\mathcal E_\\rho/);
  assert.match(freeze, /not uniformly continuous/);

  assert.match(proof,
    /\\frac\{c_\*\}\{C_H\}\\Lambda\^\{-2\}e\^\{\\Lambda\\mathcal A_\*\}/);
  assert.match(proof, /same time-\\\(T_\*\\\) Navier--Stokes flow map/);
  assert.match(proof, /not different solution maps/);
});

test("R0.73N registered symmetry and compactness obstructions preserve the equation ledger", async () => {
  const scaling = await read(paths.scaling);

  for (const phrase of [
    "\\nu'=\\frac AC\\nu",
    "L'=\\frac LC",
    "T'=\\frac{T}{AC}",
    "b_\\Lambda=\\frac{a_\\Lambda^4}{\\Lambda^3}",
    "\\frac58\\Lambda^2",
    "amplitudeOnlyIdentificationIsNSSymmetry=FALSE",
    "timeTranslationIdentifiesLambdaFamily=FALSE",
    "parabolicScalingIdentifiesLambdaFamilyOnFixedTorus=FALSE",
    "finiteTimeSingularity=OPEN",
    "Clay=OPEN",
  ]) assert.ok(scaling.includes(phrase), "scaling boundary: " + phrase);

  assert.match(scaling, /covering map,\s+not an invertible torus automorphism/);
  assert.match(scaling, /Pure amplitude is accidental only on the base shear/);
  assert.match(scaling, /Every strong limit is either\s+zero or a single first-harmonic heat shear/);
});

test("R0.73N analytic text is free of forbidden control characters", async () => {
  for (const [name, path] of Object.entries(paths)) {
    const value = await read(path);
    assert.doesNotMatch(value, /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/,
      name + " contains a control character");
    assert.equal(value.endsWith("\n"), true, name + " lacks final newline");
  }
});
