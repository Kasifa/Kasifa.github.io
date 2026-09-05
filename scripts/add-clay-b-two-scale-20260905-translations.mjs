#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "claybtwoscale20260905";

// Local, direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "provides the classical background for smooth coarse-graining and the SGS energy budget. General filters at the two scales do not automatically form a nested Germano hierarchy, and the difference-field production in this note is not the standard SGS flux.",
  "provides the classical background for the composite-filter stress identity;",
  "Literature review v2.43 · 2026-09-05",
  "Filtering literature and claim boundary for the Clay-B two-scale difference energy",
  "Public boundary for ClayB-TwoScale-20260905",
  "PROVED LOCALLY: the complete moving-cutoff difference-energy identity; a globally smooth true NS family rules out unpriced instantaneous absorption with a constant independent of the solution, time, and admissible scale; and the fixed-positive-scale weak endpoint and fully paid estimate E.5. FINITE COMPUTATION: Fraction-based Fourier mode convolution recomputes only the initial-slice coefficients. LITERATURE: classical filtered stress and coarse-grained flux budgets. OPEN: inverse-square scale payment, initial-data dependence, complete-time cancellation, scale smallness and summability, cross-scale contraction, the prescribed-centre contract G, regularity, and singularity. There is no simulation or scientific figure, and no novelty or priority claim. NOT CLAY.",
  "01 / Result map",
  "07 / Strict boundary",
  "08 / Literature boundary",
  "09 / Frozen evidence",
  "Seven new scientific assets and two upstream dependencies are bound to the source commits and SHA-256 values; the handoff and manifest are separately bound to the freeze commit. Hashes establish byte identity, not mathematical correctness.",
  "Saved result",
  "Identifier: ClayB-TwoScale-20260905",
  "Residual drift and stretching",
  "Difference-energy identity: proved",
  "The initial squared L2, gradient-L2, and H1 norms are 3A2/2, 2A2, and 7A2/2. Changing A changes the initial norm, so this is not a singularity arising in one solution.",
  "The first component is the decaying cosine shear, while the third solves a two-dimensional linear advection-diffusion equation with smooth shear and zero pressure. This is a globally smooth invariant class of the original unforced NS system, not a linear approximation. The differentiated energy estimate is",
  "Frozen manifest",
  "Independent analytic audit",
  "The independent analytic audit read D.1--D.24 and E.1--E.10 item by item and found no mathematical issue requiring correction. The exact Fraction program recomputes energy coefficients (1,1/2), dissipation coefficients (1,1), and production coefficients (-1/4,1/4), and passes sign-reversal and mode-deletion sensitivity checks.",
  "For a Leray--Hopf solution and any fixed positive smoothing scale, the periodically mollified equation can be written as",
  "For every fixed smooth h, the inverse-square rescaling of the filter difference converges in Sobolev space to a constant multiple of minus the Laplacian. For smooth u(t), this scales both the production and quadratic terms like R4 and keeps the ratio continuous near t=0.",
  "For any A>0, take the mean-zero initial data",
  "Return to the research-note index",
  "Simulation: not run",
  "The negative result concerns only instantaneous estimates with no extra payment and with constants independent of the solution and time. It does not rule out inverse-square scale payment, constants depending on the initial data, cancellation over the complete time interval, or a different bridge using genuinely three-dimensional vorticity structure.",
  "gives the composite-filter stress identity for filters that preserve constants and commute with derivatives. The general compactly supported kernels used here need not form a nested pair, and the squared difference field cannot be identified directly with Leonard stress.",
  "gives the classical coarse-grained SGS energy budget. The standard flux is not the same object as the two-term difference-field production in D.7, so the sign of one term cannot be interpreted as a complete net backscatter.",
  "Given C, first choose A so that 3A/32>C, then choose a fixed positive time that preserves the limiting inequality, and finally choose R small enough to satisfy both the spatial and time-scale restrictions. Hence there is no finite C independent of the solution, time, and admissible scale such that every smooth true NS solution obeys",
  "Fix the terminal time and an admissible positive R. Let J be the long parabolic interval and J1 its terminal subinterval, and define the radius-cR moving tubes along the same coarse-scale path. Write",
  "Weak-solution time endpoints at fixed positive smoothing scale",
  "Contract G: OPEN",
  "Classical filtering background and the distinction from the present object",
  "Exact Fourier program",
  "Recomputable sources, audit, and byte binding",
  "Portable ledger",
  "Source summary",
  "Let f be the radial Fourier multiplier of the kernel, with d1 and d2 its differences at the two relevant wave-number lengths. Trigonometric orthogonality gives",
  "Let S be periodic convolution with the fixed even radial smoothing kernel, and define the filtered velocities and stresses. At scales r=theta R and R, define the velocity, stress, and pressure differences. Subtracting the two exact filtered equations gives",
  "Positive semidefiniteness of the filtered stress covariance cannot be promoted to automatic dissipation of the two-scale difference energy. For every finite C, one can choose the family amplitude, then a fixed positive time, and finally an admissible scale so that instantaneous production exceeds C times dissipation plus energy. This quantifier order avoids treating an initial slice or an inadmissible scale as a counterexample.",
  "The volume energy of g is not identified with the original local energy, a path difference, or a path trace.",
  "The finite Fourier regression is not presented as a simulation, DNS, or a certificate for the continuous PDE statements.",
  "No cross-scale contraction, packing theorem, prescribed-centre good-scale contract G, regularity theorem, or exclusion of singularities is proved.",
  "There is no scientific figure; analytic inequalities do not justify manufacturing a display curve.",
  "The result does not rule out a genuine cutoff payment proportional to the inverse-square scale times the squared difference, an initial-data-dependent constant, or cancellation over the complete time interval.",
  "No smallness or summability of the local cubic and pressure quantities at the candidate centre is proved.",
  "The smoothing kernel and Leray projection bound the time derivative of the filtered velocity in each fixed spatial regularity class. Compactness of the fixed-scale smoothing map sends the weakly continuous representative of u to a strongly continuous representative of the filtered velocity. Thus the fixed-scale paths and difference field have well-defined closed-interval endpoints, and D.5 can be integrated between any two such endpoints.",
  "Choose a time cutoff that starts at the left endpoint of J and equals one on J1, together with a moving spatial cutoff supported in the radius-2R ball and equal to one in the radius-R ball. The complete estimate is",
  "A globally smooth true NS test family and its exact coefficients",
  "Time cutoff and spatial Laplacian",
  "The two-scale difference-energy identity for one original equation",
  "Uniform instantaneous absorption: ruled out",
  "Pressure boundary work",
  "Pressure is identically zero for this family, so the failure cannot be blamed on an omitted pressure boundary term. The conclusion also cannot be enlarged into a blowup solution, necessary bad scales, or impossibility of contract G.",
  "Take the moving cutoff along the coarse-scale path and integrate by parts term by term to obtain",
  "One proposed route is ruled out; one fully paid estimate survives",
  "The moving tube has parabolic volume of order R5, so one also has",
  "The complete paid estimate in a moving tube",
  "Stretching, stress difference, pressure boundary work, residual drift, spatial cutoff, and time cutoff all remain in the ledger. Setting the cutoff to one removes the pressure and cutoff terms, and self-adjointness of the even kernel gives the equivalent global expression",
  "The two stress-difference terms",
  "The small-scale expansion of the multiplier gives the first difference at order R2 and the second at twice that leading value, hence",
  "On the three-dimensional torus with viscosity normalized to one and no forcing, I subtract two filtered scales of the same true Navier--Stokes solution while retaining the moving cutoff, time cutoff, stress difference, and pressure work. A globally smooth test family rules out unpriced instantaneous absorption with a constant independent of the solution, time, and admissible scale; at fixed positive scale, a closed-endpoint estimate is paid by local quadratic, cubic, and pressure three-halves quantities.",
  "Ledger term",
  "This independent note does not occupy an R0-series identifier, is not a regularity proof, and makes no novelty or priority claim. The prescribed-centre contract G remains OPEN. NOT CLAY.",
  "This is not the energy equality for the original weak solution and does not remove its local energy defect. It pairs only the smoothed fields at fixed positive scale and cannot send R to zero without uniform bounds.",
  "What this section does not prove",
  "Here g is a spatial filter difference, not the difference between two paths; its volume energy does not automatically yield a trace estimate along a path.",
  "These constants come from analytic trigonometric orthogonality. The exact Fraction Fourier program independently recomputes them from mode convolution and serves only as a finite initial-slice regression check.",
  "These literature facts do not supply a good-scale theorem at the prescribed candidate centre. The local work is limited to a term-by-term derivation and audit of the candidate estimate; the search was not a novelty review and does not support a novelty or priority claim.",
  "The positive result is a local estimate at fixed scales with a fixed ratio. After retaining the complete cutoff and pressure ledger, the local energy and dissipation of the two-scale difference are paid by the quadratic, cubic, and pressure three-halves quantities in the same moving tube. Finiteness of the right-hand side is not smallness and gives no scale summability.",
  "Positive time and admissible scales: uniform instantaneous absorption fails",
  "Formal scientific figure: not applicable",
  "The proof applies local Young and Holder inequalities and a pointwise bound for the path velocity term by term. Residual drift, stretching, stress-gradient, stress-cutoff, pressure-boundary, time-cutoff, and spatial-Laplacian terms all have explicit payments; no favorable sign is assigned to pressure or stress.",
  "Per-time upper bound",
  "Independent Clay-B bridge note · 2026-09-05",
  "D manuscript",
  "E manuscript",
  "E.5 and E.10 are scale-invariant fixed-scale payment forms, but they do not derive smallness of the right-hand side from arbitrary initial data and do not yield a contraction factor below one.",
  "Fourier regression: exact rational arithmetic",
  "G remains OPEN. Global regularity and singularity formation remain OPEN. NOT CLAY.",
  "The independent bridge note does not occupy an R0-series identifier and does not change the current R0.76L endpoint; it separately records one frozen audit of a Clay-B proof route.",
  "Research-note master index · v2.43 · 2026-09-05",
  "View the literature and claim boundary",
  "Contract G: OPEN · NOT CLAY",
  "Two-scale difference energy: limits of instantaneous absorption and the complete payment",
  "Instantaneous uniform absorption: ruled out",
  "Complete payment E.5: proved",
  "Download the synchronized Chinese PDF",
  "A globally smooth true NS family rules out unpriced uniform instantaneous absorption. At fixed positive scale, the complete moving-cutoff ledger gives E.5, paid by local quadratic, cubic, and pressure three-halves quantities. Inverse-square scale payment, initial-data-dependent constants, and complete-time cancellation are not ruled out; contract G remains OPEN. NOT CLAY.",
  "Read the Clay-B two-scale note →",
  "Review v2.43 · 2026-09-05",
  "Independent Clay-B note shortcuts",
  "Clay-B result boundary",
  "The Clay-B two-scale difference-energy note rules out unpriced uniform instantaneous absorption and retains the fixed-scale estimate with complete cutoff, cubic, and pressure payments. Inverse-square scale payment, initial-data dependence, complete-time cancellation, and contract G remain open.",
];

