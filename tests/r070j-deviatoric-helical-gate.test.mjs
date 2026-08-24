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
const certificateRoot = new URL("certificates/r070j/", research);
const figureRoot = new URL(
  "figures/r070j-deviatoric-helical/fig-r070j-deviatoric-helical/",
  root,
);

test("locks the R0.70J report scope and route decision", async () => {
  const report = await readFile(new URL("r070j_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /deviatoric diagonal correlation/i);
  assert.match(report, /closes that possibility in the negative/);
  assert.match(report, /universal algebraic-null branch[\s\S]{0,160}is closed/);
  assert.match(
    report,
    /Nothing here proves global regularity, constructs a singularity, or solves\s+the Millennium problem/,
  );
});

test("locks the exact STF and physical-cutoff Fourier identities", async () => {
  const report = await readFile(new URL("r070j_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`S:\mathring Q(w)=w^{\mathsf T}Sw`));
  assert.match(report, /deviatoric projection supplies no second cancellation/);
  assert.ok(report.includes(String.raw`P_\xi S P_\xi=0`));
  assert.ok(report.includes(String.raw`\widehat\chi(-\xi-\eta)`));
  assert.match(report, /multiplication, not a Fourier projection/);
  assert.ok(report.includes(String.raw`\(k+(-k)=0\) term`));
});

test("locks the real helical symbol and the missing helicity cancellation", async () => {
  const report = await readFile(new URL("r070j_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`h_\sigma(\xi)=\frac{e_1+i\sigma e_2}{\sqrt2}`));
  assert.ok(report.includes(String.raw`h_\sigma^*Sh_\sigma`));
  assert.ok(report.includes(String.raw`-\frac12\xi^{\mathsf T}S\xi`));
  assert.ok(report.includes(String.raw`-2\sigma S_{12}\sin2\theta`));
  assert.ok(report.includes(String.raw`K_S(\xi)`));
  assert.match(report, /=\s*-\\xi\^\{\\mathsf T\}S\\xi/);
  assert.match(report, /independent of the helicity sign/);
  assert.ok(report.includes(String.raw`\(\xi\mapsto-\xi\)`));
});

test("locks the isotropy iff condition and the positive-part failure", async () => {
  const report = await readFile(new URL("r070j_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\sum_jw_j\xi_j\otimes\xi_j`));
  assert.ok(report.includes(String.raw`=\frac{\sum_jw_j}{3}I`));
  assert.match(report, /Condition \(5\.2\) is exact\s+second-order isotropy/);
  assert.ok(report.includes(String.raw`\langle(K_{S_0})_+\rangle_{S^2}=\frac{\sqrt{3}}{9}`));
  assert.ok(report.includes(String.raw`\left\langle K_S\right\rangle_{\rm ring}`));
  assert.ok(report.includes(String.raw`\frac{73}{50}>0`));
  assert.ok(report.includes(String.raw`positive-part sum \(1\)`));
});

test("locks the pointwise-positive Beltrami and periodic NSE witnesses", async () => {
  const report = await readFile(new URL("r070j_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`S_0=\operatorname{diag}\left(\frac12,\frac12,-1\right)`));
  assert.ok(report.includes(String.raw`\omega_\sigma^{\mathsf T}S_0\omega_\sigma`));
  assert.ok(report.includes(String.raw`\equiv1`));
  assert.ok(report.includes(String.raw`\int\chi\,dx>0`));
  assert.ok(report.includes(String.raw`u(t,x)=e^{-\nu t}(\sin x_3,\cos x_3,0)`));
  assert.ok(report.includes(String.raw`(u\cdot\nabla)u=0`));
  assert.match(report, /not the wave's own strain/);
  assert.match(report, /does not identify[\s\S]*with the mode's self-generated pressure Hessian/);
});

test("locks the exact compact exterior strain and retained return fields", async () => {
  const report = await readFile(new URL("r070j_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`G_S=\nabla\times\left[-\frac13\zeta_{\rm ext}(x)`));
  assert.ok(report.includes(String.raw`\nabla\times(x\times P_S)=-3P_S`));
  assert.ok(report.includes(String.raw`\operatorname{supp}\Gamma_S\subset B_5\setminus B_4`));
  assert.ok(report.includes(String.raw`G_S=\nabla\times(-\Delta)^{-1}\Gamma_S`));
  assert.match(report, /produces strain exactly\s+equal to[\s\S]*throughout the open core/);
  assert.ok(report.includes(String.raw`\nabla\times V_e=e`));
  assert.ok(report.includes(String.raw`\nabla\times V_{\sigma,\kappa}=W_{\sigma,\kappa}`));
  assert.match(report, /return vorticity[\s\S]*is not\s+discarded/);
});

test("locks physical filtering and the compact-versus-bandlimited boundary", async () => {
  const report = await readFile(new URL("r070j_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\widehat\varphi(\sigma_0\kappa e_3)`));
  assert.match(report, /so that this scalar is nonzero preserves strict\s+positivity/);
  assert.match(report, /uncertainty-principle boundary/);
  assert.match(report, /cannot also have compact Fourier support/);
  assert.match(report, /strict Littlewood--Paley block[\s\S]*requires a separate\s+high-frequency pseudolocal error estimate/);
  assert.match(report, /does not silently identify these two objects/);
});

test("locks the degree-zero critical coordinates and compact norm comparator", async () => {
  const report = await readFile(new URL("r070j_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`P_r^{(0)}=aR^{-2}S`));
  assert.ok(report.includes(String.raw`M_r^{(0)}=a^2r^{-1}Q_0`));
  assert.ok(report.includes(String.raw`m_r^{(0)}=rM_r^{(0)}=a^2Q_0`));
  assert.ok(report.includes(String.raw`c_r=r^2P_r^{(0)}=a\Lambda^{-2}S`));
  assert.ok(report.includes(String.raw`r^3P_r^{(0)}:M_r^{(0)}`));
  assert.ok(report.includes(String.raw`a^3\Lambda^{-2}S:Q_0>0`));
  assert.ok(report.includes(String.raw`\int r^{-1}|c_r(t)|^2dt`));
  assert.ok(report.includes(String.raw`\int r|\mathcal N_r^{(0)}(t)|^2dt`));
  assert.ok(report.includes(String.raw`a=r^{-1/2}`));
  assert.match(report, /function-space non-implication/);
  assert.match(report, /arbitrary\s+time envelope prevents \(8\.13\) from being reported as an NSE trajectory/);
});

test("locks the initial-face and pressure-Hessian boundaries", async () => {
  const report = await readFile(new URL("r070j_report-source.md", research), "utf8");

  assert.match(report, /initial-face NSE compatibility/i);
  assert.ok(report.includes(String.raw`0\le t\le\tau_*(\varepsilon,\Lambda)r^2`));
  assert.match(report, /intervals shrink\s+to zero/);
  assert.match(report, /pressure-Hessian boundary/i);
  assert.ok(report.includes(String.raw`\nabla^2p(0)=S`));
  assert.match(report, /claim stops at the center coefficient/);
  assert.match(report, /does not prove that a\s+velocity-generated pressure satisfies/);
  assert.ok(report.includes(String.raw`\nabla^2p(x)\equiv S`));
});

test("locks the bounded ten-source primary literature audit", async () => {
  const audit = await readFile(new URL("r070j_literature_audit.md", research), "utf8");

  assert.match(audit, /search stopped after ten high-signal primary sources/);
  for (const source of [
    "Applequist",
    "Ledesma--Mewes",
    "Waleffe",
    "Biferale--Musacchio--Toschi",
    "Constantin--Fefferman",
    "Beirão da Veiga--Berselli",
    "Galanti--Gibbon--Heritage",
    "Hamlington--Schumacher--Dahm",
    "Neustupa--Penel",
    "Miller",
  ]) {
    assert.ok(audit.includes(source), source);
  }
  assert.match(audit, /bounded search finding, not a theorem/);
  assert.match(audit, /DNS observations are not elevated to theorems/);
  assert.match(audit, /do not disprove a deeper cancellation tied to one self-consistent NSE\s+trajectory/);
});

test("archives the final independent PASS audit", async () => {
  const audit = await readFile(new URL("r070j_independent_audit.md", research), "utf8");

  assert.match(audit, /(?:Final status|Overall(?: verdict)?):\*{0,2}\s*PASS\b/i);
  assert.match(audit, /not external peer review/i);
  assert.match(audit, /Millennium/i);
});

test("reproduces the five-group R0.70J exact producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070j_deviatoric_helical_audit.py", research));
  const archived = JSON.parse(await readFile(new URL("result.json", certificateRoot), "utf8"));
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70J");
  assert.equal(archived.status, "exact-symbolic-deviatoric-helical-audit");
  assert.equal(Object.keys(archived.checks).length, 5);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
  assert.equal(archived.helicalSymbol.phaseAveragedKernel, "K_S(xi)=-xi^T*S*xi");
  assert.equal(archived.angularLedger.normalizedSpherePositivePartAverage, "sqrt(3)/9");
  assert.equal(archived.angularLedger.sameShellPairing, "73/50");
  assert.equal(archived.criticalScaleLedger.cauchyProduct, "amplitude**3/Lambda**2");
  assert.equal(archived.criticalScaleLedger.lerayNormalizedPairing, "1/(Lambda**2*r**(3/2))");
  assert.match(archived.claimBoundary.notComputerProved, /strict annular LP localization/);
});

test("locks every R0.70J certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 7);
  assert.match(sums, /\.\.\/\.\.\/r070j_deviatoric_helical_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070j_report-source\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070j_literature_audit\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid checksum line: ${line}`);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives the 10-file figure package and its 22-check validation", async () => {
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

  assert.equal(manifest.figureId, "fig-r070j-deviatoric-helical");
  assert.equal(manifest.release, "R0.70J");
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

  assert.equal(validation.release, "R0.70J");
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 22);
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.equal(validation.diagnostics.sphereSignedMean, 0);
  assert.ok(Math.abs(validation.diagnostics.spherePositivePartMean - Math.sqrt(3) / 9) < 1e-15);
  assert.equal(validation.diagnostics.dataRows, 145);
  assert.equal(contract.data.rowCount, 145);
  assert.match(caption, /closed-form analytic/i);
  assert.match(figureContract, /not DNS/i);
  assert.ok((await stat(new URL("figure.png", figureRoot))).size > 500_000);
  assert.ok((await stat(new URL("figure.pdf", figureRoot))).size > 40_000);
  assert.ok((await stat(new URL("figure.svg", figureRoot))).size > 80_000);
});
