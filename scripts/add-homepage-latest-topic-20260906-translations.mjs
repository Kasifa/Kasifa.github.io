#!/usr/bin/env node

import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const checkOnly = process.argv.includes("--check-only");
const args = ["scripts/add-clay-b-plateau-history-20260906-translations.mjs"];
if (checkOnly) args.push("--check-only");
const result = spawnSync(process.execPath, args, { cwd: root, encoding: "utf8" });
assert.equal(result.status, 0, `${result.stdout}\n${result.stderr}`);
process.stdout.write(`${JSON.stringify({
  release: "Homepage-LatestTopic-20260906",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
  delegatedSnapshot: "ClayB-PlateauHistory-20260906",
  applied: !checkOnly,
}, null, 2)}\n`);
