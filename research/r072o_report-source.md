# R0.72O -- physical reinsertion doubles the one-carrier strong window, while multi-carrier mixing remains conditional

**Date:** 2026-08-27

**Status:** a proof-grade physical-reinsertion theorem in the fixed-background,
row-aligned, phase-aligned, exact-root-corrected one-carrier triangular
2.5D Navier--Stokes family inherited from R0.72L--N. The R0.72N
enhanced-dissipation cubic estimate survives the exact-root correction and
enlarges the normalized strong-coupling window from order
\(R^{2/3}\log R\) to order \(R^{4/3}(\log R)^2\). It does not close fixed
geometry as the coupling tends to infinity. For a common-band
multi-carrier family, the same algebra follows from an explicit integrated
enhanced-dissipation hypothesis with constants uniform over the compared
family, but the existing common-band assumptions do not imply that
hypothesis. A triangle-rich family excludes naive
carrierwise tensorization, and an exact two-carrier shear has a degenerate
critical point despite amplitude balance and common-band support.

**Keywords:** Navier--Stokes regularity, triangular 2.5D flow, enhanced
dissipation, physical normalization, strong coupling, exact root,
multi-carrier superposition, cross terms, degenerate shear

---

## 0. Direct decision

R0.72N proved the raw one-carrier estimate

\[
 \mathcal C_{\rm diss}\lesssim a^2\varepsilon^{1/2},
 \qquad \varepsilon=\frac{|\delta|a}{R^2},
 \tag{0.1}
\]

but the R0.72L physical root ledger contains

\[
 \frac{\Theta\mathcal C_\times}
 {D^{1/3}\Lambda_{1,*}},
 \qquad
 \Lambda_{1,*}\gtrsim K+x.
 \tag{0.2}
\]

Thus the square-root exponent cannot be inserted directly into the final
dimensionless ledger. For one carrier, \(N=B=p=1\), \(g=\varepsilon R^2\),
and

\[
 \Theta\asymp\frac{g^2}{a^2R^2},
 \qquad
 D^{1/3}\asymp g^{2/3}R^{2/3}.
 \tag{0.3}
\]

Consequently

\[
 \boxed{
 \frac{\Theta(a^2\varepsilon^{1/2})}{D^{1/3}}
 \asymp \varepsilon^{11/6}.}
 \tag{0.4}
\]

The exponent \(11/6\), rather than \(1/2\), is the correct normalized
numerator.

Let

\[
 L_R=1+\log R,
 \qquad
 L_{R,\varepsilon}
 =1+\log\!\left(2+R^2(1+\varepsilon)\right).
 \tag{0.5}
\]

For the R0.72L exact-root-corrected one-carrier launch, the complete ledger
obeys

\[
\boxed{
\begin{aligned}
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 \le C\Bigg[&
 \frac{\varepsilon^{4/3}}{K+x}
 +\varepsilon^{1/3}R^{-1/3}L_R^{-1/2}
   \frac{\sqrt x}{K+x}\\
 &+\frac{\min\{\varepsilon^{7/3},
                  \varepsilon^{1/3}Rx,
                  \varepsilon^{11/6}\}}
        {K+x}\Bigg].
\end{aligned}}
\tag{0.6}
\]

The first two cubic entries in the minimum are the inherited R0.72L
branches. The last is the R0.72N enhanced-dissipation branch after the
physical lift.

The exact-root construction gives

\[
 x\ge Z
 :=c\varepsilon^2R^{2/3}(1+\varepsilon)^{-2/3}
 L_{R,\varepsilon}.
 \tag{0.7}
\]

For \(\varepsilon\ge1\), (0.6)--(0.7) imply

\[
\boxed{
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 \le C\left[
 \frac1{R^{2/3}L_{R,\varepsilon}}
 +\frac{\varepsilon^{-1/3}}
 {R^{2/3}(L_RL_{R,\varepsilon})^{1/2}}
 +\frac{\varepsilon^{1/2}}
 {R^{2/3}L_{R,\varepsilon}}
 \right].}
 \tag{0.8}
\]

Hence the improved one-carrier window is

\[
\boxed{
 \varepsilon^{1/2}
 \lesssim R^{2/3}L_{R,\varepsilon},}
 \tag{0.9}
\]

or equivalently in implicit form,

\[
\boxed{
 \varepsilon
 \lesssim R^{4/3}L_{R,\varepsilon}^{\,2}.}
 \tag{0.10}
\]

