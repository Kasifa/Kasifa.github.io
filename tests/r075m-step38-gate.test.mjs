import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const node = process.execPath;
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

const frozen = {
  "research/r075m_dyadic_packet_diffusive_flux_gain.md": "13434bbc15eabecd5a695eceef01a7d63415e96511b14c29cc8abcd1297c7bf7",
  "research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md": "2b5ee050c09e3be925143c12c29082c3fe562a83b9a2d2669511a2bb1684d7dc",
  "research/r075m_report-source.md": "f8ed7af8ef5051b0efa73177d0530562917d55dfa6476b00b8f871db0da99d67",
  "scripts/r075m_dyadic_packet_diffusive_flux_gain_fixtures.json": "b93d727b4bf0729af2064e51fbc0c1450d98806c9b92fe11727b4d5423fa157f",
  "scripts/r075m_dyadic_packet_diffusive_flux_gain_expected.json": "cef1705998bc935448f371d6f389d46059b59e99bf230bd75dad0489fb85a4f4",
  "research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json": "1794cee5294ed55a41697f74d6a4b0bbb5e31e59b3a74ed11f277d0ae8e17423",
  "research/r075m_dyadic_packet_diffusive_flux_gain_certificate_report.md": "cd2882d59ec90471d1e74cb135426490c46863fbf6e6df3db3532926aaa5002f",
  "research/r075m_dyadic_packet_diffusive_flux_gain_independent_audit.md": "507fdbb899f0e74abccc0477405949ca07f9379d4b20ce20ab3bd87e63a76881",
  "research/r075m_dyadic_packet_diffusive_flux_gain_qa_report.md": "b7513c9ee3660a21473f7ea87a19d4ae0f70aa6a99ceb88b397d159e7a56bad0",
  "scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate.py": "8a55852a3eabcf8989feadcb25cb178db57b1dccbd2249e73d48e61e7755811b",
  "scripts/r075m_dyadic_packet_diffusive_flux_gain_certificate_independent.rb": "6436063bc4ec623dfc27d7fc3edee8ee6751784f8a43ecdd5aa1b4170b35dd1b",
  "scripts/r075m_dyadic_packet_diffusive_flux_gain_qa.sh": "9e61cb0e57f4116e371beda1d6709ca479ea146538758287d6451b2641e87cf2",
};

test("R0.75M frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075m_dyadic_packet_diffusive_flux_gain_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions.total, 19);
  assert.equal(certificate.assertions.passed, 19);
  assert.equal(Object.keys(certificate.checks).length, 19);
  assert.match(read("research/r075m_dyadic_packet_diffusive_flux_gain_primary_audit.md"), /Verdict: PASS\. Mathematical blocker count: 0\. Release blocker count: 0\./);
  assert.match(read("research/r075m_dyadic_packet_diffusive_flux_gain_qa_report.md"), /130\/130 Python; 130\/130 Ruby/);
});

test("R0.75M theorem boundary, equation ledger, and no-mode-count result are materialized", () => {
  const source = read("research/r075m_dyadic_packet_diffusive_flux_gain.md");
  for (let index = 1; index <= 20; index += 1) assert.ok(source.includes(`\\tag{M.${index}}`), `M.${index}`);
  for (const marker of [
    "Schur's test", "No pair count appears", "does not appear", "W_xi", "K^{-2/3}M_K^{2/3}",
    "27163}{71442", "inter-packet summation", "full-torus", "No novelty", "priority", "NOT\\ CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75M public reader is complete and forbidden future output is absent", () => {
  const note = read("public/notes/r0-75m.html");
  for (const marker of [
    "R0.75M · STEP 38", "FINITE REAL DYADIC PACKET", "DIAGONAL CANCELED", "SCHUR TEST",
    "NO MODE-COUNT LOSS", "ENERGY K^-2", "GAIN K^-2/3", "WIENER ROW W_XI", "ONE PACKET ONLY",
    "M.1", "M.20", "130/130", "12/12", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 400_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75m.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/notes/r0-75n.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75n.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075m")), false);
});

test("R0.75M local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075m-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 47/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075m_dyadic_packet_diffusive_flux_gain_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":130/);
});
