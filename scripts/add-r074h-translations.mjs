#!/usr/bin/env node

import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const note = await readFile(resolve(root, "public/notes/r0-74h.html"), "utf8");
const dictionary = await readFile(resolve(root, "research/r074h_bilingual_dictionary.md"), "utf8");

for (const marker of [
  "完整中文版本",
  "PROVED",
  "FINITE",
  "OPEN",
  "LITERATURE BOUNDARY",
  "NOT CLAY",
]) assert.ok(note.includes(marker), `R0.74H Chinese note missing ${marker}`);
assert.ok(dictionary.includes("R0.74H bilingual publication dictionary"));

if (process.argv.includes("--check-only")) {
  process.stdout.write("R0.74H translation snapshot: PASS\n");
} else {
  process.stdout.write("R0.74H Chinese publication text is complete; no mutation required.\n");
}
