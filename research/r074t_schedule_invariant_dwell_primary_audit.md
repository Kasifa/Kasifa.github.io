# R0.74T Step 19 — independent primary analytic audit

## 0. Verdict and audit boundary

**Verdict: PASS.**

This audit independently checks the mathematical deductions in
`r074t_schedule_invariant_dwell_coercivity.md`, with special attention to the
exact outer-lobe constant, the fixed-deletion quantifier order, the dwell-time
exponent, and the asynchronous common-shear construction.  The audited main
source has SHA-256

```text
8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd
```

The audit is analytic and human-readable.  It is not a machine-checked proof,
not a formalization of the Navier--Stokes PDE, and not an independent proof of
every inherited estimate.  It verifies that the cited inherited statements
have been used with compatible hypotheses and that the new deductions follow
from them.  It proves no regularity or blow-up theorem and does not solve the
Navier--Stokes Millennium problem.  **NOT CLAY.**

## 1. Frozen dependency ledger

The following byte hashes were recomputed from the working tree at the time of
this audit.

| Role | Path | SHA-256 |
|---|---|---|
| audited Step 19 source | `research/r074t_schedule_invariant_dwell_coercivity.md` | `8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd` |
| periodic bridge and one-packet lobe | `research/r074f_two_packet_survival.md` | `0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb` |
| exact finite common-shear NSE family | `research/r074q_common_shear_multipacket_gate.md` | `60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695` |
| relaxed multipacket placement, dominance, and cubic row | `research/r074q_relaxed_multipacket_cubic_obstruction.md` | `ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d` |
| fixed-deletion and simultaneous-height definitions | `research/r074s_fixed_deletion_simultaneous_height.md` | `305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1` |
| clock, cutoff, and Version-M definitions | `research/r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` |

The repository HEAD during the check was
`963613d54303eb240c1daa40c57ffc106a92535b` on branch
`codex/r074r-cubic-packing`.  The Step 19 files were not yet part of that
commit, so the SHA-256 ledger above, rather than HEAD alone, is the binding
for this audit.

## 2. Exact coercive constant in (T.9)--(T.10)

On the outer lobe, Step 19 assumes

\[
 |\Omega _2(t)|=\frac1{16}L_2R^3,
 \qquad
 h_2\le \frac{\Gamma _2}{2R}
             \int_{\Omega _2(t)}|u(t,x)|^2\,dx
\]

for almost every \(t\in J_2\), where \(|J_2|=\theta R^3\).  Therefore

\[
 |\Omega _2(t)|^{-1/2}=4L_2^{-1/2}R^{-3/2}
\]

and spatial Hölder gives

\[
\begin{aligned}
 \int_{\Omega _2(t)}|u|^3
 &\ge |\Omega _2(t)|^{-1/2}
       \left(\int_{\Omega _2(t)}|u|^2\right)^{3/2}\\
 &\ge 4L_2^{-1/2}R^{-3/2}
       \left(\frac{2Rh_2}{\Gamma _2}\right)^{3/2}\\
 &=2^{7/2}h_2^{3/2}\Gamma _2^{-3/2}L_2^{-1/2}.
\end{aligned}
\]

The lobe is in \(A_{k_2}(R)=A_{k_2-1}(2R)\), so its exterior weight is at
least

\[
 \gamma_{k_2-1}=\Gamma _2^{1/4}.
\]

Restricting the nonnegative exterior velocity-cubic payment to the jointly
measurable moving lobe gives

\[
\begin{aligned}
 P_R^M
 &\ge (2R)^{-2}\Gamma _2^{1/4}
       |J_2|\,2^{7/2}h_2^{3/2}
       \Gamma _2^{-3/2}L_2^{-1/2}\\
 &=2\sqrt2\,\theta h_2^{3/2}R
       \Gamma _2^{-5/4}L_2^{-1/2}.
\end{aligned}
\]

Thus the constant and every exponent in (T.9) are exact.  Since
\((2\sqrt2)^{2/3}=2\), taking the \(2/3\) power yields exactly

\[
 (P_R^M)^{2/3}\ge2\Lambda _2h_2,
 \qquad
 \Lambda _2=\theta^{2/3}R^{2/3}
              \Gamma _2^{-5/6}L_2^{-1/3},
\]

which verifies (T.10).  The robust variant is also correct: replacing the
weight and volume by
\(W_{2R}\ge c_W\Gamma _2^{1/4}\) and
\(|\Omega _2(t)|\le C_\Omega L_2R^3\) changes the prefactor to
\(2^{-1/2}c_WC_\Omega^{-1/2}\).  At
\(c_W=1\), \(C_\Omega=1/16\), this returns \(2\sqrt2\).

