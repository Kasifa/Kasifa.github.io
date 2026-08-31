# R0.73T dynamic autocorrelation budget

**Status:** self-contained analytic reconstruction; constants, exact examples,
and literature attribution are audited separately

**Domain:** \(\mathbb T^3=[0,2\pi]^3\) with normalized Haar measure
\(d\mu=(2\pi)^{-3}dx\)

**Equation:**

\[
 \partial_tu+(u\cdot\nabla)u+\nabla p=\nu\Delta u,
 \qquad \nabla\cdot u=0,
 \qquad \int_{\mathbb T^3}u\,d\mu=0,
 \tag{0.1}
\]

with \(\nu>0\).  The differential identities below are classical for a
smooth solution.  Whenever a Fourier series is rearranged, one may first
truncate the fields at a fixed time and then pass to the limit using their
smooth periodic decay; no claim that a Navier--Stokes solution remains
finite-spectrum is being made.

## 1. Scalar autocorrelation data

Write

\[
 w=|u|^2,
 \qquad
 C_h=\widehat w(h)
 =\int_{\mathbb T^3}w(x)e^{-ih\cdot x}\,d\mu(x).
 \tag{1.1}
\]

The scalar quantities inherited from R0.73S are

\[
 Q=\sum_h|C_h|^2=\|u\|_4^4,
 \qquad
 A=\sum_h|C_h|,
 \tag{1.2}
\]

and the exact static inequality is

\[
 \|u\|_6^6=\int w^3\,d\mu\le A Q.
 \tag{1.3}
\]

The quantity \(A\) is the Wiener norm of the energy density, not the Wiener
norm of the velocity.  It is finite for a smooth periodic field, but its
finiteness at each subcritical time does not imply a uniform or integrable
bound near a possible maximal time.

## 2. Exact coefficient evolution

Taking the scalar product of (0.1) with \(2u\) yields

\[
 \partial_tw+u\cdot\nabla w+2u\cdot\nabla p
 =\nu\Delta w-2\nu|\nabla u|^2.
 \tag{2.1}
\]

Because \(\nabla\cdot u=0\), this is equivalently

\[
 \partial_tw
 =\nu\Delta w-2\nu|\nabla u|^2
  -\nabla\cdot\bigl(u(w+2p)\bigr).
 \tag{2.2}
\]

Fourier transformation therefore gives the exact law

\[
 \boxed{
 \dot C_h
 =-\nu|h|^2C_h
  -2\nu\widehat{|\nabla u|^2}(h)
  -ih\cdot\widehat{u(w+2p)}(h).}
 \tag{2.3}
\]

Two omissions would make (2.3) false: viscosity is not represented only by
\(-\nu|h|^2C_h\), and pressure cannot be cancelled together with transport.
The law retains the signed vector flux \(u(w+2p)\), which scalar \(C\) does
not determine even if \(p\) is supplied.  Separately, reconstructing \(p\)
in general requires the full tensor \(T_{ij}=u_i u_j\) through
\(p=R_iR_jT_{ij}\), whereas \(C=\widehat{\operatorname{tr}T}\) contains only
its trace.  These are distinct missing-information mechanisms.

## 3. Exact quartic balance

Set

\[
 X^2=\|\nabla w\|_2^2,
 \qquad
 Y=\int_{\mathbb T^3}w|\nabla u|^2\,d\mu.
 \tag{3.1}
\]

Multiply (2.1) by \(2w\) and integrate.  The transport term vanishes:

\[
 \int 2w\,u\cdot\nabla w\,d\mu
 =\int u\cdot\nabla(w^2)\,d\mu=0.
 \tag{3.2}
\]

Periodic integration by parts gives

\[
 2\nu\int w\Delta w\,d\mu=-2\nu X^2,
 \qquad
 -4\int w\,u\cdot\nabla p\,d\mu
 =4\int p\,u\cdot\nabla w\,d\mu.
 \tag{3.3}
\]

Consequently

\[
 \boxed{
 Q'+4\nu Y+2\nu X^2
 =4\int_{\mathbb T^3}p\,u\cdot\nabla w\,d\mu.}
 \tag{3.4}
\]

This is the standard \(L^4\) balance reconstructed through the Fourier
autocorrelation.  It is an identity, not a regularity theorem.

## 4. One-sided dynamic use of the R0.73S certificate

The mean-zero pressure obeys

\[
 -\Delta p=\partial_i\partial_j(u_i u_j),
 \qquad
 p=R_iR_j(u_i u_j),
 \tag{4.1}
\]

where the sign convention is absorbed in the periodic Riesz transforms.  Let
\(C_R\) be a valid \(L^3\) operator constant after summing the finitely many
tensor components.  Calderón--Zygmund boundedness gives

