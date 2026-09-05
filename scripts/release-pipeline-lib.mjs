#!/usr/bin/env node

import { createHash } from "node:crypto";
import { spawn, spawnSync } from "node:child_process";
import {
  lstat,
  mkdir,
  readFile,
  readdir,
  realpath,
  rename,
  writeFile,
} from "node:fs/promises";
import { dirname, isAbsolute, posix, relative, resolve, sep } from "node:path";

import { resolveReleasePublicationGate } from "./run-release-publication-gate.mjs";
import { loadPublicationQaConfig } from "./publication-qa-lib.mjs";

export const STAGES = Object.freeze([
  "intake",
  "generate",
  "translate",
  "bind",
  "gate",
  "commit",
  "push",
  "deploy",
  "qa",
]);

export const STATE_AFTER_STAGE = Object.freeze({
  intake: "INTAKE_VALIDATED",
  generate: "CONTENT_GENERATED",
  translate: "TRANSLATION_VALIDATED",
  bind: "PDF_BOUND",
  gate: "AUDIT_PASSED",
  commit: "COMMIT_CONFIRMED",
  push: "PUSH_CONFIRMED",
  deploy: "DEPLOYMENT_CONFIRMED",
  qa: "LIVE_QA_PASSED",
});

const REQUIRED_BOUNDARIES = Object.freeze(["PROVED", "FINITE", "OPEN", "NOT CLAY"]);
const CORE_LIVE_ROLES = Object.freeze(["homepage", "note-html", "note-index", "site-version"]);
const PDF_LIVE_ROLES = Object.freeze(["note-pdf"]);
const FIGURE_LIVE_ROLES = Object.freeze(["figure-pdf", "figure-svg", "figure-png"]);
const CACHEABLE_STAGES = new Set(["intake", "generate", "translate", "bind", "gate"]);
const RUNTIME_SCHEMA = "research-publication-runtime-v1";
export const DETERMINISTIC_RUNTIME_INPUTS = Object.freeze([
  "package.json",
  "pnpm-lock.yaml",
  "scripts/release-pipeline-lib.mjs",
  "scripts/run-release-publication-gate.mjs",
]);

function releaseFileStem(releaseId) {
  return releaseId.replace(/([a-z0-9])([A-Z])/g, "$1-$2").toLowerCase();
}

function isSupportedReleaseId(releaseId) {
  return /^r0\d{2}[a-z]$/.test(releaseId) ||
    /^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d{8}$/.test(releaseId);
}

function artifactPolicy(contract) {
  return contract.artifactPolicy ?? { readerPdf: "REQUIRED", scientificFigure: "REQUIRED" };
}

export function stateAfterStage(contract, name) {
  if (name === "bind" && artifactPolicy(contract).readerPdf === "OMIT_NEW") {
    return "HTML_ARTIFACTS_BOUND";
  }
  return STATE_AFTER_STAGE[name];
}

export function isStageCacheable(name) {
  return CACHEABLE_STAGES.has(name);
}

export function canReuseStage(name, { noCache, cachedFingerprint, fingerprint, outputsMatch }) {
  return isStageCacheable(name) && !noCache && cachedFingerprint === fingerprint && outputsMatch;
}

export function recordSuccessfulStage(state, contract, name, stageReceipt) {
  state.currentState = stateAfterStage(contract, name);
  state.stages[name] = stageReceipt;
  if (state.failedStage === name) delete state.failedStage;
  return state;
}

function requiredLiveRoles(contract) {
  const policy = artifactPolicy(contract);
  return [
    ...CORE_LIVE_ROLES,
    ...(policy.readerPdf === "REQUIRED" ? PDF_LIVE_ROLES : []),
    ...(policy.scientificFigure === "REQUIRED" ? FIGURE_LIVE_ROLES : []),
  ];
}

export class ReleasePipelineError extends Error {
  constructor(stage, failures) {
    const normalized = failures.map((failure) => ({
      label: failure.label ?? stage,
      message: failure.message ?? String(failure),
      stdout: failure.stdout ?? "",
      stderr: failure.stderr ?? "",
    }));
    super(
      `${stage} found ${normalized.length} error(s):\n` +
        normalized
          .map((failure, index) => `${index + 1}. ${failure.label}: ${failure.message}`)
          .join("\n"),
    );
    this.name = "ReleasePipelineError";
    this.stage = stage;
    this.failures = normalized;
  }
}

function fail(label, message) {
  throw new ReleasePipelineError(label, [{ label, message }]);
}

function isObject(value) {
  return value !== null && typeof value === "object" && !Array.isArray(value);
}

export function requireSafeRelativePath(value, label) {
  if (typeof value !== "string" || value.length === 0) {
    fail("contract", `${label} must be a nonempty string`);
  }
  if (/\p{Cc}/u.test(value) || value.includes("\\") || value.includes(":")) {
    fail("contract", `${label} contains an unsafe character`);
  }
  if (isAbsolute(value) || value.startsWith("/") || value !== posix.normalize(value)) {
    fail("contract", `${label} must be a normalized repository-relative POSIX path`);
  }
  if (value.split("/").some((part) => part === "" || part === "." || part === "..")) {
    fail("contract", `${label} contains an unsafe path segment`);
  }
  return value;
}

function requireSha256(value, label) {
  if (typeof value !== "string" || !/^[0-9a-f]{64}$/.test(value)) {
    fail("contract", `${label} must be a lowercase SHA-256 digest`);
  }
  return value;
}

function requireCommit(value, label) {
  if (typeof value !== "string" || !/^[0-9a-f]{40}$/.test(value)) {
    fail("contract", `${label} must be a full lowercase Git SHA-1 commit`);
  }
  return value;
}

function requireStringArray(value, label, { nonempty = true } = {}) {
  if (!Array.isArray(value) || (nonempty && value.length === 0)) {
    fail("contract", `${label} must be ${nonempty ? "a nonempty" : "an"} array`);
  }
  const result = value.map((entry, index) => {
    if (typeof entry !== "string" || entry.length === 0) {
      fail("contract", `${label}[${index}] must be a nonempty string`);
    }
    return entry;
  });
  if (new Set(result).size !== result.length) {
    fail("contract", `${label} contains duplicates`);
  }
  return result;
}

function resolveContained(root, repositoryPath, label) {
  requireSafeRelativePath(repositoryPath, label);
  const target = resolve(root, repositoryPath);
  const child = relative(resolve(root), target);
  if (child === "" || child === ".." || child.startsWith(`..${sep}`) || isAbsolute(child)) {
    fail("contract", `${label} escapes the repository`);
  }
  return target;
}

