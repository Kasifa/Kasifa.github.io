#!/usr/bin/env node

import { resolve } from "node:path";
import { pathToFileURL } from "node:url";

import { runQaCli } from "./publication-qa-lib.mjs";

const root = resolve(import.meta.dirname, "..");
const invokedDirectly = process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url;
if (invokedDirectly) await runQaCli("online", root);
