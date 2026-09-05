import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

import {
  GLOBAL_INVARIANT,
  RETAINED_GLOBAL_TESTS,
  resolveReleasePublicationGate,
  runResolvedReleasePublicationGate,
} from "../scripts/run-release-publication-gate.mjs";

const root = resolve(import.meta.dirname, "..");

async function fixture(overrides = {}) {
  const directory = await mkdtemp(join(tmpdir(), "release-publication-gate-"));
  await Promise.all([
    mkdir(join(directory, "research"), { recursive: true }),
    mkdir(join(directory, "tests"), { recursive: true }),
    mkdir(join(directory, "scripts"), { recursive: true }),
  ]);
  const manifest = {
    schemaVersion: "research-release-manifest-v1",
    latestCompletedRelease: "r072p",
    latestReleaseGate: "tests/r072p-superposition-gate.test.mjs",
    latestReleasePublicationTest: "tests/r072p-release.test.mjs",
    ...overrides,
  };
  await writeFile(
    join(directory, "research/release-manifest.json"),
    JSON.stringify(manifest),
  );
  for (const name of [
    GLOBAL_INVARIANT,
    "tests/r072p-superposition-gate.test.mjs",
    "tests/r072p-release.test.mjs",
    ...RETAINED_GLOBAL_TESTS,
  ]) {
    await writeFile(join(directory, name), "// fixture\n");
  }
  await writeFile(
    join(directory, "scripts/add-r072p-translations.mjs"),
    'if (process.argv.includes("--check-only")) process.exitCode = 0;\n',
  );
  return directory;
}

test("resolves the merged endpoint to release-owned, regular repository files", async () => {
  const manifest = JSON.parse(
    await readFile(resolve(root, "research/release-manifest.json"), "utf8"),
  );
  const gate = await resolveReleasePublicationGate(root);
  const publication = manifest.latestPublication;
  const release = publication?.releaseId ?? manifest.latestCompletedRelease;
  assert.deepEqual(
    {
      release: gate.release,
      invariant: gate.invariant,
      gate: gate.gate,
      publication: gate.publication,
      translation: gate.translation,
    },
    {
      release,
      invariant: "tests/release-publication-invariant.test.mjs",
      gate: publication?.gate ?? manifest.latestReleaseGate,
      publication: publication?.publicationTest ?? manifest.latestReleasePublicationTest,
      translation: `scripts/add-${release}-translations.mjs`,
    },
  );
});

test("runs the fail-closed stages in the declared order", async () => {
  const manifest = JSON.parse(
    await readFile(resolve(root, "research/release-manifest.json"), "utf8"),
  );
  const gate = await resolveReleasePublicationGate(root);
  const publication = manifest.latestPublication;
  const release = publication?.releaseId ?? manifest.latestCompletedRelease;
  const calls = [];
  runResolvedReleasePublicationGate(gate, (directory, label, arguments_) => {
    calls.push({ directory, label, arguments_ });
  });
  assert.deepEqual(
    calls.map(({ arguments_ }) => arguments_),
    [
      ["--test", "tests/release-publication-invariant.test.mjs"],
      ["--test", publication?.gate ?? manifest.latestReleaseGate],
      ["--test", publication?.publicationTest ?? manifest.latestReleasePublicationTest],
      [`scripts/add-${release}-translations.mjs`, "--check-only"],
      ...RETAINED_GLOBAL_TESTS.map((testPath) => ["--test", testPath]),
    ],
  );
  assert.ok(calls.every(({ directory }) => directory === root));
});

test("supports an independently named publication without advancing the R0 endpoint", async () => {
  const latestPublication = {
    releaseId: "clay-b-two-scale-20260905",
    gate: "tests/clay-b-two-scale-20260905-gate.test.mjs",
    publicationTest: "tests/clay-b-two-scale-20260905-release.test.mjs",
    translationScript: "scripts/add-clay-b-two-scale-20260905-translations.mjs",
  };
  const directory = await fixture({ latestPublication });
  try {
    await Promise.all([
      writeFile(join(directory, latestPublication.gate), "// fixture\n"),
      writeFile(join(directory, latestPublication.publicationTest), "// fixture\n"),
      writeFile(
        join(directory, latestPublication.translationScript),
        'if (process.argv.includes("--check-only")) process.exitCode = 0;\n',
      ),
    ]);
    const gate = await resolveReleasePublicationGate(directory);
    assert.equal(gate.release, latestPublication.releaseId);
    assert.equal(gate.gate, latestPublication.gate);
    assert.equal(gate.publication, latestPublication.publicationTest);
    assert.equal(gate.translation, latestPublication.translationScript);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("rejects traversal and release-mismatched manifest pointers", async (context) => {
  for (const [name, overrides, pattern] of [
    [
      "traversal",
      { latestReleaseGate: "tests/../r072p-superposition-gate.test.mjs" },
      /not a normalized repository path|unsafe path segment/,
    ],
    [
      "absolute",
      { latestReleaseGate: "/tmp/r072p-superposition-gate.test.mjs" },
      /repository-relative/,
    ],
    [
      "other release",
      { latestReleaseGate: "tests/r072o-physical-reinsertion-gate.test.mjs" },
      /does not belong to r072p/,
    ],
    [
      "gate reused as publication test",
      {
        latestReleasePublicationTest:
          "tests/r072p-superposition-gate.test.mjs",
      },
      /not a distinct r072p publication test/,
    ],
    [
      "translation override",
      {
        latestReleaseTranslationScript:
          "scripts/add-r072o-translations.mjs",
      },
      /must equal the release-derived path/,
    ],
  ]) {
    await context.test(name, async () => {
      const directory = await fixture(overrides);
      try {
        await assert.rejects(resolveReleasePublicationGate(directory), pattern);
      } finally {
        await rm(directory, { recursive: true, force: true });
      }
    });
  }
});

test("rejects a missing derived translation checker", async () => {
  const directory = await fixture();
  try {
    await rm(join(directory, "scripts/add-r072p-translations.mjs"));
    await assert.rejects(
      resolveReleasePublicationGate(directory),
      /latest release translation script does not exist/,
    );
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("PR and Pages workflows invoke the same publication runner", async () => {
  const [pullRequest, pages] = await Promise.all([
    readFile(resolve(root, ".github/workflows/release-publication-gate.yml"), "utf8"),
    readFile(resolve(root, ".github/workflows/pages.yml"), "utf8"),
  ]);
  assert.match(pullRequest, /pull_request:/);
  for (const workflow of [pullRequest, pages]) {
    assert.match(
      workflow,
      /uses: actions\/checkout@v6\s+with:\s+fetch-depth: 0/,
    );
    assert.match(workflow, /actions\/setup-node@v4/);
    assert.match(workflow, /node-version: "22\.13\.0"/);
    assert.match(workflow, /node scripts\/run-release-publication-gate\.mjs/);
  }
  assert.doesNotMatch(pages, /latest_gate=|latest_publication_test=/);
});
