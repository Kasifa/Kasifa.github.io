# R0.38: a tail-aware Newton restart beyond the R0.37 radius

## Status and boundary

R0.37 put the reduced active equation in a one-derivative weighted Wiener
space and proved a same-radius all-order bound.  Its degree-40 restart used
the full-space estimate

\[
 \|D\Phi(p)h\|_{\mathcal B_r}
 \le 6\|p\|_{\mathcal B_r}\|h\|_{\mathcal B_r}.
\tag{0.1}
\]

I first tested the proposed next step: insert the exact 62-dimensional
Jacobian inverse as a low-block preconditioner.  The total-degree grading
shows that this block is inert on the correction space used by the restart.
It is a valid finite inverse, but it does not reduce the infinite tail
defect.

The useful improvement comes from the same grading.  A degree-\(N\)
polynomial and a correction supported strictly above degree \(N\) have
disjoint degree supports.  Keeping this information in the R0.37
mixed-layer inequality almost halves the derivative constant.  With
\(N=80\), an exact rational contraction increases the proved common radius
from

\[
 r_{37}=\frac{16}{243}
 \quad\hbox{to}\quad
 r_{38}=\frac{59}{500}.
\tag{0.2}
\]

The ratio is

\[
 \frac{r_{38}}{r_{37}}
 =\frac{14337}{8000}
 =1.792125.
\tag{0.3}
\]

The all-order tail theorem and Banach contraction prove this new radius for
the reduced active and normalized transport fields.  The degree-80
polynomial, 62-dimensional inverse, and 55 degree-81 tail columns are finite
exact computations.  This result does not prove regularity or blow-up for
the full three-dimensional Navier--Stokes equation, and it does not certify
the R0.32 finite Padé candidate.

## 1. Weighted support-cone space

For a monomial \(Z^nW^k\), write

\[
 L=n+k,
 \qquad
 q=2k-n.
\tag{1.1}
\]

The active series lies in the support cone \(q\ge-1\).  R0.37 used the
complete coefficient space

\[
 \mathcal B_r^+
 =
 \left\{
 f=\sum_{q\ge-1}f_{n,k}Z^nW^k:
 \|f\|_{\mathcal B_r}
 =\sum_{n,k}(n+k)|f_{n,k}|r^{n+k}<\infty
 \right\}.
\tag{1.2}
\]

If \(A_i\) and \(H_j\) are the homogeneous coefficient \(\ell^1\) norms of
\(f\) and \(h\), respectively, the all-order polarized estimate is

\[
 \|(D\Phi(f)h)_L\|_1
 \le
 \frac32
 \sum_{i+j=L}
 \min(i,j)(A_iH_j+H_iA_j).
\tag{1.3}
\]

No finite charge cutoff is used in (1.3).  The cancellation of the
charge-\(-2\) output from two charge-\(-1\) inputs makes the support cone
invariant.

## 2. The tail-aware derivative theorem

Let

\[
 p_N=\sum_{1\le i\le N}p_i,
 \qquad
 h=\sum_{j>N}h_j,
\tag{2.1}
\]

and put

\[
 A_i=\|p_i\|_1,
 \qquad
 M_N(r)=\sum_{i=1}^N iA_i r^i,
 \qquad
 S_N(r)=\sum_{i=1}^N i^2A_i r^i.
\tag{2.2}
\]

The two terms in the polarized sum (1.3) agree after swapping \(i,j\).
Because every nonzero pair now satisfies \(i\le N<j\),

\[
 \min(i,j)=i,
 \qquad
 \frac{i+j}{j}=1+\frac ij
 \le 1+\frac{i}{N+1}.
\tag{2.3}
\]

Multiplying (1.3) by \((i+j)r^{i+j}\), summing, and using (2.3) proves

\[
 \begin{aligned}
 \|D\Phi(p_N)h\|_{\mathcal B_r}
 &\le
 3\sum_{\substack{i\le N\\j>N}}
 (i+j)iA_iH_jr^{i+j}\\
 &\le
 3\left(
 M_N(r)+\frac{S_N(r)}{N+1}
 \right)
 \|h\|_{\mathcal B_r}.
 \end{aligned}
\tag{2.4}
\]

Thus the exact all-order tail constant is bounded by

