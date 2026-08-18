import { mkdir, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import { collectSiteStrings } from "./i18n-lib.mjs";

const projectRoot = resolve(import.meta.dirname, "..");
const output = resolve(
  process.argv[2] ?? resolve(projectRoot, ".i18n-work", "segments.json"),
);
const entries = await collectSiteStrings(resolve(projectRoot, "public"));
const payload = entries.map((entry, index) => ({
  id: `s${String(index + 1).padStart(4, "0")}`,
  ...entry,
}));

await mkdir(dirname(output), { recursive: true });
await writeFile(output, `${JSON.stringify(payload, null, 2)}\n`);

const characters = payload.reduce((sum, entry) => sum + entry.zh.length, 0);
console.log(
  JSON.stringify(
    { output, segments: payload.length, characters },
    null,
    2,
  ),
);
