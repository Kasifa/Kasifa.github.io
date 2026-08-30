# R0.73K bilingual terminology ledger

**Status:** source stage
**Scope:** proof, finite diagnostic, figure, bilingual note, PDF, and recap

| 中文 | English | Usage boundary |
|---|---|---|
| 参数一致黏性谱支 | parameter-uniform viscous spectral branch | Uniform for (d\in[0,1/450]) and sufficiently small positive viscosity; the viscosity threshold is existential. |
| 奇异黏性极限 | singular vanishing-viscosity limit | The domain changes from all of (L^2) at (arepsilon=0) to (H^2_{\rm per}) for (arepsilon>0). |
| 耗散基算子 | dissipative base operator | (H_{\varepsilon,d}=M_d-\varepsilon L), before the compact Rayleigh correction (K_d) is restored. |
| 紧 Fredholm 夹逼 | compact--Fredholm sandwich | The compact correction converts joint strong base-resolvent convergence into operator-norm convergence on the selected spectral block. |
| 共同 Riesz 围道 | common Riesz contour | (Gamma_*={|z-0.17|=0.003}), valid for the whole profile interval and all sufficiently small viscosities. |
| 算子范数投影收敛 | operator-norm projection convergence | (sup_d|P_\varepsilon(d)-P_0(d)|	o0); it is not full norm-resolvent convergence. |
| 共同黏度阈值 | common viscosity threshold | One existential (arepsilon_K>0) works for all (d); no explicit numerical value is claimed. |
| 黏性 rank-one 支 | viscous rank-one branch | The selected Riesz projection has rank one, so the enclosed eigenvalue is algebraically simple. |
| 左右条件数 | left--right conditioning | For rank one, (|P|) is the reciprocal normalized left--right overlap. |
| 一阶黏性位移 | first-order viscous displacement | The audited bound (|lambda_\varepsilon-lambda_0|le C\varepsilon); no asymptotic coefficient expansion is claimed. |
| 反射—共轭对称 | reflection--conjugation symmetry | The antiunitary symmetry preserving the viscous domain and forcing the unique enclosed eigenvalue to be real. |
| 固定相位锚 | fixed phase anchor | (alpha(h)=\frac12(L^{-1/2}h)(0)) in transformed (L^2), used only after uniform nonvanishing is proved. |
| 固定半平面无谱污染 | no pollution in a fixed half-plane | The selected eigenvalue is the only spectrum in (operatorname{Re}zge0.12). |
| 缩减 resolvent | reduced resolvent | The resolvent of the part in (Q_\varepsilon H), analytically regular through the removed selected eigenvalue. |
| 补空间半群界 | complementary semigroup bound | (|e^{tB_\varepsilon}Q_\varepsilon|le Ce^{0.12t}), proved from a full vertical-line resolvent estimate, not from the gap alone. |
| 不稳定块逆向群 | inverse group on the unstable block | (e^{-tB_\varepsilon}P_\varepsilon) is defined on the rank-one spectral block; it is not a negative-time semigroup on the full space. |
| 全算子范数 resolvent 收敛 | full norm-resolvent convergence | Structurally false here because compact viscous resolvents cannot converge in norm to the noncompact inviscid resolvent. |
| 有限动能压缩 | finite kinetic compression | The transformed Fourier matrix whose Euclidean norm matches the compressed kinetic norm; it remains diagnostic only. |
| 固定圆盘计数 | fixed-disk eigenvalue count | A binary64 finite check that the chosen compression has one eigenvalue in the disk; it is not a continuum winding certificate. |
| 左右嵌入残差 | embedded right/left residual | Residuals after zero-padding into a larger cutoff, used to expose unresolved Fourier tails on both nonnormal sides. |
| 独立有限重建 | independent finite reconstruction | A second matrix implementation from the Fourier coefficients of (W_d,W_d''), without importing the primary recurrence. |

## Fixed theorem language

- **Chinese:** 对充分小的正黏性和全部
  (d\in[0,1/450])，共同圆盘内恰有一个代数简单的实解析黏性特征值支；
  其 Riesz 投影在算子范数中一致收敛到无黏投影，特征值误差为
  (O(\varepsilon))。
- **English:** For every sufficiently small positive viscosity and all
  (d\in[0,1/450]), the common disk contains exactly one algebraically
  simple real-analytic viscous eigenvalue branch.  Its Riesz projection
  converges uniformly in operator norm to the inviscid projection, and the
  eigenvalue error is (O(\varepsilon)).

- **Chinese:** 在固定半平面
  (operatorname{Re}z\ge0.12) 内没有其他黏性谱；移除该 rank-one 支后，
  缩减 resolvent 与补空间半群具有参数一致界。
- **English:** There is no other viscous spectrum in the fixed half-plane
  (operatorname{Re}z\ge0.12).  After removal of the rank-one branch, the
  reduced resolvent and complementary semigroup obey parameter-uniform
  bounds.

## Required limitation language

- **Chinese:** 黏度阈值是存在性的，有限 Fourier 计算只作诊断。本节不证明
  长时间非自伴绝热跟踪、匹配作用量、非线性或三维闭合、有限时间奇性，
  也不解决 Clay 问题。
- **English:** The viscosity threshold is existential, and the finite Fourier
  calculation is diagnostic only.  This section does not prove long-time
  nonselfadjoint adiabatic tracking, a matching action, nonlinear or
  three-dimensional closure, finite-time singularity, or the Clay problem.
