import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import test from "node:test";

const root = new URL("..", import.meta.url).pathname;
const notePath = join(root, "public/notes/r0-68b1.html");
const homePath = join(root, "public/research-review.html");
const translationsPath = join(root, "public/i18n-en.js");
const figureRoot = join(
  root,
  "figures/r068b1-eighth-order-spectrum/fig-r068b1-eighth-order-spectrum",
);

test("publishes the exact R0.68B-1 spectrum with its heat boundary", async () => {
  const [note, home, translations] = await Promise.all([
    readFile(notePath, "utf8"),
    readFile(homePath, "utf8"),
    readFile(translationsPath, "utf8"),
  ]);
  assert.ok(home.includes("R0.68B-1 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));
  assert.ok(home.includes("综述 v0.84 · 2026-08-25"));
  assert.match(home, /href="\/notes\/r0-68b1\.html"/);
  assert.match(home, /id="r068b1"/);
  assert.match(note, /note-retro\.css\?v=0\.56/);
  assert.match(note, /i18n-en\.js\?v=0\.56/);
  assert.ok(note.includes("A+B+C+D-E-F-G=Q"));
  assert.ok(note.includes("2\\times128\\times7=1792"));
  assert.ok(note.includes("\\operatorname{rank}W_8=204"));
  assert.ok(note.includes("x^{56}(x-4096)^{14}"));
  assert.ok(note.includes("q_{4,256}(x)^{14}q_{10,16}(x)^6q_{18}(x)"));
  assert.ok(note.includes("Y_{8,r}=C_{8,0}\\nu^r+O(4800^r)"));
  assert.ok(note.includes("-0.02612679363405570&lt;C_{8,0}&lt;-0.02612679362708268"));
  assert.ok(note.includes("\\frac{256}{\\lambda^2}"));
  assert.match(note, /这个收缩率只属于零时间代数分支/);
  assert.match(note, /完整八阶热渐近/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-68b1-eighth-order-spectrum\.svg/);
  assert.match(note, /3ddf6d30965837311c0b659d5fb21e41c3b80f14/);
  assert.match(note, /0e5387192f6ed2b796da4212ef3bf3220eed6e4c/);
  assert.match(note, /9b18c20/);
  assert.match(note, /00d60f5abd080f90c551126f388e005df4ead5bd556308f8a63c5972766d483b/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.match(translations, /exact spectrum and reachable dominant projection/i);
  assert.match(translations, /complete seven-simplex heat projection remains open/i);
});

test("publishes byte-exact mirrors of the formal R0.68B-1 figure", async () => {
  for (const [publicName, archiveName] of [
    ["r0-68b1-eighth-order-spectrum.svg", "figure.svg"],
    ["r0-68b1-eighth-order-spectrum.png", "figure.png"],
    ["r0-68b1-eighth-order-spectrum.pdf", "figure.pdf"],
  ]) {
    const [publicBuffer, archiveBuffer] = await Promise.all([
      readFile(join(root, "public/figures", publicName)),
      readFile(join(figureRoot, archiveName)),
    ]);
    assert.deepEqual(publicBuffer, archiveBuffer);
  }
});

test("keeps every R0.68B-1 note navigation target resolvable", async () => {
  const note = await readFile(notePath, "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.68B-1 target: #" + match[1]);
  }
});
