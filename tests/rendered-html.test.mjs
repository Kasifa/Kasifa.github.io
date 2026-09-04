import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import test from "node:test";

const siteUrl = new URL("../public/research-review.html", import.meta.url);
const firstNoteUrl = new URL("../public/notes/r0-1.html", import.meta.url);
const secondNoteUrl = new URL("../public/notes/r0-2.html", import.meta.url);
const thirdNoteUrl = new URL("../public/notes/r0-3.html", import.meta.url);
const fourthNoteUrl = new URL("../public/notes/r0-4.html", import.meta.url);
const fifthNoteUrl = new URL("../public/notes/r0-5.html", import.meta.url);
const sixthNoteUrl = new URL("../public/notes/r0-6.html", import.meta.url);
const seventhNoteUrl = new URL("../public/notes/r0-7.html", import.meta.url);
const eighthNoteUrl = new URL("../public/notes/r0-8.html", import.meta.url);
const ninthNoteUrl = new URL("../public/notes/r0-9.html", import.meta.url);
const tenthNoteUrl = new URL("../public/notes/r0-10.html", import.meta.url);
const eleventhNoteUrl = new URL("../public/notes/r0-11.html", import.meta.url);
const twelfthNoteUrl = new URL("../public/notes/r0-12.html", import.meta.url);
const thirteenthNoteUrl = new URL("../public/notes/r0-13.html", import.meta.url);
const fourteenthNoteUrl = new URL("../public/notes/r0-14.html", import.meta.url);
const fifteenthNoteUrl = new URL("../public/notes/r0-15.html", import.meta.url);
const sixteenthNoteUrl = new URL("../public/notes/r0-16.html", import.meta.url);
const seventeenthNoteUrl = new URL("../public/notes/r0-17.html", import.meta.url);
const eighteenthNoteUrl = new URL("../public/notes/r0-18.html", import.meta.url);
const nineteenthNoteUrl = new URL("../public/notes/r0-19.html", import.meta.url);
const twentiethNoteUrl = new URL("../public/notes/r0-20.html", import.meta.url);
const twentyFirstNoteUrl = new URL("../public/notes/r0-21.html", import.meta.url);
const twentySecondNoteUrl = new URL("../public/notes/r0-22.html", import.meta.url);
const twentyThirdNoteUrl = new URL("../public/notes/r0-23.html", import.meta.url);
const twentyFourthNoteUrl = new URL("../public/notes/r0-24.html", import.meta.url);
const twentyFifthNoteUrl = new URL("../public/notes/r0-25.html", import.meta.url);
const twentySixthNoteUrl = new URL("../public/notes/r0-26.html", import.meta.url);
const twentySeventhNoteUrl = new URL("../public/notes/r0-27.html", import.meta.url);
const twentyEighthNoteUrl = new URL("../public/notes/r0-28.html", import.meta.url);
const twentyNinthNoteUrl = new URL("../public/notes/r0-29.html", import.meta.url);
const thirtiethNoteUrl = new URL("../public/notes/r0-30.html", import.meta.url);
const thirtyFirstNoteUrl = new URL("../public/notes/r0-31.html", import.meta.url);
const thirtySecondNoteUrl = new URL("../public/notes/r0-32.html", import.meta.url);
const thirtyThirdNoteUrl = new URL("../public/notes/r0-33.html", import.meta.url);
const thirtyFourthNoteUrl = new URL("../public/notes/r0-34.html", import.meta.url);
const thirtyFifthNoteUrl = new URL("../public/notes/r0-35.html", import.meta.url);
const thirtyFifthPdfUrl = new URL("../public/notes/r0-35.pdf", import.meta.url);
const thirtySixthNoteUrl = new URL("../public/notes/r0-36.html", import.meta.url);
const thirtySixthPdfUrl = new URL("../public/notes/r0-36.pdf", import.meta.url);
const thirtySeventhNoteUrl = new URL("../public/notes/r0-37.html", import.meta.url);
const thirtySeventhPdfUrl = new URL("../public/notes/r0-37.pdf", import.meta.url);
const thirtyEighthNoteUrl = new URL("../public/notes/r0-38.html", import.meta.url);
const thirtyEighthPdfUrl = new URL("../public/notes/r0-38.pdf", import.meta.url);
const thirtyNinthNoteUrl = new URL("../public/notes/r0-39.html", import.meta.url);
const thirtyNinthPdfUrl = new URL("../public/notes/r0-39.pdf", import.meta.url);
const fortiethNoteUrl = new URL("../public/notes/r0-40.html", import.meta.url);
const fortiethPdfUrl = new URL("../public/notes/r0-40.pdf", import.meta.url);
const fortyFirstNoteUrl = new URL("../public/notes/r0-41.html", import.meta.url);
const fortyFirstPdfUrl = new URL("../public/notes/r0-41.pdf", import.meta.url);
const fortySecondNoteUrl = new URL("../public/notes/r0-42.html", import.meta.url);
const fortySecondPdfUrl = new URL("../public/notes/r0-42.pdf", import.meta.url);
const fortyThirdNoteUrl = new URL("../public/notes/r0-43.html", import.meta.url);
const fortyThirdPdfUrl = new URL("../public/notes/r0-43.pdf", import.meta.url);
const fortyFourthNoteUrl = new URL("../public/notes/r0-44.html", import.meta.url);
const fortyFourthPdfUrl = new URL("../public/notes/r0-44.pdf", import.meta.url);
const fortyFifthNoteUrl = new URL("../public/notes/r0-45.html", import.meta.url);
const fortyFifthPdfUrl = new URL("../public/notes/r0-45.pdf", import.meta.url);
const fortySixthNoteUrl = new URL("../public/notes/r0-46.html", import.meta.url);
const fortySixthPdfUrl = new URL("../public/notes/r0-46.pdf", import.meta.url);
const fortySeventhNoteUrl = new URL("../public/notes/r0-47.html", import.meta.url);
const fortySeventhPdfUrl = new URL("../public/notes/r0-47.pdf", import.meta.url);
const fortyEighthNoteUrl = new URL("../public/notes/r0-48.html", import.meta.url);
const fortyEighthPdfUrl = new URL("../public/notes/r0-48.pdf", import.meta.url);
const fortyNinthNoteUrl = new URL("../public/notes/r0-49.html", import.meta.url);
const fortyNinthPdfUrl = new URL("../public/notes/r0-49.pdf", import.meta.url);
const fiftiethNoteUrl = new URL("../public/notes/r0-50.html", import.meta.url);
const fiftiethPdfUrl = new URL("../public/notes/r0-50.pdf", import.meta.url);
const fiftyFirstNoteUrl = new URL("../public/notes/r0-51.html", import.meta.url);
const fiftyFirstPdfUrl = new URL("../public/notes/r0-51.pdf", import.meta.url);
const fiftySecondNoteUrl = new URL("../public/notes/r0-52.html", import.meta.url);
const fiftySecondPdfUrl = new URL("../public/notes/r0-52.pdf", import.meta.url);
const fiftyThirdNoteUrl = new URL("../public/notes/r0-53.html", import.meta.url);
const fiftyThirdPdfUrl = new URL("../public/notes/r0-53.pdf", import.meta.url);
const fiftyFourthNoteUrl = new URL("../public/notes/r0-54.html", import.meta.url);
const fiftyFourthPdfUrl = new URL("../public/notes/r0-54.pdf", import.meta.url);
const fiftyFifthNoteUrl = new URL("../public/notes/r0-55.html", import.meta.url);
const fiftyFifthPdfUrl = new URL("../public/notes/r0-55.pdf", import.meta.url);
const fiftySixthNoteUrl = new URL("../public/notes/r0-56.html", import.meta.url);
const fiftySixthPdfUrl = new URL("../public/notes/r0-56.pdf", import.meta.url);
const fiftySeventhNoteUrl = new URL("../public/notes/r0-57.html", import.meta.url);
const fiftySeventhPdfUrl = new URL("../public/notes/r0-57.pdf", import.meta.url);
const fiftySeventhFigureSvgUrl = new URL(
  "../public/figures/r0-57-coherent-fixed-output.svg",
  import.meta.url,
);
const fiftySeventhFigurePngUrl = new URL(
  "../public/figures/r0-57-coherent-fixed-output.png",
  import.meta.url,
);
const fiftyEighthNoteUrl = new URL("../public/notes/r0-58.html", import.meta.url);
const fiftyEighthPdfUrl = new URL("../public/notes/r0-58.pdf", import.meta.url);
const fiftyEighthFigureSvgUrl = new URL(
  "../public/figures/r0-58-duhamel-critical-saturation.svg",
  import.meta.url,
);
const fiftyEighthFigurePngUrl = new URL(
  "../public/figures/r0-58-duhamel-critical-saturation.png",
  import.meta.url,
);
const fiftyNinthNoteUrl = new URL("../public/notes/r0-59.html", import.meta.url);
const fiftyNinthPdfUrl = new URL("../public/notes/r0-59.pdf", import.meta.url);
const fiftyNinthFigureSvgUrl = new URL(
  "../public/figures/r0-59-multi-output-critical-saturation.svg",
  import.meta.url,
);
const fiftyNinthFigurePngUrl = new URL(
  "../public/figures/r0-59-multi-output-critical-saturation.png",
  import.meta.url,
);
const sixtiethNoteUrl = new URL("../public/notes/r0-60.html", import.meta.url);
const sixtiethPdfUrl = new URL("../public/notes/r0-60.pdf", import.meta.url);
const sixtiethFigureSvgUrl = new URL(
  "../public/figures/r0-60-invariant-shear-picard.svg",
  import.meta.url,
);
const sixtiethFigurePngUrl = new URL(
  "../public/figures/r0-60-invariant-shear-picard.png",
  import.meta.url,
);
const sixtyFirstNoteUrl = new URL("../public/notes/r0-61.html", import.meta.url);
const sixtyFirstPdfUrl = new URL("../public/notes/r0-61.pdf", import.meta.url);
const sixtyFirstFigureSvgUrl = new URL(
  "../public/figures/r0-61-quartic-target.svg",
  import.meta.url,
);
const sixtyFirstFigurePngUrl = new URL(
  "../public/figures/r0-61-quartic-target.png",
  import.meta.url,
);
const sixtyFirstFigurePdfUrl = new URL(
  "../public/figures/r0-61-quartic-target.pdf",
  import.meta.url,
);
const sixtySecondNoteUrl = new URL("../public/notes/r0-62.html", import.meta.url);
const sixtySecondPdfUrl = new URL("../public/notes/r0-62.pdf", import.meta.url);
const sixtySecondFigureSvgUrl = new URL(
  "../public/figures/r0-62-quartic-correlation.svg",
  import.meta.url,
);
const sixtySecondFigurePngUrl = new URL(
  "../public/figures/r0-62-quartic-correlation.png",
  import.meta.url,
);
const sixtySecondFigurePdfUrl = new URL(
  "../public/figures/r0-62-quartic-correlation.pdf",
  import.meta.url,
);
const sixtyThirdNoteUrl = new URL("../public/notes/r0-63.html", import.meta.url);
const sixtyThirdFigureSvgUrl = new URL(
  "../public/figures/r0-63-time-layer-transfer.svg",
  import.meta.url,
);
const sixtyThirdFigurePngUrl = new URL(
  "../public/figures/r0-63-time-layer-transfer.png",
  import.meta.url,
);
const sixtyThirdFigurePdfUrl = new URL(
  "../public/figures/r0-63-time-layer-transfer.pdf",
  import.meta.url,
);
const sixtyFourthNoteUrl = new URL("../public/notes/r0-64.html", import.meta.url);
const sixtyFourthFigureSvgUrl = new URL(
  "../public/figures/r0-64-supercritical-cycle.svg",
  import.meta.url,
);
const sixtyFourthFigurePngUrl = new URL(
  "../public/figures/r0-64-supercritical-cycle.png",
  import.meta.url,
);
const sixtyFourthFigurePdfUrl = new URL(
  "../public/figures/r0-64-supercritical-cycle.pdf",
  import.meta.url,
);
const sixtyFifthNoteUrl = new URL("../public/notes/r0-65.html", import.meta.url);
const sixtyFifthFigureSvgUrl = new URL(
  "../public/figures/r0-65-weighted-cycle.svg",
  import.meta.url,
);
const sixtyFifthFigurePngUrl = new URL(
  "../public/figures/r0-65-weighted-cycle.png",
  import.meta.url,
);
const sixtyFifthFigurePdfUrl = new URL(
  "../public/figures/r0-65-weighted-cycle.pdf",
  import.meta.url,
);
const sixtySixthNoteUrl = new URL("../public/notes/r0-66.html", import.meta.url);
const sixtySixthFigureSvgUrl = new URL(
  "../public/figures/r0-66-spectral-projection.svg",
  import.meta.url,
);
const sixtySixthFigurePngUrl = new URL(
  "../public/figures/r0-66-spectral-projection.png",
  import.meta.url,
);
const sixtySixthFigurePdfUrl = new URL(
  "../public/figures/r0-66-spectral-projection.pdf",
  import.meta.url,
);

