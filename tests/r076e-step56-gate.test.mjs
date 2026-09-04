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
  "research/r076e_linear_modal_entropy_window.md": "1494cb7e3863ef934f87746412f2a64ef98f78deb5ce81be3cece7d5a7571ca4",
  "research/r076e_linear_modal_entropy_window_primary_audit.md": "5ce8fb3f2f2f487002b0e391db49855edb3cff72574058e26150813d69615d27",
  "research/r076e_report-source.md": "10e506fa9d250b14d9f42f6eac7c2c83cfca934a85a2da6e223cd473f21e0c12",
  "scripts/r076e_linear_modal_entropy_window_fixtures.json": "9b5b0a7d88fe31d4156a7fbc8f73b52a9b5a8271437ee1be867970cec244cf47",
  "scripts/r076e_linear_modal_entropy_window_expected.json": "af6c1fd49d57945306f5f97a99f160a8fcbaec21bce887b78fe74e0bbe4d4f80",
  "scripts/r076e_linear_modal_entropy_window_certificate.py": "57e629e0952131928e738501ee14f525daf3e2ac5fcb3b37fe02b118d7fb0f6c",
  "scripts/r076e_linear_modal_entropy_window_certificate_independent.rb": "e5f340e181b96a45d202ec88e5d98d71744b2ed23008e579c8c705c88fc30bdd",
  "scripts/r076e_linear_modal_entropy_window_qa.sh": "76859a4f6fc86652957336a096ec06c73f643cfac0e46df38e1c38bad1b9fee0",
  "research/r076e_linear_modal_entropy_window_certificate.json": "73daf5a6fe12096b29b87704a667e45c994cd2233244e6f2f8daba987b471245",
  "research/r076e_linear_modal_entropy_window_certificate_report.md": "8e3937b7b5843b49c53fbbc6b3cc0490a139b1c2ff2e469bb64758f112d11f31",
  "research/r076e_linear_modal_entropy_window_independent_audit.md": "bc5ed58d5a47a1c847ea626c85da49078a19ed148323c72eaf3d452b90ad3842",
  "research/r076e_linear_modal_entropy_window_qa_report.md": "0afdabc3805121ef593c1c2741b12d6011821a0cc98c7b07b76306c7f24ef631",
};

test("R0.76E frozen ledger is byte-exact and both certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076e_linear_modal_entropy_window_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionsPassed, 135);
  assert.equal(certificate.assertionsTotal, 135);
  assert.equal(certificate.negativeMutations.length, 135);
  assert.equal(certificate.exact.delayedSplit.m, 10);
  assert.equal(certificate.exact.delayedSplit.maximumTerms, 6);
  assert.equal(certificate.exact.delayedSplit.sampleStart, 96);
  assert.equal(certificate.exact.delayedSplit.strictBinaryUpperExponent, -93);
  assert.equal(certificate.exact.delayedSplit.weightedEarlyPower, "4/3");
  assert.equal(certificate.exact.energy.gradientCoefficient, "257/64");
  assert.equal(certificate.exact.energy.weightedLambdaPower, "-1/3");
  assert.equal(certificate.exact.energy.endpointLambdaPower, "0");
  assert.equal(certificate.exact.scaleLedger.frozenRate, "-2/11907");
  assert.match(read("research/r076e_linear_modal_entropy_window_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r076e_linear_modal_entropy_window_independent_audit.md"), /Ruby assertions: 135\/135/);
  assert.match(read("research/r076e_linear_modal_entropy_window_qa_report.md"), /135\/135 Python; 135\/135 Ruby/);
});
test("R0.76E theorem retains the linear entropy loss and exact claim boundary", () => {
  const source = read("research/r076e_linear_modal_entropy_window.md");
  const compact = source.split(/\s+/).join(" ");
  const tags = [...source.matchAll(/\\tag\{E\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 34 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 38);
  for (const marker of [
    "q\\in\\mathbb N", "n_j\\in\\mathbb N", "\\phi_j,B\\in\\mathbb R",
    "e^{C_*q}a^{2/3}R^{-1/3}", "q(L)=o(L^2)", "S_N=C_0N\\log(N+1)",
    "4^{-1/3}S_N^{4/3}K_T^{2/3}", "e^{CN}T^{-2/3}K_T^{2/3}",
    "\\lambda^{-1/3}H^{2/3}", "complete real square", "not uniform in \`q\`",
    "not an arbitrary-packet estimate", "**NOT CLAY.**",
  ]) assert.ok(compact.includes(marker), marker);
});

test("R0.76E reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-76e.html");
  for (const marker of [
    "R0.76E · STEP 56", "EXP(C Q) LOSS", "LINEAR MODAL ENTROPY",
    "Q(L) = o(L^2)", "DELAYED STABLE HEAT CLOCK", "LAST-UNIT ENDPOINT",
    "E.1", "E.34", "135/135", "12/12", "NO FIGURE / NO DNS", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 442; section <= 449; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 600_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076e")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76E local translation and frozen certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r076e-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 56/);
  assert.match(translationOutput, /"dgxUsed": false/);
  assert.match(read("research/r076e_linear_modal_entropy_window_qa_report.md"), /Verdict: \*\*PASS\*\*[\s\S]*135\/135 Python; 135\/135 Ruby/);
});
