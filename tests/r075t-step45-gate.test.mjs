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
  "research/r075t_two_harmonic_collar_coercivity.md": "822059f8a6248143ff3f36938a2333bee9f909b9166db951e227c426c2e8bc66",
  "research/r075t_two_harmonic_collar_coercivity_primary_audit.md": "97d804444737284d7ec40b3ce45389272b1a9f61d1901f7bcebf9ed0eab935e5",
  "research/r075t_report-source.md": "c2255cdd07f2e490921d93ba7e62a809c0348a9e6136b7fd5537cf3799e4e8d8",
  "scripts/r075t_two_harmonic_collar_coercivity_fixtures.json": "939b04eeccb9c96b6d5cb21d49ebc48e7a8387dfccdc08afd2dfd6db77fd4393",
  "scripts/r075t_two_harmonic_collar_coercivity_expected.json": "cd58217667129d5a2f01dd2b315b86a934de1258be2eefab401f5b66efc127c5",
  "scripts/r075t_two_harmonic_collar_coercivity_certificate.py": "75e31019f8fe05d35a025e727098e99ebe4e5d8eebd60865e559456650c3a439",
  "scripts/r075t_two_harmonic_collar_coercivity_certificate_independent.rb": "24ccdc21eca83d8cff18b3ae8a7e3ab293e92e4d765fc70008c9c3ca4f4ddb25",
  "scripts/r075t_two_harmonic_collar_coercivity_qa.sh": "1be6a16dc1bf7eb10900128c3e2b10005ba530e0a168460f8a5c2a3bb19b0fb3",
  "research/r075t_two_harmonic_collar_coercivity_certificate.json": "85a78058a71b6d381edc14336c05c608719f25b88bad39add88d1e4b853b8966",
  "research/r075t_two_harmonic_collar_coercivity_certificate_report.md": "863b6af73f397691b0b7af1a21c7caadd84f29817c47742d4e8553d2209298b9",
  "research/r075t_two_harmonic_collar_coercivity_independent_audit.md": "5b4f2e9d3c68b8f408e5737f5cb7769586e9934792ab110c1626b5e7dec2b50d",
  "research/r075t_two_harmonic_collar_coercivity_qa_report.md": "96fec40029dda57bf6b3ce1a8e50616047b0c92a8462cf6e5b1776236dc837a9",
};

test("R0.75T frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075t_two_harmonic_collar_coercivity_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionCount, 14);
  assert.equal(certificate.assertions.length, 14);
  assert.ok(certificate.assertions.every((row) => row.pass === true));
  assert.match(read("research/r075t_two_harmonic_collar_coercivity_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075t_two_harmonic_collar_coercivity_independent_audit.md"), /Assertions: 15\/15/);
  assert.match(read("research/r075t_two_harmonic_collar_coercivity_qa_report.md"), /52\/52 Python; 52\/52 Ruby/);
});

test("R0.75T theorem boundary and equation ledger are materialized", () => {
  const source = read("research/r075t_two_harmonic_collar_coercivity.md");
  const tags = [...source.matchAll(/\\tag\{T\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 31 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 32);
  for (const marker of [
    "0\\le C,A,\\quad 1\\le m<k\\le2m", "maR>=C_0", "`d=k-m`", "q_{d,\\ell}",
    "H_{d,\\ell}", "4\\pi a\\delta_0R^2", "a^2R^3H_{d,aR}^3",
    "T.31 is not assumed or proved here", "complete two-harmonic flux payment",
    "No novelty or priority claim", "NOT\\ CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75T public reader is complete and future R0.75U output is absent", () => {
  const note = read("public/notes/r0-75t.html");
  for (const marker of [
    "R0.75T · STEP 45", "SPATIAL THEOREM", "EXACTLY TWO HARMONICS", "ONE DYADIC PAIR",
    "HIGH CARRIER", "EXACT PLATEAU FIBRE", "SLOW-ENVELOPE COERCIVITY", "BEAT DEFECT",
    "SHARP DEGENERACY", "UNEQUAL HEAT RATES", "FOUR-FREQUENCY FLUX", "TEMPORAL PAYMENT OPEN",
    "T.1", "T.31", "52/52", "12/12", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 351; section <= 357; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 490_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75t.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/assets/r075t")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75u.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75u.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075u")), false);
});

test("R0.75T local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075t-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 46/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075t_two_harmonic_collar_coercivity_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":52/);
});
