import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const node = process.execPath;
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

const frozen = {
  "research/r075n_radial_collar_averaged_wiener_row.md": "ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318",
  "research/r075n_radial_collar_averaged_wiener_row_primary_audit.md": "c43c063b1c003be22782e7d8e1ce0b3f42cdd3ef4d01912c9de34c876d8c9aba",
  "research/r075n_report-source.md": "ae9d5d630ee0549193c016fcbc07c599b0c678fbaf9c15c5d3c7f24bdf18e27c",
  "scripts/r075n_radial_collar_averaged_wiener_row_fixtures.json": "2dee2146f94f3fa6d0d0c5828d8d6f354f0856f620e1261a133c9a2c81f8a0cb",
  "scripts/r075n_radial_collar_averaged_wiener_row_expected.json": "31614fc11bc4355723fff7773bec8ab13bc44808ffffa0958c78ec1cfe2bba48",
  "research/r075n_radial_collar_averaged_wiener_row_certificate.json": "891774ec5c7e747a4f9c172f0b71e4f6f2af40d8a983bc7c69ebbd1756f405d7",
  "research/r075n_radial_collar_averaged_wiener_row_certificate_report.md": "cad991130fb614d923c224a891001010119a746f9d32c1d17d0fbc5f6c56c0b5",
  "research/r075n_radial_collar_averaged_wiener_row_independent_audit.md": "779d359b62c2860a07e8889826d038d88cad8356af9c53ce31f5bfd1d85441b6",
  "research/r075n_radial_collar_averaged_wiener_row_qa_report.md": "d45d0eef91dab59db773940e2b47caea282781671e186709d7c58f0111c4c4ef",
  "scripts/r075n_radial_collar_averaged_wiener_row_certificate.py": "47256d34a25a188a32147e4cb9f0388819238f2c854e1e814612b9bfd217950e",
  "scripts/r075n_radial_collar_averaged_wiener_row_certificate_independent.rb": "63836294b2924433afa0e95d07baee6427446c7c26c14a34dcd9a5818e0fed56",
  "scripts/r075n_radial_collar_averaged_wiener_row_qa.sh": "568b7934a403e076fb51ae0f18b142547f621a1a514c6ced14e01635c540c66e",
};

test("R0.75N frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075n_radial_collar_averaged_wiener_row_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions.total, 16);
  assert.equal(certificate.assertions.passed, 16);
  assert.equal(Object.keys(certificate.checks).length, 16);
  assert.match(read("research/r075n_radial_collar_averaged_wiener_row_primary_audit.md"), /Verdict: PASS\. Mathematical blocker count: 0\. Release blocker count: 0\./);
  assert.match(read("research/r075n_radial_collar_averaged_wiener_row_qa_report.md"), /107\/107 Python; 107\/107 Ruby/);
});

test("R0.75N theorem boundary, equation ledger, and averaged rows are materialized", () => {
  const source = read("research/r075n_radial_collar_averaged_wiener_row.md");
  for (let index = 1; index <= 17; index += 1) assert.ok(source.includes(`\\tag{N.${index}}`), `N.${index}`);
  for (const marker of [
    "canonical representative", "supremum is taken separately", "two integrations by parts", "4\\pi a\\delta",
    "C_\\vartheta L", "C_\\vartheta L^2R", "K>=R^(-3/2)", "inter-packet", "No novelty", "priority", "NOT\\ CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75N public reader is complete and forbidden future output is absent", () => {
  const note = read("public/notes/r0-75n.html");
  for (const marker of [
    "R0.75N · STEP 39", "CANONICAL RADIAL COLLAR", "SELECTABLE CUTOFF", "X1-AVERAGED ROW",
    "SUM-SUP ORDER", "D0 = 0", "NO R^-1 LOSS", "WIENER ROW O(L)", "FULL AVERAGE O(L^2 R)",
    "N.1", "N.17", "107/107", "12/12", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 400_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75n.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/notes/r0-75o.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75o.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075n")), false);
});

test("R0.75N local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075n-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 48/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075n_radial_collar_averaged_wiener_row_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":107/);
});
