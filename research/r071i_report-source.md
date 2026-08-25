# R0.71I — Joint parabolic damping reduces weighted BV to one-sided creation, while a smooth zero-entry 2D3C pulse preserves the two-power volume gap

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, projected Lamb vectors, Littlewood--Paley transfer,
localized time--frequency occupation, and temporal variation

**Status:** formal release source.  The report proves exact identities on
classical-solution intervals, a deterministic BV reduction, a soft-denominator
ledger, an exact common-heat obstruction, and a global-smooth fixed-energy
2D3C zero-entry pressure test for one declared smooth radial two-ring
multiplier.  It proves no Leray-level weighted-BV bound, continuation theorem,
global regularity result, singularity construction, novelty claim, or
Millennium-problem claim.

## 1. Direct decision

R0.71H isolated the joint amplitude--direction mismatch but left open whether
its viscous and source pieces could cancel strongly enough to recover the two
frequency powers missing from the direct estimate.  R0.71I gives a sharper
answer.

Let

\[
 L=\mathbb P(u\times\omega)=u_t-\nu\Delta u,
 \qquad F=A L,
 \qquad C=\nabla\times(\chi A\omega),
 \tag{1.1}
\]

where \(A=e^{s\Delta}T_j\), and put

\[
 Y=\|\omega\|_2^2,
 \quad \rho=\|C\|_2,
 \quad d=\rho^2,
 \quad B=\langle F,C\rangle,
 \quad E=C/\rho,
 \quad P=I-E\otimes E.
 \tag{1.2}
\]

For the nominal parabolic rate \(\lambda=\nu K^2\), define the complete
remainders

\[
 N=F_t+\lambda F,
 \qquad M=C_t+\lambda C.
 \tag{1.3}
\]

On a component of \(\{\rho>0\}\), set

\[
 x=F/\sqrt Y,
 \qquad \beta=\langle F,E\rangle=B/\rho,
 \qquad q=(\beta^+)^2=(B^+)^2/d,
 \qquad z=\langle x,E\rangle,
 \qquad a=q/Y=(z^+)^2,
 \tag{1.4}
\]

and

\[
 \boxed{
 \mathcal J=
 \left\langle\frac N{\sqrt Y},E\right\rangle
 +\frac{\langle Px,PM\rangle}{\rho}
 -\frac{Y_t}{2Y}z.}
 \tag{1.5}
\]

Then the scalar evolution is exactly

\[
 \boxed{
 z_t+\lambda z=\mathcal J,
 \qquad
 a_t+2\lambda a=2z^+\mathcal J.}
 \tag{1.6}
\]

This yields the strongest positive reduction currently available:

\[
 \boxed{
 \operatorname{TV}_I(a)+a(T_-)+a(T_+)
 \le 2a(T_-)+4\int_I z^+\mathcal J^+\,dt.}
 \tag{1.7}
\]

Thus the terminal trace is not an independent burden.  The unresolved rows
are the initial trace, positive joint creation, denominator components,
soft-limit faces, and partition refresh atoms.

The identity does not close the estimate.  A two-mode common-heat path with
zero entry and exit faces has

\[
 \frac{K^{-2}\operatorname{TV}(a)}
 {\displaystyle\int K^{-2}\|F\|_2^2/Y\,dt}
 =\frac{\nu(71-17\sqrt{17})}{3}K^2.
 \tag{1.8}
\]

That path is not by itself an NSE \((F,C)\) pair.  A stronger construction
is.  A fixed-energy, global-smooth 2D3C solution, with \(\chi=1\), strictly
positive denominator, zero entry coefficient, and one fixed smooth radial
two-ring multiplier, creates an \(O(1)\) interior value of \(a\) on a viscous
time window.  Its outer-weighted variation and one-sided creation are
\(\gtrsim K^{-2}\), while the R0.71F physical-time heat volume is
\(O(K^{-4})\).  Their ratio again grows like \(K^2\).

The release decision is therefore:

