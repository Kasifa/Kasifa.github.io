# R0.72W independent analytic audit

**Date:** 2026-08-28

**Audit outcome:** **PASS** for the global analytic-tail envelope, the
growing-core absorption theorem, the no-go to global termwise absorption, the
uniform exact-family unit-cell theorem, both negative-Sobolev
globalizations, and the exact periodic energy-block contraction.  **PASS with
an explicit claim boundary** for the numerical stress test: it is
reproducible evidence, not a computer-assisted proof.  Outer-time
concatenation, the complete linearized shear system, nonlinear closure, and
the Clay problem remain open.

---

## 0. Statement under audit

Let

\[
 V_\alpha(S,X)=\alpha^{-3}
 \left[2e^{-\alpha^2S}\sin(\alpha X)
 -e^{-4\alpha^2S}\sin(2\alpha X)\right],
 \qquad0<\alpha\le1,
\]

on $I=(-T,T)$ and
$\mathbb T_\alpha=\mathbb R/(2\pi/\alpha)\mathbb Z$.  The main estimate is

\[
 \|v\|_{L^2(I\times\mathbb T_\alpha)}
 \le C_T\left(
 \|v_X\|_2+
 \|(\partial_S-i\sigma V_\alpha)v\|_{L^2H^{-1}}
 \right),
 \tag{0.1}
\]

with one constant for every $0<\alpha\le1$ and both signs.  The resulting
energy solution must satisfy a strict fixed-block contraction.

The audit also checks two boundary statements:

1. the heat-polynomial corrections admit a weighted global envelope and
   bounded-core absorption;
2. they cannot be globally absorbed as an $o(1)$ perturbation of the cubic
   graph theorem.

---

## 1. Rescaling and sign audit

Starting from

\[
 v_d=v_{xx}-i\sigma\varepsilon_cW(d,x)v,
 \qquad
 W(d,x)=\frac12e^{-d}
 \left[-\sin x+\frac12e^{-3d}\sin2x\right],
\]

set $\varepsilon_c=4\alpha^{-5}$, $d=\alpha^2S$, and $x=\alpha X$.
Multiplication by $\alpha^2$ gives

\[
 u_S=u_{XX}-i\sigma4\alpha^{-3}
 W(\alpha^2S,\alpha X)u.
\]

Direct substitution yields

\[
 -4\alpha^{-3}W(\alpha^2S,\alpha X)
 =V_\alpha(S,X).
\]

Thus the scaled equation is

\[
 (\partial_S-i\sigma V_\alpha)u=u_{XX}.
\]

The sign and the torus length $2\pi/\alpha$ are correct.  The spatial
Jacobian contributes the same constant factor at both endpoints, so it
cancels from the contraction ratio.

**Verdict:** PASS.

---

## 2. Independent audit of the exact-tail envelope

Write $a=\alpha^2S$ and expand the two sines through degree seven.  The
coefficients of $X,X^3,X^5,X^7$ are respectively

\[
 2\alpha^{-2}(e^{-a}-e^{-4a}),
\]

\[
 \frac{4e^{-4a}-e^{-a}}3,
\]

\[
 \alpha^2\frac{e^{-a}-16e^{-4a}}{60},
\]

\[
 \alpha^4\frac{64e^{-4a}-e^{-a}}{2520}.
\]

Expanding these through orders $3,2,1,0$ independently reproduces every
coefficient of

\[
 H_3-\frac{\alpha^2}{4}H_5
 +\frac{\alpha^4}{40}H_7.
\]

For the four exponential remainders, the worst second-harmonic factors are

\[
 4^4=256,\qquad16\cdot4^2=256,
 \qquad64\cdot4=256.
\]

The sine remainder contributes $2^9=512=2\cdot256$.  This exactly recovers

\[
 |\mathcal R_\alpha|
 \le2(e^T+256e^{4T})\alpha^6
 \sum_{n=0}^4
 \frac{T^{4-n}|X|^{2n+1}}
 {(4-n)!(2n+1)!}.
\]

Unlike a formal local series, this proof uses global Lagrange remainder
bounds for sine and exponential.  The statement is therefore valid for all
$X\in\mathbb R$.

**Verdict:** PASS.

---

## 3. Weighted estimate and core absorption audit

R0.72V applies to

\[
 P_0=\partial_S-i\sigma H_3.
\]

The exact identity

\[
 P_0v=P_\alpha v+i\sigma(V_\alpha-H_3)v
\]

and $\|f\|_{H^{-1}}\le\|f\|_2$ give the weighted theorem without changing
the R0.72V graph domain beyond explicitly requiring the three weighted
products to be finite.

On $|X|\le R$, the leading bounded multiplier is
$\alpha^2R^5/4$.  The critical scale is

\[
 R=r\alpha^{-2/5}=r\kappa^{2/25}.
\]

At that scale,

\[
 \frac{\alpha^2}{4}R^5=\frac{r^5}{4},
\]

while

