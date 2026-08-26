# R0.71S -- Nonzero-mean temporal packets recover an entry, but their critical Bessel bound pays the same two-derivative tax

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, localized Littlewood--Paley observables, temporal
frames, adjoint heat packets, and parabolic Carleson packing

**Status:** release source.  This report proves a finite conditional
directional-packet theorem, derives its exact Bessel and directional Carleson
requirements, and audits nonzero-mean averaging packets, backward-heat
adjoints, bounded bilinear temporal kernels, and even-order touches.  A
covariantly rescaled genuine Navier--Stokes initial face proves that a
scale-invariant entry atom cannot be paid by the bare time integral of the
normalized Leray \(\dot H^{-1}\) Lamb budget with a scale-independent
constant.  The genuine example is an observation-boundary entry.  No internal
repeated-entry Navier--Stokes family, internal-entry impossibility theorem,
temporal packing theorem, continuation criterion, singularity, global
regularity, novelty, or priority result is claimed.

## 0. Direct decision

R0.71R left open the possibility that retaining the direction

\[
 e_\beta=\frac{c_\beta}{\|c_\beta\|_2}
\]

and the signed pairing \(\langle F_j,e_\beta\rangle\) could repair the
two-derivative mismatch of the endpoint-square certificate.  R0.71S tests
that possibility at the level of a finite temporal frame.

For a positive entry \(\beta=(j,Q,t_\beta)\), put

\[
 f_\beta(s)
 =\frac{\langle F_j(s),e_\beta\rangle}{\sqrt{Y(s)}},
 \qquad
 a_\beta
 =\kappa_j^{-2}\bigl(f_\beta(t_\beta)^+\bigr)^2.
 \tag{0.1}
\]

Thus \(a_\beta=\kappa_j^{-2}A_{\beta,+}\) is the R0.71P entry target.  Let

\[
 h_\beta=\theta_\beta\kappa_j^{-2},
 \qquad 0<\theta_-\le\theta_\beta\le\theta_*,
 \qquad I_\beta=[t_\beta,t_\beta+h_\beta].
 \tag{0.2}
\]

The audit has one conditional positive statement and four exact negative
statements.

1. A nonzero-mean \(L^2\)-normalized time packet recovers \(a_\beta\) if its
   directional average stays coherent with the entry trace.
2. If the associated solution-dependent space--time packets satisfy a Bessel
   inequality in the Leray-paid direct-sum Hilbert space, then the entire
   finite entry family is paid.  Repeated entries remain in the Bessel sum.
3. The required critical packet has squared norm \(\kappa_j^2\).  Hence even
   one packet forces a Bessel constant at least \(\kappa_j^2\); \(N\)
   identical copies force at least \(N\kappa_j^2\).
4. In the frozen-denominator annular model, a backward-heat adjoint has
   exactly the same diagonal cost.  A general
   bounded bilinear temporal kernel has a sharp dichotomy: a nonzero constant
   mode sees the entry and costs \(\kappa_j^2\), while cancellation of the
   constant mode makes the entry invisible.
5. At an even-order positive touch, the left and right signed faces cancel.
   A signed or mean-zero packet therefore cannot dominate the one-sided target
   without adding a Jordan or positive-variation operation.

There is also a stronger scaling verdict.  The R0.71O genuine NSE initial
face and its integer covariant dilations have invariant entry target, whereas

\[
 \int\frac{\|L\|_{\dot H^{-1}}^2}{Y}\,dt
\]

loses two powers on the corresponding dilated time interval.  Consequently,
no covariant theorem that includes this observation-boundary entry can pay the
original atomic target from that bare time integral with a scale-independent
constant.  This verdict is narrower than an impossibility theorem for
internal entries or for every nonlinear NSE-specific signed identity.

## 1. Interface and exact scale table

Work on the normalized periodic torus.  Let \(u\) be a nontrivial zero-mean
classical solution on an interval, and use the fixed-frame notation

\[
 \omega=\operatorname{curl}u,
 \qquad Y=\|\omega\|_2^2,
 \qquad L=\mathbb P(u\times\omega),
 \qquad F_j=T_jL,
 \tag{1.1}
\]