Along any fixed polynomial coupling regime,
\(L_{R,\varepsilon}\asymp L_R\), so (0.10) reads

\[
 \varepsilon\lesssim R^{4/3}L_R^2.
 \tag{0.11}
\]

The right side of (0.8) is uniformly bounded at the upper scale and tends
to zero under the little-o version of (0.9). This doubles both the power
of \(R\) and the power of the logarithm in the preceding one-carrier
window.

For fixed \(R\), however, the proven action floor gives only

\[
 \frac{\varepsilon^{11/6}}{K+x}
 \lesssim\frac{\varepsilon^{1/2}}{\log\varepsilon}.
 \tag{0.12}
\]

This upper envelope does not decay. Equation (0.1) closes raw
sublinearity, but not the arbitrarily strong fixed-geometry normalized
ledger.

For \(N\) common-band carriers, define \(p=\sqrt N/B\). Suppose there are
constants \(C_{\rm ED}\ge1\) and \(c_{\rm ED}>0\), uniform over the stated
\((N,p,R,\varepsilon)\) range and the declared geometry family, such that the
**full superposition**, rather than each carrier separately, satisfies

\[
 \int_0^1E(y)\,dy
 \le C_{\rm ED}\varepsilon^{-1/2}E(0),
 \qquad
 E(1)\le C_{\rm ED}e^{-c_{\rm ED}\sqrt\varepsilon}E(0),
 \tag{0.13}
\]

then all self and cross cubic terms obey

\[
 \boxed{
 \mathcal C_\times
 \lesssim a^2N^2\varepsilon^{1/2}.}
 \tag{0.14}
\]

The resulting conditional normalized numerator and window are

\[
 U_{\rm ED}\asymp\varepsilon^{11/6}p^{4/3},
 \tag{0.15}
\]

\[
\boxed{
 \varepsilon^{1/2}
 \lesssim p^{2/3}R^{2/3}L_{R,\varepsilon},
 \qquad
 \varepsilon
 \lesssim p^{4/3}R^{4/3}L_{R,\varepsilon}^{\,2}.}
 \tag{0.16}
\]

Equations (0.13)--(0.16) are conditional for more than one carrier. Their
uniform scaling content requires the stated constants to remain uniform;
with parameter-dependent constants they give only a pointwise implication.
Common-band support and amplitude balance alone do not prove (0.13).

---

## 1. Exact identification of the raw cubic

In the R0.72L common-band notation,

\[
 h=P_0V_wF,
 \qquad b=P_0V_w^2F,
 \qquad
 \mathcal C_\times=|\delta|\int_I|hb|\,dx.
 \tag{1.1}
\]

Take one carrier \(R\), one fixed nonzero orthogonal target \(q_*\), and put
\(\mu=q_*^2/R^2>0\). With \(y=R^2x\) and the phase rotation of R0.72M, the
complete dissipative chain is

\[
 \partial_yf_n=-n^2f_n+\varepsilon e^{-y}(f_{n-1}-f_{n+1}).
 \tag{1.2}
\]

For the antisymmetric launch used in R0.72N,

\[
 h=-2ae^{-(1+\mu)y}f_1,
 \qquad
 b=-2a^2e^{-(2+\mu)y}(f_0-f_2).
 \tag{1.3}
\]

Since \(dx=R^{-2}dy\) and \(|\delta|a/R^2=\varepsilon\), (1.1) becomes

\[
 \mathcal C_\times
 =4a^2\int_0^1\varepsilon e^{-(3+2\mu)y}
 |f_1(f_0-f_2)|\,dy.
 \tag{1.4}
\]

This is exactly the R0.72N quantity \(\mathcal C_{\rm diss}\). There is no
additional physical factor hidden between the two reports.

The normalized root ledger is not (1.4) itself. R0.72L first multiplies
the complete extended-root inequality by \(\Theta\), then divides by
\(D^{1/3}\Lambda_{1,*}\). Equations (0.3)--(0.4) follow by direct exponent
arithmetic:

\[
 \frac{\Theta a^2}{D^{1/3}}
 \asymp
 \frac{g^2R^{-2}}
 {g^{2/3}R^{2/3}}
 =g^{4/3}R^{-8/3}
 =\varepsilon^{4/3}.
 \tag{1.5}
\]

Multiplication by \(\varepsilon^{1/2}\) gives
\(\varepsilon^{11/6}\).

---

