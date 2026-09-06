# 完整历史检查：原文接口和量词匹配

2026-09-06。**PRIMARY SOURCE RECORD / LIMITED IMPORT / NOT CLAY。**

## 1. KNSS 的 kernel 与 mild 接口

本轮重新检查 Koch、Nadirashvili、Seregin、Šverák 的
[arXiv:0709.3599](https://arxiv.org/abs/0709.3599)。
实际原件仍是作者 2007 预印本：
`/tmp/ns-strategy-primary.TEj0ZX/knss-2007.pdf`，26 页、231150 bytes，
SHA `5d86444c4c34bcad3642b2087a69b98d265f6da0e366bd50621d4ce792abc9f2`。

完整重读 PDF 页 6–13、18–20，覆盖第 3–4 节及本节使用的第 6 节
提取段；视觉检查页 7、10、11、19。Stokes 的散度源核可积，
而裸 Leray 投影并不是 \(L^\infty\) 有界算子。终点统一速度界
由局部 mild 延拓给出，不能仅凭剩余寿命长度假定。BI 另证了周期
核和全空间提升接口；内部平滑与紧性仍明确引用标准外部结果。

本轮作者 PDF 网页重开超时，本地字节与上一轮哈希一致；arXiv
版本条目重新访问成功。不把网络重开失败称为来源消失或换版。

## 2. Albritton–Barker：准确条件先于应用

Dallas Albritton、Tobias Barker，*On local Type I singularities of
the Navier–Stokes equations and Liouville theorems*，
[arXiv:1811.00502v2](https://arxiv.org/abs/1811.00502v2)，2019-11-18
提交修订，PDF 题头为 November 19, 2019；期刊 J. Math. Fluid
Mech. 21:43 (2019)，[DOI](https://doi.org/10.1007/s00021-019-0448-z)。

实际下载的 arXiv v2 为
`/tmp/ns-strategy-primary.TEj0ZX/albritton-barker-typei-v2.pdf`，15 页、
183358 bytes，SHA
`fbaf90712190e3aa2c700af7d1fd4c79c5dafdc1b98b3a3cce1af3992c9d3c66`。
主审完整读取 15 页，包括正文、脚注和参考文献；视觉核验页 2–4
的 Theorems 1.1/1.2、\(I\) 的定义和 Type I 区别。

本轮仅将 Theorem 1.2 的准确陈述用作适用条件对照：同一个
全空间 mild 古老解，在一列趋向负无穷的时刻具有统一全空间
\(L^3\) 界，才有该零解结论。本文的 Theorem 1.1 使用全部
抛物球上的尺度不变预算 \(I<\infty\)，不是只有速度有界；
Remark 3.2 还区分速度 Type I 的正向与反向用途。

完整阅读不等于完整依赖复核。弱 \(L^{3,\infty}\) 解理论、
向后唯一性、临界空间扰动论及其他外引结果没有全部重新证明。
这里不把 Theorem 4.1 的更一般 Besov 距离版本或 Theorem 1.1
的反向构造当成本项目已核验可用的无假设出口，也不据此构造奇点。

## 3. 为什么初始胞范数不满足该接口

BI 的缩放给每个 \(k\) 的初始胞 \(L^3\) 范数恰等于固定
\(u_0\) 的 \(L^3\) 范数；速度振幅三次方与空间 Jacobian
准确抵消。但这些时刻是 \(-b_k\)，随 \(k\) 离开每个紧时间
区间。局部极限并不在这些变动时刻受到收敛控制。

要用 Fatou 与扩张球得到极限 \(v(\tau)\) 的全空间界，应先在
一个固定极限时刻 \(\tau\) 给 \(v_k(\tau)\) 的尺度一致胞
\(L^3\) 上界，再令 \(k\to\infty\)，最后扩大空间球。
目前只由 record 和能量得到
\(\|v_k(\tau)\|_3^3\le M_kE_0\)，它随 \(k\) 增长。
这里说明现有估计不足，不证明所有可能的 NS 改进均不成立。

此外，非零周期提升的全空间 \(L^3\) 积分无穷，不能省略“胞”
与“全空间”的区别。Theorem 1.2 所需的是单个极限解的一列
时刻，不是一个三角形序列的各自初值。不得交换两种量词。

本次检索限于 KNSS 的后续 Type I／古老解接口，未做穷尽式
新颖性检索，也未完成 Deep Research 工作流。原始 PDF 和渲染
只作本地阅读证据，不作为公开资产再分发。无新读者 PDF。
