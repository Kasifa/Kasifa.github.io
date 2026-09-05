#!/usr/bin/env node

import { spawnSync } from "node:child_process";
import { resolve } from "node:path";

import { runQaCli } from "./publication-qa-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const publicationCommit = process.env.CLAY_B_SIGNED_SCALE_DEPLOYED_COMMIT ??
  spawnSync("git", ["rev-parse", "HEAD"], { cwd: root, encoding: "utf8" }).stdout.trim();
const arguments_ = process.argv.length > 2 ? process.argv.slice(2) : [
  "--config", "release/qa/clay-b-signed-scale-20260905.json",
  "--commit", publicationCommit,
  ...(process.env.CLAY_B_SIGNED_SCALE_PUBLIC_BASE_URL
    ? ["--base-url", process.env.CLAY_B_SIGNED_SCALE_PUBLIC_BASE_URL]
    : []),
];
await runQaCli("browser", root, arguments_);
