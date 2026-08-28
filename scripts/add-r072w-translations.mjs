import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";


const root = resolve(process.env.R072W_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r072w-missing.json");
const checkOnly = process.argv.includes("--check-only");
const activePages = [
  "literature-review.html",
  "notes/r0-72w.html",
  "recap-r0-61-r0-72w.html",
  "research-review.html",
];

for (const relative of activePages) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.36')) {
    throw new Error(`${relative}: expected i18n cache version v1.36`);
  }
}

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r072w\d+$/.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.72W batch");
}

const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(activePages)) {
  throw new Error(`Unexpected R0.72W missing-string files: ${JSON.stringify(missingFiles)}`);
}

const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
if (!Array.isArray(snapshot) || snapshot.length === 0) {
  throw new Error("Empty R0.72W snapshot");
}
const snapshotChinese = snapshot.map((entry) => entry.zh);
const liveChinese = missing.map((entry) => entry.zh);
if (JSON.stringify(snapshotChinese) !== JSON.stringify(liveChinese)) {
  const index = liveChinese.findIndex((value, offset) => value !== snapshotChinese[offset]);
  throw new Error(`R0.72W missing-string snapshot drift at row ${index + 1}`);
}
const englishByChinese = new Map(snapshot.map((entry) => [entry.zh, entry.en]));
if (englishByChinese.size !== snapshot.length) {
  throw new Error("Duplicate R0.72W snapshot keys");
}

const longRoute = missing.find(
  (entry) =>
    entry.zh.startsWith("中。R0.69P–R0.71P") &&
    entry.zh.includes("R0.72W 证明 finite H5/H7/R9 termwise absorption"),
);
const previousRoute = retained.find(
  (entry) =>
    entry.zh.startsWith("中。R0.69P–R0.71P") &&
    entry.zh.includes("R0.72V 再以 coefficient-uniform") &&
    !entry.zh.includes("R0.72W 证明 finite H5/H7/R9 termwise absorption"),
);
if (!longRoute || !previousRoute) {
  throw new Error("Missing cumulative R0.72W literature-route binding");
}
const routeTail = " General Navier–Stokes regularity remains open.";
const vMarker = " R0.72V then globalizes";
if (!previousRoute.en.endsWith(routeTail) || !previousRoute.en.includes(vMarker)) {
  throw new Error("Unexpected retained R0.72V literature-route shape");
}
englishByChinese.set(
  longRoute.zh,
  previousRoute.en.slice(0, previousRoute.en.indexOf(vMarker)) +
    " R0.72V then globalizes coefficient-uniform unit charts through a nonhomogeneous H^-1 direct sum, closing whole-line graph coercivity for the exact cubic linear scalar model; an independent all-L2 evolution yields fixed-block contraction." +
    " R0.72W proves that finite H5/H7/R9 termwise absorption is FALSE on the entire expanding period and instead retains the full analytic sine tail; the compact--escaping cell dichotomy, torus H^-1 direct sum, and all-L2 energy evolution close exact periodic scalar collision-block contraction. Uniformity as T downarrow 0 is FALSE; outer A1/A2 time concatenation, the complete linearized shear subsystem, nonlinear closure, and Clay remain open." +
    routeTail,
);

const boundaryTokens = (value) => value.match(/\b(?:CLOSED|OPEN|FALSE)\b/g) ?? [];
const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh)?.trim();
  if (!en || en === "__DERIVED_FROM_R072V_ROUTE__" || containsChinese(en)) {
    throw new Error(`Invalid R0.72W English row: ${entry.zh}`);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error(`Plural voice in R0.72W English row: ${entry.zh}`);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error(`Protected-token mismatch for R0.72W row: ${entry.zh}`);
  }
  if (JSON.stringify(boundaryTokens(en)) !== JSON.stringify(boundaryTokens(entry.zh))) {
    throw new Error(`CLOSED/OPEN/FALSE boundary drift for R0.72W row: ${entry.zh}`);
  }
  return { ...entry, id: `r072w${String(index + 1).padStart(3, "0")}`, en };
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
    throw new Error("R0.72W translations are stale");
  }
  if (await readFile(bundlePath, "utf8") !== bundleOutput) {
    throw new Error("R0.72W bundle is stale");
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
