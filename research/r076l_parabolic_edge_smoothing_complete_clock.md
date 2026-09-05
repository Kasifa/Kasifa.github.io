# R0.76L -- parabolic edge smoothing and the complete-clock Chebyshev residual

## 0. Result and exact boundary

R0.76K proves that a real one-dyadic-band Chebyshev packet can have the
fixed-slice cap-to-plateau gain

\[
 \exp\!\left(\Theta\!\left(\frac m{\sqrt A}\right)\right),
 \qquad A:=a-\delta _0,
 \tag{L.1}
\]

and embeds that slice in an exact integer heat shear.  It leaves open what
one and the same packet does over the complete clock.  The present note
settles the corresponding internal R0.76K question for a start-prepaid
Chebyshev family in the whole R0.76K degree window.

Retain the frozen geometry

\[
 a=\frac{32}{63}L,\qquad
 R=e^{-9L^2/40000},\qquad
 \omega=e^{-2L^2/3969},\qquad
 A=a-\delta _0,\qquad e_a=\frac Aa,
 \tag{L.2}
\]

and let `m=m(L)` be even with

\[
 \sqrt A\ll m=o(A^2),\qquad
 q=m+1,qquad
 \mu:=\left(\frac{m^2}{A}\right)^{1/3}.
 \tag{L.3}
\]

Thus `mu -> infinity`, `mu/A -> 0`, and the fixed-slice exponent in L.1
is `m/sqrt(A)=mu^(3/2)`.  There is an exact smooth real unforced
Navier--Stokes shear with the `q` positive integer frequencies

\[
 m,m+1,\ldots,2m
 \tag{L.4}
\]

and scaled drift

\[
 v_L:=\frac{B_LR}{a}=-\frac\beta A,
 \qquad B_L=-\frac{\beta a}{AR},
 \qquad \beta>0\ \hbox{fixed},
 \tag{L.5}
\]

for which the complete signed collar flux is eventually positive.  Put

\[
 \begin{aligned}
 G_L(s,z)&:=F_L(R^2s,aRz),\\
 \mathcal S_L
 &:=v_L\int_0^4\!\zeta(s)
       \int_{\mathbb R}W_a(z)|G_L(s,z)|^2\,dzds,\\
 \mathcal K_L
 &:=\int_0^4\!\int_{\mathbb R}
       \mathcal A_a(z)|G_L(s,z)|^3\,dzds,
 \end{aligned}
 \tag{L.6}
\]

where

\[
 W_a(z)=-2\pi az\vartheta(a(|z|-1)),
 \qquad
 \mathcal A_a(z)=\pi\left(
 [(a+\delta _0)^2-a^2z^2]_+
 -[(a-\delta _0)^2-a^2z^2]_+
 \right).
 \tag{L.7}
\]

The physical flux and full-plateau mass are exactly

\[
 \mathcal T_L=\frac{a^2R^3}{2}\mathcal S_L,
 \qquad
 M_L^{\rm plat}=aR^5\mathcal K_L.
 \tag{L.8}
\]

Let the frozen positive subcap satisfy

\[
 \delta _0<r_c-3h<r_c+3h<\delta,
 \qquad
 \vartheta(r)\ge c_\vartheta>0
 \quad(|r-r_c|\le3h),
 \tag{L.9}
\]

and define the strictly positive cap-to-plateau edge gap

\[
 c_-:=r_c-h+\delta _0,qquad
 c_p:=2\delta _0,qquad
 \Delta_c:=c_--c_p=r_c-h-\delta _0>0.
 \tag{L.10}
\]

Then constants `c,C,L_0>0`, depending only on the frozen cutoffs and
`beta`, satisfy for `L>=L_0`

\[
 \boxed{
 \begin{aligned}
 &c\,\frac{\beta a^{2/3}}{A(1+\mu^2)}
 \exp\!\left(
   [2^{-1/3}\Delta_c-o(1)]\mu\right)\\
 &\hspace{38mm}\le
 R^{1/3}\frac{\mathcal T_L}{(M_L^{\rm plat})^{2/3}}\\
 &\hspace{38mm}\le
 C\,\frac{\beta a^{4/3}}A(1+\mu^2)^{2/3}
 e^{C\mu}.
 \end{aligned}}
 \tag{L.11}
\]

