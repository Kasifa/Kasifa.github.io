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
const certificateRoot = new URL("certificates/r070k/", research);
const figureRoot = new URL(
  "figures/r070k-anisotropy-evolution/fig-r070k-anisotropy-evolution/",
  root,
);

test("locks the R0.70K report scope and route decision", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /trace-normalized, spatially localized filtered-vorticity/);
  assert.match(report, /normalization alone cannot[\s\S]{0,120}missing Leray-to-critical estimate/i);
  assert.match(report, /source-evolution compensator problem/i);
  assert.match(
    report,
    /does not prove blow-up, global\s+regularity, or any part of the Millennium theorem/i,
  );
});

test("locks the normalization correction and exact master identity", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`B=R-\frac13I=\frac AE`));
  assert.ok(report.includes(String.raw`actually normalized in R0.70K is \(B=A/E\)`));
  assert.ok(report.includes(String.raw`\dot B=\mathcal T_B(F)`));
  assert.ok(report.includes(String.raw`\frac{\operatorname{dev}F-B\operatorname{tr}F}{E}`));
  assert.ok(report.includes(String.raw`\(F=\lambda Q\Rightarrow\dot B=0\)`));
  assert.ok(report.includes(String.raw`\frac12\dot\alpha`));
  assert.match(report, /Every flux must carry its own denominator correction/);
  assert.ok(report.includes(String.raw`undefined at \(E=0\)`));
});

test("locks every filtered covariance flux without a hidden closure model", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  for (const flux of [String.raw`F_\chi`, String.raw`F_S`, String.raw`F_\nu`, String.raw`F_C`]) {
    assert.ok(report.includes(flux), flux);
  }
  assert.ok(report.includes(String.raw`\partial_t\chi+U\cdot\nabla\chi+\nu\Delta\chi`));
  assert.ok(report.includes(String.raw`-2\nu\int\chi\sum_a`));
  assert.ok(report.includes(String.raw`C_{ai}\partial_a(\chi\Omega_j)`));
  assert.match(report, /not an eddy-viscosity model/);
  assert.match(report, /minimal suitable-weak or[\s\S]{0,80}Leray formulation requires/);
});

test("locks sharp trace-one realizability bounds and the raw-work boundary", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`-\frac13\le\lambda_i(B)\le\frac23`));
  assert.ok(report.includes(String.raw`0\le|B|_F^2\le\frac23`));
  assert.ok(report.includes(String.raw`\lambda_{\min}(\Sigma)`));
  assert.ok(report.includes(String.raw`|q|\le\sqrt{\frac23}\,|\Sigma|_F`));
  assert.ok(report.includes(String.raw`\Sigma:A=E(\Sigma:B)=Eq`));
  assert.match(report, /bounded shape is not bounded raw work/i);
});

test("locks the frozen-source variance law and equality case", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`F_\Sigma=\Sigma Q+Q\Sigma`));
  assert.ok(report.includes(String.raw`\dot R\big|_\Sigma`));
  assert.ok(report.includes(String.raw`2\operatorname{tr}\!\left[R(\Sigma-qI)^2\right]`));
  assert.ok(report.includes(String.raw`\operatorname{ran}R\subseteq\ker(\Sigma-qI)`));
  assert.match(report, /opposite of a damping law/i);
});

