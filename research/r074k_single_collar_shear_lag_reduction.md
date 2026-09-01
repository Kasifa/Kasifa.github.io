# R0.74K — the square-root-log frontier reduces to one inward collar

## Status and scope

R0.74J determines the complete payment of the exact R0.74F--H family, but
leaves matching upper bounds for both the weighted endpoint \(X_j\) and the
positive collar flux \(\mathfrak C_j\) open.  This note audits both routes
and freezes the smaller next problem.

The decisive finite result is that a free transverse Gaussian estimate has
enough exponent room in every inward shell except the nearest one.  In the
nearest inner shell \(A_{j-1}(R_j)\), it fails even after using the sharp
squared-kernel denominator \(132\), and it fails on a slab with a genuine
positive \(x_1\)-chord.  The missing mechanism must therefore retain the
joint dependence between inward Brownian bridges and the positive
differential shear displacement.  Existing Peetre reductions erase exactly
that dependence.

This is a **PROVED ROUTE REDUCTION**, not the missing analytic estimate.
The exact certificate returns **PASS** for the finite comparisons.  A
matching upper bound for \(X_j\) or \(\mathfrak C_j\) remains **OPEN**.
No singular solution is constructed and no possible singularity is
excluded.  **NOT CLAY.**

---

## 1. Frozen family and annular bookkeeping

Retain the exact constants

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \rho=\frac1{320},\qquad
 c_\gamma=\frac8{3969},
\tag{1.1}
\]

and set

\[
 L_j=\lambda2^j,\qquad
 R_j=e^{-\rho L_j^2},\qquad
 r_j=L_jR_j,\qquad
 h_j=c_hr_j.
\tag{1.2}
\]

The annular weights are

\[
 \Gamma_k=e^{-4^{k-1}/32},
 \qquad
 \Gamma_j=e^{-c_\gamma L_j^2},
\tag{1.3}
\]

and the frozen amplitude is

\[
 \mathfrak a_j=B_j\Gamma_j^{-1/2},
 \qquad
 \beta_j:=B_jR_j^2\longrightarrow\frac1{128}.
\tag{1.4}
\]

The exact solution is

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),\qquad p_j=0.
\tag{1.5}
\]

The inversion symmetry gives

\[
 X_{R_j}(t)=a_{R_j}(t)=a_{R_j}'(t)=0,
\tag{1.6}
\]

so Versions M and F coincide on this family.  Pressure, frame acceleration,
and the constant pressure gauge do not participate in the remaining
question.  The two velocity components are orthogonal in every quadratic
row.

For \(1\le m\le j-1\), the outer edge of the physical inward shell
\(A_{j-m}(R_j)\), in units of \(r_j\), is

\[
 a_m=\frac{2^{1-m}}\lambda,
\qquad
 d_m=c_h-a_m.
\tag{1.7}
\]

Its weight gain relative to the target shell is

\[
 \frac{\Gamma_{j-m}}{\Gamma_j}
 =\exp\!\left[G_mL_j^2\right],
 \qquad
 G_m=c_\gamma(1-4^{-m}).
\tag{1.8}
\]

---

## 2. The sharp free-tail exponent test

At heat age \(T\le66R_j^2\), the square of a transverse free heat kernel
at distance \(d_mL_jR_j\) supplies at best the exponential factor

\[
 \exp\!\left[-E_mL_j^2\right],
 \qquad
 E_m=\frac{d_m^2}{132}.
\tag{2.1}
\]

This is the optimistic denominator.  The coarser transverse-marginal
estimate inherited from R0.74G uses \(262\) instead of \(132\).

### Proposition 2.1 — all deeper inner shells have sharp exponent room

For all sufficiently large \(j\) and every physical shell index
\(2\le m\le j-1\),

\[
 \boxed{
 E_m-G_m
 \ge \frac{204385}{134120448}>0.}
\tag{2.2}
\]

**Proof.**  If \(m\ge2\), then

