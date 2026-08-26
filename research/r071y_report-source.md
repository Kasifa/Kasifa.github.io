# R0.71Y report source -- operator-sampling suppression for growing root families

**Date:** 2026-08-26  
**Status:** analytic theorem for the fixed-target triangular Fourier-lattice
class under explicit data and root-time enstrophy floors. The result closes
the prescribed-root gain, and every at-most-linear total-root gain, at
uniformly bounded observation coupling. It does not prove a universal
Navier--Stokes endpoint estimate or an all-root count.

## 0. Direct decision

R0.71X left one perturbative branch open: allow the number \(N\) of exact
target roots and the response dimension to grow, and hope that the atom sum
overwhelms the \(D^{1/3}\) data payment. A quantitative ECT inverse and an
\(N\)-dependent implicit-function radius appeared to be the next
prerequisites.

R0.71Y also corrects one comparison in the R0.71X route matrix. Since the
operator norm is measured only for \(x\ge A_0>0\), its lower Fourier bound is
by the heat-weighted norm
\(\|z_le^{-\nu d^2r_l^2A_0}\|_2\), not by the unweighted \(\|z\|_2\).
The unweighted upper bound used below is valid. The R0.71X fixed-dimensional
endpoint theorem did not use the incorrect lower comparison.

The ECT inverse is not a prerequisite for the upper bound. At an exact target
root the diagonal heat term vanishes in that coordinate. The target slope is
one coordinate of the shear multiplication operator applied to the active
scalar. The full triangular advection--diffusion evolution is an exact
\(\ell^2\) contraction, so the active scalar costs only the square root of
the number of launched carrier phases. Summing \(N\) root slopes costs at
most \(N(2N+1)\), whereas \(2N+1\) distinct unit carrier phases have the
unavoidable lattice cost

\[
 K_{s,N}\ge \sum_{j=1}^{2N+1}j^2\asymp N^3.
\]

After optimizing the scalar/shear amplitude ratio, the sum over the selected
\(N\) exact roots satisfies

\[
 \boxed{
 \frac{\mathcal J_N^{\rm sel}}
 {D_N^{1/3}\Lambda_1(I;u_N)}
 \le C\nu^{-2}\frac{\delta_{\mathrm{obs},N}^{4/3}}{N}.}
 \tag{0.1}
\]

Here

\[
 \delta_{\mathrm{obs},N}
 =\frac{P_N}{q_N^2}
 \sup_{x\ge A_0}\|V_{z_N}(x)\|_{\ell^2\to\ell^2}
\]

is the actual root-layer multiplication-operator coupling. The constant in
(0.1) is independent of \(q_N,N,S_N,P_N\), the interpolation coefficients,
the ECT determinant, and the inverse Jacobian. It may depend on the fixed
target multiplier, viscosity, modulus \(d\), interval, and the two stated
enstrophy-floor constants.

Consequently every family with uniformly bounded
\(\delta_{\mathrm{obs},N}\) has a vanishing normalized **selected** atom sum as
\(N\to\infty\). A nonvanishing endpoint ratio requires
\(\delta_{\mathrm{obs},N}\gtrsim N^{3/4}\); a divergent ratio requires
\(\delta_{\mathrm{obs},N}/N^{3/4}\to\infty\) along the divergent subsequence.
Growing dimension therefore does not rescue the prescribed-root part of the
uniformly small-coupling R0.71W mechanism. Corollary 4.4 quantifies what an
additional-root escape would still have to do.

The symbol is deliberately \(\delta_{\mathrm{obs},N}\), not an IFT radius.
For a target map launched at \(x=0\), the Dyson series also depends on

\[
 \eta_{\mathrm{Dyson},N}
 =\frac{P_N}{q_N^2}\int_0^{\tau_N}\|V_{z_N}(x)\|\,dx,
 \tag{0.2}
\]