test("ships the complete Chinese research review as static HTML", async () => {
  const html = await readFile(siteUrl, "utf8");

  assert.match(
    html,
    /<html lang="zh-CN" data-site-version="\d+\.\d+">/,
  );
  assert.match(html, /三维 Navier–Stokes 全局正则性问题/);
  assert.doesNotMatch(html, /三维 Navier–Stokes 存在性与光滑性问题/);
  assert.doesNotMatch(html, /Navier–Stokes 开放研究日志/);
  assert.match(html, /这个问题要求证明什么/);
  assert.match(html, /目前已经知道什么/);
  assert.match(html, /接下来的工作计划/);
  assert.match(html, /当前研究进展/);
  assert.doesNotMatch(html, /08 \/ Selected sources|id="references"/);
  assert.doesNotMatch(html, /id="publish"|href="#publish"|Open publication/);
  assert.doesNotMatch(html, /codex-preview|SkeletonPreview|react-loading-skeleton/);
});

test("maps the complete published route as a branching tree", async () => {
  const [home, publicNoteFiles] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readdir(new URL("../public/notes/", import.meta.url)),
  ]);
  const start = home.indexOf('<section class="route-overview"');
  const end = home.indexOf('<div class="page-shell">', start);

  assert.ok(start >= 0, "research route map is missing");
  assert.ok(end > start, "research route map does not end before the main article");

  const route = home.slice(start, end);
  const sequential = Array.from(
    { length: 66 },
    (_, index) => `/notes/r0-${index + 1}.html`,
  );
  const completedTail = publicNoteFiles
    .map((file) => file.match(/^r0-(\d{2}[a-z])\.html$/)?.[1])
    .filter(Boolean)
    .map((release) => `r0${release}`)
    .filter((release) => release.localeCompare("r070a") >= 0)
    .sort();
  const later = [
    "/notes/r0-67.html",
    "/notes/r0-67b.html",
    "/notes/r0-67c1.html",
    "/notes/r0-67c2.html",
    "/notes/r0-68a.html",
    "/notes/r0-68b1.html",
    "/notes/r0-68b2.html",
    "/notes/r0-68b2de.html",
    "/notes/r0-68b2fgh.html",
    ...Array.from(
      { length: 21 },
      (_, index) => `/notes/r0-69${String.fromCharCode(97 + index)}.html`,
    ),
    "/notes/r0-69v.html",
    "/notes/r0-69w.html",
    ...completedTail.map((release) =>
      release.replace(/^r0(\d{2})([a-z])$/, "/notes/r0-$1$2.html"),
    ),
  ];
  const expected = [...sequential, ...later];
  const actual = [...route.matchAll(/href="(\/notes\/r0-[^"]+\.html)"/g)].map(
    (match) => match[1],
  );

  assert.deepEqual(actual, expected);
  assert.match(route, /class="route-tree"/);
  assert.match(route, /class="tree-root"/);
  assert.equal((route.match(/class="tree-row/g) ?? []).length, 6);
  assert.equal((route.match(/class="tree-branch/g) ?? []).length, 5);
  assert.equal(
    (route.match(/<details class="tree-notes"[^>]*>/g) ?? []).length,
    7,
  );
  assert.doesNotMatch(route, /class="route-topology"|class="route-stage"/);
  assert.match(route, /R0\.1–R0\.8/);
  assert.match(route, /R0\.61–R0\.66/);
  assert.match(route, /R0\.67A–R0\.68B-2h/);
  assert.match(route, /R0\.69B–R0\.69F/);
  assert.match(route, /R0\.69G–R0\.69O/);
  const latestMatch = completedTail.at(-1).match(/^r0(\d{2})([a-z])$/);
  const latestCode = `R0.${latestMatch[1]}${latestMatch[2].toUpperCase()}`;
  const nextCode =
    latestMatch[2] === "z"
      ? `R0.${String(Number(latestMatch[1]) + 1).padStart(2, "0")}A`
      : `R0.${latestMatch[1]}${String.fromCharCode(
          latestMatch[2].charCodeAt(0) + 1,
        ).toUpperCase()}`;
  assert.match(route, new RegExp(`R0\\.69P–${latestCode.replace(".", "\\.")}`));
  const detailsBlocks = [
    ...route.matchAll(
      /<details class="tree-notes"[^>]*>([\s\S]*?)<\/details>/g,
    ),
  ];
  const currentDetails = detailsBlocks.at(-1)?.[1] ?? "";
  const currentRouteCount = (
    currentDetails.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []
  ).length;
  assert.ok(currentRouteCount > 0);
  assert.ok(route.includes(`展开 ${currentRouteCount} 篇公开笔记`));
  assert.ok(route.includes(["R0.75F", "R0.75G", "R0.75H", "R0.75I", "R0.75J", "R0.75K", "R0.75L", "R0.75M", "R0.75N", "R0.75O", "R0.75P", "R0.75Q", "R0.75R"].includes(latestCode) ? "NEXT · NOT AUTHORIZED" : `NEXT · ${nextCode}`));
  assert.match(route, /路线回返/);
  assert.match(route, /当前主线/);
  assert.doesNotMatch(route, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);

  await Promise.all(
    expected.map((path) =>
      readFile(new URL(`../public${path}`, import.meta.url), "utf8"),
    ),
  );
});

test("publishes and links the Leray polarization-channel theorem and normal obstruction", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftySixthNoteUrl, "utf8"),
    readFile(fiftySixthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-56\.html"/);
  assert.match(home, /href="\/notes\/r0-56\.pdf"/);
  assert.ok(home.includes("R0.56 已完成："));
  assert.ok(home.includes("R0.57 已完成："));
  assert.match(note, /研究笔记 R0\.56/);
  assert.match(note, /href="\/notes\/r0-56\.pdf"/);
  assert.match(note, /精确两通道结构已证明/);
  assert.ok(note.includes("g_N=\\frac{|p\\times q|}{|p||k|}"));
  assert.ok(note.includes("g_T\\le(1+\\rho)/2&lt;1"));
  assert.ok(note.includes("\\langle g_N\\rangle=\\pi/4"));
  assert.match(note, /1,764,912 个/);
  assert.match(note, /400,000 个/);
  assert.match(note, /21 项检查全部通过/);
  assert.match(
    note,
    /ff0b68729476dfc2d8e53d1483c7a29b383914a5dd8ba761502c57534858fafe/,
  );
  assert.match(note, /r0-56-leray-polarization-channels\.svg/);
  assert.match(note, /R0\.57 的验收标准不是观察到数值抵消/);
  assert.match(note, /更接近一条严谨的结构性引理/);
  assert.match(note, /不能声称已经解决、接近解决或显著推进/);
  assert.ok(note.includes("我在每个非共线 Fourier 三元组上建立"));
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(
    note,
    /\(lambd|\(alph|\(bet|\(omeg|[^\u005c]qquad|[^\u005c]times10/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes the sharp R0.57 fixed-output obstruction with reproducible assets", async () => {
  const [home, note, pdf, figureSvg, figurePng] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftySeventhNoteUrl, "utf8"),
    readFile(fiftySeventhPdfUrl),
    readFile(fiftySeventhFigureSvgUrl, "utf8"),
    readFile(fiftySeventhFigurePngUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-57\.html"/);
  assert.match(home, /href="\/notes\/r0-57\.pdf"/);
  assert.ok(home.includes("R0.57 已完成："));
  assert.ok(home.includes("R0.58 已完成："));
  assert.match(note, /研究笔记 R0\.57/);
  assert.match(note, /全指标相干反例已证明/);
  assert.match(note, /20 项检查全通过/);
  assert.match(note, /正式频率对：200,000 个/);
  assert.match(note, /全指标实例：1,000,000 个/);
  assert.ok(note.includes("|\\mathfrak B_k(U,V)|"));
  assert.ok(note.includes("C(1/L,\\arctan(1/L))\\ge1"));
  assert.match(note, /瞬时固定输出比值仍恒等于一/);
  assert.match(note, /交换项逐个为零/);
  assert.match(note, /r0-57-coherent-fixed-output\.svg/);
  assert.match(note, /r0-57-coherent-fixed-output\.png/);
  assert.match(note, /下一步直接计算时间积分 Duhamel 算子的精确核/);
  assert.match(
    note,
    /84bdf17eea9967a3ad9e4150b0b9ef2457bfcc2f984b4b437dff588d2df413c8/,
  );
  assert.ok(note.includes("我把 R0.56 留下的法向通道按固定输出频率求和"));
  assert.match(note, /不能声称已经解决、接近解决或显著推进/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.match(figureSvg, /Coherent fixed-output saturation/);
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
});

test("publishes the exact R0.58 Duhamel denominator and critical saturation", async () => {
  const [home, note, pdf, figureSvg, figurePng] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftyEighthNoteUrl, "utf8"),
    readFile(fiftyEighthPdfUrl),
    readFile(fiftyEighthFigureSvgUrl, "utf8"),
    readFile(fiftyEighthFigurePngUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-58\.html"/);
  assert.match(home, /href="\/notes\/r0-58\.pdf"/);
  assert.ok(home.includes("R0.58 已完成："));
  assert.ok(home.includes("R0.59 已完成："));
  assert.match(note, /研究笔记 R0\.58/);
  assert.match(note, /全指标 Duhamel 定理已证明/);
  assert.match(note, /24 项检查全通过/);
  assert.match(note, /精确频率实例：8,390,656 个/);
  assert.match(note, /最大符号长度：4,194,304/);
  assert.ok(note.includes("d_L(t;c)=e^{-t}\\sum_{N=L}^{2L-1}"));
  assert.ok(note.includes("\\frac1{32L}\\le d_L(t_L)\\le\\frac1{2L}"));
  assert.ok(note.includes("\\Theta(L^{-2})"));
  assert.ok(note.includes("\\Theta(L^{-1})"));
  assert.ok(note.includes("\\Theta(L^{-3})"));
  assert.ok(note.includes("(2+\\sqrt2)\\sqrt L"));
  assert.match(note, /临界饱和定理，不是范数膨胀/);
  assert.match(note, /更高 Picard 余项/);
  assert.match(note, /r0-58-duhamel-critical-saturation\.svg/);
  assert.match(note, /r0-58-duhamel-critical-saturation\.png/);
  assert.match(
    note,
    /c04d2f00dd90ad16e885af573f00cde5f2ec3c3d499fdb5909952f4cec8512b2/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.match(
    figureSvg,
    /Exact Duhamel denominator: shell gain versus critical saturation/,
  );
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
});

test("publishes the R0.59 growing multi-output critical-saturation theorem", async () => {
  const [home, note, pdf, figureSvg, figurePng] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftyNinthNoteUrl, "utf8"),
    readFile(fiftyNinthPdfUrl),
    readFile(fiftyNinthFigureSvgUrl, "utf8"),
    readFile(fiftyNinthFigurePngUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-59\.html"/);
  assert.match(home, /href="\/notes\/r0-59\.pdf"/);
  assert.ok(home.includes("R0.59 已完成："));
  assert.ok(home.includes("R0.60 已完成："));
  assert.match(note, /研究笔记 R0\.59/);
  assert.match(note, /全指标多输出定理已证明/);
  assert.match(note, /24 项检查全通过/);
  assert.match(note, /频率实例：4,190,209 个/);
  assert.match(note, /交叉配对：29,822,521 个/);
  assert.match(note, /张量前缀：16,760,836 个/);
  assert.ok(note.includes("H=4LM"));
  assert.ok(note.includes("H/M=4L"));
  assert.ok(note.includes("U\\cdot\\nabla U=V\\cdot\\nabla V=V\\cdot\\nabla U=0"));
  assert.ok(note.includes("d_m(t)=m e^{-m^2t}\\sum_{n=0}^{L-1}"));
  assert.ok(note.includes("\\frac{2mL}{25H^2}&lt;d_m(t_H)"));
  assert.ok(note.includes("C_T=(1+\\sqrt2)(2+\\sqrt2)"));
  assert.ok(note.includes("线性项与第一非线性项在 \\(L^2\\) 中精确正交"));
  assert.match(note, /下一步直接检验三阶共振与高阶 Picard 余项/);
  assert.match(note, /r0-59-multi-output-critical-saturation\.svg/);
  assert.match(note, /r0-59-multi-output-critical-saturation\.png/);
  assert.match(
    note,
    /88774c0d5647f46700ed499409754f4207fdcef5a0193e5a337e7887eb3c6dce/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /\(Pi_0\)|\(mathcal|\(dot B|\(sqrt\{/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.match(
    figureSvg,
    /One flattened high shell sustains a growing coherent output set/,
  );
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
});

test("publishes the R0.60 invariant-shear reduction and cubic target gap", async () => {
  const [home, note, pdf, figureSvg, figurePng] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixtiethNoteUrl, "utf8"),
    readFile(sixtiethPdfUrl),
    readFile(sixtiethFigureSvgUrl, "utf8"),
    readFile(sixtiethFigurePngUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-60\.html"/);
  assert.match(home, /href="\/notes\/r0-60\.pdf"/);
  assert.ok(home.includes("R0.60 已完成："));
  assert.ok(home.includes("R0.61 已完成："));
  assert.ok(home.includes("R0.62 已完成："));
  assert.ok(home.includes("R0.63 已完成："));
  assert.ok(home.includes("R0.64 已完成："));
  assert.ok(home.includes("R0.65 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));

  assert.match(note, /研究笔记 R0\.60/);
  assert.match(note, /不变约化与支撑定理已证明/);
  assert.match(note, /24 项检查全通过/);
  assert.match(note, /支撑状态转移：32,771,750 次/);
  assert.match(note, /能量卷积配对：323,216 对/);
  assert.match(note, /公式覆盖载频：67,092,481 个/);
  assert.ok(note.includes("u=(0,F(x_1,t),G(x_1,x_2,t))"));
  assert.ok(note.includes("(\\partial_t-\\Delta_{12})G_n"));
  assert.ok(note.includes("|\\xi_1|\\ge2H-(H+D)=H-D=3N+1>\\frac34H"));
  assert.ok(note.includes("\\Pi_0G_n=0\\quad\\text{for }n\\in\\{3,5,7,9\\}"));
  assert.ok(note.includes("-(H+N-5)+5(H+N-1)-5H=0"));
  assert.ok(note.includes("-Q+Q+P-P=0"));
  assert.match(note, /下一步精确计算四次目标系数，而不是继续搜索三次共振/);
  assert.match(note, /r0-60-invariant-shear-picard\.svg/);
  assert.match(note, /r0-60-invariant-shear-picard\.png/);
  assert.match(
    note,
    /681fd7c5e2a6aef645f4bbff8e63733e62a002c608cb138856a17747489263b2/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|杀死错误想法|突破/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.match(
    figureSvg,
    /Support thresholds in the invariant shear Picard chain/,
  );
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
});

test("publishes the R0.61 quartic target formula and finite scan boundary", async () => {
  const [home, note, pdf, figureSvg, figurePng, figurePdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixtyFirstNoteUrl, "utf8"),
    readFile(sixtyFirstPdfUrl),
    readFile(sixtyFirstFigureSvgUrl, "utf8"),
    readFile(sixtyFirstFigurePngUrl),
    readFile(sixtyFirstFigurePdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-61\.html"/);
  assert.match(home, /href="\/notes\/r0-61\.pdf"/);
  assert.ok(home.includes("R0.61 已完成："));
  assert.ok(home.includes("R0.62 已完成："));
  assert.ok(home.includes("R0.63 已完成："));
  assert.ok(home.includes("R0.64 已完成："));
  assert.ok(home.includes("R0.65 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));

  assert.match(note, /研究笔记 R0\.61/);
  assert.match(note, /10 项计算检查全通过/);
  assert.match(note, /不同三元组：461 个/);
  assert.match(note, /有序路径：7,494,536,238 条/);
  assert.ok(note.includes("A+B-C=Q"));
  assert.ok(note.includes("(A,B,-C)"));
  assert.ok(note.includes("-[\\alpha_0,\\alpha_1,\\alpha_2,\\alpha_3]e^{-Tx}>0"));
  assert.ok(note.includes("-\\frac{\\varepsilon^2}{L^2}R_{L,M,m}"));
  assert.ok(note.includes("0.0013286562612066827"));
  assert.ok(note.includes("0.001328656261206690024552778522639"));
  assert.match(note, /一致上界还没有证明/);
  assert.match(note, /一致界尚未证明/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-61-quartic-target\.svg/);
  assert.match(note, /r0-61-quartic-target\.png/);
  assert.match(note, /r0-61-quartic-target\.pdf/);
  assert.match(note, /895543f44b3c83c777014eefc9594f95b3b9d829/);
  assert.match(note, /044dea434aba9448c2bfcf1f999992f9b96e3e5b/);
  assert.match(note, /737a9e5645c3f4b07b0ea695f0c216eb1c14808f/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|杀死错误想法|突破/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.match(figureSvg, /Finite quartic target scan in the invariant shear chain/);
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(figurePdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes the R0.62 three-carry reduction and all-index square-root bound", async () => {
  const [home, note, pdf, figureSvg, figurePng, figurePdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixtySecondNoteUrl, "utf8"),
    readFile(sixtySecondPdfUrl),
    readFile(sixtySecondFigureSvgUrl, "utf8"),
    readFile(sixtySecondFigurePngUrl),
    readFile(sixtySecondFigurePdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-62\.html"/);
  assert.match(home, /href="\/notes\/r0-62\.pdf"/);
  assert.ok(home.includes("R0.62 已完成："));
  assert.ok(home.includes("R0.63 已完成："));
  assert.ok(home.includes("R0.64 已完成："));
  assert.ok(home.includes("R0.65 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));

  assert.match(note, /研究笔记 R0\.62/);
  assert.match(note, /4 项整数检查全通过/);
  assert.match(note, /新增完整目标：3,584 个/);
  assert.match(note, /累计不同三元组：4,042 个/);
  assert.match(note, /累计有序路径：27,082,065,198 条/);
  assert.ok(note.includes("k\\in\\{-1,0,1\\}"));
  assert.ok(
    note.includes("\\sum_{k=-1}^{1}I_{L,k}O_{M,m-1,k}"),
  );
  assert.ok(
    note.includes("&lt;7.8343\\Bigl(\\frac mM\\Bigr)^2\\sqrt M"),
  );
  assert.ok(note.includes("0.0012127996801718404"));
  assert.ok(note.includes("0.0011457637853978923"));
  assert.match(note, /一致界还差一次热核消去/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-62-quartic-correlation\.svg/);
  assert.match(note, /r0-62-quartic-correlation\.png/);
  assert.match(note, /r0-62-quartic-correlation\.pdf/);
  assert.match(note, /f7159fe6e089af6207c18d6aee3ea081a2b8508f/);
  assert.match(note, /db6203643c5aa371bfa50af6f62128db60f5219b/);
  assert.match(note, /be7eb1a0a8719aea2f9d74299357a1a6fc959b17/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|杀死错误想法|突破/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.match(
    figureSvg,
    /Heat-weighted quartic profiles and the unweighted correlation gap/,
  );
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(figurePdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes the R0.63 time-layer factorization and lifted transfer boundary", async () => {
  const [home, note, figureSvg, figurePng, figurePdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixtyThirdNoteUrl, "utf8"),
    readFile(sixtyThirdFigureSvgUrl, "utf8"),
    readFile(sixtyThirdFigurePngUrl),
    readFile(sixtyThirdFigurePdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-63\.html"/);
  assert.ok(home.includes("R0.63 已完成："));
  assert.ok(home.includes("R0.64 已完成："));
  assert.ok(home.includes("R0.65 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));

  assert.match(note, /研究笔记 R0\.63/);
  assert.match(note, /4 项审计检查全通过/);
  assert.match(note, /时间层比较：27 项/);
  assert.match(note, /整数递推：10 层/);
  assert.match(note, /28,977,859,974 条路径/);
  assert.ok(note.includes("S_{4,m}=\\int_{\\Delta_T}"));
  assert.ok(note.includes("C_{n+1}^{\\boldsymbol\\sigma}(q)"));
  assert.ok(
    note.includes(
      "(-1)^{\\boldsymbol\\sigma\\cdot\\boldsymbol\\varepsilon}",
    ),
  );
  assert.match(note, /十六态才闭合目标/);
  assert.ok(note.includes("0.0190323022"));
  assert.ok(note.includes("5.06\\times10^4"));
  assert.ok(note.includes("没有证明 \\(|S_{4,m}|\\le CL^2M\\)"));
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-63-time-layer-transfer\.svg/);
  assert.match(note, /r0-63-time-layer-transfer\.png/);
  assert.match(note, /r0-63-time-layer-transfer\.pdf/);
  assert.match(note, /54898a2ba78e48ac075f6613ae6af5d77ce4f28d/);
  assert.match(note, /89de4b0/);
  assert.match(note, /f77ff9e/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|杀死错误想法|突破/);
  assert.match(
    figureSvg,
    /The quartic transfer closes only after a lifted state system/,
  );
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(figurePdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes the R0.64 exact reachable supercritical cycle", async () => {
  const [home, note, figureSvg, figurePng, figurePdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixtyFourthNoteUrl, "utf8"),
    readFile(sixtyFourthFigureSvgUrl, "utf8"),
    readFile(sixtyFourthFigurePngUrl),
    readFile(sixtyFourthFigurePdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-64\.html"/);
  assert.ok(home.includes("R0.64 已完成："));
  assert.ok(home.includes("R0.65 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));

  assert.match(note, /研究笔记 R0\.64/);
  assert.match(note, /9 项审计检查全通过/);
  assert.match(note, /状态维数：48/);
  assert.match(note, /直接卷积：10 层/);
  assert.ok(note.includes("x^{42}(x-16)^2"));
  assert.ok(note.includes("\\lambda=25.1515893341\\ldots"));
  assert.ok(note.includes("\\rho(W)\\le16"));
  assert.ok(note.includes("q_r=2\\frac{16^r-1}{15}"));
  assert.ok(note.includes("\\log_{16}\\lambda=1.1631444155\\ldots>1"));
  assert.match(note, /逐层公共范数/);
  assert.match(note, /没有证明或否定/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-64-supercritical-cycle\.svg/);
  assert.match(note, /r0-64-supercritical-cycle\.png/);
  assert.match(note, /r0-64-supercritical-cycle\.pdf/);
  assert.match(note, /245e53c18100ac05b4143571d1160d4bf6339c20/);
  assert.match(note, /d854e72d4348cefae6294a03d874058e0d7d9832/);
  assert.match(note, /8e22415/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|杀死错误想法|突破/);
  assert.match(
    figureSvg,
    /A zero-time digit cycle exceeds the factor-two threshold/,
  );
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(figurePdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes the R0.65 exact-moment heat-weighted cycle enclosures", async () => {
  const [home, note, figureSvg, figurePng, figurePdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixtyFifthNoteUrl, "utf8"),
    readFile(sixtyFifthFigureSvgUrl, "utf8"),
    readFile(sixtyFifthFigurePngUrl),
    readFile(sixtyFifthFigurePdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-65\.html"/);
  assert.ok(home.includes("R0.65 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));

  assert.match(note, /研究笔记 R0\.65/);
  assert.match(note, /11 项审计检查全通过/);
  assert.match(note, /最高总次数：96/);
  assert.ok(note.includes("1\\le r\\le24"));
  assert.ok(note.includes("S_r<0\\ (14\\le r\\le24)"));
  assert.ok(note.includes("\\frac{|S_r|}{|S_{r-1}|}>16"));
  assert.ok(note.includes("25.29<\\frac{|S_{24}|}{|S_{23}|}<25.30"));
  assert.ok(note.includes("T=\\log2/2=\\operatorname{atanh}(1/3)"));
  assert.ok(note.includes("2\\times10^{-12}"));
  assert.match(note, /有限个尺度无论多大/);
  assert.ok(note.includes("没有证明 \\(|S_r|/M_r\\) 无界"));
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-65-weighted-cycle\.svg/);
  assert.match(note, /r0-65-weighted-cycle\.png/);
  assert.match(note, /r0-65-weighted-cycle\.pdf/);
  assert.match(note, /22044d1d0fd530f2d50f4a541978aa7ae118da56/);
  assert.match(note, /8e2a6eb43bf3536fb4d66d4f72047a9cbfc7cf8d/);
  assert.match(note, /8e2660c871453a4cbd6e60464d6d7fb0d26c6ce8/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|杀死错误想法|突破/);
  assert.match(
    figureSvg,
    /Heat-weighted periodic target through 24 four-bit cycles/,
  );
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(figurePdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes the R0.66 nonzero dominant spectral projection", async () => {
  const [home, note, figureSvg, figurePng, figurePdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixtySixthNoteUrl, "utf8"),
    readFile(sixtySixthFigureSvgUrl, "utf8"),
    readFile(sixtySixthFigurePngUrl),
    readFile(sixtySixthFigurePdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-66\.html"/);
  assert.ok(home.includes("R0.66 已完成："));
  assert.ok(home.includes("下一步 R0.68B-2c："));

  assert.match(note, /研究笔记 R0\.66/);
  assert.match(note, /26 项正式检查全通过/);
  assert.match(note, /仿射分支：12,288 条/);
  assert.ok(note.includes("r_0=100"));
  assert.ok(note.includes("S_r=C_*\\lambda^r+O(r16^r)"));
  assert.ok(note.includes("25.1515893341015&lt;\\lambda&lt;25.1515893341016"));
  assert.ok(note.includes("C_*&lt;-2\\times10^{-5}"));
  assert.ok(note.includes("\\frac{|S_r|}{M_r}\\longrightarrow\\infty"));
  assert.ok(note.includes("Aw=256w"));
  assert.ok(note.includes("\\|\\mathcal P\\zeta\\|_{KR,w}"));
  assert.ok(note.includes("总误差与零点的距离相差超过 \\(255\\) 倍"));
  assert.match(note, /下一步计算首个六次反馈/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-66-spectral-projection\.svg/);
  assert.match(note, /r0-66-spectral-projection\.png/);
  assert.match(note, /r0-66-spectral-projection\.pdf/);
  assert.match(note, /0dc5a9b3e0bef25a08fe7c882bff2cb7e38448a0/);
  assert.match(note, /76e98d31ebb32d125902a443eaf12c2d3a9fc89b/);
  assert.match(note, /e1cf47fe92e259160184cb147d32c090c94c36c2/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|杀死错误想法|突破/);
  assert.match(
    figureSvg,
    /Dominant heat-weighted spectral coefficient is strictly negative/,
  );
  assert.equal(figurePng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(figurePdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("keeps all in-page navigation targets resolvable", async () => {
  const html = await readFile(siteUrl, "utf8");
  const targets = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const internalLinks = [
    ...html.matchAll(/\shref="#([^"]+)"/g),
  ].map((match) => match[1]);

  assert.ok(internalLinks.length >= 10);
  for (const target of internalLinks) {
    assert.ok(targets.has(target), `Missing in-page target: #${target}`);
  }
});

test("labels the unresolved and preprint status explicitly", async () => {
  const html = await readFile(siteUrl, "utf8");

  assert.match(html, /尚未解决/);
  assert.match(html, /预印本主张/);
  assert.match(html, /不能等同于已经过同行评议和独立复核的定理/);
  assert.match(html, /https:\/\/www\.claymath\.org\/wp-content/);
  assert.match(html, /https:\/\/arxiv\.org\/abs\/2509\.25116/);
});

test("publishes and links the first auditable research note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(firstNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-1\.html"/);
  assert.match(note, /研究笔记 R0\.1/);
  assert.match(note, /Leray 投影/);
  assert.match(note, /\\dot H\^\{1\/2\}/);
  assert.match(note, /\(T_k,T_p,T_q\)=\(1,-4,3\)/);
  assert.match(note, /不是新定理/);
});

test("publishes and links the dyadic-helical locality audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(secondNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-2\.html"/);
  assert.match(note, /研究笔记 R0\.2/);
  assert.match(note, /2\^{-2M\}/);
  assert.match(note, /high–high→low/);
  assert.match(note, /同号高频螺旋/);
  assert.match(note, /异号高频螺旋/);
  assert.match(note, /近对角区仍然没有小因子/);
  assert.match(note, /不是新的定理/);
});

test("publishes and links the exact near-diagonal helical-kernel audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirdNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-3\.html"/);
  assert.match(note, /研究笔记 R0\.3/);
  assert.match(note, /\\mathcal C_s=\|g_\{kpq\}W_s\|/);
  assert.match(note, /\\sqrt\{15\}\/16/);
  assert.match(note, /0\.6354564734866010/);
  assert.match(note, /同号类有精确抵消/);
  assert.match(note, /不存在一个仅由单三元组几何产生/);
  assert.match(note, /不是新定理/);
});

test("publishes and links the dense near-diagonal packet argument", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fourthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-4\.html"/);
  assert.match(note, /研究笔记 R0\.4/);
  assert.match(note, /\\widehat u_N\(k\)=N\^\{-3\/2\}a\(k\/N\)/);
  assert.match(note, /\\#\\operatorname\{supp\}\\widehat u_N\\asymp N\^3/);
  assert.match(note, /六维 Riemann 和/);
  assert.match(note, /不存在只依赖高频尺度/);
  assert.match(note, /动力学可持续性/);
  assert.match(note, /不是奇性构造/);
});

test("publishes and links the short-time critical-packet dynamics audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fifthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-5\.html"/);
  assert.match(note, /研究笔记 R0\.5/);
  assert.match(note, /\\tau=N\^2t/);
  assert.match(note, /热流同号引理/);
  assert.match(note, /Fourier–Galerkin/);
  assert.match(note, /83\.72%/);
  assert.match(note, /时间步减半/);
  assert.match(note, /不是 PDE 证明/);
});

test("publishes and links the fixed-injection leakage optimization", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-6\.html"/);
  assert.match(note, /研究笔记 R0\.6/);
  assert.match(note, /一阶频谱泄漏公式/);
  assert.match(note, /C\^2=\\sqrt2 A\^2/);
  assert.match(note, /32\.22030867/);
  assert.match(note, /58\.24/);
  assert.match(note, /6\.248/);
  assert.match(note, /14\.1\\%/);
  assert.match(note, /不是奇性轨道/);
});

test("publishes and links the full six-mode coercivity note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(seventhNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-7\.html"/);
  assert.match(note, /研究笔记 R0\.7/);
  assert.match(note, /六模态强制性不等式/);
  assert.match(note, /9\.7253\\times10\^\{-8\}/);
  assert.match(note, /2D3C 分裂/);
  assert.match(note, /0\.07013115/);
  assert.match(note, /0\.06782090/);
  assert.match(note, /中心模型本身不能成为 Navier-Stokes 奇性轨道/);
});

test("publishes and links the minimal non-coplanar butterfly note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(eighthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-8\.html"/);
  assert.match(note, /研究笔记 R0\.8/);
  assert.match(note, /最小性命题/);
  assert.match(note, /\\mathfrak S=-\(\\sqrt2\+1\)\\mathfrak T/);
  assert.match(note, /0\.0545359/);
  assert.match(note, /0\.0156872/);
  assert.match(note, /生成模态把增长区间延长了约 3\.5 倍/);
  assert.match(note, /没有给出 Galerkin 截断趋于无穷时的解析误差界/);
});

test("publishes and links the exact cone-chain Duhamel note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(ninthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-9\.html"/);
  assert.match(note, /研究笔记 R0\.9/);
  assert.match(note, /c_j\+e_j\+a_\{j\+1\}=0/);
  assert.match(note, /3J\+2/);
  assert.match(note, /4\^\{5j\}H_j/);
  assert.match(note, /81\/\(173056\\sqrt3\)/);
  assert.match(note, /m_N\/N\^3/);
  assert.match(note, /必要，不是充分/);
  assert.match(note, /不是完整动力学近似/);
});

test("publishes and links the dense cross-shell packet note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(tenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-10\.html"/);
  assert.match(note, /研究笔记 R0\.10/);
  assert.match(note, /N\^\{-2\}a_\\delta\(k\/N\)/);
  assert.match(note, /136\\pi\\sqrt6/);
  assert.match(note, /688905/);
  assert.match(note, /O\(\\delta\^5\)/);
  assert.match(note, /\\operatorname\{span\}\(1,-1,-1\)/);
  assert.match(note, /一维极化像/);
  assert.match(note, /没有估计第二 Picard/);
});

test("publishes and links the three-gate polarization relay note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(eleventhNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-11\.html"/);
  assert.match(note, /研究笔记 R0\.11/);
  assert.match(note, /\\mathcal C_\{p,q\}/);
  assert.match(note, /h_n=\\frac\{\\sqrt3\\,x\}/);
  assert.match(note, /\\frac\{3\}\{2\\sqrt2\}/);
  assert.match(note, /一维反向障碍/);
  assert.match(note, /2,000 组固定随机复极化/);
  assert.match(note, /没有稠密包的时间顺序/);
});

test("publishes and links the full two-shell Taylor audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twelfthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-12\.html"/);
  assert.match(note, /研究笔记 R0\.12/);
  assert.match(note, /14\\varepsilon\^2\+2\\varepsilon\^4/);
  assert.match(note, /104\.5341618/);
  assert.match(note, /758\.6825/);
  assert.match(note, /1\.9866%/);
  assert.match(note, /六叶频率恒等式/);
  assert.match(note, /Taylor 余项、稠密包极限和逐壳重复都没有估计/);
});

test("publishes and links the exact fifth-order tree audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirteenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-13\.html"/);
  assert.match(note, /研究笔记 R0\.13/);
  assert.match(note, /47797\\sqrt6\/1120/);
  assert.match(note, /45\.739348964727/);
  assert.match(note, /2\.139524880320144%/);
  assert.match(note, /根节点分裂/);
  assert.match(note, /固定极化、等幅同相/);
  assert.match(note, /热项、Taylor 余项、稠密包和逐壳迭代没有包含在定理中/);
});

test("publishes and links the certified two-amplitude audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fourteenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-14\.html"/);
  assert.match(note, /研究笔记 R0\.14/);
  assert.match(note, /45\.73934896472748/);
  assert.match(note, /11434837\}\{250000/);
  assert.match(note, /94 个有理叶盒/);
  assert.match(note, /35 次消元因子/);
  assert.match(note, /夹逼尚未退化为精确等号/);
  assert.match(note, /不是 Navier–Stokes 方程的全局估计/);
});

test("publishes and links the complex closure and polarization variation", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fifteenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-15\.html"/);
  assert.match(note, /研究笔记 R0\.15/);
  assert.match(note, /45\.73934896472748/);
  assert.match(note, /5420\.19793447103/);
  assert.match(note, /24 个外部叶盒/);
  assert.match(note, /-35\.30791087050734/);
  assert.match(note, /固定 R0\.11 极化不是第五阶/);
  assert.match(note, /不是 Navier–Stokes 方程的全局正则性或奇性结论/);
});

test("publishes and links the second polarization variation and finite candidate", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixteenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-16\.html"/);
  assert.match(note, /研究笔记 R0\.16/);
  assert.match(note, /15 组 Laurent 极点全部抵消/);
  assert.match(note, /-4\.568599750231022/);
  assert.match(note, /18\.035985268234917/);
  assert.match(note, /5\.253208520121551/);
  assert.match(note, /二维反对称降维失效/);
  assert.match(note, /不是 PDE 正则性或奇性结果/);
});

test("publishes and links the decoupled candidate and positive joint Hessian", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(seventeenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-17\.html"/);
  assert.match(note, /研究笔记 R0\.17/);
  assert.match(note, /15\.801443619697901/);
  assert.match(note, /5\.951869509758118/);
  assert.match(note, /0\.7297369691966722/);
  assert.match(note, /五维联合 Hessian 严格正定/);
  assert.match(note, /精细点的一阶导数仍非零/);
  assert.match(note, /任何 Navier–Stokes 正则性或奇性结论/);
});

test("publishes and links the certified antisymmetric stationary point", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(eighteenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-18\.html"/);
  assert.match(note, /研究笔记 R0\.18/);
  assert.match(note, /15\.801442609207275814/);
  assert.ok(note.includes("半径为 \\(10^{-30}\\)"));
  assert.match(note, /严格 Krawczyk 包含/);
  assert.match(note, /严格对角占优余量/);
  assert.match(note, /反对称三变量图中的严格局部极小点/);
  assert.match(note, /完整五维局部极小仍列为开放项/);
  assert.match(note, /不是 Navier–Stokes 正则性或奇性结果/);
});

test("publishes and links the full five-variable Hessian certificate", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(nineteenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-19\.html"/);
  assert.match(note, /研究笔记 R0\.19/);
  assert.match(note, /334 个被某个 jet 激活的频率/);
  assert.match(note, /共同一阶导数恒为零/);
  assert.match(note, /0\.8956390641009896/);
  assert.match(note, /0\.4992780686859093/);
  assert.match(note, /五维 Hessian 正定/);
  assert.match(note, /只指四个实极化图坐标与一个振幅比变量/);
  assert.match(note, /没有得到三维 Navier–Stokes 的正则性或有限时奇性结论/);
  assert.doesNotMatch(note, /R019_[A-Z_]+/);
});

test("publishes and links the positive-parameter global classification", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentiethNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-20\.html"/);
  assert.match(note, /研究笔记 R0\.20/);
  assert.match(note, /恰有两个正内部驻点/);
  assert.match(note, /5\.9518698677219236/);
  assert.match(note, /3\.280940959752690/);
  assert.match(note, /64 \/ 64 完成/);
  assert.match(note, /512 \/ 512 完成/);
  assert.match(note, /未决盒为零/);
  assert.match(note, /计算机辅助有限模型定理/);
  assert.match(note, /没有证明三维 Navier–Stokes 解的全局正则性或有限时奇性/);
  assert.match(note, /src="\/figures\/r0-20-certificate-map\.svg"/);
});

test("publishes and links the viscous correction and cone cancellation progress", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentyFirstNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-21\.html"/);
  assert.match(note, /R0\.21 中间进展/);
  assert.match(note, /-2\.611276916335079/);
  assert.match(note, /-2\.8144704386643693/);
  assert.match(note, /\(L\+1\)\^3/);
  assert.match(note, /11,024 个生成标签/);
  assert.match(note, /模式级算子引理/);
  assert.match(note, /没有证明三维 Navier–Stokes 解的全局正则性或有限时奇性/);
});

test("publishes and links the sharp analytic-radius obstruction", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentySecondNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-22\.html"/);
  assert.match(note, /研究笔记 R0\.22/);
  assert.match(note, /\\frac\{24\}\{e\^2\\eta\^2\}/);
  assert.match(note, /\\frac\{27\}\{2\}/);
  assert.match(note, /r\(a_N\+b_N\)=r\(a_N\)\+r\(b_N\)/);
  assert.match(note, /一阶解析半径估计不可能成立/);
  assert.match(note, /没有证明三维 Navier–Stokes 的全局正则性或有限时奇性/);
});

test("publishes and links the first generated-subspace sharpness audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentyThirdNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-23\.html"/);
  assert.match(note, /研究笔记 R0\.23/);
  assert.match(note, /0\.3045602145/);
  assert.match(note, /0\.0043346408/);
  assert.match(note, /1720 个精确非零输出标签/);
  assert.match(note, /8\.3\\times10\^\{-4\}/);
  assert.match(note, /不能推出所有 \\(N\\) 的增长阶|不能决定渐近阶/);
  assert.match(note, /没有证明三维 Navier–Stokes 的全局正则性或有限时奇性/);
});

test("publishes and links the minimal-face N=3 sharpness audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentyFourthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-24\.html"/);
  assert.match(note, /研究笔记 R0\.24/);
  assert.match(note, /320 个非零标签/);
  assert.match(note, /0\.361556/);
  assert.match(note, /0\.00195675/);
  assert.match(note, /7\.71697\\times10\^\{-7\}/);
  assert.match(note, /所有二次域基坐标完全一致/);
  assert.match(note, /两个点不能证明有界或次二次增长/);
  assert.match(note, /没有证明三维 Navier–Stokes 的全局正则性或有限时奇性/);
});

test("publishes and links the boundary-face polarization-channel reduction", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentyFifthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-25\.html"/);
  assert.match(note, /研究笔记 R0\.25/);
  assert.match(note, /四个相互作用通道依次按 \\\(N\^2,N,N,1\\\) 分层/);
  assert.match(note, /44N\^2\|\\sigma_A\\sigma_B\|/);
  assert.match(note, /0\.421619/);
  assert.match(note, /2\.27410\\times10\^\{-11\}/);
  assert.match(note, /相对差低于 \\\(1\.5\\times10\^\{-43\}\\\)/);
  assert.match(note, /没有得到所有 \\\(N\\\) 的增益上界/);
  assert.match(note, /没有证明三维 Navier–Stokes 的全局正则性或有限时奇性/);
});

test("publishes and links the exact edge and three-leaf transfer audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentySixthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-26\.html"/);
  assert.match(note, /研究笔记 R0\.26/);
  assert.match(note, /\\\(b_N\\\) 完全由 \\\(P_-,C_\+\\\) 两个生成元产生/);
  assert.match(note, /24t=11\.9010214083238/);
  assert.match(note, /18\.8124/);
  assert.match(note, /1620\.26/);
  assert.match(note, /最大相对精度差为 \\\(3\.57\\times10\^\{-43\}\\\)/);
  assert.match(note, /不能单独证明或否定 \\\(\\sigma=O\(N\^\{-1\}\)\\\)/);
  assert.match(note, /没有得到 Navier–Stokes 全局正则性或有限时奇性的结论/);
});

test("publishes and links the scalar generating-equation audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentySeventhNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-27\.html"/);
  assert.match(note, /研究笔记 R0\.27/);
  assert.match(note, /b_N=\[r\^N\\xi\^1\]\(A,S\)/);
  assert.match(note, /3\.21\\times10\^\{-43\}/);
  assert.match(note, /0\.9997788687/);
  assert.match(note, /N=34,45,57,68/);
  assert.match(note, /有限计算，只能提供强数值证据，不能证明极限/);
  assert.match(note, /没有得到三维 Navier–Stokes 全局正则性或有限时奇性的结论/);
  assert.match(note, /r0-27-endpoint-polarization\.svg/);
});

test("publishes and links the exact rational finite-ratio audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentyEighthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-28\.html"/);
  assert.match(note, /研究笔记 R0\.28/);
  assert.match(note, /d=pu\+qv/);
  assert.match(note, /62214\.5105/);
  assert.match(note, /\\rho\^D_N<\\rho\^A_N/);
  assert.match(note, /1\.0294319301/);
  assert.match(note, /1\.2221486618/);
  assert.match(note, /有限窗口尚不能证明比值收敛/);
  assert.match(note, /没有证明 \\\(\|\\sigma_\{B,N\}\|\\to1\\\)/);
  assert.match(note, /r0-28-ratio-separation\.svg/);
});

test("publishes and links the all-order canonical transport reduction", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(twentyNinthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-29\.html"/);
  assert.match(note, /研究笔记 R0\.29/);
  assert.match(note, /\\boxed\{\\\{U,V\\\}=UV\}/);
  assert.match(note, /\\frac UV=\\frac ZW e\^\{-a\}/);
  assert.match(note, /k f_\{k,q\+1\}/);
  assert.match(note, /有限扇区锥不闭合/);
  assert.match(note, /次数 119 的 GMP 计算只是独立回归，不是定理依据/);
  assert.match(note, /16,176,149 次精确卷积相互作用/);
  assert.match(note, /峰值常驻内存为 33\.422 MiB/);
  assert.match(note, /没有得到三维 Navier–Stokes 正则性或有限时奇性的结论/);
  assert.match(note, /r0-29-canonical-reduction\.svg/);
});

test("publishes and links the all-order analytic majorant", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtiethNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-30\.html"/);
  assert.match(note, /研究笔记 R0\.30/);
  assert.match(note, /\\frac\{k\}\{3k-q-1\}\\le1/);
  assert.match(note, /A_L\\le\\frac32\\sum_\{i\+j=L\}\\min\(i,j\)A_iA_j/);
  assert.match(note, /H_L\\le16\\sum_\{i\\ge1\}\\frac1\{i\^2\}<32/);
  assert.match(note, /A_L\\le\\frac\{2K\^\{L-1\}\}\{L\^3\}/);
  assert.match(note, /半径 \\\(1\/96\\\)/);
  assert.match(note, /半径 \\\(1\/192\\\)/);
  assert.match(note, /5,484,501 次有序递推相互作用/);
  assert.match(note, /没有证明三维 Navier–Stokes 解的全局正则性或有限时奇性/);
  assert.match(note, /r0-30-analytic-domain\.svg/);
});

