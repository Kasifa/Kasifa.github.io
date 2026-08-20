# R0.67A — The exact zero-time sixth-order cycle

## 1. Result and boundary

R0.66 proved that the complete heat-weighted quartic coefficient on the
explicit periodic packet has a nonzero dominant spectral projection.  The
next Picard term that can return to the target plane is the sixth-order term.
This note derives its complete path formula and proves the corresponding
**zero-time** five-carrier spectral theorem.

Let

\[
 M_r=16^r,\qquad
 q_r=2\frac{16^r-1}{15},
\tag{1.1}
\]

and let \(a_n^s(j)\), \(s\in\{0,1\}\), be the two Rudin--Shapiro coefficient
states at length \(2^n\).  Define the unweighted sixth-order target scalar

\[
 \begin{aligned}
 Y_r={}&a_{4r}^0(q_r)
 \sum_{\substack{A+B+C-D-E=q_r\\
                  0\le A,B,C,D,E<M_r}}
 a_{4r}^0(A)a_{4r}^0(B)a_{4r}^0(C)
 a_{4r}^0(D)a_{4r}^0(E).
 \end{aligned}
\tag{1.2}
\]

There is a real constant \(C_{6,0}\) such that

\[
 \boxed{Y_r=C_{6,0}\mu^r+O(300^r),}
\tag{1.3}
\]

where

\[
 \mu=16\lambda,\qquad
 402.425429345624<\mu<402.4254293456256,
\tag{1.4}
\]

and \(\lambda\) is the dominant R0.66 root.  The exact outward interval in the
R0.67A audit gives

\[
 -0.013063396815425
 <C_{6,0}<
 -0.013063396815144.
\tag{1.5}
\]

In particular,

\[
 \boxed{\frac{|Y_r|}{M_r^2}\longrightarrow\infty,}
\tag{1.6}
\]

because \(M_r^2=256^r\) and \(\mu>400>256\).

Equations (1.3)--(1.6) concern the unweighted five-carrier correlation.  They
do **not** yet prove that the complete five-simplex heat observable has a
nonzero \(\mu\)-projection.  That heat-weighted projection is the remaining
R0.67 task.

## 2. The complete sixth-order heat path formula

Use the R0.61 notation

\[
 N=LM,\qquad H=4N,\qquad
 I_N=\{H,\ldots,H+N-1\}.
\tag{2.1}
\]

For a positive target sector \(m\), an order-six path starts at \(-Q\), with
\(Q\in J_m\), and adds five shear carriers.  The final first frequency is
zero exactly when

\[
 p_1+p_2+p_3+p_4+p_5=Q.
\tag{2.2}
\]

The shell geometry forces exactly three positive and two negative carriers.
Four or five positive carriers are already too large, while at most two
positive carriers cannot give a positive target.  Thus every path has the
unique sign form

\[
 \boxed{A+B+C-D-E=Q,\qquad A,B,C,D,E\in I_N.}
\tag{2.3}
\]

Let \(\operatorname{Sh}(3,2)\) be the ten words containing three plus signs
and two minus signs.  For a word \(\omega\), insert \(A,B,C\) into its
positive positions in their order of occurrence and insert \(-D,-E\) into
its negative positions in their order of occurrence.  This convention counts
every ordered path exactly once, including repeated carrier magnitudes.

For one ordered path put

\[
 k_0=-Q,\qquad
 k_j=-Q+\sum_{\ell=1}^j p_\ell,\quad 1\le j\le5,
 \qquad k_5=0.
\tag{2.4}
\]

Its six dimensionless heat rates are

\[
 \alpha_j
 =\frac{k_j^2+\sum_{\ell=j+1}^5p_\ell^2}{H^2},
 \quad 0\le j\le4,
 \qquad
 \alpha_5=0.
\tag{2.5}
\]

Define the positive five-simplex kernel

\[
 K_T^{(5)}(\alpha_0,\ldots,\alpha_5)
 =
 \int_{\substack{\tau_j\ge0\\
                  \tau_0+\cdots+\tau_5=T}}
 e^{-\sum_{j=0}^5\alpha_j\tau_j}
 \,d\tau_0\cdots d\tau_4
 =
 -[\alpha_0,\ldots,\alpha_5]e^{-Tx}.
\tag{2.6}
\]

The confluent divided difference in (2.6) includes all repeated-rate cases.
The complete dimensionless sixth-order sum is

