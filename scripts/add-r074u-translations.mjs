#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const checkOnly = process.argv.includes("--check-only");
const delegated = spawnSync(
  process.execPath,
  [resolve(root, "scripts/add-r074u-step20-translations.mjs"), ...(checkOnly ? ["--check-only"] : [])],
  { cwd: root, encoding: "utf8" },
);
process.stdout.write(delegated.stdout || "");
process.stderr.write(delegated.stderr || "");
process.exit(delegated.status ?? 1);
