import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { mkdtempSync, readFileSync, readdirSync, rmSync, statSync } from "node:fs";
import { tmpdir } from "node:os";
import { join, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");
const python = process.env.CODEX_PYTHON || "python3";
const figureId = "fig-r075a-local-persistence-payment";

const frozen = {
  "research/r075a_publication_handoff.md": "489b2f4b67d88974c555ea22e543906b9cd5cd469f135562fdca6c2aad0ad581",
  "research/r075a_spectral_persistence_payment_dichotomy.md": "f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388",
  "research/r075a_spectral_persistence_payment_dichotomy_primary_audit.md": "c599a1dcee8a82ec1c91512d5b664b1394707fd6d69ac2ca7ba022ebf715d3f6",
  "research/r075a_spectral_persistence_payment_dichotomy_literature_audit.md": "169eff2e607338ae990fb9994db3f75e11830246a36ee5cce8a7376e64302cea",
  "research/r075a_spectral_route_risk_audit.md": "ff712f4a846e70a35a5936348574b77ca59ca78c46e56c488ebb4731650afd35",
  "research/r075a_spectral_persistence_payment_dichotomy_certificate.json": "7f504c91bcfcb8ba463c0dec977d946d8f36b26b4f732a2082863bbe5221a38e",
  "research/r075a_spectral_persistence_payment_dichotomy_certificate_report.md": "bfb87b97e661703c4a7ddd6231b50058dfe116d0d9343d9a6e4c1554714ef238",
  "research/r075a_spectral_persistence_payment_dichotomy_certificate_independent_audit.md": "966335bf8a6e759abda01c61d17ef3be4ee3c76e6dd4396b33d6488874dc4960",
  "research/r075a_spectral_persistence_payment_dichotomy_certificate_qa_report.md": "83cc4ff615823d1ce8b1b87d60004bf310f86b4faac2d876fb49b8deef2f0d84",
  "scripts/r075a_spectral_persistence_payment_dichotomy_certificate.py": "d5256d8ea9db81adc5133e3cce69b9f7089f8ab8a2c5d39f30877815e6052e5a",
  "scripts/r075a_spectral_persistence_payment_dichotomy_certificate_independent.rb": "30d28440b4cba3b0578fa7644cf5539ff6a2806f449c020d6cd1718e553ade27",
  "scripts/r075a_spectral_persistence_payment_dichotomy_certificate_qa.sh": "b9b07e3d1a8d1303111cf1978481530e791f3e14d81b6865674d16f73caa2538",
  "research/r075a_milestone_recap_delta.md": "7dd9ac686d0c599b21992bf7622e862f88caf0480f6e27f2cb82b9aaf844eee1",
  "research/r075a_milestone_recap_delta_independent_audit.md": "f727eb01002772936b5f8aa6e7212e238c7e0e04ab546261232f4abcee9d9b82",
};

test("R0.75A Step 26 frozen authority and exact evidence bytes", () => {
  assert.equal(Object.keys(frozen).length, 14);
  for (const [path, expected] of Object.entries(frozen)) assert.equal(sha(path), expected, path);
});

test("R0.75A Step 26 Python certificate reproduces byte-exactly", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075a-primary-"));
  try {
    const stdout = JSON.parse(execFileSync(python, ["scripts/r075a_spectral_persistence_payment_dichotomy_certificate.py"], {
      cwd: root,
      encoding: "utf8",
      env: {
        ...process.env,
        R075A_JSON: join(outputRoot, "certificate.json"),
        R075A_REPORT: join(outputRoot, "report.md"),
      },
    }));
    assert.deepEqual(stdout, { assertions: 14, mutation: null, verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "certificate.json"))).digest("hex"), frozen["research/r075a_spectral_persistence_payment_dichotomy_certificate.json"]);
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "report.md"))).digest("hex"), frozen["research/r075a_spectral_persistence_payment_dichotomy_certificate_report.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75A Step 26 independent Ruby certificate reproduces", () => {
  const outputRoot = mkdtempSync(join(tmpdir(), "r075a-ruby-"));
  try {
    const stdout = JSON.parse(execFileSync("ruby", ["scripts/r075a_spectral_persistence_payment_dichotomy_certificate_independent.rb"], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, R075A_RUBY_REPORT: join(outputRoot, "independent.md") },
    }));
    assert.deepEqual(stdout, { assertions: 17, mutation: null, verdict: "PASS" });
    assert.equal(createHash("sha256").update(readFileSync(join(outputRoot, "independent.md"))).digest("hex"), frozen["research/r075a_spectral_persistence_payment_dichotomy_certificate_independent_audit.md"]);
  } finally {
    rmSync(outputRoot, { recursive: true, force: true });
  }
});

test("R0.75A formal figure archive is complete and byte-identical across mirrors", () => {
  const canonicalRoot = `research/figures/r075a/${figureId}`;
  const names = readdirSync(resolve(root, canonicalRoot)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  assert.equal(names.reduce((sum, name) => sum + statSync(resolve(root, canonicalRoot, name)).size, 0), 2588462);
  const ledgerRows = readFileSync(resolve(root, canonicalRoot, "SHA256SUMS"), "utf8").trim().split("\n");
  assert.equal(ledgerRows.length, 24);
  for (const row of ledgerRows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, row);
    assert.equal(sha(`${canonicalRoot}/${match[2]}`), match[1], match[2]);
  }
  for (const mirror of [`figures/r075a/${figureId}`, `public/figures/r075a/${figureId}`]) {
    assert.deepEqual(readdirSync(resolve(root, mirror)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
    for (const name of names) assert.equal(sha(`${mirror}/${name}`), sha(`${canonicalRoot}/${name}`), `${mirror}/${name}`);
  }
  assert.equal(sha(`${canonicalRoot}/figure.svg`), "cfbb92394ebbcb5ce9603b3f7df32568e37837c5b2238112b69bfec31f8dfe27");
  assert.equal(sha(`${canonicalRoot}/figure.png`), "81546061c9febeac81ff683e8a7bd0811d7a9f3c10a90db05037febc0ee25d70");
  assert.equal(sha(`${canonicalRoot}/figure.pdf`), "ab588b17586d556744bebe8a5957725f4f92033bc1d0133619710c76aee13f5f");
});
