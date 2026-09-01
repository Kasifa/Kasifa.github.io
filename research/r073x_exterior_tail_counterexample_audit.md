# R0.73X exterior-tail counterexample audit

**Audit date:** 2026-09-01

**Scope:** independent pressure test of the schematic estimate (5.3) in
`r073x_problem_freeze.md`

**Status:** one analytic heat-kernel upper bound and several static
falsification tests; no Navier--Stokes regularity theorem, no singular
trajectory, and no public release are asserted

**DGX used:** false

**Claim boundary:** all translated-packet witnesses below are smooth,
divergence-free static fields.  They are not asserted to be unforced
Navier--Stokes trajectories.  Consequently they refute only inequalities
whose quantifiers include arbitrary smooth divergence-free data, or proposed
purely velocity-functional estimates that do not use the equation.  The
choice \(p=\mu=0\) is unconstrained and is generally not the pressure
associated with the packet, so these witnesses also do not refute an
associated-pressure inequality.

NOT CLAY.

## 1. Question and conclusion

The frozen schematic target is

\[
 {\cal C}^{\rm abs}_{{\mathscr S},0}(z_0,R)
 \le C\left[
 {\cal E}(z_0,2R)^{3/2}+{\cal P}(z_0,2R)+{\cal M}(z_0,2R)
 +{\cal A}_{\rm ext}(z_0,R)\right].
\tag{1.1}
\]

The audit gives four answers.

1. A tail-free version of (1.1) is false as a velocity-only functional
   inequality for unconstrained triples with arbitrary smooth divergence-free
   velocity and \(p=\mu=0\).  A packet translated outside
   \(B_{2R}\) has zero local energy, pressure, and defect rows, but the
   Gaussian has infinite support and can give a nonzero value of
   \({\mathscr S}_s\) in \(B_R\).
2. A Gaussian exterior row built only from a weighted \(L^2\) velocity mass,
   and then raised to the \(3/2\) power, is also insufficient.  Shrinking the
   translated packet produces a ratio of order \(\delta^{-3/2}\).
3. A critical weighted \(L^3\) velocity tail, with a decay no faster than a
   proved heat-kernel majorant, closes the \({\mathscr S}_s\) estimate.  The
   resulting bound is proved below for every energy-class field for which the
   tail is finite; it does not use the Navier--Stokes equation.
4. Far-field low frequencies, a pressure gauge, and amplitude multiplication
   do not create a new unbounded ratio once the critical velocity/pressure
   tail is included.  The remaining open problem is to control or make that
   tail small from a useful non-circular hypothesis.

Thus the minimal safe next step is not a larger Fourier grid.  It is to freeze
the exact-kernel tail in Section 3, or an annular majorant with rigorously
slower decay, and then investigate whether that row follows from a usable
all-scale energy/pressure condition.

## 2. Periodic heat-kernel majorant

Let

\[
 g_s(y)=(4\pi s)^{-3/2}e^{-|y|^2/(4s)},\qquad
 G_s(z)=\sum_{m\in\mathbb Z^3}g_s(z+2\pi m)
\tag{2.1}
\]

be the Euclidean and periodic heat kernels.  Define the periodic first-moment
kernel

\[
 H_s(z)=\sum_{m\in\mathbb Z^3}
 { |z+2\pi m|\over4s}\,g_s(z+2\pi m).
\tag{2.2}
\]

Term by term, with \(r=|z+2\pi m|/\sqrt{s}\),

\[
 { |z+2\pi m|\over4s}g_s(z+2\pi m)
 \le C_0s^{-1/2}g_{2s}(z+2\pi m),
\tag{2.3}
\]

because \(r e^{-r^2/8}\) is bounded.  Hence

\[
 H_s(z)\le C_0s^{-1/2}G_{2s}(z).
\tag{2.4}
\]

The same termwise comparison gives

\[
 G_s(z)\le 2^{3/2}G_{2s}(z).
\tag{2.5}
\]

