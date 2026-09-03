# R0.74Y — payment-compatible two-coordinate route screen

## 0. Decision

R0.74X isolates the correct next target:

\[
\frac{\min\{K_{r,R}(t_r),K_{s,R}(t_s)\}}
{(P_R^M)^{2/3}}\longrightarrow\infty,
\qquad r\ne s.
\tag{Y.1}
\]

This note screens four modifications of the common-shear heat-packet
architecture against (Y.1).  The conclusions are:

| route | exponent decision |
|---|---|
| non-equal target amplitudes | strictly ruled out by the packet's own target-lobe payment in the frozen geometry |
| non-adjacent shell placement | strictly worse than adjacent placement |
| geometry without cancellation | ruled out for two dyadically distinct surviving W-type endpoints |
| genuine exponential target-lobe field cancellation | not ruled out at the level of necessary exponents; new geometry and corrector theorems required |
| accumulated viscosity as the second coordinate | not certified; a dimensional ledger predicts an extra factor \(R\), but the required \(H^1\)/occupation upper is open |

The selected construction target is deliberately formal.  It uses two
adjacent packets, a smaller fixed vertical gap, a non-equal outer amplitude,
and an exponentially accurate cancellation of the outer target lobe which
must leave the remote inward tail intact.  Its necessary exponent ledger has
a nonempty strict window, but the changed-geometry common-shear platform, the
cancellation cell, and the complete payment upper bound are not constructed
here.  The accumulated-viscosity alternative remains a separate open audit
until a genuine \(H^1\)/occupation upper is proved or disproved.

Thus the status is

\[
\boxed{
\begin{gathered}
\textbf{FROZEN-GEOMETRY NO-GO PROVED; FORMAL CANCELLATION WINDOW FOUND;}\\
\textbf{ACCUMULATED-VISCOSITY BRANCH OPEN; NO CONSTRUCTION THEOREM.}
\end{gathered}}
\tag{Y.2}
\]

The proved frozen-geometry no-go retains the exact smooth unforced
common-shear Navier--Stokes structure and the fixed-deletion
\(\inf_S\sup_t\) order.  The changed-geometry candidate must re-establish the
same structure before it can be used.
\(\mathbf{NOT\ CLAY}\).

## 1. Frozen functional and source boundary

The relevant local snapshots are:

| source | SHA-256 | use |
|---|---|---|
| research/r074p_temporal_observable_triage.md | a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867 | canonical nonnegative clock and payment |
| research/r074q_common_shear_multipacket_gate.md | 60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695 | exact finite common-shear superposition |
| research/r074q_relaxed_multipacket_cubic_obstruction.md | ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d | amplitude-weighted lobe and cubic-payment ledger |
| research/r074s_fixed_deletion_simultaneous_height.md | 305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1 | fixed-deletion order |
| research/r074w_remote_adjacent_inward_comparison.md | d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10 | W-type remote survival and sweeping |
| research/r074x_three_packet_fixed_deletion_gate.md | 4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3 | payment-normalization blocker |

The functional is

