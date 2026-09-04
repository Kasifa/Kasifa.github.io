# R0.75Y primary mathematical audit

## Verdict

- Audited object:
  `research/r075y_strongly_separated_multimode_flux_payment.md`
- Current verdict: **PASS**
- Mathematical blocker count: **0**
- Release blocker count: **0**
- Claim boundary: a complete signed-flux theorem only for the strongly
  separated exact common-shear family.  **NOT CLAY.**

This audit rederives the continuum estimates.  Finite fixtures may check
the ledger and algebra, but are not represented as proof of the Gram or
complete-clock lemmas.

## 1. Assumptions and geometry

The theorem retains all assumptions used immediately:

1. `T_R=4R^2`;
2. `0<=eta_R<=1`, `eta_R(0)=0`, and
   `||eta_R'||_infinity<=C_eta R^(-2)`;
3. `0<delta_0<delta`, `a>=4delta_0`, and
   `(a+delta)R<pi/2`;
4. distinct positive integer modes
   `1<=n_1<...<n_q<=2n_1`;
5. signed-spectrum separation
   `ell delta_n>=8q`, where `ell=aR` and `delta_n` includes both every
   positive-frequency gap and `2n_1`.

The third row keeps the plateau fibre in one Euclidean torus chart.  The
last row is not cosmetic: `2n_1` is the distance between the nearest
positive and negative signed frequencies.

For `q>=2`, the dyadic band gives

\[
 (q-1)\delta_{\boldsymbol n}
 \le n_q-n_1\le n_1.
 \tag{YA.1}
\]

Thus Y.3 implies
`n_1ell>=8q(q-1)`.  The theorem is a separated high-carrier statement.

## 2. Independent Gram calculation

Let `Lambda={-n_q,...,-n_1,n_1,...,n_q}`.  The complex coefficients of a
real cosine sum obey

\[
 \sum_{\lambda\in\Lambda}|c_\lambda|^2
 =\frac12\sum_{j=1}^qA_j(t)^2=\frac12S(t)^2.
 \tag{YA.2}
\]

The diagonal contribution on `I_ell` is
`ell sum|c_lambda|^2`.  Every ordered off-diagonal integral has absolute
value at most

\[
 \frac2{|\lambda-\mu|}
 \le\frac2{\delta_{\boldsymbol n}}.
 \tag{YA.3}
\]

Cauchy--Schwarz in the form
`(sum|c_lambda|)^2<=2q sum|c_lambda|^2` gives

\[
 \sum_{\lambda\ne\mu}|c_\lambda||c_\mu|
 \le(2q-1)\sum_\lambda|c_\lambda|^2.
 \tag{YA.4}
\]

Hence the off-diagonal-to-diagonal ratio is at most

\[
 \frac{2(2q-1)}{\ell\delta_{\boldsymbol n}}
 \le\frac{2q-1}{4q}
 =\frac12-\frac1{4q}<\frac12.
 \tag{YA.5}
\]

This leaves the claimed lower bound

\[
 \int_{I_\ell}|F|^2
 \ge\frac\ell2\sum_\lambda|c_\lambda|^2
 =\frac\ell4S(t)^2.
 \tag{YA.6}
\]

The stronger residual in YA.5 is deliberately not used.  Holder on an
interval of length `ell` gives

\[
 \int_{I_\ell}|F|^3
 \ge\ell^{-1/2}\left(\int_{I_\ell}|F|^2\right)^{3/2}
 \ge\frac\ell8S(t)^3.
 \tag{YA.7}
\]

The constants and the factor two in YA.3 have been checked independently.

## 3. Independent complete-clock calculation

Scale `t=R^2s` and set

\[
 \Lambda_0=\lambda R^2,\qquad
 \sigma=rBR^2,\qquad
 \zeta(s)=\eta_R(R^2s).
 \tag{YA.8}
\]

Then `zeta(0)=0` and `|zeta'|<=C_eta`.  Put
`tau=1` for `Lambda_0<=1` and `tau=Lambda_0^(-1)` otherwise.  Direct
integration gives

\[
 \left(\int_0^4e^{-3\Lambda_0s/2}\,ds\right)^{2/3}
 \asymp\tau^{2/3}.
 \tag{YA.9}
\]

If `|sigma|tau<=1`, the unweighted case is bounded by `4|sigma|` and the
large-heat case is bounded by
`C|sigma|Lambda_0^(-2)<=Ctau`.  If
`|sigma|tau>=1`, integration by parts with
`w=zeta exp(-Lambda_0s)` gives

\[
 \left|\sigma\int_0^4w(s)\sin(\alpha+\sigma s)\,ds\right|
 \le |w(4)|+\int_0^4|w'(s)|\,ds
 \le C\min\{1,\Lambda_0^{-1}\}.
 \tag{YA.10}
\]

