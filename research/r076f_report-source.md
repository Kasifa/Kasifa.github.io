# R0.76F source report -- exponential spatial-observation obstruction

- Audience: internal mathematical audit and later publication handoff
- Date: 2026-09-04
- Scope: dependence on the number of modes in the R0.76E spatial observation
- Exclusions: full collar-flux sharpness, arbitrary packets, regularity, and singularity

## Direct answer

The exponential dependence on `q` in the inherited spatial observation
cannot be removed uniformly, even inside the exact real dyadic shear class.
The local binomial construction in the main note gives a lower bound
`2^(q-1)` for the fixed interval pair `I=[-1/2,1/2]` and
`J=[-3/2,3/2]`.

This closes only the proposed route of replacing the R0.76E observation
constant by a polynomial in `q`.  It does not show that the complete flux
estimate itself needs an exponential constant.

## Source ledger

### 1. General Turan--Nazarov exponent

Omer Friedland's 2026 preprint, [A Disk-Growth Remez Principle and a
Modular Proof of the Measurable Turan--Nazarov
Inequality](https://arxiv.org/abs/2606.24823), proves the measurable
Turan--Nazarov inequality with exponent `m-1` and explicitly records that
this exponent is sharp already on intervals.  This is a recent preprint,
not a peer-reviewed sharp-constant result.

F. L. Nazarov's original source is [Local estimates for exponential
polynomials and their applications to inequalities of the uncertainty
principle type](https://m.mathnet.ru/php/archive.phtml?jrnid=aa&option_lang=eng&paperid=397&wshow=paper),
Algebra i Analiz 5(4), 1993, 3--66; English translation in St. Petersburg
Mathematical Journal 5(4), 1994, 663--717.  It is the historical source for
the measurable local estimate used upstream.

### 2. Sharp trigonometric Remez constants

S. Tikhonov and P. Yuditskii, [Sharp Remez
Inequality](https://doi.org/10.1007/s00365-019-09473-2), Constructive
Approximation 52(2), 2020, 233--246, prove the exact circle constant
`T_n(sec(s/4))`.  For fixed missing-set measure this grows exponentially in
the degree.  The [author preprint](https://arxiv.org/abs/1809.09726) gives
the same theorem and equality family.

Tamas Erdelyi's [sharp even-trigonometric
version](https://arxiv.org/abs/1809.07466) gives a compatible exact
Chebyshev expression.  It is context rather than an input to the local
binomial proof.

## Claim-to-source matrix

| claim | evidence | confidence | limitation |
|---|---|---:|---|
| The general measurable Turan--Nazarov exponent `m-1` is sharp. | Friedland 2026, Remark 5.3 | high | recent preprint |
| Fixed-geometry trigonometric Remez constants can grow exponentially in degree. | Tikhonov--Yuditskii 2020, exact Chebyshev constant | high | full circle formulation, not the present nested intervals |
| The present obstruction lies in the exact real dyadic shear subclass. | F.3--F.17, direct local construction | proof in main note | not a literature novelty claim |
| The complete collar-flux constant must be exponential. | no supporting theorem | unsupported | expressly not claimed |

## Collision and gap assessment

The literature already establishes exponential-order sharpness in broader
Remez and exponential-polynomial classes.  The elementary factor
`(1-e^(i delta z))^(q-1)` is therefore not presented as a new approximation
theorem.  Its role is narrower: it verifies that the exact restrictions of
the Navier--Stokes shear route do not remove the classical obstruction.

No source located in the bounded search states the exact R0.76E interval,
dyadic-band, real-cosine specialization with the `2^(q-1)` constant.  This
absence is not evidence of novelty or priority.

## Searches performed and stopping rule

The search covered the original Nazarov source, the recent modular
Turan--Nazarov proof and sharpness remark, exact trigonometric Remez
constants, even-trigonometric variants, and adjacent pointwise Remez work.
Search stopped after the two consequential literature facts had primary or
publisher-backed sources and the remaining result reduced to a direct
construction.  Additional general Remez references were unlikely to change
the claim boundary.
