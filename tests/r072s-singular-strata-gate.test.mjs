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
const certificate = resolve(root, "research/certificates/r072s");
const figure = resolve(
  root,
  "figures/r072s-heat-collisions/fig-r072s-heat-collisions",
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

test("R0.72S source proves only the incidence-preimage strata and two declared heat collisions", async () => {
  const [report, literature, gaps, independentAudit] = await Promise.all([
    text("research/r072s_report-source.md"),
    text("research/r072s_literature_audit.md"),
    text("research/r072s_gap_matrix.md"),
    text("research/r072s_independent_audit.md"),
  ]);
  for (const token of [
    "classification of **incidence preimages**",
    "restricted miniversal (\\(R^+\\)-versal) unfolding through \\(A_5\\)",
    "not the order-zero-through-three Wronskian",
    "\\boxed{\\det W_0=5400.}",
    "z_{20}=4i",
    "z_{30}=0",
    "4/3/2",
    "4/2/2",
    "\\partial_yF=\\partial_\\phi^2F+F",
    "\\xi_\\pm=\\pm\\sqrt{-2\\delta}",
    "\\phi_\\pm=\\pm\\sqrt{-6\\delta}",
    "The next defensible gate is R0.72T",
    "remains low",
  ]) assert.ok(report.includes(token), token);
  assert.match(report, /full miniversal\s+unfolding of \\\(A_5\\\)/);
  assert.match(report, /one additional constant parameter/);
  assert.match(report, /Counting multiplicity[\s\S]{0,120}total count four/);
  assert.match(report, /transversely \*\*inside the real-even[\s\S]*not called transverse in the full coefficient space/);
  assert.match(report, /not a global classification of the image/);
  assert.match(report, /enhanced dissipation uniformly through an \\\(A_2\\\) or \\\(A_3\\\) collision/);
  assert.doesNotMatch(report, /complete four-dimensional caustic image.*(?:proved|closed)/i);
  assert.doesNotMatch(report, /(?:Clay|Millennium).*(?:solved|partial solution)/i);

  for (const source of [report, literature]) {
    assert.match(source, /978-1-4612-4122-5_4/);
    assert.doesNotMatch(source, /978-1-4612-4122-5_8/);
  }
  assert.match(literature, /restricted miniversal, or \\\(R\^\+\\\)-versal/);
  assert.match(literature, /bounded-search absence, not novelty/);
  assert.match(literature, /does not supply a global stratification of the/);
  assert.match(literature, /None of these results by itself classifies the image self-intersections/);
  assert.match(gaps, /Counting multiplicity gives four at the crossing/);
  assert.match(gaps, /Full miniversality including the function-value direction needs one additional constant parameter/);
  assert.match(independentAudit, /count and transversality ledger fields are computed from/);
  assert.match(independentAudit, /not the finite programs[—-]deduce the/);
});

test("Fraction producer, BigInt audit, comparator, and sealer lock the latest canonical schema", async () => {
  const [producer, independent, comparator, builder] = await Promise.all([
    text("research/r072s_exact_audit.py"),
    text("research/r072s_independent_audit.mjs"),
    text("research/r072s_compare_audits.py"),
    text("research/certificates/r072s/build_hashes.py"),
  ]);
  assert.match(producer, /from fractions import Fraction/);
  assert.match(producer, /def determinant\(/);
  assert.match(independent, /Independent BigInt audit/);
  assert.match(independent, /function determinantBareiss\(/);
  assert.doesNotMatch(
    producer,
    /r072s_independent_audit|independent-(?:config|payload|result|progress|resource|monitor)/,
  );
  assert.doesNotMatch(
    independent,
    /r072s_exact_audit|producer-(?:config|payload|result|progress|resource|monitor)/,
  );

  for (const token of [
    '"restrictedMiniversality": {',
    '"coefficientDerivativeJetDeterminant": rational(coefficient_jet_det)',
    '"moduloAdditiveConstants": True',
    '"fullA5MiniversalParameterCountIncludingConstant": 5',
    '"uniqueDegenerateEventForYNonnegative": a2_unique_event_inputs',
    '"distinctCriticalCounts": a2_distinct_counts',
    '"criticalCountWithMultiplicityAtCrossing": a2_multiplicity_count',
    '"allNoncollisionCriticalPointsSimple": a2_noncollision_simple',
    '"distinctCriticalCounts": a3_distinct_counts',
    '"criticalCountWithMultiplicityAtCrossing": a3_multiplicity_count',
    '"realEvenSliceTransverse": a3_slice_transverse',
    '"globalSignGuards": {',
    '"heatEquationIdentity": {',
    '"harmonicDecayExponents": {"n1": 0, "n2": 3, "n3": 8}',
  ]) assert.ok(producer.includes(token), `producer schema: ${token}`);
  for (const token of [
    "restrictedMiniversality: {",
    "coefficientDerivativeJetDeterminant: textFraction(fraction(coefficientJetDeterminant))",
    "moduloAdditiveConstants: true",
    "fullA5MiniversalParameterCountIncludingConstant: 5",
    "uniqueDegenerateEventForYNonnegative: a2UniqueEventInputs",
    "distinctCriticalCounts: a2DistinctCounts",
    "criticalCountWithMultiplicityAtCrossing: a2MultiplicityCount",
    "allNoncollisionCriticalPointsSimple: a2NoncollisionSimple",
    "distinctCriticalCounts: a3DistinctCounts",
    "criticalCountWithMultiplicityAtCrossing: a3MultiplicityCount",
    "realEvenSliceTransverse: a3SliceTransverse",
    "globalSignGuards: {",
    "heatEquationIdentity: {",
    "harmonicDecayExponents: { n1: 0, n2: 3, n3: 8 }",
  ]) assert.ok(independent.includes(token), `independent schema: ${token}`);
  assert.doesNotMatch(producer, /"uniqueDegenerateEventForYNonnegative": True/);
  assert.doesNotMatch(producer, /"allNoncollisionCriticalPointsSimple": True/);
  assert.doesNotMatch(producer, /"fullCoefficientSpaceTransverse": True/);
  assert.doesNotMatch(producer, /"distinctCriticalCounts": \{"before": 4/);
  assert.doesNotMatch(producer, /"criticalCountWithMultiplicityAtCrossing": 4/);
  assert.doesNotMatch(independent, /uniqueDegenerateEventForYNonnegative: true/);
  assert.doesNotMatch(independent, /allNoncollisionCriticalPointsSimple: true/);
  assert.doesNotMatch(independent, /realEvenSliceTransverse: true/);
  assert.doesNotMatch(independent, /distinctCriticalCounts: \{ before: 4/);
  assert.doesNotMatch(independent, /criticalCountWithMultiplicityAtCrossing: 4/);
  for (const token of [
    'payload.get("restrictedMiniversality", {})',
    'miniversality.get("coefficientDerivativeJetDeterminant") == "5400/1"',
    'a2.get("distinctCriticalCounts")',
    'a3.get("distinctCriticalCounts")',
    'a2.get("criticalCountWithMultiplicityAtCrossing") == 4',
    'a3.get("criticalCountWithMultiplicityAtCrossing") == 4',
    '"a2FiniteGuardInputsExact": a2.get("globalSignGuards") ==',
    '"a3FiniteGuardInputsExact": a3.get("globalSignGuards") ==',
    'payload.get("heatEquationIdentity", {})',
  ]) assert.ok(comparator.includes(token), `comparator schema: ${token}`);
  for (const token of [
    "REQUIRED_CROSSCHECK_CHECKS",
    '"restrictedMiniversalityExact"',
    '"a2DerivedLedgerConsistent"',
    '"a2FiniteGuardInputsExact"',
    '"a3DerivedLedgerConsistent"',
    '"a3FiniteGuardInputsExact"',
    '"heatEquationIdentityExact"',
    "R0.72S crosscheck uses a stale schema",
    "temporary R0.72S crosscheck cannot be formally hashed",
    "unexpected certificate artifacts",
  ]) assert.ok(builder.includes(token), `sealer schema: ${token}`);
});

test("temporary dual exact routes agree, expose every new guard, and remain unsealable", async (t) => {
  const directory = await mkdtemp(join(tmpdir(), "r072s-audit-"));
  t.after(() => rm(directory, { recursive: true, force: true }));

  await Promise.all([
    run(python, ["research/r072s_exact_audit.py", "--output-dir", directory]),
    run(node, ["research/r072s_independent_audit.mjs", "--output-dir", directory]),
  ]);
  await run(python, [
    "research/r072s_compare_audits.py",
    "--certificate-dir",
    directory,
    "--allow-unsealed",
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
    "R0.72S-exact-Ak-strata-and-two-heat-collisions",
  );
  assert.ok(Object.values(producerPayload.exactChecks).every(Boolean));
  assert.deepEqual(producerPayload.restrictedMiniversality, {
    coefficientDerivativeJetAtPhiZero: [
      [0, -2, 0, -3],
      [-4, 0, -9, 0],
      [0, 8, 0, 27],
      [16, 0, 81, 0],
    ],
    coefficientDerivativeJetDeterminant: "5400/1",
    coefficientOrder: ["Re(z2)", "Im(z2)", "Re(z3)", "Im(z3)"],
    derivativeOrders: [1, 2, 3, 4],
    fullA5MiniversalParameterCountIncludingConstant: 5,
    globalEmbeddedStratificationClaimed: false,
    localCodimensions: { A2: 1, A3: 2, A4: 3, A5: 4 },
    moduloAdditiveConstants: true,
  });
  assert.deepEqual(producerPayload.a2HeatPath.distinctCriticalCounts, {
    before: 4, at: 3, after: 2,
  });
  assert.deepEqual(producerPayload.a2HeatPath.crossingPowerIdentity, {
    tau: "1/2", "8TauCubed": "1/1",
  });
  assert.deepEqual(producerPayload.a2HeatPath.representativeK, {
    before: "2/1", at: "1/1", after: "1/2",
  });
  assert.equal(producerPayload.a2HeatPath.kLogDerivative, "-3/1");
  assert.equal(producerPayload.a2HeatPath.uniqueDegenerateEventForYNonnegative, true);
  assert.equal(producerPayload.a2HeatPath.fullCoefficientSpaceTransverse, true);
  assert.equal(producerPayload.a2HeatPath.criticalCountWithMultiplicityAtCrossing, 4);
  assert.deepEqual(producerPayload.a2HeatPath.globalSignGuards, {
    offAxisDegeneracyAfterMultiplyBy8k: {
      constant: "-1/1", kSquared: "-8/1",
    },
    pAtMinusOne: { constant: "1/1", k: "1/1" },
    pAtOne: { constant: "-1/1", k: "1/1" },
    pAtZero: { k: "-1/1" },
    rootProduct: "-1/2",
  });
  assert.deepEqual(producerPayload.a3HeatPath.distinctCriticalCounts, {
    before: 4, at: 2, after: 2,
  });
  assert.deepEqual(producerPayload.a3HeatPath.crossingPowerIdentities, {
    tauCubed: "1/8", tauEighth: "1/256",
  });
  assert.deepEqual(producerPayload.a3HeatPath.representativeTau, {
    before: "3/4", at: "1/2", after: "1/4",
  });
  assert.equal(producerPayload.a3HeatPath.realEvenSliceTransverse, true);
  assert.equal(producerPayload.a3HeatPath.fullCoefficientSpaceTransverse, false);
  assert.equal(producerPayload.a3HeatPath.criticalCountWithMultiplicityAtCrossing, 4);
  assert.deepEqual(producerPayload.a3HeatPath.globalSignGuards, {
    hTauDerivativeParentAtTauOne: "-2307/1280",
    qMinusOneCoefficients: ["1/1", "2563/320", "3/10"],
    qXUpperParentAtTauOne: "-2307/1280",
  });
  assert.deepEqual(producerPayload.heatEquationIdentity, {
    harmonicDecayExponents: { n1: 0, n2: 3, n3: 8 },
    identity: "partial_y F=partial_phi^2 F+F",
    onIncidence: ["partial_y F'=F'''", "partial_y F''=F''''"],
  });
  assert.equal(crosscheck.status, "passed");
  for (const name of [
    "canonicalPayloadsIdentical",
    "restrictedMiniversalityExact",
    "a2DerivedLedgerConsistent",
    "a2FiniteGuardInputsExact",
    "a3DerivedLedgerConsistent",
    "a3FiniteGuardInputsExact",
    "heatEquationIdentityExact",
  ]) assert.equal(crosscheck.checks[name], true, name);
  assert.equal(crosscheck.checks.formalSourceReady, false);
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, true);

  const scaffold = resolve(root, "research/certificates/r072s");
  for (const name of ["README.md", "command.txt", "write_environment.py", "build_hashes.py"]) {
    await copyFile(resolve(scaffold, name), join(directory, name));
  }
  await run(python, [join(directory, "write_environment.py")], {
    env: { ...process.env, R072S_NODE: node },
  });
  for (const key of Object.keys(crosscheck.checks)) crosscheck.checks[key] = true;
  await writeFile(
    join(directory, "crosscheck.json"),
    `${JSON.stringify(crosscheck, null, 2)}\n`,
  );
  await assert.rejects(
    run(python, [join(directory, "build_hashes.py")]),
    /temporary R0\.72S crosscheck cannot be formally hashed/,
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
  assert.equal((await verifyFlatHashLedger(directory)).length, 18);

  await writeFile(join(directory, "unexpected.txt"), "must fail\n");
  await assert.rejects(
    run(python, [join(directory, "build_hashes.py")]),
    /unexpected certificate artifacts: unexpected\.txt/,
  );
});

test("formal certificate command remains fail closed across source and release stages", async () => {
  const [command, readme, builder, manifest] = await Promise.all([
    text("research/certificates/r072s/command.txt"),
    text("research/certificates/r072s/README.md"),
    text("research/certificates/r072s/build_hashes.py"),
    json("research/release-manifest.json"),
  ]);
  assert.doesNotMatch(command, /allow-unsealed(?:-source)?/);
  assert.ok(command.indexOf("r072s_exact_audit.py") < command.indexOf("r072s_independent_audit.mjs"));
  assert.ok(command.indexOf("r072s_compare_audits.py") < command.indexOf("write_environment.py"));
  assert.ok(command.indexOf("write_environment.py") < command.indexOf("build_hashes.py"));
  assert.match(readme, /continuous argument[\s\S]{0,160}not this finite computation/);
  assert.match(readme, /deduces event uniqueness, global[\s\S]{0,100}transversality/);
  assert.match(readme, /does not certify a global embedded caustic stratification/);
  assert.match(builder, /R0\.72S crosscheck uses a stale schema/);
  assert.match(builder, /temporary R0\.72S crosscheck cannot be formally hashed/);

  const names = (await readdir(certificate, { withFileTypes: true }))
    .filter((entry) => entry.isFile())
    .map((entry) => entry.name)
    .sort();
  assert.ok(["r072r", "r072s"].includes(manifest.latestCompletedRelease));
  if (manifest.latestCompletedRelease === "r072r") {
    assert.equal(manifest.nextReleaseSourceStage?.release, "r072s");
    assert.deepEqual(names, [
      "README.md",
      "build_hashes.py",
      "command.txt",
      "write_environment.py",
    ]);
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072s");
  assert.equal((await verifyFlatHashLedger(certificate)).length, 18);
  const crosscheck = await json("research/certificates/r072s/crosscheck.json");
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.ok(Object.values(crosscheck.checks).every((value) => value === true));
});

test("R0.72S figure scaffold is source-only until its sealed package and public copies coexist", async () => {
  const [manifest, contract, config, caption, readme, plot, validator, builder] = await Promise.all([
    json("research/release-manifest.json"),
    json("figures/r072s-heat-collisions/fig-r072s-heat-collisions/contract.json"),
    json("figures/r072s-heat-collisions/fig-r072s-heat-collisions/config.json"),
    text("figures/r072s-heat-collisions/fig-r072s-heat-collisions/caption.md"),
    text("figures/r072s-heat-collisions/fig-r072s-heat-collisions/README.md"),
    text("figures/r072s-heat-collisions/fig-r072s-heat-collisions/plot.py"),
    text("figures/r072s-heat-collisions/fig-r072s-heat-collisions/validate.py"),
    text("figures/r072s-heat-collisions/fig-r072s-heat-collisions/build_manifest.py"),
  ]);
  assert.equal(contract.schemaVersion, "r072s-figure-contract-v1");
  assert.match(contract.supportedTakeaway, /4\/3\/2 distinct critical points/);
  assert.match(contract.supportedTakeaway, /4\/2\/2 across an A3 collision/);
  assert.match(contract.claimBoundary, /not the complete four-dimensional caustic image/);
  assert.match(contract.claimBoundary, /no enhanced dissipation through a collision/);
  assert.match(contract.panelClaims.B, /noncolliding simple pair is omitted/);
  assert.match(contract.panelClaims.C, /simple phi=pi branch lies outside/);
  assert.match(caption, /noncolliding simple pair is omitted/);
  assert.match(caption, /persistent simple \\\(\\phi=\\pi\\\)/);
  assert.match(readme, /Panel B omits the surviving simple pair/);
  assert.deepEqual(
    {
      a2Y: config.parameters.a2CrossingY,
      a2Split: config.parameters.a2SplitSquared,
      a2Jet: config.parameters.a2ThirdJet,
      a3A0: config.parameters.a3A0,
      a3B0: config.parameters.a3B0,
      a3Y: config.parameters.a3CrossingY,
      a3Split: config.parameters.a3SplitSquared,
      a3Jet: config.parameters.a3FourthJet,
      determinant: config.parameters.coefficientDerivativeJetDeterminant,
    },
    {
      a2Y: Math.log(2), a2Split: -2, a2Jet: -3,
      a3A0: -2563 / 1280, a3B0: 1 / 30, a3Y: Math.log(2),
      a3Split: -6, a3Jet: -1533 / 512, determinant: 5400,
    },
  );
  for (const source of [plot, validator, builder]) {
    assert.match(source, /temporaryUnsealedSourceAllowed/);
  }
  assert.match(plot, /"formalSourceReady": True/);
  assert.match(builder, /checks\.get\("formalSourceReady"\) is not True/);
  assert.match(builder, /"formalSourceReady": True/);
  assert.match(plot, /numericSamplingDoesNotReplaceContinuousProof/);
  assert.match(validator, /all\(value is True for value in cross\.values\(\)\)/);
  assert.match(validator, /required_series_and_sampling_intervals/);
  assert.match(validator, /seriesExact/);
  assert.match(validator, /persistentRange/);
  assert.match(builder, /R072S_VISUAL_QA_INSPECTED/);
  assert.match(builder, /publicCopiesComplete/);

  const names = await readdir(figure);
  for (const required of [
    "README.md", "build_manifest.py", "caption.md", "certificate_ledger.py",
    "command.txt", "config.json", "contract.json", "figure-contract.md",
    "plot.py", "publish_assets.py", "qa_images.py", "requirements.txt", "validate.py",
  ]) assert.ok(names.includes(required), required);
  const formalFiles = [
    "manifest.json", "results.json", "validation.json", "SHA256SUMS",
    "figure.pdf", "figure.svg", "figure.png",
  ];
  if (manifest.latestCompletedRelease === "r072r") {
    for (const forbidden of formalFiles) assert.equal(names.includes(forbidden), false, forbidden);
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072s");
  for (const required of formalFiles) assert.ok(names.includes(required), required);
  const packageNames = await verifyFlatHashLedger(figure);
  const figureManifest = await json(
    "figures/r072s-heat-collisions/fig-r072s-heat-collisions/manifest.json",
  );
  assert.equal(figureManifest.release, "R0.72S");
  assert.equal(figureManifest.figureId, "fig-r072s-heat-collisions");
  assert.equal(figureManifest.schemaVersion, "1.1");
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.computation.incidencePreimageA2ThroughA5Closed, true);
  assert.equal(figureManifest.computation.restrictedMiniversalityModuloConstantsClosed, true);
  assert.equal(figureManifest.computation.uniqueA2HeatCollisionClosed, true);
  assert.equal(figureManifest.computation.realEvenA3HeatCollisionClosed, true);
  assert.equal(figureManifest.computation.completeFourDimensionalCausticImageClassified, false);
  assert.equal(figureManifest.computation.causticCrossingEnhancedDissipationClosed, false);
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  const { stdout } = await run(python, ["research/validate_figure_package.py", figure]);
  assert.deepEqual(JSON.parse(stdout).errors, []);
  for (const suffix of ["pdf", "png", "svg"]) {
    assert.ok(packageNames.includes(`figure.${suffix}`));
    const master = await readFile(resolve(figure, `figure.${suffix}`));
    const published = await readFile(
      resolve(root, `public/assets/r072s/fig-r072s-heat-collisions.${suffix}`),
    );
    assert.equal(Buffer.compare(master, published), 0, `${suffix} public byte identity`);
  }
});
