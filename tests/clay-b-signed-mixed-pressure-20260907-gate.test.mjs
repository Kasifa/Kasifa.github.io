import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("SignedMixedPressure ledger binds the 6+150 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_signed_mixed_pressure_frozen_ledger_20260907.json"));
  assert.equal(ledger.schemaVersion, "clay-b-signed-mixed-pressure-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-SignedMixedPressure-20260907");
  assert.equal(ledger.sourceCommit, "cb5acbb4416ca2d6502e9b7d48d19f91a150f2a0");
  assert.equal(ledger.baseCommit, "ecc17ffc95f3399f0cca1289f4b1787c1bdba3a1");
  assert.equal(ledger.freezeCommit, "cf4f8a27bc1ddab92f857945b229a24fb05d5517");
  assert.equal(ledger.scientificFileCount, 6);
  assert.equal(ledger.dependencyFileCount, 150);
  assert.equal(ledger.verifiedFileCount, 156);
  assert.equal(ledger.textSourceFileCount, 3);
  assert.equal(ledger.formulaTagCount, 23);
  assert.equal(ledger.arithmeticCheckCount, 25);
  assert.equal(ledger.negativeControlCount, 4);
  assert.equal(ledger.previousFrozenRowCount, 149);
  assert.equal(ledger.additionalHistoricalSourceCount, 0);
  assert.equal(ledger.files.length, 156);
  assert.equal(new Set(ledger.files.map((row) => row.path)).size, 156);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_signed_mixed_pressure_release_20260907.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-SameParentResidual-20260906");
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

test("BV retains 23 continuous labels and the exact signed-work boundary", () => {
  const body = read("research/clay_b_signed_mixed_pressure_20260907.md");
  const tags = [...body.matchAll(/\\tag\{(BV\.\d+)\}/g)].map((match) => match[1]);
  assert.deepEqual(tags, Array.from({ length: 23 }, (_, index) => `BV.${index + 1}`));
  for (const marker of [
    "同一原解", "M_R", "常数不依赖 \\(R\\)", "只是每个时间的估计",
    "是充分条件，不是实际压力功消失的必要条件", "联合压力原函数的消失",
    "不证明", "三个双线性式", "有限成本是充分条件",
    "累计耗散", "自压力", "一般三维正则性和 Clay 问题仍 OPEN",
  ]) assert.ok(body.includes(marker), marker);
});

test("source QA preserves rational arithmetic, predecessor freeze, and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_signed_mixed_pressure_qa_20260907.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 3);
  assert.equal(qa.formula_tags_checked, 23);
  assert.equal(qa.arithmetic_checks.length, 25);
  assert.ok(qa.arithmetic_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 149);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.previous_saved_QA_live_identical, true);
  assert.ok(Object.values(qa.limited_negative_controls).every(Boolean));
  assert.equal(qa.protected_state.user_agents_unchanged, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");
  assert.equal(qa.clay_result, false);

  const joined = [
    "research/clay_b_signed_mixed_pressure_reading_20260907.md",
    "research/clay_b_signed_mixed_pressure_report_20260907.md",
    "research/clay_b_signed_mixed_pressure_audit_20260907.md",
  ].map(read).join("\n");
  for (const marker of [
    "两条不同的充分输入", "联合压力原函数", "自压力仍须保留",
    "不是 NS 场", "不是外部同行评审", "不宣称文献新颖性", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
