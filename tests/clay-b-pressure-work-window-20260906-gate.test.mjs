import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("PressureWorkWindow ledger binds the 7+4 scientific package and 2-file handoff envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_pressure_work_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-pressure-work-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-PressureWorkWindow-20260906");
  assert.equal(ledger.sourceRepository, "navier-stokes-r074m");
  assert.equal(ledger.sourceCommit, "fd6fa4b2bcebb702ddc2e8c03884496dca139101");
  assert.equal(ledger.baseCommit, "9771fa5b79b25824ce015c2e9174ae9bc9de6ae7");
  assert.equal(ledger.freezeCommit, "4c52c02026ce0191a121e03241d88fa6573d5536");
  assert.equal(ledger.scientificFileCount, 7);
  assert.equal(ledger.dependencyFileCount, 4);
  assert.equal(ledger.formulaTagCount, 60);
  assert.equal(ledger.files.length, 11);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_pressure_work_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-PressureQuotient-20260906");
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

test("AI and AJ preserve all 60 unique formula tags and genuine pressure-work conclusions", () => {
  const ai = read("research/clay_b_compact_pressure_work_preflight_20260906.md");
  const aj = read("research/clay_b_short_time_pressure_work_preflight_20260906.md");
  const tags = [ai, aj].flatMap((source) => [...source.matchAll(/\\tag\{([A-Z]+\.\d+)\}/g)].map((match) => match[1]));
  assert.equal(tags.length, 60);
  assert.equal(new Set(tags).size, 60);
  for (const marker of [
    "W_{\\mathbb R^3}(V_N)",
    "(H_\\epsilon'(0))_+",
    "t_\\epsilon=\\tau_0\\epsilon^{5/2}",
    "\\frac{H_\\epsilon(t_\\epsilon)}{H_\\epsilon(0)}",
    "C(V)\\sqrt\\epsilon",
    "t_\\epsilon/\\epsilon^2=\\tau_0\\sqrt\\epsilon\\to0",
    "不能顺带排除允许常数依赖",
  ]) assert.ok((ai + "\n" + aj).includes(marker), marker);
});

test("audits, report, and literature retain the exact early-time and prior-art boundaries", () => {
  const joined = [
    "research/clay_b_pressure_work_internal_audit_20260906.md",
    "research/clay_b_pressure_work_freeze_audit_20260906.md",
    "research/clay_b_pressure_work_literature-boundary_20260906.md",
    "research/clay_b_pressure_work_report-source_20260906.md",
    "research/clay_b_signed_work_work_plan_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "只反驳 AJ.30",
    "严格早于成熟扩散时间",
    "不是一条固定解的首次奇点历史",
    "不使用“\\(L^3\\) norm inflation”",
    "不支持首创、优先权、论文等级或接近 Clay 的判断",
    "下一项从 AB 的成熟时间带符号局部恒等式出发",
  ]) assert.ok(joined.includes(marker), marker);
});
