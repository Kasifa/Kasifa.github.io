# R0.73S analytic draft: a quadratic-autocorrelation upper certificate

**Status:** analytic proof passed independent reconstruction; the exact
finite certificate is at the hash-bound pre-seal stage

**Dependencies:** normalized Haar measure on \(\mathbb T^d\), Parseval,
finite Fourier support, and the R0.73R LP--caloric equivalence

## 1. Exact autocorrelation bridge

Let

\[
 f(x)=\sum_{k\in S}a(k)e^{ik\cdot x},
 \qquad a(k)\in\mathbb C^r,
\]

and use the Euclidean norm in the target.  Define

\[
 C(h)=\sum_k a(k+h)\cdot\overline{a(k)}.
 \tag{1.1}
\]

Then \(C=\widehat{|f|^2}\).  In particular,

\[
 Q:=\sum_h|C(h)|^2=\||f|^2\|_2^2=\|f\|_4^4.
 \tag{1.2}
\]

Put \(A=\sum_h|C(h)|\).  Absolute Fourier convergence and Parseval give

\[
 \||f|^2\|_\infty\le A,
 \qquad
 \||f|^2\|_2^2=Q.
 \tag{1.3}
\]

Therefore

\[
\begin{aligned}
 \|f\|_6^6
 &=\int_{\mathbb T^d}|f|^6
 =\int_{\mathbb T^d}|f|^2|f|^4\\
 &\le\||f|^2\|_\infty\||f|^2\|_2^2
 \le A Q.
\end{aligned}
 \tag{1.4}
\]

This is the exact Wiener-autocorrelation form of the upper certificate.
It is an elementary classical interpolation argument applied to \(|f|^2\),
not a new harmonic-analysis theorem.

## 2. Two certified upper bounds for the Wiener factor

Let

\[
 E=\|f\|_2,
 \qquad M=|S|,
 \qquad D_C=|\operatorname{supp}C|,
 \qquad D_\Delta=|S-S|.
\]

First, the triangle inequality in (1.1) gives

\[
\begin{aligned}
 A
 &\le\sum_h\sum_k|a(k+h)|\,|a(k)|\\
 &=\left(\sum_k|a(k)|\right)^2
 \le M\sum_k|a(k)|^2
 =ME^2.
\end{aligned}
 \tag{2.1}
\]

Second, \(C\) is supported in \(S-S\), so Cauchy--Schwarz and (1.2) give

\[
 A\le\sqrt {D_C}\left(\sum_h|C(h)|^2\right)^{1/2}
 =\sqrt{D_CQ}\le\sqrt{D_\Delta Q}.
 \tag{2.2}
\]

Combining (1.4), (2.1), and (2.2),

\[
 \boxed{
 \|f\|_6^6
 \le AQ
 \le Q\min\{ME^2,\sqrt{D_CQ}\}
 \le Q\min\{ME^2,\sqrt{D_\Delta Q}\}.}
 \tag{2.3}
\]

For \(E>0\), define

\[
 \Gamma={Q\over E^4},
 \qquad
 \Theta={\|f\|_6^6\over E^6},
 \qquad
 \alpha={A\over E^2}.
\]

Then (2.3) becomes

\[
 \boxed{
 \Theta\le\alpha\Gamma
 \le\Gamma\min\{M,\sqrt{D_C\Gamma}\}
 \le\Gamma\min\{M,\sqrt{D_\Delta\Gamma}\}.}
 \tag{2.4}
\]

The difference-set branch is equivalently

\[
 \|f\|_6\le D_C^{1/12}\|f\|_4
 \le D_\Delta^{1/12}\|f\|_4.
 \tag{2.5}
\]

Equation (2.5) is a finite-spectrum Nikolskii estimate applied to
\(|f|^2\).  Equation (2.4) records the normalization needed by the R0.73R
shell interface.

## 3. Selected-shift certificate

For a chosen set \(H\subset S-S\), define the magnitude correlation

\[
 B(h)=\sum_k|a(k+h)|\,|a(k)|.
 \tag{3.1}
\]

Then \(|C(h)|\le B(h)\),

\[
 \sum_hB(h)=\left(\sum_k|a(k)|\right)^2=:S_1^2,
 \tag{3.2}
\]

and \(B(h)\le E^2\) by Cauchy--Schwarz.  Consequently

