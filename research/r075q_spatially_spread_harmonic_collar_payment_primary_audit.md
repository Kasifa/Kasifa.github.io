# R0.75Q primary analytic audit

## Audit object

- Main note: `research/r075q_spatially_spread_harmonic_collar_payment.md`
- Audit type: radial geometry, phase-uniform mass, exponent, and claim-boundary audit
- Verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**

The finite certificate will bind the final main-note SHA-256 after an
independent review. This author-side audit does not authorize publication.

## 1. Radial derivative audit

The central-chart support of `xi_(a,R)` is a shell of radius comparable to
`aR` and fixed normalized thickness, hence has volume at most
`C_delta a^2 R^3`. Since `|partial_2 xi|<=C_vartheta R^(-1)`,

\[
 V_{\xi,3}:=\int_{\mathbb T^3}|\partial_2\xi|\,dx
 \le C_\vartheta a^2R^2.
\]

The condition `(a+delta)R<pi/2` keeps the whole calculation in one Euclidean
chart of the torus. The periodic lift therefore creates no boundary term or
overlap ambiguity.

## 2. Signed-flux cancellation audit

For `F_k=A e^(-k^2t)cos(k(x_2-Bt))`, direct differentiation gives

\[
 (\partial_t+B\partial_2-\partial_2^2)F_k=0.
\]

The constant term in
`F_k^2=(A^2e^(-2k^2t)/2)(1+cos(2k(x_2-Bt)))` integrates to zero against
`partial_2 xi`. Taking absolute values after this exact cancellation gives

\[
 |\mathcal T_{k,\eta}^{(3)}|
 \le {A^2|B|V_{\xi,3}\over4}
       \int_0^T e^{-2k^2t}\,dt
 \le {A^2|B|V_{\xi,3}\over8k^2}.
\]

Combining with the derivative row yields Q.14. No enhanced-dissipation
estimate is used.

## 3. Rectangular subcollar audit

On `|x_2|,|x_3|<=aR/4`, the transverse radius is at most
`aR/(2sqrt(2))`. If `a>=4delta_0`, this is at most
`(a-2delta_0)R`. The exact two-sided `x_1` fibre through the plateau shell is

\[
 2R\left[
 \sqrt{(a+\delta_0)^2-q^2}
 -\sqrt{(a-\delta_0)^2-q^2}\right],
 \qquad q={|(x_2,x_3)|\over R}.
\]

The bracket is at least `2delta_0`; hence the fibre length is at least
`4delta_0R`.

The period of `|cos(kx-phi)|^3` is `pi/k`, and its integral over one period
is `4/(3k)`. For an interval of length `ell` with `k ell/pi>=1`, the first
`floor(k ell/pi)` period-length subintervals give

\[
 \int_I|\cos(kx-\phi)|^3\,dx
 \ge {4\over3k}\left\lfloor{k\ell\over\pi}\right\rfloor
 \ge {2\ell\over3\pi}.
\]

Taking `ell=aR/2` gives Q.18. Multiplication by the `x_3` length `aR/2`
and the fibre length `4delta_0R` gives exactly
`2delta_0 a^2R^3/(3pi)`. This bound is uniform in the translated phase.

## 4. Time integral and cubic inversion audit

The condition `k^2T>=1` gives

\[
 \int_0^T e^{-3k^2t}\,dt
 \ge {1-e^{-3}\over3k^2}.
\]

Consequently

\[
 M_{k,\rm col}
 \ge {2(1-e^{-3})\over9\pi}
       \delta_0a^2R^3k^{-2}A^3.
\]

Solving this inequality for `A^2` contributes
`delta_0^(-2/3)a^(-4/3)R^(-2)k^(4/3)M_col^(2/3)`.
Substitution into Q.14 cancels `R^2`, leaves `a^(2/3)`, and changes
`k^(-2)` to `k^(-2/3)`. Thus Q.3--Q.4 have the correct constant powers.

## 5. Frozen exponent audit

Since `M_col=R^2 omega^(-1)p_col`, normalization by `omega/R` changes Q.4
to

\[
 \mathfrak X_{k,\rm col}
 \le C|B|a^{2/3}R^{1/3}\omega^{1/3}k^{-2/3}
 p_{k,\rm col}^{2/3}.
\]

The frozen bounds `|B|<=C_BR^(-2)` and `k>=R^(-3/2)` leave
`C L^(2/3)R^(-2/3)omega^(1/3)`. Its exponential rate is

\[
 {\rho\over6}-{c_\gamma\over12}
 =-{1\over12}\left({8\over3969}-{9\over5000}\right)
 =-{4279\over238140000}<0.
\]

The polynomial factor is therefore harmless for sufficiently large `L`.

## 6. Version-M and low-entrance boundary audit

- Q.26 separately places the whole flux window `[0,T]` in the same frozen
  scale-`2R` exterior measurement interval and the plateau tube in a row of
  weight at least `omega`.
- Q.26 separately assumes that `F_k` is an actual coordinate component of
  the same smooth velocity `v_R` measured by `P_R^M` on that tube.
- Pointwise `|F_k|<=|v_R|` and nonnegativity of the cubic row then give
  `p_col<=C P_R^M`; no such domination is claimed for Fourier or
  Littlewood--Paley projections of a larger component.
- The note does not claim that an arbitrary harmonic realizes the frozen
  inversion-paired zero-trajectory family.
- On the full transverse torus, `E_0=2pi^2A^2`. Any R0.75P entrance cutoff
  has support area at most `pi a^2R^2`, so
  `E_in/E_0<=a^2R^2/(2pi)`.
- For every fixed `0<=sigma<2`, `a^2R^2/R^sigma` tends to zero. Thus this
  subfamily can fall strictly below P's sufficient entrance threshold; Q is
  not a restatement of P.
- Q remains one real harmonic, constant shear, independent of `x_1,x_3`,
  and total-field based. Interference, arbitrary low-concentration packets,
  nonconstant shear, E.24, complete clock, fixed deletion, suitable-weak
  transfer, regularity, and singularity remain open.
- No completeness, novelty, or priority claim is made. **NOT CLAY.**

## Audit conclusion

The derivative row, exact cancellation, fibre geometry, phase-uniform
period count, time integral, cubic powers, frozen exponent, conditional
Version-M inclusion, and low-entrance diagnostic are internally consistent.
The draft is ready for independent mathematical audit and finite-certificate
construction.
