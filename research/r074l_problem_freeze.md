# R0.74L problem freeze — normalized-bridge occupation at the main collar

## Status

This file freezes the question which was open at the start of R0.74L.
The companion proof r074l_forward_bridge_bv_reduction.md now proves (F.6),
and r074l_main_collar_independent_audit.md independently reconstructs that
proof.  The formulas and exclusions below remain the original frozen
contract.

R0.74K reduced the matching collar-flux upper bound on the exact
R0.74F--H smooth periodic unforced family to two analytically different
rows:

1. time multiplicity of the true packet at the target-shell collar; and
2. positive shear expulsion at the nearest inward shell.

R0.74L treats only the first row.  The nearest inward shell, the full
signed hypothesis R0.74K (4.3), the matching upper bound for
\(\mathfrak C_j\), the stronger \(X_j\) upper bound, and every universal
regularity statement remain outside this freeze.  **NOT CLAY.**

## 1. Inherited family and normalizations

Retain, without modification,

\[
 L_j=\frac{63}{32}2^j,\qquad
 R_j=e^{-L_j^2/320},\qquad
 r_j=L_jR_j,\qquad
 h_j=\frac{15}{16}r_j,
\]

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),\qquad
 F_j=F_j^++F_j^-,\qquad
 B_jR_j^2\longrightarrow\frac1{128},
\]

and the exact inversion relation

\[
 F_j^-(t,x_2,x_3)=-F_j^+(t,-x_2,-x_3).
\]

Write \(R=R_j\), \(L=L_j\), \(h=h_j\), \(B=B_j\), and
\(Q=Q_j\).  For the positive packet, R0.74F--G prove

\[
 G(t,z,y):=F_j^+(t,Q(t)+z,h+y)
 =R^3K_T(y)\,\mathbb E_{t,y}^{\rm br}
   \partial K_T(z+\mathfrak S_t^y),
 \qquad T=R^2+t,
\tag{F.1}
\]

where \(K_T\) is the periodic one-dimensional heat kernel, every winding
is retained, and

\[
 \mathfrak S_t^y
 =B\int_0^t
 [\theta_j(t-s,h)-\theta_j(t-s,h+Y_s^y)]\,ds.
\tag{F.2}
\]

The probability measure \(\mathbb P_{t,y}^{\rm br}\) is the normalized
periodic bridge from R0.74G (4.9).  It depends on both \(t\) and \(y\);
that dependence may not be discarded when time is integrated.

Let \(\psi_j^{R}\) be the frozen target-shell cutoff and put

\[
 M_j(x_2,x_3)
 :=\int_{\mathbb R}
 |\partial_2\psi_j^{R}(x_1,x_2,x_3)|\,dx_1.
\tag{F.3}
\]

R0.74K proves the geometric slice bound

\[
 \sup_{x_3}\int_{\mathbb R}M_j(x_2,x_3)\,dx_2
 \le C LR.
\tag{F.4}
\]

## 2. Exact bridge--BV majorant

Jensen applied to (F.1), followed by
\(u=z+\mathfrak S_t^y\), produces the nonnegative quantity

\[
\begin{aligned}
 \mathscr B_j(\tau)
 :=R^6\int_{I_{2R}\cap(-\infty,\tau]}
 \int_{\mathbb R}|\theta_j(t,h+y)|K_T(y)^2
 \mathbb E_{t,y}^{\rm br}\!\left[
   \int_{\mathbb R}|\partial K_T(u)|^2
   M_j\!\left(
      Q(t)-\mathfrak S_t^y+u,h+y
   \right)du
 \right]dy\,dt .
\end{aligned}
\tag{F.5}
\]

The real integrals in (F.5) are evaluated against the lifted compact
collar; the kernels and bridge remain periodic and therefore retain all
periodic copies.  Formula (F.5), rather than a heuristic deterministic
shift, is the frozen object to be checked.

### Primary R0.74L question

Does there exist a constant \(C\), independent of \(j\), such that for all
sufficiently large \(j\),

\[
 \boxed{
 \sup_{\tau\in I_R}\mathscr B_j(\tau)
 \le C LR^5?}
\tag{F.6}
\]

This is the exact positive Jensen majorant for the absolute main-collar
integrand; the factor \(|\theta_j|\) is retained rather than replaced by
one.  A proof may use the forward relation
\(dq_\omega=B\theta_j\,dt\), but only after constructing a common-time
path law that is actually compatible with the \((t,y)\)-dependent bridge
in (F.5).  Applying a deterministic change of variables separately at
each terminal time is not a proof.

## 3. Consequence if the majorant is proved

Equations (F.1), (F.5)--(F.6), and Jensen imply, for each sign,

\[
 \sup_{\tau\in I_R}
 \int_{I_{2R}\cap(-\infty,\tau]}
 \int_{\mathbb R^3}
 |\theta_j|\,|F_j^\pm|^2
 |\partial_2\psi_j^R|\,dx\,dt
 \le C LR^5.
\tag{F.7}
\]

The inversion identity gives the same estimate for the two self terms,
and

\[
 |F_j|^2\le2(|F_j^+|^2+|F_j^-|^2)
\tag{F.8}
\]

controls the cross term without claiming cancellation.  Multiplication by
the target-shell weight \(\Gamma_j\) therefore gives the desired absolute
main-collar contribution at scale
\(C\Gamma_jLR^5\).

This implication does not treat the nearest inward shell and therefore
does not by itself prove R0.74K (4.3).

## 4. Negative-result boundary

If (F.6) fails, the failure must be classified before any conclusion is
drawn.

- A counterexample to a pathwise time-change argument is only a failure of
  that proof mechanism.
- A counterexample to the Jensen majorant (F.6) still does not refute the
  smaller signed main-collar integral, because Jensen and absolute values
  may lose cancellation.
- Only a lower bound for the original signed contribution with incompatible
  scale and sign could refute that signed target.

No failure in this section may be reported as a counterexample to
Navier--Stokes regularity or as singularity evidence.

## 5. Required deliverables

R0.74L is complete only after all of the following are present.

1. A derivation of (F.5) from the exact periodic representation, including
   its lifted integration domains and all numerical powers of \(R\).
2. Either a proof of (F.6), or an explicit negative result identifying the
   first false statement and the strongest surviving replacement.
3. A separate audit of the \((t,y)\)-dependent bridge quantifiers and any
   common-time coupling used in the proof.
4. A finite exact-arithmetic or interval certificate for every calibrated
   exponent/constant comparison used by the analytic argument.
5. A bounded primary-source collision audit.  A finite non-hit is not a
   novelty or priority claim.
6. An independent mathematical audit and a journal-ready formal figure
   package with source data, SVG, vector PDF, 600-dpi PNG, and visual QA.
7. A frozen publication handoff to the independent task titled
   **发布任务**.  Publication remains a separate later transaction.
