#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r075vstep47";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  "12/12 frozen files; no formal scientific figure, simulation, DNS, or DGX; finite checks do not replace the continuum multiplier-jet or endpoint-trace proof. NO NOVELTY CLAIM. NOT CLAY.",
  "Connect A's local dichotomy to the complete clock and physical signed flux.",
  "Extend the one-mode gain to a finite packet and connect it to physical collar mass.",
  "Extend the one-mode theorem directly to a packet theorem.",
  "Treating a failed method as a counterexample; modewise absolute values; ignoring signed cancellation.",
  "Split the two-wave cubic mass into two one-wave lower bounds.",
  "Retain and pay the joint quadratic cancellation of all three rows.",
  "Preserve the previous milestone recap",
  "From clock compression to complete signed flux for an exact high-carrier pair",
  "Frozen commit, certificates, and publication boundary",
  "For the exact diffusive pair with the stated amplitude, dyadic-band, and high-carrier conditions, T, U, and V combine to give",
  "Taking absolute values of the three rows separately; factoring the common phase too early; replacing continuum lemmas with finite stress tests.",
  "Construct an exact family that genuinely pays the flux.",
  "Treat one two-harmonic dyadic pair exactly.",
  "Spatial coercivity, the difference row, and the coupled self/sum block do not replace one another",
  "Identify the plateau-only obstruction and close the complete-frequency one-harmonic case.",
  "Every power of R cancels and the exact logarithmic L^2 rate remains -2/11907. This is a finite-dimensional exact-subfamily theorem, not an arbitrary two-mode projection or arbitrary-field estimate.",
  "Does the cubic collar mass of the same dyadic pair retain the cancelling beat defect?",
  "Extend to a dyadic packet.",
  "Stress-test two-wave cancellation.",
  "Use T's beat defect to pay the low difference-frequency row of the exact flux.",
  "Read R0.75V Step 47",
  "Realize a physical flux gain in an exact common-shear family.",
  "Pay the remaining self/self/sum block without destroying quadratic cancellation.",
  "The earlier clock-compression route and A's local dichotomy remain valid",
  "This cumulative milestone recap after R0.60 contains 190 nodes and covers 250 public notes. It preserves the recap through R0.75A byte-for-byte and compresses the twenty-one B–V nodes into an auditable route, with a strict distinction among T, U, and V.",
  "These steps organize necessary ledgers; they do not prove arbitrary-field E.24.",
  "Prove sharp spatial collar coercivity, recording two-wave cancellation with the stated beat defect.",
  "Pay the difference-frequency row.",
  "Only the exact diffusive high-carrier dyadic two-harmonic pair; Version-M V.43 remains conditional.",
  "Covers only one harmonic or a diagnostic family.",
  "Spatial coercivity only; it does not pay the temporal signed flux.",
  "A packetwise cardinality loss; paying arbitrary multimode flux from plateau mass alone.",
  "B pays the safe subclock; C--F rule out packing, positivity, and naive modal routes; G fixes the exact gain threshold.",
  "The four-frequency signed flux of the exact high-carrier dyadic pair is fully paid",
  "A fixed positive adjoint majorant; manufacturing gain by amplitude scaling.",
  "Using fixed-grid fast-phase quadrature as proof.",
  "H's ballistic residence, K's positive-majorant no-go, and L's one-real-harmonic diffusive k^(-2/3) gain isolate a cancellation-compatible route.",
  "Inter-packet aggregation and the arbitrary-field problem remain open.",
  "Low carriers, three or more modes, arbitrary packets, and general Version-M extraction.",
  "Low-carrier pairs, three or more harmonics, arbitrary dyadic packets, inter-packet aggregation, nonconstant or vertically dependent shear, projection from a larger velocity, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain OPEN. Later versions were not authorized, read, or published.",
  "M retains a mode-count-free packet gain; N calibrates the radial-collar Wiener row; O--Q establish vertical-diffusion, entrance-concentration, and spatially spread one-harmonic payments.",
  "The multiplier two-jet, exact quadratic identity, phase-by-phase integration by parts, heat extra term, and right-endpoint trace jointly prove V.3; adding U gives the complete exact-pair signed flux V.4.",
  "After pair closure, the open boundary begins with low carriers and three-plus modes",
  "R gives a multimode concentration obstruction; S completes the complete-clock payment for one exact harmonic at every frequency.",
  "Cumulative recap of 190 nodes from R0.61 through R0.75V, distinguishing T's spatial coercivity, U's difference-frequency payment, V's coupled self/sum payment, and the exact-pair theorem",
  "The 169-node ledger from R0.61 through R0.75A remains an independent, byte-exact prior recap. B–V starts from A.63's complete-clock extraction gap and passes through signed-flux route screening, one-mode and packet payments, collar calibration, and a multimode obstruction before splitting the exact two-harmonic high-carrier branch into T, U, and V.",
  "R0.61–R0.75V cumulative milestone recap | From clock compression to exact-pair signed flux",
  "All nodes from R0.61 through R0.75V",
  "S's Version-M consequence still depends on the realized-subclass and ledger-alignment hypotheses.",
  "T proves only that the plateau cubic mass of the same high-carrier dyadic pair controls the sharp two-wave beat defect; it does not pay temporal signed flux.",
  "The two self rows and the sum row remain uncontrolled, so this is not a complete pair theorem.",
  "U pays the difference row with a complete-clock weighted moving-phase estimate; the self/self/sum rows remain one unpaid coupled block.",
  "V does not take rowwise absolute values: it retains quadratic cancellation and jointly pays the remaining block. Only after combining with U does this yield the complete signed-flux theorem for the exact pair.",
  "The weighted moving-phase lemma and radial quotient give a complete-clock payment of the difference row; every power of R cancels and the rate is -2/11907.",
  "Master index of 250 research notes",
  "View the R0.75V card on the home page",
  "Current endpoint R0.75V Step 47 exact-pair complete signed-flux payment",
  "logarithmic rate. NO NOVELTY CLAIM. NOT CLAY.",
  "Cumulative milestone recap R0.61–R0.75V · 2026-09-04",
  "Jump to the R0.75V card on the home page →",
  "Research note R0.75V Step 47 · 2026-09-04 · COUPLED SELF/SUM PAYMENT",
  "Read the complete R0.61–R0.75V cumulative recap →",
  "Read the latest R0.75V research note →",
  "Expand 160 public notes",
  "Review v2.26 · 2026-09-04",
  "Latest milestone recap through V",
  "Latest cumulative recap (R0.61–R0.75V, 190 nodes)",
  "Low carriers, three or more modes, arbitrary packets, general Version-M extraction, regularity, and the Clay problem remain OPEN.",
  "The cumulative recap after R0.60 contains 190 nodes; the site now has 250 public research notes",
  "R0.70A–R0.75V · 152 sections published",
  "R0.70A–R0.75V: 152 sections published, 104 fully archived",
  "R0.75V Step 47 retains and pays the joint cancellation of the two self rows and the sum row. Combined with U's difference row, it gives a complete signed collar-flux theorem for one exact diffusive high-carrier dyadic two-harmonic pair. Low carriers, three or more modes, and arbitrary packets remain open.",
  "R0.75V: complete signed-flux payment for one dyadic two-harmonic pair",
  "R0.75V | Complete signed-flux payment for one dyadic two-harmonic shear",
  "T supplies two-wave spatial collar coercivity, U pays the difference-frequency row, and V retains and pays the joint cancellation of the two self rows and sum row. Together they prove the complete signed collar-flux theorem only for one exact diffusive high-carrier dyadic two-harmonic pair while retaining the exact",
  "T fixes two-wave spatial coercivity, U pays the difference-frequency row, and V jointly pays the self and sum rows; the complete signed flux for the exact high-carrier dyadic pair is closed.",
  "V's multiplier two-jet, quadratic cancellation, separate phase integration, and right-endpoint trace jointly pay the self/sum block. Adding U's difference row yields the complete signed-flux theorem for the exact high-carrier dyadic pair. Low carriers, three modes or more, arbitrary packets, and general Version-M extraction remain open. There is no formal figure, simulation, DNS, or DGX. NO NOVELTY CLAIM. NOT CLAY.",
  "V closes the complete signed collar flux only for one exact diffusive high-carrier dyadic two-harmonic pair. Low-carrier pairs, three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction remain open. Later work was not authorized, read, or published.",
  "Literature review v2.26 · 2026-09-04",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.75V work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Read the milestone recap through V",
  "Outside the exact pair, low carriers, three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, E.24, and Version-M extraction remain open. Later material was not authorized, read, or published.",
  "PROVED: the V.13--V.17 radial-quotient two-jet; V.21--V.25 quadratic cancellation and heat extra term; V.27 exact separate-phase integration; V.31--V.36 right-endpoint trace; V.3 joint self/sum payment; V.4--V.7 complete exact-pair signed-flux estimate, R-power cancellation, and -2/11907 rate; and the exact smooth unforced shear V.42. CONDITIONAL: V.43 still requires realized-subclass and ledger alignment, with F a component of the same actual velocity. OPEN: low-carrier pairs, three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertically dependent shear, projection, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity. Finite checks do not replace continuum lemmas; there is no formal figure, simulation, numerical fit, DNS, or DGX.",
  "R0.75V Step 47 bounded primary-source screen and claim boundary",
  "R0.75V Step 47 public boundary · EXACT HIGH-CARRIER PAIR ONLY",
  "Singh--Sridhar, Bedrossian--Vicol--Wang, Egidi--Veselic, and the official Clay statement provide only adjacent context on exact shear, mixing, observability, and the Millennium problem. V's multiplier two-jet, quadratic cancellation, endpoint trace, and flux payment use local elementary arguments and import none of those external theorems. A finite search establishes no completeness, novelty, or priority conclusion.",
  "Step 47 jointly pays the two self rows and the sum row using the radial-quotient two-jet, quadratic cancellation, phase-by-phase integration by parts, and a right-endpoint complete-clock trace. Combined with U's difference row, this yields the complete signed collar-flux theorem for the exact diffusive high-carrier dyadic pair.",
  "250 public research notes; latest node R0.75V.",
  "Complete signed-flux payment for one dyadic two-harmonic shear",
  "Research-note master index · v2.26 · 2026-09-04",
  "Latest node R0.75V · continuously revised",
  "364 / Full text",
  "365 / Full text",
  "366 / Full text",
  "367 / Full text",
  "368 / Full text",
  "369 / Full text",
  "370 / Full text",
  "371 / Full text",
  "372 / Full text",
  "373 / Full text",
  "This site stops at R0.75V Step 47. V closes the complete signed collar flux only for one exact diffusive high-carrier dyadic two-harmonic pair. Low-carrier pairs, three or more harmonics, arbitrary packets, inter-packet aggregation, nonconstant or vertical shear, projection, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later work was not authorized, read, or published.",
  "logarithmic rate. Low carriers, three modes or more, and arbitrary packets remain open.",
  "Later-work boundary →",
  "Synchronized recap PDF",
  "Research note R0.75V · Step 47 · COUPLED SELF/SUM PAYMENT",
  "Status · R0.75V STEP 47",
  "Latest cumulative recap through R0.75V",
  "Certificate: Python 17/17, Ruby 18/18, V.1--V.43, 43/43 tags, and 43/43 displays; byte stability across three Python hash seeds and complete regeneration stability; both implementations reject all 84/84 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite checks do not replace the continuum multiplier-jet or endpoint-trace proof. This section contains no formal figure, simulation, DNS, or DGX.",
  "Step 47 main text",
  "Step 47 main text, primary-source boundary, two certificate implementations, and fail-closed QA",
  "The exact roles of T, U, and V",
  "V / Frozen evidence",
  "V retains the joint quadratic cancellation of the two self-frequency rows and the sum-frequency row and pays this coupled block. Combined with U's difference-frequency payment, it gives a complete signed collar-flux theorem only for one exact diffusive high-carrier dyadic two-harmonic pair while retaining the exact",
];

assert.equal(summaries.length, 115, "R0.75V Step 47 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.75V Step 47 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.75V Step 47 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.75V Step 47 source-string count drift");
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
  release: "R0.75V Step 47",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
