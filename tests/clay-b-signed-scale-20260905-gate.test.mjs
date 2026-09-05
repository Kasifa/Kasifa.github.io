import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("signed-scale ledger binds the 6+2 frozen package and handoff envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_signed_scale_frozen_ledger_20260905.json"));
  assert.equal(ledger.schemaVersion, "clay-b-signed-scale-frozen-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-SignedScale-20260905");
  assert.equal(ledger.sourceCommit, "f8534cf78950487c6d1d50d8781881043e5d0b1f");
  assert.equal(ledger.baseCommit, "79880dbbffe0956d798e99374bda97cf7c5e1236");
  assert.equal(ledger.handoffCommit, "37b74d4c564b67b85c3f8f385f47a877eb3e7b8e");
  assert.equal(ledger.scientificFileCount, 6);
  assert.equal(ledger.dependencyFileCount, 2);
  assert.equal(ledger.files.length, 8);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
  }

  const manifest = JSON.parse(read("research/clay_b_signed_scale_release_20260905.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.source_commit, ledger.sourceCommit);
  assert.equal(manifest.base_commit, ledger.baseCommit);
  assert.equal(manifest.status, "research-frozen");
  assert.equal(manifest.claim_boundaries.NOT_CLAY, true);
  assert.equal(manifest.claim_boundaries.novelty_claimed, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.scientific_figure_required, false);
  assert.equal(manifest.simulation_required, false);
  assert.equal(manifest.recap_required, false);
  assert.deepEqual(manifest.excluded_from_publication, [
    "research/near_edge_paper_completion_receipt_20260905.md",
  ]);
});

test("analytic sources preserve F.1-F.4, S.1-S.15, T.1-T.12 and the open Next boundary", () => {
  const f = read("research/clay_b_signed_scale_telescope_preflight_20260905.md");
  const s = read("research/clay_b_signed_scale_local_budget_20260905.md");
  const t = read("research/clay_b_heat_dual_test_obstruction_20260905.md");
  const plan = read("research/clay_b_signed_scale_work_plan_20260905.md");
  for (let index = 1; index <= 4; index += 1) assert.match(f, new RegExp(`\\\\tag\\{F\\.${index}\\}`));
  for (let index = 1; index <= 15; index += 1) assert.match(s, new RegExp(`\\\\tag\\{S\\.${index}\\}`));
  for (let index = 1; index <= 12; index += 1) assert.match(t, new RegExp(`\\\\tag\\{T\\.${index}\\}`));
  assert.match(plan, /\\tag\{Next\}/);
  for (const marker of [
    "T_R=128R^2", "H^1", "首次奇点", "没有减少 G 的未证假设", "NOT CLAY",
  ]) assert.ok(`${s}\n${t}\n${plan}`.includes(marker), marker);
});

test("the independent audit preserves the exact limitation set", () => {
  const audit = read("research/clay_b_signed_scale_independent_audit_20260905.md");
  for (const marker of [
    "S.1--S.15", "F.1--F.4", "T.1--T.12", "L^2 一致而 H^1 不一致",
    "T_R=128R^2", "无必改问题",
  ]) assert.ok(audit.includes(marker), marker);
});