test("locks the axisymmetric replicator solution", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\Sigma_0=\operatorname{diag}(-1/2,-1/2,1)`));
  assert.ok(report.includes(String.raw`\dot p=3p(1-p)`));
  assert.ok(report.includes(String.raw`\dot q=\frac92p(1-p)=(1+2q)(1-q)`));
  assert.ok(report.includes(String.raw`p(t)=\frac{p_0e^{3t}}{1-p_0+p_0e^{3t}}`));
  assert.match(report, /is isotropic,[\s\S]{0,80}not stationary/);
});

test("locks the complete source-correlation compensator ledger", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`S(U)(x,t)=\Sigma(t)+\widetilde S(x,t)`));
  assert.ok(report.includes(String.raw`F_{\rm err}=F_\chi+F_{\widetilde S}+F_\nu+F_C`));
  assert.ok(report.includes(String.raw`\dot\Sigma:B`));
  assert.ok(report.includes(String.raw`\Sigma:\mathcal T_B(F_{\rm err})`));
  assert.match(report, /pressure therefore enters[\s\S]{0,180}evolution of/i);
  assert.ok(report.includes("No term in (8.4) is assigned a sign"));
});

test("locks the self-consistent Burgers-vortex witness and its boundary", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\frac{\Gamma\gamma}{4\pi\nu}`));
  assert.ok(report.includes(String.raw`e^{-\gamma\rho^2/(4\nu)}e_3`));
  assert.ok(report.includes(String.raw`R=e_3\otimes e_3`));
  assert.ok(report.includes(String.raw`q=\Sigma_\gamma:B=\gamma>0`));
  assert.ok(report.includes(String.raw`\operatorname{tr}F_{\Sigma_\gamma}=2\gamma E>0`));
  assert.match(report, /not\s+a Leray finite-energy solution/);
  assert.match(report, /not a counterexample to regularity/);
  assert.ok(report.includes("https://arxiv.org/abs/math/0503354"));
});

