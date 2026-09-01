# R0.74B — independent analytic audit

**Audit date:** 2026-09-01

**Audited source:** `research/r074b_buffered_tail_closure.md`

**Audited source SHA256:**
`bec0a239b3c5d145238c9f06c734661f2e85e8cb339f594e8350c4c111bc87ab`

**Audit mode:** independent equation-by-equation reconstruction

**Verdict:** `R074B_INDEPENDENT_AUDIT_PASS`

This audit checks the analytic proof at the displayed source hash.  It does
not silently extend its verdict to a later revision.  The current source
passes the stated buffered size-closure gate.  The result remains a
positive-scale upper estimate, not an absorption theorem or a regularity
criterion.

---

## 1. Periodized torus test — `PASS`

For each lifted compact cutoff \(\psi_m\), the source defines

\[
 \Phi_m(x)=\sum_{n\in\mathbb Z^3}
 \psi_m(\widetilde x+2\pi n).
\]

The sum is finite at every point because \(\psi_m\) has compact support.  A
change of lift reindexes the lattice sum, so \(\Phi_m\) is a well-defined,
smooth, nonnegative periodic function.  It is therefore an admissible
spatial factor in the suitable local energy inequality.

For every periodic integrable \(F\), unfolding gives

\[
 \int_{\mathbb T^3}F\Phi_m
 =\int_{\mathbb R^3}\widetilde F\psi_m,
\]

and the same identity holds with first or second derivatives on the cutoff.
Consequently, the torus local energy inequality controls exactly the lifted
annular integrals used in \(\mathcal U_{\rm ext}^{\infty,\square}\) and
\(\mathcal D_{\rm ext}^{\square}\).  No nonperiodic test is inserted into a
torus inequality.

The Euclidean support volume is
\(O(2^{3m}R^3)\).  This is the correct periodic-lift cell count, and

\[
 \sup_{0<\theta\le1}
 \sum_{m\ge1}2^{3m}\gamma_m(\theta)<\infty
\]

absorbs it.  The source supplies a valid uniform proof: the first three
terms have finite suprema, while the remaining terms are dominated by a
geometric series at \(\theta=1\).

---

## 2. Finite-shell limit — `PASS`

The local energy inequality is first applied shell by shell and summed only
over \(1\le m\le M\).  After the flux is replaced by its nonnegative
majorant, every right-hand-side row is nonnegative.  Fatou and monotone
convergence then license \(M\to\infty\).  The proof does not use an infinite
sum of test functions as one local-energy test.

For the endpoint row,

\[
 \operatorname*{ess\,sup}_t
 \sum_m\gamma_m E_m(t)
 \le \sum_m\gamma_m
 \operatorname*{ess\,sup}_tE_m(t),
\]

so the sum of the single-shell inequalities dominates the required
essential supremum of the Gaussian annular energy.

---

## 3. First two shells and the \(m=2\) core exception — `PASS`

The exact doubled-radius identity is

\[
 A_k(R)=A_{k-1}(2R),\qquad k\ge2.
\]

For \(m\ge3\), the target shell and its two neighboring support shells map
to the \((m-2)\)-nd through \(m\)-th annuli at radius \(2R\), whose weights
are at least as large as the target weight.  This proves the shifted
annular majorization without the false comparison
\(\gamma_m\lesssim\gamma_{m+1}\).

The source now treats both \(m=1\) and \(m=2\) separately.  Their inner
cutoff collars lie in \(B_{4R}\), while their exterior portions lie in the
first two \(2R\)-annuli.  Thus the core leakage of \(\psi_2\) is not omitted.
Moreover,

\[
 \sup_{0<\theta\le1}
 [\gamma_1(\theta)+\gamma_2(\theta)]<\infty,
\]

so both core weights are absorbed by one uniform constant.  The local
velocity row is paid on \(B_{8R}\), and the pressure core uses the matching
radius-\(2R\) local/harmonic split on \(B_{4R}\).

---

## 4. Standard and viscosity-adapted clocks — `PASS`

Put

\[
 \kappa_{\rm std}=1,\qquad \kappa_\nu=\nu,
 \qquad
 I_\rho^\square=(t_0-\rho^2/\kappa_\square,t_0).
\]

The cutoff from \(I_{2R}^\square\) to \(I_R^\square\) has

\[
 |\partial_t\chi^\square|
 \le C\kappa_\square R^{-2}.
\]

After multiplication by \(\gamma_m/R\), the time and Laplacian rows have
the explicit combined coefficient

\[
 C(\kappa_\square+\nu)R^{-3}S_2.
\]

Since \(|I_{2R}^\square|=4R^2/\kappa_\square\), weighted Holder gives

\[
 R^{-3}S_2
 \le C\kappa_\square^{-1/3}
 (R^{-2}S_3)^{2/3}.
\]

