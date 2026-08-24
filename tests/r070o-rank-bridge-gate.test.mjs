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
const certificateRoot = new URL("certificates/r070o/", research);

test("locks the R0.70O scope, rank strata, and route decision", async () => {
  const report = await readFile(new URL("r070o_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /best-plane and best-line identities/i);
  assert.match(report, /coercive--near-plane--near-line trichotomy/i);
  assert.ok(report.includes("\\mathsf L_{\\delta,\\eta}"));
  assert.ok(report.includes("\\lambda_3/E<\\delta"));
  assert.ok(report.includes("(\\lambda_2+\\lambda_3)/E\\leq\\eta"));
  assert.match(report, /finite high-frequency-blind or smoothing scalar-filter/i);
  assert.match(report, /not a new Navier--Stokes[\s\S]{0,40}regularity criterion/i);
  assert.match(report, /not[\s\S]{0,160}a solution of the[\s\S]{0,20}Millennium problem/i);
});

test("locks exact variational identities and spectral gaps", async () => {
  const report = await readFile(new URL("r070o_report-source.md", research), "utf8");

  for (const token of [
    "### Theorem 3.1",
    "\\lambda_3",
    "\\min_{|n|=1}",
    "\\lambda_2+\\lambda_3",
    "\\min_{|\\ell|=1}",
    "### Theorem 4.1",
    "(1-2\\eta)E",
    "(\\eta-2\\delta)E",
    "Q_M=\\operatorname{diag}(M,M,0)",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /exact algebraic reason[\s\S]{0,120}two transverse vorticity components/i);
  assert.match(report, /Ratios do not control absolute residuals/i);
});

test("locks the complete simple-spectrum and direction-regularity ledger", async () => {
  const report = await readFile(new URL("r070o_report-source.md", research), "utf8");

  for (const token of [
    "\\dot Q=\\Sigma Q+Q\\Sigma+F",
    "\\dot\\lambda_a=2\\lambda_a\\sigma_{aa}+f_{aa}",
    "e_b^{\\mathsf T}\\dot e_a",
    "\\dot P_a",
    "\\dot E",
    "\\dot g_P",
    "\\dot g_L",
    "f_{33}(t_0)=0",
    "\\partial_iP_1",
    "\\lambda_1-\\lambda_2",
    "\\|\\partial_iP_1\\|_F",
    "\\|\\partial_iQ\\|_F",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /individual eigenvector need not be differentiable/i);
  assert.match(report, /orientability is an additional[\s\S]{0,20}global issue/i);
});

test("locks the exact smooth dynamic obstruction and its time boundary", async () => {
  const report = await readFile(new URL("r070o_report-source.md", research), "utf8");

  for (const token of [
    "### Theorem 7.1",
    "u_N(t,y)",
    "N^{-1/2}e^{-\\nu N^2t}\\sin(Ny)\\,e_3",
    "(u_N\\cdot\\nabla)u_N=0",
    "r_N(t)=\\lambda_2(t)+\\lambda_3(t)",
    "\\frac{A(Ne_2)}{4\\sqrt\\nu}",
    "\\frac1{2\\nu^{1/4}}",
    "\\theta_{N,T}=1-e^{-4\\nu N^2T}",
    "=\\frac1{A(Ne_2)}",
    "\\Phi(0)=0",
    "[\\tau,\\infty)",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /initial layer of width/i);
  assert.match(report, /does[\s\S]{0,10}not[\s\S]{0,10}disprove a delayed-time estimate/i);
  assert.match(report, /uniform quantitative reconstruction/i);
});

test("locks the compact-band endpoint and fixed-projection positive theorem", async () => {
  const report = await readFile(new URL("r070o_report-source.md", research), "utf8");

  for (const token of [
    "### Theorem 8.1",
    "Choose \\(a\\neq0\\)",
    "n_k=2^k",
    "r(t)=\\lambda_2(t)+\\lambda_3(t)=0",
    "\\frac1{16\\nu}\\sum_{k\\geq k_0}1",
    "### Theorem 9.1",
    "A(k)\\geq a_0",
    "A(k)\\geq a_0|k|^{-1}",
    "### Corollary 9.2",
    "\\|P\\omega\\|_{L^4(0,T;L^2)}^4",
    "[T_j,P]\\omega",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /does not contradict Chae--Choe,[\s\S]{0,80}Miller/i);
  assert.match(report, /periodic analogue of Miller's theorem must[\s\S]{0,80}cited or proved/i);
});

test("locks the bounded primary-literature audit and independent audit", async () => {
  const literature = await readFile(
    new URL("r070o_literature_audit.md", research),
    "utf8",
  );
  const independent = await readFile(
    new URL("r070o_independent_audit.md", research),
    "utf8",
  );

  for (const source of [
    "Chae--Choe",
    "Miller",
    "Constantin--Fefferman",
    "Cheskidov--Dai",
    "Bradshaw--Grujić",
    "Neustupa",
    "Balakrishna",
    "Biswas",
  ]) {
    assert.ok(literature.includes(source), source);
  }
  assert.match(literature, /bounded audit/i);
  assert.match(literature, /fixed global unit vector/i);
  assert.match(literature, /spatially Lipschitz unit lift/i);
  assert.match(literature, /nudging\/data-assimilation PDE/i);

  assert.match(independent, /Audit status:\*{0,2}\s*PASS/i);
  assert.match(independent, /producer reproduced byte-identically/i);
  assert.match(independent, /compact-band dyadic/i);
  assert.match(independent, /claim boundary/i);
});

test("reproduces the five-group exact producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070o_rank_bridge_audit.py", research));
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70O");
  assert.equal(archived.status, "exact-rank-strata-bridge-audit");
  assert.equal(Object.keys(archived.checks).length, 5);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the exact spectral, obstruction, gap, and reconstruction payload", async () => {
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );

  assert.deepEqual(
    archived.spectralProjectorLedger.exactSample.eigenvalueRates,
    ["33", "-4", "3"],
  );
  assert.equal(
    archived.spectralProjectorLedger.exactSample.planeRatioRate,
    "1/121",
  );
  assert.equal(
    archived.spectralProjectorLedger.exactSample.lineRatioRate,
    "-139/121",
  );
  assert.deepEqual(
    archived.spectralProjectorLedger.exactSample.projectorRateSum,
    [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]],
  );

  assert.deepEqual(
    archived.bestSubspaceVariationalLedger.exactFiniteFrame.eigenvalues,
    ["7", "3", "1"],
  );
  assert.equal(
    archived.bestSubspaceVariationalLedger.exactFiniteFrame.bestPlane.residual,
    "1",
  );
  assert.equal(
    archived.bestSubspaceVariationalLedger.exactFiniteFrame.bestLine.residual,
    "4",
  );

  assert.equal(
    archived.dynamicFilterObstruction.residualL2TimeNorm,
    "1/(4*sqrt(nu)*(N**2 + 1)**2)",
  );
  assert.equal(
    archived.dynamicFilterObstruction.unfilteredTransverseL4L2Norm,
    "1/(2*nu**(1/4))",
  );
  assert.equal(archived.dynamicFilterObstruction.residualLimit, "0");
  assert.equal(
    archived.dynamicFilterObstruction.finiteHorizon.exactInstabilityRatio,
    "1/A(N*e2)",
  );
  assert.deepEqual(
    archived.dynamicFilterObstruction.finiteCalibration.directFourierCovarianceAtT0,
    [["4/4225", "0", "0"], ["0", "0", "0"], ["0", "0", "4241/8450"]],
  );
  assert.equal(
    archived.dynamicFilterObstruction.compactBandDyadicApproximants.diagonalLowerBound,
    "1/2",
  );

  assert.equal(
    archived.linearReconstructionGate.finiteModeSample.l2Slack,
    "7/4",
  );
  assert.equal(
    archived.linearReconstructionGate.finiteModeSample.hMinusHalfSlack,
    "1/12",
  );
  assert.match(archived.spectralGapCertificates.partition, /otherwise near-line/i);
});

test("locks every R0.70O certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 8);
  assert.match(sums, /\.\.\/\.\.\/r070o_rank_bridge_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070o_report-source\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070o_literature_audit\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070o_independent_audit\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
