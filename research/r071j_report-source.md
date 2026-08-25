# R0.71J — Positive shellwise creation has a nonnegative all-frame defect, and the existing broad parent frame preserves the two-power heat gap

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, Littlewood--Paley transfer, projected Lamb vectors,
temporal variation, and frequency-localized enstrophy production

**Status:** formal release source.  The report proves an exact all-shell
positive-defect identity on classical-solution intervals, records the only
linear tight-frame telescope available before taking positive parts, and
constructs a fixed-energy global-smooth 2D3C family inside the broad flat-top
parent frame already declared in R0.71E.  For that complete frequency frame,
total one-sided joint creation is at least order \(K^{-2}\), while the total
physical-time heat endpoint is at most order \(K^{-4}\).  The report proves no
matched-spatial-cell theorem, face-paid weighted-BV theorem, Leray-level
continuation criterion, global regularity result, singularity construction,
priority claim, or Millennium-problem claim.

## 1. Direct decision

R0.71I reduced the temporal weighted-BV problem to shellwise entry traces,
faces, and the one-sided joint source

\[
 \sum_{j,Q}K_j^{-2}\int z_{j,Q}^{+}\mathcal J_{j,Q}^{+}\,dt.
 \tag{1.1}
\]

It also constructed a zero-entry pulse for one fixed smooth radial two-ring
multiplier, but it did not complete the calculation over the site's existing
broad frame.  R0.71J closes that frequency-frame gap.

For a finite family of fixed frame/cell indices \(\gamma\), let

\[
 a_{\gamma,t}+2\nu\kappa_\gamma^2a_\gamma
 =2z_\gamma^+\mathcal J_\gamma,
 \qquad w_\gamma=\kappa_\gamma^{-2},
 \tag{1.2}
\]

and put

\[
 \mathcal A_w=\sum_\gamma w_\gamma a_\gamma,
 \qquad
 \mathcal Z_\pm=\sum_\gamma
 w_\gamma z_\gamma^+\mathcal J_\gamma^\pm.
 \tag{1.3}
\]

Then, pointwise almost everywhere between partition refreshes,

\[
 \boxed{
 2\mathcal Z_+
 =\partial_t\mathcal A_w
 +2\nu\sum_\gamma a_\gamma
 +2\mathcal Z_-.}
 \tag{1.4}
\]

This is the universal all-shell identity after taking the positive part.  The
only telescope is the time derivative.  A nonnegative damping mass and a
nonnegative negative-source defect remain.  The soft denominator adds the
further nonnegative row

\[
 2\nu\sum_\gamma\theta_{\varepsilon,\gamma}
 a_{\varepsilon,\gamma}.
 \tag{1.5}
\]

Thus ordinary signed shell transfer cannot cancel (1.1) after the shellwise
positive parts have been taken.

The result is not only algebraic.  Use the smooth log-radius parent frame
declared in R0.71E:

\[
 \sum_{j\in\mathbb Z}m(\log_2|\xi|-j)^2=1,
 \quad
 m=1\ \hbox{on }[0,1/2],
 \quad
 \operatorname{supp}m\subset[-1/2,1].
 \tag{1.6}
\]

For every dyadic integer \(K\), a fixed-energy 2D3C datum is chosen so that
the parent at frequency \(\kappa=4K\) has

\[
 \boxed{
 \|u_0\|_2^2=\frac{2041}{200},\quad
 Y(0)=178K^2,\quad
 \|F_\kappa(0)\|_2^2=500K^2,\quad
 d_\kappa(0)=3942K^4,\quad
 B_\kappa(0)=0.}
 \tag{1.7}
\]

The solution is global and smooth.  On

\[
 I_K=\left[0,\frac{\theta_*}{\nu K^2}\right],
 \qquad \theta_*\equiv\frac{\log2}{18},
 \tag{1.8}
\]

the parent coefficient converges to a strictly positive value

\[
 A_*
 =\frac{4}{
 57(2^{1/9}+44)
 (3\,2^{1/9}+4\,2^{7/9}+120)}
 \approx1.19655\times10^{-5}.
 \tag{1.9}
\]

For all sufficiently large dyadic \(K\), the complete parent-frame sums obey

\[
 \boxed{
 \mathcal Z_K^{\rm frame}
 :=\sum_j2^{-2j}\int_{I_K}z_j^+\mathcal J_j^+dt
 \ge\frac{A_*}{64K^2},}
 \tag{1.10}
\]

