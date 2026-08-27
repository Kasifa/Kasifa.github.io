# R0.72Q -- arbitrary phases in a dominant-harmonic finite-pattern cone, with the exact 1:2 caustic

**Date:** 2026-08-28

**Status:** a quantitative Morse-shape theorem and a family-uniform
enhanced-dissipation corollary for fixed finite commensurate carrier patterns
with a dominant first harmonic. All relative phases are arbitrary. For the
1:2 pattern, the real unit-circle caustic is computed exactly and the largest
phase-uniform disk around the one-carrier profile has radius \(1/4\). The
result remains inside the triangular 2.5D Navier--Stokes class; it is not a
regularity theorem for general three-dimensional Navier--Stokes.

**Keywords:** Navier--Stokes regularity, enhanced dissipation, finite Fourier
pattern, arbitrary phase, Morse shear, moving critical points, caustic,
full superposition, hypocoercivity

---

## 0. Direct decision

R0.72P proved a full-superposition enhanced-dissipation estimate for a fixed
1:2 pattern, but imposed real collinear phases. That phase restriction is
not needed in the same coefficient range. More generally, a simple weighted
coefficient cone controls every phase at once.

Fix an integer \(M\ge2\). After translating the cell variable so that the
first harmonic is real and positive, consider

\[
 W_{\boldsymbol\beta,\boldsymbol\theta}(y,\phi)
 =e^{-y}\cos\phi
 +\sum_{m=2}^{M}\beta_m e^{-m^2y}
       \cos(m\phi+\theta_m),
 \qquad 0\le y\le1,
 \tag{0.1}
\]

where the signs of the real numbers \(\beta_m\) may equivalently be absorbed
into the arbitrary phases \(\theta_m\). Write \(b_m=|\beta_m|\), and assume

\[
 \boxed{Q_2:=\sum_{m=2}^{M}m^2b_m\le\frac12.}
 \tag{0.2}
\]

Then, uniformly in all phases and all coefficients satisfying (0.2):

1. \(W(y,\cdot)\) has exactly two critical points for every \(y\in[0,1]\);
2. the two points lie within \(\pi/12\) of \(0\) and \(\pi\), respectively;
3. Coble--He's shape assumptions hold with the explicit choices

   \[
    N_{\rm crit}=2,\qquad r=\frac\pi{12},\qquad
    \mathfrak C_0=81,\qquad \mathfrak C_1=36;
    \tag{0.3}
   \]
4. the complete affine-row propagator has a phase- and coefficient-uniform
   enhanced-dissipation estimate, with constants depending only on the fixed
   value of \(M\).

For the 1:2 profile, write

\[
 F_z(\phi)=\cos\phi+\operatorname{Re}(ze^{2i\phi}),
 \qquad z=\rho e^{i\theta}.
 \tag{0.4}
\]

Its degenerate-critical-point locus is the exact closed curve

\[
 \boxed{
 z(\phi)=\frac18e^{-3i\phi}-\frac38e^{-i\phi},
 \qquad \phi\in\mathbb T,}
 \tag{0.5}
\]

or, equivalently on its real locus,

\[
 \boxed{
 \left(|z|^2-\frac1{16}\right)^3
 =\frac{27}{1024}(\operatorname{Im}z)^2.}
 \tag{0.6}
\]

Every ray from the origin meets (0.5) exactly once. The wall radius belongs
to \([1/4,1/2]\), and its minimum \(1/4\) occurs on the real axis. Hence

\[
 \boxed{|z|<\frac14\quad\Longrightarrow\quad
 F_z\text{ has exactly two nondegenerate critical points for every phase}.}
 \tag{0.7}
\]

The radius \(1/4\) is sharp for a disk that must work for every phase. It is
a theorem-applicability wall, not a proof that enhanced dissipation fails on
or beyond the wall.

---

## 1. Exact full-superposition cell reduction

Take commensurate carriers

\[
 r_m=mR,\qquad 1\le m\le M,\qquad R\in\mathbb N,
 \tag{1.1}
\]

and coefficients

