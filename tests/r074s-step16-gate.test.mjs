import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync, spawnSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "python3";

function runPrimaryCertificate() {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074s-taylor-primary-"));
  try {
    return JSON.parse(execFileSync(python, ["scripts/r074s_moving_frame_taylor_vortex_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074S_TAYLOR_JSON: join(outputRoot, "certificate.json"),
        R074S_TAYLOR_REPORT: join(outputRoot, "certificate-report.md"),
      },
    }));
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
}

function runIndependentCertificate() {
  const result = spawnSync("ruby", ["scripts/r074s_moving_frame_taylor_vortex_certificate_independent.rb"], {
    cwd: root,
    encoding: "utf8",
  });
  assert.equal(result.error, undefined, result.error?.message);
  const payload = JSON.parse(result.stdout);
  const failed = [
    ...payload.independent_checks,
    ...payload.artifacts,
    ...payload.note_checks,
    ...payload.primary_artifact_checks,
    ...payload.negative_mutation_checks,
  ].filter((row) => !row.pass);
  assert.equal(result.status, 0, JSON.stringify({ stderr: result.stderr, failed }, null, 2));
  return payload;
}

test("R0.74S Step 16 exact frozen source lock and certificate boundary", () => {
  const locks = {
    "research/r074s_moving_frame_taylor_vortex_obstruction.md": "de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0",
    "research/r074s_moving_frame_taylor_vortex_primary_audit.md": "1140e3f72ddf9565bb6e9c565aaf10de75c8f04b9417ad12e4cddffbabc9a262",
    "research/r074s_moving_frame_taylor_vortex_independent_audit.md": "30af657d18b428fa0355a8cd93a3cf7b7af452588561259ae53a9a734dc55da2",
    "research/r074s_moving_frame_taylor_vortex_certificate.json": "27f93a7e23268be2c337eef6ae0488a8fb60508c51f6dbf12080807e5f636271",
    "research/r074s_moving_frame_taylor_vortex_certificate_report.md": "9b2868d2e9a7cf0bd574ab347d266da1e30a1426c22d48a20f3a472557eab362",
    "scripts/r074s_moving_frame_taylor_vortex_certificate.py": "ec11a53bfc6221344eabd8b809c72deb8996adb56a2da81a6502bc7b914bb54a",
    "scripts/r074s_moving_frame_taylor_vortex_certificate_independent.rb": "9b1fcd3805e162bf7d8f24a2ed0818722dc9413ca709696380d0f02614892677",
  };
  for (const [path, expected] of Object.entries(locks)) assert.equal(sha(path), expected, path);

  const primary = runPrimaryCertificate();
  assert.equal(primary.verdict, "PASS");
  assert.equal(primary.finite_checks.length, 7);
  assert.equal(primary.finite_checks.reduce((sum, row) => sum + row.cases, 0), 2207);
  assert.equal(primary.claim_boundary.S342_quadratic_tail_for_p_gt_1, "FALSE_BY_SMOOTH_EXACT_NSE");
  assert.equal(primary.claim_boundary.S444_critical_L1_tail, "OPEN");

  const independent = runIndependentCertificate();
  assert.equal(independent.pass, true);
  assert.deepEqual(
    [
      independent.summary.independent_groups_passed,
      independent.summary.independent_groups_total,
      independent.summary.independent_cases,
    ],
    [9, 9, 2839],
  );
});
