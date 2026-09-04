#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075wstep48";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "12/12 frozen files; no formal scientific figure, simulation, DNS, or DGX; finite checks do not replace the continuum ODE compactness or Turan–Nazarov proof. NO NOVELTY CLAIM. NOT CLAY.",
  "Extending T's defect directly to low frequency; dividing by v, a frequency, or the frequency gap; taking absolute values row by row.",
  "Without the now-invalid T pointwise defect, how can one pay the low-carrier regime maR",
  "From clock compression to full-frequency signed flux for an exact pair",
  "For an exact diffusive pair with nonnegative amplitudes and dyadic frequencies, W pays maR<C_0 and V pays maR>=C_0, leaving no frequency endpoint uncovered:",
  "The three-step high-carrier chain and the independent low-carrier route do not replace one another",
  "Three or more harmonics, arbitrary dyadic packets, inter-packet aggregation, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain OPEN. R0.75X and later versions were not authorized, read, or published.",
  "Three or more modes, arbitrary packets, inter-packet aggregation, and complete Version-M transfer.",
  "Every power of R cancels and the exact logarithmic L^2 rate remains -2/11907. This is a finite-dimensional exact-subfamily theorem, not an arbitrary two-mode projection, three-mode, packet, or arbitrary-field estimate.",
  "Read R0.75W Step 48",
  "The earlier clock-compression route and the high-carrier exact-pair closure remain valid",
  "This cumulative milestone recap after R0.60 contains 191 nodes and covers 251 public notes. It preserves the recaps through R0.75A and R0.75V byte-for-byte and compresses the twenty-two B–W nodes into an auditable route, strictly separating the T–U–V high-carrier chain from W's independent low-carrier route.",
  "Only the exact diffusive dyadic two-harmonic shear; W.33's Version-M consequence remains conditional.",
  "Confluent fourth-order spatial observation, a frequency-gap-free Turan–Nazarov terminal trace, the scaled odd-kernel primitive, and the exact local-energy identity pay the low-carrier regime; combined with V's maR>=C_0 theorem, they give a full-frequency exact-pair theorem.",
  "The signed flux of an exact diffusive dyadic pair now covers all carrier frequencies",
  "After full-frequency pair closure, the open boundary begins with three-plus modes",
  "A 191-node cumulative recap from R0.61 through R0.75W, distinguishing the T–U–V high-carrier route, W's independent low-carrier payment, and their exhaustive union",
  "The 190-node ledger from R0.61 through R0.75V remains an independent, byte-exact prior recap. B–V starts from A.63's complete-clock extraction gap and proceeds through signed-flux route screening, one-mode and packet payments, collar calibration, and a multimode obstruction before T, U, and V close the exact two-harmonic high-carrier branch; W handles low carriers separately.",
  "R0.61–R0.75W cumulative milestone recap | From clock compression to full-frequency exact-pair signed flux",
  "All nodes from R0.61 through R0.75W",
  "T proves only under maR>=C_0 that plateau cubic mass controls the sharp two-wave beat defect; it does not pay temporal signed flux.",
  "U pays the difference row with a complete-clock weighted moving-phase estimate; the self/self/sum rows remain unpaid.",
  "V retains quadratic cancellation and jointly pays the remaining block; only after combining with U does this yield the high-carrier exact-pair theorem.",
  "W does not extend T's defect: confluent observation, a Turan–Nazarov trace, and the local-energy identity pay maR<C_0 and form an exhaustive high/low union with V.",
  "Master index of 251 research notes",
  "View the R0.75W card on the home page",
  "Current endpoint R0.75W Step 48 full-frequency exact-pair signed-flux payment",
  "Cumulative milestone recap R0.61–R0.75W · 2026-09-04",
  "Three or more modes, arbitrary packets, general Version-M extraction, regularity, and the Clay problem remain OPEN.",
  "Jump to the R0.75W card on the home page →",
  "Research note R0.75W Step 48 · 2026-09-04 · FULL-FREQUENCY EXACT PAIR",
  "Read the complete R0.61–R0.75W cumulative recap →",
  "Read the latest R0.75W research note →",
  "Expand 161 public notes",
  "Review v2.27 · 2026-09-04",
  "Latest milestone recap through W",
  "Latest cumulative recap (R0.61–R0.75W, 191 nodes)",
  "The cumulative recap after R0.60 contains 191 nodes; the site now has 251 public research notes",
  "R0.70A–R0.75W · 153 sections published",
  "R0.70A–R0.75W: 153 sections published, 104 fully archived",
  "R0.75W Step 48 pays maR<C_0 by an independent local-energy route. Combined with V's maR>=C_0 high-carrier theorem, this gives a complete signed collar-flux theorem without a carrier restriction for one exact diffusive dyadic two-harmonic shear. Three or more modes, arbitrary packets, and general Version-M transfer remain open.",
  "R0.75W: full-frequency signed-flux payment for one dyadic two-harmonic pair",
  "R0.75W | Full-frequency signed-flux payment for one dyadic two-harmonic shear",
  "T supplies high-carrier spatial coercivity, U pays the difference row, and V pays the remaining high-carrier coupled block; W uses confluent observation, a Turan–Nazarov terminal trace, and the local-energy identity to pay low carriers. Their exhaustive union gives full-frequency signed flux only for one exact diffusive dyadic two-harmonic shear. NO NOVELTY CLAIM. NOT CLAY.",
  "T fixes high-carrier spatial coercivity, U pays the difference row, V jointly pays the remaining high-carrier block, and W pays the low-carrier regime by an independent local-energy route. The exhaustive union gives full-frequency signed flux for the exact pair.",
  "W uses confluent fourth-order observation, a Turan–Nazarov terminal trace, and the exact local-energy identity to pay the low-carrier regime. Combined with V's high-carrier theorem, this gives a full-frequency theorem for an exact dyadic two-harmonic shear. Three or more modes, arbitrary packets, and general Version-M extraction remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "W closes full-frequency signed collar flux only for one exact diffusive dyadic two-harmonic shear. Three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction remain open. Later work was not authorized, read, or published.",
  "Literature review v2.27 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75W work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Read the milestone recap through W",
  "Outside the exact pair, three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction remain open. Later material was not authorized, read, or published.",
  "Nazarov's 1993/1994 original theorem and Friedland–Yomdin's 2013 primary restatement provide the exponential-polynomial measurable-set inequality; its constant is independent of imaginary frequencies and frequency gaps. The official Clay description only defines the Millennium problem. W proves its confluent spatial observation, scaled kernel, and local-energy identity locally. The bounded search establishes no completeness, novelty, or priority conclusion.",
  "PROVED: W.8--W.10 low-carrier scaling; W.12--W.14 confluent fourth-order observation; W.15--W.19 frequency-gap-free terminal trace; W.20--W.23 scaled radial primitive and exact flux scaling; W.24--W.29 local-energy identity; W.30--W.31 low-carrier payment; the exhaustive union of W.7 and V's high-carrier theorem; W.2--W.4 full-frequency exact-pair estimate, cancellation of all R powers, and the -2/11907 rate; and W.32 exact smooth unforced shear. CONDITIONAL: W.33 still requires the realized-subclass and ledger-alignment hypotheses, with F a component of the same actual velocity. OPEN: three or more harmonics; arbitrary packets; inter-packet aggregation; nonconstant or vertically dependent shear; projection; arbitrary-field E.24; complete Version-M extraction; fixed deletion; suitable-weak transfer; regularity; and singularity. The cubic center node only refutes a low-frequency extension of the old high-carrier pointwise defect, not W.2. Finite checks do not replace continuum lemmas; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75W Step 48 bounded primary-source screen and claim boundary",
  "R0.75W Step 48 public boundary · FULL-FREQUENCY EXACT DYADIC PAIR ONLY",
  "Step 48 uses confluent fourth-order spatial observation, a frequency-gap-free Turan–Nazarov terminal trace, and the exact local-energy identity to pay maR<C_0. Combined with V's maR>=C_0 high-carrier theorem, this gives a full-frequency signed collar-flux theorem for one exact diffusive dyadic two-harmonic shear.",
  "251 public research notes; latest node R0.75W.",
  "Full-frequency signed-flux payment for one dyadic two-harmonic shear",
  "Research-note master index · v2.27 · 2026-09-04",
  "Latest node R0.75W · continuously revised",
  "; combined with V's high-carrier theorem, this yields a complete signed collar-flux theorem without a carrier restriction only for one exact diffusive dyadic two-harmonic shear. The exact logarithmic rate remains",
  "374 / Full text",
  "375 / Full text",
  "376 / Full text",
  "377 / Full text",
  "378 / Full text",
  "379 / Full text",
  "380 / Full text",
  "381 / Full text",
  "382 / Full text",
  "383 / Full text",
  "This site stops at R0.75W Step 48. W combines V's high-carrier exact-pair result with an independent low-carrier local-energy route to obtain a full-frequency theorem for one exact diffusive dyadic two-harmonic shear. Three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "Research note R0.75W · Step 48 · FULL-FREQUENCY EXACT PAIR",
  "Status · R0.75W STEP 48",
  "Latest cumulative recap through R0.75W",
  "Certificate: Python 18/18, Ruby 19/19, W.1--W.33, 33/33 tags, and 34/34 displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 89/89 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace continuum ODE compactness or the Turan–Nazarov lemma. This section contains no formal figure, simulation, DNS, or DGX.",
  "Step 48 main text",
  "Step 48 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
  "The exact roles of T, U, V, and W",
  "W / Frozen evidence",
  "W does not extend the high-carrier pointwise defect. Instead, confluent fourth-order observation, a frequency-gap-free Turan–Nazarov terminal trace, and the exact local-energy identity independently pay",
];

assert.equal(summaries.length, 81, "R0.75W Step 48 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75W Step 48 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75W Step 48 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75W Step 48 source-string count drift");
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
  release: "R0.75W Step 48",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
