import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { lstat, readFile, readdir } from "node:fs/promises";
import { resolve, sep } from "node:path";
import test from "node:test";
import { pathToFileURL } from "node:url";

const root = process.env.R073Y_RELEASE_TEST_ROOT
  ? pathToFileURL(resolve(process.env.R073Y_RELEASE_TEST_ROOT) + sep)
  : new URL("../", import.meta.url);
const text = async (path) => (await readFile(new URL(path, root), "utf8"));
const bytes = async (path) => readFile(new URL(path, root));
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const sourceCommit = "1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66";
const figureSourceCommit = "e37bf12cb5c2a8eb975e5097229dbc48fa597b35";
const figurePackageCommit = "05fdbc717a02be9f88fafc2b67a658e706b40be4";
const figureId = "fig-r073y-exact-shear-obstruction";

function git(argumentsList, encoding = "utf8") {
  const completed = spawnSync("git", argumentsList, {
    cwd: new URL(root).pathname,
    encoding,
  });
  assert.equal(completed.status, 0, completed.stderr?.toString() || completed.stdout?.toString());
  return completed.stdout;
}

async function regular(path) {
  const info = await lstat(new URL(path, root));
  assert.equal(info.isSymbolicLink(), false, path + " must not be a symlink");
  assert.equal(info.isFile(), true, path + " must be a regular file");
}

async function snapshot(paths) {
  const rows = [];
  for (const path of paths.sort()) {
    const payload = await bytes(path);
    const info = await lstat(new URL(path, root));
    rows.push([path, payload.length, info.mtimeNs?.toString() ?? String(info.mtimeMs), sha256(payload)]);
  }
  return rows;
}

test("general orthogonal shear theorem is analytic, all-scale, and scope-limited", async () => {
  const theorem = await text("research/r073y_exact_shear_no_go.md");
  for (const marker of [
    "a\\cdot k=0",
    "\\Pi_s=\\mathscr S_s=Q_s=0",
    "D_{ii,s}",
    ">0",
    "|A|^3",
    "zero-preserving",
    "amplitude-independent universal bound",
  ]) assert.ok(theorem.includes(marker), "missing theorem marker: " + marker);
  assert.match(theorem, /does \*\*not\*\* refute a\s+regularity criterion/);
  assert.match(theorem, /strictly positive\s+periodic heat kernel/);
  assert.ok(!theorem.includes("strict positivity follows from samples"));
});

test("single-mode executable certificate is not conflated with the general theorem", async () => {
  const certificate = JSON.parse(await text("research/r073y_exact_shear_certificate.json"));
  assert.equal(certificate.claim_ledger.generalOrthogonalShearClass,
    "PROVED_ANALYTICALLY_NOT_CERTIFICATE_SCOPE");
  assert.equal(certificate.claim_ledger.productionOnlyCoerciveBridge,
    "FALSE_BY_EXACT_NSE_FAMILY");
  assert.equal(certificate.claim_ledger.arbitraryThreeDimensionalGlobalRegularity, "OPEN");
  assert.equal(certificate.claim_ledger.clayConclusion, "OPEN");
  assert.equal(certificate.not_clay, true);
  assert.ok(certificate.numerical_cross_checks.maximum_overall_scaled_error < 2e-10);
  assert.equal(certificate.claim_ledger.gradientCovarianceStrictlyPositiveForAneq0AndSgt0,
    "PROVED_ANALYTICALLY");
});

