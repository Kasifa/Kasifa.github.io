# R0.25 boundary-face polarization-channel reduction

## Status

R0.24 reduced the first sharp-label calculation to the closed face

\[
  m_2=-L
\]

at leaf count \(L\).  The generated gains at \(N=2,3\) were much smaller
than the full-space sharp gains, but two values did not identify a quantity
that could be estimated for every \(N\).

This note isolates that quantity.  Every charged boundary coefficient has a
unique sharp--longitudinal decomposition.  On the R0.22 label pair, the four
polarization channels have sizes

\[
  N^2,\qquad N,\qquad N,\qquad 1.
\]

Only the sharp--sharp channel carries the second-order analytic-radius loss.
It follows that \(O(N^{-1})\) decay of each normalized generated sharp
coordinate is sufficient for a uniformly bounded generated gain.

That decay is not proved here.  A two-precision recurrence extends the finite
probe to \(N=4,5\).  All four observed values satisfy the proposed scaling,
but a finite table is not an asymptotic theorem.

## Catalyst parity on the boundary face

Write the four boundary generators by their first and third coordinates:

\[
  P_+=(1,1),\quad P_-=(-1,-1),\quad
  C_+=(1,-1),\quad C_-=(-1,1).
\]

The two \(P\)-leaves carry rational amplitudes.  The two \(C\)-leaves carry
one factor of the quadratic-field generator \(t\), where \(t^2\in\mathbb Q\).
If a tree has \(C\) catalyst leaves and total label \(m=(m_1,-L,m_3)\), then

\[
  C_+-C_- = \frac{m_1-m_3}{2}.
\]

Since \(C\equiv C_+-C_-\pmod 2\), every contributing tree has the same
catalyst parity:

\[
  C\equiv \frac{m_1-m_3}{2}\pmod 2.
\tag{2.1}
\]

Consequently the whole coefficient belongs to one rational line of
\(\mathbb Q(t)\):

\[
 U_{L-1}(m)\in
 \begin{cases}
   \mathbb Q, & (m_1-m_3)/2\text{ even},\\
   t\mathbb Q, & (m_1-m_3)/2\text{ odd}.
 \end{cases}
\tag{2.2}
\]

For the sharp family, the parities of \(a_N,b_N,a_N+b_N\) are respectively
\(N-1,N,1\) modulo two.  This explains the alternating rational/radical basis
seen in the exact checkpoints.  It reduces arithmetic, but by itself it does
not control polarization.

## Sharp and longitudinal coordinates

For a cone label \(m\), let

\[
 q_m=\frac{3m_1-m_3}{12},\qquad \beta_m\cdot d=0,
 \qquad d=(1,1,1).
\]

A cone coefficient is a pair \((w,\ell)\), with \(w\cdot d=0\), satisfying

\[
 q_m\ell+\beta_m\cdot w=0.
\tag{3.1}
\]

Use the mode norm

\[
 M(w,\ell)=|w|+|\ell|.
\tag{3.2}
\]

When \(q_m\ne0\), define two unit modes

\[
 S_m=\left(\frac{d\times\beta_m}{\sqrt3|\beta_m|},0\right),
\tag{3.3}
\]

and, for the sharp inputs where \(q_m=1/6\),

\[
 L_m=\left(
 \frac{\beta_m}{|\beta_m|(1+6|\beta_m|)},
 -\frac{6|\beta_m|}{1+6|\beta_m|}
 \right).
\tag{3.4}
\]

Both satisfy (3.1) and have mode norm one.  Their transverse parts are
orthogonal.  Therefore every nonzero coefficient has a unique decomposition

\[
 \frac{U(m)}{M(U(m))}=\sigma_m S_m+\lambda_m L_m.
\tag{3.5}
\]

The number \(\sigma_m\) is the normalized sharp coordinate.  This is not the
same as the cosine formed using the transverse part alone: a coefficient can
look sharply aligned inside the transverse plane while its full mode norm is
dominated by \(\ell\).

For the two sharp inputs and \(N\ge2\),

\[
 |\lambda_m|\le 1+\frac1{12N}\le\frac{25}{24}.
\tag{3.6}
\]

Indeed, a normalized coefficient has \(|\ell|\le1\), while the longitudinal
entry of \(L_m\) has magnitude \(6|\beta_m|/(1+6|\beta_m|)\), and
\(|\beta_m|\ge2N\).