\[
 \|p\|_3\le C_R\|u\otimes u\|_3
 \le C_R\|u\|_6^2.
 \tag{4.2}
\]

Hölder and Young, with
\(a=\sqrt\nu X\) and
\(b=2C_R\nu^{-1/2}\|u\|_6^3\), give

\[
\begin{aligned}
 4\left|\int p\,u\cdot\nabla w\,d\mu\right|
 &\le4C_R\|u\|_6^3X\\
 &\le\nu X^2+{4C_R^2\over\nu}\|u\|_6^6.
\end{aligned}
 \tag{4.3}
\]

Combining (3.4), (4.3), and (1.3) proves the main R0.73T estimate:

\[
 \boxed{
 Q'+4\nu Y+\nu X^2
 \le {4C_R^2\over\nu}A Q.}
 \tag{4.4}
\]

In particular,

\[
 Q(t)\le Q(0)
 \exp\!\left({4C_R^2\over\nu}\int_0^tA(s)\,ds\right)
 \tag{4.5}
\]

for every smooth interval on which the integral is finite.

### Conditional continuation statement

If \(T_*<\infty\) is a maximal strong-solution time and

\[
 \int_0^{T_*}A(t)\,dt<\infty,
 \tag{4.6}
\]

then (4.5) bounds \(u\) in \(L_t^\infty L_x^4\) up to \(T_*\).  The
classical Prodi--Serrin continuation criterion then extends the solution.
This implication is not a new regularity criterion, because (4.6) is at
least as restrictive as a classical endpoint criterion, as shown next.

## 5. Scaling and classical-strength boundary

Under the Navier--Stokes rescaling

\[
 u^{[\lambda]}(x,t)=\lambda u(\lambda x,\lambda^2t),
 \tag{5.1}
\]

using integer \(\lambda\) on the fixed torus, the nonzero Fourier
coefficients of \(|u^{[\lambda]}|^2\) are the dilated coefficients of
\(|u|^2\), each multiplied by \(\lambda^2\).  Hence

\[
 A^{[\lambda]}(t)=\lambda^2A(\lambda^2t),
 \qquad
 \int_0^{T/\lambda^2}A^{[\lambda]}(t)\,dt
 =\int_0^TA(s)\,ds.
 \tag{5.2}
\]

Thus the missing time integral is scale critical.  Fourier inversion also
gives

\[
 \|u(t)\|_\infty^2
 =\||u(t)|^2\|_\infty
 \le\sum_h|C_h(t)|=A(t).
 \tag{5.3}
\]

Therefore

\[
 A\in L_t^1
 \quad\Longrightarrow\quad
 u\in L_t^2L_x^\infty.
 \tag{5.4}
\]

The right side is the time-exponent-\(2\), space-exponent-\(\infty\) end of
the classical Prodi--Serrin scaling line.  Thus \(A\in L_t^1\) is at
least as restrictive as, and directly implies, the classical
\(L_t^2L_x^\infty\) hypothesis.  This is the spatial-\(L^\infty\) end of the
LPS line, not the delicate \(L_t^\infty L_x^3\) endpoint.  R0.73T has
converted a static autocorrelation certificate into dynamics, but has not
weakened the known critical continuation threshold.

## 6. Why differentiating \(A\) does not close the system

Because coefficients may cross zero, use the upper Dini derivative.  From
(2.3),

\[
 D^+A+\nu\sum_h|h|^2|C_h|
 \le2\nu\sum_h\left|\widehat{|\nabla u|^2}(h)\right|
 +\sum_h|h|\left|\widehat{u(w+2p)}(h)\right|.
 \tag{6.1}
\]

The first term requires derivative-weighted Wiener control of \(u\); the
second requires one more derivative on a cubic pressure flux.  Neither is a
function of \((A,Q,\|u\|_2)\).  Thus differentiating \(AQ\) merely moves the
unknown into stronger Wiener norms.

A resolution-independent but superlinear fallback can be obtained from
Gagliardo--Nirenberg and Young:

\[
 Q'\le C\left(\nu^{-7}Q^3+\nu^{-1}Q^{3/2}\right).
 \tag{6.2}
\]

Its comparison ODE can blow up in finite time, so (6.2) supplies local
control only.

## 7. Exact non-autonomy of scalar autocorrelation

For every integer \(n\ge1\), define

\[
 u^{(n)}(x)=\bigl(0,\cos(nx_1),\sin(nx_1)\bigr).
 \tag{7.1}
\]

Then \(u^{(n)}\) is real, mean zero, divergence free,
\((u^{(n)}\cdot\nabla)u^{(n)}=0\), and \(|u^{(n)}|^2\equiv1\).  Every
member therefore has the same complete scalar autocorrelation,