\[
 \boxed{
 Z_N(r)
 =
 3\left(
 M_N(r)+\frac{S_N(r)}{N+1}
 \right).
 }
\tag{2.5}
\]

The estimate uses every uncomputed tail degree \(j>N\); it is not a finite
column scan.  The general quadratic estimate remains

\[
 \|\Phi(h)\|_{\mathcal B_r}
 \le3\|h\|_{\mathcal B_r}^2.
\tag{2.6}
\]

## 3. Why the exact low inverse does not produce the gain

Let \(P_m\) project onto correction degrees at most \(m\), let
\(J=I-D\Phi(p_N)\), and define the natural block preconditioner

\[
 \mathcal A_m
 =
 P_m(P_mJP_m)^{-1}P_m+(I-P_m).
\tag{3.1}
\]

For R0.38, \(m=12\) and \(N=80\).  If \(h\) is supported above degree
\(N\), then \(D\Phi(p_N)h\) is also supported above \(N\): every factor of
\(p_N\) has positive degree.  Therefore

\[
 P_mJh=0,
 \qquad
 \mathcal A_mJh=Jh,
\tag{3.2}
\]

and hence

\[
 \boxed{
 (I-\mathcal A_mJ)h=D\Phi(p_N)h.
 }
\tag{3.3}
\]

The exact low inverse handles low inputs, but the recurrence polynomial
already has zero residual there and the tail fixed-point map never produces
them.  Consequently the 62-dimensional inverse cannot improve the certified
tail contraction.  I retain it as an exact regression and as evidence that
the proposed preconditioning mechanism was checked rather than assumed.

## 4. Exact degree-80 restart

Let \(p_{80}\) be the exact recurrence polynomial through total degree 80,
and define

\[
 F(p)=p-(Z+W)-\Phi(p).
\tag{4.1}
\]

Triangular recurrence makes every coefficient of \(F(p_{80})\) through
degree 80 vanish.  Its complete residual has 6345 nonzero terms in degrees
81 through 160.

At

\[
 r_*=\frac{59}{500},
\tag{4.2}
\]

the exact certificate gives

\[
 \begin{aligned}
 M_{80}(r_*)&\approx0.32561381732092066191,\\
 S_{80}(r_*)&\approx0.42267275596390072178,\\
 6M_{80}(r_*)&\approx1.9536829039255239715,\\
 Z_{80}(r_*)&\approx0.99249599847994349395.
 \end{aligned}
\tag{4.3}
\]

The third line is important: the old R0.37 full-space bound is greater than
one at this radius.  Merely raising the polynomial cutoff does not close the
old proof.  The strict margin

\[
 m=1-Z_{80}(r_*)
 \approx0.0075040015200565060461
\tag{4.4}
\]

comes from the all-order tail theorem (2.5).

As a nearby negative control, the same exact sufficient bound at
\(r=19/160=0.11875\) is approximately \(1.0007181486>1\).  Thus that
slightly larger radius is not certified by this inequality.  This failure
does not prove that the canonical series is nonanalytic there.

The complete exact residual satisfies

\[
 Y=\|F(p_{80})\|_{\mathcal B_{r_*}}
 \approx7.4633025649988919148\times10^{-70}.
\tag{4.5}
\]

Choose

\[
 \varepsilon=\frac m{12}
 \approx0.00062533346000470883718.
\tag{4.6}
\]

On the closed support-cone tail space of degrees above 80, solve

\[
 h=-F(p_{80})+D\Phi(p_{80})h+\Phi(h).
\tag{4.7}
\]

This space is invariant: the residual begins at degree 81,
\(D\Phi(p_{80})\) raises a degree-above-80 input, and \(\Phi(h)\) begins
above degree 160.  Equations (2.5) and (2.6) give

\[
 \|\mathcal T(h)\|
 \le
 Y+Z_{80}\varepsilon+3\varepsilon^2.
\tag{4.8}
\]

The exact residual allowance is

\[
 \frac{m^2}{16}
 \approx3.5193774258131470820\times10^{-6},
\tag{4.9}
\]

so the residual uses only

\[
 2.1206314816531809212\times10^{-64}
\tag{4.10}
\]

of the allowance.  The mapping and Lipschitz checks are

