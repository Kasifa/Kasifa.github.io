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
  "research/r076c_full_frequency_fixed_mode_flux_payment.md": "2b2f4a2b353645e72ca54bfc06495a9f52329498b9c16a9e451ca7b3456f6bbf",
  "research/r076c_full_frequency_fixed_mode_flux_payment_primary_audit.md": "d60546eab80d2fa6ef633efeb0b34120d7b9f81a33249e500f8d94b9a8c15f74",
  "research/r076c_report-source.md": "be523d313f5a487fd0b1550cb948f1e05b117f6d1734b8d9cbfd5ab1b5d57b27",
  "scripts/r076c_full_frequency_fixed_mode_flux_payment_fixtures.json": "36d1612b57932fad7ff6e9a4375b842d4900b0868625cfb5d498ce89a4dcee82",
  "scripts/r076c_full_frequency_fixed_mode_flux_payment_expected.json": "6dbd56d366b6b048acd769ff5b5eff303ede111153330de763ec04cee571ad52",
  "scripts/r076c_full_frequency_fixed_mode_flux_payment_certificate.py": "cd336bbee4c0e0a31be3642522bdc4703b724ef5d5f21ca587a74d84e7897452",
  "scripts/r076c_full_frequency_fixed_mode_flux_payment_certificate_independent.rb": "4e26bc8b0c79222bbc3c5f4945a8c85fff9980bcf6ad5f607de48ace86293259",
  "scripts/r076c_full_frequency_fixed_mode_flux_payment_qa.sh": "55e0325e87df901aa4261971f204a8b2bcdd7f45a98ea358e73f47f3da8e166f",
  "research/r076c_full_frequency_fixed_mode_flux_payment_certificate.json": "0ffd5fff7812eb777866cff70eb0bff68112ae176ffd8706ea732ddda55b4a9b",
  "research/r076c_full_frequency_fixed_mode_flux_payment_certificate_report.md": "be4c0d24e4b98fd0ae7c26fd4fd0fb955dc7007f64bba2c49f517b71c17ba8f6",
  "research/r076c_full_frequency_fixed_mode_flux_payment_independent_audit.md": "a24ebbf47641c706dd756ce23ba65f5b68c59010bfa1e65f829ae97d7022c358",
  "research/r076c_full_frequency_fixed_mode_flux_payment_qa_report.md": "ccea7ec3ec37ed32c3746d11f67f8e3eee0a66089a53934dbac5fa0005f3dfc6",
};

test("R0.76C frozen ledger is byte-exact and both certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076c_full_frequency_fixed_mode_flux_payment_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(Object.keys(certificate.assertions).length, 15);
  assert.ok(Object.values(certificate.assertions).flatMap((group) => Object.values(group)).every((value) => value === true));
  assert.equal(certificate.negativeMutations.length, 140);
  assert.equal(certificate.computed.scaledCase.alpha, "48");
  assert.equal(certificate.computed.scaledCase.n1R, "2");
  assert.equal(certificate.computed.scaledCase.lambda, "4");
  assert.equal(certificate.computed.scaledCase.ultraHighBranch, true);
  assert.equal(certificate.computed.scaledCase.realPartsWithinMinusFourMinusOne, true);
  assert.equal(certificate.computed.spatialObservation.lengthRatio, "8");
  assert.equal(certificate.computed.temporalClock.weightedLambdaPower, "-1/3");
  assert.equal(certificate.computed.temporalClock.endpointLambdaPower, "0");
  assert.equal(certificate.computed.point.scaledPdeResidual, "0");
  assert.equal(certificate.computed.scaleLedger.frozenRate, "-2/11907");
  assert.match(read("research/r076c_full_frequency_fixed_mode_flux_payment_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r076c_full_frequency_fixed_mode_flux_payment_independent_audit.md"), /Ruby assertions: 140\/140/);
  assert.match(read("research/r076c_full_frequency_fixed_mode_flux_payment_qa_report.md"), /140\/140 Python; 140\/140 Ruby/);
});

test("R0.76C exact theorem quantifiers, exhaustive branches, and complete-square route are materialized", () => {
  const source = read("research/r076c_full_frequency_fixed_mode_flux_payment.md");
  const compact = source.split(/\s+/).join(" ");
  const tags = [...source.matchAll(/\\tag\{C\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 35 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 35);
  for (const marker of [
    "Fix an integer `q>=1`", "n_1,\\ldots,n_q\\in\\mathbb N", "\\phi_j\\in\\mathbb R",
    "all sufficiently large frozen `L`", "\\lambda=\\frac{\\alpha^2}{a^2}", "(n_1R)^2>1",
    "every `Q(.;z)` an exponential polynomial satisfying C.12", "T^{-2/3}K_T^{2/3}",
    "\\lambda^{-1/3}H^{2/3}", "complete real square", "before any absolute value",
    "no carrier upper bound", "not uniform for growing packets", "**NOT CLAY.**",
  ]) assert.ok(compact.includes(marker), marker);
  assert.equal(/(^|[^\\])qquad/.test(source), false, "corrected bare qquad must not reappear");
});

test("R0.76C reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-76c.html");
  for (const marker of [
    "R0.76C · STEP 54", "FIXED INTEGER Q", "INTEGER MODES", "REAL PHASES", "EXACT REAL DYADIC BAND",
    "ALL CARRIERS", "N_1 R &lt;= 1 · B", "N_1 R &gt; 1 · C", "C.14 POINTWISE FAMILY",
    "LAMBDA^(-1/3) WEIGHTED", "LAMBDA^0 TERMINAL", "COMPLETE REAL SQUARE",
    "C.1", "C.35", "140/140", "12/12", "NO FIGURE / NO DNS", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 425; section <= 432; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 500_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076c")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76C local translation and frozen certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r076c-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 46/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaReport = read("research/r076c_full_frequency_fixed_mode_flux_payment_qa_report.md");
  assert.match(qaReport, /Verdict: \*\*PASS\*\*/);
  assert.match(qaReport, /140\/140 Python; 140\/140 Ruby/);
});
