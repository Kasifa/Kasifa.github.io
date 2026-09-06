import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("EnergyAtomCostScreen ledger binds the 6+109 package and frozen envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_energy_atom_cost_screen_frozen_ledger_20260906.json"));
  assert.equal(ledger.schemaVersion, "clay-b-energy-atom-cost-screen-portable-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-EnergyAtomCostScreen-20260906");
  assert.equal(ledger.sourceCommit, "7567e791fa3170bc71551c817cecc50b663d4d65");
  assert.equal(ledger.baseCommit, "11f6e30c0f181d9b590303e47d41f902b3046009");
  assert.equal(ledger.freezeCommit, "ccad47d0ed3549d1d1bf75d9b18ace5647fd1d96");
  assert.equal(ledger.scientificFileCount, 6);
  assert.equal(ledger.dependencyFileCount, 109);
  assert.equal(ledger.verifiedFileCount, 115);
  assert.equal(ledger.textSourceFileCount, 3);
  assert.equal(ledger.formulaTagCount, 18);
  assert.equal(ledger.arithmeticCheckCount, 18);
  assert.equal(ledger.negativeControlCount, 3);
  assert.equal(ledger.previousFrozenRowCount, 104);
  assert.equal(ledger.additionalHistoricalSourceCount, 4);
  assert.equal(ledger.files.length, 115);
  assert.equal(new Set(ledger.files.map((row) => row.path)).size, 115);
  assert.equal(ledger.handoffEnvelope.length, 1);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
    assert.match(row.commit, /^[0-9a-f]{40}$/);
  }

  const manifest = JSON.parse(read("research/clay_b_energy_atom_cost_screen_release_20260906.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.logical_predecessor, "ClayB-EulerCompactnessScreen-20260906");
  assert.equal(manifest.status, "RESEARCH_COMPLETE");
  assert.equal(manifest.is_clay_result, false);
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.compute.simulation, false);
  assert.equal(manifest.compute.DGX_required, false);
  assert.equal(manifest.compute.new_reader_PDF, false);
  assert.equal(manifest.recap.update_required, false);
  assert.deepEqual(manifest.excluded_user_paths, ["AGENTS.md"]);
});

test("BO.1 through BO.18 are continuous and retain the exact conditional-cost boundary", () => {
  const body = read("research/clay_b_energy_atom_dissipation_20260906.md");
  const tags = [...body.matchAll(/\\tag\{(BO\.\d+)\}/g)].map((match) => match[1]);
  assert.deepEqual(tags, Array.from({ length: 18 }, (_, index) => `BO.${index + 1}`));
  for (const marker of [
    "CONDITIONAL NECESSITY", "最后阈值", "全环面", "完整带符号", "N_r",
    "r^{1/2}", "嵌套窗口", "不能相加", "G OPEN", "NOT CLAY",
  ]) assert.ok(body.includes(marker), marker);
});

test("source QA preserves exact arithmetic, prior freeze, history, and open boundaries", () => {
  const qa = JSON.parse(read("research/clay_b_energy_atom_qa_20260906.json"));
  assert.equal(qa.status, "PASS");
  assert.equal(qa.sources.length, 3);
  assert.equal(qa.formula_tags_checked, 18);
  assert.equal(qa.arithmetic_checks.length, 18);
  assert.ok(qa.arithmetic_checks.every((row) => row.pass));
  assert.equal(qa.previous_freeze.rows_checked, 104);
  assert.deepEqual(qa.previous_freeze.failures, []);
  assert.equal(qa.historical_sources.rows.length, 4);
  assert.ok(qa.historical_sources.rows.every((row) => row.pass));
  assert.ok(Object.values(qa.limited_negative_controls).every(Boolean));
  assert.equal(qa.protected_state.user_agents_unchanged, true);
  assert.equal(qa.publication_state_inspected, false);
  assert.equal(qa.simulation, false);
  assert.equal(qa.G, "OPEN");
  assert.equal(qa.clay_result, false);

  const joined = [
    "research/clay_b_energy_atom_primary_reading_20260906.md",
    "research/clay_b_energy_atom_report_20260906.md",
    "research/clay_b_energy_atom_internal_audit_20260906.md",
  ].map(read).join("\n");
  for (const marker of [
    "不是外部同行评审", "完整抽读 PDF 1--7 页", "共同伴随", "嵌套尾积分不可相加",
    "本次实际推导的必要不等式没有产生矛盾", "NOT CLAY",
  ]) assert.ok(joined.includes(marker), marker);
});
