# R0.74J — the exact family has a matching complete-payment law

## Status and scope

R0.74I left open whether the exact R0.74F--H family pays the full scale
\(B_j^3R_j^3\).  This note closes that familywise gap.  A fixed box in the
fifth weighted annulus sees the background shear for the whole payment time
interval.  That single nonnegative row gives the missing lower bound.

The result is

\[
 P_{R_j}^M=P_{R_j}^F\asymp B_j^3R_j^3,
 \qquad
 \frac{\log P_{R_j}^M}{L_j^2}\longrightarrow\frac3{320}.
\]

This is a statement about one explicit sequence of smooth periodic unforced
solutions.  It does not prove a universal endpoint estimate, create a good
scale at a possible singular point, or prove global regularity.  **NOT
CLAY.**

Proof status: **PROVED**.  Release checks: finite certificate
**PASS 38/38** and formal figure **PASS 79/79**.  Exact-source analytic
rebinds, the freeze manifest, and publication are recorded separately so
that this proof byte sequence can remain fixed.

---

## 1. Frozen family and inherited upper bound

Retain exactly the R0.74F--H constants and fields analysed in R0.74I.  Thus

\[
 L_j=\frac{63}{32}2^j,\qquad
 R_j=e^{-\rho L_j^2},\qquad
 \rho=\frac1{320},
\tag{1.1}
\]

\[
 g_j(x_3)=\sigma\!\left(\frac{\sin x_3}{16R_j}\right),
 \qquad
 \theta_j(t,x_3)=e^{t\partial_3^2}g_j(x_3),
\tag{1.2}
\]

\[
 \gamma_j^{\rm tar}=e^{-c_\gamma L_j^2},
 \qquad c_\gamma=\frac8{3969},
\tag{1.3}
\]

The target weight is the same numerical sequence as the annular weights in
(3.2), because

\[
 c_\gamma L_j^2
 =\frac8{3969}\left(\frac{63}{32}\right)^2 4^j
 =\frac{4^{j-1}}{32},
 \qquad \gamma_j^{\rm tar}=e^{-4^{j-1}/32}=\Gamma_j.
\tag{1.3a}
\]

The roles remain different: \(j\) is the family index in the packet
amplitude, whereas \(k\) is the payment-shell index in \(\Gamma_k\).

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),\qquad p_j=0,
 \qquad \mathfrak a_j=B_j(\gamma_j^{\rm tar})^{-1/2}.
\tag{1.4}
\]

The saturation \(\sigma\in C^\infty(\mathbb R;[-1,1])\) is odd and obeys
\(\sigma(s)=\operatorname {sgn}s\) for \(|s|\ge1\).  The exact contrast
calibration gives

\[
 \beta_j:=B_jR_j^2\longrightarrow\frac1{128}.
\tag{1.5}
\]

The symmetry identities frozen in R0.74F imply

\[
 X_{R_j}(t)=a_{R_j}(t)=a_{R_j}'(t)=0.
\tag{1.6}
\]

Consequently Versions M and F coincide on this family, including every
acceleration row.  Write their common payment as

\[
 P_j:=P_{R_j}^M=P_{R_j}^F.
\tag{1.7}
\]

R0.74G Theorem 1.1 supplies a constant \(C<\infty\), independent of \(j\),
such that

\[
 P_j\le C B_j^3R_j^3
\tag{1.8}
\]

for all sufficiently large \(j\).  It remains only to prove the reverse
inequality.

---

## 2. A profile-independent shear platform

Set

\[
 z_{0,j}=(65R_j^2,0),\qquad z_0=z_{0,j}.
\tag{2.1}
\]

In this section write \(R=R_j\), \(B=B_j\), \(g=g_j\), and
\(\theta=\theta_j\).  Put

\[
 \delta_R=\arcsin(16R),\qquad
 P_R=[\delta_R,\pi-\delta_R]\pmod {2\pi}.
\tag{2.2}
\]

The initial shear profile satisfies \(g=1\) on \(P_R\) and
\(-1\le g\le1\) everywhere.

### Lemma 2.1 — uniform fifth-shell shear lower bound

If \(0<R\le1/200\), then

\[
 \boxed{
 \theta(t,x_3)\ge\frac12
 \quad\text{whenever}\quad
 0\le t\le65R^2,\quad80R\le x_3\le96R.}
\tag{2.3}
\]

**Proof.**  Since \(R\le1/32\), the elementary estimate inherited from
R0.74F gives

\[
 \delta_R=\arcsin(16R)\le32R.
\tag{2.4}
\]

For \(x_3\in[80R,96R]\), the distance to the left endpoint of \(P_R\)
is at least \(48R\).  The distance to the right endpoint is at least

\[
 \pi-\delta_R-96R
 \ge3-128R
 \ge48R,
\tag{2.5}
\]

where \(\pi>3\) and \(R\le1/200\) were used in the last two steps.
Thus the circular distance from \(x_3\) to \(P_R^c\) is at least \(48R\).

