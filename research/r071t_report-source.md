# R0.71T -- A genuine smooth internal entry rules out bare Leray-time payment, while outgoing occupation gives an exact scale-matched representation

**Date:** 2026-08-26

**Audience:** analysts working on three-dimensional incompressible
Navier--Stokes regularity, localized Littlewood--Paley observables, temporal
occupation measures, critical scaling, and parabolic packing

**Status:** release source.  This report constructs a smooth periodic
Navier--Stokes solution with a genuine positive-time internal zero of the
R0.71P target observable.  A two-parameter amplitude--frequency family then
proves that the corresponding scale-invariant entry atom cannot be paid by
the bare time integral of the normalized Leray \(\dot H^{-1}\) Lamb budget
with a uniform constant, even while the initial energy and critical
\(\dot H^{1/2}\) norm tend to zero and the initial enstrophy stays bounded.
The report also proves an exact outgoing-coarea representation, a finite
conditional trace--variation estimate with the complete variable-enstrophy
ledger, and a Leray-paid amplitude-excursion alternative for fixed packets.
No summed occupation bound, recurrence theorem, continuation criterion,
singularity, global regularity, novelty, or priority result is claimed.

## 0. Direct decision

R0.71S proved a two-derivative scaling obstruction using a genuine NSE
observation-boundary entry, but left open the possibility that positive-time
internal dynamics might repair the payment.  R0.71T closes that caveat.

For the seed

\[
 U(x)=(0,\cos x_1,\cos x_2),
 \tag{0.1}
\]

the quadratic projected Lamb field lies on the Fourier shell \(|k|^2=2\),
whereas \(U\) itself lies on \(|k|^2=1\).  Fix a small time \(\tau>0\).
A finite-dimensional implicit-function argument changes only the initial
target shell by

\[
 z(a)=-a^2\tau F_*+O(a^3)
 \tag{0.2}
\]

so that the entire target shell vanishes exactly at time \(\tau\).  At that
time its nonlinear forcing remains

\[
 F_j(\tau)=a^2e^{-2\nu\tau}F_*+O(a^3)\ne0.
 \tag{0.3}
\]

The zero is therefore simple, strictly inside the observation interval, and
has positive entry atom

\[
 \kappa_j^{-2}A_+(a)
 =\frac{a^2e^{-2\nu\tau}}4+O(a^3).
 \tag{0.4}
\]

Now choose the base amplitude \(a_\lambda=\lambda^{-2}\) and apply the exact
integer NSE dilation.  The scaled atom is of order \(\lambda^{-4}\), whereas
the bare normalized Leray--Lamb time budget is of order \(\lambda^{-6}\).
Their ratio grows like

\[
 \frac{2\nu}{\sinh(2\nu\tau)}\lambda^2.
 \tag{0.5}
\]

This is a genuine smooth positive-time internal counterfamily to the proposed
bare payment.  It is not an abstract forced path and does not rely on an
initial observation face.

The negative result does not make every internal dynamical route impossible.
Two scale-matched objects survive the audit.

1. An outgoing radial occupation density represents every finite-order
   right-entry atom exactly, including even touches.
2. A symmetric trace identity pays a finite family conditionally from strong
   shell-Lamb, \(F_t\), and \(Y_t\) variation budgets.

Neither right side is presently controlled by the Leray energy inequality.
The open problem has therefore moved from locating an internal event to
paying a scale-zero occupation or jet charge across all relevant events.

## 1. Setting and inherited entry atom

Work on the normalized three-torus.  Let \(u\) be a zero-mean classical
solution of

\[
 \partial_tu-\nu\Delta u
 =\mathbb P(u\times\omega)=:L,
 \qquad
 \omega=\operatorname{curl}u,
 \qquad
 \operatorname{div}u=0,
 \tag{1.1}
\]

on an interval containing \([0,2\tau]\).  Let \(T_j\) be a real-even
annular Fourier multiplier, and put

\[
 W_j=T_j\omega,
 \qquad
 F_j=T_jL,
 \qquad
 Y=\|\omega\|_2^2.
 \tag{1.2}
\]

For a nonnegative smooth cell cutoff \(\chi_Q\), define

\[
 C_{j,Q}=\operatorname{curl}(\chi_QW_j).
 \tag{1.3}
\]

At an isolated finite-order zero \(t_\beta\), write

\[
 C_{j,Q}(t_\beta+s)
 =c_\beta s^{m_\beta}+O_{L^2}(|s|^{m_\beta+1}),
 \qquad c_\beta\ne0.
 \tag{1.4}
\]

The right and left directional faces are

\[
 A_{\beta,+}
 =\frac{\langle F_j(t_\beta),c_\beta\rangle_+^2}
 {Y(t_\beta)\|c_\beta\|_2^2},
 \tag{1.5}
\]

