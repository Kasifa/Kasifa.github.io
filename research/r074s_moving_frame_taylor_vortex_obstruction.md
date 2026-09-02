# R0.74S Step 16 — a smooth obstruction to the quadratic temporal tail for every \(p>1\)

## 0. Result and scope

Step 15 showed that one common-deletion temporal flux tail would pay both
branches of the combined terminal residual.  The exponent \(p>1\) in the
Step 13 candidate (S.342), however, asks for more than that reduction needs.
This note tests that extra time integrability on an exact smooth solution.

There are five conclusions.

1. A translated copy of Taylor's 1923 bi-periodic decaying vortex is an exact
   smooth, periodic, mean-zero, unforced three-dimensional Navier--Stokes
   solution for every amplitude \(A>0\).
2. Its fixed-frame Bernoulli flux through every periodic shell vanishes
   exactly.  In Version M, the mollified terminal trajectory leaves a
   nonzero moving-cutoff drift.  The drift can be computed exactly by one
   radial Fourier multiplier.
3. Given any finite deletion budget \(N\), the scale \(R\) can be fixed so
   that the first \(N+1\) physical shells all have a strictly positive drift
   multiplier.  With \(N,R\) fixed, on a terminal interval of physical
   length \(c/A\), every one of those flux densities is of size \(A^3\).
4. The complete frozen payment is at most \(C_R A^3\), whereas the
   common-deletion temporal tail is at least
   \(c_{p,N,R}A^{3-1/p}\).  Therefore, for every \(p>1\), every finite \(N\),
   and every proposed universal constant, a smooth member of this family
   violates (S.342).  Thus **(S.342 is false)**, already in the smooth
   periodic class.
5. At the critical exponent \(p=1\), the same family has
   \(\mathfrak H^F_{1,N,R}\asymp_{N,R} A^2\) and
   \(P_R^M\asymp_R A^3\).  It therefore saturates the amplitude exponent at
   fixed \(N,R\), rather than contradicting the quadratic scale.  A natural
   surviving candidate, still sufficient by Step 15, is the fixed-deletion
   \(L_t^1\) estimate (S.444) below.

The counterexample is only to the supercritical temporal-tail statement
(S.342).  It does **not** disprove the hybrid terminal-flux gate, the
critical \(L_t^1\) candidate, Step 10 (S.243), Q.12, Q.1, scale contraction,
or regularity.  It is not a singular solution and says nothing directly
about singularity formation.  **NOT CLAY.**

## 1. Taylor's exact smooth bi-periodic decaying vortex

On \(\mathbb T^3=(-\pi,\pi]^3\), put

\[
 \boxed{
 W(x)=\bigl(\sin x_1\cos x_2,-\cos x_1\sin x_2,0\bigr),
 \qquad
 p_W(x)={\cos 2x_1+\cos 2x_2\over4}.}
 \tag{S.417}
\]

Direct differentiation gives

\[
 \boxed{
 \nabla\!\cdot W=0,
 \qquad \Delta W=-2W,
 \qquad (W\!\cdot\!\nabla)W=-\nabla p_W.}
 \tag{S.418}
\]

Fix \(t_0>0\), choose \(R\) later with
\(\overline I_{8R}\Subset(0,T)\), and define

\[
 b_A(t):=Ae^{-2(t-t_0)},
 \qquad
 u_A(t,x):=b_A(t)W(x),
 \qquad
 p_A(t,x):=b_A(t)^2p_W(x).
 \tag{S.419}
\]

Equations (S.418)--(S.419) prove exactly that

\[
 \partial_tu_A-\Delta u_A+(u_A\!\cdot\!\nabla)u_A+\nabla p_A=0.
 \tag{S.420}
\]

The field is smooth for all finite times, periodic, mean zero, and
independent of \(x_3\).  Its use below is therefore a two-dimensional smooth
screen embedded in the three-dimensional solution class.  Amplitude
multiplication is legitimate here because \(W\) is simultaneously a steady
Euler field and a Laplace eigenfield; it is not being used as a symmetry of
general Navier--Stokes solutions.

