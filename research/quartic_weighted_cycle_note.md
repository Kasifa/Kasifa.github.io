# R0.65 — Exact moment enclosures for the heat-weighted cycle

## 1. Result

R0.64 found an exact supercritical cycle for the zero-time quartic
Rudin--Shapiro transfer.  The unresolved question was whether the Gaussian
weights and the three-time simplex integral suppress that cycle before a norm
is taken.  This note retains the complete heat kernel.

Set

\[
 L=1,\qquad M_r=16^r,\qquad
 q_r=2\frac{16^r-1}{15},\qquad m_r=q_r+1,
\tag{1.1}
\]

and let \(S_r=S_{4,m_r}\) be the exact dimensionless quartic sum in R0.61.
The target digits of \(q_r\), read from least to most significant, are \(r\)
copies of \(0100\).

An exact integer moment transfer, followed by a rational interval enclosure
of the simplex series through order \(48\), gives the following finite-scale
theorem.

\[
 \boxed{
 \begin{array}{ll}
 S_r>0,&1\le r\le13,\\
 S_r<0,&14\le r\le24.
 \end{array}}
\tag{1.2}
\]

Moreover, all ten transitions \(r-1\to r\) with \(15\le r\le24\) satisfy

\[
 \boxed{\frac{|S_r|}{|S_{r-1}|}>16.}
\tag{1.3}
\]

At the final certified scale,

\[
 M_{24}=16^{24}=79228162514264337593543950336,
\tag{1.4}
\]

the interval gives

\[
 1.17<\frac{|S_{24}|}{M_{24}}<1.19,
 \qquad
 25.29<\frac{|S_{24}|}{|S_{23}|}<25.30.
\tag{1.5}
\]

The last ratio is close to the zero-time eigenvalue
\(25.1515893341\ldots\), but (1.2)--(1.5) are finite statements.  They rule
out a claim that every four-digit block is reduced to growth at most \(16\).
They do **not** by themselves prove that \(|S_r|/M_r\) is unbounded.

The sign change is also new.  The earlier scans saw a positive quartic sum,
corresponding to a stabilizing phase relative to the quadratic target.  Along
the periodic family (1.1), that phase reverses at \(r=14\).  Therefore an
all-scale proof cannot use positivity of this heat-weighted coefficient.

## 2. Exact bivariate moment lift

Let \(a_n^s(j)\) be the coefficient of the length-\(2^n\)
Rudin--Shapiro state \(s\in\{0,1\}\).  For a target \(q_n\), cubic state
\(\boldsymbol\sigma\in\{0,1\}^3\), carry \(k\in\{-1,0,1\}\), and
nonnegative integers \(i,j\), define

\[
 \begin{aligned}
 X_n^{s,\boldsymbol\sigma,k;i,j}(q_n)
 :={}&a_n^s(q_n)
 \sum_{A+B-C=q_n+k2^n}
 a_n^{\sigma_1}(A)a_n^{\sigma_2}(B)a_n^{\sigma_3}(C)
 A^iB^j.
 \end{aligned}
\tag{2.1}
\]

Only two free moment variables are needed because
\(C=A+B-q_n-k2^n\).  Append the next target bit \(b\), and write
\(\boldsymbol\varepsilon=(\varepsilon_1,\varepsilon_2,
\varepsilon_3)\).  With \(N=2^n\) and

\[
 k'=2k+b-(\varepsilon_1+\varepsilon_2-\varepsilon_3),
\tag{2.2}
\]

the exact recurrence is

