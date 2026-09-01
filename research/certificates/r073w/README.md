# R0.73W exact signed subgrid-production certificate

This package checks a finite Fourier witness for

\[
 \Pi_s=-\tau_s:\nabla v_s,
 \qquad v_s=e^{s\Delta}u,
 \qquad \tau_s=e^{s\Delta}(u\otimes u)-v_s\otimes v_s.
\]

The domain is \(\mathbb T^3=[0,2\pi]^3\) with normalized Haar probability
measure.  I set \(q=e^{-s}\), so the heat multiplier at mode \(k\) is
\(q^{|k|^2}\).  The primary field is

\[
 R=\bigl(\cos(y+z)-\sin(x+y+z)+\cos(2z),
          \cos x+\sin(x+y+z),0\bigr).
\]

It is real, mean-zero, and divergence-free.  Its Fourier support has exact
rational rank three.  The rank is recomputed from the actual support in both
producers.

## Two independent exact producers

`compute_fourier_certificate.py` uses sparse complex Fourier modes and
Gaussian-rational Laurent-polynomial dictionaries.  It reconstructs the
stress, velocity gradient, production, and gradient energies by convolution.

`independent_trig_certificate.py` does not import the primary producer.  It
starts from the real \(\cos/\sin\) field, uses product-to-sum identities, and
stores rational \(q\)-polynomials as dense tuples.  The two paths use
different bases and different polynomial data structures.

Both producers rebuild the full stress and certify

\[
 \frac{\langle\Pi_s(AR)\rangle}{A^3}
 =\frac14q^2(1-q^2),
\]

\[
 \langle|\nabla R|^2\rangle=\frac{13}{2},
 \qquad
 \frac{\langle|\nabla v_s|^2\rangle}{A^2}
 =\frac12q^2+q^4+3q^6+2q^8,
\]

and

\[
 \frac{\langle D_{ii,s}\rangle}{A^2}
 =\frac12(1-q^2)+(1-q^4)+3(1-q^6)+2(1-q^8).
\]

The scripts recompute \(-R\) rather than only declaring parity.  They verify
that stress and gradient defect are even while production is odd.

For \(A>0\), \(\nu>0\), and \(0<q<1\), the exact mean absorption ratio is

\[
 \frac{|\langle\Pi_s\rangle|}
 {\nu\langle D_{ii,s}\rangle}
 =\frac{Aq^2}{2\nu(13+12q^2+10q^4+4q^6)}.
\]

It grows linearly in \(A\), and its coefficient tends to \(1/(78\nu)\) as
\(s\downarrow0\).  Thus no amplitude-independent constant can absorb this
mean production by this same-time viscous defect for all amplitudes.

## Diagnostic witnesses retained

The package also retains the originally requested 2D3C field

\[
 U=(0,-2,-1)\cos x+(-2,0,-1)\cos y
   +(-2,2,-1)\sin(x+y),
\]

for which

\[
 \langle\Pi_s(AU)\rangle/A^3=-q^2(1-q^2),\qquad
 \langle D_{ii,s}\rangle/A^2=(1-q^2)(14+9q^2).
\]

An intermediate field

\[
 W=(\cos(y+z)-\sin(x+y+z),\ \cos x+\sin(x+y+z),0)
\]

depends on all three displayed coordinates, but its wavevectors satisfy
\((1,1,1)=(1,0,0)+(0,1,1)\).  Its frequency rank is only two and
\((\partial_y-\partial_z)W=0\).  The package labels it as a rank-two triad,
not as a rank-three field.  Adding \((\cos 2z,0,0)\) produces the primary
rank-three extension \(R\).  The two producers fully recompute its cubic
mean; they do not assume that the new cross terms vanish.

## Reproduction

Run the six commands in `command.txt` from the repository root.  The first
two producers write `results.json` and `independent-results.json`.  The seal
script requires their complete `commonCore` objects to agree byte for byte,
then writes `manifest.json` and `SHA256SUMS` with file hashes and the
common-core digest.

This initial manifest is intentionally
`COMPUTED_HASH_BOUND_PENDING_COMMIT_SEAL`.  It contains no git pin.  After
the nine source files are committed, pass the full lowercase 40-hex commit
through `--source-commit`.  The final seal reads each source blob with
`git cat-file`, rejects a missing or byte-different blob, and records the blob
object identifier.  The two final commands are included in `command.txt`.
The resulting status is `SEALED_COMMIT_BOUND`; its `SHA256SUMS` binds all
eleven source/generated inputs plus `manifest.json`.

The machine-readable primary witness key is `rankThreeExtension`.  The
top-level `field`, `identities`, and `ratio` objects in `contract.json` are
retained only for the originally requested 2D3C diagnostic and must not be
read as the primary witness.

No floating point, third-party package, network access, GPU, or DGX is used.
Ordinary translation path: `LOCAL_DIRECT_NO_DGX`; `dgxUsed=false`.

## Boundary

The certificate disproves a narrowly stated amplitude-independent
spatial-mean absorption inequality and a universal pointwise one-sided sign
rule across all fields.  It does not prove that either individual witness
changes sign pointwise, a singularity, arbitrary-data global regularity, or
the Clay conclusion.  See
`claim-boundary.md`.  `NOT CLAY`.