Since `0<tau<=1` in the second heat regime,
`tau<=tau^(2/3)`.  This proves Y.21 uniformly in the phase, heat rate, and
`B`.  If `B=0`, the target row is zero before scaling.

Returning to physical time gives

\[
 \left|B\int_0^{4R^2}\eta_RPe^{-\lambda t}
 \sin(\alpha+rBt)\,dt\right|
 \le\frac{C}{rR^{4/3}}
 \left(\int_0^{4R^2}(Pe^{-\lambda t})^{3/2}\,dt\right)^{2/3}.
 \tag{YA.11}
\]

The factor `R^(-4/3)` is exact: the cubic time integral contributes
`R^(4/3)` after the `2/3` power.

## 4. Row count, signs, and scale ledger

Squaring Y.4 gives:

- `q` self rows at `r=2n_j`;
- one difference row at `r=n_j-n_i>0` for each `i<j`;
- one sum row at `r=n_i+n_j` for each `i<j`.

Thus the exact number of nonconstant rows is

\[
 q+2\binom q2=q^2.
 \tag{YA.12}
\]

For the convention
`cos(ry-theta)=cos(ry)cos(theta)+sin(ry)sin(theta)` and odd `D_R`, the
difference phase is `phi_j(t)-phi_i(t)` and its speed is
`(n_j-n_i)B`.  The sum and self signs in Y.28 follow identically.  Since
the proof takes the absolute value of every already controlled row, an
overall orientation sign of the radial derivative would not alter the
bound.

The radial quotient and clock lemma give each row

\[
 \frac{|J_{r,R}|}{r}R^{-4/3}
 \le Ca^2R^{5/3}.
 \tag{YA.13}
\]

With `S(t)^2=sum_j A_j(t)^2`, both
`A_j(t)^3<=S(t)^3` and
`(A_i(t)A_j(t))^(3/2)<=S(t)^3`.  Summing YA.13 therefore produces
`q^2a^2R^(5/3)(int S^3)^(2/3)`.

The exact plateau fibre has area `4pi a delta_0R^2`.  Combined with YA.7
and `ell=aR`, it gives

\[
 M_{\boldsymbol n,R}^{\rm plat}
 \ge\frac{\pi\delta_0}{2}a^2R^3
 \int_0^{4R^2}S(t)^3\,dt.
 \tag{YA.14}
\]

The final exponents are

\[
 a^2R^{5/3}(a^2R^3)^{-2/3}
 =a^{2/3}R^{-1/3}.
 \tag{YA.15}
\]

Normalization cancels `R` and yields `omega^(1/3)`.  There is no hidden
mode-count constant in YA.3--YA.15, so the explicit factor is `q^2` even
when `q=q(L)`.  If `log q=o(L^2)` and Y.3 continues to hold, the exact
coefficient remains `-2/11907`.  This is a statement for an increasingly
sparse admissible class, not uniform control of dense growing packets.

## 5. Adversarial deletion tests

Three nearby weakenings fail or lose the proof:

1. If `2n_1` is deleted from `delta_n`, take `q=1` and
   `F(y)=A sin(n_1y)` with `n_1ell->0`.  The claimed phase-uniform Gram
   lower bound fails.
2. If `eta_R(0)=0` is deleted, take `zeta=1`,
   `Lambda_0->infinity`, `|sigma|/Lambda_0->infinity`, and phase zero.
   The oscillatory row need not have the `Lambda_0^(-2/3)` decay required
   by Y.21.
3. If Y.3 is deleted, consecutive modes can have a nearly singular local
   Gram matrix; the outer-cap packet of R0.75R lies in precisely this
   unresolved regime.

These tests show why the retained onset, signed separation, and packet
boundary are structural assumptions.

## 6. Source, exact-solution, and claim audit

The bounded source report distinguishes classical Ingham-type
separated-frequency observability from Y's deliberately elementary Gram
proof.  No external theorem is imported, and no completeness, novelty, or
priority claim is made.

The field is an exact smooth solution of
`F_t+B F_(x_2)-F_(x_2x_2)=0` and embeds in
`u=(0,B,F(t,x_2))`.  The constant background is not proved to lie in the
frozen mean-zero, inversion-paired Version-M subclass.  Version-M use
therefore remains conditional on the same actual-component, row, weight,
realized-subclass, and ledger-alignment hypotheses.

Unresolved clusters, arbitrary packets, inter-packet aggregation,
nonconstant shear, projections of larger fields, E.24, complete Version-M
extraction, fixed deletion, suitable-weak transfer, regularity, and
singularity remain open.  The proof is analytic, so a simulation or formal
scientific figure would not add certificate value.

## Final decision

Y.1--Y.39 form a complete proof of the stated strongly separated
multimode collar-flux estimate, with explicit `q^2` dependence and correct
normalization.  **PASS; mathematical blockers 0; release blockers 0.**
**NOT CLAY.**
