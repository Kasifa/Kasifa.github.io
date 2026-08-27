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

test("publishes the bounded R0.72G theorem without changing its numerical method", async () => {
  const [home, note, recap, literature, notePdf, recapPdf] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72g.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72g.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72g.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72g.pdf")),
  ]);

  assert.match(note, /研究笔记 R0\.72G/);
  assert.match(note, /complete-root|完整根/i);
  assert.ok(note.includes(String.raw`\delta\ge1`));
  assert.match(note, /Rolle.?BV/i);
  assert.ok(note.includes(String.raw`G_{\rm all}`));
  assert.ok(note.includes(String.raw`\asymp\log\delta`));
  assert.ok(note.includes(String.raw`D^{1/3}\Lambda_{1,*}`));
  assert.match(note, /fixed-step RK4/);
  assert.match(note, /Hermite[^<]{0,40}Brent/);
  assert.doesNotMatch(note, /adaptive BDF/i);
  assert.match(note, /Fourier Strang/i);
  assert.match(note, /9\.18[^<]{0,24}10\^\{-7\}|9\.18[^<]{0,24}10<sup>−?7<\/sup>/);
  assert.match(note, /failed attempt|失败尝试|首轮失败/i);
  assert.match(note, /research\/certificates\/r072g/);
  for (const extension of ["png", "svg", "pdf"]) {
    assert.match(
      note,
      new RegExp(`/figures/r0-72g-complete-root-packing\\.${extension}`),
    );
  }

  assert.match(note, /R0\.72H/);
  assert.ok(note.includes(String.raw`\mathcal E_Q`));
  assert.match(note, /mixed row term|混合(?:行|项)/i);
  assert.match(note, /dimension-free|载波数无关|维数无关/i);
  assert.match(note, /multi-carrier|多载波/i);
  assert.match(note, /fixed-\(q_0\)|fixed-q0|固定(?:整数 )?\\\(q_0\\\)/i);
  assert.match(note, /不(?:是|证明).*一般.*Navier|不触及一般.*正则性|没有证明.*正则性/s);
  assert.doesNotMatch(note, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);

  assert.match(literature, /id="r072g-boundary"/);
  assert.match(literature, /href="\/notes\/r0-72g\.html"/);
  assert.match(literature, /R0\.69P–R0\.72G/);
  assert.match(literature, /开放接口 · R0\.72H/);

  for (const [label, pdf] of Object.entries({ notePdf, recapPdf })) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, label);
  }
  for (const page of [home, note, recap, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.20"/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
});

test("recaps the full post-R0.60 route through R0.72G", async () => {
  const recap = await readFile(
    resolve(publicRoot, "recap-r0-61-r0-72g.html"),
    "utf8",
  );

  assert.match(recap, /R0\.60 之后的研究回顾/);
  assert.match(recap, /R0\.61–R0\.72G 的 97 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：157/);
  assert.match(recap, /R0\.70A–R0\.72G 已公开版本/);
  assert.match(recap, /35<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 23);

  for (const routeToken of [
    "R0.61–R0.66",
    "R0.69P–R0.69W",
    "R0.70A–R0.70I",
    "R0.71A–R0.71D",
    "R0.71U–R0.71Z",
    "R0.72A",
    "R0.72F",
    "R0.72G",
  ]) {
    assert.ok(recap.includes(routeToken), routeToken);
  }
  assert.match(recap, /完整根|complete-root/i);
  assert.match(recap, /Rolle.?BV/i);
  assert.match(recap, /问题状态：仍未解决/);
  assert.match(recap, /R0\.72H/);
  assert.ok(recap.includes(String.raw`\mathcal E_Q`));
  assert.match(recap, /dimension-free|载波数无关|维数无关/i);
  assert.match(recap, /multi-carrier|多载波/i);

  const nodeIndexStart = recap.indexOf('<section id="node-index">');
  const nodeIndexEnd = recap.indexOf("</section>", nodeIndexStart);
  assert.ok(nodeIndexStart >= 0 && nodeIndexEnd > nodeIndexStart);
  assert.equal(
    (
      recap
        .slice(nodeIndexStart, nodeIndexEnd)
        .match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []
    ).length,
    97,
  );
  assert.match(recap, /href="\/recap-r0-60\.html"/);
  assert.match(recap, /href="\/notes\/r0-72g\.html"/);
  assert.doesNotMatch(recap, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
});

test("synchronizes v1.20 counts, inventory, latest gate, and next release", async () => {
  const [home, releaseManifest, archive, siteVersion, noteFiles] =
    await Promise.all([
      readFile(resolve(publicRoot, "research-review.html"), "utf8"),
      readJson(resolve(root, "research/release-manifest.json")),
      readJson(resolve(root, "research/formal-archive-inventory.json")),
      readJson(resolve(publicRoot, "site-version.json")),
      readdir(resolve(publicRoot, "notes")),
    ]);

  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 157);
  assert.match(home, /<html lang="zh-CN" data-site-version="1\.20">/);
  assert.match(home, /<strong>v1\.20<\/strong>网页版本/);
  assert.match(home, /<strong>157<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72G<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72G<\/span>/);
  assert.match(home, /展开 67 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72H/);
  assert.match(home, /累计回顾收录 97 个节点；全站现有 157 篇公开研究笔记/);
  assert.match(home, /59 个版本已公开/);
  assert.match(home, /35 个完整封存/);
  assert.match(home, /24 个旧版附图档案列入回补清单/);
  assert.equal((home.match(/href="\/notes\/r0-72g\.html"/g) ?? []).length, 2);
  assert.equal((home.match(/data-release="r072g"/g) ?? []).length, 1);
  assert.match(home, /recap-r0-61-r0-72g\.html/);

  assert.equal(releaseManifest.latestCompletedRelease, "r072g");
  assert.equal(releaseManifest.siteVersion, "1.20");
  assert.equal(releaseManifest.publicHtmlNoteCount, 157);
  assert.equal(releaseManifest.postR060RecapNodeCount, 97);
  assert.equal(releaseManifest.postR070APublishedReleaseCount, 59);
  assert.equal(releaseManifest.postR070AFormalSealedReleaseCount, 35);
  assert.equal(releaseManifest.legacyFormalFigureBacklogCount, 24);
  assert.equal(releaseManifest.nextRelease, "r072h");
  assert.equal(
    releaseManifest.latestReleaseGate,
    "tests/r072g-complete-root-packing-gate.test.mjs",
  );

  assert.equal(archive.latestPublishedRelease, "r072g");
  assert.equal(archive.publishedReleaseCount, 59);
  assert.equal(archive.formalSealedReleaseCount, 35);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.ok(archive.formalSealedReleases.includes("r072g"));

  assert.equal(siteVersion.version, "1.20");
  assert.equal(siteVersion.latestRelease, "R0.72G");
  assert.equal(siteVersion.publicHtmlNoteCount, 157);
  assert.equal(siteVersion.publishedDate, "2026-08-27");
});
