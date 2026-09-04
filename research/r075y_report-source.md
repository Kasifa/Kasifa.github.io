# R0.75Y bounded source and collision report

## 0. Scope and search boundary

- Audit date: 2026-09-04.
- Target: the strongly separated finite-harmonic signed collar-flux theorem
  in `research/r075y_strongly_separated_multimode_flux_payment.md`.
- Search scope: a bounded exact-topic search for finite Fourier-mode
  Navier--Stokes shears, local observation, signed collar flux, and
  separated-frequency lower bounds.
- Exclusions: an exhaustive citation graph, a priority search over every
  language and database, arbitrary-packet observability, and any claim that
  failure to find an exact match proves novelty.

Deep Research was used only for source discovery and collision control.
No external paper is used as proof of any R0.75Y inequality.

## 1. Queries and usable records

The bounded search used the following query families:

1. `site:arxiv.org Navier-Stokes exact shear flow finite Fourier modes local
   observability signed flux`;
2. `site:arxiv.org Ingham inequality separated frequencies finite Fourier
   sum interval lower bound`;
3. `site:arxiv.org Turan Nazarov exponential polynomial local observation
   finite frequencies`.

The first query did not return a source matching the full R0.75Y object:
an exact diffusive shear, the frozen odd collar kernel, complete-clock
moving phases, plateau `L^3` mass, and the precise
`a^(2/3)R^(-1/3)` payment.

Two relevant background records were retained:

| record | verified scope | use in R0.75Y |
|---|---|---|
| P. Jaming and C. Saba, *From Ingham to Nazarov's inequality: a survey on some trigonometric inequalities*, arXiv:2311.17714 | overview of `L^p` inequalities for harmonic and nonharmonic trigonometric polynomials, including Ingham-type `L^2` bounds and stronger bounds under additional frequency structure | contextual only; no theorem imported |
| S. Kunis, H. M. Möller, T. Peter, and U. von der Ohe, *Prony's method under an almost sharp multivariate Ingham inequality*, arXiv:1705.11017 | an Ingham inequality in a separated-frequency reconstruction setting | contextual only; different dimension, object, and application |

Primary record URLs:

- https://arxiv.org/abs/2311.17714
- https://arxiv.org/abs/1705.11017

## 2. Exact separation from the background literature

The general phenomenon “separated exponential frequencies admit interval
`L^2` lower bounds” is classical and must not be advertised as new.
R0.75Y does not invoke a sharp Ingham theorem.  Instead it expands the
finite signed spectrum `\{-n_q,\ldots,-n_1,n_1,\ldots,n_q\}` and bounds
every off-diagonal Gram entry by

\[
 \frac{2}{|\lambda-\mu|}.
 \tag{YS.1}
\]

The elementary inequality

\[
 \sum_{\lambda\ne\mu}|c_\lambda||c_\mu|
 \le(2q-1)\sum_\lambda|c_\lambda|^2
 \tag{YS.2}
\]

then shows directly that
`aR\,\delta_{\boldsymbol n}\ge8q` leaves at least one half of the diagonal
Gram mass.  The constant `8q` and the resulting explicit `q^2` flux-row
count are therefore checked inside the note, rather than attributed to the
two background sources.

The phase-free complete-clock lemma is also proved inside R0.75Y by a
slow/fast split and one integration by parts.  The radial quotient
`|J_{r,R}|/r<=Ca^2R^3` is a frozen internal predecessor result from
R0.75U.  Neither background source contains the combined collar-flux
statement.

## 3. Collision matrix

| possible collision | status | exact boundary |
|---|---|---|
| Ingham-type separated-frequency `L^2` observability | known background phenomenon | Y uses a deliberately nonsharp, self-contained finite Gram estimate |
| sharper dependence on frequency separation | not claimed | Y freezes the sufficient condition `aR\,\delta_{\boldsymbol n}\ge8q` |
| Navier--Stokes shear exact solutions | standard exact subclass | Y's research content is the localized signed-flux payment within the frozen route, not existence of the shear |
| complete-clock oscillatory integration | elementary | proved in Y.20--Y.25, with the cutoff onset retained |
| arbitrary multimode packet payment | explicitly false | consecutive or clustered packets can fail Y.3 and remain subject to R0.75R |
| regularity or Clay conclusion | explicitly false | Version-M transfer and all global regularity steps remain open |

## 4. Claim decision

The bounded search found relevant classical context but no exact collision
with the complete R0.75Y theorem.  This is evidence for keeping the result
distinctly labeled and source-audited; it is not evidence of completeness,
novelty, or priority.

Safe public wording:

> We prove an internal, self-contained strongly separated multimode
> collar-flux estimate within the frozen exact-shear model, with an explicit
> `q^2` factor.  The separated-frequency `L^2` principle is classical; no
> novelty or priority claim is made.

Unresolved high-carrier clusters, arbitrary packets, E.24, Version-M
extraction, suitable-weak transfer, regularity, and singularity remain
open.  **NOT CLAY.**
