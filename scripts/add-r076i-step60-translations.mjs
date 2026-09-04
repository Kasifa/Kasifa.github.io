#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r076istep60";

// Local direct translations in deterministic collectSiteStrings order. No DGX is used.
const summaries = [
  ", and the exact normalized rate returns to",
  ", so it rejects only G's explicit candidate.",
  ", therefore allowing",
  "; bilateral rescaling, polynomial derivative and terminal rows, the complete-real four-row energy identity, and physical normalization yield",
  ". It therefore retains the exact negative logarithmic rate under",
  ". This is not a theorem for arbitrary packets or arbitrary fields.",
  "12/12 frozen files; no formal scientific figure, simulation, DNS, or DGX; finite checks do not validate the imported 34-page preprint. CONDITIONAL-LITERATURE. NOT CLAY.",
  "cost to absorb the cap; the raw rate is",
  "From the exp(Cq) barrier to a conditional Chebyshev-scale window",
  "Frozen commit, certificates, and evidence levels",
  "An independent proof of Zhang Proposition 4.2, sharp polynomial dependence, a matching exact-shear lower bound, multiple dyadic bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain OPEN. Later versions remain unauthorized, unread, and unpublished.",
  "A structural gap remains before arbitrary nonlinear fields",
  "The spatial lower bound, central-fibre flux, and full-plateau absorption must remain distinct",
  "The preceding cumulative recap remains an independent historical object and is not rewritten. It covers clock compression, signed-flux route screening, single-mode and exact two-harmonic families, the T–V high-carrier pair closure, and W's independent local-energy payment for low carriers.",
  "upper bound and",
  "The shrinking endpoint gap expands the sufficient window to",
  "scale.",
  "After the same packet acquires nonzero drift, it produces an exponential signed-flux lower bound over the complete clock relative to a central-fibre proxy; that denominator is not the physical plateau mass.",
  "The normalized exterior gap of the full plateau is",
  "absorbs the exponential and polynomial losses, while the exact normalized rate remains",
  "retains the exact negative logarithmic rate",
  "The explicit shifted-binomial packet proves that E's fixed spatial observation row requires at least exponential mode loss; its realizing example has zero drift and therefore no complete flux lower bound.",
  "Adjacent full-plateau fibres pay",
  "Read R0.76I Step 60",
  "This is the cumulative milestone recap after R0.60. It contains 203 nodes and the site had 263 public research notes at the endpoint. It preserves the previous recap through R0.75W byte-for-byte and connects the twelve nodes R0.75X–R0.76I into an auditable route, distinguishing the evidence levels of E, F–H, and I.",
  "The composite theorem depends on Zhang Proposition 4.2, which has not been independently reproved on this site; it covers only exact real one-band constant shears.",
  "A 203-node cumulative recap from R0.61 through R0.76I, distinguishing E's uniform exponential barrier, the explicit-candidate sequence F–H, and I's literature-conditional q=o(L^(5/2)) exact-shear window",
  "The 191-node R0.61–R0.75W ledger is preserved byte-for-byte",
  "R0.61–R0.76I cumulative milestone recap | From the exp(Cq) barrier to a conditional Chebyshev-scale window",
  "Every node from R0.61 through R0.76I",
  "R0.76E gives a frequency-uniform full-plateau estimate for exact real one-band constant shears, but pays",
  "Zhang 2026-07 arXiv v1 Proposition 4.2 gives endpoint extrapolation for arbitrary real-frequency sparse Fourier sums; Erdelyi and Kós give the interior, Markov derivative, and reverse-time endpoint inequalities.",
  "Master index of 263 research notes",
  "View the R0.76I card on the home page",
  "Current endpoint R0.76I Step 60 Chebyshev-scale conditional full-plateau window",
  "The recap distinguishes E's exp(Cq)/q=o(L²) barrier, the explicit-candidate lower-bound, flux, and absorption chain F–H, and I's Zhang-arXiv-v1-dependent exp(O(q/√a))/q=o(L^(5/2)) conditional upper bound.",
  "Cumulative milestone recap R0.61–R0.76I · 2026-09-05",
  "Jump to the R0.76I card on the home page →",
  "Research note R0.76I Step 60 · 2026-09-05 · CHEBYSHEV-SCALE FULL-PLATEAU WINDOW",
  "Read the complete R0.61–R0.76I cumulative recap →",
  "Read the latest R0.76I research note →",
  "Conditional on Zhang 2026-07 arXiv v1 Proposition 4.2, I uses bilateral endpoint extrapolation, Erdelyi's derivative estimate, Kós's terminal trace, and the complete four-row energy identity to expand the exact real one-band constant-shear sufficient window to q=o(L^(5/2)), while retaining the exact normalized rate -2/11907. There is no formal figure, simulation, DNS, or DGX. CONDITIONAL-LITERATURE. NOT CLAY.",
  "Expand 173 public notes",
  "Review v2.39 · 2026-09-05",
  "Latest milestone recap through I",
  "Latest cumulative recap (R0.61–R0.76I, 203 nodes)",
  "I's composite theorem depends on Zhang arXiv v1 Proposition 4.2, which has not been independently reproved, and covers only exact real one-band constant shears. Multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "An independent proof, multiple bands, arbitrary nonlinear packets, Version-M extraction, regularity, and Clay remain OPEN.",
  "The cumulative recap after R0.60 contains 203 nodes; the site now has 263 public research notes",
  "R0.70A–R0.76I · 165 sections published",
  "R0.70A–R0.76I: 165 sections published, 104 fully archived",
  "Conditional on Zhang 2026-07 arXiv v1 Proposition 4.2, R0.76I Step 60 changes the exact real one-band constant-shear full-plateau cost to q^7 exp(12√2q√Δ_a) and expands the sufficient window to q=o(L^(5/2)); this is not an arbitrary Navier–Stokes, Version-M, or regularity theorem.",
  "R0.76I: a conditional Chebyshev-scale full-plateau window",
  "R0.76I | Chebyshev-scale growing-mode window on the full plateau",
  "; derivative, terminal, and four-row reconstruction give the full cost",
  "An independent proof of Zhang Proposition 4.2, sharp polynomial dependence, a matching exact-shear lower bound, multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "and the sufficient window",
  "changes the exact real one-band constant-shear spatial loss to",
  "Literature review v2.39 · 2026-09-05",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P–R0.76I work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "Read the milestone recap through I",
  "LITERATURE: Zhang Proposition 4.2 and the three Erdelyi/Kós exponential-sum inequalities. PROVED LOCALLY: bilateral rescaling, full-plateau geometry, polynomial derivative and terminal consequences, complete four-row reconstruction, physical powers, and the asymptotic implication. CONDITIONAL-LITERATURE: the composite boxed theorem gives q⁷ exp(12√2q√Δ_a), the q=o(L^(5/2)) sufficient window, and the exact normalized rate -2/11907 only for exact real one-band constant shears. FINITE COMPUTATION: binds only exact ledgers, bytes, powers, signs, tags, and claim boundaries, and does not prove the imported continuum theorem. OPEN: an independent proof of Zhang Proposition 4.2, sharp polynomial dependence, a matching exact-shear lower bound, multiple bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity.",
  "Proposition 4.2 provides sparse-Fourier endpoint extrapolation without frequency separation; this 34-page 2026-07 v1 preprint is not represented as peer reviewed, and this site does not independently reproduce its Hardy-space proof.",
  "R0.76I Step 60 conditional-literature and exact-shear boundary",
  "R0.76I Step 60 public boundary · CHEBYSHEV-SCALE FULL-PLATEAU WINDOW",
  "Step 60 takes Zhang 2026-07 arXiv v1 Proposition 4.2 as a conditional literature input and uses the shrinking endpoint gap",
  "Theorems 2.3 and 2.20 and equation (1.2) supply the interior, Markov derivative, and Kós endpoint inputs. Zhang Proposition 8.4's confluent complex witness is retained only as range-qualified context for the larger sparse-Fourier class and is not converted into sharpness for exact real dyadic heat shears.",
  "263 public research notes; latest node R0.76I.",
  "Chebyshev-scale growing-mode window on the full plateau",
  "Research-note master index · v2.39 · 2026-09-05",
  "Latest node R0.76I · continuously revised",
  ", while the exact normalized rate remains",
  ", where",
  "; the sufficient window expands from",
  "472 / Full text",
  "473 / Full text",
  "474 / Full text",
  "475 / Full text",
  "476 / Full text",
  "477 / Full text",
  "478 / Full text",
  "479 / Full text",
  "480 / Full text",
  "Retained W recap",
  "This site is currently published through R0.76I Step 60. I's composite theorem depends on Zhang 2026-07 arXiv v1 Proposition 4.2, which has not been independently reproved, and covers exact real one-band constant shears only. Multiple dyadic bands, nonconstant shear, arbitrary nonlinear packets, arbitrary-field E.24, complete Version-M extraction, fixed deletion, suitable-weak transfer, regularity, and singularity remain open. Later versions remain unauthorized, unread, and unpublished.",
  "View the latest cumulative recap",
  "changes to",
  "to",
  "Research note R0.76I · Step 60 · CHEBYSHEV-SCALE FULL-PLATEAU WINDOW",
  "Taking Zhang 2026-07 arXiv v1 Proposition 4.2 as a literature premise, I changes the full-plateau loss for exact real one-band constant shears from",
  "Status · R0.76I STEP 60",
  "Certificate: Python 129/129, Ruby 129/129, I.1--I.38, and 42/42 displays; byte stability across three Python hash seeds and complete regeneration; both implementations reject all 129/129 targeted mutations and fail closed on unknown mutations. The complete frozen ledger is 12/12. Finite certificates do not prove Zhang Proposition 4.2 or the other continuum inequalities; this section contains no formal figure, simulation, DNS, or DGX.",
  "E's uniform barrier, the explicit-candidate chain F–H, and I's conditional window",
  "I / Frozen evidence",
  "Latest R0.61–R0.76I cumulative recap",
  "Step 60 main text",
  "Step 60 main text, literature boundary, two certificate implementations, and fail-closed QA",
];

assert.equal(summaries.length, 97, "R0.76I Step 60 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.76I Step 60 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.76I Step 60 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.76I Step 60 source-string count drift");
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
  release: "R0.76I Step 60",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