\[
 \alpha^4R^7=O(\alpha^{6/5}),
 \qquad
 \alpha^6R^9=O(\alpha^{12/5}).
\]

All terms containing positive powers of $T$ are smaller.  The absorption
condition and the original-coordinate width $\alpha R=r\kappa^{-3/25}$ are
correct.

**Verdict:** PASS.

---

## 4. Gauge-invariant no-go audit

A large constant value of a real potential can be removed by a time-only
phase, so it is not a legitimate obstruction.  The report instead compares
the odd spatial variation around a translated cell.

For an even nonzero bump $f(Y)$ centered at $R$,

\[
 H_3(R+Y)-H_3(R-Y)=6R^2Y+2Y^3+12SY,
\]

whereas

\[
 H_5(R+Y)-H_5(R-Y)=10R^4Y+O_T(R^2).
\]

After the factor one half in the odd projection, the leading relative cost
of $\alpha^2H_5/4$ is

\[
 \frac{(5/4)\alpha^2R^4}{3R^2}
 =\frac5{12}\alpha^2R^2.
\]

The $H_7$ contribution is

\[
 \frac7{120}\alpha^4R^4.
\]

Consequently, the correction is unbounded relative to the cubic graph
operator on the whole line.  At $R=\pi/\alpha-c$, the $H_5$ ratio tends to
$5\pi^2/12>4$, and the combined ratio tends in absolute value to

\[
 \left|-\frac{5\pi^2}{12}
 +\frac{7\pi^4}{120}\right|\approx1.570.
\]

For the exact potential,

\[
 V_{\alpha,X}(0,\pi/\alpha-c)
 =-4\alpha^{-2}+O(1),
\]

while $H_{3,X}=3\pi^2\alpha^{-2}+O(\alpha^{-1})$.  Thus the relative
centered difference tends to $-1-4/(3\pi^2)$.  None of these statements is
changed by a scalar gauge.

**Verdict:** PASS.  Global termwise absorption is FALSE.

---

## 5. Cell derivative and time-variation audit

Independent differentiation gives

\[
 V_{XXX}=-2e^{-\alpha^2S}\cos(\alpha X)
 +8e^{-4\alpha^2S}\cos(2\alpha X),
\]

\[
 V_{XXXX}=2\alpha e^{-\alpha^2S}\sin(\alpha X)
 -16\alpha e^{-4\alpha^2S}\sin(2\alpha X).
\]

The stated bounds follow.  Since $V_S=V_{XX}$,

\[
 (V_X)_S=V_{XXX},
 \qquad
 (V_{XX}/2)_S=V_{XXXX}/2.
\]

This is the crucial nonautonomous point: an escaping cell slope changes by
only $O_T(1)$, and an escaping curvature changes by $O_T(\alpha)$, over the
fixed block.  There is no hidden $O(\lambda)$ rotation term in the adaptive
moment.

**Verdict:** PASS.

---

## 6. Probe and varying cell-length audit

Scaling the R0.72V probe from $J_1$ to $J_\ell$ gives

\[
 \mu_2(\ell)=\ell^2/44,
 \qquad
 \mu_4(\ell)=3\ell^4/2288,
\]

and

\[
 \mu_4(\ell)-\mu_2(\ell)^2
 =5\ell^4/6292.
\]

For $1\le\ell\le2$, the adaptive variance is bounded below by $5/6292$.
The scaled probe and its degree-two multiples vanish to sufficient order at
the boundary.  Poincare constants, multiplication norms, and test-function
$H_0^1$ norms vary continuously with $\ell$ and are bounded on this compact
interval.

**Verdict:** PASS.

---

## 7. Bounded-cell contradiction audit

At $S=0$ and phase center $\theta=\alpha X_0$,

\[
 b=2\alpha^{-2}(\cos\theta-\cos2\theta),
\]

\[
 a=\alpha^{-1}(-\sin\theta+2\sin2\theta).
\]

The first trigonometric factor vanishes only when
$\cos\theta\in\{1,-1/2\}$; the second is
$\sin\theta(4\cos\theta-1)$.  Their only common zero is
$\theta=0\pmod{2\pi}$.  Near zero, the second factor equals
$3\theta+O(\theta^3)$.  Hence bounded $a,b$ and $\alpha\to0$ imply
$\theta=O(\alpha)$ and a bounded representative of the rescaled cell center
$X_0$ modulo the expanding period.  In the original coordinate, the
corresponding center satisfies $x_0=\alpha X_0=O(\alpha)$.

The chart then converges to translated $H_3$.  If $\alpha$ instead stays
positive, the phase center and cell length lie in compact sets and the
limiting exact trigonometric potential is nonconstant on every open cell.

With the centered potential bounded, the scalar cell mean has derivative
tending to zero.  Weighted Poincare makes the full counterexample sequence
converge strongly to the same spacetime constant.  Passing the graph equation
to distributions forces that constant times a nonconstant centered potential
to vanish, contradicting normalization.

