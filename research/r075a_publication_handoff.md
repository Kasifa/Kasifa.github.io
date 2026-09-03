# R0.75A Step 26 frozen publication handoff

## Release identity and queue order

- release id: R0.75A-Step26
- publication owner: the single active long-lived Codex task `发布任务`
- publication task id: `01a06480-0532-7fd0-bdf0-57571465a2d4`
- logical predecessor: `R0.74Z-Step25`
- queue rule: append exactly once after R0.74Z completes; do not use the
  archived same-name task and do not create another publishing, recap,
  reflection, or “lessons learned” task/system
- frozen research/certificate commit:
  `d15b7d8f9a3b16b63b4f324c75c9e156e9d03ff8`
- frozen figure-archive commit:
  `243969b9d75d71224070bbdb3da64ce0103c1441`
- frozen milestone-recap commit:
  `9f01a3a8df2f60633a16e41eb2a1cb606c750198`
- cumulative recap required: **true**
- formal scientific figure required: **true**

This handoff authorizes only R0.75A and its cumulative P--A recap delta.
Do not read or publish R0.75B, R0.75C, or later work.  Preserve the existing
compact retro site style and append to the existing cumulative recap rather
than replacing it.

## Frozen research, audit, and certificate ledger

| SHA-256 | repository path |
|---|---|
| `f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388` | `research/r075a_spectral_persistence_payment_dichotomy.md` |
| `c599a1dcee8a82ec1c91512d5b664b1394707fd6d69ac2ca7ba022ebf715d3f6` | `research/r075a_spectral_persistence_payment_dichotomy_primary_audit.md` |
| `169eff2e607338ae990fb9994db3f75e11830246a36ee5cce8a7376e64302cea` | `research/r075a_spectral_persistence_payment_dichotomy_literature_audit.md` |
| `ff712f4a846e70a35a5936348574b77ca59ca78c46e56c488ebb4731650afd35` | `research/r075a_spectral_route_risk_audit.md` |
| `7f504c91bcfcb8ba463c0dec977d946d8f36b26b4f732a2082863bbe5221a38e` | `research/r075a_spectral_persistence_payment_dichotomy_certificate.json` |
| `bfb87b97e661703c4a7ddd6231b50058dfe116d0d9343d9a6e4c1554714ef238` | `research/r075a_spectral_persistence_payment_dichotomy_certificate_report.md` |
| `966335bf8a6e759abda01c61d17ef3be4ee3c76e6dd4396b33d6488874dc4960` | `research/r075a_spectral_persistence_payment_dichotomy_certificate_independent_audit.md` |
| `83cc4ff615823d1ce8b1b87d60004bf310f86b4faac2d876fb49b8deef2f0d84` | `research/r075a_spectral_persistence_payment_dichotomy_certificate_qa_report.md` |
| `d5256d8ea9db81adc5133e3cce69b9f7089f8ab8a2c5d39f30877815e6052e5a` | `scripts/r075a_spectral_persistence_payment_dichotomy_certificate.py` |
| `30d28440b4cba3b0578fa7644cf5539ff6a2806f449c020d6cd1718e553ade27` | `scripts/r075a_spectral_persistence_payment_dichotomy_certificate_independent.rb` |
| `b9b07e3d1a8d1303111cf1978481530e791f3e14d81b6865674d16f73caa2538` | `scripts/r075a_spectral_persistence_payment_dichotomy_certificate_qa.sh` |

Certificate status: primary analytic audit **PASS**, blockers 0; literature
audit **PASS**; Python 14/14; Ruby 17/17; eight negative mutations rejected;
`PYTHONHASHSEED=0,1,42` byte-identical.  The certificate is finite exact
arithmetic/structure evidence and is not a continuous PDE proof.

## Milestone recap ledger

| SHA-256 | repository path |
|---|---|
| `7dd9ac686d0c599b21992bf7622e862f88caf0480f6e27f2cb82b9aaf844eee1` | `research/r075a_milestone_recap_delta.md` |
| `f727eb01002772936b5f8aa6e7212e238c7e0e04ab546261232f4abcee9d9b82` | `research/r075a_milestone_recap_delta_independent_audit.md` |

The recap audit is **PASS**, blockers 0.  Extend the already-published
R0.61--R0.74O cumulative recap through R0.75A using this delta.  Preserve its
five-field P--A ledger, especially the corrected R0.74V boundary: the six
central-chart pairs are only the finite table on which occupation estimates
are posed; the whole-annulus occupation estimates remain OPEN.

