import { readFile, writeFile } from "node:fs/promises";
import { resolve } from "node:path";

const [, , sourceArgument, outputArgument, missingArgument, ...resultArguments] =
  process.argv;

if (!sourceArgument || !outputArgument || !missingArgument || !resultArguments.length) {
  console.error(
    "Usage: node scripts/merge-i18n.mjs SOURCE OUTPUT MISSING RESULT [RESULT ...]",
  );
  process.exit(1);
}

const sourcePath = resolve(sourceArgument);
const outputPath = resolve(outputArgument);
const missingPath = resolve(missingArgument);
const source = JSON.parse(await readFile(sourcePath, "utf8"));
const translatedByChinese = new Map();

function preserveInitialCase(match, replacement) {
  return /^[A-Z]/.test(match)
    ? replacement[0].toUpperCase() + replacement.slice(1)
    : replacement;
}

function normalizeEnglish(value) {
  const protectedValues = [];
  const maskedValue = value.replace(
    /\\\([\s\S]*?\\\)|\\\[[\s\S]*?\\\]|https?:\/\/[^\s<]+/g,
    (match) => {
      const marker = `__NS_PROTECTED_${protectedValues.length}__`;
      protectedValues.push(match);
      return marker;
    },
  );
  const replacements = [
    [/\bwave numbers\b/gi, "wavenumbers"],
    [/\bwave number\b/gi, "wavenumber"],
    [/\bthree waves\b/gi, "triads"],
    [/\btriplets\b/gi, "triads"],
    [/\btriplet\b/gi, "triad"],
    [/\bspiral triads\b/gi, "helical triads"],
    [/\bre-calculable\b/gi, "reproducible"],
    [/\bresearch station\b/gi, "research site"],
    [/\btriangular polynomial\b/gi, "trigonometric polynomial"],
    [/\btriangular polynomials\b/gi, "trigonometric polynomials"],
    [/\bcritical nucleus\b/gi, "critical kernel"],
    [/\bcritical nuclei\b/gi, "critical kernels"],
    [/\bnuclei\b/gi, "kernels"],
    [/\bnucleus\b/gi, "kernel"],
    [/\bRiemann integral\b/gi, "Riemann sum"],
    [/\bfrequency package\b/gi, "frequency packet"],
    [/\bdiscrete package\b/gi, "discrete packet"],
    [/\bhexagonal package\b/gi, "six-leaf packet"],
    [/\bdense package\b/gi, "dense packet"],
    [/\bgenerating package\b/gi, "generated packet"],
    [/\bquadruplet package\b/gi, "four-leaf packet"],
    [/\btransmission\b/gi, "transfer"],
    [/\bquadratic homogeneous\b/gi, "homogeneous of degree two"],
    [/\bconstant variation\b/gi, "variation of constants"],
    [/\bintegral upper term\b/gi, "upper-limit term in the integral"],
    [/\bmodulus energy\b/gi, "modal energy"],
    [/\banti-aliasing\b/gi, "dealiased"],
    [/\breality symmetry\b/gi, "conjugate symmetry"],
    [/\bsupport external output\b/gi, "out-of-support output"],
    [/\bstagnation point\b/gi, "stationary point"],
    [/\bstrictly not zero\b/gi, "strictly nonzero"],
    [/\bzero undecided boxes\b/gi, "no undecided boxes"],
    [/\bthermal semigroup\b/gi, "heat semigroup"],
    [/\bthermal flow\b/gi, "heat flow"],
    [/\bthermal multiplier\b/gi, "heat multiplier"],
    [/\bthermal integral\b/gi, "heat integral"],
    [/\bhexamode\b/gi, "six-mode"],
    [/\bas machine zero\b/gi, "as zero to machine precision"],
    [/\bgeneration modes\b/gi, "generated modes"],
    [/\bcritical transport\b/gi, "critical transfer"],
    [/\btangential leakage\b/gi, "normal leakage"],
    [/\bentire space\b/gi, "full space"],
    [/\binitial values\b/gi, "initial data"],
    [/\binitial value\b/gi, "initial data"],
    [/\bprecisely non-zero\b/gi, "exactly nonzero"],
    [/\bprecisely nonzero\b/gi, "exactly nonzero"],
    [/\bpolar projections\b/gi, "polarization projections"],
    [/\bpolar projection\b/gi, "polarization projection"],
    [/\bgeneration coefficients\b/gi, "generated coefficients"],
    [/\breal generating coefficients\b/gi, "true generated coefficients"],
    [/\breal generating subspaces\b/gi, "true generated subspaces"],
    [/\breal generating subspace\b/gi, "true generated subspace"],
    [/\breal generation coefficients\b/gi, "true generated coefficients"],
    [/\bthermal terms\b/gi, "heat terms"],
    [/\bthermal term\b/gi, "heat term"],
    [/\bthermal decay\b/gi, "viscous decay"],
    [/\bthermal dissipation\b/gi, "viscous dissipation"],
    [/\bfive-order\b/gi, "fifth-order"],
    [/\bsix-order\b/gi, "sixth-order"],
    [/\bten-order\b/gi, "tenth-order"],
    [/\btwelve-order\b/gi, "twelfth-order"],
  ];
  let normalized = maskedValue
    .trim()
    .replace(/^s\d{1,4}(?=(?:\s|·))/i, "")
    .replace(/\\t/g, " ")
    .replace(/\s*\bEND\b/g, "");
  for (const [pattern, replacement] of replacements) {
    normalized = normalized.replace(pattern, (match) =>
      preserveInitialCase(match, replacement),
    );
  }
  normalized = normalized
    .replace(/。/g, ". ")
    .replace(/，/g, ", ")
    .replace(/；/g, "; ")
    .replace(/：/g, ": ")
    .replace(/、/g, ", ")
    .replace(/\s+([,.;:])/g, "$1")
    .replace(/([,.;:])(?=[A-Za-z])/g, "$1 ")
    .replace(/\.\s*\.(?=\s|$)/g, ".")
    .replace(/\s{2,}/g, " ")
    .trim();
  return normalized.replace(/__NS_PROTECTED_(\d+)__/g, (_, index) =>
    protectedValues[Number(index)],
  );
}

for (const argument of resultArguments) {
  const records = JSON.parse(await readFile(resolve(argument), "utf8"));
  for (const record of records) {
    if (record.zh && record.en?.trim()) {
      const normalizedEnglish = normalizeEnglish(record.en);
      translatedByChinese.set(record.zh, normalizedEnglish);
    }
  }
}

const translated = [];
const missing = [];
for (const item of source) {
  const en = translatedByChinese.get(item.zh);
  if (en) translated.push({ ...item, en });
  else missing.push(item);
}

await Promise.all([
  writeFile(outputPath, `${JSON.stringify(translated, null, 2)}\n`),
  writeFile(missingPath, `${JSON.stringify(missing, null, 2)}\n`),
]);

console.log(
  JSON.stringify(
    {
      source: source.length,
      translated: translated.length,
      missing: missing.length,
      output: outputPath,
      missingOutput: missingPath,
    },
    null,
    2,
  ),
);
