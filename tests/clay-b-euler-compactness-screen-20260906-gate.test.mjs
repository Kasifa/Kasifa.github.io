import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("EulerCompactnessScreen ledger binds the 14+90 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_euler_compactness_screen_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-euler-compactness-screen-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-EulerCompactnessScreen-20260906");
  assert.equal(ledger.sourceCommit, "14d5a44345c6835aff8dfd19123c979ae185b471");
  assert.equal(ledger.baseCommit, "b85838c7139c7e6e248d3c1dfebd0866a92a166a");
  assert.equal(ledger.freezeCommit, "e22c9a5669dbc3cc29fa2e0d313d3656836774c2");
  assert.equal(ledger.scientificFileCount, 14);
  assert.equal(ledger.dependencyFileCount, 90);
  assert.equal(ledger.verifiedFileCount, 104);
  assert.equal(ledger.textSourceFileCount, 5);
  assert.equal(ledger.formulaTagCount, 48);
  assert.equal(ledger.newFormulaTagCount, 36);
  assert.equal(ledger.arithmeticCheckCount, 20);
  assert.equal(ledger.negativeControlCount, 3);
  assert.equal(ledger.previousFrozenRowCount, 89);
  assert.equal(ledger.historicalStageFileCount, 6);
  assert.equal(ledger.files.length, 104);
  assert.equal(new Set(ledger.files.map((row) => row.path)).size, 104);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_euler_compactness_screen_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-FixedHistoryScreen-20260906");
  assert.equal(manifest.status, "RESEARCH_COMPLETE");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_PDF, false);
  assert.equal(manifest.recap.update_required, false);
  assert.deepEqual(manifest.excluded_user_paths, ["AGENTS.md"]);
});

test("BK through BN retain 48 continuous labels and the exact conditional chain", () => {
  const sources = [
    ["research/clay_b_euler_scaling_energy_preflight_20260906.md", "BK", 12],
    ["research/clay_b_critical_euler_compactness_20260906.md", "BL", 20],
    ["research/clay_b_euler_rigidity_energy_atom_20260906.md", "BM", 8],
    ["research/clay_b_periodic_no_atom_endpoint_20260906.md", "BN", 8],
  ];
  for (const [path, prefix, count] of sources) {
    const body = read(path);
    const tags = [...body.matchAll(new RegExp(`\\\\tag\\{(${prefix}\\.\\d+)\\}`, "g"))].map((match) => match[1]);
    assert.deepEqual(tags, Array.from({ length: count }, (_, index) => `${prefix}.${index + 1}`), path);
  }
  const joined = sources.map(([path]) => read(path)).join("\n");
  for (const marker of [
    "额外假设", "规范周期压力", "局部能量等式", "不声称全空间能量守恒",
    "Gavrilov", "反例不是 NS 解序列", "epsilon_*^4", "条件必要",
    "11/3", "-\\frac3{10}", "-\\frac9{20}", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});

test("source QA preserves exact arithmetic, historical-stage, literature, and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_euler_compactness_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 5);
  assert.equal(qa.new_formula_tags_checked, 36);
  assert.equal(qa.combined_BK_BN_tags, 48);
  assert.equal(qa.arithmetic_checks.length, 20);
  assert.ok(qa.arithmetic_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 89);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.previous_internal_stage.files.length, 6);
  assert.ok(qa.previous_internal_stage.files.every((row) => row.unchanged));
  assert.ok(Object.values(qa.limited_negative_controls).every(Boolean));
  assert.equal(qa.protected_state.user_agents_unchanged, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");

  const joined = [
    "research/clay_b_euler_compactness_primary_reading_20260906.md",
    "research/clay_b_euler_compactness_report_20260906.md",
    "research/clay_b_euler_compactness_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "没有进行穷尽性新颖性检索", "不是固定初值 NS 缩放可达性", "外部同行评审",
    "压力输入可以删去，刚性出口仍未成立", "G、原 NS 输入生成", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
