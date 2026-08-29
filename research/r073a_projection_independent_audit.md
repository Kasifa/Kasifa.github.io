# R0.73A independent audit: moving projection and positive-gap dual obstruction

**Date:** 2026-08-29

**Role:** independent re-derivation of the moving rank-one projection,
orthogonal tangent line, finite Fourier leakage, and positive-gap dual
obstruction in `research/r073a_projection_derivation_agent.md`, followed by a
scope audit against `research/r073a_report-source.md`.

**Decision:** **ANALYTIC PASS WITH SCOPE EDITS APPLIED.** The
moving-projection signs, the necessary-and-sufficient transported-dual
condition, the sharp projection-speed constant, all four coefficients of
the vector \(G\), the two-mode leakage coefficients, and the \(g^{-1}\)
dual-pressure lower bound all pass an independent derivation. No numerical
constant or algebraic sign failed. The nonzero-\(c\), operator-domain,
compact-\(d\), common-space, and pressure-component qualifications listed in
Sec. 8 have been applied to the canonical report, internal derivation, and
gap matrix and were rechecked after editing.

This audit uses no literature assertion and is not by itself a release
authorization.

---

## 0. Decision ledger

| Item audited | Decision | Independent conclusion |
|---|---|---|
| exact gapless tangent orbit \(\phi_d=\mathscr A_0\phi\) | **PASS** | follows from \(\mathscr B_0\phi=0\) and the two heat rates |
| \(P^2=P\), \(P_d\), and \(Q\mathscr AP=P_dP\) | **PASS** | signs agree with a first-slot conjugate-linear pairing |
| amplitude/complement equations | **PASS** | the complement equation is exactly closed and the system is triangular |
| two-sided moving invariance | **PASS WITH DOMAIN HYPOTHESES** | equivalent to \(\psi_d=-\mathscr A^*\psi\) for strong/domain-compatible objects |
| anti-parabolic transported dual | **PASS WITH SCOPE** | forward leading term is \(+\mathcal L_0\); finite-mode obstruction requires \(c\ne0\) |
| orthogonal projection speed | **PASS** | \(\|(P_\perp)_d\|=3r/(1+r^2)\le3/2\), sharply |
| explicit \(G=\mathscr B_0^*\phi\) | **PASS** | coefficients \(-3ab/16,3a^2/32,-37ab/144,3b^2/32\) all agree |
| orthogonal defect and projected blocks | **PASS** | \(h_\perp=(2\zeta+icG)/N\) |
| two-mode pressure leakage | **PASS** | \(\mathscr B_0q=-3(a x_2+2b x_1)(\cos x-\cos3x)/16\) |
| fixed two-mode OS invariance, stated without a condition on \(c\) | **FAIL AS UNQUALIFIED** | false for \(c\ne0\), but true in the trivial case \(c=0\) |
| return coupling and higher-mode cascade | **PASS WITH \(c\ne0\)** | the pressure orbit reaches arbitrarily high odd modes |
| normalized-dual constant coefficient \(1/g\) | **PASS** | forced exactly by \(\langle\psi,\phi\rangle=1\) |
| projection/raw-adjoint dichotomy | **PASS WITH FIXED/COMPACT \(d\)** | at least one is \(g^{-1}\)-scale in unweighted coordinates |
| bounded-projection pressure off-block lower bound | **PASS** | \(Q^*\mathscr B^*\psi\) retains \(g^{-1}-O(1)\) |
| full OS off-block divergence, stated without the \(|c|\) factor | **FAIL AS UNQUALIFIED** | the audited pressure component is \(g^{-1}\); the OS pressure block is \(|c|g^{-1}\) |
| norm discontinuity across two different Hilbert spaces | **FAIL AS A BARE STATEMENT** | a common-space identification or extension must first be declared |

---

## 1. Conventions and the tangent orbit

Use

\[
 \langle f,g\rangle_0
 =\frac1{2\pi}\int_0^{2\pi}\overline f g\,dx,
 \qquad
 (u\otimes v)f=u\langle v,f\rangle_0.
 \tag{1.1}
\]

The pairing is conjugate-linear in its first argument. Put

\[
 a=e^{-d},\qquad b=e^{-4d},
 \tag{1.2}
\]

\[
 W=-\frac a2\sin x+\frac b4\sin2x,
 \qquad
 \phi=W_{xx}=\frac a2\sin x-b\sin2x.
 \tag{1.3}
\]

On \(H_0=L^2_0(\mathbb T)\), let

