# R0.76J -- local edge-extrapolation reconstruction for the exact-shear plateau

## 0. Result and status change

R0.76I obtained the exact-shear full-plateau window
`q=o(L^(5/2))`, but labelled the result **CONDITIONAL-LITERATURE** because
Proposition 4.2 of Ruizhe Zhang's July 2026 arXiv v1 preprint entered as a
black box.  This note reconstructs the required endpoint theorem in full.
The architecture follows Zhang's Sections 2--4, with attribution; no
independent-discovery or priority claim is made.

The reconstruction below is stronger in provenance than initially needed.
The same Volterra basis that controls negative-time evaluation also controls
its positive-time tail.  This gives a local infinite--finite range lemma,
so the edge theorem uses no specialized extrapolation or finite-range
result as a black box.  Boundary Plancherel is the only standard analytic
input singled out there; the remaining finite-dimensional analytic steps
are written out.  The insertion into the frozen R0.76I proof
still uses its peer-reviewed Erdelyi/Kós derivative and terminal inputs.
Thus the new theorem is **PROVED LOCALLY FROM ESTABLISHED LITERATURE**, not
conditional on the correctness of the 2026 preprint.

For `N>=1`, let

\[
 \mathcal T_N:=\left\{
 g(t)=\sum_{j=1}^{N}c_je^{i\mu_jt}:
 c_j\in\mathbb C,\ \mu_j\in\mathbb R
 \right\}.
 \tag{J.1}
\]

Zero coefficients are allowed, and repeated frequencies are merged before
the effective term count is read.

**Locally reconstructed bilateral edge theorem.**  For every
`g in T_N` and every `d>=0`,

\[
 \boxed{
 \max\{|g(1+d)|,|g(-1-d)|\}
 \le \sqrt{\frac{250}{19}}\,N
 e^{5\sqrt2N\sqrt d}\|g\|_{L^2[-1,1]}.}
 \tag{J.2}
\]

Now fix the R0.76I packet data

\[
 q\ge1,\qquad
 1\le n_1<\cdots<n_q\le2n_1,
 \quad n_j\in\mathbb N,
 \quad A_j\ge0,\quad \phi_j,B\in\mathbb R,
 \tag{J.3}
\]

\[
 F(t,x_2)=\sum_{j=1}^qA_je^{-n_j^2t}
 \cos(n_jx_2-\phi_j-n_jBt),
 \qquad u=(0,B,F(t,x_2)).
 \tag{J.4}
\]

Retain the frozen full-plateau mass
`M_(n,R)^(plat)`, signed flux `T_(n,R)`, and scaling `a=pL`.  Put

\[
 \Delta_a:=\frac{\delta+\delta_0}{a-\delta_0},
 \qquad
 \Phi_a^{\rm loc}:=20\sqrt2q\sqrt{\Delta_a}.
 \tag{J.5}
\]

For all sufficiently large frozen `L`, in particular
`a>=delta+2delta_0`, there are constants independent of every packet
parameter such that

