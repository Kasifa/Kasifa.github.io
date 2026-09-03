# Chart contract and source-data specification

## Analytical question

Does the already constructed canonical common-shear lobe intrinsically remain
inside its physical annulus long enough to contradict the exponentially short
dwell required by the bounded-payment escape?

## Supported takeaway

Yes, for this frozen architecture. Exact centre kinematics give a certified
geometric corridor of size `Theta(L_i R^3)`. That corridor lies inside the
completed-clock superlevel set, yielding only a lower
`Omega(L_i R^3)` statement for the latter. For the outer packet the resulting
normalized dwell is at least `(72/5)L_2`, incompatible with the inherited
exponentially vanishing necessary upper bound.

## Surface and form

- Surface: standalone double-column journal figure.
- Physical size: 178 mm by 116 mm.
- Exports: vector SVG and one-page PDF, plus 4204 by 2740 PNG at 600 dpi.
- Layout: four panels in a two-by-two grid.
- Renderer: Python 3.12.13, NumPy, Matplotlib, Pillow, pypdf, and pypdfium2
  with pinned versions.
- Evidence: exact formulas, exact rational checks, and deterministic
  derived-analytic evaluations; no stochastic sampling or PDE simulation.

## Panel contract

- **A:** symmetric centre corridor `(-A(L_i)r_i,+A(L_i)r_i)` around
  `Q_i(tau_i)=0`, its monotone time preimage, and intersection with the exact
  terminal slab. The time geometry is schematic and not to scale.
- **B:** the exponent ledger `R^-2` speed, `L_iR` room, and reciprocal-speed
  multiplication giving `L_iR^3`, together with the exact speed bounds.
- **C:** a set-inclusion diagram that assigns the two-sided `Theta` estimate
  only to the geometric corridor and the lower-only `Omega` estimate to the
  full `K`-superlevel set.
- **D:** 121 deterministic values for each of `log10 theta_cert_lower`,
  `log10 theta_necessary_upper` (illustrative `C=1`), and their log-gap on
  `9216 <= L_1 <= 20000`, with `d_L=log L_1` and `L_2=2L_1`.

## Palette and non-color distinctions

The palette uses one navy and one burnt-orange root plus charcoal and neutral
grays. Solid/dashed lines, open/filled markers, hatches, direct labels, and
set nesting duplicate every important distinction. A grayscale export is a
required QA asset. The research blossom is fixed at the top-right header.

## Source-data schema

`source-data.csv` is long-form with fields

`panel,record,series,x,y,x_unit,y_unit,evidence_class,formula_source,method`.

Panels A--C encode the exact constants, exponent ledgers, and relation types
used in the schematics; they do not treat drawing coordinates as data. Panel
D stores only direct binary64 evaluations of the displayed analytic
identities. Numeric values use round-trip-safe decimal formatting. The
validator regenerates every row from `config.json` and requires exact equality.

## Formula authority and claim boundary

The exclusive mathematical authority is core commit
`d74e7b297928147334136f4c3cb29c5226d66381`, file
`research/r074u_intrinsic_certified_residence.md`, blob
`3359036a04afd87eb51123d9b9d9a321a5bfc898`, SHA-256
`e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99`,
especially equations (U.11)--(U.45). The plotted upper bound must never be
transferred from the certified geometric corridor to the completed-clock
superlevel set.
