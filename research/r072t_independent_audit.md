# R0.72T independent analytic audit

**Date:** 2026-08-28

**Audit outcome:** the exact local identities, scaling, inviscid propagator,
van der Corput estimate, bracket length, and drift-only constants are
internally consistent.  The full cubic-model contraction is not proved and is
correctly marked open.

## 1. Exact-profile audit

Starting from the R0.72S physical heat path and inserting
\(y=\log2+d\), \(\phi=\pi/2+x\) gives

\[
 W(d,x)=\frac12e^{-d}
 \left[-\sin x+\frac12e^{-3d}\sin2x\right].
\]

Direct differentiation verifies \(W_d=W_{xx}\).  At \(d=0\), the coefficients
of \(x^3,x^5,x^7\) are respectively

\[
 -\frac14,\qquad \frac1{16},\qquad -\frac1{160}.
\]

Applying \(e^{d\partial_x^2}\) gives exactly

\[
 -\frac14H_3+\frac1{16}H_5-\frac1{160}H_7,
\]

with the next term at parabolic weight nine.  This also confirms that the
velocity germ is cubic plus spacetime linear.  The quadratic expression is
the derivative germ, not the primitive entering the Fourier-mode PDE.

## 2. Scaling audit

Let \(X=\kappa^ax\), \(S=\kappa^bd\).  Equalizing

\[
 b,\quad 2a,\quad 1-3a,\quad 1-a-b
\]

gives \(a=1/5\), \(b=2/5\), uniquely.  Under this scaling,

\[
 \kappa H_3(d,x)=\kappa^{2/5}H_3(S,X),
\]

\[
 \frac\kappa4H_5(d,x)
 =\frac14\kappa^{-2/5}\kappa^{2/5}H_5(S,X),
\]

and

\[
 \frac\kappa{40}H_7(d,x)
 =\frac1{40}\kappa^{-4/5}\kappa^{2/5}H_7(S,X).
\]

The signs in the report follow from
\(-i\sigma\varepsilon_cW\) and \(\varepsilon_c=4\kappa\):

\[
 +i\sigma H_3,\qquad
 -i\sigma\frac{\kappa^{-2/5}}4H_5,\qquad
 +i\sigma\frac{\kappa^{-4/5}}{40}H_7.
\]

## 3. Gauge and translation audit

A scalar potential \(A(S)\) is removed by a time-dependent scalar phase.  For
\(H_3(S,Y+c)\), the coefficients of \(Y^2\) and \(Y\) are \(3c\) and
\(3c^2+6S\).  A real translation that removes the quadratic term has \(c=0\),
so it cannot also remove \(6SY\).  The report limits this no-go statement to
real translations and scalar gauges; it does not exclude more general
canonical or nonunitary transforms.

