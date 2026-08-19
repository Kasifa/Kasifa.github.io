# R0.55 — A critical Fourier bridge and a no-go theorem for scalar charge

## 1. Scope and decision

R0.54 closes the complete product-affine weight family inside the reduced
canonical edge generating system.  The next question is whether that system
can receive a scale-critical, rotation-consistent upper bound from the full
three-dimensional Fourier equation.

This note separates two issues that should not be conflated.

1. The full Fourier--Leray nonlinearity does admit a finite scale-critical
   estimate when viscous dissipation is retained.  The natural baseline is
   the Fourier space \(\mathcal X^{-1}\) used by Lei and Lin.  This gives a
   scalar *degree* majorant for small data.
2. The nontrivial scalar *charge* used by the reduced edge system cannot be
   made both additive under convolution and invariant under rotations on
   arbitrary Fourier data.  This is an exact algebraic obstruction to the
   most direct charge-preserving bridge.

An explicit high--high-to-low triad saturates the critical symbol estimate at
arbitrarily large input/output frequency separation.  Thus the obstruction
cannot be removed by inserting a favorable high--high-to-low scale factor.

The scale-critical estimate is a classical small-data mechanism, not a new
large-data theorem.  The charge result rules out one interface design, not
vector-valued, directional, or multi-frame alternatives.  Nothing here proves
or disproves global regularity for three-dimensional Navier--Stokes.

## 2. Fourier convention and critical norms

Use the Fourier normalization for which

\[
 \widehat{fg}(\xi)=\int_{\mathbb R^3}
 \widehat f(\eta)\widehat g(\xi-\eta)\,d\eta.
\]

On \(\mathbb T^3\), use normalized Haar measure, so products have the
corresponding discrete convolution with constant one.  For \(\sigma\in
\mathbb R\), define

\[
 \|u\|_{\mathcal X^\sigma(\mathbb R^3)}
 =\int_{\mathbb R^3}|\xi|^\sigma|\widehat u(\xi)|\,d\xi,
\tag{2.1}
\]

and, for a mean-zero periodic field,

\[
 \|u\|_{\mathcal X^\sigma(\mathbb T^3)}
 =\sum_{k\in\mathbb Z^3\setminus\{0\}}
 |k|^\sigma|\widehat u(k)|.
\tag{2.2}
\]

For the Navier--Stokes scaling

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
\]

the Fourier transform obeys

\[
 \widehat u_\lambda(\xi,t)
 =\lambda^{-2}\widehat u(\xi/\lambda,\lambda^2t).
\]

Changing variables gives the exact exponent

\[
 \|u_\lambda(t)\|_{\mathcal X^\sigma}
 =\lambda^{\sigma+1}
 \|u(\lambda^2t)\|_{\mathcal X^\sigma}.
\tag{2.3}
\]

Consequently

\[
 L_t^\infty\mathcal X^{-1}
 \quad\text{and}\quad
 L_t^1\mathcal X^1
\tag{2.4}
\]

are both scale invariant.  On the torus, the same calculation is exact under
integer dilations \(u^{(m)}(x,t)=m u(mx,m^2t)\).

Lei and Lin proved global well-posedness in \(\mathcal X^{-1}\) when the
initial norm is strictly below viscosity.  That published theorem is the
baseline for this section; I do not claim it as a new result.

## 3. The exact Fourier--Leray cancellation

Let \(p+q=k\ne0\).  For divergence-free Fourier coefficients

\[
 p\cdot\widehat u(p)=0,
 \qquad q\cdot\widehat v(q)=0,
\]

one ordered Navier--Stokes interaction is

\[
 \mathscr B_k(p,q)
 =iP_k\big[(q\cdot\widehat u(p))\widehat v(q)\big],
\tag{3.1}
\]

where \(P_k=I-k\otimes k/|k|^2\) is the Leray projection.  Input
incompressibility gives the exact identity

\[
 q\cdot\widehat u(p)
 =(k-p)\cdot\widehat u(p)
 =k\cdot\widehat u(p).
\tag{3.2}
\]

Since \(P_k\) is an orthogonal projection,

\[
 |k|^{-1}|\mathscr B_k(p,q)|
 \le |\widehat u(p)|\,|\widehat v(q)|.
\tag{3.3}
\]

Summing or integrating the convolution proves

\[
 \boxed{
 \|P(u\cdot\nabla v)\|_{\mathcal X^{-1}}
 \le
 \|u\|_{\mathcal X^0}\|v\|_{\mathcal X^0}.
 }
\tag{3.4}
\]

This keeps the Leray projection and uses incompressibility before taking
absolute values.  In particular, the apparent factor
\(|q|/|k|\) in a high--high-to-low interaction disappears.

