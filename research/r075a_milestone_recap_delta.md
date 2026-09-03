# R0.75A milestone recap delta

## 0. Handoff boundary and frozen state

This delta extends the existing R0.61--R0.74O cumulative recap through
R0.75A. It is content input only to the existing active FIFO publication
task `01a06480-0532-7fd0-bdf0-57571465a2d4`: append the eventual R0.75A
action exactly once after `R0.74Z-Step25`. Do not create a separate recap,
reflection, “lessons learned”, publication task, or publication system. This
delta is not executable publication authority; that requires a separately
frozen R0.75A publication handoff.

- Core commit: `d15b7d8f9a3b16b63b4f324c75c9e156e9d03ff8`.
- Figure archive commit: `243969b9d75d71224070bbdb3da64ce0103c1441`.
- A main: `f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388`.
- A primary audit: `c599a1dcee8a82ec1c91512d5b664b1394707fd6d69ac2ca7ba022ebf715d3f6`
  (PASS, blockers 0).
- A literature audit: `169eff2e607338ae990fb9994db3f75e11830246a36ee5cce8a7376e64302cea`
  (PASS; closest pure-heat precedent identified; the bounded direct-collision
  non-hit is not a novelty or priority finding).

Available certificate and figure objects are frozen as follows.

| artifact | SHA-256 |
|---|---|
| `research/r075a_spectral_persistence_payment_dichotomy_certificate.json` | `7f504c91bcfcb8ba463c0dec977d946d8f36b26b4f732a2082863bbe5221a38e` |
| `research/r075a_spectral_persistence_payment_dichotomy_certificate_report.md` | `bfb87b97e661703c4a7ddd6231b50058dfe116d0d9343d9a6e4c1554714ef238` |
| `research/r075a_spectral_persistence_payment_dichotomy_certificate_independent_audit.md` | `966335bf8a6e759abda01c61d17ef3be4ee3c76e6dd4396b33d6488874dc4960` |
| `research/r075a_spectral_persistence_payment_dichotomy_certificate_qa_report.md` | `83cc4ff615823d1ce8b1b87d60004bf310f86b4faac2d876fb49b8deef2f0d84` |
| `research/figures/r075a/fig-r075a-local-persistence-payment/figure.svg` | `cfbb92394ebbcb5ce9603b3f7df32568e37837c5b2238112b69bfec31f8dfe27` |
| `research/figures/r075a/fig-r075a-local-persistence-payment/figure.png` | `81546061c9febeac81ff683e8a7bd0811d7a9f3c10a90db05037febc0ee25d70` |
| `research/figures/r075a/fig-r075a-local-persistence-payment/figure.pdf` | `ab588b17586d556744bebe8a5957725f4f92033bc1d0133619710c76aee13f5f` |
| `research/figures/r075a/fig-r075a-local-persistence-payment/manifest.json` | `f354dc90a34f8f322bfce0a6f9879487f417e483b0fe128d875e7dec3e9c7a38` |
| `research/figures/r075a/fig-r075a-local-persistence-payment/validation.json` | `91cfa04c6f807b5112c08cd1d11fc34e5fa760634158de8520439b159b589f98` |
| `research/figures/r075a/fig-r075a-local-persistence-payment/qa-report.md` | `098a99edfaf30f8df50ab4605774d714c56fc32b88a448aa5805d82a393c6aa0` |

## 1. Milestone summary

P--A converted a broad clock-compression problem into one proved local
dichotomy and one sharply isolated remaining gap. The route completed the
local-energy clock, pressure-tested finite deletion with exact common-shear
multipackets, corrected the order of time/deletion quantifiers, proved
schedule-invariant residence and remote adjacent-inward witnesses, and
tested three-packet and cancellation-cell routes. R0.75A finally removes
the “arbitrarily short endpoint focusing” escape for the W remote kinetic
witness: either localized mass persists backward, or the mass accumulated
during its rapid change forces the same exterior cubic payment. The next
problem is complete-clock extraction, not spectral persistence.

## 2. Node ledger: problem / result / rejected route / boundary / next

