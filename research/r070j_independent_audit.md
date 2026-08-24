# R0.70J independent internal audit

**Release:** R0.70J
**Audit date:** 2026-08-24
**Scope:** mathematical correctness, realization, source use, figure integrity,
and claim boundary

## Overall verdict

Overall verdict: PASS.

This is an internal independent audit, not external peer review. The verdict
certifies only the finite R0.70J route decision and its archived evidence. It
does not certify a Navier--Stokes regularity theorem, a singularity mechanism,
or a solution of the Millennium problem.

## Exact algebra and helical sector

- The STF contraction reduces exactly to
  \(S:\operatorname{dev}(w\otimes w)=w^{\mathsf T}Sw\).
- The real pure-helicity, phase-averaged symbol is
  \(K_S(\xi)=-\xi^{\mathsf T}S\xi\); it is independent of helicity and even
  under \(\xi\mapsto-\xi\).
- For \(S_0=\operatorname{diag}(1/2,1/2,-1)\), both helicities give the
  pointwise coupling \(1\). Hence every nonzero nonnegative physical cutoff
  retains a strictly positive pairing.
- The full-sphere signed mean is zero, while its positive-part mean is
  \(\sqrt3/9\). The same-shell witness and the weighted second-order-isotropy
  criterion were checked independently.

Verdict: PASS.

## Compact realization and scale ledger

- The compact homotopy construction produces the prescribed exterior STF
  strain on an open core and retains all transition-annulus vorticity.
- Constant and locally helical compact core carriers are divergence-free;
  their return vorticity is retained.
- The buffered convolution filter and annular selector separate the exterior
  source from the core carrier exactly on the observation region.
- The \(a,r,\Lambda\) ledger is dimensionally and algebraically consistent.
  In particular, the pairing is \(a^3\Lambda^{-2}\), and at
  \(a=r^{-1/2}\) it is \(\Lambda^{-2}r^{-3/2}\).
- The nonnegative, nonzero time envelope gives \(\int\theta^3>0\), so the
  strict sign in the parabolic comparator is justified.

Verdict: PASS.

## NSE and pressure boundaries

- The small-\(L^3\) construction proves only sign persistence near an initial
  face. Under co-scaling, the positive intervals shrink like \(r^2\); it does
  not produce a cascade at one fixed positive terminal time.
- The pressure construction realizes a prescribed STF center coefficient
  \(\nabla^2p(0)=S\) by a finite positive orbit combination with the required
  dilation-amplitude compensation. It does not realize an open-core constant
  pressure Hessian or a self-consistent concentrating trajectory.

Verdict: PASS.

## Literature and figure audit

- The bounded ten-source primary-literature audit distinguishes direct source
  results, R0.70J inferences, and applicability boundaries. No absence claim
  is inferred from the bounded search.
- The journal figure is a closed-form analytic visualization, not DNS. Its
  600 dpi PNG, vector PDF/SVG, data, contract, caption, manifest, and 22-check
  validation agree. Visual inspection found no curve, label, annotation, or
  legend collision.

Verdict: PASS.

## Reproduction gates

- The R0.70J focused gate passed 14/14 tests, including producer-to-archive
  equality, seven payload hashes, and the complete figure package.
- The repository regression suite passed 539/539 tests in the pinned
  scientific Python environment.

Verdict: PASS.

## Route decision certified

The universal algebraic-null route based only on trace freedom,
incompressibility, fixed helicity, phase/angular averaging, and physical
cutoff is closed by an exact counterexample. A successful continuation must
instead quantify anisotropy or exploit a source-aware, equation-correlated
spacetime mechanism. This route decision is narrower than, and must not be
reported as, progress proving the Millennium statement itself.
