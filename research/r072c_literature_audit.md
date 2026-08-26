# R0.72C bounded literature audit

**Checked:** 2026-08-27
**Questions:** Which primary sources support the Rudin--Shapiro input? Does a
checked enhanced-dissipation theorem uniformly control the changing
many-frequency phase profile or its launch-inclusive root ledger?

## Direct answer

The Rudin--Shapiro recursion, coefficient description, and
\(\sqrt M\)-scale supremum bound are classical and directly reproducible from
the parallelogram identity. Modern primary sources record the same formulas.

No checked enhanced-dissipation source proves the R0.72C statement. The
closest results concern a fixed shear, a slowly varying shear with uniform
critical geometry, scalar modulation of one fixed spatial profile, or a
rigidly translating sine. None estimates a coordinate-zero derivative ledger
accumulated before the decay time, and none supplies constants uniform in the
present heat-decaying \(M\)-frequency phase family.

This is a bounded conclusion about the sources listed below. It is not a
claim that no other relevant paper exists.

## Claim-to-source ledger

| R0.72C claim | Primary source | Exact use | Boundary |
|---|---|---|---|
| Rudin--Shapiro recursion and \(|P_n|^2+|Q_n|^2=2M\) | T. Erdelyi, [*The \(L_q\) norm of the Rudin--Shapiro polynomials on subarcs of the unit circle*](https://arxiv.org/abs/2311.04395), 2023 | Equations (1.1)--(1.3) record the recurrence, \(\pm1\) coefficients, and parallelogram identity | R0.72C reproves the needed sup bound; no deeper distribution theorem is used |
| Binary overlapping-\(11\) coefficient formula and arbitrary-prefix context | P. Balister, [*Bounds on Rudin--Shapiro polynomials of arbitrary degree*](https://arxiv.org/abs/1909.08777), 2019 | Introduction records \(a_n=(-1)^{\sum b_ib_{i+1}}\), the recursion, and \(O(\sqrt n)\) prefix bounds | Only dyadic odd generations are needed for the exact sharpness theorem |
| Time-dependent shear enhanced dissipation | D. Coble and S. He, [*A Note on Enhanced Dissipation and Taylor Dispersion of Time-dependent Shear Flows*](https://arxiv.org/abs/2309.15738), Commun. Math. Sci. 22 (2024) | Provides decay for slowly varying time-dependent shears with fixed finite critical structure and uniform shape hypotheses | Does not give \(M\)-uniform constants for changing heat-weighted phase sums or a root-slope ledger |
| Pathwise fixed-shear decay | V. Gardner, K. L. Liss, and J. C. Mattingly, [*A pathwise approach to the enhanced dissipation of passive scalars advected by shear flows*](https://arxiv.org/abs/2410.05657), 2024 | Treats local streamline geometry and finite/infinite-order critical behavior for fixed profiles | Not a changing-profile or launch-ledger theorem |
| Scalar time modulation | J. Benthaus and C. Nobili, [*Enhanced Dissipation via time-modulated velocity fields*](https://arxiv.org/abs/2501.16905), 2025 | Treats \(v(y,t)=\xi(t)w(y)\) with one fixed spatial shape | Relative Fourier weights in R0.72C change with time |
| Translating shear | J. Benthaus, G. M. Coclite, and C. Nobili, [*Mixing and enhanced dissipation in a time-translating shear flow*](https://arxiv.org/abs/2603.14624), 2026 | Treats the specialized profile \(\sin(y-ct)\) | Does not cover an \(M\)-frequency heat-decaying sum |
| Fixed-field hypoelliptic framework | D. Albritton, R. Beekie, and M. Novack, [*Enhanced dissipation and Hörmander's hypoellipticity*](https://arxiv.org/abs/2105.12308), J. Funct. Anal. 283 (2022) | Gives a fixed-bracket geometric framework | Does not track changing critical geometry or exact coordinate roots |
| Stationary quantitative shear rates | J. Bedrossian and M. Coti Zelati, [*Enhanced dissipation, hypoellipticity, and anomalous small noise inviscid limits in shear flows*](https://doi.org/10.1007/s00205-017-1099-y), Arch. Ration. Mech. Anal. 224 (2017) | Supplies the standard critical-degeneracy dependence for stationary shears | Used only as an adjacent frozen comparison |
| Higher-dimensional stationary parallel shears | M. Coti Zelati and T. Gallay, [*Enhanced dissipation and Taylor dispersion in higher-dimensional parallel shear flows*](https://doi.org/10.1112/jlms.12782), J. Lond. Math. Soc. 108 (2023) | Sharp stationary semigroup estimates | No changing phase family or accumulated root ledger |
| Uniform-in-diffusivity fixed-profile mixing | D. Albritton and R. Beekie, [*Sharp uniform-in-diffusivity mixing rates for passive scalars in parallel shear flows*](https://arxiv.org/abs/2511.18536), 2025 preprint | Proves optimal mixing under a fixed \(C^{N+2}\) profile bound and fixed critical-point separation | The constants and diffusivity threshold depend on \(b\); uniform-in-diffusivity does not mean uniform in an \(M\)-dependent profile family |
| Stochastic representation for fixed shears | K. L. Liss and K. Luan, [*Uniform-in-Diffusivity Mixing by Shear Flows: Stochastic and Dynamical Perspectives*](https://arxiv.org/abs/2603.09238), 2026 | Gives fixed-profile mixing via Brownian trajectory phases | Its random phase is a path integral of one fixed \(b\), not random Fourier carrier coefficients |
| Random alternating-phase exponential mixing | A. Blumenthal, M. Coti Zelati, and R. S. Gvalani, [*Exponential mixing for random dynamical systems and an example of Pierrehumbert*](https://arxiv.org/abs/2204.13651), Ann. Probab. (2023) | Treats fresh independent phases in alternating horizontal and vertical sine shears | Not a deterministic phase-uniform theorem and not a growing one-direction carrier family |
| Harris enhanced dissipation for random flows | W. Cooperman, G. Iyer, and S. Son, [*A Harris Theorem for Enhanced Dissipation, and an Example of Pierrehumbert*](https://arxiv.org/abs/2403.19858), Nonlinearity 38 (2025) | Gives diffusivity-independent long-time rates for a fixed random dynamical system satisfying Harris conditions | An \(M\)-uniform application would require uniform drift, minorization, submersion, and regularity estimates not supplied there |

## Exact literature boundary

For a candidate profile at time \(A\), terminal semigroup decay and
launch-inclusive root accumulation are different quantities. The latter
splits additively:

\[
G_{\rm all}^{\rm ex}([0,A+L])
=G_{\rm pre}^{\rm ex}([0,A])
+G_{\rm tail}^{\rm ex}((A,A+L]).
\]

Even a valid terminal decay estimate can only improve the tail through the
remaining energy. It cannot cancel the first nonnegative term.

The changing profile must also be compared with a frozen one using the
coupling-weighted error

\[
\Xi_A=|\delta|\int_A^{A+L}
\|b(x)-b(A)\|_\infty\,dx,
\]

not only \(L\kappa r_{\max}^2\). A small unweighted profile change can be
amplified by large coupling.

## Rudin--Shapiro use in R0.72C

R0.72C needs only the elementary recursion

\[
P_{n+1}=P_n+z^{2^n}Q_n,\qquad
Q_{n+1}=P_n-z^{2^n}Q_n
\]

and its direct consequence

\[
|P_n(z)|^2+|Q_n(z)|^2=2^{n+1}\qquad(|z|=1).
\]

For odd \(n\), evaluation at \(z=1\) attains the upper bound. This gives an
exact multiplier norm, \(\chi_0=1/4\), and the sharp algebraic
\(M^{-8/3}\) prefactor. No probabilistic flatness assertion, random-phase
theorem, or unproved genericity statement enters the result.

## Search scope

The bounded audit checked the primary sources above and targeted searches for:

- time-dependent shear enhanced dissipation;
- moving critical points and changing spatial profiles;
- scalar time modulation and intermittent shear;
- translating shear profiles;
- heat-evolving or heat-decaying Fourier sums;
- many-frequency uniform constants;
- Rudin--Shapiro recurrence, supremum bounds, and arbitrary prefixes.

Secondary summaries were not used to support theorem statements.

The words *uniform-in-diffusivity*, *pathwise*, and *random phase* require
care here. In the checked sources they refer respectively to constants uniform
in the molecular diffusivity for one fixed profile, a stochastic
representation of trajectories, or fresh independent shifts in a fixed
low-dimensional alternating-shear model. None of these meanings supplies
uniformity in the number \(M\) of Fourier carriers.

## Consequence

The R0.72C phase theorem is independent of an enhanced-dissipation theorem.
Its new input is algebraic: conjugate pairing, target-row Parseval, the joint
phase inequality, and heat participation. Enhanced dissipation remains a
separate possible tail improvement. The unresolved step is dynamical
sharpness of the actual normalized root ledger.
