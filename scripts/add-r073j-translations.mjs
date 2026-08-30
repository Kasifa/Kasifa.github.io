import { access, open, readFile, rename, stat, unlink, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(process.env.R073J_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r073j-missing.json");
const usage = "usage: add-r073j-translations.mjs (--apply | --check-only | --capture-missing)";
const argumentsList = process.argv.slice(2);
if (argumentsList.includes("--help") || argumentsList.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
const allowedArguments = new Set(["--apply", "--check-only", "--capture-missing"]);
const unknownArguments = argumentsList.filter((argument) => !allowedArguments.has(argument));
if (unknownArguments.length) {
  throw new Error("Unknown R0.73J translation argument: " + unknownArguments[0] + "\n" + usage);
}
const selectedActions = argumentsList.filter((argument) => allowedArguments.has(argument));
if (selectedActions.length !== 1 || new Set(selectedActions).size !== 1) {
  console.log(usage);
  process.exit(selectedActions.length === 0 ? 0 : 2);
}
const apply = selectedActions[0] === "--apply";
const checkOnly = selectedActions[0] === "--check-only";
const captureMissing = selectedActions[0] === "--capture-missing";
const activePages = [
  "literature-review.html",
  "notes/index.html",
  "notes/r0-73j.html",
  "recap-r0-61-r0-73j.html",
  "research-review.html",
];
const discouragedChinese = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
];

async function exists(path) {
  try {
    await access(path);
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
}

async function removeIfPresent(path) {
  try {
    await unlink(path);
  } catch (error) {
    if (error?.code !== "ENOENT") throw error;
  }
}

async function syncDirectories(paths) {
  for (const directory of [...new Set(paths.map((path) => dirname(path)))]) {
    const handle = await open(directory, "r");
    try {
      await handle.sync();
    } finally {
      await handle.close();
    }
  }
}

async function writeTranslationTransaction(writes) {
  if (writes.length !== 3 || new Set(writes.map(({ path }) => path)).size !== 3) {
    throw new Error("R0.73J translation transaction requires exactly three distinct files");
  }
  const nonce = `${process.pid}-${Date.now()}-${process.hrtime.bigint()}`;
  const entries = [];
  for (const [index, { path, payload }] of writes.entries()) {
    const info = await stat(path);
    if (!info.isFile()) throw new Error("Translation target is not a regular file: " + path);
    entries.push({
      path,
      payload,
      mode: info.mode & 0o777,
      temporary: resolve(dirname(path), `.${path.split("/").at(-1)}.r073j-${nonce}-${index}.tmp`),
      backup: resolve(dirname(path), `.${path.split("/").at(-1)}.r073j-${nonce}-${index}.bak`),
      backedUp: false,
      installed: false,
    });
  }
  let committed = false;
  try {
    for (const entry of entries) {
      const handle = await open(entry.temporary, "wx", entry.mode);
      try {
        await handle.writeFile(entry.payload, "utf8");
        await handle.sync();
      } finally {
        await handle.close();
      }
    }
    for (const entry of entries) {
      await rename(entry.path, entry.backup);
      entry.backedUp = true;
    }
    for (const entry of entries) {
      await rename(entry.temporary, entry.path);
      entry.installed = true;
    }
    await syncDirectories(entries.map(({ path }) => path));
    committed = true;
  } catch (error) {
    const rollbackErrors = [];
    for (const entry of [...entries].reverse()) {
      try {
        if (entry.installed) await removeIfPresent(entry.path);
        if (entry.backedUp) await rename(entry.backup, entry.path);
      } catch (rollbackError) {
        rollbackErrors.push(rollbackError);
      }
    }
    try {
      await syncDirectories(entries.map(({ path }) => path));
    } catch (rollbackError) {
      rollbackErrors.push(rollbackError);
    }
    if (rollbackErrors.length) {
      throw new AggregateError([error, ...rollbackErrors], "R0.73J translation rollback failed");
    }
    throw error;
  } finally {
    for (const entry of entries) await removeIfPresent(entry.temporary);
    if (committed) {
      for (const entry of entries) await removeIfPresent(entry.backup);
      await syncDirectories(entries.map(({ path }) => path));
    }
  }
}

const pagePresence = await Promise.all(
  activePages.map(async (relativePage) => ({
    relativePage,
    present: await exists(resolve(publicDirectory, relativePage)),
  })),
);
const absentPages = pagePresence
  .filter(({ present }) => !present)
  .map(({ relativePage }) => relativePage);
if (absentPages.length) {
  throw new Error(
    "R0.73J HTML must be generated before translation snapshot/application: " +
    JSON.stringify(absentPages),
  );
}

for (const relativePage of activePages) {
  const html = await readFile(resolve(publicDirectory, relativePage), "utf8");
  if (!html.includes("/i18n-en.js?v=1.50")) {
    throw new Error(relativePage + ": expected i18n cache version v1.50");
  }
  for (const phrase of discouragedChinese) {
    if (html.includes(phrase)) {
      throw new Error(relativePage + ": public-voice violation " + phrase);
    }
  }
}

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r073j\d+$/.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.73J batch");
}

const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(activePages)) {
  throw new Error("Unexpected R0.73J missing-string files: " + JSON.stringify(missingFiles));
}

if (captureMissing) {
  const skeleton = missing.map(({ zh }) => ({ zh, en: "" }));
  await writeFile(snapshotPath, JSON.stringify(skeleton, null, 2) + "\n");
  console.log(JSON.stringify({
    captured: skeleton.length,
    snapshot: "scripts/i18n-snapshots/r073j-missing.json",
  }));
  process.exit(0);
}

const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
if (!Array.isArray(snapshot) || snapshot.length === 0) {
  throw new Error("Empty R0.73J snapshot");
}
const snapshotChinese = snapshot.map((entry) => entry.zh);
const liveChinese = missing.map((entry) => entry.zh);
if (JSON.stringify(snapshotChinese) !== JSON.stringify(liveChinese)) {
  const index = liveChinese.findIndex((value, offset) => value !== snapshotChinese[offset]);
  throw new Error("R0.73J missing-string snapshot drift at row " + String(index + 1));
}
const englishByChinese = new Map(snapshot.map((entry) => [entry.zh, entry.en]));
if (englishByChinese.size !== snapshot.length) {
  throw new Error("Duplicate R0.73J snapshot keys");
}

const boundaryTokens = (value) =>
  value.match(/\b(?:FALSE_AS_INFERENCE|CONDITIONAL|INCONCLUSIVE|NOT_RUN|FAILED|CLOSED|OPEN|PASS|FALSE)\b/g) ?? [];
const machineLedgerTokens = (value) =>
  [...value.matchAll(
    /\b([A-Za-z][A-Za-z0-9]*)=([A-Z][A-Z0-9_]*)\b/g,
  )].map((match) => `${match[1]}=${match[2]}`);
const accountingTokens = (value) =>
  [...value.matchAll(
    /R0\.\d+[A-Z]?|v\d+(?:\.\d+)+[A-Z]?|(?<![\p{L}\p{N}_])\d+(?:\.\d+)?(?![\p{L}\p{N}_])/gu,
  )].map((match) => match[0]);

const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh)?.trim();
  if (!en || containsChinese(en)) {
    throw new Error("Invalid R0.73J English row: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Plural voice in R0.73J English row: " + entry.zh);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error("Protected-token mismatch for R0.73J row: " + entry.zh);
  }
  if (JSON.stringify(accountingTokens(en)) !== JSON.stringify(accountingTokens(entry.zh))) {
    throw new Error("Version/count-token mismatch for R0.73J row: " + entry.zh);
  }
  if (JSON.stringify(boundaryTokens(en)) !== JSON.stringify(boundaryTokens(entry.zh))) {
    throw new Error("Claim-state boundary drift for R0.73J row: " + entry.zh);
  }
  if (JSON.stringify(machineLedgerTokens(en)) !== JSON.stringify(machineLedgerTokens(entry.zh))) {
    throw new Error("Machine-ledger sequence drift for R0.73J row: " + entry.zh);
  }
  return { ...entry, id: "r073j" + String(index + 1).padStart(3, "0"), en };
});

