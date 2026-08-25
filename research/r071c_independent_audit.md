# R0.71C independent mathematical audit

**Date:** 2026-08-25

**Scope:** independent checking of the finite-partition signed-before-square
ledger, the explicit two-triad full-response witness, its Stokes and true
Navier--Stokes time derivatives, the complete shell-injection conditional
quantity, the signed-interval reverse-Cauchy obstruction, the three-mode
normalization discontinuity, and the balanced \(M=8,64\) HHL heat/NSE
witness for the exact-radius Parseval response.

The checker does not import any project audit module.  It rebuilds every
Fourier multiplier and convolution from the stated coefficients.  It does
not read the R0.71C producer.  All deciding calculations use exact rational
or symbolic arithmetic.

## 1. Audit verdict

All requested identities pass.  In particular,

\[
 W(0)=0,
 \qquad
 W'(0)=12\nu\varepsilon^3+\frac{76}{5}\varepsilon^4>0
 \tag{1.1}
\]

for the scaled finite Fourier datum and the full-response covariance
\(Q=\omega\otimes\omega\).

The two additional exact gates also pass.  The three-mode positive-output
term is \(A^2B^2/64\) for every \(\eta>0\), while its normalized one-sided
limit is

\[
 \frac{A^2B^2}{32(A^2+B^2)}.
 \tag{1.2}
\]

For the balanced exact-radius HHL datum, every initial output work is zero
and the true NSE target derivative is

\[
 \frac{2193\delta^3}{19304720}
 \left(2193\delta+32704\sqrt{1206545}\,\nu\right)>0.
 \tag{1.3}
\]

There is one implementation point that is mathematically essential.  When
differentiating \(Q\), the nonlinear derivative \(\dot\omega\) already has
Fourier support outside the initial twelve modes.  Those generated modes can
pair with an initial mode and return to either selected output.  Retaining only
derivatives of the initial support gives the incorrect quartic coefficient
\(-21/5\).  The full convolution has 50 nonzero generated modes and gives
\(76/5\).

The conclusion is deliberately narrow.  It is a no-go for a monotone
signed-partial-sum argument at fixed full-response output nodes.  It does not
exclude an adaptive localization or a genuine PDE flux identity that controls
the refinement defects.

## 2. Finite partitions: refinement only exposes more positive mass

Let \(i\) range over a finite set, let \(w_i\in\mathbb R\), and let
\(d_i>0\).  For a partition \(\Pi\), put

\[
 W_B=\sum_{i\in B}w_i,
 \qquad
 D_B=\sum_{i\in B}d_i,
 \qquad
 E_\Pi=\sum_{B\in\Pi}\frac{(W_B^+)^2}{D_B}.
 \tag{2.1}
\]

Two facts hold without a PDE.

First,

\[
 \left(\sum_iw_i\right)^+
 \leq \sum_{B\in\Pi}W_B^+
 \leq
 \left(\sum_i d_i\right)^{1/2}E_\Pi^{1/2}.
 \tag{2.2}
\]

