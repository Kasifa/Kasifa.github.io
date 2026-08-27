# R0.72Q independent analytic audit

**Date:** 2026-08-28

**Status:** PASS for the declared fixed-(M), jet-dominated, arbitrary-phase
shape theorem and for the exact (1{:}2) caustic.  Formal source sealing is
not part of this source-stage audit.

## 1. Phase quotient and normalized profile

After a global translation makes the first Fourier coefficient positive real,
the remaining coefficients retain only relative phases.  Write the normalized
fixed-pattern profile as

\[
 F_y(\phi)=\cos\phi+
 \sum_{m=2}^{M}\operatorname{Re}
 \bigl(\beta_m(y)e^{im\phi}\bigr),
 \qquad M<\infty,
\]

and define

\[
 Q_j:=\sup_y\sum_{m=2}^{M}m^j|\beta_m(y)|.
\]

The theorem assumes

\[
 Q_2\le\frac12.
 \tag{1.1}
\]

Because (m\le m^2/2) and (1\le m^2/4) for (m\ge2), (1.1) gives the
exact consequences

\[
 Q_1\le\frac14,
 \qquad
 Q_0\le\frac18.
 \tag{1.2}
\]

No phase alignment is used in (1.1)--(1.2).

## 2. Two critical points for every phase pattern

Put (r=\pi/12).  The exact identity

\[
 \sin^2\frac\pi{12}=\frac{2-\sqrt3}{4}
\]

and (48<49) prove

\[
 \sin\frac\pi{12}>\frac14.
 \tag{2.1}
\]

At any critical point (c),

\[
 |\sin c|
 \le \sum_{m=2}^{M}m|\beta_m(y)|
 \le Q_1\le\frac14.
\]

Hence every critical point lies in exactly one of the fixed boxes

\[
 I_0=\{d(\phi,0)<r\},
 \qquad
 I_\pi=\{d(\phi,\pi)<r\}.
\]

