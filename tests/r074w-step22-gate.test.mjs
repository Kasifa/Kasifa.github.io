import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "python3";
const figureId = "fig-r074w-remote-adjacent-inward-threshold";

const frozen = {
  "research/r074w_publication_handoff.md": "01a9d5cb2d9a5d2c7a8f57c8e8fca964f2c59b330eebc2975b0e968840e1ec5b",
  "research/r074w_remote_adjacent_inward_comparison.md": "d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10",
  "research/r074w_remote_adjacent_inward_comparison_primary_audit.md": "66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73",
  "research/r074w_remote_adjacent_inward_literature_audit.md": "ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99",
  "research/r074w_remote_adjacent_inward_comparison_certificate.json": "7c0b86b6f4f9a5782946f443bdf731445adbce9069fcba726a7b8fe75df9c171",
  "research/r074w_remote_adjacent_inward_comparison_certificate_report.md": "d70b18dbde23d49e51ec24c1cf8e0f764a5a639297ce783bcc23bf69d050b003",
  "research/r074w_remote_adjacent_inward_comparison_independent_audit.md": "dd6a2b1820da126e049aae97ab9b26bb9ef0d02bacca1dc248298303bb2748a3",
  "research/r074w_remote_adjacent_inward_comparison_qa_report.md": "26df7a1b5fbff87f752a8cebb98113b4fcc13f3b8828566b3fab2eda07e7f223",
  "scripts/r074w_remote_adjacent_inward_comparison_certificate.py": "33084928360a5b649ae862cc416679deca8e34574820095f7ffdac52bb760395",
  "scripts/r074w_remote_adjacent_inward_comparison_certificate_independent.rb": "ff69d1f31d90bea7ec4b6d935d75870bb633f027ffb91bacd073da2d7a4916a4",
  "scripts/r074w_remote_adjacent_inward_comparison_qa.sh": "40c798d56d3845753abc5fe5a2ee022f7a62716ed98ef5184c7f82e039d0f5db",
};

test("R0.74W Step 22 frozen authority and exact evidence bytes", () => {
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.74W Step 22 primary certificate reproduces in an isolated directory", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074w-remote-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r074w_remote_adjacent_inward_comparison_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R074W_JSON: join(outputRoot, "certificate.json"), R074W_REPORT: join(outputRoot, "certificate-report.md") },
    }));
    const result = JSON.parse(readFileSync(join(outputRoot, "certificate.json"), "utf8"));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.checks_passed}/${stdout.checks_total}`, cases: stdout.cases },
      { verdict: "PASS", groups: "33/33", cases: 33 },
    );
    assert.equal(result.checks.filter((row) => row.group === "finite").length, 22);
    assert.equal(result.checks.filter((row) => row.group === "structural").length, 8);
    assert.equal(result.checks.filter((row) => row.group === "hash").length, 3);
    assert.ok(result.checks.every((row) => row.pass));
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r074w_remote_adjacent_inward_comparison_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate-report.md"))).digest("hex"), frozen["research/r074w_remote_adjacent_inward_comparison_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74W Step 22 independent Ruby verifier reproduces", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074w-remote-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r074w_remote_adjacent_inward_comparison_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R074W_INDEPENDENT_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.groups_passed}/${stdout.groups_total}`, assertions: stdout.assertions },
      { verdict: "PASS", groups: "6/6", assertions: 56 },
    );
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r074w_remote_adjacent_inward_comparison_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74W Step 22 QA preserves fail-closed probability and deletion boundaries", () => {
  const report = bytes("research/r074w_remote_adjacent_inward_comparison_qa_report.md").toString("utf8");
  for (const marker of [
    "33/33 checks, 33 cases",
    "6/6 groups, 56 assertions",
    "23/23 rejected",
    "24/24 rejected",
    "PYTHONHASHSEED 0, 1, 42",
    "whole-shell or fixed-deletion theorem",
  ]) assert.ok(report.includes(marker), marker);
});

test("R0.74W Step 22 frozen figure archive has exact complete hash coverage", () => {
  const archive = resolve(root, "research/figures/r074w", figureId);
  const names = readdirSync(archive).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  const ledgerRows = readFileSync(resolve(archive, "SHA256SUMS"), "utf8").trim().split("\n");
  assert.equal(ledgerRows.length, 24);
  const ledgerNames = [];
  for (const row of ledgerRows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, row);
    assert.equal(sha(`research/figures/r074w/${figureId}/${match[2]}`), match[1], match[2]);
    ledgerNames.push(match[2]);
  }
  assert.deepEqual(ledgerNames, names.filter((name) => name !== "SHA256SUMS"));
  assert.equal(sha(`research/figures/r074w/${figureId}/figure.svg`), "d5d3bb5aa4e407bbbd340482432ab055dd743026bb9286411e23914b1a35adef");
  assert.equal(sha(`research/figures/r074w/${figureId}/figure.png`), "a20af302fa70828f4f9870b2afd14757ac858f30f0f4c618d6aa5af0b2c5b5c6");
  assert.equal(sha(`research/figures/r074w/${figureId}/figure.pdf`), "85c0876206ac0976302858e2f588d7295ed3f2326616228c7394772e4e52a52c");
});
