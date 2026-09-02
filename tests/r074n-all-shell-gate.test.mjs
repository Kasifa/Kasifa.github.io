import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import {
  cp,
  mkdir,
  mkdtemp,
  readFile,
  readdir,
  rm,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import test from "node:test";
import { promisify } from "node:util";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const execFileAsync = promisify(execFile);

const proofHash = "ca1ddabb6ea931b2f1a96b5cb000e955492c6852b0ea3b2aaa6148c6f3fa9e1e";
const certificateHash = "53481cf393308a786c3a414da6238faaa9b8a15dac0017638c47584615bbecc2";

const frozen = new Map([
  ["research/r074n_problem_freeze.md", "4b2df724cf81cf28d0c9b89636ae166ade11746f623ca2a3466f08e4e1adfacc"],
  ["research/r074n_all_shell_synthesis.md", proofHash],
  ["research/r074n_all_shell_independent_audit.md", "5173ac954ca82e2abc0371258527ddd8b6bc372e43de6c3a2aeea2a9f2b187e9"],
  ["research/r074n_crossnote_implication_independent_audit.md", "7c289055939cdbf21780337e7da2a1d91109172d89a6c168258703124b50be8a"],
  ["research/r074n_final_source_rebind_audit.md", "ea51805047a8dbb3e914f4f29c8f93fd117ff1a22d8320f832af1cab7002042c"],
  ["research/r074n_gap_matrix.md", "986a2ddc20318f6f70a968f80fd972c671e7ae43fe769e2acd00d4230d08fb06"],
  ["research/r074n_primary_literature_boundary.md", "485883f09b417a51326acc1cf94e37d86cb62cf4ff22bfaba2ef9f0f9d555054"],
  ["research/r074n_primary_literature_independent_audit.md", "4ebdfc06dfd548285686f869dd70b792edafd792e95aedabc5d8992a8a94daa1"],
  ["research/r074n_report-source.md", "b3a50fe4aaf9ca1b98d92fa4df3ab3ff3a461163fc9d857c0219cea3a29272c1"],
  ["research/r074n_bilingual_dictionary.md", "d1418d676333293fab29c11d21da053e60f61241068d4b8aaf2565636c270755"],
  ["research/r074n_reader_source_independent_audit.md", "ab63f12d729d60012e68205015dc4e6a6a93896d0b484bbb60c7e6dbaedbd00e"],
  ["research/r074n_all_shell_certificate.json", certificateHash],
  ["research/r074n_all_shell_certificate_report.md", "3c10f8925fb8e89e891774310ec118652ac59997ca9bdf2c002f4bbdbdcaeb99"],
  ["research/r074n_certificate_independent_audit.md", "53a8d9c71955070c56587c2370cc5a45388084c1dcd16bac366f34e4e73e20d2"],
  ["research/r074n_certificate_adversarial_audit.md", "0c251b5ba3f30fae668aaa9ca1504ee4f713feb26e60aeb674a02f9b77064448"],
  ["research/r074n_figure_independent_audit.md", "b0fc5ee9ca8220acde7c3727633d7d0046c33af72ca146f70109dcdb27b7eb1c"],
  ["scripts/r074n_all_shell_certificate.py", "1174dfba5484fa53f4022ed5725bbd511cf4596f5b133997262844c439857e8c"],
  ["scripts/r074n_all_shell_certificate_independent.rb", "32621a28ca2312fcddea83135309ecd7cd3cc3d2515f929b401d04b9d221f744"],
  ["research/r074n_freeze_manifest.json", "9c6529d19833ce4bf1c2346fca58d91a7def949acee76384b3a97733cf943e0a"],
]);

const figureBase = "research/figures/r074n/fig-r074n-all-shell-synthesis";
const figureFrozen = new Map([
  ["figure.svg", "830c091a6b55abf8c4e1a737e595d0ada9a7a088d4b77b9a0678c22ee35590f8"],
  ["figure.pdf", "cbc1de4ea76e201d921fab1b4cbb50913838106c2814cc9a460ce390cc4c3878"],
  ["figure.png", "809a0c89e94494d562c35baecb993f8674b1539436710775484374216909bad4"],
  ["qa-svg-quicklook.png", "c2884eba9c14fd22aac88b330b410a939ff72b94acae8fc5d4edc342263226b6"],
  ["source-data.csv", "6b38ff70fc036922058fa4336413b84a15114b3da9ae96c9af2fb5fb95b056bb"],
  ["plot.py", "bdaa25661e182f33f841dbce4b2a6cdb8bc0d5b6c9d109ac36d41bab00ad9749"],
  ["validate.py", "772b3066dd38dadbebfc1bd4c5922918e6fde96bdb5d297a47ad7580d64b0f27"],
  ["validation.json", "f28e2c40eb58a8f284a8e1b681c3bf0561c6aa26cc805076bd438d9cc58d1bad"],
  ["manifest.json", "fc5d6f5a9fe861068ffc4014f42d7eecd7261dbd41fd4d6b0f7f29c55458cea9"],
  ["SHA256SUMS", "4cd2b72d53f8ebcf02b403c3f5497ac159a85d49bfe87b9f944be1a95605fa3f"],
]);

test("R0.74N mathematical, reader, and audit assets remain byte-exact", async () => {
  for (const [path, expected] of frozen)
    assert.equal(sha256(await read(path)), expected, path);

  const proof = await text("research/r074n_all_shell_synthesis.md");
  const tags = proof.match(/\\tag\{[^}]+\}/g) ?? [];
  assert.equal(tags.length, 61);
  assert.equal(new Set(tags).size, 61);

  for (const path of [
    "research/r074n_all_shell_independent_audit.md",
    "research/r074n_crossnote_implication_independent_audit.md",
    "research/r074n_final_source_rebind_audit.md",
    figureBase + "/manifest.json",
  ]) assert.ok((await text(path)).includes(proofHash), path);

  const rebind = await text("research/r074n_final_source_rebind_audit.md");
  assert.ok(rebind.includes("53/55 pre-existing displays are verbatim unchanged"));
  assert.ok(rebind.includes("61/61 UNIQUE TAGS"));

  const crossNote = await text("research/r074n_crossnote_implication_independent_audit.md");
  assert.ok(crossNote.includes("R0.74N CROSS-NOTE IMPLICATION: PASS"));
  assert.ok(crossNote.includes("The argument proves no lower bound"));

  const freeze = JSON.parse(await text("research/r074n_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.74N");
  assert.equal(freeze.origin_main_baseline, "99ffbad667904a98735f04de18608a417097be26");
  assert.equal(
    freeze.claim_status.complete_signed_all_shell_condition,
    "PROVED_AT_C_GAMMA_J_L_J_R_J_POWER_5_AND_INDEPENDENTLY_AUDITED",
  );
  assert.equal(
    freeze.claim_status.matching_weighted_kinetic_dissipation_law,
    "PROVED_FAMILYWISE_BY_NONCIRCULAR_CROSS_NOTE_SYNTHESIS",
  );
  assert.equal(
    freeze.claim_status.exterior_dissipation_component,
    "PROVED_UPPER_ONLY_AT_B_J_SQUARED_L_J_R_J_SQUARED",
  );
  assert.equal(freeze.claim_status.universal_square_root_log_endpoint, "OPEN_NOT_CLAIMED");
  assert.equal(freeze.claim_status.clay_problem, "NOT_CLAIMED");
  assert.equal(freeze.publication_handoff.owner_task_title, "发布任务");
  assert.equal(freeze.publication_handoff.owner_task_id, "01a05bea-7f45-7410-8792-4e1f840b83f8");
  assert.equal(freeze.publication_handoff.task_reuse, false);
});

test("R0.74N exact certificate reproduces the frozen 84-row JSON", async () => {
  const python = process.env.CODEX_PYTHON || process.env.PYTHON || "python3";
  const { stdout } = await execFileAsync(
    python,
    ["scripts/r074n_all_shell_certificate.py"],
    { cwd: root, maxBuffer: 20 * 1024 * 1024 },
  );
  const bytes = Buffer.from(stdout);
  assert.deepEqual(bytes, await read("research/r074n_all_shell_certificate.json"));
  const certificate = JSON.parse(stdout);
  assert.equal(certificate.result, "PASS");
  assert.deepEqual(certificate.summary, { passed: 84, total: 84 });
  const byId = new Map(certificate.checks.map((row) => [row.id, row]));
  assert.equal(byId.get("bad_reserve").left, "72851/1270080");
  assert.equal(byId.get("outer_reserve").left, "1237/423360");
  assert.equal(byId.get("chord_uniform_majorant").left, "22/1");
  assert.equal(byId.get("outer_tail_factor").left, "2/1");
  assert.equal(
    certificate.status_flags.all_shell_analytic_proof,
    "REQUIRES_INDEPENDENT_AUDIT",
  );
});

test("R0.74N independent Ruby reconstruction matches all 84 rows", async () => {
  const { stdout } = await execFileAsync(
    "/usr/bin/ruby",
    ["scripts/r074n_all_shell_certificate_independent.rb"],
    { cwd: root, maxBuffer: 20 * 1024 * 1024 },
  );
  assert.match(stdout, /RESULT: PASS \(84\/84 checks\)/);
  assert.match(stdout, /PASS 84\/84/);
  assert.ok(stdout.includes("certificate_sha256: " + certificateHash));
  for (const marker of [
    "chord_uniform_majorant",
    "outer_tail_factor",
    "bad_reserve",
    "outer_reserve",
    "outer_summed_raw_R_power",
  ]) assert.ok(stdout.includes(marker), marker);
});

test("R0.74N adversarial certificate audit is bound and finite-only", async () => {
  const audit = await text("research/r074n_certificate_adversarial_audit.md");
  assert.ok(audit.includes("PASS, with the stated finite-only scope"));
  assert.ok(audit.includes("Single-byte, semantics-preserving mutation"));
  assert.ok(audit.includes("Canonical field mutation"));
  assert.ok(audit.includes(certificateHash));
  assert.ok(audit.includes("FINITE ONLY; NOT CLAY"));
});

test("R0.74N formal figure seal, entries, and external bindings are exact", async () => {
  const names = await readdir(resolve(root, figureBase));
  assert.equal(names.length, 26);

  for (const [name, digest] of figureFrozen)
    assert.equal(sha256(await read(figureBase + "/" + name)), digest, name);

  const manifest = JSON.parse(await text(figureBase + "/manifest.json"));
  const validation = JSON.parse(await text(figureBase + "/validation.json"));
  assert.equal(manifest.entries.length, 24);
  assert.equal(manifest.external_bindings.length, 21);
  assert.equal(manifest.validation, "PASS");
  assert.equal(validation.result, "PASS");
  assert.deepEqual(validation.summary, { passed: 67, total: 67 });

  for (const entry of manifest.entries) {
    const bytes = await read(figureBase + "/" + entry.path);
    assert.equal(bytes.byteLength, entry.bytes, entry.path + " bytes");
    assert.equal(sha256(bytes), entry.sha256, entry.path + " sha256");
  }
  for (const binding of manifest.external_bindings)
    assert.equal(sha256(await read(binding.path)), binding.sha256, binding.path);

  const lines = (await text(figureBase + "/SHA256SUMS")).trim().split("\n");
  assert.equal(lines.length, 25);
  const sealed = new Map();
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    sealed.set(match[2], match[1]);
  }
  assert.equal(sealed.size, 25);
  for (const name of names.filter((name) => name !== "SHA256SUMS"))
    assert.equal(sha256(await read(figureBase + "/" + name)), sealed.get(name), name);

  const results = JSON.parse(await text(figureBase + "/results.json"));
  assert.equal(results.analytic_proof_audit, "PASS");
  assert.equal(results.figure_package_independent_audit, "EXTERNAL_SEPARATE_NOT_CLAIMED");
  assert.equal(results.simulation, false);

  const svg = await text(figureBase + "/figure.svg");
  assert.equal((svg.match(/@font-face/g) ?? []).length, 2);
  assert.equal((svg.match(/data:font\/ttf;base64,/g) ?? []).length, 2);
  assert.ok(svg.includes("ANALYTIC AUDIT PASS"));
  assert.ok(svg.includes("FAMILYWISE"));
  assert.ok(svg.includes("NOT CLAY"));

  const caption = await text(figureBase + "/caption.md");
  for (const marker of [
    "k\\le j-1",
    "k\\ge j+1",
    "72851/1270080",
    "1237/423360",
    "no DNS",
    "NOT CLAY",
  ]) assert.ok(caption.includes(marker), marker);
});

