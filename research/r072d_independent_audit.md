# Independent analytic audit of R0.72D

**Date:** 2026-08-27  
**Object audited:** `research/r072d_report-source.md`  
**Decision:** pass inside the declared exact triangular class, subject to the
scope and constant dependencies stated below.

## 1. Audit boundary

This audit reconstructs the proof from the defining equations.  It does not
use a terminal plot as evidence for a root, does not replace the projected
rotational charge by one selected Fourier shell, and does not infer a result
for general three-dimensional Navier--Stokes solutions.

The producer and independent numerical certificates are separate from this
analytic audit.  The producer checks finite algebra and scaling bookkeeping;
only the independent program checks representative finite ODE truncations.
The proof below is the reason the asymptotic claims hold.

## 2. Shifted Rudin--Shapiro moments

For

\[
 r_j=M+j,\qquad 0\le j<M,
\]

direct subtraction of square sums gives

\[
\begin{aligned}
 K_s
 &=\sum_{r=M}^{2M-1}r^2\\
 &=\frac{(2M-1)(2M)(4M-1)}6
 -\frac{(M-1)M(2M-1)}6\\
 &=\frac{M(2M-1)(7M-1)}6
 \sim\frac73M^3.
\end{aligned}
\]

With \(|w_j|=a\), \(K_v=a^2K_s\).  The target row has two entries per
carrier, so

\[
 \rho_0^2=2K_z^2a^2M.
\]

No sign or phase enters this identity.

## 3. Heat-weighted phase cancellation

Let

\[
 A_k(z)=\sum_{j=0}^k\varepsilon_jz^j,
 \qquad
 b_j=e^{-\kappa(M+j)^2x}.
\]

The checked RS input is

\[
 \max_{k<M}\|A_k\|_{L^\infty(\mathbb T)}\le C\sqrt M.
\]

Because \(b_j\) decreases,

\[
 \sum_{j=0}^{M-1}\varepsilon_jb_jz^j
 =b_{M-1}A_{M-1}+\sum_{k=0}^{M-2}(b_k-b_{k+1})A_k.
\]

The total coefficient on the right is

\[
 b_{M-1}+\sum_{k=0}^{M-2}(b_k-b_{k+1})=b_0.
\]

Therefore the heat-weighted polynomial is at most
\(C\sqrt M e^{-\kappa M^2x}\).  Multiplication by \(z^M\) does not change
its modulus.  Conjugate pairing contributes only the fixed factor
\(2|K_z|a\).  This proves

\[
 \|V_M(x)\|\le Ca\sqrt M e^{-\kappa M^2x}.
\]

Bernstein's inequality at degree below \(2M\) gives

\[
 \|\partial_\theta V_M(x)\|
 \le CaM^{3/2}e^{-\kappa M^2x}.
\]

The three required integrals are consequently

\[
 \int\|V_M\|\le CaM^{-3/2},
 \qquad
 \int\|V_M\|^2\le Ca^2M^{-1},
 \qquad
 \int\|\partial_\theta V_M\|\le CaM^{-1/2}.
\]

For the matching lower mixed-exposure scale, Abel summation with the
increasing weights \(1-e^{-\kappa(M+j)^2x}\) gives
\(\|V_M(x)-V_M(0)\|\le Ca\sqrt M\,M^2x\).  On a sufficiently short fixed
multiple of \([0,M^{-2}]\), both \(\|V_M(x)\|\) and \(\rho(x)\) therefore
remain fixed fractions of their launch values.  Consequently
\(\ell_\times\asymp M^{-2}\), not merely \(O(M^{-2})\).

The proof is uniform in the unequal heat weights.  It is not an assertion that
every arbitrary phase pattern has the same bound; it uses the RS prefix
property.

Parseval supplies the lower multiplier bound
\(\Omega_0\ge\rho_0\asymp a\sqrt M\).  Hence

\[
 \Omega_0\asymp a\sqrt M,
 \quad
 \chi_0\asymp1,
 \quad
 \Omega_0^2/K_v\asymp M^{-2},
\]

and the static coefficient is exactly of order \(M^{-8/3}\).

## 4. Exact row alignment

Set

\[
 G_M=\frac{i\operatorname{sgn}(K_z)}{\sqrt2}
 \sum_j\varepsilon_j(e_{r_j}+e_{-r_j}).
\]

There are \(2M\) coefficients of modulus \(1/\sqrt2\), so
\(\|G_M\|_2^2=M\).  Inserting the two row entries associated with each
carrier gives