1. **retain** the joint identity and the one-sided unsquared creation term;
2. **stop** direct residual-square and heat-volume-only closure;
3. **do not** infer failure of the full face-paid weighted-BV target;
4. test next whether the complete all-shell sum of positive joint creation
   has a genuinely new NSE cancellation not reducible to the R0.71F volume.

## 2. Classical setup and complete source ledger

Work on the normalized periodic torus.  Let \(u\) be a zero-mean classical
solution on a compact interval \(I\):

\[
 u_t+u\cdot\nabla u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
 \qquad \omega=\nabla\times u.
 \tag{2.1}
\]

For example,

\[
 u\in C(I;H^5)\cap C^1(I;H^3)
 \tag{2.2}
\]

is more than sufficient for the displayed differentiations.  No minimal
regularity assertion is made.  Passing to Leray--Hopf solutions would require
finite-shell and space--time regularization followed by estimates uniform in
every limiting parameter; those estimates are part of the open problem.

Let \(S_k=T_k^*T_k\) be a tight shell resolution and write

\[
 u_k=S_ku,
 \qquad \omega_k=S_k\omega,
 \qquad L_k=S_kL.
 \tag{2.3}
\]

For every ordered pair \((k,\ell)\), define

\[
 \begin{aligned}
 \mathfrak H_{k\ell}={}&
 -A\mathbb P((L_k\cdot\nabla)u_\ell)
 -A\mathbb P((u_k\cdot\nabla)L_\ell)\\
 &+2\nu\sum_mA\mathbb P
 ((\partial_m u_k\cdot\nabla)\partial_m u_\ell),\\
 \mathfrak G_{k\ell}={}&A\bigl(
 (\omega_k\cdot\nabla)u_\ell
 -(u_k\cdot\nabla)\omega_\ell\bigr).
 \end{aligned}
 \tag{2.4}
\]

Finite truncation followed by the smooth limit gives

\[
 \boxed{
 F_t=\nu\Delta F+\sum_{k,\ell}\mathfrak H_{k\ell}.}
 \tag{2.5}
\]

No low--high, high--low, comparable, or high--high-to-low pair has been
discarded.

For a mollified transport velocity \(V_r\), put

\[
 R=(\partial_t+V_r\cdot\nabla)\chi,
 \qquad
 \mathcal K_\chi W
 =2\sum_m(\partial_m\chi)\partial_mW+(\Delta\chi)W,
 \qquad W=A\omega.
 \tag{2.6}
\]

The exact Eulerian localized-vorticity ledger is

\[
 \begin{aligned}
 C_t={}&\nu\Delta C
 +\nabla\times\left(\chi\sum_{k,\ell}\mathfrak G_{k\ell}\right)\\
 &+\nabla\times\bigl((R-V_r\cdot\nabla\chi)W\bigr)
 -\nu\nabla\times(\mathcal K_\chi W).
 \end{aligned}
 \tag{2.7}
\]

Write the three non-heat rows as \(G\), so that

\[
 C_t=\nu\Delta C+G.
 \tag{2.8}
\]

A transported cutoff with \(R=0\) still has
\(\chi_t=-V_r\cdot\nabla\chi\) in this Eulerian formula, and the viscous
collar remains.  Consequently

\[
 \boxed{
 \begin{aligned}
 N&=\nu(\Delta+K^2)F+\sum_{k,\ell}\mathfrak H_{k\ell},\\
 M&=\nu(\Delta+K^2)C+G.
 \end{aligned}}
 \tag{2.9}
\]

Equation (1.5) uses these complete quantities, not a same-shell surrogate.

## 3. Exact hard-denominator joint identities

Assume \(Y>0\) and \(\rho>0\) on one open interval.  Define

\[
 \beta=\langle F,E\rangle,
 \quad q=(\beta^+)^2,
 \quad y=Y_t/Y,
 \tag{3.1}
\]

and

\[
 S=\langle N,E\rangle+\rho^{-1}\langle PF,PM\rangle.
 \tag{3.2}
\]

Because \(P C=0\),

\[
 PM=P(C_t+\lambda C)=PC_t,
 \qquad
 E_t=\frac{PM}{\rho}.
 \tag{3.3}
\]