test("R0.74N figure validator regenerates the seal byte-exact in isolation", async () => {
  const python = process.env.CODEX_PYTHON || process.env.PYTHON || "python3";
  const tempRoot = await mkdtemp(join(tmpdir(), "r074n-figure-gate-"));
  try {
    const sourcePackage = resolve(root, figureBase);
    const tempPackage = resolve(tempRoot, figureBase);
    await mkdir(dirname(tempPackage), { recursive: true });
    await cp(sourcePackage, tempPackage, { recursive: true });

    const manifest = JSON.parse(await text(figureBase + "/manifest.json"));
    for (const binding of manifest.external_bindings) {
      const destination = resolve(tempRoot, binding.path);
      await mkdir(dirname(destination), { recursive: true });
      await cp(resolve(root, binding.path), destination);
    }

    const wrapper = [
      "import importlib.util",
      "import sys",
      "from pathlib import Path",
      "validator_path = Path(sys.argv[1]).resolve()",
      "spec = importlib.util.spec_from_file_location('r074n_figure_validator', validator_path)",
      "validator = importlib.util.module_from_spec(spec)",
      "spec.loader.exec_module(validator)",
      "validator.PYTHON = Path(sys.executable)",
      "validator.main()",
    ].join("\n");
    const { stdout } = await execFileAsync(
      python,
      ["-B", "-c", wrapper, resolve(tempPackage, "validate.py")],
      {
        cwd: tempRoot,
        env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
        maxBuffer: 20 * 1024 * 1024,
      },
    );
    assert.match(stdout, /verify-only PASS 67\/67; 24 package entries/);

    const tempNames = await readdir(tempPackage);
    assert.deepEqual(tempNames.sort(), (await readdir(sourcePackage)).sort());
    for (const name of tempNames)
      assert.deepEqual(
        await readFile(resolve(tempPackage, name)),
        await readFile(resolve(sourcePackage, name)),
        name,
      );
  } finally {
    await rm(tempRoot, { recursive: true, force: true });
  }

  for (const [name, digest] of figureFrozen)
    assert.equal(sha256(await read(figureBase + "/" + name)), digest, "source " + name);
});

