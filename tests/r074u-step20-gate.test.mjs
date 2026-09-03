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
  "research/r074u_publication_handoff.md": "115620fe742b3321c7d1422743b202ab83886beb4016fd8da45c81142d66a22b",
  "research/r074u_intrinsic_certified_residence.md": "e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99",
  "research/r074u_intrinsic_certified_residence_primary_audit.md": "b509d8201ae8334f6e589f65b63be65e6b2f427c9250c74a400c9419cc2de314",
  "research/r074u_intrinsic_residence_literature_audit.md": "0cf6e19a42e524aaf79aca10d72c5380029dce37032215974d99976a0b2a327c",
  "research/r074u_intrinsic_certified_residence_certificate.json": "4c79619f25ff207b69cc7342edf46aad2c579518c9ec25179296751641fcc649",
  "research/r074u_intrinsic_certified_residence_certificate_report.md": "607d1171803e2a21fe5c8776e72cbc735bc6341b0d09cb4c413b53735da2135d",
  "research/r074u_intrinsic_certified_residence_independent_audit.md": "fe9b34c23a1c2755ca0501a832f8acbe63c786613a2515c406c6c227d4f62fa2",
  "research/r074u_intrinsic_certified_residence_qa_report.md": "3dabeada679ef005c8e42d1b3feea751364a47d9244e3f376b3ae1db0b16b670",
  "scripts/r074u_intrinsic_certified_residence_certificate.py": "a1947f7af58049d13c2ca2f2a0d9653391045e09e23ef8b9fbfbbf50bda2fdaa",
  "scripts/r074u_intrinsic_certified_residence_certificate_independent.rb": "58ff798a631c2eab22621afaf16fe3f8d0de7e27a999dae090efc61694932505",
  "scripts/r074u_intrinsic_certified_residence_qa.sh": "b87d412ff8e540daff62f4dbb6b581cdc7eea4ab1c224b0689997ac74c363656",
};

test("R0.74U Step 20 frozen authority and exact evidence bytes", () => {
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.74U Step 20 primary certificate reproduces in an isolated directory", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074u-residence-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r074u_intrinsic_certified_residence_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074U_RESIDENCE_JSON: join(outputRoot, "certificate.json"),
        R074U_RESIDENCE_REPORT: join(outputRoot, "certificate-report.md"),
      },
    }));
    const result = JSON.parse(readFileSync(join(outputRoot, "certificate.json"), "utf8"));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.checks_passed}/${stdout.checks_total}`, finiteCases: stdout.finite_cases },
      { verdict: "PASS", groups: "31/31", finiteCases: 869 },
    );
    const groups = Object.groupBy(result.checks, (row) => row.group);
    assert.equal(groups.finite.length, 17);
    assert.equal(groups.finite.reduce((sum, row) => sum + row.cases, 0), 869);
    assert.equal(groups.structural.length, 6);
    assert.equal(groups.hash.length, 8);
    assert.ok(result.checks.every((row) => row.pass));
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r074u_intrinsic_certified_residence_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate-report.md"))).digest("hex"), frozen["research/r074u_intrinsic_certified_residence_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74U Step 20 independent Ruby verifier reproduces", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074u-residence-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r074u_intrinsic_certified_residence_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R074U_RESIDENCE_INDEPENDENT_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.groups_passed}/${stdout.groups_total}`, assertions: stdout.assertions },
      { verdict: "PASS", groups: "9/9", assertions: 1651 },
    );
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r074u_intrinsic_certified_residence_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74U Step 20 QA preserves fail-closed quantifier boundaries", () => {
  const report = bytes("research/r074u_intrinsic_certified_residence_qa_report.md").toString("utf8");
  for (const marker of [
    "PASS, 31/31 groups, 869 finite cases",
    "PASS, 9/9 groups, 1,651 independent Rational assertions",
    "23/23 rejected",
    "24/24 rejected",
    "PYTHONHASHSEED 0, 1, and 42",
    "corridor/K quantifiers",
    "does not machine-prove continuous PDE estimates",
  ]) assert.ok(report.includes(marker), marker);
});
