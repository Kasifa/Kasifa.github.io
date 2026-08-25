import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69L with the exact three-zone budget and boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69l.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069l"/);
  assert.match(home, /href="\/notes\/r0-69l\.html"/);
  assert.match(home, /综述 v0\.87 · 2026-08-25/);
  assert.match(home, /i18n-en\.js(?:\?[^"]*)?/);
  assert.match(home, /下一步 R0\.69M/);
  assert.match(note, /r\^3\|\\mathcal P_r\|/);
  assert.match(note, /\\sigma_r\(N_r\+B_M\)/);
  assert.match(note, /2\^\{-5M\}\\sum_\{m\\ge M\}e_m/);
  assert.match(note, /\\inf_\{M\\ge3\}B_M/);
  assert.match(note, /\\sum_\{m\\ge2\}2\^\{-5m\}e_m/);
  assert.match(note, /\\beta\^2\/\\alpha/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
});

test("keeps every R0.69L navigation target resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69l.html", publicRoot), "utf8");
  const ids = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const localTargets = [...note.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(localTargets.length >= 10);
  for (const target of localTargets) {
    assert.ok(ids.has(target), "missing #" + target);
  }
  for (const asset of [
    "figures/r0-69l-three-zone.pdf",
    "figures/r0-69l-three-zone.svg",
    "figures/r0-69l-three-zone.png",
  ]) {
    const payload = await readFile(new URL(asset, publicRoot));
    assert.ok(payload.byteLength > 1000, asset);
  }
});

test("lists the R0.69L translations in the bilingual build", async () => {
  const translations = await readFile(
    new URL("../translations/en.json", import.meta.url),
    "utf8",
  );
  assert.match(
    translations,
    /R0\.69L \| Far-tail smallness migrates into the transition-shell budget/,
  );
  const generated = await readFile(new URL("i18n-en.js", publicRoot), "utf8");
  assert.match(
    generated,
    /R0\.69L \| Far-tail smallness migrates into the transition-shell budget/,
  );
});
