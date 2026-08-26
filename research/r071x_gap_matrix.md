# R0.71X gap matrix -- multiblock, multiple-root, and strong-coupling routes

**Date:** 2026-08-26

**Status:** independently audited route matrix.  The fixed-dimensional
endpoint statement is analytic.  The multiblock bounds below are propositions
only under their stated comparable-band or enstrophy-floor hypotheses; the
growing-root ledger is a conditional diagnostic, not a constructed family.
The final strong-coupling section is a conjectural next-stage candidate, not
an R0.71X result.

## 0. Direct decision

Within the fixed-target, fixed-macroscopic-window, uniformly small rescaled
coupling regime of R0.71W, the comparable-band selected-root estimate rules
out a divergent one-atom ratio

\[
 \frac{J_*}{D^{1/3}}\longrightarrow\infty
\]

for seed--shear imbalance and for any finite comparable-frequency block
collection satisfying the explicit launch and root-time enstrophy floors in
Section 1.  The same algebra gives a favourable upper envelope for growing
coherent blocks, but no exact growing-block root family is claimed.

The reason is not merely the special choice
\(\mathscr A_q=q^\alpha\). For one fixed target root, Fourier
Cauchy--Schwarz reduces the best possible gain to the collective shear
coupling raised to the power \(4/3\).  Parseval makes that collective scale a
lower bound for the multiplication-operator parameter in the comparable-band
case.  For noncomparable frequencies, the energy proxy and the exact operator
norm must be kept separate.

There are two qualifications.

* The endpoint itself is attained inside the existing IFT neighbourhood. If
  \(0<\delta_*<\delta_0\) is a sufficiently small fixed number and
  \(\mathscr A_q=\delta_*q^2\), then the exact roots persist and
  \(J_*/D^{1/3}\asymp\delta_*^{4/3}\). Thus the exponent \(1/3\) is an
  actual critical exponent of this family, not only a limit as
  \(\alpha\uparrow2\). This saturates but does not disprove an endpoint
  payment.
* A growing number \(N(q)\) of distinct root times is not closed by the
  selected-root argument. Existing ECT and IFT estimates are uniform in
  \(q\) only after \(N\), the interpolation nodes, and the phase family are
  fixed. A quantitative growing-dimensional ECT--IFT theorem is required
  before that route can be accepted or rejected.

A large-coupling Bessel-root construction may bypass the perturbative IFT,
but its enhanced-dissipation and full-frequency Lamb-charge estimates are
not proved. It is recorded only as a next-stage conjectural candidate in
Section 7.

## 1. One selected root: the collective-coupling obstruction

Let \(a(t)=\widehat f(K_y,K_z,t)\) be the coefficient of the fixed target
\(k_*=(K_y,K_z)\). At a target root, the diffusion term vanishes and the
triangular equation gives, up to a fixed Fourier-normalization constant,

\[
 a_t(t_*)=-iK_z\sum_n \widehat v(n,t_*)
 \widehat f(K_y-n,K_z,t_*).
 \tag{1.1}
\]

First suppose all active carrier frequencies are comparable to
\(\lambda\gg1\). Put

\[
 P_2^2=\sum_n|\widehat v(n,t_*)|^2,
 \qquad
 S_2^2=\sum_n|\widehat f(K_y-n,K_z,t_*)|^2.
 \tag{1.2}
\]

Fourier Cauchy--Schwarz gives

\[
 |a_t(t_*)|^2\le C_*P_2^2S_2^2.
 \tag{1.3}
\]

Assume that the launch seed and shear are supported in one band
\(c\lambda\le |n|,|K_y-n|\le C\lambda\), and retain the R0.71W root-time
enstrophy floor.  Heat decay of the shear and \(L^2\) contraction of the
active scalar then give the two lower bounds

\[
 Y(t_*)\ge c\lambda^2(P_2^2+S_2^2),
 \qquad
 D\ge c\lambda^2(P_2^2+S_2^2).
 \tag{1.4}
\]

No assertion that launch \(D\) and root-time \(Y\) are generally comparable
is needed.  Equations (1.3)--(1.4) imply that one target atom obeys

\[
 J_*(t_*)
 \lesssim
 \frac{P_2^2S_2^2}{\lambda^2(P_2^2+S_2^2)}.
 \tag{1.5}
\]

