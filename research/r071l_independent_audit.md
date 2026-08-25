# R0.71L independent audit — fixed-cell viscous collar and projective tangent

## 1. Audit status

This audit reconstructs the R0.71J pure-heat Fourier witness and the R0.71K
fixed tensor cell without importing either earlier checker or an exact
producer.  It separates the selected-cell projective tangent into its
heat-main and viscous-collar parts, retains the radial and enstrophy
normalization rows, and checks their fusion into the scalar joint source.

The numerical output is **diagnostic only**.  Gauss--Legendre samples do not
prove a sign on a continuous time interval.  The checker evaluates only the
pure-heat leading coefficient; it does not compute a sequence of finite-
\(K\) trajectories or verify an asymptotic remainder.  The audit is not a
finite-frequency DNS calculation, an arbitrary-partition statement, a signed
full-frame theorem, or a Leray-level passage.

The standalone checker is
`research/r071l_independent_audit.py`.  Its default command is

```bash
tmp/r068b-venv/bin/python research/r071l_independent_audit.py \
  --output /tmp/r071l-independent-result.json
```

The spatial and time rules can be changed independently with
`--spatial-order` and `--time-order`.  The defaults are respectively 180 and
48.

## 2. Fixed scaled object

Use

\[
 y=Kx,\qquad \theta=\nu K^2t,\qquad
 \kappa=4K,\qquad \theta_*={\log2\over18}.
\]

For one unfolded cell, all inner products use

\[
 \langle f,g\rangle_\eta
 ={1\over(2\pi)^3}\int_{\mathbb R^3}f(y)\cdot g(y)\,dy.
 \tag{2.1}
\]

Let \(\bar F,\bar W,\bar\omega\) be the selected-parent pure-heat fields
rebuilt from the fourteen-mode real 2D3C velocity datum.  For the fixed
R0.71K atom

\[
 \eta(y)=h(y_1)h(y_2)h(y_3),
\]

put

\[
 \bar C=\nabla_y\times(\eta\bar W),\quad
 d=\|\bar C\|_\eta^2,\quad
 B=\langle\bar F,\bar C\rangle_\eta,\quad
 Y=\|\bar\omega\|_2^2,
 \tag{2.2}
\]

\[
 \Pi\bar F=\bar F-{B\over d}\bar C,
 \qquad
 \zeta={B\over\sqrt{dY}}.
 \tag{2.3}
\]

The script reconstructs Fourier curl, convolution, Leray projection, parent
restriction, and time differentiation directly.  It then evaluates the
complete tensor cell in physical space.

## 3. Heat, collar, and fused tangent

Because the cutoff is fixed and the limiting parent vorticity satisfies
\(\bar W_\theta=\Delta_y\bar W\),

\[
 \bar C_\theta=\Delta_y\bar C+\bar G_{\rm col},
 \tag{3.1}
\]

where

\[
 \bar G_{\rm col}
 =-\nabla_y\times\left(
 2\sum_m(\partial_m\eta)\partial_m\bar W
 +(\Delta\eta)\bar W
 \right).
 \tag{3.2}
\]

Define

\[
 \tau_H={\langle\Pi\bar F,\Delta\bar C\rangle\over\sqrt{dY}},
 \qquad
 \tau_{\rm col}
 ={\langle\Pi\bar F,\bar G_{\rm col}\rangle\over\sqrt{dY}},
 \tag{3.3}
\]

\[
 \tau_{\rm tan}
 ={\langle\Pi\bar F,\bar C_\theta\rangle\over\sqrt{dY}}.
 \tag{3.4}
\]

The fused tangent (3.4) is evaluated directly.  The heat term is evaluated
by periodic integration by parts,

\[
 \langle\Pi\bar F,\Delta\bar C\rangle
 =-\langle\nabla\Pi\bar F,\nabla\bar C\rangle.
 \tag{3.5}
\]

The collar is evaluated in the corresponding weak form

\[
 \langle\Pi\bar F,\bar G_{\rm col}\rangle
 =\langle\Pi\bar F,\bar C_\theta\rangle
 +\langle\nabla\Pi\bar F,\nabla\bar C\rangle.
 \tag{3.6}
\]

Thus no numerical third derivative of the bump is required.  The audit
checks

\[
 \boxed{\tau_{\rm tan}=\tau_H+\tau_{\rm col}.}
 \tag{3.7}
\]

## 4. Complete scalar fusion

The other two rows are

