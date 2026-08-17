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
