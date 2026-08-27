import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import {
  copyFile,
  mkdtemp,
  readFile,
  readdir,
  rm,
  writeFile,
} from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, join, resolve, sep } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.CODEX_PYTHON || "python3";
const node = process.env.CODEX_NODE || process.execPath;
const certificate = resolve(root, "research/certificates/r072r");
const figure = resolve(
  root,
  "figures/r072r-caustic-free-core/fig-r072r-caustic-free-core",
);
const execFileAsync = promisify(execFile);

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function run(executable, arguments_, options = {}) {
  return execFileAsync(executable, arguments_, {
    cwd: root,
    maxBuffer: 16 * 1024 * 1024,
    ...options,
  });
}

async function verifyFlatHashLedger(directory) {
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd()
    .split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    const [, expected, name] = match;
    const target = resolve(directory, name);
    assert.ok(target.startsWith(directory + sep), `ledger path escapes: ${name}`);
    assert.equal(
      createHash("sha256").update(await readFile(target)).digest("hex"),
      expected,
      name,
    );
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries
      .filter(
        (entry) =>
          entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name),
      )
      .map((entry) => entry.name)
      .sort(),
  );
  return names;
}

test("R0.72R report proves only the declared four-real-dimensional caustic-free core", async () => {
  const report = await text("research/r072r_report-source.md");
  for (const token of [
    "a four-real-dimensional caustic-free core beyond the \\(Q_2\\le 1/2\\) cone",
    "\\left|z_2-\\frac3{20}\\right|\\le\\frac1{100}",
    "|z_3|\\le\\frac1{1000}",
    "=\\frac{14}{25}",
    "N_{\\rm crit}=2",
    "r=\\frac\\pi{48}",
    "\\mathfrak C_0=144",
    "\\mathfrak C_1=240",
    "\\frac{20489}{256000}<\\frac12",
    "\\frac18u^{-3}-\\frac38u^{-1}",
    "\\exists |u|=1:\\quad D(u)=D'(u)=0",
    "\\frac1{15}\\le b\\le\\frac13",
    "R0.72S should move from a safe core to the wall itself",
    "Clay problem",
  ]) assert.ok(report.includes(token), token);
  assert.match(
    report,
    /\\eta_\{\\rm CH\}[\s\S]{0,80}2,[\s\S]{0,80}\\frac\\pi\{48\},[\s\S]{0,80}144,[\s\S]{0,80}240,[\s\S]{0,80}\\frac\{161\}\{25\}/,
    "the Coble--He threshold must receive the complete shape/derivative tuple",
  );
  assert.match(report, /complete four-dimensional caustic stratification[\s\S]*not claimed/i);
  assert.match(
    report,
    /old [^\n]*Q_2=1\/2[^\n]* boundary exactly once[\s\S]*crossing is not a caustic/,
  );
  assert.match(
    report,
    /No constant uniform as \\\(\\beta_-\\downarrow0\\\) is claimed/,
  );
  assert.match(report, /not a theorem stated verbatim in their paper/);
  assert.doesNotMatch(report, /(?:complete four-dimensional chamber|general three-dimensional).*CLOSED/i);
});