## 2. The mollified trajectory and its exact phase

Let the frozen even radial mollifier be the one from R0.74E.  Every Fourier
mode of \(W\) has length \(\sqrt2\), so radiality gives one real multiplier

\[
 \varphi_R^{\rm per}*W=\mu_R W,
 \qquad
 \mu_R:=\int_{\mathbb R^3}\varphi(z)
            \cos\!\bigl(R(1,1,0)\cdot z\bigr)\,dz.
 \tag{S.421}
\]

All Fourier modes of \(W\) have length \(\sqrt2\), so radiality makes this
the common multiplier.  Since \(\varphi\ge0\) and \(\int\varphi=1\),
\(|\mu_R|\le1\); by continuity at the origin, \(\mu_R\to1\) as
\(R\downarrow0\).  We will require \(1/2\le\mu_R\le1\).

Choose the terminal centre

\[
 x_*=(\pi/4,0,0),
 \qquad X_R(t_0)=x_*.
\]

Writing \(\xi(t)=X_R(t)\), the Version-M trajectory and moving fields are

\[
 \boxed{
 \dot\xi=\mu_Rb_AW(\xi),
 \quad
 v_R(t,y)=b_A(t)W(y+\xi(t)),
 \quad
 \pi_R(t,y)=b_A(t)^2p_W(y+\xi(t)).}
 \tag{S.422}
\]

Uniqueness in the second and third coordinate equations gives
\(\xi_2=\xi_3=0\).  The first coordinate satisfies

\[
 \dot\xi_1=\mu_Rb_A\sin\xi_1,
 \qquad
 \boxed{
 \tan{\xi_1(t)\over2}
 =\tan{\pi\over8}
 \exp\!\left(-\mu_R\int_t^{t_0}b_A(s)\,ds\right).}
 \tag{S.423}
\]

In particular, \(0<\xi_1(t)\le\pi/4\) throughout the past time window.
This terminal-value path has no winding or lift ambiguity.

## 3. Exact moving-shell flux

For the inherited unperiodized shell cutoff \(\psi_k^R\) and its
periodization \(\Psi_k^R\), define

\[
 m_{k,R}:=\int_{\mathbb R^3}\psi_k^R(y)\,dy,
 \qquad
 J_{k,R}(\xi):=\int_{\mathbb T^3}\Psi_k^R(y)
          |W(y+\xi)|^2\,dy.
 \tag{S.424}
\]

The pointwise Bernoulli function
\(B_W=|W|^2/2+p_W\) obeys
\(\nabla\cdot(B_WW)=0\) by (S.418).  Hence the kinetic and physical-pressure
parts of the shell flux cancel after periodic integration by parts.  The
time-dependent pressure gauge also integrates to zero by incompressibility.
Substitution in the exact Version-M flux derivative leaves only the
moving-cutoff drift:

\[
\begin{aligned}
 \dot F_{k,R}(t)
 &= -{\gamma_k\eta_Rb_A(t)^2\over2R}\,
       \mu_Rb_A(t)W(\xi(t))\cdot
       \int_{\mathbb T^3}|W(y+\xi(t))|^2\nabla\Psi_k^R(y)\,dy\\
 &=\boxed{
 {\gamma_k\mu_R\eta_R(t)b_A(t)^3\over2R}
       W(\xi(t))\cdot\nabla_\xi J_{k,R}(\xi(t)).}
 \tag{S.425}
\end{aligned}
\]

The sign in the second line follows from

\[
 \int |W(y+\xi)|^2\nabla\Psi_k^R(y)\,dy
 =-\nabla_\xi J_{k,R}(\xi).
\]

This identity is important: the fixed-frame physical energy flux is zero,
but the frozen observable follows a nonconstant local velocity.  The
resulting drift is part of the Version-M shell flux and cannot be discarded.

## 4. One radial multiplier activates \(N+1\) physical shells

Taylor's planar field has

\[
 |W(x)|^2={1-\cos2x_1\cos2x_2\over2}.
 \tag{S.426}
\]

