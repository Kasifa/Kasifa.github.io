# R0.74Q common-shear gate finite certificate report

## Result

The finite certificate passes:

\[
 \boxed{21/21\text{ rational checks PASS},\qquad
        19/19\text{ structural checks PASS}.}
\]

The frozen bindings are

    analytic note
    60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695

    certificate producer
    a7a1f0ae1927cf4fcc6a71a61d2064616b5c32f9ca487c95a14e4672d30100ed

    certificate JSON
    a13435b6eaf3d92675bca902a40ed04cd47c21676fb4ef78a460db6a91b5adec

A fresh producer run is byte-identical to the stored JSON.  The producer
returns a nonzero status when any rational or structural check fails.  A
temporary negative-mutation test changed tag Q.76a to Q.76z; the producer
returned status 1 and identified equation_tags_consecutive as failed.

This is a finite arithmetic and source-binding certificate.  It is not a
numerical Navier--Stokes simulation and does not prove any analytic theorem.

## 1. Two-parameter platform constants

The certificate reconstructs

\[
 a_D=\frac{\alpha^2}{260}=\frac{49}{14625},
 \qquad
 a_S=\frac{c_h^2}{264}=\frac{75}{22528},
\]

and verifies

\[
 a_D-a_S=\frac{6997}{329472000}>0.
\]

It also checks the finite constants used in the new two-parameter platform
lemma:

\[
 (c_h-\alpha)9216=\frac{192}{5}>32,
 \qquad
 4\cdot65=260,
 \qquad
 64\cdot4=256.
\]

The periodic Gaussian-tail argument and its application to the heat shear
remain analytic parts of the main note.

## 2. Adjacent-shell exponent windows

The inherited amplified-amplitude reserve is reconstructed as

\[
 m=\frac1{320}-\frac32\frac8{3969}
  =\frac{43}{423360}>0.
\]

For adjacent dyadic shells, the three outer coefficients are

\[
 4\rho=\frac1{80},
 \qquad
 6c_\gamma=\frac{16}{1323},
 \qquad
 5c_\gamma=\frac{40}{3969}.
\]

Their exact gaps above the inner survival exponent are

\[
 \frac1{80}-\frac{75}{22528}
 =\frac{1033}{112640}>0,
\]

\[
 \frac{16}{1323}-\frac{75}{22528}
 =\frac{261223}{29804544}>0,
\]

\[
 \frac{40}{3969}-\frac{75}{22528}
 =\frac{603445}{89413632}>0.
\]

These identities support the proof-window comparison.  The certificate does
not turn an upper majorant into a lower bound and does not prove packet-tail
non-cancellation.

## 3. Structural and claim-boundary checks

The producer verifies all 81 equation tags in order, including the suffixed
tags Q.47a, Q.48a, Q.48b, Q.49a--Q.49c, Q.62a, Q.76a, and Q.96a.  It checks
their uniqueness and binds the displayed window fractions to the source
text.

It also requires the note to retain the following boundaries:

- the common-calibration result is asymptotic and geometry-specific;
- divergence of the inherited cubic upper majorant is not actual cubic
  divergence;
- the genuine cubic obstruction is conditional on an explicit
  no-cancellation hypothesis;
- physical pressure flux is zero, while the frozen local-pressure payment
  need not vanish;
- the fixed-scale effective-shell inequality, global regularity, and the
  Clay problem remain unresolved.

## 4. Reproduction

From the repository root:

    python3 scripts/r074q_common_shear_gate_certificate.py \
      > /tmp/r074q-common-shear-certificate.json
    cmp /tmp/r074q-common-shear-certificate.json \
      research/r074q_common_shear_gate_certificate.json

Expected result: producer status 0 and byte-identical JSON.
