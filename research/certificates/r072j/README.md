# R0.72J mixed-parity finite-audit bundle

This bundle records the producer, independent, and cross-route finite audits
for the genuinely non-bipartite carrier block

\[
S_R=\{R,R+1,\ldots,3R-1\},\qquad N=2R,
\qquad \delta=0.05R.
\]

Every carrier coefficient is one.  The aligned launch places
\(i/\sqrt2\) at every signed carrier.  An independently evolved \(e_0\)
column corrects one complex target root at \(\tau=R^{-3}\), and the corrected
launch is normalized to \(\|F(0)\|_2^2=N\).

## Exact combinatorial checks

The positive ordered relations \(a+b=c\) in this block and the associated
signed ordered triangles satisfy

\[
A_R=\frac{R(R+1)}2,
\qquad T_R=6A_R=3R(R+1).
\]

Both implementations enumerate these relations independently.  Since
\(T_R>0\), the carrier Cayley graph contains a triangle and is not bipartite.
For the uncorrected aligned launch they also recover

\[
|P_0V^2F(0)|=\frac{T_R}{\sqrt2}.
\]

At \(R=64\), `signedTriangles = 12480` and
`uncorrectedB0Abs = 8824.692629208112`.

## Producer route

- source: `research/r072j_exact_audit.py`;
- operator: complex Fourier shifts implemented by independent array slices;
- integrator: SciPy DOP853 in \(y=R^2x\);
- quadrature: 1201-point composite Simpson rule after \(y=z^3\);
- truncation radius: \(8R\);
- finite sizes: \(R=4,8,16,32,64\).

All declared checks pass.  The last-three-size log slopes are

- `deltaIntegralAbsHB`: `1.9501881021393963`;
- `normalizedTrueCubic`: `-0.7370277418337389`.

Thus this finite family is consistent with a raw true-cubic scale \(R^2\)
and a physical normalized scale \(R^{-2/3}\).  At \(R=64\),

- `criticalQ = 1141.625196724164`;
- `deltaIntegralAbsHB = 69.21663850231755`;
- `normalizedTrueCubic = 1.0386272881747376e-6`;
- `normalizedMeasuredBvUpperProxy = 0.002033248207738247`;
- `evolvedRootResidual = 3.035766201128069e-18`.

Here `normalizedTrueCubic` means
\(2\theta[\delta\int|hP_0V^2F|]/[D^{1/3}(1+\theta Q_*)]\), including the
factor two with which the cubic row enters the measured BV upper proxy.

The exact finite exposure is

\[
2\delta\sum_{r=R}^{3R-1}r^{-2},
\]

which tends to \(4\gamma/3\).  At \(R=64\) it equals
`0.06736502921960838`, with relative error `0.010475438294125713` from
the limit.

## Independent route

- source: `research/r072j_independent_audit.py`;
- operator: an explicit directed edge list with destination accumulation;
- integrator: SciPy RK45 in \(y=R^2x\);
- quadrature: 260-point Gauss--Legendre after \(y=z^3\);
- truncation radius: \(9R\);
- triangle counter: signed ordered pair-sum `Counter`;
- profile envelope: independent dense logarithmic grid.

The independent result also passes every declared check.  At \(R=64\),

- `criticalQ = 1141.6262732647224`;
- `deltaIntegralAbsHB = 69.21663850219481`;
- `normalizedTrueCubic = 1.0386272843805003e-6`;
- `evolvedRootResidual = 2.7870376410284506e-14`.

## Cross-route agreement

`crosscheck.json` is generated only after both full calculations finish.  It
does not feed producer values into the independent calculation.  Across the
five common sizes, its largest relative discrepancies are

| Quantity | Maximum relative discrepancy |
|---|---:|
| critical action \(Q_*\) | `1.5332219747631151e-6` |
| \(\delta\int|hP_0V^2F|\) | `2.9406301718957877e-12` |
| mixed row | `3.972163143457586e-12` |
| normalized true cubic | `7.280337702150978e-9` |
| exact-root slope \(|h(\tau)|\) | `6.30135148739205e-12` |

## Boundary

This is binary64 finite evidence.  It constructs one exact complex root and
does not enumerate all temporal roots.  The real-valued Rolle complete-root
corollary does not apply to this coherent complex launch.  The measured BV
quantity is therefore labeled an upper proxy, not a complete-root ledger.
The finite slopes do not by themselves prove asymptotics, and this special
carrier block does not cover all mixed-parity sets or imply a general
Navier--Stokes regularity result.

Run the commands in `command.txt` from the repository root.  Rebuild
`SHA256SUMS` only after every other file in this directory is final.
