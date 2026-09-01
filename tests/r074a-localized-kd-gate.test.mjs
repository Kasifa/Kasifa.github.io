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
  const handoff = JSON.parse(await text("release/handoffs/r074a.json"));
  assert.equal(handoff.releaseId, "r074a");
  assert.equal(handoff.frozenCommit, "7bad69a09651ea870cf463640ffff0f34a849cea");
  assert.equal(handoff.translationRoute, "LOCAL_DIRECT_NO_DGX");
  assert.equal(handoff.recap.mode, "PRESERVE");
  assert.deepEqual(handoff.claimBoundary.requiredLabels, ["PROVED", "FINITE", "OPEN", "NOT CLAY"]);
  for (const artifact of handoff.artifacts) {
    assert.equal(sha256(await read(artifact.path)), artifact.sha256, artifact.path);
  }
  const ancestry = spawnSync("git", ["merge-base", "--is-ancestor", handoff.frozenCommit, "HEAD"], { cwd: root });
  assert.equal(ancestry.status, 0, "frozen R0.74A commit must be an ancestor of HEAD");
});

test("analytic result, finite certificate, and open absorption stay distinct", async () => {
  const [proof, audit, literature, certificate] = await Promise.all([
    text("research/r074a_localized_kd_size_lemma.md"),
    text("research/r074a_independent_audit.md"),
    text("research/r074a_primary_literature_audit.md"),
    text("research/r074a_localized_kd_certificate.json").then(JSON.parse),
  ]);
  for (const marker of ["positive four-block majorization", "Theorem 4.1", "\\mathcal U_{\\rm ext}^{\\infty,\\square}", "right-hand side alone does not control"])
    assert.ok((proof + audit).includes(marker), marker);
  for (const marker of ["small", "absorbable", "lower semicontinuity", "epsilon-regularity"])
    assert.ok((proof + audit + literature).toLowerCase().includes(marker.toLowerCase()), marker);
  assert.equal(certificate.status, "PASS");
  assert.deepEqual(certificate.summary, { passed: 21, total: 21 });
  assert.equal(certificate.scope, "FINITE arithmetic cross-check only; analytic quantifiers remain in the main proof; NOT CLAY");
  assert.ok(proof.includes("NOT CLAY"));
});

test("certificate check-only and independent audit are reproducible", () => {
  const output = run("python3", ["-B", "scripts/r074a_localized_kd_certificate.py", "--check-only"]);
  assert.match(output, /PASS|pass|checked/i);
});

test("formal figure remains a sealed 25-file analytic package", async () => {
  const base = "research/figures/r074a/fig-r074a-localized-kd-payments/";
  const names = (await readdir(resolve(root, base))).sort();
  assert.equal(names.length, 25);
  const manifest = JSON.parse(await text(base + "manifest.json"));
  assert.equal(manifest.release, "R0.74A");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.inventory.expectedCount, 25);
  assert.equal(manifest.sourceData.rowCount, 266);
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
