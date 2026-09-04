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
  "research/r076a_complete_clock_localized_current_sign_obstruction.md": "d23532f84702be1630daa0b8d56d02242571dd8a1f8024c59a7f71bec30f26eb",
  "research/r076a_complete_clock_localized_current_sign_obstruction_primary_audit.md": "0f7f56d32025f4cd86218f54dfcf5155675f316d2afecdd0007b13ad70240a8d",
  "research/r076a_report-source.md": "0bbf94774c7d76e623c025a731e0238eca39080c4720a039f080afb038ecad8b",
  "scripts/r076a_complete_clock_localized_current_sign_obstruction_fixtures.json": "f3644b2a7a641bc92c6c1936f1c05cbed88a6a3e94e25d650c7258ce07b30a31",
  "scripts/r076a_complete_clock_localized_current_sign_obstruction_expected.json": "32d0f99d07d842bf6c9161698249c186c4d23d2f1f33e7f8bd7fc18804887697",
  "scripts/r076a_complete_clock_localized_current_sign_obstruction_certificate.py": "7dfff7dfb26ccfb9399c0a9cc32a914d5e1d94f3a81ed172f4ec245343d43ab5",
  "scripts/r076a_complete_clock_localized_current_sign_obstruction_certificate_independent.rb": "5633861e614cba477f59e8ca4d6f52bc9c29e561178ae07117af53d83cc13366",
  "scripts/r076a_complete_clock_localized_current_sign_obstruction_qa.sh": "d34a0275f6b321c84db14fd47219701ef5a3caa53572b941f37343c88d680539",
  "research/r076a_complete_clock_localized_current_sign_obstruction_certificate.json": "cd09488885f0e31d95f94c7f46bf0c80b1ad476a438a3fa081d3ec83d4c2949c",
  "research/r076a_complete_clock_localized_current_sign_obstruction_certificate_report.md": "665e69226763e2df99615714829387309a3f66a1ec1e35b19f4af35d005c0d12",
  "research/r076a_complete_clock_localized_current_sign_obstruction_independent_audit.md": "cd5608262b4f9c35f30afec9af2a108621f4f89cf8f4a69d973e1e07b6ee670d",
  "research/r076a_complete_clock_localized_current_sign_obstruction_qa_report.md": "fb8681c63bfa83bc26fadeb867c0c25c6167b28789bda9480e061dcdf0409a82",
};

test("R0.76A frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r076a_complete_clock_localized_current_sign_obstruction_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions.length, 15);
  assert.ok(certificate.assertions.every((row) => row.pass === true));
  assert.equal(certificate.negativeMutations.length, 86);
  assert.equal(certificate.computed.cluster.threshold, 16);
  assert.equal(certificate.computed.cluster.carrier, 176);
  assert.equal(certificate.computed.cluster.alpha, 16);
  assert.equal(certificate.computed.cluster.beta, "1/11");
  assert.equal(certificate.computed.cluster.gapConditionFails, true);
  assert.equal(certificate.computed.bounds.strictNegative, true);
  assert.equal(certificate.computed.point.J, "-1/11");
  assert.equal(certificate.computed.point.correctionDensity, "-351/121");
  assert.equal(certificate.computed.auxiliary.fullGradient, "30625/121");
  assert.match(read("research/r076a_complete_clock_localized_current_sign_obstruction_primary_audit.md"), /Current verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r076a_complete_clock_localized_current_sign_obstruction_independent_audit.md"), /Assertions: 15\/15/);
  assert.match(read("research/r076a_complete_clock_localized_current_sign_obstruction_qa_report.md"), /86\/86 Python; 86\/86 Ruby/);
});

test("R0.76A primitive, complete-clock strict signs, and narrow no-go are materialized", () => {
  const source = read("research/r076a_complete_clock_localized_current_sign_obstruction.md");
  const compact = source.split(/\s+/).join(" ");
  const tags = [...source.matchAll(/\\tag\{A\.(\d+)\}/g)].map((match) => Number(match[1]));
  assert.deepEqual(tags, Array.from({ length: 34 }, (_, index) => index + 1));
  assert.equal((source.match(/\\\[/g) ?? []).length, 34);
  for (const marker of [
    "0<\\delta_0<\\delta", "actual unresolved high-carrier cluster", "complete clock",
    "\\tag{A.8}", "\\tag{A.9}", "\\tag{A.10}", "\\tag{A.17}", "\\tag{A.31}", "\\tag{A.34}",
    "strict sign obstruction but not a large-error obstruction", "not a counterexample to the two-mode collar-flux estimate",
    "positive carrier-density term", "quantitative localized current estimate", "Version-M extraction", "**NOT CLAY.**",
  ]) assert.ok(compact.includes(marker), marker);
});

test("R0.76A reader is complete, figure-free, and preserves the W milestone recap", () => {
  const note = read("public/notes/r0-76a.html");
  for (const marker of [
    "R0.76A · STEP 52", "0 &lt; DELTA_0 &lt; DELTA", "ACTUAL COLLAR PRIMITIVE", "COMPLETE CLOCK",
    "Q=2 UNRESOLVED CLUSTER", "LOCAL CURRENT STRICTLY NEGATIVE", "CORRECTION ROW STRICTLY NEGATIVE",
    "CARRIER DENSITY RETAINED", "SIGN-DROPPING CLOSED", "W TWO-MODE PAYMENT INTACT", "VERSION-M CONDITIONAL",
    "A.1", "A.34", "15/15", "86/86", "12/12",
    "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  for (let section = 409; section <= 415; section += 1) assert.ok(note.includes(`<section id="s-${section}">`), `s-${section}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 500_000);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(existsSync(resolve(root, "public/assets/r076a")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76A local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r076a-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 45/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r076a_complete_clock_localized_current_sign_obstruction_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":86/);
});