Writing \(r=S_2/P_2\) and
\(\eta=P_2/\lambda^2\), equations (1.4)--(1.5) give

\[
 \boxed{
 \frac{J_*(t_*)}{D^{1/3}}
 \lesssim
 \eta^{4/3}\frac{r^2}{(1+r^2)^{4/3}}.}
 \tag{1.6}
\]

The amplitude factor in (1.6) is maximal at \(r^2=3\), with value
\(3/4^{4/3}\). Thus seed--shear imbalance cannot improve the endpoint
power.

The scaled Fourier-lattice perturbation is multiplication by the shear after
division by \(\lambda^2\). Its operator norm satisfies

\[
 \frac{\|v\|_{L^\infty}}{\lambda^2}
 \ge c\frac{\|v\|_{L^2}}{\lambda^2}
 \asymp c\eta.
 \tag{1.7}
\]

Hence a selected-atom endpoint ratio can diverge only if the collective
operator coupling also diverges. This is incompatible with the fixed small
neighbourhood in Theorem 4.2 of R0.71W.

### 1.1 Noncomparable frequencies

For a general high-frequency shear with \(|n|\ge2|K_y|\), define

\[
 E_v=\sum_n n^2|\widehat v(n)|^2,
 \qquad
 R_v^{(*)}=\sum_n\frac{|\widehat v(n)|^2}{|K_y-n|^2},
 \tag{1.8}
\]

weighted Cauchy--Schwarz estimate in (1.1) yields

\[
 |a_t(t_*)|^2\le C_*E_fR_v^{(*)}.
 \tag{1.9}
\]

Here the weights \(|K_y-n|^{\pm2}\) are exact; under
\(|n|\ge2|K_y|\), they are comparable to \(n^{\pm2}\).  If, in addition,
the launch data and root-time floor control \(E_f+E_v\), optimization in
\(E_f/E_v\) gives the conditional estimate

\[
 \boxed{
 \frac{J_*(t_*)}{D^{1/3}}
 \lesssim \frac{R_v^{(*)}}{E_v^{1/3}}
 \asymp\left(\frac{R_v^3}{E_v}\right)^{1/3},}
 \tag{1.10}
\]

where \(R_v=\sum_n|\widehat v(n)|^2/n^2\) in the final comparison.

Equivalently, the effective weighted coupling is

\[
 \Theta_v:=\left(\frac{R_v^3}{E_v}\right)^{1/4},
 \qquad
 \frac{J_*}{D^{1/3}}\lesssim\Theta_v^{4/3}.
 \tag{1.11}
\]

If \(|n|\ge\lambda_{\min}\), then

\[
 \Theta_v\le
 \frac{\|v\|_{L^2}}{\lambda_{\min}^2}
 \le C\frac{\|v\|_{L^\infty}}{\lambda_{\min}^2}.
 \tag{1.12}
\]

Thus spreading the shear over several auxiliary scales does not evade the
same operator-coupling barrier for one selected root when the stated
launch-to-root enstrophy control is available.  Without that control,
(1.10) is a diagnostic rather than a theorem for an arbitrary multiscale
flow.

## 2. The endpoint is attained with a small fixed prefactor

Theorem 4.2 of R0.71W supplies constants \(\delta_0>0\) and \(q_0\) that are
independent of \(q\). Choose a fixed

\[
 0<\delta_*<\bar\delta<\delta_0
 \tag{2.1}
\]

