import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

test("states the directional zero-sampling theorem and its sharp boundaries", async () => {
  const [report, note] = await Promise.all([
    readFile(resolve(root, "research/r072k_report-source.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72k.html"), "utf8"),
  ]);

  for (const text of [report, note]) {
    assert.match(text, /real or complex Banach|实或复 Banach/);
    assert.ok(text.includes("W^{2,1}"));
    assert.match(text, /norming functional|norming direction/);
    assert.match(text, /factor two|系数 2/i);
    assert.match(text, /first-root|首根/i);
    assert.match(text, /root count|根数/i);
  }

  assert.ok(report.includes("\\sum_{j=2}^m\\|X'(t_j)\\|_B^2"));
  assert.ok(report.includes("2\\int_I\\|X'(t)\\|_B\\,\\|X''(t)\\|_B\\,dt"));
  assert.ok(note.includes("\\sum_{j=2}^{m}\\|X'(t_j)\\|_B^2"));
  assert.ok(note.includes("2\\int_I\\|X'(t)\\|_B\\,\\|X''(t)\\|_B\\,dt"));
  assert.match(report, /X\(t\)=e\^\{2\\pi it\}-1[\s\S]{0,180}X'\(t\)\\ne0/);
  assert.match(note, /e\^\{2\\pi it\}-1[\s\S]{0,180}literal complex Rolle/);
});

test("closes the complete complex target ledger without a real gauge", async () => {
  const [report, note, gap] = await Promise.all([
    readFile(resolve(root, "research/r072k_report-source.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72k.html"), "utf8"),
    readFile(resolve(root, "research/r072k_gap_matrix.md"), "utf8"),
  ]);

  for (const text of [report, note, gap]) {
    assert.match(
      text,
      /complete complex-target|complete complex target|complete complex-root/i,
    );
    assert.match(text, /E_A\\rho_A\^2\+2\\mathcal E_Q(?:\(I\))?\+2\\mathcal C_\\times(?:\(I\))?/);
    assert.match(text, /\\delta\\ne0|delta\s*!=\s*0/i);
    assert.match(text, /real gauge|实 gauge/i);
  }
  assert.doesNotMatch(note, /complete complex-root ledger: OPEN/i);
  assert.match(note, /complete complex-target ledger: CLOSED/i);
  assert.match(note, /literal complex Rolle 不成立/i);
  assert.doesNotMatch(note, /额外.*2\\lambda_0\^2Q_\*/);
});

test("keeps the common-band physical theorem exact and scoped", async () => {
  const [report, note] = await Promise.all([
    readFile(resolve(root, "research/r072k_report-source.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72k.html"), "utf8"),
  ]);

  for (const text of [report, note]) {
    assert.match(text, /G_\{\\rm all\}\^\{\\rm ex\}\\asymp a\^2N\^2/);
    assert.match(text, /\\mathcal J_\{\\rm all\}\\asymp(?:\\frac\{g\^2N\}\{R\^2\}|\s*\\frac\{g\^2N\}\{R\^2\})/);
    assert.ok(text.includes("R^{-4/9}(1+\\log R)^{-2/3}"));
    assert.match(text, /multiscale|多尺度/i);
    assert.match(text, /strong coupling|strong-coupling/i);
  }
  assert.match(note, /一般三维正则性：OPEN/);
  assert.match(note, /Clay 千禧年问题仍未解决/);
  assert.doesNotMatch(note, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
});
