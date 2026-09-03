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
  "research/r074t_publication_handoff.md": "13ff4edeeebf1da9c9356246c3308e67109857bf36fbceb67fcba5188c1fa71f",
  "research/r074t_schedule_invariant_dwell_coercivity.md": "8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd",
  "research/r074t_schedule_invariant_dwell_primary_audit.md": "0a0a66f6e8d84bb6fad18f6744f02bbf4c2848c96fa5b37dd4b8dc49c628ef99",
  "research/r074t_schedule_invariant_literature_audit.md": "60b49f6279c696a370af5f8050a6162753372eba81f8215e02e15259f084e88b",
  "research/r074t_schedule_invariant_dwell_certificate.json": "ab78d8a8e9a76dc2650d147836c3a51d011c6ef7866f84aa08ed4868b8323c47",
  "research/r074t_schedule_invariant_dwell_certificate_report.md": "acb54e58cf4af40d759962a593a17379cf2bc9769d9664abae800f6afe73764c",
  "research/r074t_schedule_invariant_dwell_independent_audit.md": "81d51239452e48b692125f5a19d2cc1a1ca66c5b65aa0405a1b8d429279b289d",
  "research/r074t_schedule_invariant_dwell_qa_report.md": "b942f990639600a1357518a92361b9c971f5fbaccb2b2bd92189448975b7996a",
  "scripts/r074t_schedule_invariant_dwell_certificate.py": "3229eb8f50a03d66e30449c36070f8734bdded6ed7b11e11324013597b715895",
  "scripts/r074t_schedule_invariant_dwell_certificate_independent.rb": "5fedbd8496e66cc55a4c624b57b21e229a00c948de28df59f91f5ac7461ea03e",
  "scripts/r074t_schedule_invariant_dwell_qa.sh": "371b5c74b1210cd7e8e8151472786b0992e2771ae8e08812f158febfee61b64e",
};

test("R0.74T Step 19 frozen authority and exact evidence bytes", () => {
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.74T Step 19 primary certificate reproduces in an isolated directory", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074t-dwell-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r074t_schedule_invariant_dwell_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074T_DWELL_JSON: join(outputRoot, "certificate.json"),
        R074T_DWELL_REPORT: join(outputRoot, "certificate-report.md"),
      },
    }));
    const result = JSON.parse(readFileSync(join(outputRoot, "certificate.json"), "utf8"));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.checks_passed}/${stdout.checks_total}`, finiteCases: stdout.finite_cases },
      { verdict: "PASS", groups: "31/31", finiteCases: 18933 },
    );
    assert.equal(result.verdict, "PASS");
    const groups = Object.groupBy(result.checks, (row) => row.group);
    assert.equal(groups.finite.length, 17);
    assert.equal(groups.finite.reduce((sum, row) => sum + row.cases, 0), 18933);
    assert.equal(groups.structural.length, 6);
    assert.equal(groups.hash.length, 8);
    assert.ok(result.checks.every((row) => row.pass));
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r074t_schedule_invariant_dwell_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate-report.md"))).digest("hex"), frozen["research/r074t_schedule_invariant_dwell_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74T Step 19 independent Ruby verifier reproduces", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074t-dwell-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r074t_schedule_invariant_dwell_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074T_DWELL_INDEPENDENT_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.groups_passed}/${stdout.groups_total}`, assertions: stdout.assertions },
      { verdict: "PASS", groups: "11/11", assertions: 9201 },
    );
    assert.equal(
      createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"),
      frozen["research/r074t_schedule_invariant_dwell_independent_audit.md"],
    );
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74T Step 19 QA report preserves fail-closed and scope boundaries", () => {
  const report = bytes("research/r074t_schedule_invariant_dwell_qa_report.md").toString("utf8");
  for (const marker of [
    "PASS, 31/31 groups, 18,933 exact finite cases",
    "PASS, 11/11 groups, 9,201 independent assertions",
    "26/26 rejected",
    "27/27 rejected",
    "PYTHONHASHSEED 0, 1, and 42",
    "It does not machine-prove continuous PDE inputs",
    "regularity, or a Clay claim",
  ]) assert.ok(report.includes(marker), marker);
});
