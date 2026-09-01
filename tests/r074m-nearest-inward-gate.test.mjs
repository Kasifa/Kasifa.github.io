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

const proofHash = "0077326ca97cfe40a0a43019caf0118504cf9ed770979595d63bf9d2ec281ef0";
const certificateHash = "5aed76e6c2aac58c1507784dd014a132560967a1bb89e69080fa0e170f65462f";

const frozen = new Map([
  ["research/r074m_problem_freeze.md", "5a6a95aae1fd00f7b7ddc79a5387b3ad3c7c675ca7eb1c92f51604f42fa4747c"],
  ["research/r074m_final_segment_expulsion.md", proofHash],
  ["research/r074m_nearest_inward_independent_audit.md", "6e81954068dbcf588c857a6ebb1e1dcc80c70d6c926f8631aba8b2bff84c281c"],
  ["research/r074m_final_source_rebind_audit.md", "5b9e9cdd77b92647dc8fb1a9602d44cc43274a7515b3a5a51d629a3b3005f86d"],
  ["research/r074m_gap_matrix.md", "b9480faf5ff607e17ca062222108df7fc8700684f968bef769d2c5b1ced59ea6"],
  ["research/r074m_primary_literature_boundary.md", "3e611c2e4d7ac308498f442c6d71f75226d763e40944bd49645c77b2b918cf53"],
  ["research/r074m_report-source.md", "37c635bf2a57d0ed01fd50838fbea4ed00fd0da0144e5bc53e13c8311b6306af"],
  ["research/r074m_bilingual_dictionary.md", "2cdef53de03fa7f032e61943c1664949a2c77aeacde924488105cdbe41954899"],
  ["research/r074m_reader_source_independent_audit.md", "f430e30bd9c5f5fda1fbfda360532c4b2595331610b4e98084e38d53076da147"],
  ["research/r074m_nearest_inward_certificate.json", certificateHash],
  ["research/r074m_nearest_inward_certificate_report.md", "6b4adcfe0992e37cba1a88d756f61b5c92e02517e17bb0e05acbffae8b0dbe25"],
  ["research/r074m_certificate_independent_audit.md", "20d710164cb6ae02b3214c4d45195d035c4758fdaa6df87cb307d6c17dc9f234"],
  ["research/r074m_figure_independent_audit.md", "4c4f6621b3d637f3fec53c526c97e01520b1b9e251b2912a8638be298e708347"],
  ["scripts/r074m_nearest_inward_certificate.py", "a888185d84252280ace748c75c07c08de808af3b1af54f74f9683299bbc414d5"],
  ["scripts/r074m_nearest_inward_certificate_independent.rb", "8a13a8268ed0e8ec1824df10102d48eef2246820594805e8f9e20118b00b2a5f"],
  ["research/r074m_freeze_manifest.json", "3604f29f99abe4b4c98c7867bcb1dd470e5fece225b23a473893475592a8350e"],
]);

const figureBase = "research/figures/r074m/fig-r074m-nearest-inward-expulsion";
const figureFrozen = new Map([
  ["figure.svg", "bfe895023513c536e6bc1fca07531560d932f5e30bd3acc7e1c106e1d756c2de"],
  ["figure.pdf", "1773da1a48e7bd0086d035261beb9647074af1e5ee3f63d53d34d4805b217d31"],
  ["figure.png", "aa91000e5c529cd48b176500571a7155f494582e794e7888119f63f1774da0a8"],
  ["qa-svg-quicklook.png", "08dfb6f7b576cc996e3388faff7a0cc93c8dbe9176c696cd36840644e4304e38"],
  ["source-data.csv", "b94b5b4357b660adc2227207be552ffa5726c3dc1e3ed10773066d375a6429a2"],
  ["plot.py", "84a9ae03679f62eb820c2a2ab074f361409e94882efdedcffdc9f27697a1bf8a"],
  ["validate.py", "8ee34fc17c30c304f98d58fd43e8eb02a99680281677698647e600d4d929db8a"],
  ["validation.json", "dba5b7ce493d73ca8750ea4fb093ab153a7c3fa384848767a46660b96f1a5d5b"],
  ["manifest.json", "78c89ee287c0f3d5b20625eac7869a749dec137e11ba4878617d8907a8f6446c"],
  ["SHA256SUMS", "acb5b41c73af70245e468996411d221866b39e274dda2d5594077c330573f3cb"],
]);

