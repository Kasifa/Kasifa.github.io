import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const root = new URL("../", import.meta.url);
const research = new URL("research/", root);
const certificateRoot = new URL("certificates/r071b/", research);

async function archivedJson(name) {
  return JSON.parse(await readFile(new URL(name, certificateRoot), "utf8"));
}

function assertClose(actual, expected, tolerance = 1e-15) {
  assert.ok(
    Math.abs(actual - expected) <= tolerance,
    `${actual} differs from ${expected} by more than ${tolerance}`,
  );
}

let reproductionPromise;

function reproduceBoth() {
  reproductionPromise ??= (async () => {
    const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
    const options = {
      cwd: fileURLToPath(root),
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    };
    const [exact, independent] = await Promise.all([
      execFileAsync(
        python,
        [fileURLToPath(new URL("r071b_exact_audit.py", research))],
        options,
      ),
      execFileAsync(
        python,
        [fileURLToPath(new URL("r071b_independent_audit.py", research))],
        options,
      ),
    ]);
    return { exact, independent };
  })();
  return reproductionPromise;
}

test("locks the R0.71B report, literature audit, and mathematical boundary", async () => {
  const [report, literature, audit, producer, checker] = await Promise.all([
    readFile(new URL("r071b_report-source.md", research), "utf8"),
    readFile(new URL("r071b_literature_audit.md", research), "utf8"),
    readFile(new URL("r071b_independent_audit.md", research), "utf8"),
    readFile(new URL("r071b_exact_audit.py", research), "utf8"),
    readFile(new URL("r071b_independent_audit.py", research), "utf8"),
  ]);

  for (const token of [
    "R0.71B — Common-response packing no-go and a sign-sensitive output coefficient",
    "\\mathcal U_M\\nearrow1",
    "M^2\\mathcal C_M\\longrightarrow-\\frac12",
    "same-low-mode fan",
    "shared-high equal-radius fan",
    "polarized common-response form",
    "Theorem 7.1 — exact positive-output Cauchy--Young reduction",
    "does not supply that bound",
    "The finite checks do not prove the arbitrary-(N) resonance lemmas",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(
    report,
    /no new\s+continuation criterion and no regularity claim/i,
  );

  assert.match(literature, /not a systematic review and makes no priority claim/i);
  assert.match(literature, /positive tent is sign blind/i);
  assert.match(literature, /signed box mass is not a classical Carleson measure/i);
  assert.match(literature, /Besov criterion does not use the rejected direct estimate/i);
  assert.match(literature, /not evidence of novelty or priority/i);

  assert.match(audit, /No blocker or major mathematical inconsistency was found/);
  assert.match(audit, /polarized three-field.*not[\s\S]*one-field Besov/i);
  assert.match(
    audit,
    /finite \(N=8\) enumerations are regression certificates, not proofs of[\s\S]*arbitrary-\(N\)/i,
  );
  assert.match(audit, /No calculation[\s\S]*Navier--Stokes solution trajectory/i);

  assert.match(producer, /producer exhaustively checks N=8/);
  assert.match(producer, /do not prove a new[\s\S]*continuation criterion/i);
  assert.match(checker, /does not import any project audit module/);
  assert.match(checker, /arbitrary-N fan statements still require the analytic/i);

  assert.doesNotMatch(report, /first ever|for the first time|proves novelty/i);
  assert.doesNotMatch(report, /proves unconditional global regularity/i);
  assert.doesNotMatch(report, /solves? the Millennium problem/i);
  assert.doesNotMatch(report, /Besov continuation criterion is false/i);
});

test("reproduces both archived R0.71B finite Fourier certificates byte for byte", async () => {
  const [exactText, independentText, reproduced] = await Promise.all([
    readFile(new URL("result.json", certificateRoot), "utf8"),
    readFile(new URL("independent-result.json", certificateRoot), "utf8"),
    reproduceBoth(),
  ]);

  assert.equal(reproduced.exact.stderr, "");
  assert.equal(reproduced.independent.stderr, "");
  assert.equal(reproduced.exact.stdout, exactText);
  assert.equal(reproduced.independent.stdout, independentText);
  assert.deepEqual(JSON.parse(reproduced.exact.stdout), JSON.parse(exactText));
  assert.deepEqual(
    JSON.parse(reproduced.independent.stdout),
    JSON.parse(independentText),
  );
});

test("locks all ten finite-producer checks and the two-shell exact algebra", async () => {
  const archived = await archivedJson("result.json");

  assert.equal(archived.release, "R0.71B");
  assert.equal(
    archived.status,
    "common-response-packing-and-positive-output-gate",
  );
  assert.deepEqual(Object.keys(archived.checks).sort(), [
    "positiveOutputCauchyYoungReduction",
    "positiveSquareNotBmoEquivalent",
    "sameCovarianceSignPairSeparated",
    "sameLowFanNoL2ToL1Upgrade",
    "sameLowFanOnlyIntendedResonances",
    "sharedHighFanEqualResponse",
    "sharedHighFanOnlyIntendedResonances",
    "sharedHighFanShellSupFailure",
    "twoShellChordQuadraticDecay",
    "twoShellCommonOrderOne",
  ]);
  assert.ok(Object.values(archived.checks).every((value) => value === true));

  const atom = archived.singleHhlLedger;
  assert.equal(atom.weightedCyclicResidual, "0");
  assert.equal(atom.commonLimit, "1");
  assert.equal(atom.M2TimesChordLimit, "-1/2");
  assert.equal(atom.commonAtM4, "180*sqrt(82)/1681");
  assert.equal(atom.chordAtM4, "-9*sqrt(82)/3362");
  assert.equal(
    atom.commonDerivative,
    "sqrt(2)*(5*M**2 + 5*M + 1)/(2*M**2 + 2*M + 1)**(5/2)",
  );
  assert.match(atom.decision, /common channel stays order one/i);
});

test("locks the certified N=8 fan reconstructions without promoting them to arbitrary N proofs", async () => {
  const archived = await archivedJson("result.json");
  const independent = await archivedJson("independent-result.json");
  const same = archived.sameLowFanLedger;
  const shared = archived.sharedHighFanLedger;

  assert.equal(same.auditN, 8);
  assert.equal(same.modeCount, 34);
  assert.equal(same.orderedResonanceCount, 96);
  assert.equal(same.expectedOrderedResonanceCount, 96);
  assert.equal(same.energy, "3/2");
  assertClose(same.totalCommonWorkFloat, 0.2497261589308691);
  assertClose(same.shellWorkL2Float, 0.08829188725200199);
  assert.deepEqual(
    same.sequence.map(({ N }) => N),
    [1, 2, 4, 8],
  );
  assertClose(same.sequence.at(-1).ratio, 2.82841568691473);

  assert.equal(shared.auditN, 8);
  assert.equal(shared.modeCount, 34);
  assert.equal(shared.orderedResonanceCount, 96);
  assert.equal(shared.expectedOrderedResonanceCount, 96);
  assert.equal(shared.commonHighRadiusDigits, 87);
  assert.equal(shared.lowFrameShellSupUpper, "1");
  assert.equal(shared.lowEnergy, "4");
  assert.equal(shared.firstHighEnergy, "1/2");
  assert.equal(shared.secondHighEnergy, "1/2");
  assert.equal(shared.rootTentSquareMass, "4");
  assert.equal(shared.crossWorkResidual, "0");
  assertClose(shared.crossWorkFloat, -0.3534669874150541);
  assertClose(shared.normalizedOperatorRatioLowerFloat, 0.7069339748301082);
  assert.deepEqual(
    shared.sequence.map(({ N }) => N),
    [1, 2, 4, 8],
  );

  assert.equal(independent.release, "R0.71B");
  assert.equal(independent.status, "independent-fourier-reconstruction-passed");
  assert.deepEqual(independent.sameLowFan, {
    N: 8,
    chordWorkFloat: -0.0002189612186295775,
    commonResidual: "0",
    commonWorkFloat: 0.2497261589308691,
    modeCount: 34,
    orderedResonanceCount: 96,
  });
  assert.deepEqual(independent.sharedHighFan, {
    N: 8,
    crossResidual: "0",
    crossWorkFloat: -0.3534669874150541,
    modeCount: 34,
    orderedResonanceCount: 96,
  });

  assert.ok(
    archived.analyticDependencies.some((entry) =>
      entry.includes("producer exhaustively checks N=8"),
    ),
  );
  assert.ok(
    independent.claimBoundary.some((entry) =>
      entry.includes("arbitrary-N fan statements still require"),
    ),
  );
  assert.ok(
    independent.claimBoundary.some((entry) =>
      entry.includes("finite N=8 instances"),
    ),
  );
});

test("locks the sign-sensitive positive-output consumer and its non-BMO example", async () => {
  const archived = await archivedJson("result.json");
  const independent = await archivedJson("independent-result.json");
  const positive = archived.positiveOutputLedger;

  assert.equal(positive.r071aPositive.positiveSquare, "9/800");
  assert.equal(positive.r071aPositive.energy, "299553/2");
  assert.equal(
    positive.r071aPositive.normalizedCoefficient,
    "3/39940400",
  );
  assert.deepEqual(positive.r071aPositive.signedOutputs, [
    { frequency: [1, 0, 1], work: "3*sqrt(2)/40" },
  ]);
  assert.equal(positive.r071aNegative.positiveSquare, "0");
  assert.equal(positive.r071aNegative.normalizedCoefficient, "0");
  assert.deepEqual(positive.r071aNegative.signedOutputs, [
    { frequency: [1, 0, 1], work: "-3*sqrt(2)/40" },
  ]);
  assert.deepEqual(positive.planeWave, {
    covarianceWork: "0",
    energy: "1/2",
    frequency: [7, 0, 0],
    positiveSquare: "0",
  });
  assert.equal(
    positive.youngResidualSquare,
    "(sqrt(nu*D)/2-T/sqrt(nu))^2",
  );
  assert.match(positive.decision, /no energy or NSE propagation bound/i);

  assert.equal(independent.r071aPositiveOutput.positiveSquare, "9/800");
  assert.equal(
    independent.r071aPositiveOutput.normalized,
    "3/39940400",
  );
  assert.equal(independent.r071aNegativeOutput.positiveSquare, "0");
  assert.equal(independent.r071aNegativeOutput.normalized, "0");
});

test("locks the continuation, literature, and Millennium-problem claim boundary", async () => {
  const archived = await archivedJson("result.json");
  const boundary = archived.claimBoundary.join("\n");

  assert.match(boundary, /common response can remain order one/i);
  assert.match(boundary, /direct polarized shell-supremum times L2 times L2/i);
  assert.match(boundary, /does not rule out the established vorticity BMO or Besov/i);
  assert.match(boundary, /ordinary positive square tent is sign blind/i);
  assert.match(boundary, /does not derive its time integrability/i);
  assert.match(boundary, /does not prove a new continuation criterion/i);
  assert.match(boundary, /does not[\s\S]*solve the Millennium problem/i);
});

test("verifies every listed R0.71B payload and source lock by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");
  const paths = lines.map((line) => line.slice(66));

  for (const required of [
    "README.md",
    "command.txt",
    "environment.txt",
    "result.json",
    "independent-result.json",
    "../../r071b_exact_audit.py",
    "../../r071b_independent_audit.py",
  ]) {
    assert.ok(paths.includes(required), `missing checksum lock: ${required}`);
  }
  assert.equal(new Set(paths).size, paths.length, "checksum paths must be unique");

  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
