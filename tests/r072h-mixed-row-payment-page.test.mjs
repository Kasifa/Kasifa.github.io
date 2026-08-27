import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

async function readJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

test("publishes the bounded R0.72H theorem, strict delta boundary, and dual audit", async () => {
  const [home, note, recap, literature, notePdf, recapPdf] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72h.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72h.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72h.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72h.pdf")),
  ]);

  assert.match(note, /研究笔记 R0\.72H/);
  assert.match(note, /多载波混合行|mixed row/i);
  assert.ok(note.includes(String.raw`\mathcal E_Q(I)`));
  assert.ok(note.includes(String.raw`Q=P_0[V_w'+V_w(D_q+\lambda_0)]`));
  assert.ok(note.includes(String.raw`m_*(A,X)`));
  assert.ok(note.includes(String.raw`6\sqrt\nu`));
  assert.match(note, /不依赖载波数、载波位置或物理剪切相位/);
  assert.ok(note.includes(String.raw`K_{v,A}`));
  assert.ok(note.includes(String.raw`\mathcal E_Q(I)\le3E_A\rho_A^2`));

  assert.ok(note.includes(String.raw`\Phi(a)`));
  assert.ok(note.includes(String.raw`(\kappa X)^{-1/3}`));
  assert.ok(note.includes(String.raw`r_j=2M+2j+1`));
  assert.match(note, /全奇数 Rudin–Shapiro/);
  assert.ok(note.includes(String.raw`\mathcal E_Q\asymp a^2M^2`));
  assert.ok(note.includes(String.raw`Q_*\asymp a^2M^{2/3}\log M`));
  assert.ok(note.includes(String.raw`m_*\asymp\frac{a^2M^{7/3}}{\log M}`));
  assert.ok(note.includes(String.raw`M^{4/3}/\log M`));
  assert.match(note, /action-only (?:payment |版本)?(?:按[^<]*|为假|失效|不成立)/i);
  assert.match(note, /moment-resolved/i);

  assert.ok(note.includes(String.raw`\tau_M=M^{-3}`));
  assert.ok(note.includes(String.raw`\zeta_M`));
  assert.match(note, /精确目标根|精确正时刻根/);
  assert.ok(note.includes(String.raw`G_{\rm all}^{\rm ex}(I)`));
  assert.ok(note.includes(String.raw`B_AQ_*^I`));
  assert.ok(note.includes(String.raw`\delta\ne0`));
  assert.ok(note.includes(String.raw`\(\delta\ne0\) 不可省`));
  assert.ok(note.includes(String.raw`在 \(\delta=0\) 时物理 slope ledger 为零`));
  assert.ok(note.includes(String.raw`raw \(h\)-ledger 不属于该 corollary`));

  assert.match(note, /PRODUCER · ALL CHECKS PASS/);
  assert.match(note, /INDEPENDENT · ALL CHECKS PASS/);
  assert.match(note, /3\.31\\times10\^\{-6\}/);
  assert.match(note, /8\.67\\times10\^\{-19\}/);
  assert.match(note, /第一次运行[^<]*失败/);
  assert.match(note, /第二次[^<]*停止/);
  assert.match(note, /research\/certificates\/r072h/);
  for (const extension of ["png", "svg", "pdf"]) {
    assert.match(
      note,
      new RegExp(`/figures/r0-72h-mixed-row-payment\\.${extension}`),
    );
  }

  assert.match(note, /R0\.72I/);
  assert.match(note, /E_A,m_\*,B_A,\\rho_A/);
  assert.ok(note.includes(String.raw`D^{1/3}\Lambda_{1,*}`));
  assert.match(note, /不是千禧年问题的部分解决/);
  assert.match(note, /一般三维正则性：OPEN/);
  assert.doesNotMatch(note, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);

  assert.match(literature, /id="r072h-boundary"/);
  assert.match(literature, /href="\/notes\/r0-72h\.html"/);
  assert.match(literature, /R0\.69P–R0\.72L/);
  assert.match(literature, /开放接口 · R0\.72M/);
  assert.match(literature, /bounded non-collision check/i);
  assert.match(literature, /ref-96/);
  assert.match(literature, /ref-104/);

  for (const [label, pdf] of Object.entries({ notePdf, recapPdf })) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, label);
  }
  for (const page of [home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.25"/);
  }
  for (const page of [note, recap]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.21"/);
  }
  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
});

