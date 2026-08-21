import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";
const root=new URL("../",import.meta.url);
const figureRoot=new URL("../figures/r069k-shell-gain/fig-r069k-shell-gain/",import.meta.url);
test("archives the formal R0.69K shell-gain figure",async()=>{
 const [m,v,c,k]=await Promise.all(["manifest.json","validation.json","caption.md","figure-contract.md"].map(p=>readFile(new URL(p,figureRoot),"utf8")));
 const manifest=JSON.parse(m), validation=JSON.parse(v);
 assert.equal(manifest.status,"formal"); assert.equal(manifest.figureId,"fig-r069k-shell-gain");
 assert.equal(manifest.git.sourceCommit,"b2c7ad329eba2df516dd251a1f74af42ad153e74");
 assert.equal(manifest.git.certificateCommit,"83049f868fb0ea2b393e0b469fa9f2343c6602cf");
 assert.equal(manifest.figure.widthMillimetres,178); assert.equal(manifest.figure.heightMillimetres,86);
 assert.equal(manifest.qa.grayscaleInspected,true); assert.equal(validation.status,"passed");
 assert.equal(Object.keys(validation.checks).length,8); assert.ok(Object.values(validation.checks).every(Boolean));
 assert.match(c,/gains two powers of far-shell\s+decay/i);
 assert.match(k,/neither proves\s+Navier-+Stokes regularity nor constructs a singularity/i);
 for(const output of manifest.figure.outputs){
  const payload=await readFile(new URL(output.path,figureRoot));
  assert.equal(createHash("sha256").update(payload).digest("hex"),output.sha256);
  const ext=output.path.split(".").at(-1);
  const pub=await readFile(new URL("../public/figures/r0-69k-shell-gain."+ext,import.meta.url));
  assert.deepEqual(pub,payload);
 }
});
test("the R0.69K figure package passes the strict validator",()=>{
 const run=spawnSync(process.env.PYTHON??"python3",[new URL("../research/validate_figure_package.py",import.meta.url).pathname,figureRoot.pathname],{cwd:root.pathname,encoding:"utf8",env:{...process.env,PYTHONDONTWRITEBYTECODE:"1"}});
 assert.equal(run.status,0,run.stderr||run.stdout); const report=JSON.parse(run.stdout);
 assert.deepEqual(report.errors,[]); assert.deepEqual(report.warnings,[]);
});
test("pins a deterministic R0.69K SVG hash salt",async()=>{
 const plot=await readFile(new URL("plot.py",figureRoot),"utf8");
 assert.match(plot,/rcParams\["svg\.hashsalt"\] = FIGURE_ID/);
});
