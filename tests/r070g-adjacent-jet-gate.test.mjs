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
const certificateRoot = new URL("certificates/r070g/", research);
const figureRoot = new URL(
  "figures/r070g-critical-transport/fig-r070g-critical-transport/",
  root,
);

test("locks the fixed-source difference boundary", async () => {
  const report = await readFile(new URL("r070g_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.ok(report.includes(String.raw`E_{J,k}-E_{J-1,k}=K*(\psi_J\Omega_k)`));
  assert.match(report, /same \$k\$ is not\s+held fixed/);
  assert.match(report, /not one\s+fixed exterior source producing a\s+harmonic field/);
  assert.match(report, /never substitutes \(2\.3\) or \(2\.4\) for \(2\.2\)/);
  assert.match(report, /not a martingale or frequency Littlewood--Paley decomposition/);
  assert.ok(report.includes(String.raw`\widehat{\psi_j\Omega}=\widehat{\psi_j}*\widehat\Omega`));
});

test("locks the exact critical transport and dilation defect", async () => {
  const report = await readFile(new URL("r070g_report-source.md", research), "utf8");

  assert.ok(
    report.includes(
      String.raw`h_j^{(n)}=c_j^{(n)}-2^{-(n+2)}c_{j-1}^{(n)}`,
    ),
  );
  assert.match(report, /\$1\/4,1\/8,1\/16\$/);
  assert.match(report, /critical dilation defect/);
  assert.ok(report.includes(String.raw`h=(I-\lambda_n S)c`));
  assert.ok(report.includes(String.raw`(1-\lambda_n)\|c\|_{\ell^p}`));
  assert.ok(report.includes(String.raw`c_m-c_{m-1}=\lambda^{m-1}`));
  assert.match(report, /ordinary adjacent difference can be small precisely while/);
});

test("locks signed Abel telescoping and the changing-core defect", async () => {
  const report = await readFile(new URL("r070g_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\sum_{j=a}^b(P_j-P_{j-1}):M_j`));
  assert.ok(report.includes(String.raw`P_j:(M_j-M_{j+1})`));
  assert.match(report, /fixed and the same signed core moment/);
  assert.match(report, /positive-part operation/);
  assert.match(report, /source cancellation/);
  assert.match(report, /positive double-scale packing/);
});

test("locks the source square function and exact dual gap", async () => {
  const report = await readFile(new URL("r070g_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`r_j^{2n+3}|J_j^{(n)}(x_0)|^2`));
  assert.ok(report.includes(String.raw`r_j^{-1}|h_j^{(n)}|^2`));
  assert.match(report, /bounded annular overlap and Calder[oó]n--Zygmund/);
  assert.match(report, /point evaluation is not a bounded functional on \$L\^2\$/);
  assert.ok(report.includes(String.raw`r_j^{-3}|M_j^{(0)}|^2`));
  assert.ok(report.includes(String.raw`r_j^{-5}|M_j^{(1)}|^2`));
  assert.match(report, /sufficient condition, not a conclusion/);
  assert.match(report, /exactly dual scale weights/);
});

test("locks the full-grid and active-only pressure tests", async () => {
  const report = await readFile(new URL("r070g_report-source.md", research), "utf8");

  assert.match(report, /target-normalized diagonal\s+observables/);
  assert.ok(report.includes(String.raw`2N\Lambda^{-2}`));
  assert.ok(report.includes(String.raw`2N\Lambda^{-4}`));
  assert.ok(report.includes(String.raw`12N\Lambda^{-3}`));
  assert.ok(report.includes(String.raw`72N\Lambda^{-6}`));
  assert.ok(report.includes(String.raw`A_1=\operatorname{diag}(1,-1/4,-3/4)`));
  assert.ok(report.includes(String.raw`\|A_1-A_0\|_F^2=\frac18`));
  assert.ok(report.includes(String.raw`\Phi_1=x_1^3-\frac32x_1(x_2^2+x_3^2)`));
  assert.ok(report.includes(String.raw`\|B_1-B_0\|_F^2=54`));
  assert.match(report, /unequal norms exclude orthogonal equivalence/);
});

test("locks the scalar-baseline dichotomy and radial correction", async () => {
  const report = await readFile(new URL("r070g_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`s_{n+1}^{(q)}-s_n^{(q)}=0`));
  assert.ok(report.includes(String.raw`w_n^{(0)}=c_\chi\eta^3\Lambda^{-2}b_n^2`));
  assert.ok(report.includes(String.raw`\sum_{n=1}^Nw_n^{(q)}\ge C_qN`));
  assert.match(report, /adjacent work variation is bounded/);
  assert.match(report, /not a universal no-go theorem/);
  assert.ok(report.includes(String.raw`F(x)=-\frac{a_0}{6}|x|^2+C`));
  assert.match(report, /solid rotation and has zero strain/);
  assert.match(report, /No source is silently deleted/);
});

test("locks the literature and common-time boundaries", async () => {
  const report = await readFile(new URL("r070g_report-source.md", research), "utf8");

  assert.match(report, /unique small global solution in its \$X\$ class/);
  assert.match(report, /does not give an \$N\$-uniform\s+persistence interval/);
  assert.match(report, /no theorem matching the\s+target was found in the audited primary sources/);
  assert.match(report, /not a proof that no\s+such theorem exists anywhere/);
  assert.match(report, /R0\.70H success criterion/);
  assert.match(report, /core-moment filter\/time variation problem/);
  assert.match(
    report,
    /Nothing here constructs a\s+common positive terminal time[\s\S]*solution of the Millennium problem/,
  );
});

test("archives the independent correction audit", async () => {
  const audit = await readFile(new URL("r070g_independent_audit.md", research), "utf8");

  assert.match(audit, /Final status:\*\* PASS after correction/);
  assert.match(audit, /Leray dissipation-level spacetime weighted coefficient estimate/);
  assert.ok(audit.includes("target-normalized sequences with \\(k(j)=j+M\\)"));
  assert.match(audit, /generator\/carrier transition plateaus/);
  assert.match(audit, /not external peer review/);
  assert.match(audit, /does not establish[\s\S]*Millennium solution/);
});

test("reproduces the exact R0.70G symbolic certificate", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070g_adjacent_jet_audit.py", research));
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.status, "exact-symbolic-audit");
  assert.equal(archived.release, "R0.70G");
  assert.equal(archived.criticalTransport.factors["0"], "1/4");
  assert.equal(archived.criticalTransport.factors["1"], "1/8");
  assert.equal(archived.criticalTransport.factors["2"], "1/16");
  assert.equal(archived.alternatingProfiles.constantDifferenceSquared, "1/8");
  assert.equal(archived.alternatingProfiles.linearDifferenceSquared, "54");
  assert.equal(archived.fullGridSpikes.constantSquareMass, "2*N*Lambda^(-4)");
  assert.equal(archived.initialFaceWork.pairedScalarDifferences, "0 for both alternating families");
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks every R0.70G certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 6);
  assert.match(sums, /\.\.\/\.\.\/r070g_adjacent_jet_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070g_report-source\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives the journal-style analytic figure and claim boundary", async () => {
  const manifest = JSON.parse(await readFile(new URL("manifest.json", figureRoot), "utf8"));
  const validation = JSON.parse(
    await readFile(new URL("validation.json", figureRoot), "utf8"),
  );
  const caption = await readFile(new URL("caption.md", figureRoot), "utf8");
  const contract = await readFile(new URL("figure-contract.md", figureRoot), "utf8");
  const svg = await readFile(new URL("figure.svg", figureRoot), "utf8");

  assert.equal(manifest.status, "explanatory");
  assert.equal(manifest.release, "R0.70G");
  assert.equal(manifest.source, "plot.py");
  const plotSource = await readFile(new URL("plot.py", figureRoot));
  assert.equal(createHash("sha256").update(plotSource).digest("hex"), manifest.sourceSha256);
  assert.match(manifest.claimBoundary, /not simulation evidence or a numerical PDE proof/i);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.match(caption, /closed formula/i);
  assert.match(contract, /No fitted parameter, sampled\s+trajectory, or simulation output/i);
  assert.match(svg, /Critical dilation/i);
  assert.match(svg, /source/i);
  assert.ok((await stat(new URL("figure.png", figureRoot))).size > 300_000);
  assert.ok((await stat(new URL("figure.pdf", figureRoot))).size > 20_000);
  assert.ok((await stat(new URL("figure.svg", figureRoot))).size > 30_000);
});
