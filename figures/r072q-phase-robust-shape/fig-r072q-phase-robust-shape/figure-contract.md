# Figure contract: R0.72Q phase-robust shape

## Analytical question

For

`F_y(phi)=cos(phi)+sum_(m=2)^M Re(beta_m(y) exp(i m phi))`,

define `Q_j=sup_y sum_(m=2)^M m^j |beta_m(y)|`. Does fixed `M` and
`Q2<=1/2` give a phase-independent quantitative Morse package strong enough
for the Coble--He proof-level family-uniform enhanced-dissipation extraction?

## Supported answer

Yes, for the declared fixed-`M` heat-weighted family. The coefficient bound
gives `Q1<=1/4`. Every critical point lies within `pi/12` of `0` or `pi`.
The `pi/12` neighborhood of that critical point lies in the `pi/6` curvature
zone, where `|F''|>=mu=(sqrt(3)-1)/2`. The normalized `F` away gap is
`>1/12`. For `W=e^{-y}F` on `0<=y<=1`, the formal shape contract used
downstream is `(r,C0,C1)=(pi/12,81,36)`. Coble--He supplies the time-dependent shear theorem;
the compact-family constant extraction remains a proof-level step in the
R0.72Q report.

## Panel inventory

| Panel | Object | Rendering | Allowed claim |
|---|---|---|---|
| A | exact 1:2 caustic and two safe disks | exact parametric samples, equal axes | the whole disk `|z|<1/4` is caustic-free; `|z|<=1/8` is the `Q2<=1/2` slice |
| B | phase-ray wall `r_*(theta)` | exact caustic parametrization mapped to polar coordinates | every phase ray meets the wall once and `r_*` lies in `[1/4,1/2]` |
| C | fixed-`M` localization and curvature margins | exact curves `cos(d)-1/2` and `sin(d)-1/4` with analytic zones | localization `pi/12`, zone `pi/6`, `mu=(sqrt(3)-1)/2`, normalized `F` away gap `>1/12`, and formal `W` constants `C0=81`, `C1=36` |

## Exact formulas

For `F(phi)=cos(phi)+Re(z exp(2 i phi))`, the caustic is

`z(phi)=exp(-3 i phi)/8-3 exp(-i phi)/8`.

It also satisfies

`(|z|^2-1/16)^3=(27/1024)(Im z)^2`, `1/4<=|z|<=1/2`.

At `z=+/-1/4` the third derivative also vanishes and the fourth derivative
does not. These two points are the real-axis cusps. In the 1:2 slice,
`Q2=4|z|`, hence `Q2<=1/2` gives the strictly interior radius `|z|<=1/8`.

For the general fixed-mode profile, a critical point obeys
`|sin(phi)|<=Q1<=1/4<sin(pi/12)`. If `d` is distance to `0` or `pi`, then
`d<=pi/12`. A point within `pi/12` of that critical point has `d<=pi/6`, and

`|F''|>=cos(pi/6)-Q2=(sqrt(3)-1)/2=mu`.

## Rendering policy

- Proved safe regions and exact analytic margins use restrained blue.
- The exact applicability wall uses ochre.
- Formula reference curves use dark neutral ink.
- Boundaries differ by line style as well as color.
- No color-only distinction, fitted curve, regression band, or heat map is
  permitted.
- Panel A uses equal Cartesian axes. Panel B covers a full relative-phase
  period. Panel C uses the exact distance coordinate.

## Data and inference policy

The formal `data.csv` is generated from the formulas above. It is a traceable
plotting table, not source evidence for the continuum theorem. The validator
must check the parametric caustic equations, the implicit residual, the wall
radius range, the two exact safe radii, and the analytic margin constants.
The caption must state that numerical sampling cannot replace the continuous
proof.

## Lineage and fail-closed policy

The prior runtime-lineage design is retained exactly for R0.72Q:

1. six explicit inputs: analytic source plus producer config/result,
   independent config/result, and formal crosscheck;
2. one derived canonical certificate ledger;
3. passed producer and independent results;
4. `formalSourceReady=true`, matching clean tracked source commits, and
   `temporaryUnsealedSourceAllowed=false`;
5. all runtime JSON files in `research/certificates/r072q/`, with a unique,
   byte-sorted, digest-correct flat `SHA256SUMS` that covers the directory;
6. analytic and audit Git blobs bound at the source commit;
7. certificate JSON and ledger blobs bound at the certificate commit;
8. figure build commit equal to the certificate commit;
9. all thirteen package sources tracked, byte-identical to that commit, and
   tracked/staged trees clean at plotting and sealing.

## Archival and visual QA

- double-column width: 177.8 mm;
- height: 82.55 mm;
- one-page vector PDF;
- editable-text, raster-free SVG;
- 600 dpi PNG;
- final-size, grayscale, and PDF-raster QA at 180 dpi;
- neutral restrained palette and non-color distinctions;
- explicit visual inspection of all three QA surfaces before sealing.

## Claim boundary

The figure covers arbitrary phases only inside the fixed-`M`, `Q2<=1/2`
contract and the declared heat-weighted slow-time path. It does not cover
`M` growing with scale, coefficient families crossing the caustic, arbitrary
fast time-dependent phases, arbitrary common-band geometry, or general
three-dimensional Navier--Stokes solutions.
