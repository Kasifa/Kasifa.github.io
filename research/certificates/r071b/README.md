# R0.71B exact-certificate bundle

This directory archives the finite exact audits for the R0.71B
common-response packing boundary and positive-output coefficient.

## Decision locked by the bundle

The producer checks ten groups of facts.

First, the exact two-shell family has

\[
 \mathcal U_M
 =\frac{\sqrt2M(M+1)(2M+1)}{(2M^2+2M+1)^{3/2}}
 \longrightarrow1,
 \qquad
 M^2\mathcal C_M\longrightarrow-\frac12.
\]

The same-low fan keeps total common work near \(1/4\) while its shell-work
\(\ell^2\) norm is asymptotic to \(1/(4\sqrt N)\).  The shared-high,
equal-radius fan makes the explicitly polarized common-response operator
ratio grow like \(\sqrt N/4\), while the frame shell supremum and two high
\(L^2\) norms stay fixed.  The latter is a no-go only for that three-field
polarized estimate; it is not a counterexample to established one-field
BMO or Besov continuation theorems.

Second, for

\[
 w_k=2\operatorname{Re}
 \big(\overline{\widehat S(k)}:\widehat Q(k)\big),
 \qquad
 \mathcal T_+^2
 =\sum_k\frac{(w_k^+)^2}
 {4|k|^2|\widehat S(k)|_F^2},
\]

the producer verifies

\[
 (\mathfrak P_Q)_+
 \le \|\nabla\omega\|_2\mathcal T_+
 \le \frac\nu4\|\nabla\omega\|_2^2
 +\nu^{-1}a_+\|\omega\|_2^2,
 \qquad
 a_+=\frac{\mathcal T_+^2}{\|\omega\|_2^2}.
\]

On the R0.71A same-covariance sign pair, the positive field gives
\(\mathcal T_+^2=9/800\) and \(a_+=3/39940400\), while the negative field
gives zero.  A single divergence-free plane wave also gives \(a_+=0\), so
this coefficient is not a BMO-equivalent norm.

## Files

- `result.json` — canonical sorted JSON emitted by the producer;
- `independent-result.json` — separate Fourier reconstruction;
- `command.txt` — exact reproduction commands;
- `environment.txt` — pinned runtime and dependency record;
- `SHA256SUMS` — hashes for every archived payload and producer dependency;
- `../../r071b_exact_audit.py` — R0.71B producer;
- `../../r071b_independent_audit.py` — independent checker;
- `../../r071b_report-source.md` — analytic source;
- `../../r071b_literature_audit.md` — primary-source boundary;
- `../../r071b_independent_audit.md` — manual audit;
- `../../r071a_exact_audit.py` — imported sign-pair dependency;
- `../../r070z_exact_audit.py` — imported frame/Fourier dependency; and
- `../../r070x_exact_audit.py` — transitive triad dependency.

## Analytic boundary

The finite programs exhaust the displayed \(N=8\) supports and the exact
R0.71A samples.  They do not replace the arbitrary-\(N\) lacunary resonance
proofs, standard Littlewood--Paley/BMO theory, or the primary-source
literature audit.

No estimate deriving \(a_+\in L_t^1\) from Leray energy or Navier--Stokes
dynamics is proved.  The bundle proves no new continuation criterion,
singularity, global regularity theorem, or solution of the Millennium
problem.

No DNS, stochastic search, GPU, or DGX resource is used.
