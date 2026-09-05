#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const baseUrl = new URL(process.env.CLAY_B_SIGNED_SCALE_PUBLIC_BASE_URL ?? "https://kasifa.github.io/");
const commit = process.env.CLAY_B_SIGNED_SCALE_DEPLOYED_COMMIT ?? "unversioned";
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const objects = [
  ["public/notes/clay-b-signed-scale-20260905.html", "/notes/clay-b-signed-scale-20260905.html"],
  ["public/notes/clay-b-two-scale-20260905.html", "/notes/clay-b-two-scale-20260905.html"],
  ["public/notes/clay-b-two-scale-20260905.pdf", "/notes/clay-b-two-scale-20260905.pdf"],
  ["public/notes/r0-76l.html", "/notes/r0-76l.html"],
  ["public/notes/r0-76l.pdf", "/notes/r0-76l.pdf"],
  ["public/recap-r0-61-r0-76i.html", "/recap-r0-61-r0-76i.html"],
  ["public/recap-r0-61-r0-76i.pdf", "/recap-r0-61-r0-76i.pdf"],
  ["public/research-review.html", "/research-review.html"],
  ["public/literature-review.html", "/literature-review.html"],
  ["public/notes/index.html", "/notes/index.html"],
  ["public/site-version.json", "/site-version.json"],
  ["public/i18n-en.js", "/i18n-en.js"],
];

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
    onlineBytes: actual.length,
    onlineSha256: sha256(actual),
    expectedBytes: expected.length,
    expectedSha256: sha256(expected),
    exact: response.status === 200 && actual.equals(expected),
  });
}

const absentUrl = new URL("/notes/clay-b-signed-scale-20260905.pdf", baseUrl);
absentUrl.searchParams.set("publication", commit);
const absentResponse = await fetch(absentUrl, { headers: { "cache-control": "no-cache" } });
const failures = results.filter((row) => !row.exact);
const pdfAbsent = absentResponse.status === 404;
console.log(JSON.stringify({
  status: failures.length === 0 && pdfAbsent ? "PASS" : "FAIL",
  releaseId: "ClayB-SignedScale-20260905",
  baseUrl: baseUrl.href,
  commit,
  objectCount: results.length,
  exactCount: results.length - failures.length,
  pdfPolicy: "NO_NEW_PDF",
  newPdfStatus: absentResponse.status,
  pdfAbsent,
  results,
  failures,
}, null, 2));
if (failures.length > 0 || !pdfAbsent) process.exitCode = 1;
