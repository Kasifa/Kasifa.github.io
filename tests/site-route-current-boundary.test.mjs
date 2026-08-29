import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

async function page(name) {
  return readFile(new URL(name, publicRoot), "utf8");
}

test("homepage current route reaches R0.73B without duplicating the note route", async () => {
  const home = await page("research-review.html");
  const match = home.match(
    /<article class="tree-node current">([\s\S]*?)<details class="tree-notes" open>/,
  );
  assert.ok(match, "current route node");
  const current = match[1];

  assert.ok(
    current.includes(
      "<h3>R0.73B：viscous-rate physical-kinetic direct sum 已闭合</h3>",
    ),
  );
  assert.equal(
    current.includes(
      "<h3>固定 \\(M\\) 的任意静态相位 Morse shape gate 已经闭合</h3>",
    ),
    false,
  );
  for (const token of [
    "R0.72R–R0.73B：",
    "caustic-free core",
    "marked \\(A_2\\)–\\(A_5\\) collisions",
    "exact scalar \\(A_2\\) block",
    "full Fourier–Leray row",
    "signed OS–Squire ledger",
    "hidden-mean transient",
    "Bloch physical-kinetic direct sum",
  ]) {
    assert.ok(current.includes(token), token);
  }

  assert.ok(
    home.includes(
      '<a class="route-map-latest" href="#r073b">阅读 R0.73B 研究笔记 →</a>',
    ),
  );
  assert.ok(home.includes('<a href="/notes/">查看完整笔记</a>'));

  const routeStart = home.indexOf('<section class="route-overview"');
  const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
  const route = home.slice(routeStart, routeEnd);
  assert.equal(
    (route.match(/href="\/notes\/r0-73b\.html"/g) ?? []).length,
    1,
    "R0.73B keeps one canonical note link in the route tree",
  );
});

test("literature route records the R0.72Z to R0.73B boundary", async () => {
  const literature = await page("literature-review.html");
  const match = literature.match(
    /<section id="route">([\s\S]*?)<figure class="topology"/,
  );
  assert.ok(match, "literature route section");
  const intro = match[1];

  for (const token of [
    "R0.72Z 在 high-gap \\(q\\)-graph 上闭合 signed OS pressure",
    "R0.73A 用 hidden physical mean 闭合 low-gap \\(X_\\mu\\) finite transient",
    "R0.73B 再由 exact Bloch carrier cancellation",
    "low-gap vector direct sum at viscous rates 已为 CLOSED",
    "complete OS--Squire A2 direct sum",
    "sharp \\(|\\Lambda|\\) law",
    "nonlinear Navier--Stokes 与 Clay 保持 OPEN",
  ]) {
    assert.ok(intro.includes(token), token);
  }
  assert.equal(
    intro.includes(
      "strong complete-row A2 estimate、low-gap vector direct sum、complete linearized shear subsystem",
    ),
    false,
  );
});
