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
  "research/r074s_fixed_deletion_certificate.json": "3594d71f53c60e9e2b03c139ac1be79fba9a93c71f11d2cd73a9c85aa30ebe00",
  "research/r074s_fixed_deletion_certificate_report.md": "9fd733deff824fe856c41879d130d753770b0e88fa1d03f90cac67ed29ef4283",
  "research/r074s_fixed_deletion_independent_audit.md": "93ecdb2457d77fb945abe2bd71891c0d115fcaf2c3c8280ddf790ea4944a9324",
  "research/r074s_fixed_deletion_literature_audit.md": "fea7470814c0c21399c6e2b25961e8b3791e584cc24612ac37e9d1be7ce707ce",
  "research/r074s_fixed_deletion_primary_audit.md": "dd9abf2e818ef096aa7fe9e2218b88c55ffb94fa6882a572f85f0f08ed31bab8",
  "research/r074s_fixed_deletion_qa_report.md": "7c53c59053204d3a3e4fce6184ca94b0f5693e37ccaa3d37647c8f5d0ceb2587",
  "research/r074s_fixed_deletion_simultaneous_height.md": "305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1",
  "scripts/r074s_fixed_deletion_certificate.py": "a2700804af8b292b86596b23cd19ccd2d9f2cdde723c95b1ce6d0bfa0d09f035",
  "scripts/r074s_fixed_deletion_certificate_independent.rb": "f21eb45ef39bc4f10211cc1a5852e8b1d22c671a5eab52377ddf867647b4009f",
  "scripts/r074s_fixed_deletion_qa.sh": "d6985c1dbaf843095478044ebfe38d79a641205b500f0cdc738a12ae97b87e5f",
};

test("R0.74S Step 18 frozen authority and exact evidence bytes", () => {
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.74S Step 18 primary certificate reproduces in an isolated directory", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074s-fixed-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r074s_fixed_deletion_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074S_FIXED_DELETION_JSON: join(outputRoot, "certificate.json"),
        R074S_FIXED_DELETION_REPORT: join(outputRoot, "certificate-report.md"),
      },
    }));
    const result = JSON.parse(readFileSync(join(outputRoot, "certificate.json"), "utf8"));
    assert.equal(stdout.verdict, "PASS");
    assert.equal(stdout.finite_cases, 283157);
    assert.equal(stdout.checks_passed, 15);
    assert.equal(stdout.checks_total, 15);
    assert.equal(result.verdict, "PASS");
    const groups = Object.groupBy(result.checks, (row) => row.group);
    assert.equal(groups.finite.length, 5);
    assert.equal(groups.finite.reduce((sum, row) => sum + row.cases, 0), 283157);
    assert.equal(groups.structural.length, 5);
    assert.equal(groups.hash.length, 5);
    assert.ok(result.checks.every((row) => row.pass));
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74S Step 18 independent Ruby verifier reproduces", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074s-fixed-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r074s_fixed_deletion_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074S_FIXED_DELETION_INDEPENDENT_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.groups_passed}/${stdout.groups_total}`, assertions: stdout.assertions },
      { verdict: "PASS", groups: "8/8", assertions: 72144 },
    );
    assert.equal(
      createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"),
      frozen["research/r074s_fixed_deletion_independent_audit.md"],
    );
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74S Step 18 QA report preserves fail-closed and scope boundaries", () => {
  const report = bytes("research/r074s_fixed_deletion_qa_report.md").toString("utf8");
  for (const marker of [
    "PASS, 15/15 groups",
    "283,157 finite rational cases",
    "PASS, 8/8 groups",
    "72,144 independent assertions",
    "3/3\\text{ seeds PASS}",
    "12/12\\text{ Python mutations rejected}",
    "13/13\\text{ Ruby mutations rejected}",
    "It does not convert finite testing",
    "into a machine proof of suitable-weak local-energy theory",
  ]) assert.ok(report.includes(marker), marker);
});
