import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { readdir, readFile, stat } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const root = new URL("../", import.meta.url);
const research = new URL("research/", root);
const certificateRoot = new URL("certificates/r070m/", research);
const figureRoot = new URL(
  "figures/r070m-deformation-holonomy/fig-r070m-deformation-holonomy/",
  root,
);

test("locks the R0.70M scope and route decision", async () => {
  const report = await readFile(new URL("r070m_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /strain-only propagator/i);
  assert.match(report, /not the physical deformation gradient/i);
  assert.match(report, /multi-scale frame coercivity\s+gate/i);
  assert.match(
    report,
    /does not prove[\s\S]{0,180}global smoothness[\s\S]{0,100}Millennium problem/i,
  );
});

test("locks the exact pullback and pulled-shape BV ledger", async () => {
  const report = await readFile(new URL("r070m_report-source.md", research), "utf8");

  for (const token of [
    "\\dot Q=\\Sigma Q+Q\\Sigma+F",
    "\\dot G=\\Sigma G",
    "\\widehat Q=G^{-1}QG^{-\\mathsf T}",
    "\\dot{\\widehat Q}=G^{-1}FG^{-\\mathsf T}",
    "\\dot{\\widehat E}=\\operatorname{tr}\\widehat F",
    "\\dot{\\widehat B}",
    "(1+\\sqrt2)\\int_s^t\\rho_G(r)\\,dr",
    "\\rho_G",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /No Grönwall factor has been inserted/i);
});

test("locks the sharp kappa-squared Euclidean obstruction", async () => {
  const report = await readFile(new URL("r070m_report-source.md", research), "utf8");

  for (const token of [
    "\\rho_G\\le\\kappa_2(G)^2\\rho_0",
    "G_k=\\operatorname{diag}(k,k^{-1},1)",
    "Q_\\varepsilon=\\operatorname{diag}(1,\\varepsilon,\\varepsilon)",
    "k^4=\\kappa_2(G_k)^2",
    "\\kappa_2(G(t))\\le e^{\\Gamma(t)}",
    "\\sqrt2\\kappa_2(G)^2",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /sharpness is for the\s+actual quotient/i);
});

test("locks the zero-integral noncommutative holonomy certificate", async () => {
  const report = await readFile(new URL("r070m_report-source.md", research), "utf8");

  for (const token of [
    "### Theorem 6.1",
    "\\int_{\\mathbb R}\\Sigma(t)\\,dt=0",
    "G_*=e^{-C}e^{-A}e^Ce^A",
    "-119/9&-160/81",
    "160/9&209/81",
    "\\operatorname{tr}G_*=-\\frac{862}{81}<-2",
    "\\frac{-431\\pm160\\sqrt7}{81}",
    "\\frac{6553600}{9889449}",
    "\\frac{13122}{3296483}",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /not been embedded in one unforced\s+finite-energy periodic NSE trajectory/i);
});

test("locks the affine-relative theorem and rank boundary", async () => {
  const report = await readFile(new URL("r070m_report-source.md", research), "utf8");

  for (const token of [
    "\\frac d{dt}\\log\\det Q",
    "\\operatorname{tr}(Q^{-1}F)",
    "\\mathfrak a(Q,F)^2",
    "d_{\\rm AI}",
    "u(x,t)=A_0e^{-\\nu N^2t}\\sin(Ny)e_1",
    "\\operatorname{rank}Q=1",
    "F_\\varepsilon",
    "-2\\varepsilon E\\Sigma",
    "=8",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /undefined on this smooth solution/i);
});

test("locks the complete pulled NSE residual and critical boundary", async () => {
  const report = await readFile(new URL("r070m_report-source.md", research), "utf8");

  for (const token of [
    "\\widehat F_\\chi",
    "\\widehat F_{\\widetilde S}",
    "\\widehat F_\\nu",
    "(\\widehat F_C)_{ij}",
    "A_\\chi+2S_G+2D_G+2C_G",
    "S_G\\le\\kappa_2(G)\\|\\widetilde S\\|_\\infty",
    "D_G\\le\\kappa_2(G)^2",
    "C_G\\le\\kappa_2(G)^2",
    "Q_\\lambda(t)=\\lambda Q(\\lambda^2t)",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /Leray energy does\s+not control/i);
});

test("locks the bounded primary literature and independent audit", async () => {
  const literature = await readFile(
    new URL("r070m_literature_audit.md", research),
    "utf8",
  );
  const independent = await readFile(
    new URL("r070m_independent_audit.md", research),
    "utf8",
  );

  assert.match(literature, /core fluid\/PDE audit stopped at twelve high-signal primary sources/i);
  for (const source of [
    "Constantin",
    "Constantin and Iyer",
    "Beale, Kato, and Majda",
    "Ponce",
    "Miller",
    "Kozono, Ogawa, and Taniuchi",
    "Phuc",
    "Gallagher, Koch, and Planchon",
    "Chevillard and Meneveau",
    "Tom, Carbone, and Bragg",
    "Moakher",
    "Bhatia and Holbrook",
    "Pennec, Fillard, and Ayache",
  ]) {
    assert.ok(literature.includes(source), source);
  }
  assert.match(literature, /bounded novelty\s+audit, not a proof of nonexistence/i);
  assert.match(literature, /not.*physical deformation gradient/is);

  assert.match(independent, /Audit status:\*{0,2}\s*PASS/i);
  assert.match(independent, /Three corrections were required before PASS/i);
  assert.ok(independent.includes("\\lim_{\\varepsilon\\downarrow0}"));
  assert.ok(independent.includes("\\frac{6553600}{9889449}"));
  assert.match(independent, /not.*unforced finite-energy periodic NSE trajectory/is);
});

test("reproduces the four-group exact producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(
    new URL("r070m_deformation_holonomy_audit.py", research),
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
  assert.equal(archived.release, "R0.70M");
  assert.equal(
    archived.status,
    "exact-deformation-holonomy-and-affine-boundary-audit",
  );
  assert.equal(Object.keys(archived.checks).length, 4);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
  assert.equal(archived.zeroIntegralLoop.detMonodromy, "1");
  assert.equal(archived.zeroIntegralLoop.physicalAnisotropy3D, "6553600/9889449");
  assert.equal(
    archived.sharpEuclideanAmplification.optimizedShapeQuotientLimit,
    "lim_epsilon_to_0 rhoG/rho0=k**4=kappa(G)**2",
  );
  assert.equal(archived.rankDefect.nullPlaneExampleRelativeSpeedSquared, "8");
});

test("locks every R0.70M certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 8);
  assert.match(sums, /\.\.\/\.\.\/r070m_deformation_holonomy_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070m_report-source\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070m_literature_audit\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070m_independent_audit\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives the R0.70M figure package and exact validation", async () => {
  const files = (await readdir(figureRoot)).sort();
  const expectedFiles = [
    "caption.md",
    "contract.json",
    "data.csv",
    "figure-contract.md",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "manifest.json",
    "plot.py",
    "validation.json",
  ].sort();
  assert.deepEqual(files, expectedFiles);

  const manifest = JSON.parse(
    await readFile(new URL("manifest.json", figureRoot), "utf8"),
  );
  const validation = JSON.parse(
    await readFile(new URL("validation.json", figureRoot), "utf8"),
  );
  const contract = JSON.parse(
    await readFile(new URL("contract.json", figureRoot), "utf8"),
  );
  const caption = await readFile(new URL("caption.md", figureRoot), "utf8");

  assert.equal(manifest.figureId, "fig-r070m-deformation-holonomy");
  assert.equal(manifest.release, "R0.70M");
  assert.ok(["draft", "formal"].includes(manifest.status));
  assert.equal(manifest.outputs.length, 8);
  const source = await readFile(new URL(manifest.source, figureRoot));
  assert.equal(
    createHash("sha256").update(source).digest("hex"),
    manifest.sourceSha256,
  );
  assert.match(manifest.claimBoundary, /not DNS[\s\S]{0,140}not a Millennium result/i);

  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.equal(validation.diagnostics.dataRows, 64);
  assert.equal(validation.diagnostics.monodromyDeterminant, 1);
  assert.ok(validation.diagnostics.monodromyTrace < -2);
  assert.ok(validation.diagnostics.firstLoopRankOneGap > 0);
  assert.ok(
    validation.diagnostics.lastLoopRankOneGap
      < validation.diagnostics.firstLoopRankOneGap,
  );
  assert.match(validation.visualQa.originalResolution, /passed/i);
  assert.match(validation.visualQa.grayscale, /passed/i);

  assert.equal(contract.data.rowCount, 64);
  assert.match(contract.takeaway, /hyperbolic holonomy/i);
  assert.match(caption, /optimized pulled\/original shape quotient/i);
  for (const name of ["figure.pdf", "figure.svg", "figure.png"]) {
    const info = await stat(new URL(name, figureRoot));
    assert.ok(info.size > 10_000, name);
  }
});
