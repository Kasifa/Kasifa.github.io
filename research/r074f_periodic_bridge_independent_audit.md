# R0.74F — independent analytic audit of the periodic bridge and two-packet survival

## Audit verdict

**INDEPENDENT ANALYTIC PASS.** This audit was performed against the exact
source bytes in research/r074f_two_packet_survival.md, with final SHA-256

0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb.

### Final same-source rebind

The analytic proof was first audited at the pre-rebind SHA-256
2a6023a623f5a2a04617df9c9a13fdb2da8467425e4b5498487b17f4b53a7299.
That exact 19052-byte, 919-line source was recovered from the four original
fixed-call audit outputs and its SHA-256 was reproduced before comparison
with the final file. A direct line and byte comparison found exactly three
non-equal operations:

1. the top audit-pending status paragraph was replaced by the proved-status
   paragraph;
2. the Section 7 subheading was changed from the audit-pending heading to
   “Proved in this version”; and
3. Section 8, the verification and literature index, was appended after the
   former end of file.

The complete byte slice from “## 1. Frozen paired-stream family” up to,
but not including, “## 7. Frozen claim boundary” is identical in the two
sources. Its SHA-256 is
43075ecd48169a2148f587d43f0c7ac17fff122c38f4f5986ab9b78046b0e981
in both files. Thus every formula, lemma, proposition, theorem statement,
and proof byte in Sections 1--6 is unchanged, and the analytic verdict is
formally rebound to the final source SHA-256 above. Any later source-byte
change invalidates this binding until another comparison is performed.

The source hashes and the final rebind were checked directly. Every requested
analytic row passes: the moving-coordinate equation, time-reversed
Feynman--Kac sign and time order, the lifted \(Z_s\)-process, the exact
all-winding bridge identity, both stochastic-time endpoints, the torus seam,
the bridge variance and mean, the \(33R\) reserve, the \(255/256\)
reduction, the \(260\to264\) exponent change, the constants \(6/R\),
\(B\le(32R^2)^{-1}\), and \(13/R\), the free-packet comparison, and
the inverted-packet suppression. These rows are sufficient for Proposition
5.2 of the audited source.

This is an independent analytic audit, not a restatement of the separate
30/30 finite-arithmetic certificate. The certificate checks rational
compatibility and conditional geometry; it does not certify Itô calculus,
periodic Brownian bridges, heat-kernel tails, packet survival, or the PDE
argument below. Conversely, this audit makes no novelty, priority,
regularity, singularity, or Clay claim.

---

## 1. Frozen notation and scale consequences

Suppress the packet index and write

\[
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \kappa=16,\qquad
 R=e^{-L^2/320},\qquad h=c_hLR.
\tag{A.1}
\]

The audited range is \(L\ge9216\). Since \(L\ge320\),

\[
 e^{L^2/320}\ge\frac{L^2}{320}\ge L,
 \qquad
 R\le\frac1L\le\frac1{9216}<\frac1{32},
\tag{A.2}
\]

and

\[
 LR\le\frac{320}{L}\le\frac5{144}.
\tag{A.3}
\]

These estimates license the principal torus chart used below. In
particular, \(h+[-R,R]\subset(0,1/16)\), after using the explicit
bounds in (A.2)--(A.3), whereas the transition adjacent to the
\(\pi\)-seam remains a fixed positive distance away.

---

## 2. Moving-coordinate PDE and time-reversed diffusion

For the positive packet, the original passive equation is

\[
 \partial_tF^++B\theta(t,x_3)\partial_2F^+
 =\Delta_{23}F^+.
\tag{A.4}
\]

Let

\[
 Q'(t)=B\theta(t,h),\qquad
 G^+(t,z,y)=F^+(t,Q(t)+z,h+y).
\tag{A.5}
\]

An independent chain-rule calculation gives

\[
\begin{aligned}
 \partial_tG^+
 &=\partial_tF^++Q'(t)\partial_2F^+\\
 &=\Delta G^+
  +B[\theta(t,h)-\theta(t,h+y)]\partial_zG^+.
\end{aligned}
\tag{A.6}
\]

Thus, with

\[
 d(t,y)=B[\theta(t,h)-\theta(t,h+y)],
\tag{A.7}
\]

the equation is \(G_t^+=\Delta G^++dG_z^+\). The sign is positive
in the moving equation. It is also consistent with the original backward
drift: the latter contributes \(-B\theta(t-s,h+Y_s)\), while the
reference path contributes \(+B\theta(t-s,h)\).