assert.equal(summaries.length, 94, "Clay-B two-scale translation table length drift");

function withProtected(summary, source) {
  const tokens = extractProtectedTokens(source);
  return tokens.length === 0 ? summary : `${summary} ${tokens.join(" ")}`;
}

process.chdir(root);
const [source, current] = await Promise.all([
  collectSiteStrings(publicRoot),
  readFile(translationPath, "utf8").then(JSON.parse),
]);
const rowPattern = new RegExp(`^${prefix}\\d+$`);
const baseCurrent = checkOnly ? current : current.filter((row) => !rowPattern.test(row.id));
const currentByZh = new Map(baseCurrent.map((entry) => [entry.zh, entry]));
const missing = source.filter((entry) => !currentByZh.has(entry.zh));
const missingOrder = missing;

if (checkOnly) {
  assert.equal(missing.length, 0, "site still has untranslated Chinese strings");
  const rows = current.filter((row) => rowPattern.test(row.id));
  assert.equal(rows.length, summaries.length, "Clay-B two-scale translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "Clay-B two-scale English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "Clay-B two-scale source-string count drift");
  const sourceByZh = new Map(missing.map((entry) => [entry.zh, entry]));
  const additions = missingOrder.map((orderedEntry, index) => {
    const entry = sourceByZh.get(orderedEntry.zh);
    assert.ok(entry, `absolute source entry missing ${orderedEntry.zh}`);
    const en = withProtected(summaries[index], entry.zh);
    assert.ok(!containsChinese(en), `Chinese remains in translation ${index + 1}`);
    assert.deepEqual(
      extractProtectedTokens(en),
      extractProtectedTokens(entry.zh),
      `protected token drift ${index + 1}`,
    );
    return { id: `${prefix}${String(index + 1).padStart(3, "0")}`, ...entry, en };
  });
  await writeFile(translationPath, `${JSON.stringify([...baseCurrent, ...additions], null, 2)}\n`);
}

process.stdout.write(`${JSON.stringify({
  release: "ClayB-TwoScale-20260905",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