\[
 A_{\beta,-}
 =\frac{\langle F_j(t_\beta),(-1)^{m_\beta}c_\beta\rangle_+^2}
 {Y(t_\beta)\|c_\beta\|_2^2}.
 \tag{1.6}
\]

The inherited target is the scale-invariant atom

\[
 a_\beta=\kappa_j^{-2}A_{\beta,+}.
 \tag{1.7}
\]

An **internal entry** means \(t_\beta\) lies strictly inside the declared
half-open observation interval.  It is not an initial trace and is not the
right endpoint.

Under the compatible fixed-torus scaling

\[
 u_\lambda(x,t)=\lambda u(\lambda x,\lambda^2t),
 \tag{1.8}
\]

with covariantly scaled multiplier, cutoff, and event, the relevant exponents
are

| Quantity | Scale exponent \(\sigma\) in \(q_\lambda(t)=\lambda^\sigma q(\lambda^2t)\) |
|---|---:|
| \(\kappa_j\) | \(+1\) |
| \(Y\) | \(+4\) |
| \(\|F_j\|_2\) | \(+3\) |
| \(\langle F_j,c/\|c\|\rangle\) | \(+3\) |
| \(A_+\) | \(+2\) |
| \(\kappa_j^{-2}A_+\) | \(0\) |
| \(\|L\|_{\dot H^{-1}}^2/Y\) | \(0\) |
| \(\int\|L\|_{\dot H^{-1}}^2/Y\,dt\) | \(-2\) |

R0.71S showed that the last two rows already obstruct a covariant payment
including the initial face.  Sections 2--5 prove that the same obstruction
occurs at a positive-time internal entry.

## 2. The exact seed and its target shell

Take \(U\) from (0.1).  Its vorticity is

\[
 \Omega=\operatorname{curl}U
 =(-\sin x_2,0,-\sin x_1).
 \tag{2.1}
\]

With normalized torus integrals,

\[
 \|\Omega\|_2^2=1.
 \tag{2.2}
\]

The Leray-projected Lamb field is

\[
 F_*=\mathbb P(U\times\Omega)
 =(0,0,\cos x_1\sin x_2).
 \tag{2.3}
\]

It is supported exactly on the four modes

\[
 (\pm1,\pm1,0),
 \tag{2.4}
\]

and hence on the radius \(\rho=\sqrt2\).  Its exact ledger is

\[
 \|F_*\|_2^2=\frac14,
 \qquad
 \|\operatorname{curl}F_*\|_2^2=\frac12,
 \tag{2.5}
\]

\[
 -\Delta F_*=2F_*,
 \qquad
 \|-\Delta F_*\|_2^2=1,
 \qquad
 \langle F_*,-\Delta F_*\rangle=\frac12.
 \tag{2.6}
\]

Let \(P_*\) be the real Fourier projection onto (2.4).  Then

\[
 P_*U=0,
 \qquad
 P_*\Omega=0,
 \qquad
 P_*\mathbb P(U\times\Omega)=F_*.
 \tag{2.7}
\]

These identities are finite Fourier algebra.  The exact and independent
certificates reconstruct them without using a time integrator.

## 3. Prescribing a positive-time full-shell zero

This section supplies the functional-analytic step that no finite script can
replace.

### 3.1 Finite-dimensional target space and local flow

Fix \(s>5/2\).  Let \(E_*\) be the finite-dimensional real, conjugation-
closed, divergence-free velocity space supported on (2.4).  The projection
\(P_*:H^{s+2}_\sigma\to E_*\) is bounded.

For smooth initial data near zero, standard periodic strong-solution theory
gives a common time interval and a fixed-time solution map

\[
 S_t:H^{s+2}_\sigma\supset\mathcal U
 \longrightarrow H^{s+2}_\sigma
 \tag{3.1}
\]

that is \(C^1\), indeed smooth on this finite-dimensional parameter family.
At the zero solution,

\[
 DS_\tau(0)h=e^{\nu\tau\Delta}h.
 \tag{3.2}
\]

Only this standard local flow result is used.  The construction does not
solve NSE backward and does not assert that \(S_\tau\) is locally onto in an
infinite-dimensional space.

### 3.2 Implicit-function theorem

For a scalar amplitude \(a\) and \(z\in E_*\), define

\[
 \Phi(a,z)=P_*S_\tau(aU+z).
 \tag{3.3}
\]

At \((a,z)=(0,0)\),

\[
 \Phi(0,0)=0,
 \qquad
 D_z\Phi(0,0)
 =e^{-2\nu\tau}I_{E_*}.
 \tag{3.4}
\]

The derivative is an invertible finite matrix.  The ordinary implicit-
function theorem therefore gives \(a_0>0\) and a smooth map

\[
 z:(-a_0,a_0)\to E_*,
 \qquad z(0)=0,
 \tag{3.5}
\]