For \(a_s(x,y)=u(x-y)-v_s(x)\), the centered production satisfies

\[
 |{\mathscr S}_s(x)|
 \le \int_{\mathbb T^3}H_s(x-y)
       |u(y)-v_s(x)|^3\,dy.
\tag{2.6}
\]

Using \(|a-b|^3\le4(|a|^3+|b|^3)\), Jensen's inequality
\(|v_s|^3\le P_s(|u|^3)\), and (2.4)--(2.5), one obtains the pointwise bound

\[
 \boxed{
 |{\mathscr S}_s(x)|
 \le C s^{-1/2}P_{2s}(|u|^3)(x).}
\tag{2.7}
\]

This estimate is deliberately unsigned.  It does not use cancellation in
\({\mathscr S}_s\), suitability, pressure, or the equation.

## 3. A ledger-complete velocity tail

Write

\[
 I_R=(t_0-R^2,t_0),\qquad U_R=B_R(x_0),
\tag{3.1}
\]

and use geodesic balls on \(\mathbb T^3\).  Freeze the exact exterior velocity
tail

\[
 \boxed{
 \begin{aligned}
 {\cal A}^{u}_{\rm ext}(z_0,R)
 :={1\over R^3}
 \int_{I_R}\!\int_{U_R}\!\int_0^{R^2}
 s^{-1/2}P_{2s}
 \big(|u(t)|^3\mathbf 1_{\mathbb T^3\setminus U_{2R}}\big)(x)
 \,ds\,dx\,dt .
 \end{aligned}}
\tag{3.2}
\]

It is dimensionless under Navier--Stokes scaling: the integrand has degree
four, \(ds\,dx\,dt\) has degree minus seven, and \(R^{-3}\) has degree
three.  It is also monotone in \(|u|\), positive, and independent of the sign
of \({\mathscr S}_s\).

### Proposition 3.1 (proved upper bound)

Let \(0<R<\pi/8\).  Suppose

\[
 u\in L^\infty(I_{2R};L^2(U_{2R}))
 \cap L^2(I_{2R};H^1(U_{2R})),
\tag{3.3}
\]

and \({\cal A}^{u}_{\rm ext}(z_0,R)<\infty\).  Then

\[
 \boxed{
 {\cal C}^{\rm abs}_{{\mathscr S},0}(z_0,R)
 \le C_\nu {\cal E}(z_0,2R)^{3/2}
 +C{\cal A}^{u}_{\rm ext}(z_0,R),}
\tag{3.4}
\]

where one may take \(C_\nu=C(1+\nu^{-1})^{3/4}\) with the normalization in
the problem freeze.  For \(\nu=1\), the constant is universal.

**Proof.**  Split the right side of (2.7) into sources in \(U_{2R}\) and
its complement.  Positivity and unit mass of \(G_{2s}\) give

\[
 \begin{aligned}
 &{1\over R^3}\int_{I_R}\!\int_{U_R}\!\int_0^{R^2}
 s^{-1/2}P_{2s}
 \big(|u|^3\mathbf1_{U_{2R}}\big)\,ds\,dx\,dt\\
 &\qquad\le {2\over R^2}
 \int_{I_R\times U_{2R}}|u|^3\,dx\,dt.
\end{aligned}
\tag{3.5}
\]

The local Sobolev inequality on \(U_{2R}\) yields, for almost every time,

\[
 \|u\|_{L^3(U_{2R})}^3
 \le C\|u\|_2^{3/2}
 \big(\|\nabla u\|_2+R^{-1}\|u\|_2\big)^{3/2}.
\tag{3.6}
\]

Hölder in time over an interval of length \(R^2\), followed by the two rows
in \({\cal E}(z_0,2R)\), gives

\[
 {1\over R^2}\int_{I_R\times U_{2R}}|u|^3
 \le C(1+\nu^{-1})^{3/4}{\cal E}(z_0,2R)^{3/2}.
\tag{3.7}
\]

