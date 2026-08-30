import { access, lstat, open, readFile, realpath, rename, unlink } from "node:fs/promises";
import { dirname, isAbsolute, relative, resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(process.env.R073K_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r073k-missing.json");
const usage = "usage: add-r073k-translations.mjs (--apply | --check-only | --capture-missing)";
const argumentsList = process.argv.slice(2);
if (argumentsList.includes("--help") || argumentsList.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
const allowedArguments = new Set(["--apply", "--check-only", "--capture-missing"]);
const unknownArguments = argumentsList.filter((argument) => !allowedArguments.has(argument));
if (unknownArguments.length) {
  throw new Error("Unknown R0.73K translation argument: " + unknownArguments[0] + "\n" + usage);
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
  "notes/r0-73k.html",
  "recap-r0-61-r0-73k.html",
  "research-review.html",
];
const discouragedChinese = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
];
const canonicalRoot = await realpath(root);

function assertInsideRoot(canonicalPath, label) {
  const offset = relative(canonicalRoot, canonicalPath);
  if (
    !offset || offset === ".." || offset.startsWith("../") ||
    offset.startsWith("..\\") || isAbsolute(offset)
  ) {
    throw new Error(label + " escaped R073K_RELEASE_ROOT: " + canonicalPath);
  }
}

async function assertSafeTarget(path, { allowMissing = false } = {}) {
  const parent = await realpath(dirname(path));
  assertInsideRoot(parent, "Translation parent");
  try {
    const info = await lstat(path);
    if (!info.isFile() || info.isSymbolicLink()) {
      throw new Error("Translation target is not a regular nonsymlink file: " + path);
    }
    const canonicalPath = await realpath(path);
    assertInsideRoot(canonicalPath, "Translation target");
    return info;
  } catch (error) {
    if (allowMissing && error?.code === "ENOENT") return null;
    throw error;
  }
}

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
    throw new Error("R0.73K translation transaction requires exactly three distinct files");
  }
  const nonce = `${process.pid}-${Date.now()}-${process.hrtime.bigint()}`;
  const entries = [];
  for (const [index, { path, payload }] of writes.entries()) {
    const info = await assertSafeTarget(path);
    entries.push({
      path,
      payload,
      mode: info.mode & 0o777,
      temporary: resolve(dirname(path), `.${path.split("/").at(-1)}.r073k-${nonce}-${index}.tmp`),
      backup: resolve(dirname(path), `.${path.split("/").at(-1)}.r073k-${nonce}-${index}.bak`),
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
      throw new AggregateError([error, ...rollbackErrors], "R0.73K translation rollback failed");
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

async function writeSingleAtomic(path, payload) {
  const info = await assertSafeTarget(path, { allowMissing: true });
  const nonce = `${process.pid}-${Date.now()}-${process.hrtime.bigint()}`;
  const temporary = resolve(dirname(path), `.${path.split("/").at(-1)}.r073k-${nonce}.tmp`);
  try {
    const handle = await open(temporary, "wx", info ? info.mode & 0o777 : 0o644);
    try {
      await handle.writeFile(payload, "utf8");
      await handle.sync();
    } finally {
      await handle.close();
    }
    await rename(temporary, path);
    await syncDirectories([path]);
  } finally {
    await removeIfPresent(temporary);
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
    "R0.73K HTML must be generated before translation snapshot/application: " +
    JSON.stringify(absentPages),
  );
}

await assertSafeTarget(translationPath);
await assertSafeTarget(bundlePath);
if (!captureMissing) await assertSafeTarget(snapshotPath);

for (const relativePage of activePages) {
  const pagePath = resolve(publicDirectory, relativePage);
  await assertSafeTarget(pagePath);
  const html = await readFile(pagePath, "utf8");
  if (!html.includes("/i18n-en.js?v=1.51")) {
    throw new Error(relativePage + ": expected i18n cache version v1.51");
  }
  for (const phrase of discouragedChinese) {
    if (html.includes(phrase)) {
      throw new Error(relativePage + ": public-voice violation " + phrase);
    }
  }
}

const translations = JSON.parse(await readFile(translationPath, "utf8"));
const retained = translations.filter((entry) => !/^r073k\d+$/.test(entry.id));
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
if (retainedByChinese.size !== retained.length) {
  throw new Error("Duplicate Chinese keys outside the R0.73K batch");
}

const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(activePages)) {
  throw new Error("Unexpected R0.73K missing-string files: " + JSON.stringify(missingFiles));
}

if (captureMissing) {
  const skeleton = missing.map(({ zh }) => ({ zh, en: "" }));
  await writeSingleAtomic(snapshotPath, JSON.stringify(skeleton, null, 2) + "\n");
  console.log(JSON.stringify({
    captured: skeleton.length,
    snapshot: "scripts/i18n-snapshots/r073k-missing.json",
  }));
  process.exit(0);
}

const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
if (!Array.isArray(snapshot) || snapshot.length === 0) {
  throw new Error("Empty R0.73K snapshot");
}
const snapshotChinese = snapshot.map((entry) => entry.zh);
const liveChinese = missing.map((entry) => entry.zh);
if (JSON.stringify(snapshotChinese) !== JSON.stringify(liveChinese)) {
  const index = liveChinese.findIndex((value, offset) => value !== snapshotChinese[offset]);
  throw new Error("R0.73K missing-string snapshot drift at row " + String(index + 1));
}
const englishByChinese = new Map(snapshot.map((entry) => [entry.zh, entry.en]));
if (englishByChinese.size !== snapshot.length) {
  throw new Error("Duplicate R0.73K snapshot keys");
}

const boundaryTokens = (value) =>
  value.match(/\b(?:FALSE_AS_INFERENCE|CONDITIONAL|INCONCLUSIVE|NOT_RUN|FAILED|CLOSED|OPEN|PASS|FALSE)\b/g) ?? [];
const machineLedgerTokens = (value) =>
  [...value.matchAll(
    /\b([A-Za-z][A-Za-z0-9]*)=([A-Z0-9][A-Z0-9_]*)\b/g,
  )].map((match) => `${match[1]}=${match[2]}`);
const accountingTokens = (value) =>
  [...value.matchAll(
    /R0\.\d+[A-Z]?|v\d+(?:\.\d+)+[A-Z]?|(?<![\p{L}\p{N}_])\d+(?:\.\d+)?(?![\p{L}\p{N}_])/gu,
  )].map((match) => match[0]);

const translatedEntries = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh)?.trim();
  if (!en || containsChinese(en)) {
    throw new Error("Invalid R0.73K English row: " + entry.zh);
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("Plural voice in R0.73K English row: " + entry.zh);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error("Protected-token mismatch for R0.73K row: " + entry.zh);
  }
  if (JSON.stringify(accountingTokens(en)) !== JSON.stringify(accountingTokens(entry.zh))) {
    throw new Error("Version/count-token mismatch for R0.73K row: " + entry.zh);
  }
  if (JSON.stringify(boundaryTokens(en)) !== JSON.stringify(boundaryTokens(entry.zh))) {
    throw new Error("Claim-state boundary drift for R0.73K row: " + entry.zh);
  }
  if (JSON.stringify(machineLedgerTokens(en)) !== JSON.stringify(machineLedgerTokens(entry.zh))) {
    throw new Error("Machine-ledger sequence drift for R0.73K row: " + entry.zh);
  }
  return { ...entry, id: "r073k" + String(index + 1).padStart(3, "0"), en };
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
    throw new Error("R0.73K snapshot is stale");
  }
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.73K translations are stale");
  }
  if (await readFile(bundlePath, "utf8") !== bundleOutput) {
    throw new Error("R0.73K bundle is stale");
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
  snapshot: "scripts/i18n-snapshots/r073k-missing.json",
  bundle: "public/i18n-en.js",
}));
