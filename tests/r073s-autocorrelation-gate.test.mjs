import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const json = (relative) => JSON.parse(read(relative));

const canonicalPaths = [
  "research/r073s_problem_freeze.md",
  "research/r073s_quadratic_autocorrelation_certificate.md",
  "research/r073s_primary_literature_audit.md",
  "research/r073s_independent_analytic_audit.md",
  "research/r073s_independent_literature_readback.md",
  "research/r073s_claim_source_ledger.md",
  "research/r073s_evidence_gap_matrix.md",
  "research/r073s_report-source.md",
  "research/r073s_bilingual_dictionary.md",
];
const corpus = canonicalPaths.map(read).join("\n");

test("R0.73S keeps the classical, local, no-go, and open boundaries separate", () => {
  for (const token of [
    "VERIFIED_CLASSICAL",
    "complete collision",
    "not a runtime lower bound",
    "preselected strict subset",
    "complete finite autocorrelation",
    "zero-nonlinearity shear flows",
    "arbitrary-data regularity",
    "Clay conclusion",
  ]) {
    assert.ok(corpus.includes(token), token);
  }
  const report = read("research/r073s_report-source.md");
  const dictionary = read("research/r073s_bilingual_dictionary.md");
  const compactDictionary = dictionary.replace(/\s+/g, " ");
  assert.ok(report.includes("没有产生新的 Nikolskii 定理"));
  assert.ok(report.includes("不是 Clay 进展"));
  assert.ok(compactDictionary.includes("not a new harmonic analysis theorem"));
  assert.ok(compactDictionary.includes("does not prove a universal runtime lower bound"));
  assert.ok(compactDictionary.includes("not the complete finite autocorrelation"));
  assert.ok(compactDictionary.includes("not a Clay result"));
  assert.doesNotMatch(report, /我们|攻关|主攻|突破|首次证明|原创性定理/);
});

test("the analytic source contains the autocorrelation certificate and its exact hard limits", () => {
  const proof = read("research/r073s_quadratic_autocorrelation_certificate.md").replace(/\s+/g, "");
  for (const token of [
    "C(h)=",
    "\\|f\\|_6^6\\leA Q",
    "\\|f\\|_6\\leD_C^{1/12}\\|f\\|_4",
    "D_C=4m-1",
    "32m\\le|k|<36m",
    "311",
    "323",
    "q\\ge14",
    "Rudin--Shapiro",
  ]) {
    assert.ok(proof.includes(token.replaceAll(" ", "")), token);
  }
  assert.ok(proof.includes("completeautocorrelation"));
  assert.ok(proof.includes("V_m\\cdot\\nabla"));
});

test("the finite package checks exact formulas while denying PDE and complexity claims", () => {
  const base = "research/certificates/r073s";
  const certificate = json(`${base}/certificate.json`);
  const diagnostic = json(`${base}/diagnostic.json`);
  const independent = json(`${base}/independent_validation.json`);
  const manifest = json(`${base}/manifest.json`);
  assert.equal(certificate.schemaVersion, "r073s-quadratic-autocorrelation-certificate-v1");
  assert.equal(certificate.rowCount, 43);
  assert.equal(diagnostic.allChecksPass, true);
  assert.equal(independent.allChecksPass, true);
  assert.ok(diagnostic.checkCount >= 169);
  assert.ok(independent.checkCount >= 18);
  assert.equal(certificate.formulaStatements.quadraticCertificate,
    "||f||_6^6 <= A*Q, A=sum_h |C(h)|");
  assert.equal(certificate.claimBoundary.quadraticAutocorrelationUpperBoundChecked, true);
  for (const key of [
    "arithmeticComplexityLowerBound",
    "clayProblemSolved",
    "continuumPdeProofCertified",
    "globalRegularityEstablished",
    "heatFlowIntegralComputed",
    "navierStokesSimulation",
    "pdeNecessityEstablished",
    "runtimeBenchmark",
  ]) {
    assert.equal(certificate.claimBoundary[key], false, key);
  }

  const releaseManifest = json("research/release-manifest.json");
  if (manifest.finalSeal === true) {
    assert.equal(manifest.status, "sealed");
    assert.equal(manifest.sourceCommitAssigned, true);
    assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  } else {
    assert.notEqual(manifest.sourceCommitAssigned, true);
  }
  if (releaseManifest.latestCompletedRelease === "r073s") {
    assert.equal(manifest.finalSeal, true,
      "a materialized R0.73S route requires the immutable-source certificate seal");
  } else {
    assert.equal(releaseManifest.latestCompletedRelease, "r073r");
  }
});

test("the literature ledger records direct primary-source collisions", () => {
  const audit = read("research/r073s_primary_literature_audit.md");
  const readback = read("research/r073s_independent_literature_readback.md");
  for (const token of [
    "Nessel",
    "10.1017/S1446788700038878",
    "Edwards",
    "10.1017/S0004972700044427",
    "Høholdt",
    "10.1109/TIT.1985.1057071",
    "Doche",
    "10.1007/s00041-004-3049-y",
    "Rodgers",
    "10.1016/j.aim.2017.09.022",
  ]) {
    assert.ok((audit + readback).includes(token), token);
  }
  assert.ok(audit.includes("Theorem 1"));
  assert.ok(readback.includes("new quadratic autocorrelation theorem"));
  assert.ok(readback.includes("forbidden; classical direct consequence"));
});
