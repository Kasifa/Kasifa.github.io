# R0.69L — A scale-invariant three-zone pressure budget

## 1. Result

R0.69K showed that stress localization improves the pressure Hessian of a
remote velocity-generated shell from the general scalar rate \(R^{-3}\) to
the sharp rate \(R^{-5}\). R0.69L places that gain in the same normalized
inequality as the near Calderón--Zygmund term and the exact cutoff flux.

Let \(u,p\) be smooth on \(\mathbb R^3\), with \(\nabla\cdot u=0\) and
sufficient decay for the formulas below. Fix a center at the origin and a
radius \(r>0\). Let
\(0\leq\phi\leq1\) equal one on \(B_{r/2}\), vanish outside \(B_r\), and
satisfy

\[
 |\nabla^k\phi|\leq C_k r^{-k},\qquad k=1,2.
 \tag{1.1}
\]

Write

\[
 S=\frac12(\nabla u+\nabla u^T),\qquad
 q=\operatorname{tr}((\nabla u)^2)
   =\partial_i\partial_j(u_i u_j),\qquad
 H=\nabla^2p,\qquad -\Delta p=q,
 \tag{1.2}
\]

and define the localized pressure pairing

\[
 \mathcal P_r:=\int\phi S:H\,dx.
 \tag{1.3}
\]

Choose a stress partition

\[
 \eta_0+\sum_{m\geq2}\chi_m=1,
 \tag{1.4}
\]

where \(\eta_0\) is supported in \(B_{4r}\), while \(\chi_m\) is supported
where \(|y|\simeq2^m r\). Put

\[
 q_0=\partial_i\partial_j(\eta_0u_i u_j),\qquad
 E_m=\int\chi_m|u|^2,\qquad e_m=\frac{E_m}{r}.
 \tag{1.5}
\]

The three scale-invariant local quantities are

\[
 \sigma_r=r^{1/2}\|\phi^{1/2}S\|_2,
 \qquad
 N_r=r^{5/2}\|q_0\|_2,
 \tag{1.6}
\]

and

\[
 b_r=r^2\int_{B_r\setminus B_{r/2}}|u|\,|q|\,dx
     +r\int_{B_r\setminus B_{r/2}}|u|\,|\nabla p|\,dx.
 \tag{1.7}
\]

For an integer \(M\geq3\), set \(A=2^M\) and

\[
 B_M=\sum_{m=2}^{M-1}2^{-5m}e_m
     +2^{-5M}\sum_{m\geq M}e_m.
 \tag{1.8}
\]

Then

\[
 \boxed{
 r^3|\mathcal P_r|
 \leq C\min\bigl\{b_r,\;\sigma_r(N_r+B_M)\bigr\}.}
 \tag{1.9}
\]

The second entry is the promised near--transition--far budget: \(N_r\) is
the near Calderón--Zygmund cost, the finite sum in \(B_M\) is the transition
annulus, and the last term has the far-field gain \(A^{-5}\).

The separation parameter cannot close the estimate by itself. In fact,

\[
 B_M-B_{M+1}
 =\bigl(2^{-5M}-2^{-5(M+1)}\bigr)
   \sum_{m\geq M+1}e_m\geq0,
 \tag{1.10}
\]

so

\[
 \boxed{
 \inf_{M\geq3}B_M
 =\sum_{m\geq2}2^{-5m}e_m.}
 \tag{1.11}
\]

Increasing \(A\) makes the lumped far tail small only by moving each fixed
shell into the transition sum. The near term \(N_r\), the exact boundary
quantity \(b_r\), and the weighted shell floor (1.11) do not acquire an
\(A\)-small factor. This is a parameter-migration obstruction, not a loss of
the \(R^{-5}\) estimate.

## 2. Exact near and shell decomposition

Let

\[
 T^{(0)}_{ij}=\eta_0u_i u_j,qquad
 T^{(m)}_{ij}=\chi_m u_i u_j.
 \tag{2.1}
\]

Because the cutoffs partition the stress before differentiation,

\[
 q=q_0+\sum_{m\geq2}q_m,qquad
 q_m=\partial_i\partial_jT^{(m)}_{ij}.
 \tag{2.2}
\]

Let \(H_0=\nabla^2(-\Delta)^{-1}q_0\). The operator acting on \(q_0\) is a
matrix of Riesz transforms, hence

\[
 \|H_0\|_2\leq C\|q_0\|_2.
 \tag{2.3}
\]

Consequently,

\[
 r^3\left|\int\phi S:H_0\right|
 \leq C\sigma_rN_r.
 \tag{2.4}
\]

The cutoff derivatives inside \(q_0\) are part of \(N_r\); omitting them
would destroy the exact decomposition (2.2).

For \(x\in B_r\) and a separated shell \(m\geq2\), two integrations by
parts give

