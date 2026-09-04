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
  "research/r075x_fixed_finite_mode_low_carrier_payment.md": "8e0c412528578c15d807b33b64f0996e62a2dabe2ebd58fa297f67c093929763",
  "research/r075x_fixed_finite_mode_low_carrier_payment_primary_audit.md": "8fffbf0c8ad50d5765c734f8e5627ce0dbe0d6b2aad4bcb26aa5c298f6143b2c",
  "research/r075x_report-source.md": "8fa756c7efe2660dbc5eeb51e2a11d10dce58f36f4c0d0f757000be1447b7f34",
  "scripts/r075x_fixed_finite_mode_low_carrier_payment_fixtures.json": "de231e977d9a2551222f0a4f0a8ebcb65490f76574bc4fa494db480e2b61a0e9",
  "scripts/r075x_fixed_finite_mode_low_carrier_payment_expected.json": "879ff3458050e712048654eb91623a00e5436a22f12c6b814fb137aa8af96311",
  "scripts/r075x_fixed_finite_mode_low_carrier_payment_certificate.py": "926dbcd704645d61392349437b10049c33b7ad8d77703e462ac3c784510190b4",
  "scripts/r075x_fixed_finite_mode_low_carrier_payment_certificate_independent.rb": "521d2026b6f27c466087b51663f7d3ca46bf9e84c3f51378fc403e05833b5ca1",
  "scripts/r075x_fixed_finite_mode_low_carrier_payment_qa.sh": "a94b5c96e600cdd9ea5c9ad8975bad5003058c067de079c495d27df7fcab7d7f",
  "research/r075x_fixed_finite_mode_low_carrier_payment_certificate.json": "717ce6ba1dcf4db39015db85c450bb1e2b7b31ff89e6b42ffb2bc30f31e3af05",
  "research/r075x_fixed_finite_mode_low_carrier_payment_certificate_report.md": "8725b6d6db67640fe20f1708d0942d994b174eaab0527828a0e0653aeb1c3701",
  "research/r075x_fixed_finite_mode_low_carrier_payment_independent_audit.md": "a1075d0ef321805a5d5d77be465820c85bd4ef820545531d983bab93094debf1",
  "research/r075x_fixed_finite_mode_low_carrier_payment_qa_report.md": "a35de008fb5195331153ed8fddfc5ba1bd064d19e423f2309bf44685cc05f183",
};

test("R0.75X frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075x_fixed_finite_mode_low_carrier_payment_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionCount, 18);
  assert.equal(certificate.assertions.length, 18);
  assert.ok(certificate.assertions.every((row) => row.pass === true));
  assert.equal(certificate.spatialOde.q, 3);
  assert.equal(certificate.spatialOde.order, 6);
  assert.equal(certificate.temporalTrace.maximumTerms, 6);
  assert.equal(certificate.transportIdentity.heatCancellation, "0");
  assert.match(read("research/r075x_fixed_finite_mode_low_carrier_payment_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075x_fixed_finite_mode_low_carrier_payment_independent_audit.md"), /Assertions: 19\/19/);
  assert.match(read("research/r075x_fixed_finite_mode_low_carrier_payment_qa_report.md"), /90\/90 Python; 90\/90 Ruby/);
});

test("R0.75X fixed-finite low-carrier boundary and equation ledger are materialized", () => {
  const source = read("research/r075x_fixed_finite_mode_low_carrier_payment.md");
  const tags = [...source.matchAll(/\\tag\{X\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 36 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 36);
  for (const marker of [
    "q>=1", "1\\le n_1<n_2<\\cdots<n_q\\le2n_1", "n_1aR<C_0", "\\tag{X.5}", "\\tag{X.15}",
    "\\tag{X.21}", "\\tag{X.26}", "\\tag{X.34}", "\\tag{X.36}", "-2/11907",
    "It never divides by `v`, an amplitude, a frequency, or a frequency gap",
    "No uniform control of `C_q` as `q` grows is proved", "high-carrier sector for three or more modes",
    "**NOT CLAY.**",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75X reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-75x.html");
  for (const marker of [
    "R0.75X · STEP 49", "FIXED FINITE q", "LOW CARRIER ONLY", "ONE DYADIC BAND",
    "2q-STATE CONFLUENT ODE", "2q-TERM TRACE", "NO GAP DIVISOR", "NO V DIVISION",
    "R POWERS CANCEL", "EXACT RATE -2/11907", "NO UNIFORM q GROWTH", "HIGH CARRIER 3+ OPEN",
    "VERSION-M CONDITIONAL", "X.1", "X.36", "18/18", "19/19", "90/90", "12/12",
    "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 384; section <= 392; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 500_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r075x")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
  assert.equal(existsSync(resolve(root, "public/notes/r0-75y.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75y.pdf")), false);
});

test("R0.75X local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075x-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 54/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075x_fixed_finite_mode_low_carrier_payment_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":90/);
});
