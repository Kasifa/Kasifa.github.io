import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("PlateauHistory ledger binds the 5+8 scientific package and 2-file handoff envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_plateau_history_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-plateau-history-frozen-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-PlateauHistory-20260906");
  assert.equal(ledger.sourceRepository, "navier-stokes-r074m");
  assert.equal(ledger.sourceCommit, "24ba1c640fb52d2cdef4d4d21c58a5745871b75a");
  assert.equal(ledger.handoffCommit, "5049060cb94f39c411bdf6fceb85f3ea79b22816");
  assert.equal(ledger.scientificFileCount, 5);
  assert.equal(ledger.dependencyFileCount, 8);
  assert.equal(ledger.files.length, 13);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_plateau_history_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.source_commit, ledger.sourceCommit);
  assert.equal(manifest.status, "research-frozen");
  assert.equal(manifest.claim_boundaries.NOT_CLAY, true);
  assert.equal(manifest.claim_boundaries.novelty_claimed, false);
  assert.deepEqual(manifest.claim_boundaries.FINITE_COMPUTATION, []);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.scientific_figure_required, false);
  assert.equal(manifest.simulation_required, false);
  assert.equal(manifest.recap_required, false);
  assert.equal(manifest.publication.generate_new_reader_pdf, false);
});

test("analytic sources preserve X.1-X.4, Y.1-Y.12 and strict history boundaries", () => {
  const x = read("research/clay_b_target_time_scope_preflight_20260906.md");
  const y = read("research/clay_b_plateau_history_20260906.md");
  for (let index = 1; index <= 4; index += 1) assert.match(x, new RegExp(`\\\\tag\\{X\\.${index}\\}`));
  for (let index = 1; index <= 12; index += 1) assert.match(y, new RegExp(`\\\\tag\\{Y\\.${index}\\}`));
  for (const marker of [
    "等号情形不能断言原窗口已在平台内",
    "不能自动继承原 delta_k^F 的逆宽度预算",
    "total boldmu",
    "左 BV 迹",
    "右侧可能非正",
    "只恢复了粗的 A+P 控制",
    "不等于 A+Z",
    "未加权的 W.14",
  ]) assert.ok(`${x}\n${y}`.includes(marker), marker);
});

test("independent audit records actual-file review without expanding the claim", () => {
  const audit = read("research/clay_b_plateau_history_independent_audit_20260906.md");
  for (const marker of [
    "三条 Y 通道均读取实际",
    "平台正工作不足的支路完整保留",
    "右侧恒正",
    "新钟不是原 K",
    "W.14 的完整 I_(2R) 未加权耗散不因此获支付",
    "审查 PASS 不表示上述开放问题已证",
  ]) assert.ok(audit.includes(marker), marker);
});
