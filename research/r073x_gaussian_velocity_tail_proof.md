# R0.73X Gaussian velocity-tail lemma

**Status:** `PROVED FUNCTIONAL LEMMA / INDEPENDENT AUDIT PASS`

**Scope:** unsigned centered production at positive heat scale; no pressure,
defect, epsilon-regularity, or Navier--Stokes trajectory is used

**DGX used:** false

## 1. Statement

Let the periodic field on \(\mathbb T^3=[0,2\pi]^3\) be lifted to
\(\mathbb R^3\), and let

\[
 g_s(y)=(4\pi s)^{-3/2}e^{-|y|^2/(4s)},\qquad
 v_s=P_su.
\]

For

\[
 \mathscr S_s(x)={1\over4s}\int_{\mathbb R^3}
 y\cdot\bigl(u(x-y)-v_s(x)\bigr)
 \bigl|u(x-y)-v_s(x)\bigr|^2g_s(y)\,dy,
\tag{1.1}
\]

one has, for every \(s>0\),

\[
 \boxed{|\mathscr S_s(x)|\le C_0s^{-1/2}P_{2s}(|u|^3)(x),}
\tag{1.2}
\]

where the explicit constant

\[
 C_0=2^{5/2}e^{-1/2}+{2^{7/2}\over\sqrt\pi}<10
\tag{1.3}
\]

is admissible.

Fix \(0<R<\pi/8\), \(0<\theta\le1\), and
\(I_R=(t_0-R^2,t_0)\), and assume
\(u\in L^3(I_R\times\mathbb T^3)\).  On the Euclidean periodic lift put

\[
 A_m(R)=B_{2^{m+1}R}(x_0)\setminus B_{2^mR}(x_0),\qquad m\ge1,
\tag{1.4}
\]

\[
 C_{3,\mathrm{core}}(z_0,R)
 ={1\over(2R)^2}\int_{I_R}\int_{B_{2R}(x_0)}|\widetilde u|^3,
\tag{1.5}
\]

and the non-circular, dimensionless annular tail

\[
 \mathcal A^{u,3}_{\mathrm{ext}}(z_0,R;\theta)
 =\sum_{m=1}^{\infty}e^{-4^m/(32\theta)}
 {1\over(2^mR)^2}\int_{I_R}\int_{A_m(R)}|\widetilde u|^3.
\tag{1.6}
\]

Then

\[
 \boxed{
 \begin{aligned}
 &{1\over R^3}\int_{I_R}\int_0^{\theta R^2}
       \int_{B_R(x_0)}|\mathscr S_s|\,dx\,ds\,dt\\
 &\quad\le 8C_0\sqrt\theta\,C_{3,\mathrm{core}}(z_0,R)
 +{8C_0\over3\sqrt{2\pi}}
       \mathcal A^{u,3}_{\mathrm{ext}}(z_0,R;\theta).
 \end{aligned}}
\tag{1.7}
\]

The infinite lifted tail is finite for periodic \(u\in L^3(I_R\times
\mathbb T^3)\), because its annular mass grows at most polynomially whereas
the weights decay super-exponentially.

## 2. Pointwise proof

The elementary inequality \(|a-b|^3\le4(|a|^3+|b|^3)\) and Jensen give

\[
 |v_s(x)|^3\le P_s(|u|^3)(x).
\tag{2.1}
\]

If \(q=|y|/\sqrt s\), then

\[
 {(|y|/s)g_s(y)\over s^{-1/2}g_{2s}(y)}
 =2^{3/2}q e^{-q^2/8}
 \le2^{5/2}e^{-1/2},
\tag{2.2}
\]

because the maximum occurs at \(q=2\).  Moreover

\[
 \int_{\mathbb R^3}|y|g_s(y)\,dy={4\sqrt s\over\sqrt\pi},
 \qquad g_s\le2^{3/2}g_{2s}.
\tag{2.3}
\]

Applying these three bounds directly to (1.1) proves (1.2)--(1.3).

## 3. Core and annular integration

For sources in \(B_{2R}\), positivity and unit mass of the heat kernel give

\[
 \int_0^{\theta R^2}s^{-1/2}\,ds=2\sqrt\theta R.
\tag{3.1}
\]

After multiplication by \(R^{-3}\), this is exactly the first term in
(1.7).

If \(x\in B_R\) and \(z\in A_m(R)\), then
\(|x-z|\ge2^{m-1}R\).  Hence

\[
 \int_{B_R}g_{2s}(x-z)\,dx
 \le {R^3\over12\sqrt{2\pi}}s^{-3/2}
       e^{-4^mR^2/(32s)}.
\tag{3.2}
\]

The remaining scale integral is exact:

\[
 \int_0^{\theta R^2}s^{-2}e^{-4^mR^2/(32s)}\,ds
 ={32\over4^mR^2}e^{-4^m/(32\theta)}.
\tag{3.3}
\]

Fubini, (3.2)--(3.3), and
\((2^mR)^{-2}=4^{-m}R^{-2}\) give the second term in (1.7).

## 4. Energy-class corollary

With the normalization of `r073x_problem_freeze.md`, local Sobolev and
Hölder in time imply

\[
 C_{3,\mathrm{core}}(z_0,R)
 \le C(1+\nu^{-1})^{3/4}\mathcal E(z_0,2R)^{3/2}.
\tag{4.1}
\]

Consequently (1.7) supplies a fully specified version of the unweighted
\(\mathcal C^{\rm abs}_{\mathscr S,0}\) candidate with a critical Gaussian
velocity tail.  Neither \(\mathcal P\) nor \(\mathcal M\) is needed for this
purely velocity-dependent term.

## 5. Exact boundary of the result

This lemma closes only the unweighted, scale-integrated absolute
\(\mathscr S_s\) row.  It does not prove any of the following:

- control of the weighted row with an additional \(s^{-1/2}\), whose direct
  majorant is logarithmically divergent at \(s=0\);
- smallness of the exterior tail from a local hypothesis;
- control of the pressure covariance or harmonic pressure;
- a suitable-weak zero-scale passage;
- a CKN epsilon scale, regularity criterion, or global regularity.

The companion scalar certificate checks the kernel maximum, scale integral,
scaling degrees, and remote-packet concentration powers independently of the
Fourier harness.

NOT CLAY.