\[
 \boxed{
 \mathcal H_K^{\rm frame}
 :=\sum_j2^{-2j}\int_{I_K}
 \frac{\|T_jL\|_2^2}{Y}\,dt
 \le\frac{1-2^{-1/9}}{2\nu K^4}.}
 \tag{1.11}
\]

Consequently

\[
 \boxed{
 \frac{\mathcal Z_K^{\rm frame}}
 {\mathcal H_K^{\rm frame}}
 \ge
 \frac{\nu A_*}{32(1-2^{-1/9})}K^2.}
 \tag{1.12}
\]

This closes two proposed mechanisms:

1. positive joint creation does not acquire a free cancellation merely by
   summing the complete frequency frame;
2. the total physical-time heat endpoint of the same complete broad parent
   frame cannot pay total positive joint creation uniformly.

The construction uses one global cell \(\chi=1\), heat height \(s=0\), and
the parent-only frame (1.6).  It does not cover the later low/high refinement
of that frame, a matched spatial partition, denominator faces, or refresh
atoms.  Those are independent burdens.

## 2. Classical setup and the R0.71I scalar equation

Work on the normalized periodic torus.  Let \(u\) be a zero-mean classical
solution on a compact interval:

\[
 u_t+u\cdot\nabla u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
 \qquad \omega=\nabla\times u.
 \tag{2.1}
\]

For a real-even multiplier \(T_j\), fixed heat height \(s\), and fixed smooth
cutoff \(\chi_Q\), write

\[
 A=e^{s\Delta}T_j,
 \qquad
 L=\mathbb P(u\times\omega)=u_t-\nu\Delta u,
 \qquad
 F=AL,
 \tag{2.2}
\]

\[
 C=\nabla\times(\chi_QA\omega),
 \quad
 Y=\|\omega\|_2^2,
 \quad
 \rho=\|C\|_2,
 \quad
 E=C/\rho,
 \quad
 P=I-E\otimes E.
 \tag{2.3}
\]

For the nominal shell rate \(\lambda=\nu\kappa^2\), define the complete
remainders

\[
 N=F_t+\lambda F,
 \qquad M=C_t+\lambda C.
 \tag{2.4}
\]

On a positive-denominator component, set

\[
 z=\frac{\langle F,E\rangle}{\sqrt Y},
 \qquad
 a=(z^+)^2,
 \tag{2.5}
\]

\[
 \mathcal J=
 \left\langle\frac N{\sqrt Y},E\right\rangle
 +\frac{\langle PF,PM\rangle}{\rho\sqrt Y}
 -\frac{Y_t}{2Y}z.
 \tag{2.6}
\]

R0.71I proved the exact equation

\[
 \boxed{
 z_t+\lambda z=\mathcal J,
 \qquad
 a_t+2\lambda a=2z^+\mathcal J.}
 \tag{2.7}
\]

Every shell pair in \(F_t\), every localized-vorticity row in \(C_t\), the
normalization \(Y_t/Y\), and the nominal mismatch are retained inside
\(\mathcal J\).  R0.71J does not replace (2.6) by a same-shell surrogate.

## 3. Exact all-shell positive-defect theorem

### Theorem 3.1 — no cancellation after shellwise positive parts

Let \(\Gamma\) be a finite fixed family of shell/cell indices on an interval
with no partition refresh.  Assume each hard denominator is positive there,
and let (2.7) hold with shell scale \(\kappa_\gamma\).  With the definitions
in (1.3),

\[
 \boxed{
 2\mathcal Z_+
 =\partial_t\mathcal A_w
 +2\nu\sum_{\gamma\in\Gamma}a_\gamma
 +2\mathcal Z_-.}
 \tag{3.1}
\]

After integration,

\[
 \boxed{
 \int_{T_-}^{T_+}\mathcal Z_+dt
 =\frac{\mathcal A_w(T_+)-\mathcal A_w(T_-)}2
 +\nu\int_{T_-}^{T_+}\sum_\gamma a_\gamma dt
 +\int_{T_-}^{T_+}\mathcal Z_-dt.}
 \tag{3.2}
\]

#### Proof

Write \(\mathcal J=\mathcal J^+-\mathcal J^-\).  For each \(\gamma\),
multiply (2.7) by \(w_\gamma=\kappa_\gamma^{-2}\):