\[
 W_j=T_j\omega,
 \qquad C_{j,Q}=\operatorname{curl}(\chi_QW_j).
 \tag{1.2}
\]

At a finite-order zero,

\[
 C_{j,Q}(t_\beta+\tau)
 =c_\beta\tau^{m_\beta}+O_{L^2}(|\tau|^{m_\beta+1}),
 \qquad c_\beta\ne0.
 \tag{1.3}
\]

The right entry is positive exactly when
\(f_\beta(t_\beta)=\langle F_j(t_\beta),e_\beta\rangle/\sqrt{Y(t_\beta)}>0\).

For a compatible integer, and dyadic when required by the multiplier family,
let

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t)
 \tag{1.4}
\]

and rescale the multiplier, cutoff, event, and time-window families
covariantly.  The following table records \(q_\lambda(t)=\lambda^\sigma
q(\lambda^2t)\), with composition in space suppressed.  Norm exponents are
the normalized-torus exponents.

| Quantity | Definition | \(\sigma\) |
|---|---|---:|
| frequency | \(\kappa_j\) | \(+1\) |
| time and window height | \(dt,h_\beta\) | \(-2\) |
| enstrophy | \(Y=\|\omega\|_2^2\) | \(+4\) |
| shell Lamb norm | \(\|F_j\|_2\) | \(+3\) |
| localized observable norm | \(\|C_{j,Q}\|_2\) | \(+3\) |
| normalized entry direction | \(e_\beta=c_\beta/\|c_\beta\|_2\) | \(0\) |
| directional Lamb pairing | \(\langle F_j,e_\beta\rangle\) | \(+3\) |
| normalized directional scalar | \(f_\beta=\langle F_j,e_\beta\rangle/\sqrt Y\) | \(+1\) |
| entry atom | \(a_\beta=\kappa_j^{-2}(f_\beta^+)^2\) | \(0\) |
| Leray Lamb norm | \(\|L\|_{\dot H^{-1}}\) | \(+2\) |
| paid time density | \(\|L\|_{\dot H^{-1}}^2/Y\) | \(0\) |
| paid time integral | \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) | \(-2\) |
| normalized temporal packet | \(\eta_\beta=h_\beta^{-1/2}\eta((t-t_\beta)/h_\beta)\) | \(+1\) |
| nonzero-mean coefficient | \(p_\beta=\int\eta_\beta f_\beta\,dt\) | \(0\) |

The last three rows already locate the issue.  The packet coefficient can have
the same scale as the atomic target, but its square is not naturally paid by
a time integral of scale exponent \(-2\).  Section 3 identifies the missing
factor as the norm of one critical dual packet, not as an overlap estimate.

The fixed annular family supplies

\[
 \sum_j\kappa_j^{-2}\|F_j(t)\|_2^2
 \le C_T\|L(t)\|_{\dot H^{-1}}^2.
 \tag{1.5}
\]

No temporal conclusion follows from (1.5) alone.

## 2. A finite nonzero-mean directional-packet theorem

Choose a real \(\eta\in L^2(0,1)\) such that

\[
 \|\eta\|_{L^2(0,1)}=1,
 \qquad \mu:=\int_0^1\eta(r)\,dr>0.
 \tag{2.1}
\]

For every finite positive-entry family \(\mathcal E\), define

\[
 \eta_\beta(s)
 =h_\beta^{-1/2}
 \eta\!\left(\frac{s-t_\beta}{h_\beta}\right)
 \mathbf1_{I_\beta}(s),
 \qquad
 p_\beta=\int_{I_\beta}\eta_\beta(s)f_\beta(s)\,ds.
 \tag{2.2}
\]

Then \(\|\eta_\beta\|_2=1\) and

\[
 \int_{I_\beta}\eta_\beta(s)\,ds=\mu\sqrt{h_\beta}.
 \tag{2.3}
\]

The required event-wise input is the **directional sampling coherence**

