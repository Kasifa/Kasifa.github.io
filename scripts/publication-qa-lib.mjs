#!/usr/bin/env node

import { createHash } from "node:crypto";
import { createReadStream, existsSync } from "node:fs";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { dirname, extname, relative, resolve } from "node:path";

const require = createRequire(import.meta.url);
const DEFAULT_PLAYWRIGHT =
  "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright";
const DEFAULT_CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const CONTENT_TYPES = new Map([
  [".html", "text/html; charset=utf-8"],
  [".js", "text/javascript; charset=utf-8"],
  [".css", "text/css; charset=utf-8"],
  [".svg", "image/svg+xml"],
  [".png", "image/png"],
  [".pdf", "application/pdf"],
  [".json", "application/json"],
]);

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

function safeRelativePath(value, label) {
  if (typeof value !== "string" || value.length === 0 || value.startsWith("/") ||
      value.includes("\\") || value.split("/").includes("..")) {
    throw new Error(`${label} must be a safe repository-relative path`);
  }
  return value;
}

async function atomicJson(path, value) {
  await mkdir(dirname(path), { recursive: true });
  const temporary = `${path}.tmp-${process.pid}`;
  await writeFile(temporary, JSON.stringify(value, null, 2) + "\n");
  await rename(temporary, path);
}

function timestamp() {
  return new Date().toISOString().replaceAll(":", "-");
}

