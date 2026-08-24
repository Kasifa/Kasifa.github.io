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
const certificateRoot = new URL("certificates/r070b/", research);

test("locks the matching-scale bridge and its exact direction", async () => {
  const report = await readFile(new URL("r070b_report-source.md", research), "utf8");

  assert.match(report, /internal research report; not a public theorem chapter/);
  assert.match(report, /n\(j\)=-j\+O\(1\)/);
  assert.ok(report.includes("\\eta_j(z)=\\eta(z/r_j)"));
  assert.ok(report.includes("\\sup_j\\|\\eta_j\\|_\\infty"));
  assert.ok(report.includes("|W_{j,k}|"));
  assert.ok(report.includes("2^{-(k-j)}\\mathfrak A_{j,k}\\mathcal Q_k"));
  assert.match(report, /reproduces the factor in Yu's Proposition 8\.6/);
  assert.ok(report.includes("There is no universal constant \\(c>0\\)"));
  assert.match(report, /kinematic family, not a[\s\S]*Navier--Stokes trajectory/);
  assert.ok(report.includes("D^{\\mathrm{sign}}_{j,k}"));
  assert.ok(report.includes("|w_{j,k}^{\\mathrm{Yu}}(x,t)-w_{j,k}^{\\eta}(x,t)|"));
  assert.ok(report.includes("\\delta_z u(x)=(-z_2,0,0)"));
  assert.match(report, /actual positive annular shell-work/);
  assert.ok(report.includes("\\le C_{\\mathrm{geom}}"));
  assert.ok(report.includes("|w^{\\mathrm{Yu}}_{j,k}(x,t)|"));
  assert.match(report, /Equation \(6\.4\) is not a closure estimate/);
  assert.match(report, /maximal honest ledger/);
});

test("records the same-cylinder subgrid counterexample without promoting it to dynamics", async () => {
  const report = await readFile(new URL("r070b_report-source.md", research), "utf8");

  assert.ok(report.includes("u_N=N^{-1/3}v+N^{2/3}w_N"));
  assert.ok(report.includes("=O(N^{-1})\\longrightarrow0"));
  assert.ok(report.includes("=cN+o(N)\\longrightarrow\\infty"));
  assert.ok(report.includes("N^{1/3}C_\\ell(v,w_N)"));
  assert.ok(report.includes("H=S_\\ell^*G\\ne0"));
  assert.ok(report.includes("F^{\\mathrm{com}}_{r,\\ell}(u)"));
  assert.ok(report.includes("\\widetilde{\\mathcal S}^{(2)}_{r,\\ell}(u_N)\\asymp N^{8/3}"));
  assert.match(report, /no universal \*\*kinematic\*\* bound/);
  assert.match(report, /not a Navier--Stokes trajectory on the whole parabolic interval/);
  assert.match(report, /does not\s+exclude a genuinely dynamical estimate/);
});

test("states the 3:4:5 no-go with its narrow exact-generation boundary", async () => {
  const report = await readFile(new URL("r070b_report-source.md", research), "utf8");

  assert.match(report, /### Theorem 8\.1 \[O\]/);
  assert.match(report, /nonnegative smooth annular[\s\S]*nonincreasing profile/);
  assert.match(report, /There is no continuous,\s+polynomially bounded/);
  assert.match(report, /translation-invariant, self-adjoint matrix Fourier/);
  assert.match(report, /exact generation with zero cubic remainder/);
  assert.ok(report.includes("\\widehat f(k)=\\int_{\\mathbb R^3}e^{-ik\\cdot x}f(x)"));
  assert.ok(report.includes("m_3=m_r(k),\\qquad m_4=m_r(p),\\qquad m_5=m_r(q)"));
  assert.ok(report.includes("16g_4-9g_3-7g_5=0"));
  assert.ok(report.includes("\\frac{72}{5}I_4(\\varepsilon r)^4"));
  assert.ok(
    report.includes("Using all of \\(O(3)\\), rather than only \\(SO(3)\\), is essential"),
  );
  assert.match(report, /little-o of this obstruction/);
  assert.ok(report.includes("the \\(O(3)\\)-averaged remainder"));
  assert.match(report, /prescribed scale law[\s\S]*independent of the solution amplitude/);
  assert.doesNotMatch(report, /under independent review/);
  assert.match(report, /Nothing in this report proves regularity or finite-time blow-up/);
  assert.doesNotMatch(report, /Theorem 8\.1 proves Navier--Stokes regularity/);

  const tags = [...report.matchAll(/\\tag\{([^}]+)\}/g)].map((match) => match[1]);
  assert.equal(tags.length, new Set(tags).size);
  assert.equal((report.match(/\\\[/g) ?? []).length, (report.match(/\\\]/g) ?? []).length);
  assert.doesNotMatch(report, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(report, /[ \t]+$/m);
});

test("reproduces the exact symbolic triad result", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070b_triad_audit.py", research));
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.status, "exact-symbolic-audit");
  assert.equal(archived.singleOrientedTriadCommonFactorRemoved, "sqrt(2)/50");
  assert.equal(archived.realSixModeCommonFactor, "sqrt(2)/25");
  assert.equal(archived.rankDerivativeMatrix, 2);
  assert.deepEqual(archived.derivativeTimesEnergyGauge, ["0", "0", "0", "0"]);
  assert.deepEqual(archived.constantWeightCheck, ["0", "0", "0", "0"]);
  assert.deepEqual(archived.squaredLengthTargetNullCheck, ["0", "0", "0", "0"]);
  assert.equal(archived.necessaryCondition, "16*g4 - 9*g3 - 7*g5 = 0");
  assert.equal(archived.smallFrequencyExpansion.leadingI4Coefficient, "72/5");
  assert.equal(archived.checks.floatCount, 0);
  assert.ok(Object.values(archived.checks).every((value) => value === true || value === 0));
});

test("locks every R0.70B symbolic payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070b_triad_audit\.py/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid checksum line: ${line}`);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("keeps compute and publication decisions proportional to the gate", async () => {
  const report = await readFile(new URL("r070b_report-source.md", research), "utf8");

  assert.match(report, /\*\*DGX:\*\* not justified/);
  assert.match(report, /\*\*Public site:\*\* do not publish this revision/);
  assert.match(report, /does not reduce the hypotheses of a regularity theorem/);
  assert.match(report, /does not advance a[\s\S]*Millennium-problem claim/);
});