## 2. The exact-root correction does not destroy enhanced dissipation

The identities (1.3)--(1.4) use the antisymmetric launch. R0.72L enforces
an exact target root at the short time \(\tau\) by replacing the initial
state \(G\) with

\[
 \widetilde G=G+\zeta e_0,
 \qquad
 |\zeta|\lesssim c_*\frac{\varepsilon}{1+\varepsilon}.
 \tag{2.1}
\]

This correction breaks the symmetry behind (1.3), so the old coordinate
identity cannot simply be quoted. The semigroup estimate, however, is an
operator-norm theorem and is stable under arbitrary \(L^2\) initial data.

### Lemma 2.1 -- bounded-coordinate enhanced-dissipation payment

Let \(S_\varepsilon(y,0)\) be the propagator of (1.2). Assume

\[
 \|S_\varepsilon(y,0)f_0\|_2
 \le M e^{-c\sqrt\varepsilon\,y}\|f_0\|_2,
 \qquad0\le y\le1,
 \tag{2.2}
\]

with \(M,c\) independent of \(\varepsilon\ge1\). For arbitrary initial
data, the one-carrier rows in (1.1) have the form

\[
 h=ae^{-(1+\mu)y}\ell_1(f),
 \qquad
 b=a^2e^{-(2+\mu)y}\ell_2(f),
 \tag{2.3}
\]

where \(\ell_1\) reads only the \(\{\pm1\}\) coordinates and \(\ell_2\)
reads only the \(\{0,\pm2\}\) coordinates. Their operator norms are bounded
by fixed geometric constants. Therefore

\[
 |hb|\le Ca^3e^{-(3+2\mu)y}\|f(y)\|_2^2.
 \tag{2.4}
\]

Using \(|\delta|R^{-2}=\varepsilon/a\), (2.2), and (2.4),

\[
\begin{aligned}
 \mathcal C_\times
 &\le Ca^2\varepsilon\|f_0\|_2^2
 \int_0^1e^{-2c\sqrt\varepsilon\,y}\,dy\\
 &\le Ca^2\varepsilon^{1/2}\|f_0\|_2^2.
\end{aligned}
 \tag{2.5}
\]

The correction (2.1) has \(\|\widetilde G\|_2^2\asymp1\), including after
the harmless energy renormalization in R0.72L. Hence

\[
 \boxed{
 \mathcal C_\times(\widetilde G)
 \lesssim a^2\varepsilon^{1/2}.}
 \tag{2.6}
\]

#### Proof of the semigroup input

With \(t=\varepsilon y\), \(\nu=\varepsilon^{-1}\), and the generating
function \(F(t,\theta)=\sum_nf_n(\nu t)e^{in\theta}\), (1.2) becomes

\[
 \partial_tF
 =\nu\partial_\theta^2F
 +2ie^{-\nu t}\sin\theta\,F.
 \tag{2.7}
\]

This is the fixed horizontal mode \(k=-2\), with horizontal-diffusion
switch zero, in the time-dependent shear theorem of Coble and He. Choose
\(U=V=e^{-\nu t}\sin\theta\). On \(0\le t\le\nu^{-1}\), the two critical
points are fixed and nondegenerate, the amplitude is in \([e^{-1},1]\),
the shape constants are uniform, and

\[
 \|\partial_{t\theta}U\|_\infty
 \le\nu\le\nu^{3/4}.
 \tag{2.8}
\]

Their Theorem 1.2 therefore gives, for \(0<\nu\le\nu_0\),

\[
 \|F(t)\|_2\le C e^{-c\nu^{1/2}t}\|F(0)\|_2,
 \qquad0\le t\le\nu^{-1},
 \tag{2.9}
\]

with constants uniform for this family. Put
\(\varepsilon_*=\max\{1,\nu_0^{-1}\}\). This proves (2.2) when
\(\varepsilon\ge\varepsilon_*\). On the remaining compact interval
\(1\le\varepsilon\le\varepsilon_*\), the imaginary shear term and diffusion
give the \(L^2\) contraction \(\|F(t)\|_2\le\|F(0)\|_2\). Increasing \(M\) by
the fixed factor \(e^{c\sqrt{\varepsilon_*}}\) therefore yields (2.2) for
all \(\varepsilon\ge1\) and \(0\le y\le1\). Equation (2.2) is (2.9) after
\(t=\varepsilon y\). The cubic implication (2.6) is a corollary proved here,
not a theorem stated by Coble and He.