### P — defect-completed clock

- **Problem:** define a suitable-weak clock without losing anomalous
  dissipation.
- **Result:** \(K=Q+F=E+D\ge0\); quadratic and flux variations obey the
  inherited \((P_R^M)^{2/3}\) and \(P_R^M\) ledgers.
- **Rejected:** defect-only detection; circular full-dissipation baseline.
- **Boundary:** rigorous ledger/compactness, not best-\(N\) compression.
- **Next:** exact multipacket stress test.

### Q — common-shear multipackets

- **Problem:** realize many coordinates by exact smooth unforced NSE.
- **Result:** finite same-shear passive packets and inversion partners are
  exact; canonical equal-target families incur central/exterior payment.
- **Rejected:** naive additivity and the canonical cheap-payment design.
- **Boundary:** constructed-family theorem, not universal exclusion;
  literature non-hit is not novelty.
- **Next:** arbitrary-clock extraction.

### R — arbitrary clocks

- **Problem:** extract a persistent lobe or paid branch from a large clock.
- **Result:** endpoint averaging, padded persistence, good-time closure,
  and conditional lobe extraction; an exposed persistent lobe pays cubically.
- **Rejected:** abstract clock examples as a substitute for PDE extraction.
- **Boundary:** uniform arbitrary-suitable-weak extraction remains OPEN.
- **Next:** fix deletion/time quantifiers.

### S — fixed-deletion quantifiers

- **Problem:** order terminal time, deletion set, and shell supremum.
- **Result:** hybrid, fixed-set simultaneous height, and coordinatewise
  excursion were ordered; fixed hybrid and simultaneous height are
  target-scale equivalent after known payments.
- **Rejected:** absolute variation and separable coordinatewise maxima.
- **Boundary:** functional counterexamples, not NSE counterexamples.
- **Next:** schedule-invariant physical residence.

### T — schedule-invariant dwell

- **Problem:** asynchronous lobes after one deletion.
- **Result:** \(\theta R^3\) residence forces exact exterior cubic payment;
  two nonnegative clocks give the correct \(N=1\) floor.
- **Rejected:** replacing \(K\) by \(H_{\rm fix}\), reversed bounds, and
  unproved arbitrary target-time shifts.
- **Boundary:** local coercivity proved; full-clock extraction OPEN.
- **Next:** certify actual packet residence.

### U — intrinsic residence

- **Problem:** retain dominance through a full terminal slab.
- **Result:** exact corridor/slab/all-winding estimates give a total-field
  lobe and \(\Omega(LR^3)\) certified residence.
- **Rejected:** transferring corridor occupation to the full \(K\)-superlevel
  set or upgrading \(\Omega\) to \(\Theta\).
- **Boundary:** explicit-family lower theorem, not maximal-clock upper.
- **Next:** completed-clock upper ledger.

### V — completed-clock upper screen

- **Problem:** bound every explicit-family clock row.
- **Result:** exact lifted tiling and coarse shear/packet scale budgets;
  (V.46)--(V.50) are restricted to six central-chart pairs, but the
  whole-annulus occupation estimates on even that finite table remain OPEN.
- **Rejected:** all-shell \(K\)-upper, arbitrary-\(k\) extension, torus cap,
  and omission of accumulated dissipation.
- **Boundary:** all-shell upper remains OPEN.
- **Next:** adjacent-inward remote comparison.

### W — remote adjacent inward

- **Problem:** test the outer packet one dyadic shell inward.
- **Result:** all-winding survival, inversion/cross margins, and exact
  endpoint geometry produce a remote lower witness.
- **Rejected:** absolute \(o(1)\), free age, deleted windings, whole-shell
  promotion.
- **Boundary:** no fixed-deletion or whole-clock upper theorem.
- **Next:** three-packet payment gate.

### X — three-packet gate

- **Problem:** retain two coordinates after one deletion with cheap payment.
- **Result:** exact three-packet algebra, four cross margins and two endpoint
  lowers prove a two-coordinate endpoint obstruction.
