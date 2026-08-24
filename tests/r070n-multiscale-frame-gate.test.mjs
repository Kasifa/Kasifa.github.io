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
const certificateRoot = new URL("certificates/r070n/", research);

test("locks the R0.70N scope, no-go, and next route", async () => {
  const report = await readFile(new URL("r070n_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /scalar\/componentwise filters/i);
  assert.match(report, /nonnegative scale, center, or time weights/i);
  assert.match(report, /universal positive multi-scale vorticity-frame constant/i);
  assert.match(report, /coercive-versus-rank-stratified dichotomy/i);
  assert.match(
    report,
    /does not prove[\s\S]{0,220}global smoothness[\s\S]{0,120}Millennium problem/i,
  );
});

test("locks the complete aggregate source and pullback ledger", async () => {
  const report = await readFile(new URL("r070n_report-source.md", research), "utf8");

  for (const token of [
    "\\dot Q_j",
    "F_{\\chi,j}",
    "F_{\\widetilde S,j|*}",
    "F_{\\nu,j}",
    "(F_{C,j})_{pq}",
    "\\dot{\\mathcal Q}_k",
    "\\mathcal F_k",
    "\\sum_{j\\in J_k}\\dot w_{k,j}Q_j",
    "(\\Sigma_j-\\Sigma_*)Q_j",
    "\\dot{\\widehat{\\mathcal Q}}_k",
    "G_*^{-1}\\mathcal F_kG_*^{-\\mathsf T}",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /scale-source mismatch/i);
  assert.match(report, /Multi-scale summation does not\s+turn it into damping/i);
});

test("locks the exact frame and common-subspace theorems", async () => {
  const report = await readFile(new URL("r070n_report-source.md", research), "utf8");

  for (const token of [
    "### Theorem 6.1",
    "\\ker\\mathcal Q_k",
    "\\bigcap_{j:w_{k,j}>0}\\ker Q_j",
    "c_*(k,t)",
    "\\frac{\\lambda_{\\min}(\\mathcal Q_k)}",
    "0\\le c_*(k,t)\\le\\frac13",
    "\\Pi_{V^\\perp}P_\\alpha",
    "P_\\alpha\\Pi_{V^\\perp}",
    "\\operatorname{Ran}\\mathscr Q\\subset V",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /positive scalar normalization changes neither\s+its range nor its kernel/i);
});

test("locks exact shear and Beltrami PDE witnesses and the positive control", async () => {
  const report = await readFile(new URL("r070n_report-source.md", research), "utf8");

  for (const token of [
    "### Theorem 7.1",
    "u_s(x,t)=A e^{-\\nu N^2t}\\sin(Ny)e_1",
    "(u_s\\cdot\\nabla)u_s=0",
    "\\partial_tu_s=\\nu\\Delta u_s",
    "\\mathcal Q_s",
    "\\frac{11}{12}",
    "### Theorem 8.1",
    "\\nabla\\times u_b=Nu_b",
    "\\mathcal Q_b",
    "\\frac{11}{6}c<0",
    "u_{2h}",
    "\\operatorname{diag}(\\alpha,\\alpha+\\beta,\\beta)",
    "\\det\\mathcal Q_{2h}=\\alpha\\beta(\\alpha+\\beta)>0",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /must not be overgeneralized to all Beltrami fields/i);
});

test("locks genuine-three-dimensional and whole-space quantitative boundaries", async () => {
  const report = await readFile(new URL("r070n_report-source.md", research), "utf8");

  for (const token of [
    "u_0^\\varepsilon=u_0^s+\\varepsilon v_0",
    "\\longrightarrow0",
    "\\omega_0=\\nabla\\times(\\psi e_3)",
    "u_0=\\nabla\\times(-\\Delta)^{-1}\\omega_0",
    "\\psi_L",
    "u_L=(-y\\psi_L,x\\psi_L,0)",
    "\\frac1{8L^2+2}",
    "small-data global class",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /not a claim about finite-time\s+singularity/i);
});

test("locks the bounded primary literature and independent audit", async () => {
  const literature = await readFile(
    new URL("r070n_literature_audit.md", research),
    "utf8",
  );
  const independent = await readFile(
    new URL("r070n_independent_audit.md", research),
    "utf8",
  );

  for (const source of [
    "Yu (2026)",
    "Germano",
    "Eyink",
    "Daubechies",
    "Mallat",
    "Duffin",
    "Narendra",
    "Pennec",
    "Bonnabel",
    "Constantin--Majda",
    "Constantin--Fefferman",
    "Chae--Choe",
    "Miller",
  ]) {
    assert.ok(literature.includes(source), source);
  }
  assert.match(literature, /bounded-search statement/i);
  assert.match(
    literature,
    /small[\s\S]{0,80}lambda_3[\s\S]{0,180}near a plane/i,
  );
  assert.match(literature, /Neither bridge is supplied by the audited literature/i);

  assert.match(independent, /Audit status:\*{0,2}\s*PASS/i);
  assert.match(independent, /producer reproduced byte-identically/i);
  assert.match(independent, /rank-one periodic shear/i);
  assert.match(independent, /two-axis Beltrami positive control/i);
  assert.match(independent, /whole-space Gaussian covariance/i);
});

test("reproduces the four-group exact producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(
    new URL("r070n_multiscale_frame_audit.py", research),
  );
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70N");
  assert.equal(archived.status, "exact-multiscale-frame-no-go-audit");
  assert.equal(Object.keys(archived.checks).length, 4);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
  assert.equal(archived.periodicShear.rank, "1");
  assert.equal(archived.periodicShear.trace, "11/12");
  assert.equal(archived.beltramiWave.rank, "2");
  assert.equal(archived.beltramiWave.trace, "11/6");
  assert.equal(
    archived.beltramiWave.twoAxisPositiveControl.determinant,
    "alpha*beta*(alpha + beta)",
  );
  assert.equal(
    archived.wholeSpaceCalibration.optimalConstantForLAtLeastOne,
    "1/(2*(4*L**2 + 1))",
  );
});

test("locks every R0.70N certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 8);
  assert.match(sums, /\.\.\/\.\.\/r070n_multiscale_frame_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070n_report-source\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070n_literature_audit\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070n_independent_audit\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
