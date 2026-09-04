# R0.75O bounded primary-source report

## Report frame

- Audience: the R0.75 proof program and future specialist referees
- Date: 2026-09-03
- Question: does existing shear-flow literature already contain the exact
  R0.75O localized packet estimate, and which parts of the argument are
  standard neighboring mechanisms?
- Scope: primary research articles and author/arXiv records for passive
  scalar advection-diffusion in shear or parallel flows; bounded exact-
  phrase searches for the project-specific Wiener-row/Schur formulation
- Exclusions: general surveys, turbulence numerics, nonlinear Navier--Stokes
  threshold claims, and any assertion of exhaustive novelty
- Assumptions: R0.75O is a finite constant-shear benchmark inside the
  frozen project, not a standalone resolution of E.24

## Direct answer

The primary sources inspected establish a broad and mature theory of
passive-scalar decay, enhanced dissipation, hypoellipticity, and Taylor
dispersion in shear or higher-dimensional parallel flows. They support
the surrounding semigroup setting and show that vertical/transverse
diffusion is a standard central feature of the literature.

The bounded search did not locate the exact project-specific statement
proved in R0.75O: a physical-cutoff signed flux controlled by the
coefficientwise `x_3`-uniform Wiener row, followed by a finite total-
frequency cap and the frozen `R,omega,L,K` normalization. This negative
search result is only a routing fact. It is not evidence of novelty or
priority.

## Primary evidence

### Higher-dimensional parallel shear

Michele Coti Zelati and Thierry Gallay study passive scalar evolution in
an infinite cylinder with bounded cross section in arbitrary dimension.
Their main regimes are enhanced dissipation and Taylor dispersion, using
resolvent and hypocoercive methods. This is the closest inspected source
for the higher-dimensional parallel-flow setting, but its public theorem
description is about long-time decay across wave-number regimes, not the
localized signed-flux/Wiener-row estimate in R0.75O.

- Journal article: Michele Coti Zelati and Thierry Gallay, “Enhanced
  dissipation and Taylor dispersion in higher-dimensional parallel shear
  flows,” *Journal of the London Mathematical Society* 108 (2023),
  1358--1392, DOI
  [10.1112/jlms.12782](https://doi.org/10.1112/jlms.12782).
- Author manuscript record:
  [arXiv:2108.11192](https://arxiv.org/abs/2108.11192).

### Periodic and channel shear semigroups

Jacob Bedrossian and Michele Coti Zelati analyze evolution semigroups for
two-dimensional drift-diffusion under shear with full or partial
diffusion, including periodic and channel settings. Their work supplies
neighboring enhanced-dissipation and regularization context. R0.75O does
not invoke their decay theorem: for constant `B`, it uses only the exact
Fourier solution and the contractivity of the transverse heat semigroup.

- Journal article: Jacob Bedrossian and Michele Coti Zelati, “Enhanced
  dissipation, hypoellipticity, and anomalous small noise inviscid limits
  in shear flows,” *Archive for Rational Mechanics and Analysis* 224
  (2017), 1161--1204, DOI
  [10.1007/s00205-017-1099-y](https://doi.org/10.1007/s00205-017-1099-y).
- Preprint record:
  [arXiv:1510.08098](https://arxiv.org/abs/1510.08098).

### Hypoelliptic formulation for nonconstant shear

Dallas Albritton, Rajendra Beekie, and Matthew Novack study passive
scalars advected by nonconstant shear and connect enhanced dissipation to
Hormander-type hypoellipticity, including periodic and boundary cases.
This confirms that the unresolved R0.75O extension to `b(x_3)` belongs to
a substantially different mechanism from constant translation. It does
not provide, on the inspected article record, the frozen local positive-
flux inequality E.24.

- Journal article: Dallas Albritton, Rajendra Beekie, and Matthew Novack,
  “Enhanced dissipation and Hormander's hypoellipticity,” *Journal of
  Functional Analysis* 283 (2022), article 109522, DOI
  [10.1016/j.jfa.2022.109522](https://doi.org/10.1016/j.jfa.2022.109522).
- Preprint record:
  [arXiv:2105.12308](https://arxiv.org/abs/2105.12308).

## Claim-to-source gap matrix

| claim family | evidence | confidence | contradiction or gap | project treatment |
|---|---|---:|---|---|
| transverse diffusion in parallel shear is a standard research setting | Coti Zelati--Gallay 2023; Bedrossian--Coti Zelati 2017 | high | domains and asymptotic aims differ from the frozen torus flux | contextual only |
| nonconstant shear can produce hypoelliptic/enhanced dissipation mechanisms | Bedrossian--Coti Zelati 2017; Albritton--Beekie--Novack 2022 | high | no automatic transfer to a positive localized cutoff flux | left open |
| constant `B` permits the exact translated heat evolution used in O.6 | direct elementary calculation | high | not a literature-dependent claim | proved locally |
| `sum_l ||d_l||_infinity` plus Schur gives O.12 | no exact matching primary theorem located | local proof audited directly | bounded search cannot establish novelty | proved locally; no priority claim |
| total-frequency cap plus short-time `L2` floor gives O.17 | direct Parseval, heat multiplier, and Holder calculation | high | requires an upper-frequency cap | proved locally with cap explicit |
| O.24 implies the frozen arbitrary-field E.24 | unsupported | none | full-torus mass, constant shear, one packet, and low differences remain | explicitly not claimed |

## Searches and stopping rule

The first pass searched primary/preprint records for passive scalars,
constant or parallel shear, vertical diffusion, Fourier modes, and heat
semigroups. The second pass targeted the exact phrases “Wiener row,”
“cutoff Wiener norm,” and “Schur's test” together with passive-scalar
shear terminology. Results converged on the three source families above;
the exact-phrase wave returned no relevant mathematical match.

Search stopped because the consequential literature boundary is already
clear: standard sources cover the surrounding shear-diffusion theory,
while the R0.75O claim must be justified by its own finite proof and
certificate. Further broad searching would not validate the missing
localization or nonconstant-shear steps and would not support a novelty
claim.

## Limitations and use boundary

- Only publicly accessible article metadata, abstracts, open full text,
  and arXiv records were inspected; no exhaustive citation-graph or
  subscription-database review was attempted.
- The closest papers use different domains, asymptotic parameters, and
  target norms. Their results are not imported as black boxes into O.
- Absence of an exact search match is not proof that no equivalent result
  exists.
- All O.1--O.24 constants and scale claims require independent local
  mathematical audit and machine certificates.
- No source establishes E.24, a Navier--Stokes regularity theorem, or a
  singularity theorem for this project. **NOT CLAY.**
