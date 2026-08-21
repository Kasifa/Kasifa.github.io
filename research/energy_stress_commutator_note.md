# R0.69N — An energy-level stress-commutator bridge and its time gap

## 1. Result

R0.69M showed that the \(L^2\) near source
\(N_r=r^{5/2}\|\partial_i\partial_j(\eta_0u_i u_j)\|_2\) is not available
for a generic suitable weak solution. R0.69N replaces that source norm by an
exact stress commutator. The resulting estimate uses only localized kinetic
energy, enstrophy, and the second-derivative dissipation that occurs on the
left side of a smooth strain-energy identity.

Let \(u\) be smooth and divergence free on \(\mathbb R^3\). Fix \(r>0\).
Choose \(0\leq\phi\leq1\), equal to one on \(B_{r/2}\), supported in \(B_r\),
with

\[
 \|\nabla^k\phi\|_\infty\leq C_k r^{-k},\qquad k=1,2,3.           \tag{1.1}
\]

There is a compactly supported divergence-free localization \(v\), supported
in \(B_{4r}\) and equal to \(u\) on \(B_{2r}\). Let

\[
 q_v=\partial_i\partial_j(v_i v_j),\qquad
 H_v=\nabla^2(-\Delta)^{-1}q_v,\qquad
 \mathcal P_{v,r}=\int\phi S:H_v\,dx,                            \tag{1.2}
\]

where \(S=S[u]=S[v]\) on the support of \(\phi\).

For \(4\leq q\leq6\), put

\[
 p=\frac{q}{q-2},\qquad
 \theta=3\left(\frac12-\frac1q\right),                           \tag{1.3}
\]

and define the dimensionless quantities

\[
 \mu_v=r^{-1/2}\|v\|_2,\qquad
 \sigma_v=r^{1/2}\|\nabla v\|_2,\qquad
 X_q=\mu_v^{2(1-\theta)}\sigma_v^{2\theta}.                      \tag{1.4}
\]

On the cutoff annulus \(A_\phi=\operatorname{supp}\nabla\phi\), set

\[
 \mu_A=r^{-1/2}\|u\|_{L^2(A_\phi)},\qquad
 \sigma_A=r^{1/2}\|\nabla u\|_{L^2(A_\phi)},\qquad
 D_A=r^3\|\nabla^2u\|_{L^2(A_\phi)}^2.                           \tag{1.5}
\]

Then the near pressure satisfies

\[
 \boxed{
 r^3|\mathcal P_{v,r}|
 \leq C_q X_q\bigl(D_A^{1/2}+\sigma_A+\mu_A\bigr).}              \tag{1.6}
\]

At the least demanding endpoint \(q=4\),

\[
 \boxed{
 r^3|\mathcal P_{v,r}|
 \leq C\mu_v^{1/2}\sigma_v^{3/2}
       \bigl(D_A^{1/2}+\sigma_A+\mu_A\bigr).}                    \tag{1.7}
\]

In particular, the leading term obeys

\[
 C\mu_v^{1/2}\sigma_v^{3/2}D_A^{1/2}
 \leq\varepsilon D_A+C_\varepsilon\mu_v\sigma_v^3.              \tag{1.8}
\]

This is an energy-level replacement for \(\sigma_rN_r\). It does not close
the regularity problem: after time integration, (1.8) requires control of a
cubic instantaneous enstrophy factor, while CKN smallness controls only its
quadratic time integral.

## 2. Exact divergence-free localization

Let \(\eta\) equal one on \(B_{2r}\) and vanish outside \(B_{3r}\). On the
annulus where \(\nabla\eta\neq0\),

\[
 f=\nabla\eta\cdot u,\qquad \int f\,dx=0.                        \tag{2.1}
\]

The Bogovskii construction gives a vector field \(w\), supported in that
annulus, such that

\[
 \nabla\cdot w=f,\qquad
 \|\nabla w\|_2\leq Cr^{-1}\|u\|_{L^2(B_{3r}\setminus B_{2r})},
 \qquad
 \|w\|_2\leq C\|u\|_{L^2(B_{3r}\setminus B_{2r})}.               \tag{2.2}
\]

Thus

\[
 v=\eta u-w                                                         \tag{2.3}
\]

is divergence free, compactly supported in \(B_{4r}\), and equals \(u\) on
\(B_{2r}\). Moreover,

\[
 \|\nabla v\|_2^2
 \leq C\left(\|\nabla u\|_{L^2(B_{3r})}^2
             +r^{-2}\|u\|_{L^2(B_{3r})}^2\right).                \tag{2.4}
\]

This localization can be inserted into the R0.69L stress partition exactly.
If \(\eta_0+\sum_{m\geq2}\chi_m=1\), with \(\eta_0=1\) on \(B_{2r}\), then

\[
 u\otimes u
 =v\otimes v+T_{\mathrm{tr}}
  +\sum_{m\geq2}\chi_m u\otimes u,\qquad
 T_{\mathrm{tr}}=\eta_0u\otimes u-v\otimes v.                   \tag{2.5}
\]