\[
 P_0V_M(0)G_M=\sqrt2|K_z|aM.
\]

Thus

\[
 |P_0V_M(0)G_M|^2=2K_z^2a^2M^2=M\rho_0^2.
\]

This is equality in the target-row Cauchy--Schwarz bound.  Phase cancellation
reduces the global multiplier norm but does not reduce the aligned target row.

## 5. Positive-time exact root

Let \(\delta a=\gamma M^{3/2}\) and \(\tau_M=M^{-3}\).  On this interval,

\[
 |\delta|\int_0^{\tau_M}\|V_M(x)\|dx
 \le C\gamma M^{-1}.
\]

The heat change of the carrier block is also \(O(M^2\tau_M)=O(M^{-1})\).
Let \(U_M\) be the exact evolution operator.  The target-to-target matrix
element satisfies

\[
 A_M=P_0U_M(\tau_M,0)e_0=1+O_\gamma(M^{-1}),
\]

while contraction and Duhamel give

\[
 |B_M|=|P_0U_M(\tau_M,0)G_M|
 \le |\delta|\int_0^{\tau_M}\|V_M(x)\|dx\,\|G_M\|_2
 \le C\gamma M^{-1}\sqrt M
 =C\gamma M^{-1/2}.
\]

For large \(M\), \(A_M\ne0\).  The choice

\[
 \zeta_M=-B_M/A_M
\]

therefore makes the target coefficient at \(\tau_M\) exactly zero.  Scaling
the whole initial vector to norm \(\sqrt M\) preserves the zero.  Since
\(|\zeta_M|=O(M^{-1/2})\), the scaling factor is
\(1+O(M^{-2})\).

The row at \(\tau_M\) differs from the aligned launch row by:

1. an \(O(M^{-1})\) relative heat change;
2. an \(O(M^{-1})\) relative coupling exposure;
3. an \(O(M^{-1})\) relative contribution from the target adjustment after
   it is propagated.

It follows that

\[
 P_0V_M(\tau_M)F_M(\tau_M)
 =\sqrt2|K_z|aM[1+O_\gamma(M^{-1})].
\]

In particular, the coupling-state error has norm
\(O_\gamma(M^{-1})\|F_M(0)\|_2=O_\gamma(M^{-1/2})\).  Applying the target
row of norm \(O(a\sqrt M)\) gives an absolute \(O_\gamma(a)\) error, so no
factor of \(\sqrt M\) is missing relative to the \(\asymp aM\) launch row.

At the target root, the diagonal target term vanishes, so the derivative is
\(\delta P_0V_MF_M\ne0\).  The root is interior and simple.

The construction uses one complex scalar launch adjustment, not an
unspecified finite-dimensional implicit-function radius.  It is exact because
the evolution is complex-linear.

## 6. Weighted active enstrophy

Let \(R e_r=re_r\).  Differentiating \(RF\), using commutation with the
diagonal diffusion and skew-adjointness of \(V_M\), gives

\[
 \frac d{dx}\|RF\|_2
 \le|\delta|\|[R,V_M]\|\|F\|_2.
\]

The commutator norm is the derivative-multiplier norm.  Therefore

\[
\begin{aligned}
 \sup_x\|RF(x)\|_2
 &\le CM^{3/2}
 +|\delta|\sqrt M\,CaM^{-1/2}\\
 &\le C_\gamma M^{3/2}.
\end{aligned}
\]

Restoring physical frequencies gives active enstrophy at most
\(C_\gamma S^2q^2M^3\).  The shear enstrophy is at most
\(CP^2a^2q^2M^3\).

The target adjustment has lattice index zero.  Therefore its contribution to
the active \(r^2\)-moment is exactly zero and

\[
 K_f=c_M^2K_s=K_s[1+O(M^{-2})].
\]

Choosing \(S^2K_f=3P^2K_v\) is an exact amplitude choice, not an asymptotic
substitution.

The low \(z\)-independent background has enstrophy comparable to \(q^2E_M\)
throughout the fixed interval.  It gives the lower bound for \(Y\); the
weighted estimates give the upper bound.  Hence

\[
 Y(t)\asymp_{I,\gamma}q^2E_M,
 \qquad
 \mathcal R_Y(I)=O_{I,\gamma}(1).
\]

The background is included in the inherited data size
\(D_M=\|u_M(0)\|_2^2+\|\omega_M(0)\|_2^2\).  There is no unpaid floor.

