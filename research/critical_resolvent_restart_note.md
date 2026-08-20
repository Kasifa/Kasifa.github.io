# R0.69E — Positive-time gluing of the critical linearized resolvent

## 1. Result

Fix the flat three-dimensional torus and a finite time \(T>0\).  For
\(0<S\le T\), use the periodic Koch--Tataru path norm

\[
 \|u\|_{X_S}=P_S(u)+Q_S(u),
\tag{1.1}
\]

where

\[
 \begin{aligned}
 P_S(u)&:=\sup_{0<t\le S}\sqrt t\,\|u(t)\|_\infty,\\
 Q_S(u)&:=\sup_{x,\ 0<R\le r_S}
 \left(
  \frac1{|B(x,R)|}
  \int_0^{R^2}\int_{B(x,R)}|u(t,y)|^2\,dy\,dt
 \right)^{1/2},\\
 r_S&:=\min\{1,\sqrt S\}.
 \end{aligned}
\tag{1.2}
\]

Let

\[
 \mathcal B(a,b)(t)
 =-\int_0^t e^{(t-s)\Delta}\mathbb P\nabla\!\cdot
       (a\otimes b)(s)\,ds,
 \qquad
 \mathcal A_vz=\mathcal B(v,z)+\mathcal B(z,v).
\tag{1.3}
\]

Fix admissible constants \(C_B,C_S>0\) such that

\[
 \|\mathcal B(a,b)\|_{X_S}
 \le C_B\|a\|_{X_S}\|b\|_{X_S}
\tag{1.4}
\]

and the periodic Stokes kernel obeys

\[
 \|e^{s\Delta}\mathbb P\nabla\!\cdot F\|_\infty
 \le C_Ss^{-1/2}\|F\|_\infty.
\tag{1.5}
\]

The whole-space Oseen-gradient estimate

\[
 |K_s(x)|\lesssim(\sqrt s+|x|)^{-4}
\tag{1.5a}
\]

implies (1.5): periodize \(K_s\), integrate its absolute value over one
fundamental cell, and bound the result by its \(L^1(\mathbb R^3)\) norm,
which is \(O(s^{-1/2})\).  Thus (1.5) does not use the false assertion that
the Leray projector alone is bounded on \(L^\infty\); the heat-smoothed
Oseen derivative is the bounded convolution operator.

Let \(v\in X_T\), choose \(0<\tau<\min\{T,1\}\), and put

\[
 a:=2C_B\|v\|_{X_\tau},
 \qquad
 V_\tau:=\sup_{\tau\le t\le T}\|v(t)\|_\infty.
\tag{1.6}
\]

Assume only the initial-block smallness

\[
 \boxed{a<1.}
\tag{1.7}
\]

For every \(\lambda>0\), define

\[
 b_\lambda:=2C_SV_\tau\sqrt{\frac\pi\lambda}.
\tag{1.8}
\]

If \(b_\lambda<1\), then

\[
 \boxed{I-\mathcal A_v:X_T\longrightarrow X_T
 \quad\hbox{is boundedly invertible}.}
\tag{1.9}
\]

More precisely, with \(r_T=\min\{1,\sqrt T\}\),

\[
 \boxed{
 \mathfrak M_v(T):=
 \|(I-\mathcal A_v)^{-1}\|_{X_T\to X_T}
 \le
 \frac{\Gamma(\tau,T,\lambda)}{(1-a)(1-b_\lambda)},}
\tag{1.10}
\]

where the completely explicit norm-equivalence factor

\[
 \Gamma(\tau,T,\lambda)
 :=1+\sqrt{27}
 +e^{\lambda(T-\tau)}
 \left(\sqrt{\frac T\tau}+\frac{r_T}{\sqrt\tau}\right)
\tag{1.11}
\]

is sufficient.  Thus the resolvent hypothesis in R0.69D is automatic on
every fixed interval on which the reference path is bounded and its initial
critical block can be made small.

In particular, if \(v\) is bounded on \([0,T]\), then

\[
 \|v\|_{X_\tau}\le2\sqrt\tau\,
 \|v\|_{L^\infty((0,T)\times\mathbb T^3)}.
\tag{1.12}
\]

Hence a sufficiently small positive \(\tau\) makes \(a<1\), and a
sufficiently large \(\lambda\) makes \(b_\lambda<1\).  Every smooth periodic
reference solution therefore has a finite critical linearized resolvent on
every compact regular interval.

