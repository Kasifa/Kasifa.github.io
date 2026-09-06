import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("LaggedPressureReduction ledger binds the 10+41 package and one-file frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_lagged_pressure_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-lagged-pressure-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-LaggedPressureReduction-20260906");
  assert.equal(ledger.sourceCommit, "891e6b85f53ae19272973c191726f1278e47918b");
  assert.equal(ledger.baseCommit, "299a3b4e7deab8f561c83559c13741aaa5137343");
  assert.equal(ledger.freezeCommit, "3501cf9d70cbb5140186bb18d0cf1da8c110480f");
  assert.equal(ledger.scientificFileCount, 10);
  assert.equal(ledger.dependencyFileCount, 41);
  assert.equal(ledger.verifiedFileCount, 51);
  assert.equal(ledger.formulaTagCount, 98);
  assert.equal(ledger.files.length, 51);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_lagged_pressure_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-PressureTestCoupling-20260906");
  assert.equal(manifest.status, "research-frozen");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_pdf, false);
  assert.equal(manifest.recap.update, false);
});

test("AY through BB preserve all 98 unique formula tags and the pressure-payment boundaries", () => {
  const sourcePaths = [
    "research/clay_b_time_ordered_pressure_preflight_20260906.md",
    "research/clay_b_joint_early_heat_work_preflight_20260906.md",
    "research/clay_b_lagged_heat_pressure_reduction_preflight_20260906.md",
    "research/clay_b_lag_scale_pressure_budget_preflight_20260906.md",
  ];
  const expectedTagCounts = [33, 23, 17, 25];
  const sources = sourcePaths.map(read);
  const tagsBySource = sources.map((source) => [...source.matchAll(/\\tag\{([A-Z]+\.\d+)\}/g)].map((match) => match[1]));
  assert.deepEqual(tagsBySource.map((tags) => tags.length), expectedTagCounts);
  const tags = tagsBySource.flat();
  assert.equal(tags.length, 98);
  assert.equal(new Set(tags).size, 98);
  const joined = sources.join("\n");
  for (const marker of [
    "本稿不重选 \\(a\\)", "不把新时刻冒充 AQ 原来的", "不证明旧压力功本身为 o(H_t)",
    "耗散份额 epsilon 是真实成本", "不是任意小残差", "不是必要尺度", "不是最优性结论",
    "BB.25 不是对源—源压力的",
  ]) assert.ok(joined.includes(marker), marker);
});

test("source QA, report, literature scope, and audit retain finite-check and open-claim limits", () => {
  const qa = JSON.parse(read("research/clay_b_lagged_pressure_source_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.source_file_count, 8);
  assert.equal(qa.formula_tag_total, 98);
  assert.deepEqual(qa.failures, []);
  assert.equal(qa.previous_release_manifest.hash_rows, 37);

  const joined = [
    "research/clay_b_lagged_pressure_report_20260906.md",
    "research/clay_b_lagged_pressure_internal_audit_20260906.md",
    "research/clay_b_lagged_pressure_literature_scope_20260906.md",
    "research/clay_b_recent_source_work_plan_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "不是必要尺度或最优尺度", "不等于外部同行评审", "没有做穷尽检索",
    "剩余 5/8 中扣除", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
