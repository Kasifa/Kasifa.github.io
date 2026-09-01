# R0.74C advected-shear finite algebra certificate

**Status:** PASS

**Scope:** FINITE_EXACT_ALGEBRA_AND_FROZEN_BYTES_ONLY

Every subject leaf has one distinct check ID. Actual algebraic values are derived from source-bound primitives before comparison with independently declared targets. No literal self-equality check is used.

## Frozen provenance

- Source commit: d6c59e31c4a10800a1e091390a25ad5672dc17d5
- Current source SHA256: b300e7c32f9d944be36813530c5ffd1d7bc7463d161bba829284b4ab2d3e2c09
- Source blob SHA256 at frozen commit: b300e7c32f9d944be36813530c5ffd1d7bc7463d161bba829284b4ab2d3e2c09
- Producer SHA256: 6a5c7933be72f3ff8fe7ba7cf8bf522db8bb60158a9621c4b1ce68bbcc8b203d
- External freeze manifest: research/r074c_certificate_freeze.json
- The producer SHA is bound one way by the external manifest. The manifest has canonical bytes and a fixed checked field set; version-control review supplies its non-self-referential immutability boundary.

## Exact finite identities

- From M=3*2^(m-1), 4^(m-1)=M^2/9 and gamma=exp(-1/288 M^2).
- R=exp(-1/96 M^2) and A=R^(-2) exp(1/576 M^2).
- I_8/R^2=['1', '65'], I_S/R^2=['61', '65'], and tau/R^2=['2', '66'].
- The affine endpoint coefficients are ['1', '0'], so the transported centre equals q=MR at t0.

## Monomial convention

Each row is [A power, R power, M power, exp(M^2) coefficient].

| Quantity | Row |
|---|---|
| E.background | ['0', '-2', '0', '0'] |
| E.heat | ['2', '2', '0', '-1/264'] |
| Gu.background | ['0', '-3', '0', '0'] |
| Gu.strip | ['3', '4', '-1', '0'] |
| Gp.background | ['0', '-3', '0', '0'] |
| Gp.heat | ['3', '3', '0', '-1/176'] |
| Hu.background | ['0', '-3', '0', '0'] |
| Hu.strip | ['3', '4', '-2', '0'] |
| P.background | ['0', '-3', '0', '0'] |
| P.heat | ['3', '3', '0', '-1/176'] |
| P.strip | ['3', '4', '-1', '0'] |
| P23.background | ['0', '-2', '0', '0'] |
| P23.heat | ['2', '2', '0', '-1/264'] |
| P23.strip | ['2', '8/3', '-2/3', '0'] |
| target.lower | ['2', '2', '2', '-1/288'] |

## Ratio ledger

- Heat row: exponential gap 1/3168 = 1/3168 > 0; the fixed polynomial denominator has degree 8.
- Exterior row after substituting R: ['0', '0', '8/3', '1/288'] with exponential coefficient 1/288 = 1/288 > 0.
- Background row after substituting A and R: ['0', '0', '2', '0']; exponential balance is 0 and the remaining M power is 2.
- These finite exponent and power identities are the algebra used by the analytic divergence proof. This certificate does not prove an infinite limit.

## Frozen labels

- EXACT_SOLUTION: True
- PROVED: True
- FINITE: True
- OPEN: True
- NOT_CLAY: True
- nu_theta_one: True
- mean_zero_derivative: True

## Result

All 83 checks pass. The coverage manifest is a bijection over 81 subject leaves.

## Analytic boundary

- The heat-kernel lower and leakage bounds are not certified.
- The Calderon--Zygmund/Jensen gauge estimate is not certified.
- Periodic-copy infinite sums and all infinite quantifiers remain analytic.
- Finite rows do not prove the divergence limit.
- Exact-solution status is a frozen source label; the PDE differentiation remains in the analytic note.
- FINITE, EXACT_SOLUTION, PROVED, OPEN, and NOT_CLAY retain their literal source meanings.
- This certificate proves no Clay Millennium Prize statement.