- **Rejected:** promoting two actual-strip uppers to whole-clock upper.
- **Boundary:** payment-normalized fixed-deletion counterexample NOT PROVED.
- **Next:** payment-compatible cancellation.

### Y — route screen

- **Problem:** cancel the target while preserving the remote coordinate.
- **Result:** exact arithmetic rejects frozen geometry and finds a formal
  changed-geometry exponent window.
- **Rejected:** dyadic \(r\ge2\) route; accumulated-viscosity dimensional
  screening as a theorem.
- **Boundary:** necessary window, not construction; platform, windings,
  survival and \(H^1\)-occupation require reproving.
- **Next:** cancellation-cell gate.

### Z — cancellation cell

- **Problem:** can finite Gaussian/Hermite/time-offset cells focus only at
  the endpoint?
- **Result:** exact closure, time-tame conditional persistence, and strict
  subcritical dwell obstruction with positive exact payment gap.
- **Rejected:** literal vertical/time translates, qualitative analyticity
  as quantitative theorem, unconditioned finite-family claims.
- **Boundary:** at Z, critical/ill-conditioned endpoint focusing and full
  Y.57 clock remained OPEN; literature result was finite non-hit only.
- **Next:** exact moving-cutoff identity.

### A — moving-cutoff dichotomy

- **Problem:** can arbitrarily short total-field endpoint focusing evade
  W-kinetic payment?
- **Result:** for the exact smooth common-shear family,
  \[
  (P_R^M)^{2/3}\gtrsim
  h_{\rm rem}R^{2/3}\omega^{-5/6}L^{-1/6},
  \]
  with exact positive exponent gap \(64279/238140000\). Persistence and
  rapid-drop cases are exhaustive, uniformly over finite-family size and
  conditioning.
- **Rejected:** a backward-growing Fourier mode as counterexample;
  horizontal band as full generator control; global modal energy as
  automatic local payment; need for spectral observability in this lemma.
- **Boundary:** positive-volume endpoint core and exact smooth family only;
  no complete-clock upper, fixed deletion, or suitable-weak extension.
- **Next:** remote complete-clock extraction, including endpoint,
  accumulated, and off-target rows without converting a strip lower into a
  whole-shell upper.

## 3. Evidence labels and literature boundary

The publication must visibly distinguish:

1. **analytic theorem/lemma** passed by primary audit;
2. **finite exact certificate** for rationals, hashes, sentinels and
   mutations, which is not a continuous PDE proof;
3. **bounded literature non-hit**, which proves neither novelty nor priority;
4. **OPEN proposition**: complete-clock extraction, fixed deletion,
   suitable-weak extension, contraction and regularity.

The pure-heat nested inner/outer cutoff has a methodological precedent in
Wang--Wang--Zhang--Zhang, arXiv:1711.04279, Section 3.2. R0.75A retains
its proof because residual shear, a moving periodic strip, shell weights,
and Version-M cubic payment are additional ingredients. Do not imply
novelty, priority, or a Clay advance.

## 4. Instructions for the one publication task

Use only the active FIFO publication task
`01a06480-0532-7fd0-bdf0-57571465a2d4`. Append the authorized R0.75A
action exactly once after `R0.74Z-Step25`; do not reuse the archived same-name
task and do not create another task.

Extend, do not replace, the R0.61--R0.74O cumulative recap:

1. milestone banner and the paragraph in Section 1;
2. P--A timeline using the five fields above;
3. a short “what changed at A” panel with the dichotomy and exact fraction;
4. an “OPEN next” panel led by remote complete-clock extraction;
5. an audit box with both A commits, the three A prose hashes, and the frozen
   certificate/figure ledger in Section 0;
6. links to main/primary/literature/certificate artifacts when available;
7. explicit “bounded non-hit, not novelty/priority” and “NOT CLAY”.

Also update homepage/latest-research counters and navigation through A,
then run the existing publication task's build, link, mobile/desktop, and
deployed-byte checks. Do not create a separate recap task, reflection task,
or second publication task/system. This delta authorizes no commit, public
edit, or deployment; a separate frozen publication handoff must do so.
**NOT CLAY.**
