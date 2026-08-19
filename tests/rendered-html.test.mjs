import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
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

test("ships the complete Chinese research review as static HTML", async () => {
  const html = await readFile(siteUrl, "utf8");

  assert.match(html, /<html lang="zh-CN">/);
  assert.match(html, /Navier–Stokes 开放研究日志/);
  assert.match(html, /这个问题要求证明什么/);
  assert.match(html, /目前已经知道什么/);
  assert.match(html, /接下来的工作计划/);
  assert.match(html, /当前研究进展/);
  assert.doesNotMatch(html, /08 \/ Selected sources|id="references"/);
  assert.doesNotMatch(html, /id="publish"|href="#publish"|Open publication/);
  assert.doesNotMatch(html, /codex-preview|SkeletonPreview|react-loading-skeleton/);
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
  const [home, firstNote, secondNote, thirdNote, fourthNote, fifthNote, sixthNote, seventhNote, eighthNote, ninthNote, tenthNote, eleventhNote, twelfthNote, thirteenthNote, fourteenthNote, fifteenthNote, sixteenthNote, seventeenthNote, eighteenthNote, nineteenthNote, twentiethNote, twentyFirstNote, twentySecondNote, twentyThirdNote, twentyFourthNote, twentyFifthNote, twentySixthNote, twentySeventhNote, twentyEighthNote, twentyNinthNote, thirtiethNote, thirtyFirstNote, thirtySecondNote, thirtyThirdNote, thirtyFourthNote, thirtyFifthNote, thirtySixthNote, thirtySeventhNote] = await Promise.all([
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
  ]);

  assert.match(home, /这是我整理的/);
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
});
