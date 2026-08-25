import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);

function assertLocalAnchorsResolve(html) {
  const ids = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(targets.length >= 12);
  for (const target of targets) assert.ok(ids.has(target), target);
}

test("publishes the exact R0.71B common-response boundary", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71b.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71b.pdf", publicRoot)),
  ]);

  assert.match(home, /id="r071b"/);
  assert.equal((home.match(/href="\/notes\/r0-71b\.html"/g) ?? []).length, 2);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.ok(pdf.length > 100_000);
  for (const token of [
    "\\mathcal U_M\\nearrow1",
    "M^2\\mathcal C_M\\longrightarrow-\\frac12",
    "\\|\\omega_N\\|_2^2=\\frac32",
    "\\sim\\frac1{4\\sqrt N}",
    "\\mathfrak P_{\\rm cr}(A_N;B_N,C_N)",
    "\\mathcal T_+^2=\\frac9{800}\\Lambda^4",
    "a_+=\\frac3{39940400}\\Lambda^2",
    "(\\mathfrak P_Q)_+",
    "a_+\\in L_t^1",
  ]) {
    assert.ok(note.includes(token), token);
  }
});

test("keeps the polarized no-go and continuation boundaries explicit", async () => {
  const note = await readFile(new URL("notes/r0-71b.html", publicRoot), "utf8");

  assert.match(note, /严格限于这个<strong>三场极化估计<\/strong>/);
  assert.match(note, /不否定已知的单场 Besov 混合估计/);
  assert.match(note, /不是闭合/);
  assert.match(note, /不会得到新的延拓定理/);
  assert.match(note, /没有给出新的无条件正则性结论/);
  assert.match(note, /不是 Navier–Stokes 解轨道/);
  assert.match(note, /有限枚举只是回归证书；任意 .*解析证明承担/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assertLocalAnchorsResolve(note);
});

test("ships the synchronized journal figure assets and local page links", async () => {
  const [note, svg, pdf, png] = await Promise.all([
    readFile(new URL("notes/r0-71b.html", publicRoot), "utf8"),
    readFile(new URL("figures/r0-71b-common-packing.svg", publicRoot), "utf8"),
    readFile(new URL("figures/r0-71b-common-packing.pdf", publicRoot)),
    readFile(new URL("figures/r0-71b-common-packing.png", publicRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71b-common-packing\.svg"/);
  assert.match(note, /href="\/figures\/r0-71b-common-packing\.pdf"/);
  assert.match(note, /href="\/figures\/r0-71b-common-packing\.png"/);
  assert.match(svg, /<svg/);
  assert.equal(pdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.ok(pdf.length > 10_000);
  assert.ok(png.length > 100_000);
});

test("links the certificate, independent checker, and primary sources", async () => {
  const note = await readFile(new URL("notes/r0-71b.html", publicRoot), "utf8");
  for (const source of [
    "research/r071b_report-source.md",
    "research/r071b_literature_audit.md",
    "research/r071b_independent_audit.md",
    "research/r071b_exact_audit.py",
    "research/r071b_independent_audit.py",
    "research/certificates/r071b",
    "ASENS_1981_4_14_2_209_0",
    "0022123685900072",
    "BF02392215",
    "57_2_303",
    "nas.pdf",
  ]) {
    assert.ok(note.includes(source), source);
  }
});

test("retains the R0.71B historical page", async () => {
  const note = await readFile(new URL("notes/r0-71b.html", publicRoot), "utf8");
  assert.match(note, /src="\/i18n-en\.js\?v=0\.87"/);
});