\[
 w_1=ae^{i\vartheta_1},\qquad
 w_m=a\beta_m e^{i\vartheta_m},\qquad a>0.
 \tag{1.2}
\]

Translation of the cell coordinate removes \(\vartheta_1\); it only replaces
the remaining phases by relative phases
\(\theta_m=\vartheta_m-m\vartheta_1\). Zero coefficients are allowed, so a
fixed \(M\) also contains patterns with missing harmonics.

For a fixed orthogonal Fourier label \(q_*\), the affine frequency row

\[
 \Lambda_{R,q_*}=\{(nR,q_*):n\in\mathbb Z\}
 \tag{1.3}
\]

is invariant under every shift \(\pm mR\). With the same normalization as
R0.72P, Fourier transform in \(n\), followed by

\[
 y=R^2x,\qquad \phi=R\theta,
 \tag{1.4}
\]

gives the complete cell equation

\[
 \partial_yG
 =(\partial_\phi^2-|q_*|^2R^{-2})G
 -is\varepsilon_c
 W_{\boldsymbol\beta,\boldsymbol\theta}(y,\phi)G,
 \qquad
 \varepsilon_c=\frac{2|\delta|a}{R^2},
 \quad s=\operatorname{sign}\delta.
 \tag{1.5}
\]

Equation (1.5) contains the full finite superposition. No carrierwise
semigroup estimate and no summation over separate one-carrier problems has
been used.

For \(\varepsilon_c>0\), set

\[
 t=\varepsilon_c y,\qquad \eta=\varepsilon_c^{-1},\qquad
 H(t,\phi)=e^{|q_*|^2R^{-2}\eta t}G(\eta t,\phi).
 \tag{1.6}
\]

Then

\[
 \partial_tH
 =\eta\partial_\phi^2H
 -isW_{\boldsymbol\beta,\boldsymbol\theta}(\eta t,\phi)H.
 \tag{1.7}
\]

This is the \(k=1\), \(\sigma=0\) mode in the time-dependent shear theorem
of Coble and He. Restoring \(G\) through
\(G(y)=e^{-|q_*|^2R^{-2}y}H(\varepsilon_c y)\) only adds favorable scalar
damping, so the estimates below are uniform in the fixed row label. The
remaining task is to verify their phase, shape, and slow-time assumptions
uniformly over the entire coefficient--phase cone.

---

## 2. A quantitative arbitrary-phase Morse lemma

Factor out the first heat envelope:

\[
 W(y,\phi)=e^{-y}F_y(\phi),
 \qquad
 F_y(\phi)=\cos\phi+
 \sum_{m=2}^{M}r_m(y)\cos(m\phi+\theta_m),
 \tag{2.1}
\]

where

\[
 r_m(y)=\beta_m e^{-(m^2-1)y}.
 \tag{2.2}
\]

Define

\[
 S_j(y)=\sum_{m=2}^{M}m^j|r_m(y)|.
 \tag{2.3}
\]

Since \(m\le m^2/2\) for \(m\ge2\), assumption (0.2) gives

\[
 S_2(y)\le\frac12,
 \qquad
 S_1(y)\le\frac12S_2(y)\le\frac14,
 \qquad 0\le y\le1.
 \tag{2.4}
\]

### 2.1 Location and number of critical points

At a critical point,

\[
 \sin\phi
 =-\sum_{m=2}^{M}m r_m(y)\sin(m\phi+\theta_m),
 \tag{2.5}
\]

so

\[
 |\sin\phi|\le S_1(y)\le\frac14.
 \tag{2.6}
\]

The exact identity

\[
 \sin\frac\pi{12}=\frac{\sqrt6-\sqrt2}{4}>\frac14
 \tag{2.7}
\]

follows from \(3>2\sqrt2\), equivalently \(9>8\). Hence every critical
point lies in one of the two arcs

\[
 J_0=\left(-\frac\pi{12},\frac\pi{12}\right),
 \qquad
 J_\pi=\left(\pi-\frac\pi{12},
                    \pi+\frac\pi{12}\right).
 \tag{2.8}
\]

