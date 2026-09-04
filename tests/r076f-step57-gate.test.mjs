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
  "research/r076f_exponential_spatial_observation_lower_bound.md": "48204fcbf8fe9af3f0fdc7720844c3dd8362d8767caf73de016eda7250b70973",
  "research/r076f_exponential_spatial_observation_lower_bound_primary_audit.md": "abcaa220c56d1f90c4b34061191e7cd009b8d911be3f83d705e95aa51b4d84cc",
  "research/r076f_report-source.md": "5e3939710dcfefcbc08b93761d8cdda1e655656a1bcd404b63fcea251ffd5e1e",
  "scripts/r076f_exponential_spatial_observation_lower_bound_fixtures.json": "1b11049ab482eb9b6d6b99cfdabfb4cd0a34ac4f483e3e69c5ec178dce752b5a",
  "scripts/r076f_exponential_spatial_observation_lower_bound_expected.json": "9703be8236b77e556085f9b358f4128ace4e32920a5391ebc1e2a900b232d37a",
  "scripts/r076f_exponential_spatial_observation_lower_bound_certificate.py": "2882146fba7376d1f2d83d324c816b763729c59443fa4cb1f5fbcc47778c6994",
  "scripts/r076f_exponential_spatial_observation_lower_bound_certificate_independent.rb": "191b7ee7c0e7ed9157a33606c0ed00e3d0bd1db374260b26d8d5d5b64807bf32",
  "scripts/r076f_exponential_spatial_observation_lower_bound_qa.sh": "ba4fb4db589a502fa28f4f4d307a46b046b5fe253e12e57487c5da0c52d51546",
  "research/r076f_exponential_spatial_observation_lower_bound_certificate.json": "0558eab8a7ce5ae36e1614fe0c2184debfa8550c655a86baab590fbb9ee6f259",
  "research/r076f_exponential_spatial_observation_lower_bound_certificate_report.md": "7de8bb9ce8b59704c4097616a14e09366c8cc9031acf2e2692b51bce9a785ea0",
  "research/r076f_exponential_spatial_observation_lower_bound_independent_audit.md": "8b90a9ab9b60a17f6e5cfc097f658c80ce4cb410142d72123b72bef6895ab7de",
  "research/r076f_exponential_spatial_observation_lower_bound_qa_report.md": "6cf856c79f89e759eec05f51a8aa80e5abad4c7f04bc743aea26b6d8933eb13d",
};

test("R0.76F frozen ledger is byte-exact and both certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076f_exponential_spatial_observation_lower_bound_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionsPassed, 83);
  assert.equal(certificate.assertionsTotal, 83);
  assert.equal(certificate.negativeMutations.length, 83);
  assert.equal(certificate.exact.q, 4);
  assert.deepEqual(certificate.exact.frequencies, [4, 5, 6, 7]);
  assert.deepEqual(certificate.exact.amplitudes, [1, 3, 3, 1]);
  assert.equal(certificate.exact.lowerBound, 8);
  assert.equal(certificate.exact.tripleAngleRatio, 2);
  assert.match(read("research/r076f_exponential_spatial_observation_lower_bound_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r076f_exponential_spatial_observation_lower_bound_independent_audit.md"), /Ruby assertions: 83\/83/);
  assert.match(read("research/r076f_exponential_spatial_observation_lower_bound_qa_report.md"), /83\/83 Python; 83\/83 Ruby/);
});
test("R0.76F theorem proves the exponential spatial-observation lower bound and exact claim boundary", () => {
  const source = read("research/r076f_exponential_spatial_observation_lower_bound.md");
  const compact = source.split(/\s+/).join(" ");
  const tags = [...source.matchAll(/\\tag\{F\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 18 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 18);
  for (const marker of [
    "n_j=q+j-1", "n_q=2q-1\\le2q=2n_1", "2^{q-1}",
    "\\frac{\\sin(3x)}{\\sin x}", "\\log C_q\\ge(q-1)\\log2",
    "not a lower bound for the complete collar flux", "No novelty, priority",
    "**NOT CLAY.**",
  ]) assert.ok(compact.includes(marker), marker);
});

test("R0.76F reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-76f.html");
  for (const marker of [
    "R0.76F · STEP 57", "2^(Q-1) LOWER BOUND", "EXP(THETA(Q)) SHARPNESS",
    "SPATIAL ROW ONLY", "NO FULL-FLUX LOWER BOUND",
    "F.1", "F.18", "83/83", "12/12", "NO FIGURE / NO DNS", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 450; section <= 455; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 630_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076f")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76F local translation and frozen certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r076f-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 59/);
  assert.match(translationOutput, /"dgxUsed": false/);
  assert.match(read("research/r076f_exponential_spatial_observation_lower_bound_qa_report.md"), /Verdict: \*\*PASS\*\*[\s\S]*83\/83 Python; 83\/83 Ruby/);
});
