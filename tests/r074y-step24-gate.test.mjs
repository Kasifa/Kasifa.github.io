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
  "research/r074y_publication_handoff.md": "d333ba1223bce44b4d5dd5d23fa123a185402560945899e4416e7a4ab27d53b4",
  "research/r074y_payment_compatible_route_screen.md": "6144fe796d6c59a286fc32b3b0aa2b794c50006fdc7879d4595b5958c9646954",
  "research/r074y_payment_compatible_route_screen_primary_audit.md": "c9b8ef6f78d0d196c2f17c6c7b83fe54667a6c80135553695dd7c68325af6f49",
  "research/r074y_payment_compatible_route_literature_audit.md": "e93275e31b1f04b1878071123fa3471a90e88fee5bb2b0dfd26afa6abf8d43a6",
  "research/r074y_payment_compatible_route_screen_certificate.json": "372779f48a53c0333f1d736528aab6eb74997dc9eac3da0634178052501dd80a",
  "research/r074y_payment_compatible_route_screen_certificate_report.md": "782c694f9edb49d668a473837d9c43f60b311ace9a9f9175b8870cac4291f2ae",
  "research/r074y_payment_compatible_route_screen_independent_audit.md": "b17af2ab982a85cd29a0fc7f3a632b390594505dd3c26e4afdff3ad0f5636d9e",
  "research/r074y_payment_compatible_route_screen_qa_report.md": "4ad724a6bd9ab9a344cb1ef579ba7ef47ebf3fa8cc8832c2c45cbe4be50fefbf",
  "scripts/r074y_payment_compatible_route_screen_certificate.py": "c0d6ee583bdc08fb42cf5cbf9b1e7fced3447b410434193d5004cc4b335a2dd2",
  "scripts/r074y_payment_compatible_route_screen_certificate_independent.rb": "d8e0d303e31b676eb143e94aab111d7c1126de6c26c34258103610fccdaa5435",
  "scripts/r074y_payment_compatible_route_screen_qa.sh": "675cbfe8e81be74b01d65a2dd035deaa4dee5d2d09ca20f7491b42e2d67c1a04",
};

test("R0.74Y Step 24 frozen authority and exact evidence bytes", () => {
  assert.equal(Object.keys(frozen).length, 11);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.74Y Step 24 primary certificate reproduces in an isolated directory", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074y-route-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r074y_payment_compatible_route_screen_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R074Y_JSON: join(outputRoot, "certificate.json"),
        R074Y_REPORT: join(outputRoot, "certificate-report.md"),
      },
    }));
    const result = JSON.parse(readFileSync(join(outputRoot, "certificate.json"), "utf8"));
    assert.deepEqual(
      { verdict: stdout.verdict, checks: stdout.checks, cases: stdout.cases },
      { verdict: "PASS", checks: 24, cases: 244 },
    );
    assert.equal(result.checks.filter((row) => row.group === "finite").length, 8);
    assert.equal(result.checks.filter((row) => row.group === "structural").length, 5);
    assert.equal(result.checks.filter((row) => row.group === "hash").length, 11);
    assert.ok(result.checks.every((row) => row.pass));
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r074y_payment_compatible_route_screen_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate-report.md"))).digest("hex"), frozen["research/r074y_payment_compatible_route_screen_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74Y Step 24 independent Ruby verifier reproduces", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r074y-route-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r074y_payment_compatible_route_screen_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R074Y_INDEPENDENT_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(
      { verdict: stdout.verdict, assertions: stdout.assertions },
      { verdict: "PASS", assertions: 21 },
    );
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r074y_payment_compatible_route_screen_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.74Y Step 24 QA preserves route-screen boundaries", () => {
  const report = bytes("research/r074y_payment_compatible_route_screen_qa_report.md").toString("utf8");
  for (const marker of [
    "Python: 24/24 checks, 244 cases",
    "Ruby: 21/21 independent assertions",
    "22/22 Python, 23/23 Ruby rejected",
    "Seeds 0/1/42 byte-identical",
    "FINITE EXACT ARITHMETIC/STRUCTURE ONLY",
  ]) assert.ok(report.includes(marker), marker);
});
