import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { access, lstat, readFile, readdir } from "node:fs/promises";
import { resolve, sep } from "node:path";
import test from "node:test";
import { pathToFileURL } from "node:url";

const root = process.env.R073Y_RELEASE_TEST_ROOT
  ? pathToFileURL(resolve(process.env.R073Y_RELEASE_TEST_ROOT) + sep)
  : new URL("../", import.meta.url);
const cwd = new URL(root).pathname;
const read = async (path) => readFile(new URL(path, root));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const figureId = "fig-r073y-exact-shear-obstruction";

const protectedHistorical = new Map([
  ["public/notes/r0-73x.html", "5e98103df24a01b690fca104938c65dec96ad00f7d40e2c9798e7dc859d6afcb"],
  ["public/notes/r0-73x.pdf", "0c1c97a754fe2c15310dff184c2d3ed142c40c53e400f5ba4895757808e267c7"],
  ["public/recap-r0-61-r0-73x.html", "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776"],
  ["public/recap-r0-61-r0-73x.pdf", "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa"],
  ["research/r073x_pdf_bindings.json", "e255810c20c13c8c90020847685048a1dde88bf513b33e7440bb7ccec5507f87"],
  ["research/r073x_recap_pdf_render.json", "a19ca701c402504e4e0b93d2ca442fdd665aa93219caa726d64f3f5ff3c00101"],
]);
const protectedRecapLedgerSha256 = "f76860a8a3d8f1b3cd83b98e566bc3ffd09461175c234dfffe35864f05b5d643";
const figureSourceCommit = "e37bf12cb5c2a8eb975e5097229dbc48fa597b35";
const figurePackageCommit = "05fdbc717a02be9f88fafc2b67a658e706b40be4";

function run(command, args) {
  const completed = spawnSync(command, args, {
    cwd,
    encoding: "utf8",
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.equal(completed.status, 0, completed.stderr || completed.stdout);
  return completed.stdout;
}

test("R0.73Y accounting separates published nodes from recap-covered nodes", async () => {
  const [manifest, site, archive, version] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text("public/site-version.json").then(JSON.parse),
    text("research/formal-archive-inventory.json").then(JSON.parse),
    text("VERSION"),
  ]);
  assert.equal(version, "1.65\n");
  assert.equal(manifest.latestCompletedRelease, "r073y");
  assert.equal(manifest.nextRelease, "r073z");
  assert.equal(manifest.siteVersion, "1.65");
  assert.equal(manifest.publicHtmlNoteCount, 201);
  assert.equal(manifest.postR060PublishedNodeCount, 141);
  assert.equal(manifest.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x");
  assert.equal(manifest.postR070APublishedReleaseCount, 103);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 79);
  assert.equal(manifest.legacyFormalFigureBacklogCount, 24);
  assert.equal(manifest.publicPdfNoteCount, 158);
  assert.equal(manifest.recapPolicy, "MILESTONE_ONLY");
  assert.match(manifest.completionRule, /recap is created only at a declared major milestone/);
  assert.equal(site.latestRelease, "R0.73Y");
  assert.equal(site.latestRecapRelease, "R0.73X");
  assert.equal(archive.publishedReleases.at(-1), "r073y");
  assert.equal(archive.formalSealedReleases.at(-1), "r073y");
  assert.equal(archive.publishedReleases.length, 103);
  assert.equal(archive.formalSealedReleases.length, 79);
});

test("R0.73X milestone note, recap, PDFs, and bindings stay byte-identical", async () => {
  for (const [path, digest] of protectedHistorical) {
    assert.equal(sha256(await read(path)), digest, path);
  }
  await assert.rejects(access(new URL("public/recap-r0-61-r0-73y.html", root)));
  await assert.rejects(access(new URL("public/recap-r0-61-r0-73y.pdf", root)));
  assert.deepEqual(
    (await readdir(new URL("research/", root))).filter((name) => /^r073y.*recap/i.test(name)),
    [],
    "R0.73Y is a note-only release and must not acquire recap metadata",
  );
  const recapPaths = (await readdir(new URL("public/", root)))
    .filter((name) => /^recap-[^/]+\.(?:html|pdf)$/.test(name))
    .map((name) => "public/" + name);
  recapPaths.push("research/r073x_pdf_bindings.json", "research/r073x_recap_pdf_render.json");
  recapPaths.sort();
  assert.equal(recapPaths.length, 154);
  const ledgerRows = [];
  for (const path of recapPaths) ledgerRows.push(`${sha256(await read(path))}  ${path}`);
  assert.equal(sha256(Buffer.from(ledgerRows.join("\n") + "\n")), protectedRecapLedgerSha256);
});

