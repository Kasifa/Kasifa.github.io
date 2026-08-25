import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { join, resolve } from "node:path";
import test from "node:test";
import { listSiteHtmlFiles } from "../scripts/i18n-lib.mjs";

const publicDirectory = resolve(import.meta.dirname, "../public");
const repositoryDirectory = resolve(publicDirectory, "..");

function idsIn(html) {
  return new Set(
    [...html.matchAll(/\sid=["']([^"']+)["']/g)].map((match) => match[1]),
  );
}

test("every reader-facing internal link, asset, and fragment resolves", async () => {
  const files = await listSiteHtmlFiles(publicDirectory);
  const htmlCache = new Map();
  for (const file of files) htmlCache.set(file, await readFile(file, "utf8"));

  for (const [file, html] of htmlCache) {
    const localIds = idsIn(html);
    for (const match of html.matchAll(/\s(href|src)=["']([^"']+)["']/g)) {
      const attribute = match[1];
      const reference = match[2];
      if (/^(?:https?:|mailto:|javascript:|data:)/.test(reference)) continue;
      if (reference.startsWith("#")) {
        assert.equal(
          attribute,
          "href",
          file + ": only href may target a fragment",
        );
        assert.ok(
          localIds.has(reference.slice(1)),
          file + ": missing fragment " + reference,
        );
        continue;
      }
      if (!reference.startsWith("/")) continue;

      const [pathAndQuery, fragment] = reference.split("#", 2);
      const pathname = pathAndQuery.split("?", 1)[0];
      const target =
        pathname === "/"
          ? join(publicDirectory, "research-review.html")
          : join(publicDirectory, pathname.slice(1));
      assert.ok(
        target.startsWith(publicDirectory + "/"),
        file + ": unsafe path " + reference,
      );
      await assert.doesNotReject(
        access(target),
        file + ": missing target " + reference,
      );

      if (fragment && target.endsWith(".html")) {
        const targetHtml =
          htmlCache.get(target) ?? (await readFile(target, "utf8"));
        assert.ok(
          idsIn(targetHtml).has(fragment),
          file + ": missing target fragment " + reference,
        );
      }
    }
  }
});

test("every GitHub main-branch source link resolves in the publication tree", async () => {
  const files = await listSiteHtmlFiles(publicDirectory);
  let checked = 0;

  for (const file of files) {
    const html = await readFile(file, "utf8");
    for (const match of html.matchAll(/\shref=["'](https:\/\/github\.com\/Kasifa\/Kasifa\.github\.io\/(?:blob|tree)\/main\/[^"']+)["']/g)) {
      const url = new URL(match[1]);
      const relativePath = decodeURIComponent(
        url.pathname.replace(/^\/Kasifa\/Kasifa\.github\.io\/(?:blob|tree)\/main\//, ""),
      );
      const target = join(repositoryDirectory, relativePath);
      assert.ok(
        target.startsWith(repositoryDirectory + "/"),
        file + ": unsafe GitHub source path " + match[1],
      );
      await assert.doesNotReject(
        access(target),
        file + ": missing GitHub source target " + match[1],
      );
      checked += 1;
    }
  }

  assert.ok(checked >= 700, `expected broad source-link coverage, checked ${checked}`);
});

test("every reader-facing HTML page follows the site voice boundary", async () => {
  const files = await listSiteHtmlFiles(publicDirectory);
  for (const file of files) {
    const html = await readFile(file, "utf8");
    assert.doesNotMatch(
      html,
      /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
      file,
    );
  }
});
