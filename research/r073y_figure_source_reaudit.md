# Independent final re-audit of the R0.73Y exact-shear figure package

**Audit date:** 2026-09-01

**Package:** `figures/r073y/fig-r073y-exact-shear-obstruction/`

**Source/raw commit:** `e49a0e0570bd3b20fb38096e4841993f990b4cc2`

**Metadata package commit:** `1aa97b39766d5eca01e7e0908ee222edd864b904`

## 1. Conclusion

`RELEASE_GATE_PASS` for the stated figure scope. A clean, independent audit
found no discrepancy in repository state, commit ancestry, source/formula
bindings, current bytes, checksums, inventory, validators, deterministic
rebuilds, plotted data, output synchronization, portability, visual QA, or
claim boundary. The audit was read-only.

This verdict certifies the formal staged figure package. It does not
independently prove a new Navier--Stokes theorem and does not attest remote
publication. The analytic theorem remains bound to the frozen research source
and its separate proof audit.

## 2. Independent integrity reconciliation

- Package HEAD was `1aa97b39766d5eca01e7e0908ee222edd864b904`, and the audited worktree was clean.
- The source/raw commit `e49a0e05...` is an ancestor of the package commit.
- All 21 source/raw current files equal their source-commit blobs byte-for-byte.
- All 21 stored SHA-256 values, byte counts, and Git blob object IDs agree.
- The three mathematical source hashes at `1ecc6fe2...` agree with the manifest.
- The package contains exactly 25 ordinary files and no extra directory or symlink.
- All `SHA256SUMS` rows pass; package verify-only makes no write.
- The generic repository validator reports `errors=[]`, `warnings=[]`.

## 3. Independent reconstruction and negative tests

Two newly created build directories independently reproduce every one of the
18 deterministic-core hashes. All 6,372 source-data rows reconstruct from the
closed formulas. Maximum observed discrepancies are:

```text
closed-form row reconstruction    1.1102e-16
stored summary reconstruction     5.5511e-17
```

Separate runtime, source, and inventory mutations are all rejected. Thus the
package does not merely self-report determinism; its declared reconstruction
and fail-closed behavior were exercised independently.

## 4. Independent visual and format audit

The PDF, SVG, and 600-dpi PNG are synchronized. The independently examined
final-size, grayscale, and PDF rasters show no crop, collision, missing glyph,
or color-only distinction. Structural checks give SVG/PNG correlation
`0.9905` and stored PDF/PNG MAE `5.8041`.

Principal output hashes are:

```text
abce445fc6409bf8b412fab47620aeca5b748499cf953b9a40aa7d1fc8a46df5  figure.pdf
7fd3b52f152e6fbc2d17325f6b1fc6f16172b7e5c3b0dcd72e7028624125e6f6  figure.png
9403d5f042b17b8903a9c6cc1a0d51456412c09652b799ad3e75f794b2f86240  figure.svg
51ea70e533db643096d6801759aa94f18e1e7ee71c21bb3c21ba6a549be5ae55  manifest.json
6c3b7accdaa6600634d7fbe7b50c33f34a36baa3fa48ff8a6becef8f3d21c04d  validation.json
860a97d197c77cd65253a209e8840a31d0e1bea76381355caf70fe7432465c2a  SHA256SUMS
```

No genuine temporary-root, home-directory, or machine-specific source path was
found in the sealed package. No GPU, DGX, network, DNS, or time-stepped PDE
computation underlies the figure.

## 5. Claim-boundary verdict

The caption and machine ledger consistently identify an analytic obstruction:
the exact shear family has zero production channels at every positive scale,
strictly positive gradient covariance, and cubic positive size. This refutes
only a zero-preserving production-only coercivity modulus with finite
amplitude-independent value at zero.

The package does not claim novelty for the basic shear mechanism, turbulence
closure validation, a singular solution, epsilon regularity, arbitrary-data
global regularity, or a Clay/Millennium solution. Within that boundary, the
final verdict is `RELEASE_GATE_PASS`. `NOT DNS`. `NOT CLAY`.