The coefficient `2^(-1/3) Delta_c` is
`2 G_4 Delta_c`, where `G_4=2^(-4/3)` is the exact terminal
parabolic edge slope.  In particular the exponential part of the
complete-clock quotient is of order `exp(Theta(mu))`, rather than the
fixed-slice `exp(Theta(mu^(3/2)))`.  If `mu/log A -> infinity`, the
unweighted middle quotient in L.11 diverges, so for this start-prepaid
family and this unweighted quotient the complete-clock obstruction is
genuine and is not merely a single-time artefact.

With the frozen normalized quantities

\[
 p_L^{\rm plat}=R^{-2}\omega M_L^{\rm plat},
 \qquad
 \mathfrak X_L=\frac\omega R[\mathcal T_L]_+,
 \tag{L.12}
\]

L.11 gives the exact quadratic logarithmic rate

\[
 \boxed{
 \lim_{L\to\infty}\frac1{L^2}
 \log\frac{\mathfrak X_L}{(p_L^{\rm plat})^{2/3}}
 =-\frac2{11907}<0.}
 \tag{L.13}
\]

Thus, for the present family, forward parabolic evolution absorbs the
stronger R0.76K edge exponent throughout `m=o(A^2)`.  It leaves a smaller, explicitly
quantified complete-clock residual, but that residual is `o(L^2)` and
cannot pay the frozen `omega^(1/3)` deficit.  This is a theorem about one
exact-shear family.  It is not a uniform theorem for arbitrary packets and
does not cover `m` comparable with or larger than `A^2`.  Section 10 records
a high-degree saddle that must therefore be studied next.  **NOT CLAY.**

The claim boundary used throughout this note is explicit:

- **LITERATURE-ESTABLISHED:** polynomial heat-flow formulas, Gaussian
  convolution, and the Chebyshev identities cited in the source report;
- **PROVED LOCALLY:** L.17--L.66 for the one exact start-prepaid family
  specified above;
- **FINITE COMPUTATION:** the deterministic diagnostic in Section 9, used
  only to catch scaling, constant, and sign regressions;
- **OPEN:** L.70--L.72, arbitrary packet classes, Version-M, and every Clay
  regularity or singularity claim.

## 1. The forward Chebyshev edge object

For `s>=0` and real `c`, define

\[
 Q_{m,A}(s,c):=
 \left(e^{sA^{-2}D_x^2}T_m\right)
 \left(1+\frac cA\right).
 \tag{L.14}
\]

Equivalently, if `Z` is standard Gaussian,

\[
 Q_{m,A}(s,c)
 =\mathbb E\,T_m\!\left(
 1+\frac{c+\sqrt{2s}Z}{A}\right).
 \tag{L.15}
\]

The scale in L.3 is selected by the dominant balance in this formula under
L.3.  On the positive exterior put
`y=c+sqrt(2s)Z`.  Then

\[
 I_{m,A}(s,c):=\frac1{\sqrt{4\pi s}}
 \int_0^\infty
 \cosh\!\left(m\operatorname {arcosh}\left(1+\frac yA\right)\right)
 e^{-(y-c)^2/(4s)}\,dy.
 \tag{L.16}
\]

After `y=mu z`, the two competing terms in the logarithm are both of
order `mu^2`:

\[
 \frac1{\mu^2}
 \left[
 m\operatorname {arcosh}\left(1+\frac{\mu z}{A}\right)
 -\frac{(\mu z-c)^2}{4s}
 \right]
 \longrightarrow
 \Phi_s(z):=\sqrt{2z}-\frac{z^2}{4s}.
 \tag{L.17}
\]

The convergence is locally uniform for `z>=0` and uniformly when `s`
ranges in a compact subset of `(0,infinity)`.  Indeed `mu/A -> 0` and

\[
 \operatorname {arcosh}(1+u)=\sqrt{2u}\,[1+O(u)]
 \quad(u\downarrow0).
 \tag{L.18}
\]

The rate function has the unique maximizer and maximum

