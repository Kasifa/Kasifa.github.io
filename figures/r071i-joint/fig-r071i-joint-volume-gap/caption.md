# Figure R0.71I - Joint heat evolution leaves an exact trace-to-volume gap

**A.** Let \(A_0=\operatorname{diag}(K^2,2K^2)\),
\(F_0=(e_1-e_2)/\sqrt2\), \(C_0=(e_1+e_2)/\sqrt2\), \(Y=1\), and
\(\tau=\nu K^2t\).  Common heat gives

\[
 q(\tau)=\frac{x(1-x)^2}{2(1+x)},\qquad x=e^{-2\tau}.
\]

Both outer faces vanish: \(q(0)=q(\infty)=0\).  The exact maximum is
\[
 q_*=\frac{71-17\sqrt{17}}{16}
\]
at \(x_*=(-3+\sqrt{17})/4\).  This is a finite-dimensional heat model,
not an NSE solution.

**B.** For the same path,
\[
 \frac{K^{-2}\operatorname{TV}(q)}
 {\int_0^\infty K^{-2}\|F(t)\|_2^2\,dt}
 =\frac{\nu(71-17\sqrt{17})}{3}K^2.
\]
The plotted points use \(\nu=1\).  The quadratic exponent is exact algebra,
not a fitted slope.  Thus variation survives even when the two outer faces
vanish, while its physical-time heat volume is smaller by two frequency
powers.

**C.** A separate exact global-smooth 2D3C NSE family has fixed kinetic
energy \(263/90\), \(B_K(0)=q_K(0)=0\), and \(d_K(0)=8K^4\).  For the fixed
smooth radial multiplier supported near \(|\xi|^2=5,10\), its rescaled
profiles converge in \(C^1([0,M])\), for every fixed \(M\), to

\[
 Q_0=\frac{4x(1-x)^2}{1+x},\quad x=e^{-10\theta},
\]
\[
 Y_0=2e^{-2\theta}+2e^{-8\theta}+2e^{-18\theta}
 +\frac45e^{-10\theta}+\frac25e^{-20\theta},
\]
\[
 A_0=Q_0/Y_0,\qquad
 G_0=\frac{4(e^{-10\theta}+e^{-20\theta})}{Y_0}.
\]

Here \(G_0\) is the limiting \(\|F_K\|_2^2/Y\) density.  The panel plots
closed-form limit profiles, not time-stepped PDE data.  Since \(A_0(0)=0\)
but \(A_0(\theta)>0\), the true NSE family also rejects a frequency-uniform
volume-only upgrade for this multiplier.  No comparison with the preselected
broad dyadic frame is asserted.

**D.** For the two-cell partition
\(\chi_{\delta,\pm}=(1\pm\delta\cos(Kx_3))/2\) on the earlier exact 2D3C
datum, the fixed-energy aggregate is
\[
 \sum_\pm a_{\delta,\pm}=\frac{U^2}{3\delta^2+4}.
\]
With \(U=1\), changing \(\delta=0\) to \(\delta=1\) costs exactly
\[
 \Delta_{\rm ref}=\frac14-\frac17=\frac3{28}.
\]
The gap is a refresh or cutoff-motion cost.  It does not reject a fixed
partition or a transport rule with an independently summable refresh budget.

All values are closed-form evaluations.  There is no DNS, ODE/PDE time
stepping, fitting, or random data.  The figure gives no unconditional
weighted-BV estimate, regularity theorem, singularity claim, originality
claim, or Millennium-problem conclusion.
