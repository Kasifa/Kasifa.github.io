# Figure R0.71U-1: modular recurrence and atom collapse

This package archives the formal journal figure that accompanies the R0.71U
recurrence theorem. The analytic result uses the exact invariant NSE class

\[
u=(f(y,z,t),0,v(y,t)),\qquad
v_t=\nu v_{yy},\qquad
f_t+vf_z=\nu(f_{yy}+f_{zz}).
\]

The computation integrates a **finite** modular Fourier lattice. It is a
reproducible corroboration of the analytic construction. It is not DNS, a
continuum Galerkin convergence proof, or a numerical proof of the implicit
function theorem.

## Fixed instance

- \(\nu=0.02\), \(K=L=1\), \(d=8\), \(N=3\);
- \(n_\ell=8\ell\), \(\ell=1,\ldots,7\);
- \(A_\ell=i\) for \(\ell\le4\), and \(A_\ell=1\) otherwise;
- prescribed times \((0.01,0.03,0.07)\);
- \(p_1=0.002\), with \(p_2,\ldots,p_7\in\mathbb R\) re-solved;
- primary cutoff \(m_{\rm cut}=24\); independent sparse refinement cutoff 36;
- SciPy DOP853 with the tolerances in config.json.

The primary shot is

\[
p=(0.002,-0.00491591839171114,0.00436374315345854,
-0.00146120943289924,4.09141700069\times10^{-5},
-1.00583426426\times10^{-4},6.24915978147\times10^{-5}).
\]

Its maximum prescribed-time target residual is
\(3.89\times10^{-20}\). The three slope magnitudes are
\(6.604\times10^{-6}\), \(9.722\times10^{-6}\), and
\(3.892\times10^{-5}\). The independently re-shot cutoff-36 parameters
differ by at most \(6.08\times10^{-18}\); its maximum slope difference from
the primary result is \(2.73\times10^{-13}\) in relative terms.

## What each panel supports

- **A:** real and imaginary target traces return to zero at all three
  prescribed times, with nonzero RHS slopes.
- **B:** the same data shown as three directed complex-plane passages through
  the origin.
- **C:** five separate shooting runs along the \(p_1\) coordinate. Their jet
  atoms have sampled log-log exponents \(2.008,2.001,2.000\). Open markers
  check the exact one-shell identity \(J=P/4\), where
  \(P=\kappa_*^{-6}\|C_{*,t}\|_2^2/Y\). This panel uses the permitted
  \(O(p_1^2)\) boundary; it is not a numerical ledger for the stronger
  \(C_{tt}\) payment in the second-time-jet theorem.
- **D:** fixed-parameter cutoff and residual comparison, plus a fresh sparse
  cutoff-36 reshoot. The modular isolation statement
  \(R_*=3<d-K=7\) and the next radius \(\sqrt{50}\) are exact arithmetic,
  not conclusions inferred from the cutoff sweep.

## Reproduction

Run the commands in command.txt from the repository root. They rebuild the
primary and independent raw results, plot data, validations, vector and raster
figures, QA previews, draft manifest, and checksum ledger. The calculation
is deterministic and uses no random seed.

manifest.json remains draft because the source and certificate commit hashes
are intentionally pending. The package is otherwise complete and QA checked.
No Git commit or public-page edit is part of this package build.

## Principal files

- modular_solver.py, primary-results.json: primary lattice and shooting;
- independent_solver.py, independent-results.json: separate sparse-shift
  implementation and cutoff-36 re-shoot;
- data.csv, figure-data-metadata.json: plot-ready data and evidence map;
- validate_data.py, independent_validate.py: producer and standalone QA;
- plot.py, figure.pdf, figure.svg, figure.png: journal figure;
- qa-original.png, qa-grayscale.png, qa-pdf.png, qa-report.md: visual QA;
- progress.ndjson, resource-log.ndjson: timestamped run monitoring;
- manifest.json, SHA256SUMS: provenance and integrity records.