## 7. Complete rotational charge

For the exact triangular velocity,

\[
 \mathbb P(u\times\omega)=(-vf_z,0,0).
\]

All modes of \(vf_z\) retain \(z\)-frequency \(\pm K_z\), so

\[
 \|\mathbb P(u\times\omega)\|_{\dot H^{-1}}
 \le C_{K_z}\|v\|_\infty\|f_z\|_2.
\]

Active contraction gives \(\|f_z\|_2^2\le CS^2M\).  Fix one admissible
integer \(q=q_0\), independent of \(M\).  Physical time is \(t=x/q^2\), and
the thermal multiplier estimate gives

\[
 \int_I\|v(t)\|_\infty^2dt
 \le C\frac{P^2a^2}{q^2M}.
\]

Dividing by the background lower bound for \(Y\) yields

\[
 \frac1{|I|}\int_I
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y(t)}dt
 \le C_I\frac{P^2S^2a^2}{q^4E_M}.
\]

The exact amplitude balance and \(E_M=4P^2K_v\) give

\[
 \frac{P^2S^2a^2}{q^4E_M}
 =\frac34\frac{P^2a^2}{q^4K_f}
 \le C\frac{P^2a^2}{q^4K_s}.
\]

Since \(P/q^2=\delta\) and \(K_s\asymp M^3\), this becomes

\[
 C_I\frac{\delta^2a^2}{M^3}=C_I\gamma^2.
\]

This estimate contains all Fourier frequencies.  The large instantaneous
target Lamb coefficient is diluted by the physical pulse duration
\(O((qM)^{-2})\); it has not been deleted.

Together with the enstrophy contrast,

\[
 \Lambda_1(I;u_M)\le C_{I,\gamma}(\nu^2+\gamma^2).
\]

## 8. Normalized lower ledger

The exact interior root occurs at
\(t_M=q^{-2}M^{-3}\in(0,T)\) for all sufficiently large \(M\), because
\(q=q_0\) is fixed.  It contributes

\[
 \mathcal J_{\rm all}\ge
 c\frac{S^2P^2a^2M^2}{q^2E_M}.
\]

The exact amplitude balance gives \(S^2/E_M=3/(4K_f)\), and hence

\[
 \mathcal J_{\rm all}
 \ge c\frac{P^2a^2M^2}{q^2K_f}
 \ge c\frac{P^2a^2}{q^2M}.
\]

Since \(D_M\le Cq^2P^2a^2M^3\),

\[
 \frac{\mathcal J_{\rm all}}{D_M^{1/3}}
 \ge c(\delta a)^{4/3}M^{-2}
 =c\gamma^{4/3}.
\]

Division by the upper bound for \(\Lambda_1\) proves

\[
 \liminf_M
 \frac{\mathcal J_{{\rm all},M}}
 {D_M^{1/3}\Lambda_1(I;u_M)}
 \ge c\frac{\gamma^{4/3}}{\nu^2+\gamma^2}>0.
\]

Every inequality has the correct direction for a lower result: the atom uses
an upper bound for root-time enstrophy, \(D^{1/3}\) uses an upper bound for
the data size, and \(\Lambda_1\) uses an upper bound for both contrast and
charge.

## 9. Upper/lower match

The R0.72C geometric factors satisfy

\[
 \frac M{K_s}\asymp M^{-2},\qquad
 \chi_0\asymp1,\qquad
 (\Omega_0^2/K_v)^{1/3}\asymp M^{-2/3}.
\]

The actual mixed exposure is \(O(M^{-2})\).  With
\(\eta\asymp\gamma M^2\), the upper ledger is \(O_\gamma(1)\), while the
lower ledger is positive.  This is scale sharpness, not an exact universal
constant.

## 10. Scope verdict

The following claims pass:

1. heat-stable shifted RS flatness;
2. an exact simple positive-time target root;
3. a noncollapsing root slope;
4. bounded fixed-interval enstrophy contrast;
5. bounded full-frequency rotational charge;
6. a nonvanishing normalized complete root ledger;
7. order-one upper/lower scale matching.

The following claims are excluded from the release:

1. divergence of the normalized ledger;
2. failure or proof of a universal \(D^{1/3}\Lambda_1\) payment;
3. a continuation criterion;
4. general three-dimensional regularity or blow-up;
5. novelty claims beyond the bounded literature audit.

Within these boundaries, the analytic audit passes.
