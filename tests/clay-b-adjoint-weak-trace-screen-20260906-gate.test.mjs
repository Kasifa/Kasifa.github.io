import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("AdjointWeakTraceScreen ledger binds the 6+129 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_adjoint_weak_trace_screen_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-adjoint-weak-trace-screen-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-AdjointWeakTraceScreen-20260906");
  assert.equal(ledger.sourceCommit, "65de3e3b22be98d65fc32a47b56394e22a050f75");
  assert.equal(ledger.baseCommit, "82b5d1f5a11c13a87151b08d17d6dfe674a89641");
  assert.equal(ledger.freezeCommit, "456e5c4c28f7e63ec3e84cbf2b8e0fbb516a5819");
  assert.equal(ledger.scientificFileCount, 6);
  assert.equal(ledger.dependencyFileCount, 129);
  assert.equal(ledger.verifiedFileCount, 135);
  assert.equal(ledger.textSourceFileCount, 3);
  assert.equal(ledger.formulaTagCount, 18);
  assert.equal(ledger.arithmeticCheckCount, 15);
  assert.equal(ledger.negativeControlCount, 3);
  assert.equal(ledger.previousFrozenRowCount, 125);
  assert.equal(ledger.additionalHistoricalSourceCount, 3);
  assert.equal(ledger.files.length, 135);
  assert.equal(new Set(ledger.files.map((row) => row.path)).size, 135);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_adjoint_weak_trace_screen_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-CommonAdjointScreen-20260906");
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

test("BS retains 18 continuous labels and the exact conditional endpoint chain", () => {
  const body = read("research/clay_b_adjoint_weak_trace_20260906.md");
  const tags = [...body.matchAll(/\\tag\{(BS\.\d+)\}/g)].map((match) => match[1]);
  assert.deepEqual(tags, Array.from({ length: 18 }, (_, index) => `BS.${index + 1}`));
  for (const marker of [
    "反时场", "弱零初态", "没有额外向量", "lim_{N\\to\\infty}", "\\tfrac12\\eta(0)",
    "Radon 测度", "没有证明", "一致可积", "L^2(0,\\delta;H^{-1}_\\sigma)",
    "Serrin", "额外", "不宣称新颖性", "NOT CLAY",
  ]) assert.ok(body.includes(marker), marker);
});

test("source QA preserves arithmetic, predecessor freeze, literature scope, and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_adjoint_trace_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 3);
  assert.equal(qa.formula_tags_checked, 18);
  assert.equal(qa.arithmetic_checks.length, 15);
  assert.ok(qa.arithmetic_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 125);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.historical_sources.rows.length, 3);
  assert.ok(qa.historical_sources.rows.every((row) => row.pass));
  assert.equal(qa.previous_saved_QA_live_identical, true);
  assert.ok(Object.values(qa.limited_negative_controls).every(Boolean));
  assert.equal(qa.protected_state.user_agents_unchanged, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");
  assert.equal(qa.clay_result, false);

  const joined = [
    "research/clay_b_adjoint_trace_primary_reading_20260906.md",
    "research/clay_b_adjoint_trace_report_20260906.md",
    "research/clay_b_adjoint_trace_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "Theorems A.1--A.3", "C_tL^3", "不是穷尽检索", "不是外部同行评审",
    "压力感知的凸测试", "尚未开始", "正原子", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
