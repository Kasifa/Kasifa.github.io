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
  ["research/r074j_problem_freeze.md", "383e4e8e9a983e4b74050e657bd11fa234ad8dfe2c6fa3c0ec1a8800781291e0"],
  ["research/r074j_matching_payment_law.md", "d495ff3d069eceea9dd7bbf1c467f8836cb72033cde7a9d9c17e9b585478dbad"],
  ["research/r074j_heat_platform_independent_audit.md", "45214485a46271174db047c6fb6565c276d712f15c6009e15221626a0d0e9f23"],
  ["research/r074j_complete_payment_ledger_independent_audit.md", "78e18dc6daa3291bb2f7fcf2bd58d56db504560a19ae6b38e2c7b303c89b599c"],
  ["research/r074j_final_source_rebind_audit.md", "c86b1edea231663df26121a4da45d76435e6e3d3e5191022031f0559a91fa050"],
  ["research/r074j_freeze_manifest.json", "608773b688371742dffedd30938bf35fb4cfda46c72d87d9b6168d629ebe0952"],
  ["research/r074j_gap_matrix.md", "4e83680b8da9c6d651de1647b9975e2ff32c26ee291a151467b2958e873b9e89"],
  ["research/r074j_report-source.md", "e36e2529f77f81e8a6617652d641e016ece175075862500412e529907d3d4f9f"],
  ["research/r074j_primary_literature_boundary.md", "a4a60575122efde993252a9cafda2a85ea15da7f67aa34d1583dc95552f45c60"],
  ["research/r074j_primary_literature_independent_audit.md", "e72aaafb4eca9c28d0834e514866522c60155bfc3220c39857fd452a01046ae2"],
  ["research/r074j_bilingual_dictionary.md", "3ea788eeb84cd82ae24dd6c9584223b8caef5d927eea8b3a0aef348c81991a8b"],
  ["scripts/r074j_matching_payment_certificate.py", "6dcc03d283612306dc39669f5b6c8b3cf8569e40205e067c4db0c2b6929879ec"],
  ["research/r074j_matching_payment_certificate.json", "493c9cf6bc1357b36da1b0a13becbc51e62ea26aab95b6af7eaeb085b65be5d5"],
  ["research/r074j_matching_payment_certificate_report.md", "6a32098c808373a7d3cfbd30b266f20d0aa33abc2b693e51b48b0c486852fa07"],
  ["scripts/r074j_matching_payment_certificate_independent.rb", "ca3da7fafea86012c58c20801e680c9bb5ed26c712c92d32cc080426f9916197"],
  ["research/r074j_certificate_independent_audit.md", "74a68cf221efd1c30e3461012b2196d7fc38621f36c9648e24fcc4814ee755e2"],
]);

test("R0.74J frozen mathematical assets remain byte-exact", async () => {
  for (const [path, expected] of frozen)
    assert.equal(sha256(await read(path)), expected, path);
});

test("R0.74J exact certificate reproduces frozen JSON", async () => {
  const python = process.env.PYTHON || "python3";
  const { stdout } = await execFileAsync(python, ["scripts/r074j_matching_payment_certificate.py"], {
    cwd: root, maxBuffer: 10 * 1024 * 1024,
  });
  assert.deepEqual(Buffer.from(stdout), await read("research/r074j_matching_payment_certificate.json"));
});

test("R0.74J independent exact reconstruction matches every row", async () => {
  const { stdout } = await execFileAsync("/usr/bin/ruby", ["scripts/r074j_matching_payment_certificate_independent.rb"], {
    cwd: root, maxBuffer: 10 * 1024 * 1024,
  });
  assert.match(stdout, /independentPassed=38/);
  assert.match(stdout, /independentTotal=38/);
  assert.match(stdout, /leafFieldComparisons=287/);
  assert.match(stdout, /mismatchCount=0/);
  assert.match(stdout, /result=PASS/);
});

test("R0.74J frozen primary figure package remains byte-exact", async () => {
  const base = "research/figures/r074j/fig-r074j-fifth-shell-payment";
  assert.equal((await readdir(resolve(root, base))).length, 24);
  const expected = new Map([
    ["figure.svg", "ed42960e32e7b2e4707bab933bd3ff400e2f0722ba77f7fc53f0dcaeff3d736b"],
    ["figure.pdf", "3cabf4a587ae6a7fbf145039740489d1f2ba79e9903ed560779d02e56ecab6f1"],
    ["figure.png", "5aef3c61cb0b557411599d0a1ff7dd92e8c89f750f4d7abcfbd3a1d7aaa689b2"],
    ["SHA256SUMS", "ea4da4d2eefcf57758c479a9cebd99cc14091ad7b42fd45f180bbb54596db366"],
    ["manifest.json", "0688dab352ac78c907b712698edd4645a4e1a6eeffb6fab5cb597dfdf05cb6cc"],
    ["validation.json", "84eb7a87482a9633aaa9d506a3b6133162cb4510f694a3705a390d1f2f1dcd81"],
  ]);
  for (const [name, digest] of expected)
    assert.equal(sha256(await read(`${base}/${name}`)), digest, name);
});
