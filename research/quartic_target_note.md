# R0.61 — The complete quartic target coefficient

## 1. Question and answer

R0.60 proved that the tensor Rudin--Shapiro packet stays in the invariant
shear class

\[
 u=(0,F(x_1,t),G(x_1,x_2,t))
\]

and that its cubic Picard term cannot reach the target plane
\(\xi_1=0\).  The first support-admissible correction to the coherent
quadratic target is therefore quartic.

R0.61 computes that quartic coefficient exactly as a finite, all-index path
formula.  At the distinguished time

\[
 t_H=\frac{T}{H^2},\qquad T=\frac{\log2}{2},
\]

and amplitude \(A=\varepsilon\sqrt H\), the ratio of the quartic and
quadratic Fourier coefficients at \(k_m=(0,m,0)\) is

\[
 \boxed{
 \frac{A^4\widehat G_4(0,m,t_H)}
      {A^2\widehat G_2(0,m,t_H)}
 =-\frac{\varepsilon^2}{L^2}R_{L,M,m}.}
\tag{1.1}
\]

The dimensionless number \(R_{L,M,m}\) is given explicitly below.  No
quadrature or time stepping is used in its definition; the only
transcendental operation is evaluation of exponentials in a confluent divided
difference.

A large deterministic numerical audit finds

\[
 0<R_{L,M,m}\leq 1.3286562612067\times10^{-3}
\tag{1.2}
\]

on 464 evaluated parameter--target instances, comprising 461 distinct
triples \((L,M,m)\), 49 distinct pairs \((L,M)\), and
7,494,536,238 ordered quartic paths.  The maximum occurs at
\((L,M,m)=(4,64,64)\).  A 60-decimal calculation independently reproduces
that value with relative discrepancy below \(5.6\times10^{-15}\) from the
long-double scanner.

The sign in (1.1) has a direct interpretation.  Positive \(R_{L,M,m}\) means
that the quartic target is opposite in phase to the quadratic target: it
dresses the coherent output down rather than reinforcing it.

Equation (1.1) and the path formula are exact.  Inequality (1.2), positivity,
and the absence of growth in \(M\) are **finite numerical evidence**, not an
all-index theorem.  The remaining mathematical problem is a weighted
four-point Rudin--Shapiro correlation estimate uniform in \(M\).

## 2. Fourier recurrence in one target sector

Put

\[
 N=LM,\qquad H=4N,\qquad I_N=\{H,H+1,\ldots,H+N-1\}.
\tag{2.1}
\]

For positive second frequency \(m\), the initial \(G\) carriers are

\[
 -Q,\qquad Q\in J_m
 :=\{H+(m-1)L,\ldots,H+mL-1\}.
\tag{2.2}
\]

Let \(c_P\in\{-1,1\}\) denote the tensor Rudin--Shapiro sign attached to
\(P\in I_N\).  The real shear has equal coefficients at \(P\) and \(-P\).
After removing the common amplitude, write \(g_n(k,t)\) for the first Fourier
coordinate \(k\) of the order-\(n\) term in the fixed positive-\(m\) sector.
The invariant-shear recurrence from R0.60 becomes

\[
 \boxed{
 \partial_tg_n(k,t)+(k^2+m^2)g_n(k,t)
 =-im\sum_{p\in\pm I_N}c_{|p|}e^{-p^2t}
        g_{n-1}(k-p,t).}
\tag{2.3}
\]

Initially,

\[
 g_1(-Q,t)=c_Qe^{-(Q^2+m^2)t},\qquad Q\in J_m.
\tag{2.4}
\]

Every interaction preserves \(m\), and every order after the first is
polarized in the \(e_3\) direction.  Thus (2.3) contains the complete quartic
calculation; no omitted Leray branch or binary Picard tree remains.

## 3. The quadratic reference coefficient

The quadratic target path is uniquely \(-Q+Q=0\).  Direct integration gives

\[
 \widehat G_2(0,m,t_H)
 =-im\,e^{-m^2t_H}H^{-2}S_{2,m},
\tag{3.1}
\]

where