\[
 z_s=2^{1/3}s^{2/3},
 \qquad
 F_s:=\Phi_s(z_s)=3\,2^{-4/3}s^{1/3}.
 \tag{L.19}
\]

In particular

\[
 z_4=2^{5/3},qquad
 F_4=3\,2^{-2/3}=\frac34\,2^{4/3}.
 \tag{L.20}
\]

## 2. Uniform Laplace principle and the edge tilt

The terminating heat formula L.14, its Gaussian representation L.15, and
the Chebyshev identities used below are classical inputs.  The local proof
starts with their simultaneous growing-degree, shrinking-edge limit.

The elementary global inequality

\[
 \operatorname {arcosh}(1+u)\le\sqrt{2u}
 \qquad(u\ge0)
 \tag{L.21}
\]

and the quadratic Gaussian penalty make the scaled integrands in L.16
exponentially tight.  The local convergence L.17 and the usual compact
upper/lower split therefore give, uniformly for
`s in [s_0,s_1] subset (0,infinity)`,

\[
 \frac1{\mu^2}\log I_{m,A}(s,0)\longrightarrow F_s.
 \tag{L.22}
\]

The next order in a fixed edge displacement is obtained without requiring
a next-order expansion of `arcosh`.  Under the probability measure

\[
 d\nu_{m,A,s}(y)=
 \frac{
  \cosh(m\operatorname {arcosh}(1+y/A))e^{-y^2/(4s)}
  \mathbf1_{y\ge0}\,dy}
 {\sqrt{4\pi s}\,I_{m,A}(s,0)},
 \tag{L.23}
\]

the random variable `Y/mu` concentrates exponentially at `z_s` with
speed `mu^2`.  The exact Gaussian tilt identity is

\[
 \frac{I_{m,A}(s,c)}{I_{m,A}(s,0)}
 =e^{-c^2/(4s)}
 \mathbb E_{\nu_{m,A,s}}
 \exp\!\left(\frac{cY}{2s}\right).
 \tag{L.24}
\]

Here the exponential tilt is unbounded, so ordinary concentration alone is
not enough.  The required tilted-tail estimate follows from the same rate
function.  Fix compact sets of positive `s` and bounded `c`.  On a compact
`z`-set outside `|z-z_s|<epsilon`, strict concavity gives a rate loss
`-kappa_epsilon mu^2`, whereas the added tilt is only `O(mu)`.  Beyond a
fixed sufficiently large `z`, L.21 gives uniformly

\[
 \mu^2\left(\sqrt{2z}-\frac{z^2}{4s}\right)+C\mu z
 \le -\frac{\mu^2z^2}{8s_1}.
\]

Consequently, for some `kappa_epsilon>0`,

\[
 \int_{|Y/\mu-z_s|>\epsilon}e^{cY/(2s)}\,d\nu_{m,A,s}
 \le
 \exp\!\left(\frac{cz_s}{2s}\mu
              -\kappa_\epsilon\mu^2+C\mu\right)
\]

uniformly on those compact sets.  On the complementary event the tilt is
trapped between its values at `mu(z_s-epsilon)` and
`mu(z_s+epsilon)`.  Taking logarithms, first sending `L` to infinity and
then `epsilon` to zero, gives

\[
 \lim_{L\to\infty}\frac1\mu
 \log\frac{I_{m,A}(s,c_2)}{I_{m,A}(s,c_1)}
 =G_s(c_2-c_1),
 \qquad
 G_s:=\frac{z_s}{2s}=2^{-2/3}s^{-1/3}.
 \tag{L.25}
\]

The convergence is uniform for `s` in a fixed positive compact interval
and `c_1,c_2` in a fixed real compact interval.  Notice

\[
 G_4=2^{-4/3}.
 \tag{L.26}
\]

It remains to pass from the positive exterior integral to the signed
polynomial heat flow.  On `-2A<=y<=0`, `|T_m(1+y/A)|<=1`, so that part of
L.15 is bounded.  If `y=-2A-u`, `u>=0`, then

\[
 |T_m(1+y/A)|
 =\cosh\!\left(m\operatorname {arcosh}(1+u/A)\right).
 \tag{L.27}
\]

Using L.21, the negative-exterior logarithm is at most