On the larger arcs

\[
 I_0=\left(-\frac\pi6,\frac\pi6\right),
 \qquad
 I_\pi=\left(\pi-\frac\pi6,\pi+\frac\pi6\right),
 \tag{2.9}
\]

the second derivative has a fixed sign. Indeed, with

\[
 \mu:=\frac{\sqrt3-1}{2}>\frac13,
 \tag{2.10}
\]

one has

\[
 F_y''(\phi)\le-\frac{\sqrt3}{2}+S_2(y)\le-\mu
 \quad(\phi\in I_0),
 \tag{2.11}
\]

and

\[
 F_y''(\phi)\ge\frac{\sqrt3}{2}-S_2(y)\ge\mu
 \quad(\phi\in I_\pi).
 \tag{2.12}
\]

At the two endpoints of each small arc \(J_0,J_\pi\), the first-harmonic
slope has magnitude \(\sin(\pi/12)>1/4\), while the total perturbing slope
has magnitude at most \(S_1\le1/4\). The endpoint signs are therefore
opposite. The intermediate-value theorem gives a zero in each small arc;
strict monotonicity from (2.11)--(2.12) makes each zero unique. Equation
(2.6) excludes every other zero.

Denote the two critical points by \(c_0(y)\in J_0\) and
\(c_\pi(y)\in J_\pi\). They are simple, depend smoothly on \(y\), and obey

\[
 d_{\mathbb T}(c_0,c_\pi)>\frac{5\pi}{6}.
 \tag{2.13}
\]

### 2.2 Explicit shape constants

Choose

\[
 r=\frac\pi{12}.
 \tag{2.14}
\]

The balls \(B_r(c_0(y))\) and \(B_r(c_\pi(y))\) are disjoint and lie inside
\(I_0\) and \(I_\pi\), respectively. Since \(e^{-1}>1/3\),
(2.10)--(2.12) and the fundamental theorem of calculus give, inside either
ball,

\[
 \frac19d_{\mathbb T}(\phi,c_j(y))
 <|\partial_\phi W(y,\phi)|
 \le\frac32d_{\mathbb T}(\phi,c_j(y)).
 \tag{2.15}
\]

Consequently

\[
 \frac1{81}d_{\mathbb T}(\phi,c_j(y))^2
 \le|\partial_\phi W(y,\phi)|^2
 \le81d_{\mathbb T}(\phi,c_j(y))^2.
 \tag{2.16}
\]

Outside the two critical balls there are two cases. If
\(\phi\in I_0\cup I_\pi\), monotonicity and distance at least \(r\) give

\[
 |\partial_\phi W|
 \ge e^{-1}\mu\frac\pi{12}>\frac1{36},
 \tag{2.17}
\]

where only \(e<3\), \(\mu>1/3\), and \(\pi>3\) were used in the last step.
If \(\phi\notin I_0\cup I_\pi\), then

\[
 |\partial_\phi W|
 \ge e^{-1}\left(\frac12-S_1\right)
 \ge\frac1{4e}>\frac1{12}>\frac1{36}.
 \tag{2.18}
\]

Everywhere,

\[
 |\partial_\phi W|\le1+S_1\le\frac54<36.
 \tag{2.19}
\]

Equations (2.16)--(2.19) prove the explicit shape contract (0.3).

### 2.3 Uniform derivative and slow-time bounds

The same cone gives

\[
 \|W\|_\infty\le\frac98,
 \qquad
 \|W_\phi\|_\infty\le\frac54,
 \qquad
 \|W_{\phi\phi}\|_\infty\le\frac32,
 \tag{2.20}
\]

and, because \(m^3\le M m^2\) for \(m\le M\),

\[
 \|W_{\phi\phi\phi}\|_\infty
 \le1+\frac M2,
 \qquad
 \|W_{y\phi}\|_\infty
 \le1+\frac M2.
 \tag{2.21}
\]

Take the actual shear as the reference shear,

\[
 U(t,\phi)=V(t,\phi)
 =sW(\eta t,\phi).
 \tag{2.22}
\]

