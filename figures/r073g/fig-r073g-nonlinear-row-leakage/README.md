# R0.73G formal figure package

This directory contains the paper-ready rendering of the finite diagnostic
supporting R0.73G.  The exact nonlinear theorem is proved analytically in
`research/r073g_nonlinear_shadowing_proof.md`; this figure does not carry that
proof.

Run from the repository root with the bundled scientific Python runtime:

```text
python figures/r073g/fig-r073g-nonlinear-row-leakage/plot.py --deps <python-packages>
```

The package writes vector PDF and SVG plus a 600 dpi PNG at 178 mm width.
`results.json` binds the experiment inputs and generated outputs by SHA-256.
The final metadata seal additionally binds the analytic source commit,
experiment/figure commit, and formal certificate commit.