such that

\[
 \boxed{P_*S_\tau(aU+z(a))=0.}
 \tag{3.6}
\]

Because curl is invertible on the nonzero finite shell, (3.6) is equivalent
to

\[
 T_*\omega^a(\tau)=0,
 \tag{3.7}
\]

where \(u^a=S_t(aU+z(a))\) and \(T_*\) is the corresponding vorticity-shell
projection.

The real/conjugate structure is preserved: \(E_*\), \(P_*\), the heat
semigroup, and the NSE flow all commute with conjugation, so the IFT solution
can be taken real valued.

### 3.3 Quadratic Duhamel expansion

The first derivative of \(\Phi\) with respect to \(a\) vanishes because the
linear heat evolution of \(U\) stays on \(|k|^2=1\).  At quadratic order,

\[
 e^{\nu(\tau-r)\Delta}P_*
 \mathbb P\bigl((e^{\nu r\Delta}U)
 \times\operatorname{curl}(e^{\nu r\Delta}U)\bigr)
 =e^{-2\nu\tau}F_*.
 \tag{3.8}
\]

The integrand is constant after the common heat factor is extracted.  Thus

\[
 \Phi(a,z)
 =e^{-2\nu\tau}igl(z+a^2\tau F_*\bigr)
 +O(\|z\|^2+|a|\|z\|+|a|^3)
 \tag{3.9}
\]

in \(E_*\).  Substitution of (3.6) gives

\[
 \boxed{z(a)=-a^2\tau F_*+O(a^3).}
 \tag{3.10}
\]

For fixed sufficiently small \(\tau\), all remainders are uniform as
\(a\to0\).  Shrinking \(a_0\) if needed gives a common classical existence
interval containing \([0,2\tau]\).

### 3.4 The forcing remains nonzero at the prescribed root

At time \(\tau\), the leading low shell is

\[
 a e^{-\nu\tau}U+O(a^2).
 \tag{3.11}
\]

Consequently,

\[
 \boxed{
 F_*(u^a(\tau))
 :=P_*\mathbb P(u^a(\tau)\times\omega^a(\tau))
 =a^2e^{-2\nu\tau}F_*+O(a^3).}
 \tag{3.12}
\]

The leading coefficient is nonzero.  Hence (3.12) is nonzero for every
sufficiently small \(a\ne0\).

### Theorem 3.1 -- genuine smooth internal positive entry

For every sufficiently small fixed \(\tau>0\), there is \(a_0>0\) such that
each \(0<|a|<a_0\) has a smooth periodic NSE solution \(u^a\) on
\([0,2\tau]\) with initial datum

\[
 u_0^a=aU+z(a),
 \qquad
 z(a)=-a^2\tau F_*+O(a^3),
 \tag{3.13}
\]

for which the global target-shell observable has a simple positive zero at
the strictly internal time \(t=\tau\).

#### Proof

Equation (3.7) gives \(W_*(\tau)=0\), hence

\[
 C_*(\tau)=\operatorname{curl}W_*(\tau)=0.
 \tag{3.14}
\]

The filtered vorticity equation is

\[
 \partial_tW_* -\nu\Delta W_*
 =\operatorname{curl}F_* (u^a).
 \tag{3.15}
\]

Taking one more curl and evaluating at \(W_*(\tau)=0\) gives

\[
 C_{*,t}(\tau)
 =\operatorname{curl}\operatorname{curl}F_*(u^a(\tau))
 =-\Delta F_*(u^a(\tau)).
 \tag{3.16}
\]

The target forcing is divergence free, annular, and nonzero by (3.12).
Therefore

\[
 \langle F_*(u^a(\tau)),C_{*,t}(\tau)\rangle
 =\|\nabla F_*(u^a(\tau))\|_2^2>0.
 \tag{3.17}
\]

In particular \(C_{*,t}(\tau)\ne0\), so the zero is simple.  The interval
\([0,2\tau)\) places it strictly inside the observation window. \(\square\)

### 3.5 Exact leading atom

At the event,

\[
 Y^a(\tau)=a^2e^{-2\nu\tau}+O(a^3),
 \tag{3.18}
\]

\[
 \|F_*(u^a(\tau))\|_2^2
 =\frac{a^4e^{-4\nu\tau}}4+O(a^5).
 \tag{3.19}
\]

On the single radius \(\rho^2=2\) with nominal \(\kappa=1\),
\(C_t=2F\).  Hence

\[
 A_+(a)=\frac{\|F_*(u^a(\tau))\|_2^2}{Y^a(\tau)}
 =\frac{a^2e^{-2\nu\tau}}4+O(a^3),
 \qquad
 A_-(a)=0.
 \tag{3.20}
\]

This proves (0.4).

## 4. Global and localized transversality