\[
 \boxed{
 \begin{aligned}
 X_{n+1}^{s,\boldsymbol\sigma,k;i,j}
 ={}&\sum_{\boldsymbol\varepsilon}
 (-1)^{sb+\boldsymbol\sigma\cdot\boldsymbol\varepsilon}
 \sum_{u=0}^{i}\sum_{v=0}^{j}
 \binom{i}{u}\binom{j}{v}
 (\varepsilon_1N)^{i-u}(\varepsilon_2N)^{j-v}\\
 &\qquad\times
 X_n^{b,\boldsymbol\varepsilon,k';u,v},
 \end{aligned}}
\tag{2.3}
\]

where a term is zero when \(k'\notin\{-1,0,1\}\).  Degree zero in (2.3)
is exactly the 48-state transfer of R0.64.  The audit checks every state and
every bivariate moment of total degree at most four against direct
enumeration through six binary levels.  For the published calculation it
retains all moments of total degree at most \(96\).

## 3. Exact simplex series

For one ordered quartic path, let \(\alpha_0,\alpha_1,\alpha_2\) be the
three nonzero heat rates in R0.61.  Expanding the exponential before
integrating over the simplex gives the identity

\[
 \boxed{
 K_T(\alpha_0,\alpha_1,\alpha_2,0)
 =\sum_{d=0}^{\infty}
 (-1)^d\frac{T^{d+3}}{(d+3)!}
 h_d(\alpha_0,\alpha_1,\alpha_2),}
\tag{3.1}
\]

where

\[
 h_d(x,y,z)=\sum_{i+j+k=d}x^iy^jz^k.
\tag{3.2}
\]

After substituting \(C=A+B-q_r\), each
\(H^{2d}h_d(\alpha_0,\alpha_1,\alpha_2)\) is an integer polynomial in
\((A,B)\) of total degree at most \(2d\).  Thus (2.3) evaluates every
coefficient of the truncated series exactly.

The three path orders have rate numerators

\[
 \begin{array}{c|c|c|c}
 &H^2\alpha_0&H^2\alpha_1&H^2\alpha_2\\ \hline
 (A,B,-C)&Q^2+A^2+B^2+C^2&(A-Q)^2+B^2+C^2&2C^2\\
 (A,-C,B)&Q^2+A^2+B^2+C^2&(A-Q)^2+B^2+C^2&2B^2\\
 (-C,A,B)&Q^2+A^2+B^2+C^2&(Q+C)^2+A^2+B^2&2B^2.
 \end{array}
\tag{3.3}
\]

Here \(H=4M\), \(Q=H+q_r\), \(A=H+a\), \(B=H+b\), and
\(C=H+a+b-q_r\).

Let \(J_{d,r}\) be the exact signed moment sum of the three polynomials in
(3.3).  Then

\[
 S_r=\sum_{d=0}^{D}(-1)^d
 \frac{T^{d+3}}{(d+3)!H^{2d}}J_{d,r}+E_{D,r}.
\tag{3.4}
\]

The zeroth coefficient satisfies \(J_{0,r}=3y_r\), with \(y_r\) the exact
unweighted reachable scalar from R0.64.

## 4. Rational remainder certificate

All path rates obey

\[
 0\le\alpha_j\le A_*:=\frac{75}{8}.
\tag{4.1}
\]

There are at most \(3M^2\) ordered paths.  Since

\[
 h_d(\alpha_0,\alpha_1,\alpha_2)
 \le \binom{d+2}{2}A_*^d,
\tag{4.2}
\]

putting \(z=A_*T\) gives

\[
 \boxed{
 |E_{D,r}|\le
 3M^2\frac{T^3}{2}
 \frac{z^{D+1}}{(D+1)!(D+4)}
 \frac{1}{1-z/(D+2)}.}
\tag{4.3}
\]

No floating-point value of \(T\) is required.  The identity

\[
 T=\frac{\log2}{2}=\operatorname{atanh}\frac13
 =\sum_{n=0}^{\infty}\frac{3^{-(2n+1)}}{2n+1}
\tag{4.4}
\]

and its positive geometric tail give rational lower and upper endpoints.
The polynomial in (3.4) is evaluated with rational interval arithmetic, and
(4.3) is then added outward.  At \(r=24\), the order-48 remainder is less
than \(2\times10^{-12}\) of the certified magnitude.

Four independent long-double path enumerations for
\(r=1,2,3,4\) agree with the exact-moment centers within one part in
\(10^{12}\).  They are cross-checks only; the stated signs and inequalities
come from integer and rational arithmetic.

## 5. Mathematical consequence

R0.64 left open the possibility that time integration reduces every
four-digit cycle below the extensive threshold \(16\).  Equations
(1.2)--(1.5) exclude that finite-block statement on the actual Navier--Stokes
quartic scalar: the Gaussian weights do not prevent a long consecutive
supercritical stretch, and they do not preserve the initially stabilizing
phase.

This is stronger than a stress test at a few moderate lengths.  It is a
certificate for explicitly named integers as large as \(16^{24}\), obtained
without enumerating \(M^2\) paths.  Its proof content is the exact moment
recurrence (2.3), the all-order identity (3.1), and the rigorous remainder
(4.3).

The finite inference boundary is essential.  A uniform estimate

\[
 |S_{4,m}|\le CM
\tag{5.1}
\]

allows an unspecified constant \(C\); no finite list of values can disprove
(5.1).  Nor does convergence of ten observed block ratios prove their
limit.  The present result therefore supplies a certified asymptotic
candidate, not an asymptotic theorem.

## 6. Next theorem

The normalized moment lift over one \(0100\) block is triangular by total
degree.  Its degree-zero diagonal block is the R0.64 matrix \(W\); higher
degree diagonal blocks inherit powers of the affine factor \(1/16\).  This
suggests the precise R0.66 task:

> Construct the analytic weighted-cycle transfer, isolate the
> \(\lambda=25.1515893341\ldots\) spectral projection, and prove with a
> rigorous tail estimate that the complete simplex functional has a nonzero
> projection onto that eigenmode.

If this succeeds, then

\[
 S_r=C_*\lambda^r+O(16^r),\qquad C_*\ne0,
\tag{6.1}
\]

and (5.1) fails on the explicit packet.  If the projection vanishes exactly,
the finite supercritical stretch must eventually collapse, and the
cancellation itself becomes the theorem.

## 7. Claim boundary

### Proved here

1. The exact bivariate moment recursion (2.3).
2. The exact simplex expansion (3.1) and rational remainder (4.3).
3. The finite sign pattern (1.2), ten certified inequalities (1.3), and the
   final-scale interval (1.5).

### Not proved

There is no proof that \(|S_r|/M_r\) is unbounded, no disproof of a uniform
quartic estimate, no control of all Picard orders, and no result for general
three-dimensional initial data.  This note does not solve the
Navier--Stokes Millennium problem.