\[
 d_m\ge d_2=\frac{689}{1008},
 \qquad
 G_m<c_\gamma.
\tag{2.3}
\]

Therefore

\[
 E_m-G_m
 >\frac1{132}\left(\frac{689}{1008}\right)^2
   -\frac8{3969}
 =\frac{204385}{134120448}>0.
\tag{2.4}
\]

This proves the uniform comparison.  Algebraically the same inequality holds
for every integer \(m\ge2\); the upper cutoff \(m\le j-1\) only records that
the frozen annular ledger starts at shell index \(1\).  \(\square\)

The old denominator \(262\) already closes every \(m\ge3\).  Its worst
case is

\[
 \frac{d_3^2}{262}-G_3
 =\frac{139297}{266208768}>0.
\tag{2.5}
\]

At \(m=2\) the old constant misses by

\[
 \frac{d_2^2}{262}-G_2
 =-\frac{28319}{266208768}<0,
\tag{2.6}
\]

whereas the sharp squared-kernel exponent (2.2) has room.  Thus \(j-2\)
requires a sharper bridge bookkeeping lemma but no new exponent mechanism.

### Proposition 2.2 — the nearest inner shell fails on positive volume

Choose the fixed inward offset

\[
 \varepsilon=\frac1{128},\qquad
 x_3=\left(\lambda^{-1}-\varepsilon\right)r_j.
\tag{2.7}
\]

Then the distance from the positive packet centre is

\[
 d_{1,\varepsilon}
 =c_h-\lambda^{-1}+\varepsilon
 =\frac{3527}{8064},
\tag{2.8}
\]

and the available squared \(x_1\)-chord is strictly positive:

\[
 \lambda^{-2}
 -\left(\lambda^{-1}-\varepsilon\right)^2
 =\frac{8129}{1032192}>0.
\tag{2.9}
\]

Nevertheless,

\[
 \boxed{
 G_1-\frac{d_{1,\varepsilon}^2}{132}
 =\frac{536399}{8583708672}>0.}
\tag{2.10}
\]

**Proof.**  Equations (2.8)--(2.10) are exact rational reductions of
(1.1), (1.7), and (2.7).  To make the volume assertion explicit, put

\[
 \eta=\lambda^{-1}-\varepsilon=\frac{4033}{8064},
 \qquad \delta=\frac1{256},
 \qquad c_*=\frac1{64},
\tag{2.9a}
\]

and consider the box

\[
 \mathcal B_j=
 \left\{\eta r_j\le x_3\le(\eta+\delta)r_j,
 \quad |x_1|,|x_2|<c_*r_j\right\}.
\tag{2.9b}
\]

Its volume is \(4c_*^2\delta r_j^3=r_j^3/262144>0\).  Moreover,

\[
 \lambda^{-2}-(\eta+\delta)^2-2c_*^2
 =\frac{14305}{4128768}>0,
 \qquad
 \eta-\frac{16}{63}=\frac{1985}{8064}>0,
\tag{2.9c}
\]

so \(\mathcal B_j\subset A_{j-1}(R_j)\).  Throughout this one-sided
thickening, \(c_h-x_3/r_j\le d_{1,\varepsilon}\); hence the free squared-tail
decay is no stronger than at (2.7), and the wrong-sign margin is at least
(2.10).  Thus the obstruction occurs on genuine three-dimensional positive
volume, not merely on a boundary slice.  \(\square\)

Equation (2.10) says that a proof which replaces the true packet by a free
heat packet would leave a factor

\[
 \exp\!\left[
 \frac{536399}{8583708672}L_j^2
 \right]
\tag{2.11}
\]

in the wrong direction.  It is a no-go for that proof mechanism, not a
counterexample to the desired upper bound.  The true stochastic formula
contains the displacement

\[
 \mathfrak S_t^y
 =B_j\int_0^t
 [\theta_j(t-s,h_j)-\theta_j(t-s,h_j+Y_s^y)]\,ds.
\tag{2.12}
\]