\[
 \tau_R
 ={\langle\bar F_\theta+16\bar F,\bar C\rangle\over\sqrt{dY}},
 \qquad
 \tau_N=-{Y_\theta\over2Y}\zeta.
 \tag{4.1}
\]

The complete limiting source is

\[
 j=\tau_R+\tau_{\rm tan}+\tau_N.
 \tag{4.2}
\]

Direct differentiation of \(B/\sqrt{dY}\) gives the independent scalar
check

\[
 \boxed{j=\zeta_\theta+16\zeta.}
 \tag{4.3}
\]

Consequently

\[
 \boxed{
 \int_0^{\theta_*}\zeta j\,d\theta
 ={\zeta(\theta_*)^2-\zeta(0)^2\over2}
 +16\int_0^{\theta_*}\zeta^2\,d\theta.}
 \tag{4.4}
\]

The numerical checker verifies both the pointwise differential fusion and
the integrated identity.  Small floating-point residuals verify the
implementation; they do not replace a mathematical proof.

## 5. Analytic scale transfer external to the checker

The statements in this section are **not outputs of the quadrature checker**.
For every fixed \(\nu>0\), the separate R0.71J fixed-window convergence in a
sufficiently high weighted Sobolev norm, followed by fixed-cutoff product and
pairing estimates, gives the analytic asymptotic transfer

\[
 z_Q=K^{-3/2}\bigl(\zeta+O_\nu(K^{-1})\bigr),
 \tag{5.1}
\]

