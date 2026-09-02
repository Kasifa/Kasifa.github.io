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
  writeFile,
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

const python =
  process.env.CODEX_PYTHON ||
  process.env.PYTHON ||
  "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const ruby = "/usr/bin/ruby";
const proofHash = "471158de1db718ac96f38adc729464d8717006f47c8c6bb57834cc4e159bd9bb";
const certificateHash = "30fd77ae3b4c88628e2d84207fc9b1728b1ab2343bf187fcd1141b080d6c5a5b";
const manifestHash = "2335dc0ce751c5c50002dd5075eaa6df741c2f388599ed57c7acedc33fa684d7";

const frozen = new Map([
  ["research/r074o_problem_freeze.md", "c461b85425e58ad0bb371bf7e1e6fe79301fd200912c67a15d4d8ebefb9ec54f"],
  ["research/r074o_amplitude_endpoint_counterexample.md", proofHash],
  ["research/r074o_amplitude_endpoint_independent_audit.md", "44ad81c0623bbba006eac0aabc8fb9a77dccde4229c50061d78e59590c6bea22"],
  ["research/r074o_final_source_rebind_audit.md", "403dfe8e0b7c7cd74b68b23d74bb0da9f9d2064719a5a168eac5042868429484"],
  ["research/r074o_gap_matrix.md", "11aaae9308056cb2afa5b8d3166fbeecf9713aeb77e05bd5128fc3835231cdcd"],
  ["research/r074o_primary_literature_boundary.md", "2925a699299b45d2d84da8ae182fdddbf94aac02195a6e7a02b93b37efce0708"],
  ["research/r074o_primary_literature_independent_audit.md", "85072caeb8c23fa17d163b8ab793d105541547f2e5c575f5cbdba4e7d1b08c14"],
  ["research/r074o_report-source.md", "c4e6363293e1a11d35d826a24b9d7bbf00e202ff9b31f1609e0ff99eb82330c3"],
  ["research/r074o_bilingual_dictionary.md", "9dfecf5ccfef88bf7ad2b63532c825078af5665aae0862679323a63a78424e87"],
  ["research/r074o_reader_source_independent_audit.md", "8bdcb2916c955fb9ae7e49d1156323271f38bb007c2933b5d2037721195cb07c"],
  ["research/r074o_amplitude_endpoint_certificate.json", certificateHash],
  ["research/r074o_amplitude_endpoint_certificate_report.md", "308453e68ec9ce2ef7b1e2a16d6faacbdc333fdfd5604417929fbca634db10fa"],
  ["research/r074o_certificate_independent_audit.md", "3ddc0e06ca8622c546a8e184f56efcc9bf7ca836b9cb476f11ef4e9e63476d47"],
  ["scripts/r074o_amplitude_endpoint_certificate.py", "3a01ab8659ed5a96bce92aa15df8190437f98522e935858d4e5840e629358671"],
  ["scripts/r074o_amplitude_endpoint_certificate_independent.rb", "562a13ebd3f66438919bccdd842fb2d2c5348f2c313fa071d39e878dd39d4062"],
  ["research/r074o_milestone_recap_delta.md", "c12c7f3fb5a30656669bcc73dbfe654b675a77d44f327974575f469283c120c2"],
  ["research/r074o_milestone_recap_independent_audit.md", "822b0a450f254f32670394d7f9962256552c1747b8860daa5df5d6245c60b8a8"],
  ["research/r074o_figure_independent_audit.md", "ba5e3f4f69bc3d951b9dcec24f77c0048e6f3002d7b8477a55f5e1492ef8cfb5"],
  ["research/r074o_freeze_manifest.json", manifestHash],
]);

const figureBase = "research/figures/r074o/fig-r074o-amplitude-endpoint";
const figureFrozen = new Map([
  ["figure.svg", "aab4bca1d44fa248d9e108312dfdfb933b835d524fe86b915beaf4f22f7475de"],
  ["figure.pdf", "3ed235968190c828ed1dfbc3b97c2201ea32902a3a180caa3b11ef6bf0a8a5da"],
  ["figure.png", "e5578383c4f982f6f2aed74397dbe80ea8369f987d97b058db20b40fcc7ff3b1"],
  ["qa-svg-quicklook.png", "872532e61707c751a3040fa769923813655335dbf3359631836b9b049d0bd57f"],
  ["source-data.csv", "513bb7a6961b68bc7ec30e4dcc46314eb58924c0bd4eccb023c42911130b1e07"],
  ["plot.py", "2e568afc1a885f53efaa746db2f38505b959933fd66aa0fc5da1292e7d4f7918"],
  ["validate.py", "1369d62ec197448245e140355149e47e089d401d7f71b80a9ddf042386505e4d"],
  ["validation.json", "00ff7b024f9bfc8ec181c98551e2d0382cf7ace7fddd93a8aefe37ee1f8a61c8"],
  ["manifest.json", "97aa60ceb42807c14d8325d37df1b7214e33e4ea10bf12af77178265b2eea2d2"],
  ["SHA256SUMS", "63d2e352b49988bca779703008b4a24697dcc2ba41b4d0c1b80eb868ed4fc1e9"],
]);