test("recaps the full post-R0.60 route through R0.72H", async () => {
  const recap = await readFile(
    resolve(publicRoot, "recap-r0-61-r0-72h.html"),
    "utf8",
  );

  assert.match(recap, /R0\.60 之后的研究回顾/);
  assert.match(recap, /R0\.61–R0\.72H 的 98 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：158/);
  assert.match(recap, /R0\.70A–R0\.72H 已公开版本/);
  assert.match(recap, /36<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 24);

  for (const routeToken of [
    "R0.61–R0.66",
    "R0.69P–R0.69W",
    "R0.70A–R0.70I",
    "R0.71A–R0.71D",
    "R0.71U–R0.71Z",
    "R0.72A",
    "R0.72F",
    "R0.72G",
    "R0.72H",
  ]) {
    assert.ok(recap.includes(routeToken), routeToken);
  }
  assert.match(recap, /finite-carrier mixed-row theorem/i);
  assert.match(recap, /载波数无关常数/);
  assert.match(recap, /全奇数 Rudin–Shapiro/);
  assert.match(recap, /compatible-real complete-root corollary|兼容实目标/);
  assert.ok(recap.includes(String.raw`\delta\ne0`));
  assert.match(recap, /问题状态：仍未解决/);
  assert.match(recap, /R0\.72I/);
  assert.ok(recap.includes(String.raw`E_A,m_*,B_A,\rho_A`));

  const nodeIndexStart = recap.indexOf('<section id="node-index">');
  const nodeIndexEnd = recap.indexOf("</section>", nodeIndexStart);
  assert.ok(nodeIndexStart >= 0 && nodeIndexEnd > nodeIndexStart);
  assert.equal(
    (
      recap
        .slice(nodeIndexStart, nodeIndexEnd)
        .match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []
    ).length,
    98,
  );
  assert.match(recap, /href="\/recap-r0-60\.html"/);
  assert.match(recap, /href="\/notes\/r0-72h\.html"/);
  assert.match(recap, /href="\/recap-r0-61-r0-72g\.html"/);
  assert.doesNotMatch(recap, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
});

test("synchronizes v1.25 counts, inventory, latest L, and next M", async () => {
  const [home, releaseManifest, archive, siteVersion, noteFiles] =
    await Promise.all([
      readFile(resolve(publicRoot, "research-review.html"), "utf8"),
      readJson(resolve(root, "research/release-manifest.json")),
      readJson(resolve(root, "research/formal-archive-inventory.json")),
      readJson(resolve(publicRoot, "site-version.json")),
      readdir(resolve(publicRoot, "notes")),
    ]);

  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 162);
  assert.match(home, /<html lang="zh-CN" data-site-version="1\.25">/);
  assert.match(home, /<strong>v1\.25<\/strong>网页版本/);
  assert.match(home, /<strong>162<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72L<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72L<\/span>/);
  assert.match(home, /展开 72 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72M/);
  assert.match(home, /累计回顾收录 102 个节点；全站现有 162 篇公开研究笔记/);
  assert.match(home, /64 个版本已公开/);
  assert.match(home, /40 个按当前 formal-figure 合同完整封存|40 个完整封存/);
  assert.match(home, /24 个旧版附图档案仍列入回补清单/);
  assert.equal((home.match(/href="\/notes\/r0-72i\.html"/g) ?? []).length, 2);
  assert.equal((home.match(/data-release="r072i"/g) ?? []).length, 1);
  assert.equal((home.match(/href="\/notes\/r0-72k\.html"/g) ?? []).length, 2);
  assert.match(home, /recap-r0-61-r0-72l\.html/);

  assert.equal(releaseManifest.latestCompletedRelease, "r072l");
  assert.equal(releaseManifest.siteVersion, "1.25");
  assert.equal(releaseManifest.publicHtmlNoteCount, 162);
  assert.equal(releaseManifest.postR060RecapNodeCount, 102);
  assert.equal(releaseManifest.postR070APublishedReleaseCount, 64);
  assert.equal(releaseManifest.postR070AFormalSealedReleaseCount, 40);
  assert.equal(releaseManifest.legacyFormalFigureBacklogCount, 24);
  assert.equal(releaseManifest.nextRelease, "r072m");
  assert.equal(
    releaseManifest.latestReleaseGate,
    "tests/r072l-strong-coupling-gate.test.mjs",
  );

  assert.equal(archive.latestPublishedRelease, "r072l");
  assert.equal(archive.publishedReleaseCount, 64);
  assert.equal(archive.formalSealedReleaseCount, 40);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.ok(archive.publishedReleases.includes("r072h"));
  assert.ok(archive.publishedReleases.includes("r072i"));
  assert.ok(archive.formalSealedReleases.includes("r072h"));
  assert.ok(archive.formalSealedReleases.includes("r072i"));
  assert.ok(archive.formalSealedReleases.includes("r072k"));

  assert.equal(siteVersion.version, "1.25");
  assert.equal(siteVersion.latestRelease, "R0.72L");
  assert.equal(siteVersion.publicHtmlNoteCount, 162);
  assert.equal(siteVersion.publishedDate, "2026-08-27");
});
