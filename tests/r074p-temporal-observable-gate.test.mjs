import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { cpSync, mkdirSync, mkdtempSync, readFileSync, readdirSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { basename, dirname, join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const packageRelative = "research/figures/r074p/fig-r074p-observable-triage";
const packageRoot = resolve(root, packageRelative);
const freezePath = resolve(root, "research/r074p_freeze_manifest.json");
const python = process.env.CODEX_PYTHON || process.env.PYTHON || "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const dependencyRoot = process.env.R074P_DEPENDENCIES_ROOT || "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies";

function sha256(bytes) { return createHash("sha256").update(bytes).digest("hex"); }
function fileSha(path) { return sha256(readFileSync(path)); }
function walk(directory) {
  return readdirSync(directory).flatMap((name) => {
    const path = join(directory, name);
    return statSync(path).isDirectory() ? walk(path) : [path];
  });
}

test("R0.74P frozen research package and exact certificates pass", () => {
  assert.equal(fileSha(freezePath), "bdac16d76a0f843adf097d1e412db3cc401d0cecc081b5c0cffc0b4244e4f405");
  const freeze = JSON.parse(readFileSync(freezePath, "utf8"));
  for (const artifact of Object.values(freeze.artifacts)) {
    const path = resolve(root, artifact.path);
    assert.equal(statSync(path).size, artifact.bytes, artifact.path);
    assert.equal(fileSha(path), artifact.sha256, artifact.path);
  }
  const problemTags = new Set(readFileSync(resolve(root, "research/r074p_problem_freeze.md"), "utf8").match(/\\tag\{[^}]+\}/g) ?? []);
  const mainTags = new Set(readFileSync(resolve(root, "research/r074p_temporal_observable_triage.md"), "utf8").match(/\\tag\{[^}]+\}/g) ?? []);
  assert.equal(problemTags.size, 56);
  assert.equal(mainTags.size, 87);

  const produced = execFileSync(python, [resolve(root, "scripts/r074p_temporal_clock_certificate.py")]);
  assert.deepEqual(produced, readFileSync(resolve(root, "research/r074p_temporal_clock_certificate.json")));
  const payload = JSON.parse(produced);
  assert.deepEqual(payload.summary, { passed: 52, total: 52, unique_ids: 52, scale_rows: 4, carleson_rows: 7, l1_l2_rows: 6 });
  assert.equal(payload.result, "PASS");
  const independent = execFileSync("ruby", [resolve(root, "scripts/r074p_temporal_clock_certificate_independent.rb")], { encoding: "utf8" });
  assert.match(independent, /PASS 52\/52/);
});

test("R0.74P formal figure package is sealed and fully reproducible", () => {
  const freeze = JSON.parse(readFileSync(freezePath, "utf8"));
  const figure = freeze.figure_package;
  assert.equal(walk(packageRoot).length, 26);
  const manifest = JSON.parse(readFileSync(resolve(packageRoot, "manifest.json"), "utf8"));
  assert.equal(manifest.artifacts.length, 24);
  assert.equal(manifest.external_bindings.length, 13);
  assert.equal(fileSha(resolve(packageRoot, "figure.svg")), figure.svg_sha256);
  assert.equal(fileSha(resolve(packageRoot, "figure.pdf")), figure.pdf_sha256);
  assert.equal(fileSha(resolve(packageRoot, "figure.png")), figure.png_sha256);
  assert.equal(fileSha(resolve(packageRoot, "source-data.csv")), figure.source_data_sha256);
  assert.equal(readFileSync(resolve(packageRoot, "SHA256SUMS"), "utf8").trim().split("\n").length, 25);
  const validation = JSON.parse(readFileSync(resolve(packageRoot, "validation.json"), "utf8"));
  assert.equal(validation.pass, true);
  assert.equal(validation.check_count, 20);
  assert.ok(validation.checks.every((row) => row.pass));

  const tempRoot = mkdtempSync(join(tmpdir(), "r074p-figure-gate-"));
  const tempPackage = resolve(tempRoot, packageRelative);
  mkdirSync(dirname(tempPackage), { recursive: true });
  cpSync(packageRoot, tempPackage, { recursive: true });
  for (const artifact of Object.values(freeze.artifacts)) {
    const source = resolve(root, artifact.path);
    const target = resolve(tempRoot, artifact.path);
    mkdirSync(dirname(target), { recursive: true });
    cpSync(source, target);
  }
  const env = { ...process.env, R074P_DEPENDENCIES_ROOT: dependencyRoot };
  execFileSync(python, [resolve(tempPackage, "plot.py")], { env, stdio: "pipe" });
  execFileSync(python, [resolve(tempPackage, "validate.py")], { env, stdio: "pipe" });
  const originals = walk(packageRoot).sort((left, right) => {
    const leftName = basename(left);
    const rightName = basename(right);
    if (leftName === "SHA256SUMS") return 1;
    if (rightName === "SHA256SUMS") return -1;
    return left.localeCompare(right);
  });
  for (const original of originals) {
    const name = original.slice(packageRoot.length + 1);
    const actual = readFileSync(resolve(tempPackage, name));
    const expected = readFileSync(original);
    assert.equal(
      sha256(actual),
      sha256(expected),
      `regenerated byte drift: ${name}; expected sha256=${sha256(expected)}, actual sha256=${sha256(actual)}`,
    );
    assert.deepEqual(actual, expected, `regenerated byte drift: ${name}`);
  }
});