Put \(q_+=(2,2,0)\) and define the radial Fourier coefficient

\[
 c_{k,R}:=\int_{\mathbb R^3}\psi_k^R(y)
                  \cos(q_+\cdot y)\,dy.
 \tag{S.427}
\]

Radial symmetry gives the same coefficient at \(q_-=(2,-2,0)\), while all
sine coefficients vanish.  Unfolding the periodization in (S.424) and
using (S.426) therefore gives the exact formula

\[
 \boxed{
 J_{k,R}(\xi)={m_{k,R}\over2}
       +c_{k,R}\left(|W(\xi)|^2-{1\over2}\right),
 \qquad
 \nabla J_{k,R}=c_{k,R}\nabla|W|^2.}
 \tag{S.428}
\]

Now fix an arbitrary deletion budget \(N\ge0\) and put \(M=N+1\).  The
inherited cutoff has

\[
 \operatorname {supp}\psi_k^R
 \subset\{|y|\le(2^{k+1}+1/8)R\}.
\]

Choose \(R\) so small that

\[
 \boxed{
 0<R<\min\left\{{\pi\over16},
 {\pi\over6\sqrt2(2^{M+1}+1/8)}\right\},
 \qquad \mu_R\ge{1\over2},
 \qquad \overline I_{8R}\Subset(0,T).}
 \tag{S.429}
\]

For \(1\le k\le M\) and \(y\in\operatorname {supp}\psi_k^R\), this gives
\(|q_+\cdot y|\le\pi/3\).  Since \(\psi_k^R\ge0\) and is not zero,

\[
 \boxed{
 c_{k,R}\ge{1\over2}m_{k,R}>0,
 \qquad 1\le k\le M.}
 \tag{S.430}
\]

These are \(N+1\) distinct physical annuli in the moving spatial frame.
No Fourier-shell index is substituted for the project shell label.

Along the invariant line \(\xi_2=0\), one has

\[
 W(\xi)\cdot\nabla|W(\xi)|^2
 =\sin\xi_1\sin2\xi_1.
 \tag{S.431}
\]

Choose a fixed \(\delta>0\) so small that

\[
 {e^{2\delta}-1\over2}
 <\log{\tan(\pi/8)\over\tan(\pi/16)}.
\]

For \(A\ge1\) and \(t_0-\delta/A\le t<t_0\), equation (S.423) and

\[
 \int_t^{t_0}b_A(s)\,ds
 ={A\over2}\left(e^{2(t_0-t)}-1\right)
 \le{e^{2\delta}-1\over2}
\]

give \(\pi/8\le\xi_1(t)\le\pi/4\).  After increasing \(A\) so that
\(\delta/A<R^2\), the same interval lies in \(I_R\), where \(\eta_R=1\).
Consequently, with

\[
 g_0:=\sin(\pi/8)\sin(\pi/4)>0,
\]

equations (S.425), (S.428), and (S.430) yield

\[
 \boxed{
 |\dot F_{k,R}(t)|=\dot F_{k,R}(t)
 \ge {\gamma_k\mu_Rc_{k,R}g_0\over2R}A^3,
 \quad
 1\le k\le M,
 \quad t_0-\delta/A\le t<t_0.}
 \tag{S.432}
\]

## 5. Failure of every \(p>1\) common-deletion tail

Retain the Step 13 dimensionless density

\[
 h_{k,R}(\sigma)=R^2
 |\dot F_{k,R}(s_R+R^2\sigma)|,
 \qquad 0<\sigma<4.
\]

The interval in (S.432) has dimensionless length
\(\delta/(AR^2)\).  Thus, for \(1<p<\infty\),

\[
 \boxed{
 \|h_{k,R}\|_{L^p(0,4)}
 \ge {\gamma_k\mu_Rc_{k,R}g_0\over2}
       \delta^{1/p}R^{\,1-2/p}A^{\,3-1/p},
 \qquad 1\le k\le M.}
 \tag{S.433}
\]