async function prepareIsolatedFigure(prefix) {
  const tempRoot = await mkdtemp(join(tmpdir(), prefix));
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
  return { tempRoot, sourcePackage, tempPackage };
}

async function assertPackageByteIdentical(sourcePackage, tempPackage) {
  const sourceNames = (await readdir(sourcePackage)).sort();
  const tempNames = (await readdir(tempPackage)).sort();
  assert.deepEqual(tempNames, sourceNames);
  for (const name of sourceNames) {
    assert.deepEqual(
      await readFile(resolve(tempPackage, name)),
      await readFile(resolve(sourcePackage, name)),
      name,
    );
  }
}

async function decodedPng(path) {
  const script = [
    "import hashlib, json, sys",
    "from PIL import Image",
    "with Image.open(sys.argv[1]) as image:",
    "    payload = {",
    "        'mode': image.mode,",
    "        'size': [image.width, image.height],",
    "        'pixel_sha256': hashlib.sha256(image.tobytes()).hexdigest(),",
    "    }",
    "print(json.dumps(payload, sort_keys=True))",
  ].join("\n");
  const { stdout } = await execFileAsync(python, ["-B", "-c", script, path], {
    cwd: root,
    maxBuffer: 1024 * 1024,
  });
  return JSON.parse(stdout);
}

function normalizedResults(value) {
  return {
    ...value,
    outputs: { ...value.outputs, png_sha256: "<platform-png-encoding>" },
  };
}

function normalizedManifest(value) {
  const platformEncoded = new Set([
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-svg-quicklook.png",
    "results.json",
  ]);
  return {
    ...value,
    entries: value.entries.map((entry) =>
      platformEncoded.has(entry.path)
        ? { ...entry, bytes: "<platform-png-encoding>", sha256: "<platform-png-encoding>" }
        : entry,
    ),
  };
}

function parseSeal(value) {
  const entries = new Map();
  for (const line of value.trim().split("\n")) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    entries.set(match[2], match[1]);
  }
  return entries;
}

async function assertCrossPlatformRegenerationEquivalent(sourcePackage, tempPackage) {
  const sourceNames = (await readdir(sourcePackage)).sort();
  const tempNames = (await readdir(tempPackage)).sort();
  assert.deepEqual(tempNames, sourceNames);

  const pngNames = [
    "figure.png",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-svg-quicklook.png",
  ];
  for (const name of pngNames) {
    assert.deepEqual(
      await decodedPng(resolve(tempPackage, name)),
      await decodedPng(resolve(sourcePackage, name)),
      name + " decoded pixels",
    );
  }

  const normalizedNames = new Set([
    ...pngNames,
    "results.json",
    "manifest.json",
    "SHA256SUMS",
  ]);
  for (const name of sourceNames.filter((name) => !normalizedNames.has(name))) {
    assert.deepEqual(
      await readFile(resolve(tempPackage, name)),
      await readFile(resolve(sourcePackage, name)),
      name,
    );
  }

  const sourceResults = JSON.parse(await readFile(resolve(sourcePackage, "results.json"), "utf8"));
  const tempResults = JSON.parse(await readFile(resolve(tempPackage, "results.json"), "utf8"));
  assert.deepEqual(normalizedResults(tempResults), normalizedResults(sourceResults));
  assert.equal(tempResults.outputs.png_sha256, sha256(await readFile(resolve(tempPackage, "figure.png"))));

  const sourceManifest = JSON.parse(await readFile(resolve(sourcePackage, "manifest.json"), "utf8"));
  const tempManifest = JSON.parse(await readFile(resolve(tempPackage, "manifest.json"), "utf8"));
  assert.deepEqual(normalizedManifest(tempManifest), normalizedManifest(sourceManifest));

  const sourceSeal = parseSeal(await readFile(resolve(sourcePackage, "SHA256SUMS"), "utf8"));
  const tempSeal = parseSeal(await readFile(resolve(tempPackage, "SHA256SUMS"), "utf8"));
  assert.deepEqual([...tempSeal.keys()].sort(), [...sourceSeal.keys()].sort());
  for (const name of sourceSeal.keys()) {
    assert.equal(
      tempSeal.get(name),
      sha256(await readFile(resolve(tempPackage, name))),
      name + " regenerated seal",
    );
    if (!normalizedNames.has(name))
      assert.equal(tempSeal.get(name), sourceSeal.get(name), name + " frozen-byte equivalence");
  }
}