## Figure archive ledger

Directory:
`research/figures/r075a/fig-r075a-local-persistence-payment/`

- archive: exactly 25 files, 2,588,462 bytes
- 24-file `SHA256SUMS` ledger:
  `bc8ecc26ed0cd934dc7d74060ac94960ecde9a7fcbeb8364b19739023f152373`
- SVG:
  `cfbb92394ebbcb5ce9603b3f7df32568e37837c5b2238112b69bfec31f8dfe27`
- publication PNG:
  `81546061c9febeac81ff683e8a7bd0811d7a9f3c10a90db05037febc0ee25d70`
- one-page vector PDF:
  `ab588b17586d556744bebe8a5957725f4f92033bc1d0133619710c76aee13f5f`
- manifest:
  `f354dc90a34f8f322bfce0a6f9879487f417e483b0fe128d875e7dec3e9c7a38`
- validation record:
  `91cfa04c6f807b5112c08cd1d11fc34e5fa760634158de8520439b159b589f98`
- figure QA report:
  `098a99edfaf30f8df50ab4605774d714c56fc32b88a448aa5805d82a393c6aa0`
- independent verify-only runs with seeds 0, 1, and 42: **PASS**
- 24/24 archive ledger entries: **PASS**
- final-size, greyscale, and PDF visual inspection: **PASS**

Preserve the visible figure scope label:

`ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE SIMULATION | NOT DNS | NO NOVELTY CLAIM | NOT CLAY`

## Result and claim boundary

For the exact smooth periodic inversion-paired common-shear family,

\[
 u=(F,b,0),\qquad
 (\partial_t+b\partial_2-\Delta_{23})F=0,
 \qquad \partial_tb-\partial_3^2b=0,
\]

the Version-M mollified trajectory is zero.  At the W remote coordinate put

\[
 p=\frac{32}{63},\qquad
 \omega=\Gamma^{1/4}.
\]

The exact moving-cutoff local-energy identity yields an exhaustive terminal
dichotomy.  Either local mass persists on the final \(R^3\) interval, or its
rapid endpoint rise forces the same spacetime mass.  In both cases the
scale-\(2R\) exterior cubic row pays the terminal kinetic witness:

\[
 \boxed{
 (P_R^M)^{2/3}
 \ge c h_{\rm rem}R^{2/3}\omega^{-5/6}L^{-1/6}.}
\]

The exact exponential gap is

\[
 \frac{5c_\gamma}{24}-\frac\rho6
 =\frac{64279}{238140000}>0.
\]

Therefore arbitrary short endpoint focusing does not rescue the W remote
kinetic witness within this finite exact smooth family, uniformly in family
size, coefficients, spectral bandwidth, and temporal conditioning.

The nearest screened methodological precedent is the nested local heat
cutoff in Wang--Wang--Zhang--Zhang, arXiv:1711.04279, Section 3.2.  It does
not supply the residual-shear, moving periodic strip, dyadic weight, or
Version-M cubic-payment steps.  The bounded literature non-hit is **not** a
novelty or priority determination.

The release does **not** control the completed clock \(K\), accumulated
dissipation, a fixed deletion, arbitrary suitable weak solutions, a
contraction, or regularity.  Its frozen status is:

- moving-cutoff local identity: **PROVED**;
- persistence/rapid-rise endpoint dichotomy: **PROVED**;
- W remote terminal kinetic payment: **PROVED IN THE EXACT SMOOTH FAMILY**;
- complete-clock extraction and fixed deletion: **OPEN**;
- suitable-weak extension and Clay conclusion: **OPEN / NOT CLAY**.

## Publication and deployment QA

Publish one bilingual research page, the formal SVG/PNG/PDF and complete
figure archive, the certificate/audit artifacts, and the cumulative recap
extension.  Update the homepage latest-research entry, research count,
navigation, literature page, downloadable PDF, version ledger, and global
index through R0.75A.  Keep all equations and exact fractions visible and
keep theorem, certificate, literature, and OPEN labels distinct.

Run the existing publication task's structural tests, internal-link and
asset checks, desktop/mobile render inspection, GitHub Pages workflow check,
and online byte-identity verification.  Report the site commit, workflow run,
page/PDF count, object count, and deployed-byte verdict.  No second task is
authorized.  **NOT CLAY.**
