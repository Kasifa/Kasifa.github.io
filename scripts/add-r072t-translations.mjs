import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "./i18n-lib.mjs";

const root = resolve(process.env.R072T_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r072t-missing.json");
const checkOnly = process.argv.includes("--check-only");

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r072t\d+$/.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) throw new Error("Duplicate retained Chinese keys");
const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
if (snapshot.length !== 136) throw new Error(`Expected 136 R0.72T snapshot rows, found ${snapshot.length}`);
const englishByChinese = new Map(snapshot.map((entry) => [entry.zh, entry.en]));
if (englishByChinese.size !== snapshot.length) throw new Error("Duplicate R0.72T snapshot keys");

for (const entry of snapshot) {
  entry.en = entry.en.replaceAll("2026-08-29", "2026-08-28")
    .replace("of which 47 satisfy", "of which 48 satisfy")
    .replace("we only get the time scale index", "the resulting time-scale index is")
    .replace("and we get", "and the result is")
    .replace("we get", "the result is")
    .replace("whether we can prove with uniform constants", "whether a uniform-constant estimate can be proved");
  englishByChinese.set(entry.zh, entry.en);
}

const set = (zh, en) => {
  if (!englishByChinese.has(zh)) throw new Error(`R0.72T correction key not found: ${zh}`);
  englishByChinese.set(zh, en);
};
set(
  "目标是以 interval-center-uniform 常数用 \\(\\partial_X(\\chi u)\\) 的 \\(L^2_SL^2_X\\) 范数和 equation residual 的 \\(L^2_SH^{-1}_X\\) 范数控制 \\(\\chi u\\) 的 \\(L^2_SL^2_X\\) 范数，并补齐 endpoint control；没有 uniform block contraction 前，不进入 periodic transfer。",
  "The target is an interval-center-uniform estimate using \\(\\partial_X(\\chi u)\\) in \\(L^2_SL^2_X\\) and the equation residual in \\(L^2_SH^{-1}_X\\) to control \\(\\chi u\\) in \\(L^2_SL^2_X\\), together with endpoint control; periodic transfer is deferred until uniform block contraction is proved.",
);
set(
  "用 \\(\\partial_X(\\chi u)\\) 的 \\(L^2_SL^2_X\\) norm 与 equation residual 的 \\(L^2_SH^{-1}_X\\) norm 控制 \\(\\chi u\\) 的 spacetime \\(L^2\\) norm，再补 all-start endpoint control。",
  "Control \\(\\partial_X(\\chi u)\\) in \\(L^2_SL^2_X\\), use the equation residual in \\(L^2_SH^{-1}_X\\), bound \\(\\chi u\\) in spacetime \\(L^2\\), and then add all-start endpoint control.",
);
set(
  "：尚缺参数自由模型在目标 \\(T\\asymp\\nu^{-3/5}\\) block 上的一致 \\(L^2\\) 收缩。",
  ": A uniform contraction on the target \\(T\\asymp\\nu^{-3/5}\\) block is still missing for the parameter-free model in \\(L^2\\).",
);
const longRoute = missing.find((entry) => entry.zh.startsWith("中。R0.69P–R0.71P") && entry.zh.includes("R0.72T 进一步固定 exact A2 spacetime germ"));
const oldRoute = retained.find((entry) => entry.id === "r072s014");
if (!longRoute || !oldRoute) throw new Error("Missing cumulative literature-route binding");
const tail = " General Navier–Stokes regularity remains open.";
if (!oldRoute.en.endsWith(tail)) throw new Error("Unexpected R0.72S route tail");
englishByChinese.set(longRoute.zh, oldRoute.en.slice(0, -tail.length) +
  " R0.72T further fixes the exact A2 spacetime germ and its unique scaling, and audits the quadratic wrong-model calibration, the physical 3/5 scaling, the combined fixed-f identity, inviscid mixing, and the CDZE 6/7 barrier; block contraction and periodic transfer remain open." + tail);

const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh)?.trim();
  if (!en || containsChinese(en)) throw new Error(`Invalid R0.72T English row: ${entry.zh}`);
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) throw new Error(`Plural voice in: ${entry.zh}`);
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error(`Protected-token mismatch for: ${entry.zh}`);
  }
  return { ...entry, id: `r072t${String(index + 1).padStart(3, "0")}`, en };
});
const finalTranslations = [...retained, ...translatedEntries];
for (const field of ["id", "zh"]) {
  if (new Set(finalTranslations.map((entry) => entry[field])).size !== finalTranslations.length) {
    throw new Error(`Duplicate final translation ${field}`);
  }
}
const finalByChinese = new Map(finalTranslations.map((entry) => [entry.zh, entry.en.trim()]));
const stillMissing = source.filter((entry) => !finalByChinese.has(entry.zh));
if (stillMissing.length) throw new Error(`Live string remains untranslated: ${stillMissing[0].zh}`);
const dictionary = Object.fromEntries(source.map((entry) => [entry.zh, finalByChinese.get(entry.zh)]));
const jsonOutput = JSON.stringify(finalTranslations, null, 2) + "\n";
const bundleOutput = `globalThis.NS_EN_TRANSLATIONS = Object.freeze(${JSON.stringify(dictionary, null, 2)});\n`;
if (checkOnly) {
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) throw new Error("R0.72T translations are stale");
  if (await readFile(bundlePath, "utf8") !== bundleOutput) throw new Error("R0.72T bundle is stale");
} else {
  await Promise.all([writeFile(translationPath, jsonOutput), writeFile(bundlePath, bundleOutput)]);
}
console.log(JSON.stringify({ checkOnly, added: translatedEntries.length, total: finalTranslations.length,
  liveStrings: source.length, missingAfter: stillMissing.length, bundle: "public/i18n-en.js" }));