The construction above uses a full-shell zero.  It also exposes exactly which
parts extend to arbitrary roots.

### Lemma 4.1 -- every positive global-shell entry is simple

Let \(\chi\equiv1\), and let a finite-order global-shell zero satisfy
\(A_+>0\).  Then the zero has order one and \(A_-=0\).

#### Proof

The annular field \(W_j\) is divergence free and zero mean.  If
\(C_j=\operatorname{curl}W_j=0\), then \(W_j\) is also curl free, so its
Fourier coefficients vanish and \(W_j=0\).  At the zero,

\[
 C_{j,t}=-\Delta F_j.
 \tag{4.1}
\]

If the root had order greater than one, then \(C_{j,t}=0\), hence
\(-\Delta F_j=0\).  Annular zero mean forces \(F_j=0\), which makes every
pairing in (1.5) zero and contradicts \(A_+>0\).  Thus the root is simple.
Moreover,

\[
 \langle F_j,C_{j,t}\rangle
 =\langle F_j,-\Delta F_j\rangle
 =\|\nabla F_j\|_2^2>0,
 \tag{4.2}
\]

so its left direction is the negative of its right direction and
\(A_-=0\). \(\square\)

Lemma 4.1 removes the even-touch cancellation for global-shell positive
entries.  It does not bound how many such entries occur or the total
variation of their face values.

### 4.1 What fails at an arbitrary localized zero

For \(C_Q=\operatorname{curl}(\chi_QW_j)\), the exact equation is

\[
\begin{aligned}
 (\partial_t-\nu\Delta)C_Q
 ={}&\operatorname{curl}(\chi_Q\operatorname{curl}F_j)\\
 &-\nu\operatorname{curl}\!\left(
 2\nabla\chi_Q\cdot\nabla W_j+(\Delta\chi_Q)W_j
 \right).
\end{aligned}
 \tag{4.3}
\]

A localized root \(C_Q=0\) does not imply \(W_j=0\).  The commutator in
(4.3) may remain nonzero, its pairing with \(F_j\) has no fixed sign, and
\(C_{Q,t}=0\) does not force \(F_j=0\).  Therefore a general localized
positive even touch is not excluded.

### Proposition 4.2 -- a full-shell root induces a positive local cell

Suppose the stronger condition \(W_j(t_*)=0\) holds, let
\(\chi_Q\ge0\), and assume

\[
 \sum_Q\chi_Q\ge c_\chi>0.
 \tag{4.4}
\]

Then at least one cell has a simple positive entry whenever \(F_j(t_*)\ne0\).

Indeed the commutator vanishes at the full-shell root and

\[
 c_Q=C_{Q,t}(t_*)
 =\operatorname{curl}(\chi_Q\operatorname{curl}F_j(t_*)),
 \tag{4.5}
\]

while periodic curl self-adjointness gives

\[
 \boxed{
 \langle F_j(t_*),c_Q\rangle
 =\int_{\mathbb T^3}\chi_Q
 |\operatorname{curl}F_j(t_*)|^2\,dx.}
 \tag{4.6}
\]

Summing (4.6) over \(Q\) is strictly positive.  At least one term is
positive, and that term also has \(c_Q\ne0\).  The R0.71T construction
therefore produces not only a global internal entry but at least one genuine
localized simple positive response for any declared nonnegative covering
partition.

## 5. Internal scaling no-go with bounded initial energy and enstrophy

The base small-amplitude family has a precise leading bare budget.

### 5.1 Base budget

On \([0,2\tau]\),

\[
 L^a(t)=a^2e^{-2\nu t}F_*+O(a^3),
 \qquad
 Y^a(t)=a^2e^{-2\nu t}+O(a^3).
 \tag{5.1}
\]

Since \(F_*\) is supported on \(|k|^2=2\),

\[
 \|F_*\|_{\dot H^{-1}}^2
 =\frac12\|F_*\|_2^2
 =\frac18.
 \tag{5.2}
\]

It follows that

\[
\begin{aligned}
 R(a)
 &:=\int_0^{2\tau}
 \frac{\|L^a(t)\|_{\dot H^{-1}}^2}{Y^a(t)}\,dt\\
 &=\frac{a^2}{8}\int_0^{2\tau}e^{-2\nu t}\,dt+O(a^3)\\
 &=\frac{a^2(1-e^{-4\nu\tau})}{16\nu}+O(a^3).
\end{aligned}
 \tag{5.3}
\]

### 5.2 Double scaling

Let \(\lambda\) run through compatible positive integers, dyadic integers if
required by the multiplier indexing.  For each \(\lambda\), first take the
base member with

\[
 a_\lambda=\lambda^{-2},
 \tag{5.4}
\]

and then define

\[
 u_\lambda(x,t)
 =\lambda u^{a_\lambda}(\lambda x,\lambda^2t).
 \tag{5.5}
\]

