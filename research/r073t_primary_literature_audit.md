# R0.73T primary-literature collision audit

**Search date:** 2026-08-31

**Scope:** three-dimensional periodic incompressible Navier--Stokes; quartic
energy, deterministic Fourier autocorrelation, turbulence correlation
functions, and Fourier-space regularity criteria

**Status:** bounded primary-source search complete; the three-family stop rule
and the Li--Sire/Serrin/energy-density-Wiener targeted checks are complete

**Priority boundary:** this is a collision audit, not evidence of priority

## 1. Collision verdict

With the R0.73T Fourier normalization, write

\[
 a_k(t)=\widehat u(k,t),\qquad
 C_h(t)=\sum_k a_{k+h}(t)\cdot\overline{a_k(t)}
       =\widehat{|u|^2}(h,t).
\]

The following distinctions are decisive.

| Question | Audit answer | Release consequence |
|---|---|---|
| Is the identity $C_h=\widehat{\lvert u\rvert^2}(h)$, and hence $Q=\sum_h\lvert C_h\rvert^2=\lVert u\rVert_4^4$, new? | **No.** It is the convolution theorem plus Parseval. | Treat as `VERIFIED_CLASSICAL`, not an R0.73T theorem. |
| Is the exact evolution of the complete family $C_h$ new? | **No at the level of mathematical content.** It is exactly the spatial Fourier transform of the classical local energy identity. | The equality itself is a complete classical collision, even though the literal $C_h$ packaging was not found in the bounded search. |
| Does that equality close autonomously in $C$? | **No.** It contains a frequency-weighted gradient correlation and a cubic pressure/flux correlation. | Any claim of a closed $C$-only dynamics is excluded. |
| Is quartic energy evolution new? | **No.** Exact $L^q$ identities, including $q=4$, and pressure-correlation criteria are already in the literature. | The $Q=\lVert u\rVert_4^4$ differential identity is classical. |
| Is a uniform $Q$ bound a new regularity criterion? | **No.** $u\in L_t^\infty L_x^4$ on a finite interval lies inside the classical Ladyzhenskaya--Prodi--Serrin regime. | Novelty cannot be attached merely to bounded $Q$. |
| Is an integrable (or uniform) full-field $A=\sum_h\lvert C_h\rvert$ bound a new criterion? | **No.** Fourier inversion gives $\lVert u\rVert_\infty^2=\lVert\lvert u\rvert^2\rVert_\infty\le A$; hence $\int_0^TA\,dt<\infty$ gives the classical $L_t^2L_x^\infty$ condition. | The unresolved issue is deriving such an $A$ budget from admissible data. A single shell $A_j$ is insufficient for the full velocity. |
| Was a paper found that designates this deterministic off-diagonal $C_h$ as the main dynamic variable and proves a $C_h$- or weighted-$C_h$-based regularity criterion? | **No direct literal collision located.** | This is only a bounded-search negative, not a priority claim or proof of absence. |

## 2. Exact identity and the closure gap

For a smooth solution of

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
\]

the local energy equality is

\[
 \partial_t|u|^2+
 \nabla\!\cdot\!\bigl((|u|^2+2p)u\bigr)
 =\nu\Delta|u|^2-2\nu|\nabla u|^2.
\]

Termwise Fourier transformation therefore gives

\[
 \boxed{
 \partial_t C_h
 =-\nu|h|^2C_h-2\nu D_h-i h\cdot F_h,}
 \tag{2.1}
\]

where

\[
 D_h=\widehat{|\nabla u|^2}(h)
 =\sum_k (k+h)\cdot k\,
   a_{k+h}\cdot\overline{a_k},
 \qquad
 F_h=\widehat{(|u|^2+2p)u}(h).
\]

