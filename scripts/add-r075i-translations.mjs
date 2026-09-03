#!/usr/bin/env node

import { execFileSync } from "node:child_process";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const checkOnly = process.argv.includes("--check-only");
const output = execFileSync(process.execPath, [
  resolve(root, "scripts/add-r075i-step34-translations.mjs"),
  ...(checkOnly ? ["--check-only"] : []),
], { cwd: root, encoding: "utf8" });

process.stdout.write(output);