\[
 \boxed{
 \begin{aligned}
 S_{6,m}={}&
 \sum_{Q\in J_m}
 \sum_{\substack{A,B,C,D\in I_N\\
 E=A+B+C-D-Q\in I_N}}
 c_Qc_Ac_Bc_Cc_Dc_E\\
 &\times
 \sum_{\omega\in\operatorname{Sh}(3,2)}
 K_T^{(5)}(\alpha_0,\ldots,\alpha_5).
 \end{aligned}}
\tag{2.7}
\]

Five Duhamel integrations and \((-im)^5=-im^5\) give

\[
 \boxed{
 \widehat G_6(0,m,t_H)
 =
 -im^5e^{-m^2t_H}H^{-10}S_{6,m}.}
\tag{2.8}
\]

Combining (2.8) with the quadratic reference from R0.61 and
\(A=\varepsilon\sqrt H\) yields

\[
 \boxed{
 \frac{A^6\widehat G_6(0,m,t_H)}
      {A^2\widehat G_2(0,m,t_H)}
 =
 \frac{\varepsilon^4}{L^4}R_{6,L,M,m},\qquad
 R_{6,L,M,m}
 =
 \frac{L^4m^4}{H^6}\frac{S_{6,m}}{S_{2,m}}.}
\tag{2.9}
\]

The plus sign in (2.9) is the alternating Picard phase after the negative
quartic ratio.

## 3. The 320-state exact transfer

At one binary level, the five carrier signs require

\[
 \boldsymbol\sigma\in\{0,1\}^5.
\tag{3.1}
\]

The partial relation in (2.3) has carry

\[
 k\in\{-2,-1,0,1,2\}.
\tag{3.2}
\]

Together with the target sign state \(s\in\{0,1\}\), the smallest direct
closure has

\[
 \boxed{2\times32\times5=320\ \text{states}.}
\tag{3.3}
\]

If the next target bit is \(b\) and the five carrier bits are
\(\boldsymbol\varepsilon\), the child carry is

\[
 k'
 =
 2k+b-(\varepsilon_1+\varepsilon_2+\varepsilon_3
        -\varepsilon_4-\varepsilon_5),
\tag{3.4}
\]

and the signed transition coefficient is

\[
 (-1)^{sb+\boldsymbol\sigma\cdot\boldsymbol\varepsilon}.
\tag{3.5}
\]

The audit compares this transfer with direct five-fold convolution in all
320 states through six binary levels.  Every integer agrees.  Both digit
matrices have rank \(80\) modulo each of two independent primes.

## 4. Exact four-bit spectrum

Let \(W_6\) be the product for the least-significant-bit-first word
\(0100\).  Exact modular ranks give

\[
 \operatorname{rank}W_6=36,\qquad
 \operatorname{rank}W_6^2
 =\operatorname{rank}W_6^3=31.
\tag{4.1}
\]

The restriction to \(\operatorname{im}W_6\) is an exact integer
\(36\times36\) matrix.  Its characteristic polynomial factors as

\[
 \boxed{
 \begin{aligned}
 \chi_{\rm im}(x)
 ={}&x^5(x-256)^5q_4(x)^4q_{10}(x),\\
 q_4(x)
 ={}&x^4-400x^3-30720x^2
      +13303808x-536870912,\\
 q_{10}(x)
 ={}&x^{10}-425x^9+27640x^8+2986608x^7
      +1690933248x^6\\
 &-861945266176x^5+79733131837440x^4
      +19372471463444480x^3\\
 &-3646484134030737408x^2
      +212882902585989660672x\\
 &-495756246980944199680.
 \end{aligned}}
\tag{4.2}
\]

The full characteristic polynomial has an additional factor \(x^{284}\).
The primary nullities over two primes are

\[
 5,\quad5,\quad16,\quad10
\tag{4.3}
\]

for \(x\), \(x-256\), \(q_4\), and \(q_{10}\), respectively.  Thus every
nonzero primary factor in (4.2) is semisimple on the image.

The key identity is exact:

\[
 \boxed{q_4(x)=16^4p(x/16),}
\tag{4.4}
\]

where \(p\) is the R0.66 quartic.  Hence its largest root is
\(\mu=16\lambda\).  The four roots of \(q_4\) lie separately in

\[
 (-208,-192),\quad(48,64),\quad(128,144),\quad(400,416).
\tag{4.5}
\]

