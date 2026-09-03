#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075estep30";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 233 research notes",
  "Control the positive signed cross-mode flux, or establish difference-frequency decay or localized observability. R0.75F/G/H and later work were neither read nor published.",
  "View the R0.75E card on the home page",
  "Current endpoint R0.75E Step 30 horizontal cross-mode flux",
  "Jump to the R0.75E card on the home page →",
  "Research note R0.75E Step 30 · 2026-09-03 · HORIZONTAL CROSS-MODE FLUX",
  "Read the latest R0.75E research note →",
  "Expand 143 public notes",
  "Review v2.09 · 2026-09-03",
  "The exact difference-frequency identity eliminates every diagonal transport term and pays the real horizontal zero mode for all payment. The complex singleton is only an algebraic diagnostic; the general real cross-mode gate remains OPEN. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "The exact signed convolution proves that diagonal flux is zero and closes the real horizontal zero mode at the P^(2/3) scale for all payment. A nonzero complex singleton is only a diagnostic; general real ±n pairs and the cross-mode gate remain OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 233 public research notes",
  "R0.70A-R0.75E · 135 sections published",
  "R0.70A-R0.75E: 135 sections published, 104 fully archived",
  "R0.75E Step 30 proves that the localized shear-transport flux is a purely off-diagonal difference-frequency quantity and closes the admissible real horizontal zero mode for all payment. Signed cross-mode aggregation for arbitrary real fields, the complete clock, and suitable-weak transfer remain unresolved.",
  "R0.75E: horizontal difference-frequency identity and all-payment real zero-mode closure",
  "R0.75E｜Horizontal cross-mode flux: real zero mode paid for all payment, arbitrary-real aggregation unresolved",
  "Control the positive signed cross-mode flux, or establish difference-frequency decay or localized observability; later material was neither read nor published.",
  "Open interface · R0.75F",
  "Literature review v2.09 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.75E work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "PROVED: the local energy identity with its endpoint and correct sign, horizontal support invariance, the exact difference-frequency formula, diagonal cancellation, zero-flux spectral-sector closure, and the all-payment P^(2/3) estimate for the real horizontal zero mode. FINITE: the real +/-1 witness has T_xi/pi = -1/2; Python 13/13, Ruby 16/16, and 39/39 mutation rejection by both. DIAGNOSTIC ONLY: a nonzero complex singleton, which is not a physical real Navier--Stokes velocity. OPEN: the arbitrary-real signed cross-mode bound, real +/-n aggregation, cutoff Fourier tails, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, DNS, or DGX.",
  "R0.75E Step 30 bounded primary-source screen and claim boundary",
  "R0.75E Step 30 public boundary",
  "Siming He supports preservation of streamwise Fourier modes by shear and heat evolution of transverse-only data; Gardner--Liss--Mattingly supports decoupling of the streamline average; Albritton--Dong supports survival of drift flux under physical localization. None directly proves this site's combination of a spherical physical collar, Xi_(m-n) convolution, and Version-M P^(2/3) normalization. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "Step 30 proves that localized transport is a purely off-diagonal difference-frequency flux and pays the admissible real zero mode for all payment; the complex singleton is only an algebraic diagnostic, while the general real cross-mode gate remains OPEN.",
  "233 public research notes; latest node R0.75E.",
  "Horizontal cross-mode flux: real zero mode paid for all payment, arbitrary-real aggregation unresolved",
  "Research-note master index · v2.09 · 2026-09-03",
  "Latest node R0.75E · continuously revised",
  "240 / Full text",
  "241 / Full text",
  "242 / Full text",
  "243 / Full text",
  "244 / Full text",
  "245 / Full text",
  "246 / Full text",
  "247 / Full text",
  "Retain the local cubic atom",
  "This site stops at R0.75E Step 30. The next proposition must control the positive signed cross-mode flux or establish difference-frequency decay or localized observability. The complex singleton may not be treated as a physical real field, and the finite witness may not be treated as a complete trajectory. The complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain unresolved. R0.75F/G/H and other later work were neither read nor published.",
  "Localized energy identity with the endpoint and correct sign",
  "When the transport flux vanishes, the time/Laplacian cutoff rows and spacetime Hölder give",
  "Define the positive signed cross-mode flux at the target normalization",
  "Frozen finite witness",
  "Frozen evidence, literature boundary, and stop line",
  "For the frozen common-shear equation",
  "This witness verifies only the algebraic normalization of the signed convolution; it is neither a complete spacetime trajectory nor a finite model of the geometric collar.",
  "The conclusion imposes no small-payment restriction and permits arbitrarily high vertical frequency. The high-vertical-frequency zero mode from R0.75D blocks only a horizontal-to-full Rayleigh inference, not the target dissipation estimate.",
  "The fixed physical-collar cutoff creates transport flux only through difference-frequency coupling between distinct horizontal modes. Every diagonal term vanishes exactly. Therefore, for every admissible real horizontal zero mode,",
  "Conclusion first: a large background is not a large flux, and the real zero mode is closed for all payment",
  "Exact horizontal difference-frequency identity",
  "Pure two-thirds payment on a zero-flux sector",
  "Let the displayed function be the spatial cutoff and retain the frozen time cutoff. Multiply by the localized conjugate field, integrate, and take the real part to obtain",
  "Exact remaining gate for arbitrary real fields",
  "The next proposition required for arbitrary real fields is",
  "The real horizontal zero mode is closed for all payment; the complex singleton is only an algebraic diagnostic; signed cross-mode aggregation for arbitrary real fields remains OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "In particular, the zero support sector is a genuinely admissible invariant subspace. The squared amplitude is independent of the horizontal coordinate, so periodic integration directly cancels the cutoff derivative. This includes arbitrarily high vertical sine modes.",
  "Both direct Laurent multiplication and the ordered off-diagonal sum give",
  "Reality boundary: a complex singleton is not a physical real field",
  "Research note R0.75E · Step 30 · HORIZONTAL CROSS-MODE FLUX",
  "Using the x1-average of the cutoff coefficient, the transport flux has the exact representation",
  "Because the multiplier vanishes on the diagonal, the flux is a purely off-diagonal difference-frequency quantity. A large background cubic atom alone cannot imply a large localized transport flux.",
  "Because the shear is independent of the horizontal coordinate, every horizontal mode evolves independently:",
  "The mixed coefficient tends to zero exponentially, so sufficiently large L yields the all-payment P^(2/3) bound without the R0.75D interaction hypothesis.",
  "The transport sign on the right is positive; the terminal endpoint is nonnegative and may be discarded only in an upper bound, not silently identified with a payment row.",
  "The exact reduction is",
  "Then every off-diagonal summand vanishes and the transport flux is zero. This is a sufficient spectral-orthogonality condition; it is not claimed for every nontrivial real support with a generic radial collar.",
  "This signed phase-mixing and difference-frequency gate is not proved. General real paired modes, cross-mode aggregation, cutoff Fourier tails, and localized observability all remain OPEN.",
  "Status · R0.75E STEP 30",
  "arbitrary-real signed cross-mode aggregation remains OPEN",
  "arbitrary-real signed cross-mode gate remains OPEN →",
  "The bounded primary-source screen supports only neighboring mechanisms: shear preserves streamwise modes, the streamline average solves one-dimensional diffusion, and physical localization retains drift flux. No searched source supplies the combined spherical-collar convolution and Version-M payment theorem used here; a finite non-hit establishes no completeness, novelty, priority, correctness, or publishability conclusion.",
  "Certificate: Python 13/13, Ruby 16/16, 24 unique tags, 24/24 displays, byte-identical output across three hash seeds, 39/39 mutations rejected by both, and unknown mutations fail closed. The finite Laurent witness verifies only E.10 algebra and normalization; it is neither a full spacetime trajectory nor a finite model of the geometric collar. This section is purely analytic and contains no formal figure, simulation, DNS, or DGX.",
  "The exact Fourier convolution proves that the transport flux contains only off-diagonal difference frequencies.",
  "Horizontal support is preserved by the modal equation. Suppose",
  "NEXT / R0.75F not authorized or read",
  "A nonzero complex singleton also has zero flux, but it is only a complexified scalar diagnostic and cannot be promoted to a physical real Navier--Stokes velocity. A real field obeys the conjugate-pair condition, so a nonzero real harmonic has paired support and its doubled difference frequency can generally couple to the cutoff.",
  "The primary analytic audit passes with zero mathematical blockers and zero release blockers. The Python certificate is 13/13 and the independent Ruby verifier is 16/16; each rejects 39/39 targeted mutations, unknown mutations fail closed, three hash seeds are byte-identical, and E.1--E.24 plus all 24 displays parse completely.",
  "R0.75E stops at the signed cross-mode gate for arbitrary real fields. The complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain unresolved. R0.75F/G/H and other later work were neither read nor published. This section has no formal figure, simulation, DNS, or DGX.",
  "Step 30 main text",
  "Step 30 main text, primary-source boundary, two certificate implementations, and QA",
  "Zero-flux spectral sectors and the real zero mode",
];

assert.equal(summaries.length, 82, "R0.75E Step 30 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75E Step 30 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75E Step 30 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75E Step 30 source-string count drift");
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
  release: "R0.75E Step 30",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