\[
 \mathcal L_0=-\partial_x^2,
 \qquad
 \mathscr B_0q=Wq+\phi\mathcal L_0^{-1}q,
 \qquad
 \mathscr A_0=-\mathcal L_0-ic\mathscr B_0,
 \tag{1.4}
\]

where \(c\in\mathbb R\). Directly,

\[
 \mathcal L_0^{-1}\phi=-W,
 \qquad
 \mathscr B_0\phi=W\phi-\phi W=0,
 \tag{1.5}
\]

and

\[
 \phi_d=-\frac a2\sin x+4b\sin2x=-\mathcal L_0\phi.
 \tag{1.6}
\]

Therefore

\[
 \boxed{\phi_d=\mathscr A_0(d)\phi.}
 \tag{1.7}
\]

This is a trajectory identity, not an instantaneous eigenvector identity.
Both Fourier coefficients are nonzero at every finite \(d\), so \(\phi_d\)
is not proportional to \(\phi\).

The adjoint calculation also passes. Since the domain is \(H_0\), the
constant mode must be removed before pairing back against a mean-zero test
function:

\[
 \boxed{
 \mathscr B_0^*=\Pi_0M_W+\mathcal L_0^{-1}\Pi_0M_\phi,
 \qquad
 \mathscr A_0^*=-\mathcal L_0+ic\mathscr B_0^*.}
 \tag{1.8}
\]

---

## 2. Moving rank-one algebra from first principles

**Decision: PASS, subject to the domain statement in Sec. 8.**

Let \(\phi_d=\mathscr A\phi\), let
\(\langle\psi,\phi\rangle=1\), and define

\[
 P=\phi\otimes\psi,
 \qquad Q=I-P.
 \tag{2.1}
\]

Normalization gives \(P^2=P\) and

\[
 \langle\psi_d,\phi\rangle
 +\langle\psi,\phi_d\rangle=0.
 \tag{2.2}
\]

Differentiation yields

\[
 P_d=\phi_d\otimes\psi+\phi\otimes\psi_d.
 \tag{2.3}
\]

On one hand,

\[
 Q\mathscr AP=(Q\phi_d)\otimes\psi.
 \tag{2.4}
\]

On the other hand, using (2.2),

\[
 \begin{aligned}
 P_dP
 &=\bigl(\phi_d+\phi\langle\psi_d,\phi\rangle\bigr)
     \otimes\psi\\
 &=\bigl(\phi_d-\phi\langle\psi,\phi_d\rangle\bigr)
     \otimes\psi\\
 &=(Q\phi_d)\otimes\psi.
 \end{aligned}
 \tag{2.5}
\]

Hence the central cancellation is exact:

\[
 \boxed{Q\mathscr AP=P_dP.}
 \tag{2.6}
\]

Let \(q_d=\mathscr Aq\), and put

\[
 \alpha=\langle\psi,q\rangle,
 \qquad z=Qq,
 \qquad q=\alpha\phi+z.
 \tag{2.7}
\]

With

\[
 h_\psi=\psi_d+\mathscr A^*\psi,
 \tag{2.8}
\]

the tangent equation and differentiated normalization give

\[
 \langle h_\psi,\phi\rangle=0.
 \tag{2.9}
\]

Consequently,

\[
 \boxed{\alpha_d=\langle h_\psi,z\rangle,}
 \tag{2.10}
\]

and

\[
 \boxed{
 z_d=\mathscr Az-\phi\langle h_\psi,z\rangle
 =(Q\mathscr AQ-P_dQ)z.}
 \tag{2.11}
\]

Thus the tangent amplitude never forces the complement. The converse
coupling generally remains. The constraint is propagated because a
solution of (2.11) satisfies

\[
 \frac d{dd}\langle\psi,z\rangle
 =\langle h_\psi,z\rangle
 -\langle\psi,\phi\rangle\langle h_\psi,z\rangle=0.
 \tag{2.12}
\]

No orthogonality or spectral gap is used in these identities.

---

## 3. Necessary and sufficient condition for two-sided invariance

**Decision: PASS, subject to strong/domain-compatible regularity.**

The moving complement is invariant precisely when

\[
 \langle h_\psi,z\rangle=0
 \quad\hbox{for every }z\in\ker\psi.
 \tag{3.1}
\]

The orthogonal complement of \(\ker\psi\) is
\(\operatorname{span}\{\psi\}\), so (3.1) implies
\(h_\psi=\lambda\psi\). Because the pairing is conjugate-linear in its
first argument, (2.9) gives