Let \(Z_t\) be a centred real Gaussian of variance \(2t\).  The periodic
heat-semigroup representation gives

\[
 \theta(t,x_3)=\mathbb E\,g(x_3+Z_t\bmod2\pi).
\tag{2.6}
\]

If the point in (2.6) leaves \(P_R\), then

\[
 48R\le d_{\mathbb T}(x_3,P_R^c)
 \le d_{\mathbb T}(x_3,x_3+Z_t)
 \le |Z_t|.
\tag{2.7}
\]

Since
\(0\le1-g\le2\), Chebyshev's inequality yields

\[
\begin{aligned}
 1-\theta(t,x_3)
 &\le2\,\mathbb P(|Z_t|\ge48R)\\
 &\le2\frac{\mathbb E|Z_t|^2}{(48R)^2}
 =\frac{4t}{2304R^2}
 \le\frac{65}{576}<\frac12.
\end{aligned}
\tag{2.8}
\]

Therefore \(\theta(t,x_3)>1/2\), proving (2.3).  Notice that the argument
uses no monotonicity or sign assumption on \(\sigma\) inside \((-1,1)\).
\(\square\)

The deliberately coarse Chebyshev bound makes every numerical comparison in
this lemma rational.  The sharper periodic Gaussian-tail estimate from
R0.74F is not needed.

---

## 3. The fifth annulus forces the missing payment

At payment radius \(2R\), the time interval and weighted annuli are

\[
 I_{2R}=(61R^2,65R^2),
 \qquad
 A_k(2R)=\{2^{k+1}R\le|x|<2^{k+2}R\},
\tag{3.1}
\]

\[
 W_{2R}(x)=\sum_{k\ge1}\Gamma_k1_{A_k(2R)}(x),
 \qquad
 \Gamma_k=e^{-4^{k-1}/32}.
\tag{3.2}
\]

In particular,

\[
 A_5(2R)=\{64R\le|x|<128R\},
 \qquad \Gamma_5=e^{-8}.
\tag{3.3}
\]

Define the spatial box

\[
 Q_R=\{|x_1|<R,\ |x_2|<R,\ 80R<x_3<96R\}.
\tag{3.4}
\]

### Lemma 3.1 — exact shell geometry

For every \(R>0\),

\[
 \boxed{Q_R\subset A_5(2R),\qquad |Q_R|=64R^3.}
\tag{3.5}
\]

**Proof.**  On \(Q_R\),

\[
 |x|>80R>64R
\tag{3.6}
\]

and

\[
 |x|^2<(96^2+1+1)R^2=9218R^2<128^2R^2.
\tag{3.7}
\]

The three side lengths are \(2R\), \(2R\), and \(16R\), so the volume is
\(64R^3\). \(\square\)

The nonnegative velocity-cubic row of the complete payment, written for the
full-space periodic lift of \(u_j\), is

\[
 \mathcal G_u(z_0,2R;1)
 =(2R)^{-2}\int_{I_{2R}}\int_{\mathbb R^3}
 W_{2R}(x)|u(t,x)|^3\,dx\,dt.
\tag{3.8}
\]

### Theorem 3.2 — explicit matching lower bound

For all sufficiently large \(j\),

\[
 \boxed{
 \mathcal G_u(z_0,2R_j;1)
 \ge8e^{-8}B_j^3R_j^3.}
\tag{3.9}
\]

**Proof.**  Since \(R_j\to0\), Lemma 2.1 applies for all sufficiently
large \(j\).  After increasing the threshold index, (1.5) also gives
\(B_j>0\).  The two velocity components in (1.4) are orthogonal, hence

\[
 |u|^3=(\mathfrak a^2F^2+B^2\theta^2)^{3/2}
 \ge B^3|\theta|^3.
\tag{3.10}
\]

Restrict (3.8) to \(I_{2R}\times Q_R\), then use Lemmas 2.1 and 3.1:

\[
\begin{aligned}
 \mathcal G_u(z_0,2R;1)
 &\ge(2R)^{-2}e^{-8}
   (4R^2)(64R^3)B^3\left(\frac12\right)^3\\
 &=8e^{-8}B^3R^3.
\end{aligned}
\tag{3.11}
\]

The passive packet cannot cancel this contribution because the integrand is
the norm of the full velocity, not a signed component. \(\square\)

### Theorem 3.3 — matching complete-payment law

There are constants \(0<c<C<\infty\) and \(j_0\) such that, for every
\(j\ge j_0\),

\[
 \boxed{
 cB_j^3R_j^3
 \le P_{R_j}^M=P_{R_j}^F
 \le CB_j^3R_j^3.}
\tag{3.12}
\]

One may take \(c=8e^{-8}\).

**Proof.**  The velocity-cubic row (3.8) is one nonnegative summand of
\(P_{R_j}^M\).  Equations (1.6)--(1.7) identify the Version-F payment with
the Version-M payment.  Theorem 3.2 gives the lower bound, and the inherited
R0.74G estimate (1.8) gives the upper bound. \(\square\)