The shared-critical-point and derivative-sign conditions are then exact.
Moreover,

\[
 \|U_{t\phi}\|_\infty
 \le\eta\left(1+\frac M2\right).
 \tag{2.23}
\]

Thus the Coble--He slow-reference condition
\(\|U_{t\phi}\|_\infty\le\eta^{3/4}\) holds whenever

\[
 \boxed{\eta\le\left(1+\frac M2\right)^{-4}.}
 \tag{2.24}
\]

The fixed-\(M\) requirement is material. Condition (0.2) alone does not
bound the third derivative uniformly as \(M\to\infty\).

---

## 3. Uniform enhanced dissipation for the finite-pattern cone

Coble--He Theorem 1.2 permits moving critical points. It requires a fixed
number of nondegenerate points, pairwise disjoint neighborhoods with fixed
radius, a linear slope comparison inside those neighborhoods, a gradient
gap outside, uniform profile norms, and a slow reference shear.

Sections 2.1--2.3 give all of those data uniformly.  For definiteness, let
\(C_{\rm sh}(M)\) be the explicit sum of the four bounds in
(2.20)--(2.21); it bounds every spatial derivative through order three of
both \(U\) and \(V\):

\[
 N_{\rm crit}=2,\quad r=\frac\pi{12},\quad
 \mathfrak C_0=81,\quad\mathfrak C_1=36,\quad
 \|W\|_{W^{3,\infty}}\le C_{\rm sh}(M).
 \tag{3.1}
\]

The published theorem is stated for one pair \((U,V)\), with a threshold
written as \(\eta_0(U,V)\). The family-uniform conclusion used here is a
proof-level corollary, not a verbatim theorem from that paper. Their
Appendix A spectral inequality uses spatial cutoffs around the critical
points. Translations of two fixed model cutoffs have the same derivative
norms for every coefficient, phase, and time.  Tracing the Appendix A
spectral constant and the absorption parameters in the proof of Theorem 1.2
shows that, once the slow-reference inequality is imposed, they use only
\[
 (N_{\rm crit},r,\mathfrak C_0,\mathfrak C_1,
   \|U\|_{W^{3,\infty}},\|V\|_{W^{3,\infty}}).
 \tag{3.2}
\]
Let \(\eta_{\rm CH}(2,\pi/12,81,36,C_{\rm sh}(M))>0\) denote the
threshold obtained from those displayed proof constants.  Then set
\[
 \eta_\sharp(M):=\min\left\{1,
 \left(1+\frac M2\right)^{-4},
 \eta_{\rm CH}(2,\pi/12,81,36,C_{\rm sh}(M))\right\}.
 \tag{3.3}
\]
This dependency trace, rather than compactness alone, supplies one threshold
for the whole fixed-\(M\) family.

Hence there is also a constant

\[
 c_\sharp(M)>0,
 \tag{3.4}
\]

such that, for \(0<\eta\le\eta_\sharp(M)\), the solution of (1.7) obeys

\[
 \|H(t)\|_2
 \le e\exp\{-c_\sharp(M)\eta^{1/2}t\}\|H(0)\|_2,
 \qquad 0\le t\le\eta^{-1}.
 \tag{3.5}
\]

The constants are uniform over all phases, all coefficients in (0.2),
\(R\), \(q_*\), and the initial datum. Returning to \(y\), restoring the
favorable scalar damping, and absorbing the square of the norm estimate into
the constants gives for sufficiently large \(\varepsilon_c\)

\[
 E(y)\le C_Me^{-c_M\sqrt{\varepsilon_c}\,y}E(0),
 \qquad E(y)=\|G(y)\|_2^2.
 \tag{3.6}
\]

For the remaining compact interval \(1\le\varepsilon_c\le
\eta_\sharp(M)^{-1}\), skew advection and diffusion give the exact
contraction \(E(y)\le E(0)\). Enlarging one fixed-\(M\) prefactor therefore
proves, for every \(\varepsilon_c\ge1\),