\[
 C_h=\mathbf1_{h=0},
 \qquad A=Q=1,
 \tag{7.2}
\]

while the exact heat solution gives

\[
 \dot C_0(0)=-2\nu n^2,
 \qquad Q'(0)=-4\nu n^2.
 \tag{7.3}
\]

Complete unweighted \(C\) therefore loses absolute carrier frequency even
before nonlinear effects are present.

There is an independent loss of signed velocity phase in the pressure
pairing.  The exact six-mode field

\[
 u(x,y)=
 \bigl(6\sin y-4\sin(x+y),\;4\sin x+4\sin(x+y),\;0\bigr)
 \tag{7.4}
\]

has

\[
 \mathcal E=\|u\|_2^2=42,
 \qquad Q=2918,
 \qquad A=164,
 \qquad D_C=15,
 \tag{7.5}
\]

and pressure contribution

\[
 \mathcal N_4(u)
 :=4\int p\,u\cdot\nabla|u|^2\,d\mu=-384.
 \tag{7.6}
\]

For \(u_L(x)=u(Lx)\), the data in (7.5) remain fixed and all velocity modes
lie in \(L\le|k|\le\sqrt2L\), but

\[
 \mathcal N_4(u_L)=-384L,
 \qquad
 \mathcal N_4(-u_L)=+384L.
 \tag{7.7}
\]

The pair \(u_L,-u_L\) has identical complete scalar \(C\).  In fact

\[
 (-u_L)\otimes(-u_L)=u_L\otimes u_L,
 \qquad p[-u_L]=p[u_L],
 \tag{7.8}
\]

so its tensor and mean-zero pressure are identical.  The signed pressure
work differs solely because the leading velocity factor in
\(p\,u\cdot\nabla|u|^2\) changes sign.  Thus this witness isolates signed
velocity phase missing from \(C\); it is not, by itself, a witness that
scalar \(C\) fails to determine pressure-tensor polarization.  The latter
general barrier follows separately from \(p=R_iR_j(u_i u_j)\) and the fact
that \(C\) records only the tensor trace.  The common viscous contribution
is of order \(-\nu L^2\), so this example does not contradict the one-sided
estimate (4.4).  It is a smooth information-and-scaling witness, not a
singular or near-singular solution.

## 8. Shellwise transport

Let \(P_j\) be a real self-adjoint Littlewood--Paley projection to a fixed
annulus \(|k|\asymp\lambda_j=2^j\), with Fourier symbol \(m_j\).  Put

\[
 v_j=P_ju,
 \qquad
 \mathcal F_j=P_j\mathbb P\nabla\cdot(u\otimes u),
 \qquad
 Q_j=\|v_j\|_4^4,
 \qquad
 A_j=\sum_h\left|\widehat{|v_j|^2}(h)\right|.
 \tag{8.1}
\]

The fixed ambient shell support and its difference set are

\[
 \Sigma_j=\{k\in\mathbb Z^3:m_j(k)\ne0\},
 \qquad
 \overline D_j=|\Sigma_j-\Sigma_j|.
 \tag{8.1a}
\]

Both \(v_j\) and \(\mathcal F_j\) have Fourier support in \(\Sigma_j\).

The exact shell law is

\[
 \boxed{
 {1\over4}Q_j'+\nu\mathcal D_j
 =-\int |v_j|^2v_j\cdot\mathcal F_j\,d\mu,}
 \tag{8.2}
\]

where

\[
 \mathcal D_j
 =\int |v_j|^2|\nabla v_j|^2\,d\mu
 +{1\over2}\|\nabla|v_j|^2\|_2^2.
 \tag{8.3}
\]

The periodic scalar frequency-localized nonlinear Bernstein inequality at
\(p=4\), applied componentwise, gives

\[
 \mathcal D_j\ge c_B\lambda_j^2Q_j
 \tag{8.4}
\]

for a constant depending only on the fixed cutoff.  This is classical input.
Indeed, for each component \(v_{j,i}\),

\[
 3\int v_{j,i}^2|\nabla v_{j,i}|^2\,d\mu
 =-\int(\Delta v_{j,i})v_{j,i}^3\,d\mu
 \ge c\lambda_j^2\|v_{j,i}\|_4^4.
 \tag{8.5}
\]

Since \(\mathcal D_j\ge\sum_i\int
v_{j,i}^2|\nabla v_{j,i}|^2d\mu\) and
\((\sum_i v_{j,i}^2)^2\le3\sum_i v_{j,i}^4\), this proves (8.4)
without requiring a separately stated vector theorem.  Let

\[
 F_j=\|\mathcal F_j\|_2,
 \qquad
 Y_j=Q_j^{1/2},
 \qquad
 X_j=Q_j^{1/4}.
 \tag{8.6}
\]

