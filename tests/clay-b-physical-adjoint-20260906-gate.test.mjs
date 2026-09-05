import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("PhysicalAdjoint ledger binds the 5+2 scientific package and 2-file handoff envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_physical_adjoint_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-physical-adjoint-frozen-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-PhysicalAdjoint-20260906");
  assert.equal(ledger.sourceRepository, "navier-stokes-r074m");
  assert.equal(ledger.sourceCommit, "ed51a0e43c9de159c0388218b0b45cf3b83c6578");
  assert.equal(ledger.handoffCommit, "7cb9b74effa96fa4c9a4c04abcfa48e16fa40461");
  assert.equal(ledger.scientificFileCount, 5);
  assert.equal(ledger.dependencyFileCount, 2);
  assert.equal(ledger.files.length, 7);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_physical_adjoint_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.source_commit, ledger.sourceCommit);
  assert.equal(manifest.status, "research-frozen");
  assert.equal(manifest.claim_boundaries.NOT_CLAY, true);
  assert.equal(manifest.claim_boundaries.novelty_claimed, false);
  assert.equal(manifest.counterexample_scope.uniform_initial_L2, false);
  assert.equal(manifest.counterexample_scope.uniform_initial_H1, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.scientific_figure_required, false);
  assert.equal(manifest.simulation_required, false);
  assert.equal(manifest.recap_required, false);
  assert.equal(manifest.publication.generate_new_pdf, false);
});

test("analytic sources preserve B.1-B.16, C.1-C.6 and the strict weak-endpoint boundary", () => {
  const budget = read("research/clay_b_physical_adjoint_budget_20260905.md");
  const shear = read("research/clay_b_physical_adjoint_shear_20260905.md");
  const report = read("research/clay_b_physical_adjoint_report-source_20260905.md");
  for (let index = 1; index <= 16; index += 1) assert.match(budget, new RegExp(`\\\\tag\\{B\\.${index}\\}`));
  for (let index = 1; index <= 6; index += 1) assert.match(shear, new RegExp(`\\\\tag\\{C\\.${index}\\}`));
  for (const marker of [
    "右侧强 \\(L^2\\) Bochner Lebesgue 点",
    "弱下半连续性",
    "D_J/R",
    "不能保证",
    "R.216--R.217",
  ]) assert.ok(budget.includes(marker), marker);
  for (const marker of ["不统一初始", "固定", "首次奇点", "最优性证明"]) {
    assert.ok(`${shear}\n${report}`.includes(marker), marker);
  }
});

test("independent audit records three actual-file passes without expanding the claim", () => {
  const audit = read("research/clay_b_physical_adjoint_independent_audit_20260906.md");
  for (const marker of [
    "PASS，无必改数学问题",
    "终点弱下半连续缺口一般不能识别为 defect 测度的时间原子",
    "Chebyshev 只给提升质量尾界",
    "不需要科学图表、仿真或数值证书",
    "无新颖性声明",
  ]) assert.ok(audit.includes(marker), marker);
});
