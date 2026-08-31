# R0.73U independent analytic audit

**Audit date:** 2026-09-01

**Method:** independent index/sign derivation, parity checks, exact sparse
Fourier scratch calculations, and collision readback against the R0.73Q--T
interfaces; no file from the parent derivation was imported into the finite
scratch calculations

**Verdict:** the positive heat-covariance hierarchy, centered pressure-variance
refinement, critical stress rows, and narrow quadratic-state no-go are
mathematically consistent subject to the release boundaries below

## 1. Index and pressure-sign audit

With

\[
 \partial_tu_i+u_k\partial_ku_i+\partial_ip=\nu\Delta u_i,
 \qquad \partial_ku_k=0,
\]

the local product tensor \(T_{ij}=u_i u_j\) satisfies

\[
 \partial_tT_{ij}
 =\nu\Delta T_{ij}-2\nu\partial_\ell u_i\partial_\ell u_j
 -\partial_k(u_ku_iu_j)
 -(u_j\partial_ip+u_i\partial_jp).
\]

Taking divergence of Navier--Stokes gives

\[
 -\Delta p=\partial_i\partial_jT_{ij},
 \qquad
 \widehat p(h)=-{h_ih_j\over|h|^2}\widehat T_{ij}(h),\quad h\ne0.
\]

All signs agree with the parent derivation.

## 2. Heat covariance audit

For \(P_s=e^{s\Delta}\), \(v_s=P_su\), and
\(\tau_s=P_s(u\otimes u)-v_s\otimes v_s\), direct expansion gives

\[
 \tau_s(x)=P_s[(u-v_s(x))\otimes(u-v_s(x))](x)\succeq0.
\]

Independent differentiation gives

\[
 (\partial_s-\Delta)\tau_s
 =2\sum_\ell\partial_\ell v_s\otimes\partial_\ell v_s,
 \qquad \tau_0=0.
\]

This is an exact equation in the filter parameter.  It must not be called a
closed physical-time stress equation.

Filtering Navier--Stokes gives

\[
 \partial_tv_s+\nabla\cdot(v_s\otimes v_s)+\nabla p_s
 =\nu\Delta v_s-\nabla\cdot\tau_s,
\]

and

\[
 -\Delta p_s=\partial_i\partial_j(v_{s,i}v_{s,j}+\tau_{s,ij}).
\]

The commutator \(\mathbb P\nabla\cdot\tau_s\) is exactly the unresolved heat
commutator identified at R0.73T.

## 3. Critical and energy-only stress bounds

Positive semidefiniteness gives

\[
 |\tau_s|_F\le\operatorname{tr}\tau_s
 \le P_s|u|^2.
\]

Therefore

\[
 \|\tau_s\|_{L_t^2L_x^3}
 \le\|u\|_{L_t^4L_x^6}^2.
\]

This is on the local/Euclidean critical exponent line, but it assumes the
strong critical norm and is not an energy-class gain.

For fixed \(s>0\) and every \(T\) inside the smooth lifespan, the energy
inequality independently yields

\[
 \|\tau_s\|_{L_t^2(0,T;L_x^3)}^2
 \le {C_S^2H_3(s)\over2\nu}\|u(0)\|_2^4,
 \qquad H_3(s)=\|P_s\|_{L^1\to L^3}.
\]

Since \(H_3(s)\asymp s^{-1}\) at short scale, the norm loses
\(s^{-1/2}\).  The constant is uniform in \(T\).  This is a genuine
positive-scale estimate but cannot be sent uniformly to \(s=0\).

## 4. Centered pressure-variance audit

The quartic balance is unchanged when \(p\) is replaced by \(p-c(t)\).  The
minimizer of

\[
 \mathcal P_c=\int |u|^2(p-c)^2d\mu
\]

is

\[
 \bar p_w={\int|u|^2p\,d\mu\over\int|u|^2d\mu}.
\]

Weighted Cauchy and Young give, for \(0<\vartheta\le2\),

\[
 Q'+4\nu Y+(2-\vartheta)\nu X^2
 \le {4\over\vartheta\nu}\mathcal P_*.
\]

At \(\vartheta=1\) this has the R0.73T left side.  The chain

\[
 \mathcal P_*\le\int |u|^2p^2
 \le C_R^2\|u\|_6^6\le C_R^2AQ
\]

is correct.  The result is a centered sharpening of that local inequality,
but it has a strong formula-level collision with the weighted pressure
correlation method in Tran--Yu--Dritschel 2021.  It must not carry a novelty
or priority claim.

## 5. Four-site parity audit

For

\[
 u=(2\sin(x+y),2\sin x-2\sin(x+y),0)
\]

and \(h_*=(1,2,0)\), two independent sparse-convolution paths give

\[
 \widehat T(h_*)=0,\qquad \widehat V(h_*)=0,
\]

and nonlinear tensor tangent

\[
 K(h_*)=\begin{pmatrix}-2&1&0\\1&0&0\\0&0&0\end{pmatrix}.
\]

Under \(u\mapsto-u\), \(T,p,V,\Theta_s,\tau_s\) are unchanged and \(K\)
changes sign.  Hence the tensor-tangent difference is

\[
 2e^{-5s}K(h_*).
\]

For \(u_L(x)=u(Lx)\), the parabolic-slice Frobenius separation is

\[
 2\sqrt6Le^{-5\theta}
 =2\sqrt{6\theta}e^{-5\theta}s^{-1/2},
 \qquad s=\theta L^{-2}.
\]

This proves non-autonomy of the even quadratic heat state.  It does not rule
out tensor-only absolute upper bounds: pointwise,

\[
 |u\otimes a+a\otimes u|_F^2
 =2\operatorname{tr}(u\otimes u)|a|^2
  +2a^T(u\otimes u)a,
\]

so the quadratic tensor can determine the magnitude of a symmetrized tangent
once \(|a|\) and its tensor pairing are available, despite losing its sign.

## 6. Publication restrictions

1. Keep local-product \(T_{ij}=u_i u_j\) distinct from two-point KHM
   \(R_{ij}(r)\).
2. Call \((v_s,\tau_s)\) the useful filtered state; \(\tau_s\) alone is even
   and non-autonomous.
3. Do not turn positive semidefiniteness into a sign claim for
   \(-\tau_s:\nabla v_s\).
4. Do not call the filter-parameter PDE a physical-time closure.
5. State the \(L_t^2L_x^3\) estimate as either conditional on
   \(L_t^4L_x^6\), or energy-only with the explicit \(s^{-1/2}\) loss.
6. The witness is planar and smooth; it is not a singularity, near-singularity,
   vortex-stretching, or blow-up example.
7. The no-go excludes an autonomous equality for the even quadratic state. It
   does not exclude one-sided estimates or an odd/cubic augmentation.
8. Arbitrary three-dimensional global regularity and the Clay problem remain
   open.
