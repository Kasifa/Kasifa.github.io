import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");
const ledger = JSON.parse(read("research/r076l_frozen_ledger.json"));
const frozen = Object.fromEntries(ledger.files.map(({ path, sha256 }) => [path, sha256]));
const figureId = "fig-r076l-parabolic-edge";

test("R0.76L frozen ledger, certificates, and formal figure are exact", () => {
  assert.equal(ledger.schemaVersion, "r076l-step63-frozen-ledger-v1");
  assert.equal(ledger.sourceCommit, "b234b63c24c7b19efc703367e23b092385066a1c");
  assert.equal(ledger.certificateCommit, "2f3e0f466cc38fd2b61f2c79773352d95b2464e1");
  assert.equal(ledger.handoffCommit, "a5edefb014ebc6dd13ce052aad196ff5115b9629");
  assert.equal(ledger.fileCount, 24);
  assert.equal(Object.keys(frozen).length, 24);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076l_parabolic_edge_smoothing_complete_clock_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.freezeReady, true);
  assert.equal(certificate.assertionsPassed, 64);
  assert.equal(certificate.assertionsTotal, 64);
  assert.equal(certificate.negativeMutations.length, 25);
  assert.deepEqual(certificate.exact.structure, { displayCount: 78, firstTag: 1, lastTag: 72, referencesClosed: true, tagCount: 72, tagSequenceComplete: true });
  assert.equal(certificate.exact.claims.completeClockEventuallyPositiveForFamily, true);
  assert.equal(certificate.exact.claims.fullPhysicalPlateauUsed, true);
  assert.equal(certificate.exact.claims.candidateKilledForThisFamily, true);
  assert.equal(certificate.exact.claims.bulkA4SaddleTheorem, false);
  assert.equal(certificate.exact.diagnostic.knownPreasymptoticAwaySequence, "degreePower=3/4; metric=unitTiltOverMu; displayedDirection=awayFromLimit");
  for (const extension of ["svg", "png", "pdf"]) {
    const source = `figures/r076l-parabolic-edge/${figureId}/figure.${extension}`;
    assert.equal(sha(`research/figures/r076l/${figureId}/figure.${extension}`), sha(source));
    assert.equal(sha(`public/figures/r076l/${figureId}/figure.${extension}`), sha(source));
    assert.equal(sha(`public/assets/r076l/${figureId}.${extension}`), sha(source));
  }
});

test("R0.76L reader states the family-specific theorem and high-degree open boundary", () => {
  const source = read("research/r076l_parabolic_edge_smoothing_complete_clock.md");
  const tags = [...source.matchAll(/\\tag\{L\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 72 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 78);
  const note = read("public/notes/r0-76l.html");
  for (const marker of ["R0.76L · STEP 63", "START-PREPAID FAMILY", "COMPLETE CLOCK POSITIVE", "FULL PHYSICAL PLATEAU", "√A ≪ m = o(A²)", "-2/11907", "L.1", "L.72", "64/64", "279/279", "24/24", "FORMAL FIGURE", "p=0.75", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  for (let section = 497; section <= 507; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 1);
  assert.ok(note.includes(`/assets/r076l/${figureId}.svg`));
  assert.ok(note.includes("略微远离解析极限"));
  const lBody = note.slice(note.indexOf('<section id="s-497">'), note.indexOf('<section id="figure">'));
  assert.equal(lBody.includes(",qquad"), false);
  assert.equal(note.includes("R0.76M"), false);
});

test("R0.76L translations and frozen QA are deterministic", () => {
  const output = execFileSync(process.execPath, ["scripts/add-r076l-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 72/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(read("research/r076l_parabolic_edge_smoothing_complete_clock_qa_report.md"), /Verdict: \*\*PASS\*\*[\s\S]*Independent Ruby finite certificate: 279\/279/);
});
