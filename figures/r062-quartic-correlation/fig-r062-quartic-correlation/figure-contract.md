# Figure contract — R0.62 quartic correlation

- Analytical question: does the new all-index `O(sqrt(M))` ceiling describe
  the observed heat-weighted quartic target, and why does the unweighted
  tensor correlation not by itself prove a uniform bound?
- Takeaway: complete heat-weighted target profiles remain at scale `10^-3`
  through `M=2048`, while an ordinary outer Rudin--Shapiro convolution grows
  after normalization by `M`; the heat weight must be retained in the next
  lemma.
- Family: three-panel research line figure.
- Data sufficiency: 3,840 complete target evaluations for `L=1` and
  `M=256,512,1024,2048`; 13 dyadic unweighted convolution levels from
  `M=256` through `M=1,048,576`.
- Static renderer: Matplotlib; 178 mm by 112 mm.
- Palette policy: hard two-root cap, blue for heat-weighted data and rust for
  unweighted data, plus neutral ink and gold annotation.
- Non-color encoding: distinct panels, solid versus dashed strokes, open
  markers, direct labels, and explicit units.
- Exports: vector PDF, SVG, and 600 dpi PNG.
- Final QA: color PNG, true grayscale, Poppler-rendered PDF, embedded fonts,
  extracted PDF text, and source-data validation.
