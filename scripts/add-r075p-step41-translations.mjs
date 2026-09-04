#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075pstep41";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 244 research notes",
  "View the R0.75P card on the home page",
  "Current endpoint R0.75P Step 41 buffered-collar entrance concentration",
  "For a constant-shear real packet satisfying E_in>=mu E_0, the transported cutoff preserves local energy until tau=c_0 mu K^(-2), while the canonical plateau fibres give a genuine three-dimensional collar cubic lower bound with power mu^(5/2). Combining it with O's signed-flux row yields a mu^(-5/3)K^(-2/3) gain; the strict frozen-scale condition is sigma<8558/178605. The final Version-M inclusion covers only an actual component of the same velocity. NO NOVELTY CLAIM. NOT CLAY.",
  "The low-concentration branch still requires a localized signed heat kernel or a cancellation-preserving near/far decomposition, together with nonconstant shear, inter-packet summation, low horizontal differences, and removal of the total upper-frequency cap. Later work was not authorized, read, or published.",
  "Jump to the R0.75P card on the home page →",
  "Research note R0.75P Step 41 · 2026-09-04 · BUFFERED-COLLAR ENTRANCE CONCENTRATION",
  "Read the latest R0.75P research note →",
  "Under E_in>=mu E_0, the moving cutoff and canonical plateau fibres give a three-dimensional collar cubic lower bound with power mu^(5/2). Combining this with O yields a mu^(-5/3)K^(-2/3) flux gain, with the strict frozen threshold sigma<8558/178605. P.31 covers only a same-velocity actual component; projections and the low-concentration branch remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Expand 154 public notes",
  "Review v2.20 · 2026-09-04",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 244 public research notes",
  "R0.70A–R0.75P · 146 sections published",
  "R0.70A–R0.75P: 146 sections published, 104 fully archived",
  "R0.75P Step 41 localizes the constant-shear packet's global full-T2 payment to a genuine three-dimensional buffered-collar atom under quantified entrance concentration and gives the strict threshold sigma<8558/178605. Low-concentration signed localization, nonconstant shear, inter-packet interactions, and low differences remain open.",
  "R0.75P: buffered-collar payment under entrance concentration",
  "R0.75P | Buffered-collar payment under entrance concentration",
  "Literature review v2.20 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75P work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Apraiz--Escauriaza--Wang--Zhang 2014 and Wang--Wang--Zhang--Zhang 2019 provide neighboring theory on heat observability from measurable or thick sets; Ervedoza--Zuazua 2011 show how observability cost depends on geometry and time; and Coti Zelati--Gallay 2023 provide higher-dimensional parallel-shear context. R0.75P imports none of these theorems and instead proves the transported-cutoff identity, local persistence, exact radial fibre bound, and mu^(5/2) cubic lower bound directly. A finite non-hit establishes no literature completeness, novelty, priority, nonexistence, correctness, or publishability conclusion.",
  "The localized signed heat kernel or cancellation-preserving near/far estimate, nonconstant shear, inter-packet summation, low horizontal differences, and removal of the total upper-frequency cap remain open. Later work was not authorized, read, or published.",
  "PROVED: canonical plateau fibres P.7--P.10; moving-cutoff local energy and persistence P.14--P.20; the physical-collar cubic lower bound P.21--P.24; the conditional signed-flux estimate P.25--P.28; the exact entrance threshold P.29--P.30; and the conditional Version-M payment P.31 under the stated alignment. SCOPE: constant shear, one real total-frequency-capped packet, and E_in>=mu E_0; sigma<8558/178605 is a strict sufficient condition; P.31 additionally requires a same-velocity actual-component realization, explicitly excluding Fourier/LP projections; P.3--P.30 do not use that realization. OPEN: low entrance concentration, a localized signed heat kernel or cancellation-preserving near/far estimate, nonconstant shear, inter-packet summation, low horizontal differences, removal of the total upper-frequency cap, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity. There is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75P Step 41 bounded primary-source screen and claim boundary",
  "R0.75P Step 41 public boundary",
  "Under E_in>=mu E_0, Step 41 uses transported-cutoff local-energy persistence and the exact radial plateau fibre to obtain a mu^(5/2) collar cubic lower bound. Combining it with O's signed-flux row yields a mu^(-5/3)K^(-2/3) gain and the strict threshold sigma<8558/178605. The final Version-M inclusion covers only a same-velocity actual component.",
  "244 public research notes; latest node R0.75P.",
  "Buffered-collar payment under entrance concentration",
  "Research-note master index · v2.20 · 2026-09-04",
  "Latest node R0.75P · continuously revised",
  ", local energy persists until",
  "; equality is excluded. The final Version-M inclusion holds only for an actual component of the same velocity; Fourier/LP projections are outside the conclusion. The low-entrance-concentration branch remains",
  "321 / Full text",
  "322 / Full text",
  "323 / Full text",
  "324 / Full text",
  "325 / Full text",
  "326 / Full text",
  "327 / Full text",
  "This site stops at R0.75P Step 41. Under the strict entrance-concentration threshold, the moving cutoff, plateau fibres, and local-energy persistence pay one constant-shear packet into a genuine three-dimensional buffered collar; the final Version-M inclusion holds only for an actual component of the same velocity. The low-concentration branch, a localized signed heat kernel or cancellation-preserving near/far estimate, nonconstant shear, inter-packet summation, low horizontal differences, removal of the total upper-frequency cap, E.24, the complete clock, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "with at least one half retained. The exact canonical plateau fibre length then gives a genuine three-dimensional collar cubic atom and pays O's signed flux with",
  "If a constant-shear real packet satisfies the entrance condition",
  "Research note R0.75P · Step 41 · BUFFERED-COLLAR ENTRANCE CONCENTRATION",
  "payment. At frozen scales, the strict condition is",
  "Status · R0.75P STEP 41",
  "Certificate: Python 21/21, Ruby 22/22, P.1--P.31 and 31/31 displays, byte stability across three Python hash seeds, and complete regeneration stability; both implementations reject all 132/132 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. This section contains no formal figure, simulation, numerical fit, DNS, or DGX.",
  "Step 41 main text",
  "Step 41 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 47, "R0.75P Step 41 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75P Step 41 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75P Step 41 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75P Step 41 source-string count drift");
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
  release: "R0.75P Step 41",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