and a quantitative IFT certificate must also pay the inverse Jacobian and
the derivative-Lipschitz constant. They are not equivalent in both
directions. For fixed \(A_0>0\), Lemma 1.1 proves the dimension-free one-way
bound
\(\delta_{\mathrm{obs},N}\le C_{A_0,\nu,d}\eta_{\mathrm{Dyson},N}\).
Thus the existing uniformly small Dyson/IFT corridor is contained in the
bounded-observation corridor closed below. The theorem itself needs no IFT:
it is conditional only on exact roots.

## 1. Exact Fourier-lattice setting

Fix the target \(k_*=(K_y,K_z)\), \(K_z\ne0\), a modulus \(d\ge1\), and a
scaled left time \(A_0>0\). For a given root count \(N\ge1\), put

\[
 M=2N+1
\]

and choose pairwise distinct positive integers \(r_1,\ldots,r_M\). The
physical carrier frequencies are \(n_{l,q}=dr_lq\). The positive-\(K_z\)
active scalar sector is normalized by

\[
 \widehat f^{\rm act}(K_y+dqr,K_z,t)
 =S F_r(x),\qquad x=q^2(t-\sigma_q),
 \tag{1.1}
\]

where the launch vector has \(M\) nonzero coefficients of unit modulus:

\[
 \|F(0)\|_{\ell^2}^2=M.
 \tag{1.2}
\]

The normalized real shear coefficients are \(z_1,\ldots,z_M\), its physical
amplitude is \(P\), and

\[
 K_{s,N}=\sum_{l=1}^M r_l^2,
 \qquad
 K_{v,N}=\sum_{l=1}^M r_l^2|z_l|^2.
 \tag{1.3}
\]

The exact scaled evolution is

\[
 \partial_xF=D_qF+\delta V_z(x)F,
 \qquad \delta=\frac{P}{q^2},
 \tag{1.4}
\]

with diagonal nonpositive \(D_q\) and

\[
 (V_z(x)F)_r
 =-iK_z\sum_{l=1}^M z_l e^{-\nu d^2r_l^2x}
 \bigl(F_{r-r_l}+F_{r+r_l}\bigr).
 \tag{1.5}
\]

Let

\[
 \Omega_N:=\sup_{x\ge A_0}
 \|V_z(x)\|_{\ell^2\to\ell^2},
 \qquad
 \delta_{\mathrm{obs},N}:=\frac{P}{q^2}\Omega_N.
 \tag{1.6}
\]

Also define the launch-to-last-root Dyson size

\[
 \eta_{\mathrm{Dyson},N}
 :=\frac{P}{q^2}\int_0^{\tau_N}
 \|V_z(x)\|_{\ell^2\to\ell^2}\,dx.
 \tag{1.6a}
\]

### Lemma 1.1 -- one-way Dyson-to-observation control

For fixed \(A_0,\nu,d>0\), there is a constant independent of \(N,q,z\)
such that

\[
 \boxed{
 \delta_{\mathrm{obs},N}
 \le C_{A_0,\nu,d}\eta_{\mathrm{Dyson},N}.}
 \tag{1.6b}
\]

Put \(\kappa=\nu d^2\) and

\[
 w(s)=\left(\sum_l|z_l|^2e^{-2\kappa r_l^2s}\right)^{1/2}.
\]

Parseval and the multiplier representation give
\(\|V_z(s)\|\ge c|K_z|w(s)\). Conversely, for \(x\ge A_0\),

\[
\begin{aligned}
 \|V_z(x)\|
 &\le2|K_z|\sum_l|z_l|e^{-\kappa r_l^2x}\\
 &\le2|K_z|
 \left(\sum_l e^{-\kappa r_l^2x}\right)^{1/2}w(x/2)\\
 &\le C_{\kappa,A_0}|K_z|w(A_0/2).
\end{aligned}
 \tag{1.6c}
\]

The function \(w\) is decreasing, so

\[
 \eta_{\mathrm{Dyson},N}
 \ge c\frac{P}{q^2}|K_z|
 \int_0^{A_0/2}w(s)\,ds
 \ge c\frac{P}{q^2}|K_z|\frac{A_0}{2}w(A_0/2),
\]