\[
 \boxed{
 p_\beta\ge
 (1-\delta)\mu\sqrt{h_\beta}\,f_\beta(t_\beta)>0,
 \qquad 0\le\delta<1.}
 \tag{2.4}
\]

For one fixed finite classical family, continuity of \(f_\beta\) makes (2.4)
true after shrinking each right window sufficiently.  That observation does
not provide a truncation-independent lower height \(\theta_->0\), and it does
not ensure that a right window remains available near a maximal endpoint.

Introduce the Hilbert space

\[
 \mathscr X
 =L^2\!\left(K^+;\bigoplus_j L^2(\mathbb T^3)\right),
 \qquad
 X_j(s)=\frac{\kappa_j^{-1}F_j(s)}{\sqrt{Y(s)}}.
 \tag{2.5}
\]

For every event let \(\Phi_\beta\in\mathscr X\) have only one nonzero shell
component,

\[
 (\Phi_\beta)_j(s,x)
 =\begin{cases}
 \kappa_j\eta_\beta(s)e_\beta(x),&j=j(\beta),\\
 0,&j\ne j(\beta).
 \end{cases}
 \tag{2.6}
\]

Then the desired coefficient is exactly

\[
 p_\beta=\langle X,\Phi_\beta\rangle_{\mathscr X}.
 \tag{2.7}
\]

### Theorem 2.1 -- finite critical directional-packet payment

Let \(\mathcal E\) be finite and suppose (0.2), (2.1), and (2.4) hold.  If
the complete indexed packet family satisfies

\[
 \boxed{
 \sum_{\beta\in\mathcal E}
 |\langle Z,\Phi_\beta\rangle_{\mathscr X}|^2
 \le B_{\rm crit}\|Z\|_{\mathscr X}^2
 \quad\text{for every }Z\in\mathscr X,}
 \tag{2.8}
\]

then

\[
 \boxed{
 \sum_{\beta\in\mathcal E}a_\beta
 \le
 \frac{B_{\rm crit}}
 {\mu^2(1-\delta)^2\theta_-}
 \int_{K^+}\frac1{Y(s)}
 \sum_j\kappa_j^{-2}\|F_j(s)\|_2^2\,ds.}
 \tag{2.9}
\]

Consequently,

\[
 \boxed{
 \sum_{\beta\in\mathcal E}a_\beta
 \le
 \frac{C_TB_{\rm crit}}
 {\mu^2(1-\delta)^2\theta_-}
 \int_{K^+}\frac{\|L(s)\|_{\dot H^{-1}}^2}{Y(s)}\,ds.}
 \tag{2.10}
\]

#### Proof

From (2.4), (0.2), and (0.1),

\[
 \begin{aligned}
 |p_\beta|^2
 &\ge\mu^2(1-\delta)^2h_\beta
 f_\beta(t_\beta)^2\\
 &=\mu^2(1-\delta)^2\theta_\beta a_\beta\\
 &\ge\mu^2(1-\delta)^2\theta_-a_\beta.
 \end{aligned}
 \tag{2.11}
\]

Sum (2.11), use (2.7)--(2.8) with \(Z=X\), and expand (2.5).  This proves
(2.9).  Formula (1.5) proves (2.10). \(\square\)

Theorem 2.1 is the strongest direct finite reduction in this packet class.
It does not establish either of its two uniform inputs: noncollapsing
directional coherence and a truncation-independent critical Bessel bound.

## 3. The single-packet and repeated-packet Bessel tax

The norm of every vector in (2.6) is exact:

\[
 \boxed{\|\Phi_\beta\|_{\mathscr X}^2=\kappa_{j(\beta)}^2.}
 \tag{3.1}
\]

Indeed, \(\|\eta_\beta\|_2=\|e_\beta\|_2=1\).  Apply (2.8) with
\(Z=\Phi_\beta\) and retain only the \(\beta\)-term.  This gives

\[
 \kappa_j^4
 \le B_{\rm crit}\kappa_j^2,
\]

and hence

\[
 \boxed{B_{\rm crit}\ge\max_{\beta\in\mathcal E}\kappa_{j(\beta)}^2.}
 \tag{3.2}
\]

