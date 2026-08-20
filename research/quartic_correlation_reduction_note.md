# R0.62 — Quartic correlation reduction and the first all-index remainder bound

## 1. Result

R0.61 reduced the complete quartic target coefficient of the tensor
Rudin--Shapiro shear packet to the dimensionless ratio

\[
 R_{L,M,m}=\frac{L^2m^2}{H^3}\frac{S_{4,m}}{S_{2,m}},
 \qquad H=4LM,
 \qquad 1\leq m\leq M.
\tag{1.1}
\]

The finite data suggested that \(R_{L,M,m}\) is uniformly bounded, but did
not prove it.  This note gives two all-index results.

First, the unweighted four-point sign sum has an exact three-carry tensor
factorization.  This identifies precisely why a bound on an ordinary
Rudin--Shapiro correlation is not yet the desired theorem: the heat kernel
couples the two tensor coordinates and destroys that factorization.

Second, direct use of the heat-flow Rudin--Shapiro bounds proves

\[
 \boxed{
 |R_{L,M,m}|
 \leq C_4\Bigl(\frac mM\Bigr)^2\sqrt M,
 \qquad C_4<7.9.}
\tag{1.2}
\]

The estimate is valid for every dyadic \(L,M\) and every
\(1\leq m\leq M\).  It removes all growth in the inner block length \(L\)
and improves the sign-free endpoint bound from order \(LM\) to order
\(\sqrt M\).  It does **not** close the uniform bound conjectured in R0.61;
one square-root factor remains.

Complete all-target scans at \(L=1\), newly extended through \(M=2048\),
still show no numerical square-root growth.  The largest values for
\(M=512,1024,2048\) are respectively

\[
 9.8557022728\times10^{-4},\qquad
 1.2127996802\times10^{-3},\qquad
 1.1457637854\times10^{-3}.
\tag{1.3}
\]

Thus (1.2) is a proved ceiling, not an observed asymptotic law.

## 2. Exact three-carry reduction

Write every carrier offset in tensor coordinates,

\[
 Q-H=rL+n,
 \qquad 0\leq r<M,
 \qquad 0\leq n<L,
\tag{2.1}
\]

and let \(c_{r,n}=b_ra_n\), where \(a_n\) and \(b_r\) are the two dyadic
Rudin--Shapiro sign sequences.  For a quartic relation \(A+B-C=Q\), put

\[
 A-H=r_AL+n_A,
 \quad B-H=r_BL+n_B,
 \quad C-H=r_CL+n_C.
\]

The relation is equivalent to

\[
 (r_A+r_B-r_C-r)L+(n_A+n_B-n_C-n)=0.
\tag{2.2}
\]

The second parenthesis is strictly between \(-2L\) and \(2L\).  It must be
a multiple of \(L\), so there is a unique carry \(k\in\{-1,0,1\}\) with

\[
 \begin{aligned}
 n_A+n_B-n_C-n&=kL,\\
 r_A+r_B-r_C-r&=-k.
 \end{aligned}
\tag{2.3}
\]

Define

\[
 I_{L,k}
 =\!\!\sum_{n_A+n_B-n_C-n=kL}
 a_na_{n_A}a_{n_B}a_{n_C}
 =[z^{kL}]P_L(z)^2P_L(z^{-1})^2,
\tag{2.4}
\]

and, for the target block \(r=m-1\),

\[
 O_{M,r,k}
 =b_r\!\!\sum_{r_A+r_B-r_C-r=-k}
 b_{r_A}b_{r_B}b_{r_C}
 =b_r[z^{r-k}]P_M(z)^2P_M(z^{-1}).
\tag{2.5}
\]

Then the complete **unweighted** carrier correlation factorizes exactly:

\[
 \boxed{
 \sum_{Q\in J_m}\sum_{A+B-C=Q}c_Qc_Ac_Bc_C
 =\sum_{k=-1}^{1} I_{L,k}O_{M,m-1,k}.}
\tag{2.6}
\]

This is an identity for every dyadic \(L,M\), not a finite-computation
claim.  The accompanying integer audit independently enumerates both sides
on small boxes.

The heat-weighted sum \(S_{4,m}\) in R0.61 contains
\(K_T(\alpha_0,\alpha_1,\alpha_2,0)\).  The rates depend on the full carrier
integers and on their time order, not separately on \(r\) and \(n\).
Consequently (2.6) cannot simply be multiplied by one scalar heat weight.
This coupling is the exact remaining analytic obstacle.

## 3. Heat-flow bounds for the two inputs

Let

\[
 C_{\rm RS}=2+\sqrt2,
 \qquad C_T=(1+\sqrt2)C_{\rm RS}.
\tag{3.1}
\]

The prefix estimate proved in R0.58 and its tensor form from R0.59 give, for
the real shear carrier polynomial \(F\),

\[
 \|e^{s\Delta}F\|_{L^\infty(\mathbb T)}
 \leq 2C_T\sqrt{LM}\,e^{-H^2s}.
\tag{3.2}
\]

In one fixed positive \(m\)-sector, the initial \(G\) packet contains one
block of \(L\) coefficients.  One-dimensional Abel summation gives

\[
 \|G_{1,m}(s)\|_{L^\infty(\mathbb T^2)}
 \leq C_{\rm RS}\sqrt L\,e^{-(H^2+m^2)s}.
\tag{3.3}
\]