which proves (1.6b). The reverse comparison is false:
\(z_R=e^{\nu d^2R^2A_0}\) keeps the observation-layer coefficient at order
one while the pre-observation Dyson integral grows exponentially after its
\(R^{-2}\) heat-time factor. If \(A_0=A_{0,N}\to0\), the constant in
(1.6b) degenerates; that short-pulse boundary is not closed here.

Suppose the exact target coordinate has \(N\) distinct roots

\[
 F_0(\tau_m)=0,
 \qquad A_0\le\tau_1<\cdots<\tau_N.
 \tag{1.7}
\]

No interpolation formula, simplicity lower bound, or implicit-function
radius is assumed below. Multiple roots are allowed; they only lower the
left side because their target slope vanishes.

## 2. Exact contraction and root-slope estimate

### Lemma 2.1 -- dimension-free active-sector contraction

For real \(z_l\), every shift sum \(T_{r_l}+T_{-r_l}\) is self-adjoint on
\(\ell^2(\mathbb Z)\). Hence \(V_z(x)\) is skew-adjoint. Since \(D_q\) is
self-adjoint and nonpositive,

\[
 \frac12\frac d{dx}\|F(x)\|_2^2
 =\langle D_qF,F\rangle\le0.
 \tag{2.1}
\]

Therefore

\[
 \|F(x)\|_2\le\|F(0)\|_2=\sqrt M
 \qquad(x\ge0).
 \tag{2.2}
\]

This exact passive-scalar energy identity contains no exponential Gronwall
factor and no coefficient-ball or inverse-Jacobian constant.

### Lemma 2.2 -- root slope is operator controlled

Because \(D_q\) is diagonal, (1.7) implies

\[
 (D_qF(\tau_m))_0=0.
\]

Equations (1.4), (1.6), and (2.2) give

\[
 |\partial_xF_0(\tau_m)|
 \le \frac{P}{q^2}\Omega_N\sqrt M
 =\delta_{\mathrm{obs},N}\sqrt M.
 \tag{2.3}
\]

Restoring physical time and scalar amplitude,

\[
 \partial_t\widehat f(k_*,t_{m,q})
 =SP\,h_m,
 \qquad
 h_m:=P_0V_z(\tau_m)F(\tau_m),
 \tag{2.4}
\]

and \(|h_m|\le\Omega_N\sqrt M\). Thus the exact nonlinear sampled-slope
mass

\[
 G_N^{\rm ex}:=\sum_{m=1}^N|h_m|^2
\]

satisfies

\[
 \boxed{G_N^{\rm ex}\le NM\Omega_N^2,}
 \qquad
 \sum_{m=1}^N
 |\partial_t\widehat f(k_*,t_{m,q})|^2
 \le S^2P^2G_N^{\rm ex}.
 \tag{2.5}
\]

