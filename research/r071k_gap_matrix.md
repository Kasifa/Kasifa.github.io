# R0.71K gap matrix — what fixed matched cells close and what they leave open

## 1. Quantified setting

| Item | R0.71K choice | Quantifier | Reason |
|---|---|---|---|
| NSE family | R0.71J global-smooth fixed-energy 2D3C family | every fixed \(\nu>0\), all sufficiently large dyadic \(K\) | genuine NSE trajectory with an exact zero-entry positive pulse |
| Frequency frame | R0.71E broad parent-only tight frame | fixed before the datum | preserves the certified R0.71J full-frame heat bound |
| Selected parent | \(\kappa=4K\) | one parent used for the lower bound | contains the exact R0.71J witness |
| Spatial partition | one smooth, nonnegative, translated, scale-covariant tensor partition | fixed once for every dyadic parent | at \(\kappa=4K\), translations are exactly \(2\pi/K\) |
| Selected cells | \(K^3\) cells of radius \(r=\rho/\kappa\) | finite | permits the exact hard-denominator identity without an infinite passage |
| Observation interval | \(I_K=[0,(\log2)/(18\nu K^2)]\) | parabolic fixed window | same window as R0.71J |
| Full positive creation | supremum over finite frame/cell truncations | extended-valued, nonnegative | only monotonicity is used outside the selected finite family |
| Heat/payment sum | full frame with bounded-overlap support packing | Tonelli/nonnegative sum | has a direct frame upper bound |

## 2. Ledger rows

| Row | Included? | Size on the witness | R0.71K conclusion |
|---|---:|---:|---|
| Interior projected-Lamb work | yes | \(B_Q=O(1)\) per cell | combines with cutoff--curl work before the positive part |
| Cutoff--curl term \(F\cdot(\nabla\chi_Q\times W)\) | yes | \(O(1)\) per cell | leading; not discarded |
| Denominator interior/collar/cross terms | yes | \(d_Q=O(K)\) per cell | all leading; together give \(D_{\rm loc}=O(K^4)\) |
| Fixed-cutoff motion row \(\chi_t\), equivalently \(R-V_r\cdot\nabla\chi\) | zero | exactly zero | fixed cells remove only this row |
| Field/projective tangent row \(\langle P_Qx,E_{Q,t}\rangle\) | yes | \(O(\nu K^{1/2})\) per cell | leading; not confused with cutoff motion |
| Viscous collar \(-\nu\nabla\times(\mathcal K_{\chi_Q}W)\) | yes | leading; weighted aggregate \(O(K^{-2})\) | cannot be called lower order or Leray-paid |
| \(Y_t/Y\) normalization | yes, inside \(\mathcal J_Q\) | leading joint row | no separate positive part is taken |
| Denominator faces | absent for selected cells | \(d_Q>0\) on \(I_K\) | proved from translation symmetry and positive parent denominator |
| Refresh atoms | absent | fixed partition | not a statement about adaptive partitions |

## 3. Exact implication matrix

| Candidate implication | Status | Evidence | Consequence |
|---|---|---|---|
| Global zero entry implies every aligned cell has zero entry | **closed** | translation symmetry gives \(B_Q=B_\kappa/K^3\) | no hidden initial face payment |
| Local denominators stay positive | **closed** | all \(d_Q\) equal; if one vanished then \(\sum_QC_Q=C_\kappa\) would vanish | hard scalar identity applies on the whole window |
| Matched cell sum retains a positive endpoint | **closed** | \(\sum_Qq_Q=(B_\kappa^+)^2/D_{\rm loc}\), \(D_{\rm loc}\le C_{\rm part}D_\kappa\) | \(A_{\rm loc}(t_*)\ge A_*/(2C_{\rm part})\) |
| Selected-cell positive creation is \(\gtrsim K^{-2}\) | **closed** | exact positive-defect identity and zero entry | finite, audit-safe lower bound |
| Same bounded-overlap local heat endpoint is \(O((\nu K^4)^{-1})\) | **closed** | \(\sum_Q\|1_{\mathrm{supp}\chi_Q}F_j\|_2^2\le N\|F_j\|_2^2\) plus R0.71J | heat-only payment fails by \(K^2\) |
| Matched localization creates an automatic coercive collar gain | **rejected as an algebraic claim** | collar is signed inside \(M_Q\) and leading order | no free positive term appears |
| Absolute viscous collar has a Leray-level bound | **open** | its aggregate is the same \(K^{-2}\) scale as creation | possible next finite gate |
| Arbitrary phase-misaligned matched partitions have the same temporal lower bound | **open** | their endpoint is positive, but their cellwise initial work need not vanish | current theorem is one fixed aligned family |
| Moving/deforming cells improve the ledger | **open** | cutoff motion and distortion return | not covered by the fixed partition theorem |
| Denominator faces and refresh atoms are summable in general | **open** | absent only in the witness family | no face-paid BV theorem |
| Infinite frame--cell hard/soft identity | **open** | only finite selected identities and monotone nonnegative sums are used | no hidden limit claim |
| Unconditional weighted BV or continuation | **open** | no Leray payment for the leading collar/tangent rows | no regularity consequence |

## 4. Route verdict

The fixed aligned matched partition does not repair the R0.71J heat-payment
gap:

\[
 \mathcal Z_K^{\mathrm{sel,loc}}
 \ge \frac{A_*}{64C_{\mathrm{part}}K^2},
 \qquad
 \mathcal H_K^{\mathrm{loc}}
 \le \frac{N(1-2^{-1/9})}{2\nu K^4}.
\]

Therefore the ratio is at least a positive constant times \(\nu K^2\).  The
rejected implication is only

\[
 \text{same local heat/support packing}
 \Longrightarrow
 \text{uniform payment of complete localized positive creation}.
\]

The calculation does not reject a right-hand side that includes a genuinely
independent, Leray-controlled collar, shape, face, or refresh budget.  The
viscous collar is itself leading order, so the next gate must either control
that row from an already available NSE quantity or stop the temporal-residence
branch.