Scale the target shell, cutoffs, and observation interval covariantly.  The
base internal time \(\tau\) becomes \(\tau/\lambda^2\), still strictly
inside \([0,2\tau/\lambda^2)\).

The atom is invariant under the second, covariant step, so (3.20) gives

\[
 a_{\beta,\lambda}
 =\frac{e^{-2\nu\tau}}{4\lambda^4}
 +O(\lambda^{-6}).
 \tag{5.6}
\]

The time integral acquires the additional scaling factor \(\lambda^{-2}\),
so (5.3) gives

\[
 R_\lambda
 =\frac{1-e^{-4\nu\tau}}{16\nu\lambda^6}
 +O(\lambda^{-8}).
 \tag{5.7}
\]

Therefore

\[
 \boxed{
 \frac{a_{\beta,\lambda}}{R_\lambda}
 =\frac{2\nu}{\sinh(2\nu\tau)}\lambda^2
 +o(\lambda^2).}
 \tag{5.8}
\]

### 5.3 Initial data do not grow in the energy scales

The precompensation has size \(O(a_\lambda^2)\), so the scaled initial data
satisfy

\[
 \|u_\lambda(0)\|_2^2=O(\lambda^{-2}),
 \tag{5.9}
\]

\[
 \|u_\lambda(0)\|_{\dot H^{1/2}}^2=O(\lambda^{-1}),
 \tag{5.10}
\]

\[
 \|\omega_\lambda(0)\|_2^2=1+o(1).
 \tag{5.11}
\]

Thus energy tends to zero, the critical norm tends to zero, and enstrophy
stays bounded.  In particular, for large \(\lambda\) the standard small
critical-data theory places these solutions in the global smooth class.  The
counterfamily is not caused by a growing energy ledger or by approaching an
unknown singularity.

### Theorem 5.1 -- no uniform bare payment for internal entries

There is no constant \(C\), uniform along the family (5.5), such that

\[
 \sum_{\beta\in\mathcal E_{\lambda,\mathrm{int}}}
 \kappa_{j(\beta)}^{-2}A_{\beta,+}
 \le C
 \int_0^{2\tau/\lambda^2}
 \frac{\|L_\lambda(t)\|_{\dot H^{-1}}^2}
 {Y_\lambda(t)}\,dt
 \tag{5.12}
\]

for every member, whenever \(\mathcal E_{\lambda,\mathrm{int}}\) contains
the constructed internal entry.

#### Proof

The left side is at least (5.6), the right side is \(C\) times (5.7), and
their quotient diverges by (5.8). \(\square\)

The theorem also excludes the same universal statement when it is advertised
for all Leray--Hopf or suitable solutions, because the counterfamily consists
of smooth classical solutions and belongs to both larger classes.

The theorem does not exclude:

1. a constant depending on high Sobolev norms or the full initial profile and
   growing at least like \(\lambda^2\);
2. a fixed-frequency or noncovariant observation theorem;
3. an added initial, BV, atomic, strong-Lamb, or material-derivative charge;
4. a result for one fixed trajectory with a trajectory-dependent constant;
5. a weak singular-time statement for which the finite-order entry itself has
   not yet been defined.

## 6. Exact outgoing-coarea representation

The bare budget fails, but a scale-matched zero-level occupation quantity
represents the atom exactly.

Let \(K\) be a compact classical interval whose endpoints are not zeros, let
the index family \(\Lambda\) be finite, and assume every zero of every
\(C_\alpha\), \(\alpha\in\Lambda\), is isolated and of finite order.  Put

\[
 r_\alpha(t)=\|C_\alpha(t)\|_2,
 \qquad
 \xi_\alpha(t)=\frac{C_\alpha(t)}{r_\alpha(t)}
 \quad\text{when }r_\alpha(t)>0,
 \tag{6.1}
\]

\[
 q_\alpha(t)
 =\frac{\langle F_{j(\alpha)}(t),\xi_\alpha(t)\rangle_+^2}
 {Y(t)}.
 \tag{6.2}
\]

Choose \(\rho\in C_c^\infty((0,1))\), \(\rho\ge0\),
\(\int_0^1\rho=1\), and set

\[
 \rho_\delta(s)=\delta^{-1}\rho(s/\delta).
 \tag{6.3}
\]

### Theorem 6.1 -- finite internal outgoing-coarea identity

Under the preceding hypotheses,

\[
\boxed{
\begin{aligned}
 &\sum_{\alpha\in\Lambda}
 \sum_{\substack{t_*\in K\\C_\alpha(t_*)=0}}
 \kappa_{j(\alpha)}^{-2}A_{\alpha,+}(t_*)\\
 &\qquad=
 \lim_{\delta\downarrow0}
 \sum_{\alpha\in\Lambda}\kappa_{j(\alpha)}^{-2}
 \int_K q_\alpha(t)\rho_\delta(r_\alpha(t))
 (r_{\alpha,t}(t))_+\,dt.
\end{aligned}}
 \tag{6.4}
\]

