import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import test from "node:test";

const root = new URL("..", import.meta.url).pathname;
const notePath = join(root, "public/notes/r0-68a.html");
const homePath = join(root, "public/research-review.html");
const translationsPath = join(root, "public/i18n-en.js");
const figureRoot = join(
  root,
  "figures/r068a-all-order-tail/fig-r068a-all-order-tail",
);

test("publishes the rigorous R0.68A all-order tail reduction", async () => {
  const [note, home, translations] = await Promise.all([
    readFile(notePath, "utf8"),
    readFile(homePath, "utf8"),
    readFile(translationsPath, "utf8"),
  ]);
  assert.ok(home.includes("R0.68B-1 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));
  assert.ok(home.includes("综述 v0.63 · 2026-08-21"));
  assert.match(home, /href="\/notes\/r0-68a\.html"/);
  assert.match(home, /id="r068a"/);
  assert.match(note, /note-retro\.css\?v=0\.56/);
  assert.match(note, /i18n-en\.js\?v=0\.55/);
  assert.ok(note.includes("\\kappa=\\frac{1+\\sqrt2}{4}"));
  assert.ok(note.includes("H-4D=4&gt;0"));
  assert.ok(note.includes("\\frac1{30000}\\left(\\frac{43}{64}\\right)^r"));
  assert.match(note, /全部十阶及以上目标项之和/);
  assert.match(note, /唯一未决有限关口/);
  assert.match(note, /数据仍属于全局光滑的平行剪切不变类/);
  assert.match(note, /没有证明八阶热项的渐近/);
  assert.match(note, /r0-68a-all-order-tail\.svg/);
  assert.match(note, /95fcc835b63b1ef3abdea9038d49ad08b951e9fd/);
  assert.match(note, /f13b8fcd56ccc932f2ea6e411af0766d44ca4a18/);
  assert.match(note, /4a80fd1d76f0cd3f30235c278542ca69b2957709/);
  assert.match(note, /f6d94a8be1d1c1394311b745bdac82db64cc43ab198e36ca209997975f21f50a/);
  assert.doesNotMatch(note, /SOURCE_COMMIT|CERTIFICATE_COMMIT|FIGURE_COMMIT/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.match(translations, /all-order target tail reduces to one eighth-order gate/i);
  assert.match(translations, /every order at least ten is jointly closed/i);
});

test("publishes byte-exact mirrors of the formal R0.68A figure", async () => {
  for (const [publicName, archiveName] of [
    ["r0-68a-all-order-tail.svg", "figure.svg"],
    ["r0-68a-all-order-tail.png", "figure.png"],
    ["r0-68a-all-order-tail.pdf", "figure.pdf"],
  ]) {
    const [publicBuffer, archiveBuffer] = await Promise.all([
      readFile(join(root, "public/figures", publicName)),
      readFile(join(figureRoot, archiveName)),
    ]);
    assert.deepEqual(publicBuffer, archiveBuffer);
  }
});

test("keeps every R0.68A note navigation target resolvable", async () => {
  const note = await readFile(notePath, "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.68A target: #" + match[1]);
  }
});
