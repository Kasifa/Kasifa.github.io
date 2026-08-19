import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const templateUrl = new URL("../figures/manifest.template.json", import.meta.url);
const styleUrl = new URL("../figures/journal.mplstyle", import.meta.url);
const guideUrl = new URL("../figures/README.md", import.meta.url);
const requirementsUrl = new URL("../requirements-research.txt", import.meta.url);
const validatorUrl = new URL(
  "../research/validate_figure_package.py",
  import.meta.url,
);
const monitorUrl = new URL(
  "../research/run_with_monitor.py",
  import.meta.url,
);
const r038ManifestUrl = new URL(
  "../figures/r038-tail-newton/fig-r038-tail-restart/manifest.json",
  import.meta.url,
);
const r039ManifestUrl = new URL(
  "../figures/r039-charge-resolved/fig-r039-charge-resolved-restart/manifest.json",
  import.meta.url,
);
const r040ManifestUrl = new URL(
  "../figures/r040-slope-resolved/fig-r040-two-endpoint-transport/manifest.json",
  import.meta.url,
);
const r041ManifestUrl = new URL(
  "../figures/r041-degree-resolved/fig-r041-degree-resolved-tail/manifest.json",
  import.meta.url,
);
const r042ManifestUrl = new URL(
  "../figures/r042-canonical-stretch/fig-r042-canonical-stretch/manifest.json",
  import.meta.url,
);
const r043ManifestUrl = new URL(
  "../figures/r043-charge-degree-floor/fig-r043-charge-degree-floor/manifest.json",
  import.meta.url,
);
const r044ManifestUrl = new URL(
  "../figures/r044-common-slope-tail/fig-r044-common-slope-tail/manifest.json",
  import.meta.url,
);
const r045ManifestUrl = new URL(
  "../figures/r045-fixed-negative-charge/fig-r045-fixed-negative-charge/manifest.json",
  import.meta.url,
);
const r046ManifestUrl = new URL(
  "../figures/r046-two-block-weight/fig-r046-two-block-weight/manifest.json",
  import.meta.url,
);
const r047ManifestUrl = new URL(
  "../figures/r047-charge-degree-lattice/fig-r047-charge-degree-lattice/manifest.json",
  import.meta.url,
);
const r048ManifestUrl = new URL(
  "../figures/r048-threshold-root/fig-r048-threshold-root/manifest.json",
  import.meta.url,
);
const r049ManifestUrl = new URL(
  "../figures/r049-charge-character/fig-r049-charge-character/manifest.json",
  import.meta.url,
);
const r050ManifestUrl = new URL(
  "../figures/r050-charge-character-optimization/fig-r050-charge-character-optimization/manifest.json",
  import.meta.url,
);

test("keeps a complete journal-figure provenance template", async () => {
  const manifest = JSON.parse(await readFile(templateUrl, "utf8"));

  assert.equal(manifest.schemaVersion, "1.0");
  assert.equal(manifest.figure.widthMillimetres, 85);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(
    manifest.figure.outputs.find(({ path }) => path.endsWith(".png")).dpi,
    600,
  );
  assert.equal(manifest.qa.status, "pending");
  assert.ok(Object.values(manifest.qa).includes(false));
  assert.ok(manifest.simulation.command);
  assert.equal(manifest.simulation.kind, "simulation");
  assert.equal(manifest.simulation.monitoring.enabled, true);
  assert.equal(manifest.simulation.monitoring.reportIntervalSeconds, 60);
  assert.ok(manifest.simulation.monitoring.trackedFields.includes("cfl"));
  assert.ok(manifest.data.some(({ path }) => path === "progress.ndjson"));
  assert.ok(manifest.data.some(({ path }) => path === "resources.csv"));
  assert.ok(manifest.compute.host);
  assert.ok(manifest.data[0].schema);
  assert.ok(Array.isArray(manifest.sourceData));
});

test("pins physical size and print-quality export defaults", async () => {
  const [style, guide, requirements] = await Promise.all([
    readFile(styleUrl, "utf8"),
    readFile(guideUrl, "utf8"),
    readFile(requirementsUrl, "utf8"),
  ]);

  assert.match(style, /^figure\.dpi:\s*254$/m);
  assert.match(style, /^savefig\.dpi:\s*600$/m);
  assert.match(style, /^savefig\.bbox:\s*standard$/m);
  assert.match(style, /^figure\.constrained_layout\.use:\s*True$/m);
  assert.match(style, /^pdf\.fonttype:\s*42$/m);
  assert.match(style, /^svg\.fonttype:\s*none$/m);
  assert.match(guide, /Single column: 85 mm wide/);
  assert.match(guide, /Double column: 178 mm wide/);
  assert.match(guide, /final-size, grayscale, label, legend, and scale checks/);
  assert.match(requirements, /^matplotlib==3\.11\.1$/m);
  assert.match(requirements, /^gmpy2==2\.3\.1$/m);
});

