import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

function run(command, arguments_) {
  const completed = spawnSync(command, arguments_, { cwd: root, encoding: "utf8" });
  assert.equal(completed.status, 0, completed.stderr || completed.stdout);
  return completed.stdout;
}

test("R0.74A publication accounting advances only the note endpoint", async () => {
  const [manifest, site, inventory, version] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text("public/site-version.json").then(JSON.parse),
    text("research/formal-archive-inventory.json").then(JSON.parse),
    text("VERSION"),
  ]);
  assert.equal(version, "1.67\n");
  assert.equal(manifest.latestCompletedRelease, "r074a");
  assert.equal(manifest.nextRelease, "r074b");
  assert.equal(manifest.siteVersion, "1.67");
  assert.equal(manifest.publicHtmlNoteCount, 203);
  assert.equal(manifest.publicPdfNoteCount, 160);
  assert.equal(manifest.postR060PublishedNodeCount, 143);
  assert.equal(manifest.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x");
  assert.equal(site.latestRelease, "R0.74A");
  assert.equal(site.latestRecapRelease, "R0.73X");
  assert.equal(inventory.publishedReleases.at(-1), "r074a");
  assert.equal(inventory.formalSealedReleases.at(-1), "r074a");
  assert.equal(inventory.publishedReleaseCount, 105);
  assert.equal(inventory.formalSealedReleaseCount, 81);
});

test("R0.73X recap is byte-preserved and no R0.74A recap exists", async () => {
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74a.html")));
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74a.pdf")));
  assert.deepEqual((await readdir(resolve(root, "research"))).filter((name) => /^r074a.*recap/i.test(name)), []);
});

test("note, homepage, literature review, and index expose honest boundaries", async () => {
  const [note, home, literature, index] = await Promise.all([
    text("public/notes/r0-74a.html"), text("public/research-review.html"),
    text("public/literature-review.html"), text("public/notes/index.html"),
  ]);
  for (const marker of ["PROVED", "FINITE", "OPEN", "NOT CLAY", "LOCAL DIRECT / NO DGX", "positiveFourBlockMajorization", "tailSmallnessOrAbsorption"])
    assert.ok(note.includes(marker), marker);
  assert.ok(note.includes('inlineMath:[["\\\\(","\\\\)"]]'));
  assert.ok(note.includes('displayMath:[["\\\\[","\\\\]"]]'));
  assert.equal((home.match(/data-release="r074a"/g) ?? []).length, 1);
  assert.ok(home.includes("NEXT · R0.74B"));
  assert.ok(home.includes("203 篇研究笔记总索引"));
  assert.ok(literature.includes('id="r074a-boundary"'));
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, 203);
  assert.ok(index.includes('href="/notes/r0-74a.pdf"'));
  assert.ok(!home.includes("/recap-r0-61-r0-74a"));
});

test("publication archive is compatible while public evidence and assets stay frozen", async () => {
  const base = "research/figures/r074a/fig-r074a-localized-kd-payments";
  const publicMirror = "public/figures/r074a/fig-r074a-localized-kd-payments";
  for (const name of await readdir(resolve(root, base))) {
    assert.deepEqual(await read(`${publicMirror}/${name}`), await read(`${base}/${name}`), `${publicMirror}/${name}`);
  }
  const archive = "figures/r074a/fig-r074a-localized-kd-payments";
  const archivedManifest = JSON.parse((await read(`${archive}/manifest.json`)).toString("utf8"));
  assert.equal(archivedManifest.publicationStatus, "published");
  assert.equal(archivedManifest.provenance.compatibilityScope, "publication archive metadata only; scientific files and public masters are unchanged");
  assert.deepEqual(await read(`${archive}/plot.py`), await read(`${base}/producer.py`));
  for (const extension of ["pdf", "png", "svg"]) {
    assert.deepEqual(
      await read(`public/assets/r074a/fig-r074a-localized-kd-payments.${extension}`),
      await read(`${base}/figure.${extension}`),
    );
  }
});

test("local translation and synchronized PDF binding check read-only", () => {
  const translation = JSON.parse(run(process.execPath, ["scripts/add-r074a-translations.mjs", "--check-only"]));
  assert.equal(translation.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(translation.dgxUsed, false);
  const binding = JSON.parse(run(process.execPath, ["scripts/bind-r074a-pdfs.mjs", "--check-only"]));
  assert.ok(binding.pageCount >= 1);
  assert.equal(binding.translationPath, "LOCAL_DIRECT_NO_DGX");
});
