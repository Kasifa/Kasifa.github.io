# R0.74Q — signed effective shells and the multi-packet stress test

## 0. Status and decision

R0.74P leaves the fixed-scale inequality

\[
 \mathfrak C_R^M
 \stackrel{?}{\le}
 C\left[(P_R^M)^{2/3}+Y_{2,R}^{\rm sf}\right]
\tag{Q.1}
\]

open.  A direct replacement of the shellwise \(\ell^1\) clock by its
\(\ell^2\) square function is false for abstract nonnegative sequences.
I treat the next step as a decision problem rather than another choice of
observable:

1. determine the weakest signed effective-shell statement that would imply
   (Q.1);
2. test that statement against an exact solution with many passive packets;
3. if the exact construction fails for a quantitative reason, isolate that
   reason as the missing PDE packing mechanism.

I will run the exact-family stress test first.  Frequency localization,
defect-measure coercivity, and path-length estimates are not being assumed.
This freeze does not prove or disprove (Q.1).  It does not prove regularity or
singularity formation.  **NOT CLAY.**

## 1. Inherited fixed-scale ledger

Fix the R0.74P Version-M setting.  Write

\[
 A_R:=(P_R^M)^{2/3},
 \qquad
 Z_R:=Y_{2,R}^{\rm sf}
      =\left(\sum_{k\ge1}v_{k,R}^2\right)^{1/2}.
\tag{Q.2}
\]

For each shell,

\[
 K_{k,R}=Q_{k,R}+F_{k,R},
 \qquad
 Q_{k,R}(s_R)=F_{k,R}(s_R)=K_{k,R}(s_R)=0,
 \qquad
 K_{k,R}\ge0,
 \qquad
 K_{k,R}(\tau)\le v_{k,R},
\tag{Q.3}
\]

where \(v_{k,R}=\operatorname{Var}^+_{[s_R,t_0)}K_{k,R}\).  R0.74P proves

\[
 \sum_{k\ge1}\operatorname{TV}Q_{k,R}\le C A_R
\tag{Q.4}
\]

and the absolutely convergent balance

\[
 \mathfrak F_R^M(\tau)
 =\sum_{k\ge1}F_{k,R}(\tau)
 =\sum_{k\ge1}K_{k,R}(\tau)
  -\sum_{k\ge1}Q_{k,R}(\tau).
\tag{Q.5}
\]

Only the positive cumulative supremum

\[
 \mathfrak C_R^M
 :=\sup_{\tau<t_0}[\mathfrak F_R^M(\tau)]_+
\tag{Q.6}
\]

must be controlled.  It is not necessary to prove an upper bound for the
full positive-variation sum \(\sum_kv_{k,R}\).

## 2. Exact terminal reduction

For an absolutely summable real shell vector \(x=(x_k)\) and an integer
\(N\ge0\), define its positive residual after removing at most \(N\)
coordinates by

