# R0.73R figure QA protocol

The package uses a fail-closed independent validator after rendering and
before either preseal or formal sealing.

1. Recompute the Rudin--Shapiro coefficients from the recursion and verify
   that every coefficient is \(+1\) or \(-1\).
2. Verify that Panel A contains \(m^2\) records per displayed positive
   packet, that both packets use the same \((q,s)\) sites, and that every
   modulus is \(1/(\sqrt2m)\).
3. Verify the omitted negative packet by conjugate reflection and confirm the
   total support size \(2m^2\).
4. Recompute every Panel B and C row directly from the recorded powers of
   \(m\). Confirm slopes \(1/6,-1/2,2/3,-1/6,0,-2/3,1/3\) without
   numerical fitting.
5. Confirm that the PDF and SVG remain vector outputs and that the PNG is
   600 dpi at 178 by 94 mm.
6. Inspect the figure at final print size and in grayscale. Filled circles,
   open squares, triangles, diamonds, and line styles must preserve every
   distinction without colour.
7. Inspect titles, axes, legend text, marker overlap, and the footer. The
   words `analytic scaling` and `not simulation` must remain visible.
8. Confirm that no panel is described as a Navier--Stokes simulation,
   measured norm value, fitted exponent, necessary criterion, unsafe
   dynamics, or Clay result.

## Two-stage sealing

- `--preseal --confirm-visual-qa` may record successful formula, surface, and
  visual checks, but must leave `sourceBindings` empty and status
  `source-unsealed-preseal`.
- `--final --source-commit <40_HEX> --confirm-visual-qa` is allowed only after
  the ten source files have been committed. The validator reads each blob
  directly from the named commit and requires byte-identical SHA-256 values.
- `--verify-only` rechecks the live assets, recorded manifest hashes,
  checksums, status, and (in final mode) every committed source binding.

Formal status never follows merely from a successful render or visual review.
