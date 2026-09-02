# R0.74P temporal-clock finite certificate report

## Result

The exact finite certificate passes:

\[
 \boxed{52/52\text{ checks PASS}.}
\]

The Python producer and an independent Ruby reconstruction agree on the
entire JSON payload.  The frozen certificate SHA-256 is

```text
c65b38def48b5439f112ab145360c1abb211de5bf6f004eca103271d8d9a204b
```

The certificate is finite arithmetic support for the analytic note.  It is
not a numerical Navier--Stokes simulation and does not prove a continuum
theorem.

## 1. Missing-scale arithmetic

The inherited amplitude reserve is

\[
 m=\frac{43}{423360}>0,
 \qquad
 \varkappa=L^{2/3}\exp\!\left(\frac m3L^2\right).
\]

Therefore

\[
 K_*:=\varkappa^2L
 =L^{7/3}\exp\!\left(\frac{43}{635040}L^2\right).
\]

The certificate verifies both exact exponents:

\[
 \frac{2m}{3}=\frac{43}{635040},
 \qquad
 2\cdot\frac23+1=\frac73.
\]

Thus the target clock scale

\[
 T_*=\varkappa^2B^2LR^2
\]

exceeds the paid average scale \(B^2R^2\) by the divergent factor \(K_*\).
The analytic proof that these are the actual PDE scales remains in the main
R0.74P note and its inherited R0.74O inputs.

## 2. Target-shell weight ledger

The passive amplitude has target-weight factor

\[
 \mathfrak a_*^2
 =\varkappa^2B^2\Gamma^{-1}.
\]

Multiplying by the physical shell weight \(\Gamma\) cancels that exponent:

\[
 \Gamma\mathfrak a_*^2=\varkappa^2B^2.
\]

This is the exact arithmetic behind the matched target clock.  The stronger
square function divides once more by \(\sqrt\Gamma\), leaving

\[
 \Gamma^{-1/2}
 =\exp\!\left(\frac4{3969}L^2\right).
\]

The positive coefficient \(4/3969\) verifies the exponential overpayment.

## 3. Sampled Carleson branches

For the finite grid

\[
 \sigma\in\left\{
 \frac14,\frac12,\frac34,1,\frac32,2,4
 \right\},
\]

the certificate records

\[
 \beta(\sigma)=\min\{\sigma,1\}>0
\]

and the corresponding bound \(K_*^{-\beta(\sigma)}\).  It distinguishes
the three analytic branches:

- \(0<\sigma<1\): the maximum occurs at the intersection
  \(x=K_*^{-1}\);
- \(\sigma=1\): the maximum equals \(K_*^{-1}\);
- \(\sigma>1\): the supremum \(K_*^{-1}\) is approached as
  \(x\uparrow1\); it is not attained because the windows satisfy
  \(J\Subset I_R\).

The certificate samples exact rational values only.  The proof for every
fixed real \(\sigma>0\) is Theorem 4.2 of the main note.

## 4. Finite \(\ell^1/\ell^2\) obstruction rows

For

\[
 N\in\{4,16,64,256,1024,4096\},
\]

the certificate uses the finite vector with \(N\) unit entries and verifies

\[
 \|v\|_{\ell^1}=N,
 \qquad
 \|v\|_{\ell^2}=\sqrt N,
 \qquad
 \frac{\|v\|_{\ell^1}}{\|v\|_{\ell^2}}=\sqrt N.
\]

These rows detect the growing finite-dimensional gap.  The analytic formula
for arbitrary \(N\) rules out a dimension-free sequence-space inequality;
the finite grid is only a reproducibility check.

## 5. Independent reconstruction

Run the producer and compare its bytes with the frozen JSON:

```bash
python3 scripts/r074p_temporal_clock_certificate.py \
  | cmp - research/r074p_temporal_clock_certificate.json
```

Run the independent reconstruction:

```bash
ruby scripts/r074p_temporal_clock_certificate_independent.rb
```

The Ruby program independently reconstructs every rational input, derived
quantity, scale row, Carleson sample, equal-entry witness, comparison row,
boundary statement, and summary field.  It also verifies the frozen JSON
hash and canonical rational spelling.

## 6. Analytic boundary

The certificate does not prove or check:

1. the local-energy measure identity or moving-test passage;
2. the shellwise total-variation bounds or infinite-shell limits;
3. the continuum optimization for all real \(\sigma>0\);
4. the terminal-lobe or target-flux PDE estimates;
5. trajectory, pressure-primitive, clock, BV, or square-function compactness;
6. an \(\ell^1\)-to-\(\ell^2\) Navier--Stokes inequality;
7. a prescribed-centre good-scale theorem;
8. literature exhaustiveness, novelty, or priority;
9. regularity, singularity, blow-up, continuation, or global smoothness.

It does not solve the Navier--Stokes Millennium problem.  **FINITE ONLY;
NOT CLAY.**
