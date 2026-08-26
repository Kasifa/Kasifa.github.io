# Figure contract: R0.71U modular recurrence packing

## Analytical question

Can one fixed compact target annulus of a genuine smooth unforced NSE
trajectory return to zero at three prescribed positive times, and what happens
to the associated jet atoms along the small implicit-function curve?

## Audience and decision

The figure is for a mathematical-fluid-dynamics paper. It lets a reader
separate four statements at a glance: prescribed roots, first-order complex
passages, quadratic atom collapse, and finite-cutoff corroboration. It must
not suggest that truncation numerics prove the analytic IFT or the second-time
jet sampling theorem.

## Data and evidence classes

- Panel A: primary \(m_{\rm cut}=24\) DOP853 trajectory and freshly shot roots.
- Panel B: lossless re-expression of local Panel-A complex coefficients.
- Panel C: five independent shooting cases in \(p_1\), plus exact one-shell
  algebra \(J=P/4\).
- Panel D: fixed-parameter cutoff sweep and separate sparse \(m_{\rm cut}=36\)
  re-shoot; the annulus gap is analytic integer arithmetic.

No stochastic data, fitted physical parameter, DNS output, or external source
data appear. Log-log exponents in Panel C are descriptive fits to five finite
samples; the analytic report supplies the \(O(p_1^2)\) statement.

## Visual encoding

- Static 2 by 2 journal figure, 178.05 mm wide and 134.11 mm high.
- Paper background, dark ink, muted blue and ochre; no rainbow scale.
- Solid, dashed, and dotted lines plus circle, square, and diamond markers
  preserve meaning in grayscale.
- Panel A states its unequal real/imaginary ordinate multipliers explicitly.
- Panel B states its unequal complex-plane coordinate multipliers explicitly;
  arrows encode time direction.
- Panels C and D use logarithmic ordinates and label reference/floor behavior.
- A small top-right blossom is decorative and carries no data encoding.

## Required labels and boundaries

- Title: “Prescribed returns in a modular exact-NSE lattice”.
- Subtitle: \(\nu,K,L,d,p_1\), primary cutoff, independent cutoff.
- Footer: finite Fourier–Galerkin corroboration, PDE time stepping, not DNS,
  no continuum truncation proof.
- Caption: analytic reduction and modular isolation are not inferred from the
  numerical sweep; Panel C is not the \(C_{tt}\) payment ledger.

## Outputs and QA

- vector PDF and SVG;
- 600 dpi archival PNG;
- color, true-grayscale, and independent Poppler PDF-render previews;
- inspection at final 178 mm print width;
- automatic producer and independent validation with checksums.
