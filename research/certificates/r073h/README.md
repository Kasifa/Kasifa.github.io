# R0.73H finite harmonic-response certificate source

This package computes the first three launch-amplitude coefficients for the
finite Galerkin perturbation equation around the R0.73G heat-decaying shear.
It reserves `epsilonNu` for \(\Lambda^{-1}\) and uses \(\rho\) for launch
amplitude:

\[
v_N(\theta;\rho)=\rho V_1+\rho^2V_2+\rho^3V_3+O(\rho^4),
\qquad \theta=d/\epsilon_\nu.
\]

The primary producer uses generic physical-velocity Fourier convolution and
modewise Leray projection.  It advances

\[
\begin{aligned}
V_1'&=A_{\epsilon_\nu}V_1,\\
V_2'&=A_{\epsilon_\nu}V_2-\frac{\epsilon_\nu}{4}B(V_1,V_1),\\
V_3'&=A_{\epsilon_\nu}V_3-\frac{\epsilon_\nu}{4}
\{B(V_1,V_2)+B(V_2,V_1)\}.
\end{aligned}
\]

It resolves the exact support ledger

- \(V_1\): \(K_z=\pm1\);
- \(V_2\): \(K_z=0,\pm2\);
- \(V_3\): \(K_z=\pm1,\pm3\).

The cubic target is additionally split into the path through the generated
zero row and the path through the doubled rows.  Raw complex coefficient
snapshots are stored in a deterministic NPZ archive; CSV files contain
human-auditable norms, signed alignments, cutoff comparisons, and step
comparisons.

`independent_validate.py` does not import the producer.  It reconstructs the
frozen matrix from the Orr--Sommerfeld Fourier coefficients and evolves the
same triangular hierarchy in scalar vorticity on an alias-free physical grid,
using FFT differentiation, Biot--Savart recovery, and an independently written
nonlinearity.

The same package also contains a separate continuum-proof subcertificate.
`exact_q2_certificate.py` verifies the \(|m|\le4\) Fourier block by exact
`Fraction` \(LDL^*\) pivots, then records the analytic tail, cross-block,
Schur, profile-time perturbation, and rate margins.  The independent script
uses positive leading principal minors and fraction-free Bareiss determinants;
it does not call or reproduce the primary LDL routine.  This finite exact
rational calculation is a subcertificate used inside a continuum coercivity
argument.  It is not a finite Galerkin approximation of the PDE.

## Source-before-run rule

The formal commands require a full source commit.  Every source file and the
configuration must match its regular Git blob at that commit.  Formal output
is accepted only in this directory.  Before the source commit exists, use
`--smoke` with a temporary directory; smoke mode is forbidden from writing
formal results here.

The grid is pilot-informed.  The extra \(\epsilon_\nu=7.5\times10^{-5}\)
case is a frozen holdout with prediction ranges recorded before its formal
execution.  A failed holdout remains a valid negative result and must not be
silently retuned.

## Evidence boundary

The amplitude hierarchy and its \(K_z\)-parity are exact algebraic identities.
All reported sizes, slopes, compensated ratios, cutoff agreement, and holdout
outcomes are finite IEEE-754 binary64 diagnostics.  The endpoint \(d=0.01\)
is not certified to lie inside the existential analytic window from R0.73F.
The package supplies no Fourier-tail enclosure, no control of fourth and
higher amplitude orders, no uniform Taylor radius, and no continuum
harmonic-resolved semigroup theorem.  It does not establish natural-seed
order-one departure.  The selected launch remains planar and has no
three-dimensional vortex stretching.  Nothing here resolves the Clay
Navier--Stokes problem.
