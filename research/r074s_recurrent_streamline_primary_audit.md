# R0.74S Step 17 — primary analytic audit

## 0. Audited object and verdict

This audit reviews
`research/r074s_recurrent_streamline_temporal_tail_obstruction.md`, equations
(S.445)--(S.475), at source SHA-256

```text
7d204b326be45a82bc0d8531ea2f2d894c0c125b76e3ccbf02fdc1978a6011c5
```

It also locks the two inherited inputs actually used:

```text
Step 15  2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d
Step 16  de2365c38201996276c280441ab17c6c065e74a4301106484dd1cdc88a341fb0
```

**Verdict: PASS within the stated negative-theorem scope.**  For every
finite shell-deletion budget and every (p\in[1,\infty]), a smooth exact
Taylor-vortex solution with its Version-M centre on a regular closed
streamline has

\[
 \mathfrak H^F_{p,N,R}\asymp_{p,N,R}A^3,
 \qquad P_R^M\asymp_RA^3
 \quad(A\to\infty).
\]

It therefore refutes every power-only absolute temporal-tail estimate with
payment exponent (eta<1), including (S.444).  The positive-excursion
estimate (S.472), the direct hybrid gate, the terminal-crown route, Q.12,
Q.1, scale contraction, and regularity remain open.  The example is smooth.
**NOT CLAY.**

## 1. Exact solution, orbit topology, and recurrence

Direct differentiation of

\[
 W=(\sin x_1\cos x_2,-\cos x_1\sin x_2,0),
 \qquad p_W={\cos2x_1+\cos2x_2\over4}
\]

gives

\[
 \nabla\!\cdot W=0,
 \qquad \Delta W=-2W,
 \qquad (W\!\cdot\!\nabla)W=-\nabla p_W.
\]

