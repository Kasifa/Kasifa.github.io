#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075cstep28";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 231 research notes",
  "Prove a passive-gradient block estimate or construct an exact forward passive family with complete accounting. R0.75D/E/F/G and later work were neither read nor published.",
  "View the R0.75C card on the home page",
  "Current endpoint R0.75C Step 28 packing false positive",
  "Jump to the R0.75C card on the home page →",
  "Research note R0.75C Step 28 · 2026-09-03 · PACKING FALSE POSITIVE",
  "Read the latest R0.75C research note →",
  "Expand 141 public notes",
  "Review v2.07 · 2026-09-03",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 231 public research notes",
  "R0.70A-R0.75C · 133 sections published",
  "R0.70A-R0.75C: 133 sections published, 104 fully archived",
  "R0.75C Step 28 proves that total-velocity cubic packing can be triggered as a false positive by a low-frequency, already-paid background shear, so B.44 cannot be a universal necessary condition. B.45 is neither proved nor disproved; only frequency-sensitive passive dissipation remains open.",
  "R0.75C: background-shear packing false positive and passive-dissipation gate",
  "R0.75C｜Background-shear packing false positive: B.44 universality eliminated, passive dissipation unresolved",
  "The saturation shear makes total-cubic effective count violate the B.44 threshold, while shear dissipation remains little-o of the two-thirds cubic payment. Thus universal B.44 is disproved, whereas B.45 and the passive row remain OPEN. This is not an NSE counterexample. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "The saturation shear makes the effective shear count grow like inverse R and violate the B.44 threshold, yet directly pays the true shear dissipation. Universal B.44 is disproved; B.45 is not disproved and the passive row remains OPEN. This is not an NSE counterexample. NO NOVELTY CLAIM. NOT CLAY.",
  "The frozen whitelist adds no literature-collision artifact; the handoff authorizes only a bounded finite non-hit statement, so it supports no conclusion about literature completeness, novelty, priority, nonexistence, correctness, or publishability.",
  "Prove a passive-gradient block estimate or construct an exact forward passive family with complete accounting; later material was neither read nor published.",
  "Open interface · R0.75D",
  "Literature review v2.07 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.75C work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "PROVED: on the frozen exact smooth saturation-shear family, the effective shear count grows like inverse R and the exact threshold gap is positive, disproving the universal B.44 proposal; the same shear's outer dissipation is nevertheless paid by a coefficient tending to zero. FINITE: Python 8/8, Ruby 9/9, and 18/18 plus 19/19 mutation rejection. OPEN: B.45, passive dissipation, full K, fixed deletion, arbitrary suitable-weak extension, regularity, and singularity. This is only a counterexample to an auxiliary packing condition, not a Navier--Stokes counterexample. A formal figure is NOT APPLICABLE; there is no simulation, DNS, or DGX.",
  "R0.75C Step 28 bounded evidence and claim boundary",
  "R0.75C Step 28 public boundary",
  "Step 28 proves that total-cubic packing has a false positive for persistent low-frequency background shear; universal B.44 is disproved, but shear dissipation is paid and B.45 plus the passive row remain OPEN.",
  "231 public research notes; latest node R0.75C.",
  "Background-shear packing false positive: B.44 universality eliminated, passive dissipation unresolved",
  "Research-note master index · v2.07 · 2026-09-03",
  "Latest node R0.75C · continuously revised",
  "226 / Full text",
  "227 / Full text",
  "228 / Full text",
  "229 / Full text",
  "230 / Full text",
  "231 / Full text",
  "The counted background-shear dissipation is still paid",
  "The frozen whitelist adds no literature-collision artifact; the handoff allows only a bounded finite non-hit statement. It is not a judgment of novelty, priority, nonexistence, correctness, or publishability. Formal figure: NOT APPLICABLE; this section is purely analytic and has no simulation, DNS, or DGX.",
  "This site stops at R0.75C Step 28. The next proposition must prove a frequency-sensitive passive block estimate or construct an exact forward passive family with complete accounting; neither is complete. An auxiliary B.44 false positive may not be described as a Navier--Stokes counterexample, B.45 may not be described as disproved, and shear-row payment may not be described as passive-row closure. Full K, fixed deletion, arbitrary suitable-weak extension, regularity, and singularity remain unproved. R0.75D/E/F/G and other later work were neither read nor published.",
  "An auxiliary B.44 false positive may not be described as a Navier--Stokes counterexample, B.45 may not be described as disproved, and shear-row payment may not be described as passive-row closure. R0.75D/E/F/G and other later work were neither read nor published.",
  "The frozen saturation shear saturates total-velocity cubic packing across an inverse-R number of blocks, yet the true shear dissipation is paid by a BV heat estimate.",
  "Frozen evidence and claim boundary",
  "For the shear-only field, a fixed positive cap obeys the displayed lower bound throughout the doubled-radius interval. Every enlarged short-block payment satisfies",
  "For a general exact common-shear field, the outer dissipation splits exactly as",
  "Combining this with the scale-two-R exterior velocity-payment lower bound gives",
  "Conclusion first: total-cubic packing is a background-shear false positive",
  "Each fixed vertical slice of the spherical outer collar has area at most the displayed scale. The one-dimensional BV norm of the frozen saturation datum is uniformly bounded; the periodic heat kernel and Young's inequality give",
  "A replacement observable must see the passive gradient or its frequency scale, rather than depend only on total cubic-velocity block masses. The direct outer-dissipation estimate B.45 remains NEITHER PROVED NOR DISPROVED in this section.",
  "The exact excess above the sufficient B.44 threshold is",
  "Research note R0.75C · Step 28 · PACKING FALSE POSITIVE",
  "In the frozen exact smooth periodic saturation-shear family, total-velocity cubic block masses in the outer collar are comparable across all inverse-R short blocks, so the effective shear count grows like inverse R. This strictly disproves the claim that the B.44 threshold must hold universally, but does not invalidate B.44 as a sufficient condition.",
  "This is not a Navier--Stokes counterexample; it is only an exact-family counterexample to an auxiliary universal packing condition. Complete K, fixed deletion, arbitrary suitable-weak extension, and regularity remain OPEN. NOT CLAY.",
  "The conclusion persists after adding any passive component because the total cubic velocity dominates the shear cubic velocity. A large effective count records only temporal persistence of the low-frequency background, not its gradient cost.",
  "Status · R0.75C STEP 28",
  "Certificate: Python 8/8, Ruby 9/9, 36 unique tags, byte-identical output across three hash seeds, and 18/18 plus 19/19 mutations rejected. The certificate covers only finite exact arithmetic, source binding, and structural sentinels. The frozen whitelist adds no literature-collision artifact; a bounded finite non-hit establishes neither novelty nor priority. This section is purely analytic and contains no formal figure, simulation, DNS, or DGX.",
  "Comparable blocks and the exact threshold gap",
  "Corrected gate: only passive dissipation remains",
  "Frequency-sensitive passive-dissipation gate remains OPEN",
  "Frequency-sensitive passive-dissipation gate remains OPEN →",
  "NEXT / R0.75D not authorized or read",
  "The primary analytic audit passes with zero mathematical blockers and zero release blockers. The Python certificate is 8/8 and the independent Ruby verifier is 9/9; all 18/18 and 19/19 targeted mutations are rejected, three hash seeds are byte-identical, and all 36 equation tags and references resolve. They verify finite exact arithmetic, source binding, and structure, not the continuous PDE proof.",
  "R0.75C stops at the corrected passive row. The next step can only prove a frequency-sensitive passive block estimate or construct an exact forward passive family with complete accounting; neither is complete.",
  "The shear row is paid, so the smallest open proposition is",
  "Step 28 main text",
  "Step 28 main text, primary audit, two certificate implementations, and QA",
  "Universal B.44: DISPROVED; B.45: NEITHER PROVED NOR DISPROVED; passive dissipation: OPEN. This is not a Navier--Stokes counterexample. NO NOVELTY CLAIM. NOT CLAY.",
];

assert.equal(summaries.length, 66, "R0.75C Step 28 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75C Step 28 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75C Step 28 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75C Step 28 source-string count drift");
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
  release: "R0.75C Step 28",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