This is a continuation theorem on an already regular interval.  It does not
show that the interval extends beyond a possible singular time, and the
bound in (1.10) can deteriorate rapidly as the measured reference amplitude
grows.

## 2. The hybrid norm removes the false endpoint-trace requirement

The Koch--Tataru norm is anchored at the initial time.  Restarting it at
every interior endpoint would require a quantitative strong
\(BMO^{-1}\) trace theorem that is not part of the standard bilinear estimate.
That trace is unnecessary.

Define the positive-time Bielecki hybrid norm

\[
 \|u\|_{\mathfrak X_{\tau,\lambda}}
 :=\max\left\{
 \|u\|_{X_\tau},
 \sqrt\tau\sup_{\tau\le t\le T}
 e^{-\lambda(t-\tau)}\|u(t)\|_\infty
 \right\}.
\tag{2.1}
\]

The original and hybrid spaces contain the same measurable paths, and

\[
 \boxed{
 \|u\|_{\mathfrak X_{\tau,\lambda}}
 \le\|u\|_{X_T}
 \le\Gamma(\tau,T,\lambda)
 \|u\|_{\mathfrak X_{\tau,\lambda}}.}
\tag{2.2}
\]

The first inequality is immediate.  For the second, the pointwise part is
bounded by

\[
 P_T(u)\le
 \left(1+e^{\lambda(T-\tau)}\sqrt{\frac T\tau}\right)
 \|u\|_{\mathfrak X_{\tau,\lambda}}.
\tag{2.3}
\]

For a Carleson ball with \(R\le\sqrt\tau\), the \(X_\tau\) block already
controls the cylinder.  If \(R>\sqrt\tau\), cover \(B(x,R)\) by at most

\[
 \left(1+\frac{2R}{\sqrt\tau}\right)^3
\tag{2.4}
\]

balls of radius \(\sqrt\tau\).  Since

\[
 \left(1+\frac{2R}{\sqrt\tau}\right)^3
 \frac{|B(0,\sqrt\tau)|}{|B(0,R)|}
 \le27,
\tag{2.5}
\]

the early part of the large cylinder costs at most
\(\sqrt{27}\|u\|_{X_\tau}\).  The late bounded part costs at most

\[
 r_Te^{\lambda(T-\tau)}
 \sup_{\tau\le t\le T}
 e^{-\lambda(t-\tau)}\|u(t)\|_\infty.
\tag{2.6}
\]

Equations (2.3)--(2.6) give (2.2).  The factor \(27\) is only a convenient
Euclidean covering bound; it is not claimed to be sharp.

## 3. Exact lower-triangular decomposition

Write \(z_0=z\mathbf1_{(0,\tau)}\) and
\(z_1=z\mathbf1_{[\tau,T]}\), and split the output in the same way.  Causality
gives the exact block form

\[
 \mathcal A_v=
 \begin{pmatrix}
  A_{00}&0\\
  A_{10}&A_{11}
 \end{pmatrix}.
\tag{3.1}
\]

For the initial block, the Koch--Tataru bilinear estimate gives

\[
 \|A_{00}z_0\|_{X_\tau}
 \le a\|z_0\|_{X_\tau}.
\tag{3.2}
\]

After its forcing stops at \(\tau\), the early contribution is exactly a
free heat evolution:

\[
 A_{10}z_0(t)=e^{(t-\tau)\Delta}(A_{00}z_0)(\tau),
 \qquad t\ge\tau.
\tag{3.3}
\]

The \(L^\infty\) heat contraction and the pointwise component of \(X_\tau\)
therefore give

\[
 \sqrt\tau\sup_{t\ge\tau}e^{-\lambda(t-\tau)}
 \|A_{10}z_0(t)\|_\infty
 \le a\|z_0\|_{X_\tau}.
\tag{3.4}
\]

For the late diagonal block, (1.5) gives

\[
 \begin{aligned}
 &\sqrt\tau e^{-\lambda(t-\tau)}
 \|A_{11}z_1(t)\|_\infty\\
 &\quad\le
 2C_SV_\tau
 \left(\int_0^{t-\tau}r^{-1/2}e^{-\lambda r}\,dr\right)
 \|z_1\|_{\mathfrak X_{\tau,\lambda}}\\
 &\quad\le b_\lambda
 \|z_1\|_{\mathfrak X_{\tau,\lambda}},
 \end{aligned}
\tag{3.5}
\]