test("ships a strict validator for formal figure packages", async () => {
  const source = await readFile(validatorUrl, "utf8");

  assert.match(source, /formal figures require PDF, SVG, and PNG outputs/);
  assert.match(source, /sha256 mismatch/);
  assert.match(source, /full 40-character commit hash/);
  assert.match(source, /manifest\.qa\.status must be passed/);
  assert.match(source, /grayscaleInspected/);
  assert.match(source, /formal simulations require monitoring\.enabled=true/);
});

test("ships a process-tree resource monitor", async () => {
  const source = await readFile(monitorUrl, "utf8");

  assert.match(source, /resources\.csv/);
  assert.match(source, /process_tree_snapshot/);
  assert.match(source, /nvidia-smi/);
  assert.match(source, /gpuMemoryUsedMiB/);
  assert.match(source, /record_row/);
});

test("archives the formal R0.38 tail-aware restart figure", async () => {
  const manifest = JSON.parse(await readFile(r038ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r038-tail-restart");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "bc230622aeac611966c091c4beca734c783f65ac",
  );
  assert.match(manifest.supportedClaim, /Z_N=3\(M_N\+S_N\/\(N\+1\)\)/);
  assert.match(manifest.supportedClaim, /low-block inverse is inert/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 253);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 104);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.39 charge-resolved restart figure", async () => {
  const manifest = JSON.parse(await readFile(r039ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r039-charge-resolved-restart");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "ed08ad45b3440a679d8132d7b3464dc21dd07fa5",
  );
  assert.match(manifest.supportedClaim, /242 fixed input-charge bounds/);
  assert.match(manifest.supportedClaim, /analytic sector covering every s>=241/);
  assert.match(manifest.supportedClaim, /0\.99941043095132664361<1/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 228);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 110);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.40 exact two-endpoint transport figure", async () => {
  const manifest = JSON.parse(await readFile(r040ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r040-two-endpoint-transport");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "413f1cbcb12a961129eacf2482eb9b705c9a2feb",
  );
  assert.match(manifest.supportedClaim, /convexity reduces every admissible input slope/);
  assert.match(manifest.supportedClaim, /monotone and reduces every input degree to j=1/);
  assert.match(manifest.supportedClaim, /0\.86219921104223892656/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 221);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 110);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.41 degree-resolved active-tail figure", async () => {
  const manifest = JSON.parse(await readFile(r041ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r041-degree-resolved-tail");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "c851762902bb97dd3f3f2510b7321771e0a1ff03",
  );
  assert.match(manifest.supportedClaim, /complete center column is a convex function of x=s\/j/);
  assert.match(manifest.supportedClaim, /0\.77854233161724448351/);
  assert.match(manifest.supportedClaim, /1\.0003750451629852617/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 274);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 140);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.42 canonical-stretch transport figure", async () => {
  const manifest = JSON.parse(await readFile(r042ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r042-canonical-stretch");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "5ff24eae1cb9f73a1aac6965b07f0c1f12c62477",
  );
  assert.match(manifest.supportedClaim, /no input-degree prefactor/);
  assert.match(manifest.supportedClaim, /r=329\/1000/);
  assert.match(manifest.supportedClaim, /1\.002872150853994/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 244);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 140);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.43 charge-implied degree-floor figure", async () => {
  const manifest = JSON.parse(await readFile(r043ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r043-charge-degree-floor");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "4fe8cb308e20921fb0490aa2e76209b1d2d84221",
  );
  assert.match(manifest.supportedClaim, /ceil\(S\/2\)/);
  assert.match(manifest.supportedClaim, /0\.99888144242700740673/);
  assert.match(manifest.supportedClaim, /1\.0038955265828946573/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 255);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 140);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.44 common-slope endpoint figure", async () => {
  const manifest = JSON.parse(await readFile(r044ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r044-common-slope-tail");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "aade631ea1a492d078f052776b443875d6a3dd73",
  );
  assert.match(manifest.supportedClaim, /H_r\(x\)=sum/);
  assert.match(manifest.supportedClaim, /0\.96621300575693572712/);
  assert.match(manifest.supportedClaim, /1\.0008564924160487608/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 300);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 140);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.45 fixed-negative-charge endpoint figure", async () => {
  const manifest = JSON.parse(await readFile(r045ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r045-fixed-negative-charge");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "8f7f9ec2b90b2d249b474ec4dbba50a71c807745",
  );
  assert.match(manifest.supportedClaim, /F'_r\(t\)>=3r-Qhat_r/);
  assert.match(manifest.supportedClaim, /0\.99722804122918895132/);
  assert.match(manifest.supportedClaim, /1\.0010616516434951437/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 240);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 140);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.46 correlated two-block figure", async () => {
  const manifest = JSON.parse(await readFile(r046ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r046-two-block-weight");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "a521a84f01b748e3c138ecb785c1b21907dc0e28",
  );
  assert.match(manifest.supportedClaim, /kappa=3\/4/);
  assert.match(manifest.supportedClaim, /0\.99770647568583198433/);
  assert.match(manifest.supportedClaim, /1\.0030411177094620525/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 264);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 140);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.47 charge-degree lattice figure", async () => {
  const manifest = JSON.parse(await readFile(r047ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r047-charge-degree-lattice");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "709ecb5f20b7321079ba114a57bf20b77ca7646a",
  );
  assert.match(manifest.supportedClaim, /239 fixed-charge all-degree theorems/);
  assert.match(manifest.supportedClaim, /0\.9999973490826196656/);
  assert.match(manifest.supportedClaim, /1\.0000026584572409359/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 458);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 142);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.48 exact threshold-root figure", async () => {
  const manifest = JSON.parse(await readFile(r048ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r048-threshold-root");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "fe65dcb365eca9d934c3ec6055c06d7a7c1a515c",
  );
  assert.match(manifest.supportedClaim, /globally unique positive root/);
  assert.match(manifest.supportedClaim, /0\.376932499290527340/);
  assert.match(manifest.supportedClaim, /243 competing columns and sectors/);
  assert.equal(manifest.simulation.kind, "exact-audit");
  assert.equal(manifest.simulation.monitoring.samples, 144);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 142);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
});

test("archives the formal R0.49 multiplicative charge-character figure", async () => {
  const manifest = JSON.parse(await readFile(r049ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r049-charge-character");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.sourceCommit,
    "26ce6d7ffd636956fe7c95a2bbeb7e6ea6573728",
  );
  assert.equal(
    manifest.git.certificateCommit,
    "613f556852bffc32bee3913b7fabc78110e8983d",
  );
  assert.match(manifest.supportedClaim, /globally unique positive threshold root/);
  assert.match(manifest.supportedClaim, /0\.382618642388680778/);
  assert.match(manifest.supportedClaim, /all 243 competing columns and sectors/);
  assert.match(manifest.supportedClaim, /1\.0459367903514846826/);
  assert.match(manifest.supportedClaim, /polydiscs are not nested/);
  assert.equal(manifest.computation.kind, "exact-audit");
  assert.equal(manifest.computation.monitoring.samples, 808);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 142);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
  assert.equal(manifest.qa.dataCrossChecked, true);
});

test("archives the formal R0.50 global charge-character optimization figure", async () => {
  const manifest = JSON.parse(await readFile(r050ManifestUrl, "utf8"));

  assert.equal(manifest.figureId, "fig-r050-charge-character-optimization");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.sourceCommit,
    "a9c469a96462e60655b0fea435177ececb8aef20",
  );
  assert.equal(
    manifest.git.certificateCommit,
    "1430978ad7e4ac04f4b6f5daf04c641b05573edd",
  );
  assert.match(manifest.supportedClaim, /unique global active-column threshold maximum/);
  assert.match(manifest.supportedClaim, /0\.8024563827/);
  assert.match(manifest.supportedClaim, /all 243 competing columns/);
  assert.match(manifest.supportedClaim, /1\.0000030613272706956/);
  assert.equal(manifest.computation.kind, "exact-audit plus high-precision presentation sampling");
  assert.equal(manifest.computation.monitoring.formalSamples, 70);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 112);
  assert.deepEqual(
    manifest.figure.outputs.map(({ path }) => path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.qa.pdfFontsEmbedded, true);
  assert.equal(manifest.qa.dataCrossChecked, true);
});