export function sha256Bytes(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

export async function sha256File(path) {
  return sha256Bytes(await readFile(path));
}

function git(root, arguments_, options = {}) {
  const result = spawnSync("git", arguments_, {
    cwd: root,
    encoding: options.binary ? null : "utf8",
    maxBuffer: 512 * 1024 * 1024,
  });
  if (result.error || result.status !== 0) {
    const detail = result.error?.message ?? String(result.stderr ?? "").trim();
    throw new Error(`git ${arguments_.join(" ")} failed: ${detail}`);
  }
  return options.binary ? result.stdout : result.stdout.trim();
}

function validateStage(contract, name, expectedScript, runner) {
  const stage = contract.stages?.[name];
  if (!isObject(stage)) fail("contract", `stages.${name} is required`);
  if (stage.runner !== runner) {
    fail("contract", `stages.${name}.runner must be ${runner}`);
  }
  if (stage.script !== expectedScript) {
    fail("contract", `stages.${name}.script must be ${expectedScript}`);
  }
  requireSafeRelativePath(stage.script, `stages.${name}.script`);
  stage.inputs = requireStringArray(stage.inputs, `stages.${name}.inputs`, { nonempty: false })
    .map((value, index) => requireSafeRelativePath(value, `stages.${name}.inputs[${index}]`));
  stage.outputs = requireStringArray(stage.outputs, `stages.${name}.outputs`)
    .map((value, index) => requireSafeRelativePath(value, `stages.${name}.outputs[${index}]`));
  return stage;
}

export function validateHandoff(contract) {
  if (!isObject(contract)) fail("contract", "handoff must be a JSON object");
  if (contract.schemaVersion !== "research-publication-handoff-v1") {
    fail("contract", "unsupported handoff schemaVersion");
  }
  if (typeof contract.releaseId !== "string" || !isSupportedReleaseId(contract.releaseId)) {
    fail("contract", "releaseId must match r0NNx or a dated independent release id");
  }
  requireCommit(contract.frozenCommit, "frozenCommit");
  if (contract.sourceRepository !== undefined &&
      (typeof contract.sourceRepository !== "string" ||
       !/^[A-Za-z0-9_.-]+$/.test(contract.sourceRepository))) {
    fail("contract", "sourceRepository must name one sibling repository without path separators");
  }
  if (contract.translationRoute !== "LOCAL_DIRECT_NO_DGX") {
    fail("contract", "translationRoute must be LOCAL_DIRECT_NO_DGX");
  }

  if (!Array.isArray(contract.artifacts) || contract.artifacts.length === 0) {
    fail("contract", "artifacts must be a nonempty array");
  }
  const artifactPaths = new Set();
  for (const [index, artifact] of contract.artifacts.entries()) {
    if (!isObject(artifact)) fail("contract", `artifacts[${index}] must be an object`);
    requireSafeRelativePath(artifact.path, `artifacts[${index}].path`);
    requireSha256(artifact.sha256, `artifacts[${index}].sha256`);
    if (artifact.commit !== undefined) {
      requireCommit(artifact.commit, `artifacts[${index}].commit`);
    }
    if (typeof artifact.role !== "string" || artifact.role.length === 0) {
      fail("contract", `artifacts[${index}].role must be a nonempty string`);
    }
    if (artifactPaths.has(artifact.path)) fail("contract", `duplicate artifact ${artifact.path}`);
    artifactPaths.add(artifact.path);
  }

  if (!isObject(contract.claimBoundary)) fail("contract", "claimBoundary is required");
  const labels = requireStringArray(contract.claimBoundary.requiredLabels, "claimBoundary.requiredLabels");
  for (const required of REQUIRED_BOUNDARIES) {
    if (!labels.includes(required)) fail("contract", `claimBoundary omits ${required}`);
  }
  contract.claimBoundary.publicFiles = requireStringArray(
    contract.claimBoundary.publicFiles,
    "claimBoundary.publicFiles",
  ).map((value, index) => requireSafeRelativePath(value, `claimBoundary.publicFiles[${index}]`));

  if (!isObject(contract.recap) || !["PRESERVE", "UPDATE"].includes(contract.recap.mode)) {
    fail("contract", "recap.mode must be PRESERVE or UPDATE");
  }
  if (typeof contract.recap.latestRecapRelease !== "string" ||
      !/^r0\d{2}[a-z]$/.test(contract.recap.latestRecapRelease)) {
    fail("contract", "recap.latestRecapRelease must match r0NNx");
  }
  contract.recap.preservedArtifacts ??= [];
  if (contract.recap.mode === "PRESERVE" && contract.recap.preservedArtifacts.length !== 2) {
    fail("contract", "PRESERVE recap requires exactly its HTML and PDF bindings");
  }
  for (const [index, artifact] of contract.recap.preservedArtifacts.entries()) {
    requireSafeRelativePath(artifact.path, `recap.preservedArtifacts[${index}].path`);
    requireSha256(artifact.sha256, `recap.preservedArtifacts[${index}].sha256`);
  }

  const policy = contract.artifactPolicy ?? {
    readerPdf: "REQUIRED",
    scientificFigure: "REQUIRED",
  };
  if (!isObject(policy) || !["REQUIRED", "OMIT_NEW"].includes(policy.readerPdf) ||
      !["REQUIRED", "NOT_REQUIRED"].includes(policy.scientificFigure)) {
    fail("contract", "artifactPolicy must declare readerPdf and scientificFigure");
  }
  contract.artifactPolicy = policy;

  const stem = releaseFileStem(contract.releaseId);
  const formal = /^r0\d{2}[a-z]$/.test(contract.releaseId);
  validateStage(
    contract,
    "generate",
    formal
      ? `scripts/generate_${contract.releaseId}_release.py`
      : `scripts/generate_${stem.replaceAll("-", "_")}_release.py`,
    "python-local",
  );
  validateStage(
    contract,
    "translate",
    `scripts/add-${stem}-translations.mjs`,
    "node-local",
  );
  if (policy.readerPdf === "REQUIRED") {
    validateStage(
      contract,
      "bind",
      formal
        ? `scripts/bind-${contract.releaseId}-pdfs.mjs`
        : `scripts/bind-${stem}-pdfs.mjs`,
      "node-local",
    );
  } else if (contract.stages?.bind !== undefined) {
    fail("contract", "HTML-only releases must omit stages.bind");
  }

  if (!isObject(contract.publication)) fail("contract", "publication is required");
  if (contract.publication.expectedCommit !== null) {
    requireCommit(contract.publication.expectedCommit, "publication.expectedCommit");
  }
  if (typeof contract.publication.siteBaseUrl !== "string" ||
      !/^https:\/\/[a-z0-9.-]+\/?$/i.test(contract.publication.siteBaseUrl)) {
    fail("contract", "publication.siteBaseUrl must be an HTTPS origin URL");
  }
  if (typeof contract.publication.repository !== "string" ||
      !/^[A-Za-z0-9_.-]+\/[A-Za-z0-9_.-]+$/.test(contract.publication.repository)) {
    fail("contract", "publication.repository must be owner/repository");
  }
  if (contract.publication.workflow !== "pages.yml") {
    fail("contract", "publication.workflow must be pages.yml");
  }
  if (contract.publication.remote !== "origin" || contract.publication.targetBranch !== "main") {
    fail("contract", "publication target must be origin/main");
  }
  contract.publication.managedPaths = requireStringArray(
    contract.publication.managedPaths,
    "publication.managedPaths",
  ).map((value, index) => requireSafeRelativePath(value, `publication.managedPaths[${index}]`));
  if (typeof contract.publication.commitMessage !== "string" || contract.publication.commitMessage.length === 0) {
    fail("contract", "publication.commitMessage must be nonempty");
  }
  if (formal &&
      !contract.publication.commitMessage.includes(contract.releaseId.toUpperCase().replace("R0", "R0."))) {
    fail("contract", "publication.commitMessage must name the public release code");
  }

  const requiredRoles = requiredLiveRoles(contract);
  if (!Array.isArray(contract.publication.expectedLive) ||
      contract.publication.expectedLive.length < requiredRoles.length) {
    fail("contract", "publication.expectedLive is incomplete");
  }
  const liveRoles = new Set();
  const livePaths = new Set();
  for (const [index, item] of contract.publication.expectedLive.entries()) {
    if (!isObject(item)) fail("contract", `expectedLive[${index}] must be an object`);
    requireSafeRelativePath(item.localPath, `expectedLive[${index}].localPath`);
    if (typeof item.urlPath !== "string" || !item.urlPath.startsWith("/") || item.urlPath.includes("..")) {
      fail("contract", `expectedLive[${index}].urlPath must be a safe absolute site path`);
    }
    if (typeof item.role !== "string" || item.role.length === 0) {
      fail("contract", `expectedLive[${index}].role is required`);
    }
    if (!Array.isArray(item.contentTypes) || item.contentTypes.length === 0 ||
        item.contentTypes.some((value) => typeof value !== "string" || value.length === 0)) {
      fail("contract", `expectedLive[${index}].contentTypes is required`);
    }
    if (liveRoles.has(item.role) || livePaths.has(item.urlPath)) {
      fail("contract", `duplicate live role or path at expectedLive[${index}]`);
    }
    liveRoles.add(item.role);
    livePaths.add(item.urlPath);
  }
  for (const role of requiredRoles) {
    if (!liveRoles.has(role)) fail("contract", `publication.expectedLive omits ${role}`);
  }
  contract.publication.expectedAbsent = requireStringArray(
    contract.publication.expectedAbsent ?? [],
    "publication.expectedAbsent",
    { nonempty: false },
  );
  for (const path of contract.publication.expectedAbsent) {
    if (!path.startsWith("/") || path.includes("..")) fail("contract", `unsafe expectedAbsent path ${path}`);
  }
  if (policy.readerPdf === "OMIT_NEW") {
    if (liveRoles.has("note-pdf")) {
      fail("contract", "HTML-only releases must not declare a live note-pdf role");
    }
    const note = contract.publication.expectedLive.find((item) => item.role === "note-html");
    const expectedPdf = note?.urlPath?.replace(/\.html$/, ".pdf");
    if (!expectedPdf || !contract.publication.expectedAbsent.includes(expectedPdf)) {
      fail("contract", "HTML-only releases must explicitly require the new note PDF to be absent");
    }
  }
  if (!isObject(contract.publication.siteVersionExpectations)) {
    fail("contract", "publication.siteVersionExpectations is required");
  }
  if (!isObject(contract.visualQa)) fail("contract", "visualQa is required");
  requireSafeRelativePath(contract.visualQa.evidencePath, "visualQa.evidencePath");
  contract.visualQa.requiredChecks = requireStringArray(
    contract.visualQa.requiredChecks,
    "visualQa.requiredChecks",
  );
  if (contract.visualQa.configPath !== undefined) {
    requireSafeRelativePath(contract.visualQa.configPath, "visualQa.configPath");
  }
  if ((!formal || policy.readerPdf === "OMIT_NEW") && !contract.visualQa.configPath) {
    fail("contract", "independent and HTML-only releases require visualQa.configPath");
  }
  return contract;
}

export async function loadHandoff(root, handoffPath) {
  const repositoryPath = requireSafeRelativePath(handoffPath, "handoff path");
  const absolute = resolveContained(root, repositoryPath, "handoff path");
  let contract;
  try {
    contract = JSON.parse(await readFile(absolute, "utf8"));
  } catch (error) {
    fail("contract", `cannot read ${repositoryPath}: ${error.message}`);
  }
  return { contract: validateHandoff(contract), path: repositoryPath, absolute };
}

async function requireRegularFile(root, repositoryPath, label) {
  const absolute = resolveContained(root, repositoryPath, label);
  let metadata;
  try {
    metadata = await lstat(absolute);
  } catch (error) {
    throw new Error(`${label} is missing: ${repositoryPath} (${error.code ?? error.message})`);
  }
  if (!metadata.isFile() || metadata.isSymbolicLink()) {
    throw new Error(`${label} must be a regular nonsymlink file: ${repositoryPath}`);
  }
  const [canonicalRoot, canonicalFile] = await Promise.all([realpath(root), realpath(absolute)]);
  const child = relative(canonicalRoot, canonicalFile);
  if (child === ".." || child.startsWith(`..${sep}`) || isAbsolute(child)) {
    throw new Error(`${label} escapes the repository: ${repositoryPath}`);
  }
  return absolute;
}

export async function verifyFrozenArtifacts(root, contract) {
  const failures = [];
  let sourceRoot = root;
  if (contract.sourceRepository) {
    try {
      const workspaceRoot = await realpath(dirname(root));
      const candidate = resolve(workspaceRoot, contract.sourceRepository);
      const metadata = await lstat(candidate);
      if (!metadata.isDirectory() || metadata.isSymbolicLink()) {
        throw new Error("sourceRepository must be a regular sibling directory");
      }
      sourceRoot = await realpath(candidate);
      if (dirname(sourceRoot) !== workspaceRoot) {
        throw new Error("sourceRepository escaped the publication workspace");
      }
    } catch (error) {
      failures.push({ label: "source repository", message: error.message });
    }
  }
  try {
    git(sourceRoot, ["rev-parse", "--verify", `${contract.frozenCommit}^{commit}`]);
    git(sourceRoot, ["merge-base", "--is-ancestor", contract.frozenCommit, "HEAD"]);
  } catch (error) {
    failures.push({ label: "frozen commit", message: error.message });
  }
  for (const artifact of contract.artifacts) {
    try {
      const absolute = await requireRegularFile(root, artifact.path, `artifact ${artifact.role}`);
      const current = await sha256File(absolute);
      if (current !== artifact.sha256) {
        throw new Error(`working-tree SHA-256 ${current} != ${artifact.sha256}`);
      }
      const sourceCommit = artifact.commit ?? contract.frozenCommit;
      git(sourceRoot, ["rev-parse", "--verify", `${sourceCommit}^{commit}`]);
      git(sourceRoot, ["merge-base", "--is-ancestor", sourceCommit, "HEAD"]);
      const objectId = git(sourceRoot, ["rev-parse", `${sourceCommit}:${artifact.path}`]);
      const frozen = sha256Bytes(git(sourceRoot, ["cat-file", "blob", objectId], { binary: true }));
      if (frozen !== artifact.sha256) {
        throw new Error(`source commit ${sourceCommit} SHA-256 ${frozen} != ${artifact.sha256}`);
      }
    } catch (error) {
      failures.push({ label: artifact.path, message: error.message });
    }
  }
  for (const artifact of contract.recap.preservedArtifacts) {
    try {
      const absolute = await requireRegularFile(root, artifact.path, "preserved recap");
      const current = await sha256File(absolute);
      if (current !== artifact.sha256) {
        throw new Error(`recap drifted: ${current} != ${artifact.sha256}`);
      }
    } catch (error) {
      failures.push({ label: artifact.path, message: error.message });
    }
  }
  if (failures.length > 0) throw new ReleasePipelineError("intake", failures);
  return {
    frozenCommit: contract.frozenCommit,
    sourceRepository: contract.sourceRepository ?? ".",
    artifactCount: contract.artifacts.length,
    recapMode: contract.recap.mode,
    latestRecapRelease: contract.recap.latestRecapRelease,
  };
}

export async function verifyClaimBoundary(root, contract) {
  const failures = [];
  for (const repositoryPath of contract.claimBoundary.publicFiles) {
    try {
      const absolute = await requireRegularFile(root, repositoryPath, "claim-boundary file");
      const text = await readFile(absolute, "utf8");
      for (const label of REQUIRED_BOUNDARIES) {
        if (!text.includes(label)) throw new Error(`missing ${label}`);
      }
    } catch (error) {
      failures.push({ label: repositoryPath, message: error.message });
    }
  }
  if (failures.length > 0) throw new ReleasePipelineError("claim-boundary", failures);
  return { labels: [...REQUIRED_BOUNDARIES], files: contract.claimBoundary.publicFiles };
}

async function collectFiles(root, repositoryPath) {
  const absolute = resolveContained(root, repositoryPath, "fingerprint path");
  let metadata;
  try {
    metadata = await lstat(absolute);
  } catch (error) {
    if (error.code === "ENOENT") return [{ path: repositoryPath, sha256: "MISSING" }];
    throw error;
  }
  if (metadata.isSymbolicLink()) throw new Error(`fingerprint path is a symlink: ${repositoryPath}`);
  if (metadata.isFile()) return [{ path: repositoryPath, sha256: await sha256File(absolute) }];
  if (!metadata.isDirectory()) throw new Error(`unsupported fingerprint path: ${repositoryPath}`);
  const names = (await readdir(absolute)).sort();
  const nested = await Promise.all(names.map((name) => collectFiles(root, posix.join(repositoryPath, name))));
  return nested.flat();
}

export async function fingerprintPaths(root, repositoryPaths, extra = {}) {
  const unique = [...new Set(repositoryPaths)].sort();
  const entries = (await Promise.all(unique.map((path) => collectFiles(root, path)))).flat();
  return sha256Bytes(JSON.stringify({ entries, extra }));
}

export async function workspaceFingerprint(root, extra = {}) {
  const head = git(root, ["rev-parse", "HEAD"]);
  const diff = git(root, ["diff", "--binary", "HEAD"], { binary: true });
  const untrackedRaw = git(root, ["ls-files", "--others", "--exclude-standard", "-z"], { binary: true });
  const untracked = untrackedRaw
    .toString("utf8")
    .split("\0")
    .filter(Boolean)
    .filter((path) => !path.startsWith(".release/") && !path.startsWith("tmp/"));
  const untrackedFingerprint = await fingerprintPaths(root, untracked, { kind: "untracked" });
  return sha256Bytes(JSON.stringify({
    head,
    diff: sha256Bytes(diff),
    untrackedFingerprint,
    extra,
  }));
}

export function runProcess(executable, arguments_, options = {}) {
  return new Promise((resolvePromise) => {
    const child = spawn(executable, arguments_, {
      cwd: options.cwd,
      env: { ...process.env, ...(options.env ?? {}) },
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", (error) => {
      resolvePromise({ status: null, stdout, stderr, error });
    });
    child.on("close", (status) => {
      resolvePromise({ status, stdout, stderr, error: null });
    });
  });
}

function commandFailure(label, result) {
  return {
    label,
    message: result.error?.message ?? `exit status ${result.status}`,
    stdout: result.stdout,
    stderr: result.stderr,
  };
}

async function outputHashes(root, paths) {
  const entries = {};
  for (const repositoryPath of paths) {
    const absolute = await requireRegularFile(root, repositoryPath, "stage output");
    entries[repositoryPath] = await sha256File(absolute);
  }
  return entries;
}

async function outputsStillMatch(root, outputs) {
  try {
    for (const [repositoryPath, expected] of Object.entries(outputs ?? {})) {
      const absolute = await requireRegularFile(root, repositoryPath, "cached output");
      if (await sha256File(absolute) !== expected) return false;
    }
    return true;
  } catch {
    return false;
  }
}

async function readJsonIfPresent(path, fallback) {
  try {
    return JSON.parse(await readFile(path, "utf8"));
  } catch (error) {
    if (error.code === "ENOENT") return fallback;
    throw error;
  }
}

async function atomicJson(path, value) {
  await mkdir(dirname(path), { recursive: true });
  const temporary = `${path}.tmp-${process.pid}`;
  await writeFile(temporary, JSON.stringify(value, null, 2) + "\n");
  await rename(temporary, path);
}

async function ensureVerificationCheckout(root, runtimeRoot, commit) {
  const checkout = resolve(runtimeRoot, "checkouts", commit);
  try {
    const metadata = await lstat(checkout);
    if (!metadata.isDirectory() || metadata.isSymbolicLink()) {
      throw new Error("verification checkout path is not a regular directory");
    }
    if (git(checkout, ["rev-parse", "HEAD"]) !== commit) {
      throw new Error("verification checkout points to the wrong commit");
    }
    if (git(checkout, ["status", "--porcelain"]) !== "") {
      throw new Error("verification checkout is dirty");
    }
    return checkout;
  } catch (error) {
    if (error.code !== "ENOENT") {
      throw new ReleasePipelineError("verify-existing", [{
        label: "isolated checkout",
        message: error.message,
      }]);
    }
  }
  await mkdir(dirname(checkout), { recursive: true });
  const cloned = spawnSync("git", ["clone", "--quiet", "--shared", "--no-checkout", root, checkout], {
    cwd: root,
    encoding: "utf8",
  });
  if (cloned.error || cloned.status !== 0) {
    throw new ReleasePipelineError("verify-existing", [{
      label: "isolated checkout",
      message: cloned.error?.message ?? cloned.stderr.trim(),
    }]);
  }
  git(checkout, ["checkout", "--quiet", "--detach", commit]);
  return checkout;
}

function stageIndex(name) {
  const index = STAGES.indexOf(name);
  if (index < 0) fail("cli", `unknown stage ${name}`);
  return index;
}

async function stageFingerprint(root, loaded, name, mode, publicationCommit) {
  const contract = loaded.contract;
  const runtime = runtimeIdentityForStage(contract, name);
  if (name === "intake") {
    return fingerprintPaths(root, [
      loaded.path,
      ...contract.artifacts.map((item) => item.path),
      ...DETERMINISTIC_RUNTIME_INPUTS,
    ], {
      name,
      mode,
      frozenCommit: contract.frozenCommit,
      runtime,
    });
  }
  if (["generate", "translate", "bind"].includes(name)) {
    const stage = contract.stages[name];
    if (!stage) {
      return fingerprintPaths(root, DETERMINISTIC_RUNTIME_INPUTS, {
        name,
        mode,
        policy: artifactPolicy(contract),
        runtime,
      });
    }
    return fingerprintPaths(root, [
      loaded.path,
      stage.script,
      ...stage.inputs,
      ...DETERMINISTIC_RUNTIME_INPUTS,
    ], { name, mode, runtime });
  }
  if (name === "gate") return workspaceFingerprint(root, { name, mode, runtime });
  if (["commit", "push", "deploy"].includes(name)) {
    return sha256Bytes(JSON.stringify({
      name,
      mode,
      publicationCommit,
      expectedCommit: contract.publication.expectedCommit,
      target: `${contract.publication.remote}/${contract.publication.targetBranch}`,
    }));
  }
  if (name === "qa") {
    return fingerprintPaths(
      root,
      [
        loaded.path,
        contract.visualQa.evidencePath,
        ...(contract.visualQa.configPath ? [contract.visualQa.configPath] : []),
        ...contract.publication.expectedLive.map((item) => item.localPath),
      ],
      { name, mode, publicationCommit },
    );
  }
  throw new Error(`unhandled stage ${name}`);
}

function executableFor(stage) {
  if (stage.runner === "node-local") return process.execPath;
  return process.env.RELEASE_PYTHON ?? "python3";
}

export function runtimeIdentityForStage(contract, name) {
  const stage = contract.stages?.[name];
  const executable = stage ? executableFor(stage) : process.execPath;
  if (stage?.runner === "python-local") {
    const identity = spawnSync(executable, [
      "-c",
      "import json,sys; print(json.dumps({'executable':sys.executable,'prefix':sys.prefix,'version':sys.version}))",
    ], { encoding: "utf8" });
    if (identity.status === 0) {
      return {
        ...JSON.parse(identity.stdout),
        command: executable,
        nodeExecutable: process.execPath,
        nodeVersion: process.version,
      };
    }
  }
  const version = spawnSync(executable, ["--version"], { encoding: "utf8" });
  return {
    executable,
    version: version.status === 0
      ? `${version.stdout ?? ""}${version.stderr ?? ""}`.trim()
      : `unavailable:${version.status ?? version.error?.message ?? "unknown"}`,
    nodeExecutable: process.execPath,
    nodeVersion: process.version,
  };
}

async function runScriptStage(root, contract, name, verifyExisting) {
  const stage = contract.stages[name];
  if (!stage && name === "bind" && artifactPolicy(contract).readerPdf === "OMIT_NEW") {
    return { execution: "omitted-by-html-only-policy", outputs: {} };
  }
  const executable = executableFor(stage);
  const commands = verifyExisting
    ? [[stage.script, "--check-only"]]
    : [[stage.script], [stage.script, "--check-only"]];
  const results = [];
  for (const arguments_ of commands) {
    const result = await runProcess(executable, arguments_, {
      cwd: root,
      env: { PYTHONDONTWRITEBYTECODE: "1" },
    });
    results.push({ arguments_, result });
    if (result.status !== 0 || result.error) {
      throw new ReleasePipelineError(name, [commandFailure(`${executable} ${arguments_.join(" ")}`, result)]);
    }
  }
  await verifyClaimBoundary(root, contract);
  return {
    execution: verifyExisting ? "check-only" : "apply-then-check",
    commands: results.map(({ arguments_, result }) => ({
      command: [executable, ...arguments_],
      status: result.status,
      stdout: result.stdout,
      stderr: result.stderr,
    })),
    outputs: await outputHashes(root, stage.outputs),
  };
}

export async function validateFreshBrowserQaConfig(root, contract) {
  if (!contract.visualQa.configPath) {
    throw new ReleasePipelineError("qa", [{
      label: "fresh browser QA",
      message: "visualQa.configPath is required for a complete online QA result",
    }]);
  }
  const config = await loadPublicationQaConfig(root, contract.visualQa.configPath);
  const failures = [];
  if (config.releaseId !== contract.releaseId) failures.push("releaseId mismatch");
  if (config.browser.evidencePath !== contract.visualQa.evidencePath) {
    failures.push("browser evidencePath does not match handoff visualQa.evidencePath");
  }
  const configuredChecks = new Set(config.browser.targets.flatMap((target) =>
    config.browser.scenarios.map((scenario) => `${target.id}-${scenario.id}`)));
  for (const id of contract.visualQa.requiredChecks) {
    if (!configuredChecks.has(id)) failures.push(`browser config omits required check ${id}`);
  }
  if (failures.length > 0) {
    throw new ReleasePipelineError("qa", failures.map((message) => ({
      label: "fresh browser QA config",
      message,
    })));
  }
  return config;
}

async function runFreshBrowserQa(root, contract, publicationCommit) {
  await validateFreshBrowserQaConfig(root, contract);
  const result = await runProcess(process.execPath, [
    "scripts/qa-publication-browser.mjs",
    "--config",
    contract.visualQa.configPath,
    "--commit",
    publicationCommit,
    "--base-url",
    contract.publication.siteBaseUrl,
  ], { cwd: root });
  if (result.status !== 0 || result.error) {
    throw new ReleasePipelineError("qa", [commandFailure("fresh browser QA", result)]);
  }
  return { command: "scripts/qa-publication-browser.mjs", summary: result.stdout.trim() };
}

export async function runChecksCollectingFailures(root, checks) {
  return Promise.all(checks.map(async (check) => ({
    ...check,
    result: await runProcess(check.executable, check.arguments_, {
      cwd: root,
      env: { PYTHONDONTWRITEBYTECODE: "1" },
    }),
  })));
}

function resolvedGateChecks(resolved) {
  return [
    {
      label: "global release-publication invariant",
      executable: process.execPath,
      arguments_: ["--test", resolved.invariant],
    },
    {
      label: `latest mathematical gate (${resolved.release})`,
      executable: process.execPath,
      arguments_: ["--test", resolved.gate],
    },
    {
      label: `latest publication test (${resolved.release})`,
      executable: process.execPath,
      arguments_: ["--test", resolved.publication],
    },
    {
      label: `latest translation snapshot (${resolved.release})`,
      executable: process.execPath,
      arguments_: [resolved.translation, "--check-only"],
    },
    ...resolved.retainedGlobalTests.map((testPath) => ({
      label: `retained global test (${testPath})`,
      executable: process.execPath,
      arguments_: ["--test", testPath],
    })),
  ];
}

async function runAuditStage(root, contract) {
  await verifyClaimBoundary(root, contract);
  const checks = [
    {
      label: "release-publication-gate",
      executable: process.execPath,
      arguments_: ["scripts/run-release-publication-gate.mjs"],
    },
    {
      label: "public-site-structural-audit",
      executable: process.env.RELEASE_PYTHON ?? "python3",
      arguments_: ["scripts/audit_public_site.py", "--json"],
    },
  ];
  const completed = await runChecksCollectingFailures(root, checks);
  const structuralFailure = completed.find(
    (check) => check.label === "public-site-structural-audit" &&
      (check.result.status !== 0 || check.result.error),
  );
  const publicationFailure = completed.find(
    (check) => check.label === "release-publication-gate" &&
      (check.result.status !== 0 || check.result.error),
  );
  const failures = structuralFailure ? [commandFailure(structuralFailure.label, structuralFailure.result)] : [];
  let diagnostic = [];
  if (publicationFailure) {
    try {
      const resolved = await resolveReleasePublicationGate(root);
      diagnostic = await runChecksCollectingFailures(root, resolvedGateChecks(resolved));
      const diagnosticFailures = diagnostic
        .filter((check) => check.result.status !== 0 || check.result.error)
        .map((check) => commandFailure(check.label, check.result));
      failures.push(...(diagnosticFailures.length > 0
        ? diagnosticFailures
        : [commandFailure(publicationFailure.label, publicationFailure.result)]));
    } catch (error) {
      failures.push({ label: "release-publication-gate resolver", message: error.message });
    }
  }
  if (failures.length > 0) throw new ReleasePipelineError("gate", failures);
  const structural = JSON.parse(completed.find((item) => item.label === "public-site-structural-audit").result.stdout);
  return {
    checks: [...completed, ...diagnostic].map((item) => ({
      label: item.label,
      status: "pass",
      stdout: item.result.stdout,
      stderr: item.result.stderr,
    })),
    structural,
    outputs: {},
  };
}

function changedPaths(root) {
  const tracked = git(root, ["diff", "--name-only", "-z", "HEAD"], { binary: true })
    .toString("utf8").split("\0").filter(Boolean);
  const untracked = git(root, ["ls-files", "--others", "--exclude-standard", "-z"], { binary: true })
    .toString("utf8").split("\0").filter(Boolean);
  return [...new Set([...tracked, ...untracked])]
    .filter((path) => !path.startsWith(".release/") && !path.startsWith("tmp/"));
}

function pathManaged(path, managedPaths) {
  return managedPaths.some((allowed) => path === allowed || path.startsWith(`${allowed}/`));
}

async function runCommitStage(root, contract, verifyExisting, allowCommit) {
  if (verifyExisting) {
    git(root, ["cat-file", "-e", `${contract.publication.expectedCommit}^{commit}`]);
    return {
      publicationCommit: contract.publication.expectedCommit,
      execution: "verified-existing",
      outputs: {},
    };
  }
  if (!allowCommit) fail("commit", "--allow-commit is required for a release commit");
  const outside = changedPaths(root).filter((path) => !pathManaged(path, contract.publication.managedPaths));
  if (outside.length > 0) {
    throw new ReleasePipelineError("commit", outside.map((path) => ({
      label: path,
      message: "changed path is outside publication.managedPaths",
    })));
  }
  git(root, ["add", "--", ...contract.publication.managedPaths]);
  const staged = spawnSync("git", ["diff", "--cached", "--quiet"], { cwd: root });
  if (staged.status === 1) git(root, ["commit", "-m", contract.publication.commitMessage]);
  if (staged.status !== 0 && staged.status !== 1) {
    throw new Error("cannot inspect staged publication changes");
  }
  const publicationCommit = git(root, ["rev-parse", "HEAD"]);
  return { publicationCommit, execution: staged.status === 1 ? "committed" : "already-committed", outputs: {} };
}

async function runPushStage(root, contract, verifyExisting, allowPush, publicationCommit) {
  if (verifyExisting) {
    return { publicationCommit, execution: "verified-existing", outputs: {} };
  }
  if (!allowPush) fail("push", "--allow-push is required before updating origin/main");
  const dirty = changedPaths(root);
  if (dirty.length > 0) {
    throw new ReleasePipelineError("push", dirty.map((path) => ({ label: path, message: "worktree is not clean" })));
  }
  const result = await runProcess("git", [
    "push",
    "--porcelain",
    contract.publication.remote,
    `HEAD:refs/heads/${contract.publication.targetBranch}`,
  ], { cwd: root });
  if (result.status !== 0 || result.error) {
    throw new ReleasePipelineError("push", [commandFailure("git push origin/main", result)]);
  }
  return { publicationCommit, execution: "pushed", outputs: {}, stdout: result.stdout.trim() };
}

function delay(milliseconds) {
  return new Promise((resolvePromise) => setTimeout(resolvePromise, milliseconds));
}

export async function waitForPagesDeployment(contract, publicationCommit, options = {}) {
  const timeoutMs = options.timeoutMs ?? 15 * 60 * 1000;
  const pollMs = options.pollMs ?? 10_000;
  const deadline = Date.now() + timeoutMs;
  const api = `https://api.github.com/repos/${contract.publication.repository}/actions/workflows/${contract.publication.workflow}/runs?branch=${encodeURIComponent(contract.publication.targetBranch)}&per_page=30`;
  let lastSeen = null;
  while (Date.now() <= deadline) {
    const response = await fetch(api, {
      headers: { Accept: "application/vnd.github+json", "User-Agent": "research-publication-pipeline" },
    });
    if (!response.ok) {
      throw new ReleasePipelineError("deploy", [{ label: "GitHub Actions API", message: `HTTP ${response.status}` }]);
    }
    const payload = await response.json();
    const run = payload.workflow_runs?.find((item) => item.head_sha === publicationCommit);
    if (run) {
      lastSeen = run;
      if (run.status === "completed" && run.conclusion === "success") {
        return {
          workflowRunId: run.id,
          url: run.html_url,
          headSha: run.head_sha,
          status: run.status,
          conclusion: run.conclusion,
          updatedAt: run.updated_at,
          outputs: {},
        };
      }
      if (run.status === "completed") {
        throw new ReleasePipelineError("deploy", [{
          label: `workflow run ${run.id}`,
          message: `completed with ${run.conclusion}`,
        }]);
      }
    }
    await delay(Math.min(pollMs, Math.max(0, deadline - Date.now())));
  }
  throw new ReleasePipelineError("deploy", [{
    label: "GitHub Pages deployment",
    message: `timeout waiting for ${publicationCommit}; last status ${lastSeen?.status ?? "not found"}`,
  }]);
}

async function verifyVisualEvidence(root, contract, publicationCommit) {
  const path = await requireRegularFile(root, contract.visualQa.evidencePath, "visual QA evidence");
  const evidence = JSON.parse(await readFile(path, "utf8"));
  const failures = [];
  if (evidence.schemaVersion !== "publication-visual-qa-v1") failures.push("unsupported schemaVersion");
  if (evidence.releaseId !== contract.releaseId) failures.push("releaseId mismatch");
  if (evidence.publicationCommit !== publicationCommit) failures.push("publicationCommit mismatch");
  if (!Array.isArray(evidence.checks)) failures.push("checks must be an array");
  const passed = new Set((evidence.checks ?? []).filter((check) => check.status === "pass").map((check) => check.id));
  for (const id of contract.visualQa.requiredChecks) {
    if (!passed.has(id)) failures.push(`missing passing visual check ${id}`);
  }
  if (!Array.isArray(evidence.defects) || evidence.defects.length !== 0) failures.push("visual defects are not empty");
  if (failures.length > 0) {
    throw new ReleasePipelineError("qa", failures.map((message) => ({ label: "visual QA", message })));
  }
  return { evidencePath: contract.visualQa.evidencePath, checkCount: passed.size, status: "pass" };
}

export async function verifyLivePublication(root, contract, publicationCommit) {
  const base = contract.publication.siteBaseUrl.replace(/\/$/, "");
  const cacheBust = `release-qa=${publicationCommit.slice(0, 12)}-${Date.now()}`;
  const liveChecks = await Promise.all(contract.publication.expectedLive.map(async (item) => {
    const local = await requireRegularFile(root, item.localPath, `live source ${item.role}`);
    const localSha256 = await sha256File(local);
    const separator = item.urlPath.includes("?") ? "&" : "?";
    const response = await fetch(`${base}${item.urlPath}${separator}${cacheBust}`, {
      redirect: "follow",
      headers: { "Cache-Control": "no-cache" },
    });
    const bytes = Buffer.from(await response.arrayBuffer());
    const liveSha256 = sha256Bytes(bytes);
    const contentType = response.headers.get("content-type") ?? "";
    const errors = [];
    if (response.status !== 200) errors.push(`HTTP ${response.status}`);
    if (!item.contentTypes.some((prefix) => contentType.toLowerCase().startsWith(prefix.toLowerCase()))) {
      errors.push(`content-type ${contentType}`);
    }
    if (liveSha256 !== localSha256) errors.push(`SHA-256 ${liveSha256} != ${localSha256}`);
    return {
      role: item.role,
      urlPath: item.urlPath,
      localPath: item.localPath,
      statusCode: response.status,
      contentType,
      bytes: bytes.length,
      localSha256,
      liveSha256,
      errors,
      body: item.role === "site-version" ? bytes.toString("utf8") : undefined,
    };
  }));
  const absentChecks = await Promise.all(contract.publication.expectedAbsent.map(async (urlPath) => {
    const separator = urlPath.includes("?") ? "&" : "?";
    const response = await fetch(`${base}${urlPath}${separator}${cacheBust}`, {
      redirect: "manual",
      headers: { "Cache-Control": "no-cache" },
    });
    return { urlPath, statusCode: response.status, errors: response.status === 404 ? [] : [`expected 404, got ${response.status}`] };
  }));
  const failures = [...liveChecks, ...absentChecks]
    .filter((check) => check.errors.length > 0)
    .flatMap((check) => check.errors.map((message) => ({ label: check.urlPath, message })));
  const siteVersionCheck = liveChecks.find((check) => check.role === "site-version");
  try {
    const siteVersion = JSON.parse(siteVersionCheck.body);
    for (const [key, value] of Object.entries(contract.publication.siteVersionExpectations)) {
      if (siteVersion[key] !== value) {
        failures.push({ label: "site-version", message: `${key}=${siteVersion[key]} != ${value}` });
      }
    }
  } catch (error) {
    failures.push({ label: "site-version", message: `invalid JSON: ${error.message}` });
  }
  if (failures.length > 0) throw new ReleasePipelineError("qa", failures);
  const visual = await verifyVisualEvidence(root, contract, publicationCommit);
  return {
    files: liveChecks.map((check) => {
      const result = { ...check };
      delete result.body;
      delete result.errors;
      return result;
    }),
    expectedAbsent: absentChecks.map((check) => {
      const result = { ...check };
      delete result.errors;
      return result;
    }),
    visual,
    outputs: {},
  };
}

export async function runReleasePipeline(options) {
  const root = resolve(options.root);
  const loaded = await loadHandoff(root, options.handoffPath);
  const contract = loaded.contract;
  if (options.verifyExisting && contract.publication.expectedCommit === null) {
    fail("contract", "--verify-existing requires publication.expectedCommit");
  }
  const through = options.through ?? "qa";
  const finalStageIndex = stageIndex(through);
  const mode = options.verifyExisting ? "verify-existing" : "release";
  const runtimeRoot = resolve(root, ".release");
  const executionRoot = options.verifyExisting
    ? await ensureVerificationCheckout(root, runtimeRoot, contract.publication.expectedCommit)
    : root;
  const cachePath = resolve(runtimeRoot, "cache", `${contract.releaseId}.json`);
  const statePath = resolve(runtimeRoot, "state", `${contract.releaseId}.json`);
  const receiptPath = resolve(runtimeRoot, "receipts", `${contract.releaseId}.json`);
  const cache = await readJsonIfPresent(cachePath, { schemaVersion: RUNTIME_SCHEMA, stages: {} });
  const state = await readJsonIfPresent(statePath, {
    schemaVersion: RUNTIME_SCHEMA,
    releaseId: contract.releaseId,
    mode,
    currentState: "RECEIVED",
    stages: {},
  });
  const startedAt = new Date().toISOString();
  const runId = startedAt.replaceAll(":", "-");
  const logRoot = resolve(runtimeRoot, "logs", contract.releaseId, runId);
  const receipt = {
    schemaVersion: "research-publication-receipt-v1",
    releaseId: contract.releaseId,
    frozenCommit: contract.frozenCommit,
    mode,
    startedAt,
    completedAt: null,
    finalState: state.currentState,
    publicationCommit: null,
    recap: {
      mode: contract.recap.mode,
      latestRecapRelease: contract.recap.latestRecapRelease,
    },
    claimBoundary: [...REQUIRED_BOUNDARIES],
    stages: [],
    logs: [],
    errors: [],
  };
  let publicationCommit = options.verifyExisting ? contract.publication.expectedCommit : null;

  for (const name of STAGES.slice(0, finalStageIndex + 1)) {
    const stageStarted = Date.now();
    const fingerprint = await stageFingerprint(root, loaded, name, mode, publicationCommit);
    const cached = cache.stages[name];
    const outputsMatch = cached && isStageCacheable(name)
      ? await outputsStillMatch(root, cached.outputs)
      : false;
    if (canReuseStage(name, {
      noCache: options.noCache,
      cachedFingerprint: cached?.fingerprint,
      fingerprint,
      outputsMatch,
    })) {
      publicationCommit = cached.details?.publicationCommit ?? publicationCommit;
      const stageReceipt = {
        name,
        state: stateAfterStage(contract, name),
        status: "pass",
        cached: true,
        durationMs: Date.now() - stageStarted,
        fingerprint,
        details: cached.details,
      };
      const logPath = resolve(logRoot, `${name}.json`);
      stageReceipt.logPath = relative(root, logPath);
      receipt.stages.push(stageReceipt);
      receipt.logs.push(stageReceipt.logPath);
      recordSuccessfulStage(state, contract, name, stageReceipt);
      await Promise.all([
        atomicJson(statePath, { ...state, updatedAt: new Date().toISOString() }),
        atomicJson(logPath, stageReceipt),
      ]);
      options.onProgress?.(stageReceipt);
      continue;
    }

    try {
      let details;
      if (name === "intake") details = { ...(await verifyFrozenArtifacts(root, contract)), outputs: {} };
      else if (["generate", "translate", "bind"].includes(name)) {
        details = await runScriptStage(executionRoot, contract, name, options.verifyExisting);
      } else if (name === "gate") details = await runAuditStage(executionRoot, contract);
      else if (name === "commit") {
        details = await runCommitStage(root, contract, options.verifyExisting, options.allowCommit);
        publicationCommit = details.publicationCommit;
      } else if (name === "push") {
        details = await runPushStage(
          root,
          contract,
          options.verifyExisting,
          options.allowPush,
          publicationCommit,
        );
      } else if (name === "deploy") {
        details = await waitForPagesDeployment(contract, publicationCommit, {
          timeoutMs: options.deploymentTimeoutMs,
          pollMs: options.deploymentPollMs,
        });
      } else if (name === "qa") {
        const browser = await runFreshBrowserQa(root, contract, publicationCommit);
        details = await verifyLivePublication(root, contract, publicationCommit);
        details.browser = browser;
      }
      const stageReceipt = {
        name,
        state: stateAfterStage(contract, name),
        status: "pass",
        cached: false,
        durationMs: Date.now() - stageStarted,
        fingerprint,
        details,
      };
      const logPath = resolve(logRoot, `${name}.json`);
      stageReceipt.logPath = relative(root, logPath);
      receipt.stages.push(stageReceipt);
      receipt.logs.push(stageReceipt.logPath);
      recordSuccessfulStage(state, contract, name, stageReceipt);
      if (isStageCacheable(name)) {
        cache.stages[name] = {
          fingerprint,
          outputs: details.outputs ?? {},
          details,
          completedAt: new Date().toISOString(),
        };
      }
      await Promise.all([
        atomicJson(statePath, { ...state, updatedAt: new Date().toISOString() }),
        atomicJson(cachePath, cache),
        atomicJson(logPath, stageReceipt),
      ]);
      options.onProgress?.(stageReceipt);
    } catch (error) {
      const normalized = error instanceof ReleasePipelineError
        ? error
        : new ReleasePipelineError(name, [{ label: name, message: error.message ?? String(error) }]);
      const stageReceipt = {
        name,
        state: state.currentState,
        status: "fail",
        cached: false,
        durationMs: Date.now() - stageStarted,
        fingerprint,
        errors: normalized.failures,
      };
      const logPath = resolve(logRoot, `${name}.json`);
      stageReceipt.logPath = relative(root, logPath);
      receipt.stages.push(stageReceipt);
      receipt.logs.push(stageReceipt.logPath);
      receipt.errors.push(...normalized.failures);
      receipt.completedAt = new Date().toISOString();
      receipt.finalState = state.currentState;
      receipt.publicationCommit = publicationCommit;
      state.failedStage = name;
      state.stages[name] = stageReceipt;
      await Promise.all([
        atomicJson(statePath, { ...state, updatedAt: new Date().toISOString() }),
        atomicJson(receiptPath, receipt),
        atomicJson(logPath, stageReceipt),
      ]);
      options.onProgress?.(stageReceipt);
      normalized.receiptPath = relative(root, receiptPath);
      throw normalized;
    }
  }

  receipt.completedAt = new Date().toISOString();
  receipt.finalState = stateAfterStage(contract, through);
  receipt.publicationCommit = publicationCommit;
  receipt.receiptPath = relative(root, receiptPath);
  await atomicJson(receiptPath, receipt);
  return receipt;
}