test("publishes and links the improved all-order analytic domain", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtyFirstNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-31\.html"/);
  assert.match(note, /研究笔记 R0\.31/);
  assert.match(note, /H_L\\le\\frac\{27\}\{4\}/);
  assert.match(note, /\\frac\{10000\}\{2187\}/);
  assert.match(note, /K=81\/4/);
  assert.match(note, /\\frac4\{81\}/);
  assert.match(note, /128\/27\\approx4\.7407/);
  assert.match(note, /256\/27\\approx9\.4815/);
  assert.match(note, /2–296 阶全部通过.*297 阶以后单调解析尾界/);
  assert.match(note, /5,484,501 次有序递推相互作用/);
  assert.match(note, /没有证明三维 Navier–Stokes 解的全局正则性或有限时奇性/);
  assert.match(note, /r0-31-improved-domain\.svg/);
});

test("publishes and links the fixed-charge singularity candidate audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtySecondNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-32\.html"/);
  assert.match(note, /研究笔记 R0\.32/);
  assert.match(note, /F_q\(R\)=\[\\Xi\^q\]F\(R,\\Xi\)/);
  assert.match(note, /\\frac\{64\}\{531441\}\\approx1\.20427/);
  assert.match(note, /-0\.749701196287094659168546/);
  assert.match(note, /全部严格小于 \\\(-1\/2\\\)/);
  assert.match(note, /零点候选/);
  assert.match(note, /13,518,749 次有序递推相互作用/);
  assert.match(note, /有限有理逼近的精确根/);
  assert.match(note, /不能从该有限诊断推出 Navier–Stokes 解的奇性/);
  assert.match(note, /r0-32-candidate-cluster\.svg/);
});

