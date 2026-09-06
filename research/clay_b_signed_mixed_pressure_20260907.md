# 有符号混合压力功：投影测试和联合截断

2026-09-07。**CONDITIONAL / DIRECT METHOD AUDIT / NON-AUTHOR REVIEW PASS / G OPEN / NOT CLAY。**

BU 已经给出完整混合压力的小量。这一节不再证明同一范数结论，
而直接测试压力功。可以去掉粗估计中显式的幅度因子 \(R\)，
但代价是一个尚未支付的加权时间积分。
同时截断两个场可以合法控制交叉压力组合；它不能单独决定混合项。
本节仍在 BP/BU 的同一原解、额外正原子条件下，不构造或排除原子。

## 1. 投影恒等式给出不显含幅度的上界

沿用 BU 的 \(b=-u(T-\rho)\)、\(w=A(T-\rho)\)、
\(c=\sqrt m>0\)、\(z=b+cw\)，在固定周期胞、固定 \(\nu>0\) 上工作。
所有时间均为反时后的正时间 \(0<\rho\le L\)。
记 \(P\) 为全周期 Leray 正交投影，\(Q=I-P\)，并定义
\[
 g_R(v)=D\beta_R(v)=\frac{v}{\sqrt{1+|v|^2/R^2}},\quad
 J_R(v)=Dg_R(v),\quad
 r=\Pi(z,w),\quad p_z=\Pi(z,z),\quad p_w=\Pi(w,w).
 \tag{BV.1}
\]
压力均取周期零均值。\(\pi=r-cp_w\)、\(q=p_z-cr\)；
本节用 \(r\) 表示混合压力，不用它表示空间半径。

无散性和 \(\Pi(z,w)=\Pi(w,z)\) 给
\[
 \nabla r=-Q[(z\cdot\nabla)w],\qquad
 M_R:=-\int g_R(w)\cdot\nabla r
       =\int Qg_R(w)\cdot(z\cdot\nabla)w .
 \tag{BV.2}
\]
每个几乎处处的正时间，所有空间积分都合法：
三场在 \(H^1\)，压力梯度在 \(L^{3/2}\)，
且 \(Qg_R(w)\in H^1\subset L^6\)。
投影的对偶配对先对光滑场成立，再用有限指数和 \(H^1\) 逼近传递。
没有把局部压力当作全周期投影。

径向梯度测试还给
\[
 \int g_R(w)\cdot(z\cdot\nabla)w
       =\int z\cdot\nabla\beta_R(w)=0,\qquad
 M_R=-\int Pg_R(w)\cdot(z\cdot\nabla)w .
 \tag{BV.3}
\]
这是实际压力功的输运消去，不是声称非线性测试本身无散。
常数漂移也不贡献 \(\Pi(z,w)\)；以下可用 \(z\) 的全 \(L^3\) 范数作充分上界，
不需要另行假设它零均值。

BT 已给 \(0<J_R\le I\)，故 \(J_R^2\le J_R\)。
令
\(\mathcal D_R=\sum_k\int J_R(w)[\partial_k w,\partial_k w]\)。
\(Qg_R(w)\) 零均值、投影与导数交换且在 \(L^2\) 收缩，因此
\[
 \|Qg_R(w)\|_6
 \le C\|\nabla Qg_R(w)\|_2
 \le C\|\nabla g_R(w)\|_2
 \le C\mathcal D_R^{1/2}
 \le C\|\nabla w\|_2 .
 \tag{BV.4}
\]
即使 \(g_R(w)\) 本身均值不为零，\(Q\) 仍消掉常数模态。
由空间 Hölder 的 \(6,3,2\) 得到
\[
 \boxed{\quad
 |M_R(\rho)|\le C\|z(\rho)\|_3\|\nabla w(\rho)\|_2
                         \mathcal D_R(\rho)^{1/2}
 \le C\|z(\rho)\|_3\|\nabla w(\rho)\|_2^2 .
 \quad}
 \tag{BV.5}
\]
常数不依赖 \(R\)。这确实改进了 BU.19 的显式 \(R\) 成本，
但右端的时间可积性尚未由 BU 支付。
这里只是每个时间的估计；固定 \(R\) 的 \(M_R\in L^1(0,L)\)
仍由 BU.19 的压力梯度表示保证，不能倒推右端可积。

## 2. 一个准确但未付的充分条件