\[
 \mathcal S_N(x)
 :=\inf_{S\subset\mathbb N,\ \#S\le N}
   \left[\sum_{k\notin S}x_k\right]_+.
\tag{Q.7}
\]

For the clock and flux ledgers put

\[
 \mathcal S_{N,R}^{K}
 :=\sup_{\tau<t_0}\mathcal S_N((K_{k,R}(\tau))_k),
 \qquad
 \mathcal S_{N,R}^{F}
 :=\sup_{\tau<t_0}\mathcal S_N((F_{k,R}(\tau))_k).
\tag{Q.8}
\]

### Proposition 2.1 — terminal effective-shell reduction

For every fixed integer \(N\ge0\),

\[
 \boxed{
 \mathfrak C_R^M
 \le C A_R+\sqrt N\,Z_R+\mathcal S_{N,R}^{K}.}
\tag{Q.9}
\]

The same conclusion holds with \(\mathcal S_{N,R}^{F}\) in place of
\(\mathcal S_{N,R}^{K}\), after changing the absolute constant in front of
\(A_R\).

**Proof.**  Fix \(\tau<t_0\) and a set \(S\) with \(\#S\le N\).  Equations
(Q.3)--(Q.5) give

\[
\begin{aligned}
 \mathfrak F_R^M(\tau)
 &\le \sum_{k\in S}K_{k,R}(\tau)
   +\sum_{k\notin S}K_{k,R}(\tau)
   +\sum_k\operatorname{TV}Q_{k,R}\\
 &\le \sum_{k\in S}v_{k,R}
   +\left[\sum_{k\notin S}K_{k,R}(\tau)\right]_+
   +C A_R\\
 &\le \sqrt N\,Z_R
   +\left[\sum_{k\notin S}K_{k,R}(\tau)\right]_+
   +C A_R.
\end{aligned}
\tag{Q.10}
\]

Take the infimum in \(S\), then the supremum in \(\tau\).  For the
flux version, use

\[
 F_{k,R}(\tau)
 \le v_{k,R}+\operatorname{TV}Q_{k,R}
\tag{Q.11}
\]

on the exceptional set and sum (Q.4).  \(\square\)

Consequently, either one of the uniform estimates

\[
 \boxed{
 \mathcal S_{N_0,R}^{K}\le C A_R}
 \qquad\hbox{or}\qquad
 \boxed{
 \mathcal S_{N_0,R}^{F}\le C A_R}
\tag{Q.12}
\]

with \(N_0\) independent of \(R\) and the solution would prove (Q.1).
The exceptional set may depend on the terminal time \(\tau\).  This is
strictly weaker than requiring only \(N_0\) clocks to have nonzero positive
variation.  Because \(K_{k,R}\ge0\), the \(K\)-version is a terminal
best-\(N\) tail and does not use cancellation between shells.  The
\(F\)-version is the genuinely signed alternative.

## 3. A stronger sequence-space route

Let \(v^*=(v_m^*)_{m\ge1}\) be the nonincreasing rearrangement of a
nonnegative \(v\in\ell^1\), and define the best-\(N\)-term \(\ell^1\) tail

\[
 \sigma_N(v)_1
 :=\inf_{\#S\le N}\sum_{k\notin S}v_k
 =\sum_{m>N}v_m^*.
\tag{Q.13}
\]

Then

\[
 \|v\|_1
 \le\sqrt N\,\|v\|_2+\sigma_N(v)_1.
\tag{Q.14}
\]

Moreover,

\[
 \sigma_N(v)_1
 =\int_0^\infty
   \bigl(\#\{k:v_k>\lambda\}-N\bigr)_+\,d\lambda.
\tag{Q.15}
\]

Thus the stronger candidate

\[
 \boxed{
 \sigma_{N_0}((v_{k,R})_k)_1\le C A_R}
\tag{Q.16}
\]

would imply (Q.12) and (Q.1).  Equation (Q.15) shows why a count at one
chosen amplitude is insufficient: the required packing is integrated over
all amplitudes.

The sequence route has a sharp obstruction.  For

\[
 v_k^{(M,L)}=M^{-1}\mathbf1_{\{L<k\le L+M\}},
\tag{Q.17}
\]

one has

\[
 \|v^{(M,L)}\|_1=1,
 \qquad
 \|v^{(M,L)}\|_2=M^{-1/2}.
\tag{Q.18}
\]

The shift \(L\) is arbitrary.  Finite-prefix control, monotonicity, one
connected shell block, unimodality, log-concavity, bounded tree width, or
qualitative membership in every \(\ell^p\) therefore does not supply a
uniform compression constant.

For a class of nonzero nonnegative sequences, the pure estimate
\(\|v\|_1\le C\|v\|_2\) is equivalent to a uniformly bounded inverse
participation number

\[
 N_{\rm eff}(v)
 :=\frac{\|v\|_1^2}{\|v\|_2^2}.
\tag{Q.19}
\]

It is also equivalent, up to constants, to a uniformly finite set of
coordinates capturing a fixed positive fraction of \(\|v\|_1\).  This is
the precise sequence meaning of an effective-shell theorem.  It is not a
consequence of the weight summability \(\sum_k\gamma_k<\infty\), because
the weight is already inside \(v_{k,R}\).

## 4. The local-payment form to seek

A direct PDE proof of (Q.12) could use nonnegative shell payments \(p_{k,R}\)
and quadratic errors \(q_{k,R}\) satisfying

\[
 \sum_kp_{k,R}\le C P_R^M,
 \qquad
 \sum_kq_{k,R}\le C A_R.
\tag{Q.20}
\]

The operational target is: for every \(\tau<t_0\), find
\(S_\tau\) with \(\#S_\tau\le N_0\) and coefficients
\(a_{k,R,\tau}\ge0\) such that, for \(k\notin S_\tau\),

\[
 K_{k,R}(\tau)
 \le q_{k,R}+a_{k,R,\tau}p_{k,R}^{2/3},
 \qquad
 \sum_{k\notin S_\tau}a_{k,R,\tau}^3\le C.
\tag{Q.21}
\]

Hölder's inequality gives

\[
 \sum_{k\notin S_\tau}a_{k,R,\tau}p_{k,R}^{2/3}
 \le
 \left(\sum_{k\notin S_\tau}a_{k,R,\tau}^3\right)^{1/3}
 \left(\sum_kp_{k,R}\right)^{2/3}
 \le C A_R.
\tag{Q.22}
\]

Hence (Q.21) implies (Q.12).  This formulation allows many residual shells;
it asks only for a Hölder-compatible \(\ell^3\) coefficient packing after
finitely many terminal exceptions.

## 5. Multi-packet exact-family stress test

Before attempting (Q.21) for arbitrary suitable weak solutions, test it on
the smooth pressure-free class underlying R0.74F--O.  The proposed ansatz is

\[
 u^{(N)}
 =\left(\sum_{\ell=1}^N\mathfrak a_\ell G_\ell,
          B\theta,0\right),
 \qquad p^{(N)}=0.
\tag{Q.23}
\]

The intended common-shear equations are

\[
 \partial_t\theta=\partial_3^2\theta,
 \qquad
 (\partial_t+B\theta\partial_2-\Delta_{23})G_\ell=0,
 \qquad 1\le\ell\le N.
\tag{Q.23a}
\]

The first component is passive and (Q.23a) is linear once the common shear
\(B\theta\) is fixed.  Exact superposition is therefore available at the PDE
level for packets satisfying the same equation; packages with different old
shear parameters cannot simply be added.  This does not make the quadratic
flux, cubic payment, moving energy, or clock ledgers additive; those cross
terms are the substance of the test.

The target configuration would use distinct shells \(k_1,\ldots,k_N\) and
one terminal time \(\tau_N\) with

\[
 K_{k_\ell,R}^{(N)}(\tau_N)\ge cT,
 \qquad 1\le\ell\le N,
\tag{Q.24}
\]

while proving the all-shell bounds

\[
 \mathfrak C_R^{M,(N)}\ge cNT,
 \qquad
 Y_{2,R}^{\rm sf,(N)}\le C\sqrt N\,T,
\tag{Q.25}
\]

and a payment estimate

\[
 P_R^{M,(N)}
 \le C T^{3/2}\sum_{\ell=1}^N\Lambda_\ell
 \quad\Longrightarrow\quad
 (P_R^{M,(N)})^{2/3}
 \le CT\left(\sum_{\ell=1}^N\Lambda_\ell\right)^{2/3}.
\tag{Q.26}
\]

If

\[
 \sum_{\ell=1}^N\Lambda_\ell=o(N^{3/2}),
\tag{Q.27}
\]

then the right side of (Q.1) is \(o(NT)\), whereas its left side is
comparable to \(NT\).  This would disprove (Q.1) on smooth exact solutions.
The especially natural case \(\Lambda_\ell\le C\) gives a payment term of
order \(N^{2/3}T\).

The construction is not complete.  It must pass six nonformal gates:

1. the common-shear superposition must satisfy the exact periodic NSE,
   divergence, parity, pressure-zero, and Version-M mollified-path identities
   with constants uniform in \(N\); periodic copies must not introduce an
   unrecorded interaction;
2. one common shear must place all terminal lobes in their assigned physical
   shells at the same terminal time, while every amplitude factor
   \(\gamma_{k_\ell}^{-1/2}\) retains the heat reserve needed by its packet;
3. diagonal and off-diagonal quadratic flux and cubic terms must be separated
   exactly or paid with the constants in (Q.25)--(Q.27);
4. the lower bound for \(\mathfrak C_R^{M,(N)}\) must pass from the positive
   terminal \(K\)-contributions to the signed full flux \(F=K-Q\), with the
   entire \(Q\) ledger paid by \(A_R\);
5. every target and off-target shell must enter the positive-variation sum,
   and the complete all-shell calculation must prove the upper bound for
   \(Y_{2,R}^{\rm sf,(N)}\) in (Q.25);
6. the full Version-M payment, including the background shear, central moving
   energy, pressure ledger, and exterior rows, must satisfy (Q.26).  In
   particular, no central term of order \(N^{3/2}T^{3/2}\) may invalidate
   (Q.27).

Success closes the matched-square-function route negatively.  A failure is
useful only if it yields a uniform quantitative obstruction; that obstruction
should then be stated as an estimate of the form (Q.21).  A merely technical
failure does not prove packing.

## 6. Mechanism triage

I will use the following order for the next calculations.

### 6.1 Retain

- **Signed adjacent-shell balance.**  Nested cutoffs and discrete Abel
  summation may cancel internal faces before positive variation is taken.
  The target is (Q.12), not a rowwise absolute estimate.
- **Local/harmonic pressure splitting.**  A shell matrix with off-diagonal
  decay could show that pressure does not create a new nonlocal tail.  It
  cannot supply coercivity by itself, since the exact family has \(p=0\).
- **BV stopping-time forests.**  These may organize terminal upcrossings and
  charge residual branches through (Q.21).  BV is the language of the
  argument, not the packing mechanism.

### 6.2 Reject as standalone arguments

- **Instantaneous active-derivative count.**  Clocks may rise on disjoint
  time intervals and retain all earlier increments.  One active derivative
  at each time can still leave \(N\) terminal clocks of size one.
- **Pure Littlewood--Paley localization.**  The index \(k\) here labels
  physical radial shells, not frequency shells.  A single frequency band
  can occupy many physical shells.
- **Anomalous defect coercivity.**  The smooth exact family has zero anomaly,
  and the weak direction found in R0.74P is unsuitable for an upper bound.
- **Path length alone.**  Bare suitability does not control the required
  \(L_t^1L_x^\infty\) relative-motion budget; pressure and viscosity also
  prevent a pure material-crossing count.

## 7. Primary-literature boundary

A bounded primary-source screen through 2026-09-02 found adjacent tools but
not the exact prescribed-terminal-centre, mollified-trajectory physical-shell
clock packing statement (Q.12).  This is a bounded non-hit, not a novelty or
priority claim.

- Yu's first 2026 preprint proves a finite-scale supply--tax alternative on
  admissible parabolic-window chains; it is not a global regularity theorem:
  [arXiv:2606.13887](https://arxiv.org/abs/2606.13887).
- Yu's second 2026 preprint studies recursive propagation after one-step
  admissibility has produced a finite renormalized chain and a static
  finite-window audit certificate is available at every scale:
  [arXiv:2606.20899](https://arxiv.org/abs/2606.20899).
- Cheskidov and Peng assign a global Fourier determining wavenumber to each
  weak solution; its determining consequence compares two solutions and its
  quantitative controls are long-time rather than prescribed-terminal-centre,
  mollified-trajectory shell-clock estimates:
  [arXiv:2407.06474](https://arxiv.org/abs/2407.06474) and
  [NoDEA 2026](https://doi.org/10.1007/s00030-026-01232-0).
- Dascaliuc and Grujic prove ensemble/time-averaged physical-space cascade
  results using optimal covers; their packing is bounded cover multiplicity,
  not a bound on active clocks at one prescribed centre:
  [arXiv:1101.2193](https://arxiv.org/abs/1101.2193) and
  [CMP 2011](https://doi.org/10.1007/s00220-011-1219-8).
- Bradshaw and Grujic reduce a conditional regularity test to a finite moving
  frequency window; the hypotheses do not produce effective shells from the
  suitable-weak energy class:
  [arXiv:1501.01043](https://arxiv.org/abs/1501.01043) and
  [ARMA 2017](https://doi.org/10.1007/s00205-016-1069-9).
- Tao's frequency bubbles and regularity epochs assume a critical
  \(L_t^\infty L_x^3\) bound and use solution-chosen centres:
  [arXiv:1908.04958](https://arxiv.org/abs/1908.04958).
- Koch and Tataru's parabolic Carleson/tent structure is part of a critical
  small-data theory in \(BMO^{-1}\), not a reverse packing theorem for an
  arbitrary suitable weak solution:
  [Advances in Mathematics 2001](https://doi.org/10.1006/aima.2000.1937).
- Cheskidov and Eguchi obtain global regularity from a frequency-localized
  smallness condition on the initial data; this does not generate shell-clock
  sparsity from the energy class:
  [arXiv:2503.11642](https://arxiv.org/abs/2503.11642).
- Albritton and Bradshaw use frequency or physical-space sparsity as a
  continuation hypothesis, rather than proving such sparsity from bare
  suitability:
  [arXiv:2110.02187](https://arxiv.org/abs/2110.02187) and
  [Nonlinearity 2022](https://doi.org/10.1088/1361-6544/ac62de).
- Caffarelli--Kohn--Nirenberg and Lin provide the suitable-weak partial
  regularity and epsilon-regularity framework; their bad-cylinder covering is
  not (Q.12):
  [CKN 1982](https://doi.org/10.1002/cpa.3160350604) and
  [Lin 1998](https://doi.org/10.1002/(SICI)1097-0312(199803)51:3%3C241::AID-CPA2%3E3.0.CO;2-A).
- Lei and Ren obtain solution-chosen spatial regular intervals and
  quantitative regularity epochs, not a shrinking scale sequence through a
  prescribed terminal centre:
  [arXiv:2210.01783](https://arxiv.org/abs/2210.01783) and
  [Advances in Mathematics 2024](https://doi.org/10.1016/j.aim.2024.109654).
- Wolf's local pressure projection supplies a local/harmonic pressure
  framework, not an active-shell count:
  [arXiv:1611.01482](https://arxiv.org/abs/1611.01482).

The safe boundary is: existing determining-wavenumber, finite-frequency,
Carleson-smallness, physical-cascade, sparsity, and partial-regularity results
do not directly provide the prescribed-terminal-centre suitable-weak
shell-clock estimate required by (Q.12).

## 8. Falsification gates

Every proposed R0.74Q estimate must pass all of the following.

1. **Plateau:** the shifted block (Q.17), which defeats qualitative sparsity.
2. **Weak-\(\ell^1\) endpoint:** truncated \(v_k=1/k\), whose \(\ell^1\)
   norm grows logarithmically while its \(\ell^2\) norm stays bounded.
3. **Tree:** square Carleson packing plus bounded branching at the critical
   child-decay threshold, which still allows the \(\ell^1\) mass to grow.
4. **Sequential activation:** one increasing clock at a time, with all
   increments retained at the terminal time.
5. **Exact family:** constants must be uniform in the target shell and all
   off-target shells must be included.
6. **Pressure-free family:** no proof may obtain packing from a favorable
   pressure sign.
7. **Terminal-set quantifier:** the reduction uses
   \(\sup_\tau\inf_{S_\tau}\), not \(\inf_S\sup_\tau\); a set allowed to
   depend on \(\tau\) must not be replaced by one fixed exceptional set.
8. **Prescribed-terminal-centre quantifier:** a centre, interval, epoch, or
   scale selected after inspecting the solution is not a
   prescribed-terminal-centre theorem.
9. **Scope:** closing (Q.1) alone does not provide scale smallness,
   contraction, regularity, or a Clay conclusion.

## 9. Execution order

I divide the next section into four auditable steps.

1. Derive the exact \(N\)-packet PDE, parity, path, and pressure identities.
2. Solve the simultaneous terminal-lobe geometry and heat-reserve constraints.
3. Compute every diagonal and off-diagonal flux, payment, central-energy, and
   all-shell clock term with constants uniform in \(N\).
4. Decide between two outcomes:
   - a smooth multi-packet counterexample to (Q.1); or
   - a proved quantitative obstruction strong enough to imply (Q.21).

No numerical simulation is needed for the algebraic stage.  Finite symbolic
checks may certify exponent and matrix bookkeeping, but they cannot replace
the uniform analytic estimates.
