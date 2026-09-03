import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const read = (path) => bytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "python3";

const frozen = {
  "research/r075b_bulk_clock_outer_padding_gate.md": "430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a",
  "research/r075b_bulk_clock_outer_padding_gate_primary_audit.md": "8f4c2b6c28c63acce86a191ec3bc32602ce9e64e3df80eef8534f2e15a255209",
  "research/r075b_literature_collision_note.md": "6cef708d967fc0e7f47bc87d14496a1d2ff67aa6101a49ebe0f29c4f2d7a023a",
  "research/r075b_bulk_clock_outer_padding_gate_certificate.json": "04ba3c9971defcf87971fc1d7722ca925074445826c437da9baa5438b9b4d0c0",
  "research/r075b_bulk_clock_outer_padding_gate_certificate_report.md": "ae5f533e57e4588b1d973a1abb34fbde3f9547f01577be8f8121b840d3e44ae2",
  "research/r075b_bulk_clock_outer_padding_gate_independent_audit.md": "9d18cc14a72030e6e98d17f9f51ef26515ceecebd80b020ef0c86d1d74715c7f",
  "research/r075b_bulk_clock_outer_padding_gate_qa_report.md": "14e6d7159d32b3b11c58651e3e89513f46d69f0ebc40c4ec8a76e4cae2db6a45",
  "scripts/r075b_bulk_clock_outer_padding_gate_certificate.py": "35cd3e2608fe143a4c092e48e16563b237fe39622bd06b5712f6b5eae18b9a08",
  "scripts/r075b_bulk_clock_outer_padding_gate_certificate_independent.rb": "0004da4bc794a6dbc844529db6c0e572e5ad05d9ee9948aaf82ef95ae6f72146",
  "scripts/r075b_bulk_clock_outer_padding_gate_qa.sh": "8ab21a4b11c4d56e88e7e405acbc9cf6d748a276d304336b10d3cd32f5226794",
};

test("R0.75B Step 27 frozen whitelist has exactly ten byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 10);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75B Step 27 Python certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075b-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r075b_bulk_clock_outer_padding_gate_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075B_JSON: join(outputRoot, "certificate.json"),
        R075B_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { checks: 8, mutation: null, tags: 47, verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075b_bulk_clock_outer_padding_gate_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075b_bulk_clock_outer_padding_gate_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75B Step 27 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075b-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075b_bulk_clock_outer_padding_gate_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R075B_RUBY_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(stdout, { verdict: "PASS", assertions: 9, mutation: null });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075b_bulk_clock_outer_padding_gate_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75B QA closes the finite gate and preserves the analytic stop line", () => {
  const qa = read("research/r075b_bulk_clock_outer_padding_gate_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 8/8",
    "Ruby assertions: 9/9",
    "20/20 and 21/21",
    "PYTHONHASHSEED byte stability: PASS",
    "outer accumulated dissipation and full clock remain OPEN",
    "method failure, not counterexample",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, `${path}: carriage return`);
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, `${path}: control character`);
  }
});
