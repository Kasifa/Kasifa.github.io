# Chart contract and source data

**Analytical question.** Why does subtracting only the constant global mean fail to restore the frozen Version-A pure \(P_R^{2/3}\) endpoint, even for an exact zero-total-mean smooth periodic Navier--Stokes family?

**One-sentence takeaway.** A zero-global-mean decaying shear transports a localized derivative-heat packet toward a fixed Version-A centre; the one-sided residual drift preserves the target while suppressing fixed-centre leakage, and the resulting target dominates all three frozen payment rows along the explicit analytic sequence.

**Surface and format.** One static, journal-width, three-panel proof schematic; Matplotlib renderer; 180 x 82 mm; live-text SVG, one-page embedded-font PDF, and approximately 600 dpi RGB PNG. Grayscale and final-size derivatives are mandatory. This is a closed-form analytic figure, not DNS, a numerical trajectory, or a simulation.

**Panel contract.** Panel A shows the exact zero-global-mean field \(u=(AF,B_Re^{-t}\cos x_3,0)\), the fixed Version-A centre, the reference path from \(q_*=1/2\) to \(q_m=M_mR\), and the scale-\(R\) packet. Panel B shows the signed residual drift \(d=B_Re^{-t}(1-\cos x_3)\le0\), the target bridge error \(O(R)\), the seam-safe one-sided Gaussian mechanism, and the strict exponent margin \(1/264>1/288\). Panel C shows separately the background, local-leakage, and exterior-residence ratios tending to infinity, followed by the exact narrow conclusion and the still-open local/mollified-frame or explicit-flux repairs.

**Canonical source grain.** `source-data.csv` contains one row per displayed geometry identity, stochastic/sign mechanism, exponent, payment row, asymptotic ratio, or scope boundary. Every quantitative row is copied from the frozen theorem at commit `ff80370fe33094f1423d312b817dfec0bf42d664`, SHA-256 `bc9f7557e27bb86d5730273985b60f7135ccea3adc2fc99b2daf7778e70c9124`. Unknown constants are labels only and are never encoded as numerical observations.

**Certificate gate.** Certificate provenance is bound only after `research/r074d_zero_mean_transport_certificate.json` has a stable `PASS` hash and check count. Plotting and validation must refuse a mismatched theorem or certificate hash.

**Palette and non-color distinction.** Single blue root for exact/proved mechanisms, amber for open boundaries, deep red only for the rejected frozen endpoint, and neutral greys for prior-art/scope text. Solid versus dashed strokes, open versus filled boxes, hatching, direct labels, and panel separation preserve meaning in grayscale; color is never the sole encoding.

**Required visible labels.** `EXACT NSE`, `PROVED`, `OPEN`, `PRIOR ART`, `NO DNS`, and `NOT CLAY` must appear as live SVG text. The figure must state that local/mollified frames and an explicit entrance-flux payment remain open, and it must make no priority claim.

**QA contract.** Exact 25-file inventory; two complete generate/validate runs with 25/25 byte identity; all text files free of whitespace defects; all `SHA256SUMS` entries verified; one 180 x 82 mm PDF page with embedded fonts; at least 4250 x 1936 pixels for the master PNG; live SVG text with no raster image and no base label below 6 pt; visual inspection of the master, PDF render, grayscale render, and final-size derivative.
