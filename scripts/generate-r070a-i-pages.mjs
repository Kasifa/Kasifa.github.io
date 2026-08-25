#!/usr/bin/env node

import { writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const releases = [
  {
    code: "R0.70A", slug: "r0-70a", label: "RATIO ROBUSTNESS · MOVING ANNULUS",
    title: "比例四的严格障碍可以短时延续，<br>移动尺度标签却不会自动闭合",
    meta: "R0.69W 比例四障碍具有非显式开邻域与共同短时稳定性；移动环带只重分配标签，尚无受控临界正规形。",
    lead: String.raw`本节把 R0.69W 的单一比例证书沿两个方向推进。联合连续性给出比例四附近的非显式开放邻域，并由局部 \(H^4\) 理论得到真实光滑解上的共同短时符号稳定性；另一方面，精确移动标签账本证明，选择 \(r(t)\) 不会把涡量拉伸自动变成边界项。`,
    state: "定性稳健性与移动标签恒等式完成；显式比例区间未认证",
    badge: "五点数值 pilot 仅作诊断，不作为结论",
    theoremTitle: "比例四的统一负余量推出一个未显式化的开邻域",
    theoremText: String.raw`对 \(u_{a,\rho}=aU_1+(1-a)U_{1/\rho}\) 与 \(G(a,\rho)=\min\{\mathcal A_0,\mathcal A_{-2}\}\)，严格证书给出`,
    theoremEq: String.raw`\max_{0\le a\le1}G(a,4)\le-\delta_*,\qquad \delta_*=1.246030236725547\times10^{-5}.`,
    detailTitle: "移动环带半径只产生可相消的标签通量",
    detailText: String.raw`存在某个 \(\eta>0\)，使 \(|\rho-4|<\eta\) 时仍有 \(G(a,\rho)<0\)。对完整近—环带—远分解，任意正函数 \(r(t)\) 满足`,
    detailEq: String.raw`\mathcal V(u)=\mathcal N_{r(t)}(u)+\mathcal A_{r(t),\Lambda}(u)+\mathcal F_{\Lambda r(t)}(u).`,
    bridgeText: String.raw`只有单独微分移动环带时才出现 \(\dot r/r\) 的标签流；恢复完整分解后这些项相消。尚未构造出导数以该三次环带项为主、余项又在临界尺度受控的二次 \(Q_r\)。`,
    bridgeEq: String.raw`{d\over dt}\mathcal A_{r(t),\Lambda}={\dot r\over r}\mathfrak B_{r,\Lambda}+\mathfrak T_{r,\Lambda}+\mathfrak S_{r,\Lambda}+\mathfrak D_{r,\Lambda}.`,
    value: String.raw`这一步把严格静态证书提升到定性参数稳健性和真实方程的短时连续依赖，同时排除“只移动观察尺度即可获得动态耗减”的误解。`,
    boundary: String.raw`\(\eta\) 与共同短时间都不是显式数值；不得把诊断 pilot 的 \(3.9<\rho<4.1\) 写成已证区间。pilot 缺少完整资源遥测和端到端生产状态锁定，只能用于排序。短时结果不是临界估计。`,
    next: String.raw`R0.70B 检查有符号物理环带能否在匹配尺度替代非负过滤储备，并用最小三波测试二次正规形。`,
    sources: [["r070a_parallel_gate_summary.md","并行门槛总结"],["r070a_scale_ratio_robustness_note.md","比例稳健性证明"],["r070a_moving_annular_balance_note.md","移动环带账本"],["r070a_literature_collision_matrix.md","文献碰撞矩阵"]],
    certificate: "r070a-pilot",
  },
  {
    code: "R0.70B", slug: "r0-70b", label: "MATCHING-SCALE BRIDGE · NORMAL-FORM NO-GO",
    title: "匹配尺度只恢复已知因子，<br>二次零余项正规形也被三波阻断",
    meta: "有符号物理环带只能由非负过滤储备单向控制；反向桥与声明的平移不变二次零余项正规形均被严格反例关闭。",
    lead: String.raw`本节把有符号物理环带与非负过滤储备放到相同尺度比较。正储备可以向下控制 signed work，但只恢复已知尺度因子；局部化交换子与主项同阶。反向控制和一个较宽的二次正规形类别都存在严格障碍。`,
    state: "直接环带—Yu 替代路线关闭",
    badge: "单向桥、运动学反例与 3:4:5 符号 no-go 完成",
    theoremTitle: "正储备到 signed work 的前向桥没有新小因子",
    theoremText: String.raw`局部化 shell work 分成两增量主项 \(T_{j,k}\) 与同阶 cutoff commutator \(C^\chi_{j,k}\)，并满足`,
    theoremEq: String.raw`W_{j,k}=T_{j,k}+C^\chi_{j,k},\qquad |W_{j,k}|\le C{r_k\over r_j}\mathfrak A_{j,k}\mathcal Q_k.`,
    detailTitle: "3:4:5 螺旋三波排除零三次余项的二次生成器",
    detailText: String.raw`声明的连续、平移不变、自伴、至多多项式增长二次 multiplier 必须满足一个符号相容式；实际物理环带在低频展开的四阶项违反它：`,
    detailEq: String.raw`16g_4-9g_3-7g_5=0,\qquad 16G(4\varepsilon)-9G(3\varepsilon)-7G(5\varepsilon)={72\over5}I_4(\varepsilon r)^4+O((\varepsilon r)^6)>0.`,
    bridgeText: String.raw`仿射剪切核心可使内部 matching-shell production 为零而过滤储备非零；高频包还使过滤 signed annuli 的绝对和趋零，而未解析高—高 commutator 发散。`,
    bridgeEq: String.raw`D^{\mathrm{sign}}_{j,k}=\iint|w_{j,k}|-|W_{j,k}|\ge0.`,
    value: String.raw`结果明确了信息方向：signed observable 位于正储备估计的下游，不能反过来替代它。符号测试也在投入更大计算前排除了一个清楚定义的正规形类。`,
    boundary: String.raw`运动学反例不是完整抛物时间区间上的 NSE 反例。正规形 no-go 只覆盖声明的二次 multiplier 与零三次余项精确恒等式，不排除局部化、解依赖、非二次、时间非局部或同阶可控余项。`,
    next: String.raw`R0.70C 检查真实 Navier–Stokes 演化是否会自动压低 signed cancellation defect。`,
    sources: [["r070b_report-source.md","完整数学报告"]], certificate: "r070b",
  },
  {
    code: "R0.70C", slug: "r0-70c", label: "DYNAMIC SIGN DEFECT · LINEAR PARITY",
    title: "真实全局光滑小数据轨道中，<br>有符号积分仍可比绝对活动低一阶",
    meta: "偶对称小数据 Navier–Stokes 解把运动学符号缺陷升级为真实全局光滑轨道障碍；缺陷已存在于线性热层。",
    lead: String.raw`R0.70B 的反例只在运动学层面。本节构造全局光滑、有限能量的小数据全空间解：绝对环带活动为三阶，而 signed integral 由于奇偶性只从四阶开始；再用两个分离副本与隐函数调节，可使时空 signed work 精确为零。`,
    state: "动态符号恢复路线关闭于一个固定泛函",
    badge: "真实 NSE 小数据解族与精确零调节完成",
    theoremTitle: "符号缺陷已经出现在三次线性热层",
    theoremText: String.raw`对固定偶滤子、偶环带窗与偶空间 cutoff，存在全局光滑小数据解 \(u^\varepsilon\)，使`,
    theoremEq: String.raw`P_I[u^\varepsilon]=A_I\varepsilon^3+O_I(\varepsilon^4),\qquad W_I[u^\varepsilon]=O_I(\varepsilon^4),\qquad {|W_I|\over P_I}\longrightarrow0.`,
    detailTitle: "两副本振幅调节把 signed work 精确压到零",
    detailText: String.raw`在足够大的固定偶 cutoff 与足够短时间柱上，隐函数给出振幅参数，使`,
    detailEq: String.raw`W_I[u^\varepsilon]=0,\qquad P_I[u^\varepsilon]>0,\qquad D_I^{\mathrm{sign}}[u^\varepsilon]=P_I[u^\varepsilon].`,
    bridgeText: String.raw`线性种子满足 \(U(-x)=U(x)\)、\(\Omega(-x)=-\Omega(x)\)，从而局部环带密度为奇函数；非线性修正只从下一振幅阶进入。`,
    bridgeEq: String.raw`w_\eta[U](-x)=-w_\eta[U](x).`,
    value: String.raw`这一步证明 signed cancellation 不是只能由强湍流产生的高阶效应。任何成功闭合都必须保留独立的正三次储备，或加入明确排除该奇偶族的结构。`,
    boundary: String.raw`结论针对一个固定泛函和刻意构造的小数据解。精确零调节需要能容纳两个分离副本的大 cutoff；不排除方向相干、正时间大数据或近奇点非退化假设。`,
    next: String.raw`R0.70D 先做纯测度论门槛：固定尺度的正局部平均能否控制未解析负质量。`,
    sources: [["r070c_report-source.md","完整数学报告"]], certificate: "r070c", figure: "r070c-parity-obstruction/fig-r070c-parity-obstruction",
  },
  {
    code: "R0.70D", slug: "r0-70d", label: "FIXED-SCALE COVER · NEGATIVE-MASS BLINDNESS",
    title: "每个固定尺度局部平均都为正，<br>负部质量仍可保持不小",
    meta: "高频正弦密度证明固定尺度 signed cover positivity 无法控制未解析负部；必须加入尺度细化、频率或 PDE 结构。",
    lead: String.raw`本节把 cover positivity 中最基础的逻辑单独抽出。对任何具有统一质量下界和一阶导数预算的固定分辨率非负权重族，可以让全部局部平均为正且趋零，同时负部保留统一质量。`,
    state: "固定尺度 cover 正性桥关闭",
    badge: "抽象测度论反例与精确负质量公式完成",
    theoremTitle: "固定分辨率的所有正平均仍看不见高频负区",
    theoremText: String.raw`取 \(f_{\delta,N}(x)=\delta+\sin(Nx_1)\)。当 \(N\ge2C_1/(\delta m_0)\) 时，每个允许权重 \(\theta\) 满足`,
    theoremEq: String.raw`{\delta\over2}\le\langle f_{\delta,N}\rangle_\theta\le{3\delta\over2}.`,
    detailTitle: "负部却有与 δ 无关的正下界",
    detailText: String.raw`对 \(0<\delta\le1/2\)，精确积分给出`,
    detailEq: String.raw`\int(f_{\delta,N})_-\,d\mu={2\sqrt{1-\delta^2}-\delta(\pi-2\arcsin\delta)\over2\pi}\ge{\sqrt3-\pi/3\over2\pi}>0.`,
    bridgeText: String.raw`总平均只有 \(\delta\)，所以负质量与总 signed mass 的比值按 \(1/(\pi\delta)\) 发散。`,
    bridgeEq: String.raw`{\int(f_{\delta,N})_-\,d\mu\over\int f_{\delta,N}\,d\mu}\sim{1\over\pi\delta}.`,
    value: String.raw`结果关闭“固定尺度正 signed averages 蕴含小负部”的抽象桥，并明确指出成功定理必须增加尺度细化、频率控制、PDE 可容许性或几何符号。`,
    boundary: String.raw`这是抽象标量密度反例，不是 Yu remainder、环带拉伸或 NSE flux 的实现。不适用于分辨率趋零的全尺度观测，也不否定带 Taylor/Kraichnan 条件和局部平衡的 cascade positivity。`,
    next: String.raw`R0.70E 回到 Yu 实际定义的 signed remainder 与 moving-shell tensor，检查单壳奇偶抵消。`,
    sources: [["r070d_report-source.md","完整数学报告"]], certificate: "r070d", figure: "r070d-cover-blindness/fig-r070d-cover-blindness",
  },
  {
    code: "R0.70E", slug: "r0-70e", label: "YU OBJECT CORRECTION · PARITY TRANSVERSALITY",
    title: "Yu 的真实 remainder work 可精确抵消，<br>同核绝对活动仍严格为正",
    meta: "纠正 Yu 对象归属后，紧支撑小数据全局光滑解给出 signed remainder 与项目 moving-shell contraction 的单壳奇偶横截性。",
    lead: String.raw`本节先纠正来源：Yu v1 定义的是 signed remainder work、其正部和 moving-shell strain tensor，并不存在先前误写的 shell scalar。随后在这些真实对象上构造单壳抵消：signed work 为零，同核 absolute activity 为正。`,
    state: "来源对象已修正；单壳 signed cancellation 完成",
    badge: "四个三次项、hard-shell 符号与非线性调节均保留",
    theoremTitle: "Yu 定义的 remainder work 可在全局光滑小数据解上精确为零",
    theoremText: String.raw`存在紧支撑光滑无散初值及其全局小数据 NSE 解，使`,
    theoremEq: String.raw`\mathcal V_\chi^{\mathrm{rem}}=0,\qquad \mathcal A_\chi^{\mathrm{rem}}>0,\qquad \mathcal V_\chi^{+,\mathrm{rem}}={1\over2}\mathcal A_\chi^{\mathrm{rem}}>0.`,
    detailTitle: "项目定义的 hard-shell contraction 也有同样横截性",
    detailText: String.raw`对一个充分分离壳对，使用 Yu 精确 moving-shell tensor 的项目配对满足`,
    detailEq: String.raw`\mathcal W_{k,m}^{\mathrm{mov}}=0,\qquad \mathcal P_{k,m}^{\mathrm{mov}}>0.`,
    bridgeText: String.raw`非线性精确零点由 \(\lambda(\varepsilon)=1+O(\varepsilon)\) 的隐函数调节得到，不是假设非线性演化保持反射对称。`,
    bridgeEq: String.raw`H_0(1)=0,\qquad H_0'(1)=-{A_1\over2}\ne0.`,
    value: String.raw`结果把 generic parity obstruction 转移到文献真正定义的 remainder work，并说明 signed cancellation 不能替代正 remainder 或 magnitude budget。`,
    boundary: String.raw`even/radial mollifier 与 cutoff 是允许类中的项目选择，不是 Yu 的普遍假设。moving-shell contraction 是项目定义；只处理一个分离壳对，不处理全跨尺度求和、commutator 或 Carleson budget。`,
    next: String.raw`R0.70F 转向固定外源环带的低阶 harmonic affine jet，检查 Taylor 增益能否求和。`,
    sources: [["r070e_report-source.md","完整数学报告"],["r070e_independent_audit.md","独立数学复核"]], certificate: "r070e", figure: "r070e-yu-parity-transversality/fig-r070e-yu-parity-transversality",
  },
  {
    code: "R0.70F", slug: "r0-70f", label: "AFFINE JET · INITIAL-FACE SATURATION",
    title: "harmonic Taylor 展开逐阶增益，<br>固定阶数仍不能阻止线性累计",
    meta: "固定外源环带的 affine jet 有精确 Taylor 尺度增益；常数与线性 jet 可在统一小数据类的初始面同号线性累积。",
    lead: String.raw`固定源 harmonic strain 可以合法做 Taylor 展开，且每多减一阶都获得一个尺度比；但 trace-free、divergence-free 与 harmonic 结构不消去常数和线性 jet。任意长初始面族在统一能量和小 \(BMO^{-1}\) 控制下仍可积累同号配对。`,
    state: "逐项绝对值的无权 affine-jet majorant 路线关闭",
    badge: "精确 Taylor 幂次与初始面饱和族完成",
    theoremTitle: "Taylor remainder 的尺度比幂次是精确的",
    theoremText: String.raw`令 \(\theta=r_k/r_j\)。常数、线性、二次 jet 以及更高余项满足`,
    theoremEq: String.raw`|\mathcal W^{(n)}_{j,k}|\le C\theta^{n+1}\mathfrak A^\psi_{j,k}\mathcal Q_k\ (n=0,1,2),\qquad |\mathcal W^{(3+)}_{j,k}|\le C\theta^4\mathfrak A^\psi_{j,k}\mathcal Q_k.`,
    detailTitle: "统一小数据初始面仍可产生线性正累计",
    detailText: String.raw`存在嵌套有限族，使`,
    detailEq: String.raw`\sup_N(\|f_N^{(q)}\|_2+\|f_N^{(q)}\|_{BMO^{-1}})<\infty,\qquad \sum_{n=1}^N\mathcal J_n^{(q)}\ge c_qN,\quad q=0,1.`,
    bridgeText: String.raw`固定 gap 幂 \(\beta>0\) 对仅有界 reservoir 序列仍线性累计；即使 affine remainder 对应 \(\beta=3\)，斜率仍为 \(1/7\)。`,
    bridgeEq: String.raw`\sum_{k=1}^N\sum_{j<k}2^{-\beta(k-j)}={N\over2^\beta-1}-{1-2^{-\beta N}\over(2^\beta-1)^2}.`,
    value: String.raw`结果区分了“尺度差上的 Taylor gain”与“粗尺度数量上的 packing”。后续需要 source-aware difference、Carleson、正交性或明确 decorrelation，而不是继续提高固定 Taylor 阶数。`,
    boundary: String.raw`饱和只在初始面成立，不是一个共同正终点的 backward-cylinder 反例。它否定的是逐项绝对值、无权、bounded-reservoir majorant，不否定真实时空抵消或条件 Carleson 机制。`,
    next: String.raw`R0.70G 把 raw annular jet 换成 adjacent-source difference，并推导临界归一化后的精确 transport law。`,
    sources: [["r070f_report-source.md","完整数学报告"],["r070f_independent_audit.md","独立数学复核"]], certificate: "r070f", figure: "r070f-affine-jet-saturation/fig-r070f-affine-jet-saturation",
  },
  {
    code: "R0.70G", slug: "r0-70g", label: "ADJACENT SOURCE · DILATION DEFECT",
    title: "物理源可以望远镜相消，<br>临界归一化却留下固定伸缩缺陷",
    meta: "相邻源 jet 的临界输运因子不是一；源侧有耗散级平方和，核心侧精确对偶估计仍缺失。",
    lead: String.raw`本节检验相邻物理 annuli 是否像 martingale difference。未归一化源确实望远镜相消；进入 Navier–Stokes 临界坐标后，普通系数一差分变成带固定衰减的协变输运，持续基线不会消失。`,
    state: "普通相邻差分捷径关闭；源侧平方函数保留",
    badge: "临界 transport law 与三组压力测试完成",
    theoremTitle: "临界坐标中的相邻差分带有 n 依赖的 dilation factor",
    theoremText: String.raw`对 \(c_j^{(n)}=r_j^{n+2}P_j^{(n)}\) 与 annular coefficient \(h_j^{(n)}\)，有`,
    theoremEq: String.raw`h_j^{(n)}=c_j^{(n)}-2^{-(n+2)}c_{j-1}^{(n)}.`,
    detailTitle: "Leray dissipation 控制源侧带权平方和",
    detailText: String.raw`固定中心与固定源满足`,
    detailEq: String.raw`\sum_jr_j^{2n+3}|J_j^{(n)}(x_0)|^2\le C_n\|\Omega\|_2^2,\qquad \sum_jr_j^{-1}|h_j^{(n)}|^2\le C_n\|\Omega\|_2^2.`,
    bridgeText: String.raw`直接 Cauchy–Schwarz 仍需要核心零阶与一阶矩的负权重平方和；有限能量没有提供该对偶量。`,
    bridgeEq: String.raw`\sum_j\bigl(r_j^{-3}|M_j^{(0)}|^2+r_j^{-5}|M_j^{(1)}|^2\bigr)<\infty.`,
    value: String.raw`结果把“望远镜恒等式成立”和“临界归一化后可用普通差分”分开，并把后续问题定位为核心矩的局部 Carleson 或配对变化估计。`,
    boundary: String.raw`结论使用固定源、固定滤波器与固定中心；physical cutoff 不是 Fourier LP projection。压力测试是初始面复现，没有共同正终点，也不证明 moving-shell packing。`,
    next: String.raw`R0.70H 推导核心矩在相邻滤波尺度和嵌套时间窗下的精确变化与对偶坐标。`,
    sources: [["r070g_report-source.md","完整数学报告"],["r070g_independent_audit.md","独立数学复核"]], certificate: "r070g", figure: "r070g-critical-transport/fig-r070g-critical-transport",
  },
  {
    code: "R0.70H", slug: "r0-70h", label: "CORE MOMENT · PARABOLIC DUALITY GAP",
    title: "固定时间核心矩变化可控，<br>嵌套时间窗却放大两个临界尺度",
    meta: "零阶与一阶临界核心矩有逐时 l1 变化估计；实际时空功额外含 r_k^-2，缺口是加权抛物 source–core embedding。",
    lead: String.raw`源侧平方函数已经存在，本节计算与之配对的核心矩。固定时间、固定中心的临界零阶与一阶矩确有总变化界；但实际嵌套时空坐标多出 \(r_k^{-2}\)，配对后形成 \(r_k^{-3}\) 负权重。`,
    state: "固定时间正估计完成；抛物型对偶缺口定位",
    badge: "普通 moment variation 不是缺失桥",
    theoremTitle: "临界核心矩的无权固定时间变化受涡量能量控制",
    theoremText: String.raw`对 \(m_k^{(0)}=r_kM_k^{(0)}\)、\(m_k^{(1)}=M_k^{(1)}\)，显式 square-function 假设给出`,
    theoremEq: String.raw`\sum_k|m_{k+1}^{(n)}-m_k^{(n)}|\lesssim r_0\|\omega\|_2^2,\qquad n=0,1.`,
    detailTitle: "实际时空坐标带来 r_k^-2 放大",
    detailText: String.raw`真正进入 R0.70F work 的坐标是 \(\mathcal N_k^{(n)}=r_k^{-2}\mathbf1_{I_k}m_k^{(n)}\)，其直接对偶需要`,
    detailEq: String.raw`\int\sum_kr_k^{-3}\!\left[\mathbf1_{I_{k+1}}|m_k^{(n)}-\rho_k^nm_{k+1}^{(n)}|^2+\mathbf1_{I_k\setminus I_{k+1}}|m_k^{(n)}|^2\right]dt.`,
    bridgeText: String.raw`配对协变增量是 \(m_k^{(n)}-\rho_k^{n+2}m_{k+1}^{(n)}\)，不是普通相邻差。直接从矩演化取绝对值会重新出现待控制的 resolved vortex stretching。`,
    bridgeEq: String.raw`\mathfrak D_k^{\mathrm{pair}}m^{(n)}=m_k^{(n)}-\rho_k^{n+2}m_{k+1}^{(n)}.`,
    value: String.raw`结果纠正了三种容易混淆的归一化，并说明缺口不是少一个时间 Hölder 指数，而是嵌套窗口产生的临界负尺度 source–core embedding。`,
    boundary: String.raw`无权 L_t^1 l1 估计不蕴含所需的加权 L_t^2 l2。结论限于固定中心的单向细尺度链；初始压力族没有统一涡量 L2，也不反驳耗散积分估计。`,
    next: String.raw`R0.70I 求出负尺度权重的精确时间核，并用 LP/Bony 分解识别可闭合与不可闭合的 sector。`,
    sources: [["r070h_report-source.md","完整数学报告"],["r070h_independent_audit.md","独立数学复核"]], certificate: "r070h", figure: "r070h-core-moment-gap/fig-r070h-core-moment-gap",
  },
  {
    code: "R0.70I", slug: "r0-70i", label: "TEMPORAL HARDY · FROZEN-LOW CLOSURE",
    title: "负尺度核心范数化成尖锐 Hardy 核，<br>frozen-low sector 可以闭合",
    meta: "核心对偶范数产生 s^-1/2 时间 Hardy 核；frozen-low/annular 与 isotropic diagonal 闭合，moving-low 和 deviatoric diagonal 保持开放。",
    lead: String.raw`本节把 R0.70H 的负尺度损失精确化成一维时间 Hardy 核。无限细链产生 \(s^{-1/2}\|\omega\|_2^4\)，超出 Leray 的时间信息；但标准 LP 分解下，完整 frozen outer-low/annular sector 可以绝对值闭合。`,
    state: "frozen-low 正结果完成；moving-low 与偏差对角项保持开放",
    badge: "Hardy 核、有限链饱和与初始边界 sharpness 完成",
    theoremTitle: "无限链的核心对偶范数具有 s^-1/2 时间核",
    theoremText: String.raw`对 \(n=0,1\)，实际核心量满足`,
    theoremEq: String.raw`\mathcal T_n\lesssim\int_0^{r_0^2}s^{-1/2}\|\omega(t_0-s)\|_2^4\,ds,`,
    detailTitle: "frozen-low/annular 下三角数组在能量层闭合",
    detailText: String.raw`若源 coefficient square function 为 \(\mathsf C\)，则`,
    detailEq: String.raw`|\mathscr W_{\mathrm{frozen\text{-}low/mixed}}|\lesssim r_0^{-3/2}\|u\|_{L_t^\infty L_x^2}\mathsf C\|\omega\|_{L_t^2L_x^2}.`,
    bridgeText: String.raw`有限链的精确 kernel 在最细尺度饱和为 \(\min\{r_K^{-1},s^{-1/2}\}\)。isotropic high–high 因 source strain trace-free 消失，deviatoric diagonal 仍需未控制的四次壳和。`,
    bridgeEq: String.raw`\int\sum_kr_k^{-1}\|W_k(t)\|_2^4\,dt\quad\text{仍未由 Leray 账本控制}.`,
    value: String.raw`结果把整个 quadratic core 缩小到 moving-low 与 deviatoric high–high diagonal 两个 sector，并证明 outer-scale loss 与 Hardy 临界核不是粗糙估计的假象。`,
    boundary: String.raw`标量 s^-alpha profile 只是函数空间障碍，不是 NSE 轨道。初始边界 sharpness 使用不同缩放的小数据解且终点趋零；不是一个解在固定正时间集中。端点 p=8 与大数据行为均未解决。`,
    next: String.raw`R0.70J 直接检查偏差 high–high tensor 与外部 harmonic strain 是否具有新的有符号零结构。`,
    sources: [["r070i_report-source.md","完整数学报告"],["r070i_independent_audit.md","独立数学复核"],["r070i_literature_audit.md","文献边界审计"]], certificate: "r070i", figure: "r070i-temporal-hardy/fig-r070i-temporal-hardy",
  },
];

const gh = "https://github.com/Kasifa/Kasifa.github.io";

function archiveLinks(item) {
  const links = item.sources.map(([file,label]) => `<a href="${gh}/blob/main/research/${file}">${label}</a>`);
  links.push(`<a href="${gh}/tree/main/research/certificates/${item.certificate}">精确证书与 SHA-256 清单</a>`);
  if (item.figure) links.push(`<a href="${gh}/tree/main/figures/${item.figure}">期刊附图包</a>`);
  return links.join(" · ");
}

function render(item) {
  const nextCode = item.next.match(/R0\.\d+[A-Z]?/)?.[0] ?? "下一节";
  return `<!doctype html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="description" content="研究笔记 ${item.code}：${item.meta}">
  <meta property="og:type" content="article">
  <meta property="og:title" content="${item.code}｜${item.title.replace("<br>", "")}">
  <meta property="og:description" content="${item.meta}">
  <meta property="og:image" content="https://kasifa.github.io/og.png">
  <title>${item.code}｜${item.title.replace("<br>", "")}</title>
  <script>window.MathJax={tex:{inlineMath:[['\\\\(','\\\\)']],displayMath:[['\\\\[','\\\\]']]},options:{skipHtmlTags:['script','noscript','style','textarea','pre','code']}};</script>
  <link rel="stylesheet" href="/bilingual.css">
  <link rel="stylesheet" href="/note-retro.css?v=0.86">
  <style>.hero h1{font-size:clamp(1.8rem,4vw,3.4rem)}</style>
  <script defer src="/i18n-en.js?v=0.86"></script>
  <script defer src="/bilingual.js"></script>
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
</head>
<body>
  <div class="topline"></div>
  <header class="bar"><div class="bar-inner"><a class="brand" href="/">ν · 三维 Navier–Stokes 个人研究记录</a><nav><a href="#result">结论</a><a href="#identity">恒等式</a><a href="#value">价值</a><a href="#boundary">边界</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav></div></header>
  <main>
    <header class="hero"><div class="hero-inner"><div><div class="eyebrow">研究笔记 ${item.code} · ${item.label}</div><h1>${item.title}</h1><p class="lead">${item.lead}</p></div><div class="stamp"><span class="state">状态 · ${item.state}</span><strong>${item.badge}</strong><p>版本 v${item.code.slice(1)} · 2026-08-25</p><p>解析推导、精确证书与报告边界已封存</p><p>本节没有构造奇性或证明全局正则性</p></div></div></header>
    <div class="layout"><aside class="toc"><strong>CONTENTS</strong><ol><li><a href="#result">00 · 本节结论</a></li><li><a href="#identity">01 · 精确账本</a></li><li><a href="#value">02 · 研究价值</a></li><li><a href="#boundary">03 · 主张边界</a></li><li><a href="#next">04 · 下一检查点</a></li><li><a href="#reproduce">05 · 复现与来源</a></li></ol></aside>
      <article>
        <section id="result"><div class="section-no">00 / Exact decision</div><h2>${item.theoremTitle}</h2><p>${item.theoremText}</p><div class="equation result">\\[${item.theoremEq}\\]</div></section>
        <section id="identity"><div class="section-no">01 / Auditable ledger</div><h2>${item.detailTitle}</h2><p>${item.detailText}</p><div class="equation result">\\[${item.detailEq}\\]</div><p>${item.bridgeText}</p><div class="equation">\\[${item.bridgeEq}\\]</div></section>
        <section id="value"><div class="section-no">02 / Research value</div><h2>这一步改变了后续检查对象</h2><p>${item.value}</p></section>
        <section id="boundary"><div class="section-no">03 / Claim boundary</div><h2>证明到这里为止</h2><p>${item.boundary}</p><p>这里没有构造有限时奇性，没有证明无条件全局光滑性，也不是对 Clay 千禧年问题的部分解答。</p></section>
        <section id="next"><div class="section-no">04 / Next gate</div><h2>${nextCode} 的检查点</h2><p>${item.next}</p></section>
        <section id="reproduce"><div class="section-no">05 / Reproducibility</div><h2>报告、证书和可用的独立复核已经封存</h2><p>${archiveLinks(item)}</p><p><a href="/notes/${item.slug}.pdf">下载同步 PDF</a> · <a href="https://www.claymath.org/millennium/navier-stokes-equation/">Clay Mathematics Institute 正式问题说明</a></p><p>公开页只摘要档案中已经审计的声明；有限生产器不替代报告中的无限维解析步骤。</p></section>
      </article>
    </div>
  </main>
  <footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>精确结果、条件结论、反例边界与开放问题分开记录。</div><div>${item.code} · 2026-08-25<br><a href="/">返回研究主页</a></div></footer>
</body>
</html>
`;
}

const root = resolve(import.meta.dirname, "..");
for (const item of releases) await writeFile(resolve(root, "public", "notes", `${item.slug}.html`), render(item));
console.log(`generated ${releases.length} notes: ${releases[0].code}–${releases.at(-1).code}`);
