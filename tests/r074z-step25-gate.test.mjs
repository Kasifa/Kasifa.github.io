import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "python3";
const figureId = "fig-r074z-remote-persistence-gate";

const frozen = {
  "research/r074z_publication_handoff.md": "decf708987cd3f210ca672397c566e7006b7fae3cba5b1079410af56a588a091",
  "research/r074z_cancellation_cell_gate.md": "bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a",
  "research/r074z_cancellation_cell_gate_primary_audit.md": "6b867551bce840cb382cd13cb2ff298affbf0c0d8b1357a8163c5cedc9bace08",
  "research/r074z_cancellation_cell_gate_literature_audit.md": "8e5346ecf3c2beef4a620e0844e790703b628388ca7f0a6997aae88818caa82f",
  "research/r074z_cancellation_cell_gate_certificate.json": "aff6d6d39b2163a263bc2a5055225d9c25d5b46d0b2704bdfcb276976dcc2285",
  "research/r074z_cancellation_cell_gate_certificate_report.md": "91602c567e612759baf9bd03c7c688465c39997b90e445de13cc159f44cf5154",
  "research/r074z_cancellation_cell_gate_independent_audit.md": "cd44004a02c3486b734b17e2261dcd725a3d287f5462d7480ec7b294e2f43420",
  "research/r074z_cancellation_cell_gate_qa_report.md": "868afc8a69413e3176553acdb97bc03451de2181671684a207b01e7367d4e71f",
  "scripts/r074z_cancellation_cell_gate_certificate.py": "512cefac3d22dcc6836b128c052a9a528203be1e7ffd7217f16556193448631a",
  "scripts/r074z_cancellation_cell_gate_certificate_independent.rb": "766edac40dc9a3686067cad1ea31c01972075f1aa453e02e7fa4b461629a706c",
  "scripts/r074z_cancellation_cell_gate_qa.sh": "beaef0722e27813e4a0a164372355b2d5521413dad35e7f34d8b177f5842689a",
};

test("R0.74Z Step 25 frozen authority and exact evidence bytes", () => {
  assert.equal(Object.keys(frozen).length, 11);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.74Z Step 25 primary certificate reproduces in an isolated directory", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074z-persistence-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r074z_cancellation_cell_gate_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074Z_JSON: join(outputRoot, "certificate.json"),
        R074Z_REPORT: join(outputRoot, "certificate-report.md"),
      },
    }));
    const result = JSON.parse(readFileSync(join(outputRoot, "certificate.json"), "utf8"));
    assert.deepEqual(
      { verdict: stdout.verdict, checks: stdout.checks, tags: stdout.tags },
      { verdict: "PASS", checks: 10, tags: 42 },
    );
    assert.equal(result.assertions, 10);
    assert.equal(result.negative_mutations.length, 22);
    assert.ok(Object.values(result.checks).every(Boolean));
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r074z_cancellation_cell_gate_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate-report.md"))).digest("hex"), frozen["research/r074z_cancellation_cell_gate_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74Z Step 25 independent Ruby verifier reproduces", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074z-persistence-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r074z_cancellation_cell_gate_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R074Z_RUBY_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(
      { verdict: stdout.verdict, assertions: stdout.assertions, tags: stdout.tags },
      { verdict: "PASS", assertions: 11, tags: 42 },
    );
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r074z_cancellation_cell_gate_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74Z Step 25 QA preserves strict, conditional, full-clock, and novelty boundaries", () => {
  const report = bytes("research/r074z_cancellation_cell_gate_qa_report.md").toString("utf8");
  for (const marker of [
    "Python assertions: 10/10",
    "Ruby assertions: 11/11",
    "Python negative mutations rejected: 22/22",
    "Ruby negative mutations rejected: 23/23",
    "PYTHONHASHSEED byte-determinism: PASS (0, 1, 42)",
    "Full-clock Y.57 and the critical",
    "finite non-hit, no novelty inference",
  ]) assert.ok(report.includes(marker), marker);
});

test("R0.74Z Step 25 frozen figure archive is complete and byte-identical across mirrors", () => {
  const canonicalRoot = `research/figures/r074z/${figureId}`;
  const names = readdirSync(resolve(root, canonicalRoot)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  assert.equal(names.reduce((sum, name) => sum + statSync(resolve(root, canonicalRoot, name)).size, 0), 3032354);
  const ledgerRows = readFileSync(resolve(root, canonicalRoot, "SHA256SUMS"), "utf8").trim().split("\n");
  assert.equal(ledgerRows.length, 24);
  for (const row of ledgerRows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, row);
    assert.equal(sha(`${canonicalRoot}/${match[2]}`), match[1], match[2]);
  }
  for (const mirror of [`figures/r074z/${figureId}`, `public/figures/r074z/${figureId}`]) {
    assert.deepEqual(readdirSync(resolve(root, mirror)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
    for (const name of names) assert.equal(sha(`${mirror}/${name}`), sha(`${canonicalRoot}/${name}`), `${mirror}/${name}`);
  }
  assert.equal(sha(`${canonicalRoot}/figure.svg`), "31cfcd6e5e8e57729a8c5bce7459def3a618cd5bbda842a066331770ad0ffd42");
  assert.equal(sha(`${canonicalRoot}/figure.png`), "0414ade9d42a899830affe8ae730212946362ba72bc3a39bcf05c61df509368c");
  assert.equal(sha(`${canonicalRoot}/figure.pdf`), "4918a691914b23fd3570847510e57663d8db3ddad8a5707873943434b400d7b0");
});
