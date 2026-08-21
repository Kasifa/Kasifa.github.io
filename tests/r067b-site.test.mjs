import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import test from "node:test";

const root = new URL("..", import.meta.url).pathname;
const notePath = join(root, "public/notes/r0-67b.html");
const homePath = join(root, "public/research-review.html");
const translationsPath = join(root, "public/i18n-en.js");
const figureRoot = join(
  root,
  "figures/r067b-affine-moment-lift/fig-r067b-affine-moment-lift",
);

test("publishes the exact R0.67B affine lift with its heat-pairing boundary", async () => {
  const [note, home, translations] = await Promise.all([
    readFile(notePath, "utf8"),
    readFile(homePath, "utf8"),
    readFile(translationsPath, "utf8"),
  ]);
  assert.ok(home.includes("R0.67B 已完成："));
  assert.ok(home.includes("R0.67C-1 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));
  assert.ok(home.includes("综述 v0.77 · 2026-08-21"));
  assert.match(home, /href="\/notes\/r0-67b\.html"/);
  assert.match(note, /1600 维块三角系统/);
  assert.ok(note.includes("26&lt;256&lt;300&lt;\\mu"));
  assert.ok(note.includes("\\mathcal MR=0"));
  assert.ok(note.includes("\\le256\\|\\zeta\\|_{(C^{1,1})^*,w}"));
  assert.ok(note.includes("\\rho_v(F_{\\theta_\\infty})\\ne0"));
  assert.match(note, /完整热投影非零/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-67b-affine-moment-lift\.svg/);
  assert.match(note, /d0347369ae6ba564d4275d0cd720ba1cd4b91615/);
  assert.match(note, /74d09579d5cf859dab79840528abaa43a1f56f1d/);
  assert.match(note, /2e3d6c7/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.match(translations, /Mass-affine lift and rigorous resolvent/);
  assert.match(translations, /complete heat-kernel projection remains undetermined/);
});

test("publishes byte-exact mirrors of the formal R0.67B figure", async () => {
  for (const [publicName, archiveName] of [
    ["r0-67b-affine-moment-lift.svg", "figure.svg"],
    ["r0-67b-affine-moment-lift.png", "figure.png"],
    ["r0-67b-affine-moment-lift.pdf", "figure.pdf"],
  ]) {
    const [publicBuffer, archiveBuffer] = await Promise.all([
      readFile(join(root, "public/figures", publicName)),
      readFile(join(figureRoot, archiveName)),
    ]);
    assert.deepEqual(publicBuffer, archiveBuffer);
  }
});

test("keeps every R0.67B note navigation target resolvable", async () => {
  const note = await readFile(notePath, "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.67B target: #" + match[1]);
  }
});