test("publishes and links the exact positive-measure obstruction", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtyThirdNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-33\.html"/);
  assert.match(note, /研究笔记 R0\.33/);
  assert.match(note, /-437\/24192/);
  assert.match(note, /-43522897\/685843200/);
  assert.match(note, /-32\/63/);
  assert.match(note, /-29699111\/12700800/);
  assert.match(note, /后续系数不能改变它们/);
  assert.match(note, /不能声称约 \\\(-0\.7495\\\) 的候选是假的/);
  assert.match(note, /不能从本次矩条件反例推出 Navier–Stokes 解的正则性或有限时奇性/);
  assert.match(note, /r0-33-hankel-obstruction\.svg/);
});

test("publishes and links the bounded-degree polynomial-background obstruction", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtyFourthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-34\.html"/);
  assert.match(note, /研究笔记 R0\.34/);
  assert.match(note, /\\deg P_d\\le d/);
  assert.match(note, /\\\(d\\le43\\\)/);
  assert.match(note, /\\\(d\\le44\\\)/);
  assert.match(note, /\\\(d\\le46\\\)/);
  assert.match(note, /216 个精确有理行列式/);
  assert.match(note, /其中 67 个为负/);
  assert.match(note, /任意实系数都失败/);
  assert.match(note, /不能声称无限解析背景不存在/);
  assert.match(note, /11cb3c386814a4d725944251a2d46faef0f5c53c/);
  assert.match(note, /r0-34-tail-background-obstruction\.svg/);
});

