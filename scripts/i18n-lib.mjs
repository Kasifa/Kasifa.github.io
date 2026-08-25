import { readdir, readFile } from "node:fs/promises";
import { join } from "node:path";

const CHINESE_RE = /[\u3400-\u9fff\uf900-\ufaff]/u;
const TRANSLATABLE_ATTRIBUTES = new Set([
  "alt",
  "aria-label",
  "content",
  "placeholder",
  "title",
]);

export function decodeHtml(value) {
  return value
    .replace(/&nbsp;/g, "\u00a0")
    .replace(/&amp;/g, "&")
    .replace(/&lt;/g, "<")
    .replace(/&gt;/g, ">")
    .replace(/&quot;/g, '"')
    .replace(/&#39;|&apos;/g, "'")
    .replace(/&#(\d+);/g, (_, value) => String.fromCodePoint(Number(value)))
    .replace(/&#x([0-9a-f]+);/gi, (_, value) =>
      String.fromCodePoint(Number.parseInt(value, 16)),
    );
}

export function normalizeKey(value) {
  return decodeHtml(value).replace(/\s+/g, " ").trim();
}

export function containsChinese(value) {
  return CHINESE_RE.test(value);
}

export function extractTranslatableStrings(html) {
  const strings = [];
  // Split only real HTML tags. A bare comparison such as TeX followed by
  // "<0" is text, not markup, and must remain in the translation key.
  const parts = html.split(
    /(<!--[\s\S]*?-->|<![^>]*>|<\/?[A-Za-z][^>]*>)/g,
  );
  let skippedElement = null;

  for (const part of parts) {
    if (!part) continue;

    if (part.startsWith("<")) {
      const closing = part.match(/^<\/\s*([a-z0-9-]+)/i)?.[1]?.toLowerCase();
      if (closing && closing === skippedElement) {
        skippedElement = null;
        continue;
      }

      if (skippedElement) continue;

      const opening = part.match(/^<\s*([a-z0-9-]+)/i)?.[1]?.toLowerCase();
      if (opening && ["script", "style", "noscript"].includes(opening)) {
        skippedElement = opening;
        continue;
      }

      for (const match of part.matchAll(/([:\w-]+)\s*=\s*(["'])([\s\S]*?)\2/g)) {
        const attribute = match[1].toLowerCase();
        if (!TRANSLATABLE_ATTRIBUTES.has(attribute)) continue;
        if (attribute === "content" && opening !== "meta") continue;
        const value = normalizeKey(match[3]);
        if (containsChinese(value)) strings.push(value);
      }
      continue;
    }

    if (skippedElement) continue;
    const value = normalizeKey(part);
    if (containsChinese(value)) strings.push(value);
  }

  return strings;
}

export async function listSiteHtmlFiles(publicDirectory) {
  const noteDirectory = join(publicDirectory, "notes");
  const noteFiles = (await readdir(noteDirectory))
    .filter((name) => /^r0-\d+[a-z0-9-]*\.html$/.test(name))
    .sort((a, b) => a.localeCompare(b, undefined, { numeric: true }));

  return [
    join(publicDirectory, "research-review.html"),
    join(publicDirectory, "literature-review.html"),
    ...noteFiles.map((name) => join(noteDirectory, name)),
  ];
}

export async function collectSiteStrings(publicDirectory) {
  const files = await listSiteHtmlFiles(publicDirectory);
  const entries = new Map();

  for (const file of files) {
    const html = await readFile(file, "utf8");
    for (const text of extractTranslatableStrings(html)) {
      const entry = entries.get(text) ?? { zh: text, count: 0, files: [] };
      entry.count += 1;
      const relative = file.slice(publicDirectory.length + 1);
      if (!entry.files.includes(relative)) entry.files.push(relative);
      entries.set(text, entry);
    }
  }

  return [...entries.values()].sort((a, b) =>
    a.files[0].localeCompare(b.files[0], undefined, { numeric: true }) ||
    a.zh.localeCompare(b.zh, "zh-CN"),
  );
}

export function extractProtectedTokens(value) {
  const tokens = [];
  const patterns = [
    /\\\([\s\S]*?\\\)/g,
    /\\\[[\s\S]*?\\\]/g,
    /https?:\/\/[^\s<]+/g,
  ];
  for (const pattern of patterns) {
    tokens.push(
      ...value.matchAll(pattern).map((match) =>
        match[0].replace(
          /\\(text|mathrm|operatorname)\{[^{}]*\}/g,
          "\\$1{__I18N_TEXT__}",
        ),
      ),
    );
  }
  return tokens;
}