The resulting clock coefficient is therefore

\[
 (\kappa_\square+\nu)\kappa_\square^{-1/3}
 =\begin{cases}
 1+\nu,&\square={\rm std},\\
 2\nu^{2/3},&\square=\nu.
 \end{cases}
\]

The two clocks are not interchanged, and every power of \(R\) is
dimensionally correct.  The cubic/pressure cutoff row has normalization
\(R^{-2}S_3\).

---

## 5. Composition of the \(P\)-theorem — `PASS`

Let

\[
 P^\square=
 [\mathcal E^\square(z_0,8R)]^{3/2}
 +\mathcal A_{\rm ext}^\square(z_0,2R;\theta).
\]

The core pressure estimate, the shifted exterior annuli, and the harmonic
payment prove

\[
 R^{-2}S_3\le C_{\nu,\square}P^\square.
\]

The preceding weighted Holder row then gives the quadratic payment
\(C(P^\square)^{2/3}\), while the direct convection/pressure flux gives
\(CP^\square\).  Hence

\[
 \mathcal U_{\rm ext}^{\infty,\square}
 +\mathcal D_{\rm ext}^{\square}
 \le C_{\nu,\square}
 [(P^\square)^{2/3}+P^\square].
\]

Also,

\[
 \mathcal E^\square(z_0,4R)
 \le C\mathcal E^\square(z_0,8R)
 \le C(P^\square)^{2/3}.
\]

Substitution in the R0.74A four-block estimate yields

\[
 \mathcal K_D^\square
 \le C_{\nu,\square}\theta^{1/4}
 [P^\square+(P^\square)^{3/2}].
\]

For \(P^\square\le1\), this reduces to
\(\mathcal K_D^\square\le C\theta^{1/4}P^\square\).  The source correctly
keeps removal of the \(+P\) row for arbitrary large payment open.

---

## 6. Lemma 4.2: pressure and gauge transfer — `PASS`

### 6.1 Algebraic harmonic row

The definition of \(\Lambda_R\) gives the exact split

\[
 \Lambda_R(t)
 =\frac1{16R^3}\int_{A_1(R)}|\widetilde u(t)|^2
 +\frac12\Lambda_{2R}(t).
\]

The source writes the harmless weaker sign \(\le\).  Raising to \(3/2\),
integrating over \(I_R^\square\), and using the local-energy supremum at
radius \(8R\) proves

\[
 \mathcal H_u^\square(R)
 \le C_{\nu,\square}
 \left([\mathcal E^\square(8R)]^{3/2}
 +\mathcal H_u^\square(2R)\right).
\]

### 6.2 Gaussian velocity row

The first \(R\)-annulus lies in \(B_{4R}\) and is paid by the local cubic
row.  For \(m\ge2\), use
\(A_m(R)=A_{m-1}(2R)\),
\(I_R^\square\subset I_{2R}^\square\), and
\(\gamma_m\le\gamma_{m-1}\).  After accounting for the factor four between
\(R^{-2}\) and \((2R)^{-2}\), this proves

\[
 \mathcal G_u^\square(R)
 \le C_{\nu,\square}
 \left([\mathcal E^\square(8R)]^{3/2}
 +\mathcal G_u^\square(2R)\right).
\]

### 6.3 Gauge difference and Gaussian pressure row

The two pressure gauges are not identified.  From the frozen pressure
splits,

\[
 c_R-c_{2R}
 =(p-c_{2R})_{B_{2R}}-(p_R^{\rm loc})_{B_{2R}}.
\]

Jensen turns the averages into \(R^{-3}\) local integrals.  The
radius-\(2R\) local/harmonic pressure split pays \(p-c_{2R}\) on
\(B_{4R}\), and Calderon--Zygmund pays \(p_R^{\rm loc}\) from the local
velocity cubic row.  Therefore

\[
 R\int_{I_R^\square}|c_R-c_{2R}|^{3/2}
 \le C_{\nu,\square}
 \left([\mathcal E^\square(8R)]^{3/2}
 +\mathcal H_u^\square(2R)\right).
\]

The weighted lifted volume satisfies

\[
 \sum_m\gamma_m|A_m(R)|\le CR^3.
\]

Multiplying the gauge-difference estimate by this volume and the
normalization \(R^{-2}\) produces exactly the preceding factor
\(R\int|c_R-c_{2R}|^{3/2}\).  Treating the first pressure annulus as a core
row and shifting all remaining annuli gives

\[
 \mathcal G_p^\square(R)
 \le C_{\nu,\square}
 \left([\mathcal E^\square(8R)]^{3/2}
 +\mathcal G_p^\square(2R)
 +\mathcal H_u^\square(2R)\right).
\]

The three rows together prove

\[
 \mathcal A_{\rm ext}^\square(R;\theta)
 \le C_{\nu,\square}P^\square.
\]

---