Since (b_A'=-2b_A), (u_A=b_AW), (p_A=b_A^2p_W) solve the unforced
periodic Navier--Stokes equations exactly for every (A>0).  This is an
identity particular to a steady Euler field that is also a Laplace
eigenfield; no general amplitude symmetry is invoked.

On (sin x_1\sin x_2=1/2) in ((0,\pi)^2), each sine is at least (1/2).
The two graphs

\[
 x_2=\arcsin\!\left({1\over2\sin x_1}\right),
 \qquad
 x_2=\pi-\arcsin\!\left({1\over2\sin x_1}\right),
 \quad {\pi\over6}\le x_1\le{5\pi\over6},
\]

join at their endpoints to form one compact oval.  The critical-point
equations would force (psi=1), so (W) is nonzero on this oval.  Thus the
trajectory (chi'=W(\chi)) on (Gamma\times\{0}) is periodic, with
(T_*=\int_\Gamma d\ell/|W|\).  Both comparison points in the note lie on
the same orbit, and (g=|W(\chi)|^2) takes the values (1/2) and (3/4).
Hence (q=g') is nonzero and periodic, (V_p>0), and (V_1\ge1/2).

For any interval of phase length (L\ge2T_*), retaining complete periods
gives

\[
 \int_a^{a+L}|q|^p\ge{V_p\over2T_*}L.
\]

No ergodic theorem or unproved recurrence statement is used.

## 2. Version-M path, exact flux, and dimensional normalization

The radial mollifier multiplies every Fourier mode of (W) by the same
real number (mu_R\to1).  Therefore

\[
 \theta_A(t)=\mu_R\int_{t_0}^{t}b_A(r)\,dr,
 \qquad X_R(t)=\chi(\theta_A(t))
\]

solves the frozen terminal-value trajectory.  On (I_R), the phase length
is

\[
 L_A={\mu_RA\over2}(e^{2R^2}-1)\asymp_RA.
\]

For the first (M=N+1) physical annuli, choosing (R) after (N) makes
(c_{k,R}\ge m_{k,R}/2>0).  The fixed-frame Bernoulli current and the
pressure gauge cancel exactly.  The moving-cutoff term is

\[
 \dot F_{k,R}
 ={\gamma_k\mu_Rc_{k,R}\over2R}\eta_Rb_A^3q(\theta_A).
\]

For finite (p), the change from physical time to the dimensionless time
(sigma) gives

\[
 \|h_{k,R}\|_p^p
 =R^{2p-2}\int|\dot F_{k,R}|^pdt.
\]

Then (d\theta=\mu_Rb_A,dt) leaves the coefficient

\[
 { (\gamma_kc_{k,R})^p\mu_R^{p-1}R^{p-2}\over2^p}
\]

before periodic averaging.  Multiplying by
(mu_RV_p(e^{2R^2}-1)A/(4T_*)) reproduces (S.456), including its
(R^{p-2}) and (2^{p+2}) factors.  At (p=\infty), (R^2/(2R)=R/2),
so (S.457) is also dimensionally exact.

For (A\ge A_0(R)), all first (N+1) coordinates have an (A^3) lower
bound.  Any deletion of at most (N) coordinates leaves one of them.
The lower bound is taken after fixing (N) and (R), exactly in the order
required to negate the universal statement.

## 3. Complete payment and exponent negation

Translations along the compact orbit do not change the norms of the fixed
smooth profiles.  On the frozen interval, the local-energy, exterior,
quadratic-cutoff, and harmonic rows have the bounds displayed in (S.460).
The super-Gaussian all-copy sum and the algebraic order-(-4) harmonic sum
remain summable.  Thus no pressure or exterior payment row is dropped.

The terminal local-energy trace is a positive constant times (A^2), so
its (3/2) power supplies the lower bound (P_R^M\ge c_RA^3); the complete
row audit gives (P_R^M\le C_RA^3).  Consequently, for (eta\ge0) the
upper payment bound and for (eta<0) the lower payment bound give

\[
 {\mathfrak H^F_{p,N,R}\over(P_R^M)^\beta}
 \gtrsim_{p,N,R,\beta}A^{3(1-\beta)}\to\infty
 \qquad(\beta<1).
\]

This is the exact negation of (S.444) at (p=1,eta=2/3), and proves the
stronger stated no-go theorem.  It is not an assertion that a linear-payment
bound holds.

## 4. Signed range, ordered excursion, and backtracking

Because (d_tg(\theta_A)=\mu_Rb_Aq(\theta_A)), integration by parts gives

\[
 F_k(b)-F_k(a)={\gamma_kc_{k,R}\over2R}
 \left([\eta_Rb_A^2g]_a^b
 -\int_a^b(\eta_R'b_A^2-4\eta_Rb_A^2)g\,dt\right).
\]

The sign (-4) follows from ((b_A^2)'=-4b_A^2).  Since the cutoff is
nondecreasing and has total derivative mass one, the all-shell signed range
is (O_R(A^2)).

The lower bound needed for the one-sided functional uses an ordered pair,
not merely two-sided oscillation.  Along the lower branch, the positive
(W)-orientation runs from ((\pi/4,\pi/4)) to
((\pi/2,\pi/6)).  Taking phases (-T_*) and (-T_*+s_*) produces
(a<b), (g(b)-g(a)=1/4), and

\[
 F_k(b)-F_k(a)
 ={\gamma_kc_{k,R}\over2R}
 \left({A^2\over4}+O_R(A)+4\int_a^bb_A^2g\,dt\right)>0
\]

for large (A).  The (N+1) pigeonhole therefore proves the lower half of
(S.471) for the forward positive excursion itself.

At (p=1), (mathfrak H^F) is exactly the best-(N) sum of total
variations.  Jordan decomposition gives

\[
 \operatorname{TV}F=|F(t_0^-)|+2\min(V^+,V^-).
\]

The coordinatewise lower bound comes from (S.456), not from the aggregate
(S.459).  Together with the coordinatewise upper bound and the (A^2)
range estimate, it proves an (A^3) backtracking debt on every activated
shell.

## 5. Minimax and completed-clock inequalities

For each fixed deletion set (S) and every terminal (	au),

\[
 \inf_{\#S_\tau\le N}\sum_{k\notin S_\tau}z_k(\tau)
 \le\sum_{k\notin S}z_k(\tau)
 \le\sum_{k\notin S}\operatorname{osc}^+F_k.
\]

Taking the terminal supremum and then the infimum over the fixed (S)
proves the first inequality in (S.470).  Hence no invalid exchange of
(sup) and (inf) occurs: the positive-excursion target is deliberately
stronger than the direct Step-15 gate, whose deletion may depend on
(	au).

For (K=F+Q\ge0) with common zero start, coordinatewise one has

\[
 o_F\le m_K+\operatorname{TV}Q,
 \qquad m_K\le o_F+\operatorname{TV}Q,
\]

\[
 \operatorname{Var}^+K\le\operatorname{TV}F+\operatorname{TV}Q,
 \qquad
 \operatorname{TV}F\le2\operatorname{Var}^+K+\operatorname{TV}Q,
 \qquad m_K\le\operatorname{Var}^+K.
\]

The factor two follows from
(operatorname{Var}^-K\le\operatorname{Var}^+K).  Selecting an
approximating deletion set for the functional on the right and paying the
whole (B_{Q,R}) proves every optimized inequality in (S.475).  The false
absolute-tail theorem is therefore positive-variation packing; the open
successor asks only for maximal-height/positive-excursion packing.

## 6. Source and claim boundary

Taylor (1923) is used only for historical provenance of the exact vortex.
The recurrence, deletion, flux, and payment arguments above are direct.
The bounded comparison search in the main note concerns nearby maximal,
physical-flux, local-pressure, and local-energy-defect architectures; it is
not a novelty or priority claim and is not a premise of the proof.

The licensed promotion is exactly:

\[
 \boxed{\text{Every power-only absolute temporal tail with }\beta<1
 \text{ is false in the frozen Version-M class.}}
\]

No conclusion about singularity formation or the Millennium problem follows
from this smooth counterexample.
