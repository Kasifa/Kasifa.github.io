import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const readBytes = (path) => readFileSync(resolve(root, path));
const read = (path) => readBytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(readBytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "/Users/kasifa/Documents/Math/.codex-research-venv/bin/python";

test("R0.74S Step 16 imports the exact frozen evidence", () => {
  const hashes = {
    "research/r074s_moving_frame_taylor_vortex_obstruction.md": "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0",
    "research/r074s_moving_frame_taylor_vortex_primary_audit.md": "1140e3f72ddf9565bb6e9c565aaf10de75c8f04b9417ad12e4cddffbabc9a262",
    "research/r074s_moving_frame_taylor_vortex_independent_audit.md": "30af657d18b428fa0355a8cd93a3cf7b7af452588561259ae53a9a734dc55da2",
    "research/r074s_moving_frame_taylor_vortex_certificate.json": "27f93a7e23268be2c337eef6ae0488a8fb60508c51f6dbf12080807e5f636271",
    "research/r074s_moving_frame_taylor_vortex_certificate_report.md": "9b2868d2e9a7cf0bd574ab347d266da1e30a1426c22d48a20f3a472557eab362",
    "scripts/r074s_moving_frame_taylor_vortex_certificate.py": "ec11a53bfc6221344eabd8b809c72deb8996adb56a2da81a6502bc7b914bb54a",
    "scripts/r074s_moving_frame_taylor_vortex_certificate_independent.rb": "9b1fcd3805e162bf7d8f24a2ed0818722dc9413ca709696380d0f02614892677",
  };
  for (const [path, expected] of Object.entries(hashes)) assert.equal(sha(path), expected, path);
});

test("R0.74S Step 16 primary and independent certificates reproduce", () => {
  const primary = JSON.parse(execFileSync(python, ["scripts/r074s_moving_frame_taylor_vortex_certificate.py"], { cwd: root, encoding: "utf8" }));
  assert.equal(primary.verdict, "PASS");
  assert.equal(primary.finite_checks.length, 7);
  assert.equal(primary.finite_checks.reduce((sum, row) => sum + row.cases, 0), 2207);
  assert.equal(primary.structural_checks.length, 7);
  assert.equal(primary.dependency_checks.length, 3);
  assert.equal(primary.claim_boundary.S342_quadratic_tail_for_p_gt_1, "FALSE_BY_SMOOTH_EXACT_NSE");
  assert.equal(primary.claim_boundary.S444_critical_L1_tail, "OPEN");
  assert.equal(primary.claim_boundary.millennium_problem_solved, false);

  const independent = JSON.parse(execFileSync("ruby", ["scripts/r074s_moving_frame_taylor_vortex_certificate_independent.rb"], { cwd: root, encoding: "utf8" }));
  assert.equal(independent.pass, true);
  assert.equal(independent.summary.independent_groups_passed, 9);
  assert.equal(independent.summary.independent_groups_total, 9);
  assert.equal(independent.summary.independent_cases, 2839);
});

test("R0.74S Step 16 public claim boundary, figure, and recap lock are synchronized", () => {
  const note = read("public/notes/r0-74s.html");
  for (const marker of [
    "Taylor 1923",
    "S.417–S.444：PROVED / FALSE / OPEN",
    "fixed-frame Bernoulli flux",
    "Version-M cutoff drift",
    "S.342：FALSE for every",
    "S.444 / S.407：OPEN",
    "Q.12 / Q.1：OPEN",
    "2,207 cases",
    "2,839 cases",
    "11 个外部负探针",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.equal(sha("public/recap-r0-61-r0-74o.html"), "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2");
  assert.equal(sha("public/recap-r0-61-r0-74o.pdf"), "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076");

  for (const extension of ["svg", "pdf", "png"]) {
    const canonical = "research/figures/r074s/fig-r074s-taylor-moving-drift/figure." + extension;
    assert.ok(existsSync(resolve(root, canonical)), canonical);
    assert.equal(sha("public/assets/r074s/fig-r074s-taylor-moving-drift." + extension), sha(canonical));
    assert.equal(sha("public/figures/r074s/fig-r074s-taylor-moving-drift/figure." + extension), sha(canonical));
  }
  const validation = JSON.parse(read("research/figures/r074s/fig-r074s-taylor-moving-drift/validation.json"));
  assert.deepEqual(validation.summary, { result: "PASS", passed: 15, total: 15 });
});

test("R0.74S Step 16 bilingual coverage is complete and local", () => {
  const node = process.env.CODEX_NODE || process.execPath;
  const output = execFileSync(node, ["scripts/add-r074s-step16-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"translationPath": "LOCAL_DIRECT_NO_DGX"/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"checked": 124/);
});