\[
 \boxed{
 E(y)\le C_Me^{-c_M\sqrt{\varepsilon_c}\,y}E(0),
 \quad 0\le y\le1,}
 \tag{3.7}
\]

\[
 \boxed{
 \int_0^1E(y)\,dy
 \le C_M\varepsilon_c^{-1/2}E(0),
 \qquad
 E(1)\le C_Me^{-c_M\sqrt{\varepsilon_c}}E(0).}
 \tag{3.8}
\]

Smooth-data approximation, Fourier truncation, and the exact \(L^2\)
contraction extend (3.7)--(3.8) to every \(L^2\) datum on the affine row.

---

## 4. Exact 1:2 caustic

The finite-pattern cone is a convenient sufficient condition, but it is not
sharp even for two harmonics. The 1:2 degeneracy wall can be computed
exactly.

Let

\[
 F_z(\phi)=\cos\phi+\operatorname{Re}(ze^{2i\phi}),
 \qquad z=\rho e^{i\theta},
 \qquad u=2\phi+\theta.
 \tag{4.1}
\]

A degenerate critical point satisfies

\[
 \sin\phi+2\rho\sin u=0,
 \qquad
 \cos\phi+4\rho\cos u=0.
 \tag{4.2}
\]

Squaring and adding gives

\[
 1=4\rho^2(1+3\cos^2u),
 \qquad
 \rho=\frac1{2\sqrt{1+3\cos^2u}}\in
 \left[\frac14,\frac12\right].
 \tag{4.3}
\]

Solving (4.2) for the complex coefficient gives the exact parameterization

\[
 z(\phi)=\frac18e^{-3i\phi}-\frac38e^{-i\phi}.
 \tag{4.4}
\]

Indeed, if \(z=x+iy\), then along (4.4)

\[
 |z|^2=\frac1{16}+\frac3{16}\sin^2\phi,
 \qquad
 y=\frac12\sin^3\phi.
 \tag{4.5}
\]

Eliminating \(\phi\) yields (0.6). Conversely, the real locus of (0.6)
has the parameterization (4.4). On a ray with fixed polar angle \(\theta\),
put \(s=\rho^2\ge1/16\). The implicit equation becomes

\[
 \frac{(s-1/16)^3}{s}
 =\frac{27}{1024}\sin^2\theta.
 \tag{4.6}
\]

The left side has value zero at \(s=1/16\), and is strictly increasing for
\(s>1/16\) because

\[
 \frac d{ds}\frac{(s-1/16)^3}{s}
 =\frac{(s-1/16)^2(2s+1/16)}{s^2}>0.
 \tag{4.7}
\]

Together with
\(H(1/16)=0\) and \(H(1/4)=27/1024\), this proves that every ray has exactly
one wall radius. At \(\theta=0,\pi\) it is \(1/4\); at
\(\theta=\pm\pi/2\) it is \(1/2\).

### 4.1 Uniform inner disk

For \(0\le\rho\le\rho_+<1/4\), every critical point satisfies

\[
 |\sin\phi|\le2\rho_+.
 \tag{4.8}
\]

At a critical point, the smallest possible Hessian occurs when the two
terms have opposite signs. Writing \(q=|\cos u|\), one obtains

\[
 |F_z''(\phi)|
 \ge\sqrt{1-4\rho^2+4\rho^2q^2}-4\rho q
 \ge1-4\rho_+>0.
 \tag{4.9}
\]

The last expression decreases in \(q\in[0,1]\), so its minimum is attained
at \(q=1\). Therefore every closed disk
\(|z|\le\rho_+<1/4\) has a uniform Hessian margin, two uniformly separated
critical points, and a uniform away-gradient gap by compactness. The count is
two because the homotopy \(\tau z\), \(0\le\tau\le1\), stays inside the disk:
all its critical points remain simple, so their number cannot change from
the two critical points of \(\cos\phi\).  For the heat-decaying 1:2 path,
\(\|W_{y\phi}\|_\infty\le1+8\rho_+\). Repeating the proof-level
Coble--He extraction of Section 3 therefore gives constants
\[
 \eta_\sharp(\rho_+)>0,\qquad c_\sharp(\rho_+)>0
 \tag{4.10}
\]
and a family-uniform enhanced-dissipation theorem on each fixed closed disk
\(|z|\le\rho_+<1/4\).  These constants may degenerate as
\(\rho_+\uparrow1/4\).