The correction \(T_{\mathrm{tr}}\) is supported outside \(B_{2r}\), so it is
a transition stress, not part of the near singular integral. If

\[
 e_{\mathrm{tr}}=\frac1r\int|T_{\mathrm{tr}}|\,dx,               \tag{2.6}
\]

then the R0.69K separated-kernel estimate gives

\[
 r^3|\mathcal P_{\mathrm{tr}}|
 \leq C\sigma_r e_{\mathrm{tr}},\qquad
 \sigma_r=r^{1/2}\|\phi^{1/2}S\|_2.                             \tag{2.7}
\]

The remote shells retain the same
\(B_\infty=\sum_{m\geq2}2^{-5m}e_m\) budget.

## 3. The pressure cancellation becomes a cutoff commutator

For a matrix field \(A\), write

\[
 \mathcal T(A)=\partial_a\partial_b(-\Delta)^{-1}A_{ab}.         \tag{3.1}
\]

Since \(v\) is divergence free,

\[
 \partial_a\partial_bS_{ab}[v]=0,\qquad \mathcal T(S[v])=0.      \tag{3.2}
\]

The pressure pairing can therefore be transferred to the localized stress:

\[
 \begin{aligned}
 \mathcal P_{v,r}
 &=\langle q_v,\mathcal T(\phi S)\rangle\\
 &=\int v_i v_j\,\partial_i\partial_j\mathcal T(\phi S)\,dx.
                                                                    \tag{3.3}
 \end{aligned}
\]

This uses the exact double-divergence identity for \(q_v\), not an absolute
value bound on \(u\,q_v\).

The key point is that \(\mathcal T(\phi S)\) loses one derivative because the
unlocalized contraction (3.2) vanishes. Direct expansion gives

\[
 \partial_a\partial_b(\phi S_{ab})
 =\nabla\phi\cdot\Delta v+(\partial_{ab}\phi)S_{ab}.              \tag{3.4}
\]

With \(g=v\cdot\nabla\phi\),

\[
 \Delta g
 =\nabla\phi\cdot\Delta v
  +2(\partial_kv_i)(\partial_{ki}\phi)
  +v_i\partial_i\Delta\phi.                                      \tag{3.5}
\]

Consequently,

\[
 \mathcal T(\phi S)
 =-v\cdot\nabla\phi+(-\Delta)^{-1}G_\phi[v],                     \tag{3.6}
\]

where

\[
 G_\phi[v]
 =-2(\partial_kv_i)(\partial_{ki}\phi)
  -v_i\partial_i\Delta\phi
  +(\partial_{ab}\phi)S_{ab}.                                   \tag{3.7}
\]

Every coefficient on the right is supported in \(A_\phi\). Formula (3.6)
is the exact stress-commutator identity used below.

## 4. Calderón--Zygmund estimate with only one derivative of strain

For \(1<p<\infty\), the \(L^p\) boundedness of
\(\nabla^2(-\Delta)^{-1}\), together with (3.6), gives

\[
 \begin{aligned}
 \|\nabla^2\mathcal T(\phi S)\|_p
 \leq C_p\bigl(&r^{-1}\|\nabla^2v\|_{L^p(A_\phi)}
 +r^{-2}\|\nabla v\|_{L^p(A_\phi)}\\
 &+r^{-3}\|v\|_{L^p(A_\phi)}\bigr).                              \tag{4.1}
 \end{aligned}
\]

For \(4\leq q\leq6\), the exponent \(p=q/(q-2)\) lies in
\([3/2,2]\), and Hölder gives

\[
 |\mathcal P_{v,r}|
 \leq\|v\|_q^2\|\nabla^2\mathcal T(\phi S)\|_p.                  \tag{4.2}
\]

Because \(A_\phi\) has volume \(O(r^3)\),

\[
 \|F\|_{L^p(A_\phi)}
 \leq Cr^{3(1/p-1/2)}\|F\|_{L^2(A_\phi)}.                        \tag{4.3}
\]

The three-dimensional Gagliardo--Nirenberg inequality gives

\[
 \|v\|_q^2
 \leq C_q\|v\|_2^{2(1-\theta)}
             \|\nabla v\|_2^{2\theta},
 \qquad
 \theta=3\left(\frac12-\frac1q\right).                           \tag{4.4}
\]

Substituting (4.1)--(4.4), and collecting the exact powers of \(r\), proves
(1.6). No \(L^2\) norm of the quadratic pressure source appears.

Combining the transition correction and the remote shells gives the complete
energy-level pressure budget

\[
 \boxed{
 r^3|\mathcal P_r|
 \leq C_q X_q(D_A^{1/2}+\sigma_A+\mu_A)
      +C\sigma_r(e_{\mathrm{tr}}+B_\infty).}                     \tag{4.5}
\]

R0.69M supplies \(B_\infty\leq\mathfrak M_2/120\).

## 5. Why the direct Hardy--BMO route stops above energy

The pressure source does possess a genuine compensated structure. For each
fixed \(j\), the vector field \(\partial_jv\) is divergence free and
\(\nabla v_j\) is curl free. Hence

