import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("PressureGeometry ledger binds the 6+3 scientific package and 2-file handoff envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_pressure_geometry_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-pressure-geometry-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-PressureGeometry-20260906");
  assert.equal(ledger.sourceRepository, "navier-stokes-r074m");
  assert.equal(ledger.sourceCommit, "40b18a9c29499f4956d72e197f8d285bd3f6b453");
  assert.equal(ledger.baseCommit, "b462101c34b2479580048893485e4ab291a9fcff");
  assert.equal(ledger.freezeCommit, "e63575d6bbb81332441d74c0916c5663e89ac74c");
  assert.equal(ledger.scientificFileCount, 6);
  assert.equal(ledger.dependencyFileCount, 3);
  assert.equal(ledger.formulaTagCount, 45);
  assert.equal(ledger.files.length, 9);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_pressure_geometry_release_20260906.json"));
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

test("the three analytic sources preserve all 45 unique formula tags and strict boundaries", () => {
  const sources = [
    read("research/clay_b_mature_l3_budget_preflight_20260906.md"),
    read("research/clay_b_pressure_geometry_20260906.md"),
    read("research/clay_b_pressure_sign_20260906.md"),
  ];
  const tags = sources.flatMap((source) => [...source.matchAll(/\\tag\{([A-Z]+\.\d+)\}/g)].map((match) => match[1]));
  assert.equal(tags.length, 45);
  assert.equal(new Set(tags).size, 45);
  const joined = sources.join("\n");
  for (const marker of [
    "这里只做无空间 cutoff 的原型",
    "这只付掉 AB.2 的远源部分",
    "临界大范数不可吸收",
    "不表示 e 是跨零集的普通 Sobolev 场",
    "\\|F\\|_{L_t^2L_x^3}",
    "此例不判定 Vasseur 的全空间条件",
    "没有普适正号或负号",
    "幅值放大也放大初始能量",
    "不是成熟时间、指定首次奇点附近的构造",
  ]) assert.ok(joined.includes(marker), marker);
});

test("independent actual-file audit preserves publication-critical distinctions", () => {
  const audit = read("research/clay_b_pressure_geometry_independent_audit_20260906.md");
  for (const marker of [
    "固定 M/r、缩球、成熟时间条件与原移动路径的不同范围均保留",
    "最后留下 (CL+eta−1)D，不能对大 L 吸收",
    "没有声称 e 跨零集属于普通 H¹",
    "能量 L²_tL²_x 的指数和为 5/2",
    "Vasseur 全6页作者稿",
    "固定角锥有 1/r 下界",
    "不能判定 Vasseur 全空间原类中条件的必要性",
    "能量增长、非成熟时间、非首次奇点、非固定能量等边界均准确",
  ]) assert.ok(audit.includes(marker), marker);
});
