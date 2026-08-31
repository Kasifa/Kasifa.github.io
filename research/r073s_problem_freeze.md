# R0.73S problem freeze: can quartic phase data replace the sextic convolution?

**Frozen date:** 2026-08-31

**Domain:** the normalized periodic torus \(\mathbb T^3=[0,2\pi]^3\),
viscosity one, and finite Fourier vector fields; the Navier--Stokes corollary
retains the real mean-zero divergence-free hypotheses of R0.73Q--R0.73R

**Dependency:** the R0.73R shell representation

\[
 \|e^{t\Delta}f\|_{L_t^4L_x^6}
 \asymp
 \left(\sum_j2^{-2j}\|P_jf\|_6^4\right)^{1/4}.
\]

## 1. Frozen question

R0.73R gives an exact phase-sensitive shell diagnostic through the Fourier
transform of \(|f_j|^2f_j\).  That diagnostic is sextic in the field and is
implemented by a triple convolution.  R0.73S asks four bounded questions.

1. Can \(\|f_j\|_6\) be certified from the quadratic autocorrelation of the
   Fourier coefficients, hence from quartic rather than sextic phase data?
2. What support geometry must accompany that quartic statistic?
3. Is the resulting support exponent sharp even for a real divergence-free
   field in one fixed-ratio annulus?
4. Does the new proxy separate the matched Dirichlet/Rudin--Shapiro pair of
   R0.73R after their common vanishing-\(L^2\) scaling?

The target is a lower-interaction-order sufficient certificate for the same
R0.73Q stability tube.  It is not a runtime lower bound, a necessary
condition, or an arbitrary-data regularity theorem.

## 2. Frozen notation

For one finite Fourier vector field

\[
 f(x)=\sum_{k\in S}a(k)e^{ik\cdot x},
 \qquad a(k)\in\mathbb C^d,
\]

put

\[
 E=\|f\|_2,
 \qquad
 C(h)=\sum_k a(k+h)\cdot\overline{a(k)},
 \qquad
 Q=\sum_h|C(h)|^2,
\]

\[
 A=\sum_h|C(h)|,
 \qquad M=|S|,
 \qquad D_C=|\operatorname{supp}C|,
 \qquad D_\Delta=|S-S|.
\]

Thus \(C=\widehat{|f|^2}\), \(Q=\|f\|_4^4\), and, when \(E>0\),

\[
 \Gamma={Q\over E^4},
 \qquad
 \Theta={\|f\|_6^6\over E^6},
 \qquad
 \alpha={A\over E^2}.
\]

All three normalized quantities are set to zero when \(E=0\).

## 3. Frozen candidate conclusions

The analytic gate may close only if independent reconstruction confirms

\[
 \boxed{
 \|f\|_6^6\le A Q,
 \qquad
 A\le\min\{ME^2,\sqrt{D_CQ}\}
 \le\min\{ME^2,\sqrt{D_\Delta Q}\}.}
\]

Equivalently,

\[
 \boxed{
 \Theta\le\alpha\Gamma
 \le\Gamma\min\{M,\sqrt{D_C\Gamma}\}
 \le\Gamma\min\{M,\sqrt{D_\Delta\Gamma}\}.}
\]

For \(f_j=P_jf\), define

\[
 U_j:=Q_j\min\{M_jE_j^2,\sqrt{D_{\Delta,j}Q_j}\}.
\]

The R0.73R caloric estimate should then give

\[
 \|e^{t\Delta}f\|_{L_t^4L_x^6}
 \lesssim
 \left(\sum_j2^{-2j}U_j^{2/3}\right)^{1/4}.
\]

This is phase-sensitive because \(Q_j=\|f_j\|_4^4\) contains the complete
pair autocorrelation.  It lowers the algebraic interaction order from the
triple convolution for \(L^6\) to the pair autocorrelation for \(L^4\).
It does not by itself prove a universal FFT or wall-clock complexity gain.

## 4. Frozen sharpness target

The factor \(\sqrt D\) cannot be removed from a bound using only
\((E,\Gamma,D)\).  The candidate witness starts from

\[
 d_m(x)=m^{-1/2}D_m(e^{ix}),
 \qquad \beta_m=m^{-1/4},
 \qquad a_m=(1-\beta_m^2)^{1/2},
\]

and, after a carrier separation, uses

\[
 F_m(x)=a_m+\beta_me^{iNx}d_m(x).
\]

The exact target asymptotics are

\[
 \|F_m\|_2=1,
 \qquad \|F_m\|_4^4\longrightarrow {5\over3},
 \qquad \|F_m\|_6^6\sim {11\over20}\sqrt m,
 \qquad |\operatorname{supp}\widehat{|F_m|^2}|=4m-1.
\]

A second carrier must convert this scalar complex family into a real
mean-zero divergence-free two-component shear whose support stays inside one
fixed-ratio annulus.  The embedding is required to preserve \(|F_m|\)
pointwise, retain \(\Gamma=O(1)\), \(\Theta\asymp\sqrt{D_C}\), and have
zero Navier--Stokes nonlinearity.

## 5. Exact exclusions

R0.73S will not claim:

- a new Nikolskii, interpolation, Wiener-algebra, or autocorrelation theorem;
- an unconditional arithmetic complexity separation between pair and triple
  convolution;
- a support-free estimate of \(L^6\) from \(L^4\);
- necessity of the R0.73Q heat-flow entrance;
- unsafe dynamics, instability, or blow-up when the proxy is large;
- a new large-data Navier--Stokes regularity theorem;
- arbitrary three-dimensional global regularity;
- any resolution or partial resolution of the Clay Millennium problem.

The local contribution under audit is the exact shell packaging, the sharp
fixed-annulus obstruction, the matched-family transfer, and a reproducible
finite certificate.  Absence of an identical package from a bounded search
will not be presented as a novelty or priority proof.
