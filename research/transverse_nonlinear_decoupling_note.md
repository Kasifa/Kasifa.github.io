# R0.69D — Conditional nonlinear decoupling from a resolvent-stable reference path

## 1. Result

Let (E_{m per}=BMO^{-1}_{\rm per}), and let (X_T) be a periodic
Koch--Tataru path space on a fixed interval ([0,T]).  Write

\[
 Sf=e^{t\Delta}f,
 \qquad
 \mathcal B(a,b)(t)
 =-\int_0^t e^{(t-\tau)\Delta}\mathbb P\nabla\!\cdot
     (a\otimes b)(\tau)\,d\tau,
\tag{1.1}
\]

and fix admissible constants (C_H,C_B>0) for

\[
 \|Sf\|_{X_T}\le C_H\|f\|_{E_{\rm per}},
 \qquad
 \|\mathcal B(a,b)\|_{X_T}
 \le C_B\|a\|_{X_T}\|b\|_{X_T}.
\tag{1.2}
\]

Let (v\in X_T) be a reference mild solution with initial datum (w_0),

\[
 v=Sw_0+\mathcal B(v,v),
\tag{1.3}
\]

and define its critical linearized operator

\[
 \mathcal A_vz:=\mathcal B(v,z)+\mathcal B(z,v).
\tag{1.4}
\]

Assume the exact reference resolvent condition

\[
 I-\mathcal A_v:X_T\to X_T\quad\hbox{is invertible},
 \qquad
 \|(I-\mathcal A_v)^{-1}\|\le M_T<\infty.
\tag{1.5}
\]

For the R0.69A packet, R0.69B gives

\[
 \delta_r:=\|U_r(0)\|_{E_{\rm per}}
 \le C_0\rho^r,
 \qquad C_0=6+4\sqrt2,
 \qquad \rho<0.797586.
\tag{1.6}
\]

Put

\[
 \chi_r:=4C_BM_T^2C_H\delta_r.
\tag{1.7}
\]

If (chi_r<1), then the Navier--Stokes mild equation with initial datum
(w_0+U_r(0)) has a unique solution (u_r=v+z_r) in the closed local
branch

\[
 \|z_r\|_{X_T}\le R_-(r),
 \qquad
 R_-(r):=
 \frac{1-\sqrt{1-\chi_r}}{2C_BM_T}.
\tag{1.8}
\]

Moreover,

\[
 \boxed{
 \|u_r-v\|_{X_T}
 \le R_-(r)
 =\frac{2M_TC_H\delta_r}{1+\sqrt{1-\chi_r}}
 \le2M_TC_HC_0\rho^r.}
\tag{1.9}
\]

Thus the complete nonlinear solution branch converges to the reference path
at the same certified geometric rate as the added packet.  No Picard term is
discarded: the proof absorbs the full perturbation self-interaction
(\mathcal B(z_r,z_r)).

This is a conditional stability theorem, not a global regularity theorem.
The condition (M_T<\infty) is precisely the missing large-reference gate.
It need not follow from the single scalar statement (|v|_{X_T}<\infty)
without a separate localization or linearized well-posedness argument in the
chosen endpoint space.

## 2. Exact difference equation

The two mild equations are

\[
 u_r=S(w_0+U_r(0))+\mathcal B(u_r,u_r),
 \qquad
 v=Sw_0+\mathcal B(v,v).
\tag{2.1}
\]

Substituting (u_r=v+z_r) and subtracting gives the exact identity

\[
 \boxed{
 z_r=SU_r(0)+\mathcal A_vz_r+\mathcal B(z_r,z_r).}
\tag{2.2}
\]

If (L_v:=(I-\mathcal A_v)^{-1}), then (2.2) is equivalent to

\[
 z_r=\Phi_r(z_r),
 \qquad
 \Phi_r(z):=L_v\bigl[SU_r(0)+\mathcal B(z,z)\bigr].
\tag{2.3}
\]

The estimate (1.2) and the resolvent hypothesis imply

\[
 \|\Phi_r(z)\|_{X_T}
 \le M_T\bigl(C_H\delta_r+C_B\|z\|_{X_T}^2\bigr),
\tag{2.4}
\]

and, for (z,y) in a radius-(R) ball,

\[
 \|\Phi_r(z)-\Phi_r(y)\|_{X_T}
 \le2M_TC_BR\|z-y\|_{X_T}.
\tag{2.5}
\]

These are estimates for the exact nonlinear map.

## 3. The smaller quadratic root closes the nonlinear map

The self-map inequality in a radius-(R) ball is

\[
 M_TC_BR^2-R+M_TC_H\delta_r\le0.
\tag{3.1}
\]

Its discriminant is (1-\chi_r).  When (chi_r<1), the smaller root is
exactly the value (R_-(r)) in (1.8), and equality holds in (3.1) at
(R=R_-(r)).  The Lipschitz factor on this ball is

