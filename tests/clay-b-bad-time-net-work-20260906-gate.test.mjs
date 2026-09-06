import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("BadTimeNetWork ledger binds the 14+3 package and 2-file frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_bad_net_work_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-bad-net-work-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-BadTimeNetWork-20260906");
  assert.equal(ledger.sourceCommit, "22c0064338dbad20a6cc37cf054c24850cd2dc2e");
  assert.equal(ledger.baseCommit, "8843d99338d62cdbc3067eaaead81ad93d7326ba");
  assert.equal(ledger.freezeCommit, "ca1bf2ecad5716ef9a4a653806e4a27fbfb2957f");
  assert.equal(ledger.scientificFileCount, 14);
  assert.equal(ledger.dependencyFileCount, 3);
  assert.equal(ledger.formulaTagCount, 131);
  assert.equal(ledger.files.length, 17);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }
  const manifest = JSON.parse(read("research/clay_b_bad_net_work_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-PressureWorkWindow-20260906");
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

test("AK through AQ preserve all 131 unique formula tags and the lower-bound direction", () => {
  const sourcePaths = [
    "research/clay_b_mature_frequency_preflight_20260906.md",
    "research/clay_b_periodic_dissipation_wavenumber_preflight_20260906.md",
    "research/clay_b_separated_pressure_pair_preflight_20260906.md",
    "research/clay_b_global_high_high_pressure_preflight_20260906.md",
    "research/clay_b_local_high_high_pressure_preflight_20260906.md",
    "research/clay_b_fixed_regular_annulus_interface_20260906.md",
    "research/clay_b_bad_time_net_work_necessity_20260906.md",
  ];
  const joined = sourcePaths.map(read).join("\n");
  const tags = [...joined.matchAll(/\\tag\{([A-Z]+\.\d+)\}/g)].map((match) => match[1]);
  assert.equal(tags.length, 131);
  assert.equal(new Set(tags).size, 131);
  for (const marker of [
    "完整局部配对", "能量绝对连续性只给", "p(h)",
    "不再是 AO 的开放前提", "坏时间留下的是带符号压力",
    "这是一个由方程预算推出的下界", "不是对 \\(\\mathcal B_J\\) 的上界",
    "不能将 AQ.8 中的权重免费删去", "不产生一个新的存在性结论",
  ]) assert.ok(joined.includes(marker), marker);
});

test("report and audits preserve literature access, fixed-annulus, and G boundaries", () => {
  const joined = [
    "research/clay_b_bad_net_work_report_20260906.md",
    "research/clay_b_mature_frequency_literature_bridge_20260906.md",
    "research/clay_b_mature_frequency_internal_audit_20260906.md",
    "research/clay_b_frequency_interaction_internal_audit_20260906.md",
    "research/clay_b_local_pressure_budget_internal_audit_20260906.md",
    "research/clay_b_bad_net_work_work_plan_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "CKN 的 DOI 入口本轮只提供", "OCR 存在符号损坏",
    "不是一项新的部分正则性定理", "必要下界，而非已付上界",
    "不证明这列时间存在", "固定半径结论也不是原合同 G",
    "仅将未付项定义为新指标不算获得上界",
  ]) assert.ok(joined.includes(marker), marker);
});