---

## 3. The improved normalized ledger

R0.72L gives, before the new cubic branch,

\[
 \frac{\mathcal J_{\rm all}}
 {D^{1/3}\Lambda_{1,*}}
 \le C\left[
 \frac{U_0}{K+x}
 +W\frac{\sqrt x}{K+x}
 +\frac{\min\{U,Vx\}}{K+x}
 \right],
 \tag{3.1}
\]

where for one carrier

\[
 U_0=\varepsilon^{4/3},
 \quad W=\varepsilon^{1/3}R^{-1/3}L_R^{-1/2},
 \quad U=\varepsilon^{7/3},
 \quad V=\varepsilon^{1/3}R.
 \tag{3.2}
\]

Equation (2.6) adds the branch \(U_{\rm ED}=\varepsilon^{11/6}\), proving
(0.6). If one retains the action branch as well, its new crossover is

\[
 H_{\rm ED}=\frac{U_{\rm ED}}V
 =\frac{\varepsilon^{3/2}}R.
 \tag{3.3}
\]

The scalar optimization is

\[
 \frac{\min\{U_{\rm ED},Vx\}}{K+x}
 \le
 \frac{U_{\rm ED}}
 {K+\max\{H_{\rm ED},Z\}}.
 \tag{3.4}
\]

For the window (0.9), \(Z\gtrsim H_{\rm ED}\); using the weaker denominator
\(K+Z\) is already sufficient. Indeed, for \(\varepsilon\ge1\),

\[
 Z\gtrsim\varepsilon^{4/3}R^{2/3}L_{R,\varepsilon}.
 \tag{3.5}
\]

The first row satisfies

\[
 \frac{U_0}{K+Z}
 \lesssim\frac1{R^{2/3}L_{R,\varepsilon}}.
 \tag{3.6}
\]

The mixed row satisfies

\[
 \frac W{\sqrt{K+Z}}
 \lesssim
 \frac{\varepsilon^{-1/3}}
 {R^{2/3}(L_RL_{R,\varepsilon})^{1/2}}.
 \tag{3.7}
\]

The enhanced-dissipation cubic satisfies

\[
 \frac{U_{\rm ED}}{K+Z}
 \lesssim
 \frac{\varepsilon^{1/2}}
 {R^{2/3}L_{R,\varepsilon}}.
 \tag{3.8}
\]

Equations (3.6)--(3.8) prove (0.8)--(0.10).

### A general exponent-transfer rule

Suppose a raw cubic theorem has the form

\[
 \mathcal C_\times
 \lesssim a^2\varepsilon^\alpha
 L_{R,\varepsilon}^{\,\beta}.
 \tag{3.9}
\]

After the one-carrier physical lift, its numerator is
\(\varepsilon^{4/3+\alpha}L_{R,\varepsilon}^{\beta}\). Relative to the
local floor (3.5), the direct normalized branch is

\[
 \varepsilon^\alpha R^{-2/3}
 L_{R,\varepsilon}^{\beta-1}.
 \tag{3.10}
\]

The old raw estimate has \((\alpha,\beta)=(1,0)\); R0.72N has
\((1/2,0)\); the still-open logarithmic target has \((0,1)\). Thus the
logarithmic sharpen is not required for raw sublinearity, but it becomes
the scale-compatible target for fixed-\(R\) physical payment.

---

## 4. Cross terms under a full-superposition hypothesis

Now return to \(N\) common-band carriers. Write

\[
 V=\sum_lV_l,
 \qquad
 h=P_0VF,
 \qquad
 b=P_0V^2F.
 \tag{4.1}
\]

The R0.72L bounds already include all self and cross terms:

\[
 \rho(y):=\|P_0V(y)\|
 \le Ca\sqrt N e^{-cy},
 \qquad
 \|V(y)\|\le CaB e^{-cy}.
 \tag{4.2}
\]

Since \(E(y)=\|F(y)\|_2^2\),

\[
 |hb|
 \le\rho(y)^2\|V(y)\|E(y)
 \le Ca^3BN e^{-3cy}E(y).
 \tag{4.3}
\]

The common-band rescaling gives

\[
 |\delta|\,dx=\frac{\varepsilon}{aB}\,dy.
 \tag{4.4}
\]

If (0.13) holds with constants uniform in the sense stated there and
\(E(0)\asymp N\) with uniform comparison constants, then

