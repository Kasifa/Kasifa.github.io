# Figure contract - fig-r071h-angular-curvature

## Analytical question

Does the exact projective heat identity yield the weighted-BV budget needed
after R0.71G, or do pointwise angular growth, cutoff source saturation, and a
two-power frequency gap remain?

## Supported takeaway

The figure supports four limited statements.

1. Pure heat has an exact Rayleigh-payment identity for projective rotation
   and spectral curvature.
2. A fixed-energy global-smooth 2D3C family disproves a uniform energy-only
   bound for the unweighted instantaneous angular speed at \(t=0\), while
   its source density approaches a finite limit.
3. One fixed finite-Fourier cutoff has finite Rayleigh and projective source
   quotients across \(0\leq\delta\leq1\).
4. The direct weighted-BV Young estimate requires a coefficient two powers
   of \(K\) stronger than the known heat-bulk coefficient.

The figure does not establish or refute a general time-integrated angular or
weighted-BV bound.

## Evidence classes

- **Closed-form pure heat model:** two orthogonal eigenmodes of a positive
  operator with eigenvalues 1 and 4.
- **Exact initial-time NSE algebra:** the finite Fourier datum belongs to a
  global-smooth 2D3C Navier-Stokes family, but only its true initial time is
  displayed.
- **Exact finite-Fourier cutoff algebra:** \(R_\delta\) and \(J_\delta\) are
  rational functions obtained by Fourier orthogonality.
- **Exact scaling bookkeeping:** the Panel D exponents are analytical and
  are not regression estimates.

## Panel contract

- **A - pure heat payment.** Display the Rayleigh drop, the cumulative
  angular-speed square, the cumulative spectral-curvature square, and their
  exact sum. The two half-payment curves coincide but remain identifiable by
  markers and line styles.
- **B - fixed-energy initial data.** Display
  \(\Omega_K(0)=K/2\) and
  \(S_K(0)=\frac14(3+2/K)^2\) for powers of two through \(K=256\). The title
  and in-panel annotation must say that the comparison is at \(t=0\).
- **C - cutoff quotient.** Display \(R_\delta\) and \(J_\delta\) for the
  fixed cutoff \(\chi_\delta=(1+\delta\cos Z)/2\).
- **D - two-power gap.** Display the available \(K^{-2}\) weight, the direct
  required weight \(1\), and the exact gap ratio \(K^2\). Label the panel as
  a scaling comparison.

## Data and numerical grain

- Total rows: 391.
- Panel A: 61 times on \(0\le t\le1.5\), four exact series.
- Panel B: nine integer powers of two, two exact initial-time series.
- Panel C: 51 exact cutoff values on \(0\le\delta\le1\).
- Panel D: nine integer powers of two, three exact scaling series.
- Producer arithmetic: IEEE binary64 formula evaluation.
- Independent arithmetic: 60-digit Python Decimal recomputation.
- Random seed: none.
- No fitted parameters, ODE integration, PDE time stepping, or DNS.

## Visual and archival rules

- Static double-column figure, exactly 178 by 108 millimetres.
- Vector PDF and SVG plus a 600 dpi PNG.
- Marker and line-style distinctions must preserve every comparison in
  grayscale.
- Inspect the full-resolution PNG, the grayscale preview, and an independently
  rasterized PDF.
- Archive the CSV, producer, plotter, two validation paths, caption,
  environment, commands, manifest, QA report, and SHA-256 ledger.

## Claim boundary

The pointwise no-go applies only to unweighted angular speed at one true
initial time. It does not disprove the integrated projective source budget,
integrated turning, or the weighted-BV target. Panel C concerns one fixed
cutoff template. Panel D diagnoses the direct Young route but does not rule
out a deeper PDE cancellation. Nothing here proves regularity, constructs a
singularity, establishes originality, or resolves the Millennium problem.
