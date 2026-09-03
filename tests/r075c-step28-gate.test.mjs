import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, rmSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const read = (path) => bytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "python3";

const frozen = {
  "research/r075c_background_shear_packing_false_positive.md": "1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89",
  "research/r075c_background_shear_packing_false_positive_primary_audit.md": "b3e1bc0b8e321e2a1bce0dafc74d21ad1f81048b63ab93f42f56e2c2a0760368",
  "research/r075c_background_shear_packing_false_positive_certificate.json": "d57a3d6d400dcd805c09e34ef7c2bec8b4abb35e8478a1e275f3a1324552355f",
  "research/r075c_background_shear_packing_false_positive_certificate_report.md": "5f91ed6b135a196849b26635a505ab809528c593db846e65a41569e13f166f50",
  "research/r075c_background_shear_packing_false_positive_independent_audit.md": "842b87327598c5458cc24937ea8def035886b9134221e77612bc778a2a3f4b8b",
  "research/r075c_background_shear_packing_false_positive_qa_report.md": "13f047fef4fb5934885d78a32f7ffcdc9a7e71eaa58b6afdbf92a965cc0c1afe",
  "scripts/r075c_background_shear_packing_false_positive_certificate.py": "2c75ae98b5ffb4c7c7b4c911758656db47ea349ec91e8c823d9309641853d010",
  "scripts/r075c_background_shear_packing_false_positive_certificate_independent.rb": "b9b8202a2d82cb5a735051cffe2ed4428f307f38c54e67a413adbd9ce20ea76b",
  "scripts/r075c_background_shear_packing_false_positive_qa.sh": "2282c525858c552c4151e4e5f65a83d3098a1d34f5afd50b02a44455fbbe98bb",
};

test("R0.75C Step 28 frozen whitelist has exactly nine byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 9);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75C Step 28 Python certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075c-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r075c_background_shear_packing_false_positive_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075C_JSON: join(outputRoot, "certificate.json"),
        R075C_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 8, mutation: null, verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075c_background_shear_packing_false_positive_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075c_background_shear_packing_false_positive_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75C Step 28 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075c-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075c_background_shear_packing_false_positive_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R075C_RUBY_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(stdout, { verdict: "PASS", assertions: 9, mutation: null });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075c_background_shear_packing_false_positive_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75C QA closes the finite gate and preserves the passive stop line", () => {
  const qa = read("research/r075c_background_shear_packing_false_positive_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 8/8",
    "Ruby assertions: 9/9",
    "18/18 and 19/19",
    "PYTHONHASHSEED byte stability: PASS",
    "Universal B.44 rejected",
    "B.45 not disproved",
    "passive dissipation OPEN",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, `${path}: carriage return`);
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, `${path}: control character`);
  }
});