Second, if \(\Pi'\) refines \(\Pi\), then

\[
 E_\Pi\leq E_{\Pi'}.
 \tag{2.3}
\]

Indeed, if a parent \(B\) is split into children \(B_j\), then

\[
 W_B^+\leq\sum_j W_{B_j}^+,
\]

and weighted Cauchy gives

\[
 \frac{(W_B^+)^2}{D_B}
 \leq
 \sum_j\frac{(W_{B_j}^+)^2}{D_{B_j}}.
 \tag{2.4}
\]

### 2.1 Exact binary defect

For child works \(x,y\) and weights \(d,e>0\), set

\[
 a=x^+,
 \qquad b=y^+,
 \qquad c=(x+y)^+.
\]

The refinement defect is exactly

\[
\begin{aligned}
 \delta
 &=\frac{a^2}{d}+\frac{b^2}{e}-\frac{c^2}{d+e}\\
 &=\frac{(ea-db)^2}{de(d+e)}
   +\frac{(a+b)^2-c^2}{d+e}\geq0.
 \tag{2.5}
\end{aligned}
\]

The first term measures a mismatch between positive work and dissipative
weight.  The second measures cancellation hidden by the parent.  If both
children are nonnegative, the second term vanishes and

\[
 \delta=\frac{(ex-dy)^2}{de(d+e)}.
 \tag{2.6}
\]

On a finite binary tree, every intermediate energy occurs once with a plus
sign and once with a minus sign.  Therefore

\[
 \boxed{E_{\operatorname{leaves}}=E_{\operatorname{root}}
 +\sum_{v\ \operatorname{internal}}\delta_v.}
 \tag{2.7}
\]

Thus nesting does not manufacture a free cancellation estimate.  Moving
from a coarse signed sum toward the fine positive-output consumer reveals a
nonnegative accumulated defect.

## 3. The explicit full-response Fourier witness

Use the six positive labels below and add their negatives with the same real
coefficient.

| label | frequency | vorticity coefficient | squared radius |
|---|---:|---:|---:|
| \(k_1\) | \((2,0,0)\) | \(e_2\) | \(4\) |
| \(p_1\) | \((1,1,0)\) | \((1,-1,0)\) | \(2\) |
| \(q_1\) | \((1,-1,0)\) | \(-e_3\) | \(2\) |
| \(k_2\) | \((0,0,2)\) | \(e_1\) | \(4\) |
| \(p_2\) | \((2,0,1)\) | \((-1,0,2)\) | \(5\) |
| \(q_2\) | \((-2,0,1)\) | \(\tfrac12e_2\) | \(5\) |

Every coefficient is perpendicular to its frequency.  The negative-mode
assignment makes a real, mean-zero, divergence-free trigonometric
polynomial.  Exact enumeration of the twelve signed modes finds 24 ordered
zero-sum triples: 12 permutations and orientations for each triad, and no
mixed-triad resonance.

For

\[
 \widehat u(k)=\frac{i\,k\times\widehat\omega(k)}{|k|^2},
 \qquad
 \widehat S(k)=\frac{i}{2}
 \bigl(k\otimes\widehat u(k)+\widehat u(k)\otimes k\bigr),
 \tag{3.1}
\]

and

\[
 \widehat Q(k)=\sum_{p+q=k}
 \widehat\omega(p)\otimes\widehat\omega(q),
 \tag{3.2}
\]

the selected matrices are

\[
 \widehat S(k_1)=
 \begin{pmatrix}0&0&-1/2\\0&0&0\\-1/2&0&0\end{pmatrix},
 \qquad
 \widehat Q(k_1)=
 \begin{pmatrix}0&0&-1\\0&0&1\\-1&1&0\end{pmatrix},
 \tag{3.3}
\]

and

\[
 \widehat S(k_2)=
 \begin{pmatrix}0&0&0\\0&0&-1/2\\0&-1/2&0\end{pmatrix},
 \qquad
 \widehat Q(k_2)=
 \begin{pmatrix}0&-1/2&0\\-1/2&0&1\\0&1&0\end{pmatrix}.
 \tag{3.4}
\]

Consequently, for

\[
 w_k=2\operatorname{Re}
 \bigl(\overline{\widehat S(k)}:\widehat Q(k)\bigr),
 \qquad
 d_k=4|k|^2|\widehat S(k)|_F^2,
 \tag{3.5}
\]

the exact ledger is

\[
 w_{k_1}=2,
 \qquad w_{k_2}=-2,
 \qquad d_{k_1}=d_{k_2}=8.
 \tag{3.6}
\]

The two outputs lie on the same radius.  Their parent has zero work, but the
fine ledger is already

\[
 E_{\rm parent}(0)=0,
 \qquad
 E_{\rm leaves}(0)=\frac12,
 \qquad
 \delta(0)=\frac12.
 \tag{3.7}
\]

## 4. Viscosity creates positive parent work

Under Stokes evolution,

\[
 w_1(t)=2e^{-8\nu t},
 \qquad
 w_2(t)=-2e^{-14\nu t},
 \qquad
 d_1(t)=d_2(t)=8e^{-8\nu t}.
 \tag{4.1}
\]

The parent work is therefore

\[
 W(t)=2e^{-8\nu t}\bigl(1-e^{-6\nu t}\bigr)>0
 \qquad(t>0),
 \tag{4.2}
\]

although \(W(0)=0\).  This is a linear effect: the negative child depends on
faster input modes and decays more quickly.

At

\[
 t_1=\frac{\log2}{6\nu},
 \tag{4.3}
\]

the exact values are

\[
 E_{\rm parent}(t_1)=2^{-16/3},
 \qquad
 E_{\rm leaves}(t_1)=2^{-7/3},
 \qquad
 \delta(t_1)=7\,2^{-16/3}.
 \tag{4.4}
\]

Thus a signed shell sum has no heat-flow maximum principle even before the
nonlinear dynamics enter.

## 5. The true Navier--Stokes derivative

The Fourier vorticity equation is

\[
 \dot{\widehat\omega}(k)
 =-\nu|k|^2\widehat\omega(k)
 +i\sum_{p+q=k}
 \left[
 (\widehat\omega(p)\cdot q)\widehat u(q)
 -(\widehat u(p)\cdot q)\widehat\omega(q)
 \right].
 \tag{5.1}
\]

Write the nonlinear part as \(\widehat{\mathcal N}(k)\).  Direct convolution
gives 50 nonzero generated modes and preserves both divergence freedom and
Fourier reality.  The work derivative is

\[
 \dot w_k
 =2\operatorname{Re}
 \left(
 \overline{\dot{\widehat S}(k)}:\widehat Q(k)
 +\overline{\widehat S(k)}:\dot{\widehat Q}(k)
 \right),
 \tag{5.2}
\]

where the full derivative

\[
 \dot{\widehat Q}(k)=
 \sum_{r+s=k}
 \left(
 \dot{\widehat\omega}(r)\otimes\widehat\omega(s)
 +\widehat\omega(r)\otimes\dot{\widehat\omega}(s)
 \right)
 \tag{5.3}
\]

must include generated \(r\) or \(s\) outside the initial support.

For the unit-amplitude datum, the independent calculation gives

| output | Stokes contribution to \(\dot w\) | nonlinear contribution to \(\dot w\) |
|---|---:|---:|
| \(k_1\) | \(-16\nu\) | \(6\) |
| \(k_2\) | \(28\nu\) | \(46/5\) |
| parent sum | \(12\nu\) | \(76/5\) |

For an additional check, the two nonlinear terms in (5.2) split as

\[
 k_1:\quad -4+10=6,
 \qquad
 k_2:\quad -\frac85+\frac{54}{5}=\frac{46}{5}.
 \tag{5.4}
\]

Scaling every initial Fourier coefficient by \(\varepsilon>0\) makes the
linear work derivative cubic and the nonlinear one quartic.  Hence

\[
 \boxed{
 W'(0)=12\nu\varepsilon^3
 +\frac{76}{5}\varepsilon^4>0.}
 \tag{5.5}
\]

As a separate regression, the checker forms the complete first-order field
\(\varepsilon\omega+h\dot\omega\), rebuilds \(S\) and \(Q\) without using the
differentiated-work routine, and extracts the coefficient of \(h\).  The
residual against (5.5) is exactly zero.

The datum is a smooth trigonometric polynomial, so local smooth
Navier--Stokes evolution exists.  Equations (3.7) and (5.5) imply
\(W(t)>0\) for all sufficiently small positive times.

This calculation uses the full-response covariance
\(Q=\omega\otimes\omega\), equivalently the identity response.  For a
nontrivial fixed frame, newly generated frequencies in (5.3) carry response
correlations that need a separate calculation.  For an adaptive frame, the
frame derivative adds further terms.  No claim about those mechanisms follows
from (5.5).

## 6. Complete shell injection gives a conditional continuation quantity

Let \((T_\alpha)\) be fixed real Fourier multipliers satisfying the Parseval
identity

\[
 \sum_\alpha T_\alpha^*T_\alpha=I.
 \tag{6.1}
\]

Put

\[
 \Omega_\alpha=T_\alpha\omega,
 \qquad
 Y_\alpha=\|\Omega_\alpha\|_2^2,
 \qquad
 D_\alpha=\|\nabla\Omega_\alpha\|_2^2,
 \tag{6.2}
\]

and use the complete vorticity nonlinearity

\[
 \mathcal N(u,\omega)
 =S\omega-u\cdot\nabla\omega
 =\nabla\times(u\times\omega).
 \tag{6.3}
\]

Define the signed injection only after summing every interaction that lands
in the same output shell:

\[
 \boxed{
 b_\alpha
 =\langle T_\alpha\omega,
 T_\alpha\mathcal N(u,\omega)\rangle.}
 \tag{6.4}
\]

Because the multipliers commute with time differentiation and the
Laplacian,

\[
 \frac12Y_\alpha'+\nu D_\alpha=b_\alpha.
 \tag{6.5}
\]

Parseval gives

\[
 \sum_\alpha Y_\alpha=Y:=\|\omega\|_2^2,
 \qquad
 \sum_\alpha D_\alpha=D:=\|\nabla\omega\|_2^2,
 \tag{6.6}
\]

and incompressibility gives

\[
 \sum_\alpha b_\alpha
 =\langle\omega,\mathcal N(u,\omega)\rangle
 =\langle\omega,S\omega\rangle
 =:\mathfrak P.
 \tag{6.7}
\]

Set

\[
 \Theta_{{\rm sb},+}^2
 =\sum_{\alpha:D_\alpha>0}
 \frac{(b_\alpha^+)^2}{D_\alpha},
 \qquad
 A_{{\rm sb},+}
 =\frac{\Theta_{{\rm sb},+}^2}{Y},
 \tag{6.8}
\]

with the zero-field value defined as zero.  Then

\[
 \mathfrak P_+
 \leq\sum_\alpha b_\alpha^+
 \leq\sqrt D\,\Theta_{{\rm sb},+}
 \leq\frac\nu2D+\frac1{2\nu}\Theta_{{\rm sb},+}^2.
 \tag{6.9}
\]

The enstrophy identity therefore implies

\[
 Y'+\nu D\leq\nu^{-1}A_{{\rm sb},+}Y.
 \tag{6.10}
\]

For a maximal \(H^1\) strong solution on \([0,T_*)\), the condition

\[
 \int_0^{T_*}A_{{\rm sb},+}(t)\,dt<\infty
 \tag{6.11}
\]

bounds \(Y\) by Gronwall, also bounds \(\int_0^{T_*}D\), and permits the
standard strong-solution continuation beyond \(T_*\).

This is a conditional reduction, not an unconditional regularity theorem.
Under the usual Navier--Stokes critical scaling (with the shell index shifted),
\(Y,D,b_\alpha,\Theta^2,A\) have exponents
\(1,3,3,3,2\), respectively.  Thus \(A\,dt\) is critical, but the calculation
does not prove its integrability.

## 7. Signed interval masses have the wrong Cauchy direction

For a time interval \(I=[t_0,t_1]\), equation (6.5) gives

\[
 \beta_{\alpha,I}:=\int_I b_\alpha\,dt
 =\frac12\bigl(Y_\alpha(t_1)-Y_\alpha(t_0)\bigr)
 +\nu\int_I D_\alpha\,dt.
 \tag{7.1}
\]

However, whenever \(\int_I D_\alpha\,dt>0\),

\[
 \boxed{
 \frac{(\beta_{\alpha,I}^+)^2}{\int_I D_\alpha\,dt}
 \leq
 \int_I\frac{(b_\alpha^+)^2}{D_\alpha}\,dt.}
 \tag{7.2}
\]

The inequality follows from
\(\beta^+\leq\int_Ib^+\) and weighted Cauchy.  It is a lower bound on the
consumer, whereas closure needs an upper bound.

An exact scalar ledger shows that the gap can be arbitrarily large.  On
\(I=[0,2\pi]\), for an integer \(N\), take

\[
 Y_N(t)=1+\frac12\sin Nt,
 \qquad
 D_N(t)=Y_N(t),
 \qquad
 b_N(t)=\frac12Y_N'(t)+D_N(t).
 \tag{7.3}
\]

This path satisfies the shell identity with \(\nu=1\), while

\[
 \int_IY_N=\int_ID_N=\int_Ib_N=2\pi
 \tag{7.4}
\]

for every \(N\).  Hence the signed box quotient is always \(2\pi\).
On the set \(\{\cos Nt\geq1/2\}\), whose measure is \(2\pi/3\),

\[
 b_N^+\geq\frac N8,
 \qquad
 D_N\leq\frac32.
\]

It follows that

\[
 \int_I\frac{(b_N^+)^2}{D_N}\,dt
 \geq\frac{\pi N^2}{144}\longrightarrow\infty.
 \tag{7.5}
\]

This path is not claimed to come from Navier--Stokes.  It proves only that
the shell energy identity, its endpoint telescoping, and integrated
dissipation cannot reverse (7.2).  Any successful upper bound must use more
of the PDE.

## 8. A three-mode normalization discontinuity

The positive-output quotient has a separate static defect at a zero strain
coefficient.  Let

\[
 p=(1,1,0),\qquad q=(1,-1,0),\qquad k=(2,0,0),
 \tag{8.1}
\]

and choose

\[
 a=e_3,\qquad
 b=\frac{e_1+e_2}{\sqrt2},\qquad
 c=-e_2.
 \tag{8.2}
\]

For \(A,B,\eta>0\), define

\[
 \omega_\eta
 =Aa\cos(p\cdot x)+Bb\cos(q\cdot x)
 +\eta c\cos(k\cdot x).
 \tag{8.3}
\]

Use the exact-radius Parseval response

\[
 \Gamma(r,s)=\mathbf1_{\{|r|^2=|s|^2\}}.
 \tag{8.4}
\]

Since \(|p|=|q|\ne|k|\), the only nonzero covariance work is at
\(k\).  The independent Fourier calculation gives

\[
 \widehat S_\eta(k)
 =\frac\eta4(e_1\otimes e_3+e_3\otimes e_1),
 \qquad
 |\widehat S_\eta(k)|_F^2=\frac{\eta^2}{8},
 \tag{8.5}
\]

and

\[
 w_k=\frac{\sqrt2}{8}AB\eta.
 \tag{8.6}
\]

Therefore the single positive-output term is exactly

\[
 \frac{(w_k^+)^2}
 {4|k|^2|\widehat S_\eta(k)|_F^2}
 =\boxed{\frac{A^2B^2}{64}},
 \tag{8.7}
\]

independent of \(\eta>0\).  Meanwhile,

\[
 Y_\eta=\|\omega_\eta\|_2^2
 =\frac{A^2+B^2+\eta^2}{2}.
 \tag{8.8}
\]

Thus the normalized coefficient is

\[
 a_+(\omega_\eta)
 =\frac{A^2B^2}
 {32(A^2+B^2+\eta^2)},
 \tag{8.9}
\]

and

\[
 \liminf_{\eta\downarrow0}a_+(\omega_\eta)
 =\frac{A^2B^2}{32(A^2+B^2)}>0.
 \tag{8.10}
\]

At \(\eta=0\), the output strain vanishes.  Under the stated zero-denominator
convention the quotient is zero, and the other output works also vanish, so

\[
 a_+(\omega_0)=0.
 \tag{8.11}
\]

The fields converge in every fixed Sobolev space, but the normalized
coefficient does not.  This rules out treating that raw same-output quotient
as a continuous propagated state variable without additional information.
It does not rule out every regularized denominator or prove that an NSE
trajectory must cross this zero set.

## 9. A balanced HHL datum creates positive work immediately

For \(M\in\{8,64\}\), write

\[
\begin{aligned}
 n&=(1,1,0),\\
 p_M&=(M,-M-1,0),\\
 q_M&=(-M-1,M,0),\\
 R_M^2&=2M^2+2M+1,
\end{aligned}
 \tag{9.1}
\]

and set

\[
 c=\frac{(1,-1,0)}{\sqrt2},\qquad
 a=e_3,\qquad
 b_M=\frac{(M,M+1,0)}{R_M},\qquad
 h_M=\frac{2M+1}{\sqrt2R_M}.
 \tag{9.2}
\]

Consider

\[
\begin{aligned}
 \Omega={}&c\cos(n\cdot x)
 +h_{64}a\cos(p_8\cdot x)
 +b_8\cos(q_8\cdot x)\\
 &+h_8a\cos(p_{64}\cdot x)
 -b_{64}\cos(q_{64}\cdot x).
\end{aligned}
 \tag{9.3}
\]

Use the same exact-radius response (8.4).  The signed support has ten modes
and exactly 24 ordered zero-sum resonances.  Direct reconstruction checks
every representative of the five Fourier pairs.  All five output works are
zero.  At the shared low output, the two individual contributions are

\[
 c_0=\frac{h_8h_{64}}4
 =\frac{2193}{8\sqrt{1206545}},
 \qquad -c_0,
 \tag{9.4}
\]

and all high-output works vanish by response separation.  Hence the complete
positive-output coefficient is zero at the initial time.

### 9.1 Heat evolution

For the scaled datum \(\delta\Omega\), Stokes evolution gives

\[
 \boxed{
 w_n^{H}(t)
 =\delta^3c_0e^{-2\nu t}
 \left(e^{-290\nu t}-e^{-16642\nu t}\right)>0
 \quad(t>0).}
 \tag{9.5}
\]

The output dissipation weight is
\(d_n(t)=\delta^2e^{-4\nu t}\).  Thus its positive-output contribution is

\[
 \mathcal T_{+,n}^2(t)
 =\delta^4c_0^2
 \left(e^{-290\nu t}-e^{-16642\nu t}\right)^2.
 \tag{9.6}
\]

The heat derivative at zero is

\[
 \frac{d}{dt}w_n^H(0)
 =\delta^3\nu
 \frac{4482492\sqrt{1206545}}{1206545}>0.
 \tag{9.7}
\]

### 9.2 True Navier--Stokes evolution

The independent checker forms the complete quadratic Fourier nonlinearity
before applying the response.  It finds 24 nonzero derivative modes, 18 of
them outside the initial support.  None of those 18 modes can pair with an
initial mode at output \(n\) while also passing the exact-radius response.
This is a calculated consequence of the response, not a support truncation.
Exactly four ordered pairs contribute to the first-order target covariance.

The exact linear and quartic target rates are

\[
 L_n
 =\nu\frac{4482492\sqrt{1206545}}{1206545},
 \qquad
 N_n=\frac{4809249}{19304720}.
 \tag{9.8}
\]

Therefore the smooth NSE solution with initial vorticity \(\delta\Omega\)
satisfies

\[
\boxed{
 w_n'(0)
 =\frac{2193\delta^3}{19304720}
 \left(
 2193\delta+32704\sqrt{1206545}\,\nu
 \right)>0.}
 \tag{9.9}
\]

The quartic rates at the other four initial output representatives are all
zero.  As a separate regression, the checker rebuilds the complete
first-order target polynomial and extracts its time coefficient without
calling the differentiated-covariance routine; the residual against (9.9)
is exactly zero.

This is stronger than a small-amplitude sign argument because both terms in
(9.9) are positive.  It rules out a homogeneous zero-preserving Gronwall
propagation for this fixed exact-radius positive-output coefficient.  It does
not exclude an additive source estimate, a different fixed frame, or an
adaptive localization carrying its own time-derivative and flux terms.

## 10. Exact claim boundary

The audit proves the following.

1. Finite signed-before-square ledgers are monotone under refinement, and
   their binary losses telescope as nonnegative defects.
2. The stated full-response two-triad parent starts with zero signed work and
   acquires positive work immediately under both Stokes and true smooth NSE
   evolution.
3. The complete shell-injection coefficient gives a scale-critical
   conditional continuation theorem.
4. Signed interval mass controls only a lower bound for the needed positive
   square variation.
5. The raw same-output normalization is discontinuous when the output strain
   tends to zero through the three-mode family.
6. The balanced \(M=8,64\) HHL datum has no initial positive output but
   creates positive low-output work immediately under heat and true NSE.

It does not prove any of the following.

- a no-go for every adaptive or PDE-specific localization;
- a no-go for a flux identity that controls the refinement defects;
- a no-go for every regularized denominator or every fixed frame;
- unconditional integrability of \(A_{{\rm sb},+}\) or the R0.71B
  coefficient;
- realization of the scalar path (7.3) by NSE;
- regularity or blow-up for the three-dimensional Navier--Stokes problem.

## 11. Reproduction

From the repository root, using the pinned research environment:

```text
tmp/r068b-venv/bin/python research/r071c_independent_audit.py \
  --output /tmp/r071c-independent.json
```

The command exits successfully only after every exact assertion passes.
