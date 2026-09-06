import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("CommonAdjointScreen ledger binds the 8+117 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_common_adjoint_screen_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-common-adjoint-screen-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-CommonAdjointScreen-20260906");
  assert.equal(ledger.sourceCommit, "32b12bff99e7a88d6be3d1317fd125cf30a72792");
  assert.equal(ledger.baseCommit, "7ea29a64cc1ba081e703afec4b59b3adeb9758da");
  assert.equal(ledger.freezeCommit, "2a2b6c9ee51cab238b11b485ae1b6b5564a75395");
  assert.equal(ledger.scientificFileCount, 8);
  assert.equal(ledger.dependencyFileCount, 117);
  assert.equal(ledger.verifiedFileCount, 125);
  assert.equal(ledger.textSourceFileCount, 5);
  assert.equal(ledger.formulaTagCount, 57);
  assert.equal(ledger.arithmeticCheckCount, 31);
  assert.equal(ledger.negativeControlCount, 3);
  assert.equal(ledger.previousFrozenRowCount, 115);
  assert.equal(ledger.additionalHistoricalSourceCount, 1);
  assert.equal(ledger.files.length, 125);
  assert.equal(new Set(ledger.files.map((row) => row.path)).size, 125);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_common_adjoint_screen_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-EnergyAtomCostScreen-20260906");
  assert.equal(manifest.status, "RESEARCH_COMPLETE");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_PDF, false);
  assert.equal(manifest.compute.third_party_PDF_redistribution, false);
  assert.equal(manifest.recap.update_required, false);
  assert.deepEqual(manifest.excluded_user_paths, ["AGENTS.md"]);
});

test("BP through BR retain 57 continuous labels and the exact conditional chain", () => {
  const sources = [
    ["research/clay_b_common_adjoint_full_tail_20260906.md", "BP", 32],
    ["research/clay_b_full_tail_second_order_20260906.md", "BQ", 13],
    ["research/clay_b_operator_budget_strength_20260906.md", "BR", 12],
  ];
  for (const [path, prefix, count] of sources) {
    const body = read(path);
    const tags = [...body.matchAll(new RegExp(`\\\\tag\\{(${prefix}\\.\\d+)\\}`, "g"))].map((match) => match[1]);
    assert.deepEqual(tags, Array.from({ length: count }, (_, index) => `${prefix}.${index + 1}`), path);
  }
  const joined = sources.map(([path]) => read(path)).join("\n");
  for (const marker of [
    "LITERATURE RECONSTRUCTION", "正原子是条件", "共同伴随", "弱零终端迹",
    "最终保留链", "不是所有连续时间对", "二阶作用无限", "不是与基本能量的矛盾",
    "已经与固定周期原解", "不宣称新颖性", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});

test("source QA preserves exact arithmetic, prior freeze, history, and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_common_adjoint_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 5);
  assert.equal(qa.formula_tags_checked, 57);
  assert.equal(qa.arithmetic_checks.length, 31);
  assert.ok(qa.arithmetic_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 115);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.historical_sources.rows.length, 1);
  assert.ok(qa.historical_sources.rows.every((row) => row.pass));
  assert.equal(qa.previous_saved_QA_live_identical, true);
  assert.ok(Object.values(qa.limited_negative_controls).every(Boolean));
  assert.equal(qa.protected_state.user_agents_unchanged, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");
  assert.equal(qa.clay_result, false);

  const joined = [
    "research/clay_b_common_adjoint_primary_reading_20260906.md",
    "research/clay_b_common_adjoint_report_20260906.md",
    "research/clay_b_common_adjoint_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "20 页没有读", "Appendix A", "不是外部同行评审", "不宣称新颖性",
    "终端唯一性", "尚未开始", "没有证明其中任一条件", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