\[
 A_H:=\sum_{h\in H}|C(h)|
       +S_1^2-\sum_{h\in H}B(h)
 \ge A,
 \tag{3.3}
\]

and

\[
 Q_H:=\sum_{h\in H}|C(h)|^2
       +E^2\left(S_1^2-\sum_{h\in H}B(h)\right)
 \ge Q.
 \tag{3.4}
\]

Thus

\[
 \boxed{\|f\|_6^6\le A_HQ_H.}
 \tag{3.5}
\]

This version evaluates only the selected phase correlations and pays a
rigorous magnitude-only tail.  Its direct sparse cost is proportional to
the number of inspected coefficient pairs.  The cost statement is an
implementation contract, not an arithmetic lower bound: on a dense padded
grid, both pair and triple convolutions may be accelerated by FFTs.

## 4. Shellwise critical heat-flow certificate

For \(f_j=P_jf\), write

\[
 E_j=\|f_j\|_2,
 \quad Q_j=\|f_j\|_4^4,
 \quad M_j=|\operatorname{supp}\widehat f_j|,
 \quad D_{C,j}=|\operatorname{supp}C_j|,
 \quad D_{\Delta,j}=|S_j-S_j|,
\]

and set

\[
 U_j:=Q_j\min\{M_jE_j^2,\sqrt{D_{\Delta,j}Q_j}\}.
 \tag{4.1}
\]

By (2.3), \(\|f_j\|_6^6\le U_j\), hence

\[
 \|f_j\|_6^4\le U_j^{2/3}.
 \tag{4.2}
\]

The upper half of the R0.73R LP--caloric equivalence now yields

\[
 \boxed{
 \|e^{t\Delta}f\|_{L_t^4L_x^6}
 \le C_+
 \left(\sum_j2^{-2j}U_j^{2/3}\right)^{1/4}.}
 \tag{4.3}
\]

The same statement holds with \(U_j\) replaced by \(A_jQ_j\) or by the
selected-shift product \(A_{H,j}Q_{H,j}\).  If the right side is below the
R0.73Q radius after multiplication by the fixed LP constant, the same
fixed-orbit global stability conclusion follows.

## 5. A bounded-quartic obstruction and an exact fixed-quartic variant

Let (m\ge2) and

\[
 D_m(z)=\sum_{q=0}^{m-1}z^q,
 \qquad d_m(x)=m^{-1/2}D_m(e^{ix}).
 \tag{5.1}
\]

The exact normalized moments are

\[
 \|d_m\|_2^2=1,
 \quad
 A_m:=\|d_m\|_4^4={2m+m^{-1}\over3},
 \quad
 B_m:=\|d_m\|_6^6={11m^2+5+4m^{-2}\over20}.
 \tag{5.2}
\]

Put

\[
 \beta_m=m^{-1/4},
 \qquad a_m=(1-m^{-1/2})^{1/2},
 \tag{5.3}
\]

and choose \(N>2(m-1)\).  Define

\[
 F_m(x)=a_m+\beta_me^{iNx}d_m(x).
 \tag{5.4}
\]

Carrier separation leaves only equal powers of the high-frequency term and
its conjugate.  Therefore

\[
 \|F_m\|_2^2=a_m^2+\beta_m^2=1,
 \tag{5.5}
\]

\[
 \Gamma_m:=\|F_m\|_4^4
 =a_m^4+4a_m^2\beta_m^2+\beta_m^4A_m,
 \tag{5.6}
\]

and

\[
 \Theta_m:=\|F_m\|_6^6
 =a_m^6+9a_m^4\beta_m^2
  +9a_m^2\beta_m^4A_m+\beta_m^6B_m.
 \tag{5.7}
\]

It follows that

\[
 \Gamma_m\longrightarrow {5\over3},
 \qquad
 \Theta_m\sim {11\over20}\sqrt m.
 \tag{5.8}
\]

The Fourier support is

\[
 \{0\}\cup\{N,N+1,\ldots,N+m-1\}.
\]

Its difference set is the disjoint union of one central interval and two
carrier intervals.  All Fourier coefficients are positive, so no
autocorrelation coefficient on this difference set vanishes.  Hence

\[
 M=m+1,
 \qquad D_C=D_\Delta=4m-1.
 \tag{5.9}
\]

