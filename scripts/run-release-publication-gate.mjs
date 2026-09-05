#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { lstat, readFile, realpath } from "node:fs/promises";
import { dirname, isAbsolute, relative, resolve, sep, posix } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const scriptDirectory = dirname(fileURLToPath(import.meta.url));
const defaultRoot = resolve(scriptDirectory, "..");

export const GLOBAL_INVARIANT =
  "tests/release-publication-invariant.test.mjs";
export const RETAINED_GLOBAL_TESTS = [
  "tests/site-route-current-boundary.test.mjs",
  "tests/internal-public-links.test.mjs",
  "tests/bilingual-content.test.mjs",
  "tests/release-publication-gate-runner.test.mjs",
];

function fail(message) {
  throw new Error(`release publication gate: ${message}`);
}

function requireSafeRelativePath(value, label) {
  if (typeof value !== "string" || value.length === 0) {
    fail(`${label} must be a nonempty string`);
  }
  if (/\p{Cc}/u.test(value)) fail(`${label} contains a control character`);
  if (value.includes("\\")) fail(`${label} must use repository POSIX paths`);
  if (isAbsolute(value) || value.startsWith("/")) {
    fail(`${label} must be repository-relative`);
  }
  if (value !== posix.normalize(value)) {
    fail(`${label} is not a normalized repository path`);
  }
  const parts = value.split("/");
  if (parts.some((part) => part === "" || part === "." || part === "..")) {
    fail(`${label} contains an unsafe path segment`);
  }
  return value;
}

function requireContainedPath(parent, target, label) {
  const child = relative(parent, target);
  if (
    child === "" ||
    child === ".." ||
    child.startsWith(`..${sep}`) ||
    isAbsolute(child)
  ) {
    fail(`${label} escapes its allowed directory`);
  }
}

async function requireRegularRepositoryFile(root, repositoryPath, allowedDirectory, label) {
  requireSafeRelativePath(repositoryPath, label);
  const repositoryRoot = resolve(root);
  const allowedRoot = resolve(repositoryRoot, allowedDirectory);
  const target = resolve(repositoryRoot, repositoryPath);
  requireContainedPath(allowedRoot, target, label);

  let metadata;
  try {
    metadata = await lstat(target);
  } catch (error) {
    fail(`${label} does not exist: ${repositoryPath} (${error.code ?? error.message})`);
  }
  if (metadata.isSymbolicLink() || !metadata.isFile()) {
    fail(`${label} must be a regular non-symlink file: ${repositoryPath}`);
  }

  const [canonicalRoot, canonicalAllowed, canonicalTarget] = await Promise.all([
    realpath(repositoryRoot),
    realpath(allowedRoot),
    realpath(target),
  ]);
  requireContainedPath(canonicalRoot, canonicalTarget, label);
  requireContainedPath(canonicalAllowed, canonicalTarget, label);
  return repositoryPath;
}

function escapeRegularExpression(value) {
  return value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
}