#### Proof

Near one zero of order \(m\),

\[
 C(t_*+s)=cs^m+O_{L^2}(|s|^{m+1}),
 \tag{6.5}
\]

so on the right

\[
 r(t_*+s)=\|c\|s^m(1+O(s)),
 \qquad
 \xi(t_*+s)\to \frac c{\|c\|}.
 \tag{6.6}
\]

For small \(\delta\), \(r\) is increasing on the right neighborhood and
decreasing toward the zero on the left neighborhood.  The factor
\((r_t)_+\) removes the left side.  On the right, the change of variables
\(y=r(t)\) gives

\[
 \int q(t)\rho_\delta(r(t))(r_t)_+\,dt
 \longrightarrow q(t_*+)=A_+(t_*).
 \tag{6.7}
\]

The same argument works for odd crossings and even touches.  Summing over
finitely many disjoint zero neighborhoods proves (6.4). \(\square\)

### 6.1 NSE radial identity

If a localized observable satisfies

\[
 C_t-\nu\Delta C=G,
 \tag{6.8}
\]

then wherever \(r>0\),

\[
\boxed{
 r_t
 =\langle\xi,G\rangle
 -\nu\frac{\|\nabla C\|_2^2}{r}.}
 \tag{6.9}
\]

Moreover, incompressibility gives

\[
 \langle C,u\cdot\nabla C\rangle=0,
 \tag{6.10}
\]

so the same radial derivative can be written with the material derivative
inside the pairing.

The density in (6.4) has scale exponent \(+2\), and its time integral is
scale zero, matching the entry atom.  This resolves the scale mismatch at the
level of representation.

It does not resolve the a priori estimate.  The elementary bound

\[
 (r_t)_+\le\|G\|_2
 \tag{6.11}
\]

leaves \(\rho_\delta(r)\), whose height is of order \(\delta^{-1}\).  An
ordinary \(L_t^pG\) estimate does not control this concentration uniformly as
\(\delta\downarrow0\).  A new outgoing-level Carleson, occupation, or
transversality estimate would be required.

## 7. A finite conditional trace--variation payment

There is a second scale-matched route for a finite entry family.  It avoids a
sampling-coherence assumption but pays with strong time variation.

For each event \(\beta\), keep the fixed direction

\[
 e_\beta=\frac{c_\beta}{\|c_\beta\|_2},
 \qquad
 f_\beta(t)
 =\frac{\langle F_{j(\beta)}(t),e_\beta\rangle}{\sqrt{Y(t)}},
 \qquad
 q_\beta=(f_\beta^+)^2.
 \tag{7.1}
\]

Use a symmetric window

\[
 I_\beta=[t_\beta-h_\beta,t_\beta+h_\beta],
 \qquad
 h_\beta=\theta_\beta\kappa_{j(\beta)}^{-2},
 \qquad
 \theta_\beta\ge\theta_->0.
 \tag{7.2}
\]

Define

\[
 K_h(s)=
 \begin{cases}
 (s+h)/(2h),&-h\le s\le0,\\
 (s-h)/(2h),&0\le s\le h.
 \end{cases}
 \tag{7.3}
\]

For every \(q\in W^{1,1}(-h,h)\), integration by parts gives the exact
identity

\[
 \boxed{
 q(0)=\frac1{2h}\int_{-h}^hq(s)\,ds
 +\int_{-h}^hK_h(s)q_t(s)\,ds.}
 \tag{7.4}
\]

Since \(|K_h|\le1/2\),

\[
 \kappa_j^{-2}A_{\beta,+}
 \le\frac1{2\theta_\beta}\int_{I_\beta}q_\beta\,dt
\frac{\kappa_j^{-2}}2\int_{I_\beta}|q_{\beta,t}|\,dt.
 \tag{7.5}
\]

### 7.1 The denominator cannot be frozen

Because \(e_\beta\) is fixed,

\[
 \boxed{
 f_{\beta,t}
 =\frac{\langle F_{j,t},e_\beta\rangle}{\sqrt Y}
 -\frac{Y_t}{2Y}f_\beta,}
 \tag{7.6}
\]

and

\[
 \boxed{
 q_{\beta,t}
 =2f_\beta^+
 \frac{\langle F_{j,t},e_\beta\rangle}{\sqrt Y}
 -\frac{Y_t}{Y}q_\beta.}
 \tag{7.7}
\]

The exponential test \(g=e^{bt}\), \(Y=e^{2bt}\) has
\(f=g/\sqrt Y\equiv1\).  The two terms in (7.6) cancel exactly.  Omitting the
denominator derivative would create a nonexistent variation charge.

