import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69O with dissipation-assisted pressure closure and strict boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69o.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069o"/);
  assert.match(home, /href="\/notes\/r0-69o\.html"/);
  assert.match(home, /综述 v0\.75 · 2026-08-21/);
  assert.match(home, /i18n-en\.js\?v=0\.75/);
  assert.match(home, /下一步 R0\.69P/);
  assert.match(note, /\\sigma_v\^2\\le C\\mu_v\\mathcal D_v\^\{1\/2\}/);
  assert.match(note, /C\\varepsilon\^\{-3\}\\mu_v\^4\\sigma_v\^2/);
  assert.match(note, /\\mathsf A_v\^2\\mathsf E_v/);
  assert.match(note, /\\frac\{27\}\{256\}\\varepsilon\^\{-3\}\\mu\^4/);
  assert.match(note, /\\int\\mathcal D_A\\,d\\tau\\ge cA\^2\\longrightarrow\\infty/);
  assert.match(note, /\\mu\^\{14\/3\}/);
  assert.match(note, /\\mu\^\{18\/5\}/);
  assert.match(note, /C_\\varepsilon\\sigma\^6/);
  assert.ok(note.includes("尚未推导完整的局部 \\(H^1\\) 不等式"));
  assert.match(note, /没有解决千禧年问题/);
});

test("keeps every R0.69O navigation target and source asset resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69o.html", publicRoot), "utf8");
  const ids = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const localTargets = [...note.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(localTargets.length >= 13);
  for (const target of localTargets) {
    assert.ok(ids.has(target), "missing #" + target);
  }
  for (const source of [
    "https://doi.org/10.1002/cpa.3160350604",
    "https://www.mathnet.ru/eng/dan43056",
    "https://arxiv.org/abs/2010.04105",
    "https://arxiv.org/abs/2009.14291",
  ]) {
    assert.ok(note.includes(source), source);
  }
  for (const asset of [
    "figures/r0-69o-pressure-time-closure.pdf",
    "figures/r0-69o-pressure-time-closure.svg",
    "figures/r0-69o-pressure-time-closure.png",
  ]) {
    const payload = await readFile(new URL(asset, publicRoot));
    assert.ok(payload.byteLength > 1000, asset);
  }
});

test("lists the R0.69O translations in the bilingual build", async () => {
  const translations = await readFile(
    new URL("../translations/en.json", import.meta.url),
    "utf8",
  );
  assert.match(
    translations,
    /R0\.69O \| The pressure time exponent closes; vortex stretching becomes the main obstruction/,
  );
  const generated = await readFile(new URL("i18n-en.js", publicRoot), "utf8");
  assert.match(
    generated,
    /R0\.69O \| The pressure time exponent closes; vortex stretching becomes the main obstruction/,
  );
});
