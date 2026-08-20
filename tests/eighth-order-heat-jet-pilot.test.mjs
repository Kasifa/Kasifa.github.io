import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const repository = new URL("..", import.meta.url).pathname;
const noteUrl = new URL(
  "../research/eighth_order_heat_jet_pilot_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/eighth_order_heat_jet_pilot.py",
  import.meta.url,
);
const archiveRoot = new URL(
  "../research/certificates/r068b2b-pilot/",
  import.meta.url,
);
const figureRoot = new URL(
  "../figures/r068b2-eighth-order-heat/fig-r068b2-eighth-order-heat/",
  import.meta.url,
);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("states the degree-eight heat-jet pilot and its proof boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);
  assert.match(note, /R0\.68B-2b pilot/);
  assert.ok(note.includes("3003\\times1792=5{,}381{,}376"));
  assert.ok(note.includes("2^6=64"));
  assert.ok(note.includes("-1.4923824320396173\\times10^{-8}"));
  assert.ok(note.includes("\\frac{16^6}{16^9}=\\frac1{4096}"));
  assert.match(note, /not yet a strict sign\s+certificate/);
  assert.match(audit, /numerical architecture and convergence pilot/);
  assert.match(audit, /does not\s+bound the zero-jet defect, the ninth derivatives/);
});

test("reproduces the low-degree moment and heat pairing", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r068b2b-jet-"));
  const output = join(scratch, "pilot.json");
  const python = process.env.CODEX_PYTHON || "python3";
  await execFileAsync(
    python,
    [
      auditUrl.pathname,
      "--output",
      output,
      "--max-degree",
      "2",
      "--heat-order",
      "48",
    ],
    { cwd: repository, maxBuffer: 20 * 1024 * 1024 },
  );
  const report = JSON.parse(await readFile(output, "utf8"));
  assert.equal(report.status, "exploratory-passed");
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.parameters.channelsPerState, 28);
  assert.equal(report.parameters.shuffleCount, 35);
  assert.ok(report.massProjection.observable < -0.02612);
  assert.ok(report.heatJet.finalPilotValue < -1.49e-8);
  assert.ok(report.heatJet.finalPilotValue > -1.51e-8);
});

test("locks the monitored degree-eight pilot archive", async () => {
  const [jsonBuffer, stdoutBuffer, stderrBuffer, resourcesBuffer, checksumText] =
    await Promise.all([
      readFile(new URL("eighth-order-heat-jet-pilot.json", archiveRoot)),
      readFile(new URL("eighth-order-heat-jet-pilot.stdout.log", archiveRoot)),
      readFile(new URL("eighth-order-heat-jet-pilot.stderr.log", archiveRoot)),
      readFile(new URL("resources.csv", archiveRoot)),
      readFile(new URL("SHA256SUMS", archiveRoot), "utf8"),
    ]);
  const report = JSON.parse(jsonBuffer.toString("utf8"));
  assert.equal(report.status, "exploratory-passed");
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.parameters.maximumJetDegree, 8);
  assert.equal(report.parameters.channelsPerState, 3003);
  assert.equal(report.parameters.totalMomentCoordinates, 5381376);
  assert.ok(report.heatJet.finalPilotValue < -1.4923e-8);
  assert.equal(report.provenance.sourceCommit.length, 40);
  assert.deepEqual(jsonBuffer, stdoutBuffer);
  assert.match(stderrBuffer.toString("utf8"), /degree=8 channels=3003/);
  assert.match(stderrBuffer.toString("utf8"), /monitor: finished returncode=0/);
  assert.match(resourcesBuffer.toString("utf8"), /exited:0/);

  const expected = new Map(
    checksumText
      .trim()
      .split("\n")
      .map((line) => {
        const [digest, name] = line.trim().split(/\s+/);
        return [name, digest];
      }),
  );
  for (const [name, buffer] of [
    ["eighth-order-heat-jet-pilot.json", jsonBuffer],
    ["eighth-order-heat-jet-pilot.stdout.log", stdoutBuffer],
    ["eighth-order-heat-jet-pilot.stderr.log", stderrBuffer],
    ["resources.csv", resourcesBuffer],
  ]) {
    assert.equal(sha256(buffer), expected.get(name));
  }
});

test("archives a mixed-evidence journal figure with an explicit boundary", async () => {
  const python = process.env.CODEX_PYTHON || "python3";
  const validator = new URL("../research/validate_figure_package.py", import.meta.url);
  const { stdout } = await execFileAsync(
    python,
    [validator.pathname, figureRoot.pathname],
    { cwd: repository },
  );
  const validation = JSON.parse(stdout);
  assert.deepEqual(validation.errors, []);
  assert.deepEqual(validation.warnings, []);
  const manifest = JSON.parse(
    await readFile(new URL("manifest.json", figureRoot), "utf8"),
  );
  assert.equal(manifest.figureId, "fig-r068b2-eighth-order-heat");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.outputs.at(-1).dpi, 600);
  assert.equal(manifest.figure.outputs.at(-1).pixels, "4204 by 2480");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.match(manifest.supportedClaim, /strictly positive/);
  assert.match(manifest.supportedClaim, /binary64 signal/);
  assert.match(manifest.claimBoundary, /exploratory/);
  assert.match(manifest.claimBoundary, /ninth derivative/);
});