\[
 \boxed{
 |\mathcal T_{\boldsymbol n,R}|
 \le C_Ja^{2/3}R^{-1/3}q^7e^{\Phi_a^{\rm loc}}
 \bigl(M_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{J.6}
\]

With

\[
 p_{\boldsymbol n,R}^{\rm plat}
 :=R^{-2}\omega M_{\boldsymbol n,R}^{\rm plat},
 \qquad
 \mathfrak X_{\boldsymbol n,R}
 :=\frac\omega R[\mathcal T_{\boldsymbol n,R}]_+,
 \tag{J.7}
\]

this becomes

\[
 \boxed{
 \mathfrak X_{\boldsymbol n,R}
 \le C_Ja^{2/3}q^7\omega^{1/3}e^{\Phi_a^{\rm loc}}
 \bigl(p_{\boldsymbol n,R}^{\rm plat}\bigr)^{2/3}.}
 \tag{J.8}
\]

Consequently, every integer-valued `q(L)=o(L^(5/2))` retains

\[
 \boxed{
 \limsup_{L\to\infty}\frac1{L^2}
 \log\!\left(C_Ja^{2/3}q(L)^7\omega^{1/3}
 e^{\Phi_a^{\rm loc}}\right)
 =-\frac2{11907}.}
 \tag{J.9}
\]

The historical R0.76I file remains frozen with its original conditional
label.  Equations J.6--J.9 are the new, deconditionalized statements.

## 1. The local positive-tail target

For `F in T_N` and `alpha>0`, define

\[
 I_\alpha(F):=\int_0^\infty|F(t)|^2e^{-\alpha t}\,dt.
 \tag{J.10}
\]

The basis constructed below will prove, rather than assume, the uniform
finite-range estimate

\[
 \boxed{
 I_\alpha(F)
 \le\frac{20}{19}\int_0^{25N/\alpha}
 |F(t)|^2e^{-\alpha t}\,dt.}
 \tag{J.11}
\]

This cutoff is not optimized.  Its purpose is to close the proof with
transparent constants and without importing Erdelyi's sharper cutoff
`9N/alpha`.

## 2. A vertical-line Takenaka--Malmquist basis

Fix `alpha>0` and distinct real frequencies
`lambda_0,...,lambda_(D-1)`.  Set

\[
 \zeta_j:=\frac\alpha2-i\lambda_j,
 \qquad
 \mathcal S:=\operatorname{span}
 \{e^{-\zeta_jt}:0\le j<D\}\subset L^2(0,\infty).
 \tag{J.12}
\]

For an integrable square-integrable function on the half-line, use the
Laplace transform

\[
 (\mathcal Lh)(s):=\int_0^\infty h(t)e^{-st}\,dt,
 \qquad \Re s>0.
 \tag{J.13}
\]

Boundary Plancherel gives

\[
 \langle\mathcal Lh_1,\mathcal Lh_2\rangle_{H^2}
 :=\frac1{2\pi}\int_{\mathbb R}
 (\mathcal Lh_1)(i\xi)
 \overline{(\mathcal Lh_2)(i\xi)}\,d\xi
 =\langle h_1,h_2\rangle_{L^2(0,\infty)}.
 \tag{J.14}
\]

Throughout, the complex inner product is linear in its first variable.

For `w` in the right half-plane, the kernel
`k_w(s)=1/(s+overline(w))` obeys

\[
 \langle G,k_w\rangle_{H^2}=G(w),
 \qquad
 \|k_w\|_{H^2}^2=\frac1{2\Re w}.
 \tag{J.15}
\]

For the finite rational functions below, J.15 follows directly from J.14:
`k_w` is the Laplace transform of `e^(-overline(w)t)`, so the inner
product is the defining Laplace integral at `w`.  No completeness theorem
for the full Hardy space is needed.

Define

\[
 B_j(s):=\frac{s-\overline{\zeta_j}}{s+\zeta_j},
 \qquad
 \widehat\varphi_m(s):=
 \frac{\sqrt\alpha}{s+\zeta_m}
 \prod_{\ell=0}^{m-1}B_\ell(s).
 \tag{J.16}
\]

For `s=x+iy` with `x>0`, direct subtraction gives

\[
 |s+\zeta_j|^2-|s-\overline{\zeta_j}|^2
 =2\alpha x>0,
 \qquad |B_j(s)|<1,
 \tag{J.17}
\]

whereas `|B_j(i y)|=1`.  Multiplication by each `B_j` therefore preserves
the boundary norm in J.14.  Since
`sqrt(alpha)/(s+zeta_m)` is the normalized kernel at
`overline(zeta_m)`, every `widehat(varphi)_m` has unit norm.

If `m<n`, cancel the common product of the first `m` boundary-unimodular
factors.  Formula J.15 then yields

\[
 \langle\widehat\varphi_n,\widehat\varphi_m\rangle_{H^2}
 =\sqrt\alpha\,(B_m\Psi)(\overline{\zeta_m})=0,
 \tag{J.18}
\]

because `B_m(overline(zeta_m))=0`; here `Psi` is the remaining bounded
rational factor times the last normalized kernel.

The rational function in J.16 has only the simple poles
`-zeta_0,...,-zeta_m`.  Hence

\[
 \widehat\varphi_m(s)=\sum_{\ell=0}^m
 \frac{c_{m\ell}}{s+\zeta_\ell},
 \qquad
 \varphi_m(t)=\sum_{\ell=0}^m c_{m\ell}e^{-\zeta_\ell t}.
 \tag{J.19}
\]

The diagonal coefficient is

\[
 c_{mm}=\sqrt\alpha\prod_{\ell=0}^{m-1}
 \frac{-\alpha+i(\lambda_m-\lambda_\ell)}
 {i(\lambda_m-\lambda_\ell)}\ne0.
 \tag{J.20}
\]

Thus the change-of-basis matrix is triangular with nonzero diagonal.
Equations J.14 and J.18--J.20 prove that
`varphi_0,...,varphi_(D-1)` is an orthonormal basis of `S`.

## 3. A frequency-uniform Laguerre majorant

For `Re(zeta)=alpha/2` and entire `h`, define the Volterra operator

\[
 (T_\zeta h)(t):=h(t)-\alpha\int_0^t
 e^{-\zeta(t-u)}h(u)\,du,
 \tag{J.21}
\]

where the integral follows the straight segment.  On the positive
half-line, the convolution theorem gives

\[
 \mathcal L(T_\zeta h)(s)
 =\frac{s-\overline\zeta}{s+\zeta}\,\mathcal Lh(s).
 \tag{J.22}
\]

Taking `h_m(t)=sqrt(alpha)e^(-zeta_m t)` and comparing J.22 with J.16
shows, first in `L^2(0,infinity)` and then everywhere by the identity
theorem, that

\[
 \varphi_m
 =T_{\zeta_0}T_{\zeta_1}\cdots T_{\zeta_{m-1}}h_m.
 \tag{J.23}
\]

Let `h_(m,0)=h_m` and, for `1<=r<=m`, set

\[
 h_{m,r}:=T_{\zeta_{m-r}}h_{m,r-1},
 \qquad h_{m,m}=\varphi_m.
 \tag{J.24}
\]

At the exterior point `-x`, substitution `u=-y` in J.21 gives

\[
 h_{m,r}(-x)=h_{m,r-1}(-x)
 +\alpha\int_0^x e^{\zeta_{m-r}(x-y)}h_{m,r-1}(-y)\,dy.
 \tag{J.25}
\]

Define `P_0(x)=1` and

\[
 P_{r+1}(x):=P_r(x)+\alpha\int_0^xP_r(y)\,dy.
 \tag{J.26}
\]

Since every `Re(zeta_j)=alpha/2`, induction in J.25 proves

\[
 |h_{m,r}(-x)|
 \le\sqrt\alpha e^{\alpha x/2}P_r(x),
 \qquad 0\le r\le m.
 \tag{J.27}
\]

Pascal's identity applied to J.26 yields

\[
 P_r(x)=\sum_{\ell=0}^r\binom r\ell
 \frac{(\alpha x)^\ell}{\ell!}
 =L_r(-\alpha x),
 \tag{J.28}
\]

where `L_r` is the ordinary Laguerre polynomial.  Hence the basis functions
obey the frequency-independent pointwise estimate

\[
 \boxed{
 |\varphi_m(-x)|
 \le\sqrt\alpha e^{\alpha x/2}L_m(-\alpha x),
 \qquad x\ge0.}
 \tag{J.29}
\]

No frequency spacing or upper-frequency cutoff entered J.17--J.29.

### Positive-time companion and proof of J.11

On the positive half-line, J.21 has a minus sign before its integral, but
the triangle inequality removes that sign.  More explicitly,

\[
 h_{m,r}(t)=h_{m,r-1}(t)-\alpha\int_0^t
 e^{-\zeta_{m-r}(t-y)}h_{m,r-1}(y)\,dy.
\]

The same induction as in J.25--J.28, now using
`abs(exp(-zeta(t-y)))=exp(-alpha(t-y)/2)`, proves

\[
 |h_{m,r}(t)|
 \le\sqrt\alpha e^{-\alpha t/2}L_r(-\alpha t),
 \qquad t\ge0,\quad 0\le r\le m.
 \tag{J.30}
\]

In particular,

\[
 |\varphi_m(t)|
 \le\sqrt\alpha e^{-\alpha t/2}L_m(-\alpha t).
 \tag{J.31}
\]

If `F=0`, J.11 is immediate.  Otherwise merge repeated frequencies and
pad with unused distinct zero-coefficient slots until the basis dimension
is `N`; then `I_alpha(F)>0`.  Let
`H(t)=e^(-alpha t/2)F(t)` and expand it in that orthonormal basis.
Cauchy--Schwarz and J.31 give, for every `t>=0`,

\[
 |F(t)|^2e^{-\alpha t}=|H(t)|^2
 \le I_\alpha(F)\,\alpha e^{-\alpha t}
 \sum_{m=0}^{N-1}L_m(-\alpha t)^2.
 \tag{J.32}
\]

The elementary Laguerre bound proved in Section 5 below implies that, for
`y>=25N`,

\[
 \begin{aligned}
 \frac1{I_\alpha(F)}
 \int_{25N/\alpha}^\infty|F(t)|^2e^{-\alpha t}\,dt
 &\le N\int_{25N}^\infty e^{-y+4\sqrt{Ny}}\,dy\\
 &\le N\int_{25N}^\infty e^{-y/5}\,dy
 =5Ne^{-5N}<\frac1{20}.
 \end{aligned}
 \tag{J.33}
\]

Here `4sqrt(Ny)<=4y/5` on that range.  The last function is decreasing
for real `N>=1`, and `5e^(-5)<1/20` follows from `e^5>100`; the latter is
already implied by the first seven nonnegative terms of the exponential
series.  Writing J.10 as the sum of its initial segment and tail, J.33
gives

\[
 \frac{19}{20}I_\alpha(F)
 \le\int_0^{25N/\alpha}|F(t)|^2e^{-\alpha t}\,dt,
 \tag{J.34}
\]

which proves J.11 entirely within the present note.

## 4. The half-line comparison theorem

Let `F in T_N`; merge repeats and, if necessary, add distinct unused
frequencies with zero coefficients so that the representation has `N`
distinct frequency slots.  Put

\[
 H(u):=e^{-\alpha u/2}F(u)
 =\sum_{j=0}^{N-1}a_je^{-\zeta_ju},
 \quad
 \|H\|_2^2=\int_0^\infty|F(u)|^2e^{-\alpha u}\,du,
 \quad
 H(-x)=e^{\alpha x/2}F(-x).
 \tag{J.35}
\]

Expand `H` in the basis from Section 2.  Both sides are finite sums of
entire exponentials, so their `L^2` equality on the half-line extends to
the whole complex plane.  Evaluation at `-x`, Cauchy--Schwarz, and J.29
give

\[
 \begin{aligned}
 |H(-x)|^2
 &\le\left(\sum_{m=0}^{N-1}|\varphi_m(-x)|^2\right)\|H\|_2^2\\
 &\le\alpha e^{\alpha x}
 \left(\sum_{m=0}^{N-1}L_m(-\alpha x)^2\right)\|H\|_2^2.
 \end{aligned}
 \tag{J.36}
\]

Cancelling the factor `e^(alpha x)` with J.35 proves the locally derived
half-line estimate

\[
 \boxed{
 |F(-x)|^2
 \le\alpha\sum_{m=0}^{N-1}L_m(-\alpha x)^2
 \int_0^\infty|F(u)|^2e^{-\alpha u}\,du.}
 \tag{J.37}
\]

## 5. From the half-line to the finite endpoint

For `m>=0` and `y>=0`, the defining series and the central-binomial bound
give

\[
 \begin{aligned}
 0\le L_m(-y)
 &\le\sum_{\ell=0}^\infty\frac{(my)^\ell}{(\ell!)^2}\\
 &\le\sum_{\ell=0}^\infty
 \frac{(2\sqrt{my})^{2\ell}}{(2\ell)!}
 =\cosh(2\sqrt{my})
 \le e^{2\sqrt{my}}.
 \end{aligned}
 \tag{J.38}
\]

For the right endpoint, set `F(u)=g(1-u)`, `alpha=25N/2`, and `x=d`.
Then

\[
 F(-d)=g(1+d),
 \qquad
 \int_0^2|F(u)|^2du=\|g\|_{L^2[-1,1]}^2.
 \tag{J.39}
\]

Combining the half-line estimate J.37 with the locally proved tail theorem
J.11, whose truncation point is now exactly `25N/alpha=2`, yields

\[
 |g(1+d)|^2
 \le \frac{20}{19}\alpha
 \left(\sum_{m=0}^{N-1}L_m(-\alpha d)^2\right)
 \|g\|_{L^2[-1,1]}^2.
 \tag{J.40}
\]

By J.38,

\[
 \sum_{m=0}^{N-1}L_m(-\alpha d)^2
 \le N e^{4\sqrt{N\alpha d}}
 =N e^{10\sqrt2N\sqrt d}.
 \tag{J.41}
\]

Since `alpha=25N/2`, taking square roots in J.40--J.41 proves the right
half of J.2.  Applying it to `t -> g(-t)` proves the left half.  This
completes the local reconstruction of the endpoint theorem.

## 6. Insertion into the exact-shear plateau proof

At a fixed scaled time, the R0.76I fibre `G(s,z)` has at most `2q`
complex branches with real frequencies `+-kappa_j`.  Set

\[
 e_a:=1-\frac{\delta_0}{a},\qquad
 E_a=[-e_a,e_a],\qquad
 I_a=\left[-1-\frac\delta a,1+\frac\delta a\right].
 \tag{J.42}
\]

This insertion is fail-closed against the frozen R0.76I dependency.  The
inherited main theorem has SHA-256
`6277cb69dfad94cae89088c6a8c007967bdde97aceee7b19954d10ec53f6efce`,
its primary audit has SHA-256
`65adf8bc77f33c5d18184c612acc67246e48e7ad3c9059b85f269e92c9372dbe`,
and the core commit is
`0b73f68e072e573d9aaaa824e137e29a49d3cd67`.  A hash mismatch invalidates
the downstream import until it is re-audited.

The two normalized exterior overshoots are at most `Delta_a` from J.5.
Apply J.2 to `x -> G(s,e_a x)` on the right and to its reflection on the
left.  Squaring, using `N<=2q`, and changing variables gives

\[
 \sup_{I_a\setminus E_a}|G(s,z)|^2
 \le\frac{1000}{19e_a}q^2e^{\Phi_a^{\rm loc}}
 \int_{E_a}|G(s,z)|^2dz.
 \tag{J.43}
\]

For an interior point `z in (-e_a,e_a)`, apply the affine form of J.2 at
`d=0` separately to `[-e_a,z]` and `[z,e_a]`.  If their lengths are
`ell_-=z+e_a` and `ell_+=e_a-z`, the two estimates are

\[
 \ell_-|G(s,z)|^2\le\frac{500}{19}N^2
 \int_{-e_a}^{z}|G(s,y)|^2dy,
 \qquad
 \ell_+|G(s,z)|^2\le\frac{500}{19}N^2
 \int_z^{e_a}|G(s,y)|^2dy.
\]

Add them, use `ell_-+ell_+=2e_a`, and then use `N<=2q`.
The endpoints follow directly by applying J.2 to all of `E_a`.  Thus

\[
 |G(s,z)|^2
 \le\frac{1000}{19e_a}q^2
 \int_{E_a}|G(s,y)|^2dy.
 \tag{J.44}
\]

Combining J.43--J.44 and using Hölder therefore gives the fully local
observation estimate

\[
 \sup_{I_a}|G(s,z)|^2
 \le\frac{1000}{19e_a}q^2e^{\Phi_a^{\rm loc}}
 \int_{E_a}|G(s,z)|^2dz
 \le\frac{2000}{19}q^2e^{\Phi_a^{\rm loc}}h(s)^{2/3}.
 \tag{J.45}
\]

The remainder of the frozen R0.76I argument uses only: Erdelyi's journal
Markov estimate; the Kós endpoint inequality recorded there; exact
full-plateau geometry; and the complete four-row energy identity.  Its
primary audit verifies each downstream sign, power, and scaling.  Replacing
I.17--I.19 by J.2 and J.43--J.45 therefore proves J.6--J.9 without changing
any polynomial power or physical scaling.

The bound `Delta_a=O(L^(-1))` gives

\[
 \frac{\Phi_a^{\rm loc}}{L^2}
 =O\!\left(\frac{q(L)}{L^{5/2}}\right),
 \qquad
 \frac{7\log q(L)}{L^2}\longrightarrow0
 \quad\text{when }q=o(L^{5/2}),
 \tag{J.46}
\]

while the frozen normalization cancels `R^(-1/3)` and contributes
`log(omega^(1/3))/L^2=-2/11907`.  This independently confirms J.9.

## 7. Claim boundary

**LITERATURE:** Erdelyi's 2017 Markov inequality and the Kós endpoint
inequality recorded in that paper enter only through the frozen downstream
R0.76I chain.  Boundary Plancherel is standard Fourier analysis.  Zhang's
2026 preprint supplies attribution for the proof architecture and the
earlier sharper-constant statement, not an unproved theorem used by J.2.

**PROVED LOCALLY:** the vertical-line basis J.12--J.20, Volterra/Laguerre
majorants J.21--J.31, local tail theorem J.32--J.34, half-line theorem
J.35--J.37, bilateral finite-edge theorem J.2 and J.38--J.41, scaled
observation J.43--J.45, and the resulting exact-shear theorem J.6--J.9
through the frozen audited R0.76I downstream chain.

**FINITE COMPUTATION:** certificates may verify constants, rational sample
values, term counts, equation order, source hashes, and dependency hashes.
They cannot prove Plancherel, the downstream literature inputs, or the
continuum arguments above.

**OPEN:** optimal polynomial and exponential constants in J.2 and J.6; a
matching lower bound inside the real dyadic heat-shear class; multiple
bands; nonconstant shear; arbitrary nonlinear packets; arbitrary-field
E.24; Version-M extraction; fixed deletion; suitable-weak transfer;
regularity; and singularity.

No simulation or formal figure is needed for this analytic proof.  The
result concerns an exact one-band constant shear, not arbitrary
three-dimensional Navier--Stokes data.  No novelty, priority, regularity,
singularity, or Clay claim is made.  **NOT CLAY.**
