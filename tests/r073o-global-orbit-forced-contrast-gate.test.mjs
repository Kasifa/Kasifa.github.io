import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFile(resolve(root, relative), "utf8");

const paths = Object.freeze({
  freeze: "research/r073o_problem_freeze.md",
  unforced: "research/r073o_global_orbit_stability_proof.md",
  forced: "research/r073o_forced_kolmogorov_contrast.md",
  independent: "research/r073o_independent_analytic_audit.md",
  literature: "research/r073o_literature_audit.md",
  ledger: "research/r073o_claim_source_ledger.md",
  gap: "research/r073o_gap_matrix.md",
  dictionary: "research/r073o_bilingual_dictionary.md",
  report: "research/r073o_report-source.md",
});

const closedTokens = Object.freeze([
  "unforcedGlobalOrbitH3Stability=CLOSED_CONDITIONALLY_AFTER_AUDIT",
  "unforcedFiniteAccumulatedH4=CLOSED_CONDITIONALLY_AFTER_AUDIT",
  "unforcedH3InputL2Output=CLOSED_AS_COROLLARY",
  "forcedKolmogorovPositivePlanarSpectrum=CLOSED_BY_COMPOSITE_PRIMARY_SOURCE_CHAIN_AFTER_AUDIT",
  "forcedKolmogorovH3InputL2Escape=CLOSED_BY_COMPOSITE_PRIMARY_SOURCE_CHAIN_AFTER_AUDIT",
  "forcedWitnessSolutionsGlobalSmooth=PLANAR_ONLY",
]);

const boundaryTokens = Object.freeze([
  "uniformL2OnlyInputThreshold=OPEN_COLLISION_SENSITIVE",
  "arbitraryThreeDimensionalGlobalRegularity=OPEN",
  "positiveEigenvalueAlgebraicallySimple=OPEN_NOT_CLAIMED",
  "essentiallyThreeDimensionalUnstableMode=OPEN_NOT_NEEDED",
  "forcedConclusionTransfersToClay=FALSE",
  "finiteComputationProvesInfiniteDimensionalSpectrum=FALSE",
  "finiteComputationProvesNonlinearInstability=FALSE",
  "finiteComputationReplacesNagatouCertificate=FALSE",
  "clayConclusion=OPEN",
  "noveltyOrPriorityClaim=FORBIDDEN",
]);