\[
 w_\gamma a_{\gamma,t}+2\nu a_\gamma
 =2w_\gamma z_\gamma^+
 (\mathcal J_\gamma^+-\mathcal J_\gamma^-).
 \tag{3.3}
\]

Move the negative-source term to the right and sum.  This gives (3.1);
integration gives (3.2).  No tight-frame property is used. \(\square\)

The formula is stronger than the observation that the summands in
\(\mathcal Z_+\) are nonnegative.  It identifies the exact defect left after
the only available time telescope.  If the weighted endpoint values agree,
then

\[
 \int\mathcal Z_+dt
 =\nu\int\sum_\gamma a_\gamma dt+\int\mathcal Z_-dt,
 \tag{3.4}
\]

which is strictly positive whenever the amplitude has positive spacetime
mass or the signed source has a negative part.

For the soft direction from R0.71I,

\[
 (a_{\varepsilon,\gamma})_t
 +2\nu\kappa_\gamma^2
 (1+\theta_{\varepsilon,\gamma})a_{\varepsilon,\gamma}
 =2z_{\varepsilon,\gamma}^+
 \mathcal J_{\varepsilon,\gamma},
 \tag{3.5}
\]

the same calculation adds

\[
 2\nu\sum_\gamma
 \theta_{\varepsilon,\gamma}a_{\varepsilon,\gamma}
 \tag{3.6}
\]

to the right side of (3.1).  The soft denominator therefore adds damping; it
does not create a cancellation.

Hard zero-denominator components must still be integrated separately.  Their
one-sided faces remain in the BV ledger.  A refresh creates an explicit jump
atom and is not part of (3.1).  These qualifications do not change the sign
of the interior defect.

## 4. What frame tightness does telescope

Take \(\chi=1\), \(s=0\), and a real-even scalar tight frame
\(\sum_jT_j^*T_j=I\) on mean-zero fields.  Since

\[
 C_j=\nabla\times(T_j\omega)=-\Delta T_ju,
 \tag{4.1}
\]

Parseval gives the raw signed identities

\[
 \boxed{
 \sum_jB_j
 =\langle L,-\Delta u\rangle
 =\frac12Y_t+\nu\|\Delta u\|_2^2,}
 \tag{4.2}
\]

\[
 \sum_jd_j=\|\Delta u\|_2^2,
 \qquad
 \sum_j\|F_j\|_2^2=\|L\|_2^2.
 \tag{4.3}
\]

Thus the raw signed sum is the classical enstrophy-production ledger, not
zero.  It contains the derivative of enstrophy and one more derivative of
dissipation; it is not controlled by the Leray kinetic-energy inequality near
a possible singular time.

For

\[
 q_j=\frac{(B_j^+)^2}{d_j},
 \tag{4.4}
\]

sum only over \(d_j>0\), and assign \(q_j=0\) when \(d_j=0\).  Indeed,
\(d_j=0\) implies \(C_j=0\) and hence \(B_j=0\).  If
\(\sum_jd_j=0\), every term below is zero; otherwise Cauchy gives the
instantaneous sandwich

\[
 \boxed{
 \frac{((\sum_jB_j)^+)^2}{\sum_jd_j}
 \le\sum_jq_j
 \le\sum_j\|F_j\|_2^2.}
 \tag{4.5}
\]

The first inequality follows from
\((\sum_jB_j)^+\le\sum_jB_j^+\); the second is shellwise Cauchy.  The
difference in (4.5) is a nonnegative frame defect.  Differentiating (4.5)
does not preserve an order capable of controlling \(\mathcal Z_+\).

The amplitude-vector identity from R0.71I also sums only nonnegative terms:

\[
 \sum_jw_j\|\Xi_{j,t}+\nu\kappa_j^2\Xi_j\|_2^2
 =\sum_jw_j\mathbf1_{\{z_j>0\}}\mathcal J_j^2
 +\sum_jw_ja_j\frac{\|P_jM_j\|_2^2}{d_j}.
 \tag{4.6}
\]

Neither (4.5) nor (4.6) contains a cross-shell negative term that could pay
the positive source in (3.1).

There is a second distinction at the cell level.  Split one component source
as

\[
 \mathcal J_Q=R_Q+T_Q,
 \tag{4.7}
\]

\[
 R_Q=\left\langle\frac N{\sqrt Y},E_Q\right\rangle
 -\frac{Y_t}{2Y}z_Q,
 \qquad
 T_Q=\langle P_Qx,E_{Q,t}\rangle,
 \qquad x=F/\sqrt Y.
 \tag{4.8}
\]

