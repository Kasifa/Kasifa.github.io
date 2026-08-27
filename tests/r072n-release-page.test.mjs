import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  collectSiteStrings,
  extractProtectedTokens,
} from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

async function json(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

test("publishes the 104-node post-R0.60 recap in 28 phases", async () => {
  const recap = await readFile(
    resolve(publicRoot, "recap-r0-61-r0-72n.html"),
    "utf8",
  );

  assert.match(recap, /R0\.61–R0\.72N 的 104 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：164/);
  assert.match(recap, /66<\/strong><span>R0\.70A–R0\.72N 已公开版本/);
  assert.match(recap, /42<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.match(recap, /28<\/strong><span>按问题划分的研究阶段/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 28);

  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, "current recap node index");
  const index = recap.slice(start, end);
  assert.equal(
    (index.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length,
    104,
  );
  assert.equal(
    (index.match(/href="\/notes\/r0-72n\.html"/g) ?? []).length,
    1,
  );

  for (const token of [
    "R0.72L–R0.72N",
    "action-poor route 失效",
    "\\mathcal C_{\\rm diss}\\lesssim a^2\\sqrt\\sigma",
    "本站 corollary",
    "logarithmic rate 与多载波仍开放",
    "R0.72O",
    "/recap-r0-60.html",
    "/recap-r0-61-r0-72m.html",
  ]) {
    assert.ok(recap.includes(token), token);
  }
});

test("retains N while synchronizing v1.28, latest O, next P, and all publication counts", async () => {
  const [home, literature, release, archive, site, files] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    json(resolve(root, "research/release-manifest.json")),
    json(resolve(root, "research/formal-archive-inventory.json")),
    json(resolve(publicRoot, "site-version.json")),
    readdir(resolve(publicRoot, "notes")),
  ]);

  assert.equal(files.filter((name) => name.endsWith(".html")).length, 165);
  assert.match(home, /<html lang="zh-CN" data-site-version="1\.28">/);
  assert.match(home, /<strong>v1\.28<\/strong>网页版本/);
  assert.match(home, /<strong>165<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72O<\/strong>最新研究节点/);
  assert.match(home, /R0\.70A–R0\.72O：67 节已公开，43 节完整封存/);
  assert.match(home, /R0\.70A–R0\.72O 共 67 个版本已公开；43 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72O<\/span>/);
  assert.match(home, /展开 75 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72P/);
  assert.match(home, /累计回顾收录 105 个节点；全站现有 165 篇公开研究笔记/);
  assert.equal((home.match(/data-release="r072n"/g) ?? []).length, 1);
  assert.equal(
    (home.match(/href="\/notes\/r0-72n\.html"/g) ?? []).length,
    2,
  );
  assert.match(home, /dissipative one-carrier decision/i);
  assert.match(home, /physical reinsertion/i);
  assert.match(home, /full-superposition ED gate/i);

  assert.match(literature, /本站 R0\.69P–R0\.72O 只列为研究笔记/);
  assert.match(literature, /id="r072n-boundary"/);
  assert.match(literature, /开放接口 · R0\.72P/);
  assert.match(literature, /href="\/notes\/r0-72n\.html"/);
  assert.match(literature, /href="\/recap-r0-61-r0-72o\.html"/);
  for (const source of [
    "10.4310/CMS.2024.v22.n6.a10",
    "arxiv.org/abs/2309.15738",
    "10.1002/cpa.21831",
    "arxiv.org/abs/2511.18536",
  ]) {
    assert.ok(literature.includes(source), source);
  }
  assert.match(literature, /D\. Coble and S\. He/);
  assert.doesNotMatch(literature, /A\. Coble and S\. He/);

  assert.deepEqual(
    {
      latest: release.latestCompletedRelease,
      version: release.siteVersion,
      notes: release.publicHtmlNoteCount,
      recap: release.postR060RecapNodeCount,
      next: release.nextRelease,
      gate: release.latestReleaseGate,
      published: release.postR070APublishedReleaseCount,
      sealed: release.postR070AFormalSealedReleaseCount,
      backlog: release.legacyFormalFigureBacklogCount,
    },
    {
      latest: "r072o",
      version: "1.28",
      notes: 165,
      recap: 105,
      next: "r072p",
      gate: "tests/r072o-physical-reinsertion-gate.test.mjs",
      published: 67,
      sealed: 43,
      backlog: 24,
    },
  );

  assert.equal(archive.latestPublishedRelease, "r072o");
  assert.equal(archive.publishedReleaseCount, 67);
  assert.equal(archive.formalSealedReleaseCount, 43);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.equal(archive.publishedReleases.length, 67);
  assert.equal(archive.formalSealedReleases.length, 43);
  assert.equal(archive.legacyFormalFigureBacklog.length, 24);
  assert.equal(archive.publishedReleases.at(-1), "r072o");
  assert.equal(archive.formalSealedReleases.at(-1), "r072o");

  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.28",
    latestRelease: "R0.72O",
    publicHtmlNoteCount: 165,
    publishedDate: "2026-08-27",
  });
});