In the heat-decaying 1:2 profile,

\[
 z(y)=z(0)e^{-3y}.
 \tag{4.11}
\]

Hence \(|z(0)|\le\rho_+<1/4\) stays in the same phase-uniform inner region for
the whole interval. In particular, R0.72P's range
\(|\lambda|\le1/8\) is valid for every relative phase, not merely the real
collinear-phase slice.

At \(|z|=1/4\), only the two real-axis cusp points are degenerate. Profiles
at the same radius with other phases can remain Morse. The correct statement
is therefore that \(1/4\) is the sharp radius of a disk uniform over all
phases, not that every profile on that circle is degenerate.

---

## 5. Physical reinsertion for a fixed pattern

R0.72L--P use the common-band exposure

\[
 \varepsilon_B=\frac{|\delta|aB}{R^2},
 \qquad p=\frac{\sqrt N}{B}.
 \tag{5.1}
\]

The exact cell exposure in (1.5) is

\[
 \varepsilon_c=\frac{2\varepsilon_B}{B}.
 \tag{5.2}
\]

For the inherited physical comparison in this section, retain the normalized
orthogonal target label \(|q_*|=1\), and take the safe fixed coherence choice
\(B=M\).
The active carrier count satisfies \(N\le M\), so \(B\) is fixed geometric
data rather than a parameter that grows along the family. Equations
(3.7)--(3.8) can therefore be rewritten as

\[
 E(y)\le C_Me^{-c_M\sqrt{\varepsilon_B}\,y}E(0),
 \qquad
 \int_0^1E(y)\,dy\le C_M\varepsilon_B^{-1/2}E(0),
 \tag{5.3}
\]

with a corresponding terminal estimate. The interval where
\(\varepsilon_B\ge1\) but \(\varepsilon_c<1\) is compact for fixed \(B\) and
is covered by the same contraction completion.

If the nonzero carriers also obey a fixed amplitude-balance floor
\[
 |\beta_m|\ge\beta_->0
 \quad\hbox{for every active }m\ge2,
 \tag{5.4}
\]
so the R0.72O physical comparison and \(E(0)\asymp_{M,\beta_-}N\) apply,
then

\[
 \boxed{
 \mathcal C_\times
 \lesssim_{M,\beta_-} a^2N^2\sqrt{\varepsilon_B}.}
 \tag{5.5}
\]

Thus the inherited numerator and window retain the same powers,

\[
 U_{\rm ED}\asymp_{M,\beta_-}
 \varepsilon_B^{11/6}p^{4/3},
 \tag{5.6}
\]

\[
 \boxed{
 \sqrt{\varepsilon_B}
 \lesssim_{M,\beta_-} p^{2/3}R^{2/3}L_{R,\varepsilon_B},
 \qquad
 \varepsilon_B
 \lesssim_{M,\beta_-} p^{4/3}R^{4/3}L_{R,\varepsilon_B}^2.}
 \tag{5.7}
\]

The subscripts \(M,\beta_-\) are essential for the physical comparison.
The enhanced-dissipation constants above require only fixed \(M\), but this
release does not claim physical constants uniform as the amplitude floor
vanishes, or as the number or maximum frequency of carriers grows.

---

## 6. Exact certificate contract

The release certificate has two independent implementations:

1. a Python producer using integer and rational arithmetic;
2. a JavaScript audit using BigInt rational arithmetic.

Neither implementation reads the other source or runtime output. They
independently verify:

1. \(2m\le m^2\) for every declared \(2\le m\le M\), hence
   \(S_1\le S_2/2\);
2. the exact radical comparisons behind
   \(\sin(\pi/12)>1/4\) and \(\mu>1/3\);
3. the rational safe constants \((r,\mathfrak C_0,\mathfrak C_1)\) used in
   Section 2;
