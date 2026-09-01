# R0.74K independent collar-ledger audit

## Verdict and source binding

**Verdict:** `R074K_COLLAR_LEDGER_INDEPENDENT_AUDIT_PASS`
**Open-gate verdict:** `TRUE_PACKET_BRIDGE_BV_REMAINS_OPEN`
**Bound source:** `research/r074k_single_collar_shear_lag_reduction.md`
**Bound source SHA-256:**
`8f21248603551c39f34864dd921847dc8b9c6f70962209864901d476fe6722e3`

This audit checks Sections 3--4 only.  It independently reconstructs the
collar-flux prefactor, the slice-BV power count, the constant-shear reference
packet estimate, the conditional implication in Theorem 4.1, and the exact
Version-M/Version-F identification.  The verdict is bound to the byte sequence
above and does not transfer to a later source without a new rebind.

## 1. Exact-family reduction and flux prefactor

On the inherited exact family,

\[
 u_j=(\mathfrak a_jF_j,B_j\theta_j,0),
 \qquad p_j=0,
 \qquad X_{R_j}=a_{R_j}=a'_{R_j}=0.
\]

Consequently the moved-only and mean-subtracted fields coincide.  Their
pressure gauges contribute zero after the divergence integration, their
acceleration rows vanish, every \(\partial_1\) row vanishes because the field
is independent of \(x_1\), and the pure-shear \(\partial_2\) row vanishes by
integration in \(x_2\).  Thus both versions have the same signed flux

\[
 \mathfrak F_{R_j}(\tau)
 =\frac{\mathfrak a_j^2B_j}{2R_j}\,\mathcal I_j(\tau),
\]

where \(\mathcal I_j\) is exactly the packet-only integral in source equation
(4.2).  Since

\[
 \mathfrak a_j^2=B_j^2\Gamma_j^{-1},
\]

the prefactor is

\[
 \boxed{
 \frac{\mathfrak a_j^2B_j}{2R_j}
 =\frac{B_j^3}{2R_j\Gamma_j}.}
\]

The calibration \(\beta_j=B_jR_j^2\to1/128\) makes \(B_j>0\) for all
sufficiently large \(j\), so multiplication by this prefactor preserves the
positive-part inequality.  No sign reversal is hidden in Theorem 4.1.

## 2. Independent slice-BV reconstruction

For the radial cutoff \(\psi_j^{R_j}\), let

\[
 M_j(x_2,x_3)
 =\int_{\mathbb R}
 |\partial_2\psi_j^{R_j}(x_1,x_2,x_3)|\,dx_1.
\]

The two derivative collars have radii

\[
 2^jR_j=\lambda^{-1}L_jR_j,
 \qquad
 2^{j+1}R_j=2\lambda^{-1}L_jR_j,
\]

and radial thickness comparable to \(R_j\).  At fixed \(x_3\), the area of
each resulting planar transition region is at most
\(C(L_jR_j)R_j\).  Since
\(|\nabla\psi_j^{R_j}|\le C/R_j\), Fubini gives

\[
 \boxed{
 \sup_{x_3}\int_{\mathbb R}M_j(x_2,x_3)\,dx_2
 \le C L_jR_j.}
\]

The constant depends only on the frozen cutoff profile.  It is independent of
\(j\), the solution amplitude, and the location of a planar tangency.  The
area argument integrates the apparent pointwise square-root chord singularity
and therefore loses no factor \(L_j^{1/2}\).  Source equations (3.3)--(3.4)
have the correct scale.

## 3. Independent reference-packet power count

For

\[
 F_{\rm fr}(t,x_2,x_3)
 =R_j^3\partial K_T(x_2-Q_j(t))K_T(x_3-h_j),
 \qquad T=R_j^2+t,
\]

the interval \(I_{2R_j}\) gives
\(T/R_j^2\in[62,66]\).  The periodic Gaussian moments have the exact powers

\[
 \int_{\mathbb T}\sup_{T/R_j^2\in[62,66]}K_T(y)^2\,dy
 \le C R_j^{-1},
\]

\[
 \int_{\mathbb T}\sup_{T/R_j^2\in[62,66]}
 |\partial K_T(z)|^2\,dz
 \le C R_j^{-3}.
\]