\[
 0=\langle\lambda\psi,\phi\rangle
 =\overline\lambda\langle\psi,\phi\rangle
 =\overline\lambda.
 \tag{3.2}
\]

Thus \(\lambda=0\). Conversely, \(h_\psi=0\) plainly makes both equations
decouple. The exact necessary-and-sufficient condition is therefore

\[
 \boxed{\psi_d=-\mathscr A^*\psi.}
 \tag{3.3}
\]

Equivalently,

\[
 \boxed{P_d=\mathscr AP-P\mathscr A=[\mathscr A,P].}
 \tag{3.4}
\]

For the gapless OS generator this becomes

\[
 \psi_d=\mathcal L_0\psi-ic\mathscr B_0^*\psi.
 \tag{3.5}
\]

The leading term is forward anti-heat. Generic \(L^2\) initial data do not
produce a forward \(L^2\) solution. When \(c\ne0\), the pressure adjoint also
creates additional Fourier modes, so a transported dual is not supplied by
the displayed two-mode tangent carrier. At \(c=0\), finite Fourier data do
remain finite Fourier data even though the forward anti-heat problem is
still ill-posed for generic \(L^2\) data. This distinction must be kept in
the public wording.

---

## 4. Orthogonal projection and the sharp speed

**Decision: PASS.**

Write \(A_1=a/2\) and set

\[
 N=\|\phi\|_2^2=\frac{A_1^2+b^2}{2}
 =\frac{a^2}{8}+\frac{b^2}{2},
 \tag{4.1}
\]

\[
 \theta=b\sin x+A_1\sin2x.
 \tag{4.2}
\]

The normalized sine basis gives

\[
 \langle\theta,\phi\rangle=0,
 \qquad
 \|\theta\|_2^2=N.
 \tag{4.3}
\]

The two coefficients in
\(\phi_d=\kappa\phi+\omega\theta\) are

\[
 \kappa=-\frac{A_1^2+4b^2}{A_1^2+b^2},
 \qquad
 \omega=\frac{3A_1b}{A_1^2+b^2}.
 \tag{4.4}
\]

Thus \(\zeta:=Q_\perp\phi_d=\omega\theta\). Since
\(N_d=2\kappa N\), differentiating
\(P_\perp=\phi\otimes\phi/N\) gives

\[
 (P_\perp)_d
 =\frac{\zeta\otimes\phi+\phi\otimes\zeta}{N}.
 \tag{4.5}
\]

In the orthonormal basis
\(e=\phi/\sqrt N\), \(f=\theta/\sqrt N\), its only nonzero block is

\[
 \begin{pmatrix}0&\omega\\ \omega&0\end{pmatrix}.
 \tag{4.6}
\]

Therefore

\[
 \|(P_\perp)_d\|=|\omega|.
 \tag{4.7}
\]

With \(r=b/A_1=2e^{-3d}>0\),

\[
 \omega=\frac{3r}{1+r^2}
 \le\frac32,
 \tag{4.8}
\]

and equality holds at \(r=1\), namely
\(d=(\log2)/3\). The constant \(3/2\) is sharp on the physical time
interval \(d\ge0\).

---

## 5. Independent Fourier calculation of \(G\)

**Decision: PASS.**

The two pieces of

\[
 G=\mathscr B_0^*\phi
 =\Pi_0(W\phi)+\mathcal L_0^{-1}\Pi_0(\phi^2)
 \tag{5.1}
\]

are obtained from
\(\sin m x\sin n x=[\cos(m-n)x-\cos(m+n)x]/2\). Their nonconstant
coefficients are

| term | \(\cos x\) | \(\cos2x\) | \(\cos3x\) | \(\cos4x\) |
|---|---:|---:|---:|---:|
| \(\Pi_0(W\phi)\) | \(5ab/16\) | \(a^2/8\) | \(-5ab/16\) | \(b^2/8\) |
| \(\mathcal L_0^{-1}\Pi_0(\phi^2)\) | \(-ab/2\) | \(-a^2/32\) | \(ab/18\) | \(-b^2/32\) |

Adding the rows gives

\[
 \boxed{
 G=-\frac{3ab}{16}\cos x
 +\frac{3a^2}{32}\cos2x
 -\frac{37ab}{144}\cos3x
 +\frac{3b^2}{32}\cos4x.}
 \tag{5.2}
\]

The sine/cosine parity immediately gives
\(\langle G,\phi\rangle=\langle G,\theta\rangle=0\), and \(G\ne0\) at
every finite \(d\). Since

