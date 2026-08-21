import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import test from "node:test";

const root = new URL("..", import.meta.url).pathname;
const notePath = join(root, "public/notes/r0-67c1.html");
const homePath = join(root, "public/research-review.html");
const translationsPath = join(root, "public/i18n-en.js");
const figureRoot = join(
  root,
  "figures/r067c1-one-cycle-heat/fig-r067c1-one-cycle-heat",
);

test("publishes the exact finite R0.67C-1 sign with its asymptotic boundary", async () => {
  const [note, home, translations] = await Promise.all([
    readFile(notePath, "utf8"),
    readFile(homePath, "utf8"),
    readFile(translationsPath, "utf8"),
  ]);
  assert.ok(home.includes("R0.67C-1 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));
  assert.ok(home.includes("综述 v0.80 · 2026-08-21"));
  assert.match(home, /href="\/notes\/r0-67c1\.html"/);
  assert.match(note, /34,690 个有效载频元组/);
  assert.match(note, /346,900 条有序带符号路径/);
  assert.ok(note.includes("\\max\\alpha_j=67014/4096=16.36083984375"));
  assert.ok(note.includes("\\boxed{J_0=5000=10\\times500.}"));
  assert.ok(note.includes("R_{32}^{\\rm abs}"));
  assert.ok(note.includes("0.0516697551544485637774"));
  assert.ok(note.includes("0.0516697551583354513640"));
  assert.match(note, /渐近主热投影非零/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-67c1-one-cycle-heat\.svg/);
  assert.match(note, /b898179036990a352a6b73e04f2a733905f9dc32/);
  assert.match(note, /bc7c318781afccc72ba6ff3fe034c9e72ee0f18c/);
  assert.match(note, /9c49fc06efd2375f6763671200da3ab03c3e6c3f/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.match(translations, /Rigorous first-cycle sign of the complete sixth-order heat kernel/);
  assert.match(translations, /asymptotic dominant projection remains unproved/);
});

test("publishes byte-exact mirrors of the formal R0.67C-1 figure", async () => {
  for (const [publicName, archiveName] of [
    ["r0-67c1-one-cycle-heat.svg", "figure.svg"],
    ["r0-67c1-one-cycle-heat.png", "figure.png"],
    ["r0-67c1-one-cycle-heat.pdf", "figure.pdf"],
  ]) {
    const [publicBuffer, archiveBuffer] = await Promise.all([
      readFile(join(root, "public/figures", publicName)),
      readFile(join(figureRoot, archiveName)),
    ]);
    assert.deepEqual(publicBuffer, archiveBuffer);
  }
});

test("keeps every R0.67C-1 note navigation target resolvable", async () => {
  const note = await readFile(notePath, "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.67C-1 target: #" + match[1]);
  }
});