Thus viscosity does not act as $-2\nu|k|^2$ on the already-summed
quantity $C_h$.  The missing linear information is the weighted
off-diagonal correlation $D_h$; the nonlinear missing information is the
cubic pressure flux $F_h$.  At $h=0$, (2.1) reduces to the global energy
equality.  For $h\ne0$, neither $D_h$ nor $ih\cdot F_h$ is determined by
the scalar sequence $C$.

For the frozen shell equation

\[
 \partial_tu_j=\Delta u_j-N_j,
\]

the corresponding exact form is

\[
 \boxed{
 \partial_tC_j(h)
 =-|h|^2C_j(h)-2G_j(h)-2H_j(h),}
 \qquad
 G_j=\widehat{|\nabla u_j|^2},\quad
 H_j=\widehat{u_j\cdot N_j}.
 \tag{2.2}
\]

Taking the $\ell^2_h$ pairing with $C_j$, equivalently testing the
projected equation by $|u_j|^2u_j$, yields

\[
 \boxed{
 {1\over4}{d\over dt}Q_j+\mathcal D_j
 =-\int_{\mathbb T^3}|u_j|^2u_j\cdot N_j,}
 \tag{2.3}
\]

with

\[
 \mathcal D_j=\int |u_j|^2|\nabla u_j|^2
 +{1\over2}\int|\nabla|u_j|^2|^2.
\]

For the unprojected solution the transport term cancels and (2.3) becomes
the classical pressure-driven quartic identity

\[
 {1\over4}{d\over dt}\|u\|_4^4
 +\nu\int |u|^2|\nabla u|^2
 +{\nu\over2}\int|\nabla|u|^2|^2
 =\int p\,u\cdot\nabla|u|^2.
 \tag{2.4}
\]

The functional $A=\sum_h|C_h|$ adds a second obstruction: it is
nondifferentiable at zero coefficients, and even an upper-Dini estimate from
(2.1) introduces $\sum_h|D_h|$ and
$\sum_h|h\cdot F_h|$.  These are not functions of $C$ alone.

### 2.1 Frequency-localized coercivity: exact citation boundary

Li--Sire's Theorem 4.2 is explicitly periodic and frequency localized: for a
**real scalar** $f$, $0<s\le2$, $1<p<\infty$, and their fixed smooth annular
projector $P_N$, equations (4.96)--(4.97) give

\[
 \int_{\mathbb T^d}(\Lambda^sP_Nf)
       |P_Nf|^{p-2}P_Nf
 \ge c_{p,s,d,\psi}N^s\lVert P_Nf\rVert_p^p.
 \tag{2.5}
\]

Thus $p=4$, $s=2$, and $d=3$ are directly covered in the scalar case.
Remark 4.1 says that similar results hold for complex- and vector-valued
functions, but its displayed vector example belongs to the mean-zero theorem
(Theorem 4.1); it does **not** formally restate frequency-localized Theorem 4.2
for vectors.  On a strict citation audit, “Theorem 4.2 + Remark 4.1” is therefore
strong support but not a literal standalone vector theorem.

The R0.73T vector conclusion nevertheless follows without that extrapolation.
For a shell $u_j=P_Nu$, apply scalar (2.5) componentwise and use the exact
$p=4$ integrations by parts:

\[
\begin{aligned}
 \mathcal D_j
 &=-\int\Delta u_j\cdot|u_j|^2u_j
 \ge \sum_{m=1}^3\int u_{j,m}^2|\nabla u_{j,m}|^2 \\
 &=\frac13\sum_{m=1}^3
   \left(-\int(\Delta u_{j,m})u_{j,m}^3\right)
 \ge c_\psi N^2\sum_{m=1}^3\lVert u_{j,m}\rVert_4^4
 \ge c'_\psi N^2\lVert u_j\rVert_4^4.
\end{aligned}
 \tag{2.6}
\]

