# 真实压力功短窗：有限文献碰撞核查

2026-09-06。**LITERATURE / LOCAL CLAIM BOUNDARY / NO NOVELTY CLAIM。**

本项要比较的是 AI/AJ 的精确量词：光滑、三维周期、黏性 1、固定初始
\(L^2\) 能量，时间 \(\tau_0\epsilon^{5/2}\) 内有固定相对 \(L^3\) 三次方
增长，而累计梯度平方趋于零。仅“范数增长”四个字不足以判断是否同一结果。

r076l_figure_audit 作了有界原始文献检索。根任务实际打开并读取以下三篇
所列位置；没有把其他候选文献的代理摘要当作已经核对的来源。
本次不是三篇论文全证明的重新审稿，也不是穷尽性新颖性检索。

## 1. 压力功与 moderator 已有直接先例

Tran--Yu 的 [Regularity of Navier–Stokes Flows with Bounds for the Pressure](https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/12230/Tran_2016_Regularity_AML_AAM.pdf?isAllowed=y&sequence=1)，
根任务核对作者稿第 2--3 页，式 (5)、Lemma 1 及式 (6)--(8)。
它在全空间衰减 NS 中写出 \(L^q\) 压力功，并给出一类不贡献该积分的
pressure moderator。不能把这些恒等式或消去机制当作本项新发现。
这里未调用它的后续条件正则性定理，也未从 moderator 推出 AJ 的反例。

## 2. 不称为临界空间 norm inflation

Bourgain--Pavlović 的 [Ill-posedness of the Navier–Stokes Equations in a Critical Space in 3D](https://arxiv.org/pdf/0807.0882)，
根任务核对第 1--4 页，尤其 Theorem 1.1、空间定义及解的分解；
并核对第 6 页的高频初值形式。
定理陈述在全空间 NS 的负阶 Besov 空间
\(\dot B^{-1,\infty}_\infty\) 中，以任意小初值产生任意短时的大同范数值。
这是该空间在原点的解映射问题，不是 AJ 的 \(L^3\) 相对增长命题。

AJ 的 \(H_\epsilon(0)\) 本身发散，也没有证明 \(L^3\) 小数据的解映射
不连续。因此，本项不使用“\(L^3\) norm inflation”或“临界空间不适定”
来描述自己的结论。此处仅比对定理陈述和机制，不重审该文全证明。

## 3. 固定涡量平方与固定速度能量不同

Kang--Yun--Protas 的 [Maximum Amplification of Enstrophy in 3D Navier–Stokes Flows](https://arxiv.org/pdf/1909.00041)，
根任务核对 §3 的 Problem 3.1、§5 中式 (32) 的 \(L^3\) 定义与跟踪对象，
以及 §6 关于数值优化方法和范围的说明。
该计算工作固定初始 enstrophy，在给定时间优化终端 enstrophy。
它与 AJ 的固定初始速度 \(L^2\) 能量不是同一约束；
AJ 允许初始梯度平方随 \(\epsilon^{-2}\) 发散。

该文提供的是相关数值研究背景，不是 AJ 量词的证明或反证。
本项也没有复现其仿真、读取其全部图像或采用其数值趋势证明正则性。

## 结论与发布边界

以上三篇的已核对陈述没有直接等同于 AJ.27--AJ.30。
这只是一份有限碰撞记录，不支持首创、优先权、论文等级或接近 Clay 的判断。
AI 的高频调制和 AJ 的短时低黏性估计使用标准解析工具；
本项价值暂定为识别一条精确候选估计的失效范围。

AI/AJ 的数学实际文件审查已完成，有限文献记录也已落盘。
本材料与 report-source、完整文件/依赖清单、哈希和冻结提交共同组成
合并研究包；冻结状态由 manifest 绑定，不由此文献记录单独认定。
短窗严格早于成熟扩散时间，原合同 G 仍 OPEN。