\[
 \frac m{\sqrt A}\sqrt{2u}
 -\frac{(2A+u+c)^2}{4s}+O(1)
 \le-cA^2+o(A^2),
 \tag{L.28}
\]

uniformly for bounded `c` and positive compact `s`.  Indeed, Young's
inequality bounds the positive term uniformly in `u>=0` by
`u^2/(16s_1)+C mu^2`; after expanding the negative square, the remaining
quadratic has supremum at most `-cA^2+Cmu^2+O(A)`.  Here
`mu^2=o(A^2)` follows from `m=o(A^2)`.  Since L.22 grows like
`exp(F_s mu^2)`, the bounded middle and L.28 are negligible.  Hence

\[
 \boxed{
 \begin{aligned}
 &Q_{m,A}(s,c)>0\quad\hbox{for all sufficiently large }L,\\
 &\frac1{\mu^2}\log Q_{m,A}(s,0)\longrightarrow F_s,\\
 &\frac1\mu\log
   \frac{Q_{m,A}(s,c_2)}{Q_{m,A}(s,c_1)}
   \longrightarrow G_s(c_2-c_1),
 \end{aligned}}
 \tag{L.29}
\]

with the same uniformity as above.  This is the family-specific double-scale
asymptotic proved here.  It is an analytic limit, not an inference from the
finite diagnostic in Section 9.

## 3. Positive series and terminal-layer control

For `0<=k<=m`, let `D_k=T_m^(k)(1)`.  The endpoint derivative formula is

\[
 D_0=1,qquad
 D_k=\frac{m^2\prod_{r=1}^{k-1}(m^2-r^2)}{(2k-1)!!}>0
 \quad(1\le k\le m),
 \tag{L.30}
\]

and therefore

\[
 \frac{D_{k+1}}{D_k}=\frac{m^2-k^2}{2k+1}
 \qquad(0\le k<m).
 \tag{L.31}
\]

Taylor expansion at `x=1` followed by the terminating heat series gives
the exact positive double sum

\[
 Q_{m,A}(s,c)=
 \sum_{\ell+2j\le m}
 \frac{D_{\ell+2j}}{A^{\ell+2j}\ell!j!}
 c^\ell s^j.
 \tag{L.32}
\]

Consequently `Q` is increasing separately in `s` and `c` on the positive
quadrant.  The same expansion gives a quantitative terminal layer.  Treat
the summands in L.32 as positive weights.  At fixed `ell`, consecutive
`j`-weights satisfy, with `k=ell+2j`,

\[
 \frac{w_{j+1,\ell}}{w_{j,\ell}}
 =\frac{s}{A^2(j+1)}
 \frac{(m^2-k^2)(m^2-(k+1)^2)}{(2k+1)(2k+3)}
 \le\frac{C\mu^6}{(j+1)^3}.
 \tag{L.33}
\]

Once `j>=C_0(1+mu^2)`, the last ratio is at most `1/2`.  Conditional on each
fixed `ell` with nonzero total weight, the part below this threshold
contributes at most the threshold and the remaining geometric tail
contributes at most a universal constant; zero-weight rows are ignored.
Averaging these conditional bounds over `ell` yields

\[
 0\le\partial_s\log Q_{m,A}(s,c)
 =\frac{\mathbb E(j)}s
 \le C(1+\mu^2)
 \tag{L.34}
\]

for `s` in a fixed positive compact interval and `c>=0` in a fixed compact
interval.  Moreover

\[
 \mathbb E[\ell(\ell-1)]
 =c^2\frac{\partial_c^2Q}{Q}
 =c^2\frac{\partial_sQ}{Q}.
 \tag{L.35}
\]

Since `ell<=1+sqrt(ell(ell-1))` for every nonnegative integer `ell`,
Cauchy--Schwarz and L.34 imply, for `c>=c_0>0`,

\[
 0\le\partial_c\log Q_{m,A}(s,c)
 \le\frac1{c_0}+\sqrt{\frac{\partial_sQ}{Q}}
 \le C(1+\mu).
 \tag{L.36}
\]

Put

\[
 h_L:=\frac1{1+\mu^2}.
 \tag{L.37}
\]