4. the 1:2 caustic parameterization and the polynomial identity (0.6);
5. the radial range \([1/4,1/2]\) and strict radial monotonicity (4.7);
6. the fixed-\(M\) derivative and slow-time ledgers.

The comparator requires exact equality of their canonical payloads. These
certificates audit algebraic identities and declared inequalities. They do
not replace the analytic Coble--He theorem or its proof-level uniform
extraction.

---

## 7. Literature boundary

Coble and He prove enhanced dissipation for time-dependent nondegenerate
shears with a slowly varying reference flow. Their Theorem 1.2 explicitly
allows moving critical points \(y_i(t)\), which is the decisive interface
for arbitrary phases here. Their theorem is stated profile by profile; the
fixed-\(M\) family uniformity in Section 3 is extracted from the constants in
their proof after the quantitative shape data have been supplied.

Pignoni proves qualitative stability of Morse functions under sufficiently
small \(C^k\) perturbations. That result supports the topology of the
argument but does not provide the coefficient cone, the constants in (0.3),
or an enhanced-dissipation threshold. Voorhaar describes the caustic and
Morse discriminant for univariate Laurent polynomials. The term *caustic*
is useful language for Section 4, but the exact real 1:2 curve used here is
derived directly in this report.

Bedrossian--Coti Zelati and Coti Zelati--Gallay give the stationary
enhanced-dissipation background. A recent preprint of
Benthaus--Coclite--Nobili shows why a spatial Morse margin alone cannot
control an arbitrarily fast moving shear: the speed of the critical points
can change or suppress the enhanced-dissipation mechanism. In the present
heat-decaying family, the slow-time bound is proved explicitly in
(2.23)--(2.24).

A bounded primary-source search did not locate a paper that states the same
fixed finite heat-decaying harmonic cone, the constants (0.3), the exact
1:2 real caustic, the affine-row reduction, and the R0.72O physical
reinsertion as one theorem. This search is not a novelty or priority claim.

---

## 8. What is proved, and what is not

### 8.1 Proved here

1. an arbitrary-phase quantitative Morse theorem for every fixed \(M\) and
   the coefficient cone (0.2);
2. exactly two moving critical points with explicit separation and shape
   constants;
3. a proof-level family-uniform extraction of the Coble--He estimate;
4. full-superposition integrated and terminal estimates for the complete
   affine-row propagator;
5. the exact real 1:2 caustic, its radial range, and the sharp all-phase
   inner-disk radius \(1/4\);
6. removal of R0.72P's real-collinear-phase restriction in its
   \(|\lambda|\le1/8\) range;
7. the fixed-pattern cross-cubic and physical-window corollary.

### 8.2 Not proved here

1. a theorem for an arbitrary coefficient polytope that crosses the
   caustic;
2. uniform constants as \(M\to\infty\), \(N\to\infty\), or \(B\to\infty\);
3. enhanced dissipation through a degenerate critical-point collision;
4. arbitrary time-dependent phases; only the heat envelope varies in time;
5. a fixed-\(R\), arbitrarily large-coupling asymptotic beyond the inherited
   window;
6. a continuation criterion for general three-dimensional Navier--Stokes;
7. exclusion of finite-time singularities or a solution of the Clay
   Millennium problem.

---

## 9. Research value

The useful increment is structural. R0.72P had one nontrivial two-carrier
class but could not vary the relative phase. R0.72Q replaces that slice by
an entire coefficient--phase cone and shows that the relevant critical
points may move without losing a uniform enhanced-dissipation estimate.
The exact 1:2 caustic also separates a theorem boundary from a dynamical
failure: crossing the wall invalidates this Morse proof, but does not by
itself disprove enhanced dissipation.

Within this project, the result closes a genuine multi-carrier robustness
gap and is suitable as a lemma or a section in a paper about the special
triangular mechanism. Its direct value for the Clay problem remains low:
the dominant-harmonic, fixed finite, commensurate, affine-row, triangular
2.5D assumptions are far from arbitrary three-dimensional data.