test("R0.74O frozen artifacts and claim manifest remain byte-exact", async () => {
  for (const [path, expected] of frozen)
    assert.equal(sha256(await read(path)), expected, path);

  const freeze = JSON.parse(await text("research/r074o_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.74O");
  assert.equal(freeze.research_branch, "codex/r074o-amplitude-endpoint");
  assert.equal(freeze.origin_main_baseline, "d112c7b5b393ccd16305b4e00a2ae0692c9262a4");
  assert.deepEqual(freeze.publication_prerequisite, {
    live_baseline_release: "R0.74N",
    live_baseline_origin_main: "d112c7b5b393ccd16305b4e00a2ae0692c9262a4",
    prerequisite_status: "SATISFIED_AND_LIVE",
    r074o_status: "PENDING_SEPARATE_PUBLISHING_TASK",
  });
  assert.equal(
    freeze.claim_status.scalar_payment_only_square_root_log_endpoint,
    "FALSE_PROVED_BY_SMOOTH_EXACT_GLOBAL_PERIODIC_UNFORCED_FAMILY",
  );
  assert.equal(
    freeze.claim_status.fixed_logarithmic_power_at_two_thirds,
    "FALSE_FOR_EVERY_FIXED_GAMMA_WITH_FAMILY_ALLOWED_TO_DEPEND_ON_GAMMA",
  );
  assert.equal(
    freeze.claim_status.realized_scalar_sub_frontier_no_go,
    "PROVED_FOR_EVERY_O_OF_P_TO_Q_STAR_TIMES_LOG_POWER_7_OVER_6_NOT_CLAIMED_OPTIMAL",
  );
  assert.equal(freeze.claim_status.augmented_structural_endpoints, "OPEN_NOT_REFUTED");
  assert.equal(freeze.claim_status.singularity_or_blowup, "NOT_CONSTRUCTED");
  assert.equal(freeze.claim_status.global_regularity_for_arbitrary_data, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.novelty_or_priority, "OPEN_NOT_CLAIMED");
  assert.equal(freeze.claim_status.clay_problem, "NOT_CLAIMED_NOT_CLAY");
  assert.equal(freeze.publication_handoff.owner_task_title, "发布任务");
  assert.equal(freeze.publication_handoff.owner_task_id, "01a05bea-7f45-7410-8792-4e1f840b83f8");
  assert.equal(freeze.publication_handoff.task_reuse, false);
  assert.equal(freeze.publication_handoff.target_html, "/notes/r0-74o.html");
  assert.equal(freeze.publication_handoff.target_pdf, "/notes/r0-74o.pdf");
  assert.equal(freeze.publication_handoff.recap_update_required, true);

  const forbiddenControl = /[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/;
  for (const path of frozen.keys())
    assert.ok(!forbiddenControl.test(await text(path)), path);
});

test("R0.74O proof, analytic audit, and source rebind preserve all 96 tagged claims", async () => {
  const problem = await text("research/r074o_problem_freeze.md");
  const proof = await text("research/r074o_amplitude_endpoint_counterexample.md");
  const audit = await text("research/r074o_amplitude_endpoint_independent_audit.md");
  const rebind = await text("research/r074o_final_source_rebind_audit.md");
  const problemTags = problem.match(/\\tag\{[^}]+\}/g) ?? [];
  const proofTags = proof.match(/\\tag\{[^}]+\}/g) ?? [];
  assert.equal(problemTags.length, 21);
  assert.equal(new Set(problemTags).size, 21);
  assert.equal(proofTags.length, 75);
  assert.equal(new Set(proofTags).size, 75);
  assert.equal(new Set([...problemTags, ...proofTags]).size, 96);

  for (const marker of [
    "is false.  Here \\(P_R^\\alpha\\)",
    "There is one sequence of smooth periodic mean-zero unforced global",
    "Theorem 6.1 — scalar sub-frontier no-go",
    "Corollary 7.1 — every fixed logarithmic power fails",
    "The family in this corollary is allowed to depend on \\(\\gamma\\)",
    "No optimality claim beyond that ledger is made.",
    "No theorem with an additional temporal, geometric, Carleson, BV,",
    "Global regularity and the Millennium problem remain open.",
    "**NOT CLAY.**",
  ]) assert.ok(proof.includes(marker), marker);
  assert.equal(
    (proof.match(/Although the physical pressure is zero, the frozen local pressure gauge is/g) ?? []).length,
    1,
  );
  for (const marker of [
    proofHash,
    "Verdict: PASS",
    "family may depend on the prescribed \\(\\gamma\\)",
    "claimed to defeat all \\(\\gamma\\) simultaneously.",
    "No optimal replacement, novelty, or priority conclusion follows.",
    "INDEPENDENT MATHEMATICAL AUDIT: PASS; NOT CLAY",
  ]) assert.ok(audit.includes(marker), marker);
  for (const marker of [
    proofHash,
    "PASS; duplicate removed.",
    "PASS; equation (6.9) is well formed.",
    "FINAL SOURCE REBIND: PASS; 96/96 UNIQUE TAGS; NOT CLAY",
  ]) assert.ok(rebind.includes(marker), marker);
});