定义扩展值成本
\[
 \mathcal W_z(\delta)=
       \int_0^\delta\|z(\rho)\|_3\|\nabla w(\rho)\|_2^2\,d\rho.
 \quad
 \mathcal W_z(\delta)<\infty
 \ \Longrightarrow\
 M_R\longrightarrow0\quad\hbox{于 }L^1(0,\delta)\ (R\to\infty).
 \tag{BV.6}
\]
证明不需要交换未经控制的极限。
几乎每个正时间 \(g_R(w)\to w\) 于 \(H^1\)：
函数项由 \(|w|^2\) 支配，导数项由
\(J_R(w)\nabla w\to\nabla w\)、\(|J_R|\le1\) 支配。
故 \(Qg_R(w)\to Qw=0\) 于 \(H^1\) 和 \(L^6\)，BV.2 给 \(M_R\to0\)。
若另有 BV.6 的有限成本，BV.5 就提供与 \(R\) 无关的可积支配函数。
这也给该幅度族的一致可积性；若成本无限，则不作此推论。
有限成本是充分条件，不是实际压力功消失的必要条件。

保留自压力功 \(S_R=\int g_R(w)\cdot\nabla p_w\)。
总压力功是 \(Q_R=cS_R+M_R\)，不是 \(M_R\) 本身。
在额外 BV.6 条件下，BT 的端点成为
\[
 \lim_{R\to\infty}\int_0^\delta S_R\,d\rho=\frac1{2c},
 \qquad S_R(\rho)\to0\quad\hbox{a.e. }\rho>0 .
 \tag{BV.7}
\]
因此即便混合项被支付，自压力仍承受非零端点，不能宣布原子矛盾。
这里不假设实际原解一定满足 \(\mathcal W_z<\infty\)，
也不主张存在满足全部条件的奇异原解。

能量只给 \(\|z\|_3\in L^4(0,L)\) 和
\(\|\nabla w\|_2^2\in L^1(0,L)\)，没有给它们的加权乘积。
这个纯时间 Hölder 缺口可以明确展示：
\[
 f(\rho)=\rho^{-1/8}\in L^4(0,1),\qquad
 d(\rho)=\rho^{-15/16}\in L^1(0,1),\qquad
 fd=\rho^{-17/16}\notin L^1(0,1).
 \tag{BV.8}
\]
这两函数不是 NS 场，不满足或反驳同一原解方程，
也不构造 BU 的全部结构；它们只说明这两个已列时间空间不能自动配对。
不能据此断言真实 \(\mathcal W_z\) 发散或真实混合功无法消去。

若试图把 BV.5 吸收到凸耗散中，任意 \(\eta>0\) 的 Young 估计为
\[
 |M_R|\le\eta\nu\mathcal D_R+
            \frac{C}{\eta\nu}\|z\|_3^2\|\nabla w\|_2^2 .
 \tag{BV.9}
\]
留下的平方加权成本也未支付。
BU.14 的混合张量消失、BU.17 的压力范数小系数，
没有自动支付相对耗散测度 \(dD_w\) 的上述加权积分，也未给出相应衰减率。

## 3. 为什么要同时截断两个场

直接用 \(z\cdot g_R(w)\) 做全时间交叉测试，会遇到
\(\int |z|\,|\nabla w|^2/R\) 型三阶导数项；
现有空间时间能量不保证它可积。
因此先把两个场以相同幅度截断，而不是先去掉其中一个截断。

令 \(s=(1+|v|^2/R^2)^{1/2}\)。
直接求导给
\[
 (D^2g_R(v))_{ijk}
 =-R^{-2}s^{-3}(\delta_{ij}v_k+\delta_{ik}v_j+\delta_{jk}v_i)
       +3R^{-4}s^{-5}v_iv_jv_k,\qquad
 |D^2g_R(v)|_{\rm bilinear}\le 6/R .
 \tag{BV.10}
\]
范数指向量值双线性映射的算子范数。
每个括号项由 \(|v|/(Rs)\le1\) 及 \(s\ge1\) 控制。
取
\[
 \Phi_R(z,w)=g_R(z)\cdot g_R(w),\quad
 Z_R[a,d]=g_R(w)\cdot D^2g_R(z)[a,d],\quad
 W_R[a,d]=g_R(z)\cdot D^2g_R(w)[a,d],\quad
 C_R[a,d]=J_R(z)a\cdot J_R(w)d .
 \tag{BV.11}
\]
这三个双线性式分别是 \(\Phi_{zz},\Phi_{ww},\Phi_{zw}\)；
所有指标的场在当前 \((\rho,x)\) 取值。
它们满足
\[
 |\Phi_R|\le|z||w|,\qquad |Z_R|,|W_R|\le6,\quad |C_R|\le1,
 \qquad Z_R,W_R\to0,\quad C_R[a,d]\to a\cdot d .
 \tag{BV.12}
\]
最后几项是有限状态下的逐点极限。
例如 \(|g_R(w)|\le|w|\)、\(D^2g_R(z)\to0\)，给 \(Z_R\to0\)；
共同幅度保证其统一有界。
两个截断幅度独立撤去时会出现幅度比，不能沿用本节的同一支配函数。

