import assert from "node:assert/strict";
import { createServer } from "node:http";
import { mkdtemp, mkdir, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";
import test from "node:test";

import { parseArguments } from "../scripts/publish-release.mjs";
import {
  STATE_AFTER_STAGE,
  STAGES,
  fingerprintPaths,
  runChecksCollectingFailures,
  validateHandoff,
  verifyFrozenArtifacts,
  verifyLivePublication,
} from "../scripts/release-pipeline-lib.mjs";

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
  assert.throws(() => parseArguments(["--through", "qa"]), /--handoff is required/);
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