\[
 \mathscr A_0^*\phi=\phi_d+icG
 =\kappa\phi+\zeta+icG,
 \tag{5.3}
\]

one obtains

\[
 \boxed{
 (\psi_\perp)_d+\mathscr A_0^*\psi_\perp
 =\frac{2\zeta+icG}{N}.}
 \tag{5.4}
\]

The factor \(2\) is correct: one copy of \(\zeta\) comes from differentiating
\(\phi/N\), and one comes from \(\mathscr A_0^*\phi/N\). Consequently the
orthogonal moving quotient is exact, but bounded \(P_d\) does not eliminate
the pressure coupling. The \(G\)-piece is present only when \(c\ne0\).

---

## 6. Fixed two-mode carrier

**Decision: Fourier identities PASS; OS noninvariance requires \(c\ne0\).**

Let

\[
 \mathcal S=\operatorname{span}\{\sin x,\sin2x\},
 \qquad
 q=x_1\sin x+x_2\sin2x.
 \tag{6.1}
\]

Since

\[
 \mathcal L_0^{-1}q=x_1\sin x+\frac{x_2}{4}\sin2x,
 \tag{6.2}
\]

the square terms in
\(Wq+\phi\mathcal L_0^{-1}q\) cancel, while the cross term is

\[
 -\frac38(a x_2+2b x_1)\sin x\sin2x.
 \tag{6.3}
\]

Therefore

\[
 \boxed{
 \mathscr B_0q
 =-\frac3{16}(a x_2+2b x_1)(\cos x-\cos3x).}
 \tag{6.4}
\]

At finite \(d\), the kernel of
\(\mathscr B_0|_{\mathcal S}\) is exactly

\[
 a x_2+2b x_1=0,
 \tag{6.5}
\]

which is the tangent line generated by
\((x_1,x_2)=(a/2,-b)\). The full generator has leakage

\[
 (I-\Pi_{\mathcal S})\mathscr A_0q
 =\frac{3ic}{16}(a x_2+2b x_1)
 (\cos x-\cos3x).
 \tag{6.6}
\]

It follows that \(\mathcal S\) is not invariant under \(\mathscr A_0\) when
\(c\ne0\). If \(c=0\), however,
\(\mathscr A_0=-\mathcal L_0\) and \(\mathcal S\) is invariant. Thus an
unqualified `fixedTwoHarmonicOSInvariance = FALSE` is too broad.

The independently recomputed return formulas are

\[
 \mathscr B_0\cos x
 =-\frac{3b}{8}(\sin x+\sin3x),
 \tag{6.7}
\]

\[
 \mathscr B_0\cos3x
 =-\frac{2a}{9}\sin4x+\frac{2a}{9}\sin2x
 +\frac{5b}{72}\sin5x-\frac{5b}{72}\sin x.
 \tag{6.8}
\]

There is an actual infinite Fourier cascade, not only one failed
four-mode truncation. For \(n\ge3\), the coefficient of
\(\sin(n+2)x\) in \(\mathscr B_0\cos nx\) is

\[
 \frac b2\left(\frac14-\frac1{n^2}\right)
 =\frac{b(n^2-4)}{8n^2}\ne0.
 \tag{6.9}
\]

Starting from the leaked \(\cos3x\) component therefore reaches
\(\sin5x,\cos7x,\ldots\). In the OS evolution this cascade is active when
\(c\ne0\).

---

## 7. Positive-gap normalized-dual obstruction

**Decision: PASS with the precise pressure-block and compact-\(d\) scope.**

For real \(\beta\), \(|\beta|\le1/2\), and

\[
 \mathcal L_{\beta,\mu}
 =(-i\partial_x+\beta)^2+\mu,
 \qquad
 g=\beta^2+\mu>0,
 \tag{7.1}
\]

the constant Fourier eigenvalue is \(g\). On full periodic \(L^2\),

\[
 \mathscr B_{\beta,\mu}^*
 =M_W+\mathcal L_{\beta,\mu}^{-1}M_\phi.
 \tag{7.2}
\]

Let \(\langle\psi_{\beta,\mu},\phi\rangle=1\). Since \(\phi\) is real and
the normalization is the real number \(1\),

\[
 \widehat{\phi\psi_{\beta,\mu}}(0)
 =\langle\phi,\psi_{\beta,\mu}\rangle
 =\overline{\langle\psi_{\beta,\mu},\phi\rangle}=1.
 \tag{7.3}
\]

It follows exactly that

