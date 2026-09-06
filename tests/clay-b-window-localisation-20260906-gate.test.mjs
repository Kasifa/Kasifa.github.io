import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("WindowLocalisation ledger binds the 7+6 scientific package and 2-file handoff envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_window_localisation_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-window-localisation-frozen-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-WindowLocalisation-20260906");
  assert.equal(ledger.sourceRepository, "navier-stokes-r074m");
  assert.equal(ledger.sourceCommit, "d34e9a1126b05902f75a7c6aba0fd13024ba51a0");
  assert.equal(ledger.handoffCommit, "e91a6997f9b3a3a88fb44bd3fda936c2c99ba798");
  assert.equal(ledger.scientificFileCount, 7);
  assert.equal(ledger.dependencyFileCount, 6);
  assert.equal(ledger.files.length, 13);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_window_localisation_release_20260906.json"));
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

test("analytic sources preserve U.1-U.9, V.1-V.12, W.1-W.14 and strict corrections", () => {
  const u = read("research/clay_b_signed_upcrossing_preflight_20260906.md");
  const v = read("research/clay_b_signed_upcrossing_time_integrability_20260906.md");
  const w = read("research/clay_b_window_localisation_20260906.md");
  for (let index = 1; index <= 9; index += 1) assert.match(u, new RegExp(`\\\\tag\\{U\\.${index}\\}`));
  for (let index = 1; index <= 12; index += 1) assert.match(v, new RegExp(`\\\\tag\\{V\\.${index}\\}`));
  for (let index = 1; index <= 14; index += 1) assert.match(w, new RegExp(`\\\\tag\\{W\\.${index}\\}`));
  for (const marker of ["整个有符号空间积分之后", "右侧可能非正", "调和压力", "中心漂移", "W_{2R}", "二者均不能仅凭定义支付 W.14"]) {
    assert.ok(`${u}\n${v}\n${w}`.includes(marker), marker);
  }
});

test("actual-file audits preserve the open boundaries and do not claim novelty", () => {
  const audit = `${read("research/clay_b_signed_upcrossing_progress_audit_20260906.md")}\n${read("research/clay_b_window_localisation_independent_audit_20260906.md")}`;
  for (const marker of [
    "PASS，无必改项",
    "cutoff 修正项不可免费删除，右侧可能非正",
    "gamma_k/gamma_(k+1) 无界",
    "不需要数值证书和科学图表",
    "不从搜索摘要",
    "不以“所有检查 PASS”表示 Clay 问题已解决",
  ]) assert.ok(audit.includes(marker), marker);
});