test("R0.73O independent readback closes the two scoped theorem interfaces", async () => {
  const values = Object.fromEntries(await Promise.all(
    Object.entries(paths).map(async ([name, relative]) => [name, await read(relative)]),
  ));

  assert.match(values.independent,
    /\*\*Release verdict:\*\* \*\*FORMAL PASS after two documented repair rounds\.\*\*/);
  assert.match(values.independent, /\*\*Unforced theorem decision:\*\* \*\*PASS/);
  assert.match(values.independent, /### 7\.5 Final decision and exact claim boundary[\s\S]*\*\*FORMAL PASS\.\*\*/);
  assert.match(values.forced,
    /\*\*Status:\*\* \*\*FORMAL PASS after final independent analytic readback\.\*\*/);
  assert.match(values.literature, /bounded primary-source audit complete/);
  assert.match(values.ledger, /\| O1 \|[\s\S]*\| O2 \|[\s\S]*\| O3 \|/);
  assert.match(values.ledger, /\| F1 \|[\s\S]*\| F2 \|[\s\S]*\| F3 \|[\s\S]*\| F4 \|[\s\S]*\| F5 \|/);

  for (const [name, value] of Object.entries(values)) {
    assert.equal(value.endsWith("\n"), true, `${name}: final newline`);
    assert.doesNotMatch(value, /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/,
      `${name}: forbidden control character`);
  }
});

test("R0.73O unforced gate is finite-action H3 stability for an a priori global orbit", async () => {
  const [freeze, proof, report] = await Promise.all(
    [paths.freeze, paths.unforced, paths.report].map(read),
  );
  const sources = `${freeze}\n${proof}`;

  for (const phrase of [
    "u\\in C([0,\\infty);H^3_{\\sigma,0})",
    "\\cap L^2_{\\rm loc}([0,\\infty);H^4_{\\sigma,0})",
    "\\mathcal A_4[u]:=\\int_0^\\infty|u(t)|_4\\,dt<\\infty",
    "R_A[u]={1\\over4C_*}e^{-C_*\\mathcal A_4[u]}>0",
    "for every \\(t_0\\ge0\\)",
    "the same radius works for every",
    "\\mathcal G_3\\) is open",
  ]) assert.ok(sources.includes(phrase), `unforced contract: ${phrase}`);

  assert.ok(proof.includes("\\le e^{C_*\\mathcal A_4[u]}"));
  assert.ok(proof.includes("e^{-(t-t_0)/2}|v(t_0)-u(t_0)|_3"));
  assert.ok(proof.includes("custom\n\\(H^3\\)-input/\\(L^2\\)-output corollary"));
  assert.ok(proof.includes("It does not prove full-three-dimensional FPS"));
  assert.ok(proof.includes("small only in \\(L^2\\) and possibly arbitrarily large in \\(H^3\\)"));
  for (const token of closedTokens.slice(0, 3)) assert.ok(report.includes(token), token);
});

test("R0.73O forced gate uses the complete spectral chain and planar FPS topology", async () => {
  const [forced, independent, report] = await Promise.all(
    [paths.forced, paths.independent, paths.report].map(read),
  );
  const sources = `${forced}\n${independent}`;

  assert.ok(sources.includes("U_*(x,y,z)=(30.12\\sin 10y,0,0)"));
  assert.ok(sources.includes("f_*(x,y,z)=(3012\\sin 10y,0,0)"));
  for (const phrase of [
    "\\alpha={m\\over N}=0.7",
    "R={30.12\\over10}=3.012",
    "[3.011528364444,\\;3.011528364446]",
    "\\operatorname{rank}\\Pi_{3.012}>0",
    "n=2,\\qquad p=2,\\qquad q=4",
  ]) assert.ok(forced.includes(phrase), `forced contract: ${phrase}`);
  assert.equal(3.012 > 3.011528364446, true, "certified parameter is supercritical");
  assert.ok(forced.includes(
    "operator at \\(U_*\\) has at least one positive real eigenvalue and a smooth"));
  assert.ok(forced.includes("extend a planar vector field constantly in \\(z\\)"));
  assert.match(forced, /every escaping solution in this construction is globally smooth/);
  for (const phrase of [
    "Ilyin supplies a finite high-\\(R\\) anchor",
    "Riesz projection varies continuously",
    "Nagatou Proposition 2.1",
    "Matsuda--Miyatake recurrence",
  ]) assert.ok(independent.includes(phrase), `independent forced readback: ${phrase}`);
  for (const token of closedTokens.slice(3)) assert.ok(report.includes(token), token);
});

test("R0.73O claim boundary keeps L2-only input, essential 3D, singularity, and Clay open", async () => {
  const [freeze, forced, literature, gap, dictionary, report] = await Promise.all(
    [paths.freeze, paths.forced, paths.literature, paths.gap, paths.dictionary,
      paths.report].map(read),
  );

  for (const token of [...closedTokens, ...boundaryTokens]) {
    assert.ok(report.includes(token), `report boundary: ${token}`);
  }
  for (const token of [
    "uniformL2OnlyInputThreshold=OPEN_COLLISION_SENSITIVE",
    "forcedConclusionTransfersToClay=FALSE",
    "finiteComputationProvesInfiniteDimensionalSpectrum=FALSE",
  ]) assert.ok(dictionary.includes(token), `dictionary boundary: ${token}`);
  assert.match(gap,
    /\| G3 \|[^\n]+\| \*\*OPEN \/ COLLISION-SENSITIVE\*\* \|/);
  assert.match(gap, /\| G4 \|[^\n]+\| \*\*OPEN\*\* \|/);
  assert.match(gap, /\| F3 \|[^\n]+\| \*\*NOT CLAIMED\*\* \|/);
  assert.match(gap, /\| C2 \|[^\n]+\| \*\*INVALID\*\* \|/);
  assert.match(literature, /\*\*No\. Classical\.\*\*/);
  assert.match(literature, /Mucha 2001[\s\S]*exact threshold dependence/);
  assert.match(freeze, /finite-time singularity, global regularity for arbitrary data, or the[\s\S]*Clay conclusion/);
  assert.match(forced, /does not establish finite-time blow-up[\s\S]*unforced Clay equation/);

  const joined = [freeze, forced, literature, gap, dictionary, report].join("\n");
  assert.doesNotMatch(joined, /(?:first|unprecedented) (?:global )?(?:stability|instability) theorem/i);
  assert.doesNotMatch(joined, /(?:solves?|resolved?) the Clay/i);
  assert.ok(joined.includes("NOT CLAY"));
});
