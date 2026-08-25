# R0.71D exact-certificate bundle

This directory archives the exact audits for the R0.71D material heat-tent
boundary.

## Decision locked by the bundle

The producer and independent checker verify the following facts.

1. The heat extension

   \[
   W_j=e^{s\Delta}T_j\omega
   \]

   satisfies the complete shell equation

   \[
   (\partial_t+u\cdot\nabla-\nu\partial_s)W_j
   =e^{s\Delta}T_j(S\omega)
   +[u\cdot\nabla,e^{s\Delta}T_j]\omega.
   \]

   Its integrated tent ledger includes the physical-time faces, vertical
   heat faces, stretching source, transport-filter commutator, and cutoff
   motion with exact signs.
2. The smooth exact NSE shear

   \[
   u=(0,A k^{-1}e^{-\nu k^2t}\sin(kx_1),0),\qquad
   \omega=(0,0,Ae^{-\nu k^2t}\cos(kx_1))
   \]

   admits the pointwise-material partition

   \[
   \phi_\pm=\frac12(1\pm\rho\cos(2kx_1)).
   \]

3. Its two child ledgers satisfy

   \[
   \beta_++\beta_-=0,
   \qquad
   \frac{(\beta_-^+)^2}{D_-}
   =\frac{\nu^2A^2k^2\rho^2}{2(2+\rho)}e^{-2\nu k^2t}>0.
   \]

   After division by parent enstrophy, the defect is

   \[
   \frac{\delta_k}{Y}=\frac{\nu^2\rho^2}{2+\rho}k^2.
   \]

4. On \(\tau_k=\theta/(\nu k^2)\),

   \[
   \frac{B_-^2}{\overline D_-}
   =\int_0^{\tau_k}\frac{(\beta_-^+)^2}{D_-}\,dt.
   \]

   The R0.71C signed time-box Cauchy inequality is exactly saturated and the
   dimensionless cost is independent of \(k\).
5. A bottom localization-filter commutator has an order-one high-mode
   coefficient at the active scale.  It cannot be discarded as a lower-order
   term without a separate estimate.
6. A second embedded-two-dimensional exact NSE family independently checks
   the same critical heat-flux mechanism with nonzero pressure and zero
   integrated cutoff-transport contribution.

These facts reject a universal subcritical gain from material-tent geometry
or viscous heat transport alone.  They do not exclude a specifically
three-dimensional nonlinear sign or depletion mechanism.

## Files

- `result.json` - canonical sorted JSON emitted by the producer;
- `independent-result.json` - standalone exact reconstruction;
- `command.txt` - exact reproduction commands;
- `environment.txt` - pinned runtime and dependency record;
- `SHA256SUMS` - hashes for every archived payload and source dependency;
- `../../r071d_exact_audit.py` - producer;
- `../../r071d_independent_audit.py` - independent checker;
- `../../r071d_report-source.md` - analytic report;
- `../../r071d_literature_audit.md` - primary-source claim ledger;
- `../../r071d_independent_audit.md` - independent manual audit.

## Analytic boundary

The programs certify the explicit Fourier averages, heat-extension boundary
identity, material partition, parabolic equality case, and bottom
commutator.  The general smooth tent identity, moving-domain formula,
pressure integration by parts, cutoff legality boundary, and literature
comparison are given analytically in the report.

The bundle does not prove that every adaptive tent norm diverges, does not
rule out nonlinear depletion, and proves no singularity, unconditional
regularity theorem, or Millennium-problem solution.

No DNS, stochastic search, GPU, or DGX resource is used.