Fix the PDE terminal time \(t\). With independent standard real Brownian
motions \(W_2,W_3\), define

\[
 Y_s^y=y+\sqrt2W_3(s)\pmod{2\pi},
\tag{A.8}
\]

and use the real lift

\[
 \widetilde Z_s
 =z+\int_0^s d(t-r,Y_r^y)\,dr+\sqrt2W_2(s),
 \qquad
 Z_s=\widetilde Z_s\pmod{2\pi}.
\tag{A.9}
\]

Writing the real lift explicitly removes ambiguity about accumulating a
real drift across the \(x_2\)-seam. Because every kernel and \(G^+\)
are periodic, either lift gives the same torus value. Itô's formula yields

\[
 dG^+(t-s,Z_s,Y_s^y)
 =[-G_t^++\Delta G^++d(t-s,Y_s^y)G_z^+]\,ds+dM_s=dM_s.
\tag{A.10}
\]

Consequently the coefficient must be evaluated at \(t-s\), not at
\(s\), and the accumulated shift is

\[
 \mathfrak S_t^y
 =\int_0^t d(t-s,Y_s^y)\,ds.
\tag{A.11}
\]

At stochastic time \(t\), the initial positive packet is evaluated. The
independent \(W_2\)-convolution gives

\[
 \mathbb E_{W_2}\partial K_{R^2}
 (z+\mathfrak S_t^y+\sqrt2W_2(t))
 =\partial K_{R^2+t}(z+\mathfrak S_t^y).
\tag{A.12}
\]

Therefore

\[
 \boxed{
 G^+(t,z,y)=R^3\mathbb E_y\!\left[
 \partial K_{R^2+t}(z+\mathfrak S_t^y)
 K_{R^2}(Y_t^y)\right].}
\tag{A.13}
\]

This verifies the sign, time order, and \(Z_s\)-definition in Lemma 2.1
of the audited source.

---

## 3. Exact periodic all-copy bridge identity

Let

\[
 k_\tau(x)=(4\pi\tau)^{-1/2}e^{-x^2/(4\tau)},\qquad
 K_\tau(x)=\sum_{m\in\mathbb Z}k_\tau(x+2\pi m).
\tag{A.14}
\]

For a nonnegative periodic function \(\Phi\), the Markov property gives,
with \(T=t+R^2\),

\[
 \mathbb E_y[\Phi(Y_s)K_{R^2}(Y_t)]
 =\int_{\mathbb T}K_s(\eta-y)\Phi(\eta)K_{T-s}(\eta)\,d\eta.
\tag{A.15}
\]

To check the copy bookkeeping from scratch, expand the two periodic kernels
with indices \(a,b\in\mathbb Z\):

\[
 \sum_{a,b}\int_{(-\pi,\pi]}
 k_s(\eta-y+2\pi a)\Phi(\eta)
 k_{T-s}(\eta+2\pi b)\,d\eta.
\tag{A.16}
\]

For fixed \(a\), set

\[
 \xi=\eta+2\pi a,\qquad n=a-b.
\tag{A.17}
\]

Then periodicity gives
\(\Phi(\eta)=\Phi(\xi\bmod2\pi)\), and evenness of
\(k_{T-s}\) changes its argument to

\[
 \eta+2\pi b=\xi-2\pi n,\qquad
 k_{T-s}(\xi-2\pi n)=k_{T-s}(2\pi n-\xi).
\tag{A.18}
\]

The intervals generated as \(a\) varies tile \(\mathbb R\), while
\((a,b)\mapsto(a,n)\) is bijective. Tonelli applies because the
integrand is nonnegative. Hence (A.15) equals

\[
 \sum_{n\in\mathbb Z}\int_{\mathbb R}
 k_s(\xi-y)k_{T-s}(2\pi n-\xi)
 \Phi(\xi\bmod2\pi)\,d\xi.
\tag{A.19}
\]

Completing the square gives exactly

\[
 k_s(\xi-y)k_{T-s}(2\pi n-\xi)
 =k_T(2\pi n-y)k_v(\xi-\mu_{n,s}),
\tag{A.20}
\]

where

\[
 v=\frac{s(T-s)}T,\qquad
 \mu_{n,s}=\frac{T-s}{T}y+\frac{s}{T}2\pi n.
\tag{A.21}
\]

This proves the audited formula (3.5), with every winding
\(n\in\mathbb Z\) retained. For the central winding,

