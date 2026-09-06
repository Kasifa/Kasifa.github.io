import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("FixedHistoryScreen ledger binds the 7+82 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_fixed_history_screen_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-fixed-history-screen-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-FixedHistoryScreen-20260906");
  assert.equal(ledger.sourceCommit, "67476e7a2e236af9c3ce50ca95f8925f032d5704");
  assert.equal(ledger.baseCommit, "56027d0cf173535de10a67865e91fa019fbef332");
  assert.equal(ledger.freezeCommit, "20a2abc781ad6784f552d2a80211298e5711c97f");
  assert.equal(ledger.scientificFileCount, 7);
  assert.equal(ledger.dependencyFileCount, 82);
  assert.equal(ledger.verifiedFileCount, 89);
  assert.equal(ledger.textSourceFileCount, 4);
  assert.equal(ledger.formulaTagCount, 52);
  assert.equal(ledger.arithmeticCheckCount, 23);
  assert.equal(ledger.affineCoefficientPairCount, 3);
  assert.equal(ledger.negativeControlCount, 3);
  assert.equal(ledger.files.length, 89);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_fixed_history_screen_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-AncientConstantScreen-20260906");
  assert.equal(manifest.status, "RESEARCH_COMPLETE");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_pdf, false);
  assert.equal(manifest.recap.update, false);
  assert.deepEqual(manifest.excluded_user_paths, ["AGENTS.md"]);
});

test("BI and BJ retain all 52 formula tags and the fixed-versus-growing-window boundary", () => {
  const bi = read("research/clay_b_fixed_history_mild_preflight_20260906.md");
  const bj = read("research/clay_b_record_time_history_preflight_20260906.md");
  const biTags = [...bi.matchAll(/\\tag\{(BI\.\d+)\}/g)].map((match) => match[1]);
  const bjTags = [...bj.matchAll(/\\tag\{(BJ\.\d+)\}/g)].map((match) => match[1]);
  assert.deepEqual(biTags, Array.from({ length: 20 }, (_, index) => `BI.${index + 1}`));
  assert.deepEqual(bjTags, Array.from({ length: 32 }, (_, index) => `BJ.${index + 1}`));
  for (const marker of [
    "不能交换两个极限", "周期副本", "不是把 \\(\\mathbb P\\) 本身视为",
    "S_k=M_k^{1+\\eta}", "只适用于固定", "不把中间时间段的真实有符号贡献称为正测度",
  ]) assert.ok(bi.includes(marker), marker);
  for (const marker of [
    "局部 mild 理论给的是下界", "D_j\\ge4c_*", "不是 \\(D_j\\) 的统一上界",
    "d_j=d_*+j^2", "这个标量族不是 NS 解", "Type I 附加条件",
  ]) assert.ok(bj.includes(marker), marker);
});

test("source QA and audit preserve finite-check, literature, and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_fixed_history_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 4);
  assert.equal(qa.formula_tags_checked, 52);
  assert.equal(qa.arithmetic_checks.length, 23);
  assert.ok(qa.arithmetic_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 81);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.protected_state.user_agents_unchanged, true);
  assert.equal(qa.protected_state.private_paper_object_unchanged, true);
  assert.ok(Object.values(qa.negative_controls).every(Boolean));
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");

  const joined = [
    "research/clay_b_fixed_history_report_20260906.md",
    "research/clay_b_fixed_history_primary_reading_20260906.md",
    "research/clay_b_fixed_history_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "不能直接使用的文献出口", "同一个全空间 mild 古老解", "不得交换两种量词",
    "同行评审，也不是", "不是 PDE 证明证书", "G、Q", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
