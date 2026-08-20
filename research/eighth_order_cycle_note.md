# R0.68B-1 — The exact zero-time eighth-order image spectrum

## 1. Result and boundary

R0.68A reduced the complete periodic target problem to one finite missing
term: the eighth-order heat coefficient.  This note closes the first half of
that obstruction.  It proves the exact **zero-time** seven-carrier spectrum
and the nonzero reachable projection.  The seven-simplex heat weight is not
yet included.

Let

\[
 M_r=16^r,\qquad q_r=2\frac{16^r-1}{15},
\tag{1.1}
\]

and let \(a_n^s(j)\), \(s\in\{0,1\}\), denote the two Rudin--Shapiro
coefficient states.  Define

\[
 \begin{aligned}
 Y_{8,r}={}&a_{4r}^0(q_r)
 \sum_{\substack{A+B+C+D-E-F-G=q_r\\
                  0\le A,B,C,D,E,F,G<M_r}}
 a_{4r}^0(A)a_{4r}^0(B)a_{4r}^0(C)a_{4r}^0(D)\\
 &\hspace{37mm}\times
 a_{4r}^0(E)a_{4r}^0(F)a_{4r}^0(G).
 \end{aligned}
\tag{1.2}
\]

There is a real constant \(C_{8,0}\) such that

\[
 \boxed{Y_{8,r}=C_{8,0}\nu^r+O(4800^r),}
\tag{1.3}
\]

where

\[
 \nu=256\lambda,
 \qquad
 6438.806869529984<\nu<6438.806869530010,
\tag{1.4}
\]

and \(\lambda\) is the dominant R0.66 quartic root.  Exact rational interval
arithmetic gives

\[
 \boxed{
 -0.02612679363405570
 < C_{8,0}
 < -0.02612679362708268.}
\tag{1.5}
\]

The remainder radius \(4800\), the root bracket, and the coefficient interval
are certified with integer polynomials and rational endpoints.  No displayed
decimal is used as proof.

Equations (1.3)--(1.5) are not the eighth-order heat theorem.  They do not
evaluate the complete seven-simplex kernel, and they do not by themselves
close the last finite term in R0.68A.

## 2. Complete eighth-order path formula

Use

\[
 N=LM,\qquad H=4N,\qquad I_N=\{H,\ldots,H+N-1\}.
\tag{2.1}
\]

An order-eight target path starts at \(-Q\), adds seven shear carriers, and
ends at first frequency zero.  Shell separation forces exactly four positive
and three negative carriers:

\[
 \boxed{A+B+C+D-E-F-G=Q.}
\tag{2.2}
\]

There are

\[
 \binom{7}{4}=35
\tag{2.3}
\]

sign shuffles.  For a fixed ordered path write

\[
 k_0=-Q,\qquad
 k_j=-Q+\sum_{\ell=1}^j p_\ell,
 \quad 1\le j\le7,
 \qquad k_7=0.
\tag{2.4}
\]

Its eight dimensionless heat rates are

\[
 \alpha_j
 =\frac{k_j^2+\sum_{\ell=j+1}^7p_\ell^2}{H^2},
 \quad0\le j\le6,
 \qquad \alpha_7=0.
\tag{2.5}
\]

Let

\[
 K_T^{(7)}(\alpha_0,\ldots,\alpha_7)
 =
 \int_{\substack{\tau_j\ge0\\\tau_0+\cdots+\tau_7=T}}
 e^{-\sum_{j=0}^7\alpha_j\tau_j}
 \,d\tau_0\cdots d\tau_6.
\tag{2.6}
\]

Then the complete dimensionless heat sum is

\[
 \begin{aligned}
 S_{8,m}={}&
 \sum_{Q\in J_m}
 \sum_{\substack{A,B,C,D,E,F\in I_N\\
 G=A+B+C+D-E-F-Q\in I_N}}
 c_Qc_Ac_Bc_Cc_Dc_Ec_Fc_G\\
 &\times
 \sum_{\omega\in\operatorname{Sh}(4,3)}
 K_T^{(7)}(\alpha_0,\ldots,\alpha_7).
 \end{aligned}
\tag{2.7}
\]

