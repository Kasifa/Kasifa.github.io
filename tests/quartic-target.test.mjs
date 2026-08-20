import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const repository = new URL("..", import.meta.url).pathname;
const noteUrl = new URL("../research/quartic_target_note.md", import.meta.url);
const scannerUrl = new URL("../research/quartic_target_scan.cpp", import.meta.url);
const highPrecisionUrl = new URL(
  "../research/quartic_target_high_precision.py",
  import.meta.url,
);

test("states the exact R0.61 quartic formula and its numerical boundary", async () => {
  const [note, scanner, highPrecision] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(scannerUrl, "utf8"),
    readFile(highPrecisionUrl, "utf8"),
  ]);

  assert.match(note, /R0\.61 — The complete quartic target coefficient/);
  assert.ok(note.includes("\\widehat G_4(0,m,t_H)"));
  assert.ok(note.includes("K_T(\\alpha_0,\\alpha_1,\\alpha_2,\\alpha_3)"));
  assert.ok(note.includes("R_{L,M,m}=\\frac{L^2m^2}{H^3}"));
  assert.ok(note.includes("-\\frac{\\varepsilon^2}{L^2}R_{L,M,m}"));
  assert.match(note, /finite numerical evidence/);
  assert.match(note, /weighted four-point Rudin--Shapiro correlation/);
  assert.match(note, /does \*\*not\*\* prove/);
  assert.match(note, /solution of the Clay Millennium problem/);
  assert.match(scanner, /confluent|Repeated rates|integer_rates/);
  assert.match(scanner, /not a proof/);
  assert.match(highPrecision, /not an interval certificate or proof/);
  assert.doesNotMatch(note, /我们|攻关|主攻|突破千禧年/);
});

test("reproduces a small complete quartic target scan", async (t) => {
  const scratch = await mkdtemp(join(tmpdir(), "r061-scan-"));
  const binary = join(scratch, "quartic-target-scan");
  const output = join(scratch, "result.json");
  try {
    await execFileAsync(
      "/usr/bin/clang++",
      [
        "-O2",
        "-std=c++20",
        "-pthread",
        scannerUrl.pathname,
        "-o",
        binary,
      ],
      { cwd: repository },
    );
  } catch (error) {
    if (error.code === "ENOENT") {
      t.skip("clang++ is unavailable on this host");
      return;
    }
    throw error;
  }
  await execFileAsync(
    binary,
    [
      "--level-l",
      "1",
      "--level-m",
      "2",
      "--target",
      "4",
      "--threads",
      "2",
      "--output",
      output,
    ],
    { cwd: repository },
  );
  const result = JSON.parse(await readFile(output, "utf8"));
  assert.equal(result.L, 2);
  assert.equal(result.M, 4);
  assert.equal(result.H, 32);
  assert.equal(result.target, 4);
  assert.equal(result.orderedQuarticPaths, 234);
  assert.ok(result.normalizedSignedRatio > 0);
  assert.ok(
    Math.abs(result.normalizedSignedRatio - 0.0007328372347447609) < 5e-18,
  );
  assert.match(result.classification, /not a proof/);
});