For \(p=\infty\), the corresponding lower bound is

\[
 \boxed{
 \|h_{k,R}\|_{L^\infty(0,4)}
 \ge {\gamma_k\mu_Rc_{k,R}g_0R\over2}A^3.}
 \tag{S.434}
\]

Deleting at most \(N=M-1\) shell indices leaves at least one of
\(1,\ldots,M\).  Hence, with \(1/p=0\) when \(p=\infty\),

\[
 \boxed{
 \mathfrak H^F_{p,N,R}
 \ge c_{p,N,R}A^{\,3-1/p},
 \qquad p\in(1,\infty],}
 \tag{S.435}
\]

where \(c_{p,N,R}>0\) is independent of \(A\).

It remains to compare this with the complete payment, not with one selected
row.  On \(\overline I_{8R}\),

\[
 b_A(t)\le Ae^{128R^2}.
\]

Translations by the trajectory change no pointwise amplitude.  Therefore
\(|v_R|+|\nabla v_R|\le C_RA\) and \(|\pi_R|\le C_RA^2\), uniformly over
the \(A\)-dependent phase \(\xi(t)\in\mathbb T^3\).  The local-pressure
split and its gauge form a uniformly bounded family of translated,
\(R\)-dependent profiles, multiplied by \(b_A^2\).  The standard
Calderón--Zygmund and all-copy estimates in the frozen payment give,
row by row,

\[
 \mathcal E^{M,R}(z_0,8R)\le C_RA^2,\qquad
 \mathcal G_{v_R,\pi_R}^{M,R}(z_0,2R;1)\le C_RA^3,
\]

\[
 \Lambda_{2R}^{M,R}(t)\le C_RA^2,\qquad
 \mathcal H_{v_R}^{M,R}(z_0,2R)\le C_RA^3.
\]

The exterior \(\mathcal G\) all-copy sums converge by the frozen
super-Gaussian shell weights, while the harmonic \(\mathcal H\) row uses
its frozen algebraic order-\(-4\) kernel.
Thus every nonnegative row in (3.10), including the fixed pressure gauge,
is included and

\[
 \boxed{P_R^M\le C_RA^3.}
 \tag{S.436}
\]

Combining (S.435)--(S.436) gives

\[
 {\mathfrak H^F_{p,N,R}\over(P_R^M)^{2/3}}
 \ge c'_{p,N,R}A^{\,1-1/p}\longrightarrow\infty
 \qquad(A\to\infty).
 \tag{S.437}
\]

This proves the exact quantifier negation of (S.342):

\[
 \boxed{
 \begin{gathered}
 \text{For every }p\in(1,\infty],\ N\in\mathbb N_0,\ C>0,\\
 \text{there are an admissible }R,z_0\text{ and a smooth periodic unforced solution}\\
 \text{for which }\mathfrak H^F_{p,N,R}>C(P_R^M)^{2/3}.
 \end{gathered}}
 \tag{S.438}
\]

The same calculation gives a sharper exponent boundary.  If a universal
estimate of the form

\[
 \mathfrak H^F_{p,N,R}\le C(P_R^M)^\beta
\]

were to hold for some fixed \(p\in[1,\infty]\) and \(\beta\ge0\), then
(S.435)--(S.436) would force

\[
 \boxed{\beta\ge1-{1\over3p}.}
 \tag{S.438a}
\]

Here \(1/\infty=0\), and more explicitly the family gives
\(\mathfrak H^F_{p,N,R}/(P_R^M)^\beta
\gtrsim_{p,N,R}A^{3-1/p-3\beta}\).
Thus \(2/3\) is exactly the amplitude-compatible power at \(p=1\), while
every \(p>1\) requires a strictly larger payment power for a bound without
additional factors.  More generally, for \(\alpha,\beta\ge0\), a
positive-window estimate

\[
 \int_I h_{k,R}\le C(P_R^M)^\beta |I|^\alpha
\]

tested on the same dimensionless \(\sigma\)-terminal block, where
\(|I|\asymp_R A^{-1}\) and \(\int_Ih_{k,R}\asymp_R A^2\), requires

