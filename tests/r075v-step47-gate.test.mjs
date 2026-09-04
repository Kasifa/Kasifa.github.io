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
  "research/r075v_complete_two_harmonic_flux_payment.md": "6917ff77099b6271b005ca90335df589434a38b0a57001893dcae8b02fd34824",
  "research/r075v_complete_two_harmonic_flux_payment_primary_audit.md": "cf23652951c5e1721270577c9a32bc476142b439aefa8ee5f62112cfd8bf5cbd",
  "research/r075v_report-source.md": "a099949ad6968468389b412e1d250c5e1a788ac046b949d4d69fbcf1501e9811",
  "scripts/r075v_complete_two_harmonic_flux_payment_fixtures.json": "d2a16f6e718931aebca696d4934fa497be6bceef8c4e301a9851d04d11e622bc",
  "scripts/r075v_complete_two_harmonic_flux_payment_expected.json": "ebe2cd2b8aad095730eca4b59e5b79e630a28a0f0215fd2cec0024a4593386c6",
  "scripts/r075v_complete_two_harmonic_flux_payment_certificate.py": "c224095be7795a0236575ecc69143e525f652fcfc45236f51751ac25ee68b0d2",
  "scripts/r075v_complete_two_harmonic_flux_payment_certificate_independent.rb": "d12e36c8aa30cf39a8184a401e929d42a843aa5a0bdeb4f374543cfd3c88dc92",
  "scripts/r075v_complete_two_harmonic_flux_payment_qa.sh": "9683be163d5a933f77ae092544341f2b7d91993cd6f50137483edeb9b42eeeb1",
  "research/r075v_complete_two_harmonic_flux_payment_certificate.json": "daa3649b42363368d9db1139a9168d46a7ec44df591e696ea36011288f5a1da5",
  "research/r075v_complete_two_harmonic_flux_payment_certificate_report.md": "9618e0a14bfc36a184381e448e17a59238ad8a02d10c22a8fb7be3546e723c7a",
  "research/r075v_complete_two_harmonic_flux_payment_independent_audit.md": "0c8ab0c24a201b53cc9bfd9eaa0c38848e5978ca47ce915493601cf4199aa9da",
  "research/r075v_complete_two_harmonic_flux_payment_qa_report.md": "d5c877711b59c6a29b11f821710bc7d04ec34a5a7d48d782695abfba566c1a30",
};

test("R0.75V frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075v_complete_two_harmonic_flux_payment_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionCount, 17);
  assert.equal(certificate.assertions.length, 17);
  assert.ok(certificate.assertions.every((row) => row.pass === true));
  assert.match(read("research/r075v_complete_two_harmonic_flux_payment_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075v_complete_two_harmonic_flux_payment_independent_audit.md"), /Assertions: 18\/18/);
  assert.match(read("research/r075v_complete_two_harmonic_flux_payment_qa_report.md"), /84\/84 Python; 84\/84 Ruby/);
});

test("R0.75V exact-pair theorem boundary and equation ledger are materialized", () => {
  const source = read("research/r075v_complete_two_harmonic_flux_payment.md");
  const tags = [...source.matchAll(/\\tag\{V\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 43 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 43);
  for (const marker of [
    "A,C>=0", "1<=m<k<=2m", "d=k-m", "maR>=C_0", "\\tag{V.3}", "\\tag{V.4}",
    "\\tag{V.13}", "\\tag{V.21}", "\\tag{V.27}", "\\tag{V.31}", "\\tag{V.43}",
    "Bounding those rows separately destroys", "If `xy=0`", "All powers of `R` cancel",
    "complete flux theorem only for the exact high-carrier dyadic pair", "three or more harmonics", "**NOT CLAY.**",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75V reader and milestone recap are complete while later output is absent", () => {
  const note = read("public/notes/r0-75v.html");
  const recap = read("public/recap-r0-61-r0-75v.html");
  for (const marker of [
    "R0.75V · STEP 47", "SELF + SUM BLOCK PAID", "JOINT CANCELLATION RETAINED",
    "EXACTLY TWO HARMONICS", "ONE DYADIC PAIR", "HIGH CARRIER", "COMPLETE CLOCK",
    "FULL EXACT-PAIR FLUX", "MULTIPLIER TWO-JET", "RIGHT-ENDPOINT TRACE",
    "R POWERS CANCEL", "EXACT RATE -2/11907", "VERSION-M CONDITIONAL", "MULTIMODE OPEN",
    "V.1", "V.43", "84/84", "12/12", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 364; section <= 373; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  for (const marker of ["CUMULATIVE MILESTONE RECAP · 190 NODES", "T · spatial coercivity", "U · difference-frequency payment", "V · coupled self/sum payment", "NODE INDEX / 190", "NOT CLAY"]) assert.ok(recap.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 500_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal((recap.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r075v")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75w.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75w.pdf")), false);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
});

test("R0.75V local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075v-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 115/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075v_complete_two_harmonic_flux_payment_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":84/);
});
