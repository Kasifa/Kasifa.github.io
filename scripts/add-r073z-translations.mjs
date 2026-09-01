#!/usr/bin/env node

// Local-direct R0.73Z translation stage. It never imports a network client or
// invokes DGX. Reviewed English copy lives in the captured snapshot.

import { createHash } from "node:crypto";
import { spawnSync } from "node:child_process";
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "./i18n-lib.mjs";

const root = resolve(process.env.R073Z_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const publicDirectory = resolve(root, "public");
const translationPath = resolve(root, "translations/en.json");
const bundlePath = resolve(publicDirectory, "i18n-en.js");
const snapshotPath = resolve(root, "scripts/i18n-snapshots/r073z-missing.json");
const mode = process.argv.length === 2 ? "--apply" : process.argv[2];
if (!["--apply", "--check-only", "--capture-missing"].includes(mode)) {
  throw new Error("usage: add-r073z-translations.mjs [--apply|--check-only|--capture-missing]");
}

// Reviewed in source order after the R0.73Z generate stage. Mathematical and
// URL tokens are copied byte-for-byte so the strict i18n guard can compare
// their ordered protected-token ledgers.
const reviewedLocalEnglish = [
  String.raw`Literature review v1.66 · 2026-09-01`,
  String.raw`The scaling and smooth-cylinder properties of the original D_s^{3/2} candidate are valid, but exact Leray--Hopf shear rules out finiteness at the initial endpoint for the general energy class. The global periodic upper bound for D_s√k_s is paid by Leray energy. A crossed classical exact family simultaneously has zero production and nonzero designated pressure covariance. The bounded search did not locate the same mixed observable; a non-hit is not proof of novelty or priority.`,
  String.raw`R0.73Z claim boundary`,
  String.raw`R0.73Z: initial-endpoint obstruction, energy repair, and pressure-active separation for positive covariance`,
  String.raw`202 public research notes; latest node R0.73Z.`,
  String.raw`The index itself is not counted as a research note. Forty-four early notes still have no matching PDF; they are explicitly labeled as historical HTML-only pages and no broken download links are emitted.`,
  String.raw`Research-note index · v1.66 · 2026-09-01`,
  String.raw`Finiteness obstruction for a positive cubic heat covariance and an energy-compatible repair`,
  String.raw`Latest node R0.73Z · continuously revised`,
  String.raw`The use of \(\sqrt{k_{\rm sgs}}\) as an unresolved velocity scale in LES models;`,
  String.raw`\(D^{3/2}\) contributes \(\lambda^6\), \(dt\,dx\,ds\) contributes \(\lambda^{-7}\), and \(R^{-1}\) contributes \(\lambda\), so the total degree is zero. For amplitude \(A\),`,
  String.raw`\[ D_s(x)\sqrt{k_s(x)}=0 \quad\Longleftrightarrow\quad u(t,\cdot)\ \text{is spatially constant}. \tag{4.6} \]`,
  String.raw`Can the global energy upper bound for \(\mathcal K_D^\square\) be localized to \(\mathcal E^\square(z_0,4R)^{3/2}\) plus a minimal, explicit, scale-compatible exterior velocity/gradient tail, and can it pay the \(Q_s\cdot\nabla\chi\) activated by the crossed witness?`,
  String.raw`Downgrade first-jet coercivity to a centered-oscillation product bound.`,
  String.raw`State the integrated kernel as spatial constants for almost every time;`,
  String.raw`Embed this loss of compactness into a single solution by taking`,
  String.raw`Version R0.73Z · 2026-09-01`,
  String.raw`The following components cannot be claimed as new in this section:`,
  String.raw`The repair established here is`,
  String.raw`This section proves an initial-endpoint obstruction, an energy-compatible positive cubic observable, and a pressure-active separation witness. It does not prove CKN coercivity, epsilon regularity, singularity formation, or arbitrary three-dimensional global regularity. NOT CLAY.`,
  String.raw`Direct conclusions of this section`,
  String.raw`Supply the suitable-limit argument;`,
  String.raw`The initial trace can diverge; the repaired quantity D`,
  String.raw`The initial data belong to \(L^2\). The local energy identity for finite Fourier truncations passes to the strong limit in \(L_t^\infty L_x^2\cap L_t^2H_x^1\), so this solution is suitable. On the other hand, each disjoint interval`,
  String.raw`From divergence at the initial endpoint to an energy-class finite observable and a pressure-active separation witness`,
  String.raw`On the three-dimensional torus, however,`,
  String.raw`It fails the energy-class finiteness gate. There is an exact shear with zero pressure that is global Leray--Hopf and suitable, and smooth for every \(t>0\), such that`,
  String.raw`The local lower bound currently available`,
  String.raw`A strict energy-class upper bound follows`,
  String.raw`Second, it gives a positive cubic observable that genuinely belongs to the Leray energy class, and proves its exact kernel and local centered-oscillation lower bound. The pressure-active crossed witness also shows that the repair cannot merely quotient out zero-pressure shears; pressure covariance must be paid separately.`,
  String.raw`First, it closes a natural-looking candidate that is unstable at the energy level: the smooth properties of \(D_s^{3/2}\) are correct, but they do not automatically cross the \(L^2\) initial endpoint. This prevents further work from being built on an undefined-or-infinite epsilon input.`,
  String.raw`Frozen proofs, audits, and certificates`,
  String.raw`The independent audit recomputed the endpoint divergence, energy upper bound, exact kernel, and local Gaussian lower bound. It required and verified three corrections:`,
  String.raw`Endpoint obstruction, energy repair, and pressure-active separation`,
  String.raw`Apply a core/exterior Gaussian annulus split simultaneously to \(k_s\) and \(D_s\);`,
  String.raw`For \(x,y\in B_R\), one lifted Gaussian term satisfies`,
  String.raw`Direct progress on the Clay problem remains limited. We still do not have local CKN coercivity, compactness, epsilon regularity, or global smoothness for arbitrary suitable weak solutions. As a paper direction, this package is stronger than R0.73Y because it combines an exact endpoint obstruction, an energy-compatible positive theorem, and a pressure-active separation witness; deeper citation-chain auditing and a genuine local payment theorem are still required before any high-level novelty claim.`,
  String.raw`Under NSE scaling`,
  String.raw`For fixed \(t,s>0\), strict positivity of the periodic heat kernel also gives`,
  String.raw`This holds for every \(T_*>0\) and every fixed positive scale band \(0<s_0<s_1\). Divergence occurs only when the time interval touches the \(L^2\) initial trace; it is not an interior singularity and does not contradict smooth-cylinder finiteness.`,
  String.raw`This holds for all \(t,x,s>0\). But the pressure--velocity covariance defined here`,
  String.raw`For every nontrivial periodic smooth field, the positive-scale kernel consists only of constant vectors.`,
  String.raw`Exact cubic homogeneity in amplitude;`,
  String.raw`Exact initial-endpoint counterexample`,
  String.raw`Two pressure-covariance components;`,
  String.raw`Two bounded primary-source audits did not locate the identical \(D_s^{3/2}\) or \(D_s\sqrt{k_s}\) local scale-space functional, nor the same three-part statement \(\Pi_s=\mathscr S_s=0\), \(Q_s\ne0\) on one classical crossed witness. This is only a bounded non-hit, not a novelty proof.`,
  String.raw`Let \(r=e^{-n^2s}\). Gaussian factorization gives`,
  String.raw`Energy-compatible repair`,
  String.raw`Here \(A_t=Ae^{-\nu n^2t}\) and \(B_t=Be^{-\nu n^2t}\). If \(AB\ne0\), then \(Q_s\not\equiv0\). At \(A_t=B_t>0\) and \(nx_1=nx_2=\pi/3\),`,
  String.raw`Determine whether the exterior gradient tail follows from the R0.73X velocity/pressure tail or must be introduced as an independent debt;`,
  String.raw`If the cylinder closure lies compactly inside the smooth lifespan and`,
  String.raw`The three-dimensional periodic heat-flow \(L^1\to L^\infty\) estimate gives`,
  String.raw`On this interval, \(\|G_n(t)\|_2\gtrsim n\), and therefore`,
  String.raw`The velocity covariance and gradient covariance satisfy`,
  String.raw`Thus \(D_{ii,s}^{3/2}=O(s^{3/2})\), and the \(s=0\) endpoint is integrable.`,
  String.raw`Hence there is a compact nonnegative bump \(\chi\) such that`,
  String.raw`Thus this is an exact NSE trajectory. The solution itself is not new: the equal-amplitude case is the classical two-dimensional Taylor--Green representation, and general \(A,B\) are steady Euler flows in one Laplacian eigenspace under viscous decay.`,
  String.raw`It retains nonnegativity, scale invariance, and cubic homogeneity, while being controlled directly by Leray energy. This is a genuine positive estimate, but it is still not CKN coercivity.`,
  String.raw`It also exactly verifies the high-frequency energy constant \(6\pi^3\), together with`,
  String.raw`The gradient covariance is the strictly nonnegative heat variance`,
  String.raw`It passes three formal gates:`,
  String.raw`For the same witness, the positive covariance is`,
  String.raw`The 201 plotted rows are deterministic evaluations of analytic formulas, not DNS, simulation, a singularity candidate, or proof by finite sampling. NOT CLAY.`,
  String.raw`Both quantities are independent of \(n\). Therefore no finite cubic upper bound depending only on bare energy can pass uniformly through the initial endpoint.`,
  String.raw`Summing infinitely many disjoint contributions yields (1.2).`,
  String.raw`The next section attacks only one interface:`,
  String.raw`First consider the smooth high-frequency family`,
  String.raw`After restricting both variances to \(B_R\),`,
  String.raw`The point of the repair is not a formal splice: it replaces the unusable time demand \(\|\nabla u\|_2^3\) by the Leray-integrable quantity \(\|u\|_2\|\nabla u\|_2^2\).`,
  String.raw`Research note R0.73Z · EXACT ANALYTIC THEOREMS / FINITE CERTIFICATE`,
  String.raw`Proceed in this order:`,
  String.raw`Therefore both \(\mathcal D_{3/2}\) and \(\mathcal K_D\) eliminate this pressure-active production kernel.`,
  String.raw`Thus, at the general suitable-weak level, \(\mathcal D_{3/2}\) must first be treated as a nonnegative functional with values in \([0,+\infty]\). It cannot be declared a finite epsilon-regularity input without proof.`,
  String.raw`Hence on every nondegenerate time interval, \(\mathcal K_D=0\) if and only if the velocity is spatially constant for almost every physical time. For unforced periodic NSE, this is a time-independent Galilean mode.`,
  String.raw`It is paid by Leray energy, while the crossed exact family separates the pressure-cutoff debt.`,
  String.raw`we have`,
  String.raw`Finiteness obstruction and repair proof`,
  String.raw`Original candidate D`,
  String.raw`Why the original candidate is correct in the smooth class`,
  String.raw`On`,
  String.raw`Test the amplitude and \(R\)-scaling of every term exactly on the crossed family;`,
  String.raw`At L`,
  String.raw`Dimensionless under Navier--Stokes scaling;`,
  String.raw`On a fixed positive scale band \(s\in[s_0,s_1]\), the periodic heat kernel has a positive lower bound. Let \(G_n=\partial_2u_1^{(n)}\); then`,
  String.raw`The boundary of this counterexample must be preserved: after any \(\delta>0\), the solution is analytic on \([\delta,T_*]\), and the original functional is finite. The interior-cylinder assumption of R0.73X has not been broken by a known singular solution.`,
  String.raw`All these properties are valid; the failure concerns suitable-weak finite-valuedness, not formal scaling.`,
  String.raw`This proves that local pressure-cutoff debt can reactivate even when both production channels vanish pointwise.`,
  String.raw`This is only a centered-oscillation product lower bound. It is not a first-jet quotient under one group action; a locally affine profile makes \(G_R=0\) and completely degenerates the right-hand side. No CKN coercivity is claimed here.`,
  String.raw`Prove the local upper payment or give an exact counterexample;`,
  String.raw`Proofs, finite certificates, open problems, and the Clay boundary are kept separate`,
  String.raw`The certificate is an executable cross-check of the analytic proof and does not carry universal quantifiers.`,
  String.raw`Certificate and audit`,
  String.raw`Only after the payment closes should quotient coercivity be reconsidered.`,
  String.raw`contributes at least a fixed multiple of`,
  String.raw`completes 12 exact checks:`,
  String.raw`Status · R0.73Z complete`,
  String.raw`The deterministic certificate works in`,
  String.raw`Gaussian scale as heat time and exact stress evolution;`,
  String.raw`Heat-semigroup Besov/carré-du-champ framework;`,
  String.raw`Positive Gaussian covariance and realizability;`,
  String.raw`Pressure-active separation witness`,
  String.raw`The exact shear in R0.73Y has \(p=Q_s=0\). This section instead takes`,
  String.raw`The candidate frozen in R0.73Y`,
  String.raw`R0.73Z has two reliable increments.`,
  String.raw`R0.74A frozen task`,
  String.raw`The resolved gradient has only two off-diagonal entries, so`,
  String.raw`Separate accounting for signed production and positive viscous covariance;`,
  String.raw`Third centered-flux divergence and centered production;`,
  String.raw`Index of 202 research notes`,
  String.raw`80 sections fully sealed`,
  String.raw`View the full R0.73Z card on the homepage`,
  String.raw`Current endpoint R0.73Z`,
  String.raw`Jump to the R0.73Z homepage card →`,
  String.raw`Next publication gate (R0.74A):`,
  String.raw`The next section attacks only one interface: localize the global energy upper bound for K_D to E^square(z_0,4R)^{3/2} plus a minimal, explicit, scale-compatible exterior velocity/gradient tail, and use it to pay the Q_s·∇χ activated by the crossed witness. First complete the core/exterior split and crossed-family scaling test. If local payment fails, publish an exact counterexample and do not restart quotient coercivity prematurely.`,
  String.raw`Research note R0.73Z · 2026-09-01`,
  String.raw`The original \(D_{ii,s}^{3/2}\) is finite on smooth cylinders but may diverge at the energy-class initial trace. The repaired \(D_{ii,s}\sqrt{k_s}\) retains nonnegativity, scale invariance, and cubic homogeneity, and is paid directly by Leray energy.`,
  String.raw`Read research note R0.73Z →`,
  String.raw`Read the latest R0.73Z research note →`,
  String.raw`Proof boundary:`,
  String.raw`A crossed exact NSE family satisfies \(\Pi_s=\mathscr S_s=0\), but its designated pressure covariance and local cutoff debt are nonzero. Thus quotienting only the zero-pressure shear kernel is insufficient.`,
  String.raw`The D_{ii,s}^{3/2} candidate has correct scaling, cubic homogeneity, and detects the shear kernel, but may diverge at the L² initial trace. The repaired D_{ii,s}√k_s retains positivity and critical homogeneity and is paid by Leray energy; the crossed exact family further shows that pressure-cutoff debt must be settled separately. NOT CLAY.`,
  String.raw`R0.70A–R0.73Z · 104 sections published`,
  String.raw`R0.70A–R0.73Z: 104 sections published, 80 fully sealed`,
  String.raw`R0.73Y closed production-only coercivity. R0.73Z further proves that D_{ii,s}^{3/2} can diverge at the energy-class initial trace and establishes D_{ii,s}√k_s as a positive cubic repair paid by Leray energy. The crossed pressure-active exact family shows that local pressure debt still requires separate settlement. NOT CLAY.`,
  String.raw`R0.73Z closes energy-class initial-endpoint finiteness for D_{ii,s}^{3/2} negatively and supplies D_{ii,s}√k_s as a positive cubic repair paid by Leray energy. Next, only the local upper payment for K_D and pressure-cutoff debt are addressed; quotient coercivity, epsilon regularity, arbitrary three-dimensional global regularity, and Clay remain OPEN.`,
  String.raw`R0.73Z: initial-endpoint finiteness obstruction, energy-compatible positive cubic repair, and pressure-active separation`,
  String.raw`R0.73Z | Finiteness obstruction for a positive cubic heat covariance and an energy-compatible repair`,
  String.raw`R0.74A next interface`,
];

function sha256(value) {
  return createHash("sha256").update(value, "utf8").digest("hex");
}

async function atomicJson(path, value) {
  await mkdir(dirname(path), { recursive: true });
  const temporary = `${path}.tmp-${process.pid}`;
  await writeFile(temporary, JSON.stringify(value, null, 2) + "\n");
  await rename(temporary, path);
}

const source = await collectSiteStrings(publicDirectory);
const translations = JSON.parse(await readFile(translationPath, "utf8"));
const existingByZh = new Map(translations.map((entry) => [entry.zh, entry]));
const missing = source.filter((entry) => !existingByZh.has(entry.zh));

if (mode === "--capture-missing") {
  if (reviewedLocalEnglish.length !== missing.length) {
    throw new Error(`reviewed R0.73Z translation ledger has ${reviewedLocalEnglish.length} rows for ${missing.length} missing strings`);
  }
  let previous = [];
  try { previous = JSON.parse(await readFile(snapshotPath, "utf8")); } catch {}
  const previousByZh = new Map(previous.map((entry) => [entry.zh, entry]));
  const snapshot = missing.map((entry, index) => ({
    zh: entry.zh,
    en: previousByZh.get(entry.zh)?.en || reviewedLocalEnglish[index],
    sourceIdAtCapture: `r073z${String(index + 1).padStart(3, "0")}`,
    capturedEnglishSha256: sha256(previousByZh.get(entry.zh)?.en || reviewedLocalEnglish[index]),
    provenance: "local-direct-reviewed",
    reasonCodes: ["R073Z_RELEASE_BATCH"],
    resolution: "direct-translation",
    reviewNote: "",
    reviewedIssues: [],
    count: entry.count,
    files: entry.files,
  }));
  await atomicJson(snapshotPath, snapshot);
  console.log(JSON.stringify({ captured: snapshot.length, snapshot: "scripts/i18n-snapshots/r073z-missing.json", translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false }));
  process.exit(0);
}

if (mode === "--apply") {
  const snapshot = JSON.parse(await readFile(snapshotPath, "utf8"));
  const snapshotByZh = new Map(snapshot.map((entry) => [entry.zh, entry]));
  const unresolved = missing.filter((entry) => !snapshotByZh.get(entry.zh)?.en?.trim());
  if (unresolved.length) {
    throw new Error(`R0.73Z local-direct snapshot has ${unresolved.length} unresolved string(s); run --capture-missing and review them`);
  }
  let nextId = translations.reduce((maximum, entry) => {
    const number = Number(String(entry.id ?? "").replace(/^s/, ""));
    return Number.isFinite(number) ? Math.max(maximum, number) : maximum;
  }, 0) + 1;
  for (const entry of missing) {
    const reviewed = snapshotByZh.get(entry.zh);
    translations.push({
      id: `s${nextId++}`,
      zh: entry.zh,
      en: reviewed.en.trim(),
      count: entry.count,
      files: entry.files,
    });
  }
  await atomicJson(translationPath, translations);
  const built = spawnSync(process.execPath, ["scripts/build-i18n.mjs", "translations/en.json"], {
    cwd: root,
    encoding: "utf8",
    maxBuffer: 128 * 1024 * 1024,
  });
  if (built.status !== 0) throw new Error(`i18n build failed: ${built.stderr || built.stdout}`);
}

const currentSource = await collectSiteStrings(publicDirectory);
const currentTranslations = JSON.parse(await readFile(translationPath, "utf8"));
const byZh = new Map(currentTranslations.map((entry) => [entry.zh, entry.en?.trim()]));
const invalid = [];
for (const entry of currentSource) {
  const english = byZh.get(entry.zh);
  if (!english) invalid.push(`${entry.zh}: missing`);
  else if (containsChinese(english)) invalid.push(`${entry.zh}: English contains Chinese`);
  else if (JSON.stringify(extractProtectedTokens(entry.zh)) !== JSON.stringify(extractProtectedTokens(english))) {
    invalid.push(`${entry.zh}: protected token drift`);
  }
}
if (invalid.length) throw new Error(`translation validation failed (${invalid.length}):\n${invalid.slice(0, 20).join("\n")}`);
const bundle = await readFile(bundlePath, "utf8");
for (const token of ["R0.73Z", "NOT CLAY", "LOCAL_DIRECT_NO_DGX"]) {
  if (!bundle.includes(token)) throw new Error(`translation bundle missing ${token}`);
}
console.log(JSON.stringify({
  applied: mode === "--apply",
  checked: true,
  sourceStrings: currentSource.length,
  translations: currentTranslations.length,
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
}));
