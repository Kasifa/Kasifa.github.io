# Clay-B 桥梁重排：原始来源与判断记录

日期：2026-09-05。读者：本项目研究者及后续独立审稿人。
范围：指定中心好尺度合同、两尺度路径预检和局部化外力接口；
不评估解决 Clay 的概率，不作整仓认证或新颖性声明。

## 直接结论

I 的正则性出口、P 的固定尺度弱稳定性、R 的条件提取蕴含可保留。
尚未闭合的是原方程如何在同一候选中心强制产生好尺度。
本轮把最终量词、尺度预算和误差项写清；粗能量路径比较留下
D_J/R 的速率缺口。已有临界正则性文献没有自动提供这个输入。

## 主张—原始来源账

| 主张及实际用途 | 原始来源、日期与定位 | 本轮读取与边界 |
|---|---|---|
| 最终任意初值、无外力周期命题 | Charles L. Fefferman, Existence and Smoothness of the Navier--Stokes Equation，Clay 官方文本，问题 B 和末页勘误；[PDF](https://www.claymath.org/wp-content/uploads/2022/06/navierstokes.pdf) | 主代理与文献审查均读；包含周期压力，不附加零均值 |
| I 的速度一尺度出口 | Yanqing Wang, Gang Wu, Daoguo Zhou, A regularity criterion at one scale without pressure for suitable weak solutions to the Navier--Stokes equations；作者版 v1，2018-11-25，Theorem 1.1；[PDF](https://arxiv.org/pdf/1811.09927) | 主代理读具体定理；delta=1/2；只借正则性出口，不宣称小性已由 NS 产生 |
| 周期局部 H^1 理论 | Terence Tao, Localisation and compactness properties of the Navier--Stokes global regularity problem，Analysis & PDE 6(1), 2013, 25--107，DOI 10.2140/apde.2013.6.25；Theorem 5.1；[出版 PDF](https://msp.org/apde/2013/6-1/apde-v6-n1-p02-s.pdf) | 主代理读均值条件、局部存在、唯一与正则条款；全局 suitable 周期 continuation 的构造未在本轮从头复证，不拿该文全空间段代替 |
| 临界有界性之后的定性出口 | Escauriaza, Seregin, Sverak，L_{3,infty}-solutions of the Navier--Stokes equations and backward uniqueness，Russian Math. Surveys 58(2), 2003, 211--250，Theorems 1.3/1.4；[原文](https://www.mathnet.ru/php/getFT.phtml?jrnid=rm&option_lang=eng&paperid=609&what=fullteng) | 混合范数为空间 L^3、时间 L^infty，不是空间弱 L^3。全空间全局/固定柱体局部结果，不生成当前所需临界控制 |
| averaged-NS 区分检验 | Terence Tao，Finite time blowup for an averaged three-dimensional Navier--Stokes equation，arXiv:1402.0290，2014-02-03，v3 2015-04-01；[PDF](https://arxiv.org/pdf/1402.0290) | 主代理复读引言 pp.4--5 的结构边界；独立审查核验构造与量词。不把全空间修改方程的爆破称为本周期原方程的反例 |
| 临界控制的定量出口 | Terence Tao，Quantitative bounds for critically bounded solutions to the Navier--Stokes equations，arXiv:1908.04958，2019-08-14，v2 2020-07-10，Theorem 1.2；[PDF](https://arxiv.org/pdf/1908.04958) | 对经典全空间无外力解，以 L_t^infty L_x^3 界为假设，给 j=0,1 的三重指数界。更高导数见作者 remark，未作此处输入 |
| 强外力范数与局部化模板 | Tobias Barker, Henry Popkin，Quantitative estimates for the forced Navier--Stokes equations and applications，arXiv:2602.09951v1，2026-02-10，Proposition 3.0.5、Lemma 4.2.1、(16)/(296)；[PDF](https://arxiv.org/pdf/2602.09951v1) | 独立审查与主代理定向核验。固定光滑领圈的外力模板有用，但不能从现有弱压力积分直接调用；完整代数及一个需补入项见 force ledger |

Barker--Popkin 的 arXiv 元数据日期是 2026-02-10，PDF 内日期
2026-02-11，实验 HTML 内显示 2026-08-24。记录此显示差异，不推断
未经核验的版本历史；按可读取的 v1 预印本引用，不写成同行评审论文。
其局部化所引用的更早论文没有在本轮逐篇复核。

## 本地证据的等级

合同与预检引用 I/P/R 的具体定义、结论及历史审查记录。
本轮重读了相关源段，独立审查重新核验了新合同的继承范围；
没有重跑全部历史证书，也没有声称全部旧证明已再审。

新路径估计是能量类场上的解析推导，不使用 PDE；
Reynolds 恒等式只在光滑真实 NS 区间使用；
截断外力是逐项乘积恒等式，独立复算后保留全部项。
这些均不代替 G 所需的动力学小尺度预算。

## 检索记录与停止

首轮按策略中的精确题名/标识直接读官方和作者来源。Tao 局部理论
的一个错误候选 1108.1161 返回编码理论文章，立即排除；
随后一次题名检索定位 1108.1165 和 MSP 出版 PDF。
文献审查分两阶段：关键范围比对；仅对 (296) 的疑似缺项作
一次 PDF/HTML 与独立代数复核。没有泛搜其它爆破宣称。

父级可见原始工具记录：
turn6180view0/1，turn6205view0，turn6207view0/1/2，
turn6209view0/2/3/4/5，turn6214view0，turn6216view0。
这些是内部检索定位，不应进入读者版。

当前停止检索：已足以决定没有一个可直接补齐 G 的已核验引理；
关键调用条件与未审边界均已列明。下轮以具体应力/压力命题为
问题再定向查询，不重新开始无界文献综述。

## 尚未解决的问题

没有从任意初值推出 E_R 小；没有跨尺度收缩；没有证明 R 的
例外壳与持留时间条件由原 NS 保证；没有排除真实 NS 奇点。
当前变化是量词与依赖清楚、一个粗推法的缺失速率明确、
以及局部化外力的准确调用账单，而不是新的全局正则性进展。