\[
 \boxed{
 \widehat{\mathcal L_{\beta,\mu}^{-1}
 (\phi\psi_{\beta,\mu})}(0)=\frac1g.}
 \tag{7.4}
\]

Taking the constant coefficient in (7.2), followed by Cauchy--Schwarz,
gives

\[
 \boxed{
 \frac1g
 \le\|\mathscr B_{\beta,\mu}^*\psi_{\beta,\mu}\|_2
 +\|W\|_\infty\|\psi_{\beta,\mu}\|_2.}
 \tag{7.5}
\]

For \(P=\phi\otimes\psi\),

\[
 \|P\|=\|\phi\|_2\|\psi\|_2.
 \tag{7.6}
\]

At a fixed finite \(d\), or uniformly on a compact \(d\)-interval on which
\(\|\phi(d)\|_2\ge m>0\), (7.5) proves the dichotomy: the unweighted
projection norm or the raw adjoint pressure vector has at least
\(g^{-1}\)-scale growth.

The lower bound survives the complementary projection when \(P\) is
uniformly bounded. First,

\[
 Q^*\mathscr B^*\psi
 =\mathscr B^*\psi
 -\psi\langle\phi,\mathscr B^*\psi\rangle,
 \tag{7.7}
\]

and

\[
 \langle\phi,\mathscr B^*\psi\rangle
 =\langle\mathscr B\phi,\psi\rangle.
 \tag{7.8}
\]

Moreover,

\[
 \mathcal L_{\beta,\mu}^{-1}\phi
 =-W-2i\beta\mathcal L_{\beta,\mu}^{-1}W_x
 +g\mathcal L_{\beta,\mu}^{-1}W,
 \tag{7.9}
\]

so

\[
 \mathscr B_{\beta,\mu}\phi
 =\phi\left(
 -2i\beta\mathcal L_{\beta,\mu}^{-1}W_x
 +g\mathcal L_{\beta,\mu}^{-1}W\right).
 \tag{7.10}
\]

The inverse in (7.10) only sees modes \(\pm1,\pm2\). For
\(|\beta|\le1/2\) their eigenvalues are at least \(1/4\), hence, on a
fixed compact \(d\)-interval,

\[
 \|\mathscr B_{\beta,\mu}\phi\|_2
 \le C_d(|\beta|+g).
 \tag{7.11}
\]

If \(\|\psi\|_2\le M\), (7.5) and the reverse triangle inequality yield

\[
 \boxed{
 \|Q^*\mathscr B_{\beta,\mu}^*\psi\|_2
 \ge\frac1g-\|W\|_\infty M
 -C_d(|\beta|+g)M^2.}
 \tag{7.12}
\]

This is a genuine \(g^{-1}\) lower bound for the **adjoint pressure
component**. The corresponding rank-one pressure block is

\[
 P\mathscr BQ=\phi\otimes(Q^*\mathscr B^*\psi),
 \tag{7.13}
\]

and has the same scale when \(\|\phi\|\) is bounded below. In the full OS
generator it is multiplied by \(|c|\). Therefore the OS pressure block has
scale \(|c|/g\); the displayed bound forces divergence only along paths for
which \(|c|/g\to\infty\). The derivation does not prove an unconditional
lower bound for the complete \(Q^*\mathscr A^*\psi\), because a diffusive
term is also present.

At \(g=0\), the audited gapless operator acts instead on \(H_0\), and the
projection in (1.8) removes the constant before applying
\(\mathcal L_0^{-1}\). This explains the difference between the finite
vector \(G\) and (7.4). Because the endpoint and positive-gap operators are
stated on different spaces, operator-norm continuity is not a defined
question until a common-space identification is chosen. A safe theorem is
the lower bound (7.12). If one identifies \(H_0\) with the mean-zero
subspace of full \(L^2\) and extends the gapless inverse by zero on constants,
then (7.4) proves failure of bounded operator-norm convergence for that
specific extension.

---

## 8. Required publication edits and applied-state check

The algebraic gate passes only with all of the following scope conditions
preserved in the canonical report and public note.

1. **Operator domains.** In the abstract proposition, require
   \(\phi(d)\in D(\mathscr A(d))\),
   \(\psi(d)\in D(\mathscr A(d)^*)\), strong \(C^1\) regularity, and strong
   solutions on which the displayed pairings and commutator are defined.
   The identities are then pointwise identities on the common domain; they
   do not by themselves assert well-posedness of the standalone quotient.