Ten exact Schur transforms prove that every root of \(q_{10}\) has modulus
strictly below \(300\).  Therefore \(\mu\) is the unique spectral value of
maximal modulus.

## 5. Reachability and the nonzero coefficient

Let \(v_0\) put value one in every sign state with carry zero, and let
\(\ell\) select the state \((s,\boldsymbol\sigma,k)=(0,\boldsymbol0,0)\).
Then

\[
 Y_r=\ell W_6^rv_0.
\tag{5.1}
\]

The first values are

\[
 \begin{aligned}
 1,\ 500,\ 75418,\ 32255026,\ 6260885266,\ldots .
 \end{aligned}
\tag{5.2}
\]

After one transient, the exact recurrence polynomial is

\[
 (x-256)q_4(x)q_{10}(x).
\tag{5.3}
\]

Equivalently, the generating function has denominator

\[
 D(z)
 =(1-256z)\,z^4q_4(1/z)\,z^{10}q_{10}(1/z).
\tag{5.4}
\]

The audit constructs its exact degree-\(15\) numerator \(N(z)\) and obtains

\[
 \boxed{\gcd_{\mathbb Q[z]}(N,D)=1.}
\tag{5.5}
\]

In particular, the pole \(z=\mu^{-1}\) is not cancelled.  Its coefficient is

\[
 C_{6,0}
 =
 -\mu\,\frac{N(\mu^{-1})}{D'(\mu^{-1})}.
\tag{5.6}
\]

Exact rational interval Horner evaluation on (1.4) gives (1.5).  Combining
this with the strict \(300\)-disk bound for all remaining factors proves
(1.3).

## 6. The C2 spectral-gap ingredient

Taking absolute values before the Rudin--Shapiro signs leaves a five-by-five
carry matrix.  It has the exact positive right eigenvector

\[
 w=(16,83441,631131,471851,28561)
\tag{6.1}
\]

with

\[
 \boxed{A_{\rm abs}w=65536w.}
\tag{6.2}
\]

The sixth-order relation has four free normalized carrier coordinates.
Every four-bit affine branch contracts each coordinate by \(1/16\).  On
signed vector measures that annihilate constants and affine functions, the
second-order Taylor remainder therefore gives the exact formal threshold

\[
 \boxed{
 \|\mathcal P_6\zeta\|_{(C^{1,1})^*,w}
 \le
 \frac{65536}{16^2}
 \|\zeta\|_{(C^{1,1})^*,w}
 =
 256\|\zeta\|_{(C^{1,1})^*,w}.}
\tag{6.3}
\]

Since \(256<\mu\), the zero-time sixth-order operator has the spectral gap
needed for a heat-observable proof, provided the mass and four first moments
are lifted exactly and the complete five-simplex observable is bounded in
\(C^{1,1}\).

Equation (6.3) is an ingredient, not yet the complete heat theorem.  The
remaining work is to construct that finite moment lift, bound its resolvent,
and certify that the complete heat functional has a nonzero pairing with the
\(\mu\)-eigendistribution.

## 7. Meaning and next step

The critical zero-time scale for the sixth coefficient is \(M_r^2=256^r\).
Equations (1.4) and (4.4) give the exact identity

\[
 \frac{\mu}{256}
 =
 \frac{\lambda}{16}.
\tag{7.1}
\]

Thus the normalized quartic and zero-time sixth correlations have the same
supercritical block ratio.  If the amplitude is scaled so that the quartic
term is order one, namely

\[
 \varepsilon_r^2\asymp(16/\lambda)^r,
\tag{7.2}
\]

then the isolated zero-time sixth contribution carries one additional factor
\((16/\lambda)^r\) and tends to zero.  This is encouraging for a
fixed-order remainder hierarchy, but it is not yet a statement about the
heat-weighted coefficient or the sum over all even orders.

The next R0.67 step is now fixed:

1. lift mass and all four first moments into an exact finite block;
2. prove the \(C^{1,1}\)-dual resolvent bound with remainder factor \(256\);
3. evaluate the complete five-simplex heat functional on the dominant
   eigendistribution with strict outward intervals;
4. compare the resulting sixth coefficient with the quartic-critical
   amplitude scale.

No result here proves norm inflation, singularity, or global regularity for
general three-dimensional data.  The packet remains in the globally smooth
invariant shear class.
