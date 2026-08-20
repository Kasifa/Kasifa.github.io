# R0.69A — The complete periodic target Picard asymptotic

## 1. Result

The eighth-order sign certificate closes the last finite term left by the
R0.68A all-order tail theorem.  For

\[
 M_r=16^r,\qquad
 q_r=\frac{2(16^r-1)}{15},\qquad
 m_r=q_r+1,\qquad H_r=4M_r,
\]

choose

\[
 \varepsilon_r^2=\left(\frac{16}{\lambda}\right)^r,
 \qquad A_r=\varepsilon_r\sqrt{H_r},
 \qquad t_r=\frac{\log2}{2H_r^2},
\]

where \(\lambda\in(25,26)\) is the R0.66 dominant quartic root.  Let
\(G=\sum_{n\ge1}A_r^nG_n\) be the exact invariant-shear amplitude series in
the positive \(m_r\)-sector.  Then

\[
 \boxed{
 \frac{\widehat G(0,m_r,t_r)}
 {A_r^2\widehat G_2(0,m_r,t_r)}
 \longrightarrow
 1-\frac{C_*}{3600D_*}>1,}
\tag{1.1}
\]

where

\[
 D_*=\frac{1-2^{-(31/30)^2}}{2(31/30)^2}
\tag{1.2}
\]

and the R0.66 coefficient satisfies \(C_*<0\).  The guarded assembly gives

\[
 2.5937\times10^{-8}
 < -\frac{C_*}{3600D_*}
 <2.6141\times10^{-8}.
\tag{1.3}
\]

Thus the complete nonlinear target has the same phase as the quadratic
target and exceeds it by a strictly positive limiting relative amount.  The
number is small but nonzero; its role is to prove that the quartic spectral
branch survives the sum of every Picard order.

This is a theorem for one target Fourier coefficient in an exactly invariant,
globally smooth parallel-shear class.  It is not a singularity theorem and it
does not settle the three-dimensional Navier--Stokes regularity problem.

## 2. The quadratic limit

For \(L=1\), the quadratic target contains one carrier

\[
 Q_r=H_r+m_r-1.
\]

Since

\[
 \frac{m_r}{H_r}\longrightarrow\frac1{30},
 \qquad
 \frac{Q_r}{H_r}\longrightarrow\frac{31}{30},
\]

the exact R0.61 formula gives

\[
 S_{2,m_r}\longrightarrow D_*>0.
\tag{2.1}
\]

The assembly audit encloses \(D_*\) using 256-bit MPFR operations with
directed rounding.

## 3. Quartic term

R0.66 proves

\[
 S_{4,m_r}=C_*\lambda^r+O(r16^r),
 \qquad C_*<0.
\tag{3.1}
\]

The exact quartic-to-quadratic ratio is

\[
 \frac{A_r^4\widehat G_4}{A_r^2\widehat G_2}
 =-\varepsilon_r^2
 \frac{m_r^2}{H_r^3}\frac{S_{4,m_r}}{S_{2,m_r}}.
\tag{3.2}
\]

Because \(H_r=4M_r\),

\[
 M_r\frac{m_r^2}{H_r^3}\longrightarrow\frac1{3600}.
\tag{3.3}
\]

Equations (3.1)--(3.3) and
\(\varepsilon_r^2=(16/\lambda)^r\) give the strictly positive correction in
(1.1).

## 4. Sixth and eighth orders vanish at this amplitude

R0.67C-2 proves the complete sixth-order heat asymptotic with dominant root

\[
 \mu=16\lambda.
\]

After the critical spatial normalization and the factor
\(\varepsilon_r^4\), its ratio to the quadratic target decays at most at the
block rate

\[
 \frac{16}{\lambda}<0.637.
\tag{4.1}
\]

For order eight, the 1,792-state mass operator has the unique dominant root

\[
 \nu=256\lambda>6438,
\]

while every finite complementary root lies in \(|z|<4800\).  The centred
degree-ten jet defect annihilates all polynomials through degree ten.  On the
remaining \(C^{10,1}\)-dual part, one four-bit affine block contracts by

\[
 \frac{16^6}{16^{11}}=16^{-5}.
\tag{4.2}
\]

The R0.68B-2h resolvent therefore lifts the finite dominant mass vector to a
genuine eigendistribution of the full affine block operator.  Its pairing
with the complete seven-simplex heat observable is enclosed by

\[
 -2.69744373399132142\times10^{-8}
 <C_{8,\mathrm{heat}}
 <-2.87321129703704757\times10^{-9}<0.
\tag{4.3}
\]

Consequently

\[
 \nu^{-r}S_{8,m_r}\longrightarrow C_{8,\mathrm{heat}},
\tag{4.4}
\]

and the eighth-to-quadratic ratio decays at most at block rate

\[
 \frac{256}{\lambda^2}<0.405.
\tag{4.5}
\]

The sign in (4.3) is stronger than is needed for (1.1); bounded convergence
at the \(\nu^r\) scale would already make the eighth term vanish after the
chosen amplitude factor.

## 5. The infinite tail

R0.60 gives

\[
 \widehat G_n(0,m_r,t_r)=0,
 \qquad n\in\{3,5,7,9\}.
\tag{5.1}
\]

R0.68A gives the sign-free bound

\[
 \frac{\left|\sum_{n\ge10}A_r^n
 \widehat G_n(0,m_r,t_r)\right|}
 {|A_r^2\widehat G_2(0,m_r,t_r)|}
 <\frac1{30000}\left(\frac{43}{64}\right)^r.
\tag{5.2}
\]

This includes every even and odd order from ten onward.  Combining (3.2),
(4.1), (4.5), and (5.2) proves (1.1).

## 6. Value and hard boundary

This theorem closes the full Picard sum on the named target; no uncomputed
order remains in that statement.  It proves that higher-order cancellation
does not erase the R0.66 quartic branch.

Its value for the Millennium problem is indirect.  The exact same structure
that makes the all-order proof possible also gives

\[
 \partial_tF-\partial_1^2F=0,
 \qquad
 \partial_tG-\Delta_{12}G+F\partial_2G=0.
\tag{6.1}
\]

For every fixed packet, (6.1) is a linear parabolic equation with smooth
coefficients and has a global smooth solution.  Therefore no coefficient
theorem confined to this invariant class can by itself produce a
Navier--Stokes singularity.  The next relevant problem is transverse: add a
genuinely three-dimensional perturbation, quantify the terms that break
(6.1), and prove either a scale-uniform stability estimate or an instability
mechanism that reaches a standard blow-up criterion.

The present result proves neither outcome.  It is not a solution of the Clay
Millennium problem.

