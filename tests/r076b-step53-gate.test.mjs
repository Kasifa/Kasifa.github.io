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
  "research/r076b_moderate_carrier_fixed_mode_flux_payment.md": "a8a4cc853ec1029cb52afee724a4a783da156bd57de5399c58a7f42e2ab0306d",
  "research/r076b_moderate_carrier_fixed_mode_flux_payment_primary_audit.md": "0a6314c454021da284bbf157de36d6c2bd1683d600a21c8394f723acc26aa447",
  "research/r076b_report-source.md": "362fcf898a533efaf4072c876dba09f4231c131ad1c48d48efc92c52215428fc",
  "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_fixtures.json": "1f9b3df9cb8ff3f9d22250ce425b837d40268829bf18cb3e12b3f7d2dca64bf2",
  "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_expected.json": "4533edf290e07f1fddc5df1b9ef1655a5623f4a3714e840b1c402cdf3b8db3f1",
  "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_certificate.py": "b4ec0ba8fbbe9033dcec3254a1acc3a4f7e662fe320c4697f253f575aa98863a",
  "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_certificate_independent.rb": "0b53934fc132eda0c51a5885d8b50089b74897aeaff1373e1033bc825c43e849",
  "scripts/r076b_moderate_carrier_fixed_mode_flux_payment_qa.sh": "dd4d802ce353c9698323cc2ad600df35794cce4796cf9457a63786165be47756",
  "research/r076b_moderate_carrier_fixed_mode_flux_payment_certificate.json": "d825624473f176c054134a75a47cb63fee65f7fe3bfe946ae505522a9c3c053e",
  "research/r076b_moderate_carrier_fixed_mode_flux_payment_certificate_report.md": "5ae840453141f3059b94459996f7aaf808766fe3367ea433251343de128f938e",
  "research/r076b_moderate_carrier_fixed_mode_flux_payment_independent_audit.md": "1962313e8898dd6cdbafa9f1b543712d3660c25521c039e5311b21629bb1f6bf",
  "research/r076b_moderate_carrier_fixed_mode_flux_payment_qa_report.md": "7ec49c58e8eb209af2e836155b0126f8257e61b89f8742d04331ae31dc628f6d",
};

test("R0.76B frozen ledger is byte-exact and both certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076b_moderate_carrier_fixed_mode_flux_payment_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions.length, 15);
  assert.ok(certificate.assertions.every((row) => row.pass === true));
  assert.equal(certificate.negativeMutations.length, 123);
  assert.deepEqual(certificate.computed.scaledCase.alphas, ["24", "289/12", "145/6"]);
  assert.equal(certificate.computed.scaledCase.highBranch, true);
  assert.equal(certificate.computed.scaledCase.inverseRadiusEndpoint, true);
  assert.equal(certificate.computed.scaledCase.realPartsWithinFour, true);
  assert.equal(certificate.computed.spatialObservation.lengthRatio, "8");
  assert.equal(certificate.computed.temporalTrace.realPartBound, "4");
  assert.equal(certificate.computed.point.scaledPdeResidual, "0");
  assert.equal(certificate.computed.scaleLedger.frozenRate, "-2/11907");
  assert.match(read("research/r076b_moderate_carrier_fixed_mode_flux_payment_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r076b_moderate_carrier_fixed_mode_flux_payment_independent_audit.md"), /Assertions: 15\/15/);
  assert.match(read("research/r076b_moderate_carrier_fixed_mode_flux_payment_qa_report.md"), /123\/123 Python; 123\/123 Ruby/);
});

test("R0.76B exact theorem quantifiers, exhaustive branches, and complete-square route are materialized", () => {
  const source = read("research/r076b_moderate_carrier_fixed_mode_flux_payment.md");
  const compact = source.split(/\s+/).join(" ");
  const tags = [...source.matchAll(/\\tag\{B\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 41 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 41);
  for (const marker of [
    "Fix an integer `q>=1`", "n_1,\\ldots,n_q\\in\\mathbb N", "\\phi_j\\in\\mathbb R",
    "all sufficiently large frozen `L`", "n_1R\\le1", "8q\\le\\alpha\\le a",
    "Together with R0.75X for `alpha<8q`", "complete square `G^2`", "before absolute values",
    "no spectral separation", "n_1R>1", "not give a constant uniform in growing `q`", "**NOT CLAY.**",
  ]) assert.ok(compact.includes(marker), marker);
  assert.equal(/(^|[^\\])qquad/.test(source), false, "corrected bare qquad must not reappear");
});

test("R0.76B reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-76b.html");
  for (const marker of [
    "R0.76B · STEP 53", "FIXED INTEGER Q", "INTEGER MODES", "REAL PHASES", "EXACT REAL DYADIC BAND",
    "N_1 R &lt;= 1", "ALPHA &lt; 8Q · X", "8Q &lt;= ALPHA &lt;= A · B", "COMPLETE REAL SQUARE",
    "ALL SELF / CROSS TERMS", "NO LOCALIZED-CURRENT SIGN", "Q-GROWTH OPEN", "N_1 R &gt; 1 OPEN",
    "B.1", "B.41", "15/15", "123/123", "12/12", "NO FIGURE / NO DNS", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 416; section <= 424; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 500_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076b")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76B local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r076b-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 47/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r076b_moderate_carrier_fixed_mode_flux_payment_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":123/);
});