The radial component of \(C_t\) cancels.  Direct differentiation gives

\[
 \boxed{
 \beta_t+\lambda\beta=S,
 \qquad
 q_t+2\lambda q=2\beta^+S.}
 \tag{3.4}
\]

After division by \(Y\),

\[
 \boxed{
 a_t+(2\lambda+y)a=\frac{2\beta^+S}{Y}.}
 \tag{3.5}
\]

Since \(z=\beta/\sqrt Y\), equations (1.5)--(1.6) follow.  The
\(Y_t/Y\) row has not disappeared: it is kept inside the signed source
\(\mathcal J\) before its positive part is taken.  If it is separated, then

\[
 z^+\mathcal J^+
 \le z^+\left(\frac S{\sqrt Y}\right)^+
 +\frac12a\,y^-.
 \tag{3.6}
\]

Thus a proof that splits the normalization must pay the negative logarithmic
enstrophy derivative independently.

### 3.1 Amplitude-vector Pythagorean identity

Set

\[
 \Xi=z^+E=\sqrt a\,E.
 \tag{3.7}
\]

The function \(r\mapsto r^+\) is differentiable almost everywhere.  On the
positive branch, radial and tangent derivatives are orthogonal, and hence

\[
 \boxed{
 \Xi_t+\lambda\Xi
 =\mathbf1_{\{z>0\}}\mathcal J E
 +z^+\frac{PM}{\rho},}
 \tag{3.8}
\]

\[
 \boxed{
 \|\Xi_t+\lambda\Xi\|_2^2
 =\mathbf1_{\{z>0\}}\mathcal J^2
 +a\frac{\|PM\|_2^2}{d}.}
 \tag{3.9}
\]

An equivalent unnormalized form retains \(S\) and \(y\) separately:

\[
 \left\|\Xi_t+\left(\lambda+\frac y2\right)\Xi\right\|_2^2
 =\mathbf1_{\{\beta>0\}}\frac{S^2}{Y}
 +a\frac{\|PM\|_2^2}{d}.
 \tag{3.10}
\]

These identities show exactly what joint cancellation achieves.  The nominal
term \(\lambda C\) is radial and therefore does not rotate \(E\); only the
complete projected mismatch \(PM=PC_t\) appears in the tangent row.

### 3.2 Why the square route still loses two powers

Young's inequality in (1.6) gives

\[
 2z^+\mathcal J
 \le \lambda a+\frac{\mathcal J^2}{\lambda},
 \qquad
 a_t+\lambda a\le\frac{\mathcal J^2}{\lambda}.
 \tag{3.11}
\]

After the outer \(K^{-2}\) weight, the right side costs

\[
 \frac{\mathcal J^2}{\nu K^4}.
 \tag{3.12}
\]

To pay it by \(K^{-2}\|F\|_2^2/Y=K^{-2}\|x\|_2^2\), one would need the
schematic depletion

\[
 |\mathcal J|^2\lesssim\nu^2K^2\|x\|_2^2.
 \tag{3.13}
\]

A fixed-relative-width annulus only gives

\[
 \|(\Delta+K^2)P_Kf\|_2=O(K^2\|P_Kf\|_2),
 \tag{3.14}
\]

not \(O(K\|P_Kf\|_2)\).  The generic joint mismatch therefore has the
nominal size \(O(\nu K^2\|x\|_2)\), leaving two frequency powers missing.

## 4. Deterministic one-sided BV reduction

For every nonnegative absolutely continuous scalar \(a\) on
\([T_-,T_+]\),

\[
 \operatorname{TV}(a)
 =2\int_{T_-}^{T_+}(a_t)^+dt+a(T_-)-a(T_+).
 \tag{4.1}
\]

Consequently

\[
 \operatorname{TV}(a)+a(T_-)+a(T_+)
 =2a(T_-)+2\int_{T_-}^{T_+}(a_t)^+dt.
 \tag{4.2}
\]

Equation (1.6) implies

