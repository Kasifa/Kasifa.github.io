# R0.74G — independent audit of full-time packet occupation

## Verdict

**PASS.**  The normalized bridge, one-sided path geometry, periodic
Peetre convolution, all-copy weights, and \(p=2,3\) powers in R0.74G
Section 4 are internally correct.

The line-by-line source was the candidate commit

    e92fbf8ab3b94c07c7a77513cb21d8e46f5bf49e

with candidate full-note SHA-256

    757cd638b178105f8eaf03f99ebbc44366f5ba27c5099452a31d9787733d3d96.

The audit requested four presentation repairs and then rechecked their
implementation.  The final read-only source SHA-256 is

    7282ccbe693c7277e111117d5105032d8fed6e55756ad26f2b6b2cd597ddd756.

No theorem, exponent, or scale changed during that repair loop.

---

## 1. Bridge normalization

The R0.74F representation is

\[
 G(t,z,y)=R^3\mathbb E_y\left[
 \partial K_T(z+\mathfrak S_t^y)K_{R^2}(Y_t^y)
 \right],
 \qquad T=R^2+t.
\]

The semigroup identity

\[
 \mathbb E_yK_{R^2}(Y_t^y)=K_T(y)>0
\]

makes

\[
 d\mathbb P_{t,y}^{\rm br}
 =\frac{K_{R^2}(Y_t^y)}{K_T(y)}d\mathbb P_y
\]

a probability measure.  Hence Jensen gives

\[
 |G|^p\le
 R^{3p}K_T(y)^p
 \mathbb E_{t,y}^{\rm br}
 |\partial K_T(z+\mathfrak S)|^p,
 \qquad p=2,3.
\]

No unnormalized bridge mass or missing power of \(K_T\) remains.

---

## 2. Calibration and pathwise displacement

For all sufficiently large indices,

\[
 48R^2\le\int_{R^2}^{65R^2}\theta(t,h)dt\le64R^2,
\]

and

\[
 \frac12\le q+\frac12\le\frac34.
\]

Thus

\[
 \frac1{128R^2}\le B\le\frac1{64R^2}.
\]

The plateau estimate is used uniformly for every
\(0\le\tau\le65R^2\):

\[
 0\le1-\theta(\tau,h)\le4e^{-aL^2},
 \qquad a=\frac{49}{14625}.
\]

Because \(\theta\le1\), every bridge path satisfies

\[
 \mathfrak S\ge-\delta,
 \qquad
 \delta\le\frac{65}{16}e^{-aL^2}.
\]

Moreover,

\[
 \frac\delta R
 \le\frac{65}{16}e^{-(a-c_R)L^2}\to0,
 \qquad a-c_R=\frac{211}{936000}>0.
\]

The opposite pathwise bound is

\[
 \mathfrak S\le2Bt\le\frac{65}{32}.
\]

These signs are decisive: a path that sees the transition can move the
negative-\(Q\) positive packet farther from the origin, but not through the
origin by more than \(o(R)\).

---

## 3. Path centre and torus seam

The physical point decomposes exactly as

\[
 (Q+z,h+y)
 =(Q-\mathfrak S,h)+(z+\mathfrak S,y).
\]

Therefore the path centre

\[
 c_{\mathfrak S}=(Q-\mathfrak S,h)
\]

has the correct sign.

If \(Q\ge-2h\), then \(Q\le q<h/2\) implies

\[
 d_{\mathbb T^2}(c_{\mathfrak S},0)
 \ge h\ge\frac{s}{\sqrt5}.
\]

If \(Q<-2h\), then \(\delta<h\) gives

\[
 Q-\mathfrak S<0,
 \qquad
 |Q-\mathfrak S|ge|Q|/2\ge\frac{s}{\sqrt5}.
\]

The centre remains in one torus chart:

\[
 -\frac{81}{32}le Q-\mathfrak S\le q+\delta,
\]

\[
 \frac{81}{32}<3<\pi,
 \qquad
 q+\delta<\frac32h\le\frac{25}{512}<\pi.
\]

Consequently,

\[
 R^2+d_{\mathbb T^2}(c_{\mathfrak S},0)^2
 \ge\frac15(R^2+h^2+Q^2).
\]

No modulo seam can return a far path centre to the origin.

---

## 4. Peetre and periodic heat-kernel moments

For

\[
 \Phi_R(x)=(R^2+d_{\mathbb T^2}(x,0)^2)^{-3/2},
\]

the periodic Peetre inequality is

\[
 \Phi_R(c+\xi)
 \le C\Phi_R(c)
 \left(1+\frac{d_{\mathbb T^2}(\xi,0)}R\right)^3.
\]

The product reduction used after \(u=z+\mathfrak S\) is

\[
 \left(1+\frac{d_{\mathbb T^2}((u,y),0)}R\right)^3
 \le C
 \left(1+\frac{d_{\mathbb T}(u,0)}R\right)^3
 \left(1+\frac{d_{\mathbb T}(y,0)}R\right)^3.
\]

The final source correctly retains the absolute constant \(C\).

Uniformly for \(T/R^2\in[62,66]\),

\[
 \int K_T^p(1+d/R)^3\le CR^{1-p},
\]

\[
 \int|\partial K_T|^p(1+d/R)^3\le CR^{1-2p}.
\]

The central Gaussian copies give these scales directly.  A noncentral
copy \(n\ne0\) retains

\[
 e^{-c(2|n|-1)^2/R^2},
\]

whose sum is absorbed by the same bounds.  Thus all heat-kernel windings
are included.

---

## 5. Exact occupation powers

The common bridge power is

\[
 R^{3p}R^{1-p}R^{1-2p}=R^2.
\]

The effective lifted weights have prefactors

\[
 a_3=R^4,
 \qquad a_2=R.
\]

Therefore

\[
 I_3^+(t)le
 C\frac{R^6}{(R^2+h^2+Q(t)^2)^{3/2}},
\]

\[
 I_2^+(t)le
 C\frac{R^3}{(R^2+h^2+Q(t)^2)^{3/2}}.
\]

The inversion relation

\[
 F^-(t,x)=-F^+(t,-x)
\]

and radial weights give identical estimates for the negative packet.
Standard \(p=2,3\) sum inequalities control the paired field without a
hidden cross row.

---

## 6. Audit boundary

This audit verifies the all-copy occupation theorem in the cited source.
It does not independently audit the buffered local energy, gauge pressure,
time-integrated complete denominator, inherited survival lower bound, or
any regularity statement.  **NOT CLAY.**