test("R0.74M mathematical and reader assets remain byte-exact", async () => {
  for (const [path, expected] of frozen)
    assert.equal(sha256(await read(path)), expected, path);

  const proof = await text("research/r074m_final_segment_expulsion.md");
  const tags = proof.match(/\\tag\{[^}]+\}/g) ?? [];
  assert.equal(tags.length, 49);
  assert.equal(new Set(tags).size, 49);

  for (const path of [
    "research/r074m_nearest_inward_independent_audit.md",
    "research/r074m_final_source_rebind_audit.md",
    figureBase + "/manifest.json",
  ]) assert.ok((await text(path)).includes(proofHash), path);

  const freeze = JSON.parse(await text("research/r074m_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.74M");
  assert.equal(freeze.origin_main_baseline, "a575c4e4affdf8d2cf363fd6eb1040f06098c1ac");
  assert.equal(
    freeze.claim_status.complete_signed_nearest_inward_row,
    "PROVED_AT_C_GAMMA_J_L_J_R_J_POWER_5_AND_INDEPENDENTLY_AUDITED",
  );
  assert.equal(freeze.claim_status.remaining_shell_synthesis, "OPEN");
  assert.equal(freeze.claim_status.clay_problem, "NOT_CLAIMED");
  assert.equal(freeze.publication_handoff.owner_task_title, "发布任务");
  assert.equal(freeze.publication_handoff.owner_task_id, "01a05bea-7f45-7410-8792-4e1f840b83f8");
  assert.equal(freeze.publication_handoff.task_reuse, false);
});

test("R0.74M exact certificate reproduces the frozen 38-row JSON", async () => {
  const python = process.env.CODEX_PYTHON || process.env.PYTHON || "python3";
  const { stdout } = await execFileAsync(
    python,
    ["scripts/r074m_nearest_inward_certificate.py"],
    { cwd: root, maxBuffer: 10 * 1024 * 1024 },
  );
  const bytes = Buffer.from(stdout);
  assert.deepEqual(bytes, await read("research/r074m_nearest_inward_certificate.json"));
  const certificate = JSON.parse(stdout);
  assert.equal(certificate.result, "PASS");
  assert.deepEqual(certificate.summary, { passed: 38, total: 38 });
  assert.equal(certificate.derived.geometry_gap, "149/5040");
  assert.equal(certificate.derived.heat_margin_at_L0, "433872896/97575");
  assert.equal(certificate.derived.bad_event_gap, "24497/423360");
  assert.equal(certificate.derived.super_rate, "1/320");
  assert.equal(
    certificate.status_flags.nearest_inward_analytic_proof,
    "REQUIRES_INDEPENDENT_AUDIT",
  );
  assert.ok((await text("research/r074m_nearest_inward_independent_audit.md"))
    .includes("INDEPENDENT ANALYTIC AUDIT: PASS"));
});

test("R0.74M independent Ruby reconstruction matches all 38 rows", async () => {
  const { stdout } = await execFileAsync(
    "/usr/bin/ruby",
    ["scripts/r074m_nearest_inward_certificate_independent.rb"],
    { cwd: root, maxBuffer: 10 * 1024 * 1024 },
  );
  assert.match(stdout, /RESULT: PASS \(38\/38 checks\)/);
  assert.match(stdout, /PASS 38\/38/);
  assert.ok(stdout.includes("certificate_sha256: " + certificateHash));
  for (const marker of [
    "geometry_gap",
    "heat_margin_at_L0",
    "bad_event_gap",
    "bad_R_power",
    "good_R_power",
  ]) assert.ok(stdout.includes(marker), marker);
});