This lower bound is diagonal.  Spatial direction separation, temporal
window separation, a better Gram-matrix estimate, and a Carleson packing
argument cannot reduce it.

If one packet is included \(N\) times with the same index, window, and
direction, then testing against that packet gives

\[
 \boxed{B_{\rm crit}\ge N\kappa_j^2.}
 \tag{3.3}
\]

Thus repeated entries or repeated labels cannot be silently deleted from the
packet estimate.  Distinct entries with disjoint windows need not incur the
factor \(N\), but each still carries the factor \(\kappa_j^2\) in the
critical Hilbert space.

For comparison, remove the factor \(\kappa_j\) from (2.6) and use the
unweighted packets

\[
 (\Psi_\beta)_j=\eta_\beta e_\beta.
 \tag{3.4}
\]

These have norm one and may have a Bessel bound controlled by temporal
overlap or directional orthogonality.  Their coefficients pair against
\(F_j/\sqrt Y\), however, and therefore give only

\[
 \sum_\beta|\langle F/\sqrt Y,\Psi_\beta\rangle|^2
 \lesssim
 \int\frac1Y\sum_j\|F_j\|_2^2\,dt.
 \tag{3.5}
\]

This is the normalized \(L^2\)-Lamb budget from the \(\rho=0\) side of
R0.71R, not the Leray \(\dot H^{-1}\) budget.  The factor that repairs the
spatial Sobolev order is exactly the factor that creates (3.1).

## 4. Directional Carleson is necessary, but cannot remove the diagonal

The full Bessel inequality (2.8) has an immediate directional Carleson
consequence.  Fix a shell \(j\), a time interval \(J\subset K^+\), and a
spatial vector \(v\in L^2(\mathbb T^3)\).  Test (2.8) with

\[
 Z_j(s)=\mathbf1_J(s)v,
 \qquad Z_k=0\quad(k\ne j).
 \tag{4.1}
\]

For every \(I_\beta\subset J\) in shell \(j\), (2.3) gives

\[
 \langle Z,\Phi_\beta\rangle
 =\mu\kappa_j\sqrt{h_\beta}\,
 \langle v,e_\beta\rangle.
 \tag{4.2}
\]

Discarding all other nonnegative terms in the Bessel sum proves

\[
 \boxed{
 \mu^2
 \sum_{\substack{\beta:j(\beta)=j\\I_\beta\subset J}}
 \kappa_j^2h_\beta|\langle v,e_\beta\rangle|^2
 \le B_{\rm crit}|J|\|v\|_2^2.}
 \tag{4.3}
\]

Formula (4.3) is a necessary directional Carleson condition.  It is not
asserted to be sufficient for arbitrary intervals, packet shapes, and
solution-dependent directions.  The complete Gram operator in (2.8) is the
authoritative condition.

Since \(\kappa_j^2h_\beta=\theta_\beta\), repeated same-direction entries in
one interval obey, conditionally,

\[
 \#\{\beta:j(\beta)=j,I_\beta\subset J,e_\beta=e\}
 \le\frac{B_{\rm crit}|J|}{\mu^2\theta_-}
 \tag{4.4}
\]

after testing with \(v=e\).  Taking \(J=I_\beta\) for one packet already
gives \(B_{\rm crit}\ge\mu^2\kappa_j^2\), consistent with the sharper
diagonal bound (3.2).

For the unweighted packets (3.4), the corresponding necessary condition is

\[
 \mu^2
 \sum_{\substack{\beta:j(\beta)=j\\I_\beta\subset J}}
 h_\beta|\langle v,e_\beta\rangle|^2
 \le B_0|J|\|v\|_2^2.
 \tag{4.5}
\]

This is the usual time-packing scale.  It may control recurrence in the
strong \(L^2\)-Lamb space, but it does not restore the missing
\(\dot H^{-1}\) weight.

## 5. Backward-heat adjoints reproduce the same packet

Write the exact R0.71R equation as

\[
 C_t-\nu\Delta C=D_{j,Q}F_j+R_{j,Q}W_j,
 \tag{5.1}
\]

