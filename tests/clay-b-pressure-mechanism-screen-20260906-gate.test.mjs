import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("PressureMechanismScreen ledger binds the 7+67 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_pressure_mechanism_screen_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-pressure-mechanism-screen-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-PressureMechanismScreen-20260906");
  assert.equal(ledger.sourceCommit, "1df0d394d3da2c6ae01b843a86b4830d266148a7");
  assert.equal(ledger.baseCommit, "bbb7074c4eb4f6b5955460a49c44db347a9b6ba8");
  assert.equal(ledger.freezeCommit, "e29c13699b36dd81dd924476bffc5e8ce724f550");
  assert.equal(ledger.scientificFileCount, 7);
  assert.equal(ledger.dependencyFileCount, 67);
  assert.equal(ledger.verifiedFileCount, 74);
  assert.equal(ledger.textSourceFileCount, 4);
  assert.equal(ledger.formulaTagCount, 37);
  assert.equal(ledger.fractionCheckCount, 25);
  assert.equal(ledger.files.length, 74);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_pressure_mechanism_screen_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-RecentSourceScreen-20260906");
  assert.equal(manifest.status, "RESEARCH_COMPLETE");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_pdf, false);
  assert.equal(manifest.recap.update, false);
});

test("BF and BG retain all 37 unique formula tags and the exact scope boundaries", () => {
  const sources = [
    read("research/clay_b_periodic_radial_pressure_identity_20260906.md"),
    read("research/clay_b_pressure_potential_energy_screen_20260906.md"),
  ];
  const tagsBySource = sources.map((source) => [...source.matchAll(/\\tag\{([A-Z]+\.\d+)\}/g)].map((match) => match[1]));
  assert.deepEqual(tagsBySource.map((tags) => tags.length), [15, 22]);
  const tags = tagsBySource.flat();
  assert.equal(tags.length, 37);
  assert.equal(new Set(tags).size, 37);
  const joined = sources.join("\n");
  for (const marker of [
    "甚至不需要无散性", "周期边界不引入额外项", "不能把整个右端都称为可忽略远场",
    "不是周期 NS", "不把任意标量函数冒充压力", "条件 C 反例",
    "这个时间族不是 NS 解", "局部能量不等式、suitable",
    "固定尺度的\n\\(L_t^{4/3}\\)", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});

test("source QA and reading records preserve arithmetic, literature, and non-NS limits", () => {
  const qa = JSON.parse(read("research/clay_b_pressure_mechanism_screen_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 4);
  assert.equal(qa.formula_tags_checked, 37);
  assert.equal(qa.fraction_checks.length, 25);
  assert.ok(qa.fraction_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 65);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.AH_reused_source.worktree_source_commit_hash, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");

  const joined = [
    "research/clay_b_pressure_mechanism_primary_reading_20260906.md",
    "research/clay_b_pressure_mechanism_screen_report_20260906.md",
    "research/clay_b_pressure_mechanism_screen_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "完整阅读正式版 §2–§4", "R\\to\\infty", "\\varepsilon_*(1)", "\\theta^k\\rho",
    "外引文献未全文重审", "不是外部同行评审", "不是 NS", "一般正则性与新颖性仍 OPEN",
  ]) assert.ok(joined.includes(marker), marker);
});