test("R0.74M formal figure seal, entries, and external bindings are exact", async () => {
  const names = await readdir(resolve(root, figureBase));
  assert.equal(names.length, 24);

  for (const [name, digest] of figureFrozen)
    assert.equal(sha256(await read(figureBase + "/" + name)), digest, name);

  const manifest = JSON.parse(await text(figureBase + "/manifest.json"));
  const validation = JSON.parse(await text(figureBase + "/validation.json"));
  assert.equal(manifest.entries.length, 22);
  assert.equal(manifest.external_bindings.length, 5);
  assert.equal(manifest.validation, "PASS");
  assert.equal(validation.result, "PASS");
  assert.deepEqual(validation.summary, { passed: 49, total: 49 });

  for (const entry of manifest.entries) {
    const bytes = await read(figureBase + "/" + entry.path);
    assert.equal(bytes.byteLength, entry.bytes, entry.path + " bytes");
    assert.equal(sha256(bytes), entry.sha256, entry.path + " sha256");
  }
  for (const binding of manifest.external_bindings)
    assert.equal(sha256(await read(binding.path)), binding.sha256, binding.path);

  const lines = (await text(figureBase + "/SHA256SUMS")).trim().split("\n");
  assert.equal(lines.length, 23);
  const sealed = new Map();
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    sealed.set(match[2], match[1]);
  }
  assert.equal(sealed.size, 23);
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
  assert.ok(svg.includes("NOT CLAY"));

  const caption = await text(figureBase + "/caption.md");
  for (const marker of [
    "\\to\\infty",
    "\\ge",
    "\\mathbb P",
    "\\le",
    "1/(8L)",
    "149/5040",
  ]) assert.ok(caption.includes(marker), marker);
  assert.ok(!caption.includes("\t"));
});

test("R0.74M figure validator regenerates the seal byte-exact in isolation", async () => {
  const python = process.env.CODEX_PYTHON || process.env.PYTHON || "python3";
  const tempRoot = await mkdtemp(join(tmpdir(), "r074m-figure-gate-"));
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
      "import shutil",
      "import sys",
      "from pathlib import Path",
      "validator_path = Path(sys.argv[1]).resolve()",
      "spec = importlib.util.spec_from_file_location('r074m_figure_validator', validator_path)",
      "validator = importlib.util.module_from_spec(spec)",
      "spec.loader.exec_module(validator)",
      "pdfinfo = shutil.which('pdfinfo')",
      "if not pdfinfo:",
      "    raise SystemExit('portable verifier requires pdfinfo on PATH')",
      "validator.PDFINFO = Path(pdfinfo)",
      "validator.PYTHON = Path(sys.executable)",
      "validator.main()",
    ].join("\n");
    const override = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/bin/override";
    const { stdout } = await execFileAsync(
      python,
      ["-B", "-c", wrapper, resolve(tempPackage, "validate.py")],
      {
        cwd: tempRoot,
        env: {
          ...process.env,
          PATH: override + ":" + (process.env.PATH || ""),
          PYTHONDONTWRITEBYTECODE: "1",
        },
        maxBuffer: 10 * 1024 * 1024,
      },
    );
    assert.match(stdout, /verify-only PASS 49\/49; 22 package entries/);

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

test("R0.74M reader source keeps the exact evidence and prose boundary", async () => {
  const report = await text("research/r074m_report-source.md");
  for (const marker of [
    "PROVED",
    "INDEPENDENT ANALYTIC AUDIT",
    "INHERITED",
    "FINITE",
    "LITERATURE BOUNDARY",
    "OPEN",
    "NOT CLAY",
    "I_{R_j}=(64R_j^2,65R_j^2)",
    "\\int_{61R_j^2}^{\\tau}",
    "T=R_j^2+t",
    "149/5040-1/(8L_j)",
    "38/38",
  ]) assert.ok(report.includes(marker), marker);
  for (const forbidden of [
    "我们",
    "攻关",
    "主攻",
    "研究纪律",
    "三重审计",
    "杀死错误想法",
    "突破",
    "首次证明",
    "世界首个",
    "解决千禧年问题",
    "接近解决",
    "全 winding",
    "正弦切片",
  ]) assert.ok(!report.includes(forbidden), forbidden);
  assert.ok(!report.includes("\t"));

  const forbiddenControl = /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/;
  for (const path of frozen.keys())
    assert.ok(!forbiddenControl.test(await text(path)), path);

  const readerAudit = await text("research/r074m_reader_source_independent_audit.md");
  assert.ok(readerAudit.includes("CURRENT R0.74M READER SOURCE: PASS; NOT CLAY"));
});
