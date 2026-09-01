# R0.74J bilingual dictionary and publication boundary

**Status:** research-side terminology freeze for the matching complete-payment
law on the exact R0.74F--H family analysed in R0.74I

**Release title (en):** R0.74J | A matching complete-payment law from the
fifth payment shell

**Public title (zh):** R0.74J｜第五支付壳给出的匹配完整支付律

**Ordinary translation path:** `LOCAL_DIRECT_NO_DGX`

**DGX used for translation:** `false`

## 1. Locked publication lead

### Chinese

> 这一节仍然没有解决三维 Navier--Stokes 千禧年问题。我重新核对了
> R0.74F--H 构造并在 R0.74I 中再次分析的精确、光滑、周期、无外力
> 解族。在支付半径
> \(2R_j\) 的第五壳，一个固定盒中的背景剪切在整个支付时间窗内保持
> 至少 \(1/2\)，所以非负的速度三次项给出
> \(8e^{-8}B_j^3R_j^3\) 的下界。与 R0.74G 已证明的上界合并后，
> Version M 和 Version F 的共同完整支付量满足
> \(P_j\asymp B_j^3R_j^3\)，并且
> \(\log P_j/L_j^2\to3/320\)。这是一个精确解族上的匹配支付律，
> 不是普适平方根对数端点上界；它没有给出 \(X_j\) 或
> \(\mathfrak C_j\) 的匹配上界，也没有在可能奇点处制造小量条件。
> **NOT CLAY.**

### English

> This release still does not solve the three-dimensional Navier--Stokes
> Millennium problem. I revisit the exact smooth periodic unforced family
> constructed across R0.74F--H and analysed again in R0.74I. On the fifth
> shell at payment radius
> \(2R_j\), a fixed box keeps the background shear above \(1/2\) throughout
> the payment interval, so the nonnegative velocity-cubic row gives the lower
> bound \(8e^{-8}B_j^3R_j^3\). Combined with the proved R0.74G upper bound,
> the common Version-M and Version-F complete payment satisfies
> \(P_j\asymp B_j^3R_j^3\), with
> \(\log P_j/L_j^2\to3/320\). This is a matching payment law on one exact
> family, not a universal square-root-log endpoint upper bound. It proves no
> matching upper bound for \(X_j\) or \(\mathfrak C_j\) and does not create
> the required smallness at a possible singular point. **NOT CLAY.**

## 2. Canonical mathematical terms

| 中文 | English | Required meaning |
|---|---|---|
| R0.74F--H 精确解族 | exact R0.74F--H family | The explicit smooth periodic unforced family constructed across R0.74F--H and analysed in R0.74I; R0.74J does not construct a new family |
| 完整支付量 | complete payment | The frozen nonnegative Version-M or Version-F payment, including every required row |
| 匹配完整支付律 | matching complete-payment law | The two-sided familywise estimate \(P_j\asymp B_j^3R_j^3\), with constants independent of all sufficiently large \(j\) |
| 支付半径 | payment radius | The radius \(2R\) or \(2R_j\) at which the complete payment row is evaluated |
| 支付壳 | payment shell | A weighted annulus \(A_k(2R)\) entering \(W_{2R}\) |
| 第五支付壳 | fifth payment shell | \(A_5(2R)=\{64R\le |x|<128R\}\), carrying weight \(\Gamma_5=e^{-8}\) |
| 证明盒 | proof box | \(Q_R=\{|x_1|<R,\ |x_2|<R,\ 80R<x_3<96R\}\subset A_5(2R)\) |
| 正剪切平台 | positive shear platform | The interval on which the initial shear equals one and whose caloric evolution stays above \(1/2\) on the proof box |
| 背景剪切 | background shear | The second velocity component \(B_j\theta_j\), not the passive packet |
| 速度三次项 | velocity-cubic row | The nonnegative row \(\mathcal G_u\) containing the weighted integral of \(|u|^3\) |
| 匹配支付下界 | matching payment lower bound | \(P_j\ge8e^{-8}B_j^3R_j^3\), obtained from the fifth-shell velocity-cubic row |
| 继承上界 | inherited upper bound | The R0.74G theorem \(P_j\le C B_j^3R_j^3\) for the same family and amplitude |
| 对数支付率 | logarithmic payment rate | \(\log P_j/L_j^2\to3/320\) on the exact family |
| 稀疏支付渐近 | lacunary payment asymptotic | \(\log(P_{j+1}/P_j)=9\rho L_j^2+O(1)\) |
| 平方根对数端点 | square-root-log endpoint | The candidate scale \(P^{2/3}\sqrt{1+\log_+P}\); no universal endpoint upper estimate is proved |
| 仅解族结论 | familywise result | A result proved on the exact R0.74F--H sequence, not for arbitrary suitable weak solutions |
| 限定式文献边界 | bounded literature boundary | A finite primary-source comparison used to avoid prior-art collisions; it is not evidence of novelty or priority |
| 最终源重绑定 | final source rebind | A byte-level audit that binds the final promoted manuscript and release evidence after all repairs are complete |