The radial and tangent rows may cancel inside \(\mathcal J_Q\); taking their
positive parts separately would lose a real cancellation.  If cell supports
\(U_Q\) have overlap at most \(N_0\), then the elementary bounds are

\[
 \sum_Qa_Q\le N_0\frac{\|F\|_2^2}{Y},
 \tag{4.9}
\]

\[
 \sum_Qz_Q^+|R_Q|
 \le N_0\frac{\|F\|_2\|N\|_2}{Y}
 +\frac{N_0|Y_t|}{2Y}\frac{\|F\|_2^2}{Y}.
 \tag{4.10}
\]

The tangent term instead contains

\[
 |T_Q|\le\|\mathbf1_{U_Q}x\|_2\|E_{Q,t}\|_2,
 \qquad
 E_{Q,t}=P_QM_Q/\rho_Q.
 \tag{4.11}
\]

Bounded overlap does not control the angular speed \(\|E_{Q,t}\|\).  A
one-component Hilbert-space path makes the missing denominator explicit.
For \(Y=1\), \(\lambda>0\), take

\[
 F(t)=e^{-\lambda t}\frac{e_1+e_2}{\sqrt2},
 \qquad
 C_\delta(t)=\delta
 (\cos(t/\delta)e_1+\sin(t/\delta)e_2).
 \tag{4.12}
\]

Then \(N=F_t+\lambda F=0\), \(\|C_{\delta,t}\|=1\), and at \(t=0\),

\[
 R=0,
 \qquad z=\frac1{\sqrt2},
 \qquad T=\frac1{\sqrt2\,\delta},
 \qquad z^+T=\frac1{2\delta}\longrightarrow\infty.
 \tag{4.13}
\]

This path is not an NSE solution.  It proves only that bounded overlap and
bounded unnormalized velocity cannot control the tangent row without an
angular-speed or denominator estimate.  Frame tightness acts on \(F\) and
\(C\), not on the nonlinear objects \(E_Q\), \(P_Q\), and \(\rho_Q^{-1}\).

## 5. The existing broad flat-top parent frame

R0.71E declared a smooth square partition in logarithmic radius.  Choose a
smooth \(m\) such that

\[
 \sum_{j\in\mathbb Z}m(\rho-j)^2=1,
 \tag{5.1}
\]

\[
 m(\rho)=1\quad(0\le\rho\le1/2),
 \qquad
 \operatorname{supp}m\subset[-1/2,1].
 \tag{5.2}
\]

The corresponding parent multipliers are

\[
 m_j(|\xi|)=m(\log_2|\xi|-j).
 \tag{5.3}
\]

This is a fixed smooth radial tight frame.  R0.71E later split each parent
into low and high children for a different trace example.  The present
release uses the parent-only frame (5.3).  Because the quotient is nonlinear,
a parent result must not be silently transferred to that later refinement.

If \(m_j(|\xi|)\ne0\), then

\[
 2^{-1/2}\le\frac{|\xi|}{2^j}\le2,
 \tag{5.4}
\]

and therefore

\[
 \boxed{
 W(\xi):=\sum_j2^{-2j}|m_j(|\xi|)|^2
 \le4|\xi|^{-2}.}
 \tag{5.5}
\]

This weighted Parseval estimate is the only full-frame fact needed for the
heat upper bound.

## 6. Exact zero-entry 2D3C datum in the broad parent

Let \(K=2^J\).  Prescribe the horizontal shear modes

\[
 \widehat u_2(\pm K,0)=1.
 \tag{6.1}
\]

Prescribe vertical driver modes

\[
 \widehat u_3(0,4K)=\frac i4,
 \qquad
 \widehat u_3(0,5K)=-\frac i5,
 \tag{6.2}
\]

together with their conjugates.  For every
\(\sigma,\tau\in\{-1,1\}\), prescribe the eight target modes

\[
 \widehat u_3(\sigma K,\tau4K)=1,
 \qquad
 \widehat u_3(\sigma K,\tau5K)=1.
 \tag{6.3}
\]

All other initial coefficients vanish.  The datum is real, zero mean,
divergence free, independent of \(x_3\), and of the form

\[
 u=(0,V(x_1,t),w(x_1,x_2,t)).
 \tag{6.4}
\]

The horizontal shear solves heat, and \(w\) solves

\[
 w_t+V\partial_2w=\nu\Delta w.
 \tag{6.5}
\]

