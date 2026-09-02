# R0.74O finite certificate report — amplitude endpoint

## Status

**FINITE: PASS, 245/245 exact checks, 245 unique row identifiers.**

The Python producer uses fractions.Fraction only. A separate Ruby Rational
implementation reconstructs every row from primitive constants, compares
the full JSON object, and fails closed on the frozen byte-level JSON hash.

This package certifies finite exponent arithmetic and raw scale bookkeeping
only. It does not prove any analytic estimate in the R0.74O argument.

## 1. Frozen rational constants

The certificate reconstructs

\[
 \rho=\frac1{320},\qquad
 c_\gamma=\frac8{3969},\qquad
 d_E=\frac{98}{29475},
\]

\[
 e_E=d_E-c_\gamma
 =\frac{17018}{12998475},
\]

\[
 m=\rho-\frac32c_\gamma
 =\frac{43}{423360}>0.
\]

After inserting the squared amplitude factor, the packet-energy reserve is
still strictly positive:

\[
 e_E-\frac23m
 =\frac{1171}{943200}>0.
\]

The endpoint increment and power are

\[
 \delta=\frac{2m}{9\rho}
 =\frac{86}{11907},
 \qquad
 q_*=\frac23+\delta
 =\frac{8024}{11907}.
\]

All of these identities and strict inequalities are exact rational rows.

## 2. Exponential amplitude ledger

The finite ledger uses

\[
 \kappa
 =\exp\!\left(\frac{m}{3}L^2\right)L^{2/3}.
\]

It checks the two cancellations

\[
 3\frac m3-\rho+\frac32c_\gamma=0,
 \qquad
 3\frac23-2=0.
\]

Thus, at the exponent-bookkeeping level,

\[
 \boxed{\kappa^3R\Gamma^{-3/2}L^{-2}=1.}
\]

The neighboring polynomial powers remain

\[
 \kappa^3L^{-7/2}=L^{-3/2},
 \qquad
 \kappa^2=L^{4/3}
\]

after the common exponential factors are separated. The first is the
harmonic-row remainder. The second is the polynomial part of the
packet-energy ratio, whose exponential part decays with reserve
\(1171/943200\).

## 3. Raw scale ledgers

The JSON stores nine complete \(B,R,L,\kappa,\Gamma\) rows. The
heat-decay column is kept separate.

| term | \(B\) | \(R\) | \(L\) | \(\kappa\) | \(\Gamma\) | extra heat coefficient |
|---|---:|---:|---:|---:|---:|---:|
| \(E_{\rm shear}\) | \(2\) | \(2\) | \(0\) | \(0\) | \(0\) | \(0\) |
| \(E_{\rm packet}\) | \(2\) | \(2\) | \(0\) | \(2\) | \(-1\) | \(-d_E\) |
| \(G_{\rm shear}\) | \(3\) | \(3\) | \(0\) | \(0\) | \(0\) | \(0\) |
| \(G_{\rm packet}\) | \(3\) | \(4\) | \(-2\) | \(3\) | \(-3/2\) | \(0\) |
| \(H_{\rm shear}\) | \(3\) | \(3\) | \(0\) | \(0\) | \(0\) | \(0\) |
| \(H_{\rm packet}\) | \(3\) | \(4\) | \(-7/2\) | \(3\) | \(-3/2\) | \(0\) |
| \(P\) | \(3\) | \(3\) | \(0\) | \(0\) | \(0\) | \(0\) |
| \(\mathfrak C\) | \(2\) | \(2\) | \(1\) | \(2\) | \(0\) | \(0\) |
| \(X\) | \(2\) | \(2\) | \(1\) | \(2\) | \(0\) | \(0\) |

Each of the six coordinates in every row has its own named check. In
particular, after substituting
\(\mathfrak a=\kappa B\Gamma^{-1/2}\), the observable factor
\(\mathfrak a^2\Gamma LR^2\) has exact ledger

\[
 \kappa^2B^2LR^2.
\]

## 4. Endpoint exponents

Under the separately proved calibration \(BR^2\asymp1\), the payment scale
\(B^3R^3\) has exponential growth coefficient \(3\rho\). The observable
scale \(\kappa^2B^2LR^2\) has coefficient

\[
 2\rho+\frac23m=\frac{1003}{158760}.
\]

The certificate checks

\[
 3\rho\delta=\frac23m,
 \qquad
 3\rho q_*=2\rho+\frac23m.
\]