\[
 q_r=2M_TC_BR_-(r)=1-\sqrt{1-\chi_r}<1.
\tag{3.2}
\]

Banach's fixed-point theorem therefore gives a unique fixed point in the
closed (R_-(r))-ball.  Rationalizing the numerator yields

\[
 R_-(r)
 =\frac{2M_TC_H\delta_r}{1+\sqrt{1-\chi_r}}.
\tag{3.3}
\]

Since (0<\sqrt{1-\chi_r}<1),

\[
 M_TC_H\delta_r<R_-(r)<2M_TC_H\delta_r.
\tag{3.4}
\]

The nonlinear amplification relative to the resolvent-linear scale is thus
between one and two.  It cannot change the geometric exponent (ho^r).

## 4. An explicit sufficient condition for small reference paths

The general theorem deliberately keeps (M_T) as a reference-dependent
quantity.  A simple sufficient condition follows directly from (1.2):

\[
 \|\mathcal A_v\|\le2C_B\|v\|_{X_T}.
\tag{4.1}
\]

If

\[
 a_T:=2C_B\|v\|_{X_T}<1,
\tag{4.2}
\]

then the Neumann series gives

\[
 M_T\le\frac1{1-a_T}.
\tag{4.3}
\]

Consequently the fully explicit condition

\[
 \frac{4C_BC_HC_0\rho^r}{(1-a_T)^2}<1
\tag{4.4}
\]

is sufficient for (1.9), with (M_T) replaced by (1/(1-a_T)).  This
corollary covers small reference paths.  It does not turn an arbitrary
order-one reference solution into a small one.

## 5. What this decides

R0.69C left open the quadratic perturbation term.  R0.69D now closes that
term on every reference interval satisfying (1.5).  The conclusion has
three direct consequences for the canonical deep packet.

1. The large physical Fourier coefficients of (U_r(0)) do not create a
   separate nearby nonlinear branch while the reference resolvent is stable.
2. Every interaction containing any number of reference factors and any
   number of perturbation factors is included in the fixed point.
3. The perturbation converges in the scaling-critical path norm at
   (O(\rho^r)); nonlinear feedback changes only a bounded prefactor.

This is stronger than the R0.69C linearized statement, but it remains local
in solution space and conditional on one order-one operator associated with
the reference path.

## 6. The exact obstruction exposed by the theorem

Suppose a common interval ([0,T]) and a fixed reference solution (v) are
given.  If the nearby solution branch generated by (U_r(0)	o0) fails to
converge locally to (v), then at least one of the hypotheses used above
must fail:

1. (I-\mathcal A_v) is not boundedly invertible in (X_T);
2. the candidate solutions leave the local uniqueness ball around (v);
3. the endpoint heat or bilinear estimates are unavailable in the selected
   function-space realization; or
4. the reference solution itself does not persist on the interval.

The first item is the new quantitative gate.  Define the reference
condition number

\[
 \mathfrak M_v(T):=
 \bigl\|(I-\mathcal A_v)^{-1}\bigr\|_{X_T\to X_T},
\tag{6.1}
\]

with value (+\infty) when the inverse does not exist.  The packet is
provably irrelevant whenever

\[
 4C_BC_HC_0\,\mathfrak M_v(T)^2\rho^r<1.
\tag{6.2}
\]

Therefore this packet can approach an order-one nonlinear obstruction only
along intervals where (mathfrak M_v(T)) grows at least on the scale
(ho^{-r/2}), or where the common reference interval disappears.  This is
a conditional necessary scaling, not evidence that such growth occurs.

## 7. Hard boundary and next problem

The theorem proves neither that (mathfrak M_v(T)) remains finite up to an
arbitrary time nor that it diverges at a singular time.  Bounded critical
path norm and bounded critical linearized resolvent are distinct statements
unless their equivalence is proved in the exact endpoint framework.  The
argument also selects the unique branch close to (v); it does not rule out
distant mild solutions in a class where unconditional uniqueness is absent.

The next falsifiable problem is now independent of the special packet
geometry: construct a restart/localization theorem for the periodic
Koch--Tataru space that bounds (mathfrak M_v(T)) by explicitly measurable
regular-interval data of a smooth reference solution.  A successful bound
would upgrade (1.9) from a resolvent-conditional statement to a continuation
statement on every certified regular interval.  Failure must identify the
precise trace, localization, or endpoint estimate that is lost.

This note does not prove global regularity, finite-time singularity, or a
solution of the Navier--Stokes Millennium problem.

## References

1. H. Koch and D. Tataru, *Well-posedness for the Navier--Stokes equations*,
   Advances in Mathematics 157 (2001), 22--35,
   <https://math.berkeley.edu/~tataru/papers/nas.pdf>.
2. P. Germain, N. Pavlovi\'c, and G. Staffilani, *Regularity of solutions to
   the Navier--Stokes equations evolving from small data in
   (BMO^{-1})*, International Mathematics Research Notices 2007,
   rnm087, <https://arxiv.org/abs/math/0609781>.