## 3. Mandatory notation disambiguation

### 3.1 Target-shell weight versus payment-shell weight

The passive-packet amplitude uses the target-shell weight

\[
 \boxed{
 \gamma_j^{\rm tar}
 =e^{-4^{j-1}/32}
 =e^{-c_\gamma L_j^2},
 \qquad c_\gamma=\frac8{3969}.}
\]

Indeed,

\[
 c_\gamma L_j^2
 =\frac8{3969}\left(\frac{63}{32}\right)^2 4^j
 =\frac{4^{j-1}}{32}.
\]

It appears only in

\[
 \mathfrak a_j=B_j(\gamma_j^{\rm tar})^{-1/2}.
\]

The complete-payment weight instead uses

\[
 \boxed{
 W_{2R}(x)=\sum_{k\ge1}\Gamma_k1_{A_k(2R)}(x),
 \qquad \Gamma_k=e^{-4^{k-1}/32}.}
\]

Thus \(\Gamma_5=e^{-8}\). The two symbols follow the same numerical weight
law but have different roles and indices. Public text must not replace either
symbol by a bare \(\gamma_j\), and it must not write the fifth payment weight
as \(\gamma_5\).

### 3.2 Decay rate versus payment radius

The symbol

\[
 \boxed{\rho=\frac1{320}}
\]

is reserved for the scale-decay rate in

\[
 R_j=e^{-\rho L_j^2}.
\]

The payment radius must be written literally as \(2R\) or \(2R_j\).
Published prose must not write “payment radius \(\rho=2R\)”. If a generic
auxiliary radius is unavoidable, use \(\varrho\), not \(\rho\).

### 3.3 Scaled amplitude scalar versus inherited shear field

The canonical R0.74J scalar is

\[
 \boxed{\beta_j:=B_jR_j^2\longrightarrow\frac1{128}.}
\]

Public text must use \(\beta_j\) for this scalar. It must not call it
\(b_j\), because the inherited R0.74F notation
\(b_j(t,x_3)=B_j\theta_j(t,x_3)\) denotes the shear field. In R0.74J, write
that field directly as \(B_j\theta_j(t,x_3)\).

### 3.4 Common Version-M and Version-F payment

On the exact family,

\[
 \boxed{P_j:=P_{R_j}^M=P_{R_j}^F.}
\]

After this definition, use \(P_j\) for the common quantity. Do not introduce
undefined symbols \(P_j^M\) or \(P_j^F\). When both versions must remain
visible, write the full equality above.

### 3.5 Exact family and logarithm convention

The canonical family name is “the exact R0.74F--H family, as analysed in
R0.74I”. R0.74I did not create a new family, so public text must not relabel
the family as “R0.74F--I”.

The universal endpoint expression uses

\[
 \log_+P=\log\max\{P,1\}.
\]

The exact-family limit may use \(\log P_j\), because the matching lower bound
implies \(P_j>1\) for all sufficiently large \(j\).

## 4. Evidence labels

| Label | Public meaning |
|---|---|
| **PROVED** | Established by the R0.74J continuum analytic proof, with every inherited input named |
| **INHERITED** | Established in an earlier frozen release and used here without being re-proved; the source theorem must be cited |
| **FINITE** | Checked by exact finite arithmetic or deterministic structural validation only; it is not a PDE proof |
| **AUDIT PASS** | An independent check passed on the exact bound byte sequence; this label does not strengthen the theorem |
| **LITERATURE BOUNDARY** | A primary-source scope comparison or finite non-hit; not a novelty or priority result |
| **OPEN** | Not established by R0.74J or the cited inherited results |
| **NOT CLAIMED** | Deliberately excluded, including novelty, priority, and any universal endpoint theorem |
| **NOT CLAY** | No global regularity, blow-up, singularity-exclusion, or Millennium-problem conclusion |

The analytic theorem, inherited upper bound, finite certificate, literature
boundary, and open statements must remain visibly separate on the HTML and
PDF versions.

## 5. Mandatory bilingual boundary sentences

