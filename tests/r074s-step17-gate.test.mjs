import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "python3";

const frozen = {
  "research/r074s_recurrent_streamline_temporal_tail_obstruction.md": "7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5",
  "research/r074s_recurrent_streamline_primary_audit.md": "1efc7a520570c22952d7b06b0486865a767981f5303f102380eb9963754a1d4c",
  "research/r074s_recurrent_streamline_independent_audit.md": "255eea01cea10367b1d4051ea960214112ca8473a8b6df47ead4e199727afff3",
  "research/r074s_recurrent_streamline_literature_audit.md": "6c7c58da5250263e2509aa7c66f66bd7b02ef9fc7b920ce5c409661879a73ec8",
  "research/r074s_recurrent_streamline_certificate.json": "a4acf1769e9b56f372b15bfa0155755cb9f0a55a9a314f431d3df0add6f99c0c",
  "research/r074s_recurrent_streamline_certificate_report.md": "efb25a4068957b17910fdf9c345ad92f383d5525c316cad98d763e642c44d202",
  "research/r074s_recurrent_streamline_independent_report.md": "c3b33e4289ecb69f7958174569b55321cfec029fa1fd004c0fde996296742dc8",
  "scripts/r074s_recurrent_streamline_certificate.py": "139a5ce3d36d11b9480f246cc8f7c5297dd3ca86edb5938849e04b7f9f2eddab",
  "scripts/r074s_recurrent_streamline_independent.rb": "6c5181f64d6db424fa280a1a0886005049863a1eef602202631895ab0b95fadb",
};

test("R0.74S Step 17 frozen seal and exact evidence bytes", () => {
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.74S Step 17 primary certificate reproduces in an isolated output directory", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074s-recurrent-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r074s_recurrent_streamline_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074S_RECURRENT_JSON: join(outputRoot, "certificate.json"),
        R074S_RECURRENT_REPORT: join(outputRoot, "certificate-report.md"),
      },
    }));
    const result = JSON.parse(readFileSync(join(outputRoot, "certificate.json"), "utf8"));
    assert.equal(stdout.verdict, "PASS");
    assert.equal(stdout.finite_groups, "12/12");
    assert.equal(stdout.finite_cases, 4325);
    assert.equal(result.verdict, "PASS");
    assert.equal(result.finite_checks.length, 12);
    assert.equal(result.finite_checks.reduce((sum, row) => sum + row.cases, 0), 4325);
    assert.equal(result.structural_checks.length, 11);
    assert.equal(result.dependency_checks.length, 2);
    assert.equal(result.claim_boundary.S444_critical_L1_temporal_tail, "FALSE_BY_RECURRENT_SMOOTH_EXACT_NSE");
    assert.equal(result.claim_boundary.S472_fixed_deletion_positive_excursion, "OPEN");
    assert.equal(result.claim_boundary.direct_hybrid_terminal_flux_gate, "OPEN_NOT_REFUTED");
    assert.equal(result.claim_boundary.millennium_problem_solved, false);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74S Step 17 independent Ruby PASS report is frozen with its source-repository ancestry contract", () => {
  const report = bytes("research/r074s_recurrent_streamline_independent_report.md").toString("utf8");
  for (const marker of [
    "Verdict: PASS within the finite-audit and negative-theorem scope",
    "Step-17 core     7355c01dead23c3524242006318b02a8324447e6",
    "independent exact groups     7/7 PASS   (294 assertions)",
    "artifact and commit locks    4/4 PASS",
    "Step-17 semantic checks     20/20 PASS",
    "negative mutation probes    32/32 rejected",
    "artifact-path substitutions  3/3 rejected",
    "reproducibility assertions  14/14 PASS",
  ]) assert.ok(report.includes(marker), marker);
});