test("producer, BigInt audit, and comparator preserve independent finite-algebra routes", async () => {
  const [producer, independent, comparator] = await Promise.all([
    text("research/r072r_exact_audit.py"),
    text("research/r072r_independent_audit.mjs"),
    text("research/r072r_compare_audits.py"),
  ]);
  assert.match(producer, /from fractions import Fraction/);
  assert.match(producer, /def determinant_bareiss\(/);
  assert.match(producer, /exactGridEvaluations/);
  assert.match(independent, /Independent BigInt audit/);
  assert.match(independent, /function determinantBareiss\(/);
  assert.match(independent, /exactGridEvaluations/);
  assert.doesNotMatch(
    independent,
    /r072r_exact_audit|producer-(?:config|payload|result|progress|resource|monitor)/,
  );
  assert.doesNotMatch(
    producer,
    /r072r_independent_audit|independent-(?:config|payload|result|progress|resource|monitor)/,
  );
  for (const pattern of [
    /center_z2 = Fraction\(3, 20\)/,
    /radius_z2 = Fraction\(1, 100\)/,
    /radius_z3 = Fraction\(1, 1000\)/,
    /q2_y1_upper == Fraction\(20489, 256000\)/,
    /boundary_margin == Fraction\(3047, 1536000\)/,
    /normalized_curvature == Fraction\(1517, 4500\)/,
    /derivative_sum == Fraction\(161, 25\)/,
    /eta = Fraction\(3, 7\) \*\* 4/,
    /"completeThresholdAlsoRequiresEtaCH": True/,
    /"gammaFixedZ3Coefficients": \["1\/8", "-3\/8", "-15\/8", "-3\/8"\]/,
    /"tensorGridIdentityProof": checked == 121/,
    /"uniformThirdCarrierAmplitudeFloor": False/,
  ]) assert.match(producer, pattern, `producer exact construction: ${pattern}`);
  for (const pattern of [
    /const centerZ2 = fraction\(3n, 20n\)/,
    /const radiusZ2 = fraction\(1n, 100n\)/,
    /const radiusZ3 = fraction\(1n, 1000n\)/,
    /same\(q2Y1Upper, fraction\(20489n, 256000n\)\)/,
    /same\(boundaryMargin, fraction\(3047n, 1536000n\)\)/,
    /same\(normalizedCurvature, fraction\(1517n, 4500n\)\)/,
    /same\(derivativeSum, fraction\(161n, 25n\)\)/,
    /const eta = power\(fraction\(3n, 7n\), 4\)/,
    /completeThresholdAlsoRequiresEtaCH: true/,
    /gammaFixedZ3Coefficients: \["1\/8", "-3\/8", "-15\/8", "-3\/8"\]/,
    /tensorGridIdentityProof: checked === 121/,
    /uniformThirdCarrierAmplitudeFloor: false/,
  ]) assert.match(independent, pattern, `BigInt exact construction: ${pattern}`);
  for (const token of [
    'polydisc.get("centerZ2") == "3/20"',
    'polydisc.get("radiusZ2") == "1/100"',
    'polydisc.get("radiusZ3") == "1/1000"',
    'heat.get("q2AtY1UpperUsingEGreaterThanTwo") == "20489/256000"',
    'geometry.get("boundarySignMargin") == "3047/1536000"',
    'geometry.get("normalizedCurvatureLower") == "1517/4500"',
    'derivatives.get("sumW3Infinity") == "161/25"',
    'derivatives.get("slowEtaSymbolic") == "(3/7)^4"',
    'derivatives.get("completeThresholdAlsoRequiresEtaCH") is True',
    'incidence.get("gammaFixedZ3Coefficients")',
    'real_slice.get("tensorGridIdentityProof") is True',
    'boundary.get("uniformThirdCarrierAmplitudeFloor") is False',
  ]) assert.ok(comparator.includes(token), `comparator canonical claim: ${token}`);
});

test("temporary dual routes agree exactly but cannot be sealed as a formal certificate", async (t) => {
  const directory = await mkdtemp(join(tmpdir(), "r072r-audit-"));
  t.after(() => rm(directory, { recursive: true, force: true }));

  await run(python, [
    "research/r072r_exact_audit.py",
    "--output-dir",
    directory,
  ]);
  await run(node, [
    "research/r072r_independent_audit.mjs",
    "--output-dir",
    directory,
  ]);
  await run(python, [
    "research/r072r_compare_audits.py",
    "--certificate-dir",
    directory,
    "--allow-unsealed-source",
  ]);

  const producerPayload = JSON.parse(
    await readFile(join(directory, "producer-payload.json"), "utf8"),
  );
  const independentPayload = JSON.parse(
    await readFile(join(directory, "independent-payload.json"), "utf8"),
  );
  const crosscheck = JSON.parse(
    await readFile(join(directory, "crosscheck.json"), "utf8"),
  );
  assert.deepEqual(producerPayload, independentPayload);
  assert.equal(
    producerPayload.theoremId,
    "R0.72R-four-real-dimensional-caustic-free-core",
  );
  assert.deepEqual(producerPayload.polydisc, {
    absZ2Range: ["7/50", "4/25"],
    centerZ2: "3/20",
    nonemptyInterior: true,
    radiusZ2: "1/100",
    radiusZ3: "1/1000",
    realDimension: 4,
  });
  assert.deepEqual(
    {
      initial: producerPayload.heatPath.q2InitialLower,
      exit: producerPayload.heatPath.coneExitMargin,
      y1: producerPayload.heatPath.q2AtY1UpperUsingEGreaterThanTwo,
      unique: producerPayload.heatPath.uniqueOldConeCrossingOnZeroOne,
    },
    { initial: "14/25", exit: "3/50", y1: "20489/256000", unique: true },
  );
  assert.deepEqual(
    {
      radius: producerPayload.shapeContract.radius,
      count: producerPayload.shapeContract.criticalCount,
      C0: producerPayload.shapeContract.C0,
      C1: producerPayload.shapeContract.C1,
      normalized: producerPayload.shapeContract.normalizedLocalSlope,
      physical: producerPayload.shapeContract.physicalLocalSlope,
    },
    {
      radius: "pi/48",
      count: 2,
      C0: "144/1",
      C1: "240/1",
      normalized: ["1/4", "5/3"],
      physical: ["1/12", "5/3"],
    },
  );
  assert.deepEqual(
    producerPayload.incidence.gammaFixedZ3Coefficients,
    ["1/8", "-3/8", "-15/8", "-3/8"],
  );
  assert.deepEqual(
    producerPayload.incidence.gammaFixedZ3Exponents,
    [-3, -1, 1, -5],
  );
  assert.equal(producerPayload.realSlice.exactGridEvaluations, 121);
  assert.equal(producerPayload.realSlice.tensorGridIdentityProof, true);
  assert.equal(
    producerPayload.claimBoundary.completeFourDimensionalChamberClassification,
    false,
  );
  assert.equal(
    producerPayload.claimBoundary.uniformThirdCarrierAmplitudeFloor,
    false,
  );
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.checks.canonicalPayloadsIdentical, true);
  assert.equal(crosscheck.checks.physicalShapeContractExact, true);
  assert.equal(crosscheck.checks.complexIncidenceExact, true);
  assert.equal(crosscheck.checks.realSliceExact, true);
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, true);

  const scaffold = resolve(root, "research/certificates/r072r");
  for (const name of [
    "README.md",
    "command.txt",
    "write_environment.py",
    "build_hashes.py",
  ]) await copyFile(resolve(scaffold, name), join(directory, name));
  await run(python, [join(directory, "write_environment.py")], {
    env: { ...process.env, R072R_NODE: node },
  });
  for (const key of Object.keys(crosscheck.checks)) crosscheck.checks[key] = true;
  await writeFile(
    join(directory, "crosscheck.json"),
    `${JSON.stringify(crosscheck, null, 2)}\n`,
  );
  await assert.rejects(
    run(python, [join(directory, "build_hashes.py")]),
    /temporary R0\.72R crosscheck cannot be formally hashed/,
  );

  for (const route of ["producer", "independent"]) {
    const target = join(directory, `${route}-config.json`);
    const config = JSON.parse(await readFile(target, "utf8"));
    config.sourceTracked = true;
    config.trackedChangesDirty = false;
    await writeFile(target, `${JSON.stringify(config, null, 2)}\n`);
  }
  crosscheck.temporaryUnsealedSourceAllowed = false;
  await writeFile(
    join(directory, "crosscheck.json"),
    `${JSON.stringify(crosscheck, null, 2)}\n`,
  );
  await run(python, [join(directory, "build_hashes.py")]);
  const names = await verifyFlatHashLedger(directory);
  assert.equal(names.length, 18);

  await writeFile(join(directory, "unexpected.txt"), "must fail\n");
  await assert.rejects(
    run(python, [join(directory, "build_hashes.py")]),
    /unexpected certificate artifacts: unexpected\.txt/,
  );
});