\[
\begin{aligned}
 \mathcal C_\times
 &\le C\varepsilon a^2N
 \int_0^1E(y)\,dy
 +C\varepsilon a^2N E(1)\\
 &\lesssim a^2N^2\varepsilon^{1/2}.
\end{aligned}
 \tag{4.5}
\]

This proves (0.14). The estimate is important for its logical direction:
once the **full** propagation estimate is available, the cross terms do not
cause an additional power loss because they were never expanded
carrierwise.

With

\[
 \Theta\asymp\frac{g^2}{a^2NR^2},
 \qquad
 D^{1/3}\asymp g^{2/3}N^{1/3}R^{2/3},
 \qquad
 p=\frac{\sqrt N}B,
 \tag{4.6}
\]

the conditional numerator is

\[
 \frac{\Theta(a^2N^2\varepsilon^{1/2})}{D^{1/3}}
 \asymp\varepsilon^{11/6}p^{4/3}.
 \tag{4.7}
\]

The strong action floor is

\[
 Z\gtrsim
 \varepsilon^{4/3}p^2R^{2/3}L_{R,\varepsilon}.
 \tag{4.8}
\]

Dividing (4.7) by (4.8) gives

\[
 \frac{\varepsilon^{1/2}}
 {p^{2/3}R^{2/3}L_{R,\varepsilon}},
 \tag{4.9}
\]

which proves the conditional window (0.16).

---

## 5. Why common-band assumptions do not prove the hypothesis

### 5.1 Carrierwise tensorization misses true cross cubics

R0.72J constructed the coherent block

\[
 S_R=\{R,R+1,\ldots,3R-1\},
 \qquad N=2R,
 \tag{5.1}
\]

with

\[
 T_R=3R(R+1)
 \tag{5.2}
\]

ordered signed Schur triples. On its triangle-rich launch,

\[
 \mathcal C_{\times,R}\asymp_\gamma a^2R^2
 \asymp a^2N^2.
 \tag{5.3}
\]

The \(N^2\) factor is therefore not a counting artifact. Any argument that
adds \(N\) independent one-carrier costs and discards mixed triples cannot
recover the true common-band scale. This does not disprove (0.14); it shows
why (0.14), if true, must be proved for the full superposition.

### 5.2 A common-band shear can have a degenerate critical point

For two carriers \(R\) and \(R+1\), take the admissible comparable
coefficients

\[
 U_R(\theta)
 =\sin(R\theta)
 -\frac{R}{R+1}\sin((R+1)\theta).
 \tag{5.4}
\]

At \(\theta=0\),

