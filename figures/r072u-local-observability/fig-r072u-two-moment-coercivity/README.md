# Figure R0.72U — exact two-moment coercivity calibration

This directory is intentionally at **source stage**. It contains the immutable
figure contract, configuration, entry point, and strict validator, but no
rendered figure, sampled data ledger, manifest, QA image, or checksum ledger.

The planned three-panel figure is analytic rather than a PDE simulation:

- Panel A: the compactly supported rational probe
  \(\rho=(315/256)(1-X^2)^4\mathbf 1_{[-1,1]}\) and \(X\rho\), with
  \(\mu_2=1/11\) and \(\mu_4=3/143\).
- Panel B: \(K_c(s)=3/143+6(c+s)/11\) for \(T=1\), including the sufficient
  fixed-sign threshold \(|c|\ge 27/13\).
- Panel C: the separate exact fixed-gauge inviscid identity
  \(3z^2+4/5\), whose unit-block floor is \(4/5\).

The whole-line block contraction is labelled **OPEN**. The figure does not
claim a machine-checked bounded-chart functional estimate, periodic transfer,
nonlinear closure, or a solution of the Clay problem.

The only command appropriate before the source commit exists is:

```sh
python3 scripts/generate_r072u_figure.py --self-test
```

That command constructs the analytic rows and drawing scene in memory and
writes nothing. Formal rendering is deliberately deferred until a formal,
source-bound R0.72U certificate has been created in a later commit stage.