test("source dry-run and full in-memory release gate are read-only and fully pinned", async () => {
  const source = JSON.parse(run("python3", ["-B", "scripts/generate_r073y_release.py", "--source-dry-run"]));
  assert.equal(source.release, "R0.73Y");
  assert.equal(source.siteVersion, "1.65");
  assert.equal(source.commitPinsReady, true);
  assert.deepEqual(source.commitPinBlockers, []);
  assert.equal(source.recapGenerated, false);
  assert.equal(source.figureExpectedFileCount, 25);
  assert.equal(source.figureScopeLabel, "ANALYTIC_EXACT_WITNESS_NOT_DNS");
  assert.equal(source.protectedRecapAssetCount, 154);
  assert.equal(source.protectedRecapLedgerSha256, protectedRecapLedgerSha256);
  assert.equal(source.writes, 0);
  const check = JSON.parse(run("python3", ["-B", "scripts/generate_r073y_release.py", "--check-only"]));
  assert.equal(check.checkOnly, true);
  assert.equal(check.transaction, "IN_MEMORY_ONLY");
  assert.equal(check.recapGenerated, false);
  assert.equal(check.writes, 0);
});

test("public note and routes are current, bilingual, and honestly bounded", async () => {
  const [note, home, literature, index] = await Promise.all([
    text("public/notes/r0-73y.html"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    text("public/notes/index.html"),
  ]);
  for (const page of [note, home, literature, index]) {
    assert.ok(page.includes("/i18n-en.js?v=1.65"));
    assert.ok(page.includes("R0.73Y"));
    assert.ok(!page.includes("/recap-r0-61-r0-73y"));
  }
  for (const marker of [
    "NOT CLAY", "Vreman", "analytic exact witness", "not DNS",
    "productionOnlyCoercivity=REFUTED_FOR_ZERO_PRESERVING_FUNCTIONALS",
    "production 对所有实振幅为零",
    "gradient covariance：STRICTLY POSITIVE FOR A ≠ 0; ZERO FOR A = 0",
    "A = 0 时为平凡零场",
    figureId,
  ]) assert.ok(note.includes(marker), "note missing " + marker);
  assert.ok(!note.includes(",qquad"), "literal qquad token leaked into public note");
  assert.ok(!note.includes("**NOT CLAY.**"), "raw Markdown emphasis leaked into public note");
  assert.ok(note.includes("<strong>NOT CLAY.</strong>"));
  assert.ok(note.includes("<em>Proc. Amer. Math. Soc.</em>"));
  assert.ok(note.includes("\\begin{aligned}"), "A4-safe single-mode display is absent");
  assert.equal((home.match(/data-release="r073y"/g) ?? []).length, 1);
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, 201);
  assert.ok(index.includes("158"));
  assert.ok(literature.includes('id="r073y-boundary"'));
});

