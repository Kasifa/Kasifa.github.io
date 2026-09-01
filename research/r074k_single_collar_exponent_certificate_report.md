# R0.74K exact single-collar exponent certificate report

## Result

**PASS 41/41.**

The Python producer uses exact `Fraction` arithmetic.  The independent Ruby
implementation reconstructs all 41 predicates without reading the Python
source or frozen JSON and returns 41/41 with zero mismatches.

## Certified finite statements

- \(\lambda=63/32\), \(c_h=15/16\), \(\rho=1/320\), and
  \(c_\gamma=8/3969\).
- The nearest inner-shell boundary gap is \(433/1008\).
- At the positive-volume offset \(\varepsilon=1/128\),
  \[
  d_{1,\varepsilon}=\frac{3527}{8064},\qquad
  \lambda^{-2}-(\lambda^{-1}-\varepsilon)^2
  =\frac{8129}{1032192}>0.
  \]
- The sharp free squared-Gaussian comparison has the wrong sign at that
  slab:
  \[
  \frac34c_\gamma-\frac{d_{1,\varepsilon}^2}{132}
  =\frac{536399}{8583708672}>0.
  \]
- The sharp \(p=2\) comparison closes \(j-2\), and every \(m\ge2\) has
  the uniform compatibility margin
  \[
  \frac{204385}{134120448}>0.
  \]
- After reserving the same \(1/128\) padding at \(j-2\), the sharp margin
  remains \(13471441/8583708672>0\).
- The inherited denominator \(262\) misses at \(m=2\) but closes at
  \(m=3\), with the exact margins stored in the JSON.
- The adjacent outer-shell exponent retains
  \(1237/423360>0\) after one inverse-\(R_j\) loss.
- The conditional collar normalization is exact:
  \[
  \frac{\mathfrak a_j^2B_j}{R_j}
  (\Gamma_jL_jR_j^5)
  =B_j^3L_jR_j^4
  =(B_jR_j^2)B_j^2L_jR_j^2.
  \]

## What the certificate does not certify

The program does not prove that a free heat packet is a valid upper or
lower model for the true passive packet.  It does not prove a normalized
Brownian-bridge estimate, a time-coupled collar-BV estimate, exceptional-path
suppression, the hypothesis of R0.74K Theorem 4.1, a matching upper bound for
\(X_j\) or \(\mathfrak C_j\), a universal endpoint theorem, regularity,
singularity, or the Millennium problem.  **NOT CLAY.**

## Reproduction

```text
python3 scripts/r074k_single_collar_exponent_certificate.py \
  | diff -u research/r074k_single_collar_exponent_certificate.json -

/usr/bin/ruby \
  scripts/r074k_single_collar_exponent_certificate_independent.rb
```