---

## 4. Exact logarithmic rate and endpoint meaning

Equation (1.5) lets us write

\[
 B_j^3R_j^3=\beta_j^3R_j^{-3}
 =\beta_j^3e^{3\rho L_j^2}.
\tag{4.1}
\]

### Corollary 4.1 — the R0.74I window collapses to a limit

\[
 \boxed{
 \lim_{j\to\infty}\frac{\log P_j}{L_j^2}
 =3\rho=\frac3{320}.}
\tag{4.2}
\]

**Proof.**  Taking logarithms in (3.12) and using
\(\beta_j\to1/128\) gives

\[
 \log P_j=3\rho L_j^2+O(1).
\tag{4.3}
\]

Division by \(L_j^2\to\infty\) proves (4.2). \(\square\)

Since \(L_{j+1}=2L_j\), the same calculation sharpens the lacunarity
asymptotic to

\[
 \boxed{
 \log\frac{P_{j+1}}{P_j}=9\rho L_j^2+O(1).}
\tag{4.4}
\]

The complete payment is much larger than the target lower-bound scale:

\[
 \frac{P_j}{B_j^2L_jR_j^2}
 \asymp\frac{B_jR_j}{L_j}
 =\frac{\beta_j}{L_jR_j}\longrightarrow\infty.
\tag{4.5}
\]

Thus an attempted familywise upper bound
\(P_j\lesssim B_j^2L_jR_j^2\) is false.

The lower bound in (3.12) and (4.1) also show that \(P_j>1\) for all
sufficiently large \(j\).  On the other hand, (3.12) and (4.2) give the exact
right-side scale

\[
 P_j^{2/3}\sqrt{1+\log_+ P_j}
 \asymp B_j^2L_jR_j^2.
\tag{4.6}
\]

Combined with the inherited R0.74F--H lower bounds
\(X_j,\mathfrak C_j\gtrsim B_j^2L_jR_j^2\), equation (4.6) explains why
the R0.74I analysis rejects every logarithmic power below \(1/2\), while it
does not reject \(1/2\) by scale counting.  Equation (4.6) alone is not an
endpoint upper bound for either observable.  A sharp upper analysis of
\(X_j\) requires a separate inward-tail audit; an upper analysis of
\(\mathfrak C_j\) also requires collar-flux and energy upper audits.

---

## 5. Literature and route boundary

The proof above is internal to the frozen explicit family.  The literature
review was used to decide what not to claim next.

1. Yang's skewed-cylinder theory already proves quantitative comparison of
   mollified trajectories and containment of intersecting admissible
   cylinders.  It also proves eventual admissibility for almost every
   spacetime point, not for every prescribed point.
2. Vasseur--Yang already combine mollified-flow recentering, a local
   pressure-free regularity mechanism, and the skewed-cylinder maximal
   function for suitable weak Navier--Stokes solutions.
3. Lei--Ren obtain a logarithmic improvement of Caffarelli--Kohn--Nirenberg
   partial regularity using nonoverlapping hollow dissipation layers.  This
   controls the size of the singular set and produces quantitative regular
   regions, but it does not turn a small hollow layer into a small normalized
   moving core at a preassigned possible singular point.
4. Wang--Wu--Zhou already prove a velocity-only one-scale epsilon-regularity
   theorem for suitable weak solutions.  Its exponent-\(3\) specialization
   does not supply the missing prescribed-point smallness mechanism.

Therefore R0.74J does not present cross-scale containment as a new theorem
and does not claim that finite energy produces the R0.74I epsilon-smallness
hypothesis.  The remaining global route gap is still a prescribed-point
core-from-shell or payment-to-admissibility mechanism.

Primary-source details and exact claim boundaries are recorded in
`research/r074j_primary_literature_boundary.md` and
`research/r074j_report-source.md`.

---

## 6. What changed, and what remains open

### Proved here

- The fifth weighted annulus alone gives
  \(\mathcal G_u\ge8e^{-8}B_j^3R_j^3\).
- The exact family has the common Version-M/Version-F quantity
  \(P_j=P_{R_j}^M=P_{R_j}^F\asymp B_j^3R_j^3\).
- Its logarithmic payment rate is exactly \(3/320\).
- Its consecutive payment ratio satisfies the sharper asymptotic (4.4).

### Historical correction

R0.74I correctly labelled the matching lower bound as unproved at its freeze
time.  Theorem 3.3 supersedes that one open-family statement.  The frozen
R0.74I file is retained unchanged as the record of the earlier state.

### Still open

- a universal square-root-log endpoint upper bound;
- a matching upper bound for \(X_j\) or \(\mathfrak C_j\) on this family;
- payment-to-admissibility or moving core-from-shell control;
- a good-scale theorem at a prescribed possible singular point;
- global regularity for arbitrary smooth finite-energy data.

No singular solution has been constructed and no singularity has been
excluded beyond the conditional criteria already recorded in R0.74I.
**NOT CLAY.**
