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

test("ships the complete Chinese research review as static HTML", async () => {
  const html = await readFile(siteUrl, "utf8");

  assert.match(html, /<html lang="zh-CN">/);
  assert.match(html, /Navier–Stokes 开放研究日志/);
  assert.match(html, /这个问题要求证明什么/);
  assert.match(html, /目前已经知道什么/);
  assert.match(html, /接下来的工作计划/);
  assert.match(html, /当前研究进展/);
  assert.match(html, /08 \/ Selected sources/);
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
  const [home, firstNote, secondNote, thirdNote, fourthNote, fifthNote, sixthNote, seventhNote, eighthNote, ninthNote, tenthNote, eleventhNote, twelfthNote, thirteenthNote, fourteenthNote, fifteenthNote, sixteenthNote, seventeenthNote, eighteenthNote, nineteenthNote, twentiethNote, twentyFirstNote, twentySecondNote, twentyThirdNote] = await Promise.all([
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
});
