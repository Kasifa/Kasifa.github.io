# R0.71N gap matrix — the complete scalar expansion returns to the known projective fusion

## 0. Claim boundary

This matrix audits one fixed-cell question left by R0.71M.  It starts from

\[
 \mathcal J_Q=z_{Q,t}+\nu\kappa_j^2z_Q
\]

and keeps \(B_{Q,t}\), \(d_{Q,t}\), and \(Y_t\) together before taking a
positive part or an absolute value.  The exact calculation returns to the
R0.71L normalization--projective identity.  Inserting the local filtered
enstrophy identity does not create a second coercive scalar fusion.

The exact statements below concern a classical periodic solution, one fixed
real smooth cutoff, and one fixed real-even scalar Fourier multiplier.  The
hard projective formulas are restricted to \(Y>0\) and \(d_Q>0\).

The finite-Fourier sign tests are diagnostics.  Until their coefficients and
roundoff margins are certified by exact convolution or interval arithmetic,
they are not theorem-level counterexamples.  This file proves no no-go
theorem, continuation criterion, regularity theorem, singularity result, or
solution of the Millennium problem.

## 1. Fixed-cell notation

On \(\mathbb T^3\) with normalized Haar measure, put

\[
 \omega=\operatorname{curl}u,\qquad
 L=\mathbb P(u\times\omega),\qquad
 Y=\|\omega\|_2^2,
\]

\[
 F=T_jL,\qquad W=T_j\omega,\qquad G=\operatorname{curl}F,
\]

and, for a cutoff \(\chi=\chi_Q\) that is independent of time,

\[
 C=\operatorname{curl}(\chi W),\qquad
 d=\|C\|_2^2,\qquad r=\sqrt d,\qquad
 B=\langle F,C\rangle.
\]

On \(Y>0\) and \(d>0\), define

\[
 E=\frac C r,\qquad
 (E\otimes E)V=\langle V,E\rangle E,\qquad
 P=I-E\otimes E,
\]

\[
 z=\frac{B}{\sqrt{Yd}},\qquad
 \lambda=\nu\kappa_j^2,
\]

\[
 N=F_t+\lambda F,\qquad
 M=C_t+\lambda C.
\]

The projector \(P\) acts in the real Hilbert space
\(L^2(\mathbb T^3;\mathbb R^3)\).  It is not the pointwise matrix obtained by
treating \(E(x)\) as a unit vector at each spatial point.  In particular,

\[
 P^2=P=P^*,\qquad PE=0,\qquad \operatorname{Ran}P=E^\perp,
\]

and

\[
 PF=F-\frac Bd C.
\]

## 2. Classification matrix

