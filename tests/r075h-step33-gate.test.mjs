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
  "research/r075h_single_pass_transport_flux_closure.md": "849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9",
  "research/r075h_single_pass_transport_flux_closure_primary_audit.md": "3c85368e051102997e66ae36fa43290b6200e688db886380215fb40ec0bb757e",
  "research/r075h_report-source.md": "5b0b05b2ce903986ef8439a766766e8bdb97e2fe4d9eb6035f73102583b1b779",
  "scripts/r075h_single_pass_transport_flux_closure_fixtures.json": "7e4b5691d6929c97f72146c293a55e3b6fcf5875bc51f78bd1a58e9f84a0b217",
  "scripts/r075h_single_pass_transport_flux_closure_expected.json": "099d017cb7ff61d5a9dff54449c9a91a12e8657343bb11579ad135e9cd350573",
  "research/r075h_single_pass_transport_flux_closure_certificate.json": "1fda0c2e812a50a4f183b78ba503ce766553cd1dcbb1206384e07e3b1f0b0b38",
  "research/r075h_single_pass_transport_flux_closure_certificate_report.md": "c77dd0ea2896ad3914bf6d74c647d5b1ebae91cfaa522df16bf2196aa13ca5a0",
  "research/r075h_single_pass_transport_flux_closure_independent_audit.md": "9c1b09a5c996c371a4ed9bcb302fc211b9ea2e97014e4c5f3f985c23207e411b",
  "research/r075h_single_pass_transport_flux_closure_qa_report.md": "ed134d1411905dd052550ea932e9ca7c4d70c5f49b1f7194002844f950b35911",
  "scripts/r075h_single_pass_transport_flux_closure_certificate.py": "68fc20b109f6017940f8f137bc79a387076c2990b52fdfe44ad5b2c4a4beead5",
  "scripts/r075h_single_pass_transport_flux_closure_certificate_independent.rb": "0b5b591b84aba87bb7cb37d119abadc108217a3d77af1eeeb08a10d3178195af",
  "scripts/r075h_single_pass_transport_flux_closure_qa.sh": "bfaa1c8e3107c33a340c066178ea2e70edd74c4afcd16784996847703b6a941a",
};

test("R0.75H Step 33 repaired frozen whitelist has exactly twelve byte-identical objects", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75H Step 33 Python certificate runs from the frozen runtime dependencies", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075h-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["-B", "scripts/r075h_single_pass_transport_flux_closure_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075H_JSON: join(outputRoot, "certificate.json"),
        R075H_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 19, suite: "r075h-single-pass-transport-flux-closure", verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075h_single_pass_transport_flux_closure_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075h_single_pass_transport_flux_closure_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75H Step 33 independent Ruby certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075h-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075h_single_pass_transport_flux_closure_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075H_JSON: resolve(root, "research/r075h_single_pass_transport_flux_closure_certificate.json"),
        R075H_RUBY_REPORT: join(outputRoot, "independent.md"),
      },
    }));
    assert.deepEqual(stdout, { suite: "r075h-single-pass-transport-flux-closure-independent", verdict: "PASS", assertions: 22 });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075h_single_pass_transport_flux_closure_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75H QA closes the repaired dependency gate and preserves the E.24 stop line", () => {
  const qa = read("research/r075h_single_pass_transport_flux_closure_qa_report.md");
  for (const marker of [
    "Verdict: **PASS**",
    "Python assertions: 19/19",
    "Ruby assertions: 22/22",
    "66/66 Python; 66/66 Ruby",
    "Unknown mutations rejected fail-closed",
    "PYTHONHASHSEED byte stability: PASS",
    "H.1--H.29",
    "29/29 displays",
    "Only the signed pure-transport terminal-tube benchmark is certified",
    "regularity, and singularity remain OPEN",
    "NOT CLAY",
  ]) assert.ok(qa.includes(marker), marker);
  for (const path of Object.keys(frozen)) {
    const value = read(path);
    assert.equal(value.includes("\r"), false, path + ": carriage return");
    assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(value), false, path + ": control character");
  }
});
