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
  "research/r075z_unresolved_cluster_carrier_current_gate.md": "30d2811e8747aa2b40b4787e6f169af19d1381b66fc84610327da221168f3d97",
  "research/r075z_unresolved_cluster_carrier_current_gate_primary_audit.md": "895d09e0b403c0a6bcf216624527dd6c2bf76f15d7ce5f6b6b0a31b6f64a1eb0",
  "research/r075z_report-source.md": "9b071b3e020210922834435ea7e5806620479d400eb044f48f34e7b02c259d4c",
  "scripts/r075z_unresolved_cluster_carrier_current_gate_fixtures.json": "9bd703f41f4b4823a4b6fe38136bf2a5bef126cf15edb3b54036cf1b80e4f4b0",
  "scripts/r075z_unresolved_cluster_carrier_current_gate_expected.json": "6043f94b70b6068a58d7716877a5319edc9edfc90b47bfee23ea7baee0ad58d4",
  "scripts/r075z_unresolved_cluster_carrier_current_gate_certificate.py": "dce8afaee87120d042a046d220aeca5f345cb38d42e306d70f89a8fb211252a1",
  "scripts/r075z_unresolved_cluster_carrier_current_gate_certificate_independent.rb": "d4d1cc3445694b6eaac4857d812f9272e9a8214efce11e212d0d03f049d86578",
  "scripts/r075z_unresolved_cluster_carrier_current_gate_qa.sh": "6c5f50401ee0e77253f7b6df8b9e5802fac70e756b497457201d602645e5a1da",
  "research/r075z_unresolved_cluster_carrier_current_gate_certificate.json": "116b2f4a6bf343f602c3c624b1eac550449162aa43d7e4038e886ba2bbf7b839",
  "research/r075z_unresolved_cluster_carrier_current_gate_certificate_report.md": "861d4585b9969bc10d779552ccd0318e71a92700aa7c0c017e8d2e8fbfbd9163",
  "research/r075z_unresolved_cluster_carrier_current_gate_independent_audit.md": "9bffb2446e7d2fd5d85628f15079265e0e94252a61c430c59642a016dda6574c",
  "research/r075z_unresolved_cluster_carrier_current_gate_qa_report.md": "0e9e4286ac132a88f47675869ceb55c5c491ceb6c9a16bd6d6511b3bf9ba1f12",
};

test("R0.75Z frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075z_unresolved_cluster_carrier_current_gate_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions.length, 15);
  assert.ok(certificate.assertions.every((row) => row.pass === true));
  assert.equal(certificate.negativeMutations.length, 72);
  assert.equal(certificate.computed.threshold, 16);
  assert.equal(certificate.computed.partition.x.sector, "X");
  assert.equal(certificate.computed.partition.yEquality.sector, "Y");
  assert.equal(certificate.computed.partition.zCluster.sector, "Z");
  assert.equal(certificate.computed.clusterLedger.carrier, 16);
  assert.deepEqual(certificate.computed.clusterLedger.offsets, [0, 1]);
  assert.equal(certificate.computed.pointLedger.J, -1);
  assert.equal(certificate.computed.pointLedger.weightedCurrent, 32);
  assert.equal(certificate.computed.pointLedger.unweightedAbsorber, 2);
  assert.match(read("research/r075z_unresolved_cluster_carrier_current_gate_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075z_unresolved_cluster_carrier_current_gate_independent_audit.md"), /Assertions: 15\/15/);
  assert.match(read("research/r075z_unresolved_cluster_carrier_current_gate_qa_report.md"), /72\/72 Python; 72\/72 Ruby/);
});

test("R0.75Z exact partition, cluster identities, and narrow no-go are materialized", () => {
  const source = read("research/r075z_unresolved_cluster_carrier_current_gate.md");
  const compact = source.split(/\s+/).join(" ");
  const tags = [...source.matchAll(/\\tag\{Z\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 31 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 31);
  for (const marker of [
    "n_1\\ell<8q", "n_1\\ell\\ge8q", "Cut the ordered frequencies at every adjacent gap at least `8q/ell`",
    "\\tag{Z.3}", "\\tag{Z.6}", "\\tag{Z.7}", "\\tag{Z.18}", "\\tag{Z.20}", "\\tag{Z.26}", "\\tag{Z.31}",
    "Z^{(N)}(y)=2-e^{iy}", "not a counterexample to the desired cluster flux estimate",
    "No full Z-sector flux payment is claimed here", "cross-cluster products", "Version-M boundary", "**NOT CLAY.**",
  ]) assert.ok(compact.includes(marker), marker);
});

test("R0.75Z reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-75z.html");
  for (const marker of [
    "R0.75Z · STEP 51", "EXHAUSTIVE X/Y/Z PARTITION", "MAXIMAL CLUSTERS", "EXACT ENVELOPE PDE",
    "DENSITY / CARRIER BLOCKS", "LOCAL CURRENT", "GLOBAL SIGN ONLY", "POINTWISE ABSORPTION NO-GO",
    "NAIVE X RECURSION CLOSED", "FULL CLUSTER PAYMENT OPEN", "CROSS-CLUSTER OPEN", "VERSION-M CONDITIONAL",
    "NO COUNTEREXAMPLE CLAIM", "Z.1", "Z.31", "15/15", "72/72", "12/12",
    "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 401; section <= 408; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 500_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r075z")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
  assert.equal(existsSync(resolve(root, "public/notes/r0-76a.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-76a.pdf")), false);
});

test("R0.75Z local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075z-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 48/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075z_unresolved_cluster_carrier_current_gate_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":72/);
});
