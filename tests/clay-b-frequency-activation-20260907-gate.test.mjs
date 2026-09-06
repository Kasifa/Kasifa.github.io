import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("FrequencyActivation ledger binds the 3+1+4 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_frequency_activation_frozen_ledger_20260907.json"));
  assert.equal(ledger.schemaVersion, "clay-b-frequency-activation-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-FrequencyActivation-20260907");
  assert.equal(ledger.sourceCommit, "1674af0dc98825d0d0299fa69e3ae12398c3d8a0");
  assert.equal(ledger.baseCommit, "c9bb03ff544c81cedeb3a6d116514d204033eb63");
  assert.equal(ledger.freezeCommit, "c688fca88da5a434aac5ca46971a7d800f146b39");
  assert.equal(ledger.scientificFileCount, 3);
  assert.equal(ledger.dependencyFileCount, 1);
  assert.equal(ledger.provenanceFileCount, 4);
  assert.equal(ledger.verifiedFileCount, 8);
  assert.equal(ledger.textSourceBindingCount, 6);
  assert.equal(ledger.formulaTagCount, 17);
  assert.equal(ledger.arithmeticCheckCount, 16);
  assert.equal(ledger.negativeControlCount, 4);
  assert.equal(ledger.files.length, 8);
  assert.equal(new Set(ledger.files.map((row) => row.path)).size, 8);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }
  const manifest = JSON.parse(read("research/clay_b_frequency_activation_release_20260907.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-SourceEnstrophy-20260907");
  assert.equal(manifest.status, "RESEARCH_FREEZE_COMPLETE");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_PDF, false);
  assert.equal(manifest.recap.update_required, false);
});

test("FA retains 17 continuous labels and exact first-activation boundaries", () => {
  const body = read("research/clay_b_frequency_activation_20260907.md");
  const tags = [...body.matchAll(/\\tag\{(FA\.\d+)\}/g)].map((m) => m[1]);
  assert.deepEqual(tags, Array.from({ length: 17 }, (_, i) => `FA.${i + 1}`));
  for (const marker of [
    "激活之后停留多久", "N^{5/2}", "压力没有删去", "目标带初始为零",
    "完整非线性解", "首次到达", "不同初值的有限时间光滑解族", "初始频谱包含在",
    "无限重复转移", "一般三维正则性仍 OPEN",
  ]) assert.ok(body.includes(marker), marker);
});

test("finite checks and audit preserve analytic-review and novelty boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_frequency_activation_checks_20260907.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.ordered_tags.length, 17);
  assert.equal(qa.display_pairs, 17);
  assert.equal(qa.exact_arithmetic.checks.length, 16);
  assert.ok(qa.exact_arithmetic.checks.every((row) => row.passed));
  assert.equal(qa.exact_arithmetic.negative_controls.length, 4);
  assert.equal(qa.exact_arithmetic.negative_controls_passed, 4);
  assert.match(qa.scope, /not PDE/i);
  const audit = read("research/clay_b_frequency_activation_audit_20260907.md");
  for (const marker of ["唯一完整非作者实际文件审查", "全文独立重推 FA.1–17", "PASS，无需修改", "不证明新颖性", "NOT CLAY"]) {
    assert.ok(audit.includes(marker), marker);
  }
});
