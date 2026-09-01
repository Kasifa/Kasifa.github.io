# R0.74F — same-source independent audit of the final survival proof

## Verdict

**ANALYTIC PROOF: PASS.**  For the source revision locked below, the explicit
odd paired-stream field is a smooth periodic mean-zero 2D3C Navier--Stokes
solution, its matching mollified trajectory is identically zero, and the
two-packet argument proves Theorem 6.2 with the stated scale and annular
weight.  The source note's `PROVISIONAL / AUDIT PENDING` qualification may be
removed for this theorem once this audit is accepted.

**FINITE CERTIFICATE: PASS, 30/30.**  The exact-arithmetic certificate was
reproduced byte for byte.  It certifies only its rational identities,
strict margins, discrete threshold, and conditional geometry algebra.  The
analytic result above is established by the written PDE, heat-kernel, and
periodic Brownian-bridge proof, not by that certificate.

**REMAINING PROGRAM: OPEN.**  No complete payment upper bound, amplitude
closure, endpoint-ratio divergence, arbitrary-solution estimate, regularity
theorem, or singular solution is obtained.  **NOT CLAY.**

---

## 1. Immutable audit target

This audit was performed from the complete current contents of
`research/r074f_two_packet_survival.md`, not from the earlier R0.74E outline
or an earlier independent-audit draft.

- analytic audit time: `2026-09-01 21:39:42 +0800`;
- final rebind time: `2026-09-01 21:50:31 +0800`;
- repository `HEAD` at audit time:
  `b2520b8d6333415aaa708af46604b09f51344212`;
- final audited file SHA-256:
  `0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb`;
- pre-rebind proof SHA-256:
  `2a6023a623f5a2a04617df9c9a13fdb2da8467425e4b5498487b17f4b53a7299`;
- audited theorem: Theorem 6.2, including all dependencies in Sections 1--6.

The pre-rebind source was recovered byte for byte from the original audit
record, and its recovered SHA-256 exactly matched the value above.  A direct
byte diff against the final source produced exactly three administrative
hunks: the top status paragraph was promoted from audit-pending to proved,
the Section 7 subheading was promoted to **Proved in this version**, and the
new Section 8 verification index was appended after the former final line.
Sections 1--6, including every formula, lemma, proposition, and Theorem 6.2
proof line, were byte-identical.  The analytic verdict is therefore formally
rebound to the final SHA-256.  Any later source change invalidates this
binding until it is compared again.

**FINAL REBIND: VERIFIED.**  The identical Sections 1--6 source slice has
SHA-256 `43075ecd48169a2148f587d43f0c7ac17fff122c38f4f5986ab9b78046b0e981`
in both the pre-rebind and final files.

For the calculations below, abbreviate

\[
 R=R_j,\quad L=L_j,\quad r=LR,\quad h=c_hLR,\quad q=\beta LR,
 \quad t_0=65R^2,
\tag{A.1}
\]

where

\[
 \lambda=\frac{63}{32},\qquad c_h=\frac{15}{16},\qquad
 \beta^2=\frac{31}{256},\qquad c_R=\frac1{320},\qquad
 R=e^{-c_RL^2},\qquad L=\lambda2^j.
\tag{A.2}
\]

In particular,

\[
 c_h^2+\beta^2=1,\qquad |(q,h)|=r,\qquad
 2^jR=\frac r\lambda,\qquad 2^{j+1}R=\frac{2r}\lambda.
\tag{A.3}
\]

---

## 2. The explicit field really is a smooth mean-zero 2D3C NSE solution

The shear seed

\[
 g_j(x_3)=\sigma\!\left(\frac{\sin x_3}{16R}\right)
\]

is smooth, periodic, and odd.  Heat evolution preserves all three
properties, so

\[
 b(t,x_3)=B\theta(t,x_3),\qquad
 \theta=e^{t\partial_3^2}g_j
\tag{A.4}
\]

is smooth, periodic, odd in \(x_3\), and has zero spatial mean.  The two
initial passive packets are smooth periodic derivatives in \(x_2\).  Their
total integrals vanish, and the advection-diffusion equation

\[
 F_t+b\partial_2F=\Delta_{23}F
\tag{A.5}
\]

