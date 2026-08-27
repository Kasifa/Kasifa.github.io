import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

test("states the coupling-uniform ledger with the actual denominator", async () => {
  const [report, note, gap] = await Promise.all([
    readFile(resolve(root, "research/r072l_report-source.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72l.html"), "utf8"),
    readFile(resolve(root, "research/r072l_gap_matrix.md"), "utf8"),
  ]);

  for (const text of [report, note, gap]) {
    assert.match(text, /\\varepsilon\s*:?=\s*(?:\\frac\{gB\}\{R\^2\}|gB\/R\^2)/);
    assert.match(text, /full[- ]Fourier[- ]lattice|full[- ]lattice/i);
  }
  for (const text of [report, note]) {
    assert.match(text, /K(?:\s*)=(?:\s*)\\mathcal R_Y/);
    assert.match(text, /x(?:\s*)=(?:\s*)\\Theta Q_\*/);
  }

  for (const token of [
    "\\frac{U_0}{K+x}",
    "W\\frac{\\sqrt x}{K+x}",
    "\\frac{\\min\\{U,Vx\\}}{K+x}",
    "\\Lambda_{1,*}\\gtrsim K+x",
  ]) {
    assert.ok(report.includes(token), token);
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /只给单边 root lift，不能写成双边等价/);
  assert.ok(note.includes("|\\delta|\\int_0^\\infty\\|V_w(x)\\|\\,dx\\lesssim\\varepsilon"));
  assert.match(note, /不假设反向估计/);
  assert.match(note, /实际 Duhamel exposure 可以更小/);
  assert.doesNotMatch(
    note,
    /\\varepsilon\s*=\s*\|\\delta\|\\int[\s\S]{0,120}\\asymp\s*\\frac\{gB\}\{R\^2\}/,
  );
});

test("keeps the exact corrected family and the window endpoint honest", async () => {
  const [report, note, audit] = await Promise.all([
    readFile(resolve(root, "research/r072l_report-source.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72l.html"), "utf8"),
    readFile(resolve(root, "research/r072l_independent_audit.md"), "utf8"),
  ]);

  for (const text of [report, note, audit]) {
    assert.match(text, /phase-aligned/i);
    assert.match(text, /row-aligned/i);
    assert.match(text, /exact(?:ly)?[- ]corrected|exact root|exact correction/i);
    assert.match(text, /fixed (?:decoupled )?background|固定背景/i);
    assert.match(text, /little-o/i);
    assert.match(text, /O\(1\)|统一有界|bounded normalized\s+ledger/i);
  }

  assert.ok(
    note.includes(
      "1\\lesssim\\varepsilon\\lesssim p^{2/3}R^{2/3}(1+\\log R)",
    ),
  );
  assert.ok(
    note.includes(
      "\\varepsilon=o(p^{2/3}R^{2/3}(1+\\log R))",
    ),
  );
  assert.ok(note.includes("cubic 项在上沿保持 \\(O(1)\\)"));
  assert.match(note, /三项才全部趋零/);
  assert.doesNotMatch(
    note,
    /上沿(?:直接|即|便|就)?(?:给出|得到|保持)?\s*(?:趋零|衰减)/,
  );
});

test("separates the projected Galerkin countertheorem from the full lattice", async () => {
  const [report, note, gap] = await Promise.all([
    readFile(resolve(root, "research/r072l_report-source.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72l.html"), "utf8"),
    readFile(resolve(root, "research/r072l_gap_matrix.md"), "utf8"),
  ]);

  for (const text of [report, note, gap]) {
    assert.match(text, /Galerkin/i);
    assert.match(text, /not a full-lattice|不是 full Fourier lattice|不能嵌入完整|非full lattice|non-embedding/i);
    assert.match(text, /no nonzero finite|没有非零有限|no finite Fourier-support embedding|extremal convolution index leaves every finite support/i);
  }
  assert.ok(note.includes("\\frac1{\\sqrt2}"));
  assert.match(note, /它不是 full Fourier lattice/);
  assert.match(note, /extreme strong coupling: OPEN/i);
  assert.match(note, /一般三维正则性：OPEN/);
  assert.match(note, /Clay 千禧年问题仍未解决/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
});