test("certificate check-only is portable and writes no tracked research/script input", async () => {
  const paths = [
    "scripts/r073y_exact_shear_certificate.py",
    "research/r073y_exact_shear_certificate.json",
    "research/r073y_exact_shear_certificate_report.md",
  ];
  const before = await snapshot(paths);
  const completed = spawnSync("python3", ["-B", "scripts/r073y_exact_shear_certificate.py", "--check-only"], {
    cwd: new URL(root).pathname,
    encoding: "utf8",
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.equal(completed.status, 0, completed.stderr || completed.stdout);
  assert.deepEqual(await snapshot(paths), before);
});

test("formal certificate inventory is derived and bound to the frozen research commit", async () => {
  const base = "research/certificates/r073y/";
  const names = (await readdir(new URL(base, root))).sort();
  assert.equal(names.length, 13);
  const manifest = JSON.parse(await text(base + "manifest.json"));
  const contract = JSON.parse(await text(base + "contract.json"));
  assert.equal(manifest.schema, "r073y-formal-certificate-manifest-v1");
  assert.equal(manifest.status, "SEALED");
  assert.equal(manifest.source.git_commit_sha1, sourceCommit);
  assert.deepEqual(manifest.inventory, {
    manifest_entry_count: 11,
    package_file_count: 13,
    sha256sums_entry_count: 12,
  });
  assert.equal(manifest.files.length, manifest.inventory.manifest_entry_count);
  assert.equal(contract.source.inputs.length, 8);
  assert.equal(contract.source.git_commit_sha1, sourceCommit);
  assert.equal(manifest.claim_boundary.not_clay, true);
  assert.equal(manifest.claim_boundary.clay_problem_solved, false);
});

test("literature collision and novelty boundary are explicit", async () => {
  const [audit, report] = await Promise.all([
    text("research/r073y_primary_literature_audit.md"),
    text("research/r073y_report-source.md"),
  ]);
  for (const marker of ["Vreman", "10.1063/1.1785131", "simple shear", "direct collision"])
    assert.ok((audit + report).includes(marker), "missing literature collision: " + marker);
  assert.ok(report.includes("不能申报为新发现"));
  assert.ok(report.includes("本节对整个 Clay 问题的直接推进很小"));
  assert.ok(report.includes("NOT CLAY"));
  assert.ok(!/first proof|首次证明|novel theorem|原创性定理/i.test(report));
});

test("reader correction preserves the frozen theorem and exposes the A=0 endpoint", async () => {
  const correction = await text("research/r073y_reader_quantifier_correction.md");
  const frozenReportDigest = sha256(await bytes("research/r073y_report-source.md"));
  assert.equal(frozenReportDigest, "d2f4df01b51ec613affc4b14a3544f6f702584de1ba1a94b2ec241e31d5efd01");
  assert.ok(correction.includes(`Frozen report SHA-256:** \`${frozenReportDigest}\``));
  for (const marker of [
    `Frozen source commit:** \`${sourceCommit}\``,
    "frozenReportBytesPreserved=true",
    "publicTransformation=EXACT_COUNTED_REPLACEMENTS",
    "zeroProduction=ALL_REAL_A",
    "strictGradientCovariance=ONLY_A_NE_0",
    "zeroAmplitudeGradientCovariance=0",
    "gradientCovarianceStrictlyPositiveForAneq0AndSgt0=PROVED_ANALYTICALLY",
    "recapPolicy=MILESTONE_ONLY",
    "latestPublishedRelease=r073y",
    "latestRecapRelease=r073x",
    "NOT CLAY",
  ]) assert.ok(correction.includes(marker), "missing reader-correction marker: " + marker);
});

test("formal figure is a 25-file analytic witness, not simulation or DNS", async () => {
  const base = `figures/r073y/${figureId}/`;
  const names = (await readdir(new URL(base, root))).sort();
  assert.equal(names.length, 25);
  for (const required of ["figure.pdf", "figure.svg", "figure.png", "source-data.csv", "manifest.json", "validation.json"])
    assert.ok(names.includes(required), "missing figure file: " + required);
  const [manifest, contract, validation, caption] = await Promise.all([
    text(base + "manifest.json").then(JSON.parse),
    text(base + "contract.json").then(JSON.parse),
    text(base + "validation.json").then(JSON.parse),
    text(base + "caption.md"),
  ]);
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.release, "R0.73Y");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.computation.kind, "exact-formula-audit");
  assert.equal(manifest.compute.dgxUsed, false);
  assert.equal(manifest.git.sourceEvidenceCommit, sourceCommit);
  assert.equal(manifest.seal.figureSourceCommit, figureSourceCommit);
  assert.equal(manifest.seal.figureSourceCommitBound, true);
  assert.equal(manifest.seal.figureSourceBindings.length, 21);
  assert.equal(contract.sourceAuthority.commit, sourceCommit);
  assert.equal(contract.claimBoundary.analyticExactWitness, true);
  assert.equal(contract.claimBoundary.navierStokesSimulation, false);
  assert.equal(contract.claimBoundary.dns, false);
  assert.equal(contract.claimBoundary.notClay, true);
  assert.equal(contract.claimBoundary.strictGradientCovarianceRequiresNonzeroAmplitude, true);
  assert.equal(contract.claimBoundary.zeroAmplitudeMemberCovariance, "zero");
  assert.equal(validation.schemaVersion, "r073y-exact-shear-validation-v3");
  assert.equal(validation.status, "PASS");
  assert.equal(validation.sealState, "formal-figure-source-seal");
  assert.match(caption, /analytic exact-?shear witness/i);
  assert.match(caption, /not (?:a )?(?:direct numerical simulation|simulation|DNS)/i);

  assert.equal(git(["merge-base", "--is-ancestor", figureSourceCommit, figurePackageCommit]), "");
  const committedPaths = git([
    "ls-tree", "-r", "--name-only", figurePackageCommit, "--", base.slice(0, -1),
  ]).trim().split("\n");
  assert.equal(committedPaths.length, 25);
  for (const path of committedPaths) {
    assert.deepEqual(git(["show", `${figurePackageCommit}:${path}`], null), await bytes(path));
  }
});

test("release sources hard-code note-only recap separation", async () => {
  const [content, generator, binder, translation] = await Promise.all([
    text("scripts/r073y_release_content.py"),
    text("scripts/generate_r073y_release.py"),
    text("scripts/bind-r073y-pdfs.mjs"),
    text("scripts/add-r073y-translations.mjs"),
  ]);
  for (const value of [content, binder]) {
    assert.ok(value.includes("fig-r073y-exact-shear-obstruction"));
    assert.ok(value.includes("NOT CLAY"));
  }
  assert.ok(generator.includes("FIGURE_ID"));
  assert.ok(generator.includes("FIGURE_SOURCE_RELATIVE"));
  assert.ok(generator.includes("NOT CLAY"));
  assert.ok(generator.includes('"postR060PublishedNodeCount": 141'));
  assert.ok(generator.includes('"postR060RecapNodeCount": 140'));
  assert.ok(generator.includes('"latestRecapRelease": "r073x"'));
  for (const source of [generator, binder, translation]) {
    assert.ok(source.includes("research/r073y_reader_quantifier_correction.md"));
  }
  const ledgerSource = content.match(
    /EXPECTED_MACHINE_LEDGER = \(([\s\S]*?)\)\nREQUIRED_LEDGER_MARKERS/,
  );
  assert.ok(ledgerSource, "reader-content machine-ledger declaration");
  const machineLedger = [...ledgerSource[1].matchAll(/"([^"]+)"/g)].map((match) => match[1]);
  assert.equal(machineLedger.length, 25);
  for (const source of [binder, translation]) {
    for (const token of machineLedger) assert.ok(source.includes(token), token);
  }
  assert.ok(!translation.includes('"recap-r0-61-r0-73y.html"'));
  assert.ok(!binder.includes('html: "public/recap-r0-61-r0-73y.html"'));
});
