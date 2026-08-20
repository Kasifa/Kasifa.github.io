import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const noteUrl = new URL(
  "../research/eighth_order_heat_defect_pilot_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/eighth_order_heat_defect_pilot.py",
  import.meta.url,
);

test("states the degree-ten defect improvement and its open mixed-derivative gate", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);
  assert.match(note, /44514/);
  assert.match(note, /16777216/);
  assert.match(note, /8008/);
  assert.match(note, /30\.23448650536/);
  assert.match(note, /0\.00469566611239/);
  assert.match(note, /2\.5663266368\\times10\^\{-6\}/);
  assert.match(note, /4368/);
  assert.match(note, /not yet a theorem/i);
  assert.match(note, /does not solve the Navier--Stokes Millennium problem/i);
  assert.match(audit, /fourteen-component/);
  assert.match(audit, /mixed[\s\S]*derivatives remain uncertified/);
});
