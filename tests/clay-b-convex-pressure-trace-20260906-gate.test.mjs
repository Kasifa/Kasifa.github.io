import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("ConvexPressureTrace ledger binds the 6+136 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_convex_pressure_trace_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-convex-pressure-trace-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-ConvexPressureTrace-20260906");
  assert.equal(ledger.sourceCommit, "1cd4679f91661ece2b3d55ae16d45ba980094344");
  assert.equal(ledger.baseCommit, "a1dc8ad6a9a5b50f6a9fd63c482538d863583c77");
  assert.equal(ledger.freezeCommit, "148dc22795632524c303231ec000b1a239da192a");
  assert.equal(ledger.scientificFileCount, 6);
  assert.equal(ledger.dependencyFileCount, 136);
  assert.equal(ledger.verifiedFileCount, 142);
  assert.equal(ledger.textSourceFileCount, 3);
  assert.equal(ledger.formulaTagCount, 22);
  assert.equal(ledger.arithmeticCheckCount, 17);
  assert.equal(ledger.negativeControlCount, 4);
  assert.equal(ledger.previousFrozenRowCount, 135);
  assert.equal(ledger.additionalHistoricalSourceCount, 0);
  assert.equal(ledger.files.length, 142);
  assert.equal(new Set(ledger.files.map((row) => row.path)).size, 142);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_convex_pressure_trace_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-AdjointWeakTraceScreen-20260906");
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

test("BT retains 22 continuous labels and the exact convex-pressure boundary", () => {
  const body = read("research/clay_b_convex_pressure_trace_20260906.md");
  const tags = [...body.matchAll(/\\tag\{(BT\.\d+)\}/g)].map((match) => match[1]);
  assert.deepEqual(tags, Array.from({ length: 22 }, (_, index) => `BT.${index + 1}`));
  for (const marker of [
    "压力梯度具有足够的时间可积性", "L^1(0,t;L^{3/2})", "有界 Hessian",
    "1\\le q<2", "q=2", "\\frac12\\eta(0)", "一致可积",
    "幅度逃逸", "任意压力", "H=D^2\\beta(z)", "没有证明", "NOT CLAY",
  ]) assert.ok(body.includes(marker), marker);
});

test("source QA preserves arithmetic, predecessor freeze, literature scope, and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_convex_pressure_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 3);
  assert.equal(qa.formula_tags_checked, 22);
  assert.equal(qa.arithmetic_checks.length, 17);
  assert.ok(qa.arithmetic_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 135);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.previous_saved_QA_live_identical, true);
  assert.ok(Object.values(qa.limited_negative_controls).every(Boolean));
  assert.equal(qa.protected_state.user_agents_unchanged, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");
  assert.equal(qa.clay_result, false);

  const joined = [
    "research/clay_b_convex_pressure_primary_reading_20260906.md",
    "research/clay_b_convex_pressure_report_20260906.md",
    "research/clay_b_convex_pressure_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "Definition 2.3", "Lemma 2.6", "Theorem 2.7", "标量", "带压力向量",
    "q<2", "q=2", "任意压力", "B 的实际候选核读记录", "尚未开始", "b+\\sqrt m", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