| Statement | Classification | Evidence | Required hypotheses | What it does not give |
|---|---|---|---|---|
| \(P=I-E\otimes E\) is the global corank-one orthogonal projection onto \(E^\perp\) | exact theorem | Hilbert-space rank-one projection algebra | real \(L^2\), \(d>0\) | no pointwise spatial projection and no definition at \(d=0\) |
| \(\mathcal J=B_t/(\sqrt Y r)-\tfrac12z(Y_t/Y+d_t/d)+\lambda z\) | exact rewrite | quotient rule applied before any sign split | \(Y>0,d>0\), classical time derivatives | no estimate or sign |
| \(B_t=\langle N,C\rangle+\langle F,M\rangle-2\lambda B\) | exact rewrite | differentiate \(B=\langle F,C\rangle\) and insert \(N,M\) | fixed Hilbert pairing | no control of \(F_t\) or \(C_t\) |
| \(\langle F,M\rangle=\langle PF,PM\rangle+(B/d)(d_t/2+\lambda d)\) | exact theorem | radial/projective decomposition and \(\langle C,M\rangle=d_t/2+\lambda d\) | \(d>0\) | no positivity of either summand |
| The \(d_t/d\) and \(\lambda\) rows cancel after the previous three identities are combined | exact theorem | direct scalar algebra in Section 3 | same | this is the R0.71L fusion, not a new coercive identity |
| \(e_t+\nu D=B+(\nu/2)R_\chi\) for \(e=\tfrac12\int\chi|W|^2\) | exact theorem | fixed-cutoff filtered-enstrophy identity | \(\chi_t=0\), periodic curl/Laplacian integration by parts | no identity between \(e\) and \(d\) |
| \(Y_t=2\langle\omega,\operatorname{curl}L\rangle-2\nu\|\nabla\omega\|_2^2\) | exact theorem | global vorticity equation | classical periodic solution | \(Y_t\) is not pure viscous dissipation in three dimensions |
| \(e\) and \(d\) are distinct state variables | exact theorem | the one-mode family in Section 4 has fixed \(e\) and frequency-dependent \(d\) | admissible smooth divergence-free blocks | no replacement of \(d_t/d\) by an enstrophy derivative |
| \(z\) is not a correlation coefficient bounded by one | exact theorem | amplitude homogeneity gives \(z[Au]=A z[u]\); Cauchy gives only \(|z|\le\|F\|_2/\sqrt Y\) | a datum with \(B\ne0\) | no universal \([-1,1]\) range |
| The fixed-cutoff formulas acquire \(\operatorname{curl}(\chi_tW)\) when \(\chi\) moves | exact theorem | product rule for \(C=\operatorname{curl}(\chi W)\) | time-dependent smooth cutoff | no reuse of the fixed-cell identity for moving or refreshed cells |
| The sampled \(\mathcal J\) takes both signs | finite-Fourier diagnostic | deterministic five-mode tests in Section 6 | declared multiplier, cutoff, viscosity, grid, and phases | not yet a formal sign counterexample |
| An exact or interval-certified negative witness would rule out a universal pointwise nonnegative pairing | conditional implication | one certified smooth initial datum suffices | local classical existence and a rigorous sign certificate | no no-go for integrated signed cancellation |
| A separately proved bound for the positive joint creation and all denominator/refresh faces would feed the earlier weighted-BV identity | conditional implication | R0.71I--R0.71K scalar BV algebra | the additional bound must be proved independently | no such bound follows here from Leray energy |
| Uniform control as \(d\downarrow0\), including internal faces | open / blocked | \(E=C/\|C\|\) can lose its limiting direction | hard-face or soft-denominator analysis | current hard-cell algebra is only componentwise on \(\{d>0\}\) |
| Leray-level payment of the complete signed source | open / blocked | the exact rewrite retains \(F_t\), \(Y_t/Y\), and the angular source | finite-shell regularization and uniform estimates | no continuation theorem |
| Moving cells, refresh atoms, infinite frame--cell passage, and priority comparison | open / blocked | outside the fixed finite gate | separate proofs and literature audit | none is settled by R0.71N |

## 3. Exact scalar cancellation

Write

\[
 y=\frac{Y_t}{Y},\qquad \delta=\frac{d_t}{d}.
\]

The quotient rule gives

\[
 \boxed{
 \mathcal J
 =\frac{B_t}{\sqrt Y\,r}
 -\frac z2(y+\delta)+\lambda z.}
 \tag{3.1}
\]

Since \(F_t=N-\lambda F\) and \(C_t=M-\lambda C\),

\[
 \boxed{
 B_t=\langle N,C\rangle+\langle F,M\rangle-2\lambda B.}
 \tag{3.2}
\]

Moreover,

\[
 \langle C,M\rangle
 =\langle C,C_t+\lambda C\rangle
 =\frac12d_t+\lambda d,
\]

so the radial/projective decomposition is

\[
 \boxed{
 \langle F,M\rangle
 =\langle PF,PM\rangle
 +\frac Bd\left(\frac12d_t+\lambda d\right).}
 \tag{3.3}
\]

Substituting (3.2)--(3.3) into (3.1) cancels both the radial logarithmic
derivative and the nominal heat rate:

\[
 \boxed{
 \mathcal J
 =\frac{\langle N,E\rangle}{\sqrt Y}
 +\frac{\langle PF,PM\rangle}{\sqrt Y\,r}
 -\frac y2z.}
 \tag{3.4}
\]

Equation (3.4) is exactly the R0.71L normalization--projective identity in
scalar coordinates.  Re-expanding it and then recovering (3.4) does not
produce an additional cancellation budget.

For the fixed cutoff,