test("ships synchronized N HTML/PDF, recap PDF, and three public figure assets", async () => {
  const [note, notePdf, recap, recapPdf, home, literature] = await Promise.all([
    readFile(resolve(publicRoot, "notes/r0-72n.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72n.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72n.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72n.pdf")),
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
  ]);

  for (const page of [note, recap]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.27"/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
  for (const page of [home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.28"/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  assert.match(note, /href="\/notes\/r0-72n\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-72n\.html"/);
  assert.match(note, /href="\/recap-r0-61-r0-72n\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-72n\.pdf"/);
  assert.match(home, /href="\/notes\/r0-72n\.pdf"/);
  assert.match(literature, /href="\/notes\/r0-72n\.html"/);

  for (const [label, pdf] of [
    ["note", notePdf],
    ["recap", recapPdf],
  ]) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label + " PDF header");
    assert.ok(pdf.length > 10_000, label + " PDF is unexpectedly small");
  }

  for (const extension of ["pdf", "png", "svg"]) {
    const relative = "/assets/r072n/fig-r072n-dissipative-carrier." + extension;
    const asset = await readFile(
      resolve(
        publicRoot,
        "assets/r072n/fig-r072n-dissipative-carrier." + extension,
      ),
    );
    assert.ok(note.includes(relative), relative);
    assert.ok(asset.length > 1_000, extension);
  }
  assert.ok(recap.includes("/assets/r072n/fig-r072n-dissipative-carrier.pdf"));
  assert.ok(home.includes("/assets/r072n/fig-r072n-dissipative-carrier.pdf"));
});

test("keeps the N table of contents, attribution, and claim boundaries intact", async () => {
  const note = await readFile(resolve(publicRoot, "notes/r0-72n.html"), "utf8");
  const tocStart = note.indexOf('<aside class="toc">');
  const tocEnd = note.indexOf("</aside>", tocStart);
  assert.ok(tocStart >= 0 && tocEnd > tocStart);
  const anchors = [
    ...note.slice(tocStart, tocEnd).matchAll(/href="#([^"]+)"/g),
  ].map((match) => match[1]);

  assert.deepEqual(anchors, [
    "result",
    "chain",
    "moment",
    "action",
    "screen",
    "mapping",
    "cubic",
    "diagnostics",
    "figure",
    "literature",
    "value",
    "next",
    "claims",
    "reproduce",
  ]);
  for (const anchor of anchors) {
    assert.ok(note.includes('id="' + anchor + '"'), anchor);
  }
  for (const token of [
    "action-poor route: DISPROVED FOR THIS LAUNCH",
    "one-carrier sublinear cubic: CLOSED",
    "logarithmic sharpen: OPEN",
    "multi-carrier extension: OPEN",
    "最后一式是我在本站完成的 corollary",
    "不是 Coble–He 原论文中的定理或原句",
    "fixed-geometry proxies",
    "\\(K_{\\rm proxy}=1+D_{\\max}\\)",
    "\\(x_{\\rm proxy}=\\sigma^2\\mathscr A_\\sigma\\)",
    "\\(\\mu=a=1\\)",
    "\\(T/V\\le1\\) 是解析 ceiling",
    "\\(\\sqrt\\sigma\\) 上界是本站从 Coble–He Theorem 1.2 推出的 corollary",
    "\\(k=-2\\)",
    "horizontal diffusion switch \\(=0\\)",
    "固定频带、row-aligned、one-carrier",
    "Clay 千禧年问题仍未解决",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(
    note,
    /\\mathcal C_\{\\rm diss\}\\lesssim[\s\S]*a\^2\\nu\^\{-1\/2\}=a\^2\\sigma\^\{1\/2\}/,
  );
  assert.doesNotMatch(
    note,
    /Coble[–-]He (?:proved|证明).*cubic|logarithmic (?:law|bound): CLOSED/i,
  );
});

test("covers every live Chinese string with the R0.72N bilingual batch", async () => {
  const [source, translations, built] = await Promise.all([
    collectSiteStrings(publicRoot),
    json(resolve(root, "translations/en.json")),
    readFile(resolve(publicRoot, "i18n-en.js"), "utf8"),
  ]);
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(
    source.filter((entry) => !byChinese.has(entry.zh)),
    [],
    "every live Chinese string must have an English translation",
  );

  const batch = translations.filter((entry) => /^r072n\d+$/.test(entry.id));
  assert.ok(batch.length > 0, "R0.72N translation batch is empty");
  assert.deepEqual(
    [...new Set(batch.flatMap((entry) => entry.files))].sort(),
    [
      "literature-review.html",
      "notes/r0-72n.html",
      "recap-r0-61-r0-72n.html",
      "research-review.html",
    ],
  );
  for (const entry of batch) {
    assert.ok(entry.en.trim().length > 0, entry.zh);
    assert.doesNotMatch(entry.en, /[\u3400-\u9fff\uf900-\ufaff]/u);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i);
    assert.deepEqual(
      extractProtectedTokens(entry.en),
      extractProtectedTokens(entry.zh),
      entry.zh,
    );
  }
  for (const chinese of [
    "状态 · R0.72N 定理完成",
    "action-poor 路线在耗散链上失效；",
    "最后一式是我在本站完成的 corollary，不是 Coble–He 原论文中的定理或原句。",
    "R0.72O：回填物理账本并检查多载波稳定性",
  ]) {
    const entry = byChinese.get(chinese);
    assert.ok(entry, chinese);
    assert.ok(entry.en.trim().length > 0, chinese + ": English value");
    assert.ok(built.includes(JSON.stringify(chinese)), chinese + ": built dictionary");
  }
});

test("the deterministic generator advances exactly from M to N", async () => {
  const generator = await readFile(
    resolve(root, "scripts/generate_r072n_release.py"),
    "utf8",
  );
  for (const token of [
    "r0-72m.html",
    "r0-72n.html",
    "recap-r0-61-r0-72m.html",
    "recap-r0-61-r0-72n.html",
    "expected 164 public HTML notes",
    '"recapNodes": 104',
    '"published": 66',
    '"formalSealed": 42',
    '"legacyBacklog": 24',
    '"phases": 28',
    '"next": "R0.72O"',
    "tests/r072n-dissipative-carrier-gate.test.mjs",
  ]) {
    assert.ok(generator.includes(token), token);
  }
});
