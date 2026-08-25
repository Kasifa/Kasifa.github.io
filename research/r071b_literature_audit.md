# R0.71B literature audit — signed common response, tent spaces, BMO, and Besov boundaries

**Date:** 2026-08-25

**Scope:** a bounded primary-source audit for four questions:

1. whether Littlewood--Paley or paraproduct algebra automatically gives a
   signed common-response scale cancellation;
2. whether the canonical positive square tent is genuinely weaker than BMO;
3. whether a signed box mass can invoke the classical Carleson embedding;
4. whether a shell-supremum or BMO continuation criterion already makes the
   R0.71B consumer non-new.

This is not a systematic review and makes no priority claim.

## 1. Result matrix

| Source | Established statement used here | R0.71B decision |
|---|---|---|
| [Bony 1981](https://www.numdam.org/item/ASENS_1981_4_14_2_209_0/) | Paraproduct and resonant decompositions separate low--high, high--low, and comparable-frequency products | Frequency bookkeeping does not itself provide sign, telescoping, or a shell-count-independent partial-sum bound |
| [Fefferman--Stein 1972](https://doi.org/10.1007/BF02392215) | Hardy spaces and BMO duality/characterizations in several variables | The ordinary square-function coefficient lies on the classical BMO side, not below it |
| [Coifman--Meyer--Stein 1985](https://www.sciencedirect.com/science/article/pii/0022123685900072) | Tent spaces provide the natural setting for square functions and Carleson measures | A positive square tent is an established size space and is insensitive to scale signs |
| [Frazier--Jawerth 1990](https://doi.org/10.1016/0022-1236(90)90137-A) | The \(\varphi\)-transform discretizes and localizes Littlewood--Paley distribution spaces | Under the standard admissible hypotheses, the local \(F^0_{\infty,2}\) square sequence is BMO; using it is not a new common-response criterion |
| [CLMS 1993 precursor](https://numdam.org/item/SEDP_1989-1990____A16_0/) | Div--curl products of \(L^2\) fields lie in Hardy space | Together with Hardy--BMO duality this gives the classical signed vortex-stretching endpoint once a BMO coefficient is supplied |
| [Kozono--Taniuchi 2000](https://doi.org/10.1007/s002090000130) | BMO norms of velocity/vorticity control blow-up of smooth Navier--Stokes solutions | Replacing the common channel by an assumed vorticity BMO coefficient is an established criterion, not R0.71B progress |
| [Kozono--Ogawa--Taniuchi 2003](https://www.jstage.jst.go.jp/article/kyushujm/57/2/57_2_303/_article) | A local solution extends if \(\int_0^T\|\operatorname{curl}u(t)\|_{\dot B^0_{\infty,\infty}}dt<\infty\); the proof uses a Besov Hölder/logarithmic estimate | Failure of a direct polarized shell-supremum \(\times L^2\times L^2\) estimate does not contradict this different nonlinear argument |
| [Nakai--Yoneda 2012](https://www.jstage.jst.go.jp/article/jmath/64/2/64_399/_pdf) | A fixed-grid dyadic-BMO velocity criterion with its stated time exponent extends the BMO family | “Weaker than ordinary BMO” alone is not enough to establish a new criterion; dyadic BMO must also be compared |
| [Koch--Tataru 2001](https://math.berkeley.edu/~tataru/papers/nas.pdf) | \(BMO^{-1}\) is characterized through a positive heat-extension Carleson square and small data give a global solution | This is a positive small-data critical space, not a signed large-data common-response cancellation theorem |
| [Constantin--Fefferman 1993](https://iumj.org/article/3627/) | Coherence of the physical vorticity direction depletes the Biot--Savart stretching kernel | A covariance response or projector must first be linked quantitatively to the physical direction; the theorem does not provide that link |
| [Bourgain--Pavlović 2008](https://arxiv.org/abs/0807.0882) | Norm inflation occurs in the large critical space \(\dot B^{-1}_{\infty,\infty}\) | A sign-blind weak critical norm cannot simply be used as a Koch--Tataru-style contraction space |

## 2. The positive tent is sign blind

A standard Littlewood--Paley tent/Carleson functional has the form

\[
 \sup_R\frac1{|R|}\int_R
 \sum_{j\ge j(R)-O(1)}|\Delta_j f|^2\,dx.
 \tag{2.1}
\]

Changing any scale sign,

\[
 \Delta_jf\mapsto\varepsilon_j\Delta_jf,
 \qquad \varepsilon_j\in\{-1,1\},
 \tag{2.2}
\]

leaves (2.1) unchanged.  This is a direct consequence of the square, not a
separate literature claim.

For an admissible smooth resolution, the square root of (2.1) is equivalent
to BMO modulo constants.  Consequently:

- it has the correct positive packing mass to absorb a paraproduct;
- it does not detect the sign difference in the R0.71A same-covariance pair;
- assuming its (L_t^1) integrability for vorticity returns to an
  established BMO-side continuation condition.

## 3. Signed box mass is not a classical Carleson measure

The classical Carleson embedding uses a positive measure, or equivalently a
bound on total variation.  For a signed measure (mu), a bound only on

\[
 |\mu(T(R))|
 \tag{3.1}
\]

allows arbitrarily large positive and negative masses inside the same box to
cancel.  It does not control

\[
 |\mu|(T(R))
 \tag{3.2}
\]

and therefore does not invoke the standard embedding theorem.

A valid signed replacement would need an additional theorem, for example:

1. a telescoping representation (M_j=G_{j+1}-G_j);
2. uniform control of signed partial sums before squaring;
3. a bounded paraproduct/operator norm; or
4. a Navier--Stokes flux identity coupling adjacent time--scale boxes.

None of these structures follows merely from the response identity or the
Leray projector.

## 4. Hardy--BMO already gives the classical signed endpoint

For each velocity component, the div--curl structure gives

\[
 h_j=\omega\cdot\nabla u_j\in\mathcal H^1,
 \qquad
 \|h_j\|_{\mathcal H^1}
 \lesssim\|\omega\|_2\|\nabla u_j\|_2.
 \tag{4.1}
\]

Hardy--BMO duality and the Biot--Savart (L^2) equivalence yield

\[
 \left|\int(\omega\cdot\nabla u)\cdot\omega\right|
 \lesssim\|\omega\|_{\mathrm{BMO}}\|\omega\|_2^2.
 \tag{4.2}
\]

This estimate keeps the sign in the dual pairing.  It does not manufacture
the BMO coefficient from energy, covariance (Q), an eigengap, or a
principal projector.  R0.71B must not relabel (4.2) as a new
common-response theorem.

## 5. The Besov criterion does not use the rejected direct estimate

Kozono--Ogawa--Taniuchi prove that their local solution extends when

\[
 \int_0^T
 \|\operatorname{curl}u(t)\|_{\dot B^0_{\infty,\infty}}\,dt
 <\infty.
 \tag{5.1}
\]

Their proof uses a Besov Hölder estimate, the boundedness of the Riesz
transforms in the relevant Besov class, frequency splitting, and a
logarithmic higher-norm factor.  It is not the direct polarized estimate

\[
 |\mathfrak P_{\rm cr}(A;B,C)|
 \lesssim
 \sup_j\|\Delta_jA\|_\infty\|B\|_2\|C\|_2.
 \tag{5.2}
\]

Therefore the R0.71B shared-high fan can disprove (5.2) without contradicting
(5.1).  The report keeps this distinction explicit.

## 6. Leray projection and response geometry

The Leray symbol

\[
 \Pi_{ij}(\xi)=\delta_{ij}-\frac{\xi_i\xi_j}{|\xi|^2}
 \tag{6.1}
\]

is order zero.  A difference such as

\[
 \Pi(\xi+\eta)-\Pi(\xi)
 \tag{6.2}
\]

can gain (O(|\eta|/|\xi|)) in an HHL region, but the common part remains
order one.  This is consistent with the exact R0.71B limit
(mathcal U_M\to1) and the small chord.  The projector does not by itself
give an alternating sign, a martingale difference, or time integrability.

## 7. Safe claim matrix

### Established and not new

- Bony paraproduct/resonant decomposition;
- tent spaces and positive Carleson embedding;
- the BMO/Frazier--Jawerth square-sequence boundary;
- CLMS Hardy compensation followed by an assumed BMO coefficient;
- vorticity BMO, (dot B^0_{\infty,\infty}), and stated dyadic-BMO
  continuation criteria;
- small-data (BMO^{-1}) well-posedness.

### Narrow R0.71B contribution

- an exact HHL common/chord pair with common limit one and quadratic chord
  decay;
- a same-low fan excluding automatic same-sign
  (ell^2\)-to-(ell^1) packing;
- an equal-radius shared-high fan excluding one direct polarized
  shell-supremum trilinear estimate;
- a sign-sensitive positive-output coefficient with an exact
  Cauchy--Young consumer and exact R0.71A values.

### Still open

- a local signed-before-square tent theorem;
- (L_t^1) propagation of the positive-output coefficient from
  Navier--Stokes dynamics;
- a nonredundant continuation theorem that does not already assume BMO,
  dyadic-BMO, or (dot B^0_{\infty,\infty}) integrability;
- an unconditional enstrophy closure.

## 8. Bounded search record

The checked concepts included:

- Bony paraproduct and resonant decomposition;
- tent spaces and Carleson embedding;
- BMO Littlewood--Paley and discrete-transform characterizations;
- dyadic paraproduct boundedness and dyadic BMO;
- CLMS div--curl Hardy estimates;
- vorticity BMO and Besov continuation criteria;
- (BMO^{-1}) heat-extension tent norms;
- Leray projector commutators and HHL differences;
- vorticity-direction coherence and frequency-localized criteria.

The bounded search did not identify “common response” or the positive-output
coefficient of R0.71B as established Navier--Stokes terminology.  This is a
search boundary only.  It is not evidence of novelty or priority.