The calibrated platform gives \(Q_j'(t)\ge3B_j/4\).  For fixed kernel
variables, the change of variables \(t\mapsto Q_j(t)\) and the slice-BV bound
give

\[
 \int_{I_{2R_j}}
 M_j(Q_j(t)+z,h_j+y)\,dt
 \le \frac{C L_jR_j}{B_j}.
\]

Hence the unweighted packet row is

\[
 R_j^6\,R_j^{-1}\,R_j^{-3}
 \frac{L_jR_j}{B_j}
 =\frac{L_jR_j^3}{B_j}.
\]

The eventual lower calibration bound
\(B_j\ge(128R_j^2)^{-1}\) therefore yields

\[
 \boxed{
 \Gamma_j\int_{I_{2R_j}}\int_{\mathbb R^3}
 |F_{\rm fr}|^2|\partial_2\psi_j^{R_j}|\,dx\,dt
 \le C\Gamma_jL_jR_j^5.}
\]

Thus every power in source equations (3.6)--(3.8) is correct.  This is an
absolute estimate for the constant-shear reference packet; it is not an
estimate for the true packet with the bridge displacement
\(\mathfrak S_t^y\).

## 4. Audit of Theorem 4.1

Assume the source hypothesis

\[
 \sup_{\tau\in I_{R_j}}[\mathcal I_j(\tau)]_+
 \le C_I\Gamma_jL_jR_j^5.
\]

Using the positive prefactor reconstructed in Section 1 gives

\[
\begin{aligned}
 \mathfrak C_j
 &\le
 \frac{B_j^3}{2R_j\Gamma_j}
 C_I\Gamma_jL_jR_j^5\\
 &=\frac{C_I}{2}B_j^3L_jR_j^4\\
 &=\frac{C_I}{2}(B_jR_j^2)
 B_j^2L_jR_j^2.
\end{aligned}
\]

Since \(\beta_j=B_jR_j^2\) is eventually bounded, this proves

\[
 \boxed{\mathfrak C_j\le C B_j^2L_jR_j^2.}
\]

The inherited R0.74H lower bound has the same common Version-M/Version-F
observable and gives the reverse inequality.  R0.74J equation (4.6) then
identifies this scale, on the exact family only, with

\[
 P_j^{2/3}\sqrt{1+\log_+P_j}.
\]

The implications (4.3) \(\Rightarrow\) (4.4) \(\Rightarrow\) (4.5)--(4.6)
are therefore valid and non-circular.  The source now calls this the
“direct” collar statement and explicitly says that direct refers to the
observable-level route: it proves sufficiency, not logical necessity among
all possible proofs.

## 5. Conditional bridge boundary

R0.74G Theorem 4.1 supplies the normalized pointwise bridge inequality and
the one-sided displacement bound

\[
 \mathfrak S_t^y\ge-\delta_j,
 \qquad \delta_j/R_j\to0.
\]

After translating the horizontal kernel, however, the collar is evaluated at

\[
 M_j(Q_j(t)-\mathfrak S_t^y+u,h_j+y).
\]

Neither the one-sided bound nor the existing Peetre reduction controls the
time multiplicity with which this shifted centre encounters a collar.  Thus
the existing theorem does not license the change of variables used for the
reference packet.  A new time-coupled bridge--BV estimate, retaining the
forward signed relation \(dq_\omega=B_j\theta_j\,dt\), is still required.

The following rows therefore remain **OPEN**:

1. source hypothesis (4.3) for the true paired packet, including all periodic
   windings;
2. the time-coupled bridge--BV estimate at the target collar;
3. the positive shear-expulsion estimate at the nearest inward collar
   \(A_{j-1}(R_j)\);
4. the matching familywise upper bound for \(\mathfrak C_j\);
5. the stronger weighted kinetic-and-dissipation upper needed for \(X_j\);
6. every universal square-root-log endpoint theorem and every global
   regularity or singularity conclusion.

The finite exponent comparisons and the constant-shear reference calculation
do not prove any of these open rows.  No missing prefactor, scale power,
Version-M/Version-F mismatch, or reversed implication was found in Sections
3--4 of the bound source.

## 6. Final source-rebind addendum

The first audit pass was bound to source SHA-256

`20f5c41db46ecb8994a095778106eca0c6a5b2620fb8df85022eba53fd93f72f`.

The current pass is rebound to source SHA-256

`8f21248603551c39f34864dd921847dc8b9c6f70962209864901d476fe6722e3`.

The intervening analytic-audit repairs were checked directly in the current
Sections 3--4:

1. Lemma 3.2 now quantifies every \(\tau\in I_{R_j}\) and writes the truncated
   interval as \(I_{2R_j}\cap(-\infty,\tau]\).  Its proof correctly bounds
   this by the full nonnegative \(I_{2R_j}\) integral, so the slice-BV change
   of variables and the scale \(C\Gamma_jL_jR_j^5\) are unchanged.
2. Theorem 4.1 is now titled the **direct** sufficient statement, and the
   text after its proof explicitly rules out a logical-necessity reading.
   This is consistent with the implication audited in Section 4 above.
3. The open true-packet work is now stated route-specifically: a proof along
   the selected normalized-bridge route must retain periodic windings,
   bridge--BV time coupling, nearest-inner shear expulsion, and the
   bridge/shear-lag correlation.  No missing estimate is promoted to a proved
   row.
4. The exact-family flux formula, the positive prefactor, the slice-BV bound,
   both periodic kernel powers, the calibration inequality
   \(B_j^{-1}\le128R_j^2\), the Version-M/Version-F identity, and the
   conditional chain (4.3)--(4.7) are mathematically unchanged.

The rebind therefore returns

`R074K_COLLAR_LEDGER_FINAL_SOURCE_REBIND_PASS`.

**NOT CLAY.**