For a typical inward bridge the displacement is positive and pushes the
packet in \(x_2\) away from the inner collar.  Proving that the exceptional
bridges are sufficiently rare is the new analytic task.

---

## 3. Why the existing bridge estimates stop here

R0.74F Lemmas 3.2--4.1 compare the positive packet with a free derivative
packet only for \(|y|\le R_j\).  Points in \(A_{j-1}(R_j)\) have
\(|y|\asymp L_jR_j\), so those lemmas do not apply.

R0.74G normalizes the stochastic representation by the periodic bridge
measure and proves

\[
 |G(t,z,y)|^p
 \le R_j^{3p}K_T(y)^p
 \mathbb E_{t,y}^{\rm br}
 |\partial K_T(z+\mathfrak S_t^y)|^p,
 \qquad p\in\{2,3\}.
\tag{3.1}
\]

Its one-sided bound

\[
 \mathfrak S_t^y\ge-\delta_j,
 \qquad \delta_j/R_j\to0,
\tag{3.2}
\]

is sufficient for the polynomial all-copy occupation rows.  It is not the
positive lower bound on \(\mathfrak S_t^y\) needed for an inward bridge.
The subsequent Peetre convolution separates \(y\) from
\(\mathfrak S_t^y\); doing so discards the correlation which must repair
(2.10).

### Lemma 3.1 — the main-collar chord has a uniform slice-BV bound

Let \(\psi_j^{R_j}\) be the frozen smooth cutoff for the target annulus and
define

\[
 M_j(x_2,x_3)
 =\int_{\mathbb R}
 |\partial_2\psi_j^{R_j}(x_1,x_2,x_3)|\,dx_1.
\tag{3.3}
\]

Then

\[
 \boxed{
 \sup_{x_3}\int_{\mathbb R}M_j(x_2,x_3)\,dx_2
 \le C L_jR_j.}
\tag{3.4}
\]

**Proof.**  The derivative is supported in the two padded radial collars of
\(A_j(R_j)\), whose radii are comparable to \(L_jR_j\), and the frozen
cutoff satisfies \(|\nabla\psi_j^{R_j}|\le C/R_j\).  At fixed \(x_3\), each
planar collar has area at most \(C(L_jR_j)R_j\).  Integrating the derivative
bound over the two collars proves (3.4).  This \(L^1_{x_2}\) estimate absorbs
the apparent square-root singularity of a pointwise chord bound near a
spherical tangent.  \(\square\)

The corresponding constant-shear reference packet is

\[
 F_{\rm fr}(t,x_2,x_3)
 =R_j^3\partial K_T(x_2-Q_j(t))K_T(x_3-h_j),
 \qquad T=R_j^2+t.
\tag{3.5}
\]

### Lemma 3.2 — the reference packet pays the main collar absolutely

For every \(\tau\in I_{R_j}\), uniformly in that upper endpoint,

\[
 \boxed{
 \Gamma_j\int_{I_{2R_j}\cap(-\infty,\tau]}\int_{\mathbb R^3}
 |F_{\rm fr}|^2
 |\partial_2\psi_j^{R_j}|\,dx\,dt
 \le C\Gamma_jL_jR_j^5.}
\tag{3.6}
\]

