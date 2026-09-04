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
  "research/r075p_buffered_collar_entrance_concentration.md": "8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6",
  "research/r075p_buffered_collar_entrance_concentration_primary_audit.md": "e065759a1df3c118f71dd47ac9b5ded9df40536217f557b3c1155e8bf64d3390",
  "research/r075p_report-source.md": "fcde6bed847b0628aff7de90a49e8150e4a279fca8e46d7053943fdadf0478ca",
  "scripts/r075p_buffered_collar_entrance_concentration_fixtures.json": "9d9bf2a00fbdf58eb85a01a3f7fe931f289a5bc1166430dac1f704e4406ec6d7",
  "scripts/r075p_buffered_collar_entrance_concentration_expected.json": "cc472fb797c98d61e004c09fb84ba4a29029d72665f60507628c166134b39d31",
  "research/r075p_buffered_collar_entrance_concentration_certificate.json": "acbb41a489120b00a32f75999909f0cabce4f96ac5e8650c3ebfd2e0a35dc0a8",
  "research/r075p_buffered_collar_entrance_concentration_certificate_report.md": "1c9bc9553d1facdab0b385a59480c378dfd516412c38eb3a20e76049745560ac",
  "research/r075p_buffered_collar_entrance_concentration_independent_audit.md": "60b042b5830167508f096fe7d990f7d2b5fca99da312f0e6116b8c39c0c7923d",
  "research/r075p_buffered_collar_entrance_concentration_qa_report.md": "81e6ff0eefc1fd4d65b1cd7fc8c950b0e284f7b9c54c4542b1e79c9c6dec1dd7",
  "scripts/r075p_buffered_collar_entrance_concentration_certificate.py": "5c13e8bb480e4565a4b7be6f6d86a0a963cea5ce9d53495f5e0cf3c7983b1c6c",
  "scripts/r075p_buffered_collar_entrance_concentration_certificate_independent.rb": "5fb32514dc125462239adc31bc5da58460946d8caaed0d3a1c76d6620b8bfd2c",
  "scripts/r075p_buffered_collar_entrance_concentration_qa.sh": "8c4fbeb7667bdb4f937e66cd73d663fa8cd85538412e538259b9a0128f9a27fb",
};

test("R0.75P frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075p_buffered_collar_entrance_concentration_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions.total, 21);
  assert.equal(certificate.assertions.passed, 21);
  assert.equal(Object.keys(certificate.checks).length, 21);
  assert.match(read("research/r075p_buffered_collar_entrance_concentration_primary_audit.md"), /Verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075p_buffered_collar_entrance_concentration_qa_report.md"), /132\/132 Python; 132\/132 Ruby/);
});

test("R0.75P theorem boundary, equation ledger, and buffered-collar rows are materialized", () => {
  const source = read("research/r075p_buffered_collar_entrance_concentration.md");
  for (let index = 1; index <= 31; index += 1) assert.ok(source.includes(`\\tag{P.${index}}`), `P.${index}`);
  for (const marker of [
    "E_{\\rm in}\\ge\\mu E_0", "\\ell_{a}(q)", "\\partial_t\\phi_t+B\\partial_2\\phi_t=0",
    "c_*a^{-1}\\mu^{5/2}K^{-2}E_0^{3/2}", "8558}{178605", "At equality the exponential rate vanishes",
    "p_{K,\\rm col}\\le C P_R^M", "not a Littlewood--Paley", "low-concentration complement",
    "No novelty\nor priority claim", "NOT\\ CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75P public reader is complete and forbidden future output is absent", () => {
  const note = read("public/notes/r0-75p.html");
  for (const marker of [
    "R0.75P · STEP 41", "CONSTANT SHEAR", "ENTRANCE CONCENTRATION", "MOVING CUTOFF",
    "RADIAL PLATEAU FIBRES", "3D COLLAR CUBIC", "STRICT ENDPOINT", "ACTUAL COMPONENT ONLY",
    "P.1", "P.31", "132/132", "12/12", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 400_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75p.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/assets/r075p")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75q.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75q.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075q")), false);
});

test("R0.75P local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075p-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": \d+/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075p_buffered_collar_entrance_concentration_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":132/);
});