test("R0.74N reader source preserves the corrected evidence boundary", async () => {
  const report = await text("research/r074n_report-source.md");
  for (const marker of [
    "PROVED",
    "INDEPENDENT ANALYTIC AUDIT",
    "INHERITED",
    "FINITE",
    "LITERATURE BOUNDARY",
    "OPEN",
    "NOT CLAY",
    "独立 Ruby 版本",
    "X_j\\asymp\\mathfrak C_j",
    "0\\le\\mathcal D_{{\\rm ext},j}\\le CT_j",
    "普适平方根对数端点不等式",
  ]) assert.ok(report.includes(marker), marker);
  for (const forbidden of [
    "我们",
    "首次证明",
    "世界首个",
    "解决千禧年问题",
    "接近解决",
  ]) assert.ok(!report.includes(forbidden), forbidden);

  const readerAudit = await text("research/r074n_reader_source_independent_audit.md");
  assert.ok(readerAudit.includes("R0.74N READER SOURCE: PASS; CROSS-NOTE BOUND; NOT CLAY"));
  assert.ok(readerAudit.includes("\\mathcal D_{{\\rm ext},j}\\ge cT_j"));
  assert.ok(readerAudit.includes("has been proved"));

  const forbiddenControl = /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/;
  for (const path of frozen.keys())
    assert.ok(!forbiddenControl.test(await text(path)), path);
});

test("R0.74N bounded literature audit keeps the non-novelty boundary", async () => {
  const literature = await text("research/r074n_primary_literature_boundary.md");
  const audit = await text("research/r074n_primary_literature_independent_audit.md");
  for (const marker of [
    "David Villringer",
    "Victor Gardner, Kyle L. Liss, and Jonathan C. Mattingly",
    "Kyle L. Liss and Kunhui Luan",
    "finite non-hit is not evidence of novelty",
  ]) assert.ok(literature.includes(marker), marker);
  assert.ok(audit.includes("Verdict: **PASS**"));
  assert.ok(audit.includes("does **not** turn that bounded non-hit into a"));
  assert.ok(audit.includes("NOT CLAY"));
});