2. **Nonzero coupling.** State
   `fixedTwoHarmonicOSInvariance = FALSE for c != 0`. The unconditional
   statement is instead that \(\mathscr B_0|_{\mathcal S}\) has the leakage
   (6.4). At \(c=0\), \(\mathcal S\) is invariant under the heat generator.
   Any claim that pressure transport prevents a finite Fourier dual also
   needs \(c\ne0\); at \(c=0\), finite Fourier anti-heat data remain finite
   Fourier data.
3. **Pressure component.** Describe (7.12) as an adjoint-pressure off-block
   lower bound. The OS pressure contribution carries an additional
   \(|c|\), and the audit does not rule out cancellation inside the complete
   diffusive-plus-pressure block without further graph-norm control.
4. **Time scope.** State the dual/projection dichotomy at fixed finite \(d\)
   or on a compact \(d\)-interval where \(\|\phi(d)\|_2\) has a positive
   lower bound. Do not make it uniform as \(d\to\infty\).
5. **Common space.** Do not say that operators acting on different Hilbert
   spaces are “not norm-continuous” without declaring the embedding or
   extension. The coordinate-free published conclusion should be (7.5) and
   (7.12); any norm-continuity corollary must name its common-space model.

All five items have been applied and rechecked:

- the report and internal proposition now use a common dense domain \(D\),
  \(\phi\in C^1(I;H)\cap C(I;D)\),
  \(\psi(d)\in D(\mathscr A(d)^*)\), continuity of
  \(d\mapsto\mathscr A(d)^*\psi(d)\), and strong solutions
  \(q\in C^1(I;H)\cap C(I;D)\);
- the internal equation-(4.4) kernel statement is explicitly restricted to
  \(c\ne0\), while the report states the unconditional kernel for
  \(\mathscr B_0|_{\mathcal S}\);
- the transported-dual finite-Fourier obstruction is restricted to
  \(c\ne0\), and both sources state that finite Fourier support is preserved
  at \(c=0\) although generic \(L^2\) forward anti-heat evolution still
  fails;
- the \(g^{-1}\) claim is explicitly the unscaled pressure off-block at fixed
  or compact \(d\), and the OS contribution retains the \(|c|\) factor;
- the cross-space operator-norm continuity assertion has been removed unless
  a common-space identification is first specified.

These were theorem-scope edits, not repairs to the computed constants.

---

## 9. Independent exact-arithmetic cross-check

The Fourier coefficients in Secs. 5--6 were also recomputed by a
dependency-free Python script using rational polynomial coefficients and
only the identities

\[
 \sin m\sin n=\frac12[\cos(m-n)-\cos(m+n)],
 \qquad
 \sin m\cos n=\frac12[\sin(m+n)+\sin(m-n)].
 \tag{9.1}
\]

The exact nonzero output was

```text
G:
  cos(1):  -3/16 a b
  cos(2):   3/32 a^2
  cos(3): -37/144 a b
  cos(4):   3/32 b^2
B(sin x):
  cos(1): -3/8 b;  cos(3): 3/8 b
B(sin 2x):
  cos(1): -3/16 a; cos(3): 3/16 a
B(cos x):
  sin(1): -3/8 b;  sin(3): -3/8 b
B(cos 3x):
  sin(1): -5/72 b; sin(2): 2/9 a;
  sin(4): -2/9 a; sin(5): 5/72 b
```

This cross-check is independent of the matrix/certificate generators. It
uses exact fractions, not floating-point quadrature.

---

## 10. Release-gate conclusion

The following mathematical claims are independently confirmed:

\[
\begin{array}{ll}
\text{exact moving-tangent quotient algebra}
 & \texttt{PASS},\\
\text{transported-dual iff condition}
 & \texttt{PASS WITH DOMAIN HYPOTHESES},\\
\text{orthogonal projection speed and explicit }G
 & \texttt{PASS},\\
\text{fixed two-mode OS invariance for }c\ne0
 & \texttt{FALSE},\\
\text{uniform unweighted positive-gap pressure dual/block}
 & \texttt{FALSE AT FIXED/COMPACT }d,\\
\text{bounded transported dual and weighted modulation theorem}
 & \texttt{OPEN}.
\end{array}
\tag{10.1}
\]

Accordingly, the projection lane has final analytic-gate status
**PASS WITH SCOPE EDITS APPLIED**. This audit does not promote any result
to a physical \(\mu=0\) velocity theorem, a Bloch-uniform propagator, the
Squire system, a nonlinear Navier--Stokes estimate, or the Clay problem.
