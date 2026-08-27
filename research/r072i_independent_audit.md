# R0.72I independent audit -- physical lift, exposure, and odd-carrier parity

**Date:** 2026-08-27

**Decision:** the analytic scaling ledger is internally consistent. The
producer and independent finite routes both pass. They corroborate the
separation between a growing generic \(B_AQ_*\) upper-bound term and the much
smaller measured cubic interaction. They do not prove the analytic theorem or
enumerate the complete temporal root set.

## 1. Analytic ledger checked independently

Set \(a=q=d=K_z=\nu=1\), take the all-odd block

\[
 r_j=2M+2j+1,
 \qquad 0\le j<M,
 \qquad \delta=P=M,
\]

and impose \(S^2K_f=3P^2K_v\). Then

\[
 K_s=K_v=\frac{M(28M^2-1)}3\asymp M^3,
 \qquad K_f\asymp M^3,
\]

\[
 D\asymp M^5,
 \qquad \Theta=\frac{3P^2}{4K_f}\asymp M^{-1},
 \qquad
 D^{1/3}(1+\Theta Q_*)\asymp M^{5/3}.
\]

The R0.72H quantities obey

\[
 E_0\asymp M,
 \quad \rho_0^2\asymp M,
 \quad B_0\asymp M^{3/2},
 \quad Q_*\asymp M^{2/3}\log M,
 \quad m_*\asymp\frac{M^{7/3}}{\log M}.
\]

Therefore the four physically lifted positive terms have scales

\[
 M,\qquad M^{-1/3}\log M,\qquad M,\qquad
 M^{13/6}\log M.
\]

Only the last divided by the candidate payment grows, at
\(M^{1/2}\log M\). This is a statement about the chosen positive upper bound,
not a lower bound for the root mass.

For the true cubic row, every carrier is odd. Hence \(V\) swaps parity,
\(V^2\) preserves parity, and

\[
 P_0V^2F=P_0V^2F_{\rm even}.
\]

The Duhamel exposure gives

\[
 \|F_{\rm even}\|_2\le C\min(\sqrt M,g/M),
 \qquad
 g\int|hP_0V^2F|\le Cg\min(\sqrt M,g/M).
\]

For \(g\le\gamma_0M^{3/2}\), this is at most \(Cg^2/M\). Together with
the R0.72C joint-exposure theorem and the exact R0.72H root, this gives
\(G_{\rm all}^{\rm ex}\asymp M^2\), not the growing separated bound.

## 2. Independent implementations

| Component | Producer | Independent |
|---|---|---|
| Sign construction | Rudin--Shapiro polynomial recurrence | parity of adjacent binary \(11\) pairs |
| Gauge | original complex Fourier lattice | real all-odd gauge |
| Integrator | SciPy DOP853 | SciPy RK45 |
| Quadrature | Simpson after \(y=z^3\) | Gauss--Legendre after \(y=z^3\) |
| Truncation | radius \(8M\) | radius \(9M\) |
| Root correction | two complex evolution columns | two real evolution columns |
| Shared code | none | none; it imports neither producer code nor producer data |

The producer used \(M=4,8,16,32,64,128\), 1,601 quadrature points, and
\(y_{\max}=16\). The independent route used
\(M=4,8,16,32,64\), 280 Gauss--Legendre nodes, and \(y_{\max}=12\).

## 3. Finite results

Both result files report `passed`, and every declared check is true.

At the largest common size \(M=64\):

| Quantity | Producer | Independent |
|---|---:|---:|
| \(Q_*\) | 57.3301763454 | 57.3302314413 |
| \(\delta\int|hb|\) | 0.1646218631 | 0.1646408965 |
| mixed row \(\int|hQF|\) | 4095.7772686 | 4095.7772686 |
| exact-root \(|h|\) | 68.0084416403 | 68.0084416404 |
| generic \(B\)-route normalized ratio | 5.5556139 | 5.5556189 |
| parity-resolved normalized diagnostic | producer BV upper: \(5.61\times10^{-3}\) | measured cubic: \(1.13\times10^{-7}\) |
| evolved root residual | \(2.08\times10^{-17}\) | \(1.13\times10^{-16}\) |

Across the common sizes, the largest relative disagreements are

\[
\begin{array}{c|c}
 Q_* & 1.57\times10^{-6}\\
 \delta\int|hb| & 1.61\times10^{-4}\\
 \int|hQF| & 9.58\times10^{-10}\\
 |h(\tau_M)| & 3.61\times10^{-9}.
\end{array}
\]

The cubic integral is the most quadrature-sensitive quantity and still agrees
to better than \(1.7\times10^{-4}\) relative error. After applying the same
canonical \(\Gamma\)-normalization, the generic \(B\)-route ratios at \(M=64\)
agree to better than \(9.0\times10^{-7}\) relative error. That ratio grows
throughout both finite sequences, while the measured cubic and the \(M^2\)
complete-mass scale remain below the physical reference payment.

At producer \(M=128\), the generic \(B\)-route normalized ratio is
8.698257692, whereas the parity-resolved measured BV ratio is
0.003563152. The generic separated bound is more than
\(2.06\times10^8\) times the measured cubic contribution used in the same
Rolle ledger.

## 4. What the computation does and does not certify

The finite runs check:

1. the exact all-odd carrier moment;
2. the physical balance formulas for \(D\) and \(\Theta\);
3. the real exact-root correction and non-collapsing root row;
4. the critical-log and reciprocal-profile scales;
5. the even-component exposure;
6. the separation between the generic \(B_AQ_*\) route and the measured
   cubic interaction.

They do not certify:

1. the infinite-\(M\) estimates;
2. all roots of the truncated target coordinate;
3. an interval enclosure of rounding or truncation error;
4. mixed-parity carriers;
5. general three-dimensional Navier--Stokes regularity.

The complete-root upper theorem is analytic. It comes from the retained
R0.72C interaction exposure or the parity-refined Rolle estimate. The finite
root constructed by both solvers supplies only the matching lower witness.
