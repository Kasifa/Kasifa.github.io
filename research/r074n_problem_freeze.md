# R0.74N problem freeze — exact all-shell synthesis

## Status at freeze

This file freezes the last familywise shell-synthesis question left after
R0.74L and R0.74M.  R0.74L proves the complete target row \(k=j\), and
R0.74M proves the complete nearest-inward row \(k=j-1\).  Neither result by
itself proves the infinite annular condition R0.74K (4.3).

R0.74N asks whether every row can be assembled without assuming cancellation
between shells or between the two packets.  A positive answer would give a
matching upper bound for the collar-flux observable on this one exact family.
It would not give the stronger weighted kinetic-and-dissipation estimate, a
universal endpoint inequality, singularity control, or a regularity theorem.
**NOT CLAY.**  This last sentence records the forecast at the moment of
freeze; Section 6 transparently records the post-closure correction found by
the later cross-note audit.

## 1. Frozen family and full observable

Retain

\[
 \lambda=\frac{63}{32},\qquad c_h=\frac{15}{16},\qquad
 c_\gamma=\frac8{3969},\qquad \rho=\frac1{320},
\]

\[
 L_j=\lambda2^j,\qquad R_j=e^{-\rho L_j^2},\qquad
 h_j=c_hL_jR_j,\qquad
 \Gamma_k=e^{-4^{k-1}/32},
\tag{F.1}
\]

so that

\[
 \Gamma_j=e^{-c_\gamma L_j^2},\qquad
 \frac{\Gamma_{j+1}}{\Gamma_j}=e^{-3c_\gamma L_j^2}.
\tag{F.2}
\]

Write \(R=R_j\), \(L=L_j\), \(h=h_j\), and let

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),\qquad
 F_j=F_j^++F_j^-,\qquad
 F_j^-(t,x_2,x_3)=-F_j^+(t,-x_2,-x_3)
\tag{F.3}
\]

be the exact smooth periodic unforced family inherited from R0.74F--H.  The
time window and inherited R0.74H cutoff are

\[
 \begin{gathered}
 s_R=61R^2,\qquad I_R=(64R^2,65R^2),\\
 \eta_R=0\ \hbox{near }s_R,\qquad
 \eta_R=1\ \hbox{on }I_R,\\
 0\le\eta_R\le1,\qquad \eta_R'\ge0,\qquad
 |\eta_R'|\le CR^{-2}.
 \end{gathered}
\tag{F.4}
\]

The cutoff is smooth and nondecreasing.  The shell estimate itself will use
only \(0\le\eta_R\le1\); the complete conditions are retained so that any
subsequent appeal to the R0.74H weighted-energy identity concerns exactly the
same object.

For the frozen radial cutoffs

\[
 \psi_k^R(x)=
 \vartheta\!\left(\frac{|x|-2^kR}{R/8}\right)
 \vartheta\!\left(\frac{2^{k+1}R-|x|}{R/8}\right),
\tag{F.5}
\]

define

\[
 \mathcal J_{j,k}(\tau)
 :=\Gamma_k\int_{s_R}^{\tau}\eta_R(t)
 \int_{\mathbb R^3}\theta_j(t,x_3)\widetilde F_j(t,x_2,x_3)^2
 \partial_2\psi_k^R(x)\,dx\,dt,
\tag{F.6}
\]

and

\[
 \mathcal I_j(\tau)=\sum_{k\ge1}\mathcal J_{j,k}(\tau).
\tag{F.7}
\]

The tilde in (F.6) is the periodic lift; the cutoff is the compact Euclidean
one.  Every lift and every shell remains part of the object.

### Primary R0.74N question

Does there exist a constant independent of \(j\) such that, for all
sufficiently large \(j\),

\[
 \boxed{
 \sup_{\tau\in I_R}[\mathcal I_j(\tau)]_+
 \le C\Gamma_jLR^5?}
\tag{F.8}
\]

This is exactly R0.74K (4.3), specialized to the frozen family.

## 2. Exact residual decomposition

For a finite annular truncation first write

\[
 \mathcal I_j^{(N)}
 =\mathcal I_{<}+\mathcal I_{=}+\mathcal I_{>,N},
\tag{F.9}
\]

where

\[
 \mathcal I_{<}=\sum_{1\le k\le j-1}\mathcal J_{j,k},\qquad
 \mathcal I_{=}=\mathcal J_{j,j},\qquad
 \mathcal I_{>,N}=\sum_{j+1\le k\le N}\mathcal J_{j,k}.
\tag{F.10}
\]

The three rows in (F.10) are disjoint and cover every \(k\ge1\) as
\(N\to\infty\).  R0.74L already supplies

\[
 \sup_{\tau\in I_R}|\mathcal I_{=}(\tau)|
 \le C\Gamma_jLR^5.
\tag{F.11}
\]