## 3. The one-deletion quantifier in (T.17)

Let \(k_1\ne k_2\), and suppose that each clock has a positive-measure time
set on which

\[
 K_{k_i,R}(t)\ge h_i>0,
 \qquad i=1,2.
\]

For every deletion set \(S\) with \(\#S\le1\), at least one of \(k_1,k_2\)
is not in \(S\).  At a time belonging to the corresponding positive-measure
set, nonnegativity of every clock gives

\[
 \sup_{t\in D}\sum_{k\notin S}K_{k,R}(t)
 \ge \min(h_1,h_2).
\]

Taking the infimum only after this statement has been proved for every fixed
\(S\) yields

\[
 \mathfrak L^K_{1,R}(D)\ge h_*:=\min(h_1,h_2).
\]

This verifies the order of quantifiers in (T.17).  It does not establish the
same lower bound for \(\mathfrak H^{\rm fix}_{1,R}\): that functional is built
from stopped forward-flux increments \(z_k\), not from completed clocks
\(K_k\).  Likewise, because \(h_*\) is only a lower witness for
\(\mathfrak L^K_{1,R}\), (T.18) does not imply
\((P_R^M)^{2/3}\gtrsim\mathfrak L^K_{1,R}\).  The directions stated in the
main source are therefore correct.

## 4. Dwell algebra in (T.24)--(T.29)

Set

\[
 L_2=2L_1,
 \qquad
 \Gamma _2=e^{-c_\gamma L_2^2},
 \qquad
 R=e^{-S},
 \qquad
 d_L=a_SL_1^2-S.
\]

Taking logarithms in the definition of \(\Lambda _2\) gives

\[
 \log\Lambda _2
 =\frac23\log\theta-\frac23S
  +\frac56c_\gamma L_2^2-\frac13\log L_2.
\]

Using \(L_2^2=4L_1^2\) and \(S=a_SL_1^2-d_L\) gives the exact identity

\[
 \log\Lambda _2
 =\frac23\left[
   \log\theta+(5c_\gamma-a_S)L_1^2+d_L
   -\frac12\log L_2\right],
\]

which is (T.24).  The rational exponent reserve is

\[
 5c_\gamma-a_S
 =\frac{40}{3969}-\frac{75}{22528}
 =\frac{603445}{89413632}>0.
\]

Consequently \(\theta=1\), \(L_1\to\infty\), and \(d_L\to\infty\) force
\(\Lambda _2\to\infty\).  More generally, the divergence condition (T.26)
has the stated direction.

If instead

\[
 \sup_n\frac{(P_{R_n}^M)^{2/3}}{h_{*,n}}<\infty,
\]

then (T.18) first forces \(\Lambda _{2,n}=O(1)\).  Solving this necessary
condition for \(\theta_n\) gives

\[
 \theta_n
 \le C R_n^{-1}\Gamma _{2,n}^{5/4}L_{2,n}^{1/2}
 =C L_{2,n}^{1/2}
   \exp\!\left[S_n-\frac54c_\gamma L_{2,n}^2\right].
\]

Substituting \(L_{2,n}=2L_{1,n}\) and
\(S_n=a_SL_{1,n}^2-d_{L,n}\) yields

\[
 \theta_n\le C L_{2,n}^{1/2}
 e^{-(5c_\gamma-a_S)L_{1,n}^2-d_{L,n}},
\]

so both the inequality direction and the exponential coefficient in
(T.28)--(T.29) are correct.  The survival condition used here is explicitly
only sufficient for the inherited bridge proof; it is not asserted to be a
necessary condition on all possible packets.

## 5. Admissibility of the asynchronous construction

Section 7 works along the sequence of Section 4 and separately imposes

\[
 R\le\frac1{32},
 \qquad L_2R\le\frac5{144},
 \qquad L_1\ge9216,
 \qquad R^{-1}e^{-a_SL_1^2}\to0.
\]

These hypotheses are sufficient for every inheritance used there.

1. The central-chart condition for the outer height implies the corresponding
   condition for the inner height.  Together with \(L_1\to\infty\), it also
   gives \(R\to0\).
2. The positive-platform estimate gives
   \(D_1=64R^2(1+o(1))\), hence
   \(B=(128R^2)^{-1}(1+o(1))\).
3. The bridge error for the inner packet vanishes by the displayed survival
   condition.  The outer packet has the stronger exponent because
   \(L_2>L_1\); the \(a_D\) term is also harmless because \(a_D>a_S\).
   Periodic bridge and inversion errors vanish because \(R\to0\).
4. For the weighted two-packet cross-tail remainder, with
   \(q=c_\gamma/2\), the chart condition gives

   \[
    R^{-2}\ge\left(\frac{144}{5}\right)^2L_2^2.
   \]

   Therefore

   \[
    C\exp\!\left(qL_2^2-\frac3{22R^2}\right)
    \le Ce^{-c_*L_2^2}\to0,
    \qquad
    c_*:=\frac3{22}\left(\frac{144}{5}\right)^2-q>0.
   \]

   Thus Section 7 does not silently reuse the special
   \(R=e^{-\rho L^2}\) choice from R0.74Q.
5. Choosing
   \(q_{{\rm pre},i}=-B\int_0^{\tau_i}\theta_R(s,y_i^\circ)\,ds\)
   gives \(Q_i(\tau_i)=0\).  On
   \(J_i=(\tau_i-\theta_iR^3,\tau_i)\), with
   \(0<\theta_i\le1\),

   \[
    |Q_i(t)|\le B\theta_iR^3\le R/64
   \]

   for sufficiently large \(L_1\).  This preserves the annular margins.
   Independent horizontal re-centring commutes with the common scalar
   advection--diffusion equation, while the inversion pair retains oddness.
   Both packets therefore remain in one exact smooth periodic mean-zero
   unforced Navier--Stokes solution with zero physical pressure.
6. The free derivative-packet age lies in the compact interval \((65,66)\)
   on \(I_R\).  Its lower bound, the inversion estimate, and the vertical
   cross-tail bounds are uniform in both prescribed admissible times and do
   not depend on the horizontal entrance points.
7. On each resulting lobe, \(\Psi_{k_i}^R=1\), and the frozen time cutoff is
   one throughout \(I_R\).  Hence the endpoint row of the nonnegative clock
   gives \(K_{k_i,R}\ge cA_*^2R^2=cT\); (T.17) then gives
   \(\mathfrak L^K_{1,R}(I_R)\ge cT\).

The vertical centres are denoted \(y_i^\circ=c_hL_iR\), while \(h_i\) is
reserved for the kinetic floors.  Thus the final source has no collision
between spatial-height and clock-height notation.

## 6. The explicit disjoint windows in (T.42)

For unit normalized dwell, Step 19 chooses

\[
 \tau_1=64R^2+2R^3,
 \qquad
 \tau_2=65R^2.
\]

This gives

\[
 J_1=(64R^2+R^3,64R^2+2R^3),
 \qquad
 J_2=(65R^2-R^3,65R^2).
\]

Both lie in \(I_R=(64R^2,65R^2)\) when \(R<1/2\).  They are strictly
disjoint precisely under the stronger sufficient inequality

\[
 64R^2+2R^3<65R^2-R^3,
\]

which is equivalent to \(R<1/3\).  Thus the condition in (T.42) is correct.
The outer window retains \(\theta_2=1\), so the positive exponent in (T.24)
forces \((P_R^M)^{2/3}/T\to\infty\) along the stated survival-compatible
asymptotic.  Time separation alone does not remove the outer cubic payment.

## 7. Claim-boundary audit

The source correctly distinguishes the following statements.

- The coercive estimate is invariant under the relative position of other
  packet times once the outer-lobe hypotheses hold.
- Section 7 realizes arbitrary prescribed lobe windows only inside the stated
  terminal slab.  It does not independently time-translate already evolved
  packets and does not realize arbitrary real target times.
- The theorem controls the explicit persistent lobe-floor witness, not an
  upper bound for the full completed-clock functional.
- A short subinterval selected from a longer-lived lobe does not erase payment
  already incurred on the longer lobe.  A genuine escape would have to make
  the maximal time set carrying a comparable outer kinetic floor
  exponentially short.
- No implication from completed-clock floors to the stopped-flux functional is
  obtained without the already recorded Step 18 payment terms.
- The fixed-deletion estimate, the direct hybrid estimate, Q.12, Q.1, scale
  contraction, regularity, blow-up, and the Clay problem all remain open.

Within these boundaries, the deductions (T.1)--(T.43) are mathematically
consistent and the audited Step 19 source passes this independent analytic
review.

<!-- R074T_STEP19_PRIMARY_AUDIT_PASS -->