\[
 (a_t)^+\le2z^+\mathcal J^+,
 \tag{4.3}
\]

which proves (1.7).  This is a deterministic identity-plus-inequality; it
does not use NSE energy estimates.

For a finite shell--cell family with no refresh inside the observation
interval, summing connected positive-denominator components gives

\[
 \begin{aligned}
 &\sum_{j,Q}K_j^{-2}
 \left[\operatorname{TV}(a_{j,Q})
 +\text{all denominator faces}\right]\\
 &\qquad\le
 2\sum_{j,Q}K_j^{-2}\text{entry}_{j,Q}
 +4\sum_{j,Q}K_j^{-2}
 \int z_{j,Q}^+\mathcal J_{j,Q}^+dt.
 \end{aligned}
 \tag{4.4}
\]

The phrase “all denominator faces” includes both one-sided values at every
component endpoint.  Algebraic cancellation of distributional signed jumps
does not cancel absolute variation.

Here the right-side entry means the sum of the left traces over **every**
connected component of \(\{d>0\}\), not only the observation-interval trace.
If a one-sided trace is unavailable, the safe convention is its limsup; an
infinite limsup leaves the ledger infinite rather than deleting that face.
For a refresh jump \(\Delta a\), the exact positive-variation extension adds
\(2(\Delta a)^+\), which is safely bounded by \(2|\Delta a|\).

### 4.1 What can be paid at one chosen smooth initial time

At a fixed smooth start, bounded spatial overlap and annular comparison give

\[
 \sum_{j,Q}K_j^{-2}a_{j,Q}(T_-)
 \lesssim
 \frac1Y\sum_jK_j^{-2}\|F_j\|_2^2
 \lesssim
 \frac{\|(-\Delta)^{-1/2}L\|_2^2}{Y}.
 \tag{4.5}
\]

By \(H^1\hookrightarrow L^6\), Hölder, and interpolation,

\[
 \|L\|_{H^{-1}}
 \lesssim\|u\times\omega\|_{6/5}
 \lesssim\|u\|_3\|\omega\|_2
 \lesssim\|u\|_2^{1/2}Y^{3/4},
 \tag{4.6}
\]

so

\[
 \boxed{
 \sum_{j,Q}K_j^{-2}a_{j,Q}(T_-)
 \lesssim\|u(T_-)\|_2Y(T_-)^{1/2}.}
 \tag{4.7}
\]

This proves finiteness at one classical start.  It does not pay later
denominator-component entries, refresh faces, or a limit approaching a
putative singular time; it is not the R0.71F local heat volume.

## 5. Soft denominator and face ledger

For \(\varepsilon>0\), define

\[
 R_\varepsilon=\sqrt{d+\varepsilon},
 \quad E_\varepsilon=C/R_\varepsilon,
 \quad P_\varepsilon=I-E_\varepsilon\otimes E_\varepsilon,
 \quad \theta_\varepsilon=\frac{\varepsilon}{d+\varepsilon}.
 \tag{5.1}
\]

Unlike \(E\), the vector \(E_\varepsilon\) is not unit.  Direct
differentiation gives the global identity

\[
 \boxed{
 (E_\varepsilon)_t
 +\lambda\theta_\varepsilon E_\varepsilon
 =R_\varepsilon^{-1}P_\varepsilon M.}
 \tag{5.2}
\]

With

\[
 \beta_\varepsilon=\langle F,E_\varepsilon\rangle,
 \qquad
 S_\varepsilon=\langle N,E_\varepsilon\rangle
 +R_\varepsilon^{-1}\langle F,P_\varepsilon M\rangle,
 \tag{5.3}
\]

one obtains

\[
 \boxed{
 (\beta_\varepsilon)_t
 +\lambda(1+\theta_\varepsilon)\beta_\varepsilon
 =S_\varepsilon.}
 \tag{5.4}
\]

Put

\[
 z_\varepsilon=\beta_\varepsilon/\sqrt Y,
 \quad a_\varepsilon=(z_\varepsilon^+)^2,
 \quad
 \mathcal J_\varepsilon
 =S_\varepsilon/\sqrt Y-\frac y2z_\varepsilon.
 \tag{5.5}
\]

