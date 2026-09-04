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
  "research/r075u_two_harmonic_difference_frequency_payment.md": "f9fb331cf880b20f3b407fe66453bce71517ac1ef2af4fa0863c00325c1022a4",
  "research/r075u_two_harmonic_difference_frequency_payment_primary_audit.md": "3687decf19ff49016e101a174d066b355689dcca7a4dc36a941b84994b118d6a",
  "research/r075u_report-source.md": "d0e9356a162b683a33c5b4c49692a62962d2a9c63cccba9eb9d84040aaf4a01f",
  "scripts/r075u_two_harmonic_difference_frequency_payment_fixtures.json": "c654b79a1b3b69078df01000c43fee54fdff39ea64c7bc47e206b114dc20b0c6",
  "scripts/r075u_two_harmonic_difference_frequency_payment_expected.json": "381e80ca54eee51fb3aab823837f0bfdc28e84353e02c8f41fceed261d6aec12",
  "scripts/r075u_two_harmonic_difference_frequency_payment_certificate.py": "040474723e1380ac6983c1fe165b910aa94751f7b8884cb7d015848d990a77a3",
  "scripts/r075u_two_harmonic_difference_frequency_payment_certificate_independent.rb": "77f2b4a6bbf389c54694dfdbf8759264ed10c89cfa2e9d085378f084810f263b",
  "scripts/r075u_two_harmonic_difference_frequency_payment_qa.sh": "26ab61750ecb1bfb5961479543fe32bc2338ae0bccfcf7c977cc26f71165c318",
  "research/r075u_two_harmonic_difference_frequency_payment_certificate.json": "87e6eb73c58a695a88ddc81948ddfea8257cb3844a1e4412068c28985ee28f5a",
  "research/r075u_two_harmonic_difference_frequency_payment_certificate_report.md": "3d0774651733e2f803cf3b679a0c8ba36a50029a27e88366c5d8bee2344d8b0d",
  "research/r075u_two_harmonic_difference_frequency_payment_independent_audit.md": "659dacda5aa67c502b3b6db315d06e9aed8cf4aa8fcd06aa45967b8de57950f8",
  "research/r075u_two_harmonic_difference_frequency_payment_qa_report.md": "180b9301689a510544c8a4b3bf74c3625767cd9f89cb84c4069c1cd56ea8132e",
};

test("R0.75U frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075u_two_harmonic_difference_frequency_payment_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionCount, 16);
  assert.equal(certificate.assertions.length, 16);
  assert.ok(certificate.assertions.every((row) => row.pass === true));
  assert.match(read("research/r075u_two_harmonic_difference_frequency_payment_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075u_two_harmonic_difference_frequency_payment_independent_audit.md"), /Assertions: 17\/17/);
  assert.match(read("research/r075u_two_harmonic_difference_frequency_payment_qa_report.md"), /61\/61 Python; 61\/61 Ruby/);
});

test("R0.75U theorem boundary and equation ledger are materialized", () => {
  const source = read("research/r075u_two_harmonic_difference_frequency_payment.md");
  const tags = [...source.matchAll(/\\tag\{U\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 28 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 28);
  for (const marker of [
    "A,C>=0", "1<=m<k<=2m", "d=k-m", "maR>=C_0", "\\tag{U.4}",
    "\\tag{U.10}", "\\tag{U.13}", "If `AC=0`", "All powers of `R` cancel",
    "This proves the difference-frequency target T.31", "not a complete two-harmonic flux theorem",
    "No novelty or priority claim", "NOT\\ CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75U public reader is complete and future R0.75V output is absent", () => {
  const note = read("public/notes/r0-75u.html");
  for (const marker of [
    "R0.75U · STEP 46", "DIFFERENCE ROW PAID", "EXACTLY TWO HARMONICS", "ONE DYADIC PAIR",
    "HIGH CARRIER", "COMPLETE CLOCK", "WEIGHTED PHASE LEMMA", "PHASE-DISTANCE MOMENT",
    "SLOW / FAST REGIMES", "AMPLITUDE CANCELS", "R POWERS CANCEL", "EXACT RATE -2/11907",
    "VERSION-M CONDITIONAL", "SELF / SUM BLOCK OPEN", "U.1", "U.28", "61/61", "12/12",
    "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 358; section <= 363; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 490_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75u.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/assets/r075u")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75u.html")), true);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75u.pdf")), true);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75v.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75v.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075u")), false);
});

test("R0.75U local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075u-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 45/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075u_two_harmonic_difference_frequency_payment_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":61/);
});
