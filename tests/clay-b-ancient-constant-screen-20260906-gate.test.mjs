import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("AncientConstantScreen ledger binds the 6+75 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_ancient_constant_screen_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-ancient-constant-screen-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-AncientConstantScreen-20260906");
  assert.equal(ledger.sourceCommit, "4dfd49be08e9f8bb253432851669c9d632936b5c");
  assert.equal(ledger.baseCommit, "9069f24128b0ef8db8192b1ddff998516b82a757");
  assert.equal(ledger.freezeCommit, "b44960f63d35f0fd269cf1fc412921df91523a9a");
  assert.equal(ledger.scientificFileCount, 6);
  assert.equal(ledger.dependencyFileCount, 75);
  assert.equal(ledger.verifiedFileCount, 81);
  assert.equal(ledger.textSourceFileCount, 3);
  assert.equal(ledger.formulaTagCount, 18);
  assert.equal(ledger.scalingCheckCount, 22);
  assert.equal(ledger.files.length, 81);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_ancient_constant_screen_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-PressureMechanismScreen-20260906");
  assert.equal(manifest.status, "RESEARCH_COMPLETE");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_pdf, false);
  assert.equal(manifest.recap.update, false);
  assert.deepEqual(manifest.excluded_user_paths, ["AGENTS.md"]);
});

test("BH retains all 18 formula tags and the fixed-history exclusions", () => {
  const source = read("research/clay_b_ancient_constant_sequence_preflight_20260906.md");
  const tags = [...source.matchAll(/\\tag\{(BH\.\d+)\}/g)].map((match) => match[1]);
  assert.deepEqual(tags, Array.from({ length: 18 }, (_, index) => `BH.${index + 1}`));
  for (const marker of [
    "每一项都是真实的光滑 NS 解", "没有把每一项称为精确的历史 record",
    "缺少控制的开放端点", "若只用后者，只能得到",
    "非零常向量", "合法的古老", "同一固定周期光滑初值",
    "n^{-11/2}", "不能排除利用", "NOT CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("source QA and strategy records preserve scaling, literature, and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_ancient_sequence_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 3);
  assert.equal(qa.formula_tags_checked, 18);
  assert.equal(qa.scaling_checks.length, 22);
  assert.ok(qa.scaling_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 74);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.protected_state.user_agents_unchanged, true);
  assert.equal(qa.protected_state.private_paper_unchanged, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");

  const joined = [
    "research/clay_b_dynamic_strategy_review_20260906.md",
    "research/clay_b_dynamic_strategy_primary_reading_20260906.md",
    "research/clay_b_ancient_sequence_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "临界控制未付", "非零不等于矛盾", "没有构造来自同一固定初值的首次爆破序列",
    "不扩大已知正则解类", "新颖性检索或 Deep Research", "不是外部同行评审",
  ]) assert.ok(joined.includes(marker), marker);
});
