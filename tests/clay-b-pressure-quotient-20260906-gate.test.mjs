import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("PressureQuotient ledger binds the 8+4 scientific package and 2-file handoff envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_pressure_quotient_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-pressure-quotient-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-PressureQuotient-20260906");
  assert.equal(ledger.sourceRepository, "navier-stokes-r074m");
  assert.equal(ledger.sourceCommit, "094124aa2e6d74be4400e5d3e5a969d83acf9468");
  assert.equal(ledger.baseCommit, "b113bf0623388c0c17cae9e7313bdf3e02b56f08");
  assert.equal(ledger.freezeCommit, "02c0cbba61060fe268e0dc13877298faf26a1311");
  assert.equal(ledger.scientificFileCount, 8);
  assert.equal(ledger.dependencyFileCount, 4);
  assert.equal(ledger.formulaTagCount, 77);
  assert.equal(ledger.files.length, 12);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_pressure_quotient_release_20260906.json"));
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
  assert.equal(manifest.publication.public_paper_included, false);
});

test("the four analytic sources preserve all 77 tags and the exact obstruction scope", () => {
  const sources = [
    read("research/clay_b_longitudinal_strain_preflight_20260906.md"),
    read("research/clay_b_pressure_projection_20260906.md"),
    read("research/clay_b_bernoulli_shell_20260906.md"),
    read("research/clay_b_pressure_residual_obstruction_20260906.md"),
  ];
  const tags = sources.flatMap((source) => [...source.matchAll(/\\tag\{([A-Z]+\.\d+)\}/g)].map((match) => match[1]));
  assert.equal(tags.length, 77);
  assert.equal(new Set(tags).size, 77);
  const joined = sources.join("\n");
  for (const marker of [
    "当前演化式说明",
    "不构成正则性结论",
    "所有速度模长函数都与",
    "当前尚未证明 AF.18 可由基本能量推出",
    "不能以该 Hilbert 收敛替代局部预算",
    "Bernoulli 总压只是把该成本与输运重新组合",
    "给定任意 \\(E_0>0\\)",
    "大残差不等于大压力功",
    "不证明同一固定解上的时间积分失败",
  ]) assert.ok(joined.includes(marker), marker);
});

test("literature and independent audits preserve prior art and F=0 boundaries", () => {
  const literature = read("research/clay_b_pressure_quotient_literature-boundary_20260906.md");
  const audit = read("research/clay_b_pressure_quotient_independent_audit_20260906.md");
  for (const marker of [
    "因此 AF/AG 的这个出发点不是新发现",
    "不足以宣布文献穷尽",
    "当前分部积分未闭合，不表述为所有弱形式的 no-go",
    "残差是未归一化条件方差积分",
    "一般 L²(q dx) 逼近不足以控制原函数及外壳项",
    "大残差下界位于 F=0 平台",
    "不讨论固定轨道的时间积分",
    "真实首次奇点预算及一般正则性继续 OPEN / NOT CLAY",
  ]) assert.ok((literature + "\n" + audit).includes(marker), marker);
});