\[
 H=(\Delta+\kappa_j^2)W,\qquad
 S=G+\nu H,\qquad
 M=\operatorname{curl}(\chi S),
\]

and periodic curl self-adjointness gives

\[
 \langle F,M\rangle
 =\int\chi G\cdot(G+\nu H).
 \tag{3.5}
\]

If (3.5) is inserted without the projective decomposition, then

\[
 \mathcal J
 =\frac{\langle N,E\rangle}{\sqrt Y}
 +\frac{1}{\sqrt Y\,r}\int\chi G\cdot(G+\nu H)
 -\lambda z-\frac z2(y+\delta).
 \tag{3.6}
\]

The source square inside (3.6) is therefore coupled to signed viscous,
radial, and normalization terms.  It is not an independent coercive row.

## 4. Why local filtered enstrophy is not the projective state

Define

\[
 e=\frac12\int\chi|W|^2,\qquad
 D=\int\chi|\nabla W|^2,\qquad
 R_\chi=\int(\Delta\chi)|W|^2.
\]

For a fixed cutoff,

\[
 \boxed{e_t+\nu D=B+\frac\nu2R_\chi,}
 \tag{4.1}
\]

or

\[
 B=e_t+\nu D-\frac\nu2R_\chi.
 \tag{4.2}
\]

Using (4.2) in (3.1) requires

\[
 B_t=e_{tt}+\nu D_t-\frac\nu2(R_\chi)_t.
 \tag{4.3}
\]

Thus the substitution introduces second time derivatives and differentiated
dissipation/cutoff moments.  It does not identify them with \(d_t\).

The distinction already appears for \(\chi=1\).  For

\[
 W_k(x)=(0,\cos(kx_1),0),
\]

which is smooth, divergence free, and zero mean,

\[
 e_k=\frac14,\qquad
 d_k=\|\operatorname{curl}W_k\|_2^2=\frac{k^2}{2}.
 \tag{4.4}
\]

Hence no universal scalar identity \(d=f(e)\) is available.  A broad annulus
gives only frequency-comparability estimates, and a nonconstant cutoff adds
the further interior, collar, and cross terms in
\(\operatorname{curl}(\chi W)\).

## 5. Domain, cutoff, and normalization risks

### 5.1 Positive denominators

The hard direction \(E=C/r\) and the projection \(P\) exist only for
\(d>0\).  Even when \(z\) stays bounded as \(d\downarrow0\), the direction
of \(C\) need not converge and the separate factor \(d_t/d\) can diverge.
The identities must therefore be integrated on connected components of
\(\{d>0\}\), with their endpoint faces retained, or replaced by a separately
audited soft denominator.

The normalization also requires \(Y>0\).  For a zero-mean periodic velocity,
\(Y=0\) forces the zero field.  This separates the trivial solution but does
not provide a quantitative lower bound for \(Y\) along a nontrivial family.

### 5.2 The range of \(z\)

Cauchy--Schwarz gives only

\[
 |z|\le\frac{\|F\|_2}{\sqrt Y}.
 \tag{5.1}
\]

At one instantaneous smooth datum, amplitude scaling gives

\[
 F[Au]=A^2F[u],\quad C[Au]=AC[u],\quad
 Y[Au]=A^2Y[u],\quad d[Au]=A^2d[u],
\]

and consequently

\[
 z[Au]=A z[u].
 \tag{5.2}
\]

Every smooth finite-Fourier datum has a local classical NSE solution, so
(5.2) is compatible with the solution class at the initial time.  The name
``normalized coefficient'' must not be interpreted as a cosine correlation
or a bound \(|z|\le1\).

### 5.3 Fixed versus moving cutoffs

If \(\chi=\chi(t,x)\), then

\[
 C_t=\operatorname{curl}(\chi W_t)
     +\operatorname{curl}(\chi_tW),
\]

\[
 M=\operatorname{curl}(\chi S)
   +\operatorname{curl}(\chi_tW),
 \tag{5.3}
\]

and (4.1) acquires

\[
 \frac12\int\chi_t|W|^2.
\]

A refresh makes these terms distributional and adds nonlinear time faces.
Neither case is covered by the fixed-cell calculation.