\[
 (H_m)_{ab}(x)
 =\int\partial_i\partial_jK_{ab}(x-y)
       \chi_m(y)u_i(y)u_j(y)\,dy,
 \tag{2.5}
\]

where \(K_{ab}=\partial_a\partial_b(4\pi|\cdot|)^{-1}\). Since
\(|\nabla^2K(x-y)|\leq C(2^m r)^{-5}\),

\[
 \|H_m\|_{L^\infty(B_r)}
 \leq C(2^m r)^{-5}E_m.
 \tag{2.6}
\]

Cauchy--Schwarz on \(B_r\) now yields

\[
 r^3\left|\int\phi S:H_m\right|
 \leq C\sigma_r\,2^{-5m}e_m.
 \tag{2.7}
\]

Summing (2.7) for \(2\leq m<M\), and using
\(2^{-5m}\leq2^{-5M}=A^{-5}\) for \(m\geq M\), proves the second bound in
(1.9).

## 3. The exact annular pressure flux on the same scale

R0.69I gave the weighted pressure identity

\[
 \mathcal P_r
 =\int(\Delta p)u\cdot\nabla\phi\,dx
  +\int u_i(\partial_jp)(\partial_{ij}\phi)\,dx.
 \tag{3.1}
\]

Both terms are supported in \(B_r\setminus B_{r/2}\). Using
\(\Delta p=-q\) and (1.1),

\[
 r^3|\mathcal P_r|\leq Cb_r.
 \tag{3.2}
\]

Thus \(b_r\), \(\sigma_rN_r\), and \(\sigma_rB_M\) are compared only after
the common factor \(r^3\) has made the pressure production dimensionless.
The annular identity is not a second source of smallness: it is an exact
alternative representation of the same pairing.

## 4. Scaling audit

Under

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
 \qquad p_\lambda(x,t)=\lambda^2p(\lambda x,\lambda^2t),
 \qquad r_\lambda=\lambda^{-1}r,
 \tag{4.1}
\]

all of

\[
 r^3\mathcal P_r,\quad \sigma_r,\quad N_r,\quad b_r,\quad e_m,\quad B_M
 \tag{4.2}
\]

are invariant. In particular, the two extra powers found in R0.69K are
separation powers, not subcritical scaling powers.

For comparison with the localized strain dissipation, define

\[
 D_r=r^3\int\phi|\nabla S|^2\,dx.
 \tag{4.3}
\]

This is also invariant. Absorbing pressure into dissipation would require a
new estimate such as

\[
 C\min\{b_r,\sigma_r(N_r+B_\infty)\}\leq\varepsilon D_r,
 \qquad \varepsilon<1,
 \tag{4.4}
\]

on the relevant sequence of scales. Finite energy and large \(A\) alone do
not imply (4.4).

## 5. Why separation alone cannot imply absorption

The obstruction is visible both in (1.11) and by amplitude homogeneity.
Take a smooth compactly supported divergence-free local field and a disjoint
remote anisotropic packet of the type used in R0.69K. Scale their amplitudes
by \(\alpha\) and \(\beta\), respectively. A local strain--remote pressure
cross term is homogeneous as

\[
 \mathcal P_{\mathrm{cross}}\sim\alpha\beta^2,
 \tag{5.1}
\]

The local field can be chosen so this coefficient is nonzero. Indeed, for a
nonzero trace-free constant matrix \(Q\),
\(\int\phi S:Q=-\int u\cdot Q\nabla\phi\), and
\(Q\nabla\phi\) is not generally a gradient; its Leray projection supplies a
divergence-free test field. The R0.69K packet supplies such a nonzero remote
matrix \(Q\), up to a smaller separation remainder.

whereas the local strain dissipation is homogeneous as

\[
 D_{\mathrm{local}}\sim\alpha^2.
 \tag{5.2}
\]

The ratio is proportional to \(\beta^2/\alpha\) and is not bounded by the
separation ratio. Every fixed smooth choice has finite energy, but no
uniform absorption constant follows from finiteness of energy. This does not
construct a singular solution; it identifies the missing hypothesis in this
particular closure attempt.

## 6. Route decision

R0.69L retains the sharp \(A^{-5}\) far-tail gain and proves that optimizing
\(A\) converges to the weighted shell quantity

\[
 B_\infty=\sum_{m\geq2}2^{-5m}e_m,
 \tag{6.1}
\]

rather than to zero. The next viable test is therefore not another choice of
separation radius. It is whether a scale-local hypothesis already compatible
with known regularity theory controls at least one of

\[
 b_r,\qquad N_r+B_\infty,
 \tag{6.2}
\]

relative to \(D_r\). R0.69M will compare these quantities with local energy,
Morrey-type, and pressure criteria, and will isolate any genuinely weaker
conditional criterion before attempting a proof.

R0.69L gives no Navier--Stokes regularity or singularity conclusion and does
not solve the Millennium Problem.
