# R0.74E outer-annulus exponent certificate report

## Result

`PASS`: all 13 exact rational checks pass.

The frozen choice is

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \beta^2=\frac{31}{256},\qquad
 c_R=\frac1{320}.
\]

The certified nonempty window is

\[
 \frac4{1323}<\frac1{320}<\frac{49}{14625}.
\]

The exact strict margins are respectively

\[
 \frac1{320}-\frac4{1323}=\frac{43}{423360}>0,
\]

and

\[
 \frac{49}{14625}-\frac1{320}=\frac{211}{936000}>0.
\]

The transverse leakage exponent beats both the inverse-\(R_j\) prefactor
and the annular weight:

\[
 \frac{75}{22528}-\frac1{320}
 =\frac{23}{112640}>0,
\]

\[
 \frac{75}{22528}-\frac8{3969}
 =\frac{117451}{89413632}>0.
\]

The explicit separation reserve is also exact:

\[
 c_h-\alpha=\frac1{240},\qquad
 7680(c_h-\alpha)=32=2\kappa.
\]

## Reproduction

Run

```bash
python3 scripts/r074e_outer_annulus_exponent_certificate.py
```

and compare its standard output byte-for-byte with
`research/r074e_outer_annulus_exponent_certificate.json` followed by one
newline.

## Boundary

This is a finite exact-arithmetic certificate only.  It does not prove the
heat-evolved contrast, Feynman--Kac packet survival, buffered leakage,
pressure ledger, exterior-payment bounds, endpoint divergence, regularity,
or the Clay problem.