## 4. 合法的联合压力恒等式

定义
\[
 F_R(\rho)=\int\Phi_R(z,w),\qquad
 \mathcal P_R=
 -\int J_R(z)g_R(w)\cdot\nabla q
 -\int J_R(w)g_R(z)\cdot\nabla\pi .
 \tag{BV.13}
\]
固定 \(R\)，两个压力测试向量有界，
\(\nabla q,\nabla\pi\in L^1_\rho L^{3/2}_x\)，故 \(\mathcal P_R\in L^1(0,L)\)。
对 BU.5 的
\(D_\rho z=-\nu\Delta z+2\nu c\Delta w-\nabla q\)、
\(D_\rho w=\nu\Delta w-\nabla\pi\)，
\(D_\rho=\partial_\rho+b\cdot\nabla\)，求导并分部积分得
\[
 \begin{aligned}
 \mathcal V_R={}&
 \nu\sum_k\int Z_R[\partial_kz,\partial_kz]
 -\nu\sum_k\int W_R[\partial_kw,\partial_kw]\\
 &-2\nu c\sum_k\int Z_R[\partial_kz,\partial_kw]
 -2\nu c\sum_k\int C_R[\partial_kw,\partial_kw].
 \end{aligned}
 \tag{BV.14}
\]
相反黏性造成的两个 \(\Phi_{zw}\) 交叉项精确抵消；
源 \(2\nu c\Delta w\) 产生第二行，不能略去。
\(C_R[a,a]\) 不在这里宣称非负：两个对称正矩阵的乘积
未必给一个非负二次型。本节只用它的界与极限。

在每个正时间闭区间，光滑漂移的线性能量法及空间逼近使链式测试合法。
也可同时卷积 \(z,w\)：各自输运交换子按 BT.7 在 \(L^1\) 消失，
固定 \(R\) 的梯度有界、联合 Hessian 有界，
强 \(L^2\) 梯度和压力梯度 \(L^1\) 收敛支付所有极限。
BU.14 给 \(|F_R(\rho)|\le e(\rho)\to0\)，所以固定 \(R\) 可到初端：
\[
 F_R(t)=\int_0^t(\mathcal V_R+\mathcal P_R)\,d\rho,\qquad F_R(0)=0.
 \tag{BV.15}
\]
这里不需要把 \(z\) 的弱迹替换成强迹，也不要求 \(\Phi_R\) 为凸函数。
BV.12 与梯度能量保证 \(\mathcal V_R\in L^1\)，其支配函数独立 \(R\)：
\[
 |\mathcal V_R|\le
 \nu(6+6c)\|\nabla z\|_2^2+\nu(6+8c)\|\nabla w\|_2^2,\quad
 \mathcal V_R\to-2\nu c\|\nabla w\|_2^2
                      \quad\hbox{于 }L^1(0,L).
 \tag{BV.16}
\]
先对空间积分用 BV.12，交叉梯度用
\(2|\nabla z||\nabla w|\le|\nabla z|^2+|\nabla w|^2\)，
再对时空可积的梯度平方支配收敛。

还有一致的端点控制：
\[
 F_R\longrightarrow \langle z,w\rangle=-2\nu cD_w
             \quad\hbox{于 }C([0,L]),\qquad
 \sup_{0\le t\le L}\left|\int_0^t\mathcal P_R\,d\rho\right|\longrightarrow0 .
 \tag{BV.17}
\]
证明先取固定 \(\epsilon>0\)。
\((z,w)\) 在 \([\epsilon,L]\) 的强 \(L^2\) 连续轨道是紧集；
\(g_R\) 的一致 Lipschitz 界和对每个固定 \(L^2\) 场的强收敛，
用有限网升级为轨道上的一致收敛。
在 \((0,\epsilon)\)，两种配对均由 \(e(\rho)\) 控制，故误差至多 \(2e(\rho)\)；
再令 \(\epsilon\downarrow0\)。
结合 BU.7 的精确交叉配对、BV.15--16 就得到第二项。

这是联合压力原函数的消失。它不证明
\(\|\mathcal P_R\|_{L^1}\to0\)、总变差有界或一致可积性。
其二次极限重现已有交叉能量记账，不是一项新的强制估计。

## 5. 联合消去仍不能单独抽出混合功

