# R0.74C — independent analytic audit of the advected-shear obstruction

**Audit date:** 2026-09-01

**Status:** `PASS`

**Frozen source:** commit
`d6c59e31c4a10800a1e091390a25ad5672dc17d5`, file
`research/r074c_advected_shear_large_payment_obstruction.md`, SHA-256
`b300e7c32f9d944be36813530c5ffd1d7bc7463d161bba829284b4ab2d3e2c09`.

I independently recalculated the analytic argument in the frozen source. I
used the R0.73X and R0.74B notes only to recover the definitions of the
frozen observables and pressure gauge. I did not use the R0.74C finite
certificate as a proof of any analytic estimate.

The conclusion of this audit is:

\[
 \boxed{
 \sup_{\substack{0<R<\pi/16\\
 (u,p)\ {\rm smooth\ periodic\ NSE}}}
 \frac{\mathcal U_{\rm ext}^{\infty}+\mathcal D_{\rm ext}}
 {\bigl(\mathcal E(z_0,8R)^{3/2}
       +\mathcal A_{\rm ext}(z_0,2R;1)\bigr)^{2/3}}
 =\infty }
\]

for the fixed-centre, standard-clock, \(\nu=\theta=1\) quantities is
supported by the displayed construction. No analytic gap was found in the
items listed below.

---

## 1. Exact periodic NSE identity and the full interval

Write

\[
 F(t,x_2)=R^2\partial_2K_{t+R^2}^{\rm per}(x_2-q(t)),
 \qquad q'(t)=V,
\]

and

\[
 u=AF e_1+Ve_2,\qquad p=0.
\]

The periodic heat equation gives

\[
 \partial_tF+V\partial_2F=\partial_2^2F.
\]

Also

\[
 \nabla\cdot u=0,\qquad
 (u\cdot\nabla)u=AV\partial_2F\,e_1,
 \qquad \Delta u=A\partial_2^2F\,e_1.
\]

Therefore

\[
 \partial_tu-\Delta u+(u\cdot\nabla)u+\nabla p=0
\]

pointwise. There is no unrecorded \(A^2\) nonlinear row: the shear is in
the \(e_1\) direction and depends only on \(x_2\), while the only advecting
component is the constant \(Ve_2\).

On the entire solution interval \(0<t<66R^2\), the heat age is
\(t+R^2>R^2\). Thus the periodic kernel and all its derivatives are
analytic there. Moreover

\[
 \overline{I_{8R}}=[R^2,65R^2]\Subset(0,66R^2).
\]

The construction is consequently an exact smooth unforced periodic NSE
trajectory on the full claimed interval, not only on the buffered slab.

**Result:** `PASS`.

---

## 2. Periodic derivative kernel, mean zero, and periodic copies

Termwise differentiation of the absolutely convergent periodic heat-kernel
series is valid for every positive heat age. Periodicity gives

\[
 \int_{-\pi}^{\pi}\partial_2K_\tau^{\rm per}(x_2-q)\,dx_2=0.
\]

Hence the shear component has zero periodic mean for every time. The total
mean of \(u\) is \(Ve_2\); the proof does not incorrectly call the whole
velocity mean zero.

For lifted estimates, the kernel centres are

\[
 q_n(t)=q(t)+2\pi n,\qquad n\in\mathbb Z.
\]

On the local buffered cylinder the central copy is at distance at least
\((M-8)R\). Under the frozen small-chart conditions, every noncentral copy
is farther away. Its contribution is bounded by a Gaussian of order
\(e^{-c/R^2}\), uniformly in the final large-\(m\) sequence. For the lifted
far-field integrals, the proof retains the full sum over all \(q_n\). The
uniform separation by \(2\pi\) gives bounded Gaussian overlap, and

\[
 \sum_{n\in\mathbb Z}\frac1{q_n^2+S^2}
 \le C\left(\frac1{q^2+S^2}+1\right)
 \le \frac C{q^2}.
\]

Thus neither the local estimate nor the lifted estimate truncates the
periodic copies.

**Result:** `PASS`.

---

## 3. Target lower bound and its exact exponent

At the terminal time the central kernel has dimensionless heat age \(66\).
For a fixed interval \(1<b_1<b_2<2\),

\[
 \left|R^2\partial_2K_{66R^2}(R\xi)\right|
 =\left|\frac d{d\xi}
  \left((4\pi66)^{-1/2}e^{-\xi^2/264}\right)\right|
 \ge c_0>0
\]

