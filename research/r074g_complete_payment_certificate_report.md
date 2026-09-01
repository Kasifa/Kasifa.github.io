# R0.74G complete-payment finite compatibility certificate report

## Result

The exact-arithmetic certificate returns **PASS: 31/31**.

This is a finite compatibility result.  It checks rational identities,
strict exponent gaps, conditional calibration arithmetic, bridge-chart
reserves, and the powers of \(R\) in the occupation ledger.  It does not
prove any heat-kernel, Brownian, Riesz-transform, pressure, endpoint, or
Navier--Stokes theorem.

## Frozen constants

\[
 \lambda=\frac{63}{32},\qquad
 c_h=\frac{15}{16},\qquad
 \alpha=\frac{14}{15},\qquad
 \beta^2=\frac{31}{256},
\]

\[
 c_R=\frac1{320},\qquad
 c_\gamma=\frac8{3969}.
\]

The radial split and centre ratio are

\[
 c_h^2+\beta^2=1,
 \qquad
 \frac{q^2}{h^2}=\frac{31}{225}<\frac14.
\]

Thus \(q<h/2\), as required in the near-path branch of the occupation
proof.

## Three decisive exponent margins

The plateau-shift exponent is

\[
 a=\frac{\alpha^2}{260}=\frac{49}{14625},
\]

and the exact margin making \(\delta/R\to0\) is

\[
 a-c_R=\frac{211}{936000}>0.
\]

The buffered transverse-energy exponent is

\[
 d_E=\frac{\alpha^2}{262}=\frac{98}{29475},
\]

with amplitude margin

\[
 d_E-c_\gamma
 =\frac{17018}{12998475}>0.
\]

The common complete-payment margin is

\[
 c_R-\frac32c_\gamma
 =\frac1{320}-\frac4{1323}
 =\frac{43}{423360}>0.
\]

This last finite inequality is the exponent gate used by both the packet
\(G_u\) and packet \(H_u\) rows.  The certificate does not prove the
analytic estimates whose substitution uses the gate.

## Buffered-energy geometry

The condition

\[
 (c_h-\alpha)L\ge16
\]

has exact continuous threshold

\[
 L\ge3840.
\]

The inherited discrete scales satisfy

\[
 L_{12}=8064>3840,
 \qquad L_{13}=16128.
\]

The Gaussian denominator in the transverse-energy subsolution is checked
as

\[
 2+4\cdot65=262.
\]

These checks do not prove the subsolution or cutoff energy identity.

## Conditional calibration and chart reserve

Under the separately proved large-index hypotheses

\[
 q\le\frac14,qquad \theta(t,h)\ge\frac34,
\]

the \(64R^2\) contrast interval gives

\[
 \mathfrak D\ge48R^2,
 \qquad
 \frac1{128R^2}\le B\le\frac1{64R^2}.
\]

The pathwise upper shift is then

\[
 2B(65R^2)\le\frac{65}{32}.
\]

Together with \(Q\ge-1/2\), the left packet-centre reserve is

\[
 \frac12+\frac{65}{32}=\frac{81}{32}<3<\pi.
\]

Thus the finite arithmetic leaves a positive torus-seam reserve.  The
certificate checks \(81/32<3\); the classical inequality \(3<\pi\) is an
analytic input, not a floating-point comparison.

The bridge heat-age range is exactly

\[
 62R^2\le T\le66R^2.
\]

## Occupation powers

After normalized bridge Jensen, the periodic heat-kernel powers are

\[
 R^{3p}R^{1-p}R^{1-2p}=R^2
 \qquad(p=2,3).
\]

Multiplication by the effective all-copy weight prefactors gives

\[
 R\cdot R^2=R^3\quad(p=2),
 \qquad
 R^4\cdot R^2=R^6\quad(p=3).
\]

The two path-geometry branches use the exact squared constants

\[
 1+2^2=5,
 \qquad
 1+\left(\frac12\right)^2=\frac54.
\]

These finite powers match the proposed \(O2\) and \(O3\) occupation rows.
The certificate does not prove Jensen--Tonelli, the periodic Peetre bound,
or the weighted heat-kernel moments.

## Scope boundary

The certificate does **not** prove:

1. the large-index hypotheses \(q\le1/4\) or
   \(\theta(t,h)\ge3/4\);
2. the transverse-energy subsolution, cutoff identity, or Gaussian bounds;
3. the local Riesz/Newton pressure identity;
4. the Brownian-bridge formula or pathwise displacement inequalities;
5. the periodic Peetre inequality or weighted kernel moments;
6. the complete denominator theorem or either endpoint counterexample;
7. Navier--Stokes regularity, singularity, or the Clay problem.

## Reproduction

From the repository root, run

    python3 scripts/r074g_complete_payment_certificate.py

The standard output must be byte-for-byte identical to
research/r074g_complete_payment_certificate.json.