Equations L.34--L.36 show that changing time by at most `h_L` and a
positive edge coordinate by at most `h_L` changes `Q` by at most a fixed
multiplicative constant.  This turns the pointwise terminal saddle into a
time interval of polynomial, rather than exponential, cost.

## 4. Exact one-band integer shear

Set

\[
 \eta=AR,qquad
 w_\eta(x)=\frac{e^{i\eta x}-1}{i\eta},
 \qquad
 h_\eta(x)=T_m(w_\eta(x))
 =\sum_{j=0}^m b_j(\eta)e^{ij\eta x}.
 \tag{L.38}
\]

The coefficient identity from R0.76K is

\[
 b_j(\eta)=
 \frac{T_m^{(j)}(i/\eta)}{j!(i\eta)^j}.
 \tag{L.39}
\]

All zeros of `T_m` and of each nonconstant derivative are real.  Hence
`T_m^(j)(i/eta)` is nonzero for every `eta>0`; the top derivative is a
nonzero constant.  Thus every `b_j(eta)` is nonzero without invoking the
coarse growing-degree condition `eta q^2 7^q -> 0` used for the more
general R0.76K slice family.

Choose

\[
 n_j=m+j,qquad M_L=m\eta,qquad
 A_j=2|b_j(\eta)|,qquad
 \phi_j\equiv-\arg b_j(\eta)\pmod{2\pi},
 \tag{L.40}
\]

and define

\[
 F_L(t,x_2)=\sum_{j=0}^m A_je^{-n_j^2t}
 \cos(n_jx_2-\phi_j-n_jB_Lt).
 \tag{L.41}
\]

The frequencies are exactly L.4 and lie in the closed dyadic band
`[m,2m]`.  The field

\[
 u_L(t,x)=(0,B_L,F_L(t,x_2))
 \tag{L.42}
\]

is divergence free and solves the unforced three-dimensional
Navier--Stokes equation with constant pressure because

\[
 (\partial_t+B_L\partial_2-\partial_2^2)F_L=0.
 \tag{L.43}
\]

This is an exact PDE solution, not a numerical approximation.  Its
constant background has not been placed in the frozen mean-zero,
inversion-paired Version-M subclass.

## 5. Uniform dynamic confluence

Write `z=e_a x`.  Direct heat-semigroup conjugation gives the complex half
of the exact scaled field:

\[
 \begin{aligned}
 \mathcal H_L(s,x)
 &=e^{-M_L^2s/A^2+iM_L(x-v_Ls/e_a)}\\
 &\quad\times
 \left(e^{sA^{-2}D_x^2}h_\eta\right)
 \left(x-\frac{v_Ls}{e_a}
       +\frac{2iM_Ls}{A^2}\right),\\
 G_L(s,e_ax)&=2\operatorname {Re}\mathcal H_L(s,x).
 \end{aligned}
 \tag{L.44}
\]

Here `M_L=mAR -> 0` faster than every algebraic scale allowed by L.3.
The growing-degree confluence in L.44 is uniform over the complete clock.
One convenient finite-dimensional proof uses `w=w_eta(x)`:

\[
 D_x^2=
 (1+i\eta w)^2D_w^2+i\eta(1+i\eta w)D_w
 =:\mathcal L_\eta.
 \tag{L.45}
\]

For a polynomial `p(w)=sum_(k=0)^m p_k w^k` and fixed `rho>0`, put
`||p||_rho=sum |p_k|rho^k`.  Multiplication by `w` has norm `rho`, while
`D_w` and `D_w^2` have norms at most `m/rho` and `m^2/rho^2`.
Consequently, on this finite-dimensional space,

\[
 \|\mathcal L_\eta-D_w^2\|\le C\eta m^2,
 \qquad
 \|\mathcal L_\eta\|+\|D_w^2\|\le Cm^2.
 \tag{L.46}
\]

Take nested fixed disks with every argument in L.44 contained in
`|x|<=5/2`, its `w_eta` image contained in `|w|<=3`, and coefficient radius
`rho=4`; this holds for all large `L`.  On that radius
`||T_m||_rho<=C_rho^m`.  If `t=s/A^2`, Duhamel's formula gives the explicit
operator estimate

