# R0.73L independent analytic audit

**Status:** PASS after two explicit repairs

**Scope:** `r073l_problem_freeze.md` and
`r073l_adiabatic_tracking_proof.md`

## 1. Direct verdict

The fixed-fast-time block mechanism is sufficient to prove an
\(\varepsilon\)-uniform bounded-prefactor theorem for the forward orbit that
starts on the selected rank-one spectral line.  The proof does not need a
uniform \(P_\varepsilon''\), a uniform \(H^2\) graph norm, or a backward
parabolic evolution.

The audit found two bookkeeping defects in the first coordinating draft:

1. the one-block Duhamel error was written for an input already in
   \(Q(s)H\), but the displayed full-space operator norm omitted
   \(\|Q(s)\|\); the proof now records
   \(Q_K\le1+P_K\) and includes it in the block threshold;
2. the first lower-bound absorption condition did not contain enough powers
   of the Kato-transport constant \(M_W\); it is replaced by
   \(4M_W^3P_K\kappa_KD_*C_Q\varepsilon_L\le1\).

Both repairs only shrink the existential \(\varepsilon_L\); neither changes
the theorem.

## 2. Scaling and inherited input audit

The conversion is

\[
 \partial_\theta u=B_\varepsilon(\varepsilon\theta)u,
 \qquad \varepsilon\partial_du=B_\varepsilon(d)u,
 \qquad \theta=d/\varepsilon.
\]

Thus the fixed slow interval \([0,D_*]\) is the full fast interval
\([0,D_*/\varepsilon]\).  The viscosity coefficient and the inverse slow
time are the same parameter.  This equality is essential when transferring
the \(O(\varepsilon)\) eigenvalue shift into only an \(e^{O(1)}\)
multiplicative action error.

The proof uses only inputs already sealed in R0.73K:

- the real algebraically simple branch and rank-one Riesz projection;
- uniform \(P\), \(P'\), full-semigroup, and frozen-complement bounds;
- the common \(H^2\) domain and Riesz invariance;
- the \(O(\varepsilon)\) eigenvalue shift;
- bounded Lipschitz profile drift on \(H\).

No unsealed graph-norm estimate is present.

## 3. Kato sign and domain audit

With \(\mathcal K=[P',P]\),

\[
 [P,\mathcal K]=-P',
\]

so the positive correction in

\[
 \varepsilon(U^{\rm a})'=(B+\varepsilon\mathcal K)U^{\rm a}
\]

is correct.  The exact evolution relative to \(U^{\rm a}\) has the negative
Duhamel term.  The proof states both signs correctly.

The common-domain step is legitimate because the unbounded part
\(-\varepsilon L\) is independent of \(d\), whereas every profile difference
is bounded on \(H\).  The proof never forms a global conjugate
\(W^{-1}BW\), so it does not require the bounded Kato transport to preserve
\(H^2\).

## 4. Fixed-block and iteration audit

On a fast block \(d=s+\varepsilon\tau\), the perturbation of the frozen
generator is

\[
 B(s+\varepsilon\tau)-B(s)+\varepsilon\mathcal K(s+\varepsilon\tau),
\]

whose norm is \(O(\varepsilon)\) for fixed block length.  Duhamel's formula
therefore gives an \(O(\varepsilon)\) block error with a constant independent
of the block start.  Choosing \(T\) first so that
\(C_Ke^{-(0.16-0.12)T}\le1/4\), and then choosing
\(\varepsilon_L\) so the corrected Duhamel term is at most \(1/4\), gives a
relative contraction factor \(1/2\).

Exact intertwining maps the endpoint into the next \(Q\) fiber.  Hence the
blocks multiply without an uncontrolled factor \(C_K^{D_*/(\varepsilon T)}\).
The final short block is absorbed in one fixed constant.  This proves the
moving-complement relative kernel using forward evolution only.

## 5. Volterra and lower-bound audit

The off-diagonal identities

\[
 P\mathcal KP=0,
 \qquad Q\mathcal KQ=0
\]

give exact coupled Volterra equations.  Integrating the relative-decay kernel
produces the factor \(\varepsilon/\gamma_Q\), so
\(q=O(\varepsilon)p\).  The selected feedback is then also
\(O(\varepsilon)\) on the fixed slow window.

No orthogonality of \(P\) and \(Q\) is assumed.  The lower bound uses only

\[
 \|P(d)u(d)\|\le\|P(d)\|\,\|u(d)\|,
\]

which is valid for a nonorthogonal Riesz projection.

## 6. Claim boundary

The proof closes:

```text
movingComplementRelativeStability=PASS
relativeSelectedErrorOepsilon=PASS
boundedPrefactorAdiabaticTracking=PASS
inviscidActionUpToBoundedPrefactor=PASS
forwardSelectedBackwardLocalization=PASS
```

It does not prove that the exact orbit remains exactly in \(P(d)H\), that an
arbitrary terminal eigenvector can be evolved backward, or that a limiting
prefactor exists.

