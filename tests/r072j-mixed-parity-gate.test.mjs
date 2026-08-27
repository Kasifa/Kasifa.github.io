import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

test("states the exact graph and triangle gates without upgrading them to NSE regularity", async () => {
  const note = await readFile(resolve(publicRoot, "notes/r0-72j.html"), "utf8");

  assert.match(note, /gcd-reduced bipartite test: CLOSED/i);
  assert.match(note, /triangle return criterion: CLOSED/i);
  assert.match(note, /common-band normalized counterfamily: NO-GO/i);
  assert.match(note, /complete complex-root ledger: OPEN/i);
  assert.ok(note.includes("\\(g=\\gcd(r_1,\\ldots,r_M)\\)"));
  assert.ok(note.includes("\\(a_j=r_j/g\\)"));
  assert.ok(note.includes("a_j\\equiv1\\pmod2"));
  assert.ok(note.includes("R_1(0)\\cap R_2(0)\\ne\\varnothing"));
  assert.ok(note.includes("s+t+u=0"));
  assert.match(note, /\\\{2,6\\\}[\s\S]{0,120}\\\{1,3\\\}/);
  assert.match(note, /\\\{1,4\\\}[\s\S]{0,180}最短奇闭路长度为五/);

  assert.ok(note.includes("S_R=\\{R,R+1,\\ldots,3R-1\\}"));
  assert.ok(note.includes("T_R=3R(R+1)"));
  assert.ok(note.includes("R^{-4/9}(1+\\log R)^{-2/3}"));
  assert.doesNotMatch(note, /R\^\{-4\/9\}\(\\log R\)\^\{-2\/3\}/);
  assert.ok(note.includes("R^{-2/3}\\longrightarrow0"));
  assert.ok(note.includes("\\mathcal C_{\\times,R}\\asymp R^2"));
  assert.match(note, /实标量 Rolle[\s\S]{0,120}没有自动延伸|实 Rolle complete-root 账本没有在本节闭合/);

  assert.match(note, /一般三维正则性：OPEN/);
  assert.match(note, /Clay 千禧年问题仍未解决/);
  assert.match(note, /没有证明 arbitrary-carrier physical inequality/);
  assert.doesNotMatch(note, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
});

test("keeps the real cubic quantity and archived research entry points visible", async () => {
  const note = await readFile(resolve(publicRoot, "notes/r0-72j.html"), "utf8");

  assert.ok(
    note.includes(
      "\\mathcal C_{\\times,R}=|\\delta_R|\\int_I|h_R(x)P_0V_R(x)^2F_R(x)|\\,dx",
    ),
  );
  assert.match(note, /不再使用 R0\.72I 已排除的 [\s\S]{0,20}B_AQ_\*[\s\S]{0,20}分离/);
  assert.match(note, /PRODUCER · ARCHIVED PASS/);
  assert.match(note, /INDEPENDENT · ARCHIVED PASS/);
  assert.match(note, /finite corroboration only/);
  assert.match(note, /R=64[\s\S]{0,80}T_R=12480/);
  assert.match(note, /8824\.692629208112/);
  assert.match(note, /1\.9501881021/);
  assert.match(note, /-0\.7370277418/);
  assert.match(note, /1\.53322\\times10\^\{-6\}/);
  assert.match(note, /2\.94064\\times10\^\{-12\}/);
  assert.match(note, /7\.28034\\times10\^\{-9\}/);

  for (const token of [
    "research/r072j_report-source.md",
    "research/r072j_gap_matrix.md",
    "research/r072j_literature_audit.md",
    "research/r072j_independent_audit.md",
    "research/certificates/r072j",
    "figures/r072j-mixed-parity-cubic/fig-r072j-mixed-parity-cubic",
    "/figures/r0-72j-mixed-parity-cubic.pdf",
    "/figures/r0-72j-mixed-parity-cubic.png",
    "/figures/r0-72j-mixed-parity-cubic.svg",
    "/notes/r0-72j.pdf",
    "/recap-r0-61-r0-72j.html",
    "/recap-r0-61-r0-72j.pdf",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /R0\.72K：多尺度、强耦合，或复目标根机制/);
});

test("the release generator starts from I and exposes deterministic J targets", async () => {
  const generator = await readFile(
    resolve(root, "scripts/generate_r072j_release.py"),
    "utf8",
  );

  assert.match(generator, /r0-72i\.html/);
  assert.match(generator, /recap-r0-61-r0-72i\.html/);
  assert.match(generator, /r0-72j\.html/);
  assert.match(generator, /recap-r0-61-r0-72j\.html/);
  assert.match(generator, /data-site-version="1\.23"/);
  assert.match(generator, /if "r072j" not in inventory\[key\]/);
  assert.match(generator, /expected 160 public HTML notes/);
});

test("the analytic report and public note use the same BV cubic normalization", async () => {
  const [report, note] = await Promise.all([
    readFile(resolve(root, "research/r072j_report-source.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72j.html"), "utf8"),
  ]);
  assert.equal((report.match(/2\\Theta\\mathcal C_\\times/g) ?? []).length, 3);
  assert.equal(
    (report.match(/2\\Theta\\mathcal C_\{\\times,R\}/g) ?? []).length,
    1,
  );
  assert.ok(note.includes("2\\Theta_R\\mathcal C_{\\times,R}"));
  assert.doesNotMatch(report, /(?<!2)\\Theta\\mathcal C_\\times/);
  assert.doesNotMatch(report, /(?<!2)\\Theta\\mathcal C_\{\\times,R\}/);
});

test("the formal figure uses the exact theorem rate and J source lineage", async () => {
  const figureRoot = resolve(
    root,
    "figures/r072j-mixed-parity-cubic/fig-r072j-mixed-parity-cubic",
  );
  const [builder, data, caption] = await Promise.all([
    readFile(resolve(figureRoot, "build_figure.py"), "utf8"),
    readFile(resolve(figureRoot, "data.csv"), "utf8"),
    readFile(resolve(figureRoot, "caption.md"), "utf8"),
  ]);
  for (const text of [builder, data, caption]) {
    assert.match(text, /R\^-4\/9\s*\(1\+log R\)\^-2\/3/i);
    assert.doesNotMatch(text, /R\^-4\/9\s*\(log R\)\^-2\/3/i);
  }
  assert.match(data, /research\/r072j_report-source\.md/);
  assert.doesNotMatch(data, /research\/r072i_report-source\.md/);
});