\[
 \|e^{t\mathcal L_\eta}T_m-e^{tD_w^2}T_m\|_\rho
 \le Ct\eta m^2 C_\rho^m e^{Ctm^2},
 \qquad 0\le s\le4.
\]

Moreover `|w_eta(x)-x|<=Ceta` on the inner disk.  The evaluation difference
is controlled by the same coefficient norm after one derivative.  Finally,
the four remaining perturbations in L.44 have sizes

\[
 M_L=m\eta,
 \qquad M_L^2/A^2,
 \qquad 2M_Ls/A^2,
 \qquad |v_L|s/e_a=O(A^{-1}),
\]

where the drift is retained in the comparison term rather than discarded.
The carrier, scalar damping, imaginary shift, operator replacement, and
`w_eta` replacement therefore give

\[
 \begin{aligned}
 \varepsilon_L
 &:=\sup_{0\le s\le4,\ |x|\le2}
 \left|
 G_L(s,e_ax)-2
 \left(e^{sA^{-2}D_x^2}T_m\right)
 \left(x-\frac{v_Ls}{e_a}\right)
 \right|\\
 &\le \eta\,\operatorname {poly}(m,A)
 \exp\!\left(Cm+C\frac{m^2}{A^2}\right)
 =\exp\!\left(-\frac9{40000}L^2+o(L^2)\right)
 \longrightarrow0.
 \end{aligned}
 \tag{L.47}
\]

Both `m=o(A^2)` and the exact frozen value of `eta=AR` are essential in the
last equality: `m=o(L^2)` and `m^2/A^2=o(L^2)`, so every positive term in
the exponent after `log eta` is `o(L^2)`.  Thus L.29 transfers
to the exact integer shear uniformly wherever the cap and plateau
arguments used below remain in fixed edge-coordinate intervals.

## 6. Paired caps and complete-clock positivity

For `r in supp(vartheta)` define

\[
 x_r=\frac{a+r}{A}=1+\frac{r+\delta _0}{A},
 \qquad
 \gamma_L:=\frac{\beta a}{A}.
 \tag{L.48}
\]

At the paired points `z=plus/minus(1+r/a)`, transport and parity show that
the ideal edge coordinates are

\[
 c_+(s,r)=r+\delta _0+\gamma_Ls,
 \qquad
 c_-(s,r)=r+\delta _0-\gamma_Ls.
 \tag{L.49}
\]

For `3<=s<=4`, L.29 is uniform over the fixed support of `vartheta` and

\[
 \frac1\mu\log
 \frac{Q_{m,A}(s,c_+(s,r))}
      {Q_{m,A}(s,c_-(s,r))}
 =2G_s\gamma_Ls+o(1)>0.
 \tag{L.50}
\]

The exact transfer error is negligible relative to the exponentially
large positive `Q`.  Uniformly for `3<=s<=4`, L.50 in fact gives

\[
 \frac{Q_{m,A}(s,c_-(s,r))^2}
      {Q_{m,A}(s,c_+(s,r))^2}
 \le e^{-c\beta\mu}.
\]

Since `W_a(-z)=-W_a(z)` and `v_L<0`, every paired collar contribution on
`3<s<4` is therefore nonnegative for all large `L`.

Possible adverse contribution from `0<=s<=3` is exponentially smaller
than the terminal contribution.  The endpoint majorant from Section 7,
applied on this fixed collar, gives the quantitative bound
`C(beta/A)Q_(m,A)(3,C)^2` for its absolute value.  Meanwhile L.22 and L.25
give