const normalizedSnapshot = missing.map((entry) => ({
  zh: entry.zh,
  en: englishByChinese.get(entry.zh).trim(),
}));
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
const dictionary = Object.fromEntries(source.map((entry) => [entry.zh, finalByChinese.get(entry.zh)]));
const snapshotOutput = JSON.stringify(normalizedSnapshot, null, 2) + "\n";
const jsonOutput = JSON.stringify(finalTranslations, null, 2) + "\n";
const bundleOutput =
  "globalThis.NS_EN_TRANSLATIONS = Object.freeze(" +
  JSON.stringify(dictionary, null, 2) +
  ");\n";

if (checkOnly) {
  if (await readFile(snapshotPath, "utf8") !== snapshotOutput) {
    throw new Error("R0.73J snapshot is stale");
  }
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.73J translations are stale");
  }
  if (await readFile(bundlePath, "utf8") !== bundleOutput) {
    throw new Error("R0.73J bundle is stale");
  }
} else if (apply) {
  await writeTranslationTransaction([
    { path: translationPath, payload: jsonOutput },
    { path: bundlePath, payload: bundleOutput },
    { path: snapshotPath, payload: snapshotOutput },
  ]);
}
console.log(JSON.stringify({
  checkOnly,
  applied: apply,
  added: translatedEntries.length,
  total: finalTranslations.length,
  liveStrings: source.length,
  missingAfter: stillMissing.length,
  snapshot: "scripts/i18n-snapshots/r073j-missing.json",
  bundle: "public/i18n-en.js",
}));
