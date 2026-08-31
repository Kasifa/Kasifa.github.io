import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import {
  mkdirSync,
  mkdtempSync,
  readFileSync,
  realpathSync,
  rmSync,
  symlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const hash = (relative) => createHash("sha256").update(
  readFileSync(resolve(root, relative)),
).digest("hex");

const title =
  "R0.73U | Full tensors in the heat hierarchy: pressure is recoverable, " +
  "but the even quadratic state is not dynamically closed";
const publicTitle =
  "R0.73U｜完整张量进入热层级：压力可以恢复，但偶二次状态的动力学并不闭合";
const activeTranslationPages = [
  "literature-review.html",
  "notes/index.html",
  "notes/r0-73u.html",
  "recap-r0-61-r0-73u.html",
  "research-review.html",
];

function runPython(...argumentsList) {
  return spawnSync("python3", ["-B", ...argumentsList], {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
}

function pythonJson(...argumentsList) {
  const result = runPython(...argumentsList);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return JSON.parse(result.stdout);
}

function pythonCodeJson(source) {
  return pythonJson("-c", source);
}

function runNode(...argumentsList) {
  return spawnSync(process.execPath, argumentsList, {
    cwd: root,
    encoding: "utf8",
  });
}

test("release content exposes the frozen nine-section boundary without writing", () => {
  const result = pythonJson("scripts/r073u_release_content.py", "--check-only");
  assert.equal(result.release, "R0.73U");
  assert.equal(result.title, title);
  assert.equal(result.publicTitleZh, publicTitle);
  assert.equal(result.canonicalSources, 8);
  assert.equal(result.canonicalSourcesPlanned, 11);
  assert.equal(result.sections, 9);
  assert.equal(result.publicationReady, true);
  assert.deepEqual(result.readinessFailures, []);
  assert.equal(result.heatCovariancePSD, "INTERNAL_EXACT");
  assert.equal(result.heatCovarianceScalePDE, "INTERNAL_EXACT");
  assert.equal(result.sameScalePressureReconstruction, "VERIFIED_CLASSICAL");
  assert.equal(result.conditionalCriticalStressRow, "INTERNAL_COROLLARY");
  assert.equal(result.fixedPositiveScaleEnergyStressBound, "INTERNAL_COROLLARY");
  assert.equal(result.fourSiteQuadraticStateNonAutonomy, "CLOSED_EXACT");
  assert.equal(result.finiteGeneralTensorClosure, "OPEN");
  assert.equal(result.arbitraryThreeDimensionalGlobalRegularity, "OPEN");
  assert.equal(result.clayConclusion, "OPEN");
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.writes, 0);
});

test("canonical text rejects control characters rather than repairing frozen sources", () => {
  const result = pythonCodeJson(`
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, "scripts")
import r073u_release_content as c
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root / "bad.md").write_bytes(b"alpha\\x08beta")
    try:
        c._regular_text(root, "bad.md")
    except c.CanonicalSourceError:
        rejected = True
    else:
        rejected = False
    print(json.dumps({"rejected": rejected}))
`);
  assert.equal(result.rejected, true);
});

test("source-dry-run exposes exact accounting and leaves tracked publication inputs byte-identical", () => {
  const watched = [
    "VERSION",
    "research/release-manifest.json",
    "research/formal-archive-inventory.json",
    "public/site-version.json",
    "public/research-review.html",
    "public/literature-review.html",
    "public/notes/index.html",
  ];
  const before = Object.fromEntries(watched.map((relative) => [relative, hash(relative)]));
  const result = pythonJson("scripts/generate_r073u_release.py", "--source-dry-run");
  const after = Object.fromEntries(watched.map((relative) => [relative, hash(relative)]));
  assert.deepEqual(after, before);
  assert.equal(result.release, "R0.73U");
  assert.equal(result.siteVersion, "1.61");
  assert.equal(result.title, title);
  assert.equal(result.publicTitleZh, publicTitle);
  assert.deepEqual(result.baselineAccounting, {
    latestCompletedRelease: "r073t",
    siteVersion: "1.60",
    publicHtmlNoteCount: 196,
    postR060RecapNodeCount: 136,
    nextRelease: "r073u",
    postR070APublishedReleaseCount: 98,
    postR070AFormalSealedReleaseCount: 74,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.deepEqual(result.targetAccounting, {
    latestCompletedRelease: "r073u",
    siteVersion: "1.61",
    publicHtmlNoteCount: 197,
    postR060RecapNodeCount: 137,
    nextRelease: "r073v",
    postR070APublishedReleaseCount: 99,
    postR070AFormalSealedReleaseCount: 75,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.equal(result.canonicalSources, 8);
  assert.equal(result.canonicalSourcesPlanned, 11);
  assert.equal(result.publicationReady, true);
  assert.deepEqual(result.readinessFailures, []);
  assert.equal(result.certificate.finalSeal, true);
  assert.equal(result.certificate.schemaVersion, "r073u-exact-tensor-heat-manifest-v1");
  assert.equal(result.figure.formal, true);
  assert.equal(result.figure.figureId, "fig-r073u-tensor-heat-hierarchy");
  assert.equal(result.releaseSourceReady, true);
  const generator = read("scripts/generate_r073u_release.py");
  const sourcePin = generator.match(
    /^RELEASE_SOURCE_COMMIT = (ZERO_COMMIT|"([0-9a-f]{40})")$/m,
  );
  assert.ok(sourcePin);
  assert.equal(result.commitPinsReady, sourcePin[1] !== "ZERO_COMMIT");
  assert.equal(result.publicTransactionImplemented, true);
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.clayConclusion, "OPEN");
  assert.ok(result.coreOutputsPlanned.includes("public/notes/r0-73u.html"));
  assert.ok(result.coreOutputsPlanned.includes("public/recap-r0-61-r0-73u.html"));
  assert.ok(result.laterStageOutputsPlanned.includes("research/r073u_pdf_bindings.json"));
  assert.ok(result.figureOutputsPlanned.includes(
    "public/assets/r073u/fig-r073u-tensor-heat-hierarchy.pdf"));
  assert.equal(result.writes, 0);
});

test("reviewed layers stay pinned across the release-source pre-seal/post-seal lifecycle", () => {
  const generator = read("scripts/generate_r073u_release.py");
  assert.match(generator,
    /RELEASE_BASELINE_COMMIT = "3d23297f072b2059da3981b69ce5a8301ed690d7"/);
  assert.match(generator,
    /ANALYTIC_SOURCE_COMMIT = "84e808dae473f6381cbf9df55a71f5fe81a1cfce"/);
  assert.match(generator,
    /FINITE_SOURCE_COMMIT = "6c79f23152116f5d420be6ff03653500ab02ef0e"/);
  assert.match(generator,
    /FINITE_PACKAGE_COMMIT = "044bfb3f7e5af98e2615f60747c9e5109ef12d7c"/);
  assert.match(generator,
    /FIGURE_PACKAGE_COMMIT = "6c20af03a21488fea3f060738084fa9048437984"/);
  assert.match(generator,
    /FINAL_CONTENT_COMMIT = "552ce0015e5eac0bf1d93968304ec53c7181774e"/);
  const sourcePin = generator.match(
    /^RELEASE_SOURCE_COMMIT = (ZERO_COMMIT|"([0-9a-f]{40})")$/m,
  );
  assert.ok(sourcePin);
  assert.ok(generator.includes("__NORMALIZED_RELEASE_SOURCE_COMMIT__"));
  assert.match(generator, /PUBLIC_TRANSACTION_IMPLEMENTED = True/);
  const checked = runPython("scripts/generate_r073u_release.py", "--check-only");
  if (sourcePin[1] === "ZERO_COMMIT") {
    assert.notEqual(checked.status, 0);
    assert.match(checked.stderr,
      /R0\.73U release source: unsealed 40-zero commit pin; binding remains fail-closed/);
  } else {
    assert.equal(checked.status, 0, checked.stderr || checked.stdout);
    const result = JSON.parse(checked.stdout);
    assert.equal(result.release, "R0.73U");
    assert.equal(result.checkOnly, true);
    assert.equal(result.applied, false);
    assert.equal(result.writes, 0);
    assert.equal(result.wouldWrite, 62);
  }
});

test("the public transaction assembles the complete target in memory without applying", () => {
  const result = pythonCodeJson([
    "import json,sys",
    "sys.path.insert(0,'scripts')",
    "import generate_r073u_release as g",
    "c=g.load_release_content(g.ROOT)",
    "s=g.build_staged(c)",
    "rel=lambda p:p.relative_to(g.ROOT).as_posix()",
    "f=json.loads(s[g.ROOT/g.FIGURE_ARCHIVE_RELATIVE/'manifest.json'])",
    "note=s[g.PUBLIC/'notes/r0-73u.html'].decode()",
    "recap=s[g.PUBLIC/'recap-r0-61-r0-73u.html'].decode()",
    "home=s[g.PUBLIC/'research-review.html'].decode()",
    "lit=s[g.PUBLIC/'literature-review.html'].decode()",
    "print(json.dumps({'count':len(s),'core':all(g.ROOT/p in s for p in g.CORE_TARGET_OUTPUTS),'html':sum(p.suffix=='.html' for p in s),'title':c.public_title_zh in note,'initialTime':'t=0' in note,'initialBoundary':'不是轨道对称性' in note and '不是轨道对称性' in recap,'rawFence':any('```' in value or '``<code' in value for value in (note,recap,home,lit)),'recap137':'137' in recap,'home197':'197' in home,'next':'R0.73V' in home,'nextGate':'加入最小的 signed third-order lift' in home and '保留 tensor-only 无符号 envelope' in home,'literature':'quadratic-state non-autonomy' in lit,'markdownDoi':'[1938 DOI](' in lit or '[2001 DOI](' in lit,'linkedDoi':'<a href=\"https://doi.org/10.1098/rspa.1938.0013\">1938 DOI</a>' in lit,'badAccent':any('K\\\\&#x27;' in value or \"K\\\\'arm\" in value or 'H\\\\&quot;' in value or 'H\\\\\"older' in value for value in (note,recap,home,lit)),'figureId':f.get('figureId'),'checks':f.get('qa',{}).get('validationChecks'),'figureCommit':f.get('git',{}).get('figurePackageCommit'),'paths':sorted(rel(p) for p in s)}))",
  ].join(";"));
  assert.equal(result.count, 62);
  assert.equal(result.core, true);
  assert.equal(result.html, 5);
  assert.equal(result.title, true);
  assert.equal(result.initialTime, true);
  assert.equal(result.initialBoundary, true);
  assert.equal(result.rawFence, false);
  assert.equal(result.recap137, true);
  assert.equal(result.home197, true);
  assert.equal(result.next, true);
  assert.equal(result.nextGate, true);
  assert.equal(result.literature, true);
  assert.equal(result.markdownDoi, false);
  assert.equal(result.linkedDoi, true);
  assert.equal(result.badAccent, false);
  assert.equal(result.figureId, "fig-r073u-tensor-heat-hierarchy");
  assert.equal(result.checks, 325);
  assert.equal(result.figureCommit, "6c20af03a21488fea3f060738084fa9048437984");
  assert.ok(result.paths.includes(
    "public/assets/r073u/fig-r073u-tensor-heat-hierarchy.pdf"));
  assert.ok(result.paths.includes(
    "public/figures/r073u/fig-r073u-tensor-heat-hierarchy/manifest.json"));
});

test("the atomic transaction rejects real and dangling symlink ancestors", () => {
  const result = pythonCodeJson(`
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, "scripts")
import generate_r073u_release as g
with tempfile.TemporaryDirectory() as directory:
    sandbox = Path(directory)
    root = sandbox / "root"
    outside = sandbox / "outside"
    root.mkdir()
    outside.mkdir()
    (root / "linked").symlink_to(outside, target_is_directory=True)
    (root / "dangling").symlink_to(sandbox / "missing", target_is_directory=True)
    g.ROOT = root
    outcomes = []
    for target in (root / "linked" / "escape.txt", root / "dangling" / "escape.txt"):
        try:
            g.commit_transaction({target: b"blocked"})
        except RuntimeError:
            outcomes.append(True)
        else:
            outcomes.append(False)
    print(json.dumps({"outcomes": outcomes, "outsideUntouched": not (outside / "escape.txt").exists()}))
`);
  assert.deepEqual(result.outcomes, [true, true]);
  assert.equal(result.outsideUntouched, true);
});

test("the normalized release-source pin accepts only the declared self-pin slot", () => {
  const result = pythonCodeJson(`
import json, sys
sys.path.insert(0, "scripts")
import generate_r073u_release as g
zero=b"RELEASE_SOURCE_COMMIT = ZERO_COMMIT\\n"
full=b'RELEASE_SOURCE_COMMIT = "' + b'a'*40 + b'"\\n'
bad=b"RELEASE_SOURCE_COMMIT = 'bad'\\n"
same=g.normalized_release_generator(zero)==g.normalized_release_generator(full)
try:
    g.normalized_release_generator(bad)
except RuntimeError:
    rejected=True
else:
    rejected=False
print(json.dumps({"same":same,"rejected":rejected}))
`);
  assert.equal(result.same, true);
  assert.equal(result.rejected, true);
});

test("deferred translation and PDF binding stages are syntax-safe, local-only, and U-scoped", () => {
  const translation = read("scripts/add-r073u-translations.mjs");
  const binder = read("scripts/bind-r073u-pdfs.mjs");
  for (const [script, usage] of [
    ["scripts/add-r073u-translations.mjs", "add-r073u-translations.mjs"],
    ["scripts/bind-r073u-pdfs.mjs", "bind-r073u-pdfs.mjs"],
  ]) {
    const checked = runNode("--check", script);
    assert.equal(checked.status, 0, checked.stderr || checked.stdout);
    const help = runNode(script, "--help");
    assert.equal(help.status, 0, help.stderr || help.stdout);
    assert.ok(help.stdout.includes(usage));
  }
  for (const relative of activeTranslationPages) assert.ok(translation.includes(relative));
  assert.ok(translation.includes("LOCAL_DIRECT_NO_DGX"));
  assert.ok(translation.includes("reviewed-local-direct-no-dgx-no-network"));
  assert.ok(translation.includes("local-direct-reviewed"));
  assert.ok(translation.includes("--capture-missing"));
  assert.ok(translation.includes("/i18n-en.js?v=1.61"));
  assert.ok(translation.includes("formalFigureChecks=325"));
  assert.ok(translation.includes("same initial time for"));
  assert.ok(translation.includes("not a trajectory symmetry"));
  assert.doesNotMatch(translation,
    /from ["']node:(?:child_process|http|https|net|tls|dns)["']/);
  assert.doesNotMatch(translation, /\bfetch\s*\(/);
  assert.ok(binder.includes("fig-r073u-tensor-heat-hierarchy"));
  assert.ok(binder.includes(title.replace(" | ", "｜")));
  assert.ok(binder.includes("R0.61–R0.73U｜R0.60 之后的研究回顾"));
  assert.ok(binder.includes("formalFigureChecks: 325"));
  assert.ok(binder.includes("public/notes/r0-73u.html"));
  assert.ok(binder.includes("public/recap-r0-61-r0-73u.html"));
});

test("PDF structure parser accepts the bound Info title and rejects a broken tail", () => {
  const fixture = (titleToken) => {
    const chunks = [Buffer.from("%PDF-1.4\n", "latin1")];
    const offsets = [0];
    const object = (number, body) => {
      offsets[number] = Buffer.concat(chunks).length;
      chunks.push(Buffer.from(`${number} 0 obj\n${body}\nendobj\n`, "latin1"));
    };
    object(1, "<< /Type /Catalog /Pages 2 0 R /Title (Decoy title) >>");
    object(2, "<< /Type /Pages /Kids [3 0 R] /Count 1 >>");
    object(3, "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] >>");
    object(4, `<< /Title ${titleToken} >>`);
    const startxref = Buffer.concat(chunks).length;
    chunks.push(Buffer.from(
      "xref\n0 5\n0000000000 65535 f \n" +
      offsets.slice(1).map((offset) =>
        `${String(offset).padStart(10, "0")} 00000 n \n`).join("") +
      "trailer\n<< /Size 5 /Root 1 0 R /Info 4 0 R >>\n" +
      `startxref\n${startxref}\n%%EOF\n`,
      "latin1",
    ));
    return Buffer.concat(chunks);
  };
  const text = "R0.73U";
  const utf16 = Buffer.concat([
    Buffer.from([0xfe, 0xff]),
    Buffer.from(text).reduce(
      (payload, value) => Buffer.concat([payload, Buffer.from([0, value])]),
      Buffer.alloc(0),
    ),
  ]).toString("hex").toUpperCase();
  const directory = mkdtempSync(join(realpathSync(tmpdir()), "r073u-pdf-test-"));
  try {
    writeFileSync(resolve(directory, "fixture.pdf"), fixture(`<${utf16}>`));
    const checked = spawnSync(
      process.execPath,
      ["scripts/bind-r073u-pdfs.mjs", "--structure-check", "fixture.pdf", text],
      {
        cwd: root,
        encoding: "utf8",
        env: { ...process.env, R073U_RELEASE_ROOT: directory },
      },
    );
    assert.equal(checked.status, 0, checked.stderr || checked.stdout);
    const structure = JSON.parse(checked.stdout);
    assert.equal(structure.title, text);
    assert.equal(structure.infoObject, "4 0 R");
    assert.equal(structure.pageCount, 1);
    assert.equal(structure.eof, true);
    assert.equal(structure.xrefKeyword, "xref");

    writeFileSync(resolve(directory, "broken.pdf"), Buffer.from(
      fixture(`<${utf16}>`).toString("latin1").replace("%%EOF", "%EOF"), "latin1"));
    const broken = spawnSync(
      process.execPath,
      ["scripts/bind-r073u-pdfs.mjs", "--structure-check", "broken.pdf", text],
      {
        cwd: root,
        encoding: "utf8",
        env: { ...process.env, R073U_RELEASE_ROOT: directory },
      },
    );
    assert.notEqual(broken.status, 0);
    assert.match(broken.stderr, /startxref\/%%EOF/);
  } finally {
    rmSync(directory, { recursive: true, force: true });
  }
});

test("all six R0.73U release files reject obsolete package identity", () => {
  const targets = [
    "scripts/r073u_release_content.py",
    "scripts/generate_r073u_release.py",
    "scripts/add-r073u-translations.mjs",
    "scripts/bind-r073u-pdfs.mjs",
    "tests/r073u-tensor-heat-hierarchy-gate.test.mjs",
    "tests/r073u-release.test.mjs",
  ];
  const corpus = targets.map(read).join("\n");
  const obsoleteFigure = ["fig-r073u", "dynamic", "autocorrelation"].join("-");
  const obsoleteTitle = ["pressure is recoverable", "but signed flux is not"].join(", ");
  assert.equal(corpus.toLowerCase().includes(obsoleteFigure), false);
  assert.equal(corpus.includes(obsoleteTitle), false);
  const staleNote = ["/notes/r0-73", "s.html"].join("");
  const staleRecap = ["/recap-r0-61-r0-73", "s.html"].join("");
  assert.equal(corpus.includes(staleNote), false);
  assert.equal(corpus.includes(staleRecap), false);
});