Hence the exponential part of the observable matches \(P^{q_*}\). Its
residual polynomial power is

\[
 2\cdot\frac23+1=\frac73.
\]

Since \(\log P\) is proportional to \(L^2\) at the scale-ledger level,

\[
 L^{7/3}\longleftrightarrow(\log P)^{7/6}.
\]

Relative to the square-root-log comparator, the excess is

\[
 L^{7/3-1}=L^{4/3}
 \longleftrightarrow(\log P)^{2/3}.
\]

These are exponent identities. The finite certificate does not itself
establish the analytic upper or lower estimates needed to turn them into a
counterexample theorem.

## 5. Exact audit window and monotone propagation

The JSON records the eight indices

\[
 14\le j\le21,
 \qquad
 L_j=\frac{63}{32}2^j.
\]

At every index it reconstructs:

\[
 c_\gamma L_j^2=\frac{4^j}{128},\qquad
 \rho L_j^2=\frac{3969\,4^j}{327680},
\]

the \(\kappa\) and \(\kappa^3\) exponential ledgers, the positive energy
reserve, the payment and observable growth exponents, the exact \(G\)
cancellation, and the \(P^{q_*}\)-to-observable exponent match.

For every adjacent pair in the window, all nine positive \(L^2\)-based
ledgers are checked to multiply by exactly four. This yields explicit
monotone propagation rather than a floating-point sample.

## 6. Polynomial-\(\kappa\) corollary grid

For the alternative finite ledger \(\kappa=L^M\), comparison with
\(P^{2/3}(\log P)^\gamma\) leaves the \(L\)-power

\[
 2M+1-2\gamma.
\]

The package checks seven exact samples:

| \(\gamma\) | chosen \(M\) | \(M-(\gamma-\tfrac12)\) | divergence \(L\)-power |
|---:|---:|---:|---:|
| \(-2\) | \(0\) | \(5/2\) | \(5\) |
| \(-1\) | \(0\) | \(3/2\) | \(3\) |
| \(0\) | \(0\) | \(1/2\) | \(1\) |
| \(1/2\) | \(1\) | \(1\) | \(2\) |
| \(1\) | \(1\) | \(1/2\) | \(1\) |
| \(2\) | \(2\) | \(1/2\) | \(1\) |
| \(4\) | \(4\) | \(1/2\) | \(1\) |

Every chosen \(M\) is rational or integral, satisfies
\(M>\gamma-\tfrac12\), and gives a strictly positive divergence exponent.
The JSON also records the corresponding energy, \(G\), and \(H\)
polynomial powers. Exponential absorption for these rows belongs to the
analytic proof, not to this finite package.

## 7. Reproduction and frozen output

Run

~~~sh
python3 scripts/r074o_amplitude_endpoint_certificate.py \
  > /tmp/r074o-amplitude-endpoint-certificate.json
cmp research/r074o_amplitude_endpoint_certificate.json \
  /tmp/r074o-amplitude-endpoint-certificate.json
ruby scripts/r074o_amplitude_endpoint_certificate_independent.rb
~~~

The checked artifacts are:

| artifact | lines | SHA-256 |
|---|---:|---|
| scripts/r074o_amplitude_endpoint_certificate.py | 762 | 3a01ab8659ed5a96bce92aa15df8190437f98522e935858d4e5840e629358671 |
| scripts/r074o_amplitude_endpoint_certificate_independent.rb | 532 | 562a13ebd3f66438919bccdd842fb2d2c5348f2c313fa071d39e878dd39d4062 |
| research/r074o_amplitude_endpoint_certificate.json | 2555 | 30fd77ae3b4c88628e2d84207fc9b1728b1ab2343bf187fcd1141b080d6c5a5b |

Immediate regeneration is byte-identical. The independent Ruby run prints
PASS 245/245.

## 8. Strict boundary

This certificate does **not** prove the buffered-energy estimate, cubic or
harmonic occupation bounds, pressure payment, calibration, collar-flux
lower bound, exterior-observable lower bound, or any asymptotic comparison
for an actual Navier--Stokes solution. It does not establish or refute a
universal endpoint theorem without the separate analytic argument. It
does not audit literature, novelty, or priority. It proves no regularity,
singularity, blow-up, continuation, or global-smoothness result.

**FINITE ONLY; NOT CLAY.**