where

\[
 D_{j,Q}F=\operatorname{curl}(\chi_Q\operatorname{curl}F)
 \tag{5.2}
\]

and \(R_{j,Q}W\) is the complete localization--viscosity commutator.  Given
terminal data \(q\), let

\[
 z(s)=e^{\nu(t+h-s)\Delta}q,
 \qquad -z_s-\nu\Delta z=0,
 \qquad z(t+h)=q.
 \tag{5.3}
\]

If \(C(t)=0\), integration by parts gives the exact adjoint identity

\[
 \boxed{
 \langle C(t+h),q\rangle
 =\int_t^{t+h}\langle F_j,D_{j,Q}^*z\rangle\,ds
 +\int_t^{t+h}\langle W_j,R_{j,Q}^*z\rangle\,ds.}
 \tag{5.4}
\]

Thus localization does not leave a pure Lamb packet: the viscous commutator
remains, and alignment of \(D^*z\) with \(e_\beta\) would be another
hypothesis.

The global annular eigenmode already decides the scale issue without these
extra errors.  Set \(\chi=1\), let \(-\Delta e=\kappa^2e\),
\(\|e\|_2=1\), and restrict to a divergence-free mode.  Then
\(D=\operatorname{curl}\operatorname{curl}=-\Delta\), and (5.4) becomes

\[
 \boxed{
 \langle C(t+h),e\rangle
 =\kappa^2\int_0^h
 e^{-\nu\kappa^2(h-r)}
 \langle F(t+r),e\rangle\,dr.}
 \tag{5.5}
\]

After the factor \(\kappa^{-1}\) required by the entry target, the effective
time kernel is

\[
 q_{\kappa,h}(r)
 =\kappa e^{-\nu\kappa^2(h-r)}\mathbf1_{(0,h)}(r),
 \qquad h=\theta\kappa^{-2}.
 \tag{5.6}
\]

Its exact mean and squared norm are

\[
 \boxed{
 \int_0^h q_{\kappa,h}(r)\,dr
 =\frac{1-e^{-\nu\theta}}{\nu\kappa},
 \qquad
 \|q_{\kappa,h}\|_2^2
 =\frac{1-e^{-2\nu\theta}}{2\nu}.}
 \tag{5.7}
\]

At \(\nu=0\), the continuous limits are \(\theta/\kappa\) and \(\theta\).
Write

\[
 g(t)=\langle F(t),e\rangle.
\]

For a constant unnormalized directional source \(g\), the exact endpoint
coefficient

\[
 p_{\rm ad}=\int_0^h q_{\kappa,h}(r)g(t+r)\,dr
 \tag{5.8}
\]

satisfies

\[
 p_{\rm ad}^2
 =\left(\frac{1-e^{-\nu\theta}}{\nu}\right)^2
 \kappa^{-2}g^2.
 \tag{5.9}
\]

Thus the backward heat kernel has nonzero mean.  In the frozen-denominator
model \(Y\equiv1\), the Leray-order scalar is \(X=\kappa^{-1}g\).  Relative
to this coordinate the dual kernel is \(\kappa q_{\kappa,h}\), whose squared
norm is

\[
 \boxed{
 \|\kappa q_{\kappa,h}\|_2^2
 =\kappa^2\frac{1-e^{-2\nu\theta}}{2\nu}.}
 \tag{5.10}
\]

Equation (5.10) is therefore an exact packet norm and an exact
frozen-denominator linear-model diagnostic.  It is not an exact identity for
the fully normalized NSE signal.  For that signal
\(f=g/\sqrt Y\), (5.8) contains \(\sqrt{Y(t+r)}f(t+r)\); alternatively,
dividing the observable by \(\sqrt Y\) produces an additional \(Y_t/(2Y)\)
coefficient.  The backward heat semigroup alone does not remove the
\(\kappa^2\) packet tax, while control or cancellation of the new denominator
term would require a separate NSE estimate not supplied here.

## 6. A general bounded bilinear packet has a mean dichotomy

