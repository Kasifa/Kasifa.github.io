#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const translationPath = resolve(root, "translations/en.json");
const publicRoot = resolve(root, "public");
const checkOnly = process.argv.includes("--check-only");
const prefix = "r074ystep24";

// Local direct translations in deterministic collectSiteStrings order.
const summaries = [
  "Master index of 227 research notes",
  "The next step must construct exponential field cancellation on the full target box while proving that the correctors are negligible on both remote strips, do not restore cubic payment through their own fields, and close the complete payment upper bound. R0.74Z, R0.75A, and unlisted work are neither read nor published.",
  "View the R0.74Y card on the home page",
  "Current endpoint R0.74Y Step 24 route screen",
  "Jump to the R0.74Y card on the home page →",
  "Research note R0.74Y Step 24 · 2026-09-03 · ROUTE SCREEN",
  "Read the latest R0.74Y research note →",
  "Expand 137 public notes",
  "Review v2.03 · 2026-09-03",
  "In the frozen common-shear heat-packet geometry, a same-packet W endpoint cannot beat its mandatory target-lobe cubic payment; unequal amplitudes and non-adjacent placement both fail strictly. The changed geometry has only a formal necessary window, while Y.57 and accumulated viscosity remain OPEN. There is no formal figure, PDE data, DNS, or simulation. NOT CLAY.",
  "In the frozen geometry, a W-type endpoint cannot beat the same packet's mandatory cubic payment; the amplitude cancels, and non-adjacent placement is worse. The changed geometry provides only a formal necessary window, while Y.57 and the accumulated-viscosity branch remain OPEN. NOT CLAY.",
  "The cumulative recap after R0.60 contains 161 nodes; the site now has 227 public research notes",
  "R0.70A-R0.74Y · 129 sections published",
  "R0.70A-R0.74Y: 129 sections published, 102 fully archived",
  "R0.74Y Step 24 proves the frozen-geometry same-packet endpoint-versus-self-payment no-go and rules out repairs based only on unequal amplitudes or non-adjacent dyadic placement. The changed geometry has only a formal necessary exponent window; the Y.57 cancellation cell and the accumulated-viscosity occupation upper remain OPEN.",
  "R0.74Y: frozen self-payment no-go and formal cancellation window",
  "R0.74Y｜Payment-compatible two-coordinate route screen: frozen-geometry no-go and formal cancellation window",
  "The next step must construct full target-box cancellation, remote-strip negligibility, and a complete payment upper. R0.74Z, R0.75A, and unlisted work are neither read nor published.",
  "The frozen audit conducted a bounded primary-source screen covering exact Navier--Stokes shearing waves, pathwise passive-scalar dissipation in shear flows, heat observability and control cost, propagation of smallness, and quantitative unique continuation. It found no exact collision with the six-part conjunction. This is only a finite non-hit dated 2026-09-03, not evidence of novelty, priority, nonexistence, correctness, sharpness, or publishability.",
  "Literature review v2.03 · 2026-09-03",
  "I list published theorems as known results, mark 2026 preprints separately, and list this site's R0.69P-R0.74Y work only as research notes. I do not extrapolate computations or notes into a regularity theorem.",
  "PROVED (frozen geometry only): a same-packet W-type adjacent endpoint cannot beat its mandatory target-lobe cubic payment; the deficit age ell and heat age ell+1 stay distinct; Xi_fr(65)=-875993/968647680<0; unequal amplitudes alone and non-adjacent dyadic placement are strict no-go results. FORMAL NECESSARY ONLY: the changed geometry has a positive rational exponent window, not a constructed family or sufficient feasibility proof. OPEN / NOT CERTIFIED: the Y.57 cancellation cell, changed-geometry platform, all-winding survival, complete payment upper, accumulated-viscosity H1/occupation upper, whole-shell clock, general suitable weak solutions, regularity, and singularity. There is no formal scientific figure, PDE data, DNS, or simulation.",
  "R0.74Y Step 24 bounded literature screen and claim boundary",
  "R0.74Y Step 24 public boundary",
  "Step 23 uses an exact three-packet family to prove an endpoint obstruction relative to T* in two distinct coordinates; the actual payment-normalized counterexample is NOT PROVED.",
  "Step 24 proves the frozen-geometry same-packet endpoint-versus-self-payment no-go; unequal amplitudes and non-adjacent placement cannot repair it. The changed geometry has only a formal necessary exponent window, while Y.57 and accumulated viscosity remain OPEN.",
  "227 public research notes; latest node R0.74Y.",
  "Payment-compatible two-coordinate route screen: frozen-geometry no-go and formal cancellation window",
  "Research-note master index · v2.03 · 2026-09-03",
  "Latest node R0.74Y · continuously revised",
  "← Step 23: two-coordinate T* obstruction and cubic-payment gate",
  "186 / Full text",
  "187 / Full text",
  "188 / Full text",
  "189 / Full text",
  "190 / Full text",
  "191 / Full text",
  "192 / Full text",
  "193 / Full text",
  "194 / Full text",
  "195 / Full text",
  "Write packet i's amplitude as the displayed exponential law. The endpoint and its self-payment to the two-thirds power contain the same 2 alpha_i term, so their difference is",
  "This section does not prove Y.57.",
  "The target screened in this section is",
  "This site stops at R0.74Y Step 24. The next step must construct adjacent inversion-paired primaries and a finite corrector family under one common shear, and then prove full target-box cancellation, negligibility on both remote strips, and the complete payment upper. R0.74Z, R0.75A, and unlisted work were neither read nor published.",
  "A same-time vector lower bound is unnecessary. For the frozen exact smooth family, the displayed clock is nonnegative and the anomalous-defect row vanishes. None of the strip statements below is promoted to a whole-shell estimate.",
  "This conclusion covers only the frozen geometry when the target lobe has not been cancelled at field level; it does not rule out every possible cancellation architecture.",
  "Inner survival nevertheless requires the displayed upper bound on rho. Even with d=0, Theta is bounded below by c_gamma/12, and the most favorable adjacent dyadic case r=2 reaches the boundary equality",
  "In the frozen common-shear heat-packet geometry, a W-type adjacent endpoint cannot beat the same packet's mandatory target-lobe cubic payment; unequal amplitudes and non-adjacent placement both fail strictly.",
  "W-bridge survival requires the displayed strict upper bound. The key point is that the bridge deficit age is ell while the free heat age is ell+1; their denominators must not be merged. At the frozen height",
  "A higher-frequency passive profile would be a new architecture and would require a fresh audit of heat damping, initial energy, complete payment, and survival.",
  "The fixed-deletion functional is",
  "Conclusion first: the frozen-geometry no-go is proved, but the cancellation construction is not",
  "Reducing only the geometric gap d cannot change the weight identity or the irreducible Gamma^(1/4) payment weight, and polynomial changes in chord, volume, or residence time cannot alter the exponential sign. The payment row contains |u|^3, so opposite signed fluxes do not cancel it; the actual field must be cancelled throughout the target spacetime box.",
  "Both required inequalities are strict, so r=2 already fails and every r>2 is worse.",
  "Let a packet have scale L and the displayed height. On the adjacent inward strip, the W-type endpoint has exponential scale",
  "If future work proves all-winding derivative and occupation upper bounds, residence counting for a moving remote packet in a fixed R-width strip would formally give",
  "If the outer and inner scales obey the displayed dyadic relation, then the outer logarithmic radius rate is reduced by r squared. The outer packet's necessary payment-compatibility condition is",
  "If a corrector reduces the target-lobe residual field and target spacetime volume by the displayed exponential factors, the necessary self-compatibility condition becomes",
  "If the packet's target lobe is not removed by actual field cancellation, the nonnegative exterior velocity-cubic row forces",
  "The failure comes from the outer packet's own cubic payment, not from cancellation by a larger packet.",
  "The four route decisions must be read at distinct claim levels. Unequal amplitudes alone fail strictly in the frozen common-shear heat-packet geometry; non-adjacent dyadic placement is worse; geometry without exponential target-field cancellation cannot make two distinct W endpoints pass simultaneously; genuine exponential field cancellation leaves only a formal necessary exponent window and has not been constructed. The accumulated-viscosity branch has only a dimensional screen and no rigorous H1/occupation upper.",
  "Therefore every frozen-geometry construction that uses a same-packet W-type adjacent witness while paying that packet's target lobe fails payment compatibility.",
  "The nearest literature concerns exact Navier--Stokes shearing waves, pathwise passive-scalar dissipation in shear flows, heat observability and control cost, and propagation of smallness. These sources warn that exponentially accurate local cancellation may carry an exponentially large global cost, but they do not complete the corrector and payment construction here.",
  "Next proposition Y.57 and stopping line",
  "The existing heat-packet width and speed produce only polynomial changes, so omega_i=0 in the current architecture. The only screened mechanism not ruled out is genuine exponential field cancellation. In principle it can be expressed within the exact PDE algebra using finitely many inversion-paired passive correctors under the same shear, but no such corrector is constructed here.",
  "The formal ledger uses",
  "Research note R0.74Y · Step 24 · route screen",
  "One deletion set must be chosen before taking the time supremum. Consequently, lower bounds in two different coordinates at two possibly different times imply",
  "An amplitude tilt may balance two clock heights and improve cross-packet dominance, but it cannot create the missing self-payment gap. Combined with the frozen survival ceiling, this yields",
  "The squared amplitude therefore cancels exactly, and the necessary condition becomes",
  "The formal rate relative to cubic payment is",
  "This function is increasing on [64,65] and satisfies",
  "For these rational data, the formal W-survival reserve, U-reserve, reference-height deficit separation, and both remote cross margins are all strictly positive. After the outer amplitude tilt, the two formal adjacent endpoints have the same exponent; the reduced cross margin is still",
  "This is not a solution of the Navier--Stokes Millennium problem and does not claim a counterexample among general solutions.",
  "This is a route screen, not a cancellation-cell theorem, payment-compatible counterexample, regularity result, or singularity result.",
  "These positive fractions show only that the necessary exponent inequalities have a nonempty window. Missing ingredients include the changed-height common-shear platform, central-reference comparison, all-winding survival, full-box cancellation cell, remote-strip negligibility, control of the correctors' own payments, and a complete upper bound for P_R^M. There is no sufficient-feasibility or constructed-family claim here.",
  "Status · R0.74Y STEP 24",
  "The minimal next target Y.57 asks for two adjacent inversion-paired primaries and a finite corrector family under one common shear, with exponential field cancellation on the outer target spacetime box, negligible correctors on both remote inward strips, and",
  "Accumulated viscosity: a dimensional screen, not a no-go theorem",
  "Certificate and bounded literature boundary",
  "Certificate scope: finite exact arithmetic, source structure, hashes, and claim boundaries, not a continuous PDE proof;",
  "Formal necessary exponent window for the changed geometry",
  "The changed geometry leaves only a formal necessary exponent window; neither the cancellation cell nor the accumulated-viscosity occupation upper is proved. ROUTE SCREEN ONLY. NOT CLAY.",
  "Fixed-deletion functional and different witness times",
  "FORMAL NECESSARY ONLY: the changed geometry's rational exponent window; there is no platform, corrector, or complete-payment theorem.",
  "Literature: the bounded primary-source screen dated 2026-09-03 found only a finite non-hit; it does not establish novelty, priority, nonexistence, correctness, sharpness, or publishability.",
  "The final modeled gap between the outer-lobe payment and the common endpoint height is",
  "NEXT / R0.74Z awaiting a frozen package",
  "OPEN / NOT CERTIFIED: the accumulated-viscosity H1/occupation upper, Y.57, whole-shell clock, arbitrary suitable weak solutions, scale contraction, regularity, and singularity.",
  "The postulated outer target-lobe cancellation exceeds the minimum required amount by",
  "PROVED: in the frozen geometry, a same-packet W-type adjacent endpoint cannot beat its mandatory target-lobe cubic payment; the amplitude powers cancel exactly; non-adjacent dyadic placement is worse; and Xi_fr(65) is strictly negative with the displayed exact value.",
  "PUBLICATION BOUNDARY: formal figure NOT APPLICABLE. This section is purely analytic and contains no Navier--Stokes numerical simulation, DNS, DGX, or formal figure. ROUTE SCREEN ONLY | NO FORMAL FIGURE | NO PDE DATA | NO DNS | LOCAL DIRECT TRANSLATION | NO DGX | NOT CLAY.",
  "Python: 24/24 checks and 244 cases; independent Ruby: 21 assertions; the Python and Ruby implementations reject 22/22 and 23/23 mutations; seeds 0/1/42 are byte-identical. The certificate covers finite exact arithmetic, structure, hashes, and claim boundaries, while the literature audit is only a bounded non-hit; neither replaces a continuum PDE proof. This route screen has no formal scientific figure, PDE data, DNS, or simulation.",
  "Route A: unequal amplitudes alone fail strictly",
  "Route B: non-adjacent dyadic placement is worse",
  "Route C: only exponential cancellation of the target field remains unruled out",
  "Step 24 main text",
  "Step 24 main text, primary and literature audits, two certificate implementations, and QA",
  "The analogous dimensional target-shell rate is also negative. Current counting therefore predicts that time integration contributes an extra factor R, while monotonicity alone cannot repair the exponent. But the frozen sources do not provide the required H1/occupation upper, so these formulas cannot be stated as rigorous conclusions.",
  "Y.57 remains to be constructed →",
  "Y.57 cancellation-cell proposition remains OPEN",
];

assert.equal(summaries.length, 102, "R0.74Y Step 24 translation table length drift");

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
  assert.equal(rows.length, summaries.length, "R0.74Y Step 24 translation count drift");
  assert.deepEqual(
    rows.map((row) => row.en),
    rows.map((row, index) => withProtected(summaries[index], row.zh)),
    "R0.74Y Step 24 English translation drift",
  );
} else {
  assert.equal(missing.length, summaries.length, "R0.74Y Step 24 source-string count drift");
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
  release: "R0.74Y Step 24",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  checked: summaries.length,
  applied: !checkOnly,
}, null, 2)}\n`);