test("formal figure scientific payload is byte-identical and publication metadata is isolated", async () => {
  const source = `figures/r073y/${figureId}`;
  const research = `research/figures/r073y/${figureId}`;
  const published = `public/figures/r073y/${figureId}`;
  const names = (await readdir(new URL(source + "/", root))).sort();
  assert.equal(names.length, 25);
  for (const name of names) {
    const original = await read(source + "/" + name);
    const researchCopy = await read(research + "/" + name);
    const publicCopy = await read(published + "/" + name);
    assert.deepEqual(publicCopy, researchCopy, "research/public mirror " + name);
    if (!["manifest.json", "SHA256SUMS"].includes(name)) {
      assert.deepEqual(researchCopy, original, "scientific payload mirror " + name);
    }
  }
  const sourceManifest = JSON.parse(await text(source + "/manifest.json"));
  const publicationManifest = JSON.parse(await text(research + "/manifest.json"));
  assert.equal(sourceManifest.publicationStatus, "staged");
  assert.equal(publicationManifest.publicationStatus, "published");
  assert.equal(publicationManifest.sourcePublicationStatus, "staged");
  assert.equal(publicationManifest.publication.figureSourceCommit, figureSourceCommit);
  assert.equal(publicationManifest.publication.figurePackageCommit, figurePackageCommit);
  const normalizedSource = structuredClone(sourceManifest);
  const normalizedPublication = structuredClone(publicationManifest);
  delete normalizedSource.publicationStatus;
  delete normalizedPublication.publicationStatus;
  delete normalizedPublication.sourcePublicationStatus;
  delete normalizedPublication.publication;
  assert.deepEqual(normalizedPublication, normalizedSource);
  for (const suffix of ["pdf", "svg", "png"]) {
    assert.deepEqual(
      await read(`public/assets/r073y/${figureId}.${suffix}`),
      await read(`${source}/figure.${suffix}`),
    );
  }
  const png = await lstat(new URL(`${source}/figure.png`, root));
  assert.ok(png.size > 50_000);
});

test("translation is local-direct and excludes recap from the R0.73Y batch", async () => {
  const source = await text("scripts/add-r073y-translations.mjs");
  assert.ok(source.includes('const translationRoute = "LOCAL_DIRECT_NO_DGX"'));
  assert.ok(source.includes('"notes/r0-73y.html"'));
  assert.ok(!source.includes('"recap-r0-61-r0-73y.html"'));
  const result = JSON.parse(run(process.execPath, ["scripts/add-r073y-translations.mjs", "--check-only"]));
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.dgxUsed, false);
});

test("only the R0.73Y note PDF is newly bound", async () => {
  const binding = JSON.parse(await text("research/r073y_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r073y-synchronized-pdf-bindings-v1");
  assert.equal(binding.documents.length, 1);
  assert.equal(binding.documents[0].kind, "research-note");
  assert.equal(binding.documents[0].html.path, "public/notes/r0-73y.html");
  assert.equal(binding.documents[0].pdf.path, "public/notes/r0-73y.pdf");
  assert.equal(
    binding.canonicalCorrectionSource.path,
    "research/r073y_reader_quantifier_correction.md",
  );
  assert.equal(
    binding.canonicalCorrectionSource.typesettingNormalization,
    "EXACT_COUNTED_NONSEMANTIC_REPAIRS",
  );
  assert.equal(binding.canonicalCorrectionSource.zeroProduction, "ALL_REAL_A");
  assert.equal(binding.canonicalCorrectionSource.strictGradientCovariance, "ONLY_A_NE_0");
  assert.equal(binding.canonicalCorrectionSource.zeroAmplitudeGradientCovariance, 0);
  assert.equal(binding.claimBoundary.recapGenerated, false);
  assert.equal(binding.claimBoundary.latestRecapRelease, "R0.73X");
  assert.equal(binding.claimBoundary.figureScope, "ANALYTIC_EXACT_WITNESS_NOT_DNS");
  const result = JSON.parse(run(process.execPath, ["scripts/bind-r073y-pdfs.mjs", "--check-only"]));
  assert.equal(result.documents, 1);
});

test("workflow and manifest route to the R0.73Y gates", async () => {
  const [manifest, pages, publication] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text(".github/workflows/pages.yml"),
    text(".github/workflows/release-publication-gate.yml"),
  ]);
  assert.equal(manifest.latestReleaseGate, "tests/r073y-exact-shear-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r073y-release.test.mjs");
  assert.equal(manifest.latestReleaseTranslationScript, "scripts/add-r073y-translations.mjs");
  for (const workflow of [pages, publication]) {
    assert.ok(workflow.includes("scripts/run-release-publication-gate.mjs"));
    assert.ok(workflow.includes(`figures/r073y/${figureId}/requirements.txt`));
  }
});
