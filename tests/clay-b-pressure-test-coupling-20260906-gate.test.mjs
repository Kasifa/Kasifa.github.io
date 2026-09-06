import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("PressureTestCoupling ledger binds the 12+25 package and 2-file frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_pressure_test_coupling_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-pressure-test-coupling-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-PressureTestCoupling-20260906");
  assert.equal(ledger.sourceCommit, "ebaf7e8a51cf08f890caf727850f1b65d6fbd0fd");
  assert.equal(ledger.baseCommit, "e887f8fdfee7f1e88d5724d1233832db39fbf1bf");
  assert.equal(ledger.freezeCommit, "2e3706c5fe1f43586b1e9a59a24cb41d04935c9a");
  assert.equal(ledger.scientificFileCount, 12);
  assert.equal(ledger.dependencyFileCount, 25);
  assert.equal(ledger.formulaTagCount, 202);
  assert.equal(ledger.files.length, 37);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }
  const manifest = JSON.parse(read("research/clay_b_pressure_test_coupling_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-BadTimeNetWork-20260906");
  assert.equal(manifest.status, "research-frozen");
  assert.equal(manifest.claim_boundaries.NOT_CLAY, true);
  assert.equal(manifest.claim_boundaries.novelty_claimed, false);
  assert.deepEqual(manifest.claim_boundaries.FINITE_COMPUTATION, []);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.scientific_figure_required, false);
  assert.equal(manifest.simulation_required, false);
  assert.equal(manifest.recap_required, false);
  assert.equal(manifest.publication.generate_new_reader_pdf, false);
});

test("AR through AX preserve all 202 unique formula tags and the test-coupling distinction", () => {
  const sourcePaths = [
    "research/clay_b_pressure_output_reduction_preflight_20260906.md",
    "research/clay_b_dyadic_pressure_ledger_preflight_20260906.md",
    "research/clay_b_global_tail_persistence_preflight_20260906.md",
    "research/clay_b_local_tail_persistence_preflight_20260906.md",
    "research/clay_b_signed_work_route_screen_20260906.md",
    "research/clay_b_exact_pressure_symbol_preflight_20260906.md",
    "research/clay_b_pressure_angular_cost_obstruction_20260906.md",
  ];
  const expectedTagCounts = [21, 37, 32, 37, 11, 44, 20];
  const sources = sourcePaths.map(read);
  const tagsBySource = sources.map((source) => [...source.matchAll(/\\tag\{([A-Z]+\.\d+)\}/g)].map((match) => match[1]));
  assert.deepEqual(tagsBySource.map((tags) => tags.length), expectedTagCounts);
  const tags = tagsBySource.flat();
  assert.equal(tags.length, 202);
  assert.equal(new Set(tags).size, 202);
  const joined = sources.join("\n");
  for (const marker of [
    "在同一坏时间上移项", "不是 NS 必须满足的速率",
    "这个例子的压力恰为零", "不是实际 NS 的必要条件",
    "不是一般 NS 带符号方法的", "保留了原测试输出频率",
    "没有估计最终测试因子，也不是压力功",
  ]) assert.ok(joined.includes(marker), marker);
});

test("report and audits keep sufficient-cost, static-field, trajectory, and novelty boundaries", () => {
  const joined = [
    "research/clay_b_pressure_test_coupling_report_20260906.md",
    "research/clay_b_pressure_geometry_history_scope_20260906.md",
    "research/clay_b_time_ordered_pressure_work_plan_20260906.md",
    "research/clay_b_pressure_test_coupling_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "不证明这种序列存在", "不是压力工作或同一条 NS 轨道的反例",
    "正是这里保留的最终测试配对", "充分条件，不是实际 NS 或带符号净功的必要条件",
    "Duhamel 恒等式本身不算新的净功估计", "不是外部同行评审或新颖性审查",
  ]) assert.ok(joined.includes(marker), marker);
});
