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
const certificateRoot = new URL("certificates/r070i/", research);
const figureRoot = new URL(
  "figures/r070i-temporal-hardy/fig-r070i-temporal-hardy/",
  root,
);

test("locks the R0.70I report scope and claim boundary", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /exact temporal kernel behind the R0\.70H core dual norm/);
  assert.match(report, /fixed center, a one-sided geometric scale chain/);
  assert.match(report, /R0\.70I obtains four precise conclusions/);
  assert.match(report, /function-space obstruction, not a\s+Navier--Stokes trajectory/);
  assert.match(
    report,
    /Nothing here proves global regularity, constructs a singularity, or solves\s+the Millennium problem/,
  );
});

test("locks the finite T_nK, fine endpoint, and exact G_K ledger", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\mathcal T_{n,K}`));
  assert.ok(report.includes(String.raw`\sum_{k=0}^{K-1} r_k^{-3}`));
  assert.match(report, /no undefined \$m_\{K\+1\}\^\{\(n\)\}\$ occurs/);
  assert.ok(report.includes(String.raw`\mathcal E_{n,K}`));
  assert.ok(report.includes(String.raw`\int_{I_K}r_K^{-3}|m_K^{(n)}|^2dt`));
  assert.ok(report.includes(String.raw`G_K(s):={}`));
  assert.ok(report.includes(String.raw`r_K^{-1}\mathbf1_{s<r_K^2}`));
  assert.ok(report.includes(String.raw`\min\{r_K^{-1},s^{-1/2}\}`));
  assert.ok(report.includes(String.raw`\mathcal T_{n,K}+\mathcal E_{n,K}`));
  assert.match(report, /uniform in the chain\s+length but records the exact finest-scale saturation/);
});

test("locks the temporal Hardy threshold and the p greater than 8 sufficient condition", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`s^{-1/2}f(t_0-s)^2`));
  assert.ok(report.includes(String.raw`f(t_0-s)=c s^{-\alpha}`));
  assert.match(report, /\$1\/4\s*\\le\s*\\alpha<1\$/);
  assert.match(report, /norm\s+non-implication only/);
  assert.ok(report.includes(String.raw`m_k^{(n)}(t)=r_k f(t)T`));
  assert.match(report, /cannot\s+be improved from the moment-size inequality \(3\.1\) alone/);
  assert.ok(report.includes(String.raw`\omega\in L_t^pL_x^2(I_0)`));
  assert.ok(report.includes(String.raw`p>8`));
  assert.ok(report.includes(String.raw`r_0^{1-8/p}`));
  assert.match(report, /no endpoint \$p=8\$ claim/);
});

test("locks the exact C/F/S physical-cutoff decomposition", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.ok(
    report.includes(
      String.raw`\mathfrak D_k^{\rm st}\mathcal N
 =\mathcal C_{k,n}+\mathcal F_{k,n}+\mathcal S_{k,n}`,
    ),
  );
  for (const term of ["C", "F", "S"]) {
    assert.ok(report.includes(String.raw`\mathcal ${term}_{k,n}`), term);
  }
  assert.ok(
    report.includes(
      String.raw`\chi_k-\rho_k\chi_{k+1}
 =(\chi_k-\chi_{k+1})+(1-\rho_k)\chi_{k+1}`,
    ),
  );
  assert.ok(report.includes(String.raw`\|a_{k,n}\|_\infty\lesssim r_k^{-1}`));
  assert.ok(report.includes(String.raw`|\operatorname{supp}a_{k,n}|\lesssim r_k^3`));
  assert.match(report, /physical shell and the time slab cannot be\s+treated as lower-order bookkeeping errors/);
});

test("locks the standard LP specialization and physical-cutoff Fourier boundary", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.match(report, /standard Littlewood--Paley resolution/);
  assert.ok(report.includes(String.raw`\Omega_k=L_0+\sum_{1\le j\le k}B_j`));
  assert.match(report, /not asserted for an arbitrary\s+\$L\^1\$-bounded filter lacking this LP structure/);
  assert.ok(report.includes(String.raw`\delta\Omega_k=\Omega_{k+1}-\Omega_k`));
  assert.match(report, /standard annular LP filter/);
  assert.ok(report.includes(String.raw`\widehat\chi_k(-\xi-\eta)`));
  assert.match(report, /no automatic small factor from\s+the scale gap/);
});

test("locks the lower-triangular r_k/r_j convolution", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.match(report, /entire triangular array \$j\\le k\$/);
  assert.ok(report.includes(String.raw`r_k^{-1/2}\frac{r_k}{r_j}`));
  assert.ok(report.includes(String.raw`H_k=\sum_{j\le k}(r_k/r_j)\|V_j\|_2`));
  assert.ok(report.includes(String.raw`\frac{r_k}{r_j}`));
  assert.ok(report.includes(String.raw`\le\rho_+^{k-j}`));
  assert.match(report, /Young's inequality for the discrete\s+\$\\ell\^1\*\\ell\^2\$ convolution/);
  assert.ok(report.includes(String.raw`\sum_kH_k^2\lesssim_{\rho_+}\sum_j\|V_j\|_2^2`));
  assert.match(report, /No coefficient \$c_k\(t\)\$ has been\s+factored out of time/);
});

test("locks frozen mixed, frozen low-low, and isotropic closures", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`|\mathscr W_{\rm frozen\text{-}low/mixed}|`));
  assert.ok(report.includes(String.raw`r_0^{-3/2}`));
  assert.ok(report.includes(String.raw`\|L_0(t)\|_\infty`));
  assert.match(report, /same argument covers the physical-cutoff and discarded-slab mixed arrays/);
  assert.ok(report.includes(String.raw`|\mathscr W_{\rm frozen\text{-}low/low}|`));
  assert.match(report, /Both \(1\.7\) and \(6\.9\) are absolute estimates/);
  assert.ok(report.includes(String.raw`c_{ii}=0`));
  assert.ok(report.includes(String.raw`c_{ij}\left(\frac{|W_k|^2}{3}\delta_{ij}\right)=0`));
  assert.match(report, /survives\s+cutoffs, time windows, and positive parts/);
});

test("locks the moving-low and deviatoric high-high open boundaries", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.ok(
    report.includes(
      String.raw`\sum_{J_0<j\le J_k-L}
 2^{3j/2}\|\Delta_j\omega\|_2`,
    ),
  );
  assert.match(report, /moving \$B\^\{3\/2\}_\{2,1\}\$-type or Carleson maximal quantity/);
  assert.match(report, /not a theorem that every possible\s+signed or equation-correlated argument must control/);
  assert.ok(report.includes(String.raw`\int\sum_k r_k^{-1}\|W_k(t)\|_2^4dt`));
  assert.ok(report.includes(String.raw`\int\sum_k\|W_k(t)\|_2^2dt<\infty`));
  assert.match(report, /missing spatial weight and time square occur together/);
  assert.match(report, /proof using a correlation special\s+to the NSE equation or a signed cancellation[\s\S]*is not\s+excluded/);
});

test("locks the degree-zero abstract source-coordinate comparator", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.match(report, /abstract source-coordinate comparator \(degree zero\)/i);
  assert.ok(report.includes(String.raw`\operatorname{dev}Q_0\ne0`));
  assert.ok(report.includes(String.raw`m_r^{(0)}(t)=r^{-1}\theta_r(t)^2Q_0`));
  assert.ok(report.includes(String.raw`c_r(t)=r^{-1/2}\theta_r(t)C_0`));
  assert.ok(report.includes(String.raw`\int r^{-1}|c_r(t)|^2dt`));
  assert.ok(report.includes(String.raw`=r^{-3/2}|\operatorname{dev}Q_0|`));
  assert.match(report, /abstract source-coordinate\/core comparator for \$n=0\$/);
  assert.match(report, /does \*\*not\*\* construct \$c_r\$ from a compact exterior/);
  assert.match(report, /treat the degree-one coefficient, or place the source and core\s+on one NSE trajectory/);
});

test("locks the fixed-geometry linear heat scaling ledger", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.match(report, /rescales one fixed cutoff, filter, complete\s+base chain, center, and terminal time together with the field/);
  assert.ok(report.includes(String.raw`r_k^{(r)}=rR_k`));
  assert.ok(report.includes(String.raw`t_0^{(r)}=r^2\tau_0`));
  assert.ok(report.includes(String.raw`m^{(n)}\mapsto A^2r^2m^{(n)}`));
  assert.ok(
    report.includes(
      String.raw`\mathcal T_n[u^{A,r};\{rR_k\},r^2\tau_0]
 =A^4r^3\mathcal T_n[v;\{R_k\},\tau_0]`,
    ),
  );
  assert.match(report, /Taking \$A=r\^\{-3\/2\}\$ keeps the two base-window quantities fixed/);
  assert.match(report, /linear heat field is not generally a\s+Navier--Stokes solution/);
});

test("locks the small-NSE scaling and fixed-positive-top boundary", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.match(report, /Koch--Tataru, Theorem[\s\S]*global small\s+solution in its \$X\$ class/);
  assert.ok(report.includes(String.raw`v^a(t)=a e^{\nu t\Delta}v_0+O(a^2)`));
  assert.match(report, /in \$C\(\[0,1\];H\^m\)\$/);
  assert.match(report, /not a verbatim assertion of Theorem 2/);
  assert.ok(report.includes(String.raw`\mathcal T_0[v^a]\ge c a^4`));
  assert.ok(report.includes(String.raw`\mathcal T_n[u^{a,r}]\gtrsim a^4/r`));
  assert.ok(report.includes(String.raw`D_{[0,r^2]}[u^{a,r}]\asymp ra^2`));
  assert.match(report, /\$F\$ locally\s+bounded near \$\(0,0\)\$/);
  assert.match(report, /no claim is made about a\s+pathological right side singular at \$\(0,0\)\$/);
  assert.match(report, /different\s+rescaled initial data and are different solutions/);
  assert.match(report, /one\s+solution history concentrating at a fixed \$t_0=T>0\$/);
});

test("locks the bounded eight-source primary-literature audit", async () => {
  const report = await readFile(new URL("r070i_report-source.md", research), "utf8");

  assert.match(report, /stopped after eight new\s+high-signal primary sources/);
  for (const author of [
    "Auscher--Monniaux--Portal",
    "Auscher--Frey",
    "Germain--Pavlović--Staffilani",
    "Jia--Šverák",
    "Bradshaw--Tsai",
    "Eyink--Aluie",
    "Cheskidov--Constantin--Friedlander--Shvydkoy",
    "Kovač--Zorin-Kranich",
  ]) {
    assert.ok(report.includes(author), author);
  }
  assert.ok(report.includes(String.raw`B:(E_T)^n\times(E_T)^n\to(E_T)^n`));
  assert.ok(report.includes(String.raw`r^{-3}\int_{Q_r}|F(x,t)|^2`));
  assert.ok(report.includes(String.raw`\int_{B_{Cr}}|\Omega_k(x,t)|^2dx`));
  assert.match(report, /bounded search finding, not a proof that no such\s+theorem exists/);
});

test("archives the final independent PASS audit", async () => {
  const audit = await readFile(new URL("r070i_independent_audit.md", research), "utf8");

  assert.match(audit, /(?:Final status|Overall(?: verdict)?):\*{0,2}\s*PASS\b/i);
  assert.match(audit, /not external peer review/i);
  assert.match(audit, /Millennium/i);
});

test("reproduces the 12-check R0.70I producer with stdout equal to result", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070i_temporal_hardy_audit.py", research));
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70I");
  assert.equal(archived.status, "exact-finite-temporal-hardy-scaling-audit");
  assert.equal(Object.keys(archived.checks).length, 12);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
  assert.equal(archived.temporalThreshold.criticalAlpha, "1/4");
  assert.equal(archived.temporalHardyKernel.finiteRegionCasesChecked, 162);
  assert.equal(archived.frozenLowMixedScale.currentBandLedger.finalOuterPower, "-3/2");
  assert.equal(archived.nseScaling.outerRadiusAndTop, "r_0=r and t_0=r^2");
  assert.match(archived.claimBoundary.notComputerProved, /lower-triangular LP convolution/);
});

test("locks every R0.70I certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 7);
  assert.match(sums, /\.\.\/\.\.\/r070i_temporal_hardy_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070i_report-source\.md/);
  assert.match(sums, /\.\.\/\.\.\/r070i_literature_audit\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid checksum line: ${line}`);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives the 10-file figure package and its 20-check validation", async () => {
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
  const validation = JSON.parse(
    await readFile(new URL("validation.json", figureRoot), "utf8"),
  );
  const contract = JSON.parse(await readFile(new URL("contract.json", figureRoot), "utf8"));
  const caption = await readFile(new URL("caption.md", figureRoot), "utf8");
  const figureContract = await readFile(
    new URL("figure-contract.md", figureRoot),
    "utf8",
  );

  assert.equal(manifest.figureId, "fig-r070i-temporal-hardy");
  assert.equal(manifest.release, "R0.70I");
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
    assert.equal(
      createHash("sha256").update(payload).digest("hex"),
      output.sha256,
      output.path,
    );
  }

  assert.equal(validation.release, "R0.70I");
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 20);
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.equal(validation.diagnostics.normalizedTargetScaleFactorOverDualScaleFactor, 1);
  assert.equal(contract.panels.find(({ id }) => id === "C").id, "C");
  assert.match(contract.panels.find(({ id }) => id === "C").takeaway, /both scale as/);
  assert.match(caption, /closed-form/i);
  assert.match(figureContract, /not a simulated NSE trajectory/i);
  assert.ok((await stat(new URL("figure.png", figureRoot))).size > 500_000);
  assert.ok((await stat(new URL("figure.pdf", figureRoot))).size > 40_000);
  assert.ok((await stat(new URL("figure.svg", figureRoot))).size > 90_000);
});
