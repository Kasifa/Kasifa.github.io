#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075astep26";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "The result is uniform in finite family size, coefficients, spectral bandwidth, and temporal conditioning because it does not decompose the field packet by packet. It gives neither a whole-shell upper bound nor a complete-clock upper bound.",
  "Promoting corridor occupation to occupation of the full K superlevel set, or upgrading Omega to Theta.",
  "Test the outer packet one dyadic shell inward.",
  "Promoting two actual-strip upper bounds to a whole-clock upper bound.",
  "From clock compression to the local persistence/payment dichotomy",
  "Extract a persistent lobe or paid branch from a large clock.",
  "Frozen commits, prose hashes, certificate, and figure ledger",
  "The next step must jointly control the endpoint, accumulated, and off-target rows without turning a strip lower bound into a whole-shell upper bound. Complete K, fixed deletion, arbitrary suitable-weak extension, contraction, regularity, and singularity remain OPEN. R0.75B/C/D were neither read nor published.",
  "Even on the finite six-pair table, the whole-annulus occupation estimates remain OPEN; the all-shell upper bound is also OPEN.",
  "Control every clock row for the explicit family.",
  "Order terminal time, deletion set, and shell supremum.",
  "Cancel the target while retaining the remote coordinate.",
  "Can arbitrarily short total-field endpoint focusing evade W-kinetic payment?",
  "Previous major route-correction recap",
  "No fixed-deletion or whole-clock upper theorem.",
  "Repair the deletion/time quantifiers.",
  "A rigorous ledger and compactness statement, not best-N compression.",
  "Retain two coordinates after one deletion while keeping payment cheap.",
  "Handle asynchronous lobes after one deletion.",
  "One proved local dichotomy and one isolated complete-clock gap",
  "Realize multiple coordinates through exact smooth unforced NSE solutions.",
  "Replacing K with H_fix, reversing bounds, and using unproved target-time shifts.",
  "Using an abstract clock example in place of PDE extraction.",
  "Can finite Gaussian, Hermite, or time-offset cells focus only at the endpoint?",
  "Finite same-shear passive packets and inversion partners close exactly; the canonical equal-target family incurs payment.",
  "Read R0.75A Step 26",
  "At Z, critical or ill-conditioned endpoint focusing and the full Y.57 clock remained OPEN; the literature result was only a finite non-hit.",
  "Define a suitable-weak clock without losing anomalous dissipation.",
  "Retain dominance across the complete terminal slab.",
  "This cumulative milestone recap after R0.60 contains 169 nodes and covers 229 public notes. It preserves the bytes of the R0.74S and earlier recaps, adds the eight R0.74T-R0.75A nodes to the existing route, and fixes the latest problem, result, rejected route, boundary, and next step in a five-field P-A ledger.",
  "Only a positive-volume endpoint core in the exact smooth family is covered; there is no complete-clock upper bound, fixed deletion, or suitable-weak extension.",
  "A.63 remote complete-clock extraction must control endpoint, accumulated, and off-target rows without converting a strip lower bound into a whole-shell upper bound.",
  "Absolute o(1), free age, deleted windings, and whole-shell promotion.",
  "Absolute variation and separable coordinatewise maxima.",
  "An all-shell K upper bound, arbitrary-k extension, the torus cap, and omission of accumulated dissipation.",
  "All-winding survival, inversion and cross margins, and exact endpoint geometry yield a remote lower witness.",
  "A backward-growing Fourier mode, treating a horizontal band as the full generator, treating global modal energy as automatic local payment, and insisting that this lemma requires spectral observability.",
  "A constructed-family theorem, not a universal exclusion; a non-hit is not novelty evidence.",
  "Critical and arbitrarily short smooth endpoint focusing are no longer escape branches",
  "Defect-only detection and circular use of the full-dissipation baseline.",
  "The dyadic r at least 2 route, and treating accumulated-viscosity dimensional screening as a theorem.",
  "Endpoint averaging, padded persistence, good-time closure, and conditional lobe extraction hold; an exposed lobe pays cubically.",
  "Exact arithmetic rejects the frozen geometry and identifies a formal changed-geometry exponent window.",
  "Exact closure, time-tame conditional persistence, and a strict subcritical dwell obstruction with a positive exact payment gap.",
  "Exact corridor, slab, and all-winding estimates yield a total-field lobe and Omega(L R cubed) certified residence.",
  "Exact lifted tiling and coarse shear/packet budgets hold; V.46-V.50 are restricted to six central-chart pairs.",
  "In the exact smooth common-shear family, persistence and rapid rise are exhaustive, and the displayed payment lower bound follows with a positive exact gap.",
  "Exact three-packet algebra, four cross margins, and two endpoint lower bounds yield a two-coordinate obstruction.",
  "An explicit-family lower theorem, not a maximal-clock upper theorem.",
  "Functional counterexamples, not NSE counterexamples.",
  "The hybrid, fixed-set simultaneous height, and coordinatewise excursion are ordered; after known payment, fixed hybrid and simultaneous height are target-scale equivalent.",
  "K equals Q plus F and E plus D and is nonnegative; quadratic and flux variations inherit the payment ledger.",
  "Literal vertical or temporal translations, qualitative analyticity used as a quantitative theorem, and unconditioned finite-family claims.",
  "Local coercivity is proved; full-clock extraction is OPEN.",
  "The moving-cutoff identity acts directly on the total field; persistence and rapid rise are exhaustive and both give the W-remote payment lower bound:",
  "Naive additivity and the canonical cheap-payment design.",
  "A necessary window, not a construction; the platform, windings, survival, and H1 occupation must be reproved.",
  "P-A turns the broad clock-compression problem into one proved local dichotomy and one sharply isolated remaining gap. The route completes the local-energy clock, stress-tests finite deletion and exact common-shear multipackets, repairs the time/deletion quantifiers, proves schedule-invariant residence and remote adjacent-inward witnesses, and tests the three-packet and cancellation-cell routes. R0.75A finally closes arbitrarily short endpoint focusing for the W remote kinetic witness: localized mass either persists backward or its rapid change forces the same exterior cubic payment. The next problem is complete-clock extraction, not spectral persistence.",
  "The pure-heat nested cutoff has a clear methodological precedent; the bounded non-hit establishes neither novelty nor priority.",
  "A 169-node cumulative recap from R0.61 through R0.75A, including the five-field P-A ledger, the R0.75A moving-cutoff dichotomy, the complete audit boundary, and the open A.63 interface",
  "R0.61-R0.75A cumulative milestone recap | From clock compression to the local dichotomy",
  "All R0.61-R0.75A nodes",
  "A theta R cubed residence interval forces exact exterior cubic payment; two nonnegative clocks give the N equals 1 floor.",
  "Uniform arbitrary-suitable-weak extraction remains OPEN.",
  "104 sections fully archived",
  "Master index of 229 research notes",
  "Preserve the previous version",
  "The endpoint, accumulated, and off-target rows must be controlled together; a strip lower bound may not be written as a whole-shell upper bound. R0.75B/C/D and later work were neither read nor published.",
  "View the R0.75A card on the home page",
  "Current endpoint R0.75A Step 26 local dichotomy",
  "Cumulative milestone recap R0.61-R0.75A · 2026-09-03",
  "Jump to the R0.75A card on the home page →",
  "Research note R0.75A Step 26 · 2026-09-03 · LOCAL DICHOTOMY",
  "Read the complete R0.61-R0.75A cumulative recap →",
  "Read the latest R0.75A research note →",
  "Expand 139 public notes",
  "Review v2.05 · 2026-09-03",
  "Latest cumulative recap (R0.61-R0.75A, 169 sections)",
  "The exact moving-cutoff identity makes both persistence and rapid rise produce the W-remote payment lower bound, covering critical and arbitrarily shorter smooth endpoint focusing. Complete K, fixed deletion, suitable-weak extension, and regularity remain OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "The exact moving-cutoff identity divides the endpoint core into persistence and rapid-rise branches. Both yield a W-remote exterior payment lower bound and jointly cover critical and arbitrarily shorter smooth focusing. Complete K, fixed deletion, and suitable-weak extension remain OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "P-A compresses the broad clock-compression problem to one proved local dichotomy and one explicit complete-clock extraction gap. A closes arbitrarily short endpoint focusing but does not control the full K.",
  "P-A cumulative recap",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 229 public research notes",
  "R0.70A-R0.75A · 131 sections published",
  "R0.70A-R0.75A: 131 sections published, 104 fully archived",
  "R0.75A Step 26 uses the exact moving-cutoff identity to close critical and arbitrarily short smooth focusing for the positive-volume W-remote endpoint core. Both persistence and rapid rise force Version-M cubic payment. The next gap is A.63 remote complete-clock extraction; complete K, fixed deletion, and suitable-weak extension remain OPEN.",
  "R0.75A: moving-cutoff local dichotomy and complete-clock open boundary",
  "R0.75A｜Local persistence/payment dichotomy: moving cutoff closes arbitrarily short endpoint focusing",
  "Step 26 frozen four-panel figure",
  "The W-remote endpoint/payment dichotomy is proved for the exact smooth common-shear family; A.63, fixed deletion, suitable-weak extension, regularity, and Clay remain OPEN.",
  "The endpoint, accumulated, and off-target rows must all be controlled. R0.75B/C/D and later work were neither read nor published.",
  "Open interface · A.63",
  "Literature review v2.05 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.75A work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Read the P-A recap",
  "PROVED: the exact smooth finite common-shear family, the moving-cutoff identity, the exhaustive persistence or rapid-rise dichotomy, the W-remote endpoint/payment lower bound, critical and arbitrarily short smooth focusing, and horizontal modal energy. FINITE: Python 14/14, Ruby 17/17, and eight mutations rejected by both implementations. OPEN: complete K, fixed deletion, a whole-shell upper bound, arbitrary suitable-weak extension, contraction, regularity, and singularity. The four-panel figure is an analytic schematic of derived values, not a PDE simulation or DNS.",
  "R0.75A Step 26 bounded literature screen and claim boundary",
  "R0.75A Step 26 public boundary",
  "Step 25 proves exact kinetic coercivity and a strict subcritical threshold for a persistent remote tube; endpoint-to-tube persistence is conditional.",
  "Step 26 proves that persistence and rapid rise are exhaustive and force W-remote payment, covering critical and arbitrarily short smooth focusing; complete K remains OPEN.",
  "Wang--Wang--Zhang--Zhang (arXiv:1711.04279, Section 3.2) provide the closest methodological precedent through a pure-heat inner-endpoint or outer-spacetime nested-cutoff estimate. It does not contain residual shear, a moving periodic anisotropic strip, a shell weight, or the Version-M cubic conversion. The bounded seven-primary-source non-hit establishes none of novelty, priority, nonexistence, correctness, or publishability.",
  "229 public research notes; latest node R0.75A.",
  "Local persistence/payment dichotomy: moving cutoff closes arbitrarily short endpoint focusing",
  "Research-note master index · v2.05 · 2026-09-03",
  "Latest node R0.75A · continuously revised",
  "206 / Full text",
  "207 / Full text",
  "208 / Full text",
  "209 / Full text",
  "210 / Full text",
  "211 / Full text",
  "212 / Full text",
  "213 / Full text",
  "214 / Full text",
  "215 / Full text",
  "Preserved previous milestone recap",
  "This site stops at R0.75A Step 26. Later work must jointly control the endpoint, accumulated, and off-target clock rows without turning a strip lower bound into a whole-shell upper bound. Complete K, fixed deletion, arbitrary suitable weak solutions, contraction, regularity, and singularity remain unproved. R0.75B, R0.75C, R0.75D, and other later work were neither read nor published.",
  "From local L2 mass to Version-M cubic payment",
  "The frozen parameters use omega equals Gamma to the one-quarter power. The visible weight from the remote clock to doubled-radius payment is omega to the one-quarter power, equal to Gamma to the one-sixteenth power; Gamma to the one-quarter power cannot be reused. Substituting all R, L, and omega exponents gives the strictly positive reserve",
  "The frozen geometry obeys the displayed drift and cutoff derivative scales. For R at most one, the error is uniformly controlled by the enlarged-strip mass times the displayed R power. The transport sign and R power are locked by two certificate implementations.",
  "After applying the exact moving-cutoff identity to the total field, local mass either persists through a c R cubed backward window or its rapid rise itself forces spacetime mass in the same enlarged strip.",
  "Conclusion first: arbitrarily short endpoint focusing must also pay",
  "The analytic main note and primary audit carry theorem or lemma status. The Python certificate passes 14/14, the independent Ruby verifier passes 17/17, and both fail closed on eight targeted mutations. They check exact rationals, hashes, formula sentinels, exponents, and boundaries, not the continuous PDE proof. The formal figure archive contains 25 files and 2,588,462 bytes; the SVG, PNG, PDF, manifest, validation, and QA objects are published at frozen hashes. The figure is an analytic schematic, not PDE simulation, DNS, a sampled trajectory, or an empirical fit.",
  "Exact common-shear closure and moving coordinates",
  "Exact exponent reserve",
  "The enlarged tube has at most the displayed spacetime volume. Holder converts A.26 into the displayed cubic lower bound. The tube lies in the scale-2R exterior row, where the weight is at least the displayed amount, so",
  "Both branches are exhaustive and yield the W-remote payment lower bound; critical and arbitrarily shorter smooth focusing are covered. Complete K, fixed deletion, suitable-weak extension, and regularity remain OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "Let E star be the total-field L2 energy on the endpoint core and look back on the displayed interval. If E remains at least half of E star, direct integration yields the stated X lower bound. Otherwise an earlier time has energy below half of E star, and integrating A.18 charges the rise to the same M. There is no third branch: persistent, critical, and arbitrarily shorter smooth endpoint focusing are all covered.",
  "Choose a nonnegative cutoff fixed in moving coordinates, equal to one on the endpoint core and supported in the enlarged remote strip. Exact integration by parts gives",
  "Horizontal Fourier modes obey exact energy decay, with forward high-frequency decay and backward amplification written mode by mode. But a horizontal band is not full generator control, and global modal energy is not automatic local-strip payment. Generic observability would introduce constants depending on shrinking geometry, frequency, and conditioning; this lemma needs no silently uniform constant because the moving cutoff acts directly on the total field.",
  "The four panels encode exact moving geometry, two exhaustive branches, the Holder, weight, and endpoint substitution, and the proved/open hierarchy. ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE SIMULATION | NOT DNS | NO NOVELTY CLAIM | NOT CLAY.",
  "The velocity u=(F,b,0), formed from one odd shear b and any finite sum of passive packets and inversion partners, remains an exact smooth periodic mean-zero unforced Navier--Stokes solution with zero pressure. After the horizontal translation along the reference height, the total field solves a linear drift-diffusion equation with residual shear. Because the proof always acts on the total field, it already includes cancellation or addition among packets, correctors, inversion partners, and all periodic windings.",
  "Stopping line and next proposition A.63",
  "Literature boundary: the closest precedent is not novelty evidence",
  "Research note R0.75A · Step 26 · local dichotomy",
  "Substituting the endpoint lower bound gives the frozen main conclusion",
  "In the frozen smooth periodic common-shear family, the positive-volume W-remote endpoint core cannot evade cubic payment by concentrating into an arbitrarily short time. Applying the moving-cutoff identity directly to the total field leaves exactly two exhaustive branches: local energy persists backward over a c R cubed interval, or its rapid rise is paid by mass in the same enlarged moving strip. Both branches yield the same spacetime lower bound. This closes the critical and arbitrarily shorter smooth focusing escape left by R0.74Z, but it does not control the complete clock K.",
  "This is an exact rational exponent ledger, not a numerical fit. The certificate also rejects the reciprocal p, the wrong transport sign, R to the minus-two or minus-four cutoff scales, the wrong omega weight, omission of the critical or shorter branch, and promotion to the full clock.",
  "Evidence levels and frozen verification",
  "Status · R0.75A STEP 26",
  "A.18: moving-cutoff local energy identity",
  "A.26: exhaustive persistence and rapid-rise branches",
  "A.63 remote complete-clock extraction remains OPEN",
  "A.63 remote complete-clock extraction remains OPEN →",
  "Certificate: Python 14/14, Ruby 17/17, three hash seeds byte-identical, and eight targeted mutations rejected by both implementations. Figure archive: 25 files and 2,588,462 bytes; verify-only and final-size, grayscale, and PDF visual QA all PASS. Neither the finite certificate nor the bounded literature non-hit establishes novelty, priority, or a continuous PDE proof.",
  "Correct uses and limits of the Fourier ledger",
  "NEXT / R0.75B not authorized or read",
  "PROVED is confined to the W-remote endpoint persistence/payment dichotomy in the exact smooth finite common-shear family and the associated horizontal modal identities. The complete clock K, accumulated or off-target rows, whole-shell upper bound, fixed deletion, extension to arbitrary suitable weak solutions, scale contraction, regularity, and singularity remain OPEN. The next proposition A.63 is remote complete-clock extraction: it must control endpoint, accumulated, and off-target rows without turning a strip lower bound into a whole-shell upper bound. NO NOVELTY CLAIM. NOT CLAY.",
  "R0.61-R0.75A cumulative recap",
  "Step 26 main text",
  "Step 26 main text, audits, two certificate implementations, formal figure, and cumulative recap",
  "Wang--Wang--Zhang--Zhang, arXiv:1711.04279, Section 3.2 provide the closest methodological precedent through a pure-heat nested-cutoff inner-endpoint or outer-spacetime estimate, with the same leading R to the minus-three scale when T is comparable to R cubed and the annular gap is comparable to R. R0.75A adds residual shear, a moving periodic anisotropic strip, a shell weight, and the Version-M cubic conversion. The bounded seven-primary-source screen found no theorem directly covering the whole chain, but that finite non-hit establishes none of novelty, priority, nonexistence, correctness, or publishability.",
];

assert.equal(summaries.length, 152, "R0.75A Step 26 translation table length drift");

function withProtected(summary, source) {
  const tokens = extractProtectedTokens(source);
  return tokens.length === 0 ? summary : `${summary} ${tokens.join(" ")}`;
}

process.chdir(root);
const [source, order, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  collectSiteStrings("./public"),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);
const baseCurrent = checkOnly ? current : current.filter((row) => !rowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missing = source.filter((entry) => !currentByZh.has(entry.zh));
const missingOrder = order.filter((entry) => !currentByZh.has(entry.zh));

if (checkOnly) {
  assert.equal(missing.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => rowPattern.test(row.id));
  assert.equal(rows.length, summaries.length, "R0.75A Step 26 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75A Step 26 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75A Step 26 source-string count drift");
  const sourceByZh = new Map(missing.map((entry) => [entry.zh, entry]));
  const additions = missingOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = withProtected(summaries[index], entry.zh);
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), `protected token drift ${index + 1}`);
    return { id: `${prefix}${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...baseCurrent, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({
  release: "R0.75A Step 26",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
