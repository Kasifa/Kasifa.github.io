import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69R with the exact optimized split and strict boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69r.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069r"/);
  assert.match(home, /href="\/notes\/r0-69r\.html"/);

  assert.match(home, /i18n-en\.js(?:\?[^"]*)?/);
  assert.match(home, /下一步 R0\.69S/);
  assert.ok(note.includes("C_{\\rm n}rA^{1/2}B^{5/2}"));
  assert.ok(note.includes("+C_{\\rm f}r^{-3/2}A^3"));
  assert.ok(note.includes("\\omega(x+z)-\\omega(x)"));
  assert.ok(note.includes("\\boxed{p+q=3,\\qquad p+3q=6"));
  assert.ok(note.includes("\\frac{27C_*^4}{256\\varepsilon^3}A^6"));
  assert.match(note, /没有解决千禧年问题/);
  assert.match(note, /R0\.69S 将在取绝对值之前检查有符号尺度局部通量/);
});

test("keeps every R0.69R navigation target and source asset resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69r.html", publicRoot), "utf8");
  const ids = new Set([...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  const localTargets = [...note.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(localTargets.length >= 13);
  for (const target of localTargets) assert.ok(ids.has(target), "missing #" + target);
  for (const source of [
    "https://doi.org/10.1512/iumj.1993.42.42034",
    "https://doi.org/10.1017/CBO9780511613203",
  ]) assert.ok(note.includes(source), source);
  for (const asset of [
    "figures/r0-69r-nonlocal-difference.pdf",
    "figures/r0-69r-nonlocal-difference.svg",
    "figures/r0-69r-nonlocal-difference.png",
  ]) {
    const payload = await readFile(new URL(asset, publicRoot));
    assert.ok(payload.byteLength > 1000, asset);
  }
});

test("lists the R0.69R translations in the bilingual build", async () => {
  const translations = await readFile(new URL("../translations/en.json", import.meta.url), "utf8");
  assert.match(
    translations,
    /R0\.69R \| The nonlocal vorticity difference removes a singular order but returns to the classical sextic cost/,
  );
  const generated = await readFile(new URL("i18n-en.js", publicRoot), "utf8");
  assert.match(
    generated,
    /R0\.69R \| The nonlocal vorticity difference removes a singular order but returns to the classical sextic cost/,
  );
});
