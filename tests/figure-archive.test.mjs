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
