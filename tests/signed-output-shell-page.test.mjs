import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69S with the exact one-shell theorem and strict boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69s.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069s"/);
  assert.match(home, /href="\/notes\/r0-69s\.html"/);
  assert.match(home, /综述 v0\.82 · 2026-08-24/);
  assert.match(home, /i18n-en\.js\?v=0\.82/);
  assert.match(home, /下一步 R0\.69T/);
  assert.ok(note.includes("\\mathcal F_0(u)=2"));
  assert.ok(note.includes("\\mathcal F_m(u)=0\\ (m\\ne0)"));
  assert.ok(note.includes("(T_k,T_p,T_q)=(2,-3,1)"));
  assert.ok(note.includes("2-3+2=1&gt;0"));
  assert.ok(note.includes("\\Gamma(u^{(\\ell)})=1"));
  assert.match(note, /只针对互不重叠的尖锐 Fourier 输出壳/);
  assert.match(note, /没有解决千禧年问题/);
  assert.match(note, /R0\.69T 转向物理空间环带/);
});

test("keeps every R0.69S navigation target and source asset resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69s.html", publicRoot), "utf8");
  const ids = new Set([...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  const localTargets = [...note.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(localTargets.length >= 13);
  for (const target of localTargets) assert.ok(ids.has(target), "missing #" + target);
  for (const source of [
    "https://doi.org/10.24033/asens.1404",
    "https://www.claymath.org/millennium/navier-stokes-equation/",
  ]) assert.ok(note.includes(source), source);
  for (const asset of [
    "figures/r0-69s-single-shell.pdf",
    "figures/r0-69s-single-shell.svg",
    "figures/r0-69s-single-shell.png",
  ]) {
    const payload = await readFile(new URL(asset, publicRoot));
    assert.ok(payload.byteLength > 1000, asset);
  }
});

test("lists the R0.69S translations in the bilingual build", async () => {
  const translations = await readFile(new URL("../translations/en.json", import.meta.url), "utf8");
  assert.match(
    translations,
    /R0\.69S \| One Fourier shell can carry all signed vortex stretching/,
  );
  const generated = await readFile(new URL("i18n-en.js", publicRoot), "utf8");
  assert.match(
    generated,
    /R0\.69S \| One Fourier shell can carry all signed vortex stretching/,
  );
});
