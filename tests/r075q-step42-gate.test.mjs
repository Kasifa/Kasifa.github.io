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
  "research/r075q_spatially_spread_harmonic_collar_payment.md": "9d7058fd7fbc61136967227507e47b0e866c7a4eeafebae198ab05a23645ed9c",
  "research/r075q_spatially_spread_harmonic_collar_payment_primary_audit.md": "92255869e165efdbe72557187dd1fe6e7e4449264dcf8033b285286d50f725be",
  "research/r075q_report-source.md": "b1fcfece0396b04ae9f59e42ef09957a422c36fa0843730a9fb22919bc24c600",
  "scripts/r075q_spatially_spread_harmonic_collar_payment_fixtures.json": "a0954f102de2fbc5ac5fb57fd68ba2ae084cc27743240fac6e3297b81d4410f5",
  "scripts/r075q_spatially_spread_harmonic_collar_payment_expected.json": "8f3e45bb4a62e2a5bd506fd3cc522610d59115f34411fd85b04c7b72081cb444",
  "research/r075q_spatially_spread_harmonic_collar_payment_certificate.json": "fc53a51af160befea1ffc146256aba31792cd4bd3de36004ff851f3b57d7cc12",
  "research/r075q_spatially_spread_harmonic_collar_payment_certificate_report.md": "b5f8fdd24f7bf4911eadf1fe6fb1aa25ac255dcd0bd7a36dcc239d2e023b591d",
  "research/r075q_spatially_spread_harmonic_collar_payment_independent_audit.md": "932d1ef7e14701a08584c926a68951e878a2e3f1a74e03a4a22a8a590faa6c8f",
  "research/r075q_spatially_spread_harmonic_collar_payment_qa_report.md": "356796d82e9857ef94642871509dfcacf2c699c4e683fe00ed2cd946a6fdc6b6",
  "scripts/r075q_spatially_spread_harmonic_collar_payment_certificate.py": "e9a2758fd7688be5bd5970c28385ef501a1716095c1d673fb81071989e0fe09e",
  "scripts/r075q_spatially_spread_harmonic_collar_payment_certificate_independent.rb": "4d0a81b580bba7061faefe98777d5ad55330d3b60f6563774e73ec8da9a17bbd",
  "scripts/r075q_spatially_spread_harmonic_collar_payment_qa.sh": "f34eee300896e19372983f027a4a52821872f9f63df2df0fa5236d888f5b9ddc",
};

test("R0.75Q frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075q_spatially_spread_harmonic_collar_payment_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions, 20);
  assert.equal(certificate.passed, 20);
  assert.equal(Object.keys(certificate.checks).length, 20);
  assert.match(read("research/r075q_spatially_spread_harmonic_collar_payment_primary_audit.md"), /Verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075q_spatially_spread_harmonic_collar_payment_qa_report.md"), /180\/180 Python; 180\/180 Ruby/);
});

test("R0.75Q theorem boundary, equation ledger, and collar-payment rows are materialized", () => {
  const source = read("research/r075q_spatially_spread_harmonic_collar_payment.md");
  for (let index = 1; index <= 28; index += 1) assert.ok(source.includes(`\\tag{Q.${index}}`), `Q.${index}`);
  for (const marker of [
    "F_k(t,x_2)=A e^{-k^2t}\\cos(k(x_2-Bt))", "V_{\\xi,3}",
    "\\frac{A^2|B|V_{\\xi,3}}{8k^2}", "c_{\\rm box}:=\\frac{2(1-e^{-3})}{9\\pi}",
    "\\frac{4279}{238140000}", "p_{k,\\rm col}\\le C P_R^M", "not asserted for a harmonic projection",
    "\\frac{E_{\\rm in}}{E_0}\\le\\frac{a^2R^2}{2\\pi}", "two or more horizontal harmonics",
    "No novelty or priority claim", "NOT\\ CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75Q public reader is complete and forbidden future output is absent", () => {
  const note = read("public/notes/r0-75q.html");
  for (const marker of [
    "R0.75Q · STEP 42", "CONSTANT SHEAR", "ONE REAL HARMONIC", "SPATIALLY SPREAD",
    "EXACT ZERO ROW", "PHASE-UNIFORM PERIODS", "RECTANGULAR SUBCOLLAR", "3D COLLAR CUBIC",
    "NO ENTRANCE CONCENTRATION", "ACTUAL COMPONENT ONLY", "Q.1", "Q.28", "180/180", "12/12",
    "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 400_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75q.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/assets/r075q")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75r.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75r.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075r")), false);
});

test("R0.75Q local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075q-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 46/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075q_spatially_spread_harmonic_collar_payment_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":180/);
});