Thus \(E=1\) and \(\Gamma=O(1)\), while
\(\Theta\asymp\sqrt {D_C}\).  No universal bound depending only on \(\Gamma\)
can hold, and the exponent \(D_C^{1/2}\) in (2.4) cannot be replaced by
\(D_C^\sigma\) with \(\sigma<1/2\).

The conclusion can be frozen at one exact quartic value rather than only
along \(\Gamma_m\to5/3\).  Let \(x_m\in(0,1)\) be the positive solution of

\[
 (A_m-3)x_m^2+2x_m-{2\over3}=0,
 \tag{5.10}
\]

and replace \(\beta_m^2\) by \(x_m\) and \(a_m^2\) by \(1-x_m\).  Then
\(x_m\sim m^{-1/2}\), \(\Gamma_m\equiv5/3\), and
\(\Theta_m\sim(11/20)\sqrt m\).  Hence the exponent obstruction does not
depend on an unstated continuity assumption in the \(\Gamma\) variable.

### Real divergence-free annular embedding

Take \(N=3m\), \(K=32m\), write
\(H_m=e^{iKx_1}F_m(x_1)\), and put

\[
 V_m(x_1,x_2,x_3)
 =\bigl(0,\operatorname{Re}H_m(x_1),
          \operatorname{Im}H_m(x_1)\bigr).
 \tag{5.11}
\]

Then \(V_m\) is real, mean zero, and divergence free, and

\[
 (V_m\cdot\nabla)V_m=0.
 \tag{5.12}
\]

Pointwise, \(|V_m|=|H_m|=|F_m|\).  Therefore the embedding preserves every
even scalar moment and the exact autocorrelation support:

\[
 \|V_m\|_2^2=1,
 \qquad
 \|V_m\|_4^4=\Gamma_m,
 \qquad
 \|V_m\|_6^6=\Theta_m,
 \qquad D_C=4m-1.
 \tag{5.13}
\]

Its positive frequencies are \(32m\) and \(35m,\ldots,36m-1\), together
with their conjugates.  Thus its vector Fourier support has \(2(m+1)\)
sites, \(D_\Delta=10m-1\), and

\[
 32m\le |k|<36m.
 \tag{5.14}
\]

Hence the \(D^{1/2}\) obstruction survives the real,
divergence-free, one-annulus restrictions relevant to R0.73R.

## 6. Why a small uninspected \(\ell^2\) tail is insufficient

The selected-shift contract (3.5) can improve only when its tail summary is
strong enough.  The normalized Dirichlet packet has a triangular
autocorrelation tail

\[
 q_h=x\left(1-{|h|\over m}\right),
 \qquad |h|<m.
 \tag{6.1}
\]

It obeys

\[
 \|q\|_2^2\asymp x^2m,
 \qquad
 \langle q*q,\widetilde q\rangle\asymp x^3m^2.
 \tag{6.2}
\]

Taking \(x=m^{-\alpha}\) with \(1/2<\alpha<2/3\) makes the quadratic tail
energy tend to zero while its cubic contribution diverges.  Removing any
sublinear number \(K=o(m)\) of shifts deletes at most \(O(Kmx^3)\), which is
lower order than \(m^2x^3\).  Thus selected correlations plus only an
\(\ell^2\)-tail mass cannot eliminate the \(\sqrt{D_{\rm tail}}\) factor.
An improvement must retain an \(\ell^1\) tail, a convolution-tail norm,
signed cancellation, or additional additive structure.

## 7. Fixed low-order summaries do not approximate the sixth moment

There is also an exact indistinguishability result.  Define

\[
 A(z)=1-z-z^2-z^3+z^4,
 \qquad
 B(z)=1-z-z^2-z^3-z^4.
 \tag{7.1}
\]

Direct integer convolution gives

\[
 \|A\|_2^2=\|B\|_2^2=5,
 \qquad
 \|A\|_4^4=\|B\|_4^4=37,
 \tag{7.2}
\]

but

\[
 \|A\|_6^6=311,
 \qquad
 \|B\|_6^6=323.
 \tag{7.3}
\]

For an integer \(q\ge14\), let

\[
 F_r(z)=\prod_{j=0}^{r-1}A(z^{q^j}),
 \qquad
 G_r(z)=\prod_{j=0}^{r-1}B(z^{q^j}).
 \tag{7.4}
\]