## 7. Corollary 4.3 — `PASS`

R0.74A (4.17) has the right-hand side

\[
 C\left\{
 [\mathcal E^\square(4R)
 +\mathcal U_{\rm ext}^{\infty,\square}(R)
 +\mathcal D_{\rm ext}^\square(R)]^{3/2}
 +\mathcal A_{\rm ext}^\square(R)\right\}.
\]

Theorem 4.1 pays the bracket by
\(C[P^\square+(P^\square)^{3/2}]\), and Lemma 4.2 pays the last term by
\(CP^\square\).  The measurable-scale and cutoff quantifiers match those
of R0.74A.  Thus the combined pressure interface (4.14) follows exactly.
It is \(O(P^\square)\) when \(P^\square\le1\), but this is still only a
size statement.

---

## 8. Optional sharper \(\eta\) reserve — `PASS`

For

\[
 \eta_m(\theta)=\theta^{-2}
 e^{-4^{m-1}/(6\theta)},
\]

put \(a=4^{m-1}\), \(r=R^2/s\), \(q=r\theta\), and
\(X=aq/\theta\).  Annular geometry gives
\(a^{1/2}\le d\le6a^{1/2}\).  Since

\[
 q/4-1/6\ge q/12,
\]

division by \(\eta_m\) leaves at most a fixed polynomial in \(X\) times
\(e^{-X/12}\).  This absorbs the heat prefactor, the gradient factor
\(d\), \(r^{5/2}\), and the remaining \(\theta^{-1/2}\) uniformly.
Therefore

\[
 R^3g_s+R^4|\nabla g_s|\le C\eta_m.
\]

Moreover,

\[
 \frac{\eta_m}{\gamma_{m+1}}
 =e^{-4^{m-1}/(24\theta)},
\]

so the exponential reserve absorbs every fixed power of \(1+2^m\).  This
derivation correctly uses the exact Gaussian exponent \(1/4\), not the
coarsened derivative exponent \(1/8\).

---

## 9. Exact dissipating shear boundary — `PASS`

For fixed nonzero \(A\), fixed \(R,\theta,\nu\), and a fixed positive time
window beginning at \(t_-\), the exact shear

\[
 u_N=Ae^{-\nu N^2(t-t_-)}\sin(Nx_2)e_1,
 \qquad p_N=0,
\]

is a smooth periodic NSE solution.  As integer \(N\to\infty\), weighted
Riemann--Lebesgue and the integrability of the Gaussian and algebraic
annular weights give

\[
 \mathcal U_{\rm ext}^{\infty}\asymp A^2,
 \qquad \mathcal D_{\rm ext}\asymp A^2,
\]

whereas the cubic time integral has heat-decay length \(O(N^{-2})\), so

\[
 \mathcal G_{u,p}+\mathcal H_u=O(A^3N^{-2}).
\]

This proves only that a same-window integrated cubic payment alone cannot
control the quadratic endpoint uniformly in frequency.  It does not exclude
a same-window estimate containing an initial annular \(L^2\) row, local
energy, or another quadratic payment, and it does not prove that every
possible closure must use a buffer.

---

## 10. Certificate boundary

An executable certificate may verify finite algebra, frozen constants,
payload integrity, hashes, or displayed scaling identities.  It cannot
replace any of the analytic arguments audited here: admissibility of the
periodized suitable test, the finite-shell limiting argument, weighted
Holder, Calderon--Zygmund pressure control, harmonic pressure transfer,
gauge comparison, or the quantified exact-shear proof.  The present verdict
is analytic and is not inferred from a certificate status.

---

## 11. Claim ledger

### `PROVED`

1. The original \(\gamma\)-weighted tails at radius \(R\) are controlled by
   the canonical doubled-radius payment.
2. The periodized suitable test, finite-shell limit, first-two-shell core
   rows, and both physical clocks are complete.
3. The tail closure (4.2), mixed-observable bound (4.4), pressure transfer
   (4.6), and combined pressure interface (4.14) follow.
4. The optional sharper-\(\eta\) kernel reserve is valid.
5. The exact shear proves the declared cubic-only same-window no-go.

### `FINITE`

At each fixed positive scale, all displayed tails and payments are finite
under the stated suitable-weak assumptions.  Finiteness is not smallness or
absorption.

### `OPEN`

1. Removal of \(+P\) for arbitrary large payment.
2. Absorption or scale-uniform smallness of \(P\).
3. Weak stability and lower semicontinuity of the selected tails.
4. A lower bound after quotienting the precise first-jet near-kernel.
5. Any epsilon-regularity or regularity consequence.

### `NOT CLAY`

Nothing in R0.74B proves epsilon regularity, smoothness, or global regularity
for three-dimensional Navier--Stokes solutions.

**Final gate:** `R074B_INDEPENDENT_AUDIT_PASS`