| 中文冻结句 | Mandatory English sentence |
|---|---|
| 本节证明的是 R0.74F--H 精确解族（按 R0.74I 的分析）上的匹配完整支付律，不是任意适合弱解的普适支付定理。 | “This release proves a matching complete-payment law on the exact R0.74F--H family as analysed in R0.74I, not a universal payment theorem for arbitrary suitable weak solutions.” |
| 第五支付壳中的固定证明盒给出 \(8e^{-8}B_j^3R_j^3\) 的解析下界；R0.74G 提供同阶继承上界。 | “The fixed proof box in the fifth payment shell gives the analytic lower bound \(8e^{-8}B_j^3R_j^3\); R0.74G supplies the inherited upper bound of the same order.” |
| \(\gamma_j^{\rm tar}\) 是被动包振幅使用的目标壳权重，\(\Gamma_k\) 是完整支付使用的第 \(k\) 壳权重。 | “The symbol \(\gamma_j^{\rm tar}\) is the target-shell weight used in the passive-packet amplitude, whereas \(\Gamma_k\) is the \(k\)-th shell weight used in the complete payment.” |
| \(\rho=1/320\) 只表示尺度衰减率；完整支付在半径 \(2R_j\) 处计算。 | “The symbol \(\rho=1/320\) denotes only the scale-decay rate; the complete payment is evaluated at radius \(2R_j\).” |
| 标量 \(\beta_j=B_jR_j^2\) 不得与早期记号中的剪切场 \(b_j(t,x_3)=B_j\theta_j(t,x_3)\) 混淆。 | “The scalar \(\beta_j=B_jR_j^2\) must not be confused with the inherited shear-field notation \(b_j(t,x_3)=B_j\theta_j(t,x_3)\).” |
| 在这个精确解族上，\(P_j\) 是 Version M 与 Version F 的共同完整支付量。 | “On this exact family, \(P_j\) is the common Version-M and Version-F complete payment.” |
| 有限证书只核对 38 行精确算术，不证明周期热半群论证、Navier--Stokes 解族或继承上界。 | “The finite certificate checks only 38 rows of exact arithmetic; it does not prove the periodic heat-semigroup argument, the Navier--Stokes family, or the inherited upper bound.” |
| 图件是严格几何与支付蕴含图，不是 DNS、数值仿真、实验数据或奇性证据。 | “The figure is a diagram of rigorous geometry and payment implications, not DNS, numerical simulation, experimental data, or evidence of a singularity.” |
| 平方根对数端点上界、\(X_j\) 与 \(\mathfrak C_j\) 的匹配上界、以及可能奇点处的小量机制仍然开放。 | “The square-root-log endpoint upper bound, matching upper bounds for \(X_j\) and \(\mathfrak C_j\), and a smallness mechanism at a possible singular point all remain open.” |
| 限定式检索的未命中不等于新颖性、优先权、不存在或第一性证明。 | “A non-hit in the bounded search is not proof of novelty, priority, non-existence, or first authorship.” |
| 任意三维光滑无散初值的全局正则性与 Clay 千禧年问题仍然开放。 | “Global regularity for arbitrary smooth divergence-free three-dimensional data and the Clay Millennium problem remain open.” |
| 普通中英翻译在本机直接完成，不调用 DGX。 | “Ordinary Chinese--English translation is performed directly on the local workstation; DGX is not used.” |

## 6. Machine-readable release boundary

```text
researchVersion=R0.74J
exactFamilyScope=R0.74F_THROUGH_R0.74H_ANALYSED_IN_R0.74I
publicTitleZh=R0.74J｜第五支付壳给出的匹配完整支付律
matchingCompletePaymentLaw=PROVED_EXACT_FAMILY_ONLY
fifthShellAnalyticLower=PROVED
completePaymentUpper=INHERITED_R0.74G
commonPayment=P_j_EQUALS_P_Rj_M_EQUALS_P_Rj_F
targetWeightSymbol=gamma_j_tar
paymentWeightSymbol=Gamma_k
decayRate=rho_EQUALS_1_OVER_320
paymentRadius=2R_NOT_RHO
scaledAmplitudeScalar=beta_j_EQUALS_B_j_R_j_SQUARED
logPaymentRate=3_OVER_320
lacunarityCoefficient=9_OVER_320
finiteCertificate=38_OF_38_EXACT_ARITHMETIC
squareRootLogEndpointUpper=OPEN
matchingUpperForXj=OPEN
matchingUpperForCollarFlux=OPEN
paymentSmallAtPossibleSingularity=OPEN
paymentToAdmissibility=OPEN
literatureSearch=BOUNDED_NOT_NOVELTY_PROOF
ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX
dgxUsedForTranslation=false
figureEvidence=EXACT_DIAGRAM_NOT_SIMULATION
arbitraryDataGlobalRegularity=OPEN
clayConclusion=NOT_CLAIMED
noveltyOrPriorityClaim=NOT_CLAIMED
NOT CLAY
```

## 7. Publication handling

- Use the locked Chinese title and lead verbatim unless a mathematical error is
  found during final source rebind.
- Keep the Chinese HTML, English translation, and synchronized PDF consistent
  with the notation rules above.
- Display **PROVED**, **INHERITED**, **FINITE**, **LITERATURE BOUNDARY**,
  **OPEN**, and **NOT CLAY** as separate evidence classes.
- Use the formal figure as an exact proof diagram and retain its explicit
  `NOT DNS`, `NOT SIMULATION`, and `NOT CLAY` boundaries.
- Do not create a cumulative recap for R0.74J alone. This ordinary section
  preserves the previous milestone recap unchanged.
- Publish only through the GitHub repository and GitHub Pages route specified
  by the project.
