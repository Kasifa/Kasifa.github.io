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
  "research/r076d_quantitative_growing_mode_entropy_window.md": "cd94e3384f01963cb7b8a14fdb8376c6197c361473447f15500db0acac5e958e",
  "research/r076d_quantitative_growing_mode_entropy_window_primary_audit.md": "9b99247ceb34cadc12c7f4f0858be642316ca80d1ff83d05dfd745a9906356d8",
  "research/r076d_report-source.md": "f2358780d382dcace69b7ebef855bf3c8e63d15b581dc86b62b7e3c751fbd310",
  "scripts/r076d_quantitative_growing_mode_entropy_window_fixtures.json": "ffe5c2b9a1a6b0c20b710dc45fcac9543069ea6af38dce34804665012984b374",
  "scripts/r076d_quantitative_growing_mode_entropy_window_expected.json": "eb5dd9ebaa6a74cbc7f999fdbd55ee54a50588342c3dfba9412ac53c935ba2dd",
  "scripts/r076d_quantitative_growing_mode_entropy_window_certificate.py": "ed96f55b1326f1e7c1330670c132c523c7861f53edcb046b662159d83e60ce54",
  "scripts/r076d_quantitative_growing_mode_entropy_window_certificate_independent.rb": "9f12fa2aadc35dfb228e8f0ab60eec420c5c6bdfa306f1b66ca4828cdde4d391",
  "scripts/r076d_quantitative_growing_mode_entropy_window_qa.sh": "b69b5380ffd60ad713c3971311cf6197bc5254a44abbb8e65f3d19990ec5e592",
  "research/r076d_quantitative_growing_mode_entropy_window_certificate.json": "e57d160e8b3b37ed714e884750f50abbaaaac25a1e3ec3ba395a0193e0b6757d",
  "research/r076d_quantitative_growing_mode_entropy_window_certificate_report.md": "460917d50cd9aeeb4af5898322915d67fa8ec3e1971f2e5945becf858ccd9c94",
  "research/r076d_quantitative_growing_mode_entropy_window_independent_audit.md": "0d6e3b7f363fdb9e031a228038ae7af4152d51d101e6050f39c4de7dc21fa69a",
  "research/r076d_quantitative_growing_mode_entropy_window_qa_report.md": "e0313b591dee896aae87930dfd01cfa2c6cd3f1e7a82875b439ba0399402fab6",
};

test("R0.76D frozen ledger is byte-exact and both certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076d_quantitative_growing_mode_entropy_window_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionsPassed, 123);
  assert.equal(certificate.assertionsTotal, 123);
  assert.equal(certificate.negativeMutations.length, 123);
  assert.equal(certificate.exact.heatTail.factorialOverFour, 9_979_200);
  assert.equal(certificate.exact.heatTail.m, 10);
  assert.equal(certificate.exact.spatialObservation.maximumOriginalFrequency, "96");
  assert.equal(certificate.exact.spatialObservation.maximumRescaledFrequency, "48");
  assert.equal(certificate.exact.energy.gradientCoefficient, "257/64");
  assert.equal(certificate.exact.energy.weightedLambdaPower, "-1/3");
  assert.equal(certificate.exact.energy.endpointLambdaPower, "0");
  assert.equal(certificate.exact.scaleLedger.frozenRate, "-2/11907");
  assert.match(read("research/r076d_quantitative_growing_mode_entropy_window_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r076d_quantitative_growing_mode_entropy_window_independent_audit.md"), /Ruby assertions: 123\/123/);
  assert.match(read("research/r076d_quantitative_growing_mode_entropy_window_qa_report.md"), /123\/123 Python; 123\/123 Ruby/);
});

test("R0.76D theorem retains every quantitative loss and claim boundary", () => {
  const source = read("research/r076d_quantitative_growing_mode_entropy_window.md");
  const compact = source.split(/\s+/).join(" ");
  const tags = [...source.matchAll(/\\tag\{D\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 41 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 41);
  for (const marker of [
    "Let `q>=1` be an integer", "n_1,\\ldots,n_q\\in\\mathbb N", "\\phi_j\\in\\mathbb R",
    "\\exp\\!\\bigl(C_*q\\log(q+1)\\bigr)", "q(L)\\log(q(L)+1)=o(L^2)",
    "(\\alpha+q)^{-1}\\|g'\\|_{L^\\infty(J)}", "\\left(\\frac54\\right)^m",
    "\\frac{(m+1)!}{4}", "\\lambda^{-1/3}H^{2/3}", "complete real square",
    "every `Q(.;z)` satisfying D.20", "not a uniform-in-`q` estimate", "**NOT CLAY.**",
  ]) assert.ok(compact.includes(marker), marker);
});

test("R0.76D reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-76d.html");
  for (const marker of [
    "R0.76D · STEP 55", "EXP(C Q LOG(Q+1))", "GROWING-MODE WINDOW", "ALPHA+Q DERIVATIVE",
    "(5/4)^M ENDPOINT", "B!=0 VERSION-M CONDITIONAL", "D.1", "D.41", "123/123",
    "12/12", "NO FIGURE / NO DNS", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 433; section <= 441; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 500_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076d")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76D local translation and frozen certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r076d-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 56/);
  assert.match(translationOutput, /"dgxUsed": false/);
  assert.match(read("research/r076d_quantitative_growing_mode_entropy_window_qa_report.md"), /Verdict: \*\*PASS\*\*[\s\S]*123\/123 Python; 123\/123 Ruby/);
});