Cauchy--Schwarz in Fourier measure gives

\[
 \|u\|_{\mathcal X^0}^2
 \le
 \|u\|_{\mathcal X^{-1}}
 \|u\|_{\mathcal X^1}.
\tag{3.5}
\]

For two fields, arithmetic--geometric mean then yields

\[
 \|P(u\cdot\nabla v)\|_{\mathcal X^{-1}}
 \le\frac12\left(
 \|u\|_{\mathcal X^{-1}}\|v\|_{\mathcal X^1}
 +\|u\|_{\mathcal X^1}\|v\|_{\mathcal X^{-1}}
 \right).
\tag{3.6}
\]

Equations (3.2)--(3.6) are all-frequency analytic inequalities.  They are not
finite Fourier experiments.

## 4. Retaining heat gives a finite solution-space bridge

For viscosity \(\nu>0\), define

\[
 \|u\|_{\mathcal E_\nu}
 =\max\left\{
 \|u\|_{L_t^\infty\mathcal X^{-1}},
 \nu\|u\|_{L_t^1\mathcal X^1}
 \right\}.
\tag{4.1}
\]

Let

\[
 \mathcal T(u,v)(t)
 =-\int_0^t e^{\nu(t-s)\Delta}
 P(u\cdot\nabla v)(s)\,ds.
\tag{4.2}
\]

If \(F\in L_t^1\mathcal X^{-1}\), direct integration of the heat multiplier
gives

\[
 \left\|\int_0^t e^{\nu(t-s)\Delta}F(s)\,ds
 \right\|_{L_t^\infty\mathcal X^{-1}}
 \le\|F\|_{L_t^1\mathcal X^{-1}},
\tag{4.3}
\]

and

\[
 \nu\left\|\int_0^t e^{\nu(t-s)\Delta}F(s)\,ds
 \right\|_{L_t^1\mathcal X^1}
 \le\|F\|_{L_t^1\mathcal X^{-1}}.
\tag{4.4}
\]

Combining (3.6) with (4.3)--(4.4) gives the explicit bridge

\[
 \boxed{
 \|\mathcal T(u,v)\|_{\mathcal E_\nu}
 \le\frac1\nu
 \|u\|_{\mathcal E_\nu}\|v\|_{\mathcal E_\nu}.
 }
\tag{4.5}
\]

The linear heat flow has

\[
 \|e^{\nu t\Delta}u_0\|_{\mathcal E_\nu}
 \le\|u_0\|_{\mathcal X^{-1}}.
\tag{4.6}
\]

After normalizing

\[
 z=\frac{\|u_0\|_{\mathcal X^{-1}}}{\nu},
 \qquad
 m=\frac{\|u\|_{\mathcal E_\nu}}{\nu},
\]

the mild fixed-point inequality has the scalar degree majorant

\[
 m\le z+m^2.
\tag{4.7}
\]

The corresponding algebraic series is

\[
 M(z)=z+M(z)^2
 =\frac{1-\sqrt{1-4z}}2
 =\sum_{n\ge1}C_{n-1}z^n,
\tag{4.8}
\]

with exact radius \(1/4\).  This proves that a finite, rotation-invariant
bridge from the full PDE to a scalar *degree* majorant exists.  It is a
conservative fixed-point baseline.  The sharper Lei--Lin a priori argument
reaches the small-data condition \(\|u_0\|_{\mathcal X^{-1}}<\nu\).

The number \(1/4\) in (4.8) must not be compared numerically with the R0.54
radius.  The variables, normalizations, coefficient systems, and initial
data are different.

## 5. An exact high--high-to-low saturation family

For every positive integer \(N\), put

\[
 p_N=(N,0,0),
 \qquad
 q_N=(-N,1,0),
 \qquad
 k=p_N+q_N=(0,1,0),
\tag{5.1}
\]

and choose unit polarizations

\[
 a=(0,1,0),
 \qquad
 b=(0,0,1).
\tag{5.2}
\]

They are exactly divergence free:

\[
 p_N\cdot a=0,
 \qquad
 q_N\cdot b=0.
\]

Moreover

\[
 q_N\cdot a=1,
 \qquad
 P_kb=b.
\]

Therefore

\[
 \boxed{
 P_k[(q_N\cdot a)b]=b,
 \qquad
 \frac{|k|^{-1}|P_k[(q_N\cdot a)b]|}{|a||b|}=1.
 }
\tag{5.3}
\]

The input/output separation obeys

\[
 \frac{\min\{|p_N|,|q_N|\}}{|k|}=N\longrightarrow\infty.
\tag{5.4}
\]

