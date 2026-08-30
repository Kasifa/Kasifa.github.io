import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(process.env.R073F_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r073f-missing.json");
const checkOnly = process.argv.includes("--check-only");
const captureMissing = process.argv.includes("--capture-missing");
const activePages = [
  "literature-review.html",
  "notes/index.html",
  "notes/r0-73f.html",
  "recap-r0-61-r0-73f.html",
  "research-review.html",
];
const discouragedChinese = [
  "我们",
  "攻关",
  "主攻",
  "突破",
  "研究纪律",
  "三重审计",
  "杀死错误想法",
];

for (const relative of activePages) {
  const html = await readFile(resolve(publicDirectory, relative), "utf8");
  if (!html.includes('/i18n-en.js?v=1.46')) {
    throw new Error(relative + ": expected i18n cache version v1.46");
  }
  for (const phrase of discouragedChinese) {
    if (html.includes(phrase)) throw new Error(relative + ": public-voice violation " + phrase);
  }
}

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r073f\d+$/.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.73F batch");
}

const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(activePages)) {
  throw new Error("Unexpected R0.73F missing-string files: " + JSON.stringify(missingFiles));
}

if (captureMissing) {
  const skeleton = missing.map(({ zh }) => ({ zh, en: "" }));
  await writeFile(snapshotPath, JSON.stringify(skeleton, null, 2) + "\n");
  console.log(JSON.stringify({
    captured: skeleton.length,
    snapshot: "scripts/i18n-snapshots/r073f-missing.json",
  }));
  process.exit(0);
}

const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
if (!Array.isArray(snapshot) || snapshot.length === 0) {
  throw new Error("Empty R0.73F snapshot");
}
const snapshotChinese = snapshot.map((entry) => entry.zh);
const liveChinese = missing.map((entry) => entry.zh);
if (JSON.stringify(snapshotChinese) !== JSON.stringify(liveChinese)) {
  const index = liveChinese.findIndex((value, offset) => value !== snapshotChinese[offset]);
  throw new Error("R0.73F missing-string snapshot drift at row " + String(index + 1));
}
const englishByChinese = new Map(snapshot.map((entry) => [entry.zh, entry.en]));
if (englishByChinese.size !== snapshot.length) {
  throw new Error("Duplicate R0.73F snapshot keys");
}

const boundaryTokens = (value) =>
  value.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [];
const accountingTokens = (value) =>
  [...value.matchAll(
    /R0\.\d+[A-Z]?|v\d+(?:\.\d+)+|(?<![\p{L}\p{N}_])\d+(?:\.\d+)?(?![\p{L}\p{N}_])/gu,
  )].map((match) => match[0]);

const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh)?.trim();
  if (!en || containsChinese(en)) {
    throw new Error("Invalid R0.73F English row: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Plural voice in R0.73F English row: " + entry.zh);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error("Protected-token mismatch for R0.73F row: " + entry.zh);
  }
  if (JSON.stringify(accountingTokens(en)) !== JSON.stringify(accountingTokens(entry.zh))) {
    throw new Error("Version/count-token mismatch for R0.73F row: " + entry.zh);
  }
  if (JSON.stringify(boundaryTokens(en)) !== JSON.stringify(boundaryTokens(entry.zh))) {
    throw new Error("Claim-state boundary drift for R0.73F row: " + entry.zh);
  }
  return {
    ...entry,
    id: "r073f" + String(index + 1).padStart(3, "0"),
    en,
  };
});

const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  if (new Set(finalTranslations.map((entry) => entry[field])).size !== finalTranslations.length) {
    throw new Error("Duplicate final translation " + field);
  }
}
const finalByChinese = new Map(finalTranslations.map((entry) => [entry.zh, entry.en.trim()]));
const stillMissing = source.filter((entry) => !finalByChinese.has(entry.zh));
if (stillMissing.length) {
  throw new Error("Live string remains untranslated: " + stillMissing[0].zh);
}
const dictionary = Object.fromEntries(
  source.map((entry) => [entry.zh, finalByChinese.get(entry.zh)]),
);
const jsonOutput = JSON.stringify(finalTranslations, null, 2) + "\n";
const bundleOutput =
  "globalThis.NS_EN_TRANSLATIONS = Object.freeze(" +
  JSON.stringify(dictionary, null, 2) +
  ");\n";

if (checkOnly) {
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.73F translations are stale");
  }
  if (await readFile(bundlePath, "utf8") !== bundleOutput) {
    throw new Error("R0.73F bundle is stale");
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