The complementary source term is exactly (3.2).  Combining (2.7), (3.5),
and (3.7) proves (3.4).  \(\square\)

Since \({\cal P},{\cal M}\ge0\), Proposition 3.1 proves the schematic
inequality (1.1) after setting
\({\cal A}_{\rm ext}\ge {\cal A}^{u}_{\rm ext}\).  Pressure and defect are
not needed to bound \({\mathscr S}_s\) itself; they belong to the larger
localized energy ledger.

## 4. Annular form and the decay constraint

Let

\[
 A_j(R)=\{y:2^jR\le d_{\mathbb T}(y,x_0)<2^{j+1}R\},
 \qquad j\ge1,
\tag{4.1}
\]

with the last nonempty annulus truncated at the torus diameter.  The periodic
Gaussian upper bound, uniformly for \(0<s\le R^2<\pi^2/64\), implies

\[
 \int_{U_R}\!\int_0^{R^2}s^{-1/2}G_{2s}(x-y)\,ds\,dx
 \le CR e^{-c_*4^j},\qquad y\in A_j(R),
\tag{4.2}
\]

after decreasing \(c_*>0\) if necessary.  Consequently

\[
 \boxed{
 {\cal A}^{u}_{\rm ext}(z_0,R)
 \le C\sum_{j\ge1}e^{-c_*4^j}
 {1\over R^2}\int_{I_R\times A_j(R)}|u|^3\,dx\,dt.}
\tag{4.3}
\]

The factor \(R^{-2}\int|u|^3\) is dimensionless.  Each annular \(L^3\) row
may alternatively be bounded by an enlarged-annulus
\(L^\infty_tL^2_x\)--\(L^2_tH^1_x\) energy via (3.6)--(3.7).  Both the
velocity mass and its gradient are required for that replacement.

The numerical value of \(c_*\) is not decorative.  If an annular surrogate
uses weights \(e^{-\alpha4^j}\) with \(\alpha\) larger than the exponent
licensed by a heat-kernel upper bound, a packet at annular index \(j\) can
make the ratio grow like
\(e^{(\alpha-c_*)4^j}\).  The exact definition (3.2) avoids this ambiguity.

## 5. Pressure and defect rows in the full ledger

Although pressure does not occur in \({\mathscr S}_s\), the covariance

\[
 Q_s=P_s(pu)-p_sv_s
\tag{5.1}
\]

must be paid when the trace identity is localized.  Fix the gauge

\[
 p^\sharp(t,x)=p(t,x)-(p)_{U_{2R}}(t).
\tag{5.2}
\]

The covariance is unchanged by this time-dependent constant.  Hölder,
Jensen, and Young give

\[
 \boxed{
 |Q_s|\le C P_s\big(|u|^3+|p^\sharp|^{3/2}\big).}
\tag{5.3}
\]

For the same observation/source geometry as (3.2), a pressure-enriched
critical exterior row is obtained by replacing \(|u|^3\) with

\[
 |u|^3+|p^\sharp|^{3/2}.
\tag{5.4}
\]

Explicitly,

\[
 \boxed{
 \begin{aligned}
 {\cal A}^{u,p}_{\rm ext}(z_0,R)
 :={1\over R^3}
 \int_{I_R}\!\int_{U_R}\!\int_0^{R^2}s^{-1/2}P_{2s}
 \Big(&\big[|u|^3+|p^\sharp|^{3/2}\big]\\
 &\mathbf1_{\mathbb T^3\setminus U_{2R}}\Big)(x)
 \,ds\,dx\,dt .
 \end{aligned}}
\tag{5.4a}
\]