because

\[
 \int_0^\infty r^{-1/2}e^{-\lambda r}\,dr
 =\sqrt{\frac\pi\lambda}.
\tag{3.6}
\]

Thus the nonnegative scalar majorant of (3.1) is

\[
 L=\begin{pmatrix}a&0\\a&b_\lambda\end{pmatrix}.
\tag{3.7}
\]

Both diagonal blocks are Neumann-invertible when \(a,b_\lambda<1\), and

\[
 (I-L)^{-1}
 =\begin{pmatrix}
  \dfrac1{1-a}&0\\[6pt]
  \dfrac{a}{(1-a)(1-b_\lambda)}&\dfrac1{1-b_\lambda}
 \end{pmatrix}.
\tag{3.8}
\]

The largest row sum is exactly

\[
 \|(I-L)^{-1}\|_{\ell^\infty\to\ell^\infty}
 =\frac1{(1-a)(1-b_\lambda)}.
\tag{3.9}
\]

Combining (2.2) and (3.9) proves (1.10).  The off-diagonal early-to-late
coupling need not be small; finite lower-triangularity is enough.

## 4. A finite time-slab certificate

The Bielecki weight gives a closed formula.  A literal finite restart
certificate is also available.  Let

\[
 \tau=t_0<t_1<\cdots<t_N=T,
 \qquad I_i=[t_{i-1},t_i],
 \qquad h_i=t_i-t_{i-1},
\tag{4.1}
\]

and define the block amplitudes

\[
 Z_0=\|z\|_{X_\tau},
 \qquad
 Z_i=\sqrt\tau\|z\|_{L^\infty(I_i\times\mathbb T^3)}
 \quad(1\le i\le N).
\tag{4.2}
\]

Let \(V=V_\tau\).  Define the nonnegative lower-triangular matrix
\(L_\Pi=(\ell_{ij})_{0\le i,j\le N}\) by

\[
 \begin{aligned}
 \ell_{00}&=a,\\
 \ell_{i0}&=a &&(i\ge1),\\
 \ell_{ii}&=4C_SV\sqrt{h_i} &&(i\ge1),\\
 \ell_{ij}&=4C_SV
 \left(
 \sqrt{t_{i-1}-t_{j-1}}
 -\sqrt{t_{i-1}-t_j}
 \right) &&(1\le j<i),\\
 \ell_{ij}&=0 &&(j>i).
 \end{aligned}
\tag{4.3}
\]

The off-diagonal formula is the exact kernel integral

\[
 2C_SV\int_{t_{j-1}}^{t_j}(t_{i-1}-s)^{-1/2}\,ds.
\tag{4.4}
\]

If

\[
 a<1,
 \qquad
 \eta_i:=4C_SV\sqrt{h_i}<1
 \quad(1\le i\le N),
\tag{4.5}
\]

then every diagonal block has a local inverse and the full finite Volterra
system has the majorant

\[
 \boxed{Z\le(I-L_\Pi)^{-1}F.}
\tag{4.6}
\]

All entries of \((I-L_\Pi)^{-1}\) are nonnegative and computable by forward
substitution.  No smallness assumption is imposed on a row sum or on the
accumulated off-diagonal coupling.  The explicit unweighted global bound is

\[
 \boxed{
 \mathfrak M_v(T)
 \le\Gamma(\tau,T,0)
 \max_{0\le i\le N}\sum_{j=0}^N
 [(I-L_\Pi)^{-1}]_{ij}.}
\tag{4.7}
\]

For equal late slabs \(h_i=h\), put \(\eta=4C_SV\sqrt h\).  The late-late
Toeplitz coefficients are exactly

\[
 \ell_0=\eta,
 \qquad
 \ell_k=\eta(\sqrt k-\sqrt{k-1})\quad(k\ge1).
\tag{4.8}
\]

Their row sum through lag \(m\) telescopes to

\[
 \eta\left(1+\sum_{k=1}^m(\sqrt k-\sqrt{k-1})\right)
 =\eta(1+\sqrt m).
\tag{4.9}
\]

This explains why a global Neumann test based on one row sum can fail even
though every finite lower-triangular system remains invertible.  The growth
of the certified row sum measures conditioning, not a loss of existence.