This is a linear passive advection--diffusion equation with a smooth global
coefficient.  The resulting three-dimensional NSE solution is therefore
global and smooth for every \(K\).

Use the parent \(j=J+2\), whose declared scale is

\[
 \kappa=2^{J+2}=4K.
 \tag{6.6}
\]

The squared radii of its initial Lamb modes are

\[
 16,17,20,25,26,29,
 \tag{6.7}
\]

and the squared radii of its initial \(C\)-modes are

\[
 16,17,25,26.
 \tag{6.8}
\]

All lie in the flat interval \([16,32]\), which is exactly
\([\kappa^2,2\kappa^2]\) after division by \(K^2\).  The parent multiplier is
one on all of them.  The shear radius \(K\) lies outside this block.

Direct normalized-Haar Fourier convolution gives (1.7).  More specifically,
the two vertical channels contribute

\[
 B_{n=4}=4K^3,
 \qquad
 B_{n=5}=-4K^3,
 \tag{6.9}
\]

so the strict denominator coexists with the exact zero entry

\[
 B_\kappa(0)=a_\kappa(0)=0.
 \tag{6.10}
\]

The independent standard-library checker also resolves the cancellation by
horizontal Fourier index:

\[
 \begin{array}{c|ccc}
 |m|&\|F\|_2^2/K^2&d/K^4&B/K^3\\ \hline
 0&328&82&36\\
 1&8&3860&-36\\
 2&164&0&0.
 \end{array}
 \tag{6.11}
\]

The cancellation in (6.10) is therefore not a missing-mode artifact.

## 7. Fixed-window parabolic limit

Put

\[
 \theta=\nu K^2t.
 \tag{7.1}
\]

For each retained vertical channel \(n\in\{4,5\}\), the sideband
coefficients obey, up to the harmless Fourier sign convention,

\[
 \frac{d}{d\theta}c_{m,n}^{(K)}
 =-(m^2+n^2)c_{m,n}^{(K)}
 +\frac{in}{\nu K}e^{-\theta}
 (c_{m-1,n}^{(K)}+c_{m+1,n}^{(K)}).
 \tag{7.2}
\]

The shift is bounded on every polynomially weighted \(\ell_s^2\), while the
diagonal part generates an analytic contraction semigroup.  The initial data
have finite support.  Duhamel's formula, followed by the differentiated
equation, gives for fixed \(M<\infty\), finite \(s\), and fixed \(\nu>0\),

\[
 \max_{n=4,5}
 \|c_{\cdot,n}^{(K)}-c_{\cdot,n}^{(0)}\|_{C^1([0,M];\ell_s^2)}
 \le\frac{C_{M,s,\nu}}K.
 \tag{7.3}
\]

The multiplier (5.3) is bounded and smooth.  Consequently the normalized
selected quadratic quantities converge in \(C^1\).  In the pure-heat limit,

\[
 \frac{B_\kappa}{K^3}\longrightarrow
 B_0(\theta)=4(e^{-34\theta}-e^{-52\theta}),
 \tag{7.4}
\]

\[
 \frac{d_\kappa}{K^4}\longrightarrow
 D_0(\theta)
 =32e^{-32\theta}+1156e^{-34\theta}
 +50e^{-50\theta}+2704e^{-52\theta},
 \tag{7.5}
\]

\[
 \frac{Y}{K^2}\longrightarrow
 Y_0(\theta)
 =2e^{-2\theta}+2e^{-32\theta}+68e^{-34\theta}
 +2e^{-50\theta}+104e^{-52\theta},
 \tag{7.6}
\]

\[
 \frac{\|F_\kappa\|_2^2}{K^2}\longrightarrow
 4e^{-34\theta}+192e^{-36\theta}
 +4e^{-52\theta}+300e^{-54\theta}.
 \tag{7.7}
\]

Hence

\[
 A_0(\theta)
 =\frac{16(e^{-34\theta}-e^{-52\theta})^2}
 {D_0(\theta)Y_0(\theta)}.
 \tag{7.8}
\]

It vanishes at \(\theta=0\) and is positive at every \(\theta>0\).  At
\(\theta_*=(\log2)/18\), exact simplification gives (1.9).  Uniform
convergence implies that, for all sufficiently large dyadic \(K\),

\[
 a_\kappa\!\left(\frac{\theta_*}{\nu K^2}\right)
 \ge\frac{A_*}{2},
 \tag{7.9}
\]