test("R0.74O Python certificate reproduces the frozen 245-row JSON byte-for-byte", async () => {
  const { stdout } = await execFileAsync(
    python,
    ["-B", "scripts/r074o_amplitude_endpoint_certificate.py"],
    { cwd: root, maxBuffer: 30 * 1024 * 1024 },
  );
  assert.deepEqual(Buffer.from(stdout), await read("research/r074o_amplitude_endpoint_certificate.json"));
  const certificate = JSON.parse(stdout);
  assert.equal(certificate.result, "PASS");
  assert.deepEqual(certificate.summary, {
    passed: 245,
    polynomial_rows: 7,
    scale_rows: 9,
    total: 245,
    unique_ids: 245,
    window_rows: 8,
  });
  assert.equal(new Set(certificate.checks.map((row) => row.id)).size, 245);
  assert.equal(certificate.derived.energy_reserve, "1171/943200");
  assert.equal(certificate.derived.delta, "86/11907");
  assert.equal(certificate.derived.q_star, "8024/11907");
  assert.equal(certificate.derived.observable_log_power, "7/6");
  assert.equal(certificate.analytic_boundary.at(-1), "does not solve the Clay Millennium problem; NOT CLAY");
});

test("R0.74O independent Ruby Rational reconstruction matches all 245 rows", async () => {
  const { stdout } = await execFileAsync(
    ruby,
    ["scripts/r074o_amplitude_endpoint_certificate_independent.rb"],
    { cwd: root, maxBuffer: 30 * 1024 * 1024 },
  );
  assert.ok(stdout.includes("certificate_sha256: " + certificateHash));
  assert.match(stdout, /audit_window: j=14\.\.21/);
  assert.match(stdout, /scale_rows: 9/);
  assert.match(stdout, /window_rows: 8/);
  assert.match(stdout, /polynomial_rows: 7/);
  assert.match(stdout, /RESULT: PASS \(245\/245 checks\)/);
  assert.match(stdout, /PASS 245\/245/);
});

test("R0.74O Ruby verifier rejects a valid-JSON semantic tamper", async () => {
  const tempRoot = await mkdtemp(join(tmpdir(), "r074o-certificate-tamper-"));
  try {
    const certificate = JSON.parse(await text("research/r074o_amplitude_endpoint_certificate.json"));
    const row = certificate.checks.find((item) => item.id === "energy_reserve_exact");
    assert.ok(row);
    row.left = "1170/943201";
    const tamperedPath = resolve(tempRoot, "tampered-valid.json");
    await writeFile(tamperedPath, JSON.stringify(certificate, null, 2) + "\n", "utf8");
    assert.equal(JSON.parse(await readFile(tamperedPath, "utf8")).checks.length, 245);

    let rejection;
    try {
      await execFileAsync(
        ruby,
        ["scripts/r074o_amplitude_endpoint_certificate_independent.rb", tamperedPath],
        { cwd: root, maxBuffer: 30 * 1024 * 1024 },
      );
    } catch (error) {
      rejection = error;
    }
    assert.ok(rejection, "tampered valid JSON unexpectedly passed");
    assert.equal(rejection.code, 1);
    const output = String(rejection.stdout ?? "") + String(rejection.stderr ?? "");
    assert.ok(output.includes("RESULT: FAIL"));
    assert.ok(output.includes("independent reconstruction differs"));
    assert.ok(output.includes("certificate SHA-256"));
  } finally {
    await rm(tempRoot, { recursive: true, force: true });
  }
});