\[
 \mu_s=\mu_{0,s}=\frac{T-s}{T}y,\qquad
 |\mu_s|\le|y|\le R.
\tag{A.22}
\]

If \(r=t-s\), then

\[
 v=s-\frac{s^2}{T},\qquad
 \boxed{v+r=t-\frac{s^2}{T}\le t.}
\tag{A.23}
\]

At \(s=0\), one has \(v=0\) and \(\mu_{n,0}=y\);
(A.20) is interpreted as the weak Dirac limit, and summing the endpoint
weights recovers \(\Phi(y)K_T(y)\). At \(s=t>0\), one has
\(T-s=R^2\) and \(v=tR^2/T>0\). When \(t=0\), the only
stochastic time is \(s=0\) and \(\mathfrak S_0^y=0\) exactly.
Thus neither endpoint hides a singular positive-time bridge assertion.

---

## 4. Transition buffer, seam, and the \(260\to264\) exponent

Let

\[
 \delta_R=\arcsin(\kappa R).
\tag{A.24}
\]

Since \(\kappa R\le1/2\), integration of
\((\arcsin x)'=(1-x^2)^{-1/2}\le2\) on \([0,1/2]\) yields

\[
 \delta_R\le2\kappa R=32R.
\tag{A.25}
\]

The saturation \(g\) equals one on
\([\delta_R,\pi-\delta_R]\pmod{2\pi}\). The point \(h\)
has distance at least

\[
 (c_hL-32)R\ge\alpha LR
\tag{A.26}
\]

from the defect set because
\((c_h-\alpha)L=L/240\ge32\). For the central bridge mean,
the allowance \(|\mu_s|\le R\) gives the exact \(33R\) reserve

\[
 \operatorname{dist}_{\mathbb T}
 (h+\mu_s,\{g\ne1\})\ge(c_hL-33)R.
\tag{A.27}
\]

The seam does not create a nearer defect: (A.2)--(A.3) put
\(h+\mu_s\) strictly near zero, while the \(\pi\)-side transition
remains a fixed distance away. The periodic heat-tail argument is
nevertheless global. If \(x\) is at circular distance \(\rho\) from
the defect set, every real lift that lands in a defect copy has
displacement at least \(\rho\). Since \(0\le1-g\le2\),

\[
 0\le1-\theta(\tau,x)
 \le2\mathbb P(|\sqrt2W_\tau|\ge\rho)
 \le4e^{-\rho^2/(4\tau)}.
\tag{A.28}
\]

Thus this tail estimate contains the seam and every lifted defect copy.

At \(L=9216\),

\[
 \frac{c_hL}{256}=\frac{135}{4}=33+\frac34,
\tag{A.29}
\]

and the left side increases with \(L\). Hence

\[
 c_hL-33\ge\frac{255}{256}c_hL.
\tag{A.30}
\]

The exponent conversion is strict:

\[
 \frac{(255/256)^2}{260}-\frac1{264}
 =\frac{3181}{112459776}>0.
\tag{A.31}
\]

Using (A.23) and \(t\le65R^2\), one obtains

\[
 1-\theta(r,h)\le4e^{-\alpha^2L^2/260},
\tag{A.32}
\]

\[
 1-\theta(r+v,h+\mu_s)
 \le4e^{-c_h^2L^2/264}.
\tag{A.33}
\]

At zero heat age these statements are pointwise equalities with left side
zero, since the relevant points lie strictly inside the \(g=1\) plateau.

---

## 5. Independent derivation of the \(6/R\) bridge bound

Put

\[
 \Phi_r(\eta)=|\theta(r,h)-\theta(r,h+\eta)|.
\tag{A.34}
\]

Because \(-1\le\theta\le1\),

\[
 \Phi_r(\eta)
 \le[1-\theta(r,h)]+[1-\theta(r,h+\eta)].
\tag{A.35}
\]

For \(n=0\), periodic semigroup composition gives

\[
\begin{aligned}
 &\int_{\mathbb R}k_v(\xi-\mu_s)\Phi_r(\xi)\,d\xi\\
 &\quad\le1-\theta(r,h)
 +1-\theta(r+v,h+\mu_s)\\
 &\quad\le4e^{-\alpha^2L^2/260}
 +4e^{-c_h^2L^2/264}.
\end{aligned}
\tag{A.36}
\]

The central endpoint weight obeys

\[
 k_T(-y)\le\frac1{2R},
\tag{A.37}
\]

because \(T\ge R^2\). For \(n\ne0\), use \(\Phi_r\le2\).
Since \(T\le66R^2\), \(R<1\), and \(|y|\le R\),

\[
 |2\pi n-y|\ge|n|.
\tag{A.38}
\]

With \(a_0=(264R^2)^{-1}\ge1\),

\[
\begin{aligned}
 \sum_{n\ne0}k_T(2\pi n-y)
 &\le\frac1R\sum_{n\ge1}e^{-n^2a_0}\\
 &\le\frac2R e^{-a_0}
 \le\frac2R e^{-c_h^2L^2/264}.
\end{aligned}
\tag{A.39}
\]

The last inequality follows from \(R^{-1}\ge L\), hence
\(R^{-2}\ge L^2\ge c_h^2L^2\). The central contribution in
(A.36)--(A.37) is at most

\[
 \frac2R\left(
 e^{-\alpha^2L^2/260}
 +e^{-c_h^2L^2/264}\right),
\tag{A.40}
\]

and the noncentral contribution is at most

\[
 \frac4R e^{-c_h^2L^2/264}.
\tag{A.41}
\]

Therefore

\[
 \boxed{
 \mathbb E_y[\Phi_{t-s}(Y_s)K_{R^2}(Y_t)]
 \le\frac6R\left(
 e^{-\alpha^2L^2/260}
 +e^{-c_h^2L^2/264}\right).}
\tag{A.42}
\]

This independently reproduces Lemma 3.2, including its displayed constant.

---

## 6. Calibration bound and the \(13/R\) accumulated shift

The direct tail estimate (A.32) is far below \(1/2\) at \(L\ge9216\),
so

\[
 \theta(s,h)\ge\frac12
 \qquad(R^2\le s\le65R^2).
\tag{A.43}
\]

Also \(q=\beta LR\le LR\le5/144<1/2\). Therefore the exact
calibration

\[
 B=\frac{q+1/2}{\int_{R^2}^{65R^2}\theta(s,h)\,ds}
\tag{A.44}
\]

gives

\[
 \boxed{0<B\le\frac1{32R^2}.}
\tag{A.45}
\]

By
\(|\mathfrak S_t^y|\le B\int_0^t\Phi_{t-s}(Y_s)\,ds\),
Tonelli and (A.42),

\[
\begin{aligned}
 \mathbb E_y[|\mathfrak S_t^y|K_{R^2}(Y_t)]
 &\le\frac{6Bt}{R}\left(
 e^{-\alpha^2L^2/260}
 +e^{-c_h^2L^2/264}\right)\\
 &\le\frac{195}{16R}\left(
 e^{-\alpha^2L^2/260}
 +e^{-c_h^2L^2/264}\right)\\
 &<\frac{13}{R}\left(
 e^{-\alpha^2L^2/260}
 +e^{-c_h^2L^2/264}\right).
\end{aligned}
\tag{A.46}
\]

The exact decay margins after the inverse-\(R\) factor are

\[
 \frac{\alpha^2}{260}-\frac1{320}
 =\frac{211}{936000}>0,\qquad
 \frac{c_h^2}{264}-\frac1{320}
 =\frac{23}{112640}>0.
\tag{A.47}
\]

Thus the right side of (A.46) tends to zero. This verifies Lemma 3.3.

---

## 7. Free positive packet

Subtract from (A.13) the zero-shift expression. Periodic smoothness permits
the real-line mean-value theorem even if \(z+\mathfrak S_t^y\) crosses
a chosen fundamental-domain seam. Since \(R^2+t\ge R^2\),

\[
 \|\partial^2K_{R^2+t}\|_\infty\le CR^{-3}.
\tag{A.48}
\]

Also

\[
 \mathbb E_yK_{R^2}(Y_t)=K_{R^2+t}(y).
\tag{A.49}
\]

Equations (A.13), (A.46), and (A.48)--(A.49) imply

\[
\begin{aligned}
 &\left|G^+(t,z,y)
 -R^3\partial K_{R^2+t}(z)K_{R^2+t}(y)\right|\\
 &\qquad\le
 CR^{-1}\left(
 e^{-\alpha^2L^2/260}
 +e^{-c_h^2L^2/264}\right)=o(1).
\end{aligned}
\tag{A.50}
\]

This is Lemma 4.1. On the terminal slice
\(65R^2-R^3<t<65R^2\), the normalized heat age lies in
\([66-R,66]\). For \(5R/4\le z\le3R/2\) and \(|y|\le R\),
the central real-Gaussian derivative has one fixed sign and nonzero uniform
magnitude after multiplication by \(R^3\); all other periodic copies are
\(O(e^{-c/R^2})\). Hence (A.50) yields the \(2c_0\)
positive-packet lobe of Proposition 4.2 for a fixed sufficiently small
\(c_0>0\).

---

## 8. Inverted packet and sufficiency for Proposition 5.2

In original coordinates the backward generator associated with

\[
 F_t+b(t,x_3)F_{x_2}=\Delta F
\tag{A.51}
\]

is

\[
 \Delta-b(t-s,x_3)\partial_2.
\tag{A.52}
\]

Thus, with

\[
 \mathfrak B_t^{x_3}=\int_0^tb(t-s,X_s^{x_3})\,ds,
\tag{A.53}
\]

the packet initially centred at \((-q_{\rm pre},-h)\) has the exact
formula

\[
 F^-(t,x_2,x_3)
 =R^3\mathbb E_{x_3}\!\left[
 \partial K_{R^2+t}(x_2+q_{\rm pre}-\mathfrak B_t^{x_3})
 K_{R^2}(X_t^{x_3}+h)\right].
\tag{A.54}
\]

The minus sign before \(\mathfrak B\) is correct by (A.52). No sign or
size information about \(\mathfrak B\) is needed because

\[
 \|\partial K_{R^2+t}\|_\infty\le CR^{-2}.
\tag{A.55}
\]

At \(x_3=h+y\), with \(|y|\le R\), transverse semigroup composition
gives

\[
 \mathbb E_{h+y}K_{R^2}(X_t+h)=K_{R^2+t}(2h+y).
\tag{A.56}
\]

The central transverse distance is at least
\((2c_hL-1)R\), while \(4(R^2+t)\le264R^2\). Since
\(2h+y\) remains in the central chart, the central copy and all other
copies obey

\[
 K_{R^2+t}(2h+y)
 \le CR^{-1}e^{-(2c_hL-1)^2/264}
 +CR^{-1}e^{-c/R^2}.
\tag{A.57}
\]

Multiplying (A.55), (A.57), and the datum factor \(R^3\) proves

\[
 \boxed{
 |F^-(t,x_2,h+y)|
 \le Ce^{-(2c_hL-1)^2/264}+Ce^{-c/R^2}=o(1),}
\tag{A.58}
\]

uniformly in \(x_2\) and \(0\le t\le65R^2\). This independently
verifies Lemma 5.1, including the noncentral copies.

Proposition 4.2 supplies a positive-packet contribution of magnitude at
least \(2c_0\), with a constant sign, throughout its terminal lobe. By
(A.58), after increasing the base index once, the inverted packet is at
most \(c_0\) there. Hence

\[
 |F^++F^-|\ge|F^+|-|F^-|\ge c_0,
\tag{A.59}
\]

and the sign agrees with the positive packet. This is exactly the claim of
Proposition 5.2. No additional Brownian confinement, longitudinal chart,
or sign control of \(\mathfrak B\) is required. Full inversion oddness
gives the reflected lobe with the opposite sign.

For the downstream endpoint lower bound, Proposition 5.2 is also the
needed analytic input: once the separately checked deterministic lobe
geometry places a positive-measure terminal lobe in \(A_j(R)\),
integration of \(|\mathfrak a_jF_j|^2\), multiplication by
\(\gamma_j\), and the \(R^{-1}\) normalization yield the source's
lower bound. This step does not supply any still-open local-energy,
pressure, transition, or full-denominator upper row.

---

## 9. Finite certificate and claim boundary

The separate producer
scripts/r074f_two_packet_survival_certificate.py
reproduces its JSON byte-for-byte and reports **PASS: 30/30**. Its scope
is finite exact arithmetic: parameter identities, strict rational margins,
the first admissible discrete index, and conditional terminal-annulus
geometry. In particular, the following analytic facts were established by
the proof above rather than by those 30 checks:

1. the moving-coordinate PDE and time-reversed stochastic sign;
2. the \(t-s\) coefficient order;
3. the all-copy Brownian-bridge identity and endpoint limits;
4. the seam-aware heat-tail estimate;
5. the \(6/R\) and \(13/R\) stochastic estimates;
6. the positive free-packet comparison; and
7. the inverted-packet suppression and Proposition 5.2 implication.

The audited result is a survival theorem for the explicit smooth periodic
paired-stream family at this exact source revision. It proves neither the
complete payment ledger nor any arbitrary-solution regularity or blow-up
statement. No novelty or priority conclusion was investigated. **NOT
CLAY.**
