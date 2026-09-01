#!/usr/bin/env node

import { resolve } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

import { ReleasePipelineError, STAGES, runReleasePipeline } from "./release-pipeline-lib.mjs";

const root = resolve(fileURLToPath(new URL("../", import.meta.url)));

function usage() {
  return `Usage: node scripts/publish-release.mjs --handoff <repo-relative.json> [options]

Options:
  --through <${STAGES.join("|")}>  Final state-machine stage (default: qa)
  --verify-existing                Read-only verification of an already deployed release
  --allow-commit                   Permit the managed release commit stage
  --allow-push                     Permit the origin/main push stage
  --no-cache                       Re-run every selected stage
  --deployment-timeout-seconds N   GitHub Pages wait timeout (default: 900)
  --deployment-poll-seconds N      GitHub Pages poll interval (default: 10)
  --json                           Emit the complete receipt JSON
  --help                           Show this help
`;
}

export function parseArguments(arguments_) {
  const options = { through: "qa" };
  for (let index = 0; index < arguments_.length; index += 1) {
    const argument = arguments_[index];
    const next = () => {
      const value = arguments_[++index];
      if (!value) throw new Error(`${argument} requires a value`);
      return value;
    };
    if (argument === "--handoff") options.handoffPath = next();
    else if (argument === "--through") options.through = next();
    else if (argument === "--verify-existing") options.verifyExisting = true;
    else if (argument === "--allow-commit") options.allowCommit = true;
    else if (argument === "--allow-push") options.allowPush = true;
    else if (argument === "--no-cache") options.noCache = true;
    else if (argument === "--json") options.json = true;
    else if (argument === "--deployment-timeout-seconds") {
      options.deploymentTimeoutMs = Number(next()) * 1000;
    } else if (argument === "--deployment-poll-seconds") {
      options.deploymentPollMs = Number(next()) * 1000;
    } else if (argument === "--help") options.help = true;
    else throw new Error(`unknown argument ${argument}`);
  }
  if (!options.help && !options.handoffPath) throw new Error("--handoff is required");
  if (!STAGES.includes(options.through)) throw new Error(`unknown --through stage ${options.through}`);
  for (const key of ["deploymentTimeoutMs", "deploymentPollMs"]) {
    if (options[key] !== undefined && (!Number.isFinite(options[key]) || options[key] <= 0)) {
      throw new Error(`${key} must be positive`);
    }
  }
  return options;
}

function compactReceipt(receipt) {
  return {
    schemaVersion: receipt.schemaVersion,
    releaseId: receipt.releaseId,
    state: receipt.finalState,
    publicationCommit: receipt.publicationCommit,
    recapRelease: receipt.recap.latestRecapRelease,
    recapMode: receipt.recap.mode,
    boundaries: receipt.claimBoundary,
    cachedStages: receipt.stages.filter((stage) => stage.cached).map((stage) => stage.name),
    durationMs: Date.parse(receipt.completedAt) - Date.parse(receipt.startedAt),
    receipt: receipt.receiptPath,
  };
}

export async function main(arguments_ = process.argv.slice(2)) {
  let options;
  try {
    options = parseArguments(arguments_);
  } catch (error) {
    process.stderr.write(`${error.message}\n${usage()}`);
    process.exitCode = 2;
    return;
  }
  if (options.help) {
    process.stdout.write(usage());
    return;
  }
  try {
    const receipt = await runReleasePipeline({
      ...options,
      root,
      onProgress(stage) {
        process.stderr.write(
          `[release] ${stage.name} ${stage.status.toUpperCase()}${stage.cached ? " (cache)" : ""} ${stage.durationMs}ms\n`,
        );
      },
    });
    process.stdout.write(
      JSON.stringify(options.json ? receipt : compactReceipt(receipt), null, options.json ? 2 : 0) + "\n",
    );
  } catch (error) {
    if (error instanceof ReleasePipelineError) {
      process.stderr.write(`${error.message}\nreceipt=${error.receiptPath ?? "unavailable"}\n`);
    } else {
      process.stderr.write(`${error.stack ?? error.message}\n`);
    }
    process.exitCode = 1;
  }
}

const invokedDirectly = process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url;
if (invokedDirectly) await main();
