# R0.71W independent computational audit

**Audit date:** 2026-08-26

## Independence contract

Three separate programs accompany the analytic report.

1. research/r071w_exact_audit.py is the 90-digit producer. It evaluates
   the closed response interpolation, the seed/background tangent envelope,
   the restored-amplitude heat/shear ledger, and a deterministic
   full-frequency rotational upper bound.
2. research/r071w_independent_audit.py does not import the producer and
   does not read research/certificates/r071w/result.json. It rebuilds the
   response and all leading ledger powers with NumPy binary64 and
   log-sum-exp heat evaluation.
3. research/r071w_truncated_coset_audit.py is a separate nonlinear finite
   Fourier-coset corroboration. It solves the retained advection--diffusion
   system with DOP853 and solves the four real prescribed-root equations with
   Levenberg--Marquardt continuation. It uses neither of the first two
   programs.

The two algebraic programs share only the mathematical specification in
research/r071w_report-source.md. The truncated program additionally shares
the fixed numerical parameters declared in its JSON output.

## Producer and independent leading-ledger agreement

For the formal example

\[
 \nu=0.02,\quad d=8,\quad K_y=K_z=1,\quad Q=4,\quad
 \tau=(0.1,0.2),\quad \alpha=\frac32,
\]

the producer and independent reconstruction both pass. The producer uses
90-digit arithmetic; the independent program uses binary64. Their fitted
powers over the declared asymptotic range are:

| Quantity | Predicted | Producer | Independent |
|---|---:|---:|---:|
| rescaled IFT parameter \(\delta_q\) | \(-0.5\) | \(-0.5000000000\) | \(-0.5000000000\) |
| leading atom proxy | \(+1\) | \(+0.9999999998\) | \(+0.9999999998\) |
| rotational upper bound | \(-1\) | \(-0.9999999997\) | \(-0.9999999997\) |
| atom / complete-ledger proxy | \(+1\) | \(+1.0025764340\) | \(+1.0025764340\) |
| leading root enstrophy | \(+5\) | \(+5.0000000002\) | \(+5.0000000002\) |

The conservative rotational bound crosses the fixed \(\nu^2\) baseline only
at large \(q\), so the certificate extends the deterministic dyadic range
before fitting the final complete-ledger ratio. This is an asymptotic
visibility choice, not a change of parameters.

Both programs also retain the R0.71V seed/background sweep. It confirms
that the tangent coefficient **before restoring the physical shear
amplitude** is \(O(q^{-2})\) relative to
\(\mathcal R_Y\nu^2\). R0.71W multiplies that coefficient by the actual
shear-amplitude square. Keeping these two rows in the same certificate
prevents the old tangent envelope from being misread as a rejection of
amplitude doping.

## Nonlinear retained-coset corroboration

The truncated program uses

\[
 q=256,512,1024,2048,4096,\qquad R=40,
\]

with positive-\(K_z\) coset indices \(r\in[-R,R]\). It fixes \(z_1=1\)
and solves for \(z_2,\ldots,z_5\) so that the real and imaginary target
coefficients vanish at both prescribed scaled times.

Across the continuation:

- the maximum four-component root residual is
  \(5.20\times10^{-18}\);
- the minimum normalized prescribed-root slope stays above the encoded
  simplicity threshold;
- the second-root atom proxy has fitted power \(+1.005713\);
- the full retained-coset \(\dot H^{-1}\) rotational charge has fitted power
  \(-1.002509\);
- their ratio has fitted power \(+2.008222\).

The rotational calculation reconstructs the entire retained convolution
\(-v f_z\) and sums its \(\dot H^{-1}\) weight over all retained output
modes. It is not a selected-target-shell charge.

At \(q=1024\), the program repeats the solve at
\(R=15,30,60\) and compares it with \(R=40\). The largest relative
difference among the second-root slope, atom, and rotational charge is
\(1.15\times10^{-13}\); the root parameters agree within the much looser
encoded \(2\times10^{-6}\) tolerance. An analytic exponential tail bound
also makes the omitted large-scaled-time charge negligible relative to the
computed quadrature.

## What the computation does not certify

No finite computation proves:

1. convergence of the Fourier truncation to the infinite-lattice solution;
2. the uniform Dyson bounds or the divided-map implicit-function theorem;
3. exact continuum roots or their continuum slope lower bound;
4. the nonlinear scalar-gradient and enstrophy estimates on the fixed
   physical interval;
5. the full continuum projected-\(L\) upper bound;
6. any continuation criterion, singularity, or global regularity result.

Those are analytic claims in Sections 4--8 of
research/r071w_report-source.md. The machine-readable results are:

- research/certificates/r071w/result.json;
- research/certificates/r071w/independent-result.json;
- research/certificates/r071w/truncated-coset-result.json.
