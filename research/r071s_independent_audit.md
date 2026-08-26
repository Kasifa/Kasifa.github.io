# R0.71S independent audit

**Audit boundary:** finite time-packet constants, soft even-touch cancellation,
and the genuine R0.71O/R0.71P initial-face frequency ledger.

`research/r071s_independent_audit.py` imports neither the exact producer nor
its JSON output.  It reconstructs the Toeplitz and periodic Gram matrices with
NumPy, diagonalizes them with `numpy.linalg.eigh`, and evaluates the adjoint
heat packets by independent 512-point Gauss--Legendre quadrature.

The executed outputs are
`research/certificates/r071s/result.json` and
`research/certificates/r071s/independent-result.json`.  Both contain six
passing checks.  Across the audited matrices, the largest producer--checker
eigenvalue difference is \(1.776\times10^{-15}\); the largest relative
difference in the inverse heat-packet mean square is
\(8.882\times10^{-16}\).

## Reconstructed statements

1. For the nonzero-mean box packet

   \[
   \psi_{b,h}=h^{-1/2}\mathbf 1_{[b,b+h)},
   \qquad h=\theta K^{-2},
   \]

   constant reproduction has diagonal norm

   \[
   \left\|\frac{\psi_{b,h}}{\int\psi_{b,h}}\right\|_2^2
   =\frac1h=\frac{K^2}{\theta}.
   \]

2. For \(N\) same-direction interval box packets with \(h=p\delta\), the
   finite Gram matrix is

   \[
   G_{k\ell}=\left(1-\frac{|k-\ell|}{p}\right)_+,
   \]

   and its largest eigenvalue lies in the exact enclosure

   \[
   p-\frac{p^2-1}{3N}\le\lambda_{\max}(G)\le p.
   \]

   For periodic equally spaced boxes it is exactly \(p=Nh/T\).

3. The backward/adjoint heat packet has

   \[
   \|p_{b,h,K}\|_2^2
   =\frac{1-e^{-2\nu K^2h}}{2\nu K^2}.
   \]

   At \(h=\theta K^{-2}\), its normalized nonzero mean therefore costs

   \[
   \left|\int\frac p{\|p\|_2}\right|^{-2}
   =\frac{\nu K^2}{2}\coth\!\left(\frac{\nu\theta}{2}\right).
   \]

4. A separable bilinear detector with a zero-mean time factor annihilates
   constant leading data.  If both \(L^2\)-normalized factors have nonzero box
   mean, normalization to unit constant response costs \(1/h=K^2/\theta\).

5. For the soft even touch \(a_\eta(t)=t^4/(t^4+\eta)\), the left and right
   signed layers have limiting masses \(-1\) and \(+1\).  The signed atom is
   zero and the Jordan atom is two.

6. The compatible covariant dilation of the genuine initial datum is

   \[
   u_{0,K}=K(0,\cos Kx_1,\cos Kx_2).
   \]

   It retains the exact one-sided ledger

   \[
   Y_0=K^4,
   \quad \|F_0\|_2^2=\frac{K^6}{4},
   \quad C_t(0)=2K^2F_0,
   \quad A_+=\frac{K^2}{4},
   \quad K^{-2}A_+=\frac14.
   \]

   NSE covariance independently gives the corresponding bare normalized
   Leray time integral a factor \(K^{-2}\).  A fixed-amplitude frequency sweep
   would not certify this statement and is not used in the final audit.

## Result boundary

The Gram and packet computations are exact finite method tests.  The
even-touch path is a forced-parabolic family, not a Navier--Stokes trajectory.
The Fourier initial face is a genuine smooth NSE initial observation-boundary
trace.  Its
positive-time integral is used only through the exact covariance identity;
the audit does not numerically advance NSE and does not produce an internal
entry or a lower bound for an actual incidence constant.

No temporal-packing theorem, infinite-frame estimate, continuation criterion,
singularity result, or global-regularity claim is checked here.
