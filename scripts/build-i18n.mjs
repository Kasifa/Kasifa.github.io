import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
  listSiteHtmlFiles,
} from "./i18n-lib.mjs";

const projectRoot = resolve(import.meta.dirname, "..");
const publicDirectory = resolve(projectRoot, "public");
const allowPartial = process.argv.includes("--allow-partial");
const inputArgument = process.argv.slice(2).find((argument) => !argument.startsWith("--"));
const input = resolve(
  inputArgument ?? resolve(projectRoot, "translations", "en.json"),
);
const output = resolve(publicDirectory, "i18n-en.js");
const translations = JSON.parse(await readFile(input, "utf8"));
const source = await collectSiteStrings(publicDirectory);
const sourceByChinese = new Map(source.map((item) => [item.zh, item]));
const translationByChinese = new Map(
  translations.map((item) => [item.zh, item.en.trim()]),
);

const missing = source.filter((item) => !translationByChinese.has(item.zh));
const stale = translations.filter((item) => !sourceByChinese.has(item.zh));
const invalid = translations.filter(
  (item) =>
    !item.en?.trim() ||
    containsChinese(item.en) ||
    JSON.stringify(extractProtectedTokens(item.zh)) !==
      JSON.stringify(extractProtectedTokens(item.en)),
);

if ((!allowPartial && missing.length) || invalid.length) {
  console.error(
    JSON.stringify(
      {
        missing: missing.slice(0, 10).map((item) => item.zh),
        missingCount: missing.length,
        invalid: invalid.slice(0, 10).map((item) => item.id),
        invalidCount: invalid.length,
      },
      null,
      2,
    ),
  );
  process.exitCode = 1;
  process.exit();
}

const dictionary = Object.fromEntries(
  source
    .filter((item) => translationByChinese.has(item.zh))
    .map((item) => [item.zh, translationByChinese.get(item.zh)]),
);
await writeFile(
  output,
  `globalThis.NS_EN_TRANSLATIONS = Object.freeze(${JSON.stringify(dictionary, null, 2)});\n`,
);

const htmlFiles = await listSiteHtmlFiles(publicDirectory);
const mathJaxScript =
  '  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>';
const assets = [
  '  <link rel="stylesheet" href="/bilingual.css">',
  '  <script defer src="/i18n-en.js"></script>',
  '  <script defer src="/bilingual.js"></script>',
].join("\n");

for (const file of htmlFiles) {
  let html = await readFile(file, "utf8");
  if (!html.includes('/bilingual.js')) {
    if (!html.includes(mathJaxScript)) {
      throw new Error(`MathJax insertion point not found in ${file}`);
    }
    html = html.replace(mathJaxScript, `${assets}\n${mathJaxScript}`);
    await writeFile(file, html);
  }
}

console.log(
  JSON.stringify(
    {
      pages: htmlFiles.length,
      translations: source.length,
      staleTranslations: stale.length,
      output,
    },
    null,
    2,
  ),
);
