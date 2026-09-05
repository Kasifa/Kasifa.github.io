import assert from "node:assert/strict";
import Ajv2020 from "ajv/dist/2020.js";
import { createServer } from "node:http";
import { mkdtemp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

import { parseArguments } from "../scripts/publish-release.mjs";
import {
  DETERMINISTIC_RUNTIME_INPUTS,
  STATE_AFTER_STAGE,
  STAGES,
  canReuseStage,
  fingerprintPaths,
  isStageCacheable,
  recordSuccessfulStage,
  runChecksCollectingFailures,
  runtimeIdentityForStage,
  stateAfterStage,
  validateHandoff,
  validateFreshBrowserQaConfig,
  verifyFrozenArtifacts,
  verifyLivePublication,
} from "../scripts/release-pipeline-lib.mjs";
import { loadPublicationQaConfig } from "../scripts/publication-qa-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const baselinePath = resolve(root, "release/handoffs/r073y-baseline.json");

test("R0.73Y baseline contract binds the frozen research commit and R0.73X recap", async () => {
  const contract = validateHandoff(JSON.parse(await readFile(baselinePath, "utf8")));
  const verified = await verifyFrozenArtifacts(root, contract);
  assert.equal(contract.releaseId, "r073y");
  assert.equal(verified.frozenCommit, "1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66");
  assert.equal(verified.recapMode, "PRESERVE");
  assert.equal(verified.latestRecapRelease, "r073x");
  assert.deepEqual(contract.claimBoundary.requiredLabels, ["PROVED", "FINITE", "OPEN", "NOT CLAY"]);
});

test("handoff rejects path traversal and arbitrary stage scripts", async () => {
  const original = JSON.parse(await readFile(baselinePath, "utf8"));
  const traversal = structuredClone(original);
  traversal.artifacts[0].path = "../research/escape.md";
  assert.throws(() => validateHandoff(traversal), /unsafe|normalized/);

  const injected = structuredClone(original);
  injected.stages.generate.script = "scripts/not-the-release-generator.py";
  assert.throws(() => validateHandoff(injected), /must be scripts\/generate_r073y_release\.py/);
});

test("state machine order is explicit and monotone", () => {
  assert.deepEqual(STAGES, [
    "intake", "generate", "translate", "bind", "gate", "commit", "push", "deploy", "qa",
  ]);
  assert.deepEqual(STAGES.map((stage) => STATE_AFTER_STAGE[stage]), [
    "INTAKE_VALIDATED",
    "CONTENT_GENERATED",
    "TRANSLATION_VALIDATED",
    "PDF_BOUND",
    "AUDIT_PASSED",
    "COMMIT_CONFIRMED",
    "PUSH_CONFIRMED",
    "DEPLOYMENT_CONFIRMED",
    "LIVE_QA_PASSED",
  ]);
});

test("HTML-only independent contracts omit bind/PDF/figure roles and use the HTML state", async () => {
  const contract = JSON.parse(await readFile(baselinePath, "utf8"));
  contract.releaseId = "ClayB-PhysicalAdjoint-20260906";
  contract.artifactPolicy = { readerPdf: "OMIT_NEW", scientificFigure: "NOT_REQUIRED" };
  contract.stages.generate.script = "scripts/generate_clay_b_physical_adjoint_20260906_release.py";
  contract.stages.translate.script = "scripts/add-clay-b-physical-adjoint-20260906-translations.mjs";
  delete contract.stages.bind;
  contract.publication.commitMessage = "Publish ClayB PhysicalAdjoint 20260906 HTML note";
  contract.publication.expectedLive = [
    { role: "homepage", localPath: "public/research-review.html", urlPath: "/", contentTypes: ["text/html"] },
    { role: "note-html", localPath: "public/notes/clay-b-physical-adjoint-20260906.html", urlPath: "/notes/clay-b-physical-adjoint-20260906.html", contentTypes: ["text/html"] },
    { role: "note-index", localPath: "public/notes/index.html", urlPath: "/notes/", contentTypes: ["text/html"] },
    { role: "site-version", localPath: "public/site-version.json", urlPath: "/site-version.json", contentTypes: ["application/json"] },
  ];
  contract.publication.expectedAbsent = ["/notes/clay-b-physical-adjoint-20260906.pdf"];
  contract.visualQa.configPath = "release/qa/clay-b-physical-adjoint-20260906.json";
  contract.visualQa.evidencePath = ".release/qa/ClayB-PhysicalAdjoint-20260906.json";
  contract.visualQa.requiredChecks = ["note-desktop"];
  const validated = validateHandoff(contract);
  assert.equal(validated.artifactPolicy.readerPdf, "OMIT_NEW");
  assert.equal(validated.stages.bind, undefined);
  assert.equal(stateAfterStage(validated, "bind"), "HTML_ARTIFACTS_BOUND");
  assert.equal(stateAfterStage(validateHandoff(JSON.parse(await readFile(baselinePath, "utf8"))), "bind"), "PDF_BOUND");

  const missingConfig = structuredClone(contract);
  delete missingConfig.visualQa.configPath;
  assert.throws(() => validateHandoff(missingConfig), /visualQa\.configPath/);
});

test("incremental fingerprint changes when an input changes", async () => {
  const directory = await mkdtemp(join(tmpdir(), "release-fingerprint-"));
  try {
    await writeFile(join(directory, "input.txt"), "first\n");
    const first = await fingerprintPaths(directory, ["input.txt"], { stage: "generate" });
    await writeFile(join(directory, "input.txt"), "second\n");
    const second = await fingerprintPaths(directory, ["input.txt"], { stage: "generate" });
    assert.notEqual(first, second);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("only deterministic local stages are cacheable and runtime identity is concrete", async () => {
  assert.deepEqual(STAGES.filter(isStageCacheable), ["intake", "generate", "translate", "bind", "gate"]);
  assert.deepEqual(STAGES.filter((name) => !isStageCacheable(name)), ["commit", "push", "deploy", "qa"]);
  const identical = { noCache: false, cachedFingerprint: "same", fingerprint: "same", outputsMatch: true };
  assert.equal(canReuseStage("generate", identical), true);
  assert.equal(canReuseStage("qa", identical), false);
  assert.equal(canReuseStage("qa", identical), false, "a second identical QA run is still fresh");
  assert.ok(DETERMINISTIC_RUNTIME_INPUTS.includes("pnpm-lock.yaml"));
  assert.ok(DETERMINISTIC_RUNTIME_INPUTS.includes("scripts/release-pipeline-lib.mjs"));
  const contract = { stages: { generate: { runner: "python-local" } } };
  const original = process.env.RELEASE_PYTHON;
  try {
    process.env.RELEASE_PYTHON = "/usr/bin/python3";
    const system = runtimeIdentityForStage(contract, "generate");
    process.env.RELEASE_PYTHON = process.execPath;
    const changed = runtimeIdentityForStage(contract, "generate");
    assert.match(system.executable, /^\//);
    assert.notDeepEqual(system, changed);
  } finally {
    if (original === undefined) delete process.env.RELEASE_PYTHON;
    else process.env.RELEASE_PYTHON = original;
  }
});

test("a successful retry clears the matching failed stage", () => {
  const state = { currentState: "DEPLOYMENT_CONFIRMED", failedStage: "qa", stages: {} };
  const contract = { artifactPolicy: { readerPdf: "OMIT_NEW", scientificFigure: "NOT_REQUIRED" } };
  recordSuccessfulStage(state, contract, "qa", { name: "qa", status: "pass" });
  assert.equal(state.currentState, "LIVE_QA_PASSED");
  assert.equal(state.failedStage, undefined);
});

test("fresh browser QA config rejects zero checks, path drift, and missing coverage", async () => {
  const directory = await mkdtemp(join(tmpdir(), "release-browser-config-"));
  try {
    await writeFile(join(directory, "empty.json"), JSON.stringify({
      schemaVersion: "publication-qa-config-v1",
      releaseId: "ClayB-Test-20260906",
      online: { expectedLive: [{ role: "site-version" }] },
      browser: { evidencePath: ".release/qa/test.json", targets: [], scenarios: [] },
    }));
    await assert.rejects(() => loadPublicationQaConfig(directory, "empty.json"), /targets must be nonempty/);

    await writeFile(join(directory, "config.json"), JSON.stringify({
      schemaVersion: "publication-qa-config-v1",
      releaseId: "ClayB-Test-20260906",
      online: { expectedLive: [{ role: "site-version" }] },
      browser: {
        evidencePath: ".release/qa/wrong.json",
        targets: [{ id: "note" }],
        scenarios: [{ id: "desktop" }],
      },
    }));
    const contract = {
      releaseId: "ClayB-Test-20260906",
      visualQa: {
        configPath: "config.json",
        evidencePath: ".release/qa/right.json",
        requiredChecks: ["note-desktop", "note-mobile"],
      },
    };
    await assert.rejects(
      () => validateFreshBrowserQaConfig(directory, contract),
      /evidencePath|omits required check/,
    );
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("contract schemas retain legacy bind and admit HTML-only state", async () => {
  const handoffSchema = JSON.parse(await readFile(resolve(root, "release/contracts/research-publication-handoff.schema.json"), "utf8"));
  const receiptSchema = JSON.parse(await readFile(resolve(root, "release/contracts/research-publication-receipt.schema.json"), "utf8"));
  const validateSchema = new Ajv2020({ strict: false, validateFormats: false }).compile(handoffSchema);
  const legacy = JSON.parse(await readFile(baselinePath, "utf8"));
  assert.equal(validateSchema(legacy), true, JSON.stringify(validateSchema.errors));

  const htmlOnly = structuredClone(legacy);
  htmlOnly.releaseId = "ClayB-Test-20260906";
  htmlOnly.artifactPolicy = { readerPdf: "OMIT_NEW", scientificFigure: "NOT_REQUIRED" };
  htmlOnly.stages.generate.script = "scripts/generate_clay_b_test_20260906_release.py";
  htmlOnly.stages.translate.script = "scripts/add-clay-b-test-20260906-translations.mjs";
  delete htmlOnly.stages.bind;
  htmlOnly.publication.commitMessage = "Publish ClayB Test 20260906 HTML note";
  htmlOnly.publication.expectedLive = [
    { role: "homepage", localPath: "public/research-review.html", urlPath: "/", contentTypes: ["text/html"] },
    { role: "note-html", localPath: "public/notes/clay-b-test-20260906.html", urlPath: "/notes/clay-b-test-20260906.html", contentTypes: ["text/html"] },
    { role: "note-index", localPath: "public/notes/index.html", urlPath: "/notes/", contentTypes: ["text/html"] },
    { role: "site-version", localPath: "public/site-version.json", urlPath: "/site-version.json", contentTypes: ["application/json"] },
  ];
  htmlOnly.publication.expectedAbsent = ["/notes/clay-b-test-20260906.pdf"];
  htmlOnly.visualQa.configPath = "release/qa/clay-b-test-20260906.json";
  htmlOnly.visualQa.evidencePath = ".release/qa/ClayB-Test-20260906.json";
  assert.equal(validateSchema(htmlOnly), true, JSON.stringify(validateSchema.errors));

  const forbiddenBind = structuredClone(htmlOnly);
  forbiddenBind.stages.bind = legacy.stages.bind;
  assert.equal(validateSchema(forbiddenBind), false);
  const missingIndependentConfig = structuredClone(htmlOnly);
  missingIndependentConfig.artifactPolicy.readerPdf = "REQUIRED";
  missingIndependentConfig.stages.bind = {
    ...legacy.stages.bind,
    script: "scripts/bind-clay-b-test-20260906-pdfs.mjs",
  };
  delete missingIndependentConfig.visualQa.configPath;
  assert.equal(validateSchema(missingIndependentConfig), false);

  assert.ok(handoffSchema.allOf.some((rule) => rule.then?.properties?.stages?.required?.includes("bind")));
  assert.ok(handoffSchema.properties.artifactPolicy.properties.readerPdf.enum.includes("OMIT_NEW"));
  assert.ok(receiptSchema.properties.finalState.enum.includes("HTML_ARTIFACTS_BOUND"));
});

test("independent checks finish together so failures can be enumerated once", async () => {
  const checks = [
    { label: "first", executable: process.execPath, arguments_: ["-e", "process.exit(2)"] },
    { label: "second", executable: process.execPath, arguments_: ["-e", "process.exit(0)"] },
    { label: "third", executable: process.execPath, arguments_: ["-e", "process.exit(3)"] },
  ];
  const results = await runChecksCollectingFailures(root, checks);
  assert.equal(results.length, 3);
  assert.deepEqual(
    results.filter((result) => result.result.status !== 0).map((result) => result.label),
    ["first", "third"],
  );
});

test("single-entry CLI keeps destructive authority explicit", () => {
  assert.deepEqual(
    parseArguments([
      "--handoff", "release/handoffs/r073y-baseline.json", "--verify-existing", "--through", "qa",
    ]),
    {
      through: "qa",
      handoffPath: "release/handoffs/r073y-baseline.json",
      verifyExisting: true,
    },
  );
  assert.deepEqual(parseArguments(["--status", "ClayB-Test-20260906"]), {
    through: "qa",
    statusReleaseId: "ClayB-Test-20260906",
  });
  assert.throws(() => parseArguments(["--through", "qa"]), /--handoff or --status is required/);
  assert.throws(() => parseArguments(["--handoff", "x.json", "--through", "unknown"]), /unknown/);
});

test("live QA compares bytes, content type, site version, absence, and visual evidence", async () => {
  const directory = await mkdtemp(join(tmpdir(), "release-live-qa-"));
  const publicationCommit = "a".repeat(40);
  const siteVersion = JSON.stringify({ latestRelease: "R0.99Z", latestRecapRelease: "R0.99Y" }) + "\n";
  await Promise.all([
    mkdir(join(directory, "public"), { recursive: true }),
    mkdir(join(directory, ".release/qa"), { recursive: true }),
  ]);
  await writeFile(join(directory, "public/site-version.json"), siteVersion);
  await writeFile(
    join(directory, ".release/qa/r099z.json"),
    JSON.stringify({
      schemaVersion: "publication-visual-qa-v1",
      releaseId: "r099z",
      publicationCommit,
      checks: [{ id: "desktop", status: "pass" }],
      defects: [],
    }),
  );
  const server = createServer((request, response) => {
    if (request.url.startsWith("/site-version.json")) {
      response.writeHead(200, { "content-type": "application/json; charset=utf-8" });
      response.end(siteVersion);
    } else {
      response.writeHead(404, { "content-type": "text/plain" });
      response.end("not found\n");
    }
  });
  await new Promise((resolvePromise) => server.listen(0, "127.0.0.1", resolvePromise));
  try {
    const address = server.address();
    const contract = {
      releaseId: "r099z",
      publication: {
        siteBaseUrl: `http://127.0.0.1:${address.port}`,
        expectedLive: [{
          role: "site-version",
          localPath: "public/site-version.json",
          urlPath: "/site-version.json",
          contentTypes: ["application/json"],
        }],
        expectedAbsent: ["/missing.html"],
        siteVersionExpectations: {
          latestRelease: "R0.99Z",
          latestRecapRelease: "R0.99Y",
        },
      },
      visualQa: {
        evidencePath: ".release/qa/r099z.json",
        requiredChecks: ["desktop"],
      },
    };
    const result = await verifyLivePublication(directory, contract, publicationCommit);
    assert.equal(result.files[0].localSha256, result.files[0].liveSha256);
    assert.equal(result.expectedAbsent[0].statusCode, 404);
    assert.equal(result.visual.status, "pass");
  } finally {
    await new Promise((resolvePromise) => server.close(resolvePromise));
    await rm(directory, { recursive: true, force: true });
  }
});
