import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");
const frozen = {
  "research/r076k_real_dyadic_edge_sharpness.md": "e293a3aa3e9c1dde443ed7a8c07afd2c709d3855d8b469b38033b04d71116bf2",
  "research/r076k_real_dyadic_edge_sharpness_primary_audit.md": "36a26cb421a108127b516e47a0008625d67ec43a1d009a14bef9d7684ef03671",
  "research/r076k_report-source.md": "21dbd71aae07ecbe910d4bcefbf6e1caccc3cddc41171a57ffd239c6eed34f3e",
  "scripts/r076k_real_dyadic_edge_sharpness_fixtures.json": "16acf468a6722ee1e66e36a855fdd1e84e56bdc3519e6e2326d6bec0a3b82518",
  "scripts/r076k_real_dyadic_edge_sharpness_expected.json": "8f32d96856fdf5d0a86030737f5bf049b227f976661089ed6d31d4a41a1c5b50",
  "scripts/r076k_real_dyadic_edge_sharpness_certificate.py": "c05ab480973a418e69cb40984b1da5c7210c5e4916e2fa1d6fb6281a9b53d1d9",
  "scripts/r076k_real_dyadic_edge_sharpness_certificate_independent.rb": "893b0b5e18e3a3fca06ef10e7879e361894dafbb845d09264373e92f116210bb",
  "scripts/r076k_real_dyadic_edge_sharpness_qa.sh": "5968f4b6a08d982c4345165e7fc0bc04c33dca66ab7cf8c1dba0be30a5212a79",
  "research/r076k_real_dyadic_edge_sharpness_certificate.json": "4d5247ca82869758c01a398f9a4858bfce87e3bd7ab3ad2a37eac0e6bdea7f1d",
  "research/r076k_real_dyadic_edge_sharpness_certificate_report.md": "43131539e1fd4105fe0215739003b7819379e87d44ddab4aa772a40bcc47daaa",
  "research/r076k_real_dyadic_edge_sharpness_independent_audit.md": "7d87a4b543051e08cc6a348c5b7f261cd433fdf8efba4986ed01514c13c78b1a",
  "research/r076k_real_dyadic_edge_sharpness_qa_report.md": "b888919d4f1992c22e5206d6350983dbd89885df29bb62b3408b581298c511ec",
};

test("R0.76K frozen ledger and finite certificates are exact", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076k_real_dyadic_edge_sharpness_certificate.json"));
  assert.equal(certificate.status, "PASS");
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionsPassed, 118);
  assert.equal(certificate.assertionsTotal, 118);
  assert.equal(certificate.negativeMutations.length, 118);
  assert.deepEqual(certificate.exact.structure, { displayCount: 48, firstTag: 1, lastTag: 48, tagCount: 48 });
  assert.equal(certificate.exact.asymptoticSample.provedWindowExponent, "2");
  assert.equal(certificate.exact.asymptoticSample.upperWindowExponent, "5/2");
  assert.equal(certificate.exact.pointwiseSample.theoremSquaredPrefactor, "1/8");
  assert.equal(certificate.exact.claims.realDyadicSharpness, true);
  assert.equal(certificate.exact.claims.exactIntegerSingleSlice, true);
  assert.equal(certificate.exact.claims.completeFluxLowerBound, false);
  assert.equal(certificate.exact.claims.l3EndpointOptimality, false);
  assert.match(read("research/r076k_real_dyadic_edge_sharpness_primary_audit.md"), /PASS -- single-slice theorem only; complete-clock flux remains open/);
  assert.match(read("research/r076k_real_dyadic_edge_sharpness_independent_audit.md"), /Ruby assertions: 168\/168/);
});

test("R0.76K single-slice theorem and open complete-clock boundary are explicit", () => {
  const source = read("research/r076k_real_dyadic_edge_sharpness.md");
  const tags = [...source.matchAll(/\\tag\{K\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 48 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 48);
  for (const marker of ["real one-dyadic-band class", "q(L)=o(L^2)", "q=o(L^(5/2))", "complete signed collar flux", "L3", "NOT CLAY"]) assert.ok(source.includes(marker), marker);
  assert.match(source, /signed\s+single-slice algebra only/);
  const note = read("public/notes/r0-76k.html");
  for (const marker of ["R0.76K · STEP 62", "REAL ONE DYADIC BAND", "EXACT HEAT-SHEAR SLICE", "q=o(L²)", "K.1", "K.48", "118/118", "168/168", "12/12", "FIXED SINGLE SLICE ONLY", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  for (let section = 489; section <= 496; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076k")), false);
  assert.equal(note.includes("R0.76L"), false);
});

test("R0.76K translations and frozen certificate QA are deterministic", () => {
  const output = execFileSync(process.execPath, ["scripts/add-r076k-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 61/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(read("research/r076k_real_dyadic_edge_sharpness_qa_report.md"), /Verdict: \*\*PASS\*\*[\s\S]*Ruby assertions: 168\/168/);
});