Then

\[
 \boxed{
 (z_\varepsilon)_t
 +\lambda(1+\theta_\varepsilon)z_\varepsilon
 =\mathcal J_\varepsilon,}
 \tag{5.6}
\]

\[
 \boxed{
 (a_\varepsilon)_t
 +2\lambda(1+\theta_\varepsilon)a_\varepsilon
 =2z_\varepsilon^+\mathcal J_\varepsilon.}
 \tag{5.7}
\]

The extra soft radial damping has a **plus sign on the left-hand side**.  For
fixed \(\varepsilon\), (5.7) is global in time.  If
\(a_\varepsilon\to a\) in \(L^1\), lower semicontinuity of BV records any
concentration at denominator zero faces.  Establishing the uniform bound
needed for that passage is still open.

At a partition refresh, \(a_Q\) has a nonlinear jump.  The refresh delta
must be recorded as a separate BV atom.  It is invalid to insert a
distributional delta into \(M\) and multiply it inside \(S\) or
\(\mathcal J\).

## 6. Common-heat zero-face obstruction

Let \(e_1,e_2\) be orthonormal and let a positive self-adjoint operator
\(A_K\) satisfy

\[
 A_Ke_1=K^2e_1,
 \qquad A_Ke_2=2K^2e_2.
 \tag{6.1}
\]

Take

\[
 F(0)=\frac{e_1-e_2}{\sqrt2},
 \qquad C(0)=\frac{e_1+e_2}{\sqrt2},
 \qquad Y\equiv1,
 \tag{6.2}
\]

and evolve both paths by \(v_t=-\nu A_Kv\).  With

\[
 \tau=\nu K^2t,
 \qquad x=e^{-2\tau},
 \tag{6.3}
\]

the normalized coefficient is exactly

\[
 \boxed{
 a(\tau)=\frac{x(1-x)^2}{2(1+x)}.}
 \tag{6.4}
\]

It starts at zero and tends to zero.  Its unique interior maximum occurs at

\[
 x_*=\frac{\sqrt{17}-3}{4},
 \qquad
 a_*=\frac{71-17\sqrt{17}}{16},
 \tag{6.5}
\]

so

\[
 \operatorname{TV}_{[0,\infty)}(a)=2a_*.
 \tag{6.6}
\]

The physical-time weighted heat volume is

\[
 \int_0^\infty K^{-2}\|F(t)\|_2^2dt
 =\frac{3}{8\nu K^4},
 \tag{6.7}
\]

whereas the weighted variation is \(2a_*K^{-2}\).  Their ratio is (1.8).

The joint source is positive throughout the interior:

\[
 \frac{\mathcal J}{\nu K^2}
 =\frac{x^{3/2}(x+3)}{\sqrt2(1+x)^{3/2}}>0,
 \tag{6.8}
\]

and its exact square cost is

\[
 \int_0^\infty\frac{\mathcal J^2}{\nu K^2}dt
 =\frac34(1-\log2).
 \tag{6.9}
\]

The two outer **amplitude** faces are zero (the denominator is not zero), so
the two-power gap is not merely an entry-trace artifact.  The boundary is
equally important: \(Y\equiv1\) is imposed,
and this abstract common-heat pair is not shown to equal the NSE quantities
in (1.1).  It is a heat-geometry obstruction, not an NSE counterexample.

## 7. Global-smooth 2D3C zero-entry pressure test

The heat obstruction can be realized at leading order inside an exact NSE
family.

### 7.1 Datum and fixed radial multiplier

At frequency scale \(K\), prescribe the horizontal shear modes

\[
 \widehat u_2(\pm K,0)=1.
 \tag{7.1}
\]

Prescribe the vertical driver modes, with conjugates,

\[
 \widehat u_3(0,2K)=\frac i2,
 \qquad
 \widehat u_3(0,3K)=-\frac i3.
 \tag{7.2}
\]

For every \(\sigma,\tau\in\{-1,1\}\), prescribe the eight target modes

