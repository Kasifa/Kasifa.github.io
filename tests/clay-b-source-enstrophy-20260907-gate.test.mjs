import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("SourceEnstrophy ledger binds the 7+157 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_source_enstrophy_frozen_ledger_20260907.json"));
  assert.equal(ledger.schemaVersion, "clay-b-source-enstrophy-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-SourceEnstrophy-20260907");
  assert.equal(ledger.sourceCommit, "53f167438c058c77aa218216a014c3e504300300");
  assert.equal(ledger.baseCommit, "363bb4b83b2b3c3db605e42e05491072cb073bf5");
  assert.equal(ledger.freezeCommit, "6c6186d86d22c925eb2f7e7d03ad39f291f4dfac");
  assert.equal(ledger.scientificFileCount, 7);
  assert.equal(ledger.dependencyFileCount, 157);
  assert.equal(ledger.verifiedFileCount, 164);
  assert.equal(ledger.textSourceFileCount, 3);
  assert.equal(ledger.formulaTagCount, 18);
  assert.equal(ledger.arithmeticCheckCount, 25);
  assert.equal(ledger.negativeControlCount, 5);
  assert.equal(ledger.previousFrozenRowCount, 156);
  assert.equal(ledger.files.length, 164);
  assert.equal(new Set(ledger.files.map((row) => row.path)).size, 164);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }
  const manifest = JSON.parse(read("research/clay_b_source_enstrophy_release_20260907.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-SignedMixedPressure-20260907");
  assert.equal(manifest.status, "RESEARCH_FREEZE_COMPLETE");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_PDF, false);
  assert.equal(manifest.recap.update_required, false);
  assert.deepEqual(manifest.excluded_user_paths, ["AGENTS.md"]);
});

test("BW retains 18 continuous labels and the one-way conditional divergence boundary", () => {
  const body = read("research/clay_b_source_enstrophy_20260907.md");
  const tags = [...body.matchAll(/\\tag\{(BW\.\d+)\}/g)].map((m) => m[1]);
  assert.deepEqual(tags, Array.from({ length: 18 }, (_, i) => `BW.${i + 1}`));
  for (const marker of [
    "严格正时间", "压力余项", "常系数正定二次组合", "所有二阶方向",
    "全部 NS 能量方法的不可能定理", "L^1_\\rho L^2_x",
    "不能从右端范数无穷", "没有证明两者等价", "自压力端点", "G",
  ]) assert.ok(body.includes(marker), marker);
});

test("source QA and literature ledger retain finite scope and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_source_enstrophy_qa_20260907.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 3);
  assert.equal(qa.formula_tags_checked, 18);
  assert.equal(qa.arithmetic_checks.length, 25);
  assert.ok(qa.arithmetic_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 156);
  assert.equal(qa.previous_saved_QA_live_identical, true);
  assert.ok(Object.values(qa.limited_negative_controls).every(Boolean));
  assert.equal(qa.literature_ledger.identity_pass, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.G, "OPEN");
  assert.equal(qa.clay_result, false);
  const literature = JSON.parse(read("research/clay_b_source_enstrophy_literature_ledger_20260907.json"));
  assert.match(literature.classification, /no imported theorem/);
  assert.match(literature.future_dedup.status, /NOT STARTED/);
  assert.equal(literature.future_dedup.paths.length, 5);
  const joined = ["research/clay_b_source_enstrophy_reading_20260907.md", "research/clay_b_source_enstrophy_report-source_20260907.md", "research/clay_b_source_enstrophy_audit_20260907.md"].map(read).join("\n");
  for (const marker of ["不证明原先的", "不可能定理", "不宣称穷尽性", "NOT STARTED", "NOT CLAY"]) assert.ok(joined.includes(marker), marker);
});
