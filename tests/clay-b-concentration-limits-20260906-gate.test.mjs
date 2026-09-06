import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("ConcentrationLimits ledger binds the 6+3 scientific package and 2-file handoff envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_concentration_limits_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-concentration-limits-frozen-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-ConcentrationLimits-20260906");
  assert.equal(ledger.sourceRepository, "navier-stokes-r074m");
  assert.equal(ledger.sourceCommit, "16b65456c8f8fbd3c677ab963ea0dd6449869f81");
  assert.equal(ledger.baseCommit, "edd69a09c9603deaea5e08c2859271f5a53b28e4");
  assert.equal(ledger.handoffCommit, "b1a9297c317ede89f9c913e93a8376b9645e41fa");
  assert.equal(ledger.scientificFileCount, 6);
  assert.equal(ledger.dependencyFileCount, 3);
  assert.equal(ledger.formulaTagCount, 63);
  assert.equal(ledger.files.length, 9);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_concentration_limits_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.source_commit, ledger.sourceCommit);
  assert.equal(manifest.base_commit, ledger.baseCommit);
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

test("analytic sources preserve all 63 tags and strict concentration/persistence boundaries", () => {
  const sources = [
    read("research/clay_b_first_singularity_scope_preflight_20260906.md"),
    read("research/clay_b_concentration_path_limits_20260906.md"),
    read("research/clay_b_local_persistence_obstruction_20260906.md"),
  ];
  const tags = sources.flatMap((source) => [...source.matchAll(/\\tag\{([A-Z]+\.\d+)\}/g)].map((match) => match[1]));
  assert.equal(tags.length, 63);
  assert.equal(new Set(tags).size, 63);
  const joined = sources.join("\n");
  for (const marker of [
    "LITERATURE CONDITIONAL",
    "不是作者勘误声明",
    "不是预先给定的幂率",
    "没有把固定 \\(R\\) 的 ODE\n换成变尺度 ODE",
    "不存在任何压力把 (M.3) 变成 NS 解",
    "AA.1 仍不成立",
    "t_B/r^2",
    "没有否定额外要求 \\(t\\ge Cr^2\\) 的局部成熟时间版本",
    "仅限首次奇点的持留命题仍是 OPEN",
    "这只控制远源压力的积分",
    "不能从 AA.18 单独推出 AA.1",
  ]) assert.ok(joined.includes(marker), marker);
});

test("independent actual-file audit preserves the distinctions needed for publication", () => {
  const audit = read("research/clay_b_concentration_limits_independent_audit_20260906.md");
  for (const marker of [
    "两份数学源文件都经实际全文审查",
    "没有把固定球发散改写为预定抛物缩球发散",
    "逐时选择一条固定尺度路径不构成一条新的变尺度 ODE",
    "这排除 NS 方程",
    "初值与能量随 B 改变",
    "t_B/r²→0",
    "裸压力梯度冲量不等于局部 L³ 恒等式中",
    "G、G-P/G-C、原 R.216--R.217 真实动力学输入继续 OPEN",
  ]) assert.ok(audit.includes(marker), marker);
});