test("formal command and certificate directory remain fail closed across source and release stages", async () => {
  const [command, readme, builder, manifest] = await Promise.all([
    text("research/certificates/r072r/command.txt"),
    text("research/certificates/r072r/README.md"),
    text("research/certificates/r072r/build_hashes.py"),
    json("research/release-manifest.json"),
  ]);
  assert.doesNotMatch(command, /allow-unsealed-source/);
  assert.ok(command.indexOf("r072r_exact_audit.py") < command.indexOf("r072r_independent_audit.mjs"));
  assert.ok(command.indexOf("r072r_compare_audits.py") < command.indexOf("write_environment.py"));
  assert.ok(command.indexOf("write_environment.py") < command.indexOf("build_hashes.py"));
  assert.match(readme, /do not replace the\s+continuum root-localization argument/);
  assert.match(readme, /uniform third-carrier\s+amplitude floor/);
  assert.match(builder, /temporary R0\.72R crosscheck cannot be formally hashed/);
  assert.match(builder, /unexpected certificate artifacts/);

  const names = (await readdir(certificate, { withFileTypes: true }))
    .filter((entry) => entry.isFile())
    .map((entry) => entry.name)
    .sort();
  assert.ok(["r072q", "r072r"].includes(manifest.latestCompletedRelease));
  if (manifest.latestCompletedRelease === "r072q") {
    assert.equal(manifest.nextRelease, "r072r");
    assert.deepEqual(names, [
      "README.md",
      "build_hashes.py",
      "command.txt",
      "write_environment.py",
    ]);
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072r");
  const ledgerNames = await verifyFlatHashLedger(certificate);
  assert.equal(ledgerNames.length, 18);
  const crosscheck = JSON.parse(
    await readFile(resolve(certificate, "crosscheck.json"), "utf8"),
  );
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.ok(Object.values(crosscheck.checks).every((value) => value === true));
});

test("R0.72R figure contract is source-only until the sealed formal package exists", async () => {
  const [manifest, contract, config, plot, validator, builder] = await Promise.all([
    json("research/release-manifest.json"),
    json("figures/r072r-caustic-free-core/fig-r072r-caustic-free-core/contract.json"),
    json("figures/r072r-caustic-free-core/fig-r072r-caustic-free-core/config.json"),
    text("figures/r072r-caustic-free-core/fig-r072r-caustic-free-core/plot.py"),
    text("figures/r072r-caustic-free-core/fig-r072r-caustic-free-core/validate.py"),
    text("figures/r072r-caustic-free-core/fig-r072r-caustic-free-core/build_manifest.py"),
  ]);
  assert.equal(contract.schemaVersion, "r072r-figure-contract-v1");
  assert.match(contract.title, /certified core beyond the weighted-jet cone/i);
  assert.match(contract.supportedTakeaway, /Q2>=14\/25>1\/2/);
  assert.match(contract.supportedTakeaway, /\(r,C0,C1\)=\(pi\/48,144,240\)/);
  assert.match(contract.claimBoundary, /complete four-dimensional caustic/);
  assert.match(contract.claimBoundary, /uniform third-carrier amplitude floor/);
  assert.deepEqual(
    {
      center: config.parameters.centerZ2,
      r2: config.parameters.radiusZ2,
      r3: config.parameters.radiusZ3,
      initial: config.parameters.q2InitialLower,
      y1: config.parameters.q2Y1Upper,
      C0: config.parameters.shapeC0,
      C1: config.parameters.shapeC1,
      slow: config.parameters.slowEta,
      derivatives: config.parameters.derivativeSum,
    },
    {
      center: 0.15,
      r2: 0.01,
      r3: 0.001,
      initial: 0.56,
      y1: 0.08003515625,
      C0: 144,
      C1: 240,
      slow: 81 / 2401,
      derivatives: 6.44,
    },
  );
  for (const source of [plot, validator, builder]) {
    assert.match(source, /temporaryUnsealedSourceAllowed/);
  }
  assert.match(plot, /"formalSourceReady": True/);
  assert.match(
    validator,
    /all\(value is True for value in cross\.values\(\)\)/,
  );
  assert.match(builder, /checks\.get\("formalSourceReady"\) is not True/);
  assert.match(builder, /R072R_VISUAL_QA_INSPECTED/);
  assert.match(builder, /publicCopiesComplete/);

  const names = await readdir(figure);
  for (const required of [
    "README.md",
    "build_manifest.py",
    "caption.md",
    "certificate_ledger.py",
    "command.txt",
    "config.json",
    "contract.json",
    "figure-contract.md",
    "plot.py",
    "publish_assets.py",
    "qa_images.py",
    "requirements.txt",
    "validate.py",
  ]) assert.ok(names.includes(required), required);
  const formalFiles = [
    "manifest.json",
    "results.json",
    "validation.json",
    "SHA256SUMS",
    "figure.pdf",
    "figure.svg",
    "figure.png",
  ];
  if (manifest.latestCompletedRelease === "r072q") {
    for (const forbidden of formalFiles) {
      assert.equal(names.includes(forbidden), false, forbidden);
    }
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072r");
  for (const required of formalFiles) assert.ok(names.includes(required), required);
  const packageNames = await verifyFlatHashLedger(figure);
  const figureManifest = JSON.parse(
    await readFile(resolve(figure, "manifest.json"), "utf8"),
  );
  assert.equal(figureManifest.release, "R0.72R");
  assert.equal(figureManifest.figureId, "fig-r072r-caustic-free-core");
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  const { stdout } = await run(python, [
    "research/validate_figure_package.py",
    figure,
  ]);
  assert.deepEqual(JSON.parse(stdout).errors, []);
  for (const suffix of ["pdf", "png", "svg"]) {
    assert.ok(packageNames.includes(`figure.${suffix}`));
    const master = await readFile(resolve(figure, `figure.${suffix}`));
    const published = await readFile(
      resolve(root, `public/assets/r072r/fig-r072r-caustic-free-core.${suffix}`),
    );
    assert.equal(Buffer.compare(master, published), 0, `${suffix} public byte identity`);
  }
});
