#!/usr/bin/env node

import { readFile } from "node:fs/promises";
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
  --status <release-id>            Read compact local pipeline status; no network or writes
  --verbose                        Emit one progress line per stage
  --json                           Emit the complete receipt/status JSON
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
    else if (argument === "--status") options.statusReleaseId = next();
    else if (argument === "--through") options.through = next();
    else if (argument === "--verify-existing") options.verifyExisting = true;
    else if (argument === "--allow-commit") options.allowCommit = true;
    else if (argument === "--allow-push") options.allowPush = true;
    else if (argument === "--no-cache") options.noCache = true;
    else if (argument === "--json") options.json = true;
    else if (argument === "--verbose") options.verbose = true;
    else if (argument === "--deployment-timeout-seconds") {
      options.deploymentTimeoutMs = Number(next()) * 1000;
    } else if (argument === "--deployment-poll-seconds") {
      options.deploymentPollMs = Number(next()) * 1000;
    } else if (argument === "--help") options.help = true;
    else throw new Error(`unknown argument ${argument}`);
  }
  if (!options.help && !options.handoffPath && !options.statusReleaseId) {
    throw new Error("--handoff or --status is required");
  }
  if (options.handoffPath && options.statusReleaseId) {
    throw new Error("--handoff and --status are mutually exclusive");
  }
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
    stageCount: receipt.stages.length,
    failureCount: receipt.errors.length,
    logCount: receipt.logs?.length ?? 0,
    durationMs: Date.parse(receipt.completedAt) - Date.parse(receipt.startedAt),
    receipt: receipt.receiptPath,
  };
}

async function readStatus(releaseId) {
  if (!/^(?:r0\d{2}[a-z]|[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d{8})$/.test(releaseId)) {
    throw new Error("invalid release id");
  }
  const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));
  const statePath = resolve(root, ".release", "state", `${releaseId}.json`);
  const receiptPath = resolve(root, ".release", "receipts", `${releaseId}.json`);
  const state = await readJson(statePath);
  let receipt = null;
  try {
    receipt = await readJson(receiptPath);
  } catch (error) {
    if (error.code !== "ENOENT") throw error;
  }
  return {
    releaseId,
    state: state.currentState,
    failedStage: state.failedStage ?? null,
    updatedAt: state.updatedAt ?? null,
    publicationCommit: receipt?.publicationCommit ?? null,
    failureCount: receipt?.errors?.length ?? 0,
    receipt: receipt ? `.release/receipts/${releaseId}.json` : null,
    statePath: `.release/state/${releaseId}.json`,
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
    if (options.statusReleaseId) {
      const status = await readStatus(options.statusReleaseId);
      process.stdout.write(options.json
        ? JSON.stringify(status, null, 2) + "\n"
        : `STATUS release=${status.releaseId} state=${status.state} failedStage=${status.failedStage ?? "none"} commit=${status.publicationCommit ?? "none"} failures=${status.failureCount} stateFile=${status.statePath} receipt=${status.receipt ?? "none"}\n`);
      return;
    }
    const receipt = await runReleasePipeline({
      ...options,
      root,
      onProgress: options.verbose ? (stage) => {
        process.stderr.write(
          `[release] ${stage.name} ${stage.status.toUpperCase()}${stage.cached ? " (cache)" : ""} ${stage.durationMs}ms\n`,
        );
      } : undefined,
    });
    if (options.json) {
      process.stdout.write(JSON.stringify(receipt, null, 2) + "\n");
    } else {
      const compact = compactReceipt(receipt);
      process.stdout.write(`PASS release=${compact.releaseId} state=${compact.state} stages=${compact.stageCount} cached=${compact.cachedStages.length} commit=${compact.publicationCommit ?? "none"} failures=${compact.failureCount} receipt=${compact.receipt} logs=${compact.logCount}\n`);
    }
  } catch (error) {
    if (error instanceof ReleasePipelineError) {
      process.stderr.write(`FAIL stage=${error.stage} failures=${error.failures.length} receipt=${error.receiptPath ?? "unavailable"}\n`);
    } else {
      process.stderr.write(`FAIL error=${error.message}\n`);
    }
    process.exitCode = 1;
  }
}

const invokedDirectly = process.argv[1] && pathToFileURL(resolve(process.argv[1])).href === import.meta.url;
if (invokedDirectly) await main();
