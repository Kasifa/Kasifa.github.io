# R0.73C `interval_monodromy` 严格证明审计

**审计对象：** `research/r073c_interval_monodromy.py`  
**当前审计快照：** 2026-08-30，443 行；SHA-256 为
`b1bdd458a75608c01f0fca64b95c217bb9f1fc01e084e14d641650e7e2b6a1fc`。
最初审计的 382 行快照是 `23cca471...abd80`；后续修改只增加版本、源码绑定、
正式 bracket 门和实时进度，下面审过的数学核心没有改变。  
**审计范围：** Taylor 区间余项、整步 Picard enclosure、monodromy
实迹与周期判据，以及 Rayleigh 相速度到时间特征值的符号。  
**状态约定：** `THEOREM` 表示不依赖浮点计算的解析事实；
`VALIDATED-CODE, conditional` 表示代码逻辑正确但依赖区间算术内核；
`COMPUTATIONAL` 表示必须由源锁定输出给出的事实；`OPEN` 表示本程序没有证明。

## 1. 审计结论

在当前 443 行版本中，我没有发现上述四个数学环节里的局部致命错误：

1. 程序把复二阶方程拆成十二维**实自治系统**，因此逐实分量使用
   Lagrange 型 Taylor 余项是合法的；`order=p` 时，程序保留到
   \(p-1\) 阶并用整步 tube 上的正规化 \(p\) 阶导数乘 \(h^p\)，阶数没有错一位。
2. `picard_enclosure` 实际检查
   \(X+[0,\bar h]\,[F](Z)\subset Z\)。在本问题 \(\eta>0\) 时向量场光滑，
   这个自映射条件足以覆盖整个闭步，不只是终点。
3. 对精确 ODE，monodromy 的行列式严格为一；利用
   \(W(2\pi-x)=-W(x)\) 可严格推出其迹为实数。因此非零周期解等价于
   \(\operatorname{tr}M=2\)，不是数值近似。
4. 对本项目冻结的算子号约定，\(c=i\eta\)、\(\eta>0\) 对应
   \(\sigma=-i\gamma c=\gamma\eta>0\)。脚本分母 `W-i*eta` 的符号与增长方向一致。

最初指出的发布级封装阻塞现在已经解除：当前主程序严格检查
`mpmath==1.3.0`，记录自身与四个算术源文件的 SHA-256，`--require-bracket`
对两个有序端点、严格异号和虚迹含零作 fail-closed 检查，并逐步刷新进度文件。
此外，完全不导入主程序或 `mpmath` 的 Decimal 独立内核已经用
`ROUND_FLOOR/ROUND_CEILING`、Machin 公式和独立的 Picard--Taylor 实现复算
通过。它给出同一对严格异号，并记录于
`experiments/r073c/decimal_interval_validation.json`。因此把正式端点证书与
下面第 4--5 节的解析桥接合并后，C4 的“至少存在一个正实冻结特征值”已经闭合；
根唯一性、代数单性和后续非自治传递仍未由此得到。

## 2. ODE 与区间 Taylor 余项

### 2.1 精确自治系统（THEOREM）

固定 \(\gamma=1/2\)、\(\mu=\gamma^2=1/4\) 和 \(\eta>0\)，令

\[
 a_\eta(x)=\mu+\frac{W''(x)}{W(x)-i\eta}
 =p_R(x)+ip_I(x),
\]

其中

\[
 p_R=\mu+\frac{W''W}{W^2+\eta^2},\qquad
 p_I=\frac{W''\eta}{W^2+\eta^2}.
\]

这正是脚本第 128--144 行使用的符号。令

\[
 s_1=\sin x,\ c_1=\cos x,\quad
 s_2=\sin 2x,\ c_2=\cos 2x,
\]