\[
 \log\frac{Q_{m,A}(4,c)}{Q_{m,A}(3,c')}
 =(F_4-F_3)\mu^2+o(\mu^2)
 \tag{L.51}
\]

for any fixed edge coordinates `c,c'`; `F_4-F_3>0`.

On the terminal box

\[
 4-h_L\le s<4,
 \qquad r_c-h\le r\le r_c+h,
 \tag{L.52}
\]

the clock cutoff is exactly one, `-W_a(1+r/a)>=ca`, and L.34--L.36 give

\[
 |G_L(s,1+r/a)|
 \ge c\,Q_{m,A}(4,c_-+4\gamma_L).
 \tag{L.53}
\]

The negative paired cap is at most `e^{-c beta mu}` times the positive one
by the squared form of L.50.  Hence the box in L.52 contributes at least
`c(beta/A)h_L Q_(m,A)(4,c_-+4gamma_L)^2`.  Relative to this term, the whole
early adverse part is at most

\[
 Ch_L^{-1}\exp\!\left(
 -2(F_4-F_3)\mu^2+o(\mu^2)\right)\longrightarrow0.
\]

Integrating L.53, using `dz=dr/a`, and absorbing this explicit ratio proves

\[
 \boxed{
 \mathcal S_L>0,
 \qquad
 \mathcal S_L\ge
 c\frac\beta A h_L
 Q_{m,A}(4,c_-+4\gamma_L)^2.}
 \tag{L.54}
\]

For the reverse bound, the fixed collar, complete clock, L.32, parity, and
the endpoint derivative bound used in the next section give

\[
 \boxed{
 \mathcal S_L\le
 C\frac\beta A
 Q_{m,A}(4,C_+)^2}
 \tag{L.55}
\]

for one fixed `C_+` depending only on the frozen support and `beta`.

## 7. Full-plateau payment

The entire plateau projects into

\[
 |x|\le1+\frac{2\delta _0}{A}.
 \tag{L.56}
\]

For `|x|<=1`, the classical endpoint derivative inequality

\[
 |T_m^{(k)}(x)|\le T_m^{(k)}(1),
 \qquad 0\le k\le m,
 \tag{L.57}
\]

follows from the Gegenbauer derivative identity; for `|x|>=1`, parity and
the positive endpoint expansion give the corresponding monotone exterior
bound.  In L.56 the drift moves an ideal real argument by at most
`4beta/(Ae_a)`, so after reflection at the negative edge every term is
majorized by the positive endpoint coordinate `c_p+4gamma_L`.  Applying
the terminating heat series term by term and then L.47 yields

\[
 \sup_{0\le s\le4,\ z\in\operatorname {proj}(\mathcal S_{a,R}^{\rm plat})}
 |G_L(s,z)|
 \le C Q_{m,A}(4,c_p+4\gamma_L).
 \tag{L.58}
\]

Since `A_a(z)<=4pi a delta_0` and the projected interval has bounded
length,

\[
 \boxed{
 \mathcal K_L\le
 Ca\,Q_{m,A}(4,c_p+4\gamma_L)^3.}
 \tag{L.59}
\]

A lower payment is obtained from a fixed positive outer plateau strip.
Use the `c` coordinate

\[
 z=e_a\left(1+\frac cA\right)
 =1+\frac{c-\delta _0}{a},
 \qquad \delta _0\le c\le\frac32\delta _0.
 \tag{L.60}
\]

On this strip `A_a(z)>=ca`, `dz=dc/a`, and the exact field is positive
and comparable with its ideal limit throughout the terminal time layer.
Equations L.34--L.36 therefore imply

\[
 \boxed{
 \mathcal K_L\ge
 c h_L Q_{m,A}(4,c_0+4\gamma_L)^3}
 \tag{L.61}
\]

with the explicit choice `c_0=delta_0`.  By L.25,

\[
 \begin{aligned}
 \log\frac{Q_{m,A}(4,c_-+4\gamma_L)}
               {Q_{m,A}(4,c_p+4\gamma_L)}
 &=[2^{-4/3}\Delta_c+o(1)]\mu,\\
 \log\frac{Q_{m,A}(4,C_+)}
               {Q_{m,A}(4,c_0+4\gamma_L)}
 &\le C\mu.
 \end{aligned}
 \tag{L.62}
\]

Combining L.54 with L.59 proves the lower half of L.11; combining L.55
with L.61 proves the upper half.  The factors `a^(2/3)` and `a^(4/3)`
come only from the exact conversion L.8 and the upper versus lower
cross-sectional estimates.  They are not part of the exponential edge
law.

## 8. Frozen normalization

The definitions L.8 and L.12 give the exact identity

\[
 \frac{\mathfrak X_L}{(p_L^{\rm plat})^{2/3}}
 =R^{1/3}\omega^{1/3}
 \frac{\mathcal T_L}{(M_L^{\rm plat})^{2/3}}.
 \tag{L.63}
\]

Because `a` and `A` are comparable with `L`, `mu=o(A)`, and

\[
 \frac1{L^2}\log\omega^{1/3}=-\frac2{11907},
 \qquad
 \frac{\mu+\log A}{L^2}\longrightarrow0,
 \tag{L.64}
\]

both sides of L.11 have the same normalized quadratic logarithmic rate.
This proves L.13.  Equivalently, since

\[
 A^2=\frac{1024}{3969}L^2+o(L^2),
 \tag{L.65}
\]

the frozen penalty is

\[
 \omega^{1/3}=\exp\!\left(-\frac{A^2}{1536}+o(A^2)\right).
 \tag{L.66}
\]

The complete-clock residual `exp(Theta(mu))` is strictly too small in the
present degree range.

## 9. Finite diagnostic and its boundary

A deterministic double-precision quadrature was run for the positive
integral L.16 at `s=4`, `c=0,1`,

\[
 A\in\{256,1024,4096,16384\},
 \qquad
 m\approx A^p,\qquad
 p\in\{0.75,1,1.25,1.5\}.
 \tag{L.67}
\]

It independently tracks the three normalized quantities

\[
 \frac{y_*}{\mu},qquad
 \frac{\log I_{m,A}(4,0)}{\mu^2},
 \qquad
 \frac{\log I_{m,A}(4,1)-\log I_{m,A}(4,0)}\mu,
 \tag{L.68}
\]

whose theoretical limits are respectively

\[
 2^{5/3}=3.174802\ldots,qquad
 3\,2^{-2/3}=1.889882\ldots,qquad
 2^{-4/3}=0.396850\ldots.
 \tag{L.69}
\]

The archived data and vector figure are consistent with the three limits
and show convergence in most displayed sequences.  The `p=0.75` unit-tilt
sequence moves slightly away from its analytic limit over the displayed
range, as is explicitly recorded in the caption.  The computation checks the selected scaling and
catches constant/sign regressions.  It is not evidence for the continuum
proof, the exact PDE transfer, or the complete-clock sign argument.

## 10. What this closes and what comes next

R0.76L establishes four statements within the explicit R0.76K
start-prepaid route:

1. the sharp leading-order fixed-positive-time double-scale saddle
   asymptotic;
2. the loss from the static exponent `mu^(3/2)` to the parabolic exponent
   `mu`;
3. complete-clock positivity of the signed paired-cap flux for one exact
   real dyadic integer shear;
4. matching full-plateau payment and the frozen negative rate L.13.

It does not prove a uniform theorem for arbitrary real dyadic packets,
remove the `exp(Cq)` factor in R0.76E, enter Version-M, or establish
regularity or singularity.

The degree restriction is structural, not cosmetic.  When `m` is much
larger than `A^2`, the saddle leaves the edge scaling used in L.17.  Direct
optimization then predicts

\[
 y_s\sim\sqrt{2sm},
 \qquad x_s-1=\frac{y_s}{A}
 \sim\frac{\sqrt{2sm}}A,
 \qquad
 \partial_c\log Q_{m,A}(s,c)
 \sim\sqrt{\frac{m}{2s}}.
 \tag{L.70}
\]

At the formal scale `m=kappa A^4`, the terminal squared cap-to-plateau
exponent becomes

\[
 \Delta_c\sqrt{\frac\kappa2}\,A^2+o(A^2).
 \tag{L.71}
\]

Comparison with L.66 gives the candidate threshold

\[
 \kappa>\frac{2}{1536^2\Delta_c^2}.
 \tag{L.72}
\]

Equations L.70--L.72 are a derived **OPEN DIRECTION**, not a theorem of
this release.  They lie far beyond the R0.76J--K mode window, and require a
new bulk-exterior saddle theorem, direct growing-degree `w_eta` transfer,
signed-pairing bounds, and a full-plateau certificate.  They prevent the
present route-specific negative result in the range `m=o(A^2)` from being
overread as a no-go theorem for every possible degree.  **NOT CLAY.**
