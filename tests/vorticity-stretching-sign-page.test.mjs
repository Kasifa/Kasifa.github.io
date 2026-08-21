import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69P with sharp local stretching geometry and strict boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69p.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069p"/);
  assert.match(home, /href="\/notes\/r0-69p\.html"/);
  assert.match(home, /综述 v0\.78 · 2026-08-21/);
  assert.match(home, /i18n-en\.js\?v=0\.78/);
  assert.match(home, /下一步 R0\.69Q/);
  assert.ok(note.includes("|\\omega\\cdot S\\omega|\\le\\sqrt{\\frac23}\\,|S|\\,|\\omega|^2"));
  assert.ok(note.includes("v_A=\\nabla\\times(\\chi B_A)"));
  assert.ok(note.includes("\\int\\omega\\cdot S\\omega\\,dx=-4\\int\\det S\\,dx"));
  assert.ok(note.includes("-4\\det S\\le2\\lambda_2^+|S|^2"));
  assert.ok(note.includes("\\lambda_2^+\\le\\frac{|S|}{\\sqrt6}"));
  assert.ok(note.includes("\\frac{27}{256}\\varepsilon^{-3}\\sigma^6"));
  assert.match(note, /没有解决千禧年问题/);
  assert.match(note, /R0\.69Q 将审计/);
});

test("keeps every R0.69P navigation target and source asset resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69p.html", publicRoot), "utf8");
  const ids = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const localTargets = [...note.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(localTargets.length >= 12);
  for (const target of localTargets) {
    assert.ok(ids.has(target), "missing #" + target);
  }
  for (const source of [
    "https://doi.org/10.1017/S0022112056000317",
    "https://doi.org/10.1512/iumj.1993.42.42034",
    "https://arxiv.org/abs/1710.05569",
  ]) {
    assert.ok(note.includes(source), source);
  }
  for (const asset of [
    "figures/r0-69p-stretching-sign.pdf",
    "figures/r0-69p-stretching-sign.svg",
    "figures/r0-69p-stretching-sign.png",
  ]) {
    const payload = await readFile(new URL(asset, publicRoot));
    assert.ok(payload.byteLength > 1000, asset);
  }
});

test("lists the R0.69P translations in the bilingual build", async () => {
  const translations = await readFile(
    new URL("../translations/en.json", import.meta.url),
    "utf8",
  );
  assert.match(
    translations,
    /R0\.69P \| Pointwise stretching can saturate exactly; the missing structure is spacetime depletion/,
  );
  const generated = await readFile(new URL("i18n-en.js", publicRoot), "utf8");
  assert.match(
    generated,
    /R0\.69P \| Pointwise stretching can saturate exactly; the missing structure is spacetime depletion/,
  );
});