## Exact geometry of the sharp pair

For

\[
 a_N=(N,-3N,3N-2),\qquad
 b_N=(-N+1,-3N+1,-3N+1),
\]

the offsets are

\[
 \begin{aligned}
 \beta_A&=(N-2/3,-2N+1/3,N+1/3),\\
 \beta_B&=(-N+1/3,-N+1/3,2N-2/3).
 \end{aligned}
\tag{4.1}
\]

Direct calculation gives

\[
 \begin{aligned}
 |\beta_A|^2&=6N^2-2N+2/3,\\
 |\beta_B|^2&=6N^2-4N+2/3,\\
 \beta_A\cdot\beta_B&=3N^2-1/3,\\
 \beta_B\cdot(d\times\beta_A)&=-(3N-1)^2.
 \end{aligned}
\tag{4.2}

The last identity is the full-space sharp determinant from R0.22.

Let

\[
 Q_N(u,v)=\mathcal B_{a_N,b_N}(u,v)
          +\mathcal B_{b_N,a_N}(v,u).
\]

Substituting (4.1) into the cone bilinear map yields

\[
 \begin{aligned}
 M(Q_N(S_A,S_B))/N^2&\longrightarrow 27,\\
 M(Q_N(S_A,L_B))/N&\longrightarrow \frac{3}{2\sqrt2},\\
 M(Q_N(L_A,S_B))/N&\longrightarrow \frac{3}{2\sqrt2},\\
 M(Q_N(L_A,L_B))&\longrightarrow \frac18.
 \end{aligned}
\tag{4.3}

Thus the second-order loss is confined to one channel.

## A uniform conditional inequality

The asymptotics can be replaced by elementary bounds.  For \(N\ge2\),

\[
 2N\le|\beta_A|,|\beta_B|\le\sqrt6N,
 \qquad |\beta_A+\beta_B|\le3\sqrt2N.
\tag{5.1}
\]

For a charged output with charge \(1/3\), an ordered interaction with scalar
factor \(s\) obeys

\[
 M(\mathcal B(u,v))
 =|s|\bigl(|v_w|+3|(\beta_A+\beta_B)\cdot v_w|\bigr)
 \le |s|\bigl(1+3|\beta_A+\beta_B|\bigr)|v_w|,
\tag{5.2}
\]

with the dot product retained for the channel estimates.  Using
\(17/10<\sqrt3<26/15\), (4.2), and (5.1) gives the convenient bounds

\[
 \begin{aligned}
 M(Q_N(S_A,S_B))&\le44N^2,\\
 M(Q_N(S_A,L_B))&\le7N,\\
 M(Q_N(L_A,S_B))&\le7N,\\
 M(Q_N(L_A,L_B))&\le1.
 \end{aligned}
\tag{5.3}

For example, the sharp scalar is at most \((45/17)N\), and the sharp output
factor is at most \((83/10)N\).  The longitudinal output factor is at most
\(7/6\), while a longitudinal left input produces a scalar at most \(3/8\).
These four estimates give (5.3) after adding the two orders.

Let \(G_N\) be the gain of the two actual normalized generated inputs.  By
bilinearity and the triangle inequality,

\[
 \boxed{
 G_N\le
 44N^2|\sigma_A\sigma_B|
 +7N\bigl(|\sigma_A\lambda_B|+|\lambda_A\sigma_B|\bigr)
 +|\lambda_A\lambda_B|.}
\tag{5.4}

In particular, if

\[
 |\sigma_A|\le C_A/N,
 \qquad |\sigma_B|\le C_B/N,
\tag{5.5}

then

\[
 G_N\le
 44C_AC_B+\frac{175}{24}(C_A+C_B)+\frac{625}{576}.
\tag{5.6}

This is the main reduction.  Proving (5.5) would remove the sharp
second-order loss for this label family.  A bound on transverse cosine alone
would not suffice; the normalization by the full longitudinal mode norm is
essential.

## Two-precision recurrence through \(N=5\)

The numerical part evaluates the same closed face recurrence at 160 and 224
MPFR bits.  It reaches time order 28, required by the \(N=5\) output.  The two
precisions agree in the recorded quantities to relative error below
\(1.5\times10^{-43}\).  At \(N=2,3\), the gains and selected-root shares agree
with the exact R0.24 quadratic-field certificate to double-conversion
accuracy.

The entries at \(N=2,3\) inherit exact nonvanishing from R0.24.  The entries at
\(N=4,5\) are high-precision numerical probes.

| \(N\) | \(\sigma_A\) | \(\sigma_B\) | \(N|\sigma_A|\) | \(N|\sigma_B|\) | \(N^2|\sigma_A\sigma_B|\) |
|---:|---:|---:|---:|---:|---:|
| 2 | -0.0228918 | 0.0723710 | 0.0457835 | 0.144742 | 0.00662679 |
| 3 | -0.0711967 | 0.0306851 | 0.213590 | 0.0920553 | 0.0196621 |
| 4 | -0.0152943 | 0.0395507 | 0.0611772 | 0.158203 | 0.00967839 |
| 5 | -0.0290965 | 0.0128570 | 0.145483 | 0.0642850 | 0.00935235 |

No monotone decay is visible in each coordinate.  The scaled quantities
\(N|\sigma|\), however, remain below \(0.214\) at all four points.  This is
consistent with (5.5), but it does not prove it.

| \(N\) | generated gain \(G_N\) | \(G_N/S_N\) | \(G_N/[r_A r_B]\) | selected-root share |
|---:|---:|---:|---:|---:|
| 2 | 0.304560 | 0.00433464 | 0.0101520 | \(4.57375\times10^{-4}\) |
| 3 | 0.361556 | 0.00195675 | 0.00502161 | \(7.71697\times10^{-7}\) |
| 4 | 0.421619 | 0.00119323 | 0.00319408 | \(3.04096\times10^{-9}\) |
| 5 | 0.235806 | 0.000409433 | 0.00112289 | \(2.27410\times10^{-11}\) |

The generated gain remains below \(0.422\) in this sample.  Its ratio to the
sharp benchmark and its radius-normalized value both continue downward.  The
selected sharp root split also becomes rapidly smaller relative to the full
output coefficient.

## Channel cancellation and root splits

The four signed channel vectors do not add by their norms.  The ratio of the
actual gain to the sum of the four channel norms is

| \(N\) | channel cancellation ratio |
|---:|---:|
| 2 | 0.7575 |
| 3 | 0.4372 |
| 4 | 0.7631 |
| 5 | 0.4272 |

The even--odd alternation is compatible with the catalyst parity in (2.1),
but four values are insufficient to turn it into an identity.

The input-coefficient recurrence is edge dominated.  For \(a_N\), the
largest grouped root split has one leaf on the right.  For \(b_N\), it has
one leaf on the left.  The corresponding norm ratios relative to the full
input coefficient are

| \(N\) | dominant \(a_N\) split | ratio | dominant \(b_N\) split | ratio |
|---:|---:|---:|---:|---:|
| 2 | \(5+1\) | 0.4156 | \(1+4\) | 0.6317 |
| 3 | \(8+1\) | 1.0379 | \(1+7\) | 0.6579 |
| 4 | \(11+1\) | 0.9860 | \(1+10\) | 0.7226 |
| 5 | \(14+1\) | 1.2565 | \(1+13\) | 0.7879 |

A ratio above one is possible because other root splits partially cancel the
dominant contribution.  This identifies the present obstruction to an
all-\(N\) proof: a positive majorant can bound the numerator of the sharp
coordinate, but it cannot supply the signed lower bound on the complete
coefficient needed in the denominator of (3.5).

## Consequence and next test

R0.25 replaces the vague question “why is the generated gain small?” by a
specific estimate:

\[
 N|\sigma_{a_N}|+N|\sigma_{b_N}|=O(1).
\tag{8.1}
\]

The next calculation should exploit the edge dominance rather than extend a
table blindly.  The increments

\[
 a_{N+1}-a_N=(1,-3,3),\qquad
 b_{N+1}-b_N=(-1,-3,-3)
\]

contain three boundary leaves.  This suggests a three-leaf transfer system
for the endpoint families, with catalyst parity carried as a two-state
variable.  The next target is to derive that finite transfer system, isolate
the one-leaf attachment term, and bound the sum of the remaining root splits.

If the remainder is contractive after the \(N\sigma\) normalization, (8.1)
may close by induction.  If not, the first noncontractive companion family
will give a precise obstruction.  No claim about global regularity follows
until an all-label analytic estimate and the viscous remainder gates are also
closed.
