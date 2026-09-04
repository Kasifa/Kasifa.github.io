#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075ostep40";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 243 research notes",
  "View the R0.75O card on the home page",
  "For constant shear, the L2 contraction of the vertical heat semigroup gives an arbitrary-vertical-frequency energy row; with a total-frequency cap and K^2T>=1, the two-dimensional packet retains the K^(-2/3) cubic gain. Inserting N's collar row gives the strict threshold kappa>98605/71442, and the frozen kappa=3/2 closes. The bound uses only the packet's own full-T2 atom, not the Version-M collar payment. NO NOVELTY CLAIM. NOT CLAY.",
  "For constant shear, vertical L2 contraction preserves the arbitrary-vertical-frequency energy estimate; for a real total-frequency-capped packet, short-time two-dimensional cubic conversion gives the K^(-2/3) gain. N's collar row and the frozen kappa=3/2 close the normalized coefficient, but only against the packet's own full-T2 atom. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Current endpoint R0.75O Step 40 vertical-diffusion packet gain",
  "The packet's own full-T2 cubic atom must still be localized to the physical buffered collar; nonconstant shear, inter-packet summation, and low horizontal differences must be handled; and the total upper-frequency cap in the cubic conversion must be removed. Later work was not authorized, read, or published.",
  "Jump to the R0.75O card on the home page →",
  "Research note R0.75O Step 40 · 2026-09-04 · VERTICAL-DIFFUSION PACKET GAIN",
  "Read the latest R0.75O research note →",
  "Expand 153 public notes",
  "Review v2.19 · 2026-09-04",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 243 public research notes",
  "R0.70A–R0.75O · 145 sections published",
  "R0.70A–R0.75O: 145 sections published, 104 fully archived",
  "R0.75O Step 40 proves that vertical diffusion does not destroy the K^(-2/3) packet-flux gain under constant shear: the energy row allows arbitrary vertical frequencies, while the cubic-conversion row requires a total-frequency cap. Physical-collar localization, nonconstant shear, inter-packet interactions, and low differences remain open.",
  "R0.75O: packet flux gain under constant-shear vertical diffusion",
  "R0.75O｜Vertical diffusion preserves the packet flux gain under constant shear",
  "Literature review v2.19 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75O work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Coti Zelati--Gallay 2023 give neighboring context for higher-dimensional parallel shear and transverse diffusion; Bedrossian--Coti Zelati 2017 study shear-flow semigroups and enhanced dissipation; and Albritton--Beekie--Novack 2022 describe a hypoelliptic mechanism for nonconstant shear. R0.75O's exact Wiener-row Schur bound, full-T2 short-time cubic conversion, and frozen local normalization are local proofs. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "Physical buffered-collar cubic localization, nonconstant shear, inter-packet summation, low horizontal differences, and removal of the total upper-frequency cap remain open. Later work was not authorized, read, or published.",
  "PROVED: the arbitrary-vertical-frequency energy estimate O.4--O.12; the total-frequency-capped cubic conversion O.13--O.17; the canonical collar insertion O.18--O.20; the strict paid-frequency threshold O.21--O.22; and the frozen kappa=3/2 closure O.23--O.24. SCOPE: constant shear; the energy row needs no upper vertical-frequency cap; the cubic row uses a finite real packet with n^2+j^2<=4K^2 and K^2T>=1; O.24 pays only against the packet's own full-T2 atom. OPEN: physical buffered-collar cubic localization, nonconstant shear, inter-packet summation, low horizontal differences, removal of the total upper-frequency cap, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75O Step 40 bounded primary-source screen and claim boundary",
  "R0.75O Step 40 public boundary",
  "Step 40 uses vertical heat-semigroup contraction and a Schur estimate to prove the arbitrary-vertical-frequency energy row; for a real total-frequency-capped packet, short-time two-dimensional cubic conversion then preserves the K^(-2/3) gain. N's collar row gives the strict kappa threshold, and the frozen kappa=3/2 closes, but only against the packet's own full-T2 atom.",
  "243 public research notes; latest node R0.75O.",
  "Vertical diffusion preserves the packet flux gain under constant shear",
  "Research-note master index · v2.19 · 2026-09-04",
  "Latest node R0.75O · continuously revised",
  ", two-dimensional short-time cubic mass recovers",
  ", the L2 contraction of the vertical heat semigroup preserves the arbitrary-vertical-frequency energy row: remove the diagonal first, then use Schur to obtain the exact",
  ". The bound concerns only the packet's own full-T2 atom, not the smaller Version-M collar payment.",
  "315 / Full text",
  "316 / Full text",
  "317 / Full text",
  "318 / Full text",
  "319 / Full text",
  "320 / Full text",
  "This site stops at R0.75O Step 40. The arbitrary-vertical-frequency energy row is closed for constant shear; with a total-frequency cap, two-dimensional cubic conversion preserves the K^(-2/3) gain and, at the frozen kappa=3/2, pays against the packet's own full-T2 atom. Physical-collar localization, nonconstant shear, inter-packet summation, low horizontal differences, removal of the total upper-frequency cap, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "For constant shear",
  "coefficient. If one additionally imposes a total-frequency cap and",
  "Research note R0.75O · Step 40 · VERTICAL-DIFFUSION PACKET GAIN",
  "Status · R0.75O STEP 40",
  "Certificate: Python 19/19, Ruby 20/20, O.1--O.24 and 24/24 displays, byte stability across three Python hash seeds, and complete regeneration stability; both implementations reject all 132/132 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "flux gain; after inserting N's collar row, the strict threshold is",
  "Step 40 main text",
  "Step 40 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 47, "R0.75O Step 40 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75O Step 40 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75O Step 40 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75O Step 40 source-string count drift");
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
  release: "R0.75O Step 40",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