test("R0.74O reader, literature, and milestone recap retain their audited boundaries", async () => {
  const report = await text("research/r074o_report-source.md");
  const dictionary = await text("research/r074o_bilingual_dictionary.md");
  const readerAudit = await text("research/r074o_reader_source_independent_audit.md");
  const literature = await text("research/r074o_primary_literature_boundary.md");
  const literatureAudit = await text("research/r074o_primary_literature_independent_audit.md");
  const recap = await text("research/r074o_milestone_recap_delta.md");
  const recapAudit = await text("research/r074o_milestone_recap_independent_audit.md");

  for (const marker of [
    "### PROVED",
    "### INHERITED",
    "### FINITE",
    "### LITERATURE BOUNDARY",
    "### OPEN",
    "**NOT CLAY.**",
    "8024/11907",
    "1171/943200",
    "这里的解族可以依赖于给定的 \\(\\gamma\\)",
    "这里没有声称 \\(8024/11907\\) 是最优指数",
  ]) assert.ok(report.includes(marker), marker);
  for (const forbidden of ["我们", "首次证明", "世界首个", "解决千禧年问题", "接近解决"])
    assert.ok(!report.includes(forbidden), forbidden);
  for (const marker of [
    "scalar-payment-only estimate",
    "The exact family may depend on the fixed \\(\\gamma\\)",
    "finite non-hit is not novelty or priority evidence",
    "NOT CLAY",
  ]) assert.ok(dictionary.includes(marker), marker);
  assert.ok(readerAudit.includes("R0.74O READER SOURCE: PASS; SCALAR NO-GO BOUND; NOT CLAY"));
  assert.ok(readerAudit.includes("one polynomial-amplitude sequence is not claimed"));

  assert.equal((literature.match(/^\| S\d+ \|/gm) ?? []).length, 14);
  assert.equal((literatureAudit.match(/^\| S\d+ \|/gm) ?? []).length, 14);
  assert.ok(literature.includes("finite non-hit is not evidence of novelty, priority"));
  assert.ok(literature.includes("NO DIRECT HIT FOUND"));
  assert.ok(literatureAudit.includes("Verdict: **PASS**"));
  assert.ok(literatureAudit.includes("not used as evidence of novelty"));
  assert.ok(literatureAudit.includes("**NOT CLAY.**"));

  for (const marker of [
    "R0.74O 是重大路线里程碑，本次必须更新累计 recap",
    "scalar-payment-only 类中严格为 FALSE",
    "这里的解族允许依赖 \\(\\gamma\\)",
    "发布任务",
    "旧 `public/recap-r0-61-r0-73x.html` 与 PDF 应保留",
  ]) assert.ok(recap.includes(marker), marker);
  assert.ok(recapAudit.includes("Seventeen-node reconstruction"));
  assert.ok(recapAudit.includes("R0.74O MILESTONE RECAP DELTA: INDEPENDENT PASS; NOT CLAY"));
  assert.ok(recapAudit.includes("must preserve the R0.61--R0.73X historical recap"));
});

test("R0.74O figure inventory, 24-entry manifest, 15 bindings, and 25-line seal are exact", async () => {
  const names = await readdir(resolve(root, figureBase));
  assert.equal(names.length, 26);
  for (const [name, digest] of figureFrozen)
    assert.equal(sha256(await read(figureBase + "/" + name)), digest, name);

  const manifest = JSON.parse(await text(figureBase + "/manifest.json"));
  const validation = JSON.parse(await text(figureBase + "/validation.json"));
  assert.equal(manifest.entries.length, 24);
  assert.equal(manifest.external_bindings.length, 15);
  assert.equal(manifest.validation, "PASS");
  assert.equal(validation.result, "PASS");
  assert.deepEqual(validation.summary, { passed: 72, total: 72 });
  assert.equal(new Set(validation.checks.map((item) => item.id)).size, 72);
  assert.ok(validation.checks.every((item) => item.pass));

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
});