### Theorem 7.1 -- finite active-direction trace payment

Assume the finite family satisfies, for every shell \(j\), time \(t\), and
spatial vector \(v\),

\[
 \sum_{\substack{\beta:j(\beta)=j\\t\in I_\beta}}
 |\langle v,e_\beta\rangle|^2
 \le\mathcal B\|v\|_2^2.
 \tag{7.8}
\]

Then

\[
\boxed{
\begin{aligned}
 \sum_\beta\kappa_{j(\beta)}^{-2}A_{\beta,+}
 \le{}&\frac{\mathcal B}{2\theta_-}
 \int\sum_j\frac{\|F_j\|_2^2}{Y}\,dt\\
 &+\mathcal B\int\sum_j\kappa_j^{-2}
 \frac{\|F_j\|_2\|F_{j,t}\|_2}{Y}\,dt\\
 &+\frac{\mathcal B}{2}\int\frac{|Y_t|}{Y^2}
 \sum_j\kappa_j^{-2}\|F_j\|_2^2\,dt.
\end{aligned}}
 \tag{7.9}
\]

#### Proof

Sum (7.5).  Apply (7.8) to the local-mean terms.  For the first term in
(7.7), apply Cauchy--Schwarz to the active directional coefficients of
\(F_j\) and \(F_{j,t}\), followed by (7.8) twice.  Apply (7.8) directly to
the denominator term.  This gives (7.9). \(\square\)

Every density on the right of (7.9) has the correct total NSE scale after
time integration.  None is a bare Leray quantity:

1. the first uses strong \(L_x^2\) shell Lamb rather than
   \(\dot H_x^{-1}\) Lamb;
2. the second uses time/material variation of the Lamb field;
3. the third uses normalized enstrophy variation;
4. \(\mathcal B\) counts repeated active directions and can grow with
   recurrence.

Thus Theorem 7.1 is a rigorous finite conditional theorem, not a closure.

## 8. A Leray-paid amplitude-excursion alternative

The literature audit identifies one internal dynamical quantity that the
ordinary energy inequality does pay.

Let \(u\) be a Leray--Hopf solution on \(I=[s,t]\), fix a smooth
time-independent divergence-free packet \(\psi\), and set

\[
 b_\psi(\tau)=\langle u(\tau),\psi\rangle.
 \tag{8.1}
\]

The weak equation gives

\[
 b_\psi'
 =-\nu(\nabla u,\nabla\psi)
 +\int u\otimes u:\nabla\psi.
 \tag{8.2}
\]

With

\[
 E_I=\operatorname*{ess\,sup}_I\|u\|_2^2,
 \qquad
 D_I=\int_I\|\nabla u\|_2^2,
 \tag{8.3}
\]

Cauchy--Schwarz gives

\[
 \boxed{
 V_I^+(b_\psi)
 \le\nu\|\nabla\psi\|_2(|I|D_I)^{1/2}
 +\|\nabla\psi\|_\infty E_I|I|.}
 \tag{8.4}
\]

If the internal positive components have heights \(m_k\), then

\[
 \sum_km_k\le V_I^+(b_\psi),
 \qquad
 N_\delta\le\delta^{-1}V_I^+(b_\psi).
 \tag{8.5}
\]

Equation (8.5) pays positive excursions or entries that reach a fixed
amplitude.  It cannot pay raw zero crossings: the functions
\(N^{-1}\sin Nt\) have uniformly bounded variation and an unbounded number of
positive entries.  This functional example is not an NSE counterexample, but
it explains why an amplitude threshold changes the problem materially.

## 9. Relation to checked primary literature

