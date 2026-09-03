# R0.75A milestone recap delta -- independent rebound audit

## 0. Frozen object, method, and verdict

This rebound audit binds exactly:

| object | SHA-256 | size |
|---|---|---:|
| research/r075a_milestone_recap_delta.md | 7dd9ac686d0c599b21992bf7622e862f88caf0480f6e27f2cb82b9aaf844eee1 | 225 lines, 11653 bytes |

The review was fail-closed. I compared the revised delta with the frozen
R0.74P--Z and R0.75A notes, their independent audits and certificates, the
two A commits, the formal figure archive, the prior publication handoffs, and
the historical R0.74O recap baseline. I also rechecked every repair required
by the earlier blocked audit.

**Verdict: PASS. Blocker count: 0. Remaining corrections required: 0.**

The recap candidate was not edited. This audit created no commit, task,
public artifact, or deployment.

## 1. Rebound of the three prior blockers

### R1. R0.74V finite-table claim grade -- closed

Lines 114--116 now say that exact lifted tiling and coarse shear/packet scale
budgets are proved, while (V.46)--(V.50) are restricted to six central-chart
pairs and their whole-annulus occupation estimates remain OPEN even on that
finite table.

This matches frozen R0.74V exactly. V proves the lifted tiling, scale budgets,
and conditional algebra. It proposes, but does not prove, the finite-table
estimates (V.47)--(V.50), the target-coordinate upper (V.56), or any
all-\(k\) lifted-copy extension. The revised recap no longer converts the
six-pair domain restriction into analytic closure.

### R2. Unique publication-task and queue binding -- closed

Both the opening boundary and Section 4 now bind the only permitted
destination to active FIFO task

    01a06480-0532-7fd0-bdf0-57571465a2d4

and require exactly one append after R0.74Z-Step25. They prohibit reuse of the
archived same-name task and prohibit a separate recap, reflection,
lessons-learned, publication task, or publication system. This agrees with
the current R0.74T--Z handoffs and removes the ambiguity created by the older
R0.74P/Q publication-task generation.

The authorization boundary is explicit twice: this delta is content input,
not executable publication authority, and a separately frozen R0.75A
publication handoff is required before any commit, public edit, or
deployment. The absence of that handoff is therefore a deliberate hold, not
a silent publication authorization.

### R3. A commits, certificate, and figure ledger -- closed

The two commits in lines 13--14 are valid:

| role | commit | parent / content check |
|---|---|---|
| research core | d15b7d8f9a3b16b63b4f324c75c9e156e9d03ff8 | contains the main note, prose audits, certificate files, and certificate scripts |
| figure archive | 243969b9d75d71224070bbdb3da64ce0103c1441 | parent is the core commit; contains the 25-file formal figure archive |

The three prose hashes match both the current bytes and their blobs at the
core commit:

| prose artifact | recomputed SHA-256 |
|---|---|
| A main | f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388 |
| A primary audit | c599a1dcee8a82ec1c91512d5b664b1394707fd6d69ac2ca7ba022ebf715d3f6 |
| A literature audit | 169eff2e607338ae990fb9994db3f75e11830246a36ee5cce8a7376e64302cea |

All ten newly listed certificate/figure paths exist. Their printed hashes
match both the working-tree bytes and the blobs in the appropriate commit:

| A artifact | recomputed SHA-256 |
|---|---|
| certificate JSON | 7f504c91bcfcb8ba463c0dec977d946d8f36b26b4f732a2082863bbe5221a38e |
| certificate report | bfb87b97e661703c4a7ddd6231b50058dfe116d0d9343d9a6e4c1554714ef238 |
| independent certificate audit | 966335bf8a6e759abda01c61d17ef3be4ee3c76e6dd4396b33d6488874dc4960 |
| certificate QA report | 83cc4ff615823d1ce8b1b87d60004bf310f86b4faac2d876fb49b8deef2f0d84 |
| figure SVG | cfbb92394ebbcb5ce9603b3f7df32568e37837c5b2238112b69bfec31f8dfe27 |
| figure PNG | 81546061c9febeac81ff683e8a7bd0811d7a9f3c10a90db05037febc0ee25d70 |
| figure PDF | ab588b17586d556744bebe8a5957725f4f92033bc1d0133619710c76aee13f5f |
| figure manifest | f354dc90a34f8f322bfce0a6f9879487f417e483b0fe128d875e7dec3e9c7a38 |
| figure validation | 91cfa04c6f807b5112c08cd1d11fc34e5fa760634158de8520439b159b589f98 |
| figure QA report | 098a99edfaf30f8df50ab4605774d714c56fc32b88a448aa5805d82a393c6aa0 |

The formal archive's SHA256SUMS independently reports 24/24 entries OK.
Section 4 now instructs the publisher to use both commits, the three prose
hashes, and the frozen certificate/figure ledger.

## 2. P--A node reconstruction

The revised five-field ledger preserves each frozen result, rejected route,
boundary, and next step.

