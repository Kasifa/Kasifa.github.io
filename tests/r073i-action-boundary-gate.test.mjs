import assert from "node:assert/strict";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.CODEX_PYTHON ?? "python3";
const read = (relative) => readFile(resolve(root, relative), "utf8");
const json = (relative) => read(relative).then(JSON.parse);

test("R0.73I exact sources keep the fixed-window claim fail-closed", async () => {
  const [freeze, upper, tangent, noGo, gap, report] = await Promise.all([
    read("research/r073i_problem_freeze.md"),
    read("research/r073i_continuum_upper_action_proof.md"),
    read("research/r073i_zero_window_tangent_proof.md"),
    read("research/r073i_fixed_window_no_go.md"),
    read("research/r073i_gap_matrix.md"),
    read("research/r073i_report-source.md"),
  ]);
  const all = [freeze, upper, tangent, noGo, gap, report].join("\n");
  for (const token of [
    "sqrt{19/180}}{392}",
    "\\Omega_H(D)",
    "-\\frac D4",
    "zero-window",
    "FALSE AS INFERENCE",
    "matchingSelectedGainAction",
  ]) assert.ok(all.includes(token), token);
  assert.match(gap, /`inheritedEndpointStrictlyBelowOneOver450` \| CLOSED/);
  assert.match(gap, /`improvedContinuumUpperAction` \| CLOSED/);
  assert.match(gap, /`zeroWindowTangentAction` \| CLOSED/);
  assert.match(gap, /`fixedWindowActionFromInheritedInputs` \| FALSE AS INFERENCE/);
  assert.match(gap, /`matchingSelectedGainAction` \| OPEN/);
  assert.match(gap, /`Clay` \| OPEN/);
  assert.doesNotMatch(report, /finite (?:Fourier|WKB)[^\n]{0,100}(?:proves|certifies) (?:the )?continuum/i);
});

test("R0.73I certificate separates exact, finite, and open claims", async () => {
  const directory = "research/certificates/r073i";
  const [certificate, independent, validation, manifest, finite] = await Promise.all([
    json(`${directory}/certificate.json`),
    json(`${directory}/independent_recompute.json`),
    json(`${directory}/validation.json`),
    json(`${directory}/manifest.json`),
    json("experiments/r073i/summary.json"),
  ]);
  assert.equal(certificate.schemaVersion, "r073i-exact-certificate-v1");
  assert.equal(certificate.allChecksPass, true);
  assert.equal(independent.allChecksPass, true);
  assert.equal(validation.allChecksPass, true);
  assert.equal(manifest.allPrerequisiteChecksPass, true);
  assert.equal(certificate.claimLedger.improvedContinuumUpperAction, "CLOSED");
  assert.equal(certificate.claimLedger.zeroWindowTangentAction, "CLOSED");
  assert.equal(certificate.claimLedger.matchingSelectedGainAction, "OPEN");
  assert.equal(certificate.claimLedger.Clay, "OPEN");
  assert.equal(finite.diagnosticOnly, true);
  assert.equal(finite.claimBoundary.finiteActionIsContinuumAction, false);
  assert.equal(finite.claimBoundary.finiteWkbCorrectionIsAsymptoticTheorem, false);

  const checked = spawnSync(python, [
    `${directory}/validate_certificate.py`,
    "--directory", directory,
    "--root", ".",
  ], { cwd: root, encoding: "utf8" });
  assert.equal(checked.status, 0, checked.stderr || checked.stdout);
  assert.equal(JSON.parse(checked.stdout).allChecksPass, true);

  const names = (await readdir(resolve(root, directory))).sort();
  assert.ok(names.includes("SHA256SUMS"));
  assert.ok(names.includes("manifest.json"));
});
