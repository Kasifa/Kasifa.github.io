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
  "research/r075y_strongly_separated_multimode_flux_payment.md": "74790f910b596c86b204291d997ef723cabbc85d14a89e3fe900814fcd88b0a6",
  "research/r075y_strongly_separated_multimode_flux_payment_primary_audit.md": "f7e1feedd1fa359877554eff4fa20c470f727ae7743c990136525ad22d6cdf3b",
  "research/r075y_report-source.md": "e6d6b1ed2830b46fc901a9ab09ef368f258f13dfc8c0961076baedd5b46e1589",
  "scripts/r075y_strongly_separated_multimode_flux_payment_fixtures.json": "45448bf75c867b3f9654db79c77ae52b9bd35d7e781b240f564a9d871faab32b",
  "scripts/r075y_strongly_separated_multimode_flux_payment_expected.json": "324e92dd32d6e1ca76b22c47a201206e1c924e1100b92de1c8429ffd17ac25d3",
  "scripts/r075y_strongly_separated_multimode_flux_payment_certificate.py": "126e97f7d248c7d5516b927816fed3cb3269b59fd2d0def3ec410d4502e7d078",
  "scripts/r075y_strongly_separated_multimode_flux_payment_certificate_independent.rb": "69c1dfdd9149fc89a0c14407a9373f03e418cfd0b3c5b2fda1d9a96261141e70",
  "scripts/r075y_strongly_separated_multimode_flux_payment_qa.sh": "dc73c406ac40d6b64f7f9164cf0d4cf494bbb3eddc31ff5f69a662da00316517",
  "research/r075y_strongly_separated_multimode_flux_payment_certificate.json": "2c74a9bf2bd9b1f24dd66fdc330bd4dd814d63ec1bce36e7efa1e337cfa4fdfe",
  "research/r075y_strongly_separated_multimode_flux_payment_certificate_report.md": "cd3b1bf9aff7b326c92a1e40a0f3ae0fc363e734be7d859e6a7d6c62fae7a0a7",
  "research/r075y_strongly_separated_multimode_flux_payment_independent_audit.md": "e45e30a34253905b24acafdf18b9dfcf3d6ffd6163cd38996a1c4991335c8d21",
  "research/r075y_strongly_separated_multimode_flux_payment_qa_report.md": "f2a49eafe9317aba8bdb582b4f0e0852e8cb7603fb8a415ec3df78ed5be5e67a",
};

test("R0.75Y frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075y_strongly_separated_multimode_flux_payment_certificate.json"));
  assert.equal(certificate.summary.verdict, "PASS");
  assert.equal(certificate.summary.assertions, 17);
  assert.equal(certificate.summary.passed, 17);
  assert.equal(certificate.summary.failed, 0);
  assert.equal(certificate.assertions.length, 17);
  assert.ok(certificate.assertions.every((row) => row.pass === true));
  assert.equal(certificate.computed.separatedCase.signedFrequencies.length, 6);
  assert.equal(certificate.computed.separatedCase.separationProduct, 24);
  assert.equal(certificate.computed.gramLedger.signedModeCount, 6);
  assert.equal(certificate.computed.rowLedger.totalRows, 9);
  assert.equal(certificate.computed.scaleLedger.target.q, 2);
  assert.equal(certificate.computed.scaleLedger.frozenRate, "-2/11907");
  assert.match(read("research/r075y_strongly_separated_multimode_flux_payment_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075y_strongly_separated_multimode_flux_payment_independent_audit.md"), /Assertions: 18\/18/);
  assert.match(read("research/r075y_strongly_separated_multimode_flux_payment_qa_report.md"), /85\/85 Python; 85\/85 Ruby/);
});

test("R0.75Y strong-separation boundary and equation ledger are materialized", () => {
  const source = read("research/r075y_strongly_separated_multimode_flux_payment.md");
  const tags = [...source.matchAll(/\\tag\{Y\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 39 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 39);
  for (const marker of [
    "1\\le n_1<n_2<\\cdots<n_q\\le2n_1", "\\ell=aR", "\\ell\\delta_{\\boldsymbol n}\\ge8q",
    "\\tag{Y.3}", "\\tag{Y.15}", "\\tag{Y.20}", "\\tag{Y.28}", "\\tag{Y.37}", "\\tag{Y.39}",
    "all displayed mode-count dependence is the\nexplicit factor `q^2`", "sparse class when `q` grows",
    "unresolved spectral clusters", "not valid merely for a Fourier projection", "-2/11907", "**NOT CLAY.**",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75Y reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-75y.html");
  for (const marker of [
    "R0.75Y · STEP 50", "STRONGLY SEPARATED", "SIGNED-SPECTRUM GAP", "GRAM COERCIVITY",
    "PHASE-FREE CLOCK", "ALL q^2 ROWS", "EXPLICIT q^2 COST", "NO HIDDEN q CONSTANT",
    "EXACT RATE -2/11907", "CLUSTERS OPEN", "VERSION-M CONDITIONAL", "Y.1", "Y.39",
    "17/17", "18/18", "85/85", "12/12", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 393; section <= 400; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 500_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r075y")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
  assert.equal(existsSync(resolve(root, "public/notes/r0-75z.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75z.pdf")), false);
});

test("R0.75Y local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075y-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 49/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075y_strongly_separated_multimode_flux_payment_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":85/);
});