**Proof.**  It is enough to bound the full nonnegative integral over
\(I_{2R_j}\).  The inherited calibration gives \(Q_j'(t)\ge3B_j/4\) there.
Apply (3.4), change variables from \(t\) to \(Q_j(t)\),
and use the uniform periodic kernel moments

\[
 \int_{\mathbb T}\sup_{T/R_j^2\in[62,66]}K_T(y)^2\,dy\le CR_j^{-1},
 \quad
 \int_{\mathbb T}\sup_{T/R_j^2\in[62,66]}
 |\partial K_T(z)|^2\,dz\le CR_j^{-3}.
\tag{3.7}
\]

The resulting scale is

\[
 R_j^6\,R_j^{-1}\,R_j^{-3}
 \frac{L_jR_j}{B_j}
 =\frac{L_jR_j^3}{B_j}
 \le128L_jR_j^5,
\tag{3.8}
\]

where \(B_j^{-1}\le128R_j^2\) for all sufficiently large \(j\).  Multiply
by \(\Gamma_j\).  \(\square\)

Thus the main shell has no exponent obstruction and needs no signed
cancellation for the reference packet.  For the true packet, however, the
normalized bridge moves the chord to

\[
 M_j(Q_j(t)-\mathfrak S_t^y+u,h_j+y).
\tag{3.9}
\]

The current one-sided bound on \(\mathfrak S_t^y\) does not control the
time multiplicity with which \(Q_j(t)-\mathfrak S_t^y\) crosses one collar.
The exact forward identity \(dq_\omega=B_j\theta_j\,dt\) suggests a signed
pathwise BV argument, but that argument has not yet been proved under the
normalized bridge measure.  This is a technical correlation-preserving
lemma distinct from the genuinely adverse exponent at \(j-1\).

The exact audit therefore has the following boundary:

- the pure shear contribution is \(O(B_j^2R_j^2)\), below the target by
  \(L_j\);
- pressure, frame, acceleration, and velocity-component cross rows vanish
  or are absent on the exact family;
- outer shells are compatible with the super-Gaussian ratio
  \(\Gamma_{j+1}/\Gamma_j=e^{-3c_\gamma L_j^2}\), with
  \(3c_\gamma-\rho=1237/423360>0\) after one inverse-\(R_j\) loss;
- fixed inner shells are already controlled by the R0.74G buffered-core
  estimate;
- the coarse transverse estimate closes \(j-m\) for \(m\ge3\), and the
  sharp \(p=2\) exponent has room at \(j-2\);
- the true main-shell packet still needs a time-coupled bridge--BV estimate,
  although Lemma 3.2 proves the reference-packet scale; and
- only \(j-1\) has a wrong-sign exponent and therefore requires the
  qualitatively new shear-expulsion estimate.

The analytic implementation of the last three bullets is not replaced by
the finite certificate.  In particular, (2.2) is exponent compatibility,
not a weighted-gradient theorem.

---

## 4. Exact sufficient reduction for the collar flux

Let \(\vartheta_R^{\rm ann}\) be the frozen smooth annular weight from
R0.74H, and let \(\eta_R\) be its time cutoff.  On the exact family, the
Version-M and Version-F collar fluxes both reduce to

\[
 \mathfrak F_R(\tau)
 =\frac{\mathfrak a^2B}{2R}
 \int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}
 \theta(t,x_3)F(t,x_2,x_3)^2
 \partial_2\vartheta_R^{\rm ann}(x)\,dx\,dt.
\tag{4.1}
\]

Define the packet-only signed integral

\[
 \mathcal I_j(\tau)
 =\int_{s_{R_j}}^{\tau}\eta_{R_j}(t)
 \int_{\mathbb R^3}
 \theta_jF_j^2
 \partial_2\vartheta_{R_j}^{\rm ann}\,dx\,dt.
\tag{4.2}
\]

### Theorem 4.1 — the direct collar statement is sufficient

Assume that there is a constant \(C_I\), independent of \(j\), such that

\[
 \boxed{
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \le C_I\Gamma_jL_jR_j^5}
\tag{4.3}
\]

for all sufficiently large \(j\).  Then

\[
 \boxed{
 \mathfrak C_j
 \le C B_j^2L_jR_j^2.}
\tag{4.4}
\]

Together with the inherited R0.74H lower bound,

\[
 \boxed{
 \mathfrak C_j\asymp B_j^2L_jR_j^2.}
\tag{4.5}
\]

Consequently, on this exact family only,

\[
 \boxed{
 \mathfrak C_j
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.}
\tag{4.6}
\]

