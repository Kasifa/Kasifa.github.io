# Primary mathematical audit of R0.75J

## 0. Frozen object and verdict

Audited file:
`research/r075j_mean_zero_adjoint_flux_obstruction.md`.

Frozen SHA-256:
`960e3cbc18ac8207253a8802da215b3eac07a714ddbcc7209985f27a00c9ff4d`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note proves a sign obstruction for the exact zero-terminal adjoint of
the physical signed collar source, checks the resulting dual identity, and
isolates the different positive-majorant problem that would actually be
needed.  It does not prove the majorant payment, E.24, or a Navier--Stokes
regularity result.

The four frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` |
| `research/r075f_modal_phase_integration_identity.md` | `f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440` |
| `research/r075h_single_pass_transport_flux_closure.md` | `849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9` |
| `research/r075i_diffusion_safe_block_participation.md` | `c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7` |

## 1. Mean-zero and sign-change audit, J.1--J.9

For fixed `(t,x_1)`, the source is

\[
 a=\eta_R b(t,x_3)\partial_2\xi.
\]

Because `b` is independent of `x_2`, Fubini and periodicity give

\[
 \int_{\mathbb T^2_{23}}a
 =\eta_R\int_{\mathbb T_{x_3}}b(t,x_3)
   \left(\int_{\mathbb T_{x_2}}\partial_2\xi\,dx_2\right)dx_3
 =0.
\]

The formal adjoint of
`partial_t+b partial_2-Delta_23` is
`-partial_t-b partial_2-Delta_23`: the drift contributes no divergence
term because `partial_2 b=0`.  Integrating the adjoint equation over the
periodic `(x_2,x_3)` torus therefore leaves only

\[
 -\frac d{dt}\int\psi=0.
\]

The zero terminal datum forces this mean to vanish on every time slice.
A continuous nonnegative function with zero spatial integral is zero, and
then the adjoint equation forces `a=0`.  Hence a nonzero source cannot have
a nonnegative exact adjoint.  More precisely, every nonzero time slice of
`psi` has both positive and negative parts.  This proves the stated
sign-change obstruction without replacing the physical source by `|a|` or
`a_+`.

## 2. Duality and sign audit, J.10--J.13

For a real passive solution, `g=F^2` satisfies

\[
 \mathcal Lg=-2|\nabla_{23}F|^2.
\]

Direct integration by parts in time and on the periodic torus gives

\[
 \int_s^{t_2}\!\int g\mathcal L^*\phi
 =\int\phi(s)g(s)-\int\phi(t_2)g(t_2)
  +\int_s^{t_2}\!\int\phi\mathcal Lg.
\]

The signs of both endpoint terms were recomputed independently.  With
`mathcal L^* psi=a`, `psi(t_2)=0`, and
`2 mathcal T=int g a`, this becomes

\[
 \mathcal T
 =\frac12\int\psi(s)F(s)^2
  -\int_s^{t_2}\!\int\psi|\nabla_{23}F|^2.
\]

Writing `psi=psi_+-psi_-` yields the valid upper bound

\[
 \mathcal T
 \le \frac12\int\psi_+(s)F(s)^2
   +\int_s^{t_2}\!\int\psi_-|\nabla_{23}F|^2.
\]

The last term has the unfavorable positive sign.  No local cubic payment
for it is available in the frozen ledger, so the identity relocates the
H.28 difficulty rather than removing it.

## 3. Constant-shift audit, J.14--J.18

Let `phi=psi+C`, where `C>=||psi_-||_infinity`.  Since constants solve the
homogeneous adjoint equation, the source is unchanged, but the terminal
datum becomes `C`.  The dual formula gives the constant contribution

\[
 \frac C2E(s)-\frac C2E(t_2)-CD.
\]

The passive energy identity

\[
 E(s)-E(t_2)=2D
\]

makes that expression exactly zero.  Thus the shift adds no information
when its endpoint and dissipation rows are both retained.  If positivity
is used to discard the final nonpositive dissipation row, the remaining
extra payment is

\[
 \frac C2(E(s)-E(t_2))=CD.
\]

This is the global energy-drop row, not the desired local Version-M cubic
payment.  The note's broader statement about a homogeneous adjoint
correction is also valid: applying the same dual identity with
`mathcal L^*h=0` shows that its complete boundary-plus-dissipation
contribution is zero before any favorable term is discarded.

## 4. Positive-majorant direction audit, J.19--J.20

Assume pointwise

\[
 a\le\mathcal L^*\Phi,
 \qquad \Phi\ge0,
 \qquad \Phi(t_2)\ge0.
\]

Since `g>=0`, multiplication preserves the first inequality.  Inserting
the dual identity gives

\[
 \begin{aligned}
 \mathcal T
 &\le\frac12\int g\mathcal L^*\Phi\\
 &=\frac12\int\Phi(s)g(s)
   -\frac12\int\Phi(t_2)g(t_2)
   -\int\Phi|\nabla_{23}F|^2\\
 &\le\frac12\int\Phi(s)F(s)^2.
 \end{aligned}
\]

Thus the majorant direction and both favorable signs are correct.  The
zero-terminal adjoint driven by `a_+` is nonnegative by the forward
parabolic maximum principle after reversing time and satisfies
`a<=a_+=mathcal L^*Phi`.  What remains unproved is precisely the estimate
of its initial row by frozen Version-M atoms with a positive `R` gain.

## 5. Source and claim-boundary audit

The source report accurately distinguishes literature context from the
local result:

- Albritton--Dong provide passive advection--diffusion regularity and
  fundamental-solution estimates under their stated drift hypotheses;
- Gardner--Liss--Mattingly use pathwise stochastic methods for passive
  scalars advected by shear;
- Hu--Li develop Davies-type off-diagonal heat-kernel bounds for regular
  Dirichlet forms.

None is claimed to prove the frozen positive-majorant payment, J.20 with a
Version-M right-hand side, or E.24.  The local mean-zero obstruction is not
promoted to a novelty or priority assertion, and it is not a blanket no-go
theorem for all resolvent or Feynman--Kac methods.

## 6. Structural audit and final boundary

- Equation tags J.1--J.20 are unique and consecutive.
- Every internal J-reference resolves.
- All 20 display-math environments are paired.
- The four frozen input hashes match.
- The main note and source report contain no disallowed control bytes.
- The adjoint problem is a standard zero-terminal backward problem, not an
  assumption of backward well-posedness for the passive equation.
- The exact signed-source obstruction and the positive-majorant
  architecture remain distinct.
- The initial occupation payment, transition geometry, periodic
  recrossing, E.24, complete clock, fixed deletion, suitable-weak transfer,
  regularity, and singularity remain open.
- No simulation, numerical fit, priority, or Clay claim is made.

The R0.75J claims are internally consistent and ready for an independent
finite certificate.  **NOT CLAY.**