Li--Sire's Lemma 4.4 is also explicitly vector-valued and supplies the
dissipation lemma needed to adapt the proof of Theorem 4.2 directly to vector
fields.  The domain change from
$[-\tfrac12,\tfrac12]^3$ to $[0,2\pi]^3$ only rescales frequency and constants.
What is not automatic is replacing Li--Sire's cutoff $\psi$ by an arbitrary
annular multiplier; R0.73T must either use the same class of fixed cutoffs or
record the cutoff-dependent proof and treat finitely many low shells
separately.

### 2.2 The $A$-integrability implication and the Serrin endpoint

For the **full-field** energy-density Wiener norm, absolute Fourier inversion
gives, for almost every time at which $A(t)<\infty$,

\[
 \lVert u(t)\rVert_\infty^2
 =\bigl\lVert |u(t)|^2\bigr\rVert_\infty
 \le \sum_h|C_h(t)|=A(t).
 \tag{2.7}
\]

Consequently

\[
 \int_0^T A(t)\,dt<\infty
 \quad\Longrightarrow\quad
 u\in L^2(0,T;L^\infty(\mathbb T^3)).
 \tag{2.8}
\]

With $p$ denoting the space exponent and $q$ the time exponent, (2.8) is the
critical-equality pair $(p,q)=(\infty,2)$:
$2/q+3/p=1$.  It is the spatial-$L^\infty$ end of the classical
Ladyzhenskaya--Prodi--Serrin family.  It is **not** the difficult
$(p,q)=(3,\infty)$ endpoint treated by Escauriaza--Seregin--Šverák
([DOI](https://doi.org/10.1070/RM2003v058n02ABEH000609)).  Indeed, the usual
$H^1$ estimate already closes
by Gronwall because its coefficient is $\lVert u(t)\rVert_\infty^2\in L^1_t$.
At the Galerkin/strong-solution level,

\[
 {1\over2}{d\over dt}\lVert\nabla u\rVert_2^2
 +\nu\lVert\Delta u\rVert_2^2
 \le \lVert u\rVert_\infty\lVert\nabla u\rVert_2
       \lVert\Delta u\rVert_2
 \le {\nu\over2}\lVert\Delta u\rVert_2^2
    +{1\over2\nu}\lVert u\rVert_\infty^2\lVert\nabla u\rVert_2^2,
 \tag{2.9}
\]

which is the standard approximation-level estimate behind this easy end of
the criterion.
The historical attribution should therefore be “the LPS class,” not a claim
that every modern endpoint formulation appears verbatim in Serrin's 1962
paper.  Bradshaw--Grujić's primary text explicitly records the equality class
$3\le p\le\infty$, $2\le q\le\infty$ and distinguishes the $p=3$ endpoint.

Equation (2.8) does not follow from a single shell norm $A_j$: that only yields
$u_j\in L^2_tL^\infty_x$.  A regularity statement for the full velocity still
needs a summable cross-shell aggregation.

### 2.3 Consequential claim / source / gap checks

| Consequential claim | Primary source and visible evidence | Audit conclusion | Remaining gap / release label |
|---|---|---|---|
| $\mathcal D_j\gtrsim N^2\lVert u_j\rVert_4^4$ for a periodic vector shell | D. Li, Y. Sire, *Remarks on the Bernstein inequality for higher order operators and related results* (2023), Theorem 4.2, Remark 4.1 and Lemma 4.4. [DOI](https://doi.org/10.1090/tran/8708), [open arXiv text](https://arxiv.org/html/2109.07952v1) | Scalar, periodic, $p=4$, $s=2$ is literal; vector coercivity follows by (2.6), while Lemma 4.4 is explicitly vector-valued. | Theorem 4.2 + Remark 4.1 alone are not a literal frequency-localized vector statement. Match the cutoff or include the short componentwise proof. `VERIFIED_CLASSICAL_WITH_ADAPTATION`. |
| $\int_0^TA\,dt<\infty\Rightarrow u\in L_t^2L_x^\infty\Rightarrow$ regularity | J. Serrin (1962), [DOI](https://doi.org/10.1007/BF00253344); Bradshaw--Grujić (2017), primary statement of $3\le p\le\infty$, $2\le q\le\infty$, $2/q+3/p=1$, [arXiv](https://arxiv.org/html/1501.01043) | The first arrow is (2.7); the second is the LPS pair $(p,q)=(\infty,2)$ and also follows from the standard $H^1$ Gronwall estimate. | Full-field $A$, strong $L_t^2L_x^\infty$, and exponent convention must be stated. Not the hard $(3,\infty)$ endpoint and not a shellwise criterion. `VERIFIED_CLASSICAL`. |
| Exact $C_h$ evolution and an attempted $AQ$ evolution | C. V. Tran, X. Yu, D. G. Dritschel (2021), local-energy and exact $L^q$ balances, [DOI / open text](https://doi.org/10.1017/jfm.2020.1033) | Fourier transforming the local-energy identity gives (2.1); differentiating $A$ introduces Wiener norms of $D_h$ and $h\cdot F_h$. | No autonomous $C$- or $(A,Q)$-only estimate follows. `VERIFIED_CLASSICAL_IDENTITY`; closure remains open/negative at this level. |
| No prior deterministic energy-density-Wiener $A$ or $AQ$ dynamic criterion was found | Velocity-Wiener near-neighbours: Ambrose--Lopes Filho--Nussenzveig Lopes (2024), [DOI](https://doi.org/10.1090/proc/16615); Biswas--Jolly--Martinez--Titi (2014), [DOI](https://doi.org/10.1007/s00332-014-9195-8). Energy-spectrum near-neighbour: Mazzucato (2005), [DOI](https://doi.org/10.1088/0951-7715/18/1/001), [author PDF](https://sites.psu.edu/alm24/files/2023/06/nonlin.pdf). | The Wiener papers control velocity coefficients/analyticity. Mazzucato controls decay of the diagonal/radial or Littlewood--Paley energy spectrum. None of the inspected sources defines $C_h=\widehat{\lvert u\rvert^2}(h)$ as the state or derives an $A$, $Q$, or $AQ$ evolution/criterion. | This is a bounded-search negative only. **Not located is not a novelty or priority proof.** `COLLISION_NOT_LOCATED_WITH_LIMITATIONS`. |

## 3. Primary-source provenance / gap matrix

| ID / family | Primary source | Visible source evidence | Overlap with R0.73T | Difference / remaining gap | Confidence |
|---|---|---|---|---|---|
| Lp-1 | G. Prodi, *Un teorema di unicità per le equazioni di Navier--Stokes* (1959), Ann. Mat. Pura Appl. 48, 173--182. [DOI](https://doi.org/10.1007/BF02410664) | Springer metadata and abstract identify a uniqueness theorem for generalized Navier--Stokes solutions. | Historical Prodi half of the velocity space--time integrability route. | No Fourier correlation variable and no evolution law for $C_h$. The exact theorem text was not openly exposed in the publisher view used here. | High on metadata; medium-high on theorem mapping. |
| Lp-2 | J. Serrin, *On the interior regularity of weak solutions of the Navier--Stokes equations* (1962), Arch. Ration. Mech. Anal. 9, 187--195. [DOI](https://doi.org/10.1007/BF00253344) | Springer record verifies title, year, volume and pages; the primary paper is the classical interior-regularity source. Bradshaw--Grujić's open primary text explicitly records the modern equality family $3\le p\le\infty$, $2\le q\le\infty$, $2/q+3/p=1$. | A finite-interval $L_t^\infty L_x^4$ bound is safely inside LPS; $L_t^2L_x^\infty$ is the spatial-$\infty$ critical-equality end. | Use “LPS class” for historical attribution rather than assigning every modern endpoint formulation verbatim to Serrin 1962. Neither hypothesis supplies its own a priori bound or a $C_h$ closure. | High on the classification; explicit attribution caveat. |
| Lp-3 | O. A. Ladyzhenskaya, *The Mathematical Theory of Viscous Incompressible Flow*, 2nd English ed. (1969), Gordon and Breach, ISBN 0677207603. [catalogue record](https://ci.nii.ac.jp/ncid/BA01437879.amp) | The bibliographic record verifies author, edition, publisher, year, translation and subject. | Historical monograph anchor for the Ladyzhenskaya--Prodi--Serrin family and classical energy methods. | Bibliographic anchor only: no stable official open scan or theorem page was inspected, so this row is not used to support a formula-level collision. | Medium; explicit access gap. |
| Lp-4 | T. Kato, *Strong $L^p$-solutions of the Navier--Stokes equation in $\mathbb R^m$, with applications to weak solutions* (1984), Math. Z. 187, 471--480. [DOI](https://doi.org/10.1007/BF01174182) | Publisher metadata and the paper title identify the strong-$L^p$ solution framework and its weak-solution application. | Confirms that strong $L^p$ continuation is a classical route. | Whole-space coefficient-amplitude theory, not deterministic cross-shift correlations on $\mathbb T^3$. | High on scope; medium-high on formula-level detail. |
| Lp-5 | Y. Giga, *Solutions for semilinear parabolic equations in $L^p$ and regularity of weak solutions of the Navier--Stokes system* (1986), J. Differential Equations 62, 186--212. [DOI / publisher page](https://doi.org/10.1016/0022-0396(86)90096-3) | The Elsevier abstract states construction of scaling-invariant $L_t^qL_x^p$ regular solutions and regularity of weak Navier--Stokes solutions in $C((0,T);L^n)$. | Modern strong-$L^p$ continuation context for any claim based only on control of $Q$. | No $C_h$, $A$, or weighted autocorrelation dynamics. | High. |
| L4-1 | C. V. Tran, X. Yu, D. G. Dritschel, *Velocity--pressure correlation in Navier--Stokes flows and the problem of global regularity* (2021), J. Fluid Mech. 911, A18. [DOI / open full text](https://doi.org/10.1017/jfm.2020.1033) | The open article displays the local energy balance, exact $L^q$ evolution identities (Section 2), and pressure-correlation regularity criteria (Theorem 3.1). | Direct collision for the unprojected $L^4$ identity (2.4) and for the fact that pressure is the surviving quartic driver. | Physical-space pressure correlation, not an autonomous off-diagonal $C_h$ system and not the projected forcing $H_j$. | High; strongest formula-level collision. |
| Bern-1 | D. Li, Y. Sire, *Remarks on the Bernstein inequality for higher order operators and related results* (2023), Trans. Amer. Math. Soc. 376, 945--967. [DOI](https://doi.org/10.1090/tran/8708), [open arXiv text](https://arxiv.org/html/2109.07952v1) | Theorem 4.2, equations (4.96)--(4.97), is periodic and frequency localized for real scalar $f$, $0<s\le2$, $1<p<\infty$; Lemma 4.4 is explicitly vector-valued; Remark 4.1 discusses vector analogues of the preceding mean-zero result. | Direct scalar support at $p=4,s=2,d=3$ and, by the componentwise calculation (2.6), the exact vector-shell coercivity needed in R0.73T. | Theorem 4.2 + Remark 4.1 are not by themselves a literal frequency-localized vector theorem. Constants depend on the fixed cutoff; arbitrary cutoffs and low shells need an explicit adaptation. | High; formula-level text inspected. |
| Corr-1 | T. von Kármán, L. Howarth, *On the Statistical Theory of Isotropic Turbulence* (1938), Proc. R. Soc. A 164, 192--215. [DOI](https://doi.org/10.1098/rspa.1938.0013) | The primary paper derives evolution of a two-point second-order velocity correlation coupled to a third-order correlation under homogeneous-isotropic statistical assumptions. | Establishes the classical fact that correlation evolution normally creates a higher-order closure term. | Its object is $R_{ij}(r)=\langle u_i(x)u_j(x+r)\rangle$; Fourier transform in separation gives a diagonal spectrum. R0.73T's $C_h$ is instead a deterministic Fourier coefficient in the base variable of the one-point density $\lvert u\rvert^2$. | High on distinction; medium-high because the official page blocked full-text extraction. |
| Corr-2 | C. C. Lin, *Note on the Law of Decay of Isotropic Turbulence* (1948), Proc. Natl. Acad. Sci. USA 34, 540--543. [DOI](https://doi.org/10.1073/pnas.34.11.540), [official archive](https://pmc.ncbi.nlm.nih.gov/articles/PMC1079163/) | The archived primary article gives the spectral form of the isotropic turbulence energy-transfer relation. | Near-neighbour for Fourier energy transfer and the diagonal energy spectrum. | Statistical, isotropic and diagonal in wave number; no deterministic sum $\sum_k a_{k+h}\overline{a_k}$ and no $C_h$ regularity criterion. | High. |
| Fourier-1 | A. Biryuk, W. Craig, S. Ibrahim, *Construction of suitable weak solutions of the Navier--Stokes equations* (2007), Contemp. Math. 429, 1--18. [DOI](https://doi.org/10.1090/conm/429/08226), [author manuscript](https://math.mcmaster.ca/craig/BiryukCraigIbrahim_Rev.pdf) | Section 5.1, equation (5.4), writes the exact Fourier-mode ODE; Theorem 5.3 bounds individual coefficients and their time integrals. | Direct primary evidence that exact mode dynamics remains convolution-coupled and that Fourier coefficient criteria are classical. | Controls $a_k$ mode by mode, not off-diagonal lag sums $C_h$; it does not eliminate phase/tensor information. | High. |
| Fourier-2 | Z. Lei, F.-H. Lin, *Global Mild Solutions of the Navier--Stokes Equations* (2011), Commun. Pure Appl. Math. 64, 1297--1304. [DOI](https://doi.org/10.1002/cpa.20361), [arXiv](https://arxiv.org/abs/1203.2699) | The primary text defines $\mathcal X^{-1}$ through the weighted Fourier $L^1$ norm $\int \lvert\xi\rvert^{-1}\lvert\widehat f(\xi)\rvert\,d\xi$ and proves global well-posedness below the viscosity threshold. | Direct collision for a modern weighted-Fourier continuation/small-data mechanism. | Uses absolute coefficient magnitudes in $\mathbb R^3$; it does not retain or evolve cross-shift phase correlations $C_h$. | High. |
| Fourier-3 | N. Kim, M. Kwak, M. Yoo, *Regularity Conditions of 3D Navier--Stokes flow in terms of large spectral components* (2015), Nonlinear Anal. 116, 75--84. [DOI](https://doi.org/10.1016/j.na.2014.12.011), [arXiv](https://arxiv.org/abs/1405.6838) | The primary abstract explicitly treats the torus and proves regularity when a Serrin norm of the high spectral component $w_N$ is finite. | Direct periodic modern Fourier criterion and the closest domain match. | Controls a high-frequency projection of $u$, not lagged quadratic correlations of its coefficients. | High. |
| Fourier-4 | Z. Bradshaw, Z. Grujić, *Frequency Localized Regularity Criteria for the 3D Navier--Stokes Equations* (2017), Arch. Ration. Mech. Anal. 224, 125--133. [DOI](https://doi.org/10.1007/s00205-016-1069-9), [arXiv](https://arxiv.org/abs/1501.01043) | Theorems 1--2 in the primary text give regularity criteria on dynamically selected Littlewood--Paley frequency windows. | Shows that shell/dyadic continuation criteria are established territory. | Uses dyadic amplitude norms, not $C_j(h)$, $A_j$, or a weighted autocorrelation closure. | High. |
| Fourier-5 | D. M. Ambrose, M. C. Lopes Filho, H. J. Nussenzveig Lopes, *Existence and analyticity of the Lei--Lin solution of the Navier--Stokes equations on the torus* (2024), Proc. Amer. Math. Soc. 152, 781--795. [DOI](https://doi.org/10.1090/proc/16615), [open arXiv text](https://arxiv.org/html/2205.12383) | The primary text defines periodic $X^{-1}$, $\mathcal X^{-1}$, and $\mathcal X^1$ by weighted $\ell^1$ norms of the **velocity** coefficients and proves small-data mild existence plus analyticity. | Closest periodic velocity-Wiener neighbour found in the targeted energy-density search. | It does not use $C_h=\widehat{\lvert u\rvert^2}(h)$, the Wiener norm $A$ of the energy density, $Q$, or an $AQ$ evolution/regularity criterion. | High on visible definitions and non-overlap. |
| Fourier-6 | A. Biswas, M. S. Jolly, V. R. Martinez, E. S. Titi, *Dissipation Length Scale Estimates for Turbulent Flows: A Wiener Algebra Approach* (2014), J. Nonlinear Sci. 24, 441--471. [DOI](https://doi.org/10.1007/s00332-014-9195-8), [arXiv](https://arxiv.org/abs/1310.3496) | The primary abstract identifies the Wiener algebra of absolutely convergent Fourier series as the phase space for periodic NSE Gevrey/analyticity estimates. | A direct periodic Wiener-algebra near-neighbour and an important terminology collision. | Its controlled Fourier/Gevrey variables are velocity coefficients and analyticity radii, not deterministic energy-density coefficients $C_h$ or $AQ$ dynamics. | High on scope; full formula-by-formula comparison was not needed for this negative distinction. |
| Fourier-7 | A. L. Mazzucato, *On the energy spectrum for weak solutions of the Navier--Stokes equations* (2005), Nonlinearity 18, 1--19. [DOI](https://doi.org/10.1088/0951-7715/18/1/001), [author PDF](https://sites.psu.edu/alm24/files/2023/06/nonlin.pdf) | Definition 2.2 builds $E(\kappa,t)$ by integrating $\lvert\widehat u(k,t)\rvert^2$ over $\lvert k\rvert=\kappa$; Theorem 1 relates a moment of its time average (or the Littlewood--Paley spectrum) to regularity of forced whole-space weak solutions. | Closest rigorous “energy spectrum + regularity” title found in the targeted pass. | The spectrum is diagonal in velocity frequency, radial and time/scale averaged; it is not the periodic base-variable Fourier transform $C_h=\widehat{\lvert u\rvert^2}(h)$ and does not evolve the energy-density Wiener norm $A$ or $AQ$. | High; definitions and theorem inspected in the author copy. |
| Near-2026 | M. Abu-Ghuwaleh, *Exact Shell--Bridge Closure and Finite Packet Exhaustion for the Three-Dimensional Periodic Navier--Stokes Equations* (2026), unreviewed v1 preprint. [primary preprint](https://www.preprints.org/manuscript/202603.1889) | The page labels the work **not peer reviewed** and states a packet-decomposition global-smoothness claim for periodic NSE. Literal page search found neither “autocorrelation” nor $C_j$. | High-risk near-neighbour because it claims an exact periodic shell closure. | Different object and method: its symbol $Q_j$ denotes a high--high/low shell obstruction, not $Q_j=\sum_h\lvert C_j(h)\rvert^2$. No correctness inference is made here; it requires an independent proof audit before citation as mathematics. | High on metadata/non-overlap; **unassessed** on validity. |

## 4. Direct-symbol search ledger

| Search channel | Queries / visible count | Result for the R0.73T object |
|---|---|---|
| Exact-phrase web search | “Navier--Stokes autocorrelation of Fourier coefficients”, “Fourier mode correlations”, “cross-mode correlation”, “shifted Fourier coefficients”, and “weighted Fourier correlation” | Results were turbulence statistics, Lagrangian/Eulerian correlations, numerical models, or ordinary spectral criteria. No deterministic $C_h$-closure or $C_h$-regularity theorem was located. |
| Targeted energy-density Wiener / $AQ$ pass | “Fourier transform of the energy density” + Navier--Stokes; “Fourier coefficients of $\lvert u\rvert^2$”; “energy-density Fourier coefficients”; “local energy density” + Wiener; “Wiener norm” + energy density; autocorrelation + $L^4$; $AQ$ + autocorrelation + Navier--Stokes | The closest primary hits were velocity-Wiener/analyticity papers (Ambrose--Lopes Filho--Nussenzveig Lopes; Biswas--Jolly--Martinez--Titi), Mazzucato's diagonal energy-spectrum regularity criterion, and statistical turbulence spectra. No inspected source evolved $A=\lVert\widehat{\lvert u\rvert^2}\rVert_{\ell^1}$, $Q=\lVert\widehat{\lvert u\rvert^2}\rVert_{\ell^2}^2$, or $AQ$ as a deterministic NSE regularity budget. |
| arXiv API | `Navier-Stokes AND autocorrelation`: 18 records; `Navier-Stokes AND "Fourier correlation"`: 0; `Navier-Stokes AND "correlation function" AND math.AP`: 3; `Navier-Stokes AND "Fourier coefficients" AND regularity`: 2; `Navier-Stokes AND "local energy" AND Fourier`: 5 | Manual title/abstract screening found statistical/Lagrangian/model correlations or coefficient criteria, not the off-diagonal deterministic $C_h$ family. |
| Crossref and OpenAlex | Phrase and concept searches for Navier--Stokes + Fourier-mode correlation/autocorrelation/local energy/weighted Fourier | Recovered the primary sources above and unrelated statistical uses; no literal $C_h$ dynamical criterion. |
| Semantic Scholar | API request returned HTTP 429 | No evidence drawn from this channel; not counted as a negative result. |

The symbolic expression itself is poorly indexed, so the negative result is
necessarily phrased as “not located in this bounded search,” never “does not
exist.”  In particular, the targeted energy-density-Wiener/$AQ$ pass is not a
novelty, absence, or priority proof.

## 5. Release boundary and remaining gap

The discovery stop rule has fired:

1. **classical $L^p/L^4$ methods:** Prodi, Serrin, Kato, Giga, and the exact
   quartic pressure identity of Tran--Yu--Dritschel, plus Li--Sire's periodic
   frequency-localized coercivity (with the vector adaptation recorded above);
2. **correlation-function methods:** von Kármán--Howarth plus Lin's spectral
   transfer formulation;
3. **modern Fourier criteria:** Biryuk--Craig--Ibrahim, Lei--Lin,
   Kim--Kwak--Yoo, Bradshaw--Grujić, Ambrose--Lopes Filho--Nussenzveig Lopes,
   Biswas--Jolly--Martinez--Titi, and Mazzucato;
4. **literal collision search:** no paper was located that makes the
   deterministic $C_h=\sum_k a_{k+h}\overline{a_k}$ an autonomous variable
   or proves a regularity criterion in $C_h$ or weighted $C_h$ alone;
5. **energy-density Wiener/$AQ$ pass:** no inspected primary source was found
   that derives a deterministic evolution or continuation criterion for
   $A=\lVert\widehat{|u|^2}\rVert_{\ell^1}$, $Q$, or their product.  This is
   expressly a bounded negative result, not a novelty proof.

Accordingly, R0.73T must not claim novelty for (2.1)--(2.4), for bounded
$L_t^\infty L_x^4$, for Wiener/Fourier coefficient control, or for the idea
that a second-order correlation equation couples to higher-order data.

The only defensible research slot left by this audit is narrower: prove a new,
correctly scaled estimate that controls the weighted-gradient and projected
nonlinear flux terms by an explicitly auditable autocorrelation functional, or
prove a precise non-closure/no-go theorem showing why such a reduction cannot
hold.  Absence of a literal prior packaging is not itself a result.
