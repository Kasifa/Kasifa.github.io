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
  "research/r075r_outer_cap_spectral_concentration_obstruction.md": "e5eba5b262a8e140eaa149b6d914f355f2f3c636ec1e74cf85515f1c38fd32f3",
  "research/r075r_outer_cap_spectral_concentration_obstruction_primary_audit.md": "9b52e3d54fce43c609f70f0b8e71c53def0b4b705144be39a7b62e88d5e07355",
  "research/r075r_report-source.md": "767bfc43f9510a2acdf7fbff9d52624ed23ed80e4c3af174c77a47c3824d87ed",
  "scripts/r075r_outer_cap_spectral_concentration_obstruction_fixtures.json": "226b7411967f2fa6f1960d29a03f32ef40945af47c6545c3f60e4115e507a1d1",
  "scripts/r075r_outer_cap_spectral_concentration_obstruction_expected.json": "25d46dc6276a42f764dc503100750186213186368aebc9d94be409cd80f3c251",
  "research/r075r_outer_cap_spectral_concentration_obstruction_certificate.json": "9dcd06306bef05f33f88c09e982e97f04b3fd5a3ee9542e2e063c083a535a3ac",
  "research/r075r_outer_cap_spectral_concentration_obstruction_certificate_report.md": "40d17a2b3ddc7c2ee024c0e6288101eded441effa468d22555a1a8cb38c4d65f",
  "research/r075r_outer_cap_spectral_concentration_obstruction_independent_audit.md": "aac8e1a9fb01f9ba5b1e41d2ac25c9ee40a97e001a65e7c16a1dc1521dcf89dc",
  "research/r075r_outer_cap_spectral_concentration_obstruction_qa_report.md": "f9fa78b9a4dc918a318a64cff38408e0b3508a83446225532989651718884b19",
  "scripts/r075r_outer_cap_spectral_concentration_obstruction_certificate.py": "2c712cc35f53063212466a9c26b094d100a39809b8d424cc4062eb5b062d4e86",
  "scripts/r075r_outer_cap_spectral_concentration_obstruction_certificate_independent.rb": "2da9b4d9cbc53c7e0bb33f834f658b72ec7cfe88bacb215d221612a2dfa4283e",
  "scripts/r075r_outer_cap_spectral_concentration_obstruction_qa.sh": "266b8c2143f02e6f47365859d1343fcc1668601b977521783cadf939f0458aa5",
};

test("R0.75R frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075r_outer_cap_spectral_concentration_obstruction_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions, 21);
  assert.equal(certificate.passed, 21);
  assert.equal(certificate.checks.length, 21);
  assert.match(read("research/r075r_outer_cap_spectral_concentration_obstruction_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075r_outer_cap_spectral_concentration_obstruction_qa_report.md"), /76\/76 Python; 76\/76 Ruby/);
});

test("R0.75R theorem boundary, equation ledger, and plateau-only obstruction are materialized", () => {
  const source = read("research/r075r_outer_cap_spectral_concentration_obstruction.md");
  for (let index = 1; index <= 41; index += 1) assert.ok(source.includes(`\\tag{R.${index}}`), `R.${index}`);
  for (const marker of [
    "D_R(y)=\\Xi_R'(y)", "G_K(y)=A\\,d_n(y-y_0)^{2m}\\cos(q(y-y_0))",
    "\\frac{11K}{8}\\le|j|\\le\\frac{13K}{8}", "(\\partial_t+B\\partial_2-\\partial_2^2)F_K=0",
    "\\mathcal T_K", "M_{K,{\\rm plat}}", "\\frac{304373}{952560000}>0",
    "plateau-only", "not a counterexample to E.24",
    "No novelty or priority claim", "NOT\\ CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75R public reader is complete and forbidden future output is absent", () => {
  const note = read("public/notes/r0-75r.html");
  for (const marker of [
    "R0.75R · STEP 43", "NEGATIVE RESULT", "EXACT SMOOTH SHEAR", "REAL HIGH-BAND PACKET",
    "OUTER-CAP CONCENTRATION", "DIRICHLET KERNEL", "SIGNED FLUX LOWER", "PLATEAU CUBIC UPPER",
    "AMPLITUDE CANCELS", "PLATEAU-ONLY NO-GO", "R.1", "R.41", "76/76", "12/12",
    "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 440_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75r.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/assets/r075r")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75s.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75s.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075s")), false);
});

test("R0.75R local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075r-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 46/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075r_outer_cap_spectral_concentration_obstruction_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":76/);
});
