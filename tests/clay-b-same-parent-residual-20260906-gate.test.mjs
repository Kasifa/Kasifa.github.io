import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("SameParentResidual ledger binds the 6+143 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_same_parent_residual_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-same-parent-residual-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-SameParentResidual-20260906");
  assert.equal(ledger.sourceCommit, "9708a86053d507a51b0c3843211774ede954efea");
  assert.equal(ledger.baseCommit, "281d36f1d55254dc13b0bc5c3b5b80ccf94467a0");
  assert.equal(ledger.freezeCommit, "6da74e5e62930a5b4b44d09962915f7e4e551541");
  assert.equal(ledger.scientificFileCount, 6);
  assert.equal(ledger.dependencyFileCount, 143);
  assert.equal(ledger.verifiedFileCount, 149);
  assert.equal(ledger.textSourceFileCount, 3);
  assert.equal(ledger.formulaTagCount, 20);
  assert.equal(ledger.arithmeticCheckCount, 20);
  assert.equal(ledger.negativeControlCount, 4);
  assert.equal(ledger.previousFrozenRowCount, 142);
  assert.equal(ledger.additionalHistoricalSourceCount, 0);
  assert.equal(ledger.files.length, 149);
  assert.equal(new Set(ledger.files.map((row) => row.path)).size, 149);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_same_parent_residual_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-ConvexPressureTrace-20260906");
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

test("BU retains 20 continuous labels and the exact residual-pressure boundary", () => {
  const body = read("research/clay_b_same_parent_residual_20260906.md");
  const tags = [...body.matchAll(/\\tag\{(BU\.\d+)\}/g)].map((match) => match[1]);
  assert.deepEqual(tags, Array.from({ length: 20 }, (_, index) => `BU.${index + 1}`));
  for (const marker of [
    "同一个 NS 原解", "\\mu_{\\rm res}", "\\mu_{\\rm res}(\\{a\\})=0",
    "-2\\nu\\Delta b", "不能把它当作齐次正向方程", "整个周期胞",
    "\\|z(\\rho)\\otimes w(\\rho)\\|_1", "o\\big(h_w(\\delta)+h_z(\\delta)\\big)",
    "不附带任何时间或临界尺度衰减率", "这不是对 \\(R\\to\\infty\\) 的一致估计",
    "\\frac12", "不是原子排除", "NOT CLAY",
  ]) assert.ok(body.includes(marker), marker);
});

test("source QA preserves arithmetic, predecessor freeze, review scope, and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_same_parent_residual_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 3);
  assert.equal(qa.formula_tags_checked, 20);
  assert.equal(qa.arithmetic_checks.length, 20);
  assert.ok(qa.arithmetic_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 142);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.previous_saved_QA_live_identical, true);
  assert.ok(Object.values(qa.limited_negative_controls).every(Boolean));
  assert.equal(qa.protected_state.user_agents_unchanged, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");
  assert.equal(qa.clay_result, false);

  const joined = [
    "research/clay_b_same_parent_residual_reading_20260906.md",
    "research/clay_b_same_parent_residual_report_20260906.md",
    "research/clay_b_same_parent_residual_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "BP.28--32", "Huang 原始预印本 v1", "没有重新读取该 PDF", "不宣称文献首创",
    "普通 little-o", "幅度族的一致估计", "非作者", "尚无完成证明", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
