import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const jFigureRoot = new URL(
  "figures/r070j-deviatoric-helical/fig-r070j-deviatoric-helical/",
  root,
);
const kFigureRoot = new URL(
  "figures/r070k-anisotropy-evolution/fig-r070k-anisotropy-evolution/",
  root,
);

function assertLocalAnchorsResolve(html, minimum) {
  const ids = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(targets.length >= minimum, `only ${targets.length} local targets`);
  for (const target of targets) {
    assert.ok(ids.has(target), `missing local target #${target}`);
  }
}

function assertBilingualAssetsPrecedeMathJax(html) {
  const css = html.indexOf('href="/bilingual.css"');
  const dictionary = html.indexOf('src="/i18n-en.js?v=0.81"');
  const runtime = html.indexOf('src="/bilingual.js"');
  const mathJax = html.indexOf("mathjax@3/es5/tex-mml-chtml.js");
  assert.ok(css >= 0 && dictionary > css && runtime > dictionary);
  assert.ok(mathJax > runtime, "MathJax must load after bilingual assets");
}

test("publishes the R0.70J exact helicity obstruction with its claim boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-70j.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r070j"/);
  assert.match(home, /href="\/notes\/r0-70j\.html"/);
  assert.match(note, /S:\\mathring Q\(w\)=w\^\{\\mathsf T\}Sw/);
  assert.match(note, /K_S\(\\xi\)=-\\xi\^\{\\mathsf T\}S\\xi/);
  assert.ok(note.includes("\\frac{\\sqrt3}{9}&gt;0"));
  assert.match(note, /紧支撑载体与严格带限对象不能是同一个函数/);
  assert.ok(note.includes("时间窗随缩放按 \\(r^2\\) 缩短"));
  assert.match(note, /空间反演奇偶与线性热层/);
  assert.match(note, /审计的十篇原始来源/);
  assert.match(note, /不是全体文献不存在性定理/);
  assert.match(note, /独立内部复核 PASS/);
  assert.equal((note.match(/<tr><td>R0\.70[A-I]<\/td>/g) ?? []).length, 9);
  assert.match(note, /不能被称为 Millennium 问题的部分解答/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|三重审计|突破|线性时间奇偶|法向动力学控制|独立 PASS 审计|不会替我|伪装成/);
  assert.doesNotMatch(note, /__[A-Z0-9_]+__/);
  assertLocalAnchorsResolve(note, 10);
  assertBilingualAssetsPrecedeMathJax(note);
});

test("publishes the R0.70K normalized-anisotropy no-go result exactly", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-70k.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r070k"/);
  assert.match(home, /href="\/notes\/r0-70k\.html"/);
  assert.ok(note.includes("B=R-\\frac13I=\\frac{\\operatorname{dev}Q}{E}"));
  assert.ok(
    note.includes(
      "\\dot B=\n            \\frac{\\operatorname{dev}F-B\\operatorname{tr}F}{E}",
    ),
  );
  assert.ok(
    note.includes(
      "2\\operatorname{tr}\\!\\left[R(\\Sigma-qI)^2\\right]\\ge0",
    ),
  );
  assert.match(note, /12\\nu p\(1-p\)\(2p-1\)/);
  assert.match(note, /\+144\\nu\/125.*-144\\nu\/125/);
  assert.ok(note.includes("恒等滤波与 \\(\\chi\\equiv1\\) 的全环面平均"));
  assert.match(note, /Burgers 涡也不是 Leray 有限能量场/);
  assert.match(note, /固定且与空间导数可交换的滤波/);
  assert.match(note, /没有解决千禧年问题/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|三重审计|突破/);
  assert.ok(note.includes("下一步，我只检查源演化补偿"));
  assert.doesNotMatch(note, /__[A-Z0-9_]+__/);
  assertLocalAnchorsResolve(note, 10);
  assertBilingualAssetsPrecedeMathJax(note);
});

test("keeps every R0.70J/K public figure byte-exact and links the archives", async () => {
  const [jNote, kNote] = await Promise.all([
    readFile(new URL("notes/r0-70j.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-70k.html", publicRoot), "utf8"),
  ]);

  for (const [release, note, archive, publicStem] of [
    ["r070j", jNote, jFigureRoot, "r0-70j-deviatoric-helical"],
    ["r070k", kNote, kFigureRoot, "r0-70k-anisotropy-evolution"],
  ]) {
    for (const source of [
      `research/${release}_report-source.md`,
      `research/${release}_literature_audit.md`,
      `research/${release}_independent_audit.md`,
      `research/certificates/${release}`,
      `figures/${release === "r070j" ? "r070j-deviatoric-helical/fig-r070j-deviatoric-helical" : "r070k-anisotropy-evolution/fig-r070k-anisotropy-evolution"}`,
      "https://www.claymath.org/millennium/navier-stokes-equation/",
    ]) {
      assert.ok(note.includes(source), `${release}: ${source}`);
    }
    for (const extension of ["pdf", "png", "svg"]) {
      const [archived, published] = await Promise.all([
        readFile(new URL(`figure.${extension}`, archive)),
        readFile(new URL(`figures/${publicStem}.${extension}`, publicRoot)),
      ]);
      assert.deepEqual(published, archived, `${release}.${extension}`);
    }
  }
});

test("ships complete R0.70J/K translations in the generated dictionary", async () => {
  const [translations, generated] = await Promise.all([
    readFile(new URL("translations/en.json", root), "utf8"),
    readFile(new URL("i18n-en.js", publicRoot), "utf8"),
  ]);
  for (const phrase of [
    "R0.70J | The deviatoric high-high correlation has no hidden helicity null structure",
    "The value is to turn a vague ‘perhaps there is a null structure’ into a falsifiable proposition",
    "R0.70K | Normalized vorticity anisotropy is bounded, but not dissipative",
    "The value is to close one route and leave a testable new gate",
  ]) {
    assert.ok(translations.includes(phrase), phrase);
    assert.ok(generated.includes(phrase), phrase);
  }
});
