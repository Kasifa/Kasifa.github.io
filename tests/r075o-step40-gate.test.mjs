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
  "research/r075o_vertical_diffusion_packet_gain.md": "3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9",
  "research/r075o_vertical_diffusion_packet_gain_primary_audit.md": "27f9341f93bd2b031dbd3fd0e8d745788d5ff36a085ddb8be4ef8e1c5553e69b",
  "research/r075o_report-source.md": "9d2c234b0ba2a33b0f573a7933c26bcc751db6fe85919f2e146a0e6a18128c2b",
  "scripts/r075o_vertical_diffusion_packet_gain_fixtures.json": "46dff6097c3a052dc968f1c712c3421105ea5be51d3c905c492cc463cc04f0ad",
  "scripts/r075o_vertical_diffusion_packet_gain_expected.json": "228ac56e500a32b1f7c64c04d4110c78c4105c4d2a997fa8b108bd7449d59833",
  "research/r075o_vertical_diffusion_packet_gain_certificate.json": "71a737b18d67cd01d494abfd0485b42fd78fce9a8bc2085931e17e2aa4be8055",
  "research/r075o_vertical_diffusion_packet_gain_certificate_report.md": "32267743fcfea2a88c5b971912db9f18dd76725b39bba5bf674bd920a8573379",
  "research/r075o_vertical_diffusion_packet_gain_independent_audit.md": "51fc9e834dbdc525b2c75c9430a87d1e8504666f7a65b0ac9e86a22baeb7dac7",
  "research/r075o_vertical_diffusion_packet_gain_qa_report.md": "69a48e0ced0ce74d8d68a94bc6df0bfb35416c35257870f9db73e39e718ec8ad",
  "scripts/r075o_vertical_diffusion_packet_gain_certificate.py": "a92864e15193139d2bfe4dd352c8a398bbe2dc2942fa0e3c2820331cb45f6e05",
  "scripts/r075o_vertical_diffusion_packet_gain_certificate_independent.rb": "33d0c8d15b34e8638160548b287f4db3acbae734b4523f09a700d0c66650f917",
  "scripts/r075o_vertical_diffusion_packet_gain_qa.sh": "084cf638304a98360aecbcefb1d074f8d67aef00c1fb2c49bfd3602db4b8496e",
};

test("R0.75O frozen ledger is byte-exact and certificates pass", () => {
  assert.equal(Object.keys(frozen).length, 12);
  for (const [relative, expected] of Object.entries(frozen)) assert.equal(sha(relative), expected, relative);
  const certificate = JSON.parse(read("research/r075o_vertical_diffusion_packet_gain_certificate.json"));
  assert.equal(certificate.verdict, "PASS");
  assert.equal(certificate.assertions.total, 19);
  assert.equal(certificate.assertions.passed, 19);
  assert.equal(Object.keys(certificate.checks).length, 19);
  assert.match(read("research/r075o_vertical_diffusion_packet_gain_primary_audit.md"), /Verdict: \*\*PASS\*\*[\s\S]*Mathematical blocker count: \*\*0\*\*[\s\S]*Release blocker count: \*\*0\*\*/);
  assert.match(read("research/r075o_vertical_diffusion_packet_gain_qa_report.md"), /132\/132 Python; 132\/132 Ruby/);
});

test("R0.75O theorem boundary, equation ledger, and vertical-diffusion rows are materialized", () => {
  const source = read("research/r075o_vertical_diffusion_packet_gain.md");
  for (let index = 1; index <= 24; index += 1) assert.ok(source.includes(`\\tag{O.${index}}`), `O.${index}`);
  for (const marker of [
    "vertical heat semigroup is an `L^2`", "No upper vertical-frequency bound was used", "\\Gamma_K",
    "e^{-3/2}", "98605}{71442", "strict inequality is required", "4279}{238140000",
    "not yet the Version-M payment", "inter-packet", "novelty or priority", "NOT\\ CLAY",
  ]) assert.ok(source.includes(marker), marker);
});

test("R0.75O public reader is complete and forbidden future output is absent", () => {
  const note = read("public/notes/r0-75o.html");
  for (const marker of [
    "R0.75O · STEP 40", "CONSTANT SHEAR", "VERTICAL DIFFUSION", "ARBITRARY VERTICAL FREQUENCIES",
    "DIAGONAL REMOVED FIRST", "SCHUR 1/4", "TOTAL-FREQUENCY CAP", "K^-2/3 GAIN",
    "O.1", "O.24", "132/132", "12/12", "NO NOVELTY CLAIM", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 400_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75o.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/assets/r075o")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75p.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75p.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075p")), false);
});

test("R0.75O local translation and certificate QA remain deterministic", () => {
  const translationOutput = execFileSync(node, ["scripts/add-r075o-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translationOutput, /"checked": 47/);
  assert.match(translationOutput, /"dgxUsed": false/);
  const qaOutput = execFileSync("bash", ["scripts/r075o_vertical_diffusion_packet_gain_qa.sh"], { cwd: root, encoding: "utf8" });
  assert.match(qaOutput, /"status":"PASS"/);
  assert.match(qaOutput, /"mutations":132/);
});
