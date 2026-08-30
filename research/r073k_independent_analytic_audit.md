# R0.73K independent analytic audit

**Final decision:** ANALYTIC PASS

**Object audited:** `research/r073k_uniform_viscous_branch_proof.md`

**Method:** line-by-line operator-domain, quantifier, compactness, spectral,
and semigroup audit; no finite diagnostic was used as proof evidence

## 1. Initial findings and repair cycle

The first pass found no blocker but required three proof expansions before a
pass could be issued.

1. The compact correction in the Riesz projection proof had to be split into
   the two explicit terms
   \[
    (G_\varepsilon K-G_0K)R_\varepsilon
    +G_0K(R_\varepsilon-R_0).
   \]
   The second term requires the collectively compact adjoint family and
   joint strong convergence of the adjoint base resolvents.
2. The \(O(\varepsilon)\) pairing required both
   \(\ell_0(d)\in D(L)\), uniformly in \(d\), and
   \(P_\varepsilon H\subset D(B_\varepsilon)=D(L)\).
3. The reduced resolvent and semigroup argument required an explicit Riesz
   domain decomposition and a square-resolvent Bromwich contour shift on the
   reduced space.

All three repairs are present in the final proof text.

## 2. K1--K3: singular resolvent and projection transfer

**PASS.**  The common-core identity is used only to establish strong
convergence, uniformly for
\((d,z)\in[0,D_*]\times\mathcal Z\).  The proof does not claim full
norm-resolvent convergence.  The adjoint argument uses
\(\overline{\mathcal Z}\), as required.

The norm-continuous compact family \(K_d\) and its adjoint are collectively
compact.  This legitimizes both sandwiches

\[
 (R_{\varepsilon,d}-R_{0,d})K_d\to0,
 \qquad
 K_d(R_{\varepsilon,d}-R_{0,d})\to0
 \tag{2.1}
\]

in operator norm, uniformly in \(d,z\).  Equations (4.5a)--(4.5b) in the
proof then establish the norm convergence of the compact correction in the
full resolvent.  Analytic cancellation of the base resolvent inside the
right-half-plane disk gives

\[
 \sup_d\|P_\varepsilon(d)-P_0(d)\|\to0.
 \tag{2.2}
\]

The rank-one conclusion follows from the standard projection-pair argument
once the norm difference is below one.

## 3. K4: the \(O(\varepsilon)\) eigenvalue rate

**PASS.**  The explicit R0.73J adjoint potential has denominator bounded by

\[
 |W_d+2i\lambda_0(d)|>0.334.
 \tag{3.1}
\]

The final proof tracks the parameter-dependent periodic ODE into every fixed
Sobolev space and obtains

\[
 \ell_0(d)\in D(L),
 \qquad
 \sup_d\|L\ell_0(d)\|<\infty.
 \tag{3.2}
\]

The contour formula for \(B_\varepsilon P_\varepsilon\) proves
\(P_\varepsilon H\subset D(B_\varepsilon)=D(L)\).  Thus moving \(L\) from
the viscous right vector to the smooth inviscid left vector is legitimate:

\[
 (\lambda_\varepsilon-\lambda_0)
 \langle\ell_0,h_\varepsilon\rangle
 =-\varepsilon\langle L\ell_0,h_\varepsilon\rangle.
 \tag{3.3}
\]

The overlap lower bound and projection convergence control the denominator.
The constant \((11/5)C_L\) is arithmetically correct.

## 4. K5: symmetry, analyticity, conditioning, and anchor

**PASS.**  The reflection--conjugation map preserves \(H^2_{\rm per}\) and
commutes anti-linearly with the viscous generator.  It sends the single
spectral point in the conjugation-invariant disk to its conjugate; algebraic
multiplicity one therefore makes the point real.

For every fixed positive viscosity, the profile family is type A on the
common domain.  The common contour, Riesz differentiation, and bounded
profile derivative give a uniform \(P_\varepsilon'(d)\) bound.  The numerical
constant

\[
 {1\over0.5853}+{2\over25}<1.789<{9\over5}
 \tag{4.1}
\]

is correct, so the viscous normalized overlap is greater than \(5/9\).
The final quantitative anchor estimate proves uniform nonvanishing before
the analytic phase normalization is made.

## 5. K6: no pollution and reduced resolvent

**PASS.**  The proof treats the unbounded half-plane in three pieces:

- a high-imaginary Neumann region;
- a high-real-part dissipative region;
- an explicitly written compact rectangle outside the selected disk.

R0.73J excludes inviscid spectrum from the third region, and the uniform
Fredholm argument transfers that exclusion to small viscosity.  The Riesz
domain decomposition makes the selected disk a resolvent set for the
complementary part.  Applying the scalar maximum principle to matrix elements
inside that disk correctly completes the uniform reduced-resolvent bound.

The proof asserts the conservative uniform gap \(1/25\), not the unattained
endpoint \(0.047\).

## 6. K7: complementary semigroup

**PASS.**  The invariant complementary part generates the restricted
analytic semigroup.  A fixed line \(\operatorname{Re}z=\omega>K_*\) lies to
the right of a common growth bound.  Integration by parts first produces an
absolutely convergent square-resolvent integral.  That integral is moved
through the pole-free reduced strip to \(\operatorname{Re}z=b_K\); the
horizontal sides vanish uniformly at order \(|\tau|^{-2}\).

This gives

\[
 \|e^{tB_\varepsilon(d)}Q_\varepsilon(d)\|
 \le C e^{b_Kt}
 \tag{6.1}
\]

with one constant for all small \(\varepsilon\), all
\(d\in[0,D_*]\), and all \(t\ge0\).  No uniform analytic-sector angle is
assumed.  The inverse estimate on the rank-one block follows directly from
\(\lambda_\varepsilon>0.167\) and the projection bound.

## 7. Final ledger

```text
K1=PASS
K2=PASS
K3=PASS
K4=PASS
K5=PASS
K6=PASS
K7=PASS
explicitViscosityThreshold=NOT_AUDITED_AND_OPEN
finiteDiagnosticUsedAsProof=false
analyticAudit=PASS
```

The audit does not assess the finite diagnostic package, the future
adiabatic theorem, any nonlinear conclusion, or the Clay problem.
