import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";
import { promisify } from "node:util";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const execFileAsync = promisify(execFile);

const frozen = new Map([
  ["research/r074k_problem_freeze.md", "ddb9467b2a68faae8f85bfc208393cd00fd90bc51ef02d723dfab24216bde2e4"],
  ["research/r074k_single_collar_shear_lag_reduction.md", "8f21248603551c39f34864dd921847dc8b9c6f70962209864901d476fe6722e3"],
  ["research/r074k_inward_tail_independent_audit.md", "df71c930f35bccf096c73261acf8a721c439eb15b932323fc8a1219379941656"],
  ["research/r074k_collar_reduction_independent_audit.md", "120856123269679c25de3d86b675cf948e6409cdb7a131cfd3ad06460c176285"],
  ["research/r074k_certificate_independent_audit.md", "89055883887b8a52003dd0f11224320855a6914d3e79213ac6d11e0e5602c6a1"],
  ["research/r074k_figure_independent_audit.md", "5a1ff2af46ef5ea8ddbac1f4056d7e9f0120d13336b33c2e043289a29fa33b0a"],
  ["research/r074k_final_source_rebind_audit.md", "45904c4307fc0b1745d44f903a62f6b06f2ed639ac7d49af4ebffb41d706a7e5"],
  ["research/r074k_freeze_manifest.json", "82e5750ab3153401ebab37f36d53c1d593ab4c6cbf4ec16a633330a88aa68769"],
  ["research/r074k_gap_matrix.md", "61382ecdd6ada4ef91883390ab03afbbc832c5ecd066fb7f26e22f11d916a4dc"],
  ["research/r074k_report-source.md", "457a0a72aa36fb35d8924b9d4af5cfc826c363e6b01852c8b3fc87be8fb7288b"],
  ["research/r074k_primary_literature_boundary.md", "a0b7d1204c9d54ee642ea7547c961ddfdb45ad1e76df88e30c3773e5a576cdd9"],
  ["research/r074k_primary_literature_independent_audit.md", "b14b219efcc2238c3067f627101bb3070769251b84876f268df55c718d9f1331"],
  ["research/r074k_bilingual_dictionary.md", "c83ded2c62979c42b27e3102907edada0248a70d02c870d9177e675ab5966f66"],
  ["scripts/r074k_single_collar_exponent_certificate.py", "c1de693bdae761826608ece64d518035e2d732578b191ce01158f30adedf0b5b"],
  ["research/r074k_single_collar_exponent_certificate.json", "67e4ab156d7d5a73fd07e584f3f87f7c9287591856b285bd9a747d00f85de41f"],
  ["research/r074k_single_collar_exponent_certificate_report.md", "86ee3ec729a087214a06c6520306bc6f8b8487d9f9df9aabe611276150b68958"],
  ["scripts/r074k_single_collar_exponent_certificate_independent.rb", "b37394432f673a9084acad963eafe32f9ab995243e1cff85fe3f819de184cc79"],
]);

test("R0.74K frozen mathematical assets remain byte-exact", async () => {
  for (const [path, expected] of frozen)
    assert.equal(sha256(await read(path)), expected, path);
});

test("R0.74K exact certificate reproduces frozen JSON", async () => {
  const python = process.env.CODEX_PYTHON || process.env.PYTHON || "python3";
  const { stdout } = await execFileAsync(python, ["scripts/r074k_single_collar_exponent_certificate.py"], {
    cwd: root, maxBuffer: 10 * 1024 * 1024,
  });
  assert.deepEqual(Buffer.from(stdout), await read("research/r074k_single_collar_exponent_certificate.json"));
});

test("R0.74K independent exact reconstruction matches every row", async () => {
  const { stdout } = await execFileAsync("/usr/bin/ruby", ["scripts/r074k_single_collar_exponent_certificate_independent.rb"], {
    cwd: root, maxBuffer: 10 * 1024 * 1024,
  });
  assert.match(stdout, /independentPassed=41/);
  assert.match(stdout, /independentTotal=41/);
  assert.match(stdout, /mismatchCount=0/);
  assert.match(stdout, /nearestPositiveVolumeWrongMargin=536399\/8583708672/);
  assert.match(stdout, /uniformDeepMargin=204385\/134120448/);
  assert.match(stdout, /result=PASS/);
});

test("R0.74K frozen primary figure package remains byte-exact and valid", async () => {
  const base = "research/figures/r074k/fig-r074k-single-inward-collar";
  assert.equal((await readdir(resolve(root, base))).length, 25);
  const expected = new Map([
    ["figure.svg", "599c269979c368473fbcb57f6691025ec06ee909ca19efbae35e078b79f0745e"],
    ["figure.pdf", "826fb9441fbdfa699f39bd528314529a734bf9f371e009aa60d86c6e9046c3bc"],
    ["figure.png", "d0644e4d3b98c73ed53151e9816f7d3ce68028150ede9d939c13eab173a624b5"],
    ["source-data.csv", "defae44140159e2d3d97271da559fb9f49520e1e50c17191529af0bbad429d32"],
    ["SHA256SUMS", "59ad9518f0525e6fb9234aa4660511ab78bbda14eccf94c1bd5ed680f070753c"],
    ["manifest.json", "758e9335265928deaa7874b3fed1689dcacc66b1a82a673f0231ca9ba3faddbd"],
    ["validation.json", "cd5919984d6b4e5b1c93b7ac58e9e45d7c762f00abba4c6098f9a7635cdf1092"],
  ]);
  for (const [name, digest] of expected)
    assert.equal(sha256(await read(`${base}/${name}`)), digest, name);
  const python = process.env.CODEX_PYTHON || process.env.PYTHON || "python3";
  const portableVerifier = String.raw`
import importlib.util
import shutil
import sys
from pathlib import Path

validator_path = Path(sys.argv[1]).resolve()
spec = importlib.util.spec_from_file_location("r074k_figure_validator", validator_path)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
pdfinfo = shutil.which("pdfinfo")
if not pdfinfo:
    raise SystemExit("portable verifier requires pdfinfo on PATH")
validator.PDFINFO = Path(pdfinfo)
sys.argv = [str(validator_path), "--verify-only"]
validator.main()
`;
  const { stdout } = await execFileAsync(python, ["-B", "-c", portableVerifier, `${base}/validate.py`], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.match(stdout, /verify-only PASS 41\/41; 25 files; seals PASS/);
});