\[
 \mathcal J_{\#,Q}
 =\nu K^{1/2}\bigl(\tau_\#+O_\nu(K^{-1})\bigr),
 \qquad
 \#\in\{H,{\rm col},{\rm tan},R,N\}.
 \tag{5.2}
\]

For

\[
 \mathfrak T_{\#,K}
 =\kappa^{-2}\sum_{Q=1}^{K^3}
 \int_0^{\theta_*/(\nu K^2)}
 z_Q^+\mathcal J_{\#,Q}\,dt,
 \tag{5.3}
\]

the cell count, frame weight, and physical-time change give

\[
 \boxed{
 \mathfrak T_{\#,K}
 ={K^{-2}\over16}
 \int_0^{\theta_*}\zeta^+\tau_\#\,d\theta
 +O_\nu(K^{-3}).}
 \tag{5.4}
\]

The absolute version replaces \(\tau_\#\) by \(|\tau_\#|\).  Thus, whenever
the relevant leading integral is nonzero, the viscous collar and projective
tangent have leading \(K^{-2}\) aggregate scale.  The checker diagnoses those
leading integrals only in the pure-heat limit; it neither proves their
continuous sign nor verifies the \(O_\nu(K^{-3})\) finite-\(K\) remainder.
That remainder belongs to the R0.71J analytic transfer.  The leading
viscosity cancels between the source and the parabolic time window.

## 6. Default numerical diagnostics

With spatial order 180 and time order 48, the checker obtains at
\(\theta_*\)

\[
 d=502.7892176509253,
 \qquad
 B=0.5400290263842784,
 \tag{6.1}
\]

\[
 Y=35.12843837102585,
 \qquad
 \zeta=0.004063447976611747.
 \tag{6.2}
\]

The following pure-heat diagnostic coefficients already contain the factor
\(1/16\) from (5.4):

| row | signed \(K^{-2}\) coefficient | absolute \(K^{-2}\) coefficient |
|---|---:|---:|
| radial | \(+1.9789472944\times10^{-7}\) | same |
| heat-main tangent | \(+2.6801550058\times10^{-7}\) | same |
| viscous collar | \(-8.9253344742\times10^{-9}\) | \(8.9253344742\times10^{-9}\) |
| fused projective tangent | \(+2.5909016611\times10^{-7}\) | same |
| normalization | \(+2.7008990203\times10^{-7}\) | same |
| complete joint source | \(+7.2707479758\times10^{-7}\) | same |

On the 48 interior time nodes,

\[
 0.0275032\le\tau_{\rm tan}\le0.1013794,
 \tag{6.3}
\]

\[
 -0.0027268\le\tau_{\rm col}\le-6.81\times10^{-7},
 \tag{6.4}
\]

and the sampled fused joint source is positive.  Again, (6.3)--(6.4) are
sample ranges, not continuous interval enclosures.

The default maximum residuals are approximately

\[
 |\tau_{\rm tan}-\tau_H-\tau_{\rm col}|<9\times10^{-18},
 \tag{6.5}
\]

\[
 |j-\zeta_\theta-16\zeta|<5\times10^{-16},
 \tag{6.6}
\]

and the integrated residual in (4.4) is below
\(2\times10^{-19}\).

The order-180 initial cell work is about \(-4.57\times10^{-6}\), whereas
the independently reconstructed global Fourier work is exactly zero.  This
is a spatial quadrature residual.  It is deliberately exposed rather than
silently reset to zero.

## 7. Sign and cancellation verdict

For this fixed template and witness, the numerical evidence has a clear
structure:

1. the heat-main tangent is positive on every sampled positive time;
2. the viscous collar is negative on every sampled positive time;
3. the collar removes only a small part of the heat-main tangent;
4. the fused tangent and complete joint source remain positive.

At the default orders, the signed collar removes about \(3.33\%\) of the
heat-main tangent integral.  This is opposite-sign partial cancellation, not
complete cancellation.

There is nevertheless an exact general cancellation mechanism.  If a fixed-
cutoff parent field lies in one Laplace eigenspace,

\[
 \bar W_\theta=-\mu\bar W,
\]

then \(\bar C_\theta=-\mu\bar C\), so

\[
 P_{\bar C^\perp}\bar C_\theta=0,
 \qquad
 P\Delta\bar C=-P\bar G_{\rm col}.
 \tag{7.1}
\]

The heat-main and collar projective vectors then cancel exactly for every
test vector.  This is a rigorous algebraic lemma, but it is not by itself a
nonzero positive-creation NSE witness.

The abstract tangent-plane algebra also permits same-sign pairings whenever
\(P\Delta C\) and \(PG_{\rm col}\) are not antiparallel.  The current audit
does not realize or certify such a pairing inside the declared NSE family.
It therefore makes no universal sign claim.

## 8. Heat payment and Leray boundary

For overlap \(N=8\), the R0.71K local heat/support endpoint is at most

\[
 \mathcal H_K^{\rm loc}
 \le {0.29650115085083817\over\nu K^4}.
 \tag{8.1}
\]

If a rigorous interval calculation confirms that the limiting absolute
collar and tangent coefficients are nonzero, the default diagnostics predict

\[
 {\mathfrak T_{{\rm col},K}^{\rm abs}\over\mathcal H_K^{\rm loc}}
 \gtrsim3.01\times10^{-8}\,\nu K^2,
 \tag{8.2}
\]

\[
 {\mathfrak T_{{\rm tan},K}^{\rm abs}\over\mathcal H_K^{\rm loc}}
 \gtrsim8.74\times10^{-7}\,\nu K^2.
 \tag{8.3}
\]

This would reject an absolute estimate of the form

\[
 \mathfrak T_K^{\rm abs}
 \le C(E_0,\nu)\mathcal H_K^{\rm loc},
 \qquad E_0=2041/200.
 \tag{8.4}
\]

It would **not** reject a bare \(O(1)\) Leray-energy or total-dissipation
budget.  The present contribution is \(O(K^{-2})\), and the dyadic sum of
\(K^{-2}\) converges.  A claim that energy-only payment is impossible would
therefore exceed the evidence.

## 9. What a formal sign certificate still needs

The current cutoff is nonalgebraic.  A formal producer should reduce the
spatial calculation to finitely many one-dimensional moments of
\(h,h',h''\), enclose those moments by directed interval integration, and
then enclose the resulting finite exponential sums over
\([0,\theta_*]\).

Because the exact collar coefficient is expected to vanish at
\(\theta=0\), the stable target is a negative enclosure for

\[
 {\tau_{\rm col}(\theta)\over\theta}
\]

rather than a strict negative enclosure for \(\tau_{\rm col}\) on a closed
interval containing zero.  A second validator may use physical-space
quadrature and order doubling, but its output remains numerical corroboration
rather than the interval proof itself.

## 10. Claim boundary

The calculation concerns one fixed aligned scale-covariant partition and the
single selected broad parent \(\kappa=4K\).  Translation symmetry extends the
one-cell pure-heat leading coefficients to its finite \(K^3\)-cell family.
The finite-\(K\) transfer and its remainder are analytic inputs from R0.71J,
not checker outputs.  All vector components are retained; this is not a
one-coordinate surrogate.

No conclusion is made for arbitrary or degenerating templates, moving cells,
denominator faces, refresh atoms, child-refined frames, signed cancellation
over the complete frame, an infinite frame--cell identity, Leray--Hopf
solutions, continuation, regularity, singularity, or the Millennium problem.
