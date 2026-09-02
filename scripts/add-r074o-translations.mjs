#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const translationRoute = "LOCAL_DIRECT_NO_DGX";
const dgxUsed = false;
const checkOnly = process.argv.includes("--check-only");

// These translations follow the deterministic collectSiteStrings order at the
// frozen R0.74O publication boundary. Keeping the English list separate avoids
// duplicating 135 long Chinese source strings in release code.
const english = [
  ", but this is not yet an arbitrary-flow endpoint.",
  "; if a constant appears in a bilinear upper bound, then",
  "01 / Historical trunk",
  "02 / Four new phases",
  "03 / Retired routes",
  "04 / Evidence classes",
  "05 / New direction",
  "Extrapolating the normalized-amplitude square-root-log match into a universal scalar endpoint is excluded by R0.74O's free passive amplitude.",
  "is excluded by the exact family; the fifth payment shell gives",
  "From signed production to the scalar-payment no-go",
  "Fixed-center transport repairs, including subtraction of only the total mean, are excluded by exact advected and mean-zero 2D3C families;",
  "Analytic results, inherited inputs, finite reconstructions, and literature boundaries remain separate",
  "Exact shear excludes production-only coercivity; positive covariance, mixed covariance, buffer collars, and advected coordinates then separate sign, absolute size, pressure, and transport layer by layer. Exact solutions exclude both fixed-center and mean-only repairs, making a local advected coordinate necessary.",
  "The preceding phase advanced from projected-Lamb heat-volume closure, local heat packing, and the critical bottom trace to exact shear, spectral branches, adiabatic tracking, critical stability tubes, and explicit exterior tails. Any continuation argument that needs a velocity action must still state",
  "Negative conclusions apply only to the stated propositions",
  "The passive amplitude in one exact 2D3C solution can independently amplify quadratic observables without changing the leading scalar-payment scale. The universal square-root-log endpoint is therefore FALSE, and every scalar majorant of order (o(p^{8024/11907}(1+\\log p)^{7/6})) also fails. No optimal replacement frontier is proved here.",
  "The next interface is not another adjustment of a logarithmic power in the scalar payment. It is an independent, scale-critical, non-circular structural observable that passes to suitable weak limits. Its first test is to detect the R0.74O quadratic passive-amplitude growth while retaining pressure, local-energy defect, and moving-tube geometry.",
  "Download the synchronized cumulative-review PDF",
  "A payment ledger that omits the fifth shell cannot support the complete lower bound;",
  "Cites earlier nodes without changing their quantifiers.",
  "A bounded search proves neither novelty, priority, nor completeness.",
  "Read R0.74O",
  "This is the second cumulative review after R0.60. It contains 157 nodes and ends with 217 public notes. It preserves the old R0.61–R0.73X review byte for byte and adds 17 nodes: R0.73Y, R0.73Z, and R0.74A–R0.74O.",
  "These no-go results neither deny Navier–Stokes global regularity nor construct a singularity.",
  "These results prove neither global smoothness for arbitrary three-dimensional data nor a finite-time singularity.",
  "Certificates, figures, and browser QA verify only implementation and finite algebra.",
  "Coercivity using signed production alone is excluded by exact shear;",
  "Lists only analytic propositions completed in the current file.",
  "may be used only under its original hypotheses. These historical inputs are not upgraded by this milestone.",
  "A periodic Brownian bridge gives terminal outer-collar survival; the complete payment ledger then closes and gains a positive collar-flux repair. Version M reaches the suitable weak gate, while",
  "The nearest inward collar is reduced to the only remaining obstruction; the common forward law, short-clock BV, final-segment expulsion, and super-Gaussian outer-shell summation close in sequence. The normalized exact family attains",
  "The optimal frontier, weak stability of an augmented observable, the arbitrary-flow endpoint, and regularity.",
  "F–J｜Exact two-packet family and complete payment",
  "K–N｜All-shell closure and normalized matching",
  "O｜Frozen scalar payment is insufficient",
  "A 157-node cumulative review from R0.61 through R0.74O: retained results, retired routes, evidence classes, and the next augmented-observable interface",
  "R0.61–R0.73X: retain earlier conclusions without rewriting their evidence",
  "R0.61–R0.74O cumulative review｜From projected-Lamb to the scalar-payment no-go",
  "All R0.61–R0.74O nodes",
  "R0.73Y–R0.74O: 17 nodes compress the problem to a new interface",
  "R0.74P: Freeze an augmented observable that detects passive amplitude",
  "Y–E｜From production-only failure to local-coordinate payment",
  "Master index of 217 research notes",
  "95 sections fully sealed",
  "View the R0.74O homepage card",
  "Current boundary:",
  "Current endpoint R0.74O",
  "Frozen scalar payment cannot universally control the quadratic observables. The next step requires an independent structural observable that is weakly stable and detects passive amplitude. Regularity for arbitrary three-dimensional data and Clay remain OPEN.",
  "Freeze an augmented observable that detects quadratic passive amplitude, is scale-critical and non-circular, and passes stably to weak limits.",
  "Cumulative review R0.61–R0.74O · 2026-09-02",
  "Milestone recap",
  "Jump to the R0.74O homepage card →",
  "The free passive amplitude in the same exact 2D3C solution excludes a universal square-root-log endpoint based on frozen scalar payment; augmented observables and the arbitrary-flow endpoint remain open.",
  "The free passive amplitude in the same exact 2D3C solution lets quadratic observables escape frozen scalar payment; augmented observables, a matching dissipation lower bound, and the arbitrary-flow endpoint remain open.",
  "The new milestone separates R0.73Y–R0.74O into four phases: the production-only obstruction, local coordinates and complete payment, all-shell square-root-log matching, and the free-amplitude no-go for the scalar endpoint.",
  "Research note R0.74O · 2026-09-02",
  "Read the complete R0.61–R0.74O cumulative review →",
  "Read the latest R0.74O research note →",
  "Expand 127 public notes",
  "The free passive amplitude leaves the leading frozen scalar-payment scale unchanged while making the endpoint quantity and positive collar flux grow quadratically; the augmented arbitrary-flow endpoint remains open.",
  "Review v1.81 · 2026-09-02",
  "Latest major-milestone recap (R0.61–R0.74O, 157 sections)",
  "The cumulative review after the R0.60 recap contains 157 nodes; the site now has 217 public research notes",
  "R0.70A–R0.74O · 119 sections published",
  "R0.70A–R0.74O: 119 sections published, 95 fully sealed",
  "R0.74O excludes the universal square-root-log endpoint that depends only on frozen scalar payment. The next step is an independent structural observable that detects quadratic passive amplitude and passes stably to weak limits; arbitrary-flow regularity and Clay remain open.",
  "R0.74O: Free amplitude excludes the scalar square-root-log endpoint",
  "R0.74O｜Free amplitude excludes the scalar square-root-log endpoint",
  "R0.74P next interface",
  "Open interface · R0.74P",
  "Fourteen primary sources confirm precedents for arbitrary passive-component amplitude in 2D3C flows and distinguish local energy, pressure, flux, skewed cylinders, and Carleson control. A finite non-hit proves neither novelty, priority, search completeness, nor publishability.",
  "Allowing the passive-component amplitude to vary within the same exact 2D3C solution leaves the complete scalar payment at the background-shear scale while the endpoint quantity and positive collar flux grow quadratically; this excludes both the universal square-root-log endpoint and the stronger realized scalar sub-frontier.",
  "Literature review v1.81 · 2026-09-02",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.74O only as research notes. I do not extrapolate computations or notes into regularity theorems.",
  "An independent structural quantity is needed that detects quadratic passive amplitude, is scale-critical and non-circular, and passes to suitable weak limits.",
  "Read the milestone recap",
  "Augmented-observable and weak-stability interface",
  "Free passive amplitude and scalar-endpoint no-go",
  "Latest milestone recap",
  "PROVED, INHERITED, FINITE, LITERATURE BOUNDARY, OPEN, and NOT CLAY are separated. This section excludes the frozen-scalar-payment square-root-log endpoint and the realized scalar sub-frontier; the optimal replacement, augmented arbitrary-flow endpoint, regularity, and Clay remain open.",
  "R0.74O public boundary",
  "R0.74O literature and claim boundary",
  "217 public research notes, with R0.74O as the latest node.",
  "Research-note master index · v1.81 · 2026-09-02",
  "Free amplitude excludes the scalar square-root-log endpoint",
  "Latest node R0.74O · continuously revised",
  "01 / Exact amplitude freedom",
  "02 / Complete payment",
  "03 / Quadratic observables",
  "04 / Scalar-endpoint no-go",
  "05 / Fixed logarithmic-power quantifiers",
  "72 validation records",
  "Scalar square-root-log endpoint: FALSE",
  "Scalar payment stays fixed while quadratic observables escape the square-root-log endpoint",
  "Scalar payment remains at the background-shear scale",
  String.raw`is not a universal upper bound. I do not claim that one polynomial-amplitude sequence handles every \(\gamma\). This corollary must remain separate from the preceding one-sequence exponential theorem.`,
  String.raw`Define \(\delta_*=86/11907\) and \(q_*=8024/11907\). The same exact sequence satisfies`,
  "Freeze a non-circular, scale-critical, weakly stable augmented observable and first test whether it detects this section's quadratic passive amplitude.",
  "The endpoint quantity and positive collar flux grow quadratically with amplitude",
  String.raw`For every finite \(j\), \(u_j^*=(\mathfrak a_{*,j}F_j,B_j\theta_j,0)\) and \(p_j^*=0\) remain exact, smooth, periodic, mean-zero, unforced solutions. This is the special linear amplitude freedom of the passive component, not a general Navier--Stokes amplitude scaling.`,
  "Independent analytic audit",
  "Analytic conclusions, inherited inputs, finite reconstructions, and literature boundaries remain separate",
  "After recomputing local energy, gauge-fixed pressure, velocity-cubic, harmonic, acceleration, and fifth-payment-shell rows, the M and F frameworks agree:",
  "Cumulative review R0.61–R0.74O",
  "Milestone recap delta",
  "The collar flux is exactly quadratic in passive amplitude. R0.74F's terminal-survival lower bound holds for every passive amplitude, and R0.74N's all-shell upper bound scales exactly as well. Their non-circular combination gives",
  String.raw`Let \(m=\rho-\tfrac32c_\gamma=43/423360>0\), and take`,
  "Every prescribed logarithmic power also fails separately",
  "An augmented observable that detects quadratic passive amplitude and passes stably to suitable weak limits remains OPEN;",
  String.raw`The energy row retains the strict positive reserve \(e_E-2m/3=1171/943200>0\). The counterexample lies in the large-payment regime; the small-payment estimate is unaffected.`,
  "The square-root logarithm is no longer a universal scalar upper bound",
  String.raw`The exact-solution structure for arbitrary passive amplitude, the complete payment ledger, the \(P_*\) scale, exact quadratic collar-flux scaling, non-circular two-sided closure of \(X_*\), the scalar sub-frontier no-go, and the fixed-\(\gamma\) corollary.`,
  "An augmented endpoint theorem for arbitrary smooth flows, payment-to-admissibility, and a prescribed good scale remain OPEN;",
  "Fourteen primary sources confirm precedents for arbitrary passive-component amplitude in 2D3C flows and distinguish local energy, pressure, flux, skewed cylinders, and Carleson control. A finite non-hit proves neither novelty, priority, exhaustiveness, nor publishability.",
  "The free passive amplitude in the same exact 2D3C solution excludes a universal square-root-log endpoint depending only on frozen scalar payment",
  "Figure 72/72: FINITE",
  "I vary only the passive component; the flow geometry is unchanged",
  "The next step must add a genuinely independent structural observable",
  String.raw`Fix any \(\gamma\in\mathbb R\), then choose \(M>\max\{0,\gamma-1/2\}\) and \(\varkappa_\gamma=L^M\). There is an exact smooth solution family, possibly depending on \(\gamma\), for which`,
  "Research note R0.74O · complete English version",
  "Realized no-go frontier: PROVED",
  String.raw`Therefore the universal square-root-log endpoint depending only on frozen scalar payment is FALSE. More generally, no \(\Phi(p)=o\!\left(p^{8024/11907}(1+\log_+p)^{7/6}\right)\) can be a universal scalar majorant. No optimality is claimed for this exponent.`,
  "Augmented arbitrary-flow endpoint: OPEN",
  String.raw`The lower bound for \(X_*\) comes from the endpoint-energy component. The dissipation component alone has only an upper bound; no matching dissipation lower bound is proved.`,
  "The construction is a no-go on globally smooth structured solutions. It produces no singularity and gives no global-regularity conclusion for arbitrary data.",
  "This section still does not solve the three-dimensional Navier--Stokes Millennium Problem. R0.74N obtains a square-root-log matching law at normalized amplitude. Here I keep the same flow geometry and vary only the passive-component amplitude already present in the exact 2D3C solution. The complete scalar payment remains at the background-shear scale while the endpoint quantity and positive collar flux grow quadratically with amplitude. Hence the universal square-root-log endpoint depending only on frozen scalar payment is false, and the stronger realized scalar sub-frontier is also excluded. Endpoints with independent structural observables, arbitrary-flow regularity, and Clay remain open.",
  "Proof, independent audits, dual-implementation certificate, milestone delta, and complete figure package",
  "Certificate 245/245: FINITE",
  "Status · R0.74O",
  "The optimal universal replacement frontier remains OPEN;",
  "Python Fraction and an independent Ruby Rational implementation reconstruct 245/245 checks; the figure package contains 26 files, 24 manifest entries, 15 external bindings, and 25 checksum lines, with 72/72 internal validations. Finite reconstruction does not replace analytic proof.",
  "The exact R0.74F--N 2D3C solution, terminal-lobe lower bound, flux identity, fifth-shell lower bound, and normalized all-shell upper bound.",
  "R0.74O mathematical gate",
  "Independent recap audit",
  "SVG is the primary web figure; PNG is the fallback and 600 dpi archive, and PDF is the vector download. The figure is a deterministic analytic schematic, not DNS, simulation, fitted data, a sampled path, or singularity evidence.",
];

process.chdir(root);
const [source, translationOrderSource, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings("./public"),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const currentByZh = new Map(current.map((entry) => [entry.zh, entry]));
const missingBefore = source.filter((entry) => !currentByZh.has(entry.zh));
const missingInTranslationOrder = translationOrderSource.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missingBefore.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => /^r074o\d+$/.test(row.id));
  assert.equal(rows.length, english.length, "R0.74O translation count drift");
  assert.deepEqual(rows.map((row) => row.en), english, "R0.74O English translation drift");
} else {
  assert.equal(missingBefore.length, english.length, "R0.74O source-string count drift");
  const sourceByZh = new Map(missingBefore.map((entry) => [entry.zh, entry]));
  const additions = missingInTranslationOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = english[index];
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), `protected token drift ${index + 1}: ${entry.zh}`);
    return { id: `r074o${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...current, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({ release: "R0.74O", translationPath: translationRoute, dgxUsed, checked: english.length, applied: !checkOnly }, null, 2)}\n`);
