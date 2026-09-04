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
  "research/r076i_chebyshev_scale_full_plateau_window.md": "6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce",
  "research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md": "65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe",
  "research/r076i_report-source.md": "0ee0fbd75f9691e2ac898a57921f8a0574ba9af9ea652f85d0199856d7e3d423",
  "scripts/r076i_chebyshev_scale_full_plateau_window_fixtures.json": "f1475b2549490c3639c15a4fc103e704d0de98a518f50249b732a8e0a135d776",
  "scripts/r076i_chebyshev_scale_full_plateau_window_expected.json": "26485db072bf886fae88f0737546d7090f77b9b23e55c356bf8affe6aeba1da5",
  "scripts/r076i_chebyshev_scale_full_plateau_window_certificate.py": "a14e7fe3bc3b118232328a6d9e4d9d4cedb1e685c057483e12416725024af538",
  "scripts/r076i_chebyshev_scale_full_plateau_window_certificate_independent.rb": "5e1ead81eb0f036d41addf2dd203527c3ae49aa497d483002a3973b69d88225c",
  "scripts/r076i_chebyshev_scale_full_plateau_window_qa.sh": "d23b771cd0e7c5253ba592f9efd2e7c0c2396cd928641f6463559b2b20953458",
  "research/r076i_chebyshev_scale_full_plateau_window_certificate.json": "6ae521f88a1e6116f466641bde60939e458b043b43ca025a10a83001613c590b",
  "research/r076i_chebyshev_scale_full_plateau_window_certificate_report.md": "b5d1f7b0e36f724522bc5b18442bad97ffe778e7be6ca579c0ca0bd89d9d061c",
  "research/r076i_chebyshev_scale_full_plateau_window_independent_audit.md": "f8c735e654031b8d5ae7029879086bf95086e7745317b7faa0e6750151093b4d",
  "research/r076i_chebyshev_scale_full_plateau_window_qa_report.md": "7f709110b3191508541367846c9ef0358016cfcb91c160e00b9db123664dd34a",
};

test("R0.76I frozen ledger is byte-exact and both finite certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076i_chebyshev_scale_full_plateau_window_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionsPassed, 129);
  assert.equal(certificate.assertionsTotal, 129);
  assert.equal(certificate.negativeMutations.length, 129);
  assert.equal(certificate.exact.structure.tagCount, 38);
  assert.equal(certificate.exact.structure.displayCount, 42);
  assert.equal(certificate.exact.physical.modeWindowExponent, "5/2");
  assert.equal(certificate.exact.physical.normalizedLogRate, "-2/11907");
  assert.match(read("research/r076i_chebyshev_scale_full_plateau_window_primary_audit.md"), /Mathematical verdict: \*\*PASS\*\*[\s\S]*Mathematical blockers: \*\*0\*\*[\s\S]*Claim-boundary blockers: \*\*0\*\*/);
  assert.match(read("research/r076i_chebyshev_scale_full_plateau_window_independent_audit.md"), /Ruby assertions: 129\/129/);
});

test("R0.76I keeps the imported theorem conditional and proves only the local exact-shear bridge", () => {
  const source = read("research/r076i_chebyshev_scale_full_plateau_window.md");
  const tags = [...source.matchAll(/\\tag\{I\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 38 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 42);
  for (const marker of [
    "CONDITIONAL-LITERATURE", "Zhang", "Proposition 4.2", "PROVED LOCALLY",
    "q(L)=o(L^{5/2})", "12\\sqrt2", "=-\\frac2{11907}", "exact real constant shears in one dyadic band",
    "a matching lower bound within I.2", "NOT CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.76I reader and recap are complete, figure-free, and future-safe", () => {
  const note = read("public/notes/r0-76i.html");
  const recap = read("public/recap-r0-61-r0-76i.html");
  for (const marker of ["R0.76I · STEP 60", "CONDITIONAL-LITERATURE", "LITERATURE", "PROVED LOCALLY", "FINITE COMPUTATION", "q=o(L^(5/2))", "-2/11907", "I.1", "I.38", "129/129", "12/12", "NO FIGURE / NO DNS", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  for (let section = 472; section <= 480; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  for (const marker of ["203 NODES", "E · UNIFORM BARRIER", "F–H · EXPLICIT PACKET CHAIN", "I · CONDITIONAL-LITERATURE", "q=o(L^(5/2))", "NO FULL-CLASS SHARPNESS CLAIM", "NOT CLAY"]) assert.ok(recap.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 700_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal((recap.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076i")), false);
  assert.equal(note.includes("R0.76J"), false);
  assert.equal(recap.includes("R0.76J"), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76I translation and frozen certificate QA remain deterministic", () => {
  const translation = execFileSync(node, ["scripts/add-r076i-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translation, /"checked": 97/);
  assert.match(translation, /"dgxUsed": false/);
  assert.match(read("research/r076i_chebyshev_scale_full_plateau_window_qa_report.md"), /Verdict: \*\*PASS\*\*[\s\S]*129\/129 Python; 129\/129 Ruby/);
});