Let \(K\) be a bounded self-adjoint operator on \(L^2(0,1)\), and define the
unitary rescaling

\[
 (U_hf)(r)=\sqrt h\,f(t+hr),
 \qquad 0<r<1.
 \tag{6.1}
\]

The associated quadratic temporal packet is

\[
 \mathcal Q_{K,h}[f]
 =\langle U_hf,KU_hf\rangle_{L^2(0,1)}.
 \tag{6.2}
\]

It is scale invariant when \(h=\theta\kappa^{-2}\) and \(f\) has the NSE
exponent in Section 1.  Put

\[
 k_0=\langle\mathbf1,K\mathbf1\rangle.
 \tag{6.3}
\]

For the constant directional signal \(f(s)=f_0\),

\[
 \boxed{
 \mathcal Q_{K,h}[f_0]
 =h f_0^2k_0
 =\theta k_0\,\kappa^{-2}f_0^2.}
 \tag{6.4}
\]

There are only two cases.

1. If \(k_0=0\), the packet has cancellation on constants and gives exactly
   zero on a positive constant directional trace.  It cannot provide an
   event-wise lower comparison for the original entry target.
2. If \(k_0\ne0\), after changing the overall sign when necessary the packet
   sees the entry.  Writing \(f=\kappa X\) gives

   \[
    \mathcal Q_{K,h}[f]
    =\kappa^2\langle U_hX,KU_hX\rangle.
    \tag{6.5}
   \]

   Testing a proposed estimate against a constant \(X\) proves that its
   single-packet form bound is at least

   \[
    \boxed{\kappa^2|k_0|.}
    \tag{6.6}
   \]

The upper form bound is \(\kappa^2\|K\|\).  Thus every bounded bilinear kernel
in this class obeys the same exact alternative:

\[
 \boxed{
 \text{constant-mode cancellation loses the entry;}
 \quad
 \text{nonzero constant mode costs }\kappa^2.}
 \tag{6.7}
\]

This includes the square of a nonzero-mean linear coefficient as a rank-one
case.  It does not cover every nonlinear functional that could be built from
the full NSE state.

## 7. Even-order touches remove the signed face, not the one-sided cost

At a zero of order \(m\), the normalized direction has the traces

\[
 \frac{C(t_\beta+\tau)}{\|C(t_\beta+\tau)\|_2}
 \longrightarrow
 \begin{cases}
 e_\beta,&\tau\downarrow0,\\
 (-1)^m e_\beta,&\tau\uparrow0.
 \end{cases}
 \tag{7.1}
\]

If \(m\) is even and
\(\langle F_j(t_\beta),c_\beta\rangle>0\), then

\[
 A_{\beta,-}=A_{\beta,+}=A_\beta>0.
 \tag{7.2}
\]

The signed face measure therefore has atom

\[
 (A_{\beta,+}-A_{\beta,-})\delta_{t_\beta}=0,
 \tag{7.3}
\]

while the target retains \(A_{\beta,+}\delta_{t_\beta}\).  A bilateral hard
jump, a mean-zero linear packet, or a bilinear packet with \(k_0=0\) cannot
recover this missing one-sided cost.

The exact scalar method test is

\[
 C_\varepsilon(t)=\varepsilon(t-t_0)^2e,
 \qquad F(t)=e,
 \qquad Y=1,
 \qquad \|e\|_2=1.
 \tag{7.4}
\]

On both punctured sides the normalized directional signal is the constant
one, and

\[
 A_-=A_+=1.
 \tag{7.5}
\]

Every signed hard-face atom and every constant-cancelling packet above is
exactly zero.  This is an abstract forced-path test, not a Navier--Stokes
trajectory.  It proves a property of the packet design, not the existence of
an NSE even touch.

To retain (7.5), a construction must use a causal one-sided packet, a Jordan
mass, or a positive-variation operation.  Those choices remove the
cancellation at the touch.  Repeated entries must then be charged by the
actual Bessel or Carleson ledger rather than by a signed telescoping argument.

## 8. Genuine NSE initial-face scaling no-go

The preceding diagonal arguments concern packet geometry.  The strongest
verdict for the requested final inequality comes from an exact NSE scaling
family.

