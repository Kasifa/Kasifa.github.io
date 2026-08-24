# R0.70M independent derivation and certificate audit

**Audit status:** PASS after naming, sharpness, and PDE-scope corrections
**Date:** 2026-08-24

## 1. Audit scope

The independent audit checked five separate claim classes:

1. the exact pullback algebra for the strain-only propagator;
2. the normalized shape quotient and the \(\kappa_2(G)^2\) exponent;
3. the zero-signed-integral noncommutative holonomy certificate;
4. the affine-relative SPD identity and rank boundary;
5. the distinction between matrix-ODE, exact periodic NSE, and unproved
   unforced-trajectory realizations.

The audit did not assume that a passing symbolic producer proves the PDE
interpretation. Algebraic identities, source conventions, and realization
claims were checked separately.

## 2. Exact pullback recomputation

Starting from

\[
 Q'=\Sigma Q+Q\Sigma+F,
 \qquad G'=\Sigma G,
 \qquad M=G^{-1},
 \tag{2.1}
\]

the independent derivation gives

\[
 M'=-M\Sigma,
 \qquad
 (MQM^{\mathsf T})'=MFM^{\mathsf T}.
 \tag{2.2}
\]

For

\[
 \widehat E=\operatorname{tr}\widehat Q,
 \quad
 \widehat R=\widehat Q/\widehat E,
 \quad
 \widehat B=\widehat R-I/3,
 \tag{2.3}
\]

the recomputed ledger is

\[
 \widehat E'=\operatorname{tr}\widehat F,
 \tag{2.4}
\]

\[
 \widehat B'
 =\frac{\operatorname{dev}\widehat F
 -\widehat B\operatorname{tr}\widehat F}{\widehat E}.
 \tag{2.5}
\]

The pure amplitude direction \(\widehat F=\lambda\widehat Q\) cancels exactly.
Using \(|\widehat B|_F\le\sqrt{2/3}\) gives the claimed constant

\[
 1+\sqrt2.
 \tag{2.6}
\]

No missing Grönwall term was found.

## 3. Independent condition-number audit

For every symmetric \(X\),

\[
 |G^{-1}XG^{-\mathsf T}|_F
 \le\|G^{-1}\|_{\rm op}^2|X|_F,
 \tag{3.1}
\]

while for \(Q\succeq0\),

\[
 \operatorname{tr}(G^{-1}QG^{-\mathsf T})
 \ge\|G\|_{\rm op}^{-2}\operatorname{tr}Q.
 \tag{3.2}
\]

Therefore the quotient loss is \(\kappa_2(G)^2\). The independent audit
also minimized exactly over the scalar amplitude parameter in both frames for

\[
 G=\operatorname{diag}(k,k^{-1},1),
 \quad Q=\operatorname{diag}(1,\varepsilon,\varepsilon),
 \quad F=e_2\otimes e_2.
 \tag{3.3}
\]

It obtained

\[
 \lim_{\varepsilon\downarrow0}
 \frac{\rho_G}{\rho_0}=k^4=\kappa_2(G)^2.
 \tag{3.4}
\]

This correction matters: an unoptimized \(|F|/E\) example alone would not
have proved sharpness for the actual quotient used in the BV theorem.

For symmetric \(\Sigma\), the singular-value calculation independently gives

\[
 \kappa_2(G(t))
 \le\exp\int
 [\lambda_{\max}(\Sigma)-\lambda_{\min}(\Sigma)]dt.
 \tag{3.5}
\]

The fixed diagonal source takes equality. Thus the exponent in the report is
not an artifact of a coarse matrix norm.

## 4. Exact holonomy recomputation

The independent certificate used

\[
 A=(\log3)\operatorname{diag}(1,-1),
 \qquad
 C=(\log3)
 \begin{pmatrix}0&1\\1&0\end{pmatrix}.
 \tag{4.1}
\]

It verified

\[
 e^A=\operatorname{diag}(3,1/3),
 \qquad
 e^C=
 \begin{pmatrix}5/3&4/3\\4/3&5/3\end{pmatrix},
 \tag{4.2}
\]

and the chronological product

\[
 G_*=e^{-C}e^{-A}e^Ce^A
 =
 \begin{pmatrix}
 -119/9&-160/81\\
 160/9&209/81
 \end{pmatrix}.
 \tag{4.3}
\]

The following exact assertions all passed:

\[
 \det G_*=1,
 \qquad
 \operatorname{tr}G_*=-862/81,
 \tag{4.4}
\]

\[
 \operatorname{spec}(G_*)
 =\left\{
 \frac{-431\pm160\sqrt7}{81}
 \right\},
 \tag{4.5}
\]

\[
 G_*^{\mathsf T}G_*-G_*G_*^{\mathsf T}
 =\frac{2048000}{6561}
 \begin{pmatrix}1&1\\1&-1\end{pmatrix},
 \tag{4.6}
\]

and

\[
 G_*G_*^{\mathsf T}
 =\frac1{6561}
 \begin{pmatrix}
 1172641&-1575680\\
 -1575680&2117281
 \end{pmatrix}.
 \tag{4.7}
\]

After the three-dimensional block embedding, the independently recomputed
anisotropy is

\[
 \operatorname{tr}B^2
 =\frac{6553600}{9889449}
 =\frac23-\frac{13122}{3296483}.
 \tag{4.8}
\]

Four disjoint smooth unit-mass scalar pulses reproduce the same ordered
exponentials exactly; smoothing is not a numerical approximation.

## 5. Affine-relative identity

For \(Q\succ0\), the independent calculation gives

\[
 \frac d{dt}\log\det Q
 =\operatorname{tr}(Q^{-1}F)
 \tag{5.1}
\]

because \(\operatorname{tr}\Sigma=0\). It also verifies that

\[
 \operatorname{tr}(\widehat Q^{-1}\widehat F)
 =\operatorname{tr}(Q^{-1}F),
 \tag{5.2}
\]

and

\[
 \operatorname{tr}[(\widehat Q^{-1}\widehat F)^2]
 =\operatorname{tr}[(Q^{-1}F)^2].
 \tag{5.3}
\]

The determinant-normalized affine shape speed in the report follows. The
audit found no hidden condition-number factor in this SPD metric.

The literature check, however, confirms that the affine-invariant metric and
its congruence invariance are prior matrix geometry. The report correctly
claims only the NSE covariance placement and boundary analysis.

## 6. Rank and regularization boundary

The periodic shear

\[
 u=A_0e^{-\nu N^2t}\sin(Ny)e_1
 \tag{6.1}
\]

was checked directly:

- it is divergence free;
- its nonlinear term vanishes;
- \(\partial_tu=\nu\Delta u\);
- its vorticity has the fixed direction \(e_3\).

Therefore every nonzero scalar-filtered weighted covariance has rank one.
This is a genuine unforced periodic NSE boundary, not a matrix-only example.

For

\[
 Q_\varepsilon=Q+\varepsilon E I,
 \tag{6.2}
\]

the audit derives

\[
 F_\varepsilon
 =F+\varepsilon\dot E I-2\varepsilon E\Sigma.
 \tag{6.3}
\]

On the null-plane example in the producer, the affine-relative square of the
last term is exactly \(8\) for every \(\varepsilon>0\). The regularization
does not pass uniformly to the rank-deficient boundary.

## 7. Corrections imposed by the audit

Three corrections were required before PASS:

1. \(G'=\Sigma G\) must be called a **strain-only propagator**, not the
   physical deformation gradient. The latter uses \(\Sigma+W\), and viscous
   Eulerian--Lagrangian formulations contain additional commutators or
   stochastic averaging.
2. Sharpness had to be verified after the scalar-amplitude infimum defining
   \(\rho_G\), not only for \(|F|/E\).
3. The four-pulse holonomy is a rigorous smooth matrix history, but it has not
   been realized along one unforced finite-energy periodic NSE trajectory.
   Only the rank-one shear boundary has that exact PDE status.

The canonical report and producer contain all three corrections.

## 8. Final claim boundary

The audit supports the following statement:

> R0.70M proves an exact conditional pulled-shape estimate, a sharp
> \(\kappa_2(G)^2\) Euclidean obstruction, a smooth noncommutative zero-integral
> holonomy certificate, and an affine-relative SPD alternative whose failure
> at covariance rank loss occurs on an exact periodic NSE solution.

It does not support:

- a finite-energy unforced NSE realization of the holonomy loop;
- an energy-controlled bound for the pulled residual;
- a new continuation criterion;
- a weak-solution passage;
- finite-time blow-up or global regularity;
- a solution of the Millennium problem.

The next mathematically justified gate is a coercive multi-scale covariance
frame, tested first against exact shear and Beltrami families.