on \([b_1,b_2]\). The noncentral periodic images are uniformly negligible
after the fixed small-\(R\) reduction. Continuity supplies a positive-time
interval immediately before \(t_0\), contained in \(I_R\), on which the
same lower bound holds.

Since

\[
 M=3\,2^{m-1},\qquad
 2^mR=\frac23MR,qquad
 2^{m+1}R=\frac43MR,
\]

the strip, intersected with a transverse disc of radius \(MR/4\), lies in
\(A_m(R)\) for all sufficiently large \(m\). Its volume is at least
\(cM^2R^3\). Dividing by the exterior-energy normalization \(R\) gives

\[
 \mathcal U_{\rm ext}^{\infty}
 \ge cA^2M^2R^2\gamma_m(1).
\]

Finally,

\[
 \gamma_m(1)=e^{-4^{m-1}/32}
 =e^{-M^2/(9\cdot32)}=e^{-M^2/288}.
\]

The essential supremum is legitimate because the lower bound holds on a
time interval of positive measure, not only at the excluded endpoint.

**Result:** `PASS`.

---

## 4. Buffered leakage and the strict exponent margin

On \(I_{8R}\times B_{8R}\),

\[
 \tau\le66R^2,
 \qquad |x_2-q(t)|\ge(M-8)R.
\]

The central Gaussian therefore contributes an exponent at most

\[
 -\frac{(M-8)^2}{264}\le-\frac{M^2}{528}
 \qquad(M\ge64).
\]

After squaring, both \(|F|^2\) and \(R^2|\partial_2F|^2\) are bounded by

\[
 C(1+M)^8e^{-M^2/264}.
\]

The degree-eight majorant is sufficient: the unsquared first two kernel
derivatives have polynomial degree at most two; the squared and cubed
expressions used later have degree at most six. No power of \(M\) has been
hidden in the exponential comparison.

The target decays with \(e^{-M^2/288}\), and

\[
 \frac1{264}-\frac1{288}=\frac1{3168}>0.
\]

Thus the local heat leakage has the required strictly faster decay.

**Result:** `PASS`.

---

## 5. Lifted annular weights and all copies

For \(S=2R\), the Gaussian annular weight satisfies

\[
 W_S(y)\le C\frac{S^4}{|y|^4},\qquad
 \int_{\mathbb R^3}W_S\le CS^3,
\]

and its transverse integral satisfies

\[
 \int_{\mathbb R^2}W_S(y_1,y_2,y_3)\,dy_1dy_3
 \le\frac{CS^4}{y_2^2+S^2}.
\]

The harmonic weight

\[
 L_S=S\sum_{j\ge1}(2^jS)^{-4}1_{A_j(S)}
\]

similarly obeys

\[
 \int_{\mathbb R^2}L_S\,dy_1dy_3
 \le\frac{CS}{y_2^2+S^2}.
\]

These are infinite-annulus estimates. Combining them with the full packet
sum over \(q_n=q+2\pi n\) gives

\[
 \int W_S|\widetilde F|^3\le\frac{CR^5}{q^2},
 \qquad
 \int L_S|\widetilde F|^2\le\frac{CR^2}{q^2}.
\]

The dimensions are respectively \(R^3\) and dimensionless after the
profile normalization, as required by the subsequent rows.

**Result:** `PASS`.

---

## 6. Frozen pressure gauge, local pressure, and CZ/Jensen

The physical pressure is \(p=0\), but the frozen local split is

\[
 p_S^{\rm loc}=\mathcal R_i\mathcal R_j
 (\zeta_S\widetilde u_i\widetilde u_j),
 \qquad h_S=\widetilde p-p_S^{\rm loc}
\]

on \(B_{3S}\). Therefore

\[
 h_S=-p_S^{\rm loc},\qquad
 c_S=(h_S)_{B_{2S}}=-(p_S^{\rm loc})_{B_{2S}}.
\]

It would be wrong to infer \(c_S=0\) from \(p=0\); the source does not make
that inference. Jensen and the whole-space Calderón--Zygmund bound give

\[
 |c_S|^{3/2}
 \le CS^{-3}\int_{B_{4S}}|u|^3.
\]

Because the lifted physical pressure is identically zero,
\(p-c_S=-c_S\) on every lifted annulus. The total Gaussian weight has mass
\(O(S^3)\), so

\[
 \mathcal G_p(z_0,S;1)
 \le CS^{-2}\int_{I_S}\int_{B_{4S}}|u|^3.
\]

The cutoff source includes the apparent \(AVF\) tensor entries. They are
not omitted: the bound uses the full \(|u|^3\), and

