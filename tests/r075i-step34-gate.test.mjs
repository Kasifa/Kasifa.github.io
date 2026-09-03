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
  "research/r075i_diffusion_safe_block_participation.md": "c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7",
  "research/r075i_diffusion_safe_block_participation_primary_audit.md": "a8e481bfa28ba244a6022b782880ce9a86c40de29e3b0064474841eca99cecbd",
  "research/r075i_report-source.md": "8459adb6735caa2ee6c6e9c27202125cda34ad9072e2d78167f3f961e34f5de3",
  "scripts/r075i_diffusion_safe_block_participation_fixtures.json": "afda306afcf26640be72978b654a1a7dd1b23c0df5e92137f450520a6c7d515b",
  "scripts/r075i_diffusion_safe_block_participation_expected.json": "27514a38beec5c5e949a2a639faa5db539a4fbdeefec175e9e6e90a0507afd2a",
  "research/r075i_diffusion_safe_block_participation_certificate.json": "fc31d5b56d7d651885116d9624258075173e78476d8a173f99a20f2a5197f027",
  "research/r075i_diffusion_safe_block_participation_certificate_report.md": "dd775b48be540c91619b9e2254f0f93ef297e513f6a99beb9d63ba393dedfc3b",
  "research/r075i_diffusion_safe_block_participation_independent_audit.md": "e23174aa885311d07a097cdf9d8f571d0d6d1f59f33bdb6e4ceafb0ab4f5e4b2",
  "research/r075i_diffusion_safe_block_participation_qa_report.md": "5907f5dbf95d216bc5a2ac7bfbe989a8ae23f3509ed2570a0c38907e50ec01fb",
  "scripts/r075i_diffusion_safe_block_participation_certificate.py": "a9e006ee41fcb818bf8403f60efceb0fd08e62c42e5973065d853967ae7218df",
  "scripts/r075i_diffusion_safe_block_participation_certificate_independent.rb": "f4b3ceb0534a4bbd4861fd441accfaeb95374d5e9d91682b7fb66462519c73d0",
  "scripts/r075i_diffusion_safe_block_participation_qa.sh": "a24faf1abe00423f5c1e245efddcad59c4876989a671a19cee8066aed6f06e7e",
};

test("R0.75I Step 34 repaired frozen whitelist has exactly twelve byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75I Step 34 Python certificate runs from the frozen runtime dependencies", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075i-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["-B", "scripts/r075i_diffusion_safe_block_participation_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075I_JSON: join(outputRoot, "certificate.json"),
        R075I_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 18, suite: "r075i-diffusion-safe-block-participation", verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075i_diffusion_safe_block_participation_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075i_diffusion_safe_block_participation_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75I Step 34 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075i-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075i_diffusion_safe_block_participation_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075I_JSON: resolve(root, "research/r075i_diffusion_safe_block_participation_certificate.json"),
        R075I_RUBY_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(stdout, { suite: "r075i-diffusion-safe-block-participation-independent", verdict: "PASS", assertions: 24 });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075i_diffusion_safe_block_participation_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75I QA closes the repaired dependency gate and preserves the E.24 stop line", () => {
  const qa = read("research/r075i_diffusion_safe_block_participation_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 18/18",
    "Ruby assertions: 24/24",
    "83/83 Python; 83/83 Ruby",
    "Unknown mutations rejected fail-closed",
    "PYTHONHASHSEED byte stability: PASS",
    "I.1--I.27",
    "27/27 displays",
    "one-block estimate uses no PDE and is diffusion-safe",
    "sufficient only; high N_eff is not",
    "regularity, and singularity remain OPEN",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, path + ": carriage return");
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, path + ": control character");
  }
});