test("R0.74O figure is vector/font-bound, analytic-only, and keeps the component boundary", async () => {
  const svg = await text(figureBase + "/figure.svg");
  const caption = await text(figureBase + "/caption.md");
  const contract = JSON.parse(await text(figureBase + "/contract.json"));
  const results = JSON.parse(await text(figureBase + "/results.json"));
  const validation = JSON.parse(await text(figureBase + "/validation.json"));
  const audit = await text("research/r074o_figure_independent_audit.md");

  assert.equal((svg.match(/@font-face/g) ?? []).length, 2);
  assert.equal((svg.match(/data:font\/ttf;base64,/g) ?? []).length, 2);
  assert.equal((svg.match(/<image\b/gi) ?? []).length, 0);
  for (const marker of [
    "SCALAR-PAYMENT-ONLY NO-GO",
    "smooth exact family",
    "1171/943200",
    "8024/11907",
    "no separate",
    "no DNS/simulation/fitted data",
    "NOT CLAY",
  ]) assert.ok(svg.includes(marker), marker);
  assert.equal(contract.simulation, false);
  assert.equal(results.simulation, false);
  assert.equal(
    contract.component_boundary,
    "The lower bound for X_* comes from endpoint energy; no separate lower bound is proved for its dissipation component.",
  );
  assert.ok(caption.includes("no separate lower bound is proved for its dissipation component"));
  assert.ok(caption.includes("no DNS, simulation, sampled path, singularity, or universal replacement theorem"));
  assert.equal(results.figure_package_independent_audit, "EXTERNAL_SEPARATE_NOT_CLAIMED");
  for (const id of [
    "pdf_vector_no_images",
    "pdf_embedded_font_names",
    "svg_vector_only",
    "svg_embedded_fonts",
    "analytic_not_simulated",
    "varkappa_not_kappa",
  ]) assert.equal(validation.checks.find((item) => item.id === id)?.pass, true, id);
  assert.ok(audit.includes("INDEPENDENT FIGURE-PACKAGE AUDIT: PASS"));
  assert.ok(audit.includes("PASS; SCALAR-PAYMENT-ONLY SCOPE; NO DNS OR SIMULATION; NO SEPARATE"));
  assert.ok(audit.includes("DISSIPATION LOWER; NO NOVELTY OR PRIORITY CLAIM; NOT CLAY"));
});

test("R0.74O figure validator reproduces all sealed metadata byte-exact in isolation", async () => {
  const { tempRoot, sourcePackage, tempPackage } = await prepareIsolatedFigure("r074o-figure-validate-");
  try {
    const { stdout } = await execFileAsync(
      python,
      ["-B", resolve(tempPackage, "validate.py")],
      {
        cwd: tempPackage,
        env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
        maxBuffer: 30 * 1024 * 1024,
        timeout: 300_000,
      },
    );
    assert.match(stdout, /verify-only PASS 72\/72; 24 package entries/);
    await assertPackageByteIdentical(sourcePackage, tempPackage);
  } finally {
    await rm(tempRoot, { recursive: true, force: true });
  }
});

test("R0.74O regeneration keeps vector masters byte-exact and PNG pixels exact in isolation", async () => {
  const { tempRoot, sourcePackage, tempPackage } = await prepareIsolatedFigure("r074o-figure-regenerate-");
  try {
    const { stdout: plotStdout } = await execFileAsync(
      python,
      ["-B", resolve(tempPackage, "plot.py")],
      {
        cwd: tempPackage,
        env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
        maxBuffer: 30 * 1024 * 1024,
        timeout: 300_000,
      },
    );
    const regenerated = JSON.parse(plotStdout);
    assert.equal(regenerated.outputs.svg_sha256, figureFrozen.get("figure.svg"));
    assert.equal(regenerated.outputs.pdf_sha256, figureFrozen.get("figure.pdf"));
    assert.equal(regenerated.outputs.png_sha256, sha256(await readFile(resolve(tempPackage, "figure.png"))));
    assert.equal(regenerated.simulation, false);

    const { stdout: validationStdout } = await execFileAsync(
      python,
      ["-B", resolve(tempPackage, "validate.py")],
      {
        cwd: tempPackage,
        env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
        maxBuffer: 30 * 1024 * 1024,
        timeout: 300_000,
      },
    );
    assert.match(validationStdout, /verify-only PASS 72\/72; 24 package entries/);
    await assertCrossPlatformRegenerationEquivalent(sourcePackage, tempPackage);
  } finally {
    await rm(tempRoot, { recursive: true, force: true });
  }
});
