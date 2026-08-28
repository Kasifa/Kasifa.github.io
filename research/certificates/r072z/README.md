# R0.72Z deterministic finite certificate

This bundle has two genuinely separate routes.  `generate_certificate.py`
uses exact rational ledgers, explicit formulas, and direct symmetric Fourier
sums.  `independent_recompute.py` does **not** import the producer; it instead
uses direct Fourier action, paired lattice enumeration, Poisson summation,
polynomial convolution, and deterministic Simpson quadrature.

The fail-closed validator checks the commutator and Fourier matrix, the exact
`M3` formula and sampled `s` bound, the strong-row alpha power, low- and
high-mode witnesses, the gapless tangent residual, the collision-scaled
cubic coefficients, kinetic orientation and lattice identities, causal
kernel integrals, the damping-gap `J` formula, and the complete 15 CLOSED / 10
FALSE / 8 OPEN claim ledger.

The certificate **does not** machine-check an infinite-dimensional low-gap
Orr--Sommerfeld propagator, a collision-scale limiting absorption theorem,
equality of a finite truncation with the full operator norm, a Bloch-uniform
physical velocity direct sum, a complete linearized shear subsystem, any
nonlinear Navier--Stokes estimate, or the Clay Millennium problem.  Those
boundaries are mandatory false booleans and OPEN claim keys; deleting or
flipping one makes validation fail.

The formal figure is sealed separately through Git ancestry and visual QA.
Its displayed high-mode range includes the complete declared sequence,
including the (n=1) witness; the certificate does not treat the figure as
analytic proof.

The lifecycle has two explicit stages.  Run the source checks without writing
or replacing any JSON output:

```sh
python3 research/certificates/r072z/independent_recompute.py --self-test
python3 research/certificates/r072z/generate_certificate.py --self-test
```

An optional deterministic draft can be generated and strictly checked with:

```sh
python3 research/certificates/r072z/generate_certificate.py --draft
python3 research/certificates/r072z/validate_certificate.py --require-draft
```

Draft generation refuses to overwrite a formal bundle.  A legacy R0.72Z
finite-hash bundle whose manifest has no `status` is intentionally accepted
as an unsealed input and can be upgraded in one formal pass.

After the report, gap matrix, literature audit, three mathematical audits,
six certificate-source files, release manifest, release and translation
scripts, the exact R0.72Z missing-string i18n snapshot, all twelve
figure-source files, and all four R0.72Z tests are frozen
in one completely clean commit, seal the certificate with:

```sh
SOURCE_COMMIT=$(git rev-parse HEAD)
python3 research/certificates/r072z/generate_certificate.py \
  --formal --formal-source-commit "$SOURCE_COMMIT"
python3 research/certificates/r072z/validate_certificate.py --require-formal
```

Formal generation requires a full lowercase 40-character commit equal to the
current clean `HEAD`.  Each of the 32 source bindings records the source
commit, Git blob, SHA-256, and byte count.  The formal manifest has
`status=formal`; the crosscheck has `status=passed`,
`formalSourceReady=true`, `temporaryUnsealedSourceAllowed=false`, the same
`sourceCommit` and `sourceBindings`, and an exhaustive all-true check map.
The producer and independent result both propagate the formal stage and
source commit.

Strict validation re-resolves the commit and every Git blob and requires the
source commit to be the current `HEAD` or an ancestor.  Every frozen source is
immutable except the current copy of `research/release-manifest.json`: its
source-commit blob remains permanently checked, while its working copy may
advance only as the clean blob of a descendant publication commit.  At the
source `HEAD`, only the five certificate outputs may be dirty after sealing.
The flat `SHA256SUMS` file covers every regular flat bundle file exactly once.
Once a manifest is formal, generation refuses to overwrite it.

Run the commands in `command.txt` from the repository root.  All outputs are
deterministic for fixed source bytes and the bundled Python runtime.
