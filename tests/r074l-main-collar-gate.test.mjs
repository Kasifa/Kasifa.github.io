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
  ["research/r074l_problem_freeze.md", "9f4cb6ce7e8cf02dbec788af8d30b06dd405b4e5f0975f28d1ab823118476856"],
  ["research/r074l_forward_bridge_bv_reduction.md", "d920e3845b38f75f187a78193b874e18d4551adf7dc03db59d5e785451654bf8"],
  ["research/r074l_main_collar_independent_audit.md", "11375ac767b14a1656ecc62dd84140b642b2a02d0c75fd5f69a9bc0a0aa70348"],
  ["research/r074l_final_source_rebind_audit.md", "e7043748a64949410bb85991bd6f3b2554d5ce1b3178a3ea0bb8364acfe4c1dc"],
  ["research/r074l_gap_matrix.md", "241c98db0b84ffd45f2dbdacc78425d3f01c559209047ef0aedf71a8e2f1f9c3"],
  ["research/r074l_primary_literature_audit.md", "d188933f1fce855f03d1b99a94f2e395e331448c54e8d06f0a32425a56f2e88b"],
  ["research/r074l_report-source.md", "aa049f52a6add4b346b6f17491f66ff7dc56d8b4610c64d4563f2b8099611ae6"],
  ["research/r074l_bilingual_dictionary.md", "e31c70998ac43d7f869e52a03c41e4e64f71d2fbdb4061f6abfb852fbd2e1876"],
  ["research/r074l_main_collar_certificate.json", "252808d60f90343e3a9d614f0ae11003984498d2362e05f9441d53175bcafd7e"],
  ["research/r074l_main_collar_certificate_report.md", "7b7557590de2f48c0f57debd461338395ed487c10522d9a9a8708f43eae8b3d8"],
  ["research/r074l_certificate_independent_audit.md", "b7c35c2d9c5a4e38caaa7ad6c4a655dc7183d535cf377d137da892fcf4c099a4"],
  ["research/r074l_figure_independent_audit.md", "14a9c6f0f6f54b1d9922a9306d95aa31aca0059e9b86672ad8305b86bc5f8089"],
  ["research/r074l_freeze_manifest.json", "4e394834a4e7d0f6125ff7e2bc0e9a8dc281d16e37ea33602199159e5a70a3dd"],
  ["scripts/r074l_main_collar_certificate.py", "fbf7a07b5a0a20336a4177c556ca5ea9342aeb0101b9f857bbda5b9144ae2420"],
  ["scripts/r074l_main_collar_certificate_independent.rb", "39196aa8741a62863094c34c49f51e7a5c4146a0526d1657cb3482d3f8883619"],
]);

test("R0.74L frozen mathematical assets remain byte-exact", async () => {
  for (const [path, expected] of frozen)
    assert.equal(sha256(await read(path)), expected, path);
});

test("R0.74L exact certificate reproduces frozen JSON", async () => {
  const python = process.env.CODEX_PYTHON || process.env.PYTHON || "python3";
  const { stdout } = await execFileAsync(python, ["scripts/r074l_main_collar_certificate.py"], {
    cwd: root, maxBuffer: 10 * 1024 * 1024,
  });
  assert.deepEqual(Buffer.from(stdout), await read("research/r074l_main_collar_certificate.json"));
});

test("R0.74L independent exact reconstruction matches all 24 rows", async () => {
  const { stdout } = await execFileAsync("/usr/bin/ruby", ["scripts/r074l_main_collar_certificate_independent.rb"], {
    cwd: root, maxBuffer: 10 * 1024 * 1024,
  });
  assert.match(stdout, /RESULT: PASS \(24\/24 checks\)/);
  assert.match(stdout, /bad_exponent_reserve/);
  assert.match(stdout, /good_R_power/);
  assert.match(stdout, /certificate_sha256: 252808d60f90343e3a9d614f0ae11003984498d2362e05f9441d53175bcafd7e/);
});

test("R0.74L frozen primary figure package remains byte-exact and valid", async () => {
  const base = "research/figures/r074l/fig-r074l-forward-clock-bv";
  assert.equal((await readdir(resolve(root, base))).length, 23);
  const expected = new Map([
    ["figure.svg", "1984bfc1aa6485601955caf1cdf7f728941429b28dfee1ae4db39f213ebb21fa"],
    ["figure.pdf", "6d714dab40747125f1b6587342c6fa559d5eaf26e8690a3e9de33770b75d3fb1"],
    ["figure.png", "8fa2e33db7f7713e0c54e924468b3135a94b10812cafb0c2f3d1429ca1e0026d"],
    ["source-data.csv", "1f57ff93fb730c630e756f858e6794942045ce4eecd4a7032888519548ce755a"],
    ["validation.json", "390d8ef9f66e115f4c4c4a914270824f9ecaea3462e39b8a6573977d84ba6ab0"],
    ["manifest.json", "4ad82fb1cfd7f9d1aea43ea5378bd1a626bc80933e94c26e8f3008f7dad83c42"],
    ["SHA256SUMS", "4e2df61354222bc74cc343315e98397c0a9bad05289097ac8fcc9006eeb1215d"],
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
spec = importlib.util.spec_from_file_location("r074l_figure_validator", validator_path)
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)
pdfinfo = shutil.which("pdfinfo")
if not pdfinfo:
    raise SystemExit("portable verifier requires pdfinfo on PATH")
validator.PDFINFO = Path(pdfinfo)
validator.PYTHON = Path(sys.executable)
sys.argv = [str(validator_path), "--verify-only"]
validator.main()
`;
  const { stdout } = await execFileAsync(python, ["-B", "-c", portableVerifier, `${base}/validate.py`], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.match(stdout, /verify-only PASS 45\/45; 21 package entries/);

  for (const [name, digest] of expected)
    assert.equal(sha256(await read(`${base}/${name}`)), digest, `post-validation ${name}`);
});
