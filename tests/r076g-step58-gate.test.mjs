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
  "research/r076g_complete_clock_central_fibre_flux_lower_bound.md": "20f32790b53f2b0f5cb39b7071bd2cda96ddb4e15f75211e1682f4ba37dd0bb2",
  "research/r076g_complete_clock_central_fibre_flux_lower_bound_primary_audit.md": "af47153c4e1f4c5749f68c3f89d7533c5d95f3c0c6f15b0c775a9e35317c807e",
  "research/r076g_report-source.md": "3aea1d04dce4987c3883c1b93bec04e714ee17b540fb6a99546d084efa326f74",
  "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_fixtures.json": "32e1dcf71a77ba0d28e3924fcb7e7aeb4d2840aa08ba2b2e352bb4d20d0464af",
  "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_expected.json": "0a2d3d086381029941310ae502b4cf9462e025d0c75e62dd87c07334728a6ba8",
  "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.py": "0afbee1f11de12cefc85aee64cbdb8c92925ad2db33cdae8d0582b79dbc01f85",
  "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_certificate_independent.rb": "ea5036ffed18ce5d1ff33addeff6086ab3603bcedf2373ca6dec7ca3e4963fa2",
  "scripts/r076g_complete_clock_central_fibre_flux_lower_bound_qa.sh": "4fdbce0ab1b3b81dd87a07d4852c9b00ba3b3e6790e714f26124aabf2784ff1e",
  "research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.json": "dcca5611f40b5de9cfcc76fccc3ed35a0219a8baedbb488574223809686c652d",
  "research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate_report.md": "f77d2e636e65ff07f662adc72fa16f13ab4edb57addf8422536fa67a0b36660c",
  "research/r076g_complete_clock_central_fibre_flux_lower_bound_independent_audit.md": "c034a9d3f01e784733fd35052ec4b9574c9ee4596ad44e466d07a78773953a68",
  "research/r076g_complete_clock_central_fibre_flux_lower_bound_qa_report.md": "d12f43049dc3bf151708561a0e8129a0c49d2dd0ca470e008818763519e2ae53",
};

test("R0.76G frozen ledger is byte-exact and both certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076g_complete_clock_central_fibre_flux_lower_bound_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionsPassed, 120);
  assert.equal(certificate.assertionsTotal, 120);
  assert.equal(certificate.negativeMutations.length, 120);
  assert.equal(certificate.exact.sample.m, 3);
  assert.equal(certificate.exact.sample.modeCount, 7);
  assert.deepEqual(certificate.exact.sample.modes, [6, 7, 8, 9, 10, 11, 12]);
  assert.equal(certificate.exact.rational.ratioBase, "9/7");
  assert.equal(certificate.exact.rational.netRateRationalLowerBound, "2/35721");
  assert.match(read("research/r076g_complete_clock_central_fibre_flux_lower_bound_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r076g_complete_clock_central_fibre_flux_lower_bound_independent_audit.md"), /Ruby assertions: 120\/120/);
  assert.match(read("research/r076g_complete_clock_central_fibre_flux_lower_bound_qa_report.md"), /120\/120 Python; 120\/120 Ruby/);
});

test("R0.76G proves the complete-clock central-fibre signed-flux lower bound and its exact boundary", () => {
  const source = read("research/r076g_complete_clock_central_fibre_flux_lower_bound.md");
  const compact = source.split(/\s+/).join(" ");
  const tags = [...source.matchAll(/\\tag\{G\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 40 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 40);
  for (const marker of [
    "q=2m+1", "n_q=4m=2n_1", "B=-\\frac{\\beta a}{R}",
    "\\left(\\frac97\\right)^{4m}", "\\frac{q(L)}{L^2}\\longrightarrow\\frac2{3969}",
    "The numerator in G.8 is the complete signed flux", "not the full physical plateau mass",
    "**NOT CLAY.**",
  ]) assert.ok(compact.includes(marker), marker);
});

test("R0.76G reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-76g.html");
  for (const marker of [
    "R0.76G · STEP 58", "COMPLETE CLOCK", "SIGNED FLUX LOWER BOUND", "NONZERO DRIFT",
    "CENTRAL-FIBRE PROXY", "(9/7)^(4M)", "NO FULL-PLATEAU LOWER BOUND",
    "G.1", "G.40", "120/120", "12/12", "NO FIGURE / NO DNS", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 456; section <= 464; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 670_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076g")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76G local translation and frozen certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r076g-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 55/);
  assert.match(translationOutput, /"dgxUsed": false/);
  assert.match(read("research/r076g_complete_clock_central_fibre_flux_lower_bound_qa_report.md"), /Verdict: \*\*PASS\*\*[\s\S]*120\/120 Python; 120\/120 Ruby/);
});