\[
 \boxed{
 S_{2,m}=\sum_{Q\in J_m}
 \frac{1-e^{-2(Q/H)^2T}}{2(Q/H)^2}>0.}
\tag{3.2}
\]

This is the dimensionless form of the coefficient \(d_m(t_H)\) in R0.59.

## 4. Exact enumeration of all quartic target paths

A quartic target path begins at \(-Q\) and uses three shear carriers
\(p_1,p_2,p_3\in\pm I_N\).  It must satisfy

\[
 p_1+p_2+p_3=Q.
\tag{4.1}
\]

Because \(H=4N\), the only possible sign pattern has two positive carriers
and one negative carrier.  Indeed, three positive carriers exceed
\(H+N-1\), while one positive carrier minus two positive magnitudes is
negative.  Hence every path can be written

\[
 A+B-C=Q,qquad A,B,C\in I_N,
\tag{4.2}
\]

with the negative carrier placed in one of the three time slots.  Taking
\((A,B)\) as an ordered pair, the complete ordered path list is

\[
 (A,B,-C),\qquad(A,-C,B),\qquad(-C,A,B).
\tag{4.3}
\]

This convention counts every ordered path exactly once, including the case
\(A=B\).

For one such path set

\[
 k_0=-Q,\qquad k_1=-Q+p_1,\qquad
 k_2=-Q+p_1+p_2,\qquad k_3=0.
\tag{4.4}
\]

The four dimensionless heat rates on the four time intervals are

\[
 \begin{aligned}
 \alpha_0&=\frac{Q^2+p_1^2+p_2^2+p_3^2}{H^2},\\
 \alpha_1&=\frac{k_1^2+p_2^2+p_3^2}{H^2},\\
 \alpha_2&=\frac{k_2^2+p_3^2}{H^2},\\
 \alpha_3&=0.
 \end{aligned}
\tag{4.5}
\]

Define the positive three-simplex heat kernel

\[
 \begin{aligned}
 K_T(\alpha_0,\alpha_1,\alpha_2,\alpha_3)
 &:={\int_{\substack{\tau_j\geq0\\
                    \tau_0+\tau_1+\tau_2+\tau_3=T}}}
 e^{-\sum_{j=0}^3\alpha_j\tau_j}
 \,d\tau_0\,d\tau_1\,d\tau_2\\
 &=-[\alpha_0,\alpha_1,\alpha_2,\alpha_3]e^{-Tx}.
 \end{aligned}
\tag{4.6}
\]

The bracket denotes the third divided difference.  Repeated rates are
interpreted confluently.  This is essential: adjacent rates can coincide, for
example when \(k_1=0\), so a partial-fraction formula with distinct
denominators is not valid for every path.

The complete dimensionless quartic sum is

\[
 \boxed{
 \begin{aligned}
 S_{4,m}:={}&\sum_{Q\in J_m}
 \sum_{\substack{A,B\in I_N\\C=A+B-Q\in I_N}}
 c_Qc_Ac_Bc_C\\
 &\quad\times\sum_{(p_1,p_2,p_3)\in\mathcal P(A,B,C)}
 K_T(\alpha_0,\alpha_1,\alpha_2,0),
 \end{aligned}}
\tag{4.7}
\]

where

\[
 \mathcal P(A,B,C)=\{(A,B,-C),(A,-C,B),(-C,A,B)\}.
\]

Three Duhamel integrations and the factor \((-im)^3=im^3\) now give

\[
 \boxed{
 \widehat G_4(0,m,t_H)
 =im^3e^{-m^2t_H}H^{-6}S_{4,m}.}
\tag{4.8}
\]

Combining (3.1) and (4.8) proves (1.1) with

\[
 \boxed{
 R_{L,M,m}=\frac{L^2m^2}{H^3}\frac{S_{4,m}}{S_{2,m}}.}
\tag{4.9}
\]

Equations (4.7)--(4.9) are valid for every dyadic \(L,M\) and every
\(1\leq m\leq M\).

## 5. Numerical audit and reproducibility

