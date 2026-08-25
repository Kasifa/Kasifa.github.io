import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import test from "node:test";
import { listSiteHtmlFiles } from "../scripts/i18n-lib.mjs";

const publicDirectory = resolve(import.meta.dirname, "../public");

function idsIn(html) {
  return new Set([...html.matchAll(/\sid=["']([^"']+)["']/g)].map((match) => match[1]));
}

test("every reader-facing internal link and fragment resolves", async () => {
  const files = await listSiteHtmlFiles(publicDirectory);
  const htmlCache = new Map();
  for (const file of files) htmlCache.set(file, await readFile(file, "utf8"));

  for (const [file, html] of htmlCache) {
    const localIds = idsIn(html);
    for (const match of html.matchAll(/\shref=["']([^"']+)["']/g)) {
      const href = match[1];
      if (/^(?:https?:|mailto:|javascript:)/.test(href)) continue;
      if (href.startsWith("#")) {
        assert.ok(localIds.has(href.slice(1)), `${file}: missing fragment ${href}`);
        continue;
      }
      if (!href.startsWith("/")) continue;

      const [pathAndQuery, fragment] = href.split("#", 2);
      const pathname = pathAndQuery.split("?", 1)[0];
      const target = pathname === "/"
        ? join(publicDirectory, "research-review.html")
        : join(publicDirectory, pathname.slice(1));
      assert.ok(target.startsWith(`${publicDirectory}/`), `${file}: unsafe path ${href}`);
      await assert.doesNotReject(access(target), `${file}: missing target ${href}`);

      if (fragment && target.endsWith(".html")) {
        const targetHtml = htmlCache.get(target) ?? await readFile(target, "utf8");
        assert.ok(idsIn(targetHtml).has(fragment), `${file}: missing target fragment ${href}`);
      }
    }
  }
});