For a cutoff with \(|\nabla\eta_R|\lesssim R^{-1}\), the inequality
\(R^{-1}\le s^{-1/2}\) on \(0<s\le R^2\) allows the same tail to dominate
the scale-integrated \(|Q_s\cdot\nabla\eta_R|\) row **after** replacing
\(U_R\) in (5.4a) by the actual observation set
\(\operatorname{supp}\nabla\eta_R\) and freezing a larger source ball.
Its local part is then bounded by \({\cal E}^{3/2}+{\cal P}\) on that larger
ball.  Equation (5.4a) as written is not claimed to cover cutoff points lying
outside \(U_R\).

For the suitable-weak defect, the local quantity \({\cal M}(z_0,2R)\) does
not control heat arriving from a defect measure supported outside
\(U_{2R}\).  If \(P_s\mu\) is used only with its favorable sign, no absolute
tail payment is required.  If its absolute scale integral is estimated, the
correct additional row is

\[
 \boxed{
 {\cal A}^{\mu}_{\rm ext}(z_0,R)
 ={1\over R^3}\int_0^{R^2}
 \int_{I_R\times U_R}
 P_s\big(\mathbf1_{\mathbb T^3\setminus U_{2R}}\mu\big)
 (dt,dx)\,ds.}
\tag{5.5}
\]

The local part is at most \(C{\cal M}(z_0,2R)\).  A translated positive
measure shows that (5.5) cannot be omitted from an absolute defect estimate.
This is a measure-theoretic observation, not a construction of a nonzero
Navier--Stokes defect.

## 6. Translated-packet stress tests

### 6.1 A packet outside the local cylinder

There are compactly supported smooth divergence-free fields
\(w\) for which

\[
 M_3(w):=\int_{\mathbb R^3}w|w|^2\,dx\ne0.
\tag{6.1}
\]

For example, take

\[
 w=(\partial_2\psi,-\partial_1\psi,0),\qquad
 \psi(x)=f(x_1)g(x_2)h(x_3),
\tag{6.2}
\]

