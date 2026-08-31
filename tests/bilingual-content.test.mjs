import assert from "node:assert/strict";
import { mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { basename, join, resolve } from "node:path";
import test from "node:test";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
  extractTranslatableStrings,
  listSiteHtmlFiles,
} from "../scripts/i18n-lib.mjs";

const projectRoot = resolve(import.meta.dirname, "..");
const publicDirectory = resolve(projectRoot, "public");

async function loadDictionary() {
  const source = await readFile(resolve(publicDirectory, "i18n-en.js"), "utf8");
  const match = source.match(/Object\.freeze\(([\s\S]+)\);\s*$/);
  assert.ok(match, "i18n-en.js must contain the generated dictionary");
  return JSON.parse(match[1]);
}

test("HTML extraction keeps mathematical comparisons in their text node", () => {
  const strings = extractTranslatableStrings(
    "<p>其对数导数为 \\(f(x)\\)<0，所以严格递减。</p>",
  );
  assert.deepEqual(strings, ["其对数导数为 \\(f(x)\\)<0，所以严格递减。"]);
});

test("recap enumeration includes canonical names and excludes conflict copies", async (t) => {
  const root = await mkdtemp(join(tmpdir(), "i18n-recap-enumeration-"));
  t.after(() => rm(root, { recursive: true, force: true }));
  const fixturePublic = join(root, "public");
  await mkdir(join(fixturePublic, "notes"), { recursive: true });

  for (const name of [
    "recap-r0-60.html",
    "recap-r0-61-r0-73t.html",
    "recap-r0-61-r0-73t 2.html",
    "recap-r0-61-r0-73t 3.html",
    "recap-r0-61-r0-73t 4.html",
  ]) {
    await writeFile(join(fixturePublic, name), "<!doctype html>");
  }

  const recapNames = (await listSiteHtmlFiles(fixturePublic))
    .map((path) => basename(path))
    .filter((name) => name.startsWith("recap-"));
  assert.deepEqual(recapNames, [
    "recap-r0-60.html",
    "recap-r0-61-r0-73t.html",
  ]);
});

test("every research page loads the shared language controls before MathJax", async () => {
  const files = await listSiteHtmlFiles(publicDirectory);
  assert.ok(files.length >= 23);
  assert.ok(files.some((file) => file.endsWith("recap-r0-60.html")));
  assert.ok(files.some((file) => file.endsWith("recap-r0-61-r0-71a.html")));
  for (const file of files) {
    const html = await readFile(file, "utf8");
    assert.match(html, /href="\/bilingual\.css"/);
    assert.match(html, /src="\/i18n-en\.js(?:\?[^"]*)?"/);
    assert.match(html, /src="\/bilingual\.js"/);
    const mathJaxIndex = html.indexOf("mathjax@3");
    assert.ok(
      mathJaxIndex < 0 || html.indexOf('src="/bilingual.js"') < mathJaxIndex,
      `${file} must translate content before MathJax typesets it`,
    );
  }
});

test("the English dictionary covers every Chinese reader-facing string", async () => {
  const [entries, dictionary] = await Promise.all([
    collectSiteStrings(publicDirectory),
    loadDictionary(),
  ]);
  const missing = entries.filter((entry) => !dictionary[entry.zh]);
  assert.deepEqual(missing, []);
  for (const entry of entries) {
    const translation = dictionary[entry.zh];
    assert.ok(!containsChinese(translation), `Chinese remains in: ${entry.zh}`);
    assert.deepEqual(
      extractProtectedTokens(translation),
      extractProtectedTokens(entry.zh),
      `Protected TeX or URL changed in: ${entry.zh}`,
    );
  }
});

test("language selection follows the browser once and persists across pages", async () => {
  const runtime = await readFile(resolve(publicDirectory, "bilingual.js"), "utf8");
  assert.match(runtime, /navigator\.language/);
  assert.match(runtime, /localStorage\.getItem\(storageKey\)/);
  assert.match(runtime, /localStorage\.setItem\(storageKey, target\)/);
  assert.match(runtime, /url\.searchParams\.set\("lang", target\)/);
  assert.match(runtime, /document\.documentElement\.lang/);
  assert.match(runtime, /location\.replace/);
  assert.match(runtime, /Chinese PDF/);
  assert.match(runtime, /window\.parent\.document\.title/);
  assert.doesNotMatch(runtime, /中文\s*\/\s*English|English\s*\/\s*中文/);
});

test("English prose keeps the voice of one human researcher", async () => {
  const dictionary = await loadDictionary();
  const prose = Object.values(dictionary).join("\n");
  assert.doesNotMatch(prose, /\b(?:we|our|ours|ourselves)\b/i);
  assert.doesNotMatch(
    prose,
    /\b(?:AI-generated|as an AI|research team|our team|breakthrough)\b/i,
  );
  assert.doesNotMatch(
    prose,
    /(?:re-calculable|research station|computer exhaustive|negative list|stacked shells|triangular polynomial|modulus energy|constant variation|integral upper term|three waves|wave numbers|spiral triads)/i,
  );
  assert.doesNotMatch(prose, /(?:^|\n)s\d{1,4}(?=(?:\s|·))/i);
  assert.doesNotMatch(prose, /\\t(?=[^A-Za-z]|$)/);
  assert.doesNotMatch(prose, /[。；，：、]/);
  assert.doesNotMatch(prose, /\bEND\b/);
  assert.match(prose, /\bI\b/);
  assert.equal(
    dictionary[
      "资料截止：2026-08-31。若后续论文状态、版本或官方判断发生变化，我会在此页更新并保留原来的证据标签。"
    ],
    "Sources checked through 2026-08-31. If publication status, versions, or official assessments change, I will update this page while preserving the original evidence labels.",
  );
  assert.match(
    dictionary[
      "因而只优化两组反对称角会漏掉一个严格下降方向。 我又取有理参数 \\(m=28/155\\)、\\(n=7/25\\)、\\(x=5377/5000\\)， 对 332 个聚合频率作精确比较，得到外部/目标比 \\(18.035985268234917\\ldots\\)，目标能量比例为 \\(5.2532085201\\ldots\\%\\)。"
    ],
    /^Therefore,.*\bI then took\b/,
  );
});
