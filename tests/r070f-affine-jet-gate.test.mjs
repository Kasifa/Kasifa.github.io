import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { stat, readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const root = new URL("../", import.meta.url);
const research = new URL("research/", root);
const certificateRoot = new URL("certificates/r070f/", research);
const figureRoot = new URL(
  "figures/r070f-affine-jet-saturation/fig-r070f-affine-jet-saturation/",
  root,
);

test("locks the fixed-annulus source boundary and project observables", async () => {
  const report = await readFile(new URL("r070f_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /fixed-source tensor/);
  assert.match(report, /project-defined scale-invariant instantaneous/);
  assert.match(report, /None of these is renamed as Yu's positive moving-shell scalar/);
  assert.match(report, /not uniform over\s+all filters or partitions/);
  assert.match(report, /initial-face statement/);
  assert.match(report, /not a\s+counterexample on the nested backward cylinders/);
});

test("locks the exact Taylor-work ledger and tensor moments", async () => {
  const report = await readFile(new URL("r070f_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`|\mathcal W^{(0)}_{j,k}|`));
  assert.ok(report.includes(String.raw`\theta\,\mathfrak A^{\psi}_{j,k}\mathcal Q_k`));
  assert.ok(report.includes(String.raw`\theta^2\,\mathfrak A^{\psi}_{j,k}\mathcal Q_k`));
  assert.ok(report.includes(String.raw`\theta^3\mathfrak A^{\psi}_{j,k}\mathcal Q_k`));
  assert.ok(report.includes(String.raw`\theta^4\mathfrak A^{\psi}_{j,k}\mathcal Q_k`));
  assert.match(report, /symmetric, trace-free, divergence-free, and\s+componentwise harmonic/);
  assert.ok(report.includes(String.raw`C_{ij\ell m}=C_{ji\ell m}=C_{ijm\ell}`));
  assert.ok(report.includes(String.raw`\sum_i C_{ijim}=0`));
  assert.ok(report.includes(String.raw`\sum_\ell C_{ij\ell\ell}=0`));
  assert.ok(report.includes(String.raw`M^{(0)}-\frac{\operatorname{tr}M^{(0)}}3I`));
  assert.match(report, /not under incompressibility alone/);
  assert.match(report, /signed cancellation\s+between pieces cannot be passed through/);
});

test("locks the compact constant and linear jet generators", async () => {
  const report = await readFile(new URL("r070f_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\mathcal L[P]`));
  assert.ok(report.includes(String.raw`-\frac1{d+2}\zeta(x)\,x\times P(x)`));
  assert.ok(report.includes(String.raw`A=\operatorname{diag}(1,-1/2,-1/2)`));
  assert.ok(report.includes(String.raw`\Phi(x)=x_1^3-3x_1x_2^2`));
  assert.ok(report.includes(String.raw`e_1\cdot L(ce_1)e_1=6c>0`));
  assert.ok(report.includes(String.raw`W x=\frac12e_1\times x`));
  assert.ok(report.includes(String.raw`\nabla\times V=e_1`));
  assert.ok(report.includes(String.raw`\operatorname{sym}\nabla V=0`));
  assert.ok(
    report.includes(String.raw`return vorticity created by \(\zeta\) is retained`),
  );
});

test("locks exact initial-face saturation and its NSE boundary", async () => {
  const report = await readFile(new URL("r070f_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`R_n=\Lambda^{-2n}`));
  assert.ok(report.includes(String.raw`r_n=R_n/\Lambda`));
  assert.ok(report.includes(String.raw`\sigma+\frac2\Lambda<c-\eta`));
  assert.ok(report.includes(String.raw`b_n=\sum_{a=0}^{n-1}\Lambda^{-4a}`));
  assert.ok(report.includes(String.raw`\Omega_{\ell_n}[f]`));
  assert.ok(report.includes(String.raw`\operatorname{supp}\psi_{j_n}`));
  assert.ok(report.includes(String.raw`R_n\le |y|\le2R_n`));
  assert.match(report, /radial-shell lemma/);
  assert.ok(report.includes(String.raw`\nabla F_n\times e_1=0`));
  assert.ok(report.includes(String.raw`c_\chi\eta^3\Lambda^{-2}b_n^2>0`));
  assert.ok(report.includes(String.raw`6c\,c_\chi\eta^3\Lambda^{-3}b_n^2>0`));
  assert.match(report, /No cross source was deleted/);
  assert.ok(report.includes(String.raw`\sup_N\|f_N^{(q)}\|_{BMO^{-1}}<\infty`));
  assert.ok(report.includes(String.raw`\(\varepsilon_*>0\), independent of \(N\)`));
  assert.ok(report.includes("No \\(N\\)-independent lower bound"));
  assert.match(report, /R0\.70F neither constructs nor excludes that\s+cascade/);
});

test("locks the exact discrete no-go and surviving route", async () => {
  const report = await readFile(new URL("r070f_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\frac{N}{2^\beta-1}`));
  assert.ok(report.includes(String.raw`\frac1{2^\beta-1}>0`));
  assert.ok(report.includes(String.raw`\text{affine remainder}&3&1/7`));
  assert.match(report, /no finite Taylor subtraction/);
  assert.match(report, /Taylor improvement alone cannot manufacture that\s+summability/);
  assert.match(report, /termwise absolute-value\s+majorant/);
  assert.match(report, /not a no-go theorem for an actual spacetime packing/);
  assert.match(report, /does not rule out\s+cancellation in the true spacetime sum/);
  assert.match(report, /R0\.70G/);
  assert.ok(report.includes("adjacent-source"));
  assert.ok(report.includes("martingale differences"));
});

test("archives the independent correction audit", async () => {
  const audit = await readFile(new URL("r070f_independent_audit.md", research), "utf8");

  assert.match(audit, /Final status:\*\* PASS after correction/);
  assert.match(audit, /coarser carriers contribute constant filtered vorticity/);
  assert.match(audit, /Newton radial-shell lemma/);
  assert.ok(audit.includes(String.raw`small solution class \(X\)`));
  assert.match(audit, /not external peer review/);
  assert.match(audit, /no claim of large-data regularity, singularity/);
});

test("reproduces the exact R0.70F symbolic certificate", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070f_affine_jet_audit.py", research));
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.status, "exact-symbolic-audit");
  assert.equal(archived.release, "R0.70F");
  assert.equal(
    archived.initialFaceWork.constantInterlacedFormula,
    "b**2*c_chi*eta**3/Lambda**2",
  );
  assert.equal(
    archived.initialFaceWork.linearInterlacedFormula,
    "6*b**2*c*c_chi*eta**3/Lambda**3",
  );
  assert.equal(archived.triangularDyadicSum.asymptoticSlopes["3"], "1/7");
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks every R0.70F certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 6);
  assert.match(sums, /\.\.\/\.\.\/r070f_affine_jet_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070f_report-source\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives the journal-style analytic figure and its claim boundary", async () => {
  const manifest = JSON.parse(await readFile(new URL("manifest.json", figureRoot), "utf8"));
  const validation = JSON.parse(
    await readFile(new URL("validation.json", figureRoot), "utf8"),
  );
  const caption = await readFile(new URL("caption.md", figureRoot), "utf8");
  const contract = await readFile(new URL("figure-contract.md", figureRoot), "utf8");
  const svg = await readFile(new URL("figure.svg", figureRoot), "utf8");

  assert.equal(manifest.status, "explanatory");
  assert.equal(manifest.release, "R0.70F");
  assert.equal(manifest.source, "plot.py");
  const plotSource = await readFile(new URL("plot.py", figureRoot));
  assert.equal(createHash("sha256").update(plotSource).digest("hex"), manifest.sourceSha256);
  assert.match(manifest.claimBoundary, /not simulation evidence or a numerical PDE proof/i);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.match(caption, /not DNS,\s+trajectory/);
  assert.match(contract, /not a fluid simulation/);
  assert.match(svg, /Taylor gain is exact/);
  assert.match(svg, /Every fixed power still grows/);
  assert.match(svg, /Initial-face witness/);
  assert.ok((await stat(new URL("figure.png", figureRoot))).size > 300_000);
  assert.ok((await stat(new URL("figure.pdf", figureRoot))).size > 20_000);
  assert.ok((await stat(new URL("figure.svg", figureRoot))).size > 30_000);
});
