# Figure contract — R0.63 time-layer transfer

- Analytical question: what finite state system actually closes the
  heat-weighted quartic correlation, and do hostile finite targets already
  contradict the desired `O(M)` scale?
- Takeaway: the two-state sign recursion lifts exactly to eight cubic states
  and sixteen target-signed states with carries; six hostile heat-weighted
  probes through `M=131072` remain at `S4/M` scale `10^-2`, but their growing
  cancellation condition prevents a numerical proof claim.
- Family: transfer diagram plus two quantitative diagnostic panels.
- Data sufficiency: exact integer lift through ten dyadic levels, 27
  time-layer factorization regressions, and six hostile targets containing up
  to 28,977,859,974 ordered paths.
- Static renderer: Matplotlib; 178 mm by 96 mm.
- Palette policy: blue for exact transfer structure, rust for numerical
  conditioning, neutral ink, and one gold boundary annotation.
- Non-color encoding: boxes and arrows, open circle versus square markers,
  solid versus dashed lines, direct labels, and explicit logarithmic axes.
- Exports: vector PDF, SVG, and 600 dpi PNG.
- Final QA: color PNG, true grayscale, Poppler-rendered PDF, embedded fonts,
  extracted PDF text, and source-data validation.
