import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";


const root = resolve(process.env.R072Y_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r072y-missing.json");
const checkOnly = process.argv.includes("--check-only");
const activePages = [
  "literature-review.html",
  "notes/r0-72y.html",
  "recap-r0-61-r0-72y.html",
  "research-review.html",
];

for (const relative of activePages) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.38')) {
    throw new Error(`${relative}: expected i18n cache version v1.38`);
  }
}

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r072y\d+$/.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72Y batch");
}

const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(activePages)) {
  throw new Error(`Unexpected R0.72Y missing-string files: ${JSON.stringify(missingFiles)}`);
}

const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
if (!Array.isArray(snapshot) || snapshot.length === 0) {
  throw new Error("Empty R0.72Y snapshot");
}
const snapshotChinese = snapshot.map((entry) => entry.zh);
const liveChinese = missing.map((entry) => entry.zh);
if (JSON.stringify(snapshotChinese) !== JSON.stringify(liveChinese)) {
  const index = liveChinese.findIndex((value, offset) => value !== snapshotChinese[offset]);
  throw new Error(`R0.72Y missing-string snapshot drift at row ${index + 1}`);
}
const englishByChinese = new Map(snapshot.map((entry) => [entry.zh, entry.en]));
if (englishByChinese.size !== snapshot.length) {
  throw new Error("Duplicate R0.72Y snapshot keys");
}

const longRoute = missing.find(
  (entry) =>
    entry.zh.startsWith("中。R0.69P–R0.71P")
    && entry.zh.includes("R0.72Y 从 Navier--Stokes 重新推导完整"),
);
const previousRoute = retained.find(
  (entry) =>
    entry.zh.startsWith("中。R0.69P–R0.71P")
    && entry.zh.includes("R0.72X 把 graph constant 推到固定")
    && !entry.zh.includes("R0.72Y 从 Navier--Stokes 重新推导完整"),
);
if (!longRoute || !previousRoute) {
  throw new Error("Missing cumulative R0.72Y literature-route binding");
}
const routeMarker = " The global caustic image is not completed";
if (!previousRoute.en.includes(routeMarker)) {
  throw new Error("Unexpected retained R0.72X literature-route shape");
}
englishByChinese.set(
  longRoute.zh,
  previousRoute.en.slice(0, previousRoute.en.indexOf(routeMarker))
    + " The global caustic image is not completed, and general three-dimensional Navier--Stokes regularity is not proved. R0.72T--W fix and close the exact scalar A2 collision block, and R0.72X then establishes the all-start A2 path on a fixed physical compact set; Bloch uniformity still belongs only to that scalar path. R0.72Y rederives the complete Fourier--Leray row, the pressure factor two, the Orr--Sommerfeld--Squire triangularization, and velocity recovery directly from Navier--Stokes. It separates the scalar invariant-row forcing conclusions by spatial norm: standard H^-1 spacetime transfer has order alpha, semiclassical H^-1 spacetime transfer has order alpha^2, and the standard endpoint has no vanishing alpha gain. Exact zero-coupling lift-up makes epsilon-only full-row closure and strict contraction of every row FALSE. The strong complete-row A2 estimate, the low-gap vector direct sum, the complete linearized shear subsystem, nonlinear Navier--Stokes, and Clay remain OPEN.",
);

const boundaryTokens = (value) => value.match(/\b(?:CLOSED|OPEN|FALSE)\b/g) ?? [];
const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh)?.trim();
  if (!en || en === "__DERIVED_FROM_R072X_ROUTE__" || containsChinese(en)) {
    throw new Error(`Invalid R0.72Y English row: ${entry.zh}`);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error(`Plural voice in R0.72Y English row: ${entry.zh}`);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error(`Protected-token mismatch for R0.72Y row: ${entry.zh}`);
  }
  if (JSON.stringify(boundaryTokens(en)) !== JSON.stringify(boundaryTokens(entry.zh))) {
    throw new Error(`CLOSED/OPEN/FALSE boundary drift for R0.72Y row: ${entry.zh}`);
  }
  return { ...entry, id: `r072y${String(index + 1).padStart(3, "0")}`, en };
});

const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  if (new Set(finalTranslations.map((entry) => entry[field])).size !== finalTranslations.length) {
    throw new Error(`Duplicate final translation ${field}`);
  }
}
const finalByChinese = new Map(finalTranslations.map((entry) => [entry.zh, entry.en.trim()]));
const stillMissing = source.filter((entry) => !finalByChinese.has(entry.zh));
if (stillMissing.length) {
  throw new Error(`Live string remains untranslated: ${stillMissing[0].zh}`);
}

const dictionary = Object.fromEntries(source.map((entry) => [entry.zh, finalByChinese.get(entry.zh)]));
const jsonOutput = JSON.stringify(finalTranslations, null, 2) + "\n";
const bundleOutput = `globalThis.NS_EN_TRANSLATIONS = Object.freeze(${JSON.stringify(dictionary, null, 2)});\n`;
if (checkOnly) {
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.72Y translations are stale");
  }
  if (await readFile(bundlePath, "utf8") !== bundleOutput) {
    throw new Error("R0.72Y bundle is stale");
  }
} else {
  await Promise.all([
    writeFile(translationPath, jsonOutput),
    writeFile(bundlePath, bundleOutput),
  ]);
}

console.log(JSON.stringify({
  checkOnly,
  added: translatedEntries.length,
  total: finalTranslations.length,
  liveStrings: source.length,
  missingAfter: stillMissing.length,
  bundle: "public/i18n-en.js",
}));
