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
  ["research/r074i_suitable_weak_tube_and_log_obstruction.md", "70ff507704c6c7aed5ea8bc0250a96373113975e8e3f92edd53e3193d7cd8457"],
  ["research/r074i_weak_extension_independent_audit.md", "68b3e02ab836106c1598ce8aa32017f83ad3f527e7b1a4aaa8f735851e6fccc1"],
  ["research/r074i_epsilon_log_independent_audit.md", "a59ff3f27a9e5322aecd5ac057458af0e508c62421f77082a4509fcd822791df"],
  ["research/r074i_final_source_rebind_audit.md", "edfa7ecbf8dd083c45732766c9045ec4a851ce41bcdf6ae978d8040a0aee7d63"],
  ["research/r074i_report-source.md", "4b2b48a45e2606ddc534d92ee1032b36d9d1b5d7169640d9311b3521d779c57e"],
  ["research/r074i_primary_literature_boundary.md", "8790ffa0de714d925569ee5de444188b970b306c35f4027aad5761b62f122b55"],
  ["research/r074i_primary_literature_independent_audit.md", "83f0e1aa746ddd1164f67517b5a60c2547940ea2ab92f43d537ad8875ca20b3a"],
  ["research/r074i_gap_matrix.md", "78cb76beb542bdd2e836d7f357838d0d11518bd989bf9c396443dde27a840374"],
  ["research/r074i_bilingual_dictionary.md", "3acff1d10887d8c07b9389137bfdbfca1331915ffb3b81870554dcff2c27d530"],
  ["scripts/r074i_tube_log_certificate.py", "5411134949eedbb1c285607c33a4f8feb9f8d358f5fc7cee91ec3601dfe3932f"],
  ["research/r074i_tube_log_certificate.json", "d4d0f32f6772bdae8a9ec0e8fd6f5f5f9248877df3c19bf544c3577055ab7bf5"],
  ["research/r074i_tube_log_certificate_report.md", "3be483123d3841a7f195a192374d56bb9ef453fe3ba2ee59ed6dc2e4fa68b0bf"],
  ["scripts/r074i_tube_log_certificate_independent.rb", "2c591dac16bce3ea456070775ac9c68408f0b32fb1492cd039b6e7d52f0040ad"],
  ["research/r074i_certificate_independent_audit.md", "a70cc641338b2e58aafce8cfe6ddadb08b05d9f35494b5d92f12bea9c8152c59"],
  ["research/r074i_freeze_manifest.json", "5b14a1e42aefcd48494be8ecbeda5d263a235cccf239eaca0aa00ed72308446e"],
]);

test("R0.74I frozen mathematical assets remain byte-exact", async () => {
  for (const [path, expected] of frozen)
    assert.equal(sha256(await read(path)), expected, path);
});

test("R0.74I exact certificate reproduces the frozen JSON", async () => {
  const python = process.env.PYTHON || "python3";
  const { stdout } = await execFileAsync(python, ["scripts/r074i_tube_log_certificate.py"], {
    cwd: root,
    maxBuffer: 10 * 1024 * 1024,
  });
  assert.deepEqual(Buffer.from(stdout), await read("research/r074i_tube_log_certificate.json"));
});

test("R0.74I independent exact reconstruction matches all rows", async () => {
  const { stdout } = await execFileAsync("/usr/bin/ruby", ["scripts/r074i_tube_log_certificate_independent.rb"], {
    cwd: root,
    maxBuffer: 10 * 1024 * 1024,
  });
  const result = JSON.parse(stdout);
  assert.equal(result.result, "PASS");
  assert.equal(result.leaf_field_comparisons, 269);
  assert.equal(result.mismatch_count, 0);
  assert.deepEqual(result.independent_summary, { passed: 36, total: 36 });
});

test("R0.74I frozen primary figure package remains byte-exact", async () => {
  const base = "research/figures/r074i/fig-r074i-moving-tube-log-screen";
  assert.equal((await readdir(resolve(root, base))).length, 24);
  const expected = new Map([
    ["figure.svg", "0ae2e2f2af20704705c711a7c3773373541794f326dfa881f3927a5416927bc3"],
    ["figure.pdf", "83a2dbd23130da9a4018aa06c13bc1b0d38a2fb91c27cd985f5790de8a7ab4f1"],
    ["figure.png", "cf4680d3249829fd193af1f94d93c0cc750bc41b29bfdf944180785f7ff3f5d0"],
    ["SHA256SUMS", "23c0646faf34bfd545db7326bfe7828fc1377875f0238c99f028ae85041b981a"],
    ["manifest.json", "b52c3558755ca35135cc7665c83d66ca7da544411a7049a8c2d8a8c41c9fb35d"],
    ["validation.json", "b9e704a67eb7421ca2093791a40fdd1645f8fdbb890573af5260578ebcbe0dc5"],
  ]);
  for (const [name, digest] of expected)
    assert.equal(sha256(await read(`${base}/${name}`)), digest, name);
});