The boundary signs of (F_y') are those of (-\sin\phi), by (2.1).  Thus
each box contains a zero.  Within (I_0),

\[
 F_y''\le-\cos r+Q_2<0,
\]

and within (I_\pi),

\[
 F_y''\ge\cos r-Q_2>0.
\]

Therefore each box contains exactly one zero and there are no others.  This
proves an arbitrary-phase critical count of exactly two.

If (c) is either critical point and (d(\phi,c)\le r), then (phi) is
within (2r=\pi/6) of (0) or (pi).  Consequently

\[
 |F_y''(\phi)|
 \ge \cos\frac\pi6-Q_2
 \ge \frac{\sqrt3-1}{2}
 =:\mu.
 \tag{2.2}
\]

The comparison (mu>1/3) is exact: it is equivalent to
(sqrt3>5/3), and squaring reduces this to (27>25).

For (d(\phi,\mathcal C_y)<r), integrating (2.2) from the unique nearest
critical point gives

\[
 \frac13d(\phi,\mathcal C_y)
 <|F_y'(\phi)|
 \le\frac32d(\phi,\mathcal C_y).
 \tag{2.3}
\]

On the complement, a minimum of (|F_y'|) occurs either at distance (r)
from a critical point or at a point where (F_y''=0).  The first alternative
is bounded below by (mu r>\pi/36>1/12).  In the second alternative,
(|\cos\phi|\le Q_2\le1/2), so

\[
 |F_y'(\phi)|
 \ge\frac{\sqrt3}{2}-\frac14
 >\frac1{12}.
 \tag{2.4}
\]

Thus the normalized shape admits the explicit contract

\[
 r=\frac\pi{12},
 \qquad \mathfrak C_0=9,
 \qquad \mathfrak C_1=12.
 \tag{2.5}
\]

The looser normalized choice (mathfrak C_0=81) is also valid.  For the
physical Coble shear

\[
 W(y,\phi)=e^{-y}F_y(\phi),\qquad 0\le y\le1,
\]

the exact series certificate

\[
 \sum_{n=0}^{4}\frac1{n!}=\frac{65}{24},
 \qquad
 \sum_{n=5}^{\infty}\frac1{n!}
 \le\sum_{k=0}^{\infty}\frac1{5!5^k}=\frac1{96},
 \qquad
 e<\frac{65}{24}+\frac1{96}=\frac{87}{32}<3
\]

gives (e^{-y}>1/3).  Multiplying
the normalized local and away-from-critical lower bounds by this envelope
gives

\[
 |W_\phi|>\frac19d(\phi,\mathcal C_y)
 \quad(d<r),
 \qquad
 |W_\phi|>\frac1{36}
 \quad(d\ge r).
\]

Hence the headline finite-window contract is

\[
 \boxed{
 r=\frac\pi{12},\qquad
 \mathfrak C_0=81,\qquad
 \mathfrak C_1=36,
 \qquad 0\le y\le1.}
 \tag{2.5a}
\]

The bounded-envelope step uses only (e<3); the normalized away estimate
uses (mu>1/3) and (pi>3), the latter following geometrically from the
inscribed regular hexagon.  Equation (2.5a) must not be read as an absolute
positive lower bound as (y\to\infty).

The fixed-(M) derivative ledger is

\[
 \|F_y\|_\infty\le\frac98,
 \qquad
 \|F_y'\|_\infty\le\frac54,
 \qquad
 \|F_y''\|_\infty\le\frac32,
 \qquad
 \|F_y'''\|_\infty\le1+\frac M2.
 \tag{2.6}
\]

The last constant depends on the fixed carrier ceiling; it is not uniform as
(M\to\infty).

For heat-decaying carriers, the mixed slow-time derivative has coefficient at
most (D_M=1+M/2).  The condition

\[
 D_M\eta\le\eta^{3/4}
\]

is guaranteed by

\[
 \eta\le D_M^{-4}
 =\left(1+\frac M2\right)^{-4}.
 \tag{2.7}
\]

At equality, both sides are exactly (D_M^{-3}); the producer and independent
routes check this with rational arithmetic for the declared integer (M).

## 3. Exact (1{:}2) caustic

For

\[
 f(\phi)=\cos\phi+a\cos(2\phi+\theta),
 \qquad z:=ae^{i\theta},
\]

simultaneous degeneracy (f'=f''=0) gives

\[
 a\sin(2\phi+\theta)=-\frac12\sin\phi,
 \qquad
 a\cos(2\phi+\theta)=-\frac14\cos\phi.
\]

Multiplication by (e^{-2i\phi}) yields the exact parametrization

\[
 \boxed{
 z(\phi)=\frac18e^{-3i\phi}-\frac38e^{-i\phi}.}
 \tag{3.1}
\]

Direct trigonometric reduction gives

\[
 \operatorname{Im}z=\frac12\sin^3\phi,
 \qquad
 |z|^2=\frac{1+3\sin^2\phi}{16}.
 \tag{3.2}
\]

Therefore the caustic is the nephroid

\[
 \boxed{
 \left(|z|^2-\frac1{16}\right)^3
 =\frac{27}{1024}(\operatorname{Im}z)^2,}
 \tag{3.3}
\]

because both sides of (3.3) equal
(27\sin^6\phi/4096).  Its radial range is exactly

\[
 \frac14\le|z|\le\frac12.
 \tag{3.4}
\]

The caustic also meets every phase ray exactly once.  Put
(s=|z|^2).  On the ray of angle (	heta), (3.3) becomes

\[
 H(s):=\frac{(s-1/16)^3}{s}
 =\frac{27}{1024}\sin^2\theta.
\]

Exact differentiation and factorization give

\[
 H'(s)
 =\frac{(s-1/16)^2(2s+1/16)}{s^2}>0
 \qquad(s>1/16).
 \tag{3.5}
\]

Moreover, (H(1/16)=0) and (H(1/4)=27/1024).  Since the right-hand
side ranges over ([0,27/1024]), each ray has one and only one solution
(s\in[1/16,1/4]), including the cusp solution at (s=1/16) when
(sin\theta=0).

In particular, the open disk (|z|<1/4) contains no degeneracy.  Homotopy to
(z=0) then gives exactly two critical points throughout that disk.  This is
the sharp two-carrier no-degeneracy statement; the stronger jet condition
(4a\le1/2), namely (a\le1/8), is what supplies the simple fixed constants
in Section 2.

On the wall,

\[
 f'''=-3\sin\phi,
 \qquad
 f''''=-3\cos\phi.
\]

The generic wall point is an (A_2) fold.  The two cusps are

\[
 (z,\phi)=\left(\frac14,\pi\right),
 \qquad
 (z,\phi)=\left(-\frac14,0\right),
\]

where the fourth derivatives are (3) and (-3), respectively, so they are
(A_3) degeneracies.  The caustic is a wall for this Morse certificate, not a
counterexample to enhanced dissipation.

For the heat profile in the task,

\[
 a=\rho e^{-3y},
\]

so the exact degeneracy condition is that
(ho e^{-3y}e^{i\theta}) lies on (3.1)--(3.3).  In particular, at relative
phase (0) or (pi), any trajectory starting with (ho\ge1/4) crosses the
cusp radius (1/4).  Hence a uniform-in-(y\ge0) phase cone containing either
real ray cannot extend beyond (ho<1/4).

## 4. Certificate boundary and independent route

The finite certificate checks:

1. the exact implications (Q_2\le1/2\Rightarrow Q_1\le1/4) and
   (Q_0\le1/8);
2. the integer square comparisons (48<49) and (27>25), together with the
   independently assembled bounded-envelope ledger
   (65/24+1/96=87/32<3), (1/3\mapsto1/9,1/36);
3. the derivative and slow-threshold rational ledger for the declared fixed
   (M);
4. the rational coefficients, implicit identity, radial range, unique-ray
   derivative factorization and cusp jets of the (1{:}2) caustic;
5. the claim boundary: fixed (M), arbitrary phases, no growing-(M) claim,
   and no assertion that a caustic is failure of enhanced dissipation.

It does not turn finite arithmetic into a proof of the continuum inequalities,
the enhanced-dissipation theorem, or Navier--Stokes regularity.  Common-band
support and normalization without the jet-dominance hypothesis remain open;
the two-carrier caustic already shows why such data alone cannot guarantee a
uniform Morse margin.

The independent JavaScript route uses only BigInt rationals and does not read
the Python source or producer artifacts.  Each route writes a canonical
payload; the comparator requires exact parsed-JSON equality.

A temporary source-stage check may be run as follows, with any fixed integer
(M\ge2):

```sh
python3 research/r072q_exact_audit.py --output-dir "$TMPDIR/r072q" --max-carrier 6
node research/r072q_independent_audit.mjs --output-dir "$TMPDIR/r072q" --max-carrier 6
python3 research/r072q_compare_audits.py --certificate-dir "$TMPDIR/r072q" --allow-unsealed-source
```

The temporary allowance must not be used in a formal certificate bundle.