preserves that zero mean.  Standard linear parabolic regularity gives a
smooth periodic \(F\) for all times used in the note.

For

\[
 u=(\mathfrak a F,b,0),\qquad p=0,
\tag{A.6}
\]

the field is independent of \(x_1\), while \(b\) is independent of
\(x_2\).  Therefore

\[
 \nabla\cdot u=\partial_1(\mathfrak a F)+\partial_2b=0.
\tag{A.7}
\]

Also

\[
 u\cdot\nabla=b\partial_2,
\]

and the three components of the unforced NSE residual are

\[
\begin{aligned}
 (\partial_t-\Delta)u_1+u\cdot\nabla u_1
 &=\mathfrak a(F_t-\Delta_{23}F+b\partial_2F)=0,\\
 (\partial_t-\Delta)u_2+u\cdot\nabla u_2
 &=B(\theta_t-\partial_3^2\theta)=0,\\
 (\partial_t-\Delta)u_3+u\cdot\nabla u_3&=0.
\end{aligned}
\tag{A.8}
\]

No pressure correction is missing: \(p=0\) makes the residual exactly zero.
Both nonzero components have zero torus mean.  Thus (A.6) is, for every
\(\mathfrak a>0\), an exact smooth periodic mean-zero 2D3C NSE field.

**Result: PASS.**

---

## 3. Odd symmetry forces the entire local-frame motion to vanish

Evenness of the periodic heat kernel and oddness of its derivative give at
time zero

\[
 F^+(0,-x_2,-x_3)=-F^-(0,x_2,x_3),\qquad
 F^-(0,-x_2,-x_3)=-F^+(0,x_2,x_3).
\tag{A.9}
\]

Hence the paired datum is odd under full inversion.  If
\(\widehat F(t,x_2,x_3)=-F(t,-x_2,-x_3)\), then oddness of \(b\) shows
that \(\widehat F\) solves the same equation and has the same initial
datum as \(F\).  Uniqueness yields

\[
 F(t,-x_2,-x_3)=-F(t,x_2,x_3).
\tag{A.10}
\]

Together with oddness of \(b\), this makes the full velocity odd on the
three-torus:

\[
 u(t,-x)=-u(t,x).
\tag{A.11}
\]

For the even radial matching mollifier,

\[
 u_R(t,0)=\int_{\mathbb T^3}\varphi_R^{\rm per}(-y)u(t,y)\,dy=0.
\tag{A.12}
\]

The smooth mollified vector field is spatially Lipschitz.  The terminal-value
ODE anchored at the origin therefore has a unique solution, and the constant
solution is it:

\[
 X_R(t)\equiv0,\qquad a_R(t)=\dot X_R(t)=0,\qquad a_R'(t)=0.
\tag{A.13}
\]

Consequently the moved and locally subtracted velocities are both exactly
\(u\), all acceleration-payment rows vanish, and Versions M and F have the
same endpoint quantity.

**Result: PASS.**

---

## 4. Positive-packet formula: sign and time ordering

Let

\[
 G^+(t,z,y)=F^+(t,Q(t)+z,h+y),\qquad
 Q'(t)=B\theta(t,h).
\tag{A.14}
\]

Direct differentiation, with no stochastic argument yet, gives

\[
 G_t^+=\Delta_{z,y}G^++d(t,y)\partial_zG^+,\qquad
 d(t,y)=B[\theta(t,h)-\theta(t,h+y)].
\tag{A.15}
\]