The exponent digits appearing in every constant-term calculation through
order six lie in \([-12,12]\).  Since \(q-1>12\), the highest nonzero
base-\(q\) digit cannot be cancelled by all lower digits.  The constant
terms therefore factor across scales, giving

\[
 \|F_r\|_2^2=\|G_r\|_2^2=5^r,
 \qquad
 \|F_r\|_4^4=\|G_r\|_4^4=37^r,
 \tag{7.5}
\]

and

\[
 \|F_r\|_6^6=311^r,
 \qquad
 \|G_r\|_6^6=323^r.
 \tag{7.6}
\]

Both products have the same Fourier support and coefficient magnitudes.
Thus they also have the same diagonal quadratic Fourier statistics and the
same support additive energy, while

\[
 {\|G_r\|_6\over\|F_r\|_6}
 =\left({323\over311}\right)^{r/6}\longrightarrow\infty.
 \tag{7.7}
\]

For any predeclared finite shift set \(H\), replacing \(z\) by \(z^L\)
with \(L>\max_{h\in H}|h|\) makes every selected nonzero autocorrelation
equal to zero for both families.  A large outer carrier followed by the
two-component embedding in (5.11) places the same obstruction in a real,
mean-zero, divergence-free fixed-ratio annulus without changing pointwise
moduli.

The quantifier is essential.  The complete autocorrelation of a finite
polynomial is itself finite and determines

\[
 \|f\|_6^6
 =\sum_{h+k+\ell=0}C(h)C(k)C(\ell).
 \tag{7.8}
\]

The obstruction concerns a preselected strict subset, sublinear shift
budgets, or low-order summaries.  It is an information-theoretic
non-identifiability statement, not a runtime lower bound.

## 8. Transfer to the R0.73R matched pair

For the unscaled R0.73R fields \(W_{D,m}\) and \(W_{P,m}\), with
\(m=2^r\), both have

\[
 E=1,
 \qquad M=2m^2,
 \qquad D_\Delta=3(2m-1)^2.
 \tag{8.1}
\]

Direct fourth-moment carrier separation gives

\[
 Q(W_{R,m})={3\over2m^4}\|R_m\|_4^8.
 \tag{8.2}
\]

For the Dirichlet branch,

\[
 A_D=2m^2,
 \qquad
 Q_D={(2m^2+1)^2\over6m^2}.
 \tag{8.3}
\]

Thus (2.3) recovers

\[
 U(W_{D,m})\asymp m^4,
 \qquad U(W_{D,m})^{1/6}\asymp m^{2/3},
 \tag{8.4}
\]

which is sharp in power.  For the Rudin--Shapiro branch, the exact dyadic
fourth moment gives

\[
 Q_P={(4m-(-1)^r)^2\over6m^2}=O(1).
 \tag{8.5}
\]

The difference-set estimate gives \(A_P=O(m)\), hence

\[
 U(W_{P,m})\lesssim m,
 \qquad
 U(W_{P,m})^{1/6}\lesssim m^{1/6}.
 \tag{8.6}
\]

Since both fields lie at frequency \(N=8m\), their caloric proxy is the
right side of (8.4) and (8.6) times \(N^{-1/2}\).  After the common R0.73R
amplitude \(\alpha_m=\sqrt8m^{-1/6}\), the Dirichlet proxy stays of order
one while the Rudin--Shapiro proxy is \(O(m^{-1/2})\).  The exact
Rudin--Shapiro heat trace is smaller, \(O(m^{-2/3})\), but the quartic proxy
still certifies entry and distinguishes the phase pair.

## 9. Boundary of the result

The inequalities in Sections 1--2 are classical interpolation, Parseval,
and finite-spectrum Nikolskii mathematics.  The selected-shift formula is
an elementary finite upper contract.  The work under local audit is the
critical shell assembly, the bounded-quartic annular obstruction with its
exact fixed-quartic variant, and
the transfer to the R0.73R matched fields.

Nothing here controls the proxy from \(L^2\) alone.  The sharp family has
zero Navier--Stokes nonlinearity after realification, so a large proxy does
not indicate dangerous dynamics.  The result gives a cheaper-interaction
sufficient diagnostic around the same fixed a priori global orbit; it does
not prove arbitrary-data regularity or any Clay conclusion.
