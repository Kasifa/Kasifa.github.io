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
  "research/r075w_full_frequency_two_harmonic_flux_payment.md": "571b8152e3e5f81becec4dd691488fb5889fac23e94ca7c99bd546399dc320d4",
  "research/r075w_full_frequency_two_harmonic_flux_payment_primary_audit.md": "78255a0d84020d1d1c9dc6509ed1cc8eb9a9fdaced21d93e4f586383e4fc9ea0",
  "research/r075w_report-source.md": "461ab29f02072eb039c9b57c497a87d04ff95255af68d561c68f4d3224726d7a",
  "scripts/r075w_full_frequency_two_harmonic_flux_payment_fixtures.json": "2b59973a6901b0a70068a2952e1324fd1780f853508c250821daaab659aa8b1f",
  "scripts/r075w_full_frequency_two_harmonic_flux_payment_expected.json": "44afc8aebea8e15a4d54adf28fd48f8da28dd61c74e6f87a9ded21667d61867f",
  "scripts/r075w_full_frequency_two_harmonic_flux_payment_certificate.py": "7d517b429fa0d08f5f2fc61597eb926b12d72fe5543444ea9e4a49094d89a29f",
  "scripts/r075w_full_frequency_two_harmonic_flux_payment_certificate_independent.rb": "3ecd32cb10eb29f84220fd0110556071bc9637ef06457577291931173bc1e9c4",
  "scripts/r075w_full_frequency_two_harmonic_flux_payment_qa.sh": "3090e129431c03f43fd7aa518d9abe0f6ce74af3e97f50b2c19c65497d1d711a",
  "research/r075w_full_frequency_two_harmonic_flux_payment_certificate.json": "cd18eca477eb0938703446c6ab9939b4bccaf1f3465e450dfa35cdee758b76c8",
  "research/r075w_full_frequency_two_harmonic_flux_payment_certificate_report.md": "5b5fc6efb2de3e5817c7299cf2b71b3df15eca8caf393e8ccbc85a4796d08284",
  "research/r075w_full_frequency_two_harmonic_flux_payment_independent_audit.md": "0e7462c2912bb4be6c63198692014d753d9f57bced48e65543c53e25193315aa",
  "research/r075w_full_frequency_two_harmonic_flux_payment_qa_report.md": "2a6f0b9171b2e1511519510d732c6c4c032fd877e4aa44be480bdc54d799793b",
};

test("R0.75W frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075w_full_frequency_two_harmonic_flux_payment_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionCount, 18);
  assert.equal(certificate.assertions.length, 18);
  assert.ok(certificate.assertions.every((row) => row.pass === true));
  assert.match(read("research/r075w_full_frequency_two_harmonic_flux_payment_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075w_full_frequency_two_harmonic_flux_payment_independent_audit.md"), /Assertions: 19\/19/);
  assert.match(read("research/r075w_full_frequency_two_harmonic_flux_payment_qa_report.md"), /89\/89 Python; 89\/89 Ruby/);
});

test("R0.75W full-frequency exact-pair boundary and equation ledger are materialized", () => {
  const source = read("research/r075w_full_frequency_two_harmonic_flux_payment.md");
  const tags = [...source.matchAll(/\\tag\{W\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 33 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 34);
  for (const marker of [
    "A,C>=0", "1<=m<k<=2m", "maR<C_0", "maR>=C_0", "\\tag{W.2}", "\\tag{W.4}",
    "\\tag{W.12}", "\\tag{W.17}", "\\tag{W.25}", "\\tag{W.31}", "\\tag{W.33}",
    "A sin(2my)-2A sin(my)", "No division by `v`, `alpha-beta`, or either frequency occurs",
    "lower or upper carrier-frequency restriction in W.2", "-2/11907",
    "three or more harmonics", "**NOT CLAY.**",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75W reader and milestone recap are complete while X output is absent", () => {
  const note = read("public/notes/r0-75w.html");
  const recap = read("public/recap-r0-61-r0-75w.html");
  for (const marker of [
    "R0.75W · STEP 48", "LOW CARRIER PAID", "HIGH / LOW UNION", "FULL FREQUENCY",
    "EXACTLY TWO HARMONICS", "ONE DYADIC PAIR", "CONFLUENT ODE", "TURAN–NAZAROV TRACE",
    "LOCAL ENERGY IDENTITY", "NO GAP DIVISOR", "NO V DIVISION", "R POWERS CANCEL",
    "EXACT RATE -2/11907", "VERSION-M CONDITIONAL", "3+ MODES OPEN", "W.1", "W.33",
    "89/89", "12/12", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 374; section <= 383; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  for (const marker of ["CUMULATIVE MILESTONE RECAP · 191 NODES", "T · high-carrier spatial coercivity", "U · high-carrier difference row", "V · high-carrier self/sum block", "W · low-carrier local energy", "NODE INDEX / 191", "NOT CLAY"]) assert.ok(recap.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 500_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal((recap.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r075w")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75x.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75x.pdf")), false);
});

test("R0.75W local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075w-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 81/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075w_full_frequency_two_harmonic_flux_payment_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":89/);
});