The plus sign in front of \(d\partial_z\) is correct: it is
\(Q'(t)-b(t,h+y)\).  For a solution at terminal time \(t\), the backward
stochastic clock must therefore use the generator

\[
 \Delta_{z,y}+d(t-s,y)\partial_z,
\tag{A.16}
\]

not \(d(s,y)\partial_z\).  With

\[
 Y_s^y=y+\sqrt2W_3(s),\qquad
 \mathfrak S_t^y=\int_0^td(t-s,Y_s^y)\,ds,
\tag{A.17}
\]

Itô's formula for \(G^+(t-s,Z_s,Y_s^y)\) cancels its drift exactly.
Convolution over the independent longitudinal Brownian motion then gives

\[
 G^+(t,z,y)=R^3\mathbb E_y\!\left[
  \partial_zK_{R^2+t}^{\rm per}(z+\mathfrak S_t^y)
  K_{R^2}^{\rm per}(Y_t^y)
 \right].
\tag{A.18}
\]

At \(t=0\), the reference point is \(Q(0)=q_{\rm pre}\), so the initial
profile in these coordinates is precisely
\(R^3\partial K_{R^2}(z)K_{R^2}(y)\).  Thus (A.18) has the right initial
centre, derivative sign, stochastic time order, and accumulated-shift sign.

**Result: PASS.**

---

## 5. Periodic bridge estimate with every winding retained

The decisive weighted expectation has the exact identity

\[
\begin{aligned}
 \mathbb E_y[\Phi(Y_s^y)K_{R^2}^{\rm per}(Y_t^y)]
 =\sum_{n\in\mathbb Z}k_T(2\pi n-y)
 \int_{\mathbb R}k_v(\xi-\mu_{n,s})
 \Phi(\xi\bmod2\pi)\,d\xi,
\end{aligned}
\tag{A.19}
\]

where

\[
 T=t+R^2,\qquad v=\frac{s(T-s)}T,\qquad
 \mu_{n,s}=\frac{T-s}{T}y+\frac{s}{T}2\pi n.
\tag{A.20}
\]

This follows by expanding both periodic kernels, tiling the real line, and
using

\[
 k_s(\xi-y)k_{T-s}(2\pi n-\xi)
 =k_T(2\pi n-y)k_v(\xi-\mu_{n,s}).
\tag{A.21}
\]

All summands are nonnegative, so Tonelli applies.  No winding has been
silently removed.

For the central winding, \(|\mu_{0,s}|\le R\).  With \(r_t=t-s\), the
heat age in \(1-\theta(r_t,\cdot)\) and the bridge variance combine as

\[
 r_t+v=t-\frac{s^2}{t+R^2}\le t\le65R^2.
\tag{A.22}
\]

The transition width obeys

\[
 \arcsin(16R)\le32R.
\tag{A.23}
\]

At \(L\ge9216\), the central mean is consequently separated from the
nearest defect of the saturated plateau by at least

\[
 (c_hL-33)R\ge\frac{255}{256}c_hLR.
\tag{A.24}
\]

The exact comparison

\[
 \frac{(255/256)^2}{260}-\frac1{264}
 =\frac{3181}{112459776}>0
\tag{A.25}
\]

then yields the leakage exponent \(c_h^2L^2/264\).  The unshifted
reference point has the separate exponent \(\alpha^2L^2/260\).

For \(n\ne0\), \(|2\pi n-y|\ge|n|\), while
\(T\le66R^2\).  Thus the complete noncentral sum is bounded by

\[
 \sum_{n\ne0}k_T(2\pi n-y)
 \le\frac2R e^{-1/(264R^2)}
 \le\frac2R e^{-c_h^2L^2/264}.
\tag{A.26}
\]

The last step follows from \(R^{-1}\ge L\) for the frozen scales.  Combining
the central and noncentral terms reproduces the weighted bound

\[
\begin{aligned}
 &\mathbb E_y\!\left[
 |\theta(t-s,h)-\theta(t-s,h+Y_s^y)|K_{R^2}(Y_t^y)
 \right]\\
 &\qquad\le\frac6R\left(
 e^{-\alpha^2L^2/260}+e^{-c_h^2L^2/264}
 \right).
\end{aligned}
\tag{A.27}
\]

The calibration interval has length \(64R^2\).  Since
\(\theta(t,h)\ge1/2\) there for large \(j\), while \(q<1/2\),

\[
 0<B\le\frac1{32R^2}.
\tag{A.28}
\]

Integrating (A.27) in stochastic time gives

\[
 \mathbb E_y[|\mathfrak S_t^y|K_{R^2}(Y_t^y)]
 \le\frac{13}{R}\left(
 e^{-\alpha^2L^2/260}+e^{-c_h^2L^2/264}
 \right).
\tag{A.29}
\]

Both terms tend to zero because

\[
 \frac{\alpha^2}{260}-c_R=\frac{211}{936000}>0,
 \qquad
 \frac{c_h^2}{264}-c_R=\frac{23}{112640}>0.
\tag{A.30}
\]

The Dirac interpretation at \(s=0\), positive remaining variance at
\(s=t\), central winding, and all noncentral windings are all covered.

**Result: PASS.**

---

## 6. Positive packet: order-one scale and fixed sign

The periodic derivative kernel satisfies

\[
 \|\partial_z^2K_{R^2+t}^{\rm per}\|_\infty\le CR^{-3}.
\tag{A.31}
\]

Subtracting the zero-shift term in (A.18) and applying (A.29) therefore
produces the uniform comparison

\[
\begin{aligned}
 &\left|G^+(t,z,y)
 -R^3\partial_zK_{R^2+t}^{\rm per}(z)
       K_{R^2+t}^{\rm per}(y)\right|\\
 &\qquad\le CR^{-1}\left(
 e^{-\alpha^2L^2/260}+e^{-c_h^2L^2/264}
 \right)=o(1).
\end{aligned}
\tag{A.32}
\]

The factor count is exact: the datum contributes \(R^3\), the second
derivative costs \(R^{-3}\), and the weighted shift contributes the
right side of (A.29).

On the terminal slice used later,

\[
 \tau=\frac{R^2+t}{R^2}\in[66-R,66],\qquad
 \frac zR\in\left[\frac54,\frac32\right],\qquad
 \left|\frac yR\right|\le1.
\tag{A.33}
\]

The central real-line part of the free term is

\[
 -\frac{z/R}{2\tau}\frac1{4\pi\tau}
 \exp\!\left[-\frac{(z/R)^2+(y/R)^2}{4\tau}\right].
\tag{A.34}
\]

It is negative throughout the displayed box and has an absolute lower
bound independent of \(j\).  For example, once \(\tau\ge65\), its absolute
value is at least

\[
 \frac5{528}\frac1{264\pi}e^{-13/1040}>0.
\tag{A.35}
\]

Noncentral periodic copies are \(O(e^{-c/R^2})\), and (A.32) is \(o(1)\).
Thus the positive packet has a fixed negative sign and an order-one lower
bound on the entire box.  This verifies the source choices

\[
 b_1=\frac54,\qquad b_2=\frac32.
\tag{A.36}
\]

**Result: PASS.**

---

## 7. The inverted packet cannot cancel the positive lobe

In original coordinates, the backward generator is

\[
 \Delta_{2,3}-b(t-s,x_3)\partial_2.
\]

Consequently

\[
\begin{aligned}
 F^-(t,x_2,x_3)=R^3\mathbb E_{x_3}\!\left[
  \partial_2K_{R^2+t}
  \left(x_2+q_{\rm pre}-\int_0^tb(t-s,X_s^{x_3})\,ds\right)
  K_{R^2}(X_t^{x_3}+h)
 \right].
\end{aligned}
\tag{A.37}
\]

The minus sign before the integrated shear is the correct sign for this
backward generator.  Its value is irrelevant after taking the uniform
derivative-kernel bound.  At \(x_3=h+y\), \(|y|\le R\), the transverse
semigroup gives exactly

\[
 \mathbb E_{h+y}K_{R^2}(X_t^{h+y}+h)
 =K_{R^2+t}(2h+y).
\tag{A.38}
\]

The principal transverse distance is at least
\((2c_hL-1)R\), while \(4(R^2+t)\le264R^2\).  Since
\(R^3\cdot R^{-2}\cdot R^{-1}=1\),

\[
 |F^-(t,x_2,h+y)|
 \le C e^{-(2c_hL-1)^2/264}+Ce^{-c/R^2}=o(1),
\tag{A.39}
\]

uniformly in \(x_2\).  This argument retains the principal transverse copy
and bounds every other periodic copy in the second term.  It does not assume
a favorable longitudinal path or sign.

Combining (A.39) with the positive-packet lower bound shows that the full
\(F=F^++F^-\) remains negative with fixed nonzero magnitude on the positive
lobe.  Full inversion oddness produces a positive reflected lobe of the same
magnitude.

**Result: PASS.**

---

## 8. Terminal time slice and reference-centre error

Define

\[
 J_j=(t_0-R^3,t_0).
\tag{A.40}
\]

Because \(0<R<1\), this interval has positive measure \(R^3\) and lies in

\[
 I_R=(t_0-R^2,t_0)=(64R^2,65R^2).
\tag{A.41}
\]

Using \(Q(t_0)=q\), \(|\theta|\le1\), and (A.28),

\[
 |Q(t)-q|
 =\left|B\int_t^{t_0}\theta(s,h)\,ds\right|
 \le\frac{t_0-t}{32R^2}
 <\frac R{32}
 \qquad(t\in J_j).
\tag{A.42}
\]

Thus the \(B\asymp R^{-2}\) shear produces an order-one displacement on
the full \(R^2\) time scale but only an order-\(R\) displacement on this
terminal \(R^3\) slice.  There is no lost power of \(R\).

**Result: PASS.**

---

## 9. Three-dimensional lobes and exact dyadic-annulus margins

For \(t\in J_j\), the positive lobe is

\[
\begin{aligned}
 \Omega_{j,+}(t)=\{x:\;&|x_1|<r/16,\quad
 (5/4)R<x_2-Q(t)<(3/2)R,\\
 &|x_3-h|<R\},
 \qquad \Omega_{j,-}(t)=-\Omega_{j,+}(t).
\end{aligned}
\tag{A.43}
\]

The sharp horizontal perturbation from \(q\) is less than

\[
 \left(\frac32+\frac1{32}\right)R=\frac{49}{32}R.
\tag{A.44}
\]

The source deliberately uses the looser valid bound \(65R/32\).  Together
with \(|x_3-h|<R\), this gives the conservative planar \(\ell^1\) error
\(97R/32\).  These are safety allowances, not claimed sharp constants.

For the inner boundary,

\[
 |x|\ge r-\frac{97}{32}R>\frac r\lambda=2^jR.
\tag{A.45}
\]

At \(L=9216\), the normalized margin is exactly

\[
 1-\frac1\lambda-\frac{97}{32L}
 =\frac{1015129}{2064384}>0.
\tag{A.46}
\]

For the outer boundary, with
\(\varepsilon_2=x_2-q\) and \(\varepsilon_3=x_3-h\), the conservative
component bounds imply

\[
 \frac{|x|^2}{r^2}
 \le1+\frac1{256}+\frac{97}{16L}
 +\frac{5249}{1024L^2}.
\tag{A.47}
\]

The exact margin at \(L=9216\) is

\[
 \left(\frac2\lambda\right)^2
 -\left(1+\frac1{256}+\frac{97}{16L}
 +\frac{5249}{1024L^2}\right)
 =\frac{116914328399}{4261681299456}>0.
\tag{A.48}
\]

The error terms decrease with \(L\).  Thus both lobes lie strictly inside
\(A_j(R)\) for all admitted scales.  The central-chart assertion is also
safe: \(LR\le320/L\le5/144<1/16\), and the additional \(O(R)\)
coordinate errors vanish much faster.

The side lengths of either lobe are

\[
 \frac r8,\qquad \left(\frac32-\frac54\right)R=\frac R4,
 \qquad 2R.
\]

Therefore

\[
 |\Omega_{j,\pm}(t)|
 =\frac r8\frac R4(2R)
 =\frac1{16}rR^2
 =\frac1{16}LR^3.
\tag{A.49}
\]

This is a genuine three-dimensional volume: the \(x_1\)-extent supplies
the factor \(LR\), even though the velocity profile is independent of
\(x_1\).

**Result: PASS.**

---

## 10. Audit of Theorem 6.2

Let \(c_0>0\) be the full-packet lower bound on the positive lobe.  For
every \(t\in J_j\), one annular summand already gives

\[
\begin{aligned}
 U_\gamma(t)
 &\ge\gamma_j\int_{\Omega_{j,+}(t)}
 |\mathfrak a_jF_j(t,x_2,x_3)|^2\,dx\\
 &\ge\frac{c_0^2}{16}\,
 \gamma_j\mathfrak a_j^2L_jR_j^3.
\end{aligned}
\tag{A.50}
\]

The time set \(J_j\) has positive measure and is contained in \(I_{R_j}\).
Therefore this pointwise-in-time lower bound is detected by the essential
supremum; it is not an endpoint-only statement.  The frozen endpoint
normalization is \(R_j^{-1}\), so

\[
 \mathcal U_{\rm ext}^{\infty}
 \ge c\mathfrak a_j^2L_jR_j^2\gamma_j.
\tag{A.51}
\]

The annular-weight identity is exact:

\[
 c_\gamma L_j^2
 =\frac8{3969}\left(\frac{63}{32}\right)^24^j
 =\frac{4^j}{128}
 =\frac{4^{j-1}}{32}.
\tag{A.52}
\]

Hence

\[
 \gamma_j=e^{-4^{j-1}/32}=e^{-c_\gamma L_j^2}.
\tag{A.53}
\]

By (A.13), Versions M and F use the same velocity and have zero acceleration
row.  Their endpoint dissipation terms are identical and nonnegative.  It
follows that, for every \(\mathfrak a_j>0\) and all sufficiently large
\(j\),

\[
 \boxed{
 X_{R_j}^M=X_{R_j}^F
 \ge c\mathfrak a_j^2L_jR_j^2e^{-c_\gamma L_j^2}.}
\tag{A.54}
\]

This is precisely Theorem 6.2.  No endpoint definition has been weakened or
renormalized in its derivation.

**Theorem 6.2: PASS.**

---

## 11. Finite certificate reproduction

The separate finite certificate was reproduced with

```text
python3 scripts/r074f_two_packet_survival_certificate.py
```

and its standard output was byte-for-byte identical to
`research/r074f_two_packet_survival_certificate.json`.  Its reported result
is **PASS: 30/30**.  The three frozen artifact hashes at audit time were

- script:
  `578879ad456b80a8a919e3b9a7f84da9347ad4d51f120cc53185ac61e27b0e19`;
- JSON:
  `44bd3208d10134ae84cf8b001e9569b6c480af6ac7d85efc25759dc4e725e981`;
- human-readable report:
  `c8aa8a832cfc74722df463e660b362a27cb778280b643f4e304491a5144ead76`.

The certificate confirms finite arithmetic such as (A.25), (A.30),
(A.46), (A.48), and (A.52), together with the threshold placement

\[
 L_{12}=8064<9216<16128=L_{13}.
\]

It does **not** certify the stochastic representation, Gaussian tails,
packet sign, NSE identity, trajectory cancellation, or Theorem 6.2.  Those
are analytic conclusions independently checked in Sections 2--10 of this
audit.

---

## 12. Final claim ledger

### Analytic PROVED for the locked source

1. The field \((\mathfrak a_jF_j,b_j,0)\), with \(p_j=0\), is an exact
   smooth periodic mean-zero 2D3C NSE solution.
2. Full inversion oddness and the even matching mollifier force
   \(X_{R_j}=a_{R_j}=a_{R_j}'=0\).
3. The positive-packet time-reversed formula has the correct sign and time
   order.
4. The weighted periodic bridge estimate retains every winding.
5. The accumulated drift error is negligible at packet scale.
6. The positive packet has a fixed sign and order-one size for
   \(b_1=5/4\), \(b_2=3/2\).
7. The inverted packet is negligible there, and inversion supplies the
   reflected lobe.
8. The terminal slice has the required \(Q\)-error, positive time measure,
   annular residence, and \(LR^3\) lobe volume.
9. The essential-supremum normalization and exact \(\gamma_j\) identity
   give Theorem 6.2.

### Finite certificate only

The exact certificate establishes 30 finite rational checks and conditional
geometry compatibility.  It is corroborating arithmetic evidence, not a
substitute for any analytic row above.

### OPEN

1. the buffered \(8R_j\) local-energy upper bound for all velocity and
   gradient components;
2. the complete transition, background, packet, and mixed \(G_u\) rows;
3. the gauge-fixed pressure row and the all-copy algebraic \(H_u\) row;
4. one amplitude \(\mathfrak a_j\) closing the complete denominator and
   deciding whether this explicit family is paid or yields a diverging
   endpoint/payment ratio;
5. the corresponding statement for arbitrary Navier--Stokes solutions;
6. every global regularity or blow-up consequence.

The proved result is an outer-annulus survival lower bound for one explicit
smooth exact family.  It is a rigorous intermediate theorem, not a solution
of the three-dimensional Navier--Stokes regularity problem.  **NOT CLAY.**
