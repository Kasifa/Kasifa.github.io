# Independent primary audit of R0.75H

## 0. Frozen object and verdict

Audited file: `research/r075h_single_pass_transport_flux_closure.md`.

Frozen SHA-256:
`849379bea9cf22e0d892ac11ac05bb3b3bc2967a1735753dbc4a6ffc7bb7d7b9`.

**Verdict: PASS. Mathematical blocker count: 0. Release blocker count: 0.**

The note proves a terminal-tube cubic payment theorem for a pure transport
benchmark. It does not assert that the benchmark pair solves
Navier--Stokes, does not transfer the characteristic argument through
diffusion, and does not claim E.24.

The four frozen inputs recompute as

| input | SHA-256 |
|---|---|
| `research/r075b_bulk_clock_outer_padding_gate.md` | `430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a` |
| `research/r075e_horizontal_cross_mode_flux_reduction.md` | `99529b8934412775e19a1b70784cddf3e62190b50c42669ccd34135a134c5049` |
| `research/r075f_modal_phase_integration_identity.md` | `f7a72ebfe0471e18c0d5d44bd3123491d7cd47a79293d1860c5d023c13acf440` |
| `research/r075g_signed_flux_gain_threshold.md` | `f2b3424dddb7eee5938200c3433cd012a1820564e43ad446e0c88d8dfa39ff41` |

## 1. Time-cutoff transport identity, H.10--H.14

From `H_t=-q'(t) partial_2 H`, periodic integration by parts gives

\[
 \frac12E_\xi'(t)
 =-\int\xi q'H\partial_2H
 =\frac12\int q'\partial_2\xi|H|^2.
\]

Multiplication by the nondecreasing time cutoff and integration in time
gives

\[
 \mathcal T_{\xi,\eta}^{\rm tr}
 =\frac12\eta_R(t_2)E_\xi(t_2)
 -\frac12\eta_R(s)E_\xi(s)
 -\frac12\int_s^{t_2}\eta_R'E_\xi.
\]

The frozen endpoint values reduce this to H.13. Since `eta_R' >= 0` and
`E_xi >= 0`, the positive part is at most `E_xi(t_2)/2`. The sign is
positive on the right of H.11 and no absolute-flux estimate is inserted.

## 2. Characteristic direction and tube inclusion, H.15--H.17

The exact solution formula is

\[
 H(t,x)=H(t_2,x+(q(t_2)-q(t))e_2).
\]

If `y` is a terminal point in `Omega_0`, its earlier preimage is

\[
 x=y-(q(t_2)-q(t))e_2.
\]

This is precisely the translated set contained in `Omega_+` by H.7.
A measure-preserving translation therefore yields

\[
 \int_{\Omega_+}|H(t)|^2
 \ge\int_{\Omega_0}|H(t_2)|^2
 \ge E_\xi(t_2),
\]

where the final inequality uses `0 <= xi <= 1` and
`supp xi = Omega_0`. Integration over the terminal interval gives H.17.
The fixed-lift/no-seam condition is explicitly retained.

## 3. Hölder and scale audit, H.18--H.25

Spacetime Hölder on a cylinder of measure
`delta_R |Omega_+|` gives

\[
 \delta_R E_\xi(t_2)
 \le(\delta_R|\Omega_+|)^{1/3}
 \left(\int_J\!\int_{\Omega_+}|H|^3\right)^{2/3}.
\]

Division by `delta_R` confirms the factor
`delta_R^(-2/3)|Omega_+|^(1/3)` in H.19. Substituting

\[
 \delta_R\asymp R^3,\qquad
 |\Omega_+|\lesssim L^2R^3,\qquad
 \int_J\!\int_{\Omega_+}|H|^3
 =R^2\omega^{-1}p_{F,J}^{\rm tr}
\]

into `(omega/R) E_xi(t_2)` gives

\[
 \frac\omega R
 R^{-2}(L^2R^3)^{1/3}
 (R^2\omega^{-1}p)^{2/3}
 =L^{2/3}\omega^{1/3}R^{-2/3}p^{2/3}.
\]

The exponential rate is

\[
 \frac\rho6-\frac{c_\gamma}{12}
 =-\frac{4279}{238140000}<0.
\]

The lower exterior weight pays the terminal atom inside the benchmark
measurement \(P_R^{M,{\rm tr}}\). The main note explicitly says this is the same
measurement formula evaluated on the benchmark and does not assert that
the benchmark is an NSE solution.

## 4. Matching-background comparison, H.26

Under the separately stated matching lower bound

\[
 p_b\ge cL^2\omega R^{-3},
\]

taking cube roots and multiplying by `R^(1/3)` gives

\[
 R^{1/3}p_b^{1/3}
 \ge c^{1/3}L^{2/3}\omega^{1/3}R^{-2/3}.
\]

Hence the inequality direction in H.26 is correct. This identifies the
benchmark scale with the R0.75G `alpha=1/3` sufficient form but does not
prove that form for the diffusive frozen family.

## 5. Diffusive identity and circularity, H.27--H.28

The R0.75E local energy identity has the form

\[
 \frac12E(t_2)+D=A+\mathcal T.
\]

Solving for the signed transport term yields

\[
 \mathcal T
 =\frac12E(t_2)+D
 -\frac12\int[\eta_R'\xi+\eta_R\Delta_{23}\xi]|F|^2,
\]

which is exactly H.28. Every sign is correct. The middle positive row is
the unknown outer accumulated dissipation, so bounding the flux through
this equality would reuse the target rather than extend the transport
theorem. The note correctly stops before making that inference.

## 6. Byte, structural, and claim audit

- An initial U+0008 control byte in H.7 was detected and corrected before
  freezing this audit.
- The final H.7 bytes contain
  `\Omega_0-\bigl(q(t_2)-q(t)\bigr)e_2`.
- The final main file contains no disallowed control characters.
- Equation tags H.1--H.29 are unique and consecutive.
- Every internal H-reference resolves to one of those tags.
- All 29 displayed equation environments are paired.
- The terminal tube is local and no all-winding or whole-annulus statement
  is inferred.
- The benchmark payment is not identified with the payment of an exact NSE
  solution.
- The diffusive terminal-tube estimate, E.24, complete clock, fixed
  deletion, suitable-weak transfer, regularity, and singularity remain
  open.
- No simulation, numerical fit, novelty, or priority claim is made.

The frozen R0.75H claims are mathematically consistent and ready for a
finite exact certificate. **NOT CLAY.**