Thus (3.3) has sharp constant one already on integer torus frequencies, and
it remains sharp along arbitrarily separated high--high-to-low interactions.
The family can be completed to a real Fourier field by adding conjugate
negative modes.

This is an all-\(N\) algebraic identity.  The machine certificate checks a
large finite window only as an independent exact regression.

## 6. No nontrivial additive rotation-invariant scalar charge

The reduced canonical edge system uses a nontrivial scalar charge because
charge must add at a convolution root.  To extend that structure directly to
arbitrary Fourier data, consider a scalar map

\[
 \chi:\mathbb R^3\to\mathbb R
\]

with

\[
 \chi(\xi+\eta)=\chi(\xi)+\chi(\eta).
\tag{6.1}
\]

Suppose also that it is rotation invariant:

\[
 \chi(R\xi)=\chi(\xi)
 \qquad(R\in SO(3)).
\tag{6.2}
\]

### Theorem 1

Every map satisfying (6.1)--(6.2) is identically zero.

### Proof

For any \(\xi\ne0\), choose a rotation through angle \(\pi\) about an axis
orthogonal to \(\xi\).  Then \(R\in SO(3)\) and \(R\xi=-\xi\).  Rotation
invariance gives

\[
 \chi(-\xi)=\chi(\xi),
\]

while additivity gives

\[
 \chi(-\xi)=-\chi(\xi).
\]

Hence \(\chi(\xi)=0\).  Also \(\chi(0)=0\), so \(\chi\equiv0\).  No
continuity or measurability assumption is needed. \(\square\)

There is a discrete torus analogue.

### Theorem 2

If \(\chi:\mathbb Z^3\to\mathbb R\) is additive and invariant under the
orientation-preserving cubic rotation group, then \(\chi\equiv0\).

### Proof

An additive map on \(\mathbb Z^3\) is determined by its values on the three
coordinate vectors.  Invariance under

\[
 \operatorname{diag}(1,-1,-1)
 \quad\text{and}\quad
 \operatorname{diag}(-1,1,-1)
\]

forces all three basis values to equal their negatives. \(\square\)

These theorems do not say that every useful charge must vanish.  They say
that a useful nontrivial additive scalar charge must select a frame, direction,
or family of frames.

## 7. Consequence for the R0.29--R0.54 generator

The current charge is a valid coordinate on the selected cone lattice and is
essential to the exact edge recurrences.  Its support property \(q\ge-1\)
and its charge-zero projector arise from that generated subspace.  They are
not universal properties of arbitrary Fourier data.

R0.55 therefore gives the following qualified decision.

1. **Full PDE to a critical scalar degree majorant:** finite; (4.5) supplies
   an explicit bridge.
2. **Full PDE to the current nontrivial scalar charge-degree generator:**
   impossible if the charge itself must be both convolution-additive and
   rotation invariant.
3. **Worst unresolved geometry:** high--high to low.  Equation (5.3) shows
   that arbitrarily strong scale separation gives no extra small factor in
   the critical symbol bound.

This is not a proof that every comparison with the reduced generator is
impossible.  The theorem leaves at least three mathematically distinct
routes:

- retain a rotation-covariant vector frequency instead of a scalar charge;
- use dyadic angular sectors and keep the relative Leray geometry;
- take a supremum or integral over a family of charge frames.

Each route is larger than the present two-index charge-degree system.  The
next useful certificate should therefore test the smallest direction-resolved
kernel rather than optimize another scalar charge weight.

## 8. Reproducibility and classification

`research/fourier_critical_charge_bridge_audit.py` records:

- the exact scaling exponents of \(\mathcal X^{-1},\mathcal X^0,\mathcal X^1\);
- the high--high-to-low identity (5.3) over a deterministic integer window;
- exact rational \(SO(3)\) half-turn matrices on an integer vector box;
- Catalan coefficients and their exact recurrence;
- a machine-readable separation between formal theorems and finite
  regressions.

The analytic proofs are the displayed identities above.  Increasing the
finite audit window does not strengthen those theorems.  The computation uses
exact integers and rational numbers, with no random seed, GPU, or
floating-point sign decision.

## References

1. Z. Lei and F.-H. Lin, *Global Mild Solutions of the Navier--Stokes
   Equations*, Communications on Pure and Applied Mathematics 64 (2011),
   1297--1304. DOI: <https://doi.org/10.1002/cpa.20361>;
   arXiv: <https://arxiv.org/abs/1203.2699>.
2. R0.21, *Cone-frequency cancellation lemma*.
3. R0.22, *Analytic-radius loss lemma*.
4. R0.29, *Canonical transport reduction and the infinite charge ladder*.
5. R0.54, *A global enclosure for the complete product-affine family*.
