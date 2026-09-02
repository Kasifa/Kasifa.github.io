# R0.74N finite certificate report — all-shell synthesis

## Status

**FINITE: PASS, 84/84 exact checks.** The certificate is generated without
floating-point arithmetic. Its explicit audit window is

\[
14\le j\le 21.
\]

The window is accompanied by exact monotonic-propagation ledgers for the two
discrete sequences. Those ledgers certify the finite arithmetic used by the
proof; they do not replace any analytic lemma in
r074n_all_shell_synthesis.md.

## 1. Frozen constants and exponent reserves

The generator reconstructs

\[
c_\gamma=\frac{8}{3969},\qquad
\rho=\frac{1}{320},\qquad
c_\gamma\lambda^2=\frac{1}{128},\qquad
\lambda=\frac{63}{32}.
\]

It then checks the two strict reserves used by the combined-inner and outer
payments:

\[
\frac{1}{16}-\rho-c_\gamma
=\frac{72851}{1270080}>0,
\]

\[
3c_\gamma-\rho
=\frac{1237}{423360}>0.
\]

The dyadic normalization is reconstructed independently at every audited
index:

\[
c_\gamma L_j^2=\frac{4^{j-1}}{32},\qquad
-\log\frac{\Gamma_{j+1}}{\Gamma_j}=3c_\gamma L_j^2,\qquad
\frac{4^{j+1}}{L_j^2}=\frac{4096}{3969}.
\]

For \(1\le m\le 8\), the inward weight exponent is also checked in the two
exact forms

\[
-\log\frac{\Gamma_j}{\Gamma_{j-m}}
=c_\gamma(1-4^{-m})L_j^2
=\frac{4^{j-1}-4^{j-m-1}}{32}
\]

at the inherited base index \(j=14\).

## 2. Combined-chord sequence

Let

\[
b_k=2^k\Gamma_k,\qquad
\delta_k=\frac{3\,4^{k-1}}{32}.
\]

Then \(b_{k+1}/b_k=2e^{-\delta_k}\). The certificate never approximates
this exponential numerically. It uses

\[
e^x\ge 1+x+\frac{x^2}{2}+\frac{x^3}{6}.
\]

At \(k=3\), \(\delta_3=3/2\), and the Taylor lower bound equals \(67/16\).
Hence

\[
\frac{b_4}{b_3}\le\frac{32}{67}<\frac{1}{2}.
\]

Since \(\delta_{k+1}=4\delta_k\), the same half-ratio bound propagates to
every \(k\ge 3\). Together with \(\Gamma_k\le 1\), this gives the exact
majorant

\[
\sum_{k\ge 1}2^k\Gamma_k
\le 2+4+2\cdot 8=22.
\]

For each \(14\le j\le 21\), the JSON additionally records the exact cubic
Taylor envelope for the last increment of
\(\sum_{k=1}^{j-1}b_k\). All eight recorded ratio envelopes are below
\(1/2\).

## 3. Outer-shell sequence

Let \(a_k=4^k\Gamma_k\). Then

\[
\frac{a_{k+1}}{a_k}=4e^{-\delta_k}.
\]

At \(k=4\), \(\delta_4=6\), while

\[
e^6\ge 1+6+\frac{6^2}{2}=25.
\]

Thus \(a_5/a_4\le 4/25<1/2\). Monotonic growth of \(\delta_k\) propagates
the half-ratio bound, and the infinite tail has the exact geometric
majorant

\[
\sum_{k\ge j+1}a_k\le 2a_{j+1}
\]

whenever \(j+1\ge 4\). The audit window records eight exact rational
envelopes for \(a_{j+2}/a_{j+1}\), one at each
\(j=14,\ldots,21\).

## 4. Raw scale ledgers

The certificate keeps the polynomial bookkeeping separate from the
exponential payments.

| row | raw factors | raw \(L\) power | raw \(R\) power | later payment |
|---|---:|---:|---:|---|
| combined-inner bad | \(R^6R^2R^{-1}R^{-3}\) | \(0\) | \(4\) | bad reserve pays \(\Gamma_jR\) |
| combined-inner good | \(R^6R^2R^{-1}R^{-4}\) | \(0\) | \(3\) | super-Gaussian tail pays \(\Gamma_jR^2\) |
| one outer shell | \(R^2R^2\) | \(0\) | \(4\) | shell weight remains explicit |
| summed outer tail | \(L^2R^4\) | \(2\) | \(4\) | outer reserve pays \(R\) and polynomial excess |
| inherited main row | \(LR^5\) | \(1\) | \(5\) | multiplied by \(\Gamma_j\) |
| target | \(LR^5\) | \(1\) | \(5\) | — |

The displacement scale is recorded only through its exact growth ledger:

\[
\frac{\Sigma_L^2}{1056R^2}
=\frac{\exp(L^2/320)}{1056\cdot 32768^2},\qquad
1056\cdot 32768^2=1133871366144.
\]

No finite row asserts the analytic Gaussian-tail domination.

## 5. Reproduction and frozen output

Run

~~~sh
python3 scripts/r074n_all_shell_certificate.py \
  > research/r074n_all_shell_certificate.json
ruby scripts/r074n_all_shell_certificate_independent.rb
~~~

The deterministic JSON is 1083 lines and has SHA-256

~~~text
53481cf393308a786c3a414da6238faaa9b8a15dac0017638c47584615bbecc2
~~~

An immediate regeneration was byte-identical, with comparison exit code
\(0\). The Ruby reconstruction returned exit code \(0\) with
“PASS 84/84.”

## 6. Strict boundary

This finite certificate does **not** prove the combined inward chord or its
periodization, the common-forward-law identity, final-segment expulsion,
the packet maximum principle, the outer collar volume estimate, or the
infinite-shell limit. Those are analytic obligations and require separate
reconstruction. It proves no universal endpoint inequality, regularity or
singularity theorem, and no Millennium result. **NOT CLAY.**