This \(G_N^{\rm ex}\) belongs to the exact nonlinear triangular evolution. It
is not the limiting first-Dyson quantity
\(\sum_m|\Gamma_N'(\tau_m)|^2\) used later in Section 5.

## 3. Data and root-time floors

Put

\[
 E_N=S^2K_{s,N}+P^2K_{v,N}.
 \tag{3.1}
\]

The theorem uses the same two explicit hypotheses as the growing-root ledger
in R0.71X. There are constants \(c_D,c_Y>0\), independent of
\(q,N,S,P,z\), such that

\[
 D_N\ge c_Dq^2E_N
 \tag{3.2}
\]

and, at every counted root,

\[
 Y_N(t_{m,q})\ge c_Yq^2E_N.
 \tag{3.3}
\]

In the R0.71W architecture these inequalities are enforced by active and
shear launch energy together with a decoupled persistent background matched
to the full high-frequency enstrophy. For growing \(N\), that background
must be matched to the full \(K_{s,N},K_{v,N}\) cost; retaining the old
fixed-\(N\) background is not admissible.

One explicit admissible scaling is

\[
 B_N=\frac{b_0q}{Q}
 \left(S^2K_{s,N}+P^2K_{v,N}\right)^{1/2},
 \tag{3.3a}
\]

for the fixed low \(z\)-independent background frequency \(Q\). Its
enstrophy is comparable to \(q^2E_N\) throughout the fixed interval, its
full launch cost is included in \(D_N\), and it enters neither the target
response nor the triangular Lamb term.

Let \(C_T\) absorb the fixed conjugate-pair, annular multiplier, and target
eigenshell constants in the atom normalization. From (2.5) and (3.3),

\[
 \mathcal J_N^{\rm sel}
 \le
 C_T\frac{NM S^2P^2\Omega_N^2}{q^2E_N}.
 \tag{3.4}
\]

## 4. Optimized operator-sampling theorem

### Theorem 4.1 -- growing-root suppression

Under (1.1)--(1.7) and (3.2)--(3.3),

\[
 \frac{\mathcal J_N^{\rm sel}}{D_N^{1/3}}
 \le C_0\frac{NM}{K_{s,N}}
 \delta_{\mathrm{obs},N}^{4/3}
 \left(\frac{\Omega_N^2}{K_{v,N}}\right)^{1/3},
 \tag{4.1}
\]

where \(C_0\) depends only on \(C_T,c_D,c_Y\). If \(K_{v,N}=0\), then the
target slope and the left side vanish, so (4.1) is interpreted by continuity.

#### Proof

Equations (3.2) and (3.4) imply

\[
 \frac{\mathcal J_N^{\rm sel}}{D_N^{1/3}}
 \le C
 \frac{NM S^2P^2\Omega_N^2}
 {q^{8/3}(S^2K_{s,N}+P^2K_{v,N})^{4/3}}.
 \tag{4.2}
\]

For

\[
 u=\frac{S^2K_{s,N}}{P^2K_{v,N}},
\]

the amplitude factor in (4.2) is

\[
 \frac{u}{(1+u)^{4/3}}
 \left(\frac{P}{q^2}\right)^{4/3}
 \frac{\Omega_N^2}
 {K_{s,N}K_{v,N}^{1/3}}.
 \tag{4.3}
\]

The scalar function \(u(1+u)^{-4/3}\) is maximal at \(u=3\), with value
\(3/4^{4/3}\). Since

\[
 \left(\frac{P}{q^2}\right)^{4/3}
 \frac{\Omega_N^2}{K_{v,N}^{1/3}}
 =\delta_{\mathrm{obs},N}^{4/3}
 \left(\frac{\Omega_N^2}{K_{v,N}}\right)^{1/3},
\]

(4.1) follows. \(\square\)

### Lemma 4.2 -- Fourier multiplier versus weighted shear energy

The shift representation (1.5) gives

\[
 \Omega_N\le2|K_z|\sum_{l=1}^M|z_l|.
\]

Weighted Cauchy--Schwarz and distinct positive integer \(r_l\) give

\[
 \sum_{l=1}^M|z_l|
 \le K_{v,N}^{1/2}
 \left(\sum_{l=1}^M\frac1{r_l^2}\right)^{1/2}
 \le\frac\pi{\sqrt6}K_{v,N}^{1/2}.
\]

Consequently

\[
 \boxed{
 \frac{\Omega_N^2}{K_{v,N}}
 \le\frac{2\pi^2K_z^2}{3}.}
 \tag{4.4}
\]

No lower comparison is used. Heat damping or phase cancellation can make
\(\Omega_N^2/K_{v,N}\) much smaller, which only strengthens (4.1).

### Lemma 4.3 -- exact lattice-count cost

Among \(M=2N+1\) distinct positive integers, the sum of squares is minimized
by \(1,\ldots,M\). Hence

\[
 K_{s,N}\ge\frac{M(M+1)(2M+1)}6
\]

and

\[
 \boxed{
 \frac{NM}{K_{s,N}}
 \le\frac{6N}{(M+1)(2M+1)}
 \le\frac{3}{4N}.}
 \tag{4.5}
\]

Combining (4.1), (4.4), and (4.5) proves

\[
 \boxed{
 \frac{\mathcal J_N^{\rm sel}}{D_N^{1/3}}
 \le C_1\frac{\delta_{\mathrm{obs},N}^{4/3}}N.}
 \tag{4.6}
\]

Finally,

\[
 \Lambda_1(I;u)
 =\mathcal R_Y(I)
 \left[\nu^2+\frac1{|I|}\int_I
 \frac{\|\mathbb P(u\times\omega)\|_{\dot H^{-1}}^2}{Y(t)}\,dt
 \right]\ge\nu^2.
\]

Therefore (0.1) follows from (4.6) without an upper estimate on the
full-frequency rotational charge.

### Corollary 4.4 -- arbitrary finite root count

The proof did not use \(M=2N+1\) until the last lattice comparison. If a
system with \(M\) unit-modulus launched carriers has any finite collection
of \(R\) exact roots in the observation layer, then

\[
 \frac{\mathcal J_R}
 {D^{1/3}\Lambda_1}
 \le
 C\nu^{-2}\frac{RM}{K_s}
 \delta_{\mathrm{obs}}^{4/3}
 \left(\frac{\Omega^2}{K_v}\right)^{1/3}.
 \tag{4.7}
\]

For distinct positive integer carriers,
\(K_s\ge M(M+1)(2M+1)/6\), so

\[
 \boxed{
 \frac{\mathcal J_R}
 {D^{1/3}\Lambda_1}
 \le C\nu^{-2}\frac{R}{M^2}
 \delta_{\mathrm{obs}}^{4/3}.}
 \tag{4.8}
\]

Thus a total root set of size \(R=O(M)\) has the same \(M^{-1}\)
suppression. At bounded observation coupling, an unaccounted-for root
proliferation would need at least quadratic order \(R\gtrsim M^2\) merely to
avoid this decay. R0.71Y does not prove an all-root count, so such quadratic
proliferation is recorded as an explicit remaining escape route.

## 5. Exact separated-root observability

The exact nonlinear slope bound can be sharpened when the sampled roots are
separated. Put \(b=2\nu d^2\) and

\[
 W_N^2=\sum_l|z_l|^2e^{-b r_l^2A_0},
 \qquad
 h_N=\min\{\tau_1-A_0,\tau_m-\tau_{m-1}:2\le m\le N\}.
 \tag{5.1}
\]

When \(A_0<\tau_1<\cdots<\tau_N\), \(h_N>0\) and
\(\tau_m\ge A_0+mh_N\). At an exact root, (1.5) and Cauchy--Schwarz give

\[
\begin{aligned}
 |h_m|^2
 &=|P_0V_z(\tau_m)F(\tau_m)|^2\\
 &\le2|K_z|^2\|F(\tau_m)\|_2^2
 \sum_l|z_l|^2e^{-b r_l^2\tau_m}\\
 &\le2|K_z|^2M
 \sum_l|z_l|^2e^{-b r_l^2\tau_m}.
\end{aligned}
 \tag{5.2}
\]

Summing the geometric heat tail yields

\[
\begin{aligned}
 G_N^{\rm ex}
 &\le2|K_z|^2M
 \sum_l |z_l|^2e^{-b r_l^2A_0}
 \sum_{m=1}^Ne^{-b r_l^2(\tau_m-A_0)}\\
 &\le2|K_z|^2M
 \sum_l\frac{|z_l|^2e^{-b r_l^2A_0}}
 {e^{bh_Nr_l^2}-1}\\
 &\le\frac{2|K_z|^2M}{bh_N}W_N^2.
\end{aligned}
 \tag{5.3}
\]

The normalized-Haar Fourier multiplier has
\(\Omega_N\ge c_{\rm mult}W_N\), with
\(c_{\rm mult}=\sqrt2|K_z|\). Repeating the exact amplitude optimization in
Theorem 4.1 gives

\[
 \boxed{
 \frac{\mathcal J_N^{\rm sel}}
 {D_N^{1/3}\Lambda_1}
 \le
 C\frac{\delta_{\mathrm{obs},N}^{4/3}M}
 {bh_NK_{s,N}}
 \left(\frac{W_N^2}{K_{v,N}}\right)^{1/3}
 \le
 C\frac{\delta_{\mathrm{obs},N}^{4/3}}
 {h_NN^2}.}
 \tag{5.4}
\]

Thus fixed scaled root spacing gives \(O(N^{-2})\), while \(N\) roots
quasi-uniformly filling a fixed scaled interval,
\(h_N\asymp N^{-1}\), recover the exact \(O(N^{-1})\) suppression. This is
an exact finite-\(q\) nonlinear estimate; no \(C^1\) transfer from the
limiting response is used.

Before taking a minimum gap, define the exact weighted sampling kernel

\[
 \mathscr S_N
 :=\frac1{W_N^2}
 \sum_l|z_l|^2e^{-b r_l^2A_0}
 \sum_{m=1}^Ne^{-b r_l^2(\tau_m-A_0)}.
 \tag{5.5}
\]

Then \(G_N^{\rm ex}\le2|K_z|^2MW_N^2\mathscr S_N\). This form remains valid
when \(\tau_1=A_0\); only the convenient \(h_N^{-1}\) corollary degenerates.

### Why ECT conditioning cannot rescue this branch

For each fixed \(N\), the R0.71W limiting response coefficients solve

\[
 \Gamma_N(x)=K_z\sum_{l=1}^{N+1}c_l
 \frac{1-e^{-b_lx}}{b_l},
 \qquad
 \Gamma_N(\tau_m)=0.
 \tag{5.6}
\]

ECT theory gives finite-\(N\) invertibility and simplicity but no uniform
smallest-singular-value estimate. Coefficient norms and inverse Jacobians may
deteriorate rapidly with \(N\). Theorem 4.1 is deliberately upstream of that
issue:

* if the interpolation has no exact roots, it supplies no counterfamily;
* if it has exact roots with large coefficients, \(K_{v,N}\) and the
  operator factor in (4.1) record their cost;
* an \(N\)-dependent IFT certificate and
  \(\delta_{\mathrm{obs},N}\) must be recorded separately, while (1.6b)
  places every bounded Dyson corridor inside the theorem; and
* even a hypothetical perfect ECT inverse cannot defeat the factor \(1/N\)
  while \(\delta_{\mathrm{obs},N}\) remains bounded.

Quantitative ECT conditioning remains mathematically relevant to constructing
the roots, but it cannot reverse this payment.

### Equal-grid determinant squeeze

The physical rates \(b_l=br_l^2\) permit one explicit growing-\(N\)
conditioning estimate. Take equally spaced nodes \(\tau_m=mh\), set
\(x_l=e^{-bhr_l^2}\), and use the \(N\) unknown real columns
\(l=2,\ldots,N+1\). Their interpolation matrix is

\[
 \mathsf M_{m,l}
 =\frac{1-x_l^m}{br_l^2}.
 \tag{5.7}
\]

The geometric identity \(1-x^m=(1-x)\sum_{k=0}^{m-1}x^k\) gives the exact
factorization

\[
 \mathsf M=\mathsf U\mathsf V\mathsf D,
 \qquad
 \mathsf V_{k,l}=x_l^{k-1},
 \qquad
 \mathsf D_{l,l}=\frac{1-x_l}{br_l^2},
 \tag{5.8}
\]

where \(\mathsf U\) is the unit lower cumulative-sum matrix. Hence

\[
 |\det\mathsf M|
 =b^{-N}\prod_{l=2}^{N+1}\frac{1-x_l}{r_l^2}
 \prod_{2\le i<j\le N+1}|x_i-x_j|.
 \tag{5.9}
\]

Since \((1-x_l)/(br_l^2)\le h\) and
\(|x_i-x_j|\le bh\,r_{\max}^2\),

\[
 |\det\mathsf M|
 \le h^N(bh\,r_{\max}^2)^{N(N-1)/2}.
\]

The product of singular values then yields

\[
 \boxed{
 \|\mathsf M^{-1}\|_2
 \ge h^{-1}(bh\,r_{\max}^2)^{-(N-1)/2}.}
 \tag{5.10}
\]

For the canonical \(r_l=l\), a nonvanishing bounded-coupling ratio in (5.4)
requires \(hN^2\lesssim\delta_{\mathrm{obs},N}^{4/3}\). If
\(\delta_{\mathrm{obs},N}\to0\), then \(bhN^2\to0\), and (5.10) forces at
least superalgebraic inverse growth. This is a rigorous
separation/conditioning squeeze. It does not by itself upper-bound the true
nonlinear branch radius: such a conclusion would also require the forcing
direction and second-derivative/Lipschitz constants in the quantitative IFT.

## 6. Exact consequence and route boundary

Equation (4.6) implies:

1. if \(\sup_N\delta_{\mathrm{obs},N}<\infty\), then
   \(\mathcal J_N^{\rm sel}/(D_N^{1/3}\Lambda_1)\to0\);
2. if the normalized atom ratio stays bounded below by a positive constant,
   then \(\delta_{\mathrm{obs},N}\gtrsim N^{3/4}\); and
3. if the normalized atom ratio diverges, then
   \(\delta_{\mathrm{obs},N}/N^{3/4}\to\infty\) along that subsequence.

The last two alternatives lie outside every fixed perturbative operator ball.
They do not prove that a strong-coupling family exists.

## 7. What remains open

1. **Enstrophy floors.** The theorem assumes (3.2)--(3.3), with the
   persistent background charged at the full growing-dimensional cost. A
   floor-free family with large enstrophy variation requires a separate use
   of the complete \(\mathcal R_Y\) factor.
2. **Unit carrier phases.** The \(N^{-1}\) corollary uses all \(M=2N+1\)
   launched carrier coefficients at unit modulus, as in R0.71W. Arbitrarily
   weighted or sparse phase families require their own rank and sampling
   cost.
3. **Fixed target and one-dimensional shear lattice.** A varying target,
   domain, multiplier, or multidimensional carrier geometry changes the atom
   normalization and is not covered.
4. **Strong coupling.** The theorem identifies the necessary scale
   \(\delta_{\mathrm{obs},N}\gtrsim N^{3/4}\) but supplies neither root
   persistence nor nonlinear charge control there. The Bessel-root route
   recorded in R0.71X remains a separate nonperturbative candidate.
5. **IFT versus observation coupling.** Bounded
   \(\delta_{\mathrm{obs},N}\) is not a sufficient condition for the
   launch-to-root implicit construction. The one-way bound (1.6b) shows that
   the existing small-Dyson proof cannot escape the theorem when \(A_0\) is
   fixed. Any proposal with growing observation coupling must be audited as
   an observation-layer strong-coupling or \(A_{0,N}\to0\) short-pulse
   mechanism.
6. **Additional exact roots.** Equation (0.1) controls the selected
   prescribed roots. Corollary 4.4 controls any finite total set once its
   cardinality is known, but no growing-\(N\) no-spurious-root theorem is
   proved. At bounded coupling an escape through extra roots requires at
   least quadratic proliferation relative to the carrier dimension.

The next finite question is whether the complete
\(\mathcal R_Y\)-weighted ledger closes the floor-free case, or whether a
genuinely strong-coupling exact-root mechanism can survive the full nonlinear
charge.

## 8. Reproducibility boundary

The producer certificate evaluates the exact optimizer, lattice factor,
Fourier multiplier bound, and \(N^{-1}\) envelope using high-precision
decimal arithmetic. The independent certificate imports neither the
producer nor its JSON and separately checks finite shift matrices for
skew-adjointness, dissipativity, root-coordinate slope inequalities, and the
algebraic envelope in binary64.

Those computations audit finite algebra. The contraction, root-slope identity,
and theorem are analytic. No DNS, singularity computation, universal endpoint
estimate, continuation criterion, global-regularity theorem, novelty claim, or
priority claim is made.
