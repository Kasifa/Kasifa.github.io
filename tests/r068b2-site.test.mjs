import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { join } from "node:path";
import test from "node:test";

const root = new URL("..", import.meta.url).pathname;
const notePath = join(root, "public/notes/r0-68b2.html");
const homePath = join(root, "public/research-review.html");
const translationsPath = join(root, "public/i18n-en.js");
const figureRoot = join(
  root,
  "figures/r068b2-eighth-order-heat/fig-r068b2-eighth-order-heat",
);

test("publishes R0.68B-2 with exact and pilot evidence kept separate", async () => {
  const [note, home, translations] = await Promise.all([
    readFile(notePath, "utf8"),
    readFile(homePath, "utf8"),
    readFile(translationsPath, "utf8"),
  ]);
  assert.match(home, /id="r068b2"/);
  assert.match(home, /href="\/notes\/r0-68b2\.html"/);
  assert.ok(home.includes("下一步 R0.68B-2c："));
  assert.ok(home.includes("综述 v0.81 · 2026-08-24"));
  assert.match(note, /note-retro\.css\?v=0\.57/);
  assert.match(note, /i18n-en\.js\?v=0\.57/);
  assert.ok(note.includes("273,823,760"));
  assert.ok(note.includes("105499"));
  assert.ok(note.includes("0.0074150893675487776"));
  assert.ok(note.includes("0.0074150893936092571"));
  assert.ok(
    note.includes(
      "B_{8,\\mathrm{pilot}}=-1.4923824320396173\\times10^{-8}",
    ),
  );
  assert.ok(note.includes("5{,}381{,}376"));
  assert.match(note, /CERTIFIED · EXACT/);
  assert.match(note, /NUMERICAL · PILOT/);
  assert.match(note, /有限正号不能外推成渐近主投影符号/);
  assert.match(note, /浮点收敛本身不能替代严格余项界/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-68b2-eighth-order-heat\.svg/);
  assert.match(note, /01cb3082bc9b51ea4430fa25f2b20c774f950e6b/);
  assert.match(note, /ccd31ce7fc83bf0134b9f0bcdb47fa476af9bf61/);
  assert.match(note, /28b71fd450a1f806ffec6423dbf1e51c5a66dba1/);
  assert.match(note, /32f6ba3353ebf9875b8d9a337ded05ae7b0934e1/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.match(translations, /first complete eighth-order heat block/i);
  assert.match(translations, /binary64/i);
});

test("publishes byte-exact mirrors of the mixed-evidence R0.68B-2 figure", async () => {
  for (const [publicName, archiveName] of [
    ["r0-68b2-eighth-order-heat.svg", "figure.svg"],
    ["r0-68b2-eighth-order-heat.png", "figure.png"],
    ["r0-68b2-eighth-order-heat.pdf", "figure.pdf"],
  ]) {
    const [publicBuffer, archiveBuffer] = await Promise.all([
      readFile(join(root, "public/figures", publicName)),
      readFile(join(figureRoot, archiveName)),
    ]);
    assert.deepEqual(publicBuffer, archiveBuffer);
  }
});

test("keeps every R0.68B-2 note navigation target resolvable", async () => {
  const note = await readFile(notePath, "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.68B-2 target: #" + match[1]);
  }
});