## 5. Endpoint trace and exact restart identity

The operator theorem above acts on all of \(X_T\), including time-measurable
inputs without a strong endpoint trace.  For the nonlinear application the
input is a heat orbit plus Duhamel terms and is strongly continuous in
\(L^\infty\) at every positive time.  In that subspace the inverse constructed
above preserves positive-time continuity.

Let \(f\) be strongly \(L^\infty\)-continuous on \([\tau,T]\) and let

\[
 z=f+\mathcal A_vz.
\tag{5.1}
\]

Then every \(z(t_i)\) exists in \(L^\infty\), and for \(t\ge t_i>0\),

\[
 \boxed{
 \begin{aligned}
 z(t)=&\ e^{(t-t_i)\Delta}z(t_i)
 +f(t)-e^{(t-t_i)\Delta}f(t_i)\\
 &-\int_{t_i}^t e^{(t-s)\Delta}\mathbb P\nabla\!\cdot
 \bigl(v\otimes z+z\otimes v\bigr)(s)\,ds.
 \end{aligned}}
\tag{5.2}
\]

This is the exact time-restart formula.  It follows by applying the
semigroup law to (5.1) at \(t_i\) and subtracting the past contribution.
The endpoint norm used after positive time is \(L^\infty\), with

\[
 \|z(t_i)\|_\infty
 \le\|z\|_{L^\infty(I_i\times\mathbb T^3)}.
\tag{5.3}
\]

No claim is made that weak-star continuity in \(BMO^{-1}\) alone supplies a
strong quantitative restart norm.  The proof avoids that issue by retaining
the critical norm only on the first block and using the pointwise component
already present in \(X_T\) after every positive time.

## 6. Consequence for R0.69D

Let \(v\) be a smooth periodic reference solution on \([0,T]\).  Equations
(1.12) and (1.8) provide explicit choices of \(\tau\) and \(\lambda\), so

\[
 M_T^{\rm cert}:=
 \frac{\Gamma(\tau,T,\lambda)}{(1-a)(1-b_\lambda)}
\tag{6.1}
\]

is a certified upper bound for the R0.69D reference condition number.  The
R0.69D packet theorem therefore becomes

\[
 4C_BC_HC_0(M_T^{\rm cert})^2\rho^r<1
 \quad\Longrightarrow\quad
 \|u_r-v\|_{X_T}
 \le2M_T^{\rm cert}C_HC_0\rho^r.
\tag{6.2}
\]

For each fixed regular reference interval the right-hand side tends to zero
geometrically.  The former resolvent hypothesis is no longer an independent
assumption on such an interval.

The remaining large-data question is different: whether a smooth reference
interval persists up to arbitrary time with enough control to prevent
\(M_T^{\rm cert}\) from losing usefulness.  R0.69E does not answer that
question.

## 7. What is proved and what is not

The proof establishes four points.

1. The periodic critical path space is equivalent, on a finite interval, to
   one initial \(X_\tau\) block followed by a weighted positive-time
   \(L^\infty\) block.
2. The reference linearization is an exact two-block lower-triangular
   Volterra operator in that norm.
3. Smallness is needed only on the two diagonal blocks; all past-to-future
   coupling is summed by forward substitution.
4. Every smooth reference path on a compact regular interval has a finite,
   explicitly bounded critical linearized resolvent.

The result does not provide a uniform bound as \(T\) approaches a hypothetical
singular time.  It does not prove that \(\sup_{t<T}\|v(t)\|_\infty\) remains
finite, does not continue a reference solution through a singular endpoint,
and does not establish global regularity or solve the three-dimensional
Navier--Stokes Millennium problem.

## References

1. H. Koch and D. Tataru, *Well-posedness for the Navier--Stokes equations*,
   Advances in Mathematics 157 (2001), 22--35,
   <https://math.berkeley.edu/~tataru/papers/nas.pdf>.
2. P. Auscher and D. Frey, *A new proof for Koch and Tataru's result on the
   well-posedness of Navier--Stokes equations in \(BMO^{-1}\)*,
   <https://arxiv.org/abs/1310.3783>.
3. H. Hou, *On regularity of solutions to the Navier--Stokes equation with
   initial data in \(BMO^{-1}\)*, SIAM Journal on Mathematical Analysis,
   <https://doi.org/10.1137/24M1719487>.
