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
  "research/r074v_publication_handoff.md": "3832ebf8b0fc84ecbb21d064ee3c94a73ce2f56966f29a0d911a6a411c2697ca",
  "research/r074v_completed_clock_upper_route.md": "031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c",
  "research/r074v_completed_clock_upper_route_primary_audit.md": "148b41ef2755d6ca42927595362fd59c81db8880713293a8e82c1c288fdea77d",
  "research/r074v_completed_clock_upper_route_certificate.json": "993054e2881ec5f7ea3a849c6d37c29b978b1cf16c18b1b450eb2c64ee7834bd",
  "research/r074v_completed_clock_upper_route_certificate_report.md": "4f6ff6943ef6e9cbfcde9f882670b72c507ca1efa6ef9f7248e9d7afec8f5bf8",
  "research/r074v_completed_clock_upper_route_independent_audit.md": "ef6626aea8b2e2b27044e34c7af1637192974ef6b6acae54221eb32e092a4880",
  "research/r074v_completed_clock_upper_route_qa_report.md": "7497748757041f08cea48ad654689d300f7ee7c63bb76c2f6bc717deffb54822",
  "scripts/r074v_completed_clock_upper_route_certificate.py": "76e823e63fe0ee46a32188c55bfbae0359581656470b064503cebf7b822956d6",
  "scripts/r074v_completed_clock_upper_route_certificate_independent.rb": "0f4295bea84f497f102064c4335fd5fafa0bc8e396d270297df5ed792bf2abcf",
  "scripts/r074v_completed_clock_upper_route_qa.sh": "a200b344f1cd93d7519fd342a35018621e3a570953933611fa12316b0c08276e",
};

test("R0.74V Step 21 frozen authority and exact evidence bytes", () => {
  assert.equal(Object.keys(frozen).length, 10);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.74V Step 21 primary certificate reproduces in an isolated directory", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074v-route-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r074v_completed_clock_upper_route_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074V_JSON: join(outputRoot, "certificate.json"),
        R074V_REPORT: join(outputRoot, "certificate-report.md"),
      },
    }));
    const result = JSON.parse(readFileSync(join(outputRoot, "certificate.json"), "utf8"));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.groups_passed}/${stdout.groups_total}`, finiteCases: stdout.finite_cases },
      { verdict: "PASS", groups: "33/33", finiteCases: 77 },
    );
    const groups = Object.groupBy(result.checks, (row) => row.group);
    assert.equal(groups.finite.length, 17);
    assert.equal(groups.finite.reduce((sum, row) => sum + row.cases, 0), 77);
    assert.equal(groups.structural.length, 6);
    assert.equal(groups.hash.length, 10);
    assert.ok(result.checks.every((row) => row.pass));
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r074v_completed_clock_upper_route_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate-report.md"))).digest("hex"), frozen["research/r074v_completed_clock_upper_route_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74V Step 21 independent Ruby verifier reproduces", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074v-route-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r074v_completed_clock_upper_route_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R074V_INDEPENDENT_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.groups_passed}/${stdout.groups_total}`, assertions: stdout.assertions },
      { verdict: "PASS", groups: "7/7", assertions: 106 },
    );
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r074v_completed_clock_upper_route_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74V Step 21 QA preserves route-only boundaries", () => {
  const report = bytes("research/r074v_completed_clock_upper_route_qa_report.md").toString("utf8");
  for (const marker of [
    "PASS, 33/33 groups, 77 finite cases",
    "PASS, 7/7 groups, 106 independent assertions",
    "29/29 rejected",
    "30/30 rejected",
    "PYTHONHASHSEED 0, 1, 42",
    "does not prove the proposed occupation estimates",
    "remote common-shear comparison",
    "completed-clock upper",
  ]) assert.ok(report.includes(marker), marker);
});
