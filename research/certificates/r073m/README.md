# R0.73M finite prescribed-action diagnostic

This package checks the finite-dimensional analogue of the R0.73M
prescribed-action recoding at the fixed profile-time endpoint

\[
D_*=1/450,
\qquad T_*=D_*/4=1/1800,
\qquad d=4t.
\]

It combines two calculations that must remain distinct.

1. The selected finite kinetic evolution supplies its actual gain
   \(G_{N,\varepsilon}\).
2. The same fixed contour is evaluated at \(\varepsilon=0\) to form the
   **finite inviscid action proxy**

   \[
   A_{N,0}=\int_0^{D_*}\lambda_{N,0}(d)\,\mathrm dd.
   \]

The prescribed-action finite prefactor is therefore

\[
g^{(0)}_{N,\varepsilon}
=G_{N,\varepsilon}\exp(-A_{N,0}/\varepsilon).
\]

The existing R0.73L diagnostic instead normalizes by the viscous finite
action \(\int\lambda_{N,\varepsilon}/\varepsilon\).  This package computes
both quantities under different field names.  It never renames or reuses the
viscous action as the inviscid proxy.

## Harmonic hierarchy

The physical-velocity producer evolves

\[
v_N(\eta)=\eta V_1+\eta^2V_2+\eta^3V_3+O(\eta^4)
\]

with the exact finite support ledger

- \(V_1\): \(K_z=\pm1\);
- \(V_2\): \(K_z=0,\pm2\);
- \(V_3\): \(K_z=\pm1,\pm3\).

At the endpoint, the recorded coefficients are normalized by the actual
physical linear gain, not by an exponential proxy:

\[
a_N=V_1/G_{N,\varepsilon},\qquad
b_N=V_2/G_{N,\varepsilon}^2,\qquad
c_N=V_3/G_{N,\varepsilon}^3.
\]

The endpoint archive stores the five raw paths
`V1`, `V2_Kz0`, `V2_KzPlusMinus2`, `V3_via_Kz0`, and
`V3_via_KzPlusMinus2`.  No fourth-order coefficient or full nonlinear
Galerkin trajectory is computed.

## Independent implementations

`independent_linear.py` does not import the primary producer.  It builds the
matrix directly from the Orr--Sommerfeld Fourier coefficients, advances the
linear orbit by midpoint matrix-exponential products, and independently
integrates both the viscous and inviscid selected actions.

`independent_hierarchy.py` also does not import the primary producer.  It
uses scalar vorticity, independent Biot--Savart recovery, alias-free physical
grids, FFT products, and fixed-step RK4 to reconstruct selected endpoint
coefficient arrays.

`exact_identities.py` checks the endpoint and nonlinear rate-margin
identities with Python `Fraction` arithmetic.  It does not accept a
floating-point reconstruction of those equalities.

## Source-before-run rule

Formal output is accepted only after these source files have been committed.
Every formal command requires the full lowercase source commit, verifies that
the working source is byte-identical to that commit, and verifies the frozen
SHA-256 bindings to the R0.73H and R0.73L algorithms.  Smoke mode writes only
to a temporary directory outside this package.

The protocol `research/r073m_numerical_protocol.md` is part of `SOURCE_FILES`.
It must be committed in the same source commit and every formal program checks
that its current bytes match that commit.

The primary monitor filenames are frozen as `primary_progress.ndjson` and
`primary_resources.ndjson`.  The two independent programs use
`independent_linear_progress.ndjson`, `independent_linear_resources.ndjson`,
`independent_hierarchy_progress.ndjson`, and
`independent_hierarchy_resources.ndjson`.

Run the commands recorded in `command.txt` from the repository root.

## Evidence boundary

All values produced here are finite IEEE-754 binary64 diagnostics.  In
particular:

- \(A_{N,0}\) is a finite action proxy, not the continuum action
  \(\mathcal A_*\);
- cutoff agreement is not a Fourier-tail proof;
- bounded observed values of \(g^{(0)}_{N,\varepsilon}\) do not prove a
  prefactor limit or the continuum two-sided theorem;
- the finite \(a_N,b_N,c_N\) hierarchy does not prove a uniform Taylor
  radius or the fourth-order continuum remainder estimate;
- no full nonlinear Navier--Stokes trajectory, transverse three-dimensional
  closure, finite-time singularity, or Clay conclusion is computed here.