\[
 \widehat u_3(\sigma K,\tau2K)=\frac15,
 \qquad
 \widehat u_3(\sigma K,\tau3K)=\frac1{10}.
 \tag{7.3}
\]

All other initial coefficients vanish.  The datum is real, zero mean,
divergence free, independent of \(x_3\), and of 2D3C form.  Its horizontal
shear solves heat, while its vertical component solves a linear passive
advection--diffusion equation.  Hence the corresponding three-dimensional
NSE solution is global and smooth for every \(K\).

Choose one fixed real-even radial symbol \(m_{\rm rad}\in C_c^\infty\) that
equals one near \(\sqrt5\) and \(\sqrt{10}\), and whose support lies in

\[
 |r^2-5|<\eta
 \quad\hbox{or}\quad
 |r^2-10|<\eta,
 \qquad0<\eta<\frac12.
 \tag{7.4}
\]

Let \(T_K=m_{\rm rad}(|D|/K)\) and take \(\chi=1\).  In the sideband
chains \((rK,nK,0)\), \(n=2,3\), the support retains exactly \(r=\pm1\).
It is a fixed smooth radial compact-annular template, not a
\(K\)-dependent finite selector.

### 7.2 Exact initial Fourier ledger

Normalized-Haar Parseval gives

\[
 \boxed{
 \|u_0\|_2^2=\frac{263}{90},
 \qquad
 Y(0)=\frac{36}{5}K^2.}
 \tag{7.5}
\]

On each of the four \(|n|=2\) target modes,

\[
 (\widehat u_3,\widehat F_3,\widehat C_3)
 =\left(\frac15,K,K^2\right),
 \tag{7.6}
\]

and on each of the four \(|n|=3\) target modes,

\[
 (\widehat u_3,\widehat F_3,\widehat C_3)
 =\left(\frac1{10},-K,K^2\right).
 \tag{7.7}
\]

Therefore

\[
 \boxed{
 \|F_K(0)\|_2^2=8K^2,
 \quad d_K(0)=8K^4,
 \quad B_K(0)=0,
 \quad a_K(0)=0.}
 \tag{7.8}
\]

The denominator is strict while the entry amplitude is exactly zero.  The
two independent release auditors reconstruct all eight modes and these five
constants separately.

### 7.3 Fixed-window heat limit

Fix \(\nu>0\), let the admissible integer (or dyadic integer) torus
frequencies \(K\to\infty\), and put \(\theta=\nu K^2t\).  Let
\(c_{m,n}^{(K)}\) denote the rescaled sideband solution with the datum above,
and let \(c_{m,n}^{(0)}\) denote the solution with the same initial sequence
after deleting the \(1/(\nu K)\) coupling.  In channel
\(n\in\{2,3\}\), the vertical
sideband coefficients satisfy, up to the harmless Fourier sign convention,

\[
 c_{m,n}'=-(m^2+n^2)c_{m,n}
 +\frac{in}{\nu K}e^{-\theta}
 (c_{m-1,n}+c_{m+1,n}).
 \tag{7.9}
\]

The shift is bounded on every polynomially weighted \(\ell_s^2\), the
diagonal part generates an analytic contraction semigroup, and the datum has
finite support.  Duhamel's formula and the differentiated equation imply:
for every fixed \(M<\infty\) and finite \(s\),

\[
 \max_{n=2,3}
 \|c_{\cdot,n}^{(K)}-c_{\cdot,n}^{(0)}\|_{C^1([0,M];\ell_s^2)}
 \le\frac{C_{M,s,\nu}}K.
 \tag{7.10}
\]

The constant \(C_{M,s,\nu}\) is independent of the admissible sequence of
frequencies \(K\).

The selected quadratic profiles therefore converge in \(C^1\).  With
\(x=e^{-10\theta}\),

\[
 \frac{q_K}{K^2}\longrightarrow
 Q_0(\theta)=\frac{4x(1-x)^2}{1+x},
 \tag{7.11}
\]

