import { execFile } from "node:child_process";
import { access, open, readFile, rename, stat, unlink, writeFile } from "node:fs/promises";
import { dirname, relative, resolve } from "node:path";
import { promisify } from "node:util";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
  extractTranslatableStrings,
  listSiteHtmlFiles,
} from "./i18n-lib.mjs";

const run = promisify(execFile);
const root = resolve(process.env.R073H_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r073h-missing.json");
const usage = "usage: add-r073h-translations.mjs (--apply | --check-only | --capture-missing)";
const argumentsList = process.argv.slice(2);
if (argumentsList.includes("--help") || argumentsList.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
const allowedArguments = new Set(["--apply", "--check-only", "--capture-missing"]);
const unknownArguments = argumentsList.filter((argument) => !allowedArguments.has(argument));
if (unknownArguments.length) {
  throw new Error("Unknown R0.73H translation argument: " + unknownArguments[0] + "\n" + usage);
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
  "notes/r0-73h.html",
  "recap-r0-61-r0-73h.html",
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
  if (writes.length !== 2 || new Set(writes.map(({ path }) => path)).size !== 2) {
    throw new Error("R0.73H translation transaction requires exactly two distinct files");
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
      temporary: resolve(dirname(path), `.${path.split("/").at(-1)}.r073h-${nonce}-${index}.tmp`),
      backup: resolve(dirname(path), `.${path.split("/").at(-1)}.r073h-${nonce}-${index}.bak`),
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
      throw new AggregateError([error, ...rollbackErrors], "R0.73H translation rollback failed");
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

function sortedEntries(entries) {
  return [...entries.values()].sort((left, right) =>
    left.files[0].localeCompare(right.files[0], undefined, { numeric: true }) ||
    left.zh.localeCompare(right.zh, "zh-CN"),
  );
}

function mergeHtml(entries, html, file) {
  for (const zh of extractTranslatableStrings(html)) {
    const entry = entries.get(zh) ?? { zh, count: 0, files: [] };
    entry.count += 1;
    if (!entry.files.includes(file)) entry.files.push(file);
    entries.set(zh, entry);
  }
}

async function collectPlannedSiteStrings() {
  const entries = new Map();
  const replaced = new Set([
    "literature-review.html", "notes/index.html", "research-review.html",
  ]);
  for (const file of await listSiteHtmlFiles(publicDirectory)) {
    const name = relative(publicDirectory, file);
    if (replaced.has(name)) continue;
    mergeHtml(entries, await readFile(file, "utf8"), name);
  }
  const probe = [
    "import json, sys",
    "sys.path.insert(0, 'scripts')",
    "import generate_r073h_release as release",
    "site = release.build_manifest_outputs()[release.PUBLIC / 'site-version.json']",
    "pages = {",
    "  'literature-review.html': release.update_literature(),",
    "  'notes/index.html': release.build_note_index(site),",
    "  'notes/r0-73h.html': release.build_note(),",
    "  'recap-r0-61-r0-73h.html': release.build_recap(),",
    "  'research-review.html': release.update_home(),",
    "}",
    "print(json.dumps(pages, ensure_ascii=False))",
  ].join("\n");
  const { stdout } = await run("python3", ["-c", probe], {
    cwd: root, maxBuffer: 64 * 1024 * 1024,
  });
  const planned = JSON.parse(stdout);
  for (const file of activePages) mergeHtml(entries, planned[file], file);
  return sortedEntries(entries);
}

const materialized = await exists(resolve(publicDirectory, "notes/r0-73h.html"));
const source = materialized
  ? await collectSiteStrings(publicDirectory)
  : await collectPlannedSiteStrings();
if (materialized) {
  for (const relativePage of activePages) {
    const html = await readFile(resolve(publicDirectory, relativePage), "utf8");
    if (!html.includes("/i18n-en.js?v=1.48")) {
      throw new Error(relativePage + ": expected i18n cache version v1.48");
    }
    for (const phrase of discouragedChinese) {
      if (html.includes(phrase)) {
        throw new Error(relativePage + ": public-voice violation " + phrase);
      }
    }
  }
}

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r073h\d+$/.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.73H batch");
}
const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(activePages)) {
  throw new Error("Unexpected R0.73H missing-string files: " + JSON.stringify(missingFiles));
}

if (captureMissing) {
  const skeleton = missing.map(({ zh }) => ({ zh, en: "" }));
  await writeFile(snapshotPath, JSON.stringify(skeleton, null, 2) + "\n");
  console.log(JSON.stringify({
    captured: skeleton.length,
    materialized,
    snapshot: "scripts/i18n-snapshots/r073h-missing.json",
  }));
  process.exit(0);
}

const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
if (!Array.isArray(snapshot) || snapshot.length === 0) {
  throw new Error("Empty R0.73H snapshot");
}
const snapshotChinese = snapshot.map((entry) => entry.zh);
const liveChinese = missing.map((entry) => entry.zh);
if (JSON.stringify(snapshotChinese) !== JSON.stringify(liveChinese)) {
  const index = liveChinese.findIndex((value, offset) => value !== snapshotChinese[offset]);
  throw new Error("R0.73H missing-string snapshot drift at row " + String(index + 1));
}
const englishByChinese = new Map(snapshot.map((entry) => [entry.zh, entry.en]));
if (englishByChinese.size !== snapshot.length) {
  throw new Error("Duplicate R0.73H snapshot keys");
}

const boundaryTokens = (value) =>
  value.match(/\b(?:FALSE_AS_INFERENCE|CONDITIONAL|CLOSED|OPEN|FALSE)\b/g) ?? [];
const claimKeyTokens = (value) =>
  value.match(/\b[A-Za-z][A-Za-z0-9]*(?==(?:FALSE_AS_INFERENCE|CLOSED|OPEN|FALSE)\b)/g) ?? [];
const accountingTokens = (value) =>
  [...value.matchAll(
    /R0\.\d+[A-Z]?|v\d+(?:\.\d+)+[A-Z]?|(?<![\p{L}\p{N}_])\d+(?:\.\d+)?(?![\p{L}\p{N}_])/gu,
  )].map((match) => match[0]);

const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh)?.trim();
  if (!en || containsChinese(en)) {
    throw new Error("Invalid R0.73H English row: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Plural voice in R0.73H English row: " + entry.zh);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error("Protected-token mismatch for R0.73H row: " + entry.zh);
  }
  if (JSON.stringify(accountingTokens(en)) !== JSON.stringify(accountingTokens(entry.zh))) {
    throw new Error("Version/count-token mismatch for R0.73H row: " + entry.zh);
  }
  if (JSON.stringify(boundaryTokens(en)) !== JSON.stringify(boundaryTokens(entry.zh))) {
    throw new Error("Claim-state boundary drift for R0.73H row: " + entry.zh);
  }
  if (JSON.stringify(claimKeyTokens(en)) !== JSON.stringify(claimKeyTokens(entry.zh))) {
    throw new Error("Claim-key sequence drift for R0.73H row: " + entry.zh);
  }
  return { ...entry, id: "r073h" + String(index + 1).padStart(3, "0"), en };
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
const dictionary = Object.fromEntries(source.map((entry) => [entry.zh, finalByChinese.get(entry.zh)]));
const jsonOutput = JSON.stringify(finalTranslations, null, 2) + "\n";
const bundleOutput =
  "globalThis.NS_EN_TRANSLATIONS = Object.freeze(" +
  JSON.stringify(dictionary, null, 2) +
  ");\n";

if (checkOnly) {
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.73H translations are stale");
  }
  if (await readFile(bundlePath, "utf8") !== bundleOutput) {
    throw new Error("R0.73H bundle is stale");
  }
} else {
  await writeTranslationTransaction([
    { path: translationPath, payload: jsonOutput },
    { path: bundlePath, payload: bundleOutput },
  ]);
}
console.log(JSON.stringify({
  checkOnly, materialized, added: translatedEntries.length,
  total: finalTranslations.length, liveStrings: source.length,
  missingAfter: stillMissing.length, bundle: "public/i18n-en.js",
}));
