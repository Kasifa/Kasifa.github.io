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
const certificateRoot = new URL("certificates/r070d/", research);
const figureRoot = new URL(
  "figures/r070d-cover-blindness/fig-r070d-cover-blindness/",
  root,
);

test("locks the fixed-resolution cutoff class and uniform positive averages", async () => {
  const report = await readFile(new URL("r070d_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.ok(report.includes(String.raw`\theta\in W^{1,1}(\mathbb T^3),\qquad \theta\ge0`));
  assert.ok(report.includes(String.raw`\|\partial_1\theta\|_{L^1(d\mu)}\le C_1<\infty`));
  assert.ok(report.includes(String.raw`N\ge \frac{2C_1}{\delta m_0}`));
  assert.ok(report.includes(String.raw`f_{\delta,N}(x)=\delta+\sin(Nx_1)`));
  assert.ok(report.includes(String.raw`\frac{\delta}{2}`));
  assert.ok(report.includes(String.raw`\le \langle f_{\delta,N}\rangle_\theta`));
  assert.ok(report.includes(String.raw`\le \frac{3\delta}{2}`));
  assert.match(report, /every ensemble \(2\.5\) lies in the same interval/);
});

test("locks the exact order-one negative mass and vanishing-observation no-go", async () => {
  const report = await readFile(new URL("r070d_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`2\sqrt{1-\delta^2}`));
  assert.ok(report.includes(String.raw`c_*:=\frac{\sqrt3-\pi/3}{2\pi}>0`));
  assert.ok(report.includes(String.raw`\int_{\mathbb T^3}f_{\delta,N}\,d\mu=\delta`));
  assert.ok(report.includes(String.raw`\longrightarrow\frac1\pi`));
  assert.ok(report.includes(String.raw`\sim\frac1{\pi\delta}`));
  assert.ok(report.includes("There is no modulus \\(\\omega(s)\\to0"));
  assert.ok(report.includes(String.raw`\le\frac{3\delta_j}{2}\longrightarrow0`));
  assert.ok(report.includes("while the left side of (3.12) is at least \\(c_*\\)"));
});

test("aligns with primary optimal-cover definitions without overstating equivalence", async () => {
  const report = await readFile(new URL("r070d_report-source.md", research), "utf8");

  assert.match(report, /Dascaliuc--Grujić's energy-cascade paper defines/);
  assert.match(report, /defines \*\*interior\*\* refined spatial/);
  assert.ok(report.includes("An optimal \\((K_1,K_2)\\)-cover"));
  assert.ok(report.includes(String.raw`\frac1T\int\frac1n\sum_{i=1}^n`));
  assert.match(report, /averaged \*\*modified flux\*\*/);
  assert.match(report, /full two-sided comparison requires local energy equality/);
  assert.ok(report.includes("https://arxiv.org/html/1101.2193v2"));
  assert.ok(report.includes("https://arxiv.org/pdf/1107.0058v4"));
  assert.match(report, /initial vorticity is a finite Radon measure/);
  assert.ok(report.includes(String.raw`\theta\in W^{1,1}_c(\mathbb R^3)`));
  assert.ok(report.includes(String.raw`\le N^{-1}\|\partial_1\theta\|_1`));
  assert.ok(report.includes(String.raw`\frac{C_1}{m_0}=O(R^{-1})`));
  assert.ok(report.includes(String.raw`q\ge1-\rho_2`));
  assert.match(report, /\*\*not all included\*\*/);
  assert.ok(report.includes(String.raw`\rho_2\ge2/3`));
  assert.match(report, /extra .* average changes nothing/);
  assert.match(report, /only a \*\*relaxation of the interior, fixed-scale observation/);
  assert.match(report, /do not encode the full optimal-cover\s+argument/);
  assert.match(report, /does not challenge their result/);
  assert.match(report, /does not, by itself, control unresolved subscale cancellation/);
});

test("keeps the scalar and Navier--Stokes claim boundaries explicit", async () => {
  const report = await readFile(new URL("r070d_report-source.md", research), "utf8");

  assert.match(report, /abstract scalar density/);
  assert.match(report, /not shown to equal Yu's filtered annular vortex-stretching density/);
  assert.match(report, /Lebesgue differentiation detects a negative set/);
  assert.match(report, /PDE admissibility/);
  assert.match(report, /not\s+Millennium-level\*\*/);
  assert.match(report, /not yet a theorem about the exact filtered annular functional/);
  assert.match(report, /Compact curl\s+blocks have zero total vorticity/);
  assert.ok(report.includes("one strictly separated pair \\(j\\le k-m_*\\)"));
  assert.ok(report.includes(String.raw`K(\lambda-1)(\lambda+1)^2`));
  assert.ok(report.includes(String.raw`\left.\partial_\lambda`));
  assert.match(report, /retain \*\*all four\*\* shell cross-pairs/);
  assert.ok(report.includes(String.raw`\int_{I_k}F_{j,k}^{\mathrm{Yu}}`));
  assert.ok(report.includes(String.raw`e^{\nu(t-t_-)\Delta}`));
  assert.ok(
    report.includes(
      String.raw`The construction for every prescribed Yu \(\chi_k\) and every \(j\le k\)`,
    ),
  );
  assert.match(report, /remains \*\*\[U\]\*\*/);
});

test("keeps the report structurally auditable", async () => {
  const report = await readFile(new URL("r070d_report-source.md", research), "utf8");
  const tags = [...report.matchAll(/\\tag\{([^}]+)\}/g)].map((match) => match[1]);

  assert.equal(tags.length, new Set(tags).size);
  assert.equal((report.match(/\\\[/g) ?? []).length, (report.match(/\\\]/g) ?? []).length);
  assert.doesNotMatch(report, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(report, /[ \t]+$/m);
  assert.match(report, /No source found there asserts/);
  assert.match(report, /bounded\s+search result, not a claim/);
});

test("reproduces the exact symbolic cover-blindness certificate", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070d_cover_audit.py", research));
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.status, "exact-symbolic-audit");
  assert.equal(archived.witness.signedMass, "8*pi**3*delta");
  assert.equal(archived.witness.negativePartMassLimitAtZero, "8*pi**2");
  assert.equal(archived.witness.ratioLeadingAsymptotic, "1/(pi*delta)");
  assert.equal(
    archived.cutoffGate.everyNormalizedLocalAverage,
    "delta/2 <= <f>_psi <= 3*delta/2",
  );
  assert.match(archived.claimBoundary, /abstract scalar measure-theoretic obstruction/);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks every R0.70D symbolic payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070d_cover_audit\.py/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid checksum line: ${line}`);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives a journal-style explanatory figure with the correct evidence boundary", async () => {
  const manifest = JSON.parse(await readFile(new URL("manifest.json", figureRoot), "utf8"));
  const validation = JSON.parse(
    await readFile(new URL("validation.json", figureRoot), "utf8"),
  );
  const caption = await readFile(new URL("caption.md", figureRoot), "utf8");
  const contract = await readFile(new URL("figure-contract.md", figureRoot), "utf8");
  const svg = await readFile(new URL("figure.svg", figureRoot), "utf8");

  assert.equal(manifest.status, "explanatory");
  assert.match(manifest.claimBoundary, /not simulation evidence or an NSE-flux realization/i);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.match(validation.claimBoundary, /not DNS, not an NSE flux sample/i);
  assert.match(caption, /not measured\s+DNS data/);
  assert.match(contract, /not a numerical proof, DNS result/);
  assert.match(svg, /Positive coarse view, negative fine mass/);
  assert.match(svg, /not DNS and not an NSE-flux realization/);
  assert.ok((await stat(new URL("figure.png", figureRoot))).size > 100_000);
  assert.ok((await stat(new URL("figure.pdf", figureRoot))).size > 15_000);
  assert.ok((await stat(new URL("figure.svg", figureRoot))).size > 20_000);
});

test("keeps compute and publication decisions proportional to the analytic gate", async () => {
  const report = await readFile(new URL("r070d_report-source.md", research), "utf8");
  const environment = await readFile(new URL("environment.txt", certificateRoot), "utf8");

  assert.match(report, /\*\*DGX:\*\* not justified/);
  assert.match(report, /\*\*Independent review:\*\* three read-only audits passed/);
  assert.match(report, /do not publish R0\.70D as a theorem chapter/i);
  assert.match(report, /merge it into\s+the public site without separate approval/);
  assert.match(report, /not DNS and not an\s+NSE flux sample/);
  assert.match(environment, /dgx_used=false/);
});