test("publishes and links the fixed-charge continuation geometry", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtyFifthNoteUrl, "utf8"),
    readFile(thirtyFifthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-35\.html"/);
  assert.match(home, /href="\/notes\/r0-35\.pdf"/);
  assert.match(note, /研究笔记 R0\.35/);
  assert.match(note, /href="\/notes\/r0-35\.pdf"/);
  assert.match(note, /3N\^2/);
  assert.match(note, /121\/48/);
  assert.match(note, /18\.3937 至 18\.3943 倍/);
  assert.match(note, /c95c74eb19c36962b55de887ee75654a12e3a833/);
  assert.match(note, /r0-35-continuation-scale\.svg/);
  assert.match(note, /不能声称 R0\.32 候选已经得到认证/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the certified in-domain short continuation step", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtySixthNoteUrl, "utf8"),
    readFile(thirtySixthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-36\.html"/);
  assert.match(home, /href="\/notes\/r0-36\.pdf"/);
  assert.match(note, /研究笔记 R0\.36/);
  assert.match(note, /href="\/notes\/r0-36\.pdf"/);
  assert.match(note, /\\delta=\\rho_\*\/7=4\/567/);
  assert.match(note, /C\(1\/2\)=121\/48/);
  assert.match(note, /5\.3934097613896530405/);
  assert.match(note, /\\frac\{35183\}\{350\}/);
  assert.match(note, /e8685f41005a3149ebff91e9f4d537b02dbacb00/);
  assert.match(note, /r0-36-short-step\.svg/);
  assert.match(note, /不能声称已经跨越 R0\.31 边界/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the all-order weighted restart beyond the old radius", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtySeventhNoteUrl, "utf8"),
    readFile(thirtySeventhPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-37\.html"/);
  assert.match(home, /href="\/notes\/r0-37\.pdf"/);
  assert.match(note, /研究笔记 R0\.37/);
  assert.match(note, /href="\/notes\/r0-37\.pdf"/);
  assert.match(note, /r_\*=\\frac\{16\}\{243\}/);
  assert.match(note, /\\frac\{40\}\{243\}/);
  assert.match(note, /精确比例 .*7\/4.*失败/);
  assert.match(note, /2\.99904918794896\\times10\^\{-46\}/);
  assert.match(note, /04e62468f383d5e07c572ffd89561ee46dc249b8/);
  assert.match(note, /r0-37-radius-restart\.svg/);
  assert.match(note, /没有给出三维 Navier–Stokes 方程的全局正则性/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the tail-aware restart and negative preconditioner audit", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtyEighthNoteUrl, "utf8"),
    readFile(thirtyEighthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-38\.html"/);
  assert.match(home, /href="\/notes\/r0-38\.pdf"/);
  assert.match(note, /研究笔记 R0\.38/);
  assert.match(note, /href="\/notes\/r0-38\.pdf"/);
  assert.match(note, /r_\*=\\frac\{59\}\{500\}/);
  assert.match(note, /Z_N\(r\)=3\\left\(M_N\(r\)\+\\frac\{S_N\(r\)\}\{N\+1\}\\right\)/);
  assert.match(note, /62 维精确逆没有进入尾部收缩常数/);
  assert.match(note, /1\.000718148591245445/);
  assert.match(note, /bc230622aeac611966c091c4beca734c783f65ac/);
  assert.match(note, /r0-38-tail-restart\.svg/);
  assert.match(note, /它没有给出三维 Navier–Stokes 方程的全局正则性/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the all-order charge-resolved restart", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirtyNinthNoteUrl, "utf8"),
    readFile(thirtyNinthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-39\.html"/);
  assert.match(home, /href="\/notes\/r0-39\.pdf"/);
  assert.match(note, /研究笔记 R0\.39/);
  assert.match(note, /href="\/notes\/r0-39\.pdf"/);
  assert.match(note, /r_\*=\\frac\{397\}\{2000\}/);
  assert.match(note, /242 个扇区全部用精确有理数求界/);
  assert.match(note, /0\.6896011188611451/);
  assert.match(note, /1\.0025428645146803/);
  assert.match(note, /ed08ad45b3440a679d8132d7b3464dc21dd07fa5/);
  assert.match(note, /r0-39-charge-resolved-restart\.svg/);
  assert.match(note, /不是完整流体方程的正则性证明/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the exact two-endpoint transport theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortiethNoteUrl, "utf8"),
    readFile(fortiethPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-40\.html"/);
  assert.match(home, /href="\/notes\/r0-40\.pdf"/);
  assert.match(note, /研究笔记 R0\.40/);
  assert.match(note, /href="\/notes\/r0-40\.pdf"/);
  assert.match(note, /r_\*=\\frac\{32\}\{125\}/);
  assert.match(note, /完整列和关于输入斜率是凸函数/);
  assert.match(note, /0\.8621992110422389/);
  assert.match(note, /1\.0002561524370209/);
  assert.match(note, /413f1cbcb12a961129eacf2482eb9b705c9a2feb/);
  assert.match(note, /r0-40-two-endpoint-transport\.svg/);
  assert.match(note, /不是完整三维方程的解答/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the degree-resolved active-tail theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortyFirstNoteUrl, "utf8"),
    readFile(fortyFirstPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-41\.html"/);
  assert.match(home, /href="\/notes\/r0-41\.pdf"/);
  assert.match(note, /研究笔记 R0\.41/);
  assert.match(note, /href="\/notes\/r0-41\.pdf"/);
  assert.match(note, /r_\*=\\frac\{9\}\{32\}/);
  assert.match(note, /完整中心核关于/);
  assert.match(note, /共同端点/);
  assert.match(note, /0\.7785423316172445/);
  assert.match(note, /1\.0003750451629853/);
  assert.match(note, /c851762902bb97dd3f3f2510b7321771e0a1ff03/);
  assert.match(note, /r0-41-degree-resolved-tail\.svg/);
  assert.match(note, /不是完整三维方程的解答/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the canonical-stretch transport theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortySecondNoteUrl, "utf8"),
    readFile(fortySecondPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-42\.html"/);
  assert.match(home, /href="\/notes\/r0-42\.pdf"/);
  assert.match(note, /研究笔记 R0\.42/);
  assert.match(note, /href="\/notes\/r0-42\.pdf"/);
  assert.match(note, /r_\*=\\frac\{329\}\{1000\}/);
  assert.match(note, /输出次数与范数权重精确抵消/);
  assert.match(note, /0\.5817058427617202/);
  assert.match(note, /0\.7633728925335545/);
  assert.match(note, /1\.0028721508539940/);
  assert.match(note, /5ff24eae1cb9f73a1aac6965b07f0c1f12c62477/);
  assert.match(note, /r0-42-canonical-stretch\.svg/);
  assert.match(note, /不是三维正则性定理/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the charge-implied degree-floor theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortyThirdNoteUrl, "utf8"),
    readFile(fortyThirdPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-43\.html"/);
  assert.match(home, /href="\/notes\/r0-43\.pdf"/);
  assert.match(note, /研究笔记 R0\.43/);
  assert.match(note, /href="\/notes\/r0-43\.pdf"/);
  assert.match(note, /r_\*=\\frac\{33\}\{100\}/);
  assert.match(note, /统一输入次数下界从 81 提高到 121/);
  assert.match(note, /0\.9988814424270074/);
  assert.match(note, /1\.0038955265828947/);
  assert.match(note, /4fe8cb308e20921fb0490aa2e76209b1d2d84221/);
  assert.match(note, /r0-43-charge-degree-floor\.svg/);
  assert.match(note, /不是三维正则性定理/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the common-slope endpoint theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortyFourthNoteUrl, "utf8"),
    readFile(fortyFourthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-44\.html"/);
  assert.match(home, /href="\/notes\/r0-44\.pdf"/);
  assert.match(note, /研究笔记 R0\.44/);
  assert.match(note, /href="\/notes\/r0-44\.pdf"/);
  assert.match(note, /r_\* = \\frac\{37\}\{100\}/);
  assert.match(note, /完整大荷正和在共同斜率上是凸函数/);
  assert.match(note, /0\.9662130057569357/);
  assert.match(note, /0\.9970118412481986/);
  assert.match(note, /1\.0008564924160487608/);
  assert.match(note, /aade631ea1a492d078f052776b443875d6a3dd73/);
  assert.match(note, /r0-44-common-slope-tail\.svg/);
  assert.match(note, /没有证明三维不可压 Navier–Stokes 全局正则性/);
  assert.match(note, /我不再让中心项各自选择最坏输入斜率/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the exact fixed-negative-charge endpoint theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortyFifthNoteUrl, "utf8"),
    readFile(fortyFifthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-45\.html"/);
  assert.match(home, /href="\/notes\/r0-45\.pdf"/);
  assert.match(note, /研究笔记 R0\.45/);
  assert.match(note, /href="\/notes\/r0-45\.pdf"/);
  assert.match(note, /r_\* = \\frac\{371\}\{1000\}/);
  assert.ok(note.includes("一个度一 \\(q=2\\) 种子足以压过全部 \\(q=1\\) 负导数"));
  assert.match(note, /0\.9972280412291890/);
  assert.match(note, /1\.0010616516434951437/);
  assert.match(note, /8f7f9ec2b90b2d249b474ec4dbba50a71c807745/);
  assert.match(note, /r0-45-fixed-negative-charge\.svg/);
  assert.match(note, /没有证明三维不可压 Navier–Stokes 全局正则性/);
  assert.match(note, /我把完整列保留为共同变量/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the correlated two-block weighted-column theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortySixthNoteUrl, "utf8"),
    readFile(fortySixthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-46\.html"/);
  assert.match(home, /href="\/notes\/r0-46\.pdf"/);
  assert.match(note, /研究笔记 R0\.46/);
  assert.match(note, /href="\/notes\/r0-46\.pdf"/);
  assert.match(note, /r\* = 376\/1000/);
  assert.ok(note.includes("权重必须放进同一输入列"));
  assert.match(note, /0\.99770647568583198433/);
  assert.match(note, /1\.0030411177094620525/);
  assert.match(note, /a521a84f01b748e3c138ecb785c1b21907dc0e28/);
  assert.match(note, /r0-46-two-block-weight\.svg/);
  assert.match(note, /没有证明三维不可压 Navier–Stokes 全局正则性/);
  assert.match(note, /我把输出零荷通道与其余输出分成两块/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the exact charge-degree lattice endpoint theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortySeventhNoteUrl, "utf8"),
    readFile(fortySeventhPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-47\.html"/);
  assert.match(home, /href="\/notes\/r0-47\.pdf"/);
  assert.match(note, /研究笔记 R0\.47/);
  assert.match(note, /href="\/notes\/r0-47\.pdf"/);
  assert.match(note, /r\* = 94233\/250000/);
  assert.ok(note.includes("239 个固定荷各自覆盖全部次数"));
  assert.match(note, /0\.9999973490826196656/);
  assert.match(note, /1\.0000026584572409359/);
  assert.match(note, /709ecb5f20b7321079ba114a57bf20b77ca7646a/);
  assert.match(note, /r0-47-charge-degree-lattice\.svg/);
  assert.match(note, /没有证明三维不可压 Navier–Stokes 全局正则性/);
  assert.match(note, /我把真实格点约束一直保留到完整列和中/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the exact threshold-root theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortyEighthNoteUrl, "utf8"),
    readFile(fortyEighthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-48\.html"/);
  assert.match(home, /href="\/notes\/r0-48\.pdf"/);
  assert.match(note, /研究笔记 R0\.48/);
  assert.match(note, /href="\/notes\/r0-48\.pdf"/);
  assert.ok(note.includes("243 个竞争对象在整个窗口更小"));
  assert.match(note, /0\.376932499290527340/);
  assert.match(note, /9\.9933786489298977945/);
  assert.match(note, /P\(r\)\\to\+\\infty/);
  assert.match(note, /\\omega_\{a\+b\}\\le\\omega_a\\omega_b/);
  assert.doesNotMatch(note, /\(rge0\)|\(rin I\)|\(sge241\)|\(omega_/);
  assert.match(note, /fe65dcb365eca9d934c3ec6055c06d7a7c1a515c/);
  assert.match(note, /r0-48-threshold-root\.svg/);
  assert.match(note, /这不是三维不可压 Navier–Stokes 正则性或奇性定理/);
  assert.match(note, /我把真实活跃列写成 80 次正系数多项式/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the multiplicative charge-character threshold theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fortyNinthNoteUrl, "utf8"),
    readFile(fortyNinthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-49\.html"/);
  assert.match(home, /href="\/notes\/r0-49\.pdf"/);
  assert.match(note, /研究笔记 R0\.49/);
  assert.match(note, /href="\/notes\/r0-49\.pdf"/);
  assert.match(note, /\\omega_s=\(4\/5\)\^s/);
  assert.match(note, /\(m\+n\)\|f_\{mn\}\|r\^\{m\+n\}c\^\{2n-m\}/);
  assert.match(note, /0\.382618642388680778/);
  assert.match(note, /1\.4157274652028842093\\times10\^\{-4\}/);
  assert.match(note, /1\.6910402110013306773\\times10\^\{-30\}/);
  assert.match(note, /1\.0459367903514846826/);
  assert.match(note, /32 项精确检查全部通过/);
  assert.match(note, /26ce6d7ffd636956fe7c95a2bbeb7e6ea6573728/);
  assert.match(note, /e36fce33f8a5edeb144cdbeda00a568b972d9a3a8ac0e96c04d7651e71a64578/);
  assert.match(note, /r0-49-charge-character\.svg/);
  assert.match(note, /不能声称已经证明或反驳三维 Navier–Stokes 正则性/);
  assert.ok(note.includes("我把荷 \\(s\\) 的权重改成精确乘法特征"));
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the global charge-character optimization theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftiethNoteUrl, "utf8"),
    readFile(fiftiethPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-50\.html"/);
  assert.match(home, /href="\/notes\/r0-50\.pdf"/);
  assert.ok(home.includes("R0.51 已完成："));
  assert.match(note, /研究笔记 R0\.50/);
  assert.match(note, /href="\/notes\/r0-50\.pdf"/);
  assert.match(note, /0\.8024563827/);
  assert.match(note, /0\.382619813709565/);
  assert.match(note, /1\.4580280493538903081\\times10\^\{-4\}/);
  assert.match(note, /1\.0000030613272706956/);
  assert.match(note, /1\.7828790986376003423\\times10\^\{-30\}/);
  assert.match(note, /33 项精确检查全部通过/);
  assert.match(note, /a9c469a96462e60655b0fea435177ececb8aef20/);
  assert.match(note, /fc173a2108ef881d21d9d54046085f0d5daf5cc33ed50e024ca32ec867f7b79a/);
  assert.match(note, /r0-50-charge-character-optimization\.svg/);
  assert.match(note, /不能声称已经证明或反驳三维 Navier–Stokes 正则性/);
  assert.ok(home.includes("我把 R0.49 固定的 \\(c=4/5\\) 放回完整乘法特征族"));
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the critical Fourier bridge and scalar-charge obstruction", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftyFifthNoteUrl, "utf8"),
    readFile(fiftyFifthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-55\.html"/);
  assert.match(home, /href="\/notes\/r0-55\.pdf"/);
  assert.ok(home.includes("R0.55 已完成："));
  assert.match(home, /R0\.55 已完成：<\/strong>完整 Fourier--Leray 项/);
  assert.match(note, /研究笔记 R0\.55/);
  assert.match(note, /临界标量桥梁有限/);
  assert.match(note, /href="\/notes\/r0-55\.pdf"/);
  assert.match(note, /\\mathcal X\^\{-1\}/);
  assert.match(note, /\\nu\^\{-1\}/);
  assert.match(note, /p_N=\(N,0,0\)/);
  assert.ok(note.includes("输入/输出尺度分离等于 \\(N\\)"));
  assert.ok(note.includes("卷积可加且 \\(SO(3)\\) 不变"));
  assert.match(note, /200,000 个三元组/);
  assert.match(note, /15,624 个/);
  assert.match(note, /17 项检查全部通过/);
  assert.match(note, /feacd0c47aa123d508f4889bfb1e6770c40da1fef6e438acc1aa9ecd99fc19ae/);
  assert.match(note, /r0-55-critical-fourier-bridge\.svg/);
  assert.match(note, /方向协变向量荷、方向扇区/);
  assert.ok(note.includes("我从完整三维 Fourier--Leray 双线性项出发"));
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(
    note,
    /\(lambd|\(alph|\(bet|\(omeg|[^\u005c]qquad|[^\u005c]times10/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the fixed affine charge-weight threshold theorem", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftyFirstNoteUrl, "utf8"),
    readFile(fiftyFirstPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-51\.html"/);
  assert.match(home, /href="\/notes\/r0-51\.pdf"/);
  assert.ok(home.includes("R0.52 已完成："));
  assert.match(note, /研究笔记 R0\.51/);
  assert.match(note, /href="\/notes\/r0-51\.pdf"/);
  assert.match(note, /c_0=\\frac\{19939\}\{25000\}=0\.79756/);
  assert.match(note, /\\lambda_0=\\frac\{7653\}\{10000\}=0\.7653/);
  assert.match(note, /0\.382624471846022/);
  assert.match(note, /1\.7808194822375234792\\times10\^\{-5\}/);
  assert.match(note, /1\.0000121743210599539/);
  assert.match(note, /2\.7403915410748708982\\times10\^\{-31\}/);
  assert.match(note, /26 项精确检查全部通过/);
  assert.match(note, /a53fdea63631977e4bb18f56da91e4e32e1a70c3/);
  assert.match(note, /db72d40ee304d1a6ce5dd96d9f5971e78037675e79c837e409c5691bb8aa582f/);
  assert.match(note, /r0-51-affine-charge-weight\.svg/);
  assert.match(note, /不能声称已经证明或反驳三维 Navier–Stokes 正则性/);
  assert.ok(note.includes("我把权重扩展为 \\(\\omega_s=c^s(1+\\lambda|s|)\\)"));
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the complete affine-family global enclosure", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftySecondNoteUrl, "utf8"),
    readFile(fiftySecondPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-52\.html"/);
  assert.match(home, /href="\/notes\/r0-52\.pdf"/);
  assert.ok(home.includes("R0.52 已完成："));
  assert.match(note, /研究笔记 R0\.52/);
  assert.match(note, /href="\/notes\/r0-52\.pdf"/);
  assert.match(note, /3826244718485988314760952288871012330925/);
  assert.match(note, /3826244718485988314760952288871012330926/);
  assert.match(note, /6\.8068\\times10\^\{-39\}/);
  assert.match(note, /242 个非活跃对象全部低于一/);
  assert.match(note, /22 项精确检查全部通过/);
  assert.match(note, /e64ed23dcd86883e9690468b05f64304ee4ac816/);
  assert.match(note, /b79e59ec327bc02b64e23ad3f903b6d61860a075d59ff75a43d82f5684590def/);
  assert.match(note, /r0-52-affine-family-global\.svg/);
  assert.match(note, /它没有证明区间中的局部 KKT 根就是精确实数意义下唯一的全局最大点/);
  assert.ok(note.includes("我现在把 \\(c&gt;0,\\lambda\\ge0\\) 的完整二参数族"));
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(
    note,
    /\(lambd|\(alph|\(omeg|Ege0|Fle0|Gle0|[^\u005c]qquad|[^\u005c]times10/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the rational product-affine witness", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftyThirdNoteUrl, "utf8"),
    readFile(fiftyThirdPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-53\.html"/);
  assert.match(home, /href="\/notes\/r0-53\.pdf"/);
  assert.ok(home.includes("R0.53 已完成："));
  assert.match(home, /R0\.53 已完成：<\/strong>&nbsp;简单有理乘积仿射权/);
  assert.match(note, /研究笔记 R0\.53/);
  assert.match(note, /第二个仿射因子&nbsp;<br>产生严格增益/);
  assert.match(note, /href="\/notes\/r0-53\.pdf"/);
  assert.match(note, /c=\\frac\{396403\}\{500000\}=0\.792806/);
  assert.match(note, /\\lambda=\\mu=\\frac\{153931\}\{500000\}=0\.307862/);
  assert.match(note, /0\.382628602237879637/);
  assert.match(note, /1\.4883451915609408904\\times10\^\{-6\}/);
  assert.match(note, /1\.0000107948905119688/);
  assert.match(note, /7\.5271302784558830723\\times10\^\{-31\}/);
  assert.match(note, /28 项精确检查全部通过/);
  assert.match(note, /96d7d8c7d0a59e1b0b75d2580403cb5969d6ea6e/);
  assert.match(note, /5d6486dfcc6f2c016380a29698ed986213701b9441dd007d95acce4fc0ea67a5/);
  assert.match(note, /r0-53-product-affine-witness\.svg/);
  assert.match(note, /没有证明这个有理点是完整三参数乘积族的全局最优点/);
  assert.ok(note.includes("我现在给出一个分母仅为 \\(5\\times10^5\\)"));
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(
    note,
    /\(lambd|\(alph|\(bet|\(omeg|[^\u005c]qquad|[^\u005c]times10/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("publishes and links the complete product-affine global enclosure", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fiftyFourthNoteUrl, "utf8"),
    readFile(fiftyFourthPdfUrl),
  ]);

  assert.match(home, /href="\/notes\/r0-54\.html"/);
  assert.match(home, /href="\/notes\/r0-54\.pdf"/);
  assert.ok(home.includes("R0.54 已完成："));
  assert.match(home, /R0\.54 已完成：<\/strong>完整乘积仿射族/);
  assert.match(note, /研究笔记 R0\.54/);
  assert.match(note, /完整三参数族&nbsp;<br>被压入严格窄区间/);
  assert.match(note, /href="\/notes\/r0-54\.pdf"/);
  assert.match(note, /0\.382628602237879637/);
  assert.match(note, /3\.97762120363\\times10\^\{-7\}/);
  assert.match(note, /1\.0000118344531892886/);
  assert.match(note, /1\.0000010395514554756/);
  assert.match(note, /14 个闭矩形覆盖整个有界不变量域/);
  assert.match(note, /16 项精确检查全部通过/);
  assert.match(note, /543a394c51a9454496638eb1a9324775164b2eaa/);
  assert.match(note, /130e954c3f8b711c28664f6f1d2aeb589942f69773ac9c839d98cc8f71b3006b/);
  assert.match(note, /r0-54-product-affine-global\.svg/);
  assert.match(note, /没有证明区间中的诊断候选是精确全局最大点/);
  assert.ok(note.includes("我现在把完整参数域 \\(c&gt;0,\\lambda,\\mu\\ge0\\)"));
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(
    note,
    /\(lambd|\(alph|\(bet|\(omeg|[^\u005c]qquad|[^\u005c]times10/,
  );
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("follows the operating system light and dark color scheme", async () => {
  const html = await readFile(siteUrl, "utf8");

  assert.match(html, /color-scheme:\s*light dark/);
  assert.match(html, /prefers-color-scheme:\s*dark/);
  assert.match(
    html,
    /name="theme-color" content="#171816" media="\(prefers-color-scheme: dark\)"/,
  );
});

test("uses a plain first-person research voice", async () => {
  const [home, firstNote, secondNote, thirdNote, fourthNote, fifthNote, sixthNote, seventhNote, eighthNote, ninthNote, tenthNote, eleventhNote, twelfthNote, thirteenthNote, fourteenthNote, fifteenthNote, sixteenthNote, seventeenthNote, eighteenthNote, nineteenthNote, twentiethNote, twentyFirstNote, twentySecondNote, twentyThirdNote, twentyFourthNote, twentyFifthNote, twentySixthNote, twentySeventhNote, twentyEighthNote, twentyNinthNote, thirtiethNote, thirtyFirstNote, thirtySecondNote, thirtyThirdNote, thirtyFourthNote, thirtyFifthNote, thirtySixthNote, thirtySeventhNote, thirtyEighthNote, thirtyNinthNote, fortiethNote, fortyFirstNote, fortySecondNote, fortyThirdNote] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(firstNoteUrl, "utf8"),
    readFile(secondNoteUrl, "utf8"),
    readFile(thirdNoteUrl, "utf8"),
    readFile(fourthNoteUrl, "utf8"),
    readFile(fifthNoteUrl, "utf8"),
    readFile(sixthNoteUrl, "utf8"),
    readFile(seventhNoteUrl, "utf8"),
    readFile(eighthNoteUrl, "utf8"),
    readFile(ninthNoteUrl, "utf8"),
    readFile(tenthNoteUrl, "utf8"),
    readFile(eleventhNoteUrl, "utf8"),
    readFile(twelfthNoteUrl, "utf8"),
    readFile(thirteenthNoteUrl, "utf8"),
    readFile(fourteenthNoteUrl, "utf8"),
    readFile(fifteenthNoteUrl, "utf8"),
    readFile(sixteenthNoteUrl, "utf8"),
    readFile(seventeenthNoteUrl, "utf8"),
    readFile(eighteenthNoteUrl, "utf8"),
    readFile(nineteenthNoteUrl, "utf8"),
    readFile(twentiethNoteUrl, "utf8"),
    readFile(twentyFirstNoteUrl, "utf8"),
    readFile(twentySecondNoteUrl, "utf8"),
    readFile(twentyThirdNoteUrl, "utf8"),
    readFile(twentyFourthNoteUrl, "utf8"),
    readFile(twentyFifthNoteUrl, "utf8"),
    readFile(twentySixthNoteUrl, "utf8"),
    readFile(twentySeventhNoteUrl, "utf8"),
    readFile(twentyEighthNoteUrl, "utf8"),
    readFile(twentyNinthNoteUrl, "utf8"),
    readFile(thirtiethNoteUrl, "utf8"),
    readFile(thirtyFirstNoteUrl, "utf8"),
    readFile(thirtySecondNoteUrl, "utf8"),
    readFile(thirtyThirdNoteUrl, "utf8"),
    readFile(thirtyFourthNoteUrl, "utf8"),
    readFile(thirtyFifthNoteUrl, "utf8"),
    readFile(thirtySixthNoteUrl, "utf8"),
    readFile(thirtySeventhNoteUrl, "utf8"),
    readFile(thirtyEighthNoteUrl, "utf8"),
    readFile(thirtyNinthNoteUrl, "utf8"),
    readFile(fortiethNoteUrl, "utf8"),
    readFile(fortyFirstNoteUrl, "utf8"),
    readFile(fortySecondNoteUrl, "utf8"),
    readFile(fortyThirdNoteUrl, "utf8"),
  ]);

  assert.match(home, /这里记录我对三维不可压缩 Navier–Stokes 全局正则性问题/);
  assert.match(home, /我目前/);
  assert.doesNotMatch(
    home,
    /我们|攻关|主攻|研究纪律|杀死错误想法|宏大新泛函|三重审计/,
  );
  assert.match(firstNote, /这里没有新定理/);
  assert.doesNotMatch(
    firstNote,
    /本笔记的职责|本轮|审计规则|准确停止|本轮真正得到/,
  );
  assert.match(secondNote, /我把 R0\.1/);
  assert.doesNotMatch(
    secondNote,
    /Research packet|AUDIT STATUS|我们|本轮|成果边界|研究判定|极值审计/,
  );
  assert.match(thirdNote, /我继续检查 R0\.2/);
  assert.doesNotMatch(
    thirdNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fourthNote, /我把 R0\.3/);
  assert.doesNotMatch(
    fourthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fifthNote, /我把 R0\.4/);
  assert.doesNotMatch(
    fifthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(sixthNote, /我把 R0\.5/);
  assert.doesNotMatch(
    sixthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(seventhNote, /我把 R0\.6/);
  assert.doesNotMatch(
    seventhNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(eighthNote, /我把 R0\.7/);
  assert.doesNotMatch(
    eighthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(ninthNote, /我把 R0\.8/);
  assert.doesNotMatch(
    ninthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(tenthNote, /我把 R0\.9/);
  assert.doesNotMatch(
    tenthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(eleventhNote, /我继续检查 R0\.10/);
  assert.doesNotMatch(
    eleventhNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twelfthNote, /我把 R0\.11/);
  assert.doesNotMatch(
    twelfthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirteenthNote, /我把 R0\.12/);
  assert.doesNotMatch(
    thirteenthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fourteenthNote, /我放开 R0\.13/);
  assert.doesNotMatch(
    fourteenthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fifteenthNote, /我补上 R0\.14/);
  assert.doesNotMatch(
    fifteenthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(sixteenthNote, /我把 R0\.15/);
  assert.doesNotMatch(
    sixteenthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(seventeenthNote, /我把 R0\.16/);
  assert.doesNotMatch(
    seventeenthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(eighteenthNote, /我把 R0\.17/);
  assert.doesNotMatch(
    eighteenthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(nineteenthNote, /我把 R0\.18/);
  assert.doesNotMatch(
    nineteenthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentiethNote, /我把 R0\.19/);
  assert.doesNotMatch(
    twentiethNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentyFirstNote, /我把 R0\.20/);
  assert.doesNotMatch(
    twentyFirstNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentySecondNote, /我完成了 R0\.21/);
  assert.doesNotMatch(
    twentySecondNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentyThirdNote, /我把 R0\.22/);
  assert.doesNotMatch(
    twentyThirdNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentyFourthNote, /我利用一个极端面选择律/);
  assert.doesNotMatch(
    twentyFourthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentyFifthNote, /我把边界系数分解为尖锐与纵向分量/);
  assert.doesNotMatch(
    twentyFifthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentySixthNote, /我把两个尖锐端点族精确化为/);
  assert.doesNotMatch(
    twentySixthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentySeventhNote, /我把 R0\.26/);
  assert.doesNotMatch(
    twentySeventhNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentyEighthNote, /我消去了负边缘递推中的根式/);
  assert.doesNotMatch(
    twentyEighthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(twentyNinthNote, /我把两个尖锐输运数组/);
  assert.doesNotMatch(
    twentyNinthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtiethNote, /我不再截断/);
  assert.doesNotMatch(
    thirtiethNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtyFirstNote, /我把 R0\.30 的粗卷积上界/);
  assert.doesNotMatch(
    thirtyFirstNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtySecondNote, /我先从两变量边缘生成函数/);
  assert.doesNotMatch(
    thirtySecondNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtyThirdNote, /我检查了 R0\.32/);
  assert.doesNotMatch(
    thirtyThirdNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtyFourthNote, /我允许背景多项式/);
  assert.doesNotMatch(
    thirtyFourthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtyFifthNote, /我先检查局部 Taylor 圆盘链/);
  assert.doesNotMatch(
    thirtyFifthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtySixthNote, /我把 R0\.35 的半径损失/);
  assert.doesNotMatch(
    thirtySixthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtySeventhNote, /我给 Wiener 范数增加一个总次数权重/);
  assert.doesNotMatch(
    thirtySeventhNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtyEighthNote, /我把度数不超过 80 的精确多项式/);
  assert.doesNotMatch(
    thirtyEighthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(thirtyNinthNote, /我保留单项式之间的荷差与荷和/);
  assert.doesNotMatch(
    thirtyNinthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fortiethNote, /我不再对每个中心单项式分别选取最坏输入端点/);
  assert.doesNotMatch(
    fortiethNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fortyFirstNote, /我保留固定输入荷下所有中心单项式共同看到的斜率/);
  assert.doesNotMatch(
    fortyFirstNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fortySecondNote, /我改用 R0\.29 的正则分解/);
  assert.doesNotMatch(
    fortySecondNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fortyThirdNote, /我把已知条件/);
  assert.doesNotMatch(
    fortyThirdNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
});