and the parent denominator remains strictly positive on the fixed window.
The profile (7.8) is an asymptotic fixed-window formula, not an exact
finite-\(K\) time curve.

## 8. Complete-frame heat upper bound

The exact 2D3C equation gives more than a general Hodge estimate.  Since

\[
 L=u_t-\nu\Delta u=(0,0,-V\partial_2w),
 \tag{8.1}
\]

and this vector is already divergence free,

\[
 \frac{\|L\|_2^2}{Y}
 \le\|V\|_\infty^2
 =4e^{-2\theta}.
 \tag{8.2}
\]

The shear does not change the vertical Fourier channel.  Every Lamb mode has
\(|\xi_2|=4K\) or \(5K\), so

\[
 |\xi|\ge4K.
 \tag{8.3}
\]

Equations (5.5), (8.2), and (8.3) imply

\[
 \begin{aligned}
 \sum_j2^{-2j}\frac{\|T_jL\|_2^2}{Y}
 &\le4\frac{\||D|^{-1}L\|_2^2}{Y}\\
 &\le\frac1{4K^2}\frac{\|L\|_2^2}{Y}\\
 &\le\frac{e^{-2\theta}}{K^2}.
 \end{aligned}
 \tag{8.4}
\]

Since \(dt=d\theta/(\nu K^2)\), integration to \(\theta_*\) gives

\[
 \mathcal H_K^{\rm frame}
 \le\frac1{\nu K^4}\int_0^{\theta_*}e^{-2\theta}d\theta
 =\frac{1-2^{-1/9}}{2\nu K^4}.
 \tag{8.5}
\]

This is the total of every parent in the fixed frame, not merely the selected
parent.

## 9. Complete-frame positive-creation lower bound

On the selected parent, the nominal rate in (2.7) is

\[
 \lambda=\nu\kappa^2=16\nu K^2.
 \tag{9.1}
\]

Integrating (2.7), using \(a_\kappa(0)=0\), gives

\[
 2\int_{I_K}z_\kappa^+\mathcal J_\kappa^+dt
 \ge a_\kappa(\sup I_K)
 \ge\frac{A_*}{2}.
 \tag{9.2}
\]

Therefore

\[
 \kappa^{-2}\int_{I_K}z_\kappa^+\mathcal J_\kappa^+dt
 \ge\frac{A_*}{64K^2}.
 \tag{9.3}
\]

Every other full-frame summand is nonnegative, so (9.3) proves (1.10).
Combining it with (8.5) proves (1.12).

### Theorem 9.1 — broad-parent full-frame heat-payment no-go

For the fixed smooth broad parent frame (5.3), fixed viscosity \(\nu>0\),
and the global-smooth fixed-energy 2D3C family (6.1)--(6.3), no constant
\(C\) independent of the dyadic frequency \(K\) can satisfy

\[
 \sum_j2^{-2j}\int_{I_K}z_j^+\mathcal J_j^+dt
 \le C
 \sum_j2^{-2j}\int_{I_K}
 \frac{\|T_jL\|_2^2}{Y}dt
 \tag{9.4}
\]

for all sufficiently large \(K\).  The ratio is bounded below by the
positive constant in (1.12) times \(K^2\).

The theorem covers the full frequency frame and a genuine global-smooth NSE
solution.  It does not say that the full positive source is infinite, and it
does not reject a different NSE quantity that is not bounded by the heat
endpoint in (9.4).

## 10. Literature boundary

The neighboring all-scale identities are well established, but they concern
different quantities.