where \(f,h\) are nonnegative bumps and \(g\) is an asymmetric bump with
\(\int(g')^3\ne0\).  Then the first component of (6.1) contains the nonzero
factor

\[
 \left(\int f^3\right)\left(\int(g')^3\right)
 \left(\int h^3\right).
\tag{6.3}
\]

Such a \(g\) can be constructed without a genericity assumption.  Choose
two disjoint nonnegative smooth bumps \(\varphi_1,\varphi_2\) so that their
ratios \(\int\varphi_i^3/(\int\varphi_i)^3\) differ, put
\(q=\varphi_1-c\varphi_2\) with \(c\) chosen so that \(\int q=0\), and set
\(g(x)=\int_{-\infty}^xq(r)\,dr\).  Then \(g\in C_c^\infty\) and the bumps
may be chosen so that \(\int(g')^3=\int q^3\ne0\).

Choose \(y_*\notin\overline{U_{2R}}\) and a generic
\(x_*\in U_R\) so that the periodic Gaussian first moment at
\(x_*-y_*\) is not orthogonal to \(M_3(w)\).  For sufficiently small
\(\delta\), set

\[
 u_{A,\delta}(t,y)=A w\left({y-y_*\over\delta}\right),
 \qquad p=0,\qquad\mu=0.
\tag{6.4}
\]

The support remains outside \(U_{2R}\), so

\[
 {\cal E}(z_0,2R)={\cal P}(z_0,2R)={\cal M}(z_0,2R)=0.
\tag{6.5}
\]

At a fixed positive heat scale \(s_0<R^2\), expansion of the Gaussian around
\(y_*\) gives, for a generic separation,

\[
 {\mathscr S}_{s_0}(x_*)
 =c(s_0,x_*-y_*,w)A^3\delta^3+o(A^3\delta^3),
 \qquad c\ne0.
\tag{6.6}
\]

More explicitly, define

\[
 B_s(z)=\sum_{m\in\mathbb Z^3}(z+2\pi m)g_s(z+2\pi m).
\tag{6.6a}
\]

The leading coefficient in (6.6) is
\((4s_0)^{-1}B_{s_0}(x_*-y_*)\cdot M_3(w)\).  It is nonzero after a generic
choice of the separation.  Since \(\int w=0\), one has
\(P_{s_0}u_{A,\delta}(x_*)=O(A\delta^4)\); hence the centering corrections
are higher order and do not cancel the \(A^3\delta^3\) term.

Continuity supplies a positive-measure neighborhood in \((x,s)\), so the
absolute tent quantity is nonzero.  This proves that a tail-free purely
functional estimate cannot hold.

The field (6.4) is generally not an unforced Navier--Stokes trajectory.  No
PDE-only estimate is refuted by (6.4) unless its proof has already reduced to
the same arbitrary-data functional inequality.

### 6.2 Why an \(L^2\)-only Gaussian tail fails

Let \(W\) be any smooth positive weight at \(y_*\).  On (6.4),

\[
 \int W|u_{A,\delta}|^3\sim A^3\delta^3,
 \qquad
 \left(\int W|u_{A,\delta}|^2\right)^{3/2}
 \sim A^3\delta^{9/2}.
\tag{6.7}
\]

Therefore the ratio of the cubic leakage to a weighted \(L^2\)-mass tail
raised to \(3/2\) grows as

\[
 \delta^{-3/2}\longrightarrow\infty.
\tag{6.8}
\]

Adding the annular gradient energy changes the conclusion:
\(\int|\nabla u_{A,\delta}|^2\sim A^2\delta\), and local Sobolev then
controls the \(L^3\) row.  Hence the safe alternatives are either the direct
critical \(L^3\) tail (3.2) or a weighted annular energy tail containing both
\(L^2\) and \(H^1\) information.

### 6.3 Amplitude, translation, and low frequency

For \(u\mapsto Au\) and the natural pressure scaling \(p\mapsto A^2p\),

\[
 {\cal C}^{\rm abs}_{{\mathscr S},0},\quad
 {\cal E}^{3/2},\quad {\cal P},\quad
 {\cal A}^{u,p}_{\rm ext}
\tag{6.9}
\]

all have cubic amplitude degree.  Amplitude multiplication therefore cannot
produce an unbounded ratio for the complete proposed denominator.

Moving a localized packet farther away multiplies both the Gaussian leakage
and the exact tail (3.2) by the same kernel.  It creates an unbounded ratio
only if the chosen annular proxy decays faster than the kernel bound, as in
Section 4.

A genuinely low-frequency field is spatially global rather than hidden in a
remote small packet.  If \(\|\nabla u\|_\infty\le L\), the increment formula
gives, for \(s\) below the wavelength squared,

\[
 |{\mathscr S}_s|\le CL^3s.
\tag{6.10}
\]

Its contribution to the dimensionless tent over \(Q_R\times(0,R^2)\) is
\(O(L^3R^6)\).  At a spatial node, the gradient part of
\({\cal E}^{3/2}\) has the same \(R^6\) order; away from a node, the local
\(L^2\) part is larger.  Thus a far-field low-frequency mode does not evade
the local energy row.

## 7. Harmonic-pressure audit

On the global periodic torus, a spatially harmonic pressure is constant.
That constant is removed by (5.2) and cancels identically from \(Q_s\).  It
cannot create a counterexample.

On a local ball, pressure generated by exterior sources can have a
nonconstant harmonic component.  Its oscillation is measured by
\({\cal P}\), while heat leakage from outside the larger ball is measured by
the pressure part of (5.4).  The product in the covariance has no amplitude
loophole because

\[
 |p^\sharp u|
 \le {2\over3}|p^\sharp|^{3/2}+{1\over3}|u|^3.
\tag{7.1}
\]

A large nearly constant harmonic component is harmless: its constant part
cancels from \(Q_s\), and only its locally measured oscillation remains.
This does not prove a pressure estimate from velocity alone; it shows only
that the declared \(L^{3/2}\) pressure payment has the correct degree and
blocks the proposed harmonic-pressure amplitude counterexample.

## 8. Decision on (5.3) and next proof target

The audit separates existence of an upper bound from usefulness of that
bound.

| Candidate exterior ledger | Verdict | Reason |
|---|---|---|
| no exterior row | false for unconstrained arbitrary-velocity triples with \(p=\mu=0\) | translated packet, (6.4)--(6.6) |
| Gaussian weighted \(L^2\) mass, then \(3/2\) power | false as a purely functional bound | concentration ratio \(\delta^{-3/2}\) |
| critical exact-kernel \(L^3\) velocity row (3.2) | proved sufficient for \({\mathscr S}_s\) | Proposition 3.1 |
| annular \(L^3\) row with rigorously slower Gaussian decay | proved sufficient | (4.2)--(4.3) |
| annular energy row with \(L^2\) but no gradient | insufficient | same concentration test |
| annular \(L^\infty L^2\cap L^2H^1\) row | viable upper-bound route | local Sobolev on enlarged annuli |
| pressure gauge alone | no counterexample | constants cancel from \(Q_s\) |
| local defect \({\cal M}\) used to bound absolute external \(P_s\mu\) | incomplete | requires (5.5); favorable signed use is different |

Accordingly, (5.3) can be promoted from a schematic statement to the proved
functional estimate (3.4) after freezing (3.2).  This is not yet an
epsilon-regularity criterion: \({\cal A}^{u}_{\rm ext}\) is finite for the
usual global energy class but is not shown to be small from a local
hypothesis.

The next non-circular analytic target is one of the following equivalent
bridges.

1. Prove that (3.2) is controlled by a summable all-scale annular energy
   functional whose first few radii can enter a CKN iteration.
2. Prove a local pressure decomposition whose harmonic part is bounded by
   the pressure version of (4.3), with the pressure gauge fixed explicitly.
3. Show that the resulting combined tail becomes small under a hypothesis
   strictly weaker than a known regularity criterion.

Until one of these bridges is established, Proposition 3.1 is a rigorous
ledger closure but not progress across the central regularity barrier.

## 9. Exact theorem/open ledger

The logical status of the audit is frozen as follows.

### Strict analytic statements

1. The periodic kernel comparisons (2.4)--(2.5) and the pointwise unsigned
   production bound (2.7).
2. Proposition 3.1, for precisely the energy/tail class in (3.3)--(3.4).
3. The annular majorization (4.3), with normalization
   \(R^{-2}\int_{I_R\times A_j}|u|^3\) and weights
   \(e^{-c_*4^j}\), where \(c_*\) is no larger than the constant licensed by
   the periodic heat-kernel upper bound.
4. The pointwise covariance bound (5.3).  Its scale-integrated cutoff
   corollary is strict only after the observation set and larger source ball
   described after (5.4a) are frozen consistently.
5. The arbitrary-data static falsifications in Section 6: omission of every
   exterior row, and replacement by a weighted \(L^2\)-mass row without
   gradient information.

### Statements conditional on the quantifiers

The translated packet is a counterexample only when arbitrary smooth
divergence-free fields lie in the quantified class, or when a purported PDE
proof invokes the rejected arbitrary-data functional inequality as an
intermediate step.  It is not a counterexample to an estimate quantified only
over unforced Navier--Stokes trajectories, or to an inequality requiring
\(p\) to be the pressure associated with \(u\).

### OPEN

1. Whether the exact tail (3.2) is controlled, and becomes small, under a
   genuinely local hypothesis suitable for CKN iteration.
2. Whether the full pressure/cutoff ledger can be closed with no assumption
   stronger than a known regularity criterion.
3. Whether the positive defect payment passes through the required weak
   limit while all pressure and exterior rows remain controlled.
4. Any improvement of epsilon regularity, singular-set bounds, continuation,
   or three-dimensional global regularity.

These open items are not decided by the static packet, Proposition 3.1, or
the annular heat-kernel estimate.  NOT CLAY.