The movement of curl in (3.5) also uses the absence of a physical boundary.
On a domain with boundary, the corresponding curl integration by parts has a
boundary term.

### 5.4 Viscous center mismatch

On one Fourier mode,

\[
 \widehat H(k)=(\kappa_j^2-|k|^2)m_j(k)\widehat\omega(k).
\]

For a broad relative annulus this factor is generally of order
\(\kappa_j^2\) and changes sign across the nominal center.  The multiplier,
its support, and the declared \(\kappa_j\) must therefore be locked in every
certificate.  Neither annular support nor the notation \(\kappa_j\) makes
\(H\) small.

## 6. Finite-Fourier diagnostics

The standalone checker `research/r071n_independent_audit.py` declares five
positive frequencies and two explicit sets of complex polarization vectors.
Every vector is projected onto its frequency-orthogonal plane and paired with
its conjugate negative mode.  The filter has \(\kappa=4\), the viscosity is
\(\nu=0.2\), the cutoff is fixed, positive, and trigonometric, and the same
calculation is repeated at grid orders 48, 64, and 80.

### 6.1 Both signs of the complete scalar source

At grid order 64 the two witnesses give

\[
 \begin{array}{c|r|r|r|r}
 \text{witness}&z&\mathcal P^\square&\mathfrak R&\mathcal J\\ \hline
 \texttt{positiveJ\_seed49}
   &0.0037338305&5023.6425100&749.9219443&1.3523543\\
 \texttt{negativeJ\_seed5}
   &0.0019598744&5167.6945795&-25941.2940133&-7.3713441
 \end{array}
\]

The underlying fields are smooth finite-Fourier initial data and hence start
local classical NSE trajectories.  The sampled signs strongly reject using
a presumed sign in the next proof attempt.  They remain diagnostics until an
exact or outward-rounded certificate proves the signs independently of FFT
roundoff.  The five independently assembled representations of \(\mathcal J\)
agree to relative residual at most \(4.82\times10^{-16}\); the maximum
48/64/80 cross-resolution relative difference is \(1.26\times10^{-14}\).

## 7. Assertions required in an R0.71N certificate

1. State the real Hilbert space and verify \(P^2=P=P^*\), \(PE=0\), and
   \(PF=F-(B/d)C\).  Do not implement \(P\) as a pointwise matrix.
2. Require \(Y>0\) and \(d>0\), and state whether the result is pointwise or
   integrated on a connected positive-denominator component.
3. Lock \(T_j\), \(\kappa_j\), \(\chi_Q\), \(\nu\), the spatial domain, and
   the inner-product normalization.
4. Verify (3.1), (3.2), and (3.3) independently before checking the
   cancellation in (3.4).
5. Verify the full three-dimensional formula for \(Y_t\), including vortex
   stretching.
6. Keep \(e\) and \(d\) as different recorded variables.  A test must fail if
   either one is silently substituted for the other.
7. Record the moving-cutoff residual \(\operatorname{curl}(\chi_tW)\) and
   assert that it is zero only because the certified cutoff is fixed.
8. Check the amplitude homogeneity of \(z\) and reject any assumed
   \(|z|\le1\) bound.
9. For a Fourier sign certificate, record spectral support, Nyquist margin,
   zero-mode quadrature margin, coefficient representation, precision, and a
   lower bound on the signed margin.
10. Require a second implementation of the quotient, projective, and radial
    forms.  Agreement of two formulas sharing one intermediate is not
    independent verification.
11. Label the finite-Fourier signs as diagnostics unless an exact or interval
    certificate has been completed.

## 8. Finite route decision

The checked route has one exact outcome:

\[
 \boxed{
 \text{the complete }(B_t,d_t,Y_t)\text{ expansion returns to the known}
 \text{ normalization--projective fusion}.}
\]

The local filtered-enstrophy substitution leaves differentiated local
moments rather than a second quadratic fusion.  The finite-Fourier tests also
show that \(\mathcal J\) should not be assigned a presumed sign in the next
estimate.

What remains open is an estimate, not another rearrangement of the same
identity: a bound for the complete signed source or its positive creation
that also survives denominator faces, moving/refresh terms, frame--cell
summation, and the Leray limit without assuming a known regularity norm.
