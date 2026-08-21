import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69Q with the exact polar identities and strict boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69q.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069q"/);
  assert.match(home, /href="\/notes\/r0-69q\.html"/);
  assert.match(home, /综述 v0\.76 · 2026-08-21/);
  assert.match(home, /i18n-en\.js\?v=0\.76/);
  assert.match(home, /下一步 R0\.69R/);
  assert.ok(note.includes("=\\rho\\alpha-\\nu\\rho|\\nabla\\xi|^2"));
  assert.ok(note.includes("(I-\\xi\\otimes\\xi)\\Delta\\xi"));
  assert.ok(note.includes("|\\nabla\\omega|^2\n            =|\\nabla\\rho|^2+\\rho^2|\\nabla\\xi|^2"));
  assert.ok(note.includes("\\nabla\\rho=\\nabla\\xi=\\nabla\\omega=0"));
  assert.ok(note.includes("\\frac{D_\\xi(T)}T\\to0"));
  assert.ok(note.includes("\\frac{D_\\omega(T)}T\\to0"));
  assert.match(note, /没有解决千禧年问题/);
  assert.match(note, /R0\.69R 将保留非局部涡量差分/);
});

test("keeps every R0.69Q navigation target and source asset resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69q.html", publicRoot), "utf8");
  const ids = new Set([...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  const localTargets = [...note.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(localTargets.length >= 12);
  for (const target of localTargets) assert.ok(ids.has(target), "missing #" + target);
  for (const source of [
    "https://doi.org/10.1512/iumj.1993.42.42034",
    "https://doi.org/10.57262/die/1356060864",
    "https://doi.org/10.1007/s00220-008-0726-8",
  ]) assert.ok(note.includes(source), source);
  for (const asset of [
    "figures/r0-69q-direction-diffusion.pdf",
    "figures/r0-69q-direction-diffusion.svg",
    "figures/r0-69q-direction-diffusion.png",
  ]) {
    const payload = await readFile(new URL(asset, publicRoot));
    assert.ok(payload.byteLength > 1000, asset);
  }
});

test("lists the R0.69Q translations in the bilingual build", async () => {
  const translations = await readFile(new URL("../translations/en.json", import.meta.url), "utf8");
  assert.match(
    translations,
    /R0\.69Q \| Direction diffusion is not extra dissipation; the affine core rules out interior absorption/,
  );
  const generated = await readFile(new URL("i18n-en.js", publicRoot), "utf8");
  assert.match(
    generated,
    /R0\.69Q \| Direction diffusion is not extra dissipation; the affine core rules out interior absorption/,
  );
});