small enough that the \(O(\delta_*)\) term in the target-slope expansion
cannot cancel any of the fixed nonzero values \(\Gamma'(\tau_m)\). Set

\[
 \mathscr A_q=\delta_*q^2.
 \tag{2.2}
\]

The same uniform IFT then gives exact simple prescribed roots for all large
\(q\). The estimates already proved in R0.71W, with \(1+\delta_*\) absorbed
into a fixed constant, give

\[
 \begin{aligned}
 D_q&\asymp \delta_*^2q^6,\\
 Y_q(t)&\asymp \delta_*^2q^6,\\
 J_{*,m,q}&\asymp \delta_*^2q^2,\\
 \frac1\ell\int_I
 \frac{\|L_q\|_{\dot H^{-1}}^2}{Y_q}\,dt
 &\lesssim\delta_*^2.
 \end{aligned}
 \tag{2.3}
\]

In particular,

\[
 \boxed{
 \frac{J_{*,m,q}}{D_q^{1/3}}
 \asymp\delta_*^{4/3}.}
 \tag{2.4}
\]

More generally, for \(\mathscr A_q=\delta_qq^2\) with
\(0<\delta_q\le\bar\delta\),

\[
 \frac{J_{*,m,q}}{D_q^{1/3}}
 \asymp\delta_q^{4/3}.
 \tag{2.5}
\]

Thus \(\delta_q\to0\) produces the subcritical families in R0.71W, while a
fixed small \(\delta_*\) gives exact endpoint saturation. The special choice
\(\mathscr A_q=q^2\) has \(\delta=1\) and may lie outside the IFT radius, but
this does not prevent endpoint scaling with a sufficiently small fixed
prefactor.

For a data power \(D^\beta\), (2.3) also gives

\[
 \frac{J_{*,m,q}}{D_q^\beta}
 \asymp
 \delta_*^{2-2\beta}q^{2-6\beta}.
 \tag{2.6}
\]

The ratio diverges for \(\beta<1/3\), remains of constant order for
\(\beta=1/3\), and vanishes for \(\beta>1/3\). This is an internal sharpness
statement for the exact triangular family, not a proof of a universal
\(D^{1/3}\) inequality.

## 3. Equal-block exponent ledger

Let the common carrier frequency, amplitude, and number of comparable
blocks have power laws

\[
 \lambda=q^\gamma,
 \qquad A=q^a,
 \qquad M=q^m.
 \tag{3.1}
\]

In the most favourable coherent selected-target envelope,

\[
 D\asymp MA^2\lambda^2,
 \qquad
 |a_t|\asymp MA^2,
 \qquad
 J_*\asymp\frac{MA^2}{\lambda^2}.
 \tag{3.2}
\]

Therefore

\[
 \frac{J_*}{D^{1/3}}
 \asymp
 \left(\frac{\sqrt M A}{\lambda^2}\right)^{4/3}
 =q^{\frac43(a+m/2-2\gamma)}.
 \tag{3.3}
\]

Parseval gives

\[
 \frac{\|v\|_{L^\infty}}{\lambda^2}
 \ge c\frac{\sqrt M A}{\lambda^2}.
 \tag{3.4}
\]

Thus the exponent in (3.3) is positive exactly when even the best possible
collective operator smallness fails. Random phases or flat trigonometric
polynomials may improve an \(\ell^1\) estimate to near \(\ell^2\), but they
cannot go below the Parseval lower bound in (3.4).

This is not an exact growing-\(M\) root construction.  In addition, a
one-dimensional integer shear lattice contains at most \(O(\lambda)\)
distinct frequencies in a fixed comparable band.  Therefore a power-law
ansatz \(M=q^m\), \(\lambda=q^\gamma\) must satisfy
\(m\le\gamma\) before any IFT or root-persistence issue is considered.

For one seed and one shear amplitude
\(S=q^s\), \(P=q^p\), the best exponent is obtained at \(s=p\). If
\(s\ne p\), then

\[
 \operatorname{pow}_q\left(\frac{J_*}{D^{1/3}}\right)
 \le \frac43(p-2\gamma),
 \tag{3.5}
\]

with strict loss away from the balanced scale. The current uniform IFT
requires \(p-2\gamma\le0\), with a sufficiently small coefficient at the
endpoint.

## 4. Failure matrix

| proposed modification | best favourable scaling or exact obstruction | decision in the current small-coupling route | missing lemma if pursued further |
|---|---|---|---|
| Seed much larger or smaller than shear | Equation (1.6); the amplitude factor is maximal at \(S_2^2=3P_2^2\). | No gain. Imbalance lowers \(J_*/D^{1/3}\). | None for the R0.71W-type family. |
| \(M(q)\) coherent comparable-frequency blocks feeding one target | \(D\sim MA^2\lambda^2\), \(J_*\sim MA^2/\lambda^2\), and the ratio is \((\sqrt M A/\lambda^2)^{4/3}\). | Divergence forces collective coupling out of the uniform IFT ball. | A nonperturbative large-coupling root theorem would be needed. |
| Incoherent block phases | The target slope is at most the coherent Cauchy--Schwarz value and is normally smaller by a square-root factor. | Worse than the coherent row. | None. |
| Flat or random shear polynomial | \(\|v\|_\infty\) can approach its \(L^2\) scale but cannot be smaller than it. | It can remove an artificial \(\ell^1\) loss, not the collective \(\sqrt M\) obstruction. | A certified flat-polynomial construction matters only for constants. |
| Growing number of fixed targets | A fixed compact multiplier on the normalized torus meets only finitely many lattice points. | \(M(q)\to\infty\) is impossible without changing the declared target. | A varying multiplier/domain theorem would change the problem and the atom weights. |
| Target frequency grows with \(q\) | The target is no longer the fixed compact \(T_*\); the \(\kappa_*^{-2}\rho_*^{-4}\) atom factors also change. | Outside the current statement. | A new scale-covariant target theorem. |
| Different seed and shear frequencies | To land directly on fixed \(k_*\), the seed frequency is \(k_*-n\), hence it is comparable to \(n\) at high frequency. | No independent frequency ratio in the first interaction. | A controlled higher-order frequency cascade would be a different mechanism. |
| Several auxiliary scales | Weighted estimate (1.10) replaces the one-band formula. | No selected-root gain while the weighted operator coupling remains small. | A nonperturbative multiscale root map if the coupling is large. |
| Larger decoupled background | It increases both \(Y\) and \(D\) while leaving the target slope unchanged. | Strictly worse. | None. |
| Smaller background | The initial active/shear enstrophy already remains in \(D\), while \(\mathcal R_Y(I)\) grows when the high modes decay. | No raw endpoint gain and a worse complete ledger. | A different persistent enstrophy-floor mechanism. |
| Background frequency grows | Persistence on a fixed macroscopic interval costs an exponential launch amplitude; \(Q=0\) supplies no enstrophy. | No gain on the fixed torus. | A new long-lived decoupled floor, if one exists. |
| Several modular cosets | Their generated additive group can acquire a small gcd and populate additional low modes. With one common large gcd they reduce to additional carriers in the same coset. | Either target isolation fails or the row reduces to the multiblock estimate. | A large-gcd/additive-isolation lemma plus a multi-output IFT. |
| Higher Dyson-order coherent paths | The factorial Dyson majorant absorbs the path multiplicity into the multiplication-operator norm; every extra order costs another collective coupling. | Worse for small coupling. | A large-coupling resonance theorem. |
| Fixed finite number of roots | It changes only a fixed constant in the sum. | Endpoint ratio remains bounded in the current family. | None after the fixed-dimensional constants are audited. |
| One root of high multiplicity | A root of order at least two has \(a_t=0\), hence its atom \(J_*\) is zero. | Cannot produce the desired atom. | None. |
| Split a high-multiplicity root at fixed response rates | R0.71V gives \(g'(t_m)=O(\Delta^{N-1})\), or \(O(\Delta^N)\) for a launch cluster. | The atom mass collapses faster than the root count grows. | A sharp quantitative ECT inequality if rates are also allowed to grow. |
| \(N(q)\) distinct roots with growing response dimension | Existing inverse matrices, coefficient norms, slope lower bounds, and IFT radii are only fixed-\(N\). | Open. This is the only small-coupling route in the table not closed by the selected-root estimate alone. | The quantitative gate in Section 5. |
| Root layers separated by macroscopic times | A heat mode active late in the interval requires an exponentially larger launch coefficient; a single unforced solution cannot be relaunched. | The launch data cost appears to overwhelm the gain. | A heat-observability lower bound for the interpolation Gramian would make this rigorous. |
| Strong-coupling Bessel roots | May create rapid exact roots with \(P/\lambda^2\to\infty\). | Outside the R0.71W uniform small-coupling IFT and not proved. | All four lemmas listed in Section 7. |

## 5. The two-parameter growing-root gate

The preceding selected-root estimate must not be used to dismiss a sum over
\(N(q)\) different times. Pointwise Cauchy--Schwarz can be paid repeatedly,
and a temporal sampling theorem is exactly where the R0.71U second-time row
enters.

For a growing interpolation family, introduce dimensionless coefficients

\[
 K_{s,N}=\sum_l r_l^2|A_l|^2,
 \qquad
 K_{v,N}=\sum_l r_l^2|z_l|^2,
 \qquad
 G_N=\sum_{m=1}^N|\Gamma_N'(\tau_m)|^2.
 \tag{5.1}
\]

Here \(K_{s,N}\) and \(K_{v,N}\) are the leading scalar and shear enstrophy
coefficients, and \(G_N\) is the total limiting slope mass. With physical
seed and shear amplitudes \(S\) and \(P\), and a background matched to the
high-frequency enstrophy, the conditional leading ledger is

\[
 D\asymp q^2(S^2K_{s,N}+P^2K_{v,N}),
 \tag{5.2}
\]

\[
 \sum_{m=1}^NJ_m
 \asymp
 \frac{S^2P^2G_N}
 {q^2(S^2K_{s,N}+P^2K_{v,N})}.
 \tag{5.3}
\]

Optimizing in the ratio \(S/P\) gives

\[
 \sup_{S/P}
 \frac{\sum_mJ_m}{D^{1/3}}
 \asymp
 \left(\frac{P}{q^2}\right)^{4/3}
 \frac{G_N}{K_{s,N}K_{v,N}^{1/3}}.
 \tag{5.4}
\]

If

\[
 \varepsilon_N:=\frac{P\sqrt{K_{v,N}}}{q^2},
 \qquad
 \mathcal Q_N:=\frac{G_N}{K_{s,N}K_{v,N}},
 \tag{5.5}
\]

then (5.4) becomes

\[
 \sup_{S/P}
 \frac{\sum_mJ_m}{D^{1/3}}
 \asymp \varepsilon_N^{4/3}\mathcal Q_N.
 \tag{5.6}
\]

Equation (5.6) is an exact algebraic rewrite of the conditional ledger, but
\(\varepsilon_N\) is an energy proxy, not the operator parameter in the IFT.
The latter is

\[
 \delta_{\mathrm{op},N}
 :=\frac{P}{q^2}
 \sup_{x\ge A_0}\|V_{z_N}(x)\|_{\ell^2\to\ell^2}.
 \tag{5.6a}
\]

For distinct positive integer frequencies \(r_l\), multiplication-operator
and Fourier estimates give

\[
 c\frac{P}{q^2}\|z_N\|_2
 \le \delta_{\mathrm{op},N}
 \le C\frac{P}{q^2}\|z_N\|_1
 \le C\varepsilon_N.
 \tag{5.6b}
\]

The last inequality uses
\(\sum_l r_l^{-2}\le\pi^2/6\). Thus small \(\varepsilon_N\) is sufficient
for small operator coupling, but is not necessary: coefficients at large
\(r_l\) can make \(K_{v,N}\) large without a comparable increase in
\(\|V_{z_N}\|\). The two quantities cannot be merged.

This isolates the unresolved finite-dimensional question. A growing-root
counterfamily would need all of the following simultaneously:

1. an explicit growing family of nodes and response rates;
2. a quantitative ECT inverse bound and coefficient curve;
3. a quantitative IFT radius stated for
   \(\delta_{\mathrm{op},N}\), not for \(\varepsilon_N\);
4. a choice of \(P,q,N\) for which the actual operator coupling lies inside
   that radius while
   \(\varepsilon_N^{4/3}\mathcal Q_N\to\infty\);
5. a uniform nonlinear enstrophy/background estimate with the full
   \(K_{s,N},K_{v,N}\) cost included; and
6. a full-frequency rotational-charge coefficient that does not grow faster
   than the proposed atom sum.

The current ECT statement gives only invertibility for each fixed \(N\). It
does not bound the smallest singular value as \(N\to\infty\). The current
Dyson estimate likewise has constants depending on the dimension, the
coefficient ball, and \(\|V_z\|\). Simplicity supplies
\(|\Gamma_N'(\tau_m)|>0\) one \(N\) at a time but no lower bound on \(G_N\).
If the phase seed has \(|A_l|=1\) and the \(r_l\) are distinct positive
integers, then already
\(K_{s,N}=\sum_lr_l^2\gtrsim N^3\). Any proposed gain must pay this
elementary lattice cost before the inverse-Jacobian and charge costs.

The R0.71V clustering calculation supplies a negative warning. For fixed
response rates and spacing \(\Delta\),

\[
 |\Gamma_N'(\tau_m)|=O(\Delta^{N-1}),
 \tag{5.7}
\]

and a cluster at the launch zero loses one further power. Avoiding this
collapse requires growing response rates or growing coefficients. Both cost
initial enstrophy and shrink the quantitative IFT radius. A useful next lemma
would be a weighted Markov/observability inequality for the exponential
response family that compares \(G_N\) directly with
\(K_{s,N}K_{v,N}\) and the inverse-Jacobian norm.

## 6. Complete rotational charge

For fixed dimension and small coupling, the R0.71W estimate generalizes at
the scaling level, under the same enstrophy floor, to

\[
 \mathcal L_I:=\frac1\ell\int_I
 \frac{\|L\|_{\dot H^{-1}}^2}{Y}\,dt
 \lesssim
 \frac{S^2P^2}{\lambda^4(S^2+P^2)}.
 \tag{6.1}
\]

If an exact selected root also has the two-sided slope estimate
\(|a_t|\asymp SP\), then the right side is comparable to
\(J_*/\lambda^2\). For an arbitrary multiblock family, only the displayed
upper bound is justified.

For \(P=S=\delta\lambda^2\), the natural scales are

\[
 D\asymp\delta^2\lambda^6,
 \qquad
 J_*\asymp\delta^2\lambda^2,
 \qquad
 \mathcal L_I\lesssim\delta^2.
 \tag{6.2}
\]

In the proved small-coupling range, the fixed \(\nu^2\) baseline already pays
\(J_*\) after multiplication by \(D^{1/3}\). No lower bound on
\(\mathcal L_I\) is needed for that conclusion.

Outside that range, the heuristic substitution
\(\mathcal L_I\asymp\delta^2\) would give

\[
 \frac{J_*}{D^{1/3}(\nu^2+\mathcal L_I)}
 \asymp
 \frac{\delta^{4/3}}{\nu^2+\delta^2},
 \tag{6.3}
\]

which is bounded and tends to zero at both extreme coupling scales. This is
only a scaling warning, not a positive theorem: R0.71W proves an upper bound
on the charge, whereas paying an atom would require a lower bound or a
nonconcentration estimate.

At a target root, the fixed low-frequency component of \(L\) equals the
target slope up to a fixed sign and multiplier. A strong-coupling
counterfamily must therefore make that component temporally narrow enough
that its time integral stays small. Conversely, a positive endpoint theorem
could follow from a persistence estimate of the form

\[
 \int_{t_*-\tau}^{t_*+\tau}
 \frac{\|L(t)\|_{\dot H^{-1}}^2}{Y(t)}\,dt
 \ge c\tau J_*(t_*),
 \tag{6.4}
\]

with a scale-compatible lower bound on \(\tau\). No such strong-coupling
estimate is currently proved.

For growing \(N\), it is not enough to reuse the fixed-\(N\) constant in
(6.1). The producer would have to record a normalized full-product
coefficient such as

\[
 H_N=\int
 \|V_N(x)F_N(x)\|_{\dot H^{-1}}^2\,dx
 \tag{6.5}
\]

and compare it with \(G_N,K_{s,N},K_{v,N}\). Target-shell-only charge is not
admissible.

## 7. Conjectural next-stage candidate: strong-coupling Bessel roots

This section is deliberately outside the R0.71X proved ledger.

Consider one shear mode

\[
 v(y,t)=P e^{-\nu\lambda^2(t-\sigma)}\cos(\lambda y)
 \tag{7.1}
\]

and put the active scalar initially on the fixed target mode rather than on
a high-frequency predecessor. Let

\[
 \delta=\frac{P}{\lambda^2}\longrightarrow\infty,
 \qquad
 \tau=P(t-\sigma).
 \tag{7.2}
\]

On every fixed \(\tau\)-interval, both the shear heat decay and the
rescaled viscosity are formally \(O(\delta^{-1})\). The limiting transport
solution has the phase

\[
 f^0(y,z,\tau)
 =S e^{i(K_yy+K_zz)}
 e^{-ic\tau\cos(\lambda y)},
 \tag{7.3}
\]

so its fixed-target coefficient is a constant multiple of \(SJ_0(c\tau)\).
The simple Bessel zeros suggest exact viscous roots by a uniform
singular-limit root-persistence argument. The coset
\(K_y+\lambda\mathbb Z\) still meets a sufficiently isolated fixed compact
target only at the declared pair.

For a sinusoidal shear, the expected rescaled enhanced-dissipation time is
of order \(\delta^{1/2}\), and the corresponding maximum squared gradient
amplification is heuristically of order \(\delta\). If one chooses

\[
 S=P\delta^{-1/2}
 \tag{7.4}
\]

and a decoupled background of enstrophy \(P^2\lambda^2\), then the heuristic
ledger is

\[
 D\asymp Y\asymp P^2\lambda^2,
 \qquad
 J_*\asymp\delta\lambda^2,
 \qquad
 \frac{J_*}{D^{1/3}}\asymp\delta^{1/3}.
 \tag{7.5}
\]

Stationary-phase/Bessel decay of every fixed low output suggests, but does
not prove,

\[
 \mathcal L_I=O(\log\delta),
 \tag{7.6}
\]

which would leave the heuristic complete ratio of order
\(\delta^{1/3}/\log\delta\). Formula (7.6) is not a full-frequency estimate,
and enhanced dissipation may change it. No counterexample claim follows.

This candidate requires four new analytic components before any numerical
sweep can count as more than exploration:

1. **Uniform viscous Bessel-root lemma.** Prove convergence of the exact
   Fourier-lattice target path and its first time derivative on fixed
   \(\tau\)-intervals, then persist at least two simple Bessel zeros.
2. **Sharp full-window enstrophy envelope.** Prove the enhanced-dissipation
   time and maximum \(\|f_y\|_2^2\) with constants sufficient to size the
   decoupled background and keep \(\mathcal R_Y(I)=O(1)\).
3. **Full-frequency Lamb-charge upper bound.** Estimate every Fourier mode
   of \(-vf_z\) in \(\dot H^{-1}\) through the mixing and dissipation
   intervals. A target-mode or stationary-phase calculation alone is not
   enough.
4. **Exact data ledger.** Include the shear, active scalar, and persistent
   background in \(D\), and verify that the proposed charge ratio still
   diverges after all constants and transition intervals are included.

Until these four items are proved, the strong-coupling route is a conjectural
candidate for a later release, not evidence against the endpoint.

## 8. Claim boundary for R0.71X

### Analytically available after independent audit

1. Exact endpoint saturation with
   \(\mathscr A_q=\delta_*q^2\), \(0<\delta_*<\delta_0\) sufficiently small.
2. The selected-root inequality (1.6) for comparable-band launch data with
   the stated root-time enstrophy floor; seed--shear imbalance cannot improve
   its \(4/3\) collective-coupling power.
3. The exact zero atom at a multiple root, the fixed-rate split-root collapse
   from R0.71V, and finiteness of lattice targets in fixed compact Fourier
   support.

### Conditional diagnostics, not release theorems

1. The noncomparable-frequency estimate (1.10), conditional on launch data
   controlling the weighted root-time enstrophy.
2. The growing coherent-block envelope (3.3), for which an exact coherent
   root family and uniform IFT have not been constructed.
3. The growing-root ledger (5.2)--(5.6), which must retain both
   \(\varepsilon_N\) and \(\delta_{\mathrm{op},N}\).
4. The fixed-dimensional charge comparison in Section 6 outside the
   R0.71W family.

### Still open

1. A quantitative growing-dimensional ECT--IFT theorem, a compatible
   operator-radius estimate, and the asymptotics of
   \(\varepsilon_N^{4/3}\mathcal Q_N\).
2. A universal \(D^{1/3}\) payment outside the constructed triangular
   family.
3. A strong-coupling nonconcentration or counterexample theorem.
4. The Bessel/enhanced-dissipation candidate in Section 7.

Nothing in this note proves a continuation criterion, a finite-time
singularity, or global regularity for three-dimensional Navier--Stokes.
