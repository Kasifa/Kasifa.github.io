# R0.73M independent analytic audit

**Audit date:** 2026-08-31

**Files audited:** `r073m_problem_freeze.md` and
`r073m_prescribed_action_departure_proof.md`

**Method:** a second derivation of the physical normalization, action
recoding, harmonic energy rates, remainder, quantifier order, and endpoint
time; the proof candidate was not treated as an authority

**Verdict:** **MATHEMATICAL FINAL PASS**

Publication remains conditional on the finite diagnostic, formal figure,
PDF/HTML synchronization, and release transaction.

## 1. Kinetic-to-physical norm

For one kinetic Fourier coefficient \(h_n\), the recovered positive-row
velocity coefficients are

\[
 v_{2,n}={1\over2}{h_n\over\sqrt{n^2+1/4}},
 \qquad
 v_{3,n}=-{n h_n\over\sqrt{n^2+1/4}}
\]

up to the harmless Fourier sign convention.  Their kinetic energy is

\[
 |v_{2,n}|^2+|v_{3,n}|^2
 ={n^2+1/4\over n^2+1/4}|h_n|^2=|h_n|^2.
\]

The change \(x=2y\) preserves the normalized periodic mean, so no Jacobian
constant appears.  The \(K_z=1\) and \(K_z=-1\) rows are orthogonal and
conjugate.  Dividing their real sum by \(\sqrt2\) therefore preserves both
the unit launch norm and the scalar selected gain.  M1 passes exactly, not
only up to norm equivalence.

## 2. Time normalization

The physical background is

\[
 \overline U_\Lambda(t,y)
 =(0,0,2\Lambda W(4t,2y)).
\]

With \(d=4t\), every term in the physical perturbation equation is divided
by four.  Hence

\[
 \mathcal L_\Lambda(d)h
 ={1\over4}\{\Delta h-\mathbb P[overline U_\Lambda(d/4)\cdot\nabla h
 +h\cdot\nabla\overline U_\Lambda(d/4)]\},
\]

\[
 \mathcal B(f,g)=-{1\over4}\mathbb P[(f\cdot\nabla)g].
\]

The profile endpoint \(D_*=1/450\) is exactly the physical endpoint
\(T_*=D_*/4=1/1800\).  The audited statement now distinguishes the two
variables explicitly.

## 3. Selected action and effective amplitude

R0.73L gives, on the same selected orbit,

\[
 c_Le^{\Lambda\mathcal A_*}\le G_\Lambda^*
 \le C_Le^{\Lambda\mathcal A_*},
 \qquad
 \|a_\Lambda(s)\|_2
 \le C_Le^{-\mu_*\Lambda(D_*-s)},
\]

where the strict R0.73J floor permits
\(\mu_*=167/1000\).  For the prescribed seed, the gain-normalized Taylor
amplitude is exactly

\[
 \delta_\Lambda
 =\rho G_\Lambda^*e^{-\Lambda\mathcal A_*}
 \in[c_L\rho,C_L\rho].
\]

Thus \(\rho_0=\delta_0/C_L\) keeps every sufficiently large \(\Lambda\)
inside one common nonlinear radius, while the endpoint lower bound becomes
\(c_L\rho/2\).  Only a bounded two-sided prefactor is used; no prefactor
limit is inferred.

## 4. Harmonic support and mean zero

The exact row-Duhamel identity and addition of \(K_z\) labels give

\[
 a:\pm1,
 \qquad b:0,\pm2,
 \qquad c:\pm1,\pm3.
\]

Consequently \(\Pi_{\pm1}b=0\).  All forcing terms are divergences of
periodic tensors, so total spatial mean zero propagates through the exact
solution, Taylor coefficients, approximation, and error.  The homogeneous
two-dimensional Ladyzhenskaya inequality is applicable.

## 5. Localized energy rates

The selected endpoint-normalized row supplies

\[
 Y_a+M_a=O(e^{-2\mu_*\Lambda(D_*-s)}).
\]

The zero row contracts by heat flow.  The doubled row uses the continuum
bound \(1/3\), and every other nonzero row uses \(1/2\).  Repeating the
Stieltjes estimate independently gives

\[
 Y_b+M_b=O(e^{-4\mu_*\Lambda(D_*-s)}),
 \qquad
 Y_c+M_c=O(e^{-6\mu_*\Lambda(D_*-s)}).
\]

The exact strict margins are

\[
 2\mu_*-{1\over3}={1\over1500},
 \qquad
 3\mu_*-{1\over2}={1\over1000},
 \qquad
 4\mu_*-{1\over2}={21\over125}.
\]

The first two would fail if the auxiliary R0.73L proof constant
\(c_K=0.16\) were substituted for the R0.73J spectral floor.  The audited
proof uses the correct \(0.167\).

## 6. Fourth-order remainder

For
\(u_{\rm app}=\delta a+\delta^2b+\delta^3c\), the residual begins at fourth
order.  The exact transport cancellations leave one coefficient-gradient
term with

\[
 \int_0^{D_*}\|\nabla u_{\rm app}\|_2^2\,ds=O(\delta^2).
\]

The product measures \(N_4,N_5,N_6\) have the respective envelopes
\(8\mu_*\), \(10\mu_*\), and \(12\mu_*\).  The error integrating factor is

\[
 e^{\Lambda(s-t)}e^{C\delta^2}.
\]

Because \(1<8\mu_*\), the leading Stieltjes integral closes uniformly and

\[
 \|e(D_*)\|_2\le C_R\delta^4.
\]

This rederivation uses only the selected \(L^2\) orbit plus cumulative
dissipation; it does not insert a full planar high-Sobolev semigroup bound.

## 7. Smooth launch and global continuation

The R0.73K rank-one vector belongs to the same viscous branch treated in
R0.73G.  Two elliptic lifts give an \(H^4\) cost
\(O(\varepsilon^{-2})\), and the velocity recovery is order zero.  Hence

\[
 \|\phi_\Lambda\|_{H^3}\le C\Lambda^2,
 \qquad
 \rho e^{-\Lambda\mathcal A_*}\|\phi_\Lambda\|_{H^3}\to0.
\]

The real launch and background lie in the invariant planar subspace.  Its
scalar vorticity satisfies the periodic two-dimensional enstrophy identity,
so every selected nonlinear orbit is global and smooth.

## 8. Quantifiers and endpoint

Take \(\Lambda_0\) to be the maximum of all upstream and transfer-lemma
thresholds, then take \(\rho_0=\delta_0/C_L\).  The order is

\[
 \exists\rho_0,c_*,\Lambda_0\quad
 \forall\Lambda\ge\Lambda_0\quad
 \forall\rho\in(0,\rho_0].
\]

All constants are independent of \(\Lambda\) and \(\rho\), and
\(c_*=c_L/2\).  The endpoint lower bound is measured at profile time
\(D_*\), equivalently physical time \(T_*\).

## 9. Exact boundary

The audit passes a prescribed-action, varying-background, planar nonlinear
departure theorem.  It does not pass a prefactor limit, a fixed-background
Lyapunov theorem, a transverse three-dimensional mechanism, a finite-time
singularity, or the Clay conclusion.
