# R0.73E deterministic analytic certificate

This package binds the R0.73E fixed-positive-half-plane, top-cluster
relative-dichotomy, logarithmic transfer, and complete-row polynomial no-go
theorem to source commit `803279d72c24a54db27c40dcdad97593636788fc`.

The primary generator checks the proof, problem freeze, independent analytic
audit, literature boundary, gap matrix, report, finite diagnostic, independent
finite recomputation, and formal-figure validation.  A separate stdlib-only
script reparses those sources and recomputes exact status and numerical
sentinels without importing the primary generator or reading
`certificate.json`.  The comparator requires both paths to pass.

Exactly nine analytic claims are sealed as `CLOSED`.  Seventeen stronger
claims remain explicitly `OPEN`.  The finite Fourier evidence and the formal
figure are fail-closed: neither can certify a continuum spectrum, a uniform
continuous-time bound, a nonlinear Navier--Stokes theorem, or the Clay
problem.
