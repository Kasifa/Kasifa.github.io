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
const certificateRoot = new URL("certificates/r070h/", research);
const figureRoot = new URL(
  "figures/r070h-core-moment-gap/fig-r070h-core-moment-gap/",
  root,
);

test("locks the report scope and nonlinear-work boundary", async () => {
  const report = await readFile(new URL("r070h_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /single reindexed source--core scale chain/);
  assert.match(report, /not an\s+identification with the complete two-index moving-shell positive packing/);
  assert.match(
    report,
    /weighted parabolic\s+(?:>\s*)?source--core embedding, not ordinary moment variation/,
  );
  assert.match(
    report,
    /Nothing in this report proves global regularity, produces a singularity, or\s+solves the Millennium problem/,
  );
});

test("locks the instantaneous critical m/c normalization", async () => {
  const report = await readFile(new URL("r070h_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`c_k^{(n)}=r_k^{n+2}P_k^{(n)}`));
  assert.ok(report.includes(String.raw`m_k^{(n)}=r_k^{1-n}M_k^{(n)}`));
  assert.ok(report.includes(String.raw`r_k^3P_k^{(n)}:M_k^{(n)}`));
  assert.ok(report.includes(String.raw`=c_k^{(n)}:m_k^{(n)}`));
  assert.ok(report.includes(String.raw`m_k^{(0)}=r_kM_k^{(0)}`));
  assert.ok(report.includes(String.raw`m_k^{(1)}=M_k^{(1)}`));
  assert.match(report, /Neither coordinate may be substituted for the\s+other without carrying its scale weight/);
});

test("locks the actual spacetime work and time-dependent coefficient boundary", async () => {
  const report = await readFile(new URL("r070h_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`r_k\int_{I_k}P_k^{(n)}:M_k^{(n)}\,dt`));
  assert.ok(report.includes(String.raw`=r_k^{-2}\int_{I_k}c_k^{(n)}(t):m_k^{(n)}(t)\,dt`));
  assert.ok(report.includes(String.raw`\bar m_k^{(n)}`));
  assert.ok(report.includes(String.raw`=r_k^{-2}\int_{I_k}m_k^{(n)}(t)\,dt`));
  assert.match(report, /Only when \$c_k\^\{\(n\)\}\(t\)\$ is constant on \$I_k\$ may \(2\.6\) be factored/);
  assert.match(report, /No such time constancy is assumed in the\s+Navier--Stokes problem/);
});

test("locks the rho/lambda indexing and the two instantaneous covariances", async () => {
  const report = await readFile(new URL("r070h_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\lambda_k^{(n)}=\rho_{k-1}^{n+2}`));
  assert.ok(report.includes(String.raw`\left(\frac{r_k}{r_{k-1}}\right)^{n+2}`));
  assert.ok(
    report.includes(String.raw`m_k^{(n)}-\rho_k^{n+2}m_{k+1}^{(n)}`),
  );
  assert.ok(
    report.includes(String.raw`m_{k+1}^{(n)}-\rho_k^{1-n}m_k^{(n)}`),
  );
  assert.ok(
    report.includes(
      String.raw`n&\text{geometric factor}&\text{pairing factor}`,
    ),
  );
  assert.ok(report.includes(String.raw`0&\rho&\rho^2`));
  assert.ok(report.includes(String.raw`1&1&\rho^3`));
  assert.match(report, /Their factors are different/);
});

test("locks the adjacent-scale ledger and one-sided fixed-time ell1 gain", async () => {
  const report = await readFile(new URL("r070h_report-source.md", research), "utf8");

  assert.match(
    report,
    /finite chain \$0\\le k\\le N\$, or a one-sided\s+fine-scale chain/,
  );
  assert.ok(report.includes(String.raw`Q_{k+1}-Q_k`));
  assert.ok(report.includes(String.raw`(\rho_k^{1-n}-1)m_k^{(n)}`));
  assert.ok(report.includes(String.raw`(\chi_{k+1}-\chi_k)y^{\otimes n}`));
  assert.ok(report.includes(String.raw`\sum_k\|D_k\|_2^2\le C_\varphi\|\omega\|_2^2`));
  assert.ok(
    report.includes(String.raw`\sum_k|m_{k+1}^{(n)}-m_k^{(n)}|`),
  );
  assert.ok(
    report.includes(String.raw`\sum_k|\mathfrak D_k^{\rm pair}m^{(n)}|`),
  );
  assert.ok(report.includes(String.raw`fixed-time $\ell_k^1$ variation`));
  assert.ok(report.includes(String.raw`common-time $L_t^1\ell_k^1$ integral`));
});

test("locks the spacetime N coordinate, overlap factors, and r^-3 dual weight", async () => {
  const report = await readFile(new URL("r070h_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\mathcal N_k^{(n)}(t)`));
  assert.ok(
    report.includes(
      String.raw`=r_k^{-2}\mathbf 1_{I_k}(t)m_k^{(n)}(t)`,
    ),
  );
  assert.ok(
    report.includes(String.raw`m_k^{(n)}-\rho_k^n m_{k+1}^{(n)}`),
  );
  assert.ok(
    report.includes(
      String.raw`overlap factor is $1$ for $n=0$ and $\rho_k$ for $n=1$`,
    ),
  );
  assert.ok(
    report.includes(
      String.raw`the instantaneous pairing factors $\rho_k^2$ and $\rho_k^3$`,
    ),
  );
  assert.ok(report.includes(String.raw`r_k^{-3}`));
  assert.ok(report.includes(String.raw`L_t^2\ell_k^2(r_k^{-1})`));
  assert.ok(report.includes(String.raw`L_t^2\ell_k^2(r_k)`));
  assert.match(report, /No bound for \(7\.3a\) has been proved/);
});

test("locks the filtered moment identity and circular stretching boundary", async () => {
  const report = await readFile(new URL("r070h_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`C_{ai}=\tau_{ai}^{\omega u}-\tau_{ai}^{u\omega}`));
  assert.ok(report.includes(String.raw`\partial_t\Omega_i+U_a\partial_a\Omega_i`));
  assert.ok(report.includes(String.raw`\int\phi\,S(U):\Omega\otimes\Omega`));
  assert.ok(report.includes(String.raw`-\int C_{ai}\partial_a(\phi\Omega_i)`));
  assert.match(report, /absolute time-variation estimate[\s\S]*already contains the\s+target vortex-stretching term/);
  assert.match(report, /circular estimate rather than a new input/);
  assert.match(report, /asserted for smooth filtered solutions/);
});

test("locks the R0.70F initial-face witness and persistence boundary", async () => {
  const report = await readFile(new URL("r070h_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\rho=\frac{r_{n+1}}{r_n}=\Lambda^{-2}`));
  assert.ok(report.includes(String.raw`q=\rho^2=\Lambda^{-4}`));
  assert.ok(report.includes(String.raw`b_n=\frac{1-q^n}{1-q}`));
  assert.ok(report.includes(String.raw`m_n^{(0)}=C_0b_n^2E`));
  assert.ok(report.includes(String.raw`m_n^{(1)}=C_1b_n^2T`));
  assert.match(report, /ordinary variation is bounded while the pairing-covariant variation and\s+square mass are linear/);
  assert.match(report, /instantaneous vorticity \$L\^2\$ norm at the initial face is not uniformly\s+bounded/);
  assert.match(report, /not a counterexample on nested\s+backward cylinders with one common positive terminal time/);
  assert.match(report, /not the fine-window factors in\s+the spacetime coordinate/);
});

test("locks the bounded eight-source audit and fixed-family source boundary", async () => {
  const report = await readFile(new URL("r070h_report-source.md", research), "utf8");

  assert.match(report, /search stopped after eight primary sources/);
  for (const author of [
    "Caffarelli--Kohn--Nirenberg",
    "Duchon--Robert",
    "Dascaliuc--Grujić",
    "Fefferman--Stein",
    "Koch--Tataru",
    "Jones--Seeger--Wright",
    "Do--Muscalu--Thiele",
  ]) {
    assert.ok(report.includes(author), author);
  }
  assert.match(report, /No theorem matching the complete target was found in this bounded audit/);
  assert.match(report, /not a proof that no such theorem exists/);
  assert.match(report, /for one fixed source\/filter family/);
  assert.match(report, /if the source filter itself changes with the\s+core index, \(7\.1\) cannot simply be reused/);
  assert.match(report, /Still open in this route/);
});

test("archives the final independent PASS audit", async () => {
  const audit = await readFile(new URL("r070h_independent_audit.md", research), "utf8");

  assert.match(
    audit,
    /(?:Final status|Overall(?: verdict)?):\*{0,2}\s*PASS\b/i,
  );
  assert.match(audit, /not external peer review/i);
  assert.match(audit, /Millennium/i);
});

test("reproduces the exact R0.70H symbolic regression certificate", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070h_core_moment_audit.py", research));
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.status, "exact-symbolic-regression-audit");
  assert.equal(archived.release, "R0.70H");
  assert.equal(
    archived.criticalMoments.spacetimeCoordinate,
    "N_k^(n)=r_k^(-2)*1_(I_k)*m_k^(n)",
  );
  assert.equal(archived.exactLedgers.spacetimeOverlapFactors.degree0, "1");
  assert.equal(archived.exactLedgers.spacetimeOverlapFactors.degree1, "rho_k");
  assert.equal(archived.exactLedgers.spacetimeDualWeight, "r_k*(r_k^(-2))^2=r_k^(-3)");
  assert.equal(archived.constantCorePressureTest.geometryChecked, false);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks every R0.70H certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 6);
  assert.match(sums, /\.\.\/\.\.\/r070h_core_moment_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070h_report-source\.md/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid checksum line: ${line}`);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives the journal-style core-moment gap figure package", async () => {
  const manifest = JSON.parse(await readFile(new URL("manifest.json", figureRoot), "utf8"));
  const validation = JSON.parse(
    await readFile(new URL("validation.json", figureRoot), "utf8"),
  );
  const caption = await readFile(new URL("caption.md", figureRoot), "utf8");
  const contract = await readFile(new URL("figure-contract.md", figureRoot), "utf8");

  assert.equal(manifest.figureId, "fig-r070h-core-moment-gap");
  assert.equal(manifest.status, "explanatory");
  assert.equal(manifest.release, "R0.70H");
  assert.equal(manifest.source, "plot.py");
  const plotSource = await readFile(new URL(manifest.source, figureRoot));
  assert.equal(createHash("sha256").update(plotSource).digest("hex"), manifest.sourceSha256);
  assert.match(manifest.claimBoundary, /not simulation evidence or a numerical PDE proof/i);

  const outputPaths = new Set(manifest.outputs.map(({ path }) => path));
  for (const required of ["figure.png", "figure.pdf", "figure.svg", "validation.json"]) {
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

  assert.equal(validation.release, "R0.70H");
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.ok(caption.length > 100);
  assert.ok(contract.length > 100);
  assert.ok((await stat(new URL("figure.png", figureRoot))).size > 300_000);
  assert.ok((await stat(new URL("figure.pdf", figureRoot))).size > 20_000);
  assert.ok((await stat(new URL("figure.svg", figureRoot))).size > 30_000);
});
