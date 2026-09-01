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
  ["research/r074g_complete_payment_counterexample.md", "95548d6225389b9cfd1822a8abaf89e495e7f15ca5ff30c6b92aaa8ac5f2d6be"],
  ["research/r074g_energy_pressure_independent_audit.md", "305d73a8d45b7292baa7f3535b9347d3822f366087a6600e936915ad20cd1d0e"],
  ["research/r074g_occupation_independent_audit.md", "aa958b3ab703e0078b4e3e1e9d028b7304889d6038be58dd3c4333f2ae6843ab"],
  ["research/r074g_complete_ledger_adversarial_audit.md", "60fff91179a49f2f71a4a68aa5d0e77304b58c6310791e2293ad50d9a95f2cb6"],
  ["scripts/r074g_complete_payment_certificate.py", "315f4cc7f0a397287cc2eb14ec1ad65bcacb797692e2a6ce5a1459985a4853ca"],
  ["research/r074g_complete_payment_certificate.json", "2a411007989e63e51ab7f1644724f654f26794b80507681aaf62e00adbeefd53"],
  ["research/r074g_complete_payment_certificate_report.md", "aee995c26795c460fa76cd004f227f56a102ca2daf1040b428c313d48f3ab3bc"],
  ["research/r074g_certificate_independent_audit.md", "598a92ef5c3cb061142ede1bb1c5dff0680848c386c0847f45d97f246b93fade"],
  ["research/r074g_gap_matrix.md", "e9001e32b993ac565eaf9d3efc70cbec55e4045cc03d3e9c1e736653bea97bf3"],
  ["research/r074g_freeze_manifest.json", "9e6df815df139212ddaa6c54e473bb7fd6e516264287784e20ee96010afe2abe"],
]);

test("R0.74G frozen mathematical assets remain byte-exact", async () => {
  for (const [path, expected] of frozen) {
    assert.equal(sha256(await read(path)), expected, path);
  }
});

test("R0.74G exact certificate reproduces the frozen JSON", async () => {
  const python = process.env.PYTHON || "python3";
  const { stdout } = await execFileAsync(
    python,
    ["scripts/r074g_complete_payment_certificate.py"],
    { cwd: root, maxBuffer: 10 * 1024 * 1024 },
  );
  assert.deepEqual(Buffer.from(stdout), await read("research/r074g_complete_payment_certificate.json"));
});

test("R0.74G frozen primary figure masters remain byte-exact", async () => {
  const base = "research/figures/r074g/fig-r074g-complete-payment-ledger";
  const expected = new Map([
    ["figure.svg", "254aa5c7482d3665ab0873690bd2a3a14dfa0a0555beb3182b001636b8518785"],
    ["figure.pdf", "62fdeeca29227ce508631386d8406815440fd8d06ee9110cb3fb2b707f0f8134"],
    ["figure.png", "57e83342f003217eaa915a7a68122c6015aef3da5d8a8d7f3e6322667306ba7d"],
  ]);
  for (const [name, digest] of expected) {
    assert.equal(sha256(await read(`${base}/${name}`)), digest, name);
  }
});