Use the R0.71O smooth initial datum

\[
 u_0(x)=(0,\cos x_1,\cos x_2),
 \tag{8.1}
\]

one real-even radial multiplier whose symbol vanishes at radius \(1\) and is
one at radius \(\sqrt2\), and \(\chi=1\).  R0.71O proves the genuine
one-sided initial face

\[
 Y(0)=1,
 \qquad \|F(0)\|_2^2=\frac14,
 \qquad C(0)=0,
 \qquad C_t(0)=2F(0),
 \tag{8.2}
\]

and hence

\[
 a_*\equiv\kappa^{-2}A_+=\frac14.
 \tag{8.3}
\]

Let \(u\) be its local classical solution.  For every compatible integer
\(\lambda\), define \(u_\lambda\) by (1.4), use the covariantly rescaled
multiplier, and put \(\kappa_\lambda=\lambda\).  The corresponding initial
entry satisfies

\[
 a_{*,\lambda}=a_*=\frac14.
 \tag{8.4}
\]

On the normalized torus,

\[
 \|L_\lambda(t)\|_{\dot H^{-1}}^2
 =\lambda^4\|L(\lambda^2t)\|_{\dot H^{-1}}^2,
 \qquad
 Y_\lambda(t)=\lambda^4Y(\lambda^2t).
 \tag{8.5}
\]

Therefore, for every base time \(T\) inside the classical interval,

\[
 \boxed{
 \int_0^{T/\lambda^2}
 \frac{\|L_\lambda(t)\|_{\dot H^{-1}}^2}{Y_\lambda(t)}\,dt
 =\lambda^{-2}
 \int_0^T\frac{\|L(s)\|_{\dot H^{-1}}^2}{Y(s)}\,ds.}
 \tag{8.6}
\]

### Theorem 8.1 -- no scale-uniform bare Leray-time payment including the initial face

There is no constant \(C\), independent of compatible integer
\(\lambda\), for which every member of the family above satisfies

\[
 \sum_{\beta\in\mathcal E_\lambda}
 \kappa_{j(\beta)}^{-2}A_{\beta,+}
 \le C
 \int_0^{T/\lambda^2}
 \frac{\|L_\lambda(t)\|_{\dot H^{-1}}^2}{Y_\lambda(t)}\,dt,
 \tag{8.7}
\]

whenever \(\mathcal E_\lambda\) contains the corresponding observation-
boundary entry.

#### Proof

The left side of (8.7) is at least \(1/4\) by (8.4).  The right side equals a
fixed finite base integral times \(C\lambda^{-2}\) by (8.6), and tends to zero
as \(\lambda\to\infty\). \(\square\)

Equivalently, the optimal constant along this family grows at least like
\(\lambda^2\).  The theorem is a genuine NSE statement, but its event is an
initial observation-boundary face.  It does not prove any of the following:

1. that a corresponding internal NSE entry exists;
2. that an internal entry can be repeated arbitrarily often;
3. that every internal-entry signed or bilinear identity has the same defect;
4. that an estimate with an additional scale-\(+2\) dynamical charge is
   impossible;
5. that a noncovariant fixed observation horizon cannot give a
   scale-dependent bound.

Theorem 8.1 does prove that changing the temporal kernel alone cannot produce
the requested covariant conclusion when the final right side remains the bare
time integral in (8.7) and the target includes observation-boundary entries.

## 9. Recurrence and what a packet frame would still have to prove

The complete entry family is indexed by events, not only by observables.
Condition (2.8) therefore keeps every return of one \(C_{j,Q}\) to zero.  A
valid recurrence argument would have to prove at least one of the following:

1. a directional Gram estimate that bounds all repeated packets;
2. a directional Carleson estimate stronger than the necessary condition
   (4.3), together with hypotheses that make it sufficient;
3. a signed telescoping identity that still detects even-order touches;
4. an NSE-specific relation that replaces the bare time-integrated
   \(\dot H^{-1}\) budget by a scale-invariant dynamical quantity.