为避免把联合量误记为 \(M_R\)，把它展开：
\[
 \mathcal P_R=\mathcal T_R-cM_R+\mathcal E_R^q+\mathcal E_R^\pi,
 \tag{BV.18}
\]
\[
 \mathcal T_R=-\int g_R(w)\cdot\nabla p_z,\quad
 \mathcal E_R^q=-\int[J_R(z)-I]g_R(w)\cdot\nabla q,\quad
 \mathcal E_R^\pi=-\int J_R(w)g_R(z)\cdot\nabla\pi .
 \tag{BV.19}
\]
每个固定 \(R\) 的三项都由有界测试与压力梯度保证时间可积。
它们在几乎每个正时间随 \(R\to\infty\) 消失：
\(\mathcal T_R\) 的极限是 \(-\int w\cdot\nabla p_z=0\)，
\(\mathcal E_R^\pi\) 的极限是 \(-\int z\cdot\nabla\pi=0\)，
\(\mathcal E_R^q\) 用 \(J_R(z)-I\to0\)。
空间支配可分别使用 \(w,z\in L^3\) 和压力梯度 \(L^{3/2}\)，
但这些支配乘积未取得全时间可积性。

因此已经得到的准确关系仅为
\[
 c\int_0^t M_R\,d\rho
 =\int_0^t(\mathcal T_R+\mathcal E_R^q+\mathcal E_R^\pi)\,d\rho
              -\int_0^t\mathcal P_R\,d\rho .
 \tag{BV.20}
\]
最后一项一致趋零，但前三项的和仍须另行控制。
交换 \(z,w\) 不给可任意替换的同一方程：
它们的压力、黏性和源不同。不能靠重命名把联合消去变成单项消去。
这不是所有耦合或非局部方法的不可能定理，只是本项测试的完整验收。

## 6. 同一配对的压力平方接口和累计约束

另一个有限而明确的支付方式直接使用压力值，不另换测试族。
几乎每个时间，空间分部积分给
\[
 M_R=\int r\,\operatorname{div}(g_R(w)-w),\qquad
 \nabla(g_R(w)-w)\to0\quad\hbox{于 }L^2((0,\delta)\times\Omega).
 \tag{BV.21}
\]
第二项由 \((J_R(w)-I)\nabla w\to0\) 及梯度能量支配得到。
所以若额外支付 \(r\in L^2((0,\delta)\times\Omega)\)，
空间时间 Cauchy--Schwarz 便给 \(\int_0^\delta|M_R|\to0\)。
只有在这个额外条件下，这里的压力值与导数乘积才直接获得全时间绝对可积性。
它不是声称此条件与 BV.6 等价，也不是压力功消失的必要条件。

已有能量确实给 \(r\in L^1_\rho L^3_x\)：
\(\|r\|_3\le C\|z\|_6\|w\|_6\)。
与 BU.17 的 \(L^2_\rho L^{3/2}_x\) 配合，得到的只是
\[
 \|r\|_{L^{4/3}(0,\delta;L^2)}
 \le \|r\|_{L^2(0,\delta;L^{3/2})}^{1/2}
          \|r\|_{L^1(0,\delta;L^3)}^{1/2}.
 \tag{BV.22}
\]
这里空间倒数 \(1/2=(2/3+1/3)/2\)，
时间倒数 \(3/4=(1/2+1)/2\)。
对偶时间应为 \(L^4\)，而 BV.21 只给 \(L^2\) 导数。
不能因为空间指数已补到 \(2\)，就把时间指数也改为 \(2\)。

最后，不能漏掉同一原解已经给出的约束：
\[
 2\nu c D_w(\rho)
       =|\langle z(\rho),w(\rho)\rangle|
       \le e(\rho)=\|z(\rho)\otimes w(\rho)\|_1\longrightarrow0 .
 \tag{BV.23}
\]
这来自 BU.7、14，只约束累计耗散，
不是 \(\|z\|_3\) 对密度 \(dD_w=\|\nabla w\|_2^2d\rho\) 的可积性。
不能把累计小量当成耗散发生时的加权控制。

本节付清了固定联合测试及不显含幅度的投影上界。
尚未证明真实 \(\mathcal W_z\) 有限或混合压力平方可积，
也未证明真实混合功或自压力功的端点消失。
下一项需要真正使用残差及原解方程，核对源项与梯度能量演化能否
支付上述加权对齐，或保留符号取得更弱的控制；同时保留自压力。
不把充分成本当作必要条件，不继续枚举邻近范数，
也不重复联合交叉记账作为新正结果。
原子存在与排除、任意奇点的原子生成、G、R.216--R.217、
一般三维正则性和 Clay 问题仍 OPEN。
