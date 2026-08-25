# Figure contract

## Analytical question

Can the joint amplitude--direction heat cancellation convert the available
physical-time heat volume into the \(K^{-2}\)-weighted BV budget, or does an
exact trace-to-volume gap remain?

## Takeaway

The joint identity preserves a real cancellation, but heat volume alone is
two frequency powers too small.  The gap occurs in a zero-face linear model
and in a zero-entry global-smooth 2D3C NSE family for one fixed smooth radial
two-ring multiplier.  Cutoff refresh is a separate positive cost.

## Chart map

| Panel | Question | Form | Data | Supported statement |
|---|---|---|---|---|
| A | Can common heat create variation with zero outer faces? | Single-series line with exact peak | 151 pulse samples plus one exact peak | \(q(0)=q(\infty)=0\), \(q_*>0\) |
| B | How does weighted BV compare with weighted heat volume? | Log--log exact line and points | Nine dyadic frequencies | ratio \(=cK^2\), no fitted exponent |
| C | Does a true NSE family realize an interior pulse? | Dual-axis paired profiles with line-style distinction | 151 closed-form limiting samples plus one test point | \(A_0(0)=0<A_0(\theta)\), \(G_0>0\) |
| D | What is the cost of changing the two-cell cutoff? | Exact curve with endpoint bracket | 101 modulation samples and two endpoints | \(\Delta_{\rm ref}=3/28\) for \(U=1\) |

## Surface

- Static Matplotlib journal figure.
- Double-column width: 178 mm.
- Height: 108 mm.
- PDF and SVG vector exports.
- PNG export at 600 dpi.
- Print-size and grayscale QA previews at 254 dpi.

## Palette and non-color encoding

- Hard two-root cap: navy and rust plus charcoal/grey neutrals.
- Every comparison also uses line style, marker fill, marker shape, axis
  separation, or direct annotation.
- White background; quiet grey grid; no gradients.

## Data sufficiency

- Panel A: 151 ordered points on \(0\le\tau\le3\), plus the exact extremum.
- Panel B: nine dyadic frequencies \(1\le K\le256\); the exponent is exact,
  not estimated from sample count.
- Panel C: 151 ordered points on \(0\le\theta\le0.6\), plus the exact
  \(\theta_*=(\log2)/10\) test point.
- Panel D: 101 ordered points on \(0\le\delta\le1\), plus exact endpoints.
- All data are deterministic closed-form formula evaluations.

## Claim boundary

Panels A--B are a common-heat Hilbert model with external \(Y=1\).  Panel C
is a rigorous fixed-window asymptotic of an exact global-smooth 2D3C NSE
family, not a numerical PDE trajectory, and uses a specially selected fixed
radial two-ring multiplier.  Panel D permits changing the analytical
partition and therefore does not contradict a fixed or quantitatively
transported partition.  No panel proves or disproves the full face-paid
weighted-BV target for the preselected broad frame.
