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
  "research/r075s_full_frequency_single_harmonic_clock_payment.md": "d2736eaa43443048bd620567c4acd72024dc4c662320a8aa58af31ccc6047ccd",
  "research/r075s_full_frequency_single_harmonic_clock_payment_primary_audit.md": "38e2bc95b5785b97df5d85474f3ed6105458a117249710b2c052cebbd769b5eb",
  "research/r075s_report-source.md": "ab9771e732204f28d3493ae9db73e7aa62aa980cc15b69dfefb39f226520b2a7",
  "scripts/r075s_full_frequency_single_harmonic_clock_payment_fixtures.json": "82874592703552c1639c69066ddbf1ab531c135cd92eeae775c20be66cd8260f",
  "scripts/r075s_full_frequency_single_harmonic_clock_payment_expected.json": "e806089d4649b73649edeed5c0204b81a42dbef79c758283b128ec49a57abd8b",
  "research/r075s_full_frequency_single_harmonic_clock_payment_certificate.json": "da70756ebf873bd9ac9d36cc676e059621cf63069ec8a8c8efc9d2ebe5473b6a",
  "research/r075s_full_frequency_single_harmonic_clock_payment_certificate_report.md": "6580726e22fa1b4af3ab3cfabdb3731b65674cb83479d7524124b456ab132987",
  "research/r075s_full_frequency_single_harmonic_clock_payment_independent_audit.md": "2ff691c30692d4742b10d5f28bda4b05f95691ecfd083941e638aef491911462",
  "research/r075s_full_frequency_single_harmonic_clock_payment_qa_report.md": "af318d1aacaa615cbf428631e0da61860668c5ee10c22e418e46df1c7e2e3378",
  "scripts/r075s_full_frequency_single_harmonic_clock_payment_certificate.py": "3a64a105f8cb01e20d2ec66ac4946beaf66dc726c05c0e9b72c2097fd0947243",
  "scripts/r075s_full_frequency_single_harmonic_clock_payment_certificate_independent.rb": "93cdcd359c7491a2bd8e48a8f092cad798efac050fd3e806e56f9a3cddbe696e",
  "scripts/r075s_full_frequency_single_harmonic_clock_payment_qa.sh": "b7d8629ea27dd7330784a43965387a8cdea03dc1b1468569260195a1cbcbcaaa",
};

test("R0.75S frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075s_full_frequency_single_harmonic_clock_payment_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions, 21);
  assert.equal(certificate.passed, 21);
  assert.equal(certificate.checks.length, 21);
  assert.match(read("research/r075s_full_frequency_single_harmonic_clock_payment_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075s_full_frequency_single_harmonic_clock_payment_qa_report.md"), /76\/76 Python; 76\/76 Ruby/);
});

test("R0.75S theorem boundary and complete-clock equation ledger are materialized", () => {
  const source = read("research/r075s_full_frequency_single_harmonic_clock_payment.md");
  for (let index = 1; index <= 41; index += 1) assert.ok(source.includes(`\\tag{S.${index}}`), `S.${index}`);
  for (const marker of [
    "T_R:=t_2-s_R=4R^2", "F_k(t,x_2)=Ae^{-k^2t}\\cos",
    "D_R(y):=", "=-2\\pi y\\vartheta(|y|/R-a)", "M_{k,R}^{\\rm plat}",
    "a^{2/3}R^{-1/3}", "\\mathfrak X_{k,R}", "-\\frac{c_\\gamma}{12}",
    "The constant and cosine rows vanish by oddness", "conditional", "not a multimode estimate",
    "No novelty or\npriority claim", "NOT\\ CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75S public reader is complete and forbidden future output is absent", () => {
  const note = read("public/notes/r0-75s.html");
  for (const marker of [
    "R0.75S · STEP 44", "POSITIVE THEOREM", "COMPLETE CLOCK", "ALL INTEGER FREQUENCIES",
    "ONE REAL HARMONIC", "EXACT SMOOTH SHEAR", "RADIAL REDUCTION", "MOVING-PHASE LEMMA",
    "LOW/HIGH COVERAGE", "AMPLITUDE CANCELS", "VERSION-M CONDITIONAL", "MULTIMODE OPEN",
    "S.1", "S.41", "76/76", "12/12",
    "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 440_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75s.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/assets/r075s")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75t.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75t.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075t")), false);
});

test("R0.75S local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075s-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 46/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075s_full_frequency_single_harmonic_clock_payment_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":76/);
});