\[
 (A|F||V|)^{3/2}
 \le C(A^3|F|^3+|V|^3).
\]

The local pressure and harmonic remainder are therefore handled even
though the selected physical gauge has \(p=0\).

**Result:** `PASS`.

---

## 7. Independent \(A,V,R,M\) payment ledger

On \(I_S=(61R^2,65R^2)\),

\[
 q\in[MR,q_*/8],\qquad |V|\asymp R^{-2},
 \qquad |dt|=\frac{|dq|}{|V|}\le CR^2|dq|.
\]

Since \(V<0\), the \(q\)-integration reverses orientation. The source's
display \(dt=dq/|V|\) is read as the positive integration measure after
that reversal. Every subsequent bound uses the correct positive measure.

The recalculated rows are:

| Quantity | constant-background row | shear row |
|---|---:|---:|
| \(\mathcal E(z_0,8R)\) | \(R^{-2}\) | \(A^2R^2\Pi_Me^{-M^2/264}\) |
| \(\mathcal G_u(z_0,S;1)\) | \(R^{-3}\) | \(A^3R^4M^{-1}\) |
| \(\mathcal G_p(z_0,S;1)\) | \(R^{-3}\) | \(A^3R^3\Pi_Me^{-3M^2/528}\) |
| \(\mathcal H_u(z_0,S)\) | \(R^{-3}\) | \(A^3R^4M^{-2}\) |

Here \(\Pi_M=(1+M)^8\). The individual derivations are:

1. The constant velocity contributes \(V^2R^2\asymp R^{-2}\) to
   \(\mathcal E\), and it has no gradient.
2. The Gaussian velocity row uses
   \(S^{-2}A^3(R^5/q^2)\), followed by the \(R^2dq\) time measure. This
   gives \(A^3R^4/M\).
3. The pressure row is local after the frozen-gauge estimate. Its shear
   part has volume \(R^3\), time \(R^2\), and normalization \(R^{-2}\),
   giving \(A^3R^3\) times the cubed leakage.
4. The harmonic row has
   \(\Lambda_S\lesssim V^2+A^2R^2/q^2\). Raising to \(3/2\), multiplying
   by \(S\), and integrating with \(R^2dq\) gives
   \(A^3R^4/M^2\).

All rows have NSE amplitude degree three after entering the payment. The
different powers of \(M\) come only from \(\int q^{-2}dq\) and
\(\int q^{-3}dq\).

**Result:** `PASS`.

---

## 8. The \(P\) and \(P^{2/3}\) ledgers

Using

\[
 P=\mathcal E(z_0,8R)^{3/2}
   +\mathcal G_u+\mathcal G_p+\mathcal H_u,
\]

the preceding rows give

\[
 P\le C\left[
 R^{-3}
 +A^3R^3\Pi_Me^{-3M^2/528}
 +A^3R^4M^{-1}
 \right].
\]

The \(A^3R^4M^{-2}\) harmonic shear row is smaller than the displayed
\(M^{-1}\) row. The polynomial in the \(3/2\)-power of the energy leakage
has degree at most six, so it is still paid by \(\Pi_M\).

Applying the concavity inequality for the \(2/3\)-power yields

\[
 P^{2/3}\le C\left[
 R^{-2}
 +A^2R^2\Pi_Me^{-M^2/264}
 +A^2R^{8/3}M^{-2/3}
 \right].
\]

The exponent conversion is exact:

\[
 \frac23\frac3{528}=\frac1{264}.
\]

No \(P\)-row is compared directly with the quadratic target before first
taking the required \(2/3\)-power.

**Result:** `PASS`.

---

## 9. The three divergent ratios

Set

\[
 R_M=e^{-M^2/96},\qquad
 A_M=R_M^{-2}e^{M^2/576},
\]

along \(M=3\,2^{m-1}\to\infty\). The target lower row is

\[
 L_M=cA_M^2M^2R_M^2e^{-M^2/288}.
\]

The three independent comparisons are:

| Denominator row in \(P^{2/3}\) | Recalculated ratio | Limit |
|---|---:|---:|
| heat leakage \(A_M^2R_M^2\Pi_Me^{-M^2/264}\) | \(\displaystyle \frac{cM^2}{\Pi_M}e^{M^2/3168}\) | \(\infty\) |
| exterior cubic \(A_M^2R_M^{8/3}M^{-2/3}\) | \(\displaystyle cM^{8/3}e^{M^2/288}\) | \(\infty\) |
| background \(R_M^{-2}\) | \(cM^2\) | \(\infty\) |

