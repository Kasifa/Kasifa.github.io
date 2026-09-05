#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const baseUrl = new URL(process.env.R076L_PUBLIC_BASE_URL ?? "https://kasifa.github.io/");
const commit = process.env.R076L_DEPLOYED_COMMIT ?? "unversioned";
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const objects = [
  ["public/notes/r0-76l.html", "/notes/r0-76l.html"], ["public/notes/r0-76l.pdf", "/notes/r0-76l.pdf"],
  ["public/assets/r076l/fig-r076l-parabolic-edge.svg", "/assets/r076l/fig-r076l-parabolic-edge.svg"],
  ["public/assets/r076l/fig-r076l-parabolic-edge.png", "/assets/r076l/fig-r076l-parabolic-edge.png"],
  ["public/assets/r076l/fig-r076l-parabolic-edge.pdf", "/assets/r076l/fig-r076l-parabolic-edge.pdf"],
  ["public/recap-r0-61-r0-76i.html", "/recap-r0-61-r0-76i.html"], ["public/recap-r0-61-r0-76i.pdf", "/recap-r0-61-r0-76i.pdf"],
  ["public/notes/r0-76j.html", "/notes/r0-76j.html"], ["public/notes/r0-76j.pdf", "/notes/r0-76j.pdf"],
  ["public/notes/r0-76k.html", "/notes/r0-76k.html"], ["public/notes/r0-76k.pdf", "/notes/r0-76k.pdf"],
  ["public/research-review.html", "/research-review.html"], ["public/literature-review.html", "/literature-review.html"],
  ["public/notes/index.html", "/notes/index.html"], ["public/site-version.json", "/site-version.json"], ["public/i18n-en.js", "/i18n-en.js"],
];
const results = [];
for (const [localPath, publicPath] of objects) {
  const expected = await readFile(resolve(root, localPath));
  const url = new URL(publicPath, baseUrl); url.searchParams.set("publication", commit);
  const response = await fetch(url, { headers: { "cache-control": "no-cache" } });
  const actual = Buffer.from(await response.arrayBuffer());
  results.push({ publicPath, status: response.status, onlineBytes: actual.length, onlineSha256: sha256(actual), expectedBytes: expected.length, expectedSha256: sha256(expected), exact: response.status === 200 && actual.equals(expected) });
}
const failures = results.filter((row) => !row.exact);
console.log(JSON.stringify({ status: failures.length === 0 ? "PASS" : "FAIL", release: "R0.76L Step 63", baseUrl: baseUrl.href, commit, objectCount: results.length, exactCount: results.length - failures.length, results, failures }, null, 2));
if (failures.length > 0) process.exitCode = 1;
