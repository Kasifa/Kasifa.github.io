# 临界紧性、定常反例与无原子的原文核验

2026-09-06。**PRIMARY SOURCE READING / BOUNDED SCOPE / G OPEN / NOT CLAY。**

我只登记本小节实际使用的基础工具、存在性结果和附加条件比较。
没有进行穷尽性新颖性检索，没有把模型复核称为外部同行评审，
也没有声称调用了 Deep Research。

## 1. Euclidean 奇异积分工具

Terence Tao，2006 Math 247A：
[Notes 4](https://www.math.ucla.edu/~tao/247a.1.06f/notes4.pdf)，
PDF 30 页，287706 bytes，SHA256：
0c200b34c1c6c625be26443c467e789614214d9ed86826103822778d8a3b44dd。
主代理完整读 PDF 5--9 页，视觉核对 6--9 页：Definition 2.1/2.4、
Lemma 2.7、Corollary 2.9 的完整弱型证明及 Corollary 2.10。
BL.9 使用的是这一标准有限 \(p\) 工具。其 \(L^2\) 假设通过
\(-\xi_i\xi_j/|\xi|^2\) 验证，核正则性通过显式 Hessian 验证。
不把它当成周期定理，也不省略原点 delta 乘法项。

[Notes 3](https://www.math.ucla.edu/~tao/247a.1.06f/notes3.pdf)，
27 页，273778 bytes，SHA256：
265e56a519141feb06c02dabd5e90e2a466768ee1e4f924a3687e8651824647d。
完整读 PDF 22--24 页，视觉核对 23--24 页，涵盖所需的
Proposition 4.3 二进 Calderón--Zygmund 分解及其完整证明。
Lebesgue 微分、基本 \(L^p\) 插值与 Fourier 基础仍作为标准分析工具，
不声称在本小节重新建立全部实分析理论。

BL 的周期 Green 修正、空间 Sobolev 小证明和完整短窗紧性直接写在
正文；没有引用未经核对的 Aubin--Lions 版本来跨越终点。

## 2. Gavrilov 的非零定常 Euler 流

[A steady Euler flow with compact support，arXiv:1810.08020v1](https://arxiv.org/abs/1810.08020v1)。
[期刊官网](https://doi.org/10.1007/s00039-019-00476-6)
确认 GAFA 29，190--197，2019；官网全文付费，未读取期刊 PDF。
作者 v1 为 7 页，127347 bytes，SHA256：
fcaca85faa77e3876b11d16718037169fc026112dfd3e4248e03e963a0ebc3c9。

主代理完整抽读 7 页，并视觉核对 1、5、6 页。
筛查代理完整读首页定理、Lemma 4 与 §3，视觉核对 5--6 页；
非作者数学复核者完整抽读并视觉核对 1、4--6 页。
真正使用的是首页存在性定理与 §3 的压力截断局部化。
BM 单独检查紧支撑规范压力和目标类成员资格。
未重新证明 Lemma 1 调用的 Hille 解析 ODE 定理或全部外部依赖。
这是文献存在性结果，不是本项目新的 Euler 构造。

定常例否定宽 Euler 类的全零刚性；它不是固定初值 NS 缩放可达性
反例。圆周附近可以有非零常数压力；只要求压力整体紧支撑，
不能以“与速度支撑相同”为由删去这一部分。

## 3. 终端能量测度文献

Leslie--Shvydkoy，
[The Energy Measure for the Euler and Navier--Stokes Equations，v4](https://arxiv.org/abs/1705.04420v4)，
接受稿 26 页，597382 bytes，SHA256：
99fc3bbd772303c63e3c396c47adf47cb885032d1eb3de11201c6d68719ad22a。
主代理完整读 PDF 1--4、8、15--24 页，视觉核对 16、21、22 页。
涵盖全空间设定、测度定义、Prop.3.1、完整 §4、§5.1、
Thm.5.4 及证明中 Regions I/II 的完整步骤。
其余 Regions III--V 全部证明和外部 Onsager/Besov 依赖未重审。

本小节只采用如下准确比较：

- Prop.3.1/4.2 的有限空间指数弱时间界在 \(6/p+5/q<3\)
  给正维数；基本能量插值线不在这个区域。
- Thm.5.4 的强时间端点要区分区域。\(p=q=11/3\) 属于
  Region I，允许 \(d=0\)，所以真有无原子结论，不能只报零维数界。
- 时间 Type I 是额外速度假设，不是基本能量或原文局部 Type II
  定义的自动后果。原稿研究 \(\mathbb R^3\)，\(\Omega\) 是其中子域。

PDF 16 页印有“\(\beta>2\)”及对应 \(r^{-\beta}\)。
按 PDF 8 页定义，时间指数应满足
\(\alpha>2\iff3/p+2/q>1\)，且在三维 \(\beta=5-2\alpha\)。
我记录这一可见符号问题，不照抄，也不据此宣布整篇无效。
BN 的周期单点证明直接使用 \(r^{5/2}\)，不依赖这处文字。

Shvydkoy，
[A study of energy concentration and drain in incompressible fluids，v2](https://arxiv.org/abs/1205.1544v2)，
15 页，190924 bytes，SHA256：
7520a2b56b273cda443d7d3ef3b06a3c81d861745d8097a128457dac2dfbafc1。
主代理完整读 PDF 1、3--5、12--14 页，视觉核对 13 页；
涵盖 Theorem 2.1 的端点段、Lemma 2.2 的完整证明和完整 §4。
引用的自动 \(L^1_tL^\infty_x\) 外部证明、较高维浓集迭代和其他
自相似排除证明未完整重审，不作为本稿的额外已付输入。

Corollary 4.1 的强 \(L^{5/3}_tL^\infty_x\) 是真正的附加条件。
更一般的 (8) 还要求累计速度半径内的能量沿子列消失。
本轮没有证明这一缩球条件，也没有把弱端点换成强端点。

## 4. 本轮能接受的范围

两篇无原子论文的所查定理没有给当前任意有限能量周期原解一个
自动无原子结论；这只是有界筛查，不是对全领域现有文献的否定。
BN 单独证明一个额外强 \(L^{11/3}\) 条件下的周期小球版本，
其新贡献仅是当前记号和规范下的可审计重算，不宣称新颖性。

第三方 PDF 只作本地阅读证据，不进入网站资产或研究发布附件。
本轮没有新读者 PDF、仿真、科学图或 DGX。G OPEN，NOT CLAY。