For the background row, the cancellation

\[
 A_M^2R_M^4e^{-M^2/288}=1
\]

is exact. For the exterior row,
\(R_M^{-2/3}e^{-M^2/288}=e^{M^2/288}\). These checks establish
\(X_{R_M}/P_{R_M}^{2/3}\to\infty\).

**Result:** `PASS`.

---

## 10. Quantifiers, finiteness, open boundary, and Clay boundary

The sequence satisfies, eventually,

\[
 R_M<\pi/16,
 \qquad M\ge64,
 \qquad MR_M\le q_*/16,
 \qquad MR_M\to0.
\]

Hence all small-chart and large-\(M\) hypotheses hold simultaneously. For
each fixed \(M\), \(R_M>0\), \(A_M<\infty\), \(T_{R_M}>0\), and the
solution and every frozen payment are finite. The proof needs no uniform
global-energy bound across the sequence, and the rejected estimate does not
assume one.

The result is a quantified sequence of smooth exact solutions at positive
scales. It is not a finite sampling, DNS, or Galerkin statement. It rules
out only the frozen fixed-centre pure \(P^{2/3}\) large-payment closure.

The following statements remain outside the proof:

1. an optimal replacement for the fixed-centre large-\(P\) row;
2. a pure \(P^{2/3}\) estimate for a co-moving, mean-subtracted observable;
3. weak stability or lower semicontinuity of the exterior tails;
4. absorption, epsilon regularity, singularity formation, global
   regularity, or blow-up.

Accordingly, `FINITE`, `OPEN`, and `NOT CLAY` are used consistently. Here
`OPEN` records what is not resolved by this frozen argument; this analytic
audit does not turn that label into a global novelty or priority claim.

**Result:** `PASS`.

---

## 11. Separation from the 83/83 finite certificate

The existing certificate reports 83 passing finite checks over frozen-byte
provenance, parsed parameters, rational exponent arithmetic, monomial
ledgers, and labels. Its declared scope excludes the heat-kernel analytic
bounds, Calderón--Zygmund estimate, infinite periodic-copy sums, infinite
quantifiers, limiting argument, and Clay boundary.

This audit did not infer analytic validity from those 83 checks. Sections
1--10 above separately recalculate the PDE identity, periodic mean,
Gaussian target and leakage estimates, lifted-copy sums, pressure gauge,
all payment powers, and limiting quantifiers. Conversely, this audit does
not reproduce the certificate producer, its parser, its coverage bijection,
or its frozen-byte machinery.

**Result:** `PASS / independent analytic layer`.

---

## 12. Uncovered boundaries

This audit does not cover:

1. primary-literature completeness, novelty, or priority;
2. optimization of numerical constants, \(R_0\), \([b_1,b_2]\), or the
   polynomial majorant degree;
3. extensions to general \(\nu\), general \(\theta\), nonperiodic domains,
   moving centres, or weak solutions;
4. the truth of any revised positive estimate listed as open;
5. independent execution or code review of the 83/83 finite certificate;
6. HTML, PDF, figure, route, or publication synchronization.

These omissions do not enter the frozen negative theorem.

---

## Final PASS ledger

| Audit item | Status |
|---|---|
| Exact periodic NSE PDE identity on \((0,T_R)\) | `PASS` |
| Buffered interval strictly inside the solution interval | `PASS` |
| Derivative-kernel periodic mean zero | `PASS` |
| Local and lifted treatment of all periodic copies | `PASS` |
| Target exponent \(-M^2/288\) | `PASS` |
| Leakage exponent \(-M^2/264\) | `PASS` |
| Strict margin \(1/264>1/288\) | `PASS` |
| Frozen \(p=0\), \(p_S^{\rm loc}\), \(h_S\), and \(c_S\) handling | `PASS` |
| Calderón--Zygmund/Jensen pressure bound | `PASS` |
| \(\mathcal G_u\) powers | `PASS` |
| \(\mathcal G_p\) powers | `PASS` |
| \(\mathcal H_u\) powers | `PASS` |
| \(P\) ledger | `PASS` |
| \(P^{2/3}\) ledger | `PASS` |
| Heat-leakage ratio divergence | `PASS` |
| Exterior-cubic ratio divergence | `PASS` |
| Background ratio divergence | `PASS` |
| Quantifiers and per-member finiteness | `PASS` |
| `OPEN` boundary | `PASS` |
| `NOT CLAY` boundary | `PASS` |
| Separation from the 83/83 finite certificate | `PASS` |

**Overall analytic verdict:** `PASS`.
