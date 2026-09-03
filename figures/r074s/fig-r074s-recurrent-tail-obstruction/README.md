# R0.74S recurrent-tail analytic figure archive

This directory is the formal 25-file archive for the Step 17 recurrent-streamline obstruction.  It visualizes the smooth exact Taylor-vortex family used in equations (S.445)--(S.475): a regular closed streamline repeatedly revisits the same flux phases, so absolute temporal variation grows cubically while signed excursion remains quadratic.

The mathematical authority is frozen core commit `7355c01dead23c3524242006318b02a8324447e6`, specifically `research/r074s_recurrent_streamline_temporal_tail_obstruction.md` and its main certificate/report.  Their Git blob object IDs and SHA-256 digests are locked in `config.json`.

## Scope

The field and streamline are analytic.  The displayed orbit is sampled from its exact level-set formula; the period is evaluated by deterministic Gauss--Legendre quadrature; and the time parametrization is rendered by fixed-step RK4 with closure, invariant, period, derivative, variation, and monotonicity audits.  This is **not DNS**, not a turbulence simulation, and **not a Clay-problem solution**.

## Reproduction

Use Python 3.12.13 with the exact packages in `requirements.txt`, then follow `command.txt`.  `plot.py` checks the pinned runtime and the frozen Git evidence before writing the 11 raw/result files.  `validate.py` reconstructs every CSV row, checks the numerical audits, validates SVG/PDF/600-dpi PNG properties, and checks the final-size, grayscale, and independently rasterized PDF QA assets.

## Two-stage Git seal

The preseal deliberately records `PENDING_FIGURE_SOURCE_COMMIT`; it never guesses a future commit.  Commit exactly the 21 source/raw files in their final repository path.  Then run the final reseal with the actual full commit hash.  Only `SHA256SUMS`, `manifest.json`, `qa-report.md`, and `validation.json` are rewritten during that final seal.

The archive partition is exactly 10 source files, 11 raw/result files, and 4 metadata files.  The source/raw preseal can therefore be reviewed and committed independently from the final Git binding.
