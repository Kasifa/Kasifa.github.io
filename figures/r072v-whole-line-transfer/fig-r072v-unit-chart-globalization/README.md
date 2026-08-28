# R0.72V unit-chart globalization figure

This source-only package specifies the formal R0.72V journal figure. It
contains analytic presentation curves and the exact structural chain used by
the proof:

- the adaptive moment floor
  \(\kappa(\theta)=(5/6292)\cos^2\theta+(1/44)\sin^2\theta\);
- the translated-cell coefficient relation
  \(b=a^2/3+6c\), with \(a=3k\), \(k\in\mathbb Z\);
- the disjoint-cell \(H^{-1}\) direct sum, whole-line graph estimate, and
  energy-solution contraction implication.

No PDE solve, simulation, fitted curve, empirical estimate of \(C_T\), or
random sampling is performed. The optional curve
\(r=s/(1+s)\), \(s=C_T^2/T\), is a presentation of the exact algebraic
contraction formula only; it does not assign a numerical value to \(C_T\).

The only command permitted before the source-bound formal certificate exists
is:

    python3 scripts/generate_r072v_figure.py --self-test

That command creates the analytic rows and drawing scene in memory and writes
nothing. Draft and formal rendering are certificate-gated. Formal rendering
also requires a distinct clean certificate commit, explicit visual inspection,
and absent output targets.