Both estimates include the heat weights.  They are therefore applicable to
the actual Duhamel recurrence, rather than only to the unweighted identity
(2.6).

## 4. An all-index quartic estimate

Within the invariant shear class the fixed-sector Picard recurrence is

\[
 G_{n,m}(t)
 =-\int_0^t e^{(t-s)\Delta}
 F(s)\,\partial_2G_{n-1,m}(s)\,ds.
\tag{4.1}
\]

The heat semigroup is an \(L^\infty\) contraction and
\(\partial_2\) is multiplication by \(im\) in this sector.  Iterating (4.1)
three times, inserting (3.2)--(3.3), and discarding only positive heat decay
gives

\[
 \begin{aligned}
 \|G_{4,m}(t_H)\|_\infty
 &\leq m^3(2C_T\sqrt{LM})^3C_{\rm RS}\sqrt L
 \int_{0<s_1<s_2<s_3<t_H}ds_1ds_2ds_3\\
 &=\frac43 C_{\rm RS}C_T^3T^3
 m^3H^{-6}L^2M^{3/2},
 \end{aligned}
\tag{4.2}
\]

where \(t_H=T/H^2\) and \(T=(\log2)/2\).  A Fourier coefficient is bounded
by the \(L^\infty\) norm.  Comparing (4.2) with the exact coefficient formula

\[
 |\widehat G_4(0,m,t_H)|=m^3H^{-6}|S_{4,m}|
\]

therefore proves

\[
 \boxed{
 |S_{4,m}|\leq
 \frac43 C_{\rm RS}C_T^3T^3L^2M^{3/2}.}
\tag{4.3}
\]

For \(Q/H\in[1,5/4)\), the summand in \(S_{2,m}\) is decreasing in
\(Q/H\).  Hence

\[
 S_{2,m}\geq \kappa_2L,
 \qquad
 \kappa_2:=\frac8{25}\left(1-2^{-25/16}\right).
\tag{4.4}
\]

Substitution of (4.3)--(4.4) into (1.1), using \(H=4LM\), yields

\[
 |R_{L,M,m}|
 \leq
 \frac{C_{\rm RS}C_T^3T^3}{48\kappa_2}
 \frac{m^2}{M^{3/2}}
 =C_4\Bigl(\frac mM\Bigr)^2\sqrt M.
\tag{4.5}
\]

Direct 60-decimal evaluation gives \(C_4<7.9\).  The decimal is only a
display of the explicit constant in (4.5); it is not used to prove the
inequality.

## 5. Numerical stress test of the remaining factor

The R0.61 scanner was run for every target at \(L=1\) and
\(M=512,1024,2048\).  The three runs contain 3584 target evaluations.  They
were deterministic, used 18 local workers, and completed in approximately
1.8, 6.0, and 35.8 seconds.  The worst targets were

| \(M\) | worst \(m\) | \(\max_m R_{1,M,m}\) |
|---:|---:|---:|
| 512 | 481 | 0.0009855702272829397 |
| 1024 | 981 | 0.0012127996801718404 |
| 2048 | 1912 | 0.0011457637853978923 |

The maximum over these three full profiles is below the earlier R0.61 value
\(R_{4,64,64}\approx0.0013286563\).  This strongly separates the proved
\(O(\sqrt M)\) ceiling from observed behaviour, but it does not prove a
uniform constant or positivity.

An unweighted cubic Rudin--Shapiro convolution does grow along selected
dyadic levels.  Therefore the hoped-for theorem cannot be obtained by
replacing the heat kernel with its supremum and bounding one ordinary
correlation coefficient.  Smoothness and time ordering must be retained.

## 6. Exact statements, finite evidence, and open problem

### Proved for every index

1. Only the three carries \(-1,0,1\) occur, and (2.6) is an exact unweighted
   tensor factorization.
2. The heat-weighted quartic sum satisfies (4.3).
3. The normalized quartic ratio satisfies the all-index estimate (1.2).
4. The estimate is independent of \(L\) and retains only \(\sqrt M\) growth.

### Finite computational evidence

1. All 3584 newly scanned \(L=1\) target values are positive.
2. Their maxima remain at scale \(10^{-3}\) through \(M=2048\).
3. These observations do not approach the proved ceiling and show no visible
   \(\sqrt M\) growth.

### Not proved

R0.62 does not prove a bound independent of \(M\), all-index positivity,
control of the complete even Picard series, norm inflation, singularity
formation, or global regularity for arbitrary three-dimensional data.  It
does not solve the Clay Millennium problem.  The packet remains inside a
globally regular invariant shear class.

## 7. Next lemma

The remaining target is now narrower than in R0.61:

> Prove that the heat-weighted four-point multiplier gains the missing
> \(M^{-1/2}\) relative to (4.3), equivalently
> \(|S_{4,m}|\leq C L^2M\), uniformly in \(m\).

The next step is to express the simplex kernel as its time integral before
summing the signs, then apply the two-state Rudin--Shapiro recursion at each
time layer.  A dyadic recursion with a contractive matrix norm would prove
the desired uniform bound.  If the matrix norm is only marginal, the exact
outer convolution growth identified by (2.6) will locate the obstruction
without confusing it with the heat-weighted problem.
