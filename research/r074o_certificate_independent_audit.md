# R0.74O finite certificate — independent audit

## Verdict

**PASS.** A separate Ruby Rational implementation reconstructed the complete
245-row R0.74O certificate from primitive constants and formulas. It did not
invoke, import, or parse mathematical inputs from the Python producer. It
compared the full reconstructed JSON object and enforced the frozen
byte-level JSON SHA-256.

The result is **FINITE ONLY**. It is not an analytic audit of the R0.74O
Navier--Stokes argument.

## 1. Independent reconstruction coverage

The Ruby verifier reconstructed:

1. the four primitive constants
   \(\lambda=63/32\), \(\rho=1/320\),
   \(c_\gamma=8/3969\), and \(d_E=98/29475\);
2. the derived constants
   \[
   e_E=\frac{17018}{12998475},\qquad
   m=\frac{43}{423360},\qquad
   e_E-\frac23m=\frac{1171}{943200};
   \]
3. the endpoint increment and power
   \[
   \delta=\frac{86}{11907},\qquad
   q_*=\frac{8024}{11907};
   \]
4. the exact \(G\)-row exponential and polynomial cancellations;
5. the \(H\)-row \(L^{-3/2}\), energy \(L^{4/3}\), observable
   \(L^{7/3}\), log \(7/6\), and endpoint-ratio log \(2/3\) powers;
6. all six coordinates of each of the nine raw
   \(B,R,L,\kappa,\Gamma\), heat-decay scale rows for
   \(E,G,H,P,\mathfrak C,X\);
7. eight complete exponent records over \(14\le j\le21\);
8. all 63 adjacent-window factor-four propagation rows; and
9. the seven-member polynomial-\(\kappa\) grid for
   \(\gamma\in\{-2,-1,0,1/2,1,2,4\}\).

Every serialized rational in a check row was reparsed and required to have
canonical numerator/denominator spelling. The verifier then recomputed the
relation, signed margin, pass flag, row order, notes, unique identifiers,
summary counts, all auxiliary ledgers, result, and analytic boundary.

## 2. Key exact identities

The independent arithmetic gives

\[
 m=\rho-\frac32c_\gamma=\frac{43}{423360}>0,
\]

\[
 e_E-\frac23m=\frac{1171}{943200}>0,
\]

\[
 \frac{2m}{9\rho}=\frac{86}{11907},
 \qquad
 \frac23+\frac{86}{11907}=\frac{8024}{11907}.
\]

For

\[
 \kappa=\exp\!\left(\frac m3L^2\right)L^{2/3},
\]

the verifier obtains

\[
 3\frac m3-\rho+\frac32c_\gamma=0,
 \qquad
 3\frac23-2=0.
\]

It separately checks

\[
 3\rho q_*
 =2\rho+\frac23m
 =\frac{1003}{158760}.
\]

No floating-point arithmetic is used in either implementation.

## 3. Window and monotone ledger

For each \(j=14,\ldots,21\), Ruby reconstructs

\[
 L_j^2=\frac{3969}{1024}4^j,\qquad
 c_\gamma L_j^2=\frac{4^j}{128},\qquad
 \rho L_j^2=\frac{3969\,4^j}{327680}.
\]

It also reconstructs the \(\kappa\), \(\kappa^3\), energy-reserve, payment,
observable, and endpoint exponent rows. At every index the \(G\) exponent
cancels exactly and the endpoint growth equals the observable growth.

For every adjacent pair, each of the nine positive exponent fields is
exactly multiplied by four. This verifies the claimed monotone propagation
without numerical evaluation of exponentials.

## 4. Polynomial-\(\kappa\) grid

The verifier independently applies

\[
 \kappa=L^M,\qquad
 \frac{\kappa^2L}{L^{2\gamma}}
 =L^{2M+1-2\gamma}.
\]

The chosen pairs are

\[
 (-2,0),\ (-1,0),\ (0,0),\
 (1/2,1),\ (1,1),\ (2,2),\ (4,4),
\]

where each pair is \((\gamma,M)\). In every row,
\(M>\gamma-\tfrac12\), and the exact divergence powers are respectively

\[
 5,\ 3,\ 1,\ 2,\ 1,\ 1,\ 1.
\]

The audit certifies only these finite exponent comparisons. The analytic
decay estimates that would absorb the accompanying polynomial \(E,G,H\)
factors are outside this certificate.

## 5. Nominal and deterministic runs

Nominal command:

~~~sh
ruby scripts/r074o_amplitude_endpoint_certificate_independent.rb
~~~

Observed output:

~~~text
certificate_sha256: 30fd77ae3b4c88628e2d84207fc9b1728b1ab2343bf187fcd1141b080d6c5a5b
audit_window: j=14..21
scale_rows: 9
window_rows: 8
polynomial_rows: 7
RESULT: PASS (245/245 checks)
PASS 245/245
~~~

Exit code: \(0\).

Regenerating the JSON from the Python producer yielded the same SHA-256 and
a byte comparison exit code of \(0\).

## 6. Fail-closed tamper test

A temporary copy changed one occurrence of the exact reserve
1171/943200 to 1170/943200 while leaving all other bytes untouched. The
Ruby verifier returned exit code \(1\) and reported three independent
barriers:

~~~text
row schema: noncanonical rational "1170/943200"
independent reconstruction differs
certificate SHA-256 ... != 30fd77ae3b4c88628e2d84207fc9b1728b1ab2343bf187fcd1141b080d6c5a5b
~~~

Thus a modified value cannot pass by retaining a stale true pass flag, and
a structurally regenerated certificate cannot pass without deliberately
rebinding the frozen hash.

## 7. Frozen implementation inventory

| artifact | lines | SHA-256 |
|---|---:|---|
| scripts/r074o_amplitude_endpoint_certificate.py | 762 | 3a01ab8659ed5a96bce92aa15df8190437f98522e935858d4e5840e629358671 |
| scripts/r074o_amplitude_endpoint_certificate_independent.rb | 532 | 562a13ebd3f66438919bccdd842fb2d2c5348f2c313fa071d39e878dd39d4062 |
| research/r074o_amplitude_endpoint_certificate.json | 2555 | 30fd77ae3b4c88628e2d84207fc9b1728b1ab2343bf187fcd1141b080d6c5a5b |
| research/r074o_amplitude_endpoint_certificate_report.md | 243 | 308453e68ec9ce2ef7b1e2a16d6faacbdc333fdfd5604417929fbca634db10fa |

The Python syntax check and Ruby syntax check both passed.

## 8. Analytic boundary

This audit does not prove the packet construction, buffered-energy
estimate, pressure payment, cubic or harmonic occupation bounds,
calibration, collar-flux lower bound, exterior-observable lower bound, or
any asymptotic comparison for an actual Navier--Stokes solution. It does
not establish or disprove a universal endpoint estimate without the
separate analytic proof. It does not verify literature, novelty, or
priority. It proves no regularity, singularity, blow-up, continuation, or
global-smoothness theorem.

**FINITE ONLY; NOT CLAY.**