\[
 \begin{aligned}
 Y+Z_{80}\varepsilon+3\varepsilon^2
 &\approx0.00062181408257889569009
 <\varepsilon,\\
 Z_{80}+6\varepsilon
 &=\frac{1+Z_{80}}2
 \approx0.99624799923997174698
 <1.
 \end{aligned}
\tag{4.11}
\]

Banach's theorem produces a unique \(h\) in the ball.  Triangular formal
uniqueness identifies \(p_{80}+h\) with the canonical active series.

## 5. Transport fields

The R0.37 transport estimate is

\[
 \|T_af\|_{\mathcal B_r}
 \le2\|a\|_{\mathcal B_r}\|f\|_{\mathcal B_r}.
\tag{5.1}
\]

The restart ball gives

\[
 \|a\|_{\mathcal B_{r_*}}
 \le M_{80}(r_*)+\varepsilon
 \approx0.32623915078092537075.
\tag{5.2}
\]

Therefore

\[
 \|T_a\|
 \le0.6524783015618507415<1,
\qquad
 \|(I-T_a)^{-1}\|
 \le2.8775181650361801284.
\tag{5.3}
\]

The canonical normalized transport fields \(U,V\) are consequently
absolutely analytic at the same new radius \(59/500\).  This does not prove
that the logarithmic quotients from R0.29 are nonzero throughout the entire
larger polydisc.

## 6. Finite exact regressions

The finite calculations have a narrower role than the theorem:

1. the GMP recurrence reaches degree 80 after 1113168 ordered
   interactions;
2. the degree-80 polynomial has 2161 nonzero terms;
3. the complete residual has 6345 terms and is included through degree 160;
4. the degree-12 support-cone Jacobian is the same 62-dimensional unit
   lower-triangular matrix as in R0.37;
5. its exact inverse passes on both sides and its two hashes match R0.37;
6. all 55 admissible degree-81 tail columns stay above the cutoff and inside
   the support cone;
7. their exact maximum weighted column ratio is approximately
   \(0.16577696827316245098\), below the all-order bound;
8. the maximum finite column is the input \(W^{81}\).

The finite column maximum is only about \(0.16703\) of the analytic bound.
It suggests room for a future charge-resolved norm, but it does not justify
replacing the all-order constant by the observed finite value.

## 7. Scale of the radius gain

Relative to R0.37,

\[
 \frac{r_{38}}{r_{37}}
 =1.792125,
\qquad
 \left(\frac{r_{38}}{r_{37}}\right)^3
 \approx5.7557893960.
\tag{7.1}
\]

Relative to the original R0.31 radius \(4/81\), the bivariate and
fixed-charge gains are

\[
 2.3895,
\qquad
 13.643352642375.
\tag{7.2}
\]

The finite R0.32 transport-candidate cluster still lies outside the proved
fixed-charge disk.  Using the lower edge of the pinned finite cluster, the
gap factor remains greater than approximately

\[
 456.1281093.
\tag{7.3}
\]

This comparison does not turn the finite candidate into a singularity.
More importantly, the reduced edge system has not been proved to control the
critical dynamics of the full three-dimensional PDE.

## 8. Next mathematical question

The exact degree-81 column scan is much smaller than the charge-blind
all-order bound.  R0.39 should therefore split the tail norm by charge sign
or charge sector and derive a finite-dimensional positive majorant matrix
whose spectral radius controls all uncomputed degrees.  The success
criterion is an all-order matrix bound, not a finite tail scan.

## Reproduction

Run research/edge_tail_newton_audit.py from the repository root.  The formal
certificate pins its clean source commit in the git.commit field and pins
the R0.32 and R0.37 input hashes.  The run uses exact GMP rationals, an
append-only progress log, and a process-tree resource log.  It uses no
random seed, GPU, or floating-point sign decision.

## References

1. R0.30, *An all-order analytic majorant for the canonical edge system*.
   This supplies the active and transport layer inequalities.
2. R0.31, *An improved common analytic domain for the canonical edge
   system*.  This supplies the first common analytic radius.
3. R0.32, *A finite fixed-charge singularity-candidate audit*.  Its candidate
   cluster is used only for scale comparison.
4. R0.37, *A weighted-Wiener restart beyond the R0.31 radius*.  This supplies
   the weighted space, the support-cone theorem, and the first all-order
   restart beyond the old radius.