---

## 10. Next gate

R0.72R should leave the dominant-first-harmonic cone in a controlled way.
The cleanest next target is the three-harmonic coefficient space:

1. compute or certify the real unit-circle caustic for \(1:2:3\);
2. identify compact connected components of its complement with fixed
   critical count and quantitative jet margin;
3. test whether the full-superposition estimate survives a controlled
   approach to, or passage through, a degenerate wall;
4. keep growing-\(M\) uniformity as a separate question rather than hiding
   it inside fixed-pattern constants.

---

## Claim-to-source ledger

| Claim used here | Primary source | Exact role | Limitation |
|---|---|---|---|
| A slowly varying time-dependent nondegenerate shear has \(e^{-c\eta^{1/2}|k|^{1/2}t}\) mode decay | D. Coble and S. He, Theorem 1.2 and Appendix A, arXiv:2309.15738 / CMS 22 (2024) | Semigroup input after the exact cell reduction | The fixed-\(M\) compact-family corollary is extracted here from their proof; it is not stated verbatim |
| Morse critical points persist under sufficiently small smooth perturbation | R. Pignoni, Section 4, Ann. SNS Pisa 6 (1979) | Qualitative background for Morse stability | No explicit cone, margin, or ED constants |
| Degenerate critical points form a caustic in Laurent-polynomial coefficient space | A. Voorhaar, Definition 1.1, arXiv:2104.05123 / Adv. Math. 432 (2023) | Terminology and coefficient-space context | Does not give the real 1:2 curve or this ED result |
| Nondegenerate stationary shear has the \(\nu^{1/2}|k|^{1/2}\) scale | J. Bedrossian and M. Coti Zelati, ARMA 224 (2017); M. Coti Zelati and T. Gallay, JLMS 108 (2023) | Stationary hypocoercive background | Not a time-dependent family theorem |
| Fast motion of otherwise Morse critical points can change or suppress ED | J. Benthaus, G. M. Coclite, and C. Nobili, arXiv:2603.14624 (2026) | Shows why the slow-time bound cannot be omitted | A translating-sine model, not the heat-decaying pattern here |

## References used at this gate

1. D. Coble and S. He, *A Note on Enhanced Dissipation and Taylor
   Dispersion of Time-dependent Shear Flows*, arXiv:2309.15738; published as
   *A Note on Enhanced Dissipation of Time-Dependent Shear Flows*,
   *Communications in Mathematical Sciences* **22** (2024), 1685--1700,
   [DOI](https://doi.org/10.4310/CMS.2024.v22.n6.a10).
2. R. Pignoni, *Density and Stability of Morse Functions on a Stratified
   Space*, *Annali della Scuola Normale Superiore di Pisa* **6** (1979),
   593--608,
   [primary record](https://numdam.org/item/ASNSP_1979_4_6_4_593_0/).
3. A. Voorhaar, *The Newton Polytope of the Morse Discriminant of a
   Univariate Polynomial*, arXiv:2104.05123; *Advances in Mathematics*
   **432** (2023), 109275,
   [DOI](https://doi.org/10.1016/j.aim.2023.109275).
4. J. Bedrossian and M. Coti Zelati, *Enhanced Dissipation,
   Hypoellipticity, and Anomalous Small Noise Inviscid Limits in Shear
   Flows*, *Archive for Rational Mechanics and Analysis* **224** (2017),
   1161--1204,
   [DOI](https://doi.org/10.1007/s00205-017-1099-y).
5. M. Coti Zelati and T. Gallay, *Enhanced Dissipation and Taylor
   Dispersion in Higher-dimensional Parallel Shear Flows*, *Journal of the
   London Mathematical Society* **108** (2023), 1358--1392,
   [DOI](https://doi.org/10.1112/jlms.12782).
6. J. Benthaus, G. M. Coclite, and C. Nobili, *Mixing and Enhanced
   Dissipation in a Time-Translating Shear Flow*, arXiv:2603.14624 (2026),
   [primary preprint](https://arxiv.org/abs/2603.14624).
