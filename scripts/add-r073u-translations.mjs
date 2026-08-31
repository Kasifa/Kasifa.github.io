#!/usr/bin/env node

// R0.73U translation stage. English copy is accepted only from the local
// direct-review snapshot produced after --capture-missing. Ordinary translation
// is LOCAL_DIRECT_NO_DGX: this module imports no process/network client, calls
// no translation service, and never invokes DGX.

import { createHash } from "node:crypto";
import { lstat, open, readFile, rename, unlink } from "node:fs/promises";
import { dirname, relative, resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
  listSiteHtmlFiles,
} from "./i18n-lib.mjs";

const usage = "usage: add-r073u-translations.mjs (--apply | --check-only | --capture-missing)";
const argumentsList = process.argv.slice(2);
if (argumentsList.includes("--help") || argumentsList.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
if (argumentsList.length !== 1 || !["--apply", "--check-only", "--capture-missing"].includes(argumentsList[0])) {
  throw new Error(usage);
}

const root = resolve(process.env.R073U_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r073u-missing.json");
const dictionaryPath = resolve(root, "research/r073u_bilingual_dictionary.md");
const reportPath = resolve(root, "research/r073u_report-source.md");
const action = argumentsList[0];
const translationRoute = "LOCAL_DIRECT_NO_DGX";
const translationMethod = "reviewed-local-direct-no-dgx-no-network";
const localDirectProvenance = "local-direct-reviewed";
const forcedSemanticReviewLedger = new Map([
  ["s1812", {
    zhSha256: "ec8cabcdbd73652c18e7723b2af7442aedb561b2401d706f0d36d56cfd1f258e",
    capturedEnSha256: "72f34d35ca0e192c02223ab27c24822ad97e6071f687baac3da7dfd8c28bd236",
  }],
  ["s1824", {
    zhSha256: "c64d1cbb0d0b21dedcf75e8b1a333e07e9a4e847ed7e672acbc8aab77a0dd891",
    capturedEnSha256: "507c78ff71eb0847e73e735bf6d7decafd0efa293fc9038e10e9d3c1976d109a",
  }],
  ["s2429", {
    zhSha256: "a3ab0dedb06f246cd9a9b6186a0f3ec23109af26918e746988c9eea0ec6b47a4",
    capturedEnSha256: "2ba8182f49721cc3825c11acc6f56c0d01ec5ac3095019ccabf018ccc198a78f",
  }],
]);
const forcedSemanticReviewIds = new Set(forcedSemanticReviewLedger.keys());

// These are reviewed, historical semantic equivalences—not a general escape
// hatch for numeric mismatches. Approval is accepted only when the live row's
// ID, Chinese source, captured English, and fixed note all match this ledger.
const semanticEquivalenceLedger = new Map([
  ["s3091", {
    zhSha256: "46a8b147da448e5027ce492912c427815b13a9a95e7b519f3ef2eef037a46c41",
    enSha256: "45cbfcaeeb08f233541c09b95e815110019cfb43513c60ea2d3145109af4285a",
    reviewNote: "Degree 296 is the last term checked, exactly equivalent to no checks from degree 297 onward.",
  }],
  ["s3573", {
    zhSha256: "a6238ef19746f7fd7fe19a907b9dee19385d4f192b1c5ff743fe6a83bb58de5b",
    enSha256: "788ddd00a3cfa3443cadcadb2b3f20bd6b9b60676e90d8cce389b5e90b0ccf74",
    reviewNote: "Vanishing below degree 41 is exactly the same integer-degree range as vanishing through degree 40.",
  }],
  ["s5412", {
    zhSha256: "9cf2603078f5f034fd3a7bff30b1d1beafc3dcee5b643088784abc50fe0eac7c",
    enSha256: "f9a2cbe3dddcc2a91e4964e70e8ec9f609a09431b1d8026e3c55bd8ebff852fc",
    reviewNote: "Chinese 20 wan pairs equals 200,000 pairs.",
  }],
  ["s5753", {
    zhSha256: "f5a65e76a95aef3bff205e9e91936da9b4b238779b35172bd370d06b6b90398b",
    enSha256: "57e913b6e5b7a2a863ca8ec4d909b048dc2eec41538e27290df467a32da502b2",
    reviewNote: "Chinese 74.95 yi paths equals 7.495 billion paths.",
  }],
  ["s5754", {
    zhSha256: "f218278eecf32af2f18f6b8176c1c310ad9660f30a52c6796460ee7e35977fbc",
    enSha256: "54606288065a2cddbf77fe9f174de28d2218e1067e44a8c8d8fb0740949b1fa4",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
  ["s5804", {
    zhSha256: "9a7315c3130e6306d955b26b77d1bf3bb45db7ef1ca6473e88333d5c8b4fced0",
    enSha256: "9e4bf02d1828cee1e388e3e2d3c2f821998d46c1d0a215f5891cfbb511016526",
    reviewNote: "Chinese 74.95 yi paths equals 7.495 billion paths.",
  }],
  ["s5824", {
    zhSha256: "2958742c07915b449c57b9af27a4c3fa7d52f5d3a50c58c668ce6d276677a3f6",
    enSha256: "2b843bd9e70b6347226f6096623aaedcbc05ec8e83ccbe8af74817116aa24ab8",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
  ["s5887", {
    zhSha256: "8218628d943a896f514d812dae7f3d513f09f8acbdd62e82d03c666cfbbc9043",
    enSha256: "a5471c5e5e956d2f33fd2241beeb6774e40d0b64c2f35c041673bf1bf17d2624",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
  ["s6435", {
    zhSha256: "a672f944b11fe37638b28e8ad449b1e4cd4257e0c72694fcdcdf68cead50c7d0",
    enSha256: "ac043bc5c4bd1661c1cd95aab235e61daa7e624dd25d24676c58175b201199e3",
    reviewNote: "Coprime is exactly equivalent to greatest common divisor 1.",
  }],
  ["s6506", {
    zhSha256: "8f700f30a39a5458533a863a32e37a91b336572386a1f07e727082beeae427d5",
    enSha256: "8a318a0e5658b002e21b703da944885b50b2bb948402fcd2239c22cd6dae1779",
    reviewNote: "Chinese 2.74 yi paths equals 274 million paths; ten wan states equals one hundred thousand states.",
  }],
  ["s6975", {
    zhSha256: "5c2e3e02d177269095cef3d692435272cfb7c5a7ec23e1ac6f2b1a908e6e448e",
    enSha256: "e8461ec554815e249b1d24eef5153e870ef1423786b782d1b2fb4f15c1394bdb",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
  ["s7048", {
    zhSha256: "77e6f15754fcdf44afcf0826619eceeb9efc2d5bf95dec5bad52dbc1b863e0ae",
    enSha256: "9f6c6e1c15b5e2a8bb42d0c690054be089c6b36427e3c0fbdeac9f8c1715b1a3",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
  ["s9815", {
    zhSha256: "4065ceefeef906f8288c8dfc8216b1352b38427a04f8e44e63cd35b5ab4d4969",
    enSha256: "7f71b3b5c6a3bceba1b7b4a90ac42f8612ccf2e6c0bd0470e028d10cddf269cb",
    reviewNote: "Chinese 289.78 yi paths equals 28.978 billion paths.",
  }],
  ["s10321", {
    zhSha256: "e333cfec960c852aceb05d7c511623862595dacd6a514d9aa56de746c1ffb0c3",
    enSha256: "1f13c316209438cf48557c10019af809483536312ba8d845a13cfb72e15823bb",
    reviewNote: "Chinese 74.95 yi paths equals 7.495 billion paths.",
  }],
  ["s10550", {
    zhSha256: "df6a8e7850d601dad817fde2d0a7ef8bb857fbbd6ca7a898a61b8628f7c0d269",
    enSha256: "19ff45fd1cdb68aa58df8b413aaa912bddae42384175520bbcf4404f6ba08078",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
  ["s10551", {
    zhSha256: "7183413154cea03640fff392c17fc5b98a38d977d9a6ade68e9a0fb76417a5f6",
    enSha256: "36aa5730e86f9e09e942f28607fe0de2fb8757678bff1926c11179adf25e1efd",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
  ["s10552", {
    zhSha256: "76d687d71497eee8a0d456ca088f0f666d65ade5bb479d1d05496e7a50d21962",
    enSha256: "7590ae80fcf6919c2698f42d5706b6cd55a7b88d3b619e184901009499f964b1",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
  ["s10569", {
    zhSha256: "3c9c8ada18aa31c8265b62dc6a26d459132ec0bd80214881120acfe1827ca086",
    enSha256: "86596e512bd8eceedc737bd5fe85da91182c671f823369dcdd0ec951eb5d7642",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
  ["s10570", {
    zhSha256: "e7a377b4e272e8dd697c91f98905b1a0bd35b9f993bcfd2cb6979bb97ce8bbf2",
    enSha256: "d21212f6c59eba298e120e8c4273410475f56105cde44f16fe95ac5a53481397",
    reviewNote: "The Chinese numeric month 08 is August in the English date.",
  }],
]);

function sha256Text(value) {
  return createHash("sha256").update(value, "utf8").digest("hex");
}

function captureBindingSha256(entry) {
  return sha256Text(JSON.stringify({
    zh: entry.zh,
    sourceIdAtCapture: entry.sourceIdAtCapture,
    capturedEnglishSha256: entry.capturedEnglishSha256,
    reasonCodes: entry.reasonCodes,
    reviewedIssues: entry.reviewedIssues,
  }));
}

// The English mapping intentionally lives in the captured review snapshot, not
// in this executable. Populate it only after the R0.73U HTML transaction has
// materialized the complete missing-string set.
const activePages = [
  "literature-review.html",
  "notes/index.html",
  "notes/r0-73u.html",
  "recap-r0-61-r0-73u.html",
  "research-review.html",
];
const discouragedChinese = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  "颠覆性", "世界首个", "接近解决", "解决了千禧年", "证明了全局正则性",
  "原创性定理", "首次证明",
];
const requiredDictionaryTokens = [
  "sourceCommitAssigned=TRUE",
  "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
  "dgxUsed=FALSE",
  "localProductTensorDistinctFromKHM=TRUE",
  "instantaneousPressureFromLocalProductTensor=VERIFIED_CLASSICAL",
  "heatCovariancePSD=INTERNAL_EXACT",
  "heatCovarianceScalePDE=INTERNAL_EXACT",
  "filterParameterEquationIsPhysicalTimeClosure=FALSE",
  "subfilterFluxSignDefinite=FALSE",
  "criticalTensorStressRow=INTERNAL_COROLLARY",
  "energyOnlyFixedScaleStress=INTERNAL_COROLLARY",
  "centeredPressureVarianceDirectClassicalCollision=TRUE",
  "fourSiteParityWitness=INTERNAL_EXACT",
  "formalFiniteCertificate=PASS",
  "formalFiniteCertificateChecks=75",
  "formalFigurePackage=PASS",
  "formalFigureChecks=325",
  "finalSeal=TRUE",
  "navierStokesSimulation=NOT_RUN",
  "arbitraryThreeDimensionalGlobalRegularity=OPEN",
  "clayConclusion=OPEN",
  "noveltyOrPriorityClaim=FORBIDDEN",
  "The comparison concerns Navier--Stokes tangents at the same initial time for \\(u\\) and \\(-u\\); it is not a trajectory symmetry.",
];
const requiredReportTokens = [
  "heatCovariancePSD=INTERNAL_EXACT",
  "heatCovarianceScalePDE=INTERNAL_EXACT",
  "sameScalePressureReconstruction=VERIFIED_CLASSICAL",
  "conditionalCriticalStressRow=INTERNAL_COROLLARY",
  "fixedPositiveScaleEnergyStressBound=INTERNAL_COROLLARY",
  "fourSiteQuadraticStateNonAutonomy=CLOSED_EXACT",
  "finiteGeneralTensorClosure=OPEN",
  "formalFiniteCertificateChecks=75",
  "formalFigureChecks=325",
  "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
  "dgxUsed=FALSE",
  "arbitraryThreeDimensionalGlobalRegularity=OPEN",
  "clayConclusion=OPEN",
];

function assertInsideRoot(path, label) {
  const offset = relative(root, path);
  if (!offset || offset === ".." || offset.startsWith("../") || offset.startsWith("..\\")) {
    throw new Error(label + " escaped R073U_RELEASE_ROOT");
  }
  return offset;
}

async function lstatOrMissing(path, label) {
  try {
    return await lstat(path);
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw new Error(label + ": lstat failed for " + path, { cause: error });
  }
}

// Validate the repository root and every lexical component with lstat. This
// deliberately rejects symlinks (including dangling symlinks), missing or
// nondirectory ancestors, and a leaf of the wrong kind. The check is repeated
// immediately before each read, write, unlink, or rename below.
async function assertSafePath(path, label, { leaf = "file", allowMissingLeaf = false } = {}) {
  const offset = assertInsideRoot(path, label);
  const rootInfo = await lstatOrMissing(root, label);
  if (!rootInfo || rootInfo.isSymbolicLink() || !rootInfo.isDirectory()) {
    throw new Error(label + ": release root must be a real directory");
  }
  const components = offset.split(/[\\/]/).filter(Boolean);
  let cursor = root;
  for (let index = 0; index < components.length; index += 1) {
    cursor = resolve(cursor, components[index]);
    const isLeaf = index === components.length - 1;
    const info = await lstatOrMissing(cursor, label);
    if (!info) {
      if (isLeaf && allowMissingLeaf) return null;
      throw new Error(label + ": missing " + (isLeaf ? "leaf" : "ancestor") + " " + cursor);
    }
    if (info.isSymbolicLink()) {
      throw new Error(label + ": symlink component rejected: " + cursor);
    }
    if (!isLeaf && !info.isDirectory()) {
      throw new Error(label + ": nondirectory ancestor rejected: " + cursor);
    }
    if (isLeaf && leaf === "file" && !info.isFile()) {
      throw new Error(label + ": expected a regular file: " + cursor);
    }
    if (isLeaf && leaf === "directory" && !info.isDirectory()) {
      throw new Error(label + ": expected a directory: " + cursor);
    }
    if (isLeaf) return info;
  }
  throw new Error(label + ": empty path walk");
}

async function assertSafeRegularFile(path, label) {
  return assertSafePath(path, label, { leaf: "file" });
}

async function assertSafeDirectory(path, label) {
  return assertSafePath(path, label, { leaf: "directory" });
}

async function assertSafeWritableFile(path, label) {
  return assertSafePath(path, label, { leaf: "file", allowMissingLeaf: true });
}

async function assertSafeMissingFile(path, label) {
  const info = await assertSafeWritableFile(path, label);
  if (info) throw new Error(label + ": scratch path already exists: " + path);
}

async function regularText(path, label) {
  await assertSafeRegularFile(path, label);
  const value = await readFile(path, "utf8");
  if (/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(value)) {
    throw new Error(label + ": control character");
  }
  return value;
}

async function safeUnlinkIfPresent(path, label) {
  const info = await assertSafeWritableFile(path, label);
  if (info) {
    await assertSafeRegularFile(path, label);
    await unlink(path);
  }
}

async function safeAtomicWrite(path, payload) {
  await assertSafeWritableFile(path, "translation target");
  await assertSafeDirectory(dirname(path), "translation parent");
  const temporary = resolve(
    dirname(path),
    `.${path.split("/").at(-1)}.r073u-${process.pid}-${Date.now()}-${process.hrtime.bigint()}.tmp`,
  );
  try {
    await assertSafeMissingFile(temporary, "translation temporary");
    const handle = await open(temporary, "wx", 0o644);
    try {
      await assertSafeRegularFile(temporary, "translation temporary");
      await handle.writeFile(payload, "utf8");
      await handle.sync();
    } finally {
      await handle.close();
    }
    await assertSafeRegularFile(temporary, "translation temporary");
    await assertSafeWritableFile(path, "translation target");
    await rename(temporary, path);
  } finally {
    await safeUnlinkIfPresent(temporary, "translation temporary cleanup");
  }
}

async function writeTransaction(writes) {
  if (writes.length !== 3 || new Set(writes.map(({ path }) => path)).size !== 3) {
    throw new Error("R0.73U translation transaction requires three distinct files");
  }
  const nonce = `${process.pid}-${Date.now()}-${process.hrtime.bigint()}`;
  const rows = writes.map(({ path, payload }, index) => ({
    path,
    payload,
    temporary: resolve(dirname(path), `.${path.split("/").at(-1)}.r073u-${nonce}-${index}.tmp`),
    backup: resolve(dirname(path), `.${path.split("/").at(-1)}.r073u-${nonce}-${index}.bak`),
    backedUp: false,
    installed: false,
  }));
  try {
    for (const row of rows) {
      const current = await assertSafeRegularFile(row.path, "translation target");
      await assertSafeDirectory(dirname(row.path), "translation target parent");
      await assertSafeMissingFile(row.temporary, "translation temporary");
      await assertSafeMissingFile(row.backup, "translation backup");
      const handle = await open(row.temporary, "wx", current.mode & 0o777);
      try {
        await assertSafeRegularFile(row.temporary, "translation temporary");
        await handle.writeFile(row.payload, "utf8");
        await handle.sync();
      } finally {
        await handle.close();
      }
    }
    for (const row of rows) {
      await assertSafeRegularFile(row.path, "translation target before backup rename");
      await assertSafeMissingFile(row.backup, "translation backup before rename");
      await rename(row.path, row.backup);
      row.backedUp = true;
    }
    for (const row of rows) {
      await assertSafeRegularFile(row.temporary, "translation temporary before install rename");
      await assertSafeMissingFile(row.path, "translation target before install rename");
      await rename(row.temporary, row.path);
      row.installed = true;
    }
  } catch (error) {
    for (const row of [...rows].reverse()) {
      try {
        if (row.installed) await safeUnlinkIfPresent(row.path, "translation rollback target");
        if (row.backedUp) {
          await assertSafeRegularFile(row.backup, "translation rollback backup");
          await assertSafeMissingFile(row.path, "translation rollback destination");
          await rename(row.backup, row.path);
        }
      } catch {
        // Preserve the first failure; a surviving backup remains recoverable.
      }
    }
    throw error;
  } finally {
    for (const row of rows) {
      await safeUnlinkIfPresent(row.temporary, "translation temporary cleanup");
      if (row.installed) {
        await safeUnlinkIfPresent(row.backup, "translation backup cleanup");
      }
    }
  }
}

function metadataField(dictionary, label) {
  return dictionary.match(
    new RegExp(`^\\*\\*${label}:\\*\\*\\s*(.+?)(?=\\n\\s*\\n)`, "ms"),
  )?.[1]?.replace(/\s+/g, " ").replace(/^\*|\*$/g, "").trim();
}

const dictionary = await regularText(dictionaryPath, "R0.73U bilingual dictionary");
const report = await regularText(reportPath, "R0.73U report source");
const releaseTitle = metadataField(dictionary, "Release title");
const publicTitle = metadataField(dictionary, "Public title \\(zh\\)");
if (releaseTitle !== "R0.73U | Full tensors in the heat hierarchy: pressure is recoverable, but the even quadratic state is not dynamically closed" ||
    publicTitle !== "R0.73U｜完整张量进入热层级：压力可以恢复，但偶二次状态的动力学并不闭合") {
  throw new Error("R0.73U bilingual dictionary canonical title ledger is absent or drifted");
}
for (const token of requiredDictionaryTokens) {
  if (!dictionary.includes(token)) throw new Error("R0.73U dictionary missing " + token);
}
for (const token of requiredReportTokens) {
  if (!report.includes(token)) throw new Error("R0.73U report missing " + token);
}
for (const stale of [
  "sourceCommitAssigned=FALSE",
  "generatedArtifactCommitAssigned=FALSE",
  "finalSeal=FALSE",
  "formalFigurePackage=PRESEAL_PENDING",
]) {
  if (dictionary.includes(stale) || report.includes(stale)) {
    throw new Error("R0.73U canonical source still carries " + stale);
  }
}
if (!/^\*\*Next release:\*\*\s*R0\.73V\s*$/m.test(dictionary)) {
  throw new Error("R0.73U dictionary next-release gate is not frozen to R0.73V");
}

const releaseManifest = JSON.parse(await regularText(
  resolve(root, "research/release-manifest.json"), "release manifest",
));
const siteVersion = JSON.parse(await regularText(
  resolve(publicDirectory, "site-version.json"), "site version",
));
if (
  releaseManifest.latestCompletedRelease !== "r073u" ||
  releaseManifest.siteVersion !== "1.61" ||
  releaseManifest.publicHtmlNoteCount !== 197 ||
  releaseManifest.postR060RecapNodeCount !== 137 ||
  releaseManifest.nextRelease !== "r073v" ||
  releaseManifest.postR070APublishedReleaseCount !== 99 ||
  releaseManifest.postR070AFormalSealedReleaseCount !== 75 ||
  releaseManifest.legacyFormalFigureBacklogCount !== 24 ||
  siteVersion.latestRelease !== "R0.73U" ||
  siteVersion.version !== "1.61" ||
  siteVersion.publicHtmlNoteCount !== 197
) {
  throw new Error("R0.73U HTML/accounting apply must precede translation work");
}

async function safeLiveSiteFileList() {
  await assertSafeDirectory(publicDirectory, "public site directory");
  await assertSafeDirectory(resolve(publicDirectory, "notes"), "public notes directory");
  const files = await listSiteHtmlFiles(publicDirectory);
  for (const path of files) await assertSafeRegularFile(path, "live site HTML");
  return files;
}

for (const relativePage of activePages) {
  const html = await regularText(resolve(publicDirectory, relativePage), relativePage);
  if (!html.includes("/i18n-en.js?v=1.61")) {
    throw new Error(relativePage + ": expected i18n cache version v1.61");
  }
  if (!html.includes("R0.73U")) throw new Error(relativePage + ": R0.73U marker absent");
  for (const phrase of discouragedChinese) {
    if (html.includes(phrase)) throw new Error(relativePage + ": public-voice violation " + phrase);
  }
}

const translations = JSON.parse(await regularText(translationPath, "translations/en.json"));
if (!Array.isArray(translations)) throw new Error("translations/en.json is not an array");
const siteFilesBefore = await safeLiveSiteFileList();
const source = await collectSiteStrings(publicDirectory);
const siteFilesAfter = await safeLiveSiteFileList();
if (JSON.stringify(siteFilesAfter) !== JSON.stringify(siteFilesBefore)) {
  throw new Error("live site HTML inventory changed during translation collection");
}

const boundaryTokens = (value) =>
  value.match(/NOT CLAY|\b(?:VERIFIED_CLASSICAL_RECONSTRUCTION|VERIFIED_CLASSICAL_WITH_ADAPTATION|VERIFIED_CLASSICAL|INTERNAL_EXACT_SCALING|INTERNAL_COROLLARY|INTERNAL_CONDITIONAL|INTERNAL_EXACT|NOT_PROVED|CLOSED_EXACT|FALSE_AS_INFERENCE|FORBIDDEN|REQUIRED|NOT_RUN|PENDING|CLOSED|OPEN|PASS|FALSE|TRUE)\b/g) ?? [];
const machineTokens = (value) =>
  [...value.matchAll(/\b([A-Za-z][A-Za-z0-9]*)=([A-Z0-9][A-Z0-9_]*)\b/g)].map((match) => match[0]);
const releaseVersionTokens = (value) =>
  value.match(/R0\.\d+[A-Z]?|v\d+(?:\.\d+)+[A-Z]?/g) ?? [];
const englishNumberWords = new Map(Object.entries({
  zero: "0", one: "1", two: "2", three: "3", four: "4", five: "5",
  six: "6", seven: "7", eight: "8", nine: "9", ten: "10",
  eleven: "11", twelve: "12", thirteen: "13", fourteen: "14", fifteen: "15",
  sixteen: "16", seventeen: "17", eighteen: "18", nineteen: "19", twenty: "20",
  thirty: "30", forty: "40", fifty: "50", sixty: "60", seventy: "70",
  eighty: "80", ninety: "90", hundred: "100",
  first: "1", second: "2", third: "3", fourth: "4", fifth: "5",
  sixth: "6", seventh: "7", eighth: "8", ninth: "9", tenth: "10",
  eleventh: "11", twelfth: "12", thirteenth: "13", fourteenth: "14",
  fifteenth: "15", sixteenth: "16", seventeenth: "17", eighteenth: "18",
  nineteenth: "19", twentieth: "20",
}));

function normalizePlainNumber(value) {
  let token = value.replaceAll(",", "").replace(/(?:st|nd|rd|th)$/i, "");
  let sign = "";
  if (token.startsWith("-") || token.startsWith("+")) {
    sign = token[0] === "-" ? "-" : "";
    token = token.slice(1);
  }
  let [integer, fraction] = token.split(".");
  integer = integer.replace(/^0+(?=\d)/, "") || "0";
  if (fraction !== undefined) {
    fraction = fraction.replace(/0+$/, "");
    token = fraction ? `${integer}.${fraction}` : integer;
  } else {
    token = integer;
  }
  if (token === "0") sign = "";
  return sign + token;
}

function plainArabicNumberTokens(value) {
  const normalizedMinus = value.replace(/[\u2212\ufe63\uff0d]/g, "-");
  const withoutReleaseVersions = normalizedMinus.replace(
    /R0\.\d+[A-Z]?|v\d+(?:\.\d+)+[A-Z]?/g,
    " ",
  );
  return [...withoutReleaseVersions.matchAll(
    /(?<![\p{L}\p{N}_])[-+]?(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?:st|nd|rd|th)?(?![\p{L}\p{N}_])/giu,
  )].map((match) => normalizePlainNumber(match[0]));
}

function englishNumericWordTokens(value) {
  const normalizedHyphen = value.replace(/[\u2010-\u2015]/g, "-");
  const words = [...normalizedHyphen.matchAll(
    /\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|first|second|third|fourth|fifth|sixth|seventh|eighth|ninth|tenth|eleventh|twelfth|thirteenth|fourteenth|fifteenth|sixteenth|seventeenth|eighteenth|nineteenth|twentieth)\b/gi,
  )].map((match) => ({
    word: match[0].toLowerCase(),
    start: match.index,
    end: match.index + match[0].length,
  }));
  const cardinalUnits = new Set(["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"]);
  const unitValues = new Set([1, 2, 3, 4, 5, 6, 7, 8, 9]);
  const tensValues = new Set([20, 30, 40, 50, 60, 70, 80, 90]);
  const plainJoin = (left, right) =>
    /^[\s-]+$/.test(normalizedHyphen.slice(left.end, right.start));
  const hundredJoin = (left, right) =>
    /^(?:[\s-]+and)?[\s-]+$/.test(normalizedHyphen.slice(left.end, right.start));
  const tokens = [];
  for (let index = 0; index < words.length; index += 1) {
    const current = words[index];
    const currentValue = Number(englishNumberWords.get(current.word));
    const next = words[index + 1];
    if (cardinalUnits.has(current.word) && next?.word === "hundred" &&
        plainJoin(current, next)) {
      let compound = currentValue * 100;
      index += 1;
      const tail = words[index + 1];
      if (tail && hundredJoin(words[index], tail)) {
        const tailValue = Number(englishNumberWords.get(tail.word));
        if (tail.word !== "hundred" && tailValue < 100) {
          compound += tailValue;
          index += 1;
          const unit = words[index + 1];
          if (tensValues.has(tailValue) && unit &&
              unitValues.has(Number(englishNumberWords.get(unit.word))) &&
              plainJoin(words[index], unit)) {
            compound += Number(englishNumberWords.get(unit.word));
            index += 1;
          }
        }
      }
      tokens.push(String(compound));
      continue;
    }
    if (tensValues.has(currentValue) && next &&
        unitValues.has(Number(englishNumberWords.get(next.word))) &&
        plainJoin(current, next)) {
      tokens.push(String(currentValue + Number(englishNumberWords.get(next.word))));
      index += 1;
      continue;
    }
    tokens.push(String(currentValue));
  }
  return tokens;
}

function multisetSignature(values) {
  const counts = new Map();
  for (const value of values) counts.set(value, (counts.get(value) ?? 0) + 1);
  return JSON.stringify([...counts].sort(([left], [right]) => left.localeCompare(right)));
}

function sameTokenMultiset(left, right) {
  return multisetSignature(left) === multisetSignature(right);
}

function containsTokenMultiset(available, required) {
  const counts = new Map();
  for (const value of available) counts.set(value, (counts.get(value) ?? 0) + 1);
  for (const value of required) {
    const remaining = counts.get(value) ?? 0;
    if (remaining === 0) return false;
    counts.set(value, remaining - 1);
  }
  return true;
}

function englishIssues(zh, english) {
  const issues = [];
  const en = typeof english === "string" ? english.trim() : "";
  if (!en) issues.push({ code: "EMPTY_ENGLISH", message: "English is empty" });
  if (containsChinese(en)) {
    issues.push({ code: "CHINESE_IN_ENGLISH", message: "English contains Chinese" });
  }
  if (/\b(?:we|our|ours|ourselves|us)\b/i.test(en)) {
    issues.push({ code: "COLLECTIVE_VOICE", message: "collective English voice" });
  }
  if (!sameTokenMultiset(extractProtectedTokens(en), extractProtectedTokens(zh))) {
    issues.push({ code: "PROTECTED_TOKEN_MULTISET", message: "protected-token multiset mismatch" });
  }
  if (!sameTokenMultiset(releaseVersionTokens(en), releaseVersionTokens(zh))) {
    issues.push({
      code: "RELEASE_VERSION_TOKEN_MULTISET",
      message: "release/version-token multiset mismatch",
    });
  }
  if (!containsTokenMultiset(
    [...plainArabicNumberTokens(en), ...englishNumericWordTokens(en)],
    plainArabicNumberTokens(zh),
  )) {
    issues.push({
      code: "REQUIRED_ARABIC_NUMBER_MULTISET",
      message: "required Chinese-source Arabic-number multiset is not preserved",
    });
  }
  if (!sameTokenMultiset(boundaryTokens(en), boundaryTokens(zh))) {
    issues.push({ code: "BOUNDARY_TOKEN_MULTISET", message: "claim-state boundary multiset mismatch" });
  }
  if (!sameTokenMultiset(machineTokens(en), machineTokens(zh))) {
    issues.push({ code: "MACHINE_TOKEN_MULTISET", message: "machine-ledger multiset mismatch" });
  }
  return { en, issues };
}

function validateEnglish(zh, english, label) {
  const { en, issues } = englishIssues(zh, english);
  if (issues.length) {
    throw new Error(
      label + " failed strict English validation for " + zh + ": " +
      issues.map(({ code, message }) => `${code} (${message})`).join(", "),
    );
  }
  return en;
}

const existingByChinese = new Map();
const allExistingIds = new Set();
const reviewableIssuesByChinese = new Map();
for (const [index, entry] of translations.entries()) {
  if (!entry || typeof entry !== "object" || Array.isArray(entry) ||
      typeof entry.id !== "string" || !entry.id ||
      typeof entry.zh !== "string" || !entry.zh || typeof entry.en !== "string") {
    throw new Error("invalid existing translation row at index " + index);
  }
  if (allExistingIds.has(entry.id)) throw new Error("duplicate existing translation id: " + entry.id);
  if (existingByChinese.has(entry.zh)) throw new Error("duplicate existing Chinese key: " + entry.zh);
  const review = englishIssues(entry.zh, entry.en);
  entry.en = review.en;
  if (review.issues.length) reviewableIssuesByChinese.set(entry.zh, review.issues);
  allExistingIds.add(entry.id);
  existingByChinese.set(entry.zh, entry);
}

const sourceByChinese = new Map();
for (const entry of source) {
  if (!entry || typeof entry.zh !== "string" || !entry.zh ||
      !Number.isInteger(entry.count) || entry.count <= 0 ||
      !Array.isArray(entry.files) || entry.files.length === 0) {
    throw new Error("invalid live source row");
  }
  if (sourceByChinese.has(entry.zh)) throw new Error("duplicate live Chinese key: " + entry.zh);
  sourceByChinese.set(entry.zh, entry);
}

const releaseId = /^r073u\d+$/;
const releaseBatch = source.filter((entry) => {
  const existing = existingByChinese.get(entry.zh);
  return !existing || releaseId.test(existing.id);
});
const releaseBatchChinese = new Set(releaseBatch.map(({ zh }) => zh));
const releaseBatchFiles = [...new Set(releaseBatch.flatMap((entry) => entry.files))].sort();
if (JSON.stringify(releaseBatchFiles) !== JSON.stringify(activePages)) {
  throw new Error("unexpected R0.73U release-batch files: " + JSON.stringify(releaseBatchFiles));
}
const isForcedSemanticReview = (entry) => {
  const existing = existingByChinese.get(entry.zh);
  return Boolean(existing && forcedSemanticReviewIds.has(existing.id));
};
const currentLegacyRepairs = source.filter((entry) => {
  const existing = existingByChinese.get(entry.zh);
  return existing && !releaseId.test(existing.id) &&
    (reviewableIssuesByChinese.has(entry.zh) || isForcedSemanticReview(entry));
});

function capturedReasonCodes(entry) {
  const existing = existingByChinese.get(entry.zh);
  const issueCodes = (reviewableIssuesByChinese.get(entry.zh) ?? []).map(({ code }) => code);
  const forcedCodes = existing && forcedSemanticReviewIds.has(existing.id)
    ? ["HUMAN_SEMANTIC_REVIEW"]
    : [];
  if (!existing) return ["NEW_LIVE_STRING", ...forcedCodes, ...issueCodes];
  if (releaseId.test(existing.id)) {
    return ["R073U_RELEASE_BATCH", ...forcedCodes, ...issueCodes];
  }
  return [...forcedCodes, ...issueCodes];
}

if (action === "--capture-missing") {
  const reviewBatch = source.filter((entry) =>
    releaseBatchChinese.has(entry.zh) || reviewableIssuesByChinese.has(entry.zh) ||
    isForcedSemanticReview(entry));
  const skeleton = reviewBatch.map(({ zh }) => {
    const row = {
      zh,
      en: existingByChinese.get(zh)?.en ?? "",
      sourceIdAtCapture: existingByChinese.get(zh)?.id ?? null,
      capturedEnglishSha256: existingByChinese.has(zh)
        ? sha256Text(existingByChinese.get(zh).en)
        : null,
      provenance: localDirectProvenance,
      reasonCodes: capturedReasonCodes(sourceByChinese.get(zh)),
      resolution: reviewableIssuesByChinese.has(zh) ||
        isForcedSemanticReview(sourceByChinese.get(zh))
        ? "translation-corrected"
        : "direct-translation",
      reviewNote: "",
      reviewedIssues: (reviewableIssuesByChinese.get(zh) ?? []).map(({ code }) => code),
    };
    return { ...row, captureBindingSha256: captureBindingSha256(row) };
  });
  await safeAtomicWrite(snapshotPath, JSON.stringify(skeleton, null, 2) + "\n");
  console.log(JSON.stringify({
    captured: skeleton.length,
    newRowsRequiringEnglish: reviewBatch.filter(({ zh }) => !existingByChinese.has(zh)).length,
    legacyRowsRequiringRepair: currentLegacyRepairs.length,
    forcedSemanticReviewCount: reviewBatch.filter(isForcedSemanticReview).length,
    reviewableIssueCount: reviewBatch.reduce(
      (total, { zh }) => total + (reviewableIssuesByChinese.get(zh)?.length ?? 0), 0),
    snapshot: "scripts/i18n-snapshots/r073u-missing.json",
    translationPath: translationRoute,
    translationMethod,
    directReviewRequired: true,
  }));
  process.exit(0);
}

const snapshot = JSON.parse(await regularText(snapshotPath, "R0.73U translation snapshot"));
if (!Array.isArray(snapshot) || snapshot.length === 0) throw new Error("empty R0.73U snapshot");
if (snapshot.some((entry) => !entry || typeof entry !== "object" || Array.isArray(entry) ||
    typeof entry.zh !== "string" || !entry.zh || typeof entry.en !== "string" ||
    !(entry.sourceIdAtCapture === null ||
      (typeof entry.sourceIdAtCapture === "string" && entry.sourceIdAtCapture)) ||
    !(entry.capturedEnglishSha256 === null ||
      (typeof entry.capturedEnglishSha256 === "string" &&
       /^[0-9a-f]{64}$/.test(entry.capturedEnglishSha256))) ||
    typeof entry.captureBindingSha256 !== "string" ||
    !/^[0-9a-f]{64}$/.test(entry.captureBindingSha256) ||
    entry.provenance !== localDirectProvenance || !Array.isArray(entry.reasonCodes) ||
    entry.reasonCodes.length === 0 || entry.reasonCodes.some((code) => typeof code !== "string") ||
    !["direct-translation", "translation-corrected", "semantic-equivalent-approved"].includes(
      entry.resolution) || typeof entry.reviewNote !== "string" ||
    !Array.isArray(entry.reviewedIssues) ||
    entry.reviewedIssues.some((code) => typeof code !== "string"))) {
  throw new Error("R0.73U accepts only local-direct-reviewed translation rows");
}
const snapshotByChinese = new Map();
for (const entry of snapshot) {
  if (snapshotByChinese.has(entry.zh)) throw new Error("duplicate R0.73U snapshot key");
  if (!sourceByChinese.has(entry.zh)) throw new Error("R0.73U snapshot contains a non-live key: " + entry.zh);
  if (new Set(entry.reasonCodes).size !== entry.reasonCodes.length) {
    throw new Error("R0.73U snapshot contains duplicate reason codes: " + entry.zh);
  }
  if (new Set(entry.reviewedIssues).size !== entry.reviewedIssues.length) {
    throw new Error("R0.73U snapshot contains duplicate reviewed issues: " + entry.zh);
  }
  if (entry.captureBindingSha256 !== captureBindingSha256(entry)) {
    throw new Error("R0.73U snapshot capture binding drift: " + entry.zh);
  }
  snapshotByChinese.set(entry.zh, entry);
}
for (const entry of releaseBatch) {
  if (!snapshotByChinese.has(entry.zh)) {
    throw new Error("R0.73U snapshot is missing a release-batch row: " + entry.zh);
  }
}
for (const entry of currentLegacyRepairs) {
  if (!snapshotByChinese.has(entry.zh)) {
    const issues = reviewableIssuesByChinese.get(entry.zh) ?? [];
    throw new Error(
      "R0.73U snapshot is missing a reviewable historical row " + entry.zh + ": " +
      (issues.length
        ? issues.map(({ code, message }) => `${code} (${message})`).join(", ")
        : "HUMAN_SEMANTIC_REVIEW"),
    );
  }
}
const issueReasonCodes = new Set([
  "EMPTY_ENGLISH", "CHINESE_IN_ENGLISH", "COLLECTIVE_VOICE",
  "PROTECTED_TOKEN_MULTISET", "RELEASE_VERSION_TOKEN_MULTISET",
  "REQUIRED_ARABIC_NUMBER_MULTISET",
  "BOUNDARY_TOKEN_MULTISET", "MACHINE_TOKEN_MULTISET",
]);
const reviewReasonCodes = new Set([...issueReasonCodes, "HUMAN_SEMANTIC_REVIEW"]);
for (const entry of snapshot) {
  if (entry.reviewedIssues.some((code) => !issueReasonCodes.has(code))) {
    throw new Error("R0.73U snapshot contains an unknown reviewed issue: " + entry.zh);
  }
  const existing = existingByChinese.get(entry.zh);
  if (entry.sourceIdAtCapture !== null) {
    if (!existing || existing.id !== entry.sourceIdAtCapture) {
      throw new Error("R0.73U snapshot source-id binding drift: " + entry.zh);
    }
    if (entry.capturedEnglishSha256 === null) {
      throw new Error("R0.73U existing-row capture hash is absent: " + entry.zh);
    }
  } else if (existing && !releaseId.test(existing.id)) {
    throw new Error("R0.73U new-row source-id lifecycle drift: " + entry.zh);
  } else if (entry.capturedEnglishSha256 !== null) {
    throw new Error("R0.73U new-row capture hash must be null: " + entry.zh);
  }
  const forcedReview = Boolean(existing && forcedSemanticReviewIds.has(existing.id));
  const forcedCodes = forcedReview ? ["HUMAN_SEMANTIC_REVIEW"] : [];
  const expectedReasonCodes = entry.sourceIdAtCapture === null
    ? ["NEW_LIVE_STRING", ...forcedCodes, ...entry.reviewedIssues]
    : releaseId.test(entry.sourceIdAtCapture)
      ? ["R073U_RELEASE_BATCH", ...forcedCodes, ...entry.reviewedIssues]
      : [...forcedCodes, ...entry.reviewedIssues];
  if (JSON.stringify(entry.reasonCodes) !== JSON.stringify(expectedReasonCodes)) {
    throw new Error("R0.73U snapshot reasonCodes binding drift: " + entry.zh);
  }
  const currentIssueCodes = (reviewableIssuesByChinese.get(entry.zh) ?? []).map(({ code }) => code);
  if (existing && entry.capturedEnglishSha256 !== null) {
    const currentEnglishSha256 = sha256Text(existing.en);
    if (currentEnglishSha256 === entry.capturedEnglishSha256) {
      if (JSON.stringify(entry.reviewedIssues) !== JSON.stringify(currentIssueCodes)) {
        throw new Error("R0.73U snapshot captured-issue binding drift: " + entry.zh);
      }
    } else if (currentEnglishSha256 !== sha256Text(englishIssues(entry.zh, entry.en).en)) {
      throw new Error(
        "R0.73U existing English is neither captured nor reviewed snapshot English: " + entry.zh,
      );
    }
  }
  if (releaseBatchChinese.has(entry.zh)) continue;
  if (!existing || releaseId.test(existing.id) ||
      !entry.reasonCodes.some((code) => reviewReasonCodes.has(code))) {
    throw new Error("R0.73U snapshot has an unproved historical repair row: " + entry.zh);
  }
}
const reviewBatch = source.filter((entry) => snapshotByChinese.has(entry.zh));
if (JSON.stringify(snapshot.map(({ zh }) => zh)) !== JSON.stringify(reviewBatch.map(({ zh }) => zh))) {
  throw new Error("R0.73U review snapshot order or membership drift");
}
const reviewedEnglishByChinese = new Map();
const semanticApprovalByChinese = new Map();
for (const entry of snapshot) {
  const existing = existingByChinese.get(entry.zh);
  const forcedReview = Boolean(existing && forcedSemanticReviewIds.has(existing.id));
  const review = englishIssues(entry.zh, entry.en);
  const currentIssueCodes = review.issues.map(({ code }) => code);
  if (forcedReview) {
    const forcedLedger = forcedSemanticReviewLedger.get(existing.id);
    if (sha256Text(entry.zh) !== forcedLedger.zhSha256 ||
        entry.capturedEnglishSha256 !== forcedLedger.capturedEnSha256) {
      throw new Error("HUMAN_SEMANTIC_REVIEW frozen capture binding drift: " + entry.zh);
    }
    if (entry.resolution !== "translation-corrected") {
      throw new Error(
        "HUMAN_SEMANTIC_REVIEW requires translation-corrected and cannot be approved: " +
        entry.zh,
      );
    }
    if (sha256Text(review.en) === forcedLedger.capturedEnSha256) {
      throw new Error("HUMAN_SEMANTIC_REVIEW requires English changed from capture: " + entry.zh);
    }
    if (review.issues.length) {
      throw new Error(
        "HUMAN_SEMANTIC_REVIEW correction failed strict validation for " + entry.zh + ": " +
        review.issues.map(({ code, message }) => `${code} (${message})`).join(", "),
      );
    }
    reviewedEnglishByChinese.set(entry.zh, review.en);
    continue;
  }
  if (entry.resolution === "semantic-equivalent-approved") {
    if (review.issues.length === 0) {
      throw new Error("semantic approval is unnecessary for a strict-pass row: " + entry.zh);
    }
    if (!sameTokenMultiset(currentIssueCodes, ["REQUIRED_ARABIC_NUMBER_MULTISET"])) {
      throw new Error(
        "semantic approval cannot waive structural, machine, boundary, release, or voice issues: " +
        entry.zh,
      );
    }
    if (!sameTokenMultiset(entry.reviewedIssues, currentIssueCodes)) {
      throw new Error("semantic approval reviewedIssues drift: " + entry.zh);
    }
    if (!existing) {
      throw new Error("semantic approval is forbidden for a new translation: " + entry.zh);
    }
    const approval = semanticEquivalenceLedger.get(existing.id);
    if (!approval) {
      throw new Error("semantic approval is absent from the frozen whitelist: " + entry.zh);
    }
    if (sha256Text(entry.zh) !== approval.zhSha256 ||
        entry.capturedEnglishSha256 !== approval.enSha256 ||
        sha256Text(existing.en) !== approval.enSha256) {
      throw new Error("semantic approval frozen source hash drift: " + entry.zh);
    }
    if (review.en !== existing.en) {
      throw new Error("semantic approval cannot alter captured English: " + entry.zh);
    }
    if (entry.reviewNote !== approval.reviewNote) {
      throw new Error("semantic approval fixed review note drift: " + entry.zh);
    }
    reviewedEnglishByChinese.set(entry.zh, review.en);
    semanticApprovalByChinese.set(entry.zh, true);
  } else {
    if (review.issues.length) {
      throw new Error(
        "R0.73U review snapshot requires corrected English for " + entry.zh + ": " +
        review.issues.map(({ code, message }) => `${code} (${message})`).join(", "),
      );
    }
    reviewedEnglishByChinese.set(entry.zh, review.en);
  }
}

const allocatedIds = new Set(
  source.flatMap((entry) => {
    const existing = existingByChinese.get(entry.zh);
    return existing ? [existing.id] : [];
  }),
);
let nextReleaseId = 1;
function allocateReleaseId() {
  while (true) {
    const candidate = "r073u" + String(nextReleaseId).padStart(3, "0");
    nextReleaseId += 1;
    if (!allExistingIds.has(candidate) && !allocatedIds.has(candidate)) {
      allocatedIds.add(candidate);
      return candidate;
    }
  }
}

let added = 0;
const finalTranslations = source.map((entry) => {
  const existing = existingByChinese.get(entry.zh);
  const id = existing?.id ?? allocateReleaseId();
  if (!existing) added += 1;
  const en = reviewedEnglishByChinese.has(entry.zh)
    ? reviewedEnglishByChinese.get(entry.zh)
    : existing?.en;
  const finalEnglish = semanticApprovalByChinese.has(entry.zh)
    ? en
    : validateEnglish(entry.zh, en, "live translation " + id);
  return {
    id,
    zh: entry.zh,
    count: entry.count,
    files: [...entry.files],
    en: finalEnglish,
  };
});

if (new Set(finalTranslations.map(({ id }) => id)).size !== finalTranslations.length) {
  throw new Error("duplicate final translation id");
}
if (new Set(finalTranslations.map(({ zh }) => zh)).size !== finalTranslations.length) {
  throw new Error("duplicate final Chinese key");
}
if (JSON.stringify(finalTranslations.map(({ zh }) => zh)) !== JSON.stringify(source.map(({ zh }) => zh))) {
  throw new Error("final translation ledger is not the live source ledger");
}
const finalByChinese = new Map(finalTranslations.map(({ zh, en }) => [zh, en.trim()]));
const stillMissing = source.filter((entry) => !finalByChinese.has(entry.zh));
if (stillMissing.length) throw new Error("live string remains untranslated: " + stillMissing[0].zh);
const liveDictionary = Object.fromEntries(source.map((entry) => [entry.zh, finalByChinese.get(entry.zh)]));
const snapshotOutput = JSON.stringify(
  reviewBatch.map(({ zh }) => ({
    zh,
    en: reviewedEnglishByChinese.get(zh),
    sourceIdAtCapture: snapshotByChinese.get(zh).sourceIdAtCapture,
    capturedEnglishSha256: snapshotByChinese.get(zh).capturedEnglishSha256,
    captureBindingSha256: snapshotByChinese.get(zh).captureBindingSha256,
    provenance: localDirectProvenance,
    reasonCodes: [...snapshotByChinese.get(zh).reasonCodes],
    resolution: snapshotByChinese.get(zh).resolution,
    reviewNote: snapshotByChinese.get(zh).reviewNote.trim(),
    reviewedIssues: [...snapshotByChinese.get(zh).reviewedIssues],
  })),
  null,
  2,
) + "\n";
const translationOutput = JSON.stringify(finalTranslations, null, 2) + "\n";
const bundleOutput = "globalThis.NS_EN_TRANSLATIONS = Object.freeze(" + JSON.stringify(liveDictionary, null, 2) + ");\n";

if (action === "--check-only") {
  if (await regularText(snapshotPath, "R0.73U translation snapshot") !== snapshotOutput) {
    throw new Error("R0.73U translation snapshot is stale");
  }
  if (JSON.stringify(translations) !== JSON.stringify(finalTranslations)) {
    throw new Error("R0.73U translations are stale");
  }
  if (await regularText(bundlePath, "public/i18n-en.js") !== bundleOutput) {
    throw new Error("R0.73U translation bundle is stale");
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
  added,
  removedStale: translations.length - finalTranslations.filter(
    ({ zh }) => existingByChinese.has(zh),
  ).length,
  legacyRowsRequiringRepair: reviewBatch.filter(({ zh }) => {
    const existing = existingByChinese.get(zh);
    return existing && !releaseId.test(existing.id);
  }).length,
  forcedSemanticReviewCount: reviewBatch.filter(isForcedSemanticReview).length,
  semanticEquivalentApprovals: semanticApprovalByChinese.size,
  reviewBatchRows: reviewBatch.length,
  total: finalTranslations.length,
  liveStrings: source.length,
  missingAfter: stillMissing.length,
  snapshot: "scripts/i18n-snapshots/r073u-missing.json",
  bundle: "public/i18n-en.js",
  translationPath: translationRoute,
  translationMethod,
  directReviewRequired: true,
}));