export async function loadPublicationQaConfig(root, configPath) {
  safeRelativePath(configPath, "config path");
  const config = JSON.parse(await readFile(resolve(root, configPath), "utf8"));
  if (config.schemaVersion !== "publication-qa-config-v1") {
    throw new Error("unsupported publication QA config schema");
  }
  if (typeof config.releaseId !== "string" ||
      !/^(?:r0\d{2}[a-z]|[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*-\d{8})$/.test(config.releaseId)) {
    throw new Error("publication QA config releaseId is invalid");
  }
  if (!Array.isArray(config.online?.expectedLive) || config.online.expectedLive.length === 0) {
    throw new Error("publication QA config online.expectedLive must be nonempty");
  }
  if (!Array.isArray(config.browser?.targets) || config.browser.targets.length === 0) {
    throw new Error("publication QA config browser.targets must be nonempty");
  }
  if (!Array.isArray(config.browser?.scenarios) || config.browser.scenarios.length === 0) {
    throw new Error("publication QA config browser.scenarios must be nonempty");
  }
  const checkIds = config.browser.targets.flatMap((target) =>
    config.browser.scenarios.map((scenario) => `${target.id}-${scenario.id}`));
  const safeId = (value) => typeof value === "string" && /^[A-Za-z0-9]+(?:-[A-Za-z0-9]+)*$/.test(value);
  if (config.browser.targets.some((target) => !safeId(target.id)) ||
      config.browser.scenarios.some((scenario) => !safeId(scenario.id)) ||
      new Set(checkIds).size !== checkIds.length) {
    throw new Error("publication QA browser target/scenario ids must be present and unique");
  }
  return config;
}

function reportPath(root, config, kind) {
  return resolve(root, ".release", "reports", config.releaseId, `${kind}-${timestamp()}.json`);
}

function relativeReportPath(root, path) {
  return relative(root, path).replaceAll("\\", "/");
}

async function writeReport(root, config, kind, report) {
  const path = reportPath(root, config, kind);
  report.reportPath = relativeReportPath(root, path);
  await atomicJson(path, report);
  await atomicJson(resolve(root, ".release", "reports", config.releaseId, `${kind}-latest.json`), report);
  return relativeReportPath(root, path);
}

function cacheBustedUrl(baseUrl, urlPath, commit) {
  const url = new URL(urlPath, baseUrl);
  url.searchParams.set("publication-qa", `${commit.slice(0, 12)}-${Date.now()}`);
  return url;
}

export async function runOnlineQa({ root, configPath, commit, baseUrl }) {
  const config = await loadPublicationQaConfig(root, configPath);
  const startedAt = new Date().toISOString();
  const origin = new URL(baseUrl ?? config.siteBaseUrl);
  const live = config.online?.expectedLive ?? [];
  const results = await Promise.all(live.map(async (item) => {
    const local = await readFile(resolve(root, safeRelativePath(item.localPath, "online localPath")));
    const response = await fetch(cacheBustedUrl(origin, item.urlPath, commit), {
      redirect: "follow",
      headers: { "Cache-Control": "no-cache" },
    });
    const actual = Buffer.from(await response.arrayBuffer());
    const contentType = response.headers.get("content-type") ?? "";
    const errors = [];
    if (response.status !== 200) errors.push(`HTTP ${response.status}`);
    if (!(item.contentTypes ?? []).some((prefix) =>
      contentType.toLowerCase().startsWith(prefix.toLowerCase()))) {
      errors.push(`content-type ${contentType}`);
    }
    if (!actual.equals(local)) errors.push(`SHA-256 ${sha256(actual)} != ${sha256(local)}`);
    return {
      role: item.role,
      localPath: item.localPath,
      urlPath: item.urlPath,
      statusCode: response.status,
      contentType,
      expectedBytes: local.length,
      onlineBytes: actual.length,
      expectedSha256: sha256(local),
      onlineSha256: sha256(actual),
      exact: errors.length === 0,
      errors,
      body: item.role === "site-version" ? actual.toString("utf8") : undefined,
    };
  }));
  const absent = await Promise.all((config.online?.expectedAbsent ?? []).map(async (urlPath) => {
    const response = await fetch(cacheBustedUrl(origin, urlPath, commit), {
      redirect: "manual",
      headers: { "Cache-Control": "no-cache" },
    });
    return { urlPath, statusCode: response.status, exact: response.status === 404 };
  }));
  const failures = results.flatMap((item) => item.errors.map((message) => ({
    label: item.urlPath,
    message,
  })));
  for (const item of absent.filter((entry) => !entry.exact)) {
    failures.push({ label: item.urlPath, message: `expected 404, got ${item.statusCode}` });
  }
  const siteVersion = results.find((item) => item.role === "site-version");
  try {
    const payload = JSON.parse(siteVersion?.body ?? "");
    for (const [key, expected] of Object.entries(config.online?.siteVersionExpectations ?? {})) {
      if (payload[key] !== expected) {
        failures.push({ label: "site-version", message: `${key}=${payload[key]} != ${expected}` });
      }
    }
  } catch (error) {
    failures.push({ label: "site-version", message: `invalid JSON: ${error.message}` });
  }
  const report = {
    schemaVersion: "publication-online-qa-v1",
    status: failures.length === 0 ? "PASS" : "FAIL",
    releaseId: config.releaseId,
    commit,
    baseUrl: origin.href,
    startedAt,
    completedAt: new Date().toISOString(),
    objectCount: results.length,
    exactCount: results.filter((item) => item.exact).length,
    absentCount: absent.length,
    results: results.map((item) => {
      const publicItem = { ...item };
      delete publicItem.body;
      return publicItem;
    }),
    absent,
    failures,
  };
  report.reportPath = await writeReport(root, config, "online", report);
  return report;
}

function loadPlaywright() {
  const modulePath = process.env.RELEASE_PLAYWRIGHT_MODULE ?? DEFAULT_PLAYWRIGHT;
  return require(modulePath);
}

async function localServer(root) {
  const publicRoot = resolve(root, "public");
  const server = createServer((request, response) => {
    const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
    const repositoryPath = pathname === "/" ? "research-review.html" : pathname.replace(/^\/+/, "");
    const target = resolve(publicRoot, repositoryPath);
    if (!target.startsWith(`${publicRoot}/`)) return response.writeHead(403).end();
    response.setHeader("Content-Type", CONTENT_TYPES.get(extname(target).toLowerCase()) ?? "application/octet-stream");
    const stream = createReadStream(target);
    stream.on("error", () => response.writeHead(404).end());
    stream.pipe(response);
  });
  await new Promise((resolvePromise, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolvePromise);
  });
  return { server, baseUrl: new URL(`http://127.0.0.1:${server.address().port}/`) };
}

function matchesAll(text, patterns) {
  return (patterns ?? []).filter((pattern) => !new RegExp(pattern, "iu").test(text));
}