The unresolved obligations at freeze are therefore the *combined* inner
sum and the infinite outer tail.  The older rowwise exponent table is not a
substitute for either analytic estimate.

## 3. Candidate combined-inner route

Define the cancellation-free positive chord

\[
 D_{<}(t,x_2,x_3)
 :=\sum_{k=1}^{j-1}\Gamma_k
 \int_{\mathbb R}
 [\theta_j(t,x_3)\partial_2\psi_k^R(x)]_+\,dx_1,
\tag{F.12}
\]

and periodize it in \((x_2,x_3)\).  Radial geometry suggests

\[
 D_{<}\le C\sum_{k\ge1}2^k\Gamma_k<\infty,
\tag{F.13}
\]

while its entire support remains inside the padded \(j-1\) radius

\[
 r_-=2^jR+\frac R8
 =\left(\frac{32}{63}L+\frac18\right)R.
\tag{F.14}
\]

If (F.13)--(F.14) survive exact periodization, the R0.74M final-segment
expulsion mechanism can potentially treat every inward shell at once.  The
new bad-path ledger would have to prove

\[
 R^4e^{-L^2/16}\lesssim\Gamma_jLR^5,
\tag{F.15}
\]

and the good-path super-Gaussian tail would have to pay \(\Gamma_jR^2\).
These are proof obligations, not assertions at freeze.

## 4. Candidate outer-tail route

For \(k\ge j+1\), a proof may use the complete true packet only if it first
establishes a uniform pointwise bound and keeps the full lift-side collar.
The proposed absolute ledger is

\[
 \|F_j\|_\infty\le C,\qquad
 \int_{\mathbb R^3}|\partial_2\psi_k^R|\,dx
 \le C4^kR^2,
\tag{F.16}
\]

followed by

\[
 R^4\sum_{k\ge j+1}\Gamma_k4^k
 \lesssim\Gamma_jLR^5.
\tag{F.17}
\]

The proof must justify the infinite sum rather than select a central torus
copy.  The expected exponential reserve is

\[
 3c_\gamma-\rho>0,
\tag{F.18}
\]

but exponent compatibility alone is not the theorem.

## 5. Completion gate

R0.74N may be promoted only after all of the following are present.

1. A proof or explicit refutation of (F.8), with the first failed implication
   identified if the proposed synthesis does not close.
2. Exact coverage of all three ranges in (F.10), both packet signs, the cross
   term, both radial cutoff faces, the time cutoff, all periodic lifts, and
   the \(N\to\infty\) limit.
3. An independent analytic reconstruction which specifically attacks
   (F.13), the outer lift-side volume estimate, and infinite-shell summation.
4. Exact finite arithmetic for the exponent margins and all discrete tail
   comparisons used in the proof.
5. A bounded primary-source collision audit reported as a finite hit or
   non-hit, never as novelty or priority proof.
6. A journal-ready formal figure package with source data, SVG, vector PDF,
   600-dpi PNG, manifest, and visual QA.
7. A frozen handoff to the independent Codex task titled **发布任务**.

The recap remains reserved for a major milestone.  Publication is a separate
transaction after this research gate closes.

## 6. Post-closure correction to the initial forecast

After (F.8) was proved, a cross-note dependency audit corrected one
conservative forecast in the opening status.  R0.74H Theorem 5.1 had already
proved, for the same full cutoff and each \(\alpha\in\{M,F\}\),

\[
 X_{R_j}^\alpha
 \le C\left[(P_{R_j}^\alpha)^{2/3}
 +\mathfrak C_{R_j}^\alpha\right].
\tag{F.19}
\]

On the zero-frame exact family, Versions M and F coincide.  R0.74J proves
\(P_j\asymp B_j^3R_j^3\), while the completed R0.74N theorem and R0.74K
give \(\mathfrak C_j\lesssim B_j^2L_jR_j^2\).  Hence

\[
 X_j\le C\left(B_j^2R_j^2+B_j^2L_jR_j^2\right)
 \le CB_j^2L_jR_j^2.
\tag{F.20}
\]

The inherited R0.74F packet-survival lower bound gives the reverse
inequality, so the post-closure status is

\[
 X_j\asymp\mathfrak C_j\asymp B_j^2L_jR_j^2
 \asymp P_j^{2/3}\sqrt{1+\log_+P_j}.
\tag{F.21}
\]

This correction does not alter the frozen primary question and does not say
that (F.8) alone implies (F.21).  It records the non-circular synthesis of
the independently established R0.74H energy closure, the R0.74J payment law,
and the R0.74N collar bound.  It is not a new stochastic estimate, gives no
matching lower bound for the dissipation component alone, and does not prove
a universal endpoint or any regularity statement.  **NOT CLAY.**
