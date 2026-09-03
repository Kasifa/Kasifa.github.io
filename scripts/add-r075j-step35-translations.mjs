#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075jstep35";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 238 research notes",
  "A majorant satisfying a<=L*Phi, Phi>=0, and Phi(t2)>=0 must be constructed, and its initial occupation/source row plus transition and periodic geometry must be paid independently by frozen Version-M atoms. Later work was not authorized, read, or published.",
  "View the R0.75J card on the home page",
  "Current endpoint R0.75J Step 35 mean-zero adjoint obstruction",
  "Jump to the R0.75J card on the home page →",
  "Research note R0.75J Step 35 · 2026-09-03 · MEAN-ZERO ADJOINT OBSTRUCTION",
  "Read the latest R0.75J research note →",
  "Expand 148 public notes",
  "Review v2.14 · 2026-09-03",
  "The exact signed-source adjoint is forced to change sign by slice-wise zero mean; exact duality recovers the unfavorable weighted dissipation, while a constant shift either cancels or creates a CD surcharge. The positive-majorant route remains viable, but its initial row is unpaid. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 238 public research notes",
  "R0.70A–R0.75J · 140 sections published",
  "R0.70A–R0.75J: 140 sections published, 104 fully archived",
  "R0.75J Step 35 proves that the exact zero-terminal adjoint of the physical signed collar source is forced to change sign by slice-wise zero mean. A constant positive shift cancels in the exact identity and costs CD if dissipation is dropped. The remaining valid route is a nonnegative majorant with a paid initial row.",
  "R0.75J: mean-zero signed adjoint obstruction and paid-majorant gate",
  "R0.75J｜Mean-zero adjoint obstruction for the signed collar flux",
  "The signed derivative source has zero mean on every fixed parameter slice, forcing any nonzero exact zero-terminal adjoint to change sign. Its negative part creates unfavorable positive dissipation in an upper bound. A constant positivity shift cancels exactly and costs CD after dropping dissipation. A nonnegative majorant is viable, but its initial occupation/source row is unpaid. NO NOVELTY CLAIM. NOT CLAY.",
  "A nonnegative majorant satisfying a<=L*Phi must be constructed and paid, especially its initial occupation/source row under frozen Version-M atoms and its transition and periodic geometry. Later work was not authorized, read, or published.",
  "Literature review v2.14 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75J work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Albritton--Dong identify the special bounded-total-speed boundary for passive scalars; Gardner--Liss--Mattingly show that pathwise shear-diffusion representations can carry information beyond formal energy identities; and Hu--Li's Davies weighted-semigroup method supports off-diagonal heat-kernel reasoning. None of the inspected sources gives the Version-M positive-majorant initial-row payment required by J.20 or proves E.24. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "PROVED: slice-wise zero mean of the physical source J.7; zero mean and forced sign change of the exact zero-terminal adjoint J.8--J.9; duality and unfavorable dissipation J.12--J.13; constant-shift cancellation and the CD surcharge J.14--J.18; and the sufficient positive-majorant architecture J.19--J.20. NOT A BLANKET NO-GO: a nonnegative majorant remains viable, but its initial occupation/source row is not paid by frozen Version-M atoms; replacing a by a_+ changes the signed source. OPEN: a paid positive majorant, transition bands, periodic recrossing, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75J Step 35 bounded primary-source screen and claim boundary",
  "R0.75J Step 35 public boundary",
  "Step 35 proves that the exact zero-terminal adjoint of the physical derivative source must change sign when nontrivial; the dual identity turns the negative weight into unfavorable positive dissipation, the constant shift cancels in the full identity, and dropping that row costs CD.",
  "238 public research notes; latest node R0.75J.",
  "Research-note master index · v2.14 · 2026-09-03",
  "Mean-zero adjoint obstruction for the signed collar flux",
  "Latest node R0.75J · continuously revised",
  "279 / Full text",
  "280 / Full text",
  "281 / Full text",
  "282 / Full text",
  "283 / Full text",
  "284 / Full text",
  "285 / Full text",
  "This site stops at R0.75J Step 35. The exact signed-source adjoint is forced to change sign by zero mean; a constant positive shift adds no exact information, and dropping dissipation creates a CD surcharge. A nonnegative majorant and its initial occupation/source row still require an independent payment, together with transition geometry, periodic recrossing, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. Later work was not authorized, read, or published.",
  "A paid positive majorant remains OPEN",
  "Physical signed source",
  "Research note R0.75J · Step 35 · MEAN-ZERO ADJOINT OBSTRUCTION",
  "has zero mean on every fixed parameter slice, so its exact zero-terminal adjoint must change sign when nonzero. Exact duality turns the negative weight into unfavorable positive weighted dissipation; a constant shift cancels exactly in the full identity, while dropping favorable dissipation pays the global surcharge",
  "Status · R0.75J STEP 35",
  "Certificate: Python 19/19, Ruby 24/24, J.1--J.20 and 20/20 displays, byte stability across three Python hash seeds, and complete regeneration stability; both implementations reject all 84/84 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 35 main text",
  "Step 35 main text, primary-source boundary, two certificate implementations, and fail-closed QA"
];

assert.equal(summaries.length, 45, "R0.75J Step 35 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75J Step 35 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75J Step 35 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75J Step 35 source-string count drift");
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
  release: "R0.75J Step 35",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
