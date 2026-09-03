import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "python3";
const figureId = "fig-r074x-three-packet-payment-gate";

const frozen = {
  "research/r074x_publication_handoff.md": "c5bf4fc67476a489f3f473635d4b2106590457f0308208046d937989967a2122",
  "research/r074x_three_packet_fixed_deletion_gate.md": "4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3",
  "research/r074x_three_packet_fixed_deletion_gate_primary_audit.md": "834ec846c3f8629f9e7462caf4503bfa99ba6b88288da2dd525793206de9357e",
  "research/r074x_three_packet_fixed_deletion_literature_audit.md": "f58f7a1d095ba6bd8b27c41872301fd367fe784597160fe060f9cd332c64c422",
  "research/r074x_three_packet_fixed_deletion_gate_certificate.json": "61f379041752142e2d1dd6d20288643f92dc64e8df73d2c26b34f6c9b847b76e",
  "research/r074x_three_packet_fixed_deletion_gate_certificate_report.md": "39357cf2cfc40cb86244e7f6ce3bf5e742f7931c1f1398e2fca3ca28533475f3",
  "research/r074x_three_packet_fixed_deletion_gate_independent_audit.md": "6b28a7dd454b4b75c8cd2cdaa86cd2e2727913540d86babd8d011584aa35c1b6",
  "research/r074x_three_packet_fixed_deletion_gate_qa_report.md": "ba46f446634a3be0584b50fdfc035f26c83f8e013bab9ea92ae04230f9531fc4",
  "scripts/r074x_three_packet_fixed_deletion_gate_certificate.py": "3a8a028b8d66e04f41e728bdc639ae23dc8fddfd2b6d2528ddf51023b467b00d",
  "scripts/r074x_three_packet_fixed_deletion_gate_certificate_independent.rb": "c019cb65ef3be236be42e44e0840dce755f2d63fc77bb21fee6873f5cc9790ec",
  "scripts/r074x_three_packet_fixed_deletion_gate_qa.sh": "c44636c754004158788552755d1bbf1231bd91b78789de1120574a2fc959775c",
};

test("R0.74X Step 23 frozen authority and exact evidence bytes", () => {
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.74X Step 23 primary certificate reproduces in an isolated directory", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074x-remote-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r074x_three_packet_fixed_deletion_gate_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R074X_JSON: join(outputRoot, "certificate.json"), R074X_REPORT: join(outputRoot, "certificate-report.md") },
    }));
    const result = JSON.parse(readFileSync(join(outputRoot, "certificate.json"), "utf8"));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.checks_passed}/${stdout.checks_total}`, cases: stdout.cases },
      { verdict: "PASS", groups: "31/31", cases: 231 },
    );
    assert.equal(result.checks.filter((row) => row.group === "finite").length, 13);
    assert.equal(result.checks.filter((row) => row.group === "structural").length, 5);
    assert.equal(result.checks.filter((row) => row.group === "hash").length, 13);
    assert.ok(result.checks.every((row) => row.pass));
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r074x_three_packet_fixed_deletion_gate_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate-report.md"))).digest("hex"), frozen["research/r074x_three_packet_fixed_deletion_gate_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74X Step 23 independent Ruby verifier reproduces", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074x-remote-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r074x_three_packet_fixed_deletion_gate_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R074X_INDEPENDENT_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(
      { verdict: stdout.verdict, groups: `${stdout.groups_passed}/${stdout.groups_total}`, assertions: stdout.assertions },
      { verdict: "PASS", groups: "5/5", assertions: 36 },
    );
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r074x_three_packet_fixed_deletion_gate_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74X Step 23 QA preserves fail-closed probability and deletion boundaries", () => {
  const report = bytes("research/r074x_three_packet_fixed_deletion_gate_qa_report.md").toString("utf8");
  for (const marker of [
    "31/31 checks, 231 cases/assertions",
    "5/5 groups, 36 assertions",
    "Python 24/24, Ruby 25/25 rejected",
    "PYTHONHASHSEED 0/1/42",
    "No analytic, fixed-deletion, novelty, or Clay proof",
  ]) assert.ok(report.includes(marker), marker);
});

test("R0.74X Step 23 frozen figure archive has exact complete hash coverage", () => {
  const archive = resolve(root, "research/figures/r074x", figureId);
  const names = readdirSync(archive).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  const ledgerRows = readFileSync(resolve(archive, "SHA256SUMS"), "utf8").trim().split("\n");
  assert.equal(ledgerRows.length, 24);
  const ledgerNames = [];
  for (const row of ledgerRows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, row);
    assert.equal(sha(`research/figures/r074x/${figureId}/${match[2]}`), match[1], match[2]);
    ledgerNames.push(match[2]);
  }
  assert.deepEqual(ledgerNames, names.filter((name) => name !== "SHA256SUMS"));
  assert.equal(sha(`research/figures/r074x/${figureId}/figure.svg`), "e0e858e33c799b567e39ce22735bbeb024c3b32b2ead54f6bc170efe3e497c5a");
  assert.equal(sha(`research/figures/r074x/${figureId}/figure.png`), "cd8994befbbf2c0c84925de0a8c84c1c8a264c86a87efed85317b334cbf6e835");
  assert.equal(sha(`research/figures/r074x/${figureId}/figure.pdf`), "a4dc69fb82457420d7883f9ba6785751e7d7c9f7465218ca89748ea0aa01301f");
});
