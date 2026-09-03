#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075bstep27";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "Master index of 230 research notes",
  "Prove an effective temporal-packing threshold or construct an exact smooth counterexample with complete accounting. R0.75C/D/E and later work were neither read nor published.",
  "View the R0.75B card on the home page",
  "Current endpoint R0.75B Step 27 outer padding gate",
  "Previous major milestone recap through A",
  "Previous major cumulative recap from R0.61 through R0.75A, 169 sections",
  "Jump to the R0.75B card on the home page →",
  "Research note R0.75B Step 27 · 2026-09-03 · OUTER PADDING GATE",
  "Read the latest R0.75B research note →",
  "Expand 140 public notes",
  "Review v2.06 · 2026-09-03",
  "The cumulative recap after R0.60 contains 169 nodes; the site now has 230 public research notes",
  "R0.70A-R0.75B · 132 sections published",
  "R0.70A-R0.75B: 132 sections published, 104 fully archived",
  "R0.75B Step 27 uses the time-cutoff Caccioppoli ledger to pay the safe complete subclock, inner padding, and the full endpoint row. Only outer-collar accumulated dissipation remains; its positive coarse full-window coefficient shows failure of the current upper-bound method, not a counterexample. The next gap is effective temporal packing.",
  "R0.75B: safe complete subclock and outer-dissipation packing gate",
  "R0.75B｜Complete-clock outer padding gate: safe subclock paid, outer dissipation unresolved",
  "Cubic payment covers the safe complete subclock, inner padding, and the full endpoint row; outer-collar accumulated dissipation reduces to effective temporal packing. The adverse full-window coefficient is not a counterexample. Full K, fixed deletion, and suitable-weak extension remain OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "The time-cutoff Caccioppoli argument pays the safe complete subclock and the full endpoint row; outer-collar accumulated dissipation reduces to temporal packing. The positive coarse rate is method failure, not a counterexample. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "Prove an effective packing threshold or construct an exact smooth counterexample with complete accounting; later work was neither read nor published.",
  "Open interface · R0.75C",
  "Literature review v2.06 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.75B work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Chang--Kang (arXiv:1806.02516) and Gallay--Slijepcevic (arXiv:1308.1544) confirm that local-energy/Caccioppoli and localized dissipation are established methods; Wang--Wang--Zhang--Zhang (arXiv:1711.04279) provide nearby heat-observability context. A bounded non-hit across three primary sources proves none of novelty, priority, nonexistence, correctness, or publishability.",
  "PROVED: payment of the safe complete subclock, inner padding, and the full endpoint row for the frozen exact smooth inversion-paired common-shear family. FINITE: Python 8/8, Ruby 9/9, and 20/20 plus 21/21 mutation rejection. OPEN: outer-collar accumulated dissipation, effective temporal packing, full K, fixed deletion, arbitrary suitable-weak extension, regularity, and singularity. The adverse full-window coefficient is method failure, not a counterexample. A formal figure is NOT APPLICABLE; there is no simulation, DNS, or DGX.",
  "R0.75B Step 27 bounded literature screen and claim boundary",
  "R0.75B Step 27 public boundary",
  "Step 22 proves the all-winding conditional-bridge threshold; fixed deletion remains OPEN.",
  "Step 26 proves that persistence and rapid rise are exhaustive and force W-remote payment, covering critical and arbitrarily short smooth focusing.",
  "Step 27 pays the safe complete subclock, inner padding, and the full endpoint row; outer accumulated dissipation reduces to temporal packing, and full K remains OPEN.",
  "230 public research notes; latest node R0.75B.",
  "Complete-clock outer padding gate: safe subclock paid, outer dissipation unresolved",
  "Research-note master index · v2.06 · 2026-09-03",
  "Latest node R0.75B · continuously revised",
  "The outer dissipation estimate remains OPEN.",
  "216 / Full text",
  "217 / Full text",
  "218 / Full text",
  "219 / Full text",
  "220 / Full text",
  "221 / Full text",
  "222 / Full text",
  "223 / Full text",
  "224 / Full text",
  "225 / Full text",
  "Split the interval into blocks of volume scale R cubed and define the effective count from each block payment.",
  "This site stops at R0.75B Step 27. The next proposition must prove an effective temporal-packing threshold or construct an exact smooth counterexample with complete accounting; neither is complete. The adverse upper-bound coefficient may not be called a counterexample, and a strip lower bound may not be written as a whole-shell upper bound. Full K, fixed deletion, arbitrary suitable-weak extension, regularity, and singularity remain unproved. R0.75C/D/E and other later work were neither read nor published.",
  "A strip lower bound may not be rewritten as a whole-shell upper bound. Formal figure: NOT APPLICABLE. This section is purely analytic and contains no Navier--Stokes simulation, DNS, DGX, or formal figure. NO NOVELTY CLAIM. NOT CLAY.",
  "The sufficient condition is exactly",
  "The frozen shell cutoff is split into a safe cutoff and an outer-collar cutoff. The safe support retains the stronger doubled-radius weight, while the outer half has only the weaker uniform weight. This index shift determines the sign difference between the safe rate and the outer accumulated rate.",
  "The exact frozen-parameter rate is",
  "Frozen exact family and scales",
  "Apply the same exhaustive dichotomy as in Step 26 on the terminal R-cubed lookback window: outer localized energy either persists or a rapid rise forces spacetime mass in the same collar. The smaller collar volume gives",
  "Integrate by parts exactly with a spatial cutoff and the frozen time cutoff, retaining dissipation from both the passive field and shear, to obtain",
  "Conclusion first: only outer accumulated dissipation remains on the complete clock",
  "The conclusion applies only to the inversion-paired exact family, for which the Version-M mollified trajectory is identically zero. It is not a theorem for arbitrary suitable weak solutions.",
  "The exact remainder is temporal packing",
  "Set the frozen indices and scales as displayed. The velocity field remains",
  "Previous major milestone recap PDF",
  "Previous major cumulative recap through R0.75A",
  "Stopping line and next proposition",
  "The next proposition has two possible forms: prove the outer-dissipation packing condition or construct an exact smooth counterexample with complete accounting. Neither is complete.",
  "Research note R0.75B · Step 27 · OUTER PADDING GATE",
  "Therefore the endpoint and full accumulated smooth-dissipation rows on the safe region close together.",
  "For the frozen exact smooth periodic inversion-paired common-shear family, Version-M cubic payment covers the safe complete subclock, inner padding, and the full endpoint row. The only unclosed term is full-time accumulated physical dissipation on the outer transition collar. Complete K, fixed deletion, arbitrary suitable-weak extension, and regularity remain OPEN.",
  "A positive coefficient says only that this upper-bound method cannot absorb the term uniformly with the frozen exponents. No saturating exact solution is constructed, so this is not a complete-clock counterexample.",
  "Evidence levels and literature boundary",
  "Status · R0.75B STEP 27",
  "The adverse full-window rate is not a counterexample",
  "The bounded primary-source screen confirms that local-energy/Caccioppoli is an established method but finds no direct statement of the frozen weighted ledger and effective-count threshold in the three screened sources. This finite non-hit establishes neither novelty nor priority.",
  "Certificate: Python 8/8, Ruby 9/9, 47 unique tags, byte-identical output across three hash seeds, and 20/20 plus 21/21 mutations rejected. The certificate covers only finite exact arithmetic, source binding, and structural sentinels. The bounded literature screen only confirms that Caccioppoli is an established method; a finite non-hit establishes neither novelty nor priority. This section is purely analytic and contains no formal figure, simulation, DNS, or DGX.",
  "NEXT / R0.75C not authorized or read",
  "The coarse full-window estimate for outer-collar accumulated dissipation gives only",
  "Outer-collar accumulated-dissipation packing remains OPEN",
  "Outer-collar accumulated-dissipation packing remains OPEN →",
  "The outer-collar endpoint is also paid",
  "The primary analytic audit passes with zero blockers. The Python certificate is 8/8 and the independent Ruby verifier is 9/9; all 20/20 and 21/21 targeted mutations are rejected, three hash seeds are byte-identical, and all 47 equation tags and references resolve. They verify exact arithmetic, source binding, and structure, not the continuous PDE proof.",
  "The safe complete subclock is paid",
  "The safe complete subclock, inner padding, and the full endpoint row are paid; only outer-collar accumulated dissipation remains. The adverse full-window rate is method failure, not a counterexample. Complete K, fixed deletion, suitable-weak extension, and regularity remain OPEN. NO NOVELTY CLAIM. NOT CLAY.",
  "The safe cutoff and outer collar must be separated",
  "Combining the safe endpoint and outer endpoint pays the full endpoint row.",
  "The safe support has at most the displayed spacetime volume. Holder's inequality and the doubled-radius payment row give",
  "Step 27 main text",
  "Step 27 main text, primary and literature audits, two certificate implementations, and QA",
  "Time-cutoff Caccioppoli ledger",
  "The time-cutoff Caccioppoli ledger splits the frozen shell into a safe region and an outer transition collar.",
  "The transport term has a positive sign on the right-hand side; the initial term vanishes because the time cutoff is zero near the initial time. The certificate locks this sign, the displayed prefactor, and all numbered references.",
];

assert.equal(summaries.length, 87, "R0.75B Step 27 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75B Step 27 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75B Step 27 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75B Step 27 source-string count drift");
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
  release: "R0.75B Step 27",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
