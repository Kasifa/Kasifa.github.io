import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");
const frozen = {
  "research/r076j_local_edge_extrapolation_reconstruction.md": "a3d67c8a27ef6ffb7068313732e8e8a08ba98931226df726ac4ee2140ab0f57f",
  "research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md": "1b2a608c6ffe16c35489b95fd384f0f47a1d4a79b22491a7825ac53382a746d5",
  "research/r076j_report-source.md": "371eac6e3f053d4ba51ded16f35024ba805d10c5a81c1f01879704ce583763c7",
  "scripts/r076j_local_edge_extrapolation_reconstruction_fixtures.json": "f0957b65e763339d1ff8cc029a13e13231b22b44dff8796b3b21883ffb352c31",
  "scripts/r076j_local_edge_extrapolation_reconstruction_expected.json": "9e5ad2f9bed318cd1232319240d2e574f070eda0364f97957df9c013f35878e8",
  "scripts/r076j_local_edge_extrapolation_reconstruction_certificate.py": "ed969fa1730597ecf33bc530ec1e40509080730f0a59552a1309182cd698f771",
  "scripts/r076j_local_edge_extrapolation_reconstruction_certificate_independent.rb": "ab58a7e8d77434de9ef363b04c43a612d5b61e0504faf82299783f7ea1b171f3",
  "scripts/r076j_local_edge_extrapolation_reconstruction_qa.sh": "d6364ed1896264a21173b2feb6b98e9b34522686d6300bd8066ef9dda18f0538",
  "research/r076j_local_edge_extrapolation_reconstruction_certificate.json": "23db36bc873a47e1992c9650e5ea04c5c1874f2e2a0bd17b6353bcb4452be89f",
  "research/r076j_local_edge_extrapolation_reconstruction_certificate_report.md": "a6c140ca114e73d975eff57de1804d85ba59fa080720fd5ac17e05d1bf7896d2",
  "research/r076j_local_edge_extrapolation_reconstruction_independent_audit.md": "63231761c982914b79e9e3eac271e3602737222fae41b30ea347941eaad056c7",
  "research/r076j_local_edge_extrapolation_reconstruction_qa_report.md": "0a59566aad669f72e9c013f1b4a02b3d35a8232fcd4a2a3781b458cc0e26cf8c",
};

test("R0.76J frozen ledger and finite certificates are exact", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076j_local_edge_extrapolation_reconstruction_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertionsPassed, 96);
  assert.equal(certificate.assertionsTotal, 96);
  assert.equal(certificate.negativeMutations.length, 96);
  assert.deepEqual(certificate.exact.structure, { displayCount: 48, firstTag: 1, lastTag: 46, tagCount: 46 });
  assert.equal(certificate.exact.asymptotic.modeWindowExponent, "5/2");
  assert.equal(certificate.exact.asymptotic.normalizedLogRate, "-2/11907");
  assert.equal(certificate.exact.constants.edgeSquaredPrefactor, "250/19");
  assert.equal(certificate.exact.constants.tailRecovery, "20/19");
  assert.match(read("research/r076j_local_edge_extrapolation_reconstruction_primary_audit.md"), /Mathematical verdict: \*\*PASS\*\*[\s\S]*Mathematical blockers: \*\*0\*\*[\s\S]*Claim-boundary blockers: \*\*0\*\*/);
  assert.match(read("research/r076j_local_edge_extrapolation_reconstruction_independent_audit.md"), /Ruby assertions: 107\/107/);
});

test("R0.76J local theorem, historical I boundary, and reader are explicit", () => {
  const source = read("research/r076j_local_edge_extrapolation_reconstruction.md");
  const tags = [...source.matchAll(/\\tag\{J\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 46 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 48);
  for (const marker of ["PROVED LOCALLY FROM ESTABLISHED LITERATURE", "q=o(L^{5/2})", "20\\sqrt2", "-\\frac2{11907}", "exact one-band constant shear", "NOT CLAY"]) assert.ok(source.includes(marker), marker);
  const note = read("public/notes/r0-76j.html");
  for (const marker of ["R0.76J · STEP 61", "LOCAL EDGE PROOF", "I HISTORY: CONDITIONAL-LITERATURE", "PROVED LOCALLY FROM ESTABLISHED LITERATURE", "J.1", "J.46", "96/96", "107/107", "12/12", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  for (let section = 481; section <= 488; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076j")), false);
  assert.equal(note.includes("R0.76K"), false);
});

test("R0.76J translations and frozen certificate QA are deterministic", () => {
  const output = execFileSync(process.execPath, ["scripts/add-r076j-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 59/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(read("research/r076j_local_edge_extrapolation_reconstruction_qa_report.md"), /Verdict: \*\*PASS\*\*[\s\S]*Ruby assertions: 107\/107/);
});