Seven Duhamel integrations give

\[
 \boxed{
 \widehat G_8(0,m,t_H)
 =im^7e^{-m^2t_H}H^{-14}S_{8,m}.}
\tag{2.8}
\]

Relative to the exact quadratic reference,

\[
 \boxed{
 \frac{A^8\widehat G_8(0,m,t_H)}
      {A^2\widehat G_2(0,m,t_H)}
 =-\frac{\varepsilon^6}{L^6}R_{8,L,M,m},
 \qquad
 R_{8,L,M,m}
 =\frac{L^6m^6}{H^9}\frac{S_{8,m}}{S_{2,m}}.}
\tag{2.9}
\]

The minus sign is the next alternating Picard phase after the positive
sixth-order ratio.

## 3. The 1792-state exact transfer

At one binary level, the seven carrier signs require

\[
 \boldsymbol\sigma\in\{0,1\}^7,
\tag{3.1}
\]

and the carry lies in

\[
 k\in\{-3,-2,-1,0,1,2,3\}.
\tag{3.2}
\]

Together with the target sign state, the direct closure has

\[
 \boxed{2\times128\times7=1792\ \text{states}.}
\tag{3.3}
\]

If the next target bit is \(b\) and the carrier bits are
\(\boldsymbol\varepsilon\), the child carry is

\[
 k'=2k+b-
 (\varepsilon_1+\varepsilon_2+\varepsilon_3+\varepsilon_4
 -\varepsilon_5-\varepsilon_6-\varepsilon_7),
\tag{3.4}
\]

with signed transition coefficient

\[
 (-1)^{sb+\boldsymbol\sigma\cdot\boldsymbol\varepsilon}.
\tag{3.5}
\]

Each digit matrix has 114,688 nonzero entries and exact rational rank 448.
The audit compares the transfer with direct seven-fold convolution in every
one of the 1792 states through six binary levels.

## 4. Exact four-bit image spectrum

Let \(W_8\) be the least-significant-bit-first \(0100\) cycle.  Exact
rational ranks are

\[
 \boxed{
 \operatorname{rank}W_8=204,
 \qquad
 \operatorname{rank}W_8^2
 =\operatorname{rank}W_8^3=148.}
\tag{4.1}
\]

The restriction to \(\operatorname{im}W_8\) has characteristic polynomial

\[
 \boxed{
 \chi_{\rm im}(x)
 =x^{56}(x-4096)^{14}
 q_{4,256}(x)^{14}
 q_{10,16}(x)^6q_{18}(x).}
\tag{4.2}
\]

Here

\[
 q_{4,256}(x)=256^4p(x/256)
 =x^4-6400x^3-7864320x^2
 +54492397568x-35184372088832,
\tag{4.3}
\]

where \(p\) is the R0.66 quartic, and

\[
 q_{10,16}(x)=16^{10}q_{10}(x/16),
\tag{4.4}
\]

where \(q_{10}\) is the R0.67A degree-ten factor.  The new factor is

\[
\begin{aligned}
q_{18}(x)={}&x^{18}-6969x^{17}-2590744x^{16}
 +139397444912x^{15}\\
&-426297237954560x^{14}
 +65541085313761280x^{13}\\
&+1817561819293822222336x^{12}
 -12923427431300516632592384x^{11}\\
&+72083289706196062643987415040x^{10}\\
&-147173596220605159573753471959040x^9\\
&-29101569723662770535965645510541312x^8\\
&+382197970754416550433344819302481526784x^7\\
&-749472734550488533458838292284403557072896x^6\\
&+2161494797667240625211172063217942790211108864x^5\\
&+3167861340246684172706078559046764091092737458176x^4\\
&-9714642251431883530476110829655218596491783122714624x^3\\
&-5562654259926397846713126171648909197020814256315039744x^2\\
&-320199342064115143523122610176213995501458910461684613120x\\
&+93468964114928862759328348387927361466359102381601325056000.
\end{aligned}
\tag{4.5}
\]

