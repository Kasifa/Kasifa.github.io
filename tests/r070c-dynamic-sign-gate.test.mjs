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
const certificateRoot = new URL("certificates/r070c/", research);
const figureRoot = new URL(
  "figures/r070c-parity-obstruction/fig-r070c-parity-obstruction/",
  root,
);

test("locks the generic dynamical sign-defect obstruction and its scope", async () => {
  const report = await readFile(new URL("r070c_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.ok(report.includes(String.raw`w_\eta[U](-x)=-w_\eta[U](x)`));
  assert.ok(report.includes(String.raw`K\supset\operatorname{supp}\chi\ \cup`));
  assert.match(report, /P_I\[u\^\\varepsilon\]\s*=A_I\\varepsilon\^3\+O_I\(\\varepsilon\^4\)/);
  assert.ok(report.includes(String.raw`W_I[u^\varepsilon]=O_I(\varepsilon^4)`));
  assert.ok(report.includes(String.raw`\frac{|W_I[u^\varepsilon]|}{P_I[u^\varepsilon]}\longrightarrow0`));
  assert.match(report, /genuine global smooth finite-energy Navier--Stokes trajectories/);
  assert.match(report, /fixed generic\s+annular functional/);
  assert.match(report, /matching transfer remains \*\*\[U\]\*\*/);
  assert.match(report, /neither result is\s+promoted to every Yu core geometry/);
  assert.match(report, /Nothing here proves regularity,[\s\S]*Millennium claim/);
});

test("records the repaired normalized fixed-point and exact two-copy gate", async () => {
  const report = await readFile(new URL("r070c_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`a^{\varepsilon,\lambda}=u^{\varepsilon,\lambda}/\varepsilon`));
  assert.ok(report.includes(String.raw`-\varepsilon\int_0^t e^{\nu(t-s)\Delta}`));
  assert.match(report, /differentiated fixed-point equation extend/);
  assert.ok(report.includes(String.raw`as a \(C^1\) function`));
  assert.ok(report.includes(String.raw`H(\varepsilon,\lambda,T)=W_{[0,T]}[a^{\varepsilon,\lambda}]`));
  assert.ok(report.includes(String.raw`[(K_+-K_-)\cup(K_--K_+)]\cap\operatorname{supp}\eta=\varnothing`));
  assert.ok(report.includes(String.raw`F(q_\lambda)=A(1-\lambda^3)`));
  assert.ok(report.includes(String.raw`F(v):=\int_{\mathbb R^3}\chi(x)`));
  assert.ok(report.includes(String.raw`p_0:=\int\chi|w_\eta[\varphi_\ell*q_1]|\,dx`));
  assert.ok(report.includes(String.raw`satisfies, for every \(0<\varepsilon<\varepsilon_0\)`));
  assert.match(report, /does \*\*not\*\* prove exact zero for every\s+prescribed Yu core cutoff/);
});

test("keeps the periodic comparator at total production rather than annular status", async () => {
  const report = await readFile(new URL("r070c_report-source.md", research), "utf8");

  assert.match(report, /Exact periodic total-production comparator/);
  assert.ok(report.includes(String.raw`B(x+h)=-B(x)`));
  assert.ok(report.includes(String.raw`(\nabla\times B)\cdot S[B](\nabla\times B)=3`));
  assert.match(report, /does not by itself identify a nonzero member of the R0\.69T decomposition/);
  assert.match(report, /shellwise torus corollary[\s\S]*remains \*\*\[U\]\*\*/);
  assert.doesNotMatch(report, /exact periodic annular model/i);
});

test("keeps the report structurally auditable", async () => {
  const report = await readFile(new URL("r070c_report-source.md", research), "utf8");
  const tags = [...report.matchAll(/\\tag\{([^}]+)\}/g)].map((match) => match[1]);

  assert.equal(tags.length, new Set(tags).size);
  assert.equal((report.match(/\\\[/g) ?? []).length, (report.match(/\\\]/g) ?? []).length);
  assert.doesNotMatch(report, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(report, /[ \t]+$/m);
  assert.match(report, /No source found in this bounded search/);
  assert.match(report, /This is a search result, not a claim/);
});

test("reproduces the exact symbolic parity certificate", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070c_parity_audit.py", research));
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.status, "exact-symbolic-audit");
  assert.equal(archived.evenR3Seed.stretching, "-3*sin(x)*sin(y)*sin(z)");
  assert.equal(archived.evenR3Seed.torusStretchingL1, "192");
  assert.equal(archived.evenR3Seed.torusStretchingL2Squared, "9*pi**3");
  assert.equal(archived.iftGate.normalizedLeadingSignedPolynomial, "1 - lam**3");
  assert.equal(archived.iftGate.derivativeAtRoot, "-3");
  assert.match(archived.iftGate.signedOrderAfterTuning, /two-plateau cutoff/);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks every R0.70C symbolic payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070c_parity_audit\.py/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid checksum line: ${line}`);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives a journal-style explanatory figure with explicit evidence boundary", async () => {
  const manifest = JSON.parse(await readFile(new URL("manifest.json", figureRoot), "utf8"));
  const validation = JSON.parse(
    await readFile(new URL("validation.json", figureRoot), "utf8"),
  );
  const caption = await readFile(new URL("caption.md", figureRoot), "utf8");
  const svg = await readFile(new URL("figure.svg", figureRoot), "utf8");

  assert.equal(manifest.status, "explanatory");
  assert.match(manifest.claimBoundary, /not simulation evidence/i);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.match(validation.claimBoundary, /not DNS/i);
  assert.match(caption, /not measured DNS data/);
  assert.match(svg, /One-order cancellation gap/);
  assert.match(svg, /not DNS/);
  assert.ok((await stat(new URL("figure.png", figureRoot))).size > 100_000);
  assert.ok((await stat(new URL("figure.pdf", figureRoot))).size > 20_000);
  assert.ok((await stat(new URL("figure.svg", figureRoot))).size > 20_000);
});

test("keeps compute and publication decisions proportional to the analytic gate", async () => {
  const report = await readFile(new URL("r070c_report-source.md", research), "utf8");
  const environment = await readFile(new URL("environment.txt", certificateRoot), "utf8");

  assert.match(report, /\*\*DGX:\*\* not justified/);
  assert.match(report, /\*\*Public site:\*\* the review gate is passed/);
  assert.match(report, /Do not merge it into the public site/);
  assert.match(report, /explanatory evidence, not part of the proof/);
  assert.match(report, /does not\s+reduce a known regularity hypothesis/);
  assert.match(environment, /dgx_used=false/);
});
