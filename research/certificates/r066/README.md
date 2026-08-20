# R0.66 publication certificate

This directory certifies a nonzero dominant spectral projection for the
complete heat-weighted quartic target on the explicit repeated-`0100`
Rudin--Shapiro packet.

## Source lock

- Source commit: `0dc5a9b`
- Exact finite stage:
  `research/quartic_weighted_cycle_finite_iterate.py`
- Spectral enclosure stage:
  `research/quartic_weighted_cycle_spectral_audit.py`
- Mathematical note:
  `research/quartic_weighted_cycle_spectral_note.md`
- Shared exact-moment dependency:
  `research/quartic_weighted_cycle_audit.py`

## Formal commands

```text
python3 research/quartic_weighted_cycle_finite_iterate.py \
  --cycles 100 --order 24 --progress \
  --output research/certificates/r066/exact-finite-iterate.json

python3 research/quartic_weighted_cycle_spectral_audit.py \
  --profile publication --cycles 100 --order 24 \
  --finite-input research/certificates/r066/exact-finite-iterate.json \
  --output research/certificates/r066/spectral-audit.json
```

The exact stage was repeated independently before the formal run.  All nine
packet parameters and rational endpoint fields agreed exactly.  The formal
endpoint hashes are:

- lower endpoint: `e1c02a3ea02ce5ef37a229e245da81168c192b05eede50fb74846ae81ce6041a`
- upper endpoint: `da2b167e11ecaa32c00198a9b2c31825010a7a75891784ff0578af07bfe2a447`

## Certified result

The dominant root is enclosed by

```text
25.1515893341015 < lambda < 25.1515893341016.
```

For the complete heat-weighted coefficient,

```text
S_r = C_* lambda^r + O(r 16^r),
```

with

```text
-2.3044567988959899827357007373579796619143E-5
  < C_* <
-2.2865275054844114494446509129452391587895E-5.
```

Therefore `C_*` is strictly negative and `|S_r|/16^r` tends to infinity on
the named packet family.

The total outward error is
`8.9646467053329352141990438860522105010704E-8`, split into:

- finite spectral convergence: `2.5597409349552049674206573981941778919496E-9`;
- finite target parameter: `2.5283438965007028185403896383198890399447E-21`;
- infinite simplex tail projection: `8.7086726118371618830673280759509386729116E-8`.

All 5 exact-stage checks and all 21 spectral-stage checks pass.

## Resources

The exact degree-48 moment run used `M=16^100`, took 669.45 wall seconds,
and reached 564,232,192 bytes maximum resident set size according to
`/usr/bin/time -l`; it reported zero swaps.  The staged spectral enclosure
took 0.35 wall seconds and reached 30,425,088 bytes maximum resident set
size.

The `stderr.log` files preserve progress and resource output.  The
`stdout.log` files preserve the complete command reports and duplicate the
corresponding JSON payloads for audit convenience.

## Claim boundary

This is an asymptotic theorem for one explicit quartic Picard coefficient.
It disproves the candidate uniform `O(M)` bound for that coefficient on the
named packet.  It does not control higher Picard orders, does not establish
singularity of the full mild solution, does not treat general initial data,
and does not solve the three-dimensional Navier--Stokes Millennium problem.
