# 周期压力机制与能量类筛查：审查记录

2026-09-06。**PASS IN STATED SCOPE / INDEPENDENT MODEL REVIEW / G OPEN / NOT CLAY。**

## 作者与独立性

BF 作者是主代理；非作者 `/root/r076l_proof_audit` 完整读取实际
文件并重新推导。BG 作者是 `/root/r076l_proof_audit`，主代理参与
问题与核心涡量检查的提出，不把主代理计作 BG 的独立审稿人。
BG 的独立全文审查由非作者 `/root/r076l_figure_audit` 完成。
主代理完整读 BG、复算两份证明并检查最终修改。

这是独立模型代理复核，不是外部同行评审。下列哈希对应实际接受
的最终文件；未把早期 PENDING 字样倒改成历史上已完成的状态。

| 源稿 | SHA256 | 行 / bytes | 标签 |
| --- | --- | --- | --- |
| `clay_b_periodic_radial_pressure_identity_20260906.md` | `20ff518eddb94f9a4b120ce2b7caaf6e9318d3c3d7bbb6310d8fde764c17664b` | 238 / 7281 | BF.1–15 |
| `clay_b_pressure_potential_energy_screen_20260906.md` | `05546f98e5afffa9093c78c95c771428d783cfc36281c82f4d0b87d62c508efb` | 332 / 10005 | BG.1–22 |

## BF 的实际复核

由周期 Green 方程得 \(\Delta H=V_{\mathbb T}^{-1}\)，从而其
Hessian 每个分量调和。内外径向卷积的常数、球面一阶匹配、没有
原点或球面 delta 的 Hessian、两个权重的质量均重新核对。
\(w\in L^2\) 和 \(G*w\in H^2\) 允许分布自伴配对，不依赖
错误的奇异核绝对 Fubini。两种权重给出同一个 \(4\pi R^2\)
修正，因此固定外尺度的 \(\mathcal C\) 真正与 \(R\) 无关。

压力 gauge 增量为 \(4\pi cR^2\)。环带核的算子范数不超过
\(2/r^3\)，所以其粗界为 \(2M^2/R\)，没有误报为低阶项。
非负核心的单调性和 BF.14–15 的不等号都正确。证明只依赖
瞬时 Poisson 关系，不提供 NS 演化或时间连续性。

## BG 的实际复核

有限 \(L^q\) Riesz、零均值 Sobolev、两种径向核范数和时间幂
计算正确，可数稠密中心及半径保证上确界可测。这里给出了两套
充分上界，不主张 \(L_t^{4/3}\) 是能量类可能达到的最优时间指数。
严格否定的是时间一致控制和有限左连续迹的自动推断。

旋转种子无散、零均值且径向速度为零；原点的压力 Hessian delta
项因 \(V(0)=0\) 消失。主值积分严格为负，光滑周期修正保持
\(O(M_0^2)\)，而主压力为 \(\epsilon^{-3}p_V\)，局部势下界为
\(cM_0^2/\epsilon\)。固定静态场仍满足有限的 C 型控制，只有
固定能量的整族没有统一逐时常数。

时间族取 \(0<\alpha<1/2\)，则总梯度能量有限、\(E_* >0\)，
缩支撑给弱连续终点零值，能量关系在终点变成不等式。核心涡量的
三个空间项均为零，而 \(A'/A\) 最终为正，所以它明确违反 NS
涡量方程。没有给该族附加未验证的局部能量、suitable 或弱 NS
资格，亦不将它写成 NS 奇点反例。\(\nu=1\) 及一般黏性换算已明示。

## 文献与报告范围

非作者实际全文范围审查接受：

- `clay_b_pressure_mechanism_primary_reading_20260906.md`：SHA `888d834803b8c018630892cf136ee1247803933c629bf9b75655c5b9e1b4e1a3`，67 行 / 4159 bytes。
- `clay_b_pressure_mechanism_screen_report_20260906.md`：SHA `2eb627e33ffebfeb49b0ddb7d40f1d6cf23ab7c15f720974a6299e291a7f2de4`，55 行 / 2785 bytes。

独立核对正式 PDF 的身份与 22 页数；视觉核对正式版的外球
\(R\to\infty\) 和两分支的 \(\varepsilon_*(1)\)。主代理完整读
§2–§4 的范围明确，外引文献未全文重审；\(\theta^k\rho\) 的
局部迭代记号校正不被扩大为对原定理的否定。报告不宣称新颖性、
NS 反例、Q/G 闭合或 Clay 进展。

## 可复现来源与算术检查

`scripts/clay_b_pressure_mechanism_screen_qa.py` 只读检查四份源文本、
37 个标签、25 个 Fraction 表达式及前一冻结包 65 行源提交和工作树
字节、哈希、大小；另核对复用 AH 源。两次实时输出及记录 JSON
逐字节一致。

非作者以独立 Ruby `Rational` 表达式重新计算了 25/25 项，不以
读取 Python 输出相等代替复算。初版脚本另以进程内常量突变测试
错误源哈希和错误前序 manifest 哈希，均 FAIL/exit 1。末次只有 BG
正文重音拼写及对应哈希绑定变化；非作者接受增量，并在最终脚本
再次确认两次实时输出与记录一致。主代理另在最终脚本重跑两项
哈希负控，均被拒绝。负控未修改磁盘文件。

最终脚本 SHA `fdff2f0b32be7aa1de3250d584ba9091c5df99a21ea618f9bdbc618e8365139b`；
QA JSON SHA `fbd5a7792c8314ed618fda081d4b37a16a9c56bc011b46a67c65578c7d14bbe9`。
这些是来源与有理算术检查，不是 PDE 自动证明证书。最终冻结清单
另绑定本审查记录和全部研究依赖，不把自查重复计作独立数学审查。

Q、净压力功上界、G、一般正则性与新颖性仍 OPEN。没有仿真、
科学图、DGX、新读者 PDF、第三方 PDF 再分发或部署验收声明。
