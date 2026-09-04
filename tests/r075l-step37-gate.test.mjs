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
  "research/r075l_single_harmonic_diffusive_signed_flux_gain.md": "52e25b2fdf1a224609c9e8fafa1c041b7f09a361f75f4b3e44ebcdddb756cdf5",
  "research/r075l_single_harmonic_diffusive_signed_flux_gain_primary_audit.md": "a7578e5370d182decc39f0da2f2fb581e5ef842ae7b914a120b5784bc32bd302",
  "research/r075l_report-source.md": "a300de54b9fe06e94455a055bbb42bdce8ec7bb004080389a95412966a5b941a",
  "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_fixtures.json": "0b9ba1f018b6e52414f20dee6687f5ff55c5ea0ef247ddbd905bc8c204245ad9",
  "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_expected.json": "9178489eaf9f44c5b182b6080cce7212591b1a3dd86459ecbd82c1382b38db9a",
  "research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json": "318136308fb0b1e46046b6483269e70b0a2d57dc44be18616236a10c5271a567",
  "research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_report.md": "00c490616bdb6641a862152a315ac76861ff345d8654137dea1d5fce552b2772",
  "research/r075l_single_harmonic_diffusive_signed_flux_gain_independent_audit.md": "31a67ab57a7c3f591f3e4dbd446dada04720ed62170e7cd0773123acc8d20604",
  "research/r075l_single_harmonic_diffusive_signed_flux_gain_qa_report.md": "387e80857b32e5048210b77a4a685be7a69c8f8e9f8da1514305a1ae96368e63",
  "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.py": "a521194d3ab26e23ffc13450244dcd92c52ac774bfb647348ebb2fac09c2571f",
  "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_independent.rb": "50888ee85e72c472881eab10145020888eda1558a7a5eb067aaaf5c61b3c307c",
  "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_qa.sh": "fa336a8dad20a400494eeb0b28a91bbb5077396238d094f5bf1621e367b7a175",
};

test("R0.75L Step 37 frozen whitelist has exactly twelve byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75L Step 37 Python certificate runs from the frozen runtime dependencies", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075l-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["-B", "scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075L_JSON: join(outputRoot, "certificate.json"),
        R075L_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 19, suite: "r075l-single-harmonic-diffusive-signed-flux-gain", verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75L Step 37 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075l-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075l_single_harmonic_diffusive_signed_flux_gain_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075L_JSON: resolve(root, "research/r075l_single_harmonic_diffusive_signed_flux_gain_certificate.json"),
        R075L_RUBY_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(stdout, { suite: "r075l-single-harmonic-diffusive-signed-flux-gain-independent", verdict: "PASS", assertions: 20 });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075l_single_harmonic_diffusive_signed_flux_gain_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75L QA closes the frozen dependency gate and preserves the E.24 stop line", () => {
  const qa = read("research/r075l_single_harmonic_diffusive_signed_flux_gain_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 19/19",
    "Ruby assertions: 20/20",
    "120/120 Python; 120/120 Ruby",
    "Unknown mutations rejected fail-closed",
    "PYTHONHASHSEED byte stability: PASS",
    "L.1--L.17",
    "17/17 displays",
    "0,+/-2k modes",
    "k^(-2/3)",
    "E.24",
    "singularity remain open",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, path + ": carriage return");
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, path + ": control character");
  }
});
