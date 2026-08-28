# R0.72U independent analytic audit

**Date:** 2026-08-28

**Audit outcome:** the uncut bounded-chart graph estimate is **PASS** after
one trace correction.  The proof may use endpoint traces of two scalar
moments, but it may not assume \(L^2_X\)-valued endpoint traces of the full
function.  The literal spacetime-cutoff inequality is mathematically true
but spatially Poincare-trivial.  The bounded-chart result does not yet prove
a whole-line block contraction, periodic transfer, or any Navier--Stokes
regularity statement.

## 0. Exact statement under audit

Let

\[
 I=(s_-,s_+),\qquad J\Subset\mathbb R,\qquad 0\in J^\circ,
\]

and let

\[
 P_{c,\sigma}
 =\partial_S-i\sigma\bigl(X^3+6(c+S)X\bigr),
 \qquad c\in\mathbb R,\quad \sigma\in\{-1,1\}.
 \tag{0.1}
\]

The negative space in this audit is

\[
 H^{-1}_D(J):=(H^1_0(J))^*.
 \tag{0.2}
\]

The claimed graph space is

\[
 \mathcal G_{c,\sigma}
 =\left\{v\in L^2(I;H^1(J)):
 P_{c,\sigma}v\in L^2(I;H^{-1}_D(J))\right\}.
 \tag{0.3}
\]

There is no temporal zero-trace condition and no spatial Dirichlet
condition.  The theorem under audit is the center-uniform estimate

\[
 \boxed{
 \|v\|_{L^2(I\times J)}
 \le C_{I,J}\left(
 \|v_X\|_{L^2(I\times J)}
 +\|P_{c,\sigma}v\|_{L^2(I;H^{-1}_D(J))}
 \right),}
 \tag{0.4}
\]

with \(C_{I,J}\) independent of \(c\) and of the two choices of
\(\sigma\).

**Verdict on (0.4): PASS.**  Sections 2--5 give an independent derivation.

## 1. Trace claim: one shortcut fails and the corrected route passes

Write \(r=P_{c,\sigma}v\).  On a fixed bounded rectangle the potential in
(0.1) is bounded for each fixed \(c\), so

\[
 v_S=r+i\sigma\bigl(X^3+6(c+S)X\bigr)v
 \in L^2(I;H^{-1}_D(J)).
 \tag{1.1}
\]

Together with \(v\in L^2(I;L^2(J))\), this gives an
\(H^{-1}_D(J)\)-valued continuous representative.  It does **not** give

\[
 v\in C(\overline I;L^2(J)).
 \tag{1.2}
\]

The usual Lions \(L^2\)-trace theorem would require a compatible Gelfand
triple with \(v\in L^2(I;H^1_0(J))\).  Arbitrary spatial traces in (0.3)
do not supply that hypothesis.

Consequently, an endpoint estimate written directly with
\(\|v(s_\pm)\|_{L^2(J)}\) is **FAIL** under the declared graph-space
hypotheses.

There is, however, a sufficient scalar statement.  If
\(\psi\in H^1_0(J)\), then

\[
 M_\psi(S):=\langle v(S),\psi\rangle
 \]

belongs to \(H^1(I)\), with

\[
 M_\psi'(S)=\langle v_S(S),\psi\rangle.
 \tag{1.3}
\]

Thus \(M_\psi(s_-)\) and \(M_\psi(s_+)\) are well defined.  The corrected
proof below uses only two such scalar moments.  This trace route is
**PASS**.

## 2. Spatial reduction and moment algebra

Choose a real even function

\[
 \rho\in C_c^\infty(J),\qquad
 \int_J\rho(X)\,dX=1,
\]

and put

\[
 \mu_2=\int_JX^2\rho(X)\,dX>0.
 \tag{2.1}
\]

For each \(S\), let \(m(S)\) be the unweighted mean of \(v(S,\cdot)\), and
write \(v=m+w\).  Poincare modulo constants gives

\[
 \|w\|_{L^2(I\times J)}
 \le C_J\|v_X\|_{L^2(I\times J)}.
 \tag{2.2}
\]

Define

\[
 A=\int_Jv\rho,\qquad
 B=\int_JvX\rho,
 \tag{2.3}
\]

and, for \(k=2,3,4\),

