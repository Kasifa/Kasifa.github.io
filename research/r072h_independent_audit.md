# R0.72H independent audit

**Date:** 2026-08-27

**Decision:** producer and independent routes pass. The finite calculations
corroborate the all-odd Rudin--Shapiro scaling, reciprocal-weight envelope,
real root correction, and moment-resolved sharpness. They do not prove the
analytic theorem.

## Independence of the two routes

The producer uses:

- Rudin--Shapiro polynomial recurrence;
- the original complex Fourier lattice;
- DOP853 after the scaling \(y=M^2x\);
- Simpson quadrature after \(y=z^3\);
- continuous scalar optimization for \(\Phi(a)\);
- truncation radius \(8M\).

The checker uses:

- the binary adjacent-\(11\) parity formula for the signs;
- the exact all-odd real gauge;
- RK45;
- Gauss--Legendre quadrature after \(y=z^3\);
- a dense logarithmic grid for \(\Phi(a)\);
- truncation radius \(9M\).

The routes share only the mathematical specification and the declared
parameter configuration.

## Configuration

\[
 M\in\{4,8,16,32,64\},\qquad
 r_j=2M+2j+1,\qquad
 a=\delta=\mu=X=1.
\]

The dynamic integral is evaluated through \(y=M^2x=12\). The
Rudin--Shapiro heat envelope beyond that point is exponentially small. The
producer uses 1001 transformed Simpson nodes; the checker uses 280
Gauss--Legendre nodes.

## Finite results

| \(M\) | producer \(\mathcal E_Q/M^2\) | checker \(\mathcal E_Q/M^2\) | producer \(Q_*/(M^{2/3}\log M)\) | producer \(m_*/(M^{7/3}/\log M)\) | evolved root residual |
|---:|---:|---:|---:|---:|---:|
| 4 | 0.996346 | 0.996346 | 1.63146 | 0.312649 | \(5.80\times10^{-17}\) |
| 8 | 0.999092 | 0.999092 | 1.22981 | 0.395616 | \(9.16\times10^{-18}\) |
| 16 | 0.999774 | 0.999774 | 1.04259 | 0.456447 | \(3.69\times10^{-18}\) |
| 32 | 0.999943 | 0.999943 | 0.933373 | 0.503037 | \(2.60\times10^{-18}\) |
| 64 | 0.999986 | 0.999986 | 0.861581 | 0.539901 | \(8.67\times10^{-19}\) |

The largest relative discrepancy between the routes, over
\(\mathcal E_Q,Q_*,m_*,\widetilde m_*\), and the normalized root slope, is

\[
 3.31\times10^{-6}.
\]

At \(M=64\),

\[
 \frac{\mathcal E_Q}{M^2}=0.9999859,\qquad
 \frac{\sqrt{M\,m_*Q_*}}{\mathcal E_Q}=0.6820421,
\]

and

\[
 \frac{\mathcal E_Q/Q_*}{M^{4/3}/\log M}=1.16064.
\]

The last two ratios remain bounded and stabilize across the sweep. This is
the numerical signature of moment-resolved saturation together with
action-only divergence.

The root correction is real in both routes. At \(M=64\),

\[
 \zeta_M=-3.0001794\times10^{-4},
 \qquad
 M^2|\zeta_M|=1.22887,
\]

and

\[
 \frac{|h(\tau_M)|}{M}=1.06263.
\]

The normalized root slope increases over the finite sweep toward its
nonzero asymptotic value. Small \(M\) is not yet in that asymptotic regime
because \(r_j^2\tau_M=O(M^{-1})\) has a large constant.

## Envelope check

The producer optimizes

\[
 \Phi(a)=\sup_{0<s\le1}
 \frac{s^{1/3}e^{-as}}{1+\log(1/s)}
\]

for 120 values \(10^{-4}\le a\le10^7\). Relative to

\[
 (1+a)^{-1/3}[1+\log(2+a)]^{-1},
\]

the observed ratio remains between \(0.4270\) and \(1.6931\). The checker
recomputes every carrier value on an unrelated dense \(u=-\log s\) grid.

## Preserved failed attempts

The first producer run correctly returned "failed". Its analytic quantities
and roots were already consistent, but the pass contract incorrectly required
every small-\(M\) normalized root slope to exceed \(0.5\), and one finite-size
profile-slope tolerance was too narrow. The result, raw data, progress log,
and resource log are retained under
"producer-attempt1-failed-*".

The second run extended the sweep to \(M=64\), then stopped in the final
check because strict pairwise iteration was mistakenly applied to two lists
whose lengths differ by one. Its progress and resource streams are retained
under "producer-attempt2-failed-*". The arithmetic was not reused to bypass a
failed mathematical check; the checking code was corrected and the entire
sweep was rerun.

## What the audit establishes

The finite evidence supports:

1. all-odd carriers preserve the exact real correction;
2. \(\mathcal E_Q\) has the predicted \(M^2\) scale;
3. \(Q_*\) and \(m_*\) carry reciprocal logarithmic factors;
4. the action-only normalized ratio grows;
5. the moment-resolved ratio stays bounded;
6. the exact interior root residual is at roundoff scale;
7. two different solvers, gauges, sign generators, quadratures, and
   truncations agree.

It does not establish:

1. an asymptotic theorem from five values of \(M\);
2. an infinite-lattice error theorem;
3. a full physical \(D^{1/3}\Lambda_{1,*}\) counterexample;
4. any statement about general three-dimensional Navier--Stokes regularity.

The analytic estimates in r072h_report-source.md carry those claims; the
audits are corroborating evidence only.