The C++20 scanner `research/quartic_target_scan.cpp` evaluates (3.2) and
(4.7) with long-double arithmetic.  It sorts the four integer rates before
forming divided differences and inserts the analytic derivative whenever
rates coincide.  Each worker uses compensated summation for both the signed
and absolute path sums.

Three deterministic scan families were run:

1. 30 edge-target pairs covering \(L=1\) through \(512\), \(M=1\) through
   \(1024\), and a diagonal family through \(L=M=32\);
2. 18 extended edge-target pairs reaching \((L,M)=(1,8192)\),
   \((2,4096)\), \((4,2048)\), \((8,1024)\), \((64,64)\), and
   \((1024,1)\);
3. every target in the four families \((1,256)\), \((4,64)\),
   \((8,64)\), and \((16,32)\), for 416 target evaluations.

After deduplication, these runs cover 461 distinct triples and 49 distinct
parameter pairs.  Every computed \(R_{L,M,m}\) is positive.  The largest
observed cancellation condition number is about \(3.86\times10^3\), which
makes an independent high-precision check necessary but remains far below
the precision margin of the long-double calculation.

The 60-decimal recomputation at the observed maximum gives

\[
 \begin{aligned}
 S_{2,64}&=0.8481125347427871303694831598510949486846\ldots,\\
 S_{4,64}&=18.46231088322773886542058198564857587878\ldots,\\
 R_{4,64,64}&=0.001328656261206690024552778522639094235268\ldots.
 \end{aligned}
\tag{5.1}
\]

The archived package contains the aggregate JSON tables, the high-precision
record, progress and resource logs, source hashes, and a journal-size figure.
No random sampling is used.

## 6. What has and has not been proved

### Exact statements

1. The invariant shear recurrence (2.3) is the complete Picard recurrence for
   this packet.
2. Every quartic target path has the form (4.2)--(4.3), and every such ordered
   path is included exactly once in (4.7).
3. The simplex kernel is the confluent divided difference (4.6), including
   all repeated-rate cases.
4. The exact coefficient identities (3.1), (4.8), and ratio formula (1.1)
   hold for all dyadic \(L,M\) and all targets \(1\leq m\leq M\).

### Finite computational evidence

1. Positivity of \(R_{L,M,m}\) on the 461 distinct evaluated triples.
2. The observed maximum in (1.2).
3. No observed growth in \(M\) over the scanned edge families.
4. Agreement of the observed maximum between long-double and 60-decimal
   arithmetic.

### Not proved

R0.61 does **not** prove:

1. \(R_{L,M,m}\geq0\) for every index;
2. a constant \(C\) such that \(|R_{L,M,m}|\leq C\) for every index;
3. a bound for the complete sum of all Picard orders at amplitude
   \(A=\varepsilon\sqrt H\);
4. norm inflation, finite-time blow-up, or global regularity for arbitrary
   three-dimensional data;
5. a solution of the Clay Millennium problem.

The underlying packet is still in a globally regular shear class.  The result
measures one nonlinear cancellation mechanism inside a sharpness test; it is
not a singularity construction.

## 7. Research value and the next theorem

The direct numerical alternative posed in R0.60 has a clear answer: the
complete quartic target coefficient does not exhibit the feared growth in
\(M\) on a broad deterministic scan.  It is small after the natural
\(L^{-2}\) normalization and has the stabilizing phase throughout the tested
set.

A sign-free estimate cannot explain this.  Since
\(0<K_T\leq T^3/6\), counting absolute paths loses precisely the tensor
cancellation needed for uniformity.  The next step is therefore not a larger
blind scan but the following analytic problem:

> Prove a smooth weighted four-point Rudin--Shapiro correlation bound for
> the kernel in (4.7), strong enough to show
> \(\sup_{L,M,m}|R_{L,M,m}|<\infty\), preferably with positivity or a sharp
> constant as a separate question.

The natural tools are tensor Rudin--Shapiro recursion, multivariate Abel
summation, and a quantitative variation bound for the confluent heat kernel.
Such a theorem would convert the observed quartic \(L^{-2}\) gain into the
first all-index nonlinear remainder estimate for this packet.  It would still
be a result about a special globally regular class, but it would be a genuine
analytic advance beyond the finite computation.