The standard flow-map input is consistent with the classical strong-solution
framework of Fujita--Kato
([DOI 10.1007/BF00276188](https://doi.org/10.1007/BF00276188)), Kato
([DOI 10.1007/BF01174182](https://doi.org/10.1007/BF01174182)), and Temam's
periodic treatment
([open book PDF](https://ftp.mi.fu-berlin.de/pub/klima/NavierStokes/Temam-NavierStokesEquationsAndNonlinearFunctionalAnalysis.pdf)).
These sources support local strong evolution and regular-interval
analyticity, not a raw zero-count estimate.

The other checked interfaces control different quantities.

- Caffarelli--Kohn--Nirenberg
  ([DOI 10.1002/cpa.3160350604](https://doi.org/10.1002/cpa.3160350604))
  controls local energy and singular-set size.  The R0.71T event occurs in a
  smooth solution and carries no anomalous defect.
- Dascaliuc--Grujić
  ([arXiv:1101.2193](https://arxiv.org/abs/1101.2193)) controls ensemble- and
  time-averaged physical-scale flux under additional cascade hypotheses, not
  every directional zero entry.
- Koch--Tataru
  ([author PDF](https://math.berkeley.edu/~tataru/papers/nas.pdf)) supplies
  upper critical parabolic Carleson norms for small data, not a lower mass per
  coefficient zero.
- de Simon
  ([primary PDF](https://www.numdam.org/item/RSMUP_1964__34__205_0.pdf)) gives
  maximal regularity when the forcing is already in an appropriate
  \(L^p\) class.  General three-dimensional Leray data do not provide the
  strong \(F_t\) ledger in (7.9).
- Bertoin--Yor
  ([DOI 10.1112/blms/bdu014](https://doi.org/10.1112/blms/bdu014)) and
  Łochowski
  ([arXiv:1503.01746](https://arxiv.org/abs/1503.01746)) relate variation to
  occupation or crossings averaged over the level or over a positive band.
  They do not give a uniform pointwise count at the distinguished level zero.
- Rice
  ([DOI 10.1002/j.1538-7305.1944.tb00874.x](https://doi.org/10.1002/j.1538-7305.1944.tb00874.x))
  computes expected crossings under probabilistic nondegeneracy assumptions,
  not deterministic pathwise NSE entries.

The bounded search found no theorem that converts these interfaces into the
bare payment rejected by Theorem 5.1.  This is not a literature-exhaustion or
novelty claim.

## 10. Certificate and finite-Galerkin corroboration boundary

The exact producer checks:

1. the sparse rational Fourier seed;
2. the resonant precompensation normal form;
3. the simple-face and slope identities;
4. outgoing coarea for zero orders one through eight;
5. the symmetric trace identity on monomials through degree eight;
6. the variable-denominator cancellation;
7. the exact double-scaling coefficients and scale table.

The independent checker uses a \(32^3\) FFT, adaptive quadrature, direct
finite differences, and a floating-point scale sweep.  It imports neither the
exact producer nor its JSON output.  All checks pass at the recorded
tolerances.

The associated finite Fourier--Galerkin experiment solves a truncated smooth
ODE and shoots the target shell to zero.  Its role is to test the implemented
geometry and asymptotic signs.  It is marked

\[
 \texttt{finiteGalerkin=true},\qquad
 \texttt{pdeTimeStepping=true},\qquad
 \texttt{dns=false}.
 \tag{10.1}
\]

It is not used to prove the continuum IFT theorem or the scaling no-go.

## 11. Exact result boundary

### Proved in R0.71T

1. a finite-dimensional IFT construction of a genuine smooth positive-time
   full-shell zero for the exact NSE flow;
2. the quadratic precompensation and nonzero event-forcing expansions;
3. a simple positive global entry with
   \(A_+(a)=a^2e^{-2\nu\tau}/4+O(a^3)\);
4. at least one simple positive localized cell induced by the full-shell
   root;
5. the lemma that every positive global-shell finite-order entry is simple;
6. the two-parameter internal scaling no-go for the bare normalized
   Leray--Lamb time integral, with bounded initial energy and enstrophy;
7. the exact finite outgoing-coarea identity, including even touches;
8. the finite conditional trace--variation theorem with all
   \(F_t\), \(Y_t\), and multiplicity terms;
9. the fixed-packet amplitude-excursion estimate paid by the Leray energy
   ledger.

### Not proved

1. a summed a priori bound for the outgoing occupation density;
2. a scale-uniform sum of instantaneous full-shell jet charges;
3. a recurrence or packing bound for global or localized entries;
4. simplicity of an arbitrary localized positive entry;
5. a uniform active-direction Bessel constant;
6. control of the strong \(F_t\) and \(Y_t\) terms from the Leray inequality;
7. an extension of the finite-order entry ledger to unknown weak singular
   times;
8. a continuation criterion, singularity construction, or global regularity.

The construction is a rigorous intermediate structural result.  It rules out
one natural payment mechanism and supplies two correctly scaled replacement
objects, but it does not resolve the Millennium problem.

## 12. Route verdict and next finite gate

R0.71T changes the route in one decisive way.  The bare normalized
\(\dot H^{-1}\)-Lamb time integral is no longer an open candidate for a
uniform payment of the R0.71P internal atom.  The obstruction survives at a
genuine positive-time smooth event and along data with improving energy and
critical norm.

The next release should test the strongest surviving NSE-specific object:

\[
 q^{\rm jet}_\beta
 =\kappa_j^{-6}
 \frac{\|C_t(t_\beta)\|_2^2}{Y(t_\beta)}
 \tag{12.1}
\]

for global-shell simple entries, together with its outgoing occupation
representation.  The finite gate is to decide whether the NSE equation gives
a true summed or Carleson estimate for these jets, or whether a new recurrence
family disproves that possibility.  In parallel, the amplitude-thresholded
excursion charge (8.5) remains the conservative Leray-paid branch.

R0.71T stops before either branch closes.
