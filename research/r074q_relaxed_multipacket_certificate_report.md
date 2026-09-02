# R0.74Q relaxed multipacket finite certificate report

## Result

The finite certificate passes:

\[
 \boxed{22/22\text{ rational checks PASS},\qquad
        41/41\text{ structural checks PASS}.}
\]

The frozen bindings are

    analytic note
    ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d

    certificate producer
    a47233d2ecf2eca1b8b278f645acf0edd583b710406f021a75eba52fbc5502d8

    certificate JSON
    77ed11f8072fc3904eab215ad1066fc8ccc219c075dfec83296bdb6d3f1386ae

A fresh producer run is byte-identical to the stored JSON.  The producer
returns a nonzero status when a rational or structural check fails.  In a
temporary negative-mutation test, changing tag Q.151 to Q.151z produced
`FAIL`, identified `equation_tags_consecutive`, and returned status 1.

This is a finite arithmetic and source-binding certificate.  It is not a
numerical Navier--Stokes simulation and does not prove an analytic theorem.

## 1. Dyadic ledger and exact outer scale

The certificate checks

\[
 1<\lambda=\frac{63}{32}<2,
 \qquad N=\lfloor\log_2(\lambda2^j)\rfloor=j,
\]

and reconstructs

\[
 \frac{L_N}{L^2}=\frac1{2\lambda}=\frac{16}{63},
 \qquad
 \frac14<\frac{16}{63}\le\frac12.
\]

It binds this calculation to Q.103--Q.105 and verifies the complete,
unique Q.100--Q.180 equation-tag ledger.

## 2. Survival and packet-dominance margins

The exact reserves are independently reconstructed as

\[
 a_D-\rho=\frac{211}{936000}>0,
 \qquad
 a_S-\rho=\frac{23}{112640}>0,
\]

\[
 a_\times=\frac{49}{14850},
 \qquad
 a_\times-\frac32c_\gamma
 =\frac{67}{242550}>0.
\]

The additional inner-packet and periodic-copy constants are

\[
 \mu_{\rm in}=\frac{4601}{2910600}>0,
 \qquad
 qL_N^2=\frac{1024}{15752961}L^4,
 \qquad
 R^{-2}=e^{L^2/160}.
\]

The moving-annulus margin is also checked exactly:

\[
 c_h^2+\frac1{256}=\frac{113}{128}
 <\left(\frac{64}{63}\right)^2.
\]

These finite identities do not replace the heat-kernel, bridge,
all-packet-dominance, or annular-containment proofs in the analytic note.

## 3. Cubic-payment exponent

The certificate verifies

\[
 \frac{5c_\gamma}{96}=\frac5{47628}>0,
 \qquad
 5c_\gamma-a_S
 =\frac{603445}{89413632}>0.
\]

It also requires the source formulas for the outer physical-shell weight
\(\Gamma_N^{1/4}\), the normalized payment lower bound, and every logarithmic
term in Q.169--Q.171.  The actual outer-lobe lower bound remains an analytic
result, not a finite-computation result.

## 4. Fail-closed claim boundary

The producer requires the note to retain all of the following boundaries:

- terminal defect-completed clocks have an analytic lower bound, but the
  signed cumulative flux statement Q.178 remains **OPEN**;
- the matching full \(Y_2\) upper bound and fixed-scale inequality Q.1 remain
  open;
- the result excludes one explicit equal-target architecture, not every
  common-shear family;
- no regularity, novelty, priority, or Clay claim is certified.

It also rejects a broken tag ledger, missing source formulas, forbidden
overclaims, malformed `,qquad`, tabs, and non-newline control characters.

## 5. Reproduction

From the repository root:

    python3 scripts/r074q_relaxed_multipacket_certificate.py \
      > /tmp/r074q-relaxed-multipacket-certificate.json
    cmp /tmp/r074q-relaxed-multipacket-certificate.json \
      research/r074q_relaxed_multipacket_certificate.json

Expected result: producer status 0 and byte-identical JSON.