export async function runBrowserQa({ root, configPath, commit, baseUrl }) {
  const config = await loadPublicationQaConfig(root, configPath);
  const startedAt = new Date().toISOString();
  let server;
  let origin;
  if (baseUrl) {
    origin = new URL(baseUrl);
  } else {
    ({ server, baseUrl: origin } = await localServer(root));
  }
  const { chromium } = loadPlaywright();
  const launch = { headless: true };
  const chrome = process.env.RELEASE_CHROME_EXECUTABLE ?? DEFAULT_CHROME;
  if (existsSync(chrome)) launch.executablePath = chrome;
  const browser = await chromium.launch(launch);
  const checks = [];
  const runId = startedAt.replaceAll(":", "-");
  const screenshotRoot = resolve(root, ".release", "screenshots", config.releaseId, commit, runId);
  await mkdir(screenshotRoot, { recursive: true });
  try {
    for (const target of config.browser?.targets ?? []) {
      for (const scenario of config.browser?.scenarios ?? []) {
        const id = `${target.id}-${scenario.id}`;
        const context = await browser.newContext({
          viewport: scenario.viewport,
          colorScheme: scenario.colorScheme,
          locale: scenario.lang === "zh" ? "zh-CN" : "en-US",
        });
        const page = await context.newPage();
        const pageErrors = [];
        page.on("pageerror", (error) => pageErrors.push(error.message));
        const failures = [];
        try {
          const url = new URL(target.path, origin);
          url.searchParams.set("lang", scenario.lang);
          url.searchParams.set("publication-qa", `${config.releaseId}-${Date.now()}`);
          const response = await page.goto(url.href, { waitUntil: "networkidle" });
          if (response?.status() !== 200) failures.push(`main document HTTP ${response?.status()}`);
          await page.waitForFunction(() => document.documentElement.dataset.language);
          await page.evaluate(async () => {
            if (window.MathJax?.startup?.promise) await window.MathJax.startup.promise;
            if (window.MathJax?.typesetPromise) await window.MathJax.typesetPromise();
          });
          const audit = await page.evaluate(({ target, lang }) => {
            const body = document.body.cloneNode(true);
            body.querySelectorAll(".language-switcher").forEach((node) => node.remove());
            const liveScope = target.languageScoped
              ? document.querySelector(`main[data-language="${lang}"]`)
              : body;
            const text = liveScope?.innerText ?? "";
            return {
              selectedLanguage: document.documentElement.dataset.language,
              documentLanguage: document.documentElement.lang,
              heading: liveScope?.querySelector("h1")?.textContent?.trim() ?? "",
              switcher: document.querySelector(".language-switcher")?.textContent?.trim() ?? "",
              overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
              chinese: (text.match(/[\u3400-\u9fff\uf900-\ufaff]/gu) ?? []).length,
              imageCount: liveScope?.querySelectorAll("img").length ?? 0,
              mathNodeCount: liveScope?.querySelectorAll("mjx-container").length ?? 0,
              mathErrorCount: liveScope?.querySelectorAll("mjx-merror, .MathJax_Error").length ?? 0,
              residualTexCount: (text.match(/\\\(|\\\[|\$\$|\\begin\{/gu) ?? []).length,
              requestedDark: window.matchMedia("(prefers-color-scheme: dark)").matches,
              bodyBackground: getComputedStyle(document.body).backgroundColor,
              bodyColor: getComputedStyle(document.body).color,
              text,
              selectors: (target.requiredSelectors ?? []).map((selector) => ({
                selector,
                present: Boolean(document.querySelector(selector)),
              })),
            };
          }, { target, lang: scenario.lang });
          if (audit.selectedLanguage !== scenario.lang) failures.push(`language ${audit.selectedLanguage}`);
          const expectedDocumentLanguage = scenario.lang === "en" ? "en" : "zh-CN";
          if (audit.documentLanguage !== expectedDocumentLanguage) {
            failures.push(`document language ${audit.documentLanguage}`);
          }
          if (audit.overflow) failures.push("horizontal overflow");
          if (audit.requestedDark !== (scenario.colorScheme === "dark")) {
            failures.push(`requested ${scenario.colorScheme} color scheme did not apply`);
          }
          if (audit.bodyBackground === "rgba(0, 0, 0, 0)") failures.push("transparent body background");
          if (scenario.lang === "en" && target.allowChinese !== true && audit.chinese !== 0) {
            failures.push(`${audit.chinese} untranslated Chinese characters`);
          }
          const headingPattern = target.headingPatterns?.[scenario.lang];
          if (headingPattern && !new RegExp(headingPattern, "iu").test(audit.heading)) {
            failures.push(`heading does not match ${headingPattern}`);
          }
          const missing = matchesAll(audit.text, [
            ...(target.requiredTextPatterns?.all ?? []),
            ...(target.requiredTextPatterns?.[scenario.lang] ?? []),
          ]);
          failures.push(...missing.map((pattern) => `missing text pattern ${pattern}`));
          failures.push(...audit.selectors.filter((item) => !item.present)
            .map((item) => `missing selector ${item.selector}`));
          if (target.imageCount !== undefined && audit.imageCount !== target.imageCount) {
            failures.push(`image count ${audit.imageCount} != ${target.imageCount}`);
          }
          if (target.checkMath !== false) {
            if (audit.mathErrorCount !== 0) failures.push(`${audit.mathErrorCount} MathJax errors`);
            if (audit.residualTexCount !== 0) failures.push(`${audit.residualTexCount} residual TeX delimiters`);
            if (target.minimumMathNodes !== undefined && audit.mathNodeCount < target.minimumMathNodes) {
              failures.push(`MathJax nodes ${audit.mathNodeCount} < ${target.minimumMathNodes}`);
            }
          }
          if (pageErrors.length > 0) failures.push(...pageErrors.map((error) => `page error ${error}`));
          const screenshotPath = resolve(screenshotRoot, `${id}.png`);
          await page.screenshot({ path: screenshotPath, fullPage: true });
          checks.push({
            id,
            target: target.id,
            scenario: scenario.id,
            status: failures.length ? "fail" : "pass",
            audit: { ...audit, text: undefined },
            screenshot: relativeReportPath(root, screenshotPath),
            pageErrors,
            failures,
          });
        } catch (error) {
          checks.push({ id, target: target.id, scenario: scenario.id, status: "fail", pageErrors, failures: [error.message] });
        } finally {
          await context.close();
        }
      }
    }
  } finally {
    await browser.close();
    if (server) await new Promise((resolvePromise) => server.close(resolvePromise));
  }
  for (const target of config.browser.targets) {
    const targetChecks = checks.filter((check) => check.target === target.id && check.audit);
    const lightBackgrounds = new Set(targetChecks
      .filter((check) => check.audit.requestedDark === false).map((check) => check.audit.bodyBackground));
    const darkBackgrounds = new Set(targetChecks
      .filter((check) => check.audit.requestedDark === true).map((check) => check.audit.bodyBackground));
    if ([...lightBackgrounds].some((value) => darkBackgrounds.has(value))) {
      for (const check of targetChecks) {
        check.status = "fail";
        check.failures.push("light and dark themes resolve to the same body background");
      }
    }
  }
  const failures = checks.filter((check) => check.status !== "pass")
    .flatMap((check) => check.failures.map((message) => ({ label: check.id, message })));
  const report = {
    schemaVersion: "publication-browser-qa-v1",
    status: failures.length === 0 ? "PASS" : "FAIL",
    releaseId: config.releaseId,
    publicationCommit: commit,
    baseUrl: origin.href,
    startedAt,
    completedAt: new Date().toISOString(),
    pageChecks: checks.length,
    checks,
    defects: failures,
  };
  if (checks.length === 0) {
    report.status = "FAIL";
    report.defects.push({ label: "browser", message: "zero browser checks executed" });
  }
  report.reportPath = await writeReport(root, config, "browser", report);
  const evidencePath = config.browser?.evidencePath;
  if (evidencePath) {
    safeRelativePath(evidencePath, "browser evidencePath");
    await atomicJson(resolve(root, evidencePath), {
      schemaVersion: "publication-visual-qa-v1",
      releaseId: config.releaseId,
      publicationCommit: commit,
      inspectedAt: report.completedAt,
      checks: checks.filter((check) => check.status === "pass").map((check) => ({
        id: check.id,
        status: "pass",
        method: "fresh automated browser QA",
      })),
      defects: failures,
    });
  }
  return report;
}

export function parseQaArguments(arguments_) {
  const options = {};
  for (let index = 0; index < arguments_.length; index += 1) {
    const argument = arguments_[index];
    const next = () => {
      const value = arguments_[++index];
      if (!value) throw new Error(`${argument} requires a value`);
      return value;
    };
    if (argument === "--config") options.configPath = next();
    else if (argument === "--commit") options.commit = next();
    else if (argument === "--base-url") options.baseUrl = next();
    else if (argument === "--json") options.json = true;
    else throw new Error(`unknown argument ${argument}`);
  }
  if (!options.configPath) throw new Error("--config is required");
  if (!options.commit) throw new Error("--commit is required");
  if (!/^(?:[0-9a-f]{40}|unversioned)$/.test(options.commit)) {
    throw new Error("--commit must be a full Git SHA-1 or unversioned");
  }
  return options;
}

export async function runQaCli(kind, root, arguments_ = process.argv.slice(2)) {
  let report;
  try {
    const options = parseQaArguments(arguments_);
    report = kind === "online"
      ? await runOnlineQa({ root, ...options })
      : await runBrowserQa({ root, ...options });
    if (options.json) {
      process.stdout.write(JSON.stringify(report, null, 2) + "\n");
    } else {
      const count = kind === "online"
        ? `${report.exactCount}/${report.objectCount} objects; ${report.absentCount} absent`
        : `${report.checks.filter((check) => check.status === "pass").length}/${report.pageChecks} pages`;
      process.stdout.write(`${report.status} ${kind} release=${report.releaseId} ${count} commit=${report.commit ?? report.publicationCommit} failures=${report.failures?.length ?? report.defects?.length ?? 0} report=${report.reportPath}\n`);
    }
    if (report.status !== "PASS") process.exitCode = 1;
  } catch (error) {
    process.stderr.write(`FAIL ${kind} error=${error.message}\n`);
    process.exitCode = 1;
  }
  return report;
}