\[
 q_v=\sum_j(\partial_jv)\cdot\nabla v_j.                          \tag{5.1}
\]

The Coifman--Lions--Meyer--Semmes div--curl theorem yields

\[
 \|q_v\|_{\mathcal H^1}
 \leq C\|\nabla v\|_2^2.                                        \tag{5.2}
\]

Riesz transforms preserve the Hardy endpoint, so Hardy--BMO duality gives

\[
 r^3|\mathcal P_{v,r}|
 \leq C\bigl(r\|\nabla v\|_2^2\bigr)
          \bigl(r^2\|\phi S\|_{\mathrm{BMO}}\bigr).               \tag{5.3}
\]

The source side is now at energy regularity, but the test side is not.
\(W^{1,2}(\mathbb R^3)\) does not embed in BMO. More generally, for
\(0<s<3\), the Hardy--Sobolev redistribution

\[
 \mathcal H^1
 \hookrightarrow\dot W^{-s,\,3/(3-s)}                           \tag{5.4}
\]

pairs against

\[
 \dot W^{s,\,3/s}.                                               \tag{5.5}
\]

Every dual point satisfies

\[
 s\left(\frac3s\right)=3,                                       \tag{5.6}
\]

the critical BMO Sobolev line. The dissipation space
\(\dot W^{1,2}\) has product \(1\cdot2=2\), strictly below that line. At the
Hilbert point \(p'=2\), (5.5) requires \(s=3/2\), not one derivative.

This is the Hardy--BMO duality wall. Estimate (4.5) avoids it by using the
second-divergence stress representation and the exact cancellation
\(\mathcal T(S)=0\), rather than pairing an arbitrary Hardy source with an
arbitrary test function.

## 6. The endpoint \(q=4\) is optimal inside the energy interpolation family

After Young's inequality, the leading term in (1.6) produces

\[
 X_q^2
 =\mu_v^{4(1-\theta)}\sigma_v^{4\theta}.                         \tag{6.1}
\]

As \(q\) runs from \(4\) to \(6\),

\[
 4\theta=6-\frac{12}{q}\quad\text{increases from }3\text{ to }4,
 \qquad
 4(1-\theta)=-2+\frac{12}{q}\quad\text{decreases from }1\text{ to }0.
                                                                    \tag{6.2}
\]

Thus \(q=4\) minimizes the enstrophy power and gives
\(\mu_v\sigma_v^3\). The other endpoint gives \(\sigma_v^4\).
No exponent in the admissible \(L^2\)-based family reaches the quadratic
CKN power \(\sigma_v^2\).

The gap is not removable by a time-only inequality. On a normalized time
interval, let

\[
 \sigma_A(t)=A\,\mathbf1_{[0,A^{-2}]}(t),\qquad \mu_A(t)=1.       \tag{6.3}
\]

Then

\[
 \int\sigma_A^2\,dt=1,\qquad
 \int\mu_A\sigma_A^3\,dt=A\longrightarrow\infty.                 \tag{6.4}
\]

Smooth time profiles approximate (6.3). This is a functional exponent
witness only; it is not asserted to satisfy Navier--Stokes.

## 7. Route decision

R0.69N produces two rigorous conclusions.

1. The direct Hardy--BMO route correctly places the pressure source at the
   energy endpoint, but necessarily places localized strain on the critical
   BMO Sobolev line. It does not close with one \(L^2\) derivative.
2. The exact stress-commutator identity bypasses that wall and replaces
   \(\sigma_rN_r\) by the energy-level family (1.6), without losing the
   \(2^{-5m}\) far-shell gain.

The remaining obstruction is now temporal and quantitative: the best
\(L^2\)-based endpoint costs \(\mu_v\sigma_v^3\), one enstrophy power above
the CKN quadratic integral.

R0.69O will test whether the local energy inequality, a backward heat cutoff,
or a time-frequency decomposition can recover that missing power without
assuming a known Serrin, gradient, or BMO regularity criterion. Its acceptance
criterion is an estimate of the time-integrated leading pressure term by
quadratic CKN quantities plus an absorbable part of \(D_A\). Failure produces
a sharp temporal-exponent no-go statement.

R0.69N gives no Navier--Stokes regularity or singularity conclusion and does
not solve the Millennium Problem.

## 8. Primary sources

1. R. Coifman, P.-L. Lions, Y. Meyer, and S. Semmes, *Compensated
   compactness and Hardy spaces*, J. Math. Pures Appl. 72 (1993), 247--286;
   bibliographic record and seminar version:
   <https://numdam.org/item/SEDP_1989-1990____A16_0/>.
2. H. Kozono and Y. Taniuchi, *Bilinear estimates in BMO and the
   Navier--Stokes equations*, Math. Z. 235 (2000), 173--194,
   <https://doi.org/10.1007/s002090000130>.
3. D. Li and X. Zhang, *A regularity upgrade of pressure*,
   <https://arxiv.org/abs/2106.11852>.
4. S. Gustafson, K. Kang, and T.-P. Tsai, *Interior regularity criteria for
   suitable weak solutions of the Navier--Stokes equations*,
   <https://arxiv.org/abs/math/0607114>.
