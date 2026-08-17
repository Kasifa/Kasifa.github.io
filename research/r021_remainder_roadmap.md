# R0.21 viscous remainder roadmap

## Current mathematical position

R0.20 is a computer-assisted global theorem for one finite fifth-order
coefficient model.  It proves that the selected positive three-parameter
family has two interior stationary points and that the first one is the
unique target-fraction maximum on the compactified parameter closure.  It
does not compare the fifth-order coefficient with the full Navier--Stokes
solution at a positive time.

For the R0.20 root box, write the target Fourier coefficient of the full
viscous Taylor expansion as

\[
  P_{\rm tar}u(\tau)
  =(-i)^5 A_5\tau^5
   +(-i)^5 A_6\tau^6
   +(-i)^5 A_7\tau^7+\mathcal R_{\geq8}(\tau),
  \qquad \tau=4^{2n}t.
\]

The first R0.21 audit proves the following facts by exact frequency and
rational-polynomial arithmetic.

1. The target is unreachable with one through five input leaves.  It is
   reachable with six leaves, unreachable with seven, and reachable again
   with eight.
2. Orders zero through four vanish at the target, even after heat insertions.
3. The order-five target is exactly the pure nonlinear coefficient studied
   in R0.20.
4. The pure nonlinear order-six target vanishes.  The full order-six target
   contains exactly one heat insertion and satisfies, throughout the
   radius-\(10^{-6}\) R0.20 root box,

   \[
     -2.6112769164 < A_6/A_5 < -2.6112696484.
   \]

5. At order seven, two heat insertions contribute approximately
   \(+3.58634 A_5\), while the two- and four-catalyst eight-leaf trees
   contribute approximately \(-5.86797 A_5\) and \(-0.53281 A_5\).
   The certified total interval is

   \[
     -2.81447044 < A_7/A_5 < -2.81441437.
   \]

These statements still stop before the infinite Taylor tail.

## Why a standard norm estimate is insufficient

All initial frequencies have the form

\[
  K_\delta(c,\beta)=\delta^{-1}c(1,1,1)+\beta,
  \qquad \beta\cdot(1,1,1)=0,
  \qquad \delta=4^{-n}.
\]

A black-box Sobolev or Fourier-Wiener estimate bounds the derivative in the
quadratic term by \(|K|=O(\delta^{-1})\).  Its certified time interval
therefore shrinks with the shell level and cannot reach a fixed positive
\(\tau\).  The computed coefficients do not show this growth: through order
12 their Fourier \(\ell^1\) sizes converge as \(n\) increases.  The missing
ingredient is the leading collinearity cancellation.  For nonzero charges
\(c_1,c_2\), incompressibility rewrites

\[
  K_\delta(c_2,\beta_2)\cdot u_1
  =\left(\beta_2-\frac{c_2}{c_1}\beta_1\right)\cdot u_1,
\]

so the apparent \(\delta^{-1}\) loss disappears.  Charge-zero outputs need a
separate invariant-subspace argument.  Proving a uniform version of this
identity is the next analytic bottleneck.

## Proof sequence

### Gate A: cone-frequency algebra

- Define a weighted sequence space for the charge-offset labels \((c,\beta)\).
- Include the first longitudinal \(\delta\)-jet needed by incompressibility.
- Prove that the charge-zero sector remains perpendicular to the common
  diagonal direction.
- Prove heat and Leray-bilinear bounds whose constants do not grow like
  \(\delta^{-1}\).

Failure condition: if the charge-zero sector produces an unavoidable
\(\delta^{-1}\) factor, the present sparse cone family cannot support a
shell-uniform Taylor argument.

### Gate B: a posteriori approximate solution

- Use the heat-inclusive Taylor polynomial through at least order 12 as the
  approximate solution.
- Compute its differential residual with outward-rounded Fourier arithmetic.
- Propagate a scalar control inequality for the correction, including the
  infinite spatial tail.
- Compare two established frameworks: the Sobolev control inequalities of
  [Morosi--Pizzocchero](https://arxiv.org/abs/1104.3832) and the robustness
  criteria of
  [Chernyshenko--Constantin--Robinson--Titi](https://arxiv.org/abs/math/0607181)
  and
  [Dashti--Robinson](https://arxiv.org/abs/math/0701341).

The first framework is closer to the present task because it turns a chosen
approximate solution and its residual into an explicit existence interval and
error function.  Its published Sobolev constants may still lose the cone
cancellation, so Gate A should be completed before numerical optimization of
the control inequality.

### Gate C: target lower bound

Find an explicit \(\tau_0>0\) and a rigorous bound

\[
  \|P_{\rm tar}\mathcal R_{\geq8}(\tau)\|
  < \|A_5\|\tau^5
    \left|1+(A_6/A_5)\tau+(A_7/A_5)\tau^2\right|
\]

for \(0<\tau\leq\tau_0\).  This proves a nonzero target transfer for the full
viscous solution.  It does not yet prove growth of a critical norm or a
repeatable shell cascade.

### Gate D: dynamical significance

- Compare the certified target amplitude with the whole new-shell output,
  not only with the fifth-order coefficient.
- Restore a physical critical-amplitude or dense-packet normalization.
- Quantify stability under phase, polarization, and packet-width errors.
- Only then test whether the one-step inequality can be iterated across
  shells without a summability or heat-loss obstruction.

## Immediate implementation tasks

1. Turn the charge-offset cancellation into an exact operator lemma and unit
   tests for all interactions generated through order 12.
2. Produce a tagged order-12 approximate solution and exact residual schema.
3. Implement the Morosi--Pizzocchero control ODE with interval arithmetic.
4. Run a finite-shell benchmark before attempting a shell-uniform proof.
5. Publish a formal R0.21 note only after Gate C either closes or yields a
   precise obstruction.