For the separate incorrect model
\[
 z_t+ik[A(t)+bx^2]z=\nu z_{xx},
\]
the time-only term is gauge removable.  When \(b\ne0\), the unitary dilation
\(x=(\nu/|kb|)^{1/4}y\) puts both diffusion and the quadratic potential at
size \((\nu|kb|)^{1/2}\).  The corresponding time scale is therefore
\[
 (\nu|kb|)^{-1/2}.
\]
This agrees with the complex harmonic-oscillator scaling discussed by Viola
(<https://arxiv.org/abs/1512.02558>).  It is not a result for the combined
model \(X^3+6SX\).

## 4. Inviscid and van der Corput audit

Integrating \(H_3(S,X)=X^3+6SX\) from \(S_0\) to \(S_1\) gives

\[
 (S_1-S_0)X^3+3(S_1^2-S_0^2)X.
\]

For \(S_0=-T/2\), \(S_1=T/2\), the linear term is zero.  The third derivative
of the phase is \(6T\) for every starting time, so the order-three van der
Corput estimate is uniform in \(S_0\).  The amplitude bounds

\[
 \|f\bar g\|_\infty+\|(f\bar g)'\|_1
 \le C\|f\|_{H^1}\|g\|_{H^1}
\]

are valid in one dimension.  Duality therefore gives the reported
\(H^1\to H^{-1}\) rate \(T^{-1/3}\).

The CDZE substitution is also correct:

\[
 p=\frac13
 \quad\Longrightarrow\quad
 q=\frac{2}{2+p}=\frac67.
\]

It cannot be reported as the desired \(3/5\) estimate.

## 5. Bracket audit

With

\[
 X_1=\partial_X,
 \qquad X_0=\partial_S-H_3\partial_\theta,
\]

Three commutators with \(X_1\) give

\[
 -(3X^2+6S)\partial_\theta,qquad
 -6X\partial_\theta,qquad
 -6\partial_\theta.
\]

The independent mixed bracket is
\[
 [X_0,[X_1,X_0]]=-6\partial_\theta.
\]
Assigning weights \(1\) and \(2\) to \(X_1\) and \(X_0\) places the generated
direction at both \(1+1+1+2=5\) and \(2+(1+2)=5\).  This is a qualitative
spanning audit, not a proof of the quantitative estimate needed for
contraction.

## 6. Drift-only constant audit

Center a block of length \(T\) at time \(m\), and write its local time as
\(r\in[-T/2,T/2]\).  After optimizing the incoming frequency, the relevant
centered characteristic is

\[
 a\left[mr+\frac12\left(r^2-\frac{T^2}{12}\right)\right].
\]

The odd/even cross term integrates to zero, while

\[
 \int_{-T/2}^{T/2}r^2\,dr=\frac{T^3}{12},
\]

\[
 \int_{-T/2}^{T/2}
 \left[\frac12\left(r^2-\frac{T^2}{12}\right)\right]^2dr
 =\frac{T^5}{720}.
\]

Hence the minimum action is

\[
 a^2\left(\frac{m^2T^3}{12}+\frac{T^5}{720}\right),
\]

and the \(L^2\)-operator norm is its negative \(\nu\)-exponential.  For fixed
\(f\), the same zero-mean decomposition removes the magnetic cross term and
gives

\[
 \int_{-T/2}^{T/2}
 \left\|\left(\partial_x-
 \frac{ia}{2}\left(r^2-\frac{T^2}{12}\right)\right)f\right\|_2^2dr
 =T\|f'\|_2^2+\frac{a^2T^5}{720}\|f\|_2^2.
\]

The coefficient \(1/720\) is therefore verified in two independent forms.

For the physical heat-path germ, \(a=kA\nu\).  Solving
\(\nu a^2T^5\asymp1\) gives
\[
 T\asymp |kA|^{-2/5}\nu^{-3/5},
\]
which verifies the physical back-substitution.

For the combined potential \(V(S,X)=aSX+bX^3\), set
\[
 A_r(X)=(ac+3bX^2)r+\frac a2r^2,\qquad
 A_{\rm av}=\frac{aT^2}{24},
\]
on a block centered at \(c\), and let
\(D_r=\partial_X-iA_r\), \(D_{\rm av}=\partial_X-iA_{\rm av}\).
The same odd/even calculation gives, for one fixed \(f\),
\[
 \begin{aligned}
 \int_{-T/2}^{T/2}\|D_rf\|_2^2\,dr
 ={}&T\|D_{\rm av}f\|_2^2\\
 &+\int_{\mathbb R}\left[
 \frac{(ac+3bX^2)^2T^3}{12}
 +\frac{a^2T^5}{720}\right]|f|^2\,dX.
 \end{aligned}
\]
The audit confirms this algebraic identity but rejects its use as a
solution-observability estimate: the solution itself evolves with \(r\).

## 7. Failure-mode audit

The following tempting inferences are invalid.

1. **Local convergence is not global perturbation theory.**  The \(H_5\) and
   \(H_7\) corrections are small on bounded scaled charts but unbounded in
   \(X\).
2. **Inviscid mixing is not viscous contraction.**  The available abstract
   conversion yields \(6/7\) and its compactness assumptions fail on the
   global line.
3. **The drift-only norm is not the cubic-model norm.**  Adding \(X^3\)
   changes the Fourier equation from first-order transport to a higher-order
   equation.
4. **Hörmander spanning is not a uniform decay estimate.**  A quantitative
   global Poincaré/observability statement, including the
   \(L^2_SH^{-1}_X\) transport residual and all-start endpoint control, is
   still absent.
5. **A collision model is not a nonlinear Navier--Stokes theorem.**  No
   vortex-stretching or nonlinear bootstrap estimate appears here.

The audit therefore accepts the following release boundary and no stronger
one:

\[
 \boxed{
 \texttt{blockContraction=OPEN},\quad
 \texttt{periodicTransfer=OPEN},\quad
 \texttt{Clay=OPEN}.}
\]
