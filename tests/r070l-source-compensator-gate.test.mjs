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
const certificateRoot = new URL("certificates/r070l/", research);
const figureRoot = new URL(
  "figures/r070l-source-compensator/fig-r070l-source-compensator/",
  root,
);

test("locks the R0.70L scope and route decision", async () => {
  const report = await readFile(new URL("r070l_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /pressure-blindness obstruction/i);
  assert.match(report, /instantaneous local source\/shape compensator/i);
  assert.match(report, /deformation-pullback residual problem/i);
  assert.match(
    report,
    /does not claim[\s\S]{0,160}regularity[\s\S]{0,100}Millennium problem/i,
  );
});

test("locks the resolved source equation and coupled ledger", async () => {
  const report = await readFile(new URL("r070l_report-source.md", research), "utf8");

  for (const token of [
    "\\Sigma(t)=S(U)(X(t),t)",
    "\\dot X(t)=U(X(t),t)",
    "-(\\Sigma^2)^\\circ",
    "-\\frac14(\\Omega_*\\otimes\\Omega_*)^\\circ",
    "-H_*^\\circ",
    "+\\nu(\\Delta S)_*",
    "-K_{\\tau,*}^\\circ",
    "B:\\Sigma^2+\\frac23|\\Sigma|_F^2-2q^2",
    "+\\Sigma:\\mathcal T_B(F_{\\rm err})",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.ok(report.includes("\\mathcal Q=2+4-8=-2."));
  assert.ok(report.includes("\\mathcal Q=-1+4-2=1."));
});

test("locks the pressure-blindness theorem and escape boundaries", async () => {
  const report = await readFile(new URL("r070l_report-source.md", research), "utf8");

  assert.ok(report.includes("### Theorem 6.1"));
  assert.ok(report.includes("\\dot\\Phi=C-D_\\Sigma\\Phi:H"));
  assert.ok(report.includes("D_\\Sigma\\Phi(\\Sigma,B)=0"));
  for (const boundary of [
    "Gaussian or strict Littlewood--Paley filter",
    "source defined by a spatial average",
    "cutoff whose acceleration",
    "functional containing",
    "fixed, quantitatively restricted energy class",
    "without a reachability",
  ]) {
    assert.ok(report.includes(boundary), boundary);
  }
});

test("locks the matched periodic pair and exact opposite derivatives", async () => {
  const report = await readFile(new URL("r070l_report-source.md", research), "utf8");

  for (const token of [
    "\\psi_-&=-\\sin x\\sin y",
    "\\sqrt{120}(\\cos z-1)",
    "\\Sigma=\\operatorname{diag}(1,-1,0)",
    "R=\\operatorname{diag}(1/2,0,1/2)",
    "B=\\operatorname{diag}(1/6,-1/3,1/6)",
    "-301/85",
    "-152/65",
    "131/85",
    "-H^-:B=\\frac{563}{510}",
    "-H^+:B=-\\frac{733}{510}",
    "\\dot q_- =\\frac{3901}{2040}>0",
    "\\dot q_+ =-\\frac{1283}{2040}<0",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /same kinetic energy/i);
  assert.match(report, /exactly the entire\s+difference in the signed derivative ledger/i);
});

test("locks the rejected spectral diagnostic and live history candidate", async () => {
  const report = await readFile(new URL("r070l_report-source.md", research), "utf8");

  for (const token of [
    "d=\\lambda_+(\\Sigma)-q\\ge0",
    "\\dot d=-2\\operatorname{tr}[R(\\Sigma-qI)^2]\\le0",
    "\\widehat Q=G^{-1}QG^{-\\mathsf T}",
    "G^{-1}F_{\\rm err}G^{-\\mathsf T}",
    "\\det G=1",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /condition number may therefore require/i);
});

test("locks the bounded primary literature and independent audit", async () => {
  const literature = await readFile(
    new URL("r070l_literature_audit.md", research),
    "utf8",
  );
  const independent = await readFile(
    new URL("r070l_independent_audit.md", research),
    "utf8",
  );

  assert.match(literature, /stopped after\s+eleven high-signal primary sources/i);
  for (const source of [
    "Tom--Carbone--Bragg",
    "Wilczek--Meneveau",
    "Germano",
    "Johnson",
    "Cantwell",
    "Chevillard--Meneveau",
    "Hamlington--Schumacher--Dahm",
    "Carbone--Bragg",
    "Yang--Xu--Pumir--He",
  ]) {
    assert.ok(literature.includes(source), source);
  }
  assert.match(literature, /bounded-search saturation statement, not a proof/i);
  assert.match(literature, /leaves the compensator\s+problem open/i);

  assert.match(independent, /Audit status:\*{0,2}\s*PASS/i);
  assert.ok(independent.includes("\\dot q_-=\\frac{3901}{2040}>0"));
  assert.ok(independent.includes("\\dot q_+=-\\frac{1283}{2040}<0"));
  assert.match(independent, /same kinetic energy/i);
  assert.match(independent, /not external peer\s+review/i);
});

test("reproduces the four-group exact producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070l_source_compensator_audit.py", research));
  const archived = JSON.parse(await readFile(new URL("result.json", certificateRoot), "utf8"));
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70L");
  assert.equal(
    archived.status,
    "exact-source-evolution-compensator-obstruction-audit",
  );
  assert.equal(Object.keys(archived.checks).length, 4);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
  assert.equal(
    archived.periodicWitness.oppositeDerivatives,
    "qdot_minus=3901/2040>0; qdot_plus=-1283/2040<0",
  );
  assert.equal(archived.beltramiFilterSplit.invariantCombinedShare, "-C");
});

test("locks every R0.70L certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 8);
  assert.match(sums, /\.\.\/\.\.\/r070l_source_compensator_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070l_report-source\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070l_literature_audit\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070l_independent_audit\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives the formal figure package and exact validation", async () => {
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

  const manifest = JSON.parse(await readFile(new URL("manifest.json", figureRoot), "utf8"));
  const validation = JSON.parse(await readFile(new URL("validation.json", figureRoot), "utf8"));
  const contract = JSON.parse(await readFile(new URL("contract.json", figureRoot), "utf8"));
  const caption = await readFile(new URL("caption.md", figureRoot), "utf8");

  assert.equal(manifest.figureId, "fig-r070l-source-compensator");
  assert.equal(manifest.release, "R0.70L");
  assert.equal(manifest.status, "explanatory");
  assert.equal(manifest.outputs.length, 8);
  const source = await readFile(new URL(manifest.source, figureRoot));
  assert.equal(createHash("sha256").update(source).digest("hex"), manifest.sourceSha256);
  assert.match(manifest.claimBoundary, /not simulation[\s\S]{0,100}not a Millennium result/i);

  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.equal(validation.diagnostics.dataRows, 21);
  assert.ok(validation.diagnostics.minusTotalDerivative > 0);
  assert.ok(validation.diagnostics.plusTotalDerivative < 0);
  assert.match(validation.visualQa.originalResolution, /passed/i);
  assert.match(validation.visualQa.grayscale, /passed/i);

  assert.equal(contract.data.rowCount, 21);
  assert.match(contract.takeaway, /pressure Hessian alone switches the sign/i);
  assert.match(caption, /pressure contribution changes/i);
  for (const name of ["figure.pdf", "figure.svg", "figure.png"]) {
    const info = await stat(new URL(name, figureRoot));
    assert.ok(info.size > 10_000, name);
  }
});