\[
 U_R'(0)=0,
 \qquad U_R''(0)=0,
 \qquad
 U_R'''(0)=R(2R+1)\ne0.
 \tag{5.5}
\]

Thus the combined shear has a degenerate critical point even though the
frequencies lie in one relative band and the amplitudes are comparable.
Coble--He Theorem 1.2 assumes fixed finitely many **nondegenerate** critical
points with uniform shape neighborhoods. Equation (5.5) proves that the
R0.72L parameters \((R,N,B,p)\) do not by themselves control those shape
constants.

This is a theorem-applicability obstruction, not a counterexample to the
final multi-carrier bound. The exact missing statement is (0.13), or the
weaker rowwise flux estimate (0.14) directly.

---

## 6. Literature boundary

Coble and He study the linear passive-scalar equation under a
time-dependent shear. Their Theorem 1.2 provides the
\(e^{-c\nu^{1/2}|k|^{1/2}t}\) mode decay under a nondegenerate critical-point
and slow-reference-shear hypothesis. The one-carrier mapping and the cubic
projection (2.3)--(2.6) are project-specific corollaries.

Coti Zelati and Gallay show for stationary parallel shears that the
enhanced-dissipation exponent depends on critical-point degeneracy. Their
one-dimensional theorem gives the rate
\(\nu^{m/(m+2)}|k|^{2/(m+2)}\) when derivatives through order \(m\) are used
to control the profile; the Morse/nondegenerate case corresponds to
\(m=2\). This supports the need to retain shear-shape data, but does not
prove (0.13) for the present time-dependent multi-carrier family.

The nonlinear stability theories for three-dimensional Couette and special
Kolmogorov flows control nonzero--nonzero interactions with flow-specific
anisotropic energies and thresholds. They are methodological precedents,
not black-box theorems for the present carrier family.

No primary source found in the bounded search states the physical
reinsertion theorem (0.6)--(0.10), the conditional cross-term implication
(0.13)--(0.16), or a uniform common-band theorem based only on
\((R,N,B,p)\). This is not a claim of novelty or priority.

---

## 7. Exact and finite audit

The analytic proof is the result. Two independent exact-arithmetic
implementations audit the exponent ledger:

1. the producer uses Python rational exponent dictionaries;
2. the independent route uses a separate JavaScript rational monomial
   implementation.

They separately verify

\[
 U_{\rm ED}^{(1)}=\varepsilon^{11/6},
 \qquad
 U_{\rm ED}^{(N)}=\varepsilon^{11/6}p^{4/3},
 \qquad
 H_{\rm ED}=\frac{\varepsilon^{3/2}p}{R},
 \tag{7.1}
\]

\[
 \frac{U_{\rm ED}}Z
 =\frac{\varepsilon^{1/2}}
 {p^{2/3}R^{2/3}L_{R,\varepsilon}},
 \tag{7.2}
\]

and the exact derivative identities (5.5). A deterministic parameter grid
plots the old and new normalized cubic screens around the predicted
window. Those finite points illustrate the algebra and do not prove the
semigroup theorem, the local action floor, or any Navier--Stokes
continuation statement.

---

## 8. Claim boundary

R0.72O proves, in the declared one-carrier exact-corrected family:

1. exact identification of the R0.72N raw cubic with the R0.72L cubic row;
2. the physical-lift exponent \(11/6\);
3. stability of the enhanced-dissipation cubic bound under the exact-root
   correction;
4. the improved normalized ledger (0.6);
5. the strong-coupling window (0.9)--(0.11);
6. the fixed-geometry proof-method boundary (0.12).

It also proves the implication

\[
 \text{full-superposition integrated ED}
 \Longrightarrow
 \mathcal C_\times\lesssim a^2N^2\varepsilon^{1/2}
 \Longrightarrow
 \text{conditional window (0.16)}.
 \tag{8.1}
\]

It does not prove:

1. (0.13) from the current common-band hypotheses;
2. a logarithmic one-carrier cubic theorem;
3. an arbitrarily strong fixed-geometry closure;
4. multiscale physical absorption;
5. a continuation criterion for arbitrary three-dimensional solutions;
6. finite-time singularity or global smoothness for general
   Navier--Stokes.

The Clay Millennium problem remains open.

---

## 9. Next exact gate

R0.72P should attack the full-superposition interface directly. The clean
target is either

\[
 \int_0^1E(y)\,dy
 \lesssim\varepsilon^{-1/2}E(0)
 \tag{9.1}
\]

with an explicit shape parameter controlling critical-point degeneracy, or
the weaker rowwise estimate

\[
 |\delta|\int|P_0VF\,P_0V^2F|\,dx
 \lesssim a^2N^2\varepsilon^{1/2}.
 \tag{9.2}
\]

A fixed finite carrier pattern with a verified uniform Morse margin is the
first honest positive class. The parallel optional gate remains the
one-carrier logarithmic bounded-variation estimate, which would settle the
fixed-\(R\) exponent transfer without a growing geometric scale.

---

## References used at this gate

1. D. Coble and S. He, *A Note on Enhanced Dissipation and Taylor
   Dispersion of Time-dependent Shear Flows*, arXiv:2309.15738; published
   as *A Note on Enhanced Dissipation of Time-Dependent Shear Flows*,
   *Communications in Mathematical Sciences* **22** (2024), 1663--1691,
   [DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10).
2. M. Coti Zelati and T. Gallay, *Enhanced Dissipation and Taylor
   Dispersion in Higher-dimensional Parallel Shear Flows*, *Journal of the
   London Mathematical Society* **108** (2023), 1358--1392,
   [DOI](https://doi.org/10.1112/jlms.12782).
3. J. Bedrossian, P. Germain, and N. Masmoudi, *On the Stability Threshold
   for the 3D Couette Flow in Sobolev Regularity*, *Annals of Mathematics*
   **185** (2017), 541--608,
   [journal](https://annals.math.princeton.edu/2017/185-2/p04).
4. T. Li, D. Wei, and Z. Zhang, *Pseudospectral Bound and Transition
   Threshold for the 3D Kolmogorov Flow*, *Communications on Pure and
   Applied Mathematics* **73** (2020), 465--557,
   [arXiv:1801.05645](https://arxiv.org/abs/1801.05645).