Using \(\|v_j\|_6^6\le A_jQ_j\) in (8.2) gives, in the upper-Dini sense
through zeros,

\[
 \boxed{
 D^+Y_j+2\nu c_B\lambda_j^2Y_j
 \le2A_j^{1/2}F_j.}
 \tag{8.7}
\]

The fixed support bound
\(A_j\le\overline D_j^{1/2}X_j^2\) gives

\[
 \boxed{
 D^+X_j+\nu c_B\lambda_j^2X_j
 \le \overline D_j^{1/4}F_j.}
 \tag{8.8}
\]

For \(X_j>0\), this follows by dividing (8.2) by \(X_j^3\).  If
\(X_j(t_0)=0\), then
\[
 D^+X_j(t_0)=\|\partial_tv_j(t_0)\|_4
 \le\overline D_j^{1/4}\|\mathcal F_j(t_0)\|_2,
\]
by the finite-spectrum \(L^2\)-to-\(L^4\) inequality on \(\Sigma_j\).
Thus the fixed ambient count, unlike the instantaneous support of
\(\widehat{|v_j|^2}\), makes (8.8) valid through zeros.

The Duhamel forms are

\[
\begin{aligned}
 Y_j(t)&\le e^{-2\nu c_B\lambda_j^2(t-s)}Y_j(s)\\
 &\quad+2\int_s^t e^{-2\nu c_B\lambda_j^2(t-r)}
 A_j(r)^{1/2}F_j(r)\,dr,
\end{aligned}
 \tag{8.9}
\]

and

\[
\begin{aligned}
 X_j(t)&\le e^{-\nu c_B\lambda_j^2(t-s)}X_j(s)\\
 &\quad+\overline D_j^{1/4}\int_s^t
 e^{-\nu c_B\lambda_j^2(t-r)}F_j(r)\,dr.
\end{aligned}
 \tag{8.10}
\]

The elementary forcing estimates

\[
 F_j\lesssim\lambda_j\|u\|_4^2,
 \qquad
 F_j\lesssim\lambda_j^{5/2}\|u\|_2^2
 \tag{8.11}
\]

show the remaining barrier precisely.  The first branch reintroduces the
full-field strong \(L_x^4\) quantity being transported; its
Serrin-critical spacetime budget is \(u\in L_t^8L_x^4\), equivalently
\(\|u\|_4^2\in L_t^4\).  The energy-only branch grows supercritically with
shell frequency.  Equations (8.9)--(8.10) are conditional transport
certificates, not an energy-class closure.

## 9. Heat-weighted variants and the next exact target

For \(s\ge0\), set

\[
 v_s=e^{s\Delta}u,
 \qquad
 R_s=e^{s\Delta}\mathbb P\nabla\cdot(u\otimes u),
 \qquad
 Q_s=\|v_s\|_4^4.
 \tag{9.1}
\]

Because \((\partial_t-\nu\partial_s)v_s=-R_s\),

\[
 \boxed{
 (\partial_t-\nu\partial_s)Q_s
 =-4\int|v_s|^2v_s\cdot R_s\,d\mu,}
 \tag{9.2}
\]

while

\[
 \partial_sQ_s
 =-2\|\nabla|v_s|^2\|_2^2
  -4\int|v_s|^2|\nabla v_s|^2\,d\mu\le0.
 \tag{9.3}
\]

Heat weighting restores an absolute parabolic scale, but

\[
 e^{s\Delta}\mathbb P\nabla\cdot(u\otimes u)
 \ne
 \mathbb P\nabla\cdot(v_s\otimes v_s).
 \tag{9.4}
\]

The difference is a bilinear heat commutator.  A useful next theorem must
control its signed pairing in (9.2) at the R0.73Q/R0.73R critical exponents.
Scalar shift weights alone cannot recover the signed velocity phase: the
pair \(u_L,-u_L\) continues to have identical weighted scalar
autocorrelations, identical \(u\otimes u\) and pressure, but different
weighted derivatives.

## 10. Exact conclusion

R0.73T proves one positive statement and two negative boundaries.

1. The static R0.73S quantity \(AQ\) enters the exact \(L^4\) dynamics
   through (4.4).
2. The time integral required to close that inequality is scale critical,
   at least as restrictive as, and directly implies the classical
   \(L_t^2L_x^\infty\) condition.
3. Scalar autocorrelation loses both carrier frequency and the signed
   velocity phase entering \(u(w+2p)\).  Independently, general pressure
   reconstruction needs the full tensor \(u_i u_j\), not only its scalar
   trace, so \(C\) cannot be an autonomous state variable.

The next mathematically justified branch is a tensor-aware, scale-aware
heat or shell hierarchy with a signed commutator estimate.  No arbitrary-data
global regularity result, blow-up exclusion, or Clay conclusion follows here.