export async function resolveReleasePublicationGate(root = defaultRoot) {
  const repositoryRoot = resolve(root);
  const manifestPath = resolve(repositoryRoot, "research/release-manifest.json");
  let manifest;
  try {
    manifest = JSON.parse(await readFile(manifestPath, "utf8"));
  } catch (error) {
    fail(`cannot read research/release-manifest.json (${error.message})`);
  }
  if (manifest.schemaVersion !== "research-release-manifest-v1") {
    fail("unsupported release manifest schema");
  }

  const independent = manifest.latestPublication;
  if (
    independent !== undefined &&
    (independent === null || typeof independent !== "object" || Array.isArray(independent))
  ) {
    fail("latestPublication must be an object when present");
  }
  const release = independent?.releaseId ?? manifest.latestCompletedRelease;
  const releaseLabel = independent ? "latestPublication.releaseId" : "latestCompletedRelease";
  const releasePattern = independent
    ? /^[a-z0-9]+(?:-[a-z0-9]+)*$/
    : /^r0\d{2}[a-z]$/;
  if (typeof release !== "string" || !releasePattern.test(release)) {
    fail(`${releaseLabel} is not a valid release id`);
  }
  const escapedRelease = escapeRegularExpression(release);
  const gatePattern = new RegExp(
    `^tests/${escapedRelease}(?:-[a-z0-9]+)*-gate\\.test\\.mjs$`,
  );
  const publicationPattern = new RegExp(
    `^tests/${escapedRelease}(?:-[a-z0-9]+)*\\.test\\.mjs$`,
  );

  const gateLabel = independent ? "latestPublication.gate" : "latestReleaseGate";
  const publicationLabel = independent
    ? "latestPublication.publicationTest"
    : "latestReleasePublicationTest";
  const translationLabel = independent
    ? "latestPublication.translationScript"
    : "latestReleaseTranslationScript";
  const gate = requireSafeRelativePath(
    independent?.gate ?? manifest.latestReleaseGate,
    gateLabel,
  );
  if (!gatePattern.test(gate)) {
    fail(`latestReleaseGate does not belong to ${release}: ${gate}`);
  }
  const publication = requireSafeRelativePath(
    independent?.publicationTest ?? manifest.latestReleasePublicationTest,
    publicationLabel,
  );
  if (
    !publicationPattern.test(publication) ||
    publication.endsWith("-gate.test.mjs") ||
    publication === gate
  ) {
    fail(
      `latestReleasePublicationTest is not a distinct ${release} publication test: ${publication}`,
    );
  }

  const derivedTranslation = `scripts/add-${release}-translations.mjs`;
  const translation = requireSafeRelativePath(
    independent?.translationScript ?? manifest.latestReleaseTranslationScript ?? derivedTranslation,
    translationLabel,
  );
  if (translation !== derivedTranslation) {
    fail(
      `latestReleaseTranslationScript must equal the release-derived path ${derivedTranslation}`,
    );
  }

  await requireRegularRepositoryFile(
    repositoryRoot,
    GLOBAL_INVARIANT,
    "tests",
    "global release-publication invariant",
  );
  await requireRegularRepositoryFile(
    repositoryRoot,
    gate,
    "tests",
    "latest release gate",
  );
  await requireRegularRepositoryFile(
    repositoryRoot,
    publication,
    "tests",
    "latest release publication test",
  );
  await requireRegularRepositoryFile(
    repositoryRoot,
    translation,
    "scripts",
    "latest release translation script",
  );
  for (const testPath of RETAINED_GLOBAL_TESTS) {
    await requireRegularRepositoryFile(
      repositoryRoot,
      testPath,
      "tests",
      `retained global test ${testPath}`,
    );
  }

  const translationSource = await readFile(resolve(repositoryRoot, translation), "utf8");
  if (!translationSource.includes("--check-only")) {
    fail(`${translation} does not implement the required --check-only mode`);
  }

  return {
    root: repositoryRoot,
    release,
    invariant: GLOBAL_INVARIANT,
    gate,
    publication,
    translation,
    retainedGlobalTests: [...RETAINED_GLOBAL_TESTS],
  };
}

function executeNode(root, label, arguments_) {
  process.stdout.write(`\n[release-gate] ${label}\n`);
  const completed = spawnSync(process.execPath, arguments_, {
    cwd: root,
    env: process.env,
    stdio: "inherit",
  });
  if (completed.error) fail(`${label} could not start (${completed.error.message})`);
  if (completed.status !== 0) {
    fail(`${label} failed with exit status ${completed.status ?? "unknown"}`);
  }
}

export function runResolvedReleasePublicationGate(
  resolvedGate,
  executor = executeNode,
) {
  const run = (label, arguments_) =>
    executor(resolvedGate.root, label, arguments_);

  run("global release-publication invariant", [
    "--test",
    resolvedGate.invariant,
  ]);
  run(`latest mathematical gate (${resolvedGate.release})`, [
    "--test",
    resolvedGate.gate,
  ]);
  run(`latest publication test (${resolvedGate.release})`, [
    "--test",
    resolvedGate.publication,
  ]);
  run(`latest translation snapshot (${resolvedGate.release})`, [
    resolvedGate.translation,
    "--check-only",
  ]);
  for (const testPath of resolvedGate.retainedGlobalTests) {
    run(`retained global test (${testPath})`, ["--test", testPath]);
  }
}

export async function main() {
  const resolvedGate = await resolveReleasePublicationGate();
  process.stdout.write(
    `[release-gate] resolved ${JSON.stringify({
      release: resolvedGate.release,
      invariant: resolvedGate.invariant,
      gate: resolvedGate.gate,
      publication: resolvedGate.publication,
      translation: resolvedGate.translation,
    })}\n`,
  );
  runResolvedReleasePublicationGate(resolvedGate);
  process.stdout.write(`\n[release-gate] PASS ${resolvedGate.release}\n`);
}

const invokedDirectly =
  process.argv[1] &&
  pathToFileURL(resolve(process.argv[1])).href === import.meta.url;
if (invokedDirectly) {
  main().catch((error) => {
    process.stderr.write(`${error.stack ?? error.message}\n`);
    process.exitCode = 1;
  });
}
