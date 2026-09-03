#!/usr/bin/env node

import assert from "node:assert/strict";
import { execFileSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const baseUrl = new URL(process.env.R074U_PUBLIC_BASE_URL ?? "https://kasifa.github.io/");
const commit = process.env.R074U_DEPLOYED_COMMIT ?? "unversioned";
const figureId = "fig-r074u-intrinsic-certified-residence";
const publicFigureRoot = `public/figures/r074u/${figureId}`;
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

const fixedObjects = [
  ["public/notes/r0-74u.html", "/notes/r0-74u.html"],
  ["public/notes/r0-74u.pdf", "/notes/r0-74u.pdf"],
  ["public/research-review.html", "/research-review.html"],
  ["public/literature-review.html", "/literature-review.html"],
  ["public/notes/index.html", "/notes/index.html"],
  ["public/site-version.json", "/site-version.json"],
  ["public/i18n-en.js", "/i18n-en.js"],
  ["public/recap-r0-61-r0-74s.html", "/recap-r0-61-r0-74s.html"],
  ["public/recap-r0-61-r0-74s.pdf", "/recap-r0-61-r0-74s.pdf"],
  [`public/assets/r074u/${figureId}.pdf`, `/assets/r074u/${figureId}.pdf`],
  [`public/assets/r074u/${figureId}.png`, `/assets/r074u/${figureId}.png`],
  [`public/assets/r074u/${figureId}.svg`, `/assets/r074u/${figureId}.svg`],
];

const figureNames = execFileSync(
  "git",
  ["ls-tree", "-r", "--name-only", "HEAD", `research/figures/r074u/${figureId}`],
  { cwd: root, encoding: "utf8" },
).trim().split("\n").filter(Boolean).map((path) => path.split("/").at(-1)).sort();
assert.equal(figureNames.length, 25, "frozen figure archive must contain exactly 25 files");
assert.ok(figureNames.every((name) => !/ 2(?:\.|$)/.test(name)), "duplicate-copy names are not publication objects");

const objects = [
  ...fixedObjects,
  ...figureNames.map((name) => [
    `${publicFigureRoot}/${name}`,
    `/figures/r074u/${figureId}/${encodeURIComponent(name)}`,
  ]),
];
assert.equal(objects.length, 37, "Step 20 online publication inventory");

const results = [];
for (const [localPath, publicPath] of objects) {
  const expected = await readFile(resolve(root, localPath));
  const url = new URL(publicPath, baseUrl);
  url.searchParams.set("publication", commit);
  const response = await fetch(url, { headers: { "cache-control": "no-cache" } });
  const actual = Buffer.from(await response.arrayBuffer());
  results.push({
    publicPath,
    status: response.status,
    bytes: actual.length,
    sha256: sha256(actual),
    expectedSha256: sha256(expected),
    exact: response.status === 200 && actual.equals(expected),
  });
}

const failures = results.filter((row) => !row.exact);
console.log(JSON.stringify({
  status: failures.length === 0 ? "PASS" : "FAIL",
  release: "R0.74U Step 20",
  baseUrl: baseUrl.href,
  commit,
  objectCount: results.length,
  exactCount: results.length - failures.length,
  failures,
}, null, 2));

if (failures.length > 0) process.exitCode = 1;