**Proof.**  Since \(\mathfrak a_j^2=B_j^2/\Gamma_j\), equations
(4.1)--(4.3) give

\[
 \mathfrak C_j
 \le \frac{B_j^3}{2R_j\Gamma_j}
 C_I\Gamma_jL_jR_j^5
 =\frac{C_I}{2}(B_jR_j^2)
 B_j^2L_jR_j^2.
\tag{4.7}
\]

The sequence \(B_jR_j^2=\beta_j\) is bounded, proving (4.4).  R0.74H
gives the reverse inequality in (4.5), and R0.74J equation (4.6) identifies
the right side with the square-root-log payment scale.  \(\square\)

Here “direct” refers to this observable-level route; (4.3) is a sufficient
condition, not a claim of logical necessity among all possible proofs.

The hypothesis (4.3) remains **OPEN**.  It is deliberately signed and
packet-only: this avoids importing the full weighted gradient estimate
needed for an \(X_j\) upper bound.  A proof along the selected normalized-
bridge route must include all periodic windings, a time-coupled bridge--BV
estimate for the main collar, and a positive shear-expulsion estimate for the
nearest inward collar.  That route must not replace \(\mathfrak S_t^y\) by
an independent or worst-case shift.

---

## 5. Primary-source boundary

The bounded literature pass is recorded in detail in
`research/r074k_primary_literature_boundary.md`.  Its conclusion is narrow.
Hypocoercivity, resolvent, Malliavin, Girsanov, and stochastic
integration-by-parts methods already establish strong mixing or enhanced
dissipation statements for broad classes of passive scalars in shear
flows.  They justify treating the shear--diffusion interaction as a real
mechanism rather than a heuristic.

They do not directly supply (4.3).  The present shear is time-dependent,
depends on \(R_j\), is exponentially flat on the relevant plateau, and is
tested over a finite calibrated window against a signed smooth radial
collar.  The literature results reviewed here concern global or
streamline-local decay/mixing norms for autonomous or differently
normalized shears.  A finite non-hit in this bounded review is not a
novelty or priority claim.

---

## 6. What is proved and what remains open

### Proved here

1. The optimistic free squared-Gaussian exponent closes every physical inward
   shell \(j-m\) with \(2\le m\le j-1\), with the uniform exact margin (2.2).
2. The older denominator \(262\) already closes \(m\ge3\), while \(m=2\)
   needs the sharper \(p=2\) bookkeeping.
3. The nearest inner shell has the strict positive-volume wrong-sign margin
   (2.10); a free-heat replacement cannot close the target scale.
4. The direct packet collar estimate (4.3) is exactly sufficient for a
   matching familywise \(\mathfrak C_j\) upper and hence for square-root-log
   saturation of that observable.
5. The target main-collar scale is proved for the constant-shear reference
   packet by the slice-BV estimate (3.4)--(3.8).
6. The selected normalized-bridge route for the missing true-packet estimates
   must preserve bridge/shear-lag correlation.

### Open after this section

1. the conditional signed collar estimate (4.3), including the distinct
   main-collar bridge--BV and nearest-inner shear-expulsion sublemmas;
2. the matching familywise upper bound for \(\mathfrak C_j\);
3. the stronger weighted kinetic-and-dissipation lemma needed for a
   matching upper bound for \(X_j\);
4. a universal square-root-log endpoint inequality;
5. payment-to-admissibility or prescribed-point core-from-shell control;
6. global regularity or singularity formation for arbitrary three-dimensional
   Navier--Stokes data; and
7. novelty or priority.

The next nonredundant task is to prove or refute (4.3) by a normalized
periodic-bridge decomposition: first retain the signed forward
\(dq_\omega=B_j\theta_jdt\) BV structure on the main collar, then separate
typical positive shear-lag paths from exceptional fast-return paths in the
nearest inward collar without losing their correlation.
**NOT CLAY.**