再把两个基本解列的 \((\phi,\phi')\) 各拆成实部、虚部，便得到脚本的十二维
实自治方程 \(z'=F_\eta(z)\)。因为

\[
 W(z)^2+\eta^2\ge \eta^2>0,
\]

沿精确状态以及任何实区间盒都没有真正的极点；自然区间扩张中的分母下端也
严格为正。由初值

\[
 (s_1,c_1,s_2,c_2)=(0,1,0,1)
\]

可唯一恢复所需的三角系数。这个自治化很重要：余项点 \(\xi\) 处的高阶导数
只依赖状态 \(z(\xi)\)，不再漏掉显式的时间变量。

### 2.2 正规化导数递推（VALIDATED-CODE, conditional）

记正规化 jet 为

\[
 z^{[k]}=\frac{1}{k!}\frac{d^kz}{dx^k}.
\]

若 \(D(t)=\sum_{j\ge0}d_jt^j\)、\(E(t)=D(t)^{-1}\)，则

\[
 e_0=d_0^{-1},\qquad
 e_n=-e_0\sum_{j=1}^n d_j e_{n-j}.
\]

这与 `series_reciprocal` 第 169--183 行完全一致。卷积、常数
\(\eta^2\) 只加入零阶系数，以及从 RHS 的 \(n\) 阶系数除以 \(n+1\) 得到
状态的 \(n+1\) 阶系数，也都正确。因此对每个点状态 \(z_0\)，
`taylor_coefficients(z0,eta,p)` 给出的第 \(k\) 项就是 \(z^{[k]}(0)\)；
把 \(z_0\) 换成区间盒 \(Z\) 后，自然区间运算给出所有 \(z_0\in Z\) 的包含。

程序在 `validated_step` 中采用

\[
 P_{p-1}(h)=\sum_{k=0}^{p-1}z^{[k]}(0)h^k,
\qquad
 R_p(h)=h^p z^{[p]}(\xi),\quad 0<\xi<h.
\]

`launch` 计算到 \(p-1\) 阶，`remainder` 在整步 enclosure 上计算到 \(p\) 阶，
第 307 行再乘 `step**order`；这正是逐实分量 Taylor 定理的余项。不同分量可以
有不同的 \(\xi\)，区间盒同时覆盖它们即可。程序并没有对一个复函数误用“复数
Lagrange 中值定理”，因为实、虚部从一开始就是不同的实状态分量。

**判定：余项公式合法。** 条件仅是整个精确轨道确实在传给
`taylor_coefficients(enclosure,...)` 的盒中；这由下一节给出。

## 3. Picard enclosure 是否覆盖整步

令 \(X\) 是一步起点区间，\(I=[0,\bar h]\)，\(Z\) 是候选盒，\([F_\eta](Z)\)
是 RHS 的自然区间扩张。脚本第 280--285 行验证的恰是

\[
 \boxed{X+I[F_\eta](Z)\subset Z.}\tag{3.1}
\]

对任一精确起点 \(z_0\in X\)，Picard 算子

\[
 ({\cal T}u)(t)=z_0+\int_0^tF_\eta(u(s))\,ds
\]

把 \(C(I,Z)\) 映入自身：每个分量的积分都包含在
\(I[F_\eta](Z)\) 中。\(Z\) 是闭凸紧盒，\(F_\eta\) 在其邻域连续且局部
Lipschitz；由标准 Picard/Schauder 存在论和局部唯一性，精确解在整个
\(I\) 上都属于 \(Z\)。因此这里使用非严格集合包含也足够；如果采用一套只接受
严格 interior inclusion 的外部验证库，则可再膨胀一个 ulp，但这不是当前
数学论证的漏洞。

第 265--279 行的 Euler hull 和 \(64h^2\) padding 只负责寻找候选 \(Z\)。
常数 64 无需先验证明：padding 不够时 (3.1) 不成立，程序在八次尝试后抛出
异常，而不会返回伪 enclosure。`zero_to_step=[0,step.b]` 覆盖完整正步；不是
只在 \(t=h\) 检查终点。

总长度方面，当前版本用向外舍入的 `2*iv.pi`，令
\(H=(2[\pi])/N\)。真正的 \(h=2\pi/N\) 属于 \(H\)。每一步独立使用同一
区间 \(H\) 会丢失相关性并加宽结果，但所需的 \(N\) 个相同步长序列仍是被包含
情形，所以最后结果包含恰在 \(x=2\pi\) 的基本矩阵。

**判定：整步 enclosure 逻辑充分。** 它依赖的计算假设是所载入的
`mpmath.iv` 对加减乘除、整数幂和 `iv.pi` 确实向外舍入。

## 4. 实迹与周期判据的精确矩阵推导

令

\[
 B_\eta(x)=
 \begin{pmatrix}0&1\\a_\eta(x)&0\end{pmatrix},
 \qquad Y'=B_\eta Y,\qquad Y(0)=I_2,
\]

并记 \(R=\operatorname{diag}(1,-1)\)。由于

\[
 W(2\pi-x)=-W(x),\qquad W''(2\pi-x)=-W''(x),
\]

当 \(\eta\in\mathbb R\) 时

\[
 a_\eta(2\pi-x)=\overline{a_\eta(x)},\qquad
 B_\eta(2\pi-x)=-R\overline{B_\eta(x)}R.\tag{4.1}
\]

记半周期传递矩阵

\[
 H=\Phi(\pi,0),\qquad K=\Phi(2\pi,\pi),\qquad M=KH.
\]

对第二半段的任一解 \(y\)，函数
\(z(t)=R\overline{y(2\pi-t)}\) 由 (4.1) 满足第一半段同一个方程。比较
\(t=0,\pi\) 即得

\[
 \boxed{K=R\overline H^{-1}R.}\tag{4.2}
\]

另一方面 \(\operatorname{tr}B_\eta=0\)，故 Liouville 公式给出

\[
 \det H=\det K=\det M=1.\tag{4.3}
\]

写

\[
 H=\begin{pmatrix}a&b\\c&d\end{pmatrix},\qquad ad-bc=1.
\]

由 (4.2)

\[
 K=
 \begin{pmatrix}\bar d&\bar b\\\bar c&\bar a\end{pmatrix},
\]

于是

\[
 \operatorname{tr}M
 =\bar da+\bar bc+\bar cb+\bar ad
 =2\operatorname{Re}(\bar da+\bar bc)\in\mathbb R.\tag{4.4}
\]

这是真实精确轨道的代数恒等式，不是因为数值输出的 `traceImag` 很小。

存在非零 \(2\pi\)-周期解当且仅当 \(Mv=v\) 对某个 \(v\ne0\) 成立，即

\[
 0=\det(M-I)=\det M-\operatorname{tr}M+1
 =2-\operatorname{tr}M.\tag{4.5}
\]

因此

\[
 \boxed{\phi\text{ 非零且周期}\iff\operatorname{tr}M=2.}
\]

这里必须使用精确的 (4.3)。仅凭一个数值 determinant “接近 1”不能把
周期条件化成 `trace=2`；当前脚本虽然不输出 determinant，但解析恒等式已经
提供所需桥接。

## 5. Rayleigh 特征值符号与异号端点的严格含义

冻结算子为

\[
 A_\gamma=-i\gamma\bigl(W+W''\mathcal L_\mu^{-1}\bigr),
 \qquad \mathcal L_\mu=-\partial_x^2+\mu,
 \qquad \mu=\gamma^2.
\]

令 \(q=\mathcal L_\mu\phi\)。从 \(A_\gamma q=\sigma q\) 出发，定义

\[
 \sigma=-i\gamma c.
\]

则

\[
 W\mathcal L_\mu\phi+W''\phi=c\mathcal L_\mu\phi,
\]

等价于

\[
 (W-c)(\phi''-\mu\phi)-W''\phi=0,
\]

也即

\[
 \phi''=\left(\mu+\frac{W''}{W-c}\right)\phi.\tag{5.1}
\]

脚本取的正是 \(c=i\eta\)。所以

\[
 \boxed{\sigma=-i\gamma(i\eta)=\gamma\eta>0}\tag{5.2}
\]

而不是 \(-\gamma\eta\)。当 \(\gamma=1/2\) 时，\(\sigma=\eta/2\)。

定义真实函数

\[
 f(\eta)=\operatorname{tr}M(\eta)-2,
 \qquad \eta>0.
\]

由 (4.4) 它取实值；由 (5.1) 的系数对 \(\eta>0\) 光滑依赖，\(f\) 连续。
因此只要源锁定区间计算在两个有序正端点上证明

\[
 [f](\eta_-)<0,\qquad [f](\eta_+)>0
\]

（反向符号也一样），中值定理便给出某个
\(\eta_*\in(\eta_-,\eta_+)\) 满足 \(f(\eta_*)=0\)。由第 4 节存在非零周期
\(\phi_*\)；因 \(\mathcal L_\mu>0\)，\(q_*=\mathcal L_\mu\phi_*\ne0\)，并由
(5.2)

\[
 \sigma_*\in\left(\frac{\eta_-}{2},\frac{\eta_+}{2}\right)\subset(0,\infty)
\]

是 \(A_{1/2}(0)\) 的真实正点谱。因为它位于纯虚的 multiplication essential
spectrum 之外，它还是孤立特征值。这个论证只证明至少一个根；不证明唯一性、
代数单性或 Riesz 投影常数。

## 6. 证书状态更新与剩余加固项

### 6.1 最初阻塞项的处理状态

1. **依赖版本门：已解除。** 主程序第 373--377 行拒绝非 1.3.0 的
   `mpmath`；正式 JSON 记录 Python、平台和实际版本。
2. **源码与算术内核绑定：已解除。** 主程序记录自身 SHA-256，并记录
   `ctx_iv.py`、`libmpi.py`、`libmpf.py`、`libelefun.py` 的字节数与哈希。
3. **bracket fail-closed：已解除。** `--require-bracket` 要求恰好两个有序
   端点、严格相反符号，且两个虚迹区间都包含零；否则程序异常退出，不写
   `status=passed`。
4. **实时进度：已解除。** `record_progress` 每个检查点向 stderr 和 NDJSON
   追加并 flush，不再等到整轮结束。
5. **独立算术内核：已解除。** 
   `experiments/r073c/independent_decimal_monodromy_validator.py`
   不导入主程序或 `mpmath`；它自写 Decimal 区间四则、Machin--arctan
   \(\pi\) 包围、十二维 RHS、Picard box 和 Taylor 余项。80 位正式输出在
   \(\eta=0.3407\) 给出严格负区间，在 \(\eta=0.3410\) 给出严格正区间；
   虚迹含零、determinant 含 \(1+0i\)、有限性、版本和源码前后哈希门全部通过。
6. **解析桥接：已解除。** 本文第 4--5 节以及
   `research/r073c_monodromy_proof.md` 明确给出实迹、determinant-one、
   周期判据和 \(\sigma=-i\gamma c\) 的推导。

### 6.2 不影响当前 C4 存在性结论的加固项

- 每步记录 Picard closure 所用 attempt、各分量 containment slack、分母下界和
  区间是否有限；这样独立验证器不必把整个 Python 控制流作为黑箱信任。
- 主程序仍可输出完整 \(2\times2\) monodromy 区间并检查
  \(1\in[\det M]\)。后者不是 (4.5) 的证明替代品，但能发现列顺序、trace 索引和
  积分错误；独立 Decimal validator 已经执行这一哨兵。
- 可以只严格传播半周期 \(H\)，再用 (4.2) 组装 \(M\) 和实迹；这会把 PT 对称
  直接编码进证书并明显减小虚部与整周期 wrapping。
- 当前已有两组不同 `(steps, order, dps)` 的主证书和一组不同内核的 Decimal
  证书。后续若改变端点，只需保持同样的三路 fail-closed 结构。

## 7. 最终 claim boundary

| 命题 | 本审计结论 |
|---|---|
| 每一成功步骤包含精确整步流 | `VALIDATED-CODE, conditional on mpmath.iv` |
| Taylor 尾项阶数与使用区域正确 | `VALIDATED-CODE, conditional on mpmath.iv` |
| 精确 monodromy 迹为实、determinant 为一 | `THEOREM` |
| 周期解当且仅当 trace 为二 | `THEOREM` |
| \(c=i\eta\) 给出 \(\sigma=\gamma\eta>0\) | `THEOREM` |
| 两端严格异号蕴含正实点谱 | `THEOREM, conditional only on certified endpoint signs` |
| 主证书加 Decimal 独立证书与解析桥接闭合 C4 存在性 | **是** |
| 单个主源文件脱离解析桥接即可证明点谱 | 否；周期与符号引理仍是证明的一部分 |
| 根唯一、特征值简单、投影有界 | `OPEN in this script` |
| 非自治快时传递 C5 | `OPEN` |
| 非线性 Navier--Stokes / Clay 结论 | `OPEN` |