| node | independent reconstruction | disposition |
|---|---|---|
| P | \(K=Q+F=E+D\ge0\), the canonical-AC/good-time boundary, and the \(P^{2/3}\)/\(P\) variation ledgers are proved; defect-only and the circular full-dissipation baseline do not solve best-\(N\) compression. | PASS |
| Q | Finite same-shear inversion-paired packets give exact smooth unforced NSE. Step 2 proves genuine exterior-cubic divergence for its explicit relaxed equal-target family; Step 1's generic exterior statement remains conditional on no cancellation. No universal common-shear exclusion follows. | PASS |
| R | Endpoint averaging, padded persistence, and good-time closure are exact; arbitrary suitable-weak clock extraction remains OPEN, while exposed persistent-lobe payment is a separate proved lemma. | PASS |
| S | The deletion/time quantifier order and target-scale equivalence are correct; the strict separations are functional examples, not NSE counterexamples. | PASS |
| T | A \(\theta R^3\) residence interval pays cubically and two asynchronous nonnegative clocks give the \(N=1\) floor; this is not completed-clock extraction. | PASS |
| U | Corridor/slab/all-winding estimates give \(\Omega(LR^3)\) certified residence for the explicit family; neither whole-superlevel occupation nor an \(\Omega\to\Theta\) upgrade is claimed. | PASS |
| V | Exact tiling, scale budgets, and conditional algebra pass; finite-table occupation and all-shell upper bounds remain OPEN. | PASS |
| W | The all-winding adjacent-inward endpoint witness disproves the frozen matching all-shell \(O(T)\) candidate only for the exact family; it proves neither fixed deletion nor a whole-clock theorem. | PASS |
| X | Two endpoint lower bounds survive one fixed deletion, possibly at different times, but are \(o((P_R^M)^{2/3})\); no payment-normalized fixed-deletion counterexample follows. | PASS |
| Y | Frozen geometry/amplitude routes are screened out and only a formal changed-geometry exponent window survives; construction, survival, windings, and \(H^1\)-occupation remain open. | PASS |
| Z | Persistent/time-tame remote kinetic cells incur the strict payment obstruction; critical ill-conditioned endpoint-only focusing and the full Y.57 clock remain OPEN. | PASS |
| A | The moving-cutoff dichotomy closes arbitrarily short focusing for the positive-volume W remote kinetic witness in the exact smooth family; complete \(K\), fixed deletion, and suitable-weak extension remain OPEN. | PASS |

The principal source hashes were recomputed and remain:

| source | SHA-256 |
|---|---|
| P main | a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867 |
| Q Step 1 | 60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695 |
| Q Step 2 | ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d |
| R extraction / persistent lobe | ac959f30b254001910e5b445264ea7c0d8714afc2f96dcf74505f5e1f794b6b7 / e7f151048e85d95133f8c6414849c0fe9dc40cc48b7a12666b7e21496ddb99b5 |
| S fixed deletion | 305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1 |
| T | 8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd |
| U | e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99 |
| V | 031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c |
| W | d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10 |
| X | 4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3 |
| Y | 6144fe796d6c59a286fc32b3b0aa2b794c50006fdc7879d4595b5958c9646954 |
| Z | bb766da4002da760c35185294081f80df97c349ea08b198a5f76db31663aaf6a |
| A | f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388 |

## 3. R0.75A theorem, certificate, and figure

The displayed A conclusion is exact:

\[
 (P_R^M)^{2/3}\gtrsim
 h_{\rm rem}R^{2/3}\omega^{-5/6}L^{-1/6}.
\]

The exponent rate independently reduces to

\[
 \frac5{24}\frac8{3969}-\frac16\frac9{10000}
 =\frac{64279}{238140000}>0.
\]

The persistent and rapid-drop cases are exhaustive. The total-field local
identity makes the result uniform over finite correction-family size,
coefficients, spectral bandwidth, and temporal condition number. It includes
critical and arbitrarily shorter smooth focusing, but it gives neither a
whole-shell upper nor an upper for the completed clock.

The finite certificate reports PASS 14/14, 64 unique tags, balanced 64/64
displays, resolved references, the exact fraction, and eight rejected
mutations. Its independent and QA reports agree. The formal figure and
caption preserve \(p=32/63\), the nested-strip geometry, the
\(\omega^{1/4}\) payment weight, the exact fraction, the A.63 next step, the
complete-\(K\) boundary, and the analytic-schematic/no-DNS label.

## 4. Literature and NOT CLAY boundary

The literature wording remains accurate and safe. The frozen main note after
(A.22) describes its calculation as a moving-drift, anisotropic version of
the standard nested-cutoff local heat estimate and cites
Wang--Wang--Zhang--Zhang, arXiv:1711.04279, Section 3.2. It then separates
the residual shear, moving periodic strip, shell weight, and Version-M cubic
conversion from that pure-heat precedent. The literature audit treats this
as a close methodological precedent, not a directly applicable theorem.

The delta explicitly says the bounded direct-collision non-hit proves neither
novelty nor priority and forbids novelty, priority, or Clay implications. It
retains complete-clock extraction, fixed deletion, suitable-weak extension,
contraction, and regularity as OPEN. NOT CLAY is explicit both in the
publication instruction and at the terminal boundary.

## 5. Structural and mechanical checks

- The historical R0.61--R0.74O recap is present in publication commit
  d56df13c72c815f7b54c376aeb8ffbaf68fe1716; the delta correctly says to
  extend it rather than replace it.
- P, Q, R, S, T, U, V, W, X, Y, Z, and A occur once each and in order.
- Source targets Y.57 and A.63 exist in the frozen notes.
- Every path in the new artifact table exists; there is no missing or
  mismatched SHA-256 entry.
- The candidate is valid UTF-8 and contains no NUL, CR, tab, or other
  nonprinting C0 control character. Inline and display delimiters balance.
- No strip lower is promoted to a whole-shell upper, and no result is
  extrapolated to fixed deletion, arbitrary suitable weak solutions,
  regularity, singularity, novelty, priority, or a Millennium conclusion.

No main research note, recap source, certificate, figure, Git state, public
artifact, task queue, or deployment was modified by this audit. No commit or
publication was made.

\[
 \boxed{
 \textbf{R0.75A MILESTONE RECAP DELTA: INDEPENDENT PASS; BLOCKERS 0; NOT CLAY.}}
\]
