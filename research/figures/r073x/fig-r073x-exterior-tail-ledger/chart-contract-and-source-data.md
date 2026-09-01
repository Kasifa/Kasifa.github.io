# R0.73X chart contract and source data

## Analytical question

Which spatial tail weights are actually licensed by the R0.73X proofs, and why
can a weighted \(L^2\) mass raised to the \(3/2\) power not replace the
critical Gaussian \(L^3\) velocity row as a purely functional estimate?

## Panel contract

- **Panel A — Gaussian annular decay.** Plot
  \(\gamma_m(\theta)=\theta^{-2}\exp[-4^{m-1}/(32\theta)]\) for
  \(\theta\in\{1,1/2,1/4\}\), \(m=1,\ldots,7\), on a logarithmic vertical
  axis.  Mark the panel visibly as `analytic formula`.
- **Panel B — algebraic pressure comparison.** Normalize both the
  \(\theta=1\) Gaussian factor and \((2^mR)^{-4}\) to one at \(m=1\).
  Compare decay shapes on a logarithmic axis.  State that the rows pay
  different quantities and are not interchangeable.
- **Panel C — packet scaling.** Read, without interpolation, all five
  `packet_concentration.numeric_rows` from the frozen certificate.  Normalize
  weighted \(L^3\) and weighted-\(L^2\)-to-\(3/2\) by their respective values
  at \(\delta=1/4\).  Plot filled-circle/solid and open-square/dashed series,
  and annotate the stored smallest-scale ratio.  Mark the panel visibly as
  `static functional diagnostic` and `NOT DNS`.

The visual uses a near-white paper, deep ink, one blue and one gold root plus
neutral grays.  Line styles, marker shapes, and filled/open markers preserve
the comparisons in grayscale.  The locked data-free five-petal research
blossom sits at the whole-figure header's top-right corner.

## Source-data schema

`source-data.csv` contains every plotted coordinate and annotation landmark:

```text
panel,series,record,x,y,x_name,y_name,formula,evidence_class,source_path,
source_sha256,normalization,note,raw_value
```

Panel A and B rows are generated only after `plot.py` parses the denominator
`32` and algebraic exponent `4` from the frozen proof text.  Panel C rows are
read from the audited certificate JSON whose payload digest is checked against
`fcac9744...`.  All formula samples are rendering coordinates, not measurements
or fitted evidence.

## Interpretation boundary

The Gaussian and algebraic factors belong to different analytic mechanisms.
Their normalized comparison is not a pointwise dominance theorem for the full
tail functionals.  The packet diagnostic has the quantifiers stated in the
independent audit: unconstrained smooth static divergence-free velocity data,
or a velocity-only intermediate inequality.  It does not refute an
associated-pressure inequality or an NSE-trajectory-only inequality.
`NOT CLAY`.
