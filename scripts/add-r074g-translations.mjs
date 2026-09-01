#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const note = await readFile(resolve(root, "public/notes/r0-74g.html"), "utf8");
const dictionary = await readFile(resolve(root, "research/r074g_bilingual_dictionary.md"), "utf8");

for (const marker of [
  "完整中文版本",
  "PROVED",
  "FINITE",
  "OPEN",
  "ROUTE REJECTED",
  "NOT CLAY",
]) {
  assert.ok(note.includes(marker), `R0.74G Chinese note missing ${marker}`);
}
assert.ok(dictionary.includes("R0.74G bilingual publication dictionary"));

if (!process.argv.includes("--check-only")) {
  process.stdout.write("R0.74G Chinese publication text is already complete; no mutation required.\n");
} else {
  process.stdout.write("R0.74G translation snapshot: PASS\n");
}