\[
\mathfrak L^K_{1,R}(\mathcal D)
=
\inf_{\substack{S\subset\mathbb N\\ \#S\le1}}
\sup_{t\in\mathcal D}
\sum_{k\notin S}K_{k,R}(t).
\tag{Y.3}
\]

One deletion set is used for every time.  Therefore two different
coordinates with lower bounds at two possibly different times imply

\[
\mathfrak L^K_{1,R}(\mathcal D)
\ge
\min\{K_{r,R}(t_r),K_{s,R}(t_s)\}.
\tag{Y.4}
\]

No time overlap is required.  A same-time vector lower bound is stronger
but unnecessary.

For the exact family,

\[
K_{k,R}=K^b_{k,R}+K^G_{k,R}\ge0
\tag{Y.5}
\]

at every smooth time.  The anomalous-defect row is zero.  No strip upper
bound below is used as a whole-shell upper bound.

## 2. Universal adjacent-endpoint versus self-payment ledger

Let one packet have scale \(L\), height

\[
h=(p+d)LR,\qquad p=\frac{32}{63},\qquad d>0,
\tag{Y.6}
\]

and let its adjacent inward strip lie near \(x_3=pLR\).  Write

\[
\mathsf a=1+\frac{t}{R^2}\in[65,66],\qquad
\rho_L=\frac{\log(1/R)}{L^2},
\tag{Y.7}
\]

\[
\Gamma=e^{-c_\gamma L^2},\qquad
c_\gamma=\frac8{3969}.
\tag{Y.8}
\]

Allow an arbitrary amplitude \(\mathfrak a\).  Up to powers of \(L\) and
\(e^{O(L)}\), the W-type adjacent inward endpoint strip has size

\[
E^{\rm adj}
\asymp
\mathfrak a^2R^2
\Gamma^{1/4}
\exp\!\left[-\frac{d^2}{2\mathsf a}L^2\right].
\tag{Y.9}
\]

The same packet has an \(R^3\)-length target-lobe interval and
\(L R^3\) target-lobe volume.  Since

\[
A_k(R)=A_{k-1}(2R),\qquad
\gamma_{k-1}=\Gamma^{1/4},
\]

the nonnegative exterior velocity-cubic row forces

\[
P_R^M
\gtrsim
|\mathfrak a|^3R^4\Gamma^{1/4}
\quad\text{up to powers of }L,
\tag{Y.10}
\]

provided the packet is not cancelled on its own target lobe.  Hence

\[
(P_R^M)^{2/3}
\gtrsim
\mathfrak a^2R^{8/3}\Gamma^{1/6}
\quad\text{up to powers of }L.
\tag{Y.11}
\]

Subtracting the exponential rates in (Y.9) and (Y.11) gives

\[
\frac1{L^2}
\log\frac{E^{\rm adj}}{(P_R^M)^{2/3}}
\le
\frac23\rho_L-\Theta(d,\mathsf a)+o(1),
\tag{Y.12}
\]

where

\[
\boxed{
\Theta(d,\mathsf a)
:=\frac{c_\gamma}{12}
+\frac{d^2}{2\mathsf a}.}
\tag{Y.13}
\]

The amplitude cancels exactly.  A necessary condition for this packet's
adjacent endpoint to beat its own lobe payment is therefore

\[
\boxed{
\rho_L>\frac32\Theta(d,\mathsf a).}
\tag{Y.14}
\]

The W bridge survival condition at the same strip is

\[
\rho_L<q(\ell),\qquad
q(\ell)=\frac{p^2}{4\ell},\qquad
\ell=\mathsf a-1.
\tag{Y.15}
\]

These two strict inequalities are the first screen for every endpoint
route.

For the frozen height \(d=433/1008\), even the most favorable payment age
\(\mathsf a=66\) gives

\[
\Theta_{\rm fr}
=\frac{c_\gamma}{12}+\frac{d^2}{132}
=\frac{210017}{134120448},
\tag{Y.16}
\]

\[
\frac32\Theta_{\rm fr}-q_{64}
=\frac{119905}{89413632}>0,
\qquad
q_{64}=\frac4{3969}.
\tag{Y.17}
\]

Since \(q(\ell)\le q_{64}\), the frozen W endpoint cannot both survive and
beat even its own mandatory target-lobe payment.  This is stronger than
the three-packet comparison in R0.74X.

There is a sharper same-age version of this no-go.  The survival exponent
uses deficit age \(\ell\), while the endpoint comparator uses heat age
\(\ell+1\).  Combining (Y.12) with
\(\rho_L<q(\ell)=p^2/(4\ell)\) gives
\[
\limsup
\frac1{L^2}
\log\frac{E^{\rm adj}}{(P_R^M)^{2/3}}
\le
\Xi_{\rm fr}(\ell),
\]
where
\[
\Xi_{\rm fr}(\ell)
:=
\frac{p^2}{6\ell}
-\frac{c_\gamma}{12}
-\frac{d^2}{2(\ell+1)}.
\tag{Y.17a}
\]
The coarse sign already follows from
\[
p^2-3d^2=-\frac{300323}{1016064}<0.
\]
Keeping the exact two ages is still strictly negative.  Indeed,
\(\Xi_{\rm fr}'(\ell)>0\) on \([64,65]\), because
\(3d^2(64/65)^2-p^2=4673072/16769025>0\), and
\[
\boxed{
\max_{64\le\ell\le65}\Xi_{\rm fr}(\ell)
=\Xi_{\rm fr}(65)
=-\frac{875993}{968647680}<0.}
\tag{Y.17b}
\]
Thus every frozen-geometry construction whose witness is one packet's
W-type adjacent strip and whose unavoidable payment is the same packet's
target lobe fails payment compatibility.  This statement is independent
of its amplitude, its absolute target normalization, and the placement of
the other packet scales.

## 3. Route A: non-equal target amplitudes

Parameterize arbitrary packet amplitudes at exponential accuracy by

\[
\log|\mathfrak a_i|
=\alpha_iL_i^2+o(L_i^2).
\tag{Y.18}
\]

For packet \(i\), the endpoint and its own lobe-payment two-thirds power
have rates

\[
\kappa_i
=2\alpha_i-2\rho_i-\frac{c_\gamma}{4}
-\frac{d_i^2}{2\mathsf a_i},
\tag{Y.19}
\]

\[
\pi_i
=2\alpha_i-\frac83\rho_i-\frac{c_\gamma}{6},
\qquad
\rho_i=\frac{\log(1/R)}{L_i^2}.
\tag{Y.20}
\]

Thus

\[
\kappa_i-\pi_i
=\frac23\rho_i-\Theta(d_i,\mathsf a_i).
\tag{Y.21}
\]

Changing \(\alpha_i\) shifts the clock and its own payment by the same
amount.  A fixed-deletion counterexample needs each of its two retained
witness clocks to exceed the total payment, so in particular it needs
\(\kappa_i>\pi_i\) for each witness packet.

Equations (Y.15)--(Y.17) show that this self-condition is impossible in
the frozen geometry, regardless of how unequal the amplitudes are.
Amplitude tilting can equalize two clock heights and improve cross-packet
dominance, but it cannot create a missing self-payment gap.

Decision:

\[
\boxed{\textbf{NON-EQUAL AMPLITUDES ALONE: STRICT NO-GO.}}
\tag{Y.22}
\]

## 4. Route B: non-adjacent shell placement

Let two packet scales obey

\[
L_{\rm out}=rL_{\rm in},\qquad r=2^j,\qquad j\ge1.
\tag{Y.23}
\]

For one common \(R\), put
\(\rho=\log(1/R)/L_{\rm in}^2\).  Then

\[
\rho_{\rm out}=\frac{\rho}{r^2}.
\tag{Y.24}
\]

Even if the inner packet merely has to survive at the largest possible
W threshold, \(\rho<q_{64}\), payment compatibility for the outer packet
requires

\[
\rho>r^2\frac32\Theta(d_{\rm out},\mathsf a_{\rm out}).
\tag{Y.25}
\]

In the frozen geometry, (Y.17) already rules this out for a single scale.
Increasing \(r\) only decreases \(\rho_{\rm out}\).

There is also an exact geometry-only barrier which persists if the
vertical gap is reduced.  Since

\[
\Theta(d,\mathsf a)\ge\frac{c_\gamma}{12},
\tag{Y.26}
\]

the least possible right side of (Y.25) for adjacent dyadic scales
\(r=2\) is

\[
4\cdot\frac32\cdot\frac{c_\gamma}{12}
=\frac{c_\gamma}{2}
=q_{64}.
\tag{Y.27}
\]

Survival requires a strict inequality below \(q_{64}\), whereas payment
compatibility requires a strict inequality above the same number.  For
\(r>2\), the gap is strictly worse.

The large outer packet is not a cancellation problem here: the inherited
vertical cross margin improves as the dyadic separation grows.  The
failure is the outer packet's own cubic payment.

Decision:

\[
\boxed{\textbf{NON-ADJACENT PLACEMENT: STRICT NO-GO.}}
\tag{Y.28}
\]

## 5. Route C: lower the outer target-lobe cubic payment

### 5.1 Pure geometry cannot remove the weight identity

Moving the reference height closer to the adjacent inward face reduces
\(d\) and therefore reduces the Gaussian part of \(\Theta\).  It does not
change

\[
A_k(R)=A_{k-1}(2R)
\tag{Y.29}
\]

or the irreducible payment weight \(\Gamma^{1/4}\).  Equation (Y.27)
therefore rules out geometry alone for two distinct dyadic W-surviving
endpoint packets, even in the limiting case \(d=0\).

Changing the lobe chord or its residence interval by a fixed power of
\(L\) also cannot change (Y.12).  An exponential improvement, not a
polynomial one, is necessary.

### 5.2 A flux sign does not help

The relevant payment row contains \(|u|^3\), equivalently
\([b^2+U^2]^{3/2}\), with a nonnegative spatial weight.  Opposite signed
fluxes do not cancel this row.  Any useful sign mechanism must cancel the
actual field \(U\) on the whole target lobe, not merely a signed flux
integral.

### 5.3 Exact cancellation requirement

Suppose a common-shear correction cell makes the residual target-lobe
amplitude smaller by

\[
|U|\le
C|\mathfrak a_iG_i|e^{-\zeta_iL_i^2}
\tag{Y.30}
\]

throughout an \(R^3\)-length target interval and the full target box.
Suppose also that a geometric mechanism reduces the corresponding
spacetime volume by \(e^{-\omega_iL_i^2}\).  Then the lobe-payment
two-thirds exponent is reduced by

\[
2\zeta_i+\frac23\omega_i.
\tag{Y.31}
\]

The necessary self-compatibility condition becomes

\[
\boxed{
\frac23\rho_i-\Theta(d_i,\mathsf a_i)
+2\zeta_i+\frac23\omega_i>0.}
\tag{Y.32}
\]

The frozen heat-packet width and the speed \(Q_i'\asymp R^{-2}\) give only
polynomial changes to the lobe volume and residence, so
\(\omega_i=0\) in the present architecture.  Consequently a true
exponential field cancellation, \(\zeta_i>0\), is the only screened
mechanism not already excluded.

Such cancellation is compatible with the exact PDE algebra in principle:
one may add finitely many inversion-paired passive correctors, all evolved
under the same shear \(b\).  It is not compatible with merely summing
packets evolved under different shears.

## 6. Formal cancellation candidate

The following rational ledger shows that one hybrid route has a nonempty
window of necessary exponent inequalities.  It is a formal target for
construction, not a constructed family and not a sufficient feasibility
proof.

Use two adjacent packets,

\[
L_2=2L_1,
\tag{Y.33}
\]

and replace the frozen height coefficient by

\[
d=\frac7{32},\qquad
c=p+d=\frac{1465}{2016}.
\tag{Y.34}
\]

Choose the common interior heat age and scale rate

\[
\mathsf a_0=\frac{131}{2},
\qquad
\rho=\frac{\log(1/R)}{L_1^2}=\frac9{10000}.
\tag{Y.35}
\]

Thus both packets may be re-centred at
\(t=(\mathsf a_0-1)R^2=64.5R^2\).  Different times would also be
permitted by (Y.4), provided the changed-geometry platform is proved.

The formal W-type survival inequality has the strict reserve

\[
q_{65}-\rho
=\frac{47627}{515970000}>0,
\tag{Y.36}
\]

and the numerical U-reserve scale inequality also has the strict reserve

\[
a_S-\rho
=\frac{34203}{14080000}>0.
\tag{Y.37}
\]

At this age define

\[
\Theta_0
=\frac{c_\gamma}{12}+\frac{d^2}{131}
=\frac{851731}{1597252608},
\tag{Y.38}
\]

\[
\chi_0
=\frac34c_\gamma-\frac{d^2}{131}
=\frac{203461}{177472512}>0.
\tag{Y.39}
\]

The inner endpoint is not excluded by its own uncancelled target-lobe
payment at the level of the necessary exponent comparison:

\[
\frac23\rho-\Theta_0
=\frac{66637853}{998282880000}>0.
\tag{Y.40}
\]

The necessary reference-height deficit separation has the positive margin

\[
\frac{c^2}{260}-\frac{p^2}{256}
=\frac{216253}{211341312}>0.
\tag{Y.41}
\]

The formal equal-target remote cross margins are also positive:

\[
\delta_{1\leftarrow2}
=\frac{194323}{1072963584}>0,
\qquad
\delta_{2\leftarrow1}
=\frac{6059}{9289728}>0.
\tag{Y.42}
\]

Now tilt only the outer primary amplitude:

\[
\mathfrak a_1
=A_*(\Gamma_1L_1)^{-1/2},
\qquad
\mathfrak a_2
=A_*(\Gamma_2L_2)^{-1/2}e^{-\sigma L_2^2},
\tag{Y.43}
\]

where

\[
\sigma=\frac38\chi_0
=\frac{203461}{473260032}.
\tag{Y.44}
\]

If \(T_*=A_*^2R^2\), then the two formal adjacent endpoint exponents are
equal:

\[
E_1^{\rm adj}
=T_*e^{\chi_0L_1^2+o(L_1^2)},
\tag{Y.45}
\]

\[
E_2^{\rm adj}
=T_*e^{4(\chi_0-2\sigma)L_1^2+o(L_1^2)}
=T_*e^{\chi_0L_1^2+o(L_1^2)}.
\tag{Y.46}
\]

The tilt improves the outer-on-inner cross margin.  It reduces the
inner-on-outer margin, but the exact remainder is still positive:

\[
\delta_{2\leftarrow1}-\sigma
=\frac{1893805}{8518680576}>0.
\tag{Y.47}
\]

Require an outer target-lobe cancellation exponent

\[
\zeta=\frac1{5000}.
\tag{Y.48}
\]

The exact minimum required by the outer self-payment comparison is

\[
\frac{\Theta_0}{2}-\frac{\rho}{12}
=\frac{382589443}{1996565760000},
\tag{Y.49}
\]

and

\[
\zeta-
\left(\frac{\Theta_0}{2}-\frac{\rho}{12}\right)
=\frac{16723709}{1996565760000}>0.
\tag{Y.50}
\]

After both the amplitude tilt and the postulated cancellation are inserted,
the modeled outer-lobe payment two-thirds exponent would lie below the
common endpoint height by

\[
\frac{16723709}{249570720000}>0.
\tag{Y.51}
\]

Thus the necessary endpoint, modeled self-payment, formal survival,
reference-deficit, and cross-packet exponent inequalities all have strict
signs.  This arithmetic does not supply the changed-height bridge theorem.

What is not proved is exactly what matters:

1. re-prove the common-shear platform, central-reference comparison,
   all-winding bridge estimate, and remote survival theorem for
   \(d=7/32\);
2. construct an inversion-paired corrector satisfying (Y.30) with
   \(\zeta=1/5000\) on the full outer target spacetime box;
3. prove that the same corrector is \(o(E_2^{\rm adj})\) on the remote
   adjacent inward strip;
4. prevent the corrector's own lobes from restoring an equal or larger
   exterior cubic payment;
5. prove a complete upper bound for every nonnegative row of \(P_R^M\),
   including the central \(3/2\)-power and harmonic rows;
6. retain all periodic copies, inversion partners, initial-energy
   finiteness, and the zero mollified path.

Until all six statements are proved, (Y.33)--(Y.51) are only a nonempty
formal necessary-exponent window.

## 7. Route D: accumulated viscosity as the second coordinate

The available V/W sources do not prove the accumulated \(H^1\) occupation
upper required in this section.  The following calculation is therefore a
dimensional screen, not a no-go theorem.

For accumulated viscosity generated by the same remote inward tail, one
would expect that during one passage through a fixed \(R\)-width horizontal
strip,

\[
|Q_i'|\asymp R^{-2}
\]

gives a residence time \(R^3\) up to powers of \(L_i\).  Spatial
derivatives of the remote Gaussian cost at most powers of \(L_i/R\).
If all-winding derivative and occupation uppers justified this counting,
the accumulated viscous clock would have the exponential scale

\[
D_i^{\rm adj}
\lesssim
\operatorname {poly}(L_i)\,
\mathfrak a_i^2R^3\Gamma_i^{1/4}
e^{-d_i^2L_i^2/(2\mathsf a_i)}.
\tag{Y.52}
\]

Comparison with (Y.11) would yield

\[
\frac1{L_i^2}
\log\frac{D_i^{\rm adj}}{(P_R^M)^{2/3}}
\le
-\frac13\rho_i-\Theta(d_i,\mathsf a_i)+o(1)<0.
\tag{Y.53}
\]

Within this formal ledger, time integration does not improve the endpoint
exponent: the gradient supplies only powers of \(L_i\), while the
moving-lobe residence adds an extra factor \(R\).  This is not a certified
upper bound on the accumulated clock.

At the intended target shell, the same dimensional counting predicts,
again up to powers of \(L_i\),

\[
D_i^{\rm tar}
\lesssim
\Gamma_i\mathfrak a_i^2R^3.
\tag{Y.54}
\]

Its formal ratio to the same target-lobe payment would obey

\[
\frac1{L_i^2}
\log\frac{D_i^{\rm tar}}{(P_R^M)^{2/3}}
\le
-\frac13\rho_i-\frac56c_\gamma+o(1)<0.
\tag{Y.55}
\]

The monotonicity of accumulated viscosity is useful for keeping a clock
high after its production, but the fixed-deletion order (Y.3) already allows
different witness times.  Monotonicity alone therefore does not repair the
missing exponent; a rigorous decision still needs the missing
\(H^1\)/occupation estimate.

A radically higher-frequency passive profile is not covered by
(Y.52)--(Y.55), but it would be a new architecture: its heat damping,
initial energy, complete payment, and survival would all require new
estimates.

Decision:

\[
\boxed{
\begin{gathered}
\textbf{CURRENT HEAT-PACKET ACCUMULATED-VISCOSITY ROUTE:}\\
\textbf{DIMENSIONALLY DISFAVORED, BUT NOT YET CERTIFIED.}
\end{gathered}}
\tag{Y.56}
\]

## 8. Comparative necessary inequalities

The four screens can be summarized without suppressing the controlling
inequality:

| modification | necessary clock-over-payment inequality | result |
|---|---|---|
| unequal amplitudes | \(\frac23\rho_i>\Theta(d_i,\mathsf a_i)\) for each witness | amplitude cancels; frozen survival contradicts it |
| shell ratio \(r\ge2\) | \(\rho>r^2\frac32\Theta\) and \(\rho<q_{64}\) | already equality at \(r=2,d=0\); worse otherwise |
| geometry only | reduce \(d\), but \(\Theta\ge c_\gamma/12\) | cannot cross the dyadic equality |
| target field cancellation | \(\frac23\rho_i-\Theta+2\zeta_i+\frac23\omega_i>0\) | possible at exponent level |
| remote accumulated viscosity | formally \(-\frac13\rho_i-\Theta>0\) | negative dimensional rate; rigorous occupation upper open |
| target accumulated viscosity | formally \(-\frac13\rho_i-\frac56c_\gamma>0\) | negative dimensional rate; rigorous occupation upper open |

Polynomial chord, volume, time, and derivative factors cannot change the
displayed exponential signs.  For the final two rows, obtaining the
displayed clock upper is itself an open analytic task.

## 9. Minimum next proposition

The smallest explicit construction target selected by the exponent screen
is the following cancellation-cell proposition.

\[
\boxed{
\begin{gathered}
\text{Construct two adjacent inversion-paired passive primary packets and}\\
\text{a finite inversion-paired corrector family, all under one common shear,}\\
\text{such that (Y.30) holds on the outer target spacetime box,}\\
\text{the correctors are negligible on both remote inward strips, and}\\
(P_R^M)^{2/3}
=o\!\left(
\min\{K_{k_1-1,R}(t_1),K_{k_2-1,R}(t_2)\}
\right).
\end{gathered}}
\tag{Y.57}
\]

The rational data (Y.33)--(Y.51) give one explicit exponent budget for
this proposition, conditional on re-proving the changed-geometry platform.
If it were proved, (Y.4) would yield

\[
\frac{\mathfrak L^K_{1,R}(\mathcal D)}
{(P_R^M)^{2/3}}\longrightarrow\infty
\tag{Y.58}
\]

without requiring \(t_1=t_2\).

In parallel, the accumulated-viscosity branch requires either a rigorous
all-winding \(H^1\)/occupation upper for the current moving heat packet or a
countermechanism showing that the dimensional estimate fails.  This note
proves neither task.

This note does not prove (Y.57).  In particular, it does not infer a
whole-shell estimate from a strip calculation and does not transfer any
endpoint statement to arbitrary suitable weak solutions.  It is a route
screen only, with no regularity, singularity, or Millennium conclusion.
\(\mathbf{NOT\ CLAY}\).
