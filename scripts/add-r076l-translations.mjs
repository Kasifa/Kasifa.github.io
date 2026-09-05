#!/usr/bin/env node

import { execFileSync } from "node:child_process";

const checkOnly = process.argv.includes("--check-only");
const output = execFileSync(
  process.execPath,
  [new URL("./add-r076l-step63-translations.mjs", import.meta.url).pathname, ...(checkOnly ? ["--check-only"] : [])],
  { encoding: "utf8", stdio: ["ignore", "pipe", "inherit"] },
);
process.stdout.write(output);