\[
 \frac{Y_K}{K^2}\longrightarrow
 \begin{aligned}[t]
 Y_0(\theta)={}&2e^{-2\theta}+2e^{-8\theta}+2e^{-18\theta}\\
 &+\frac45e^{-10\theta}+\frac25e^{-20\theta},
 \end{aligned}
 \tag{7.12}
\]

\[
 \frac{\|F_K\|_2^2}{K^2}\longrightarrow
 F_0^2(\theta)=4(e^{-10\theta}+e^{-20\theta}).
 \tag{7.13}
\]

Thus

\[
 A_K=\frac{q_K}{Y_K}\longrightarrow A_0=\frac{Q_0}{Y_0},
 \qquad
 \frac{\|F_K\|_2^2}{Y_K}\longrightarrow G_0=\frac{F_0^2}{Y_0}.
 \tag{7.14}
\]

At

\[
 \theta_*=\frac{\log2}{10},
 \tag{7.15}
\]

one has

\[
 Q_0(\theta_*)=\frac13,
 \qquad
 A_*=A_0(\theta_*)
 =\frac{2}{3(1+3\,2^{1/5}+2\,2^{4/5})}>0.
 \tag{7.16}
\]

Since \(A_K(0)=0\), for all sufficiently large \(K\),

\[
 K^{-2}\operatorname{TV}_{[0,\theta_*/(\nu K^2)]}(A_K)
 \ge\frac{A_*}{2K^2}.
 \tag{7.17}
\]

On the other hand,

\[
 \int_0^{\theta_*/(\nu K^2)}
 K^{-2}\frac{\|F_K(t)\|_2^2}{Y_K(t)}dt
 =O_{\nu,\theta_*}(K^{-4}).
 \tag{7.18}
\]

The ratio grows at least like \(c_\nu K^2\).

More directly, integrating (1.6) gives

\[
 2\int_0^{\theta_*/(\nu K^2)}z_K^+\mathcal J_K^+dt
 \ge A_K(\theta_*/(\nu K^2))
 \ge\frac{A_*}{2}.
 \tag{7.19}
\]

After the outer weight, positive joint creation is \(\gtrsim K^{-2}\), not
\(O(K^{-4})\).  This is the precise true-NSE no-go: the R0.71F heat volume
alone cannot pay the one-sided joint source for this fixed smooth radial
two-ring component, even with zero entry, \(d>0\), \(\chi=1\), and no
refresh.

A smooth square-partition completion around the two-ring component is a
plausible construction, but no explicit completed frame and no estimate of
the **total** full-frame right side are part of this release.  No comparison
has been proved with the site's preselected broad standard single-ring dyadic
frame, and no impossibility theorem for every frame is claimed.

## 8. Cutoff motion and refresh are separate costs

This calculation uses a **different** six-mode 2D3C datum from R0.71G--H,
not the eight-target pulse in Section 7.  At unit frequency its three
positive modes are

\[
 \widehat u(1,0,0)=(0,-1,0),\quad
 \widehat u(0,1,0)=(0,0,-1),\quad
 \widehat u(-1,-1,0)=(0,0,-i),
 \tag{8.1}
\]

together with their conjugates.  At frequency \(K\), multiply wave vectors
by \(K\) and Fourier coefficients by \(\alpha K\).  This datum is again
global smooth by the 2D3C reduction.  On its declared low-sphere component,
take the complementary cutoffs

\[
 \chi_{\delta,\pm}(x)=\frac{1\pm\delta\cos(Kx_3)}2,
 \qquad0\le\delta\le1.
 \tag{8.2}
\]

For the amplitude normalization used in that family, exact Fourier
orthogonality gives

\[
 B_{\delta,\pm}=\alpha^3K^6,
 \qquad
 d_{\delta,\pm}=\frac{3\delta^2+4}{4}\alpha^2K^6,
 \tag{8.3}
\]

\[
 a_{\delta,\pm}
 =\frac{\alpha^2K^2}{2(3\delta^2+4)}.
 \tag{8.4}
\]

Hence the aggregate change from \(\delta=0\) to \(\delta=1\) is

