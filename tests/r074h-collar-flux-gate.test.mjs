import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";
import { promisify } from "node:util";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const execFileAsync = promisify(execFile);

const frozen = new Map([
  ["research/r074h_collar_flux_two_regime_closure.md", "8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1"],
  ["research/r074h_energy_identity_independent_audit.md", "a63377c01ddaf8aaa07f99befc05696abff86e69854ca9d8ac76c748afd4d104"],
  ["research/r074h_packet_flux_independent_audit.md", "9330181d9288ca50ab806f31d96ca76223d3248026561950f4e21535f0374649"],
  ["research/r074h_scaling_and_claim_audit.md", "a6dd7f5e1efae508ed332acfb7b3af3170668a9b12e95a1eec167ee90cad3be2"],
  ["research/r074h_full_note_adversarial_audit.md", "e42e2a6a64b689c4477a7814d58cfd273e25a881724a76afbb2c6bcf139dab32"],
  ["research/r074h_final_source_rebind_audit.md", "f0aef5522c7201250f625418275e57512f85309f50ec1e24e1ccb9b6ef93f1d7"],
  ["scripts/r074h_collar_flux_certificate.py", "acce024b8dd78ba727e3ec8176a308dc53ecc34b7bdaf57b6c48e5d1e1a5c6e4"],
  ["research/r074h_collar_flux_certificate.json", "783591f3da880ec9182be89c585eb732e35d5842b7d196dc2ae4e35b6c0d2ba4"],
  ["research/r074h_collar_flux_certificate_report.md", "c675d4efea3edfdd3e77844b54ae34a7721902a5f03d6ace72e3dc09ce85bc27"],
  ["scripts/r074h_collar_flux_certificate_independent.rb", "9004240b7a041001fb853eb9963ed10cc768f2e2a3c4b675d1187167c051a39f"],
  ["research/r074h_certificate_independent_audit.md", "3760692601b27e40fcd219aabe9ed612c10e8e1063100b58b6208055ba969545"],
  ["research/r074h_report-source.md", "d72917b04e067113f419f89bc009861f264d859e80cb22dce1276c6dbfbc2c47"],
  ["research/r074h_primary_literature_boundary.md", "722e338f4cdd729f3a8756b886c920f17d08e08592bbce6ed9561179d6afbadf"],
  ["research/r074h_primary_literature_independent_audit.md", "f5c0572c16f26e5066edbf07db8347d591815fe461ffeb81b8c95e2a4ac39f81"],
  ["research/r074h_gap_matrix.md", "3cc23977e865596eb679cceef6260ce7909204da785168efd42663fef9841251"],
  ["research/r074h_freeze_manifest.json", "94911632e1763e308c58a3f01cd90b532e2087be9b5c24264bed90fb53d019d7"],
]);

test("R0.74H frozen mathematical assets remain byte-exact", async () => {
  for (const [path, expected] of frozen)
    assert.equal(sha256(await read(path)), expected, path);
});

test("R0.74H exact certificate reproduces the frozen JSON", async () => {
  const python = process.env.PYTHON || "python3";
  const { stdout } = await execFileAsync(python, ["scripts/r074h_collar_flux_certificate.py"], {
    cwd: root,
    maxBuffer: 10 * 1024 * 1024,
  });
  assert.deepEqual(Buffer.from(stdout), await read("research/r074h_collar_flux_certificate.json"));
});

test("R0.74H independent exact reconstruction matches all rows", async () => {
  const { stdout } = await execFileAsync("/usr/bin/ruby", ["scripts/r074h_collar_flux_certificate_independent.rb"], {
    cwd: root,
    maxBuffer: 10 * 1024 * 1024,
  });
  const result = JSON.parse(stdout);
  assert.equal(result.result, "PASS");
  assert.equal(result.field_comparisons, 150);
  assert.equal(result.mismatch_count, 0);
  assert.deepEqual(result.independent_summary, { passed: 25, total: 25 });
});

test("R0.74H frozen primary figure masters remain byte-exact", async () => {
  const base = "research/figures/r074h/fig-r074h-collar-flux-repair";
  const expected = new Map([
    ["figure.svg", "9989d22ac20c619f0f5da285108676318584e53b194fd13abe4a9456c97b09c3"],
    ["figure.pdf", "80441f23ea0a056fdc7a22ee39bc3a452ce39ff11725867b4304b025791d55a0"],
    ["figure.png", "876b88609a12dcda7a88fbffd1f97fcbaf2749251060fbe148ac2b221e8b6c9a"],
  ]);
  for (const [name, digest] of expected)
    assert.equal(sha256(await read(`${base}/${name}`)), digest, name);
});
