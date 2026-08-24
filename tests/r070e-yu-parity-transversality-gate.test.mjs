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
const certificateRoot = new URL("certificates/r070e/", research);
const figureRoot = new URL(
  "figures/r070e-yu-parity-transversality/fig-r070e-yu-parity-transversality/",
  root,
);

test("repairs the Yu object attribution before stating the theorem", async () => {
  const report = await readFile(new URL("r070e_report-source.md", research), "utf8");

  assert.match(report, /internal canonical research report; not a public theorem chapter/);
  assert.match(report, /does \*\*not\*\* define a scalar/);
  assert.ok(report.includes(String.raw`F_{j,k}^{\mathrm{Yu}}`));
  assert.ok(report.includes(String.raw`\mathcal V_\chi^{\mathrm{rem}}`));
  assert.ok(report.includes(String.raw`\mathcal W_{k,m}^{\mathrm{mov}}`));
  assert.match(report, /legitimate project notation built from \(2\.8\)/);
  assert.match(report, /not renamed\s+as a Yu-defined signed scalar/);
  assert.match(report, /does not display an identity bridging\s+the intermediate region/);
  assert.match(report, /never identifies \(2\.4\) with a sum of \(1\.2\)/);
});

test("locks the exact Yu remainder sign defect and its positive-part identity", async () => {
  const report = await readFile(new URL("r070e_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`\mathcal V_\chi^{\mathrm{rem}}=0`));
  assert.ok(report.includes(String.raw`\mathcal A_\chi^{\mathrm{rem}}>0`));
  assert.ok(report.includes(String.raw`\mathcal V_\chi^{+,\mathrm{rem}}`));
  assert.ok(report.includes(String.raw`=\tfrac12\mathcal A_\chi^{\mathrm{rem}}>0`));
  assert.ok(report.includes(String.raw`\frac{\mathcal A_\chi^{\mathrm{rem}}`));
  assert.match(report, /same-kernel,\s+same-filter, same-cutoff absolute companion/);
  assert.match(report, /global smooth\s+small-data class/);
});

test("locks the explicit Fourier pair, hard shell, and all cubic coefficients", async () => {
  const report = await readFile(new URL("r070e_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`E(x,y,z)=(\cos y,\cos z,\cos x)`));
  assert.ok(report.includes(String.raw`O(x,y,z)=(\sin y,\sin z,\sin x)`));
  assert.ok(report.includes(String.raw`\mathcal RE=-E`));
  assert.ok(report.includes(String.raw`\mathcal RO=O`));
  assert.ok(report.includes(String.raw`K_{132}(z)=\frac{3}{8\pi|z|^5}(z_1^2-z_3^2)`));
  assert.ok(report.includes(String.raw`\frac{q^2(b^2-a^2)}{10}+O(q^4b^4)`));
  assert.ok(report.includes(String.raw`3\int_{qa}^{qb}\frac{j_2(s)}s`));
  assert.ok(report.includes(String.raw`\frac{A_1+A_3}{8}`));
  assert.ok(report.includes(String.raw`\frac{A_1-3A_3}{8}\lambda`));
  assert.ok(report.includes(String.raw`\frac{-A_1+3A_3}{8}\lambda^2`));
  assert.ok(report.includes(String.raw`\frac{-A_1-A_3}{8}\lambda^3`));
  assert.ok(report.includes(String.raw`H_0'(1)=-\frac{A_1}{2}\ne0`));
  assert.match(report, /No cross-pair is\s+silently deleted/);
});

test("keeps compact return fields, heat tails, and cutoff asymmetry explicit", async () => {
  const report = await readFile(new URL("r070e_report-source.md", research), "utf8");

  assert.ok(report.includes(String.raw`E_L=\nabla\times(\zeta_L A_{E,q})`));
  assert.ok(report.includes(String.raw`O_L=\nabla\times(\zeta_L A_{O,q})`));
  assert.match(report, /necessary return field is present, explicitly/);
  assert.match(report, /return field is \*\*not\*\* declared\s+geometrically invisible/);
  assert.match(report, /must not be dropped term by term/);
  assert.ok(report.includes(String.raw`\exp\!\left[-c_\nu(L-2\Gamma-2)^2`));
  assert.match(report, /sum of\s+two identical nonnegative smooth bumps/);
  assert.match(report, /inversion even/);
  assert.doesNotMatch(report, /radial inversion-even cutoff/);
  assert.match(report, /The full nonlinear solution does not preserve the linear parity/);
  assert.ok(report.includes(String.raw`\lambda(\varepsilon)=1+O(\varepsilon)`));
});

test("states the significance and stopping boundaries without a Millennium overclaim", async () => {
  const report = await readFile(new URL("r070e_report-source.md", research), "utf8");

  assert.match(report, /route-elimination plus an exact transfer/);
  assert.match(report, /does not prove regularity/);
  assert.match(report, /does not control Yu's commutator defect or localization budgets/);
  assert.match(report, /not a proof of\s+regularity or blow-up/);
  assert.match(report, /R0\.70F/);
  assert.match(report, /low-order external affine strain jet/);
  assert.match(report, /\*\*DGX:\*\* not justified/);
  assert.match(report, /Do\s+not push, merge, or present Theorems 9\.1--9\.2/);
});

test("records three independent audits and both substantive corrections", async () => {
  const audit = await readFile(new URL("r070e_independent_audit.md", research), "utf8");

  assert.match(audit, /Primary-source audit — PASS/);
  assert.match(audit, /Algebra and kernel audit — PASS/);
  assert.match(audit, /PDE localization and IFT audit — PASS/);
  assert.match(audit, /relative shell\s+multiplier is/);
  assert.ok(audit.includes(String.raw`\frac{q^2(b^2-a^2)}{10}`));
  assert.match(audit, /exact remainder does \*\*not\*\* discard the global return field/);
  assert.match(audit, /No audit identifies the project scalar with Yu's positive annular quantity/);
});

test("reproduces the exact symbolic parity-transversality certificate", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(
    new URL("r070e_yu_parity_transversality_audit.py", research),
  );
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.status, "exact-symbolic-audit");
  assert.equal(archived.release, "R0.70E");
  assert.equal(archived.reflectionCubic.derivativeAtRoot, "-A1/2");
  assert.match(archived.hardShellMoment.relativeStrainMultiplier, /^\+q\^2/);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks every R0.70E symbolic payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070e_yu_parity_transversality_audit\.py/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, `invalid checksum line: ${line}`);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});

test("archives a journal-style analytic figure with source data and boundaries", async () => {
  const manifest = JSON.parse(await readFile(new URL("manifest.json", figureRoot), "utf8"));
  const validation = JSON.parse(
    await readFile(new URL("validation.json", figureRoot), "utf8"),
  );
  const caption = await readFile(new URL("caption.md", figureRoot), "utf8");
  const contract = await readFile(new URL("figure-contract.md", figureRoot), "utf8");
  const svg = await readFile(new URL("figure.svg", figureRoot), "utf8");

  assert.equal(manifest.status, "explanatory");
  assert.equal(manifest.release, "R0.70E");
  assert.match(manifest.claimBoundary, /not simulation evidence or a numerical PDE proof/i);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.match(caption, /not DNS,\s+trajectory data/);
  assert.match(contract, /numerical proof of compact localization/);
  assert.match(svg, /Two-lobe transversality/);
  assert.match(svg, /Hard shell remains active/);
  assert.ok((await stat(new URL("figure.png", figureRoot))).size > 300_000);
  assert.ok((await stat(new URL("figure.pdf", figureRoot))).size > 20_000);
  assert.ok((await stat(new URL("figure.svg", figureRoot))).size > 30_000);
});
