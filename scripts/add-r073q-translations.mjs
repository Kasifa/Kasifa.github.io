#!/usr/bin/env node

// R0.73Q translation stage. Full-sentence translations are reviewed and
// written directly on the local workstation from the missing-string snapshot.
// This script has no network client, calls no translation service, and never
// invokes DGX. The bilingual dictionary fixes terms and claim-state boundaries.

import { lstat, open, readFile, rename, unlink } from "node:fs/promises";
import { dirname, relative, resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const usage = "usage: add-r073q-translations.mjs (--apply | --check-only | --capture-missing)";
const argumentsList = process.argv.slice(2);
if (argumentsList.includes("--help") || argumentsList.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
if (argumentsList.length !== 1 || !["--apply", "--check-only", "--capture-missing"].includes(argumentsList[0])) {
  throw new Error(usage);
}

const root = resolve(process.env.R073Q_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r073q-missing.json");
const dictionaryPath = resolve(root, "research/r073q_bilingual_dictionary.md");
const action = argumentsList[0];
const translationMethod = "reviewed-local-direct-no-dgx-no-network";
const activePages = [
  "literature-review.html",
  "notes/index.html",
  "notes/r0-73q.html",
  "recap-r0-61-r0-73q.html",
  "research-review.html",
];
const discouragedChinese = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  "颠覆性", "世界首个", "接近解决", "解决了千禧年", "证明了全局正则性",
  "原创性定理", "首次证明",
];
const requiredDictionaryTokens = [
  "periodicOseenHLS=CLOSED_AFTER_AUDIT",
  "linearizedVolterraInverse=CLOSED_AFTER_AUDIT",
  "uniformAllRestartRadius=CLOSED_AFTER_AUDIT",
  "periodicHeatFlowTube=CLOSED_AFTER_AUDIT",
  "strictExtensionByUnion=CLOSED",
  "heatFlowBallContainsEntirePublishedH12Ball=NOT_PROVED",
  "bareKatoSupFromL4L6=BLOCKED_BY_ENDPOINT",
  "fullKochTataruTheory=NOT_REFUTED",
  "uniformL2Only=OPEN",
  "nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL",
  "arbitraryThreeDimensionalGlobalRegularity=OPEN",
  "formulaDiagnosticValidation=PASS",
  "formulaDiagnosticPackage=CLOSED",
  "sourceCommitAssigned=TRUE",
  "finalSeal=TRUE",
  "formalFigurePackage=PASS",
  "publicReleaseContent=READY",
  "noveltyOrPriorityClaim=FORBIDDEN",
];

async function regularText(path, label, { allowMissing = false } = {}) {
  try {
    const info = await lstat(path);
    if (!info.isFile() || info.isSymbolicLink()) {
      throw new Error(label + ": expected a regular nonsymlink file");
    }
    const value = await readFile(path, "utf8");
    if (/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(value)) {
      throw new Error(label + ": control character");
    }
    return value;
  } catch (error) {
    if (allowMissing && error?.code === "ENOENT") return null;
    throw error;
  }
}

function assertInsideRoot(path, label) {
  const offset = relative(root, path);
  if (!offset || offset === ".." || offset.startsWith("../") || offset.startsWith("..\\")) {
    throw new Error(label + " escaped R073Q_RELEASE_ROOT");
  }
}

async function safeAtomicWrite(path, payload) {
  assertInsideRoot(path, "translation target");
  const parentInfo = await lstat(dirname(path));
  if (!parentInfo.isDirectory() || parentInfo.isSymbolicLink()) {
    throw new Error("unsafe translation parent: " + dirname(path));
  }
  const temporary = resolve(
    dirname(path),
    `.${path.split("/").at(-1)}.r073q-${process.pid}-${Date.now()}-${process.hrtime.bigint()}.tmp`,
  );
  try {
    const handle = await open(temporary, "wx", 0o644);
    try {
      await handle.writeFile(payload, "utf8");
      await handle.sync();
    } finally {
      await handle.close();
    }
    await rename(temporary, path);
  } finally {
    try {
      await unlink(temporary);
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
    }
  }
}

async function writeTransaction(writes) {
  if (writes.length !== 3 || new Set(writes.map(({ path }) => path)).size !== 3) {
    throw new Error("R0.73Q translation transaction requires three distinct files");
  }
  const nonce = `${process.pid}-${Date.now()}-${process.hrtime.bigint()}`;
  const rows = writes.map(({ path, payload }, index) => ({
    path,
    payload,
    temporary: resolve(dirname(path), `.${path.split("/").at(-1)}.r073q-${nonce}-${index}.tmp`),
    backup: resolve(dirname(path), `.${path.split("/").at(-1)}.r073q-${nonce}-${index}.bak`),
    backedUp: false,
    installed: false,
  }));
  try {
    for (const row of rows) {
      assertInsideRoot(row.path, "translation target");
      const current = await lstat(row.path);
      if (!current.isFile() || current.isSymbolicLink()) {
        throw new Error("unsafe translation target: " + row.path);
      }
      const handle = await open(row.temporary, "wx", current.mode & 0o777);
      try {
        await handle.writeFile(row.payload, "utf8");
        await handle.sync();
      } finally {
        await handle.close();
      }
    }
    for (const row of rows) {
      await rename(row.path, row.backup);
      row.backedUp = true;
    }
    for (const row of rows) {
      await rename(row.temporary, row.path);
      row.installed = true;
    }
  } catch (error) {
    for (const row of [...rows].reverse()) {
      try {
        if (row.installed) await unlink(row.path);
        if (row.backedUp) await rename(row.backup, row.path);
      } catch {
        // Preserve the original failure; backup files remain for recovery.
      }
    }
    throw error;
  } finally {
    for (const row of rows) {
      try {
        await unlink(row.temporary);
      } catch (error) {
        if (error?.code !== "ENOENT") throw error;
      }
      if (row.installed) {
        try {
          await unlink(row.backup);
        } catch (error) {
          if (error?.code !== "ENOENT") throw error;
        }
      }
    }
  }
}

const dictionary = await regularText(dictionaryPath, "R0.73Q bilingual dictionary");
const metadataField = (label) => dictionary.match(
  new RegExp(`^\\*\\*${label}:\\*\\*\\s*(.+?)(?=\\n\\s*\\n)`, "ms"),
)?.[1]?.replace(/\s+/g, " ").replace(/^\*|\*$/g, "").trim();
const releaseTitle = metadataField("Release title");
if (releaseTitle !== "R0.73Q | A critical heat-flow tube beyond the \\(H^{1/2}\\) entrance") {
  throw new Error("R0.73Q bilingual dictionary release title drift");
}
for (const token of requiredDictionaryTokens) {
  if (!dictionary.includes(token)) throw new Error("R0.73Q dictionary missing " + token);
}
if (dictionary.includes("formulaDiagnosticValidation=PRESEAL_PENDING") ||
    dictionary.includes("formulaDiagnosticPackage=PRESEAL_PENDING") ||
    /\bpublicRelease=/.test(dictionary)) {
  throw new Error("R0.73Q dictionary still carries prepublication provenance");
}
if (!/^\*\*Next release:\*\*\s*R0\.73R\s*$/m.test(dictionary)) {
  throw new Error("R0.73Q dictionary next-release gate is not frozen to R0.73R");
}

const releaseManifest = JSON.parse(await regularText(
  resolve(root, "research/release-manifest.json"), "release manifest",
));
const siteVersion = JSON.parse(await regularText(
  resolve(publicDirectory, "site-version.json"), "site version",
));
if (
  releaseManifest.latestCompletedRelease !== "r073q" ||
  releaseManifest.siteVersion !== "1.57" ||
  releaseManifest.nextRelease !== "r073r" ||
  siteVersion.latestRelease !== "R0.73Q" ||
  siteVersion.version !== "1.57"
) {
  throw new Error("R0.73Q HTML/accounting apply must precede translation work");
}

for (const relativePage of activePages) {
  const html = await regularText(resolve(publicDirectory, relativePage), relativePage);
  if (!html.includes("/i18n-en.js?v=1.57")) {
    throw new Error(relativePage + ": expected i18n cache version v1.57");
  }
  if (!html.includes("R0.73Q")) throw new Error(relativePage + ": R0.73Q marker absent");
  for (const phrase of discouragedChinese) {
    if (html.includes(phrase)) throw new Error(relativePage + ": public-voice violation " + phrase);
  }
}

const translations = JSON.parse(await regularText(translationPath, "translations/en.json"));
if (!Array.isArray(translations)) throw new Error("translations/en.json is not an array");
const retained = translations.filter((entry) => !/^r073q\d+$/.test(entry.id));
if (new Set(retained.map((entry) => entry.zh)).size !== retained.length) {
  throw new Error("duplicate Chinese key outside R0.73Q translation batch");
}
const retainedByChinese = new Map(retained.map((entry) => [entry.zh, entry]));
const source = await collectSiteStrings(publicDirectory);
const missing = source.filter((entry) => !retainedByChinese.has(entry.zh));
const missingFiles = [...new Set(missing.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(missingFiles) !== JSON.stringify(activePages)) {
  throw new Error("unexpected R0.73Q missing-string files: " + JSON.stringify(missingFiles));
}

if (action === "--capture-missing") {
  const skeleton = missing.map(({ zh }) => ({ zh, en: "" }));
  await safeAtomicWrite(snapshotPath, JSON.stringify(skeleton, null, 2) + "\n");
  console.log(JSON.stringify({ captured: skeleton.length, snapshot: "scripts/i18n-snapshots/r073q-missing.json" }));
  process.exit(0);
}

const snapshot = JSON.parse(await regularText(snapshotPath, "R0.73Q translation snapshot"));
if (!Array.isArray(snapshot) || snapshot.length === 0) throw new Error("empty R0.73Q snapshot");
if (JSON.stringify(snapshot.map(({ zh }) => zh)) !== JSON.stringify(missing.map(({ zh }) => zh))) {
  throw new Error("R0.73Q missing-string snapshot drift");
}
const englishByChinese = new Map(snapshot.map(({ zh, en }) => [zh, en]));
if (englishByChinese.size !== snapshot.length) throw new Error("duplicate R0.73Q snapshot key");

const boundaryTokens = (value) =>
  value.match(/NOT CLAY|\b(?:VALIDATED_SEALED|CLOSED_AS_COROLLARY|FALSE_AS_INFERENCE|PENDING|CLOSED|OPEN|PASS|FALSE|TRUE)\b/g) ?? [];
const machineTokens = (value) =>
  [...value.matchAll(/\b([A-Za-z][A-Za-z0-9]*)=([A-Z0-9][A-Z0-9_]*)\b/g)].map((match) => match[0]);
const accountingTokens = (value) =>
  [...value.matchAll(/R0\.\d+[A-Z]?|v\d+(?:\.\d+)+[A-Z]?|(?<![\p{L}\p{N}_])\d+(?:\.\d+)?(?![\p{L}\p{N}_])/gu)].map((match) => match[0]);

const translated = missing.map((entry, index) => {
  const en = englishByChinese.get(entry.zh)?.trim();
  if (!en || containsChinese(en)) throw new Error("invalid R0.73Q English row: " + entry.zh);
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    throw new Error("collective English voice in R0.73Q row: " + entry.zh);
  }
  if (JSON.stringify(extractProtectedTokens(en)) !== JSON.stringify(extractProtectedTokens(entry.zh))) {
    throw new Error("protected-token mismatch for R0.73Q row: " + entry.zh);
  }
  if (JSON.stringify(accountingTokens(en)) !== JSON.stringify(accountingTokens(entry.zh))) {
    throw new Error("version/count-token mismatch for R0.73Q row: " + entry.zh);
  }
  if (JSON.stringify(boundaryTokens(en)) !== JSON.stringify(boundaryTokens(entry.zh))) {
    throw new Error("claim-state boundary drift for R0.73Q row: " + entry.zh);
  }
  if (JSON.stringify(machineTokens(en)) !== JSON.stringify(machineTokens(entry.zh))) {
    throw new Error("machine-ledger drift for R0.73Q row: " + entry.zh);
  }
  return { ...entry, id: "r073q" + String(index + 1).padStart(3, "0"), en };
});

const finalTranslations = [...retained, ...translated];
if (new Set(finalTranslations.map(({ id }) => id)).size !== finalTranslations.length) {
  throw new Error("duplicate final translation id");
}
const finalByChinese = new Map(finalTranslations.map(({ zh, en }) => [zh, en.trim()]));
const stillMissing = source.filter((entry) => !finalByChinese.has(entry.zh));
if (stillMissing.length) throw new Error("live string remains untranslated: " + stillMissing[0].zh);
const liveDictionary = Object.fromEntries(source.map((entry) => [entry.zh, finalByChinese.get(entry.zh)]));
const snapshotOutput = JSON.stringify(missing.map(({ zh }) => ({ zh, en: englishByChinese.get(zh).trim() })), null, 2) + "\n";
const translationOutput = JSON.stringify(finalTranslations, null, 2) + "\n";
const bundleOutput = "globalThis.NS_EN_TRANSLATIONS = Object.freeze(" + JSON.stringify(liveDictionary, null, 2) + ");\n";

if (action === "--check-only") {
  if (await regularText(snapshotPath, "R0.73Q translation snapshot") !== snapshotOutput) {
    throw new Error("R0.73Q translation snapshot is stale");
  }
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.73Q translations are stale");
  }
  if (await regularText(bundlePath, "public/i18n-en.js") !== bundleOutput) {
    throw new Error("R0.73Q translation bundle is stale");
  }
} else {
  await writeTransaction([
    { path: translationPath, payload: translationOutput },
    { path: bundlePath, payload: bundleOutput },
    { path: snapshotPath, payload: snapshotOutput },
  ]);
}

console.log(JSON.stringify({
  checkOnly: action === "--check-only",
  applied: action === "--apply",
  added: translated.length,
  total: finalTranslations.length,
  liveStrings: source.length,
  missingAfter: stillMissing.length,
  snapshot: "scripts/i18n-snapshots/r073q-missing.json",
  bundle: "public/i18n-en.js",
  translationMethod,
}));