1. [Eyink--Aluie, arXiv:0909.2386](https://arxiv.org/abs/0909.2386) constructs
   nonnegative smooth band energies from a multiscale Germano identity and
   derives the usual flux-difference telescope.  The paper explicitly
   distinguishes signed flux from mean absolute flux; the latter is immune
   to cancellation.  R0.71J does not claim a new smooth band-energy or
   Germano identity.
2. [Germano, J. Fluid Mech. 238 (1992)](https://doi.org/10.1017/S0022112092001733)
   gives the classical exact relation between filtered stresses at different
   levels.  Linear filter nesting does not control the normalized shellwise
   positive source in (3.1).
3. [Cheskidov--Constantin--Friedlander--Shvydkoy,
   arXiv:0704.0759](https://arxiv.org/abs/0704.0759) gives Littlewood--Paley
   commutator representations and critical Besov flux estimates for Euler.
   Those estimates require additional regularity; they are not an
   unconditional Leray payment for (1.1).
4. [Koch--Tataru](https://math.berkeley.edu/~tataru/papers/nas.pdf) controls a
   heat-flow Carleson norm for small \(BMO^{-1}\) data and obtains global
   well-posedness in that small-data class.  Importing that norm would be a
   conditional route, not a consequence of the Leray energy inequality.
5. [Cheskidov--Shvydkoy,
   arXiv:0708.3067](https://arxiv.org/abs/0708.3067) derives regularity from
   critical Besov continuity/jump conditions.  Those conditions cannot be
   inserted into R0.71J as though they were already proved by the target
   weighted-BV estimate.

A bounded primary-source search through 2026-08-26 found no theorem for the
specific normalized quantity in (1.1) with the complete \(N\), \(M\),
\(Y_t/Y\), soft denominators, spatial cells, and refresh faces.  This negative
finding is not a novelty or priority determination.  A formal novelty claim
would require broader database and expert citation review.

## 11. What is closed and what remains open

### 11.1 Closed by exact calculation

1. The hard all-shell source satisfies the positive-defect identity (3.1).
2. The soft denominator adds a nonnegative radial damping defect.
3. Tightness telescopes the raw signed numerator only to the classical
   enstrophy-production ledger (4.2).
4. The R0.71E broad parent frame contains an exact zero-entry 2D3C datum with
   the five constants in (1.7).
5. Its fixed-window limit produces a strictly positive parent amplitude.
6. The complete broad parent frame has heat endpoint \(O(K^{-4})\), while
   complete-frame positive creation is \(\gtrsim K^{-2}\).
7. Hence ordinary full-frequency-frame summation and the same full-frame heat
   endpoint do not close the R0.71I BV reduction.

### 11.2 Not closed

1. The later R0.71E low/high child refinement is not covered.
2. A matched spatial cell partition and its collar/movement terms are not
   covered.
3. Denominator zero faces and partition refresh atoms are not paid.
4. No different Leray-controlled NSE quantity paying \(\mathcal Z_+\) is
   ruled out.
5. No infinite frame--cell soft-limit theorem is proved.
6. No unconditional weighted-BV continuation criterion is proved.
7. No global regularity or singularity conclusion follows.

The phrase “no cancellation” in this release means precisely (3.1): after
the shellwise positive parts defining the target have been taken, the
universal shell sum leaves nonnegative defects.  It does not mean that all
signed NSE interactions lack cancellations.

## 12. Route verdict and next finite gate

The frequency-only escape left by R0.71I is now closed for the existing broad
parent frame:

\[
 \text{full-frame tightness or the same full-frame heat endpoint}
 \not\Longrightarrow
 \text{uniform payment of positive joint creation}.
 \tag{12.1}
\]

The temporal-residence branch can continue only if it introduces a genuinely
different NSE budget, already meaningful at the Leray level, or if matched
spatial localization creates a coercive defect that is absent in the global
cell.  Reusing a signed shell-transfer telescope after taking positive parts,
or reweighting the same heat endpoint, is no longer a viable step.

The next finite gate is R0.71K: retain the broad parent frame, replace the
global cell by one fixed matched spatial partition, and determine whether the
sum of localized quotients inherits the global \(K^2\) gap or instead gains a
new collar/transport payment.  The calculation must keep every localization
boundary, denominator face, and refresh atom.  If the cell sum merely moves
the same positive defect into uncontrolled faces, the temporal-residence
branch should stop rather than rename that cost.

## 13. Reproduction and evidence map

The exact producer is `research/r071j_exact_audit.py`.  It uses symbolic
arithmetic and the repository's finite-Fourier primitives.  It verifies the
hard/soft positive-defect identities, all initial constants, the complete
pure-heat profiles, \(A_*\), the full-frame heat bound, and the \(K^2\)
separation.

The independent checker is `research/r071j_independent_audit.py`.  It imports
neither the producer nor the project Fourier helper.  Using only the Python
standard library, it independently reconstructs curl, convolution, Leray
projection, parent filtering, horizontal-mode cancellation, the parabolic
profiles, and successive \(K^2\) ratios.

The proof of fixed-window convergence is analytic.  The certificates do not
time-step the three-dimensional PDE and do not use DNS, fitted parameters,
GPU computation, or the DGX system.  Closed-form algebra is the stronger
evidence for this structural gate.
