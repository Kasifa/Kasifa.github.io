import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("RecentSourceScreen ledger binds the 9+56 package and one-file frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_recent_source_screen_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-recent-source-screen-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-RecentSourceScreen-20260906");
  assert.equal(ledger.sourceCommit, "5314045dcedcc7e781d9fed0f167cae5c0451d62");
  assert.equal(ledger.baseCommit, "2b7cfe590decf90aea2326e9b76bc04bcf345e0b");
  assert.equal(ledger.freezeCommit, "9b556d81330a93f274372ed2e3be262e4be37d98");
  assert.equal(ledger.scientificFileCount, 9);
  assert.equal(ledger.dependencyFileCount, 56);
  assert.equal(ledger.verifiedFileCount, 65);
  assert.equal(ledger.textSourceFileCount, 7);
  assert.equal(ledger.formulaTagCount, 57);
  assert.equal(ledger.fractionCheckCount, 29);
  assert.equal(ledger.files.length, 65);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_recent_source_screen_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-LaggedPressureReduction-20260906");
  assert.equal(manifest.status, "research-frozen");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_pdf, false);
  assert.equal(manifest.recap.update, false);
});

test("BC through BE retain 57 unique tags and the method-screen boundaries", () => {
  const sourcePaths = [
    "research/clay_b_recent_source_energy_benchmark_20260906.md",
    "research/clay_b_dyadic_recent_source_screen_20260906.md",
    "research/clay_b_static_background_comparison_20260906.md",
  ];
  const expectedTagCounts = [18, 22, 17];
  const sources = sourcePaths.map(read);
  const tagsBySource = sources.map((source) => [...source.matchAll(/\\tag\{([A-Z]+\.\d+)\}/g)].map((match) => match[1]));
  assert.deepEqual(tagsBySource.map((tags) => tags.length), expectedTagCounts);
  const tags = tagsBySource.flat();
  assert.equal(tags.length, 57);
  assert.equal(new Set(tags).size, 57);
  const joined = sources.join("\n");
  for (const marker of [
    "不能把 \\(\\widetilde A_J\\) 偷换成 \\(A_J\\)",
    "它不是 NS 解必须满足的必要条件",
    "不把 \\(R\\) 当成独立 NS 解",
    "也不是 BC.11 的已付上界",
    "它不是无散速度、不是 NS 轨道",
    "本稿不排除 Fourier 相位",
    "不是以 \\(N\\) 重定义的集合",
    "这一比较没有判定 \\(R=P_{>N}u\\)",
  ]) assert.ok(joined.includes(marker), marker);
});

test("source QA and scoped records preserve finite-check, literature, and open-claim limits", () => {
  const qa = JSON.parse(read("research/clay_b_recent_source_screen_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 7);
  assert.equal(qa.formula_tags_checked, 57);
  assert.equal(qa.fraction_checks.length, 29);
  assert.ok(qa.fraction_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 51);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");

  const joined = [
    "research/clay_b_recent_source_screen_report_20260906.md",
    "research/clay_b_recent_source_screen_literature_20260906.md",
    "research/clay_b_pressure_mechanism_review_plan_20260906.md",
    "research/clay_b_recent_source_screen_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "没有外部同行", "条件 (C) 是额外假设", "未做穷尽新颖性检索",
    "全文证明与周期余项是下一项未完成检查", "Q、小窗口净压力功上界", "一般正则性与新颖性仍 OPEN",
    "不等同于 \\(P_{>N}p\\)", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
