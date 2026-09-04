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
  "research/r076h_full_plateau_absorption_for_shifted_packet.md": "11490112a1893400a1099dd9f45b906ce78d7dab1ebcf549eaa7870241dc0ef4",
  "research/r076h_full_plateau_absorption_for_shifted_packet_primary_audit.md": "91e1f31f3adf19a9f352a8cd6defc8988971e51f0905e4a634f949223992c58d",
  "research/r076h_report-source.md": "3e706ae12caace1118f941f92c85bc0a1a11ed4a6e158acf7258918a67616d87",
  "scripts/r076h_full_plateau_absorption_for_shifted_packet_fixtures.json": "035ff9b04f61c11744668c51e6fd8ef1e35da93de85fab2bd9b971acca79747d",
  "scripts/r076h_full_plateau_absorption_for_shifted_packet_expected.json": "f80cc1d8b6673a6f18069d6756f605de821ac661561d11295a40c468532e083b",
  "scripts/r076h_full_plateau_absorption_for_shifted_packet_certificate.py": "65cd03fa1420eaffbf1a0e795d178b13b46829f79811963a724f2c25a9c72b2f",
  "scripts/r076h_full_plateau_absorption_for_shifted_packet_certificate_independent.rb": "4b1d72ad23b82eb48eef6df96d98bb904aa8f72e4932724ac72557c881c46cb3",
  "scripts/r076h_full_plateau_absorption_for_shifted_packet_qa.sh": "eea1b5f41b4c3959d1bdab214dc4c3b07fa05a0ca0f9a659c7ed8fa4fc565a02",
  "research/r076h_full_plateau_absorption_for_shifted_packet_certificate.json": "452e46b75a10d7fcb637d85234e1d3f76c471cd4ea1cec6b69b568260a8ff55e",
  "research/r076h_full_plateau_absorption_for_shifted_packet_certificate_report.md": "d9c80bc4af24f7f55046e2b5d13484841d3c430232c586913c10b23cbd425267",
  "research/r076h_full_plateau_absorption_for_shifted_packet_independent_audit.md": "f3d301f7b29cd1d5ceb89604d4b14d306e3f1fb47c35a5cce1cd689fc8b16fbd",
  "research/r076h_full_plateau_absorption_for_shifted_packet_qa_report.md": "bff6f11944ce50a875ad5395576b55a0d777f2df41a61f969558c755732cb54c",
};

test("R0.76H frozen ledger is byte-exact and both certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076h_full_plateau_absorption_for_shifted_packet_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionsPassed, 126);
  assert.equal(certificate.assertionsTotal, 126);
  assert.equal(certificate.negativeMutations.length, 126);
  assert.equal(certificate.exact.sample.a, 64);
  assert.equal(certificate.exact.sample.m, 4);
  assert.equal(certificate.exact.sample.q, 9);
  assert.deepEqual(certificate.exact.sample.modes, [8, 9, 10, 11, 12, 13, 14, 15, 16]);
  assert.equal(certificate.exact.rates.rawRate, "3/40000");
  assert.equal(certificate.exact.rates.normalizedRate, "-2/11907");
  assert.match(read("research/r076h_full_plateau_absorption_for_shifted_packet_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r076h_full_plateau_absorption_for_shifted_packet_independent_audit.md"), /Ruby assertions: 126\/126/);
  assert.match(read("research/r076h_full_plateau_absorption_for_shifted_packet_qa_report.md"), /126\/126 Python; 126\/126 Ruby/);
});

test("R0.76H proves full-plateau absorption and the exact normalized rate for only the explicit packet", () => {
  const source = read("research/r076h_full_plateau_absorption_for_shifted_packet.md");
  const compact = source.split(/\s+/).join(" ");
  const tags = [...source.matchAll(/\\tag\{H\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 39 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 39);
  for (const marker of [
    "candidate-killing result", "not a full-plateau counterexample", "M_L^{\\rm plat}",
    "\\exp\\!\\left(C_*\\frac ma\\right)", "=\\frac3{40000}", "=-\\frac2{11907}<0",
    "This does not improve R0.76E's uniform `exp(Cq)` upper bound", "**NOT CLAY.**",
  ]) assert.ok(compact.includes(marker), marker);
});

test("R0.76H reader is complete, figure-free, future-safe, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-76h.html");
  for (const marker of [
    "R0.76H · STEP 59", "CANDIDATE KILLED", "FULL PLATEAU ABSORPTION", "EXPLICIT PACKET ONLY",
    "RAW RATE 3/40000", "NORMALIZED RATE -2/11907", "H.1", "H.39", "126/126", "12/12",
    "NO FIGURE / NO DNS", "NO LATER RELEASE AUTHORIZED", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 465; section <= 471; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 685_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076h")), false);
  assert.equal(note.includes("R0.76I"), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76H local translation and frozen certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r076h-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 54/);
  assert.match(translationOutput, /"dgxUsed": false/);
  assert.match(read("research/r076h_full_plateau_absorption_for_shifted_packet_qa_report.md"), /Verdict: \*\*PASS\*\*[\s\S]*126\/126 Python; 126\/126 Ruby/);
});