**Verdict:** PASS.

---

## 8. Escaping-cell endpoint ledger audit

Let $\lambda=(a^2+b^2)^{1/2}\to\infty$ and

\[
 p=\frac a\lambda(y^2-\mu_2)+\frac b\lambda y.
\]

Taylor's theorem and the time-variation ledger yield

\[
 U=\lambda p+h,
 \qquad \|h\|_\infty\le R_T.
\]

For $A=\int vq$ and $B=\int vpq$,

\[
 \|B\|_2\lesssim\delta,
\]

\[
 B'=i\sigma[\lambda\kappa+\ell(S)]A+E,
 \qquad
 \kappa\ge5/6292,
\]

and

\[
 \|A'\|_2+\|E\|_2
 \lesssim(1+\lambda)\delta+\varepsilon.
\]

The scalar trace estimates are

\[
 |A(\pm T)|\lesssim
 1+\sqrt{(1+\lambda)\delta+\varepsilon},
\]

\[
 |B(\pm T)|\lesssim
 \delta+\sqrt{\lambda\delta}.
\]

After division by $\lambda$, the endpoint product is a sum of terms bounded
by

\[
 \delta,\quad \sqrt{\delta/\lambda},\quad
 \delta^{3/2}/\sqrt\lambda,\quad
 \sqrt{\delta\varepsilon/\lambda},
\]

and smaller quantities.  All vanish without requiring
$\lambda\delta\to0$.  The two bulk error terms similarly reduce to
$O(\delta^2+\delta+\varepsilon/\lambda)$.

**Verdict:** PASS.

---

## 9. Negative-Sobolev globalization audit

The local negative space is $H_D^{-1}(J)=(H_0^1(J))^*$ with the full inherited
$H^1$ norm.  For disjoint cells, zero extension embeds the Hilbert direct sum
of $H_0^1$ spaces isometrically into the global $H^1$ space.  Duality gives

\[
 \sum_j\|g_j\|_{H_D^{-1}}^2
 \le\|g\|_{H^{-1}}^2.
\]

The same proof works on the whole line and on a finite partition of a torus.
For the torus, $L=2\pi/\alpha\ge2\pi$ and $N=\lfloor L\rfloor$, so

\[
 1\le L/N<\frac{2\pi}{2\pi-1}<2.
\]

Every cell therefore lies inside the uniform length family audited in
Section 6.  Cellwise scalar gauges preserve each local negative norm and need
not agree across cell boundaries because the estimates are summed only after
taking norms.

**Verdict:** PASS.

---

## 10. Energy contraction audit

For each fixed $\alpha$, the torus potential is smooth, bounded, and real.
Standard nonautonomous parabolic theory gives the energy solution and

\[
 E(S_2)+2\int_{S_1}^{S_2}\|u_X\|_2^2=E(S_1).
\]

The graph theorem and $\|u_{XX}\|_{H^{-1}}\le\|u_X\|_2$ give

\[
 \int_{-T}^T E(S)\,dS
 \le4C_T^2\int_{-T}^T\|u_X\|_2^2\,dS
 =2C_T^2[E(-T)-E(T)].
\]

Since $E$ is nonincreasing,

\[
 2T E(T)\le\int_{-T}^TE(S)\,dS.
\]

Dividing by two and rearranging gives

\[
 E(T)\le\frac{C_T^2}{T+C_T^2}E(-T).
\]

The factor is strictly below one for every fixed $T>0$.  No explicit value
of the nonconstructive $C_T$ is asserted.

**Verdict:** PASS.

---

## 11. Numerical audit boundary

The numerical calculation uses the exact time-dependent potential, Fourier
heat half-steps, exact pointwise phase steps, and power iteration on the
discrete forward--adjoint product.  Reversing the step order and conjugating
the phase is the correct discrete adjoint.  Simultaneous spatial and temporal
refinement gives stable reported values.

However, Strang splitting and a finite Fourier grid do not provide a rigorous
upper bound for the infinite-dimensional propagator norm.  The numerical
result is correctly labelled `diagnostic only`; the proof of contraction is
the analytic graph-plus-energy argument.

**Verdict:** PASS as a reproducible stress test; NOT a machine-assisted proof.

---

## 12. Final claim boundary

The exact positive result is stronger than a weighted local perturbation:
the full sine tail is kept and one natural collision block on the physical
torus contracts uniformly at strong coupling.  It remains a linear scalar
theorem.

The audit does **not** certify:

- a graph constant uniform as $T\downarrow0$;
- the outer nondegenerate time intervals;
- concatenation into a full heat-history semigroup estimate;
- all Fourier rows or their nonlinear convolution;
- pressure or vortex-stretching closure;
- a Navier--Stokes continuation criterion;
- global regularity, finite-time blow-up, or any Clay-level conclusion.

The next defensible theorem is the exact concatenation of the two outer
$A_1$ regions with the completed $A_2$ collision block.
