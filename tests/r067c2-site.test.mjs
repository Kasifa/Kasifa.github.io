import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import test from "node:test";

const root = new URL("..", import.meta.url).pathname;
const notePath = join(root, "public/notes/r0-67c2.html");
const homePath = join(root, "public/research-review.html");
const translationsPath = join(root, "public/i18n-en.js");
const noteCssPath = join(root, "public/note-retro.css");
const figureRoot = join(
  root,
  "figures/r067c2-dominant-heat/fig-r067c2-dominant-heat",
);

test("publishes the strict dominant R0.67C-2 sign and its fixed-order boundary", async () => {
  const [note, home, translations, noteCss] = await Promise.all([
    readFile(notePath, "utf8"),
    readFile(homePath, "utf8"),
    readFile(translationsPath, "utf8"),
    readFile(noteCssPath, "utf8"),
  ]);
  assert.ok(home.includes("R0.67C-2 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));
  assert.ok(home.includes("综述 v0.67 · 2026-08-21"));
  assert.match(home, /href="\/notes\/r0-67c2\.html"/);
  assert.match(home, /id="r067c2"/);
  assert.match(home, /mjx-container\[display="true"\].+font-size:\s*\.66em/);
  assert.match(note, /note-retro\.css\?v=0\.54/);
  assert.match(noteCss, /\.lead\{font-size:1rem\}/);
  assert.match(note, /67,200 维中心矩提升/);
  assert.ok(note.includes("320\\times210=67{,}200"));
  assert.ok(note.includes("=\\frac1{4096}"));
  assert.ok(note.includes("5.16125216688\\times10^{-5}"));
  assert.ok(note.includes("-1.715485437712\\times10^{-6}"));
  assert.ok(note.includes("-2.025145622883\\times10^{-7}"));
  assert.match(note, /没有控制完整偶数阶级数/);
  assert.match(note, /构造仍在全局光滑的平行剪切不变类中/);
  assert.match(note, /r0-67c2-dominant-heat\.svg/);
  assert.match(note, /ed153f5919f040c7fc16b169685b05fc574f3d17/);
  assert.match(note, /cd4124a4c781ba6593635d23aab425515a2ee155/);
  assert.match(note, /e7828299d5df0ab2fc01fa32605e5c5cf8af95c0/);
  assert.doesNotMatch(note, /CERTIFICATE_COMMIT|FIGURE_COMMIT/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.match(translations, /asymptotic dominant projection[^\n]+strictly negative/i);
  assert.match(translations, /all-even-order|all even orders|full even-order/i);
  assert.match(translations, /"结论边界：": "Claim boundary:"/);
});

test("publishes byte-exact mirrors of the formal R0.67C-2 figure", async () => {
  for (const [publicName, archiveName] of [
    ["r0-67c2-dominant-heat.svg", "figure.svg"],
    ["r0-67c2-dominant-heat.png", "figure.png"],
    ["r0-67c2-dominant-heat.pdf", "figure.pdf"],
  ]) {
    const [publicBuffer, archiveBuffer] = await Promise.all([
      readFile(join(root, "public/figures", publicName)),
      readFile(join(figureRoot, archiveName)),
    ]);
    assert.deepEqual(publicBuffer, archiveBuffer);
  }
});

test("keeps every R0.67C-2 note navigation target resolvable", async () => {
  const note = await readFile(notePath, "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.67C-2 target: #" + match[1]);
  }
});