\[
 C_k=\int_JvX^k\rho.
 \tag{2.4}
\]

The parity of \(\rho\), followed by (2.2), gives

\[
 \begin{aligned}
 A&=m+e_A,& \|e_A\|_{L^2(I)}&\le C\|v_X\|_{L^2},\\
 B&=e_B,& \|B\|_{L^2(I)}&\le C\|v_X\|_{L^2},\\
 C_2&=\mu_2A+F_2,& \|F_2\|_{L^2(I)}&\le C\|v_X\|_{L^2},\\
 C_3&=e_3,& \|C_3\|_{L^2(I)}&\le C\|v_X\|_{L^2}.
 \end{aligned}
 \tag{2.5}
\]

Also

\[
 \|C_4\|_{L^2(I)}
 \le C\|v\|_{L^2(I\times J)}.
 \tag{2.6}
\]

Pairing \(v_S=r+i\sigma[X^3+6(c+S)X]v\) with \(\rho\) and \(X\rho\)
gives the exact scalar equations

\[
 A'=iLB+E_0,
 \tag{2.7}
\]

\[
 B'=iL\mu_2A+iLF_2+E_1,
 \tag{2.8}
\]

where

\[
 L=6\sigma c,
 \tag{2.9}
\]

\[
 E_0=\langle r,\rho\rangle+i\sigma C_3+i6\sigma SB,
 \tag{2.10}
\]

and

\[
 E_1=\langle r,X\rho\rangle+i\sigma C_4+i6\sigma SC_2.
 \tag{2.11}
\]

These identities independently confirm the signs and the factor \(6c\).
For a normalized contradiction sequence with

\[
 \|v\|_{L^2(I\times J)}=1,
 \qquad
 \delta:=\|v_X\|_{L^2}+
 \|r\|_{L^2H^{-1}_D}\longrightarrow0,
 \tag{2.12}
\]

they imply

\[
 \|A\|_2\le C,\quad
 \|B\|_2+\|F_2\|_2+\|E_0\|_2\le C\delta,
 \quad
 \|E_1\|_2\le C.
 \tag{2.13}
\]

The moment algebra is **PASS**.

## 3. Large-center identity and endpoint audit

Suppose

\[
 |c|\longrightarrow\infty.
\]

Since \(A,B\in H^1(I)\), scalar integration by parts is legitimate:

\[
 \begin{aligned}
 \int_I B'\overline A\,dS
 &= [B\overline A]_{s_-}^{s_+}
 -\int_I B\overline{A'}\,dS\\
 &= [B\overline A]_{s_-}^{s_+}
 +iL\int_I|B|^2\,dS
 -\int_I B\overline{E_0}\,dS.
 \end{aligned}
 \tag{3.1}
\]

On the other hand, (2.8) gives

\[
 \int_I B'\overline A\,dS
 =iL\mu_2\int_I|A|^2\,dS
 +iL\int_IF_2\overline A\,dS
 +\int_IE_1\overline A\,dS.
 \tag{3.2}
\]

Taking imaginary parts, allowing either sign of \(L\), and estimating the
error terms yields

\[
 \begin{aligned}
 |L|\mu_2\|A\|_2^2
 \le{}& |[B\overline A]_{s_-}^{s_+}|
 +|L|\|B\|_2^2
 +\|B\|_2\|E_0\|_2\\
 &+|L|\|F_2\|_2\|A\|_2
 +\|E_1\|_2\|A\|_2.
 \end{aligned}
 \tag{3.3}
\]

It remains to check that the endpoint term does not hide an unjustified
trace or an uncontrolled factor of \(c\).

For every scalar \(f\in H^1(I)\),

\[
 |f(s_-)|^2+|f(s_+)|^2
 \le C_I\left(\|f\|_2^2+\|f\|_2\|f'\|_2\right).
 \tag{3.4}
\]

Equations (2.7)--(2.13) give

\[
 \|A'\|_2\le C(|L|\delta+\delta),
 \qquad
 \|B'\|_2\le C(|L|+1).
 \tag{3.5}
\]

Therefore

\[
 |A(s_\pm)|^2\le C(1+|L|\delta),
 \tag{3.6}
\]

\[
 |B(s_\pm)|^2
 \le C\left(\delta^2+\delta(|L|+1)\right).
 \tag{3.7}
\]

For

\[
 |L|\ge1,\qquad \delta\le1,
\]

these bounds imply

\[
 \frac{|B(s_\pm)A(s_\pm)|}{|L|}
 \le C\left(\delta+\sqrt{\frac{\delta}{|L|}}\right)
 \longrightarrow0.
 \tag{3.8}
\]

No rate relation between \(\delta\to0\) and \(|c|\to\infty\) is required.
This is the point at which a direct \(L^2\)-trace shortcut for \(v\) would
fail, while the scalar-moment proof closes.

Dividing (3.3) by \(|L|\) and using (2.13) and (3.8) gives

\[
 \mu_2\|A\|_2^2
 \le o(1)+C\delta+C\delta^2+\frac{C}{|L|}.
 \tag{3.9}
\]

Hence \(A\to0\).  Equations (2.2) and (2.5) then give

\[
 \|v\|_{L^2(I\times J)}
 \le C\left(\|A\|_{L^2(I)}+\delta\right)
 \longrightarrow0,
\]

contradicting (2.12).  The large-\(|c|\) argument, including its endpoint
terms, is **PASS**.

## 4. Bounded-center compactness audit

Suppose \(c_n\) remains bounded and (2.12) holds.  After taking a
subsequence, \(c_n\to c_*\) and \(\sigma_n\) is constant.  By (2.2),
\(v_n-m_n\to0\) strongly in \(L^2\).

The potential is uniformly bounded in this regime.  Equation (2.7) shows
that \(A_n\) is bounded in \(H^1(I)\), hence precompact in \(L^2(I)\).
Since \(A_n-m_n\to0\), the sequence \(v_n\) converges strongly to a
function \(m(S)\) independent of \(X\).

Passing to the distributional limit gives

\[
 m'(S)-i\sigma\bigl(X^3+6(c_*+S)X\bigr)m(S)=0.
 \tag{4.1}
\]

Differentiating in \(X\),

\[
 \bigl(3X^2+6(c_*+S)\bigr)m(S)=0.
 \tag{4.2}
\]

For each \(S\), the polynomial in (4.2) is not identically zero on \(J\).
Thus \(m=0\), contradicting the unit normalization.  The bounded-center
argument is **PASS**.

Combining Sections 3 and 4 proves (0.4) uniformly for all
\(c\in\mathbb R\).

## 5. Literal cutoff audit

If the advertised cutoff is compactly supported in the spatial interior and

\[
 v=\chi u,
\]

then \(v(S,\cdot)\in H^1_0(J)\).  Spatial Poincare alone gives

\[
 \|\chi u\|_{L^2(I\times J)}
 \le \frac{|J|}{\pi}
 \|\partial_X(\chi u)\|_{L^2(I\times J)}.
 \tag{5.1}
\]

The transport residual is unnecessary.  Therefore:

- the literal cutoff inequality is **PASS** as a formal inequality;
- the claim that (5.1) detects the A2 spacetime geometry is **FAIL**;
- a time-compact graph estimate also cannot by itself certify enhanced
  dissipation, because its cutoff derivative can pay for nondecaying modes.

The last point has an elementary zero-potential proof even if the spatial
zero trace is removed.  Put \(P_0=\partial_S\), retain arbitrary spatial
traces, and suppose that the \(H^{-1}_D(J)\)-continuous representative of
\(v\) has zero trace at one temporal endpoint, say \(v(s_-)=0\).  With the
same normalized probe \(\rho\), set

\[
 A(S)=\langle v(S),\rho\rangle.
\]

Then \(A(s_-)=0\), \(A'=\langle \partial_Sv,\rho\rangle\), and one-dimensional
Poincare gives

\[
 \|A\|_{L^2(I)}
 \le C_I\|\partial_Sv\|_{L^2(I;H^{-1}_D(J))}.
 \tag{5.2}
\]

The spatial Poincare-modulo-constants estimate and
\(A=m+O(\|v_X\|_{L^2(J)})\) therefore give

\[
 \boxed{
 \|v\|_{L^2(I\times J)}
 \le C_{I,J}\left(
 \|v_X\|_{L^2(I\times J)}
 +\|P_0v\|_{L^2(I;H^{-1}_D(J))}
 \right).}
 \tag{5.3}
\]

Thus the temporal-zero-trace theorem already holds when the multiplication
potential is identically zero.  It cannot, by itself, distinguish mixing or
enhanced dissipation.

The nontrivial R0.72U theorem is (0.4): no temporal cutoff, no spatial zero
trace, and a constant uniform in the interval center.

This distinction is substantive.  If the entire multiplication potential is
replaced by zero, so that the operator becomes \(\partial_S\), then the
uncut function \(v\equiv1\) has \(v_X=0\) and \(Pv=0\), so (0.4) fails.
The uncut estimate therefore contains mixing information that the literal
cutoff inequality does not.

## 6. Solution-level implication and its exact boundary

Let a solution on the bounded chart satisfy

\[
 P_{c,\sigma}u=u_{XX}
 \tag{6.1}
\]

in distributions.  Since test functions in \(H^1_0(J)\) vanish at the
spatial boundary,

\[
 \|u_{XX}\|_{H^{-1}_D(J)}
 \le \|u_X\|_{L^2(J)}.
 \tag{6.2}
\]

Applying (0.4) gives

\[
 \boxed{
 \|u\|_{L^2(I\times J)}
 \le 2C_{I,J}\|u_X\|_{L^2(I\times J)}.}
 \tag{6.3}
\]

Because \(C_{I,J}\) is independent of \(c\), (6.3) is a genuine
bounded-chart, all-start solution observability estimate.  This implication
is **PASS**.

It is not yet a whole-line contraction.  On a bounded chart with arbitrary
spatial traces, the local energy balance contains the boundary flux

\[
 2\operatorname{Re}[u_X\overline u]_{\partial J}.
 \tag{6.4}
\]

Estimate (6.3) does not control (6.4).  On the whole line, (0.4) controls
only the mass inside one fixed \(J\); the bounded-interval Poincare reduction
does not control the tails.  A partition introduces cutoff commutators, and
The cubic time-dependent chart potential is not a periodic coefficient to
which the chart theorem can be transferred without additional work.

## 7. Claim matrix and release boundary

| Claim | Verdict | Reason |
|---|---:|---|
| Literal spatial-cutoff inequality | **PASS, trivial** | Spatial Poincare proves it without \(P_{c,\sigma}\). |
| Literal cutoff is an A2 observability certificate | **FAIL** | The residual and A2 polynomial are unused. |
| \(L^2_X\)-valued endpoint traces of arbitrary \(v\in\mathcal G_{c,\sigma}\) | **FAIL** | The graph space gives \(H^{-1}_D\) continuity, not the compatible \(L^2\) trace theorem. |
| Scalar endpoint traces of \(A=\langle v,\rho\rangle\), \(B=\langle v,X\rho\rangle\) | **PASS** | Both moments lie in \(H^1(I)\). |
| Large-\(|c|\) endpoint bound | **PASS** | Equation (3.8) tends to zero with no hidden rate assumption. |
| Uncut bounded-chart graph estimate (0.4) | **PASS** | Bounded centers follow by compactness; large centers follow from the two-moment identity. |
| Bounded-chart all-start solution observability (6.3) | **PASS** | \(u_{XX}:L^2\to H^{-1}_D\) is paid by \(u_X\). |
| Whole-line block contraction | **OPEN** | Spatial tails and chart-boundary flux are not controlled. |
| Periodic transfer | **OPEN** | No periodic localization/commutator theorem is proved. |
| Nonlinear Navier--Stokes closure | **OPEN** | No nonlinear vortex-stretching bootstrap follows from the model estimate. |
| Clay problem | **OPEN** | The result is a linear local-model estimate only. |

The accepted release boundary is therefore

\[
 \boxed{
 \begin{gathered}
 \texttt{boundedChartGraph=PASS},\qquad
 \texttt{centerUniformLocalGraphCoercivity=CLOSED},\\
 \texttt{boundedChartAllStartObservability=PASS},\qquad
 \texttt{localSolutionObservability=CLOSED},\\
 \texttt{wholeLineBlock=OPEN},\qquad
 \texttt{wholeLineBlockContraction=OPEN},\\
 \texttt{periodicTransfer=OPEN},\qquad
 \texttt{Clay=OPEN}.
 \end{gathered}}
\]