\[
 \boxed{
 \Delta_{\rm ref}
 =\sum_\pm|a_{0,\pm}-a_{1,\pm}|
 =\frac{3}{28}\alpha^2K^2.}
 \tag{8.5}
\]

At fixed kinetic amplitude \(U=\alpha K\), this unweighted jump is
\(3U^2/28\); after the target outer weight it is
\(3U^2/(28K^2)\).  Repeated smooth alternation can create variation
proportional to the number of alternations; discrete refreshes create the
same atoms.

This is not an NSE instability.  The cost is supplied by \(\chi_t\), or by
the explicit refresh jump.  A fixed cutoff or an independently controlled
transported partition remains admissible.  Smoothness of \(\chi\) alone is
not a quantitative motion budget.

## 9. Conditional finite-family theorem and open rows

For a finite truncation, (4.4) proves the desired weighted BV if the following
independent quantities are finite uniformly in the regularization:

\[
 \begin{aligned}
 \mathcal Z&=\sum_{j,Q}K_j^{-2}
 \int z_{j,Q}^+\mathcal J_{j,Q}^+dt,\\
 \mathcal F&=\sum_{j,Q}K_j^{-2}
 \bigl(\text{denominator faces}+\text{refresh atoms}\bigr),\\
 \mathcal I&=\sum_{j,Q}K_j^{-2}
 \sum_{J\subset\{d_{j,Q}>0\}}a_{j,Q}(\inf J+).
 \end{aligned}
 \tag{9.1}
\]

The first chosen smooth-time contribution \(\mathcal I\) is finite by
(4.7).  No unconditional Leray estimate has been proved for \(\mathcal Z\),
later component entries, \(\mathcal F\), or the infinite shell--cell and
\(\varepsilon\downarrow0\) limits.

The 2D3C pulse proves that \(\mathcal Z\) cannot be uniformly bounded by the
R0.71F physical-time heat volume alone for the declared multiplier class.
It does not exclude a genuinely different NSE budget, a cancellation visible
only after the full tight-frame sum, or a theorem restricted to another fixed
frame.

Inputs that would make the route conditional include:

1. a Serrin or critical Besov continuation norm;
2. Cheskidov--Dai occupation smallness;
3. a uniform lower bound on every denominator;
4. the target weighted-BV sum itself;
5. a caloric-defect smallness assumption not derived from the Leray budget.

## 10. Reproduction and claim boundary

The exact producer is
`research/r071i_exact_audit.py`.  It uses symbolic arithmetic and direct
finite Fourier convolution.  The independent checker is
`research/r071i_independent_audit.py`; it uses only the Python standard
library, reconstructs the eight target modes without importing the producer,
and separately checks the hard path, soft path, heat integrals, \(K^2\)
scaling, and refresh constants.

The journal figure package records four distinct panels:

1. the abstract common-heat zero-face pulse;
2. its exact \(K^2\) weighted-BV/volume ratio;
3. the \(K\to\infty\), fixed-\(\theta\) 2D3C limiting profiles;
4. the cutoff shape/refresh gap from a separate construction.

There is no DNS, parameter fit, three-dimensional time stepping, GPU run, or
DGX computation in this release.  Closed-form algebra is preferable here
because the question is structural rather than resolution-limited.

The following statements are **not** proved:

- an unconditional weighted-BV estimate;
- an infinite-frame or Leray-level passage;
- failure of every fixed dyadic frame;
- a continuation criterion below known critical hypotheses;
- global smoothness or finite-time singularity for three-dimensional NSE;
- originality, priority, or resolution of the Millennium problem.

The next finite gate is R0.71J: retain the complete \(N\), \(M\),
\(Y_t/Y\), soft-face, and refresh ledger, and test whether the all-shell,
all-cell sum of \(z^+\mathcal J^+\) has an NSE-specific cancellation or
telescoping law that is not a reformulation of the heat volume or a known
continuation hypothesis.  If every candidate estimate reduces to one of the
conditional inputs above, the temporal-residence branch should stop.
