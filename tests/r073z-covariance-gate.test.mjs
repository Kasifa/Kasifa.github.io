import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

function run(command, arguments_) {
  const completed = spawnSync(command, arguments_, {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.equal(completed.status, 0, completed.stderr || completed.stdout);
  return completed.stdout;
}

test("frozen handoff bytes and original ancestry remain intact", async () => {
  const handoff = JSON.parse(await text("release/handoffs/r073z.json"));
  assert.equal(handoff.releaseId, "r073z");
  assert.equal(handoff.frozenCommit, "845a8b825f06513c454807ae770bcaee6d0d3b04");
  assert.equal(handoff.translationRoute, "LOCAL_DIRECT_NO_DGX");
  assert.equal(handoff.recap.mode, "PRESERVE");
  assert.deepEqual(handoff.claimBoundary.requiredLabels, ["PROVED", "FINITE", "OPEN", "NOT CLAY"]);
  for (const artifact of handoff.artifacts) {
    assert.equal(sha256(await read(artifact.path)), artifact.sha256, artifact.path);
  }
  const ancestry = spawnSync("git", ["merge-base", "--is-ancestor", handoff.frozenCommit, "HEAD"], { cwd: root });
  assert.equal(ancestry.status, 0, "frozen R0.73Z commit must be an ancestor of HEAD");
});

test("analytic result, finite certificate, and open bridge stay distinct", async () => {
  const [proof, pressure, matrix, report, certificate] = await Promise.all([
    text("research/r073z_finiteness_obstruction_and_repair.md"),
    text("research/r073z_pressure_active_kernel.md"),
    text("research/r073z_evidence_gap_matrix.md"),
    text("research/r073z_report-source.md"),
    text("research/r073z_covariance_certificate.json").then(JSON.parse),
  ]);
  for (const marker of ["D_{ii,s}^{3/2}", "FALSE BY EXACT LERAY--HOPF SHEAR", "D_s\\sqrt{k_s}", "OPEN HIGH-VALUE TARGET"])
    assert.ok((proof + matrix).includes(marker), marker);
  for (const marker of ["pressure-active", "\\Pi_s=\\mathscr S_s=0", "Q_s", "local pressure-cutoff debt"])
    assert.ok((pressure + report).includes(marker), marker);
  assert.equal(certificate.claim_boundary.notClay, true);
  assert.equal(certificate.claim_boundary.clayProblemSolved, false);
  assert.equal(certificate.claim_boundary.epsilonRegularity, "OPEN");
  assert.ok(report.includes("bounded non-hit"));
  assert.ok(report.includes("不能写成 novelty proof"));
  assert.ok(report.includes("NOT CLAY"));
});

test("certificate check-only and independent audit are reproducible", () => {
  const output = run("python3", ["-B", "scripts/r073z_covariance_certificate.py", "--check-only"]);
  assert.match(output, /PASS|pass|checked/i);
});

test("formal figure remains a sealed 25-file analytic package", async () => {
  const base = "research/figures/r073z/fig-r073z-covariance-separation/";
  const names = (await readdir(resolve(root, base))).sort();
  assert.equal(names.length, 25);
  const manifest = JSON.parse(await text(base + "manifest.json"));
  assert.equal(manifest.release, "R0.73Z");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.inventory.expectedCount, 25);
  assert.equal(manifest.sourceData.rowCount, 201);
  assert.equal(manifest.claimBoundary.directNumericalSimulation, false);
  assert.equal(manifest.claimBoundary.notClay, true);
  assert.equal(manifest.validation.status, "PASS");
  assert.equal(manifest.validation.visualQaConfirmed, true);
  const sourceCommit = manifest.sourceEvidence.commit;
  for (const [path, digest] of Object.entries(manifest.sourceEvidence.files)) {
    const historical = spawnSync("git", ["show", `${sourceCommit}:${path}`], { cwd: root });
    assert.equal(historical.status, 0, path);
    assert.equal(sha256(historical.stdout), digest, path);
    assert.equal(sha256(await read(path)), digest, path + " current bytes");
  }
});