test("locks the exact periodic diffusion sign pair", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\frac D2e^{-4\nu t}\sin(2x_3)`));
  assert.ok(report.includes(String.raw`(u\cdot\nabla)u=0`));
  assert.ok(report.includes(String.raw`(\omega\cdot\nabla)u=0`));
  assert.ok(report.includes(String.raw`\dot p=6\nu p(1-p)`));
  assert.ok(report.includes(String.raw`12\nu p(1-p)(2p-1)`));
  assert.ok(report.includes(String.raw`+144\nu/125`));
  assert.ok(report.includes(String.raw`-144\nu/125`));
  assert.match(report, /caused solely by relative diffusion/);
});

test("locks scaling, homogeneity, and the fixed-positive-time boundary", async () => {
  const report = await readFile(new URL("r070k_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`u^{(r)}(x,t)=r^{-1}u(x/r,t/r^2)`));
  assert.ok(report.includes(String.raw`Q^{(r)},E^{(r)},A^{(r)}\sim r^{-1}`));
  assert.ok(report.includes(String.raw`r^2q^{(r)}\sim1`));
  assert.ok(report.includes(String.raw`\Sigma^{(r)}:A^{(r)}\sim r^{-3}`));
  assert.match(report, /persistence interval shrinks[\s\S]{0,60}parabolically/);
  assert.match(report, /does not give a common fixed positive terminal time/);
});

test("locks the bounded ten-source primary literature audit", async () => {
  const audit = await readFile(new URL("r070k_literature_audit.md", research), "utf8");

  assert.match(audit, /search stopped after ten\s+high-signal primary sources/i);
  for (const source of [
    "Germano",
    "Eyink--Aluie",
    "Cerutti--Meneveau--Knio",
    "Dascaliuc--Grujić",
    "Betchov",
    "Johnson",
    "Goto--Saito--Kawahara",
    "Danish--Meneveau",
    "Hamlington--Dahm",
    "Bernard--Berger",
  ]) {
    assert.ok(audit.includes(source), source);
  }
  assert.match(audit, /bounded-search saturation statement, not a proof/);
  assert.match(audit, /DNS proportions are observations, not theorems/);
  assert.match(audit, /source-evolution compensator[\s\S]{0,80}precise open gate/i);
});

test("archives the independent PASS audit and its exact boundaries", async () => {
  const audit = await readFile(new URL("r070k_independent_audit.md", research), "utf8");

  assert.match(audit, /Audit status:\*{0,2}\s*PASS/i);
  assert.ok(audit.includes(String.raw`\frac12\dot\alpha`));
  assert.ok(audit.includes(String.raw`\frac{144}{125}\nu`));
  assert.match(audit, /separate three-mode commutator counterexample is unnecessary/i);
  assert.match(audit, /not external peer review/i);
  assert.match(audit, /Millennium-problem result/i);
});

test("reproduces the six-group R0.70K exact producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070k_anisotropy_evolution_audit.py", research));
  const archived = JSON.parse(await readFile(new URL("result.json", certificateRoot), "utf8"));
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70K");
  assert.equal(archived.status, "exact-normalized-anisotropy-evolution-audit");
  assert.equal(Object.keys(archived.checks).length, 6);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
  assert.equal(archived.realizability.normBound, "0 <= tr(B**2) <= 2/3");
  assert.equal(
    archived.frozenSourceVarianceLaw.correlationDerivative,
    "dq/dt=2*(tr(R*Sigma**2)-q**2)",
  );
  assert.equal(
    archived.periodicShear.oppositeSigns,
    "+144*nu/125 at p=4/5 and -144*nu/125 at p=1/5",
  );
  assert.match(archived.burgersVortex.boundary, /not a Leray finite-energy field/);
});

test("locks every R0.70K certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 8);
  assert.match(sums, /\.\.\/\.\.\/r070k_anisotropy_evolution_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070k_report-source\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070k_literature_audit\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070k_independent_audit\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid checksum line: ${line}`);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives the 10-file figure package and its 25-check validation", async () => {
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
  const figureContract = await readFile(new URL("figure-contract.md", figureRoot), "utf8");

  assert.equal(manifest.figureId, "fig-r070k-anisotropy-evolution");
  assert.equal(manifest.release, "R0.70K");
  assert.equal(manifest.status, "explanatory");
  assert.equal(manifest.source, "plot.py");
  assert.equal(manifest.outputs.length, 8);
  const plotSource = await readFile(new URL(manifest.source, figureRoot));
  assert.equal(createHash("sha256").update(plotSource).digest("hex"), manifest.sourceSha256);
  assert.match(manifest.claimBoundary, /not simulation evidence or a numerical PDE proof/i);

  const outputPaths = new Set(manifest.outputs.map(({ path }) => path));
  for (const required of [
    "contract.json",
    "figure-contract.md",
    "caption.md",
    "data.csv",
    "validation.json",
    "figure.pdf",
    "figure.svg",
    "figure.png",
  ]) {
    assert.ok(outputPaths.has(required), required);
  }
  for (const output of manifest.outputs) {
    const payload = await readFile(new URL(output.path, figureRoot));
    assert.equal(payload.byteLength, output.bytes, output.path);
    assert.equal(createHash("sha256").update(payload).digest("hex"), output.sha256, output.path);
  }

  assert.equal(validation.release, "R0.70K");
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 25);
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.equal(validation.diagnostics.dataRows, 483);
  assert.ok(Math.abs(validation.diagnostics.negativeDiffusionWitness + 144 / 125) < 1e-15);
  assert.ok(Math.abs(validation.diagnostics.positiveDiffusionWitness - 144 / 125) < 1e-15);
  assert.deepEqual(validation.diagnostics.pngPixels, [4204, 2267]);
  assert.equal(contract.data.rowCount, 483);
  assert.equal(contract.surface.renderer, "static Matplotlib");
  assert.match(figureContract, /600 dpi PNG/);
  assert.match(figureContract, /There is no fit,[\s\S]{0,80}PDE time-stepper/);
  assert.match(caption, /not DNS/i);
  assert.match(caption, /does not establish regularity/i);

  const png = await stat(new URL("figure.png", figureRoot));
  const pdf = await stat(new URL("figure.pdf", figureRoot));
  const svg = await stat(new URL("figure.svg", figureRoot));
  assert.ok(png.size > 100_000);
  assert.ok(pdf.size > 10_000);
  assert.ok(svg.size > 10_000);
});
