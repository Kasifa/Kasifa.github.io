import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const pkg = resolve(root, "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model");
const run = promisify(execFile);
const json = async (name) => JSON.parse(await readFile(resolve(pkg, name), "utf8"));

test("R0.72T journal figure is analytic, complete, and byte-identical to public assets", async () => {
  const [manifest, validation, contract, caption] = await Promise.all([
    json("manifest.json"), json("validation.json"), json("contract.json"), readFile(resolve(pkg, "caption.md"), "utf8"),
  ]);
  assert.ok(["draft", "formal"].includes(manifest.status));
  assert.equal(manifest.figureId, "fig-r072t-a2-spacetime-model");
  assert.equal(contract.simulationPerformed, false);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(manifest.figure.outputs.find((item) => item.path === "figure.png").dpi, 600);
  assert.match(caption, /1\/720/);
  assert.match(caption, /do not prove block/);
  for (const extension of ["pdf", "svg", "png"]) {
    const master = await readFile(resolve(pkg, `figure.${extension}`));
    const publicCopy = await readFile(resolve(root, `public/assets/r072t/fig-r072t-a2-spacetime-model.${extension}`));
    assert.equal(createHash("sha256").update(publicCopy).digest("hex"), createHash("sha256").update(master).digest("hex"));
  }
  await run(process.env.CODEX_PYTHON || "python3", [resolve(pkg, "validate.py")], { cwd: root });
});