Analyticity makes the zeros of one nontrivial finite observable isolated on a
compact classical subinterval.  It gives a finite minimum separation only
after that observable and interval have been fixed.  It does not provide a
uniform separation or Bessel constant over an infinite shell--cell frame or
near a possible maximal endpoint.

The squared-root forced paths from R0.71R remain useful packet tests.  With
\(F=Y=1\), they create many same-direction entries.  Nonzero-mean one-sided
packets count every entry, so their Gram or Carleson constant must grow when
the windows crowd.  These paths are not NSE recurrence examples and are not
used in Theorem 8.1.

## 10. Relation to primary parabolic upper budgets

Koch--Tataru's \(BMO^{-1}\) construction uses a scale-invariant parabolic
square-Carleson upper norm for caloric extensions and solutions
([Advances in Mathematics 157 (2001), 22--35](https://doi.org/10.1006/aima.2000.1937)).
That norm is an upper tent budget.  It does not state that every zero of a
localized filtered observable carries a lower packet coefficient, and it does
not remove the diagonal calculation (3.1).

The literature interfaces already bounded in `research/r071r_literature_audit.md`
remain unchanged: parabolic Carleson estimates, epsilon regularity, signed
physical-scale flux, Sturm zero-number theorems, and backward uniqueness do
not directly supply (2.4) or (2.8).  R0.71S adds a direct functional and NSE
scaling audit; it does not claim that no theorem outside the checked
interfaces could control a different internal-entry functional.

## 11. Exact result boundary

### Proved in R0.71S

1. the exact scale table in Section 1 for the covariant fixed-torus family;
2. the finite conditional directional-packet theorem (2.9)--(2.10), with its
   complete constant;
3. the single-packet lower bound
   \(B_{\rm crit}\ge\max\kappa_j^2\);
4. the repeated identical-packet lower bound
   \(B_{\rm crit}\ge N\kappa_j^2\);
5. the necessary directional Carleson condition (4.3);
6. the exact backward-heat annular kernel and frozen-denominator norms
   (5.7)--(5.10);
7. the bounded bilinear constant-mode dichotomy (6.7);
8. the loss of an even positive touch under signed-face or constant-mode
   cancellation;
9. the genuine NSE initial observation-boundary scaling no-go, Theorem 8.1.

### Not proved

1. a truncation-independent directional sampling height or coherence
   constant;
2. a scale-independent critical Bessel or directional Carleson bound;
3. an internal NSE positive-entry example for this exact fixed frame;
4. an internal repeated-entry NSE family;
5. an impossibility theorem for every internal-entry nonlinear functional;
6. a scale-invariant replacement dynamical charge;
7. a temporal packing theorem, Leray-limit passage, continuation criterion,
   singularity, or global regularity.

The abstract even-touch and recurrence paths test the method only.  The
scaling obstruction in Section 8 uses genuine NSE solutions but includes an
initial observation-boundary event.  These two evidence classes are not
interchanged.

## 12. Route verdict and next finite gate

Within the following declared class,

\[
 \boxed{
 \begin{gathered}
 \text{original scale-invariant positive-entry target,}\\
 \text{nonzero-mean linear or bounded bilinear temporal packet,}\\
 \text{final payment by }
 \displaystyle\int\|L\|_{\dot H^{-1}}^2/Y\,dt,
 \end{gathered}}
 \tag{12.1}
\]

the two-derivative mismatch is not repaired.  A packet that sees a constant
directional trace has the \(\kappa_j^2\) diagonal tax.  A packet that cancels
that trace cannot dominate an even positive touch.  Backward heat changes the
kernel shape but not this alternative.

The next finite gate should therefore change at least one structural input.
Two mathematically distinct options remain:

1. restrict explicitly to internal entries and derive an NSE-specific
   nonlinear identity that is not a generic temporal Bessel estimate; or
2. retain the full target and identify a genuinely scale-invariant dynamical
   right side, rather than the bare \(dt\)-integral of a scale-zero density.

Neither option is supplied here.  R0.71S stops the temporal-packet branch only
at the boundary stated in (12.1).