The full 1792-state characteristic polynomial is

\[
 x^{1588}\chi_{\rm im}(x).
\tag{4.6}
\]

The 204 image coefficients obtained from exact rational elimination agree
coefficient by coefficient with (4.2).  Their canonical JSON SHA-256 is

```text
2a1ac6b6b2c0fc5b6939492425fd13709592b9eea14cae3d24a24f2bd248d75d
```

## 5. Unique dominant root

The three nondominant roots of \(q_{4,256}\) lie in the scaled intervals

\[
 (-3328,-3072),\qquad(768,1024),\qquad(2048,2304).
\tag{5.1}
\]

The fourth lies in the strict interval (1.4).  Ten exact Schur transforms
place every root of \(q_{10,16}\) inside \(|x|<4800\), and eighteen exact
Schur transforms do the same for \(q_{18}\).  Since \(4096<4800<\nu\),
\(\nu\) is the unique spectral value of maximal modulus.

## 6. Reachability and exact negative projection

Let \(v_0\) put value one in every sign state with carry zero, and let
\(\ell\) select \((s,\boldsymbol\sigma,k)=(0,\boldsymbol0,0)\).  Then

\[
 Y_{8,r}=\ell W_8^rv_0.
\tag{6.1}
\]

The first values are

\[
 1,\ 11896,\ 19053696,\ 190789779104,\
 510830384639264,\ldots .
\tag{6.2}
\]

After one transient, the exact recurrence polynomial is

\[
 \boxed{
 P_{33}(x)=(x-4096)q_{4,256}(x)q_{10,16}(x)q_{18}(x).}
\tag{6.3}
\]

The certificate verifies the full vector identity

\[
 \boxed{P_{33}(W_8)W_8v_0=0}
\tag{6.4}
\]

in every one of the 1792 integer coordinates, while
\(P_{33}(W_8)v_0\ne0\).  Thus the one-step transient is exact, not a finite
fit.  The generating numerator is coprime to \(P_{33}\), so every factor in
(6.3), including the dominant quartic factor, is genuinely reachable.

Evaluating the residue formula over the rational interval (1.4) gives (1.5).
This proves both nonvanishing and sign without floating-point root finding.

## 7. What the zero-time scaling says

The unweighted correlation grows faster than the eighth-order spatial
threshold:

\[
 \frac{|Y_{8,r}|}{M_r^3}\longrightarrow\infty,
 \qquad M_r^3=4096^r<\nu^r.
\tag{7.1}
\]

At the quartic-critical amplitude
\(\varepsilon_r^2=(16/\lambda)^r\), however, the formal zero-time
eighth-order ratio has block rate

\[
 \left(\frac{16}{\lambda}\right)^{3r}
 \left(\frac{256\lambda}{4096}\right)^r
 =\left(\frac{256}{\lambda^2}\right)^r
 <\left(\frac{256}{625}\right)^r
 <\left(\frac{41}{100}\right)^r.
\tag{7.2}
\]

This is a rigorous algebraic scaling result for the zero-time branch.  It is
not yet a bound on \(S_{8,m}\), because the heat kernel couples all 35 time
orders to the six free carrier positions.

## 8. Next step: R0.68B-2

The remaining finite task is now sharply specified.

1. Insert the exact seven-simplex kernel (2.6) into all 35 sign shuffles.
2. Lift the 1792-state transfer by the finite affine moments needed for the
   dominant heat projection.
3. Prove that the finite dominant coefficient stays nonzero, or derive a
   countervailing heat spectral branch.
4. Bound the analytic remainder strictly below that finite projection.

Only after those four checks may the eighth-order term be combined with the
R0.68A infinite-tail theorem.

## 9. Claim boundary

This result is an exact fixed-order algebraic theorem for a periodic packet
inside the globally smooth invariant parallel-shear class.  It does not yet
prove the complete eighth-order heat asymptotic.  It does not handle general
three-dimensional perturbations, prove norm inflation or singularity, prove
global regularity, or solve the Navier--Stokes Millennium problem.