\[
 \boxed{3\beta-\alpha\ge2.}
 \tag{S.438b}
\]

In particular, the quadratic payment power \(\beta=2/3\) permits no
positive time anti-concentration exponent \(\alpha>0\) in the bare class.

## 6. Fixed-\((N,R)\) amplitude saturation at the critical \(L_t^1\) scale

The same exact path explains why the endpoint \(p=1\) is different.  For
all \(k\), formula (S.428) remains valid, with
\(|c_{k,R}|\le m_{k,R}\).  Since \(0<\xi_1\le\pi/4\), the change of variable

\[
 d\xi_1=\mu_Rb_A\sin\xi_1\,dt
\]

in (S.425) gives

\[
 \int_{s_R}^{t_0}|\dot F_{k,R}(t)|\,dt
 \le {\gamma_k|c_{k,R}|\over R}
       \sup_{I_{2R}}b_A^2
       \int_0^{\pi/4}\sin x\cos x\,dx
 \le C_R\gamma_km_{k,R}A^2.
 \tag{S.439}
\]

Here \([s_R,t_0)=\mathcal T_R=I_{2R}\), \(0\le\eta_R\le1\), and the
factor \(\mu_R\) cancels exactly in the change of variables.

Because \(m_{k,R}\le C2^{3k}R^3\) and
\(\sum_k2^{3k}\gamma_k<\infty\), summing (S.439) gives

\[
 \mathfrak H^F_{1,N,R}\le C_RA^2.
 \tag{S.440}
\]

The terminal lower bound (S.432), now integrated over \(\delta/A\), and the
same pigeonhole among \(N+1\) shells give the reverse bound

\[
 \mathfrak H^F_{1,N,R}\ge c_{N,R}A^2.
 \tag{S.441}
\]

Take local-energy good times increasing to \(t_0\).  Then
\(v_R(t,y)\to AW(y+x_*)\), and
\(\int_{B_{8R}}|W(y+x_*)|^2\,dy>0\).  Hence the essential supremum over the
open interval \(I_{8R}\), through the endpoint part of the buffered local
energy, gives

\[
 P_R^M\ge c_RA^3.
 \tag{S.442}
\]

Together with (S.436),

\[
 \boxed{
 \mathfrak H^F_{1,N,R}\asymp_{N,R}A^2,
 \qquad
 P_R^M\asymp_RA^3,
 \qquad
 \mathfrak H^F_{1,N,R}\asymp_{N,R}(P_R^M)^{2/3}.}
 \tag{S.443}
\]

Thus the smooth family rules out the quadratic \(P^{2/3}\) tail for every
\(p>1\), but it does not rule out the critical candidate

\[
 \boxed{
 \begin{gathered}
 \exists\,N_1\in\mathbb N_0,\ C>0\ \text{universal such that}\\
 \forall\text{ admissible Version-M solutions, }R,z_0
 \text{ and terminal settings},\qquad
 \mathfrak H^F_{1,N_1,R}\le C(P_R^M)^{2/3}.
 \end{gathered}}
 \tag{S.444}
\]

Equation (S.444) is **OPEN**.  Step 15 (S.386)--(S.387) already includes
\(p=1\).  Repeating the implication (S.389)--(S.391) with (S.444) as its
antecedent and \(4^{1-1/p}=1\) would still pay the complete hybrid residual
with one fixed-across-time deletion set.  This is the critical endpoint
inside the global common-deletion temporal-tail ansatz, not a claim that it
is the weakest possible terminal route.  The \(p>1\) time-window gain from
Step 13 must not be used here.

## 7. Independent exact-family screen

The mechanism is not tied to one accidental identity.  The equal-parameter
\(A_{\rm ABC}=B_{\rm ABC}=C_{\rm ABC}=1\) ABC field

\[
 U=(\sin x_3+\cos x_2,\ \sin x_1+\cos x_3,\
       \sin x_2+\cos x_1)
\]

obeys \(\nabla\times U=U,\ \Delta U=-U\).  Thus, with
\(b_A(t)=Ae^{-(t-t_0)}\), the field \(u=b_AU\) and the mean-zero pressure
\(-b_A^2(|U|^2-3)/2\) form another exact smooth periodic solution.  At the
phase \(\xi_*=0\),

\[
 U(0)\cdot\nabla|U|^2(0)=6.
\]

The velocity mollifier has one positive radial multiplier at frequency
one, while the nonconstant modes of \(|U|^2\) have frequency length
\(\sqrt2\).  Radiality gives
\(J_{k,R}(\xi)=3m_{k,R}+c_{k,R}(|U(\xi)|^2-3)\).  Small \(R\) makes
\(c_{k,R}>0\) on the first \(N+1\) shells.  Continuity of the terminal
trajectory on a block of length \(O(A^{-1})\), together with the displayed
directional derivative, then reproduces the \(A^{3-1/p}\) obstruction.
This is a corroborating verification sketch, not a second theorem needed
for Taylor's proof.  For classical ABC context, see Dombre et al.,
[*Chaotic streamlines in the ABC flows*](https://doi.org/10.1017/S0022112086002859)
(1986).

## 8. Primary-source boundary

The exact field in (S.417) is Taylor's 1923 bi-periodic decaying vortex,
often called the two-dimensional Taylor--Green vortex in modern numerical
work; it is not the fully three-dimensional datum studied by Taylor and
Green in 1937.  Relevant historical sources are Taylor's
[*On the decay of vortices in a viscous fluid*](https://doi.org/10.1080/14786442308634295)
(1923) and Taylor--Green's
[*Mechanism of the production of small eddies from large ones*](https://doi.org/10.1098/rspa.1937.0036)
(1937).  Modern exact-flow context includes Chai--Wu--Fang,
[*Single-scale two-dimensional-three-component generalized-Beltrami-flow
solutions of incompressible Navier--Stokes equations*](https://doi.org/10.1016/j.physleta.2020.126857),
and Antuono,
[*Tri-periodic fully three-dimensional analytic solutions for the
Navier--Stokes equations*](https://doi.org/10.1017/jfm.2020.126) (2020).
The exact field, generalized-Beltrami mechanism, and exponential decay are
not novelty claims.

A bounded collision search did not locate a theorem or counterexample with
the project-specific combination of a terminal mollified trajectory,
periodized physical annuli, one fixed shell deletion before the time norm,
and the payment \(P_R^M\).  That search boundary is not a priority claim.
The conclusion (S.438) rests on the displayed direct substitution, not on
absence from the literature.

## 9. Claim ledger and route correction

The following are **PROVED** in the frozen Version-M setting:

- the exact smooth NSE identities (S.417)--(S.420);
- the radial mollifier and terminal-path formulas (S.421)--(S.423);
- the exact Bernoulli cancellation and moving-drift identity
  (S.424)--(S.425);
- simultaneous positivity on arbitrary \(N+1\) physical shells
  (S.426)--(S.432);
- the temporal-tail lower bounds and complete-payment upper bound
  (S.433)--(S.437);
- the quantifier-level disproof of (S.342), (S.438); and
- fixed-\((N,R)\) critical \(L_t^1\) amplitude saturation,
  (S.439)--(S.443).

The following is **OPEN**:

- the natural critical estimate (S.444), which remains sufficient by
  Step 15.

The following remain **OPEN AND UNCHANGED**:

- the direct hybrid terminal-flux gate, the selected-crown estimate
  (S.407), (S.375), (S.288), (S.303), (S.272), Step 10 (S.243), Q.12,
  Q.1, scale contraction, and regularity.

The route decision is now strict.  No proof attempt may assume (S.342),
because it is false even for smooth exact solutions.  The next short-flux
task is to decompose the critical \(L_t^1\) tail in (S.444), keeping signed
moving-drift cancellation and the common deletion set.  In parallel, the
terminal-crown route remains available through the separate open
coercivity estimate (S.407).
