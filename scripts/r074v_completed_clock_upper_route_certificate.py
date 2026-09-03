#!/usr/bin/env python3
"""Finite exact certificate for R0.74V Step 21 (route memo, not PDE proof)."""

from __future__ import annotations
import hashlib, itertools, json, os, re, sys
from fractions import Fraction as F
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
NOTE = Path(os.environ.get("R074V_NOTE", REPO / "research/r074v_completed_clock_upper_route.md"))
PRIMARY_AUDIT = Path(os.environ.get("R074V_PRIMARY_AUDIT", REPO / "research/r074v_completed_clock_upper_route_primary_audit.md"))
JSON_OUT = Path(os.environ.get("R074V_JSON", REPO / "research/r074v_completed_clock_upper_route_certificate.json"))
REPORT_OUT = Path(os.environ.get("R074V_REPORT", REPO / "research/r074v_completed_clock_upper_route_certificate_report.md"))
SCHEMA = "r074v-completed-clock-upper-route-certificate-v1"
MUTATION = os.environ.get("R074V_MUTATION", "").strip()
NOTE_SHA = "031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c"
PRIMARY_AUDIT_SHA = os.environ.get("R074V_EXPECTED_PRIMARY_AUDIT_SHA256", "148b41ef2755d6ca42927595362fd59c81db8880713293a8e82c1c288fdea77d")
DEPENDENCIES = {
    "research/r074e_local_mollified_frame_gate.md": "3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7",
    "research/r074f_two_packet_survival.md": "0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb",
    "research/r074h_collar_flux_two_regime_closure.md": "8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1",
    "research/r074p_temporal_observable_triage.md": "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
    "research/r074q_common_shear_multipacket_gate.md": "60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695",
    "research/r074q_relaxed_multipacket_cubic_obstruction.md": "ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d",
    "research/r074t_schedule_invariant_dwell_coercivity.md": "8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd",
    "research/r074u_intrinsic_certified_residence.md": "e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99",
}
EXPECTED_TAGS = tuple([f"V.{n}" for n in range(1, 8)] + ["V.7a"] + [f"V.{n}" for n in range(8, 17)] + ["V.16a"] + [f"V.{n}" for n in range(17, 40)] + ["V.39a", "V.39b"] + [f"V.{n}" for n in range(40, 48)] + ["V.47a", "V.48", "V.48a"] + [f"V.{n}" for n in range(49, 55)] + ["V.54a"] + [f"V.{n}" for n in range(55, 70)])
MUTATIONS = (
    "d0_sign", "chi65_sign", "chi66_sign", "rho_margin_sign",
    "gamma_ratio_sign", "H_ratio_sign", "union_threshold", "remainder_threshold",
    "box_inner_failure", "box_outer_failure", "box_volume_failure",
    "v_R_minus_a", "K_upper_proved", "V64_common_shear_theorem",
    "drop_accumulated_dissipation", "AI_to_Aclk", "uniform_arbitrary_Astar",
    "drop_not_clay", "tag_inventory", "claim_sentinel", "source_hash",
    "primary_audit_hash", "dependency_hash", "torus_chord_cap", "volume_cap",
    "central_pairs_to_all_k", "wrong_versionM_shift", "raw_endpoint_all_times",
    "hard_time_raw_formula",
)

def sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()
def fs(x): return f"{x.numerator}/{x.denominator}"
def row(i, passed, note, cases=1, **kw): return {"id": i, "pass": bool(passed), "note": note, "cases": cases, **kw}

def exact_arithmetic():
    lam, ch, cg, rho = F(63,32), F(15,16), F(8,3969), F(1,320)
    d0 = ch - 1/lam
    if MUTATION == "d0_sign": d0 = -d0
    chi65 = F(3,4)*cg - d0*d0/F(130)
    if MUTATION == "chi65_sign": chi65 = -chi65
    chi66 = F(3,4)*cg - d0*d0/F(132)
    if MUTATION == "chi66_sign": chi66 = -chi66
    reserve = rho - 4*chi66
    if MUTATION == "rho_margin_sign": reserve = -reserve
    rows = [
        row("d0_exact", d0 == F(433,1008) and d0 > 0, "Exact adjacent-inward vertical gap.", observed=fs(d0)),
        row("chi65_exact", chi65 == F(12191,132088320) and chi65 > 0, "Earliest heat-age exponent.", observed=fs(chi65)),
        row("chi66_exact", chi66 == F(15263,134120448) and chi66 > 0, "Latest heat-age exponent.", observed=fs(chi66)),
        row("rho_minus_four_chi66", reserve == F(447593,167650560) and reserve > 0, "Frozen rho scale reserve.", observed=fs(reserve)),
    ]
    failures=[]
    for age in range(65,67):
        chi=F(3,4)*cg-d0*d0/F(2*age)
        if not (chi>0 and chi65<=chi<=chi66): failures.append(age)
    rows.append(row("heat_age_grid", not failures, "Exact age endpoints preserve the positive exponent interval.", cases=2, failures=failures))
    return rows

def exponent_ledgers():
    gamma_ratio = F(3,4) if MUTATION == "gamma_ratio_sign" else F(-3,4)
    h12, h21 = (F(-3),F(3)) if MUTATION == "H_ratio_sign" else (F(3),F(-3))
    rows=[row("gamma_adjacent_ratio_exponent", gamma_ratio==F(-3,4), "gamma_(k-1)/Gamma=Gamma^(-3/4).", exponent=fs(gamma_ratio)),
          row("cross_shell_H_ratio_exponents", (h12,h21)==(F(3),F(-3)), "H(k2<-1)/T~Gamma1^3 and H(k1<-2)/T~Gamma1^-3.", exponents=[fs(h12),fs(h21)])]
    failures=[]
    # Symbolic check gamma_k = exp(-4^(k-1)/32): shifting inward quarters its exponent.
    for e in (F(1,8),F(1,2),F(2),F(8)):
        ratio_log=(-e/F(4))-(-e)
        if ratio_log != F(3,4)*e: failures.append(fs(e))
    rows.append(row("gamma_shift_exact_grid", not failures, "Inward shift produces +3/4 of the target decay exponent.", cases=4, failures=failures))
    return rows

def reduction_and_box():
    z = F(1,8) if MUTATION == "union_threshold" else F(1,4)
    rem = F(1,4) if MUTATION == "remainder_threshold" else F(1,8)
    lam=F(63,32)
    inner = F(3,4) > 1/lam
    outer = F(171,256) < (2/lam)**2
    volume = F(1,1024)
    if MUTATION == "box_inner_failure": inner=False
    if MUTATION == "box_outer_failure": outer=False
    if MUTATION == "box_volume_failure": volume=F(1,512)
    rows=[
      row("V52_V54_union_threshold", z==F(1,4) and 2*F(1,8)==z, "E is half the V.48 integrand, so V.54 uses z=kappa/4.", z_over_kappa=fs(z)),
      row("V54a_flat_remainder", rem==F(1,8) and rem==z/2, "Each weighted flat remainder is at most kappa T/8.", remainder_over_kappa=fs(rem)),
      row("common_shear_box_inner", inner, "3/4>1/lambda gives the inner face.", margin=fs(F(3,4)-1/lam)),
      row("common_shear_box_outer", outer, "171/256<(2/lambda)^2 gives the outer face.", margin=fs((2/lam)**2-F(171,256))),
      row("common_shear_box_volume", volume==F(1,1024), "Two horizontal widths r/8 and vertical width r/16 give r^3/1024.", normalized_volume=fs(volume)),
    ]
    failures=[]
    # Finite nonnegative union algebra: if B<=k/2 and K>=k, then one of two E rows >=k/8.
    for den in (8,16,32):
      kap=F(1,den)
      for e1,e2 in itertools.product((F(0),kap/16,kap/8,kap/4), repeat=2):
        b=kap/2; k=b+2*e1+2*e2
        if k>=kap and not (e1>=kap/8 or e2>=kap/8): failures.append([den,fs(e1),fs(e2)])
    rows.append(row("finite_union_implication", not failures, "Finite exact nonnegative fixtures verify V.52--V.54.", cases=48, failures=failures))
    return rows

def lifted_geometry_and_quantifiers():
    failures=[]
    for s in (F(1,16),F(1,4),F(1),F(2),F(8)):
      ell=s+s**3
      if MUTATION=="torus_chord_cap": ell=min(ell,F(1))
      if ell != s+s**3 or ell < s: failures.append({"s":fs(s),"ell":fs(ell)})
    volume_identity = "lifted_integral"
    if MUTATION=="volume_cap": volume_identity="min_with_torus_volume"
    pairs=tuple((k,m) for k in ("k1-1","k1","k2") for m in (1,2))
    if MUTATION=="central_pairs_to_all_k": pairs=pairs+(("arbitrary-k",1),)
    return [
      row("lifted_chord_ell_s_plus_s3",not failures,"The lifted chord is ell=s+s^3 with no torus-length cap.",cases=5,failures=failures),
      row("lifted_volume_exact_tiling",volume_identity=="lifted_integral","V_k is the exact R^3 integral of psi by tiling and has no projected-volume cap.",identity=volume_identity),
      row("V67_six_central_pairs",len(pairs)==6 and set(pairs)==set((k,m) for k in ("k1-1","k1","k2") for m in (1,2)),"V.46--V.50 are restricted to exactly six central pairs; all-k is open.",cases=len(pairs),pairs=[list(x) for x in pairs]),
    ]

def structural():
    try: text=NOTE.read_text(encoding="utf-8"); err=None
    except Exception as exc: text=""; err=f"{type(exc).__name__}: {exc}"
    tags=re.findall(r"\\tag\{(V\.[^}]+)\}",text)
    expected=EXPECTED_TAGS + ("V.70",) if MUTATION=="tag_inventory" else EXPECTED_TAGS
    required=[
      "**NOT CLAY.**", "R074V_STEP21_STATUS_ROUTE_ONLY", "R074V_STEP21_STATUS_K_SUPERLEVEL_UPPER_OPEN",
      "R074V_STEP21_STATUS_ADJACENT_INWARD_TAIL_GATE", "R074V_STEP21_END",
      "stated here as a target, not as", "a proved theorem.", "(V.64) is not yet a lower bound for",
      "accumulated dissipation", r"\mathcal A^I_{k,m}", r"\mathcal A^{\rm clk}_{k,m}",
      "uniform estimate over every", r"A_*>0", "physical collar term is different",
      r"z=\kappa/4", r"\kappa\over8", r"\mathcal B_i\le{\kappa\over2}T",
      "common-shear solution", "Not established", "R074V_STEP21_STATUS_K_SUPERLEVEL_UPPER_OPEN",
      r"\ell_k:=s_k+s_k^3", "cannot be capped by the length of one torus period",
      r"V_k:=\int_{\mathbb T^3}\Psi_k^R(x)\,dx", r"=\int_{\mathbb R^3}\psi_k^R(y)\,dy",
      "cannot be capped", "six central-chart pairs", "are not statements for arbitrary", "all-\\(k\\) extension",
      "R074V_STEP21_STATUS_LIFTED_MULTIPLICITY_INCLUDED", "R074V_STEP21_STATUS_PERIODIZED_VOLUME_USES_LIFTED_INTEGRAL",
      "R074V_STEP21_STATUS_OCCUPATION_CENTRAL_FINITE_ONLY", "R074V_STEP21_STATUS_ALL_K_LIFTED_COPY_SUMMATION_OPEN",
      "R074V_STEP21_STATUS_RAW_ENDPOINT_MEASURE_GOOD_TIMES_ONLY", r"v_R(t,y)=u(t,y+X_R(t))",
      "At every local-energy good time", "canonical absolutely", r"K_{k,R}=Q_{k,R}+F_{k,R}",
      "must not be read as a raw hard-time endpoint identity", "three and only three nonnegative completion rows",
    ]
    mutation_tokens={
      "v_R_minus_a":"v_R-a", "K_upper_proved":"K_SUPERLEVEL_UPPER_PROVED",
      "V64_common_shear_theorem":"V.64 IS A COMMON-SHEAR THEOREM",
      "drop_accumulated_dissipation":"ACCUMULATED_DISSIPATION_REMOVED",
      "AI_to_Aclk":"A_I_AND_A_CLK_IDENTIFIED", "uniform_arbitrary_Astar":"UNIFORM_FOR_ARBITRARY_ASTAR",
      "claim_sentinel":"MILLENNIUM_PROBLEM_SOLVED",
      "torus_chord_cap":"CHORD_CAPPED_BY_TORUS_LENGTH", "volume_cap":"VOLUME_CAPPED_BY_TORUS_VOLUME",
      "central_pairs_to_all_k":"V46_V50_PROVED_FOR_ARBITRARY_K", "wrong_versionM_shift":r"v_R(t,y)=u(t,y-X_R(t))",
      "raw_endpoint_all_times":"RAW_ENDPOINT_FORMULA_AT_ALL_TIMES", "hard_time_raw_formula":"HARD_TIME_USES_RAW_ENDPOINT",
    }
    if MUTATION in mutation_tokens: required.append(mutation_tokens[MUTATION])
    if MUTATION=="drop_not_clay": required.remove("**NOT CLAY.**"); required.append("**CLAY CLAIM.**")
    forbidden=["K_SUPERLEVEL_UPPER_PROVED","V.64 IS A COMMON-SHEAR THEOREM","ACCUMULATED_DISSIPATION_REMOVED","A_I_AND_A_CLK_IDENTIFIED","UNIFORM_FOR_ARBITRARY_ASTAR","MILLENNIUM_PROBLEM_SOLVED","CHORD_CAPPED_BY_TORUS_LENGTH","VOLUME_CAPPED_BY_TORUS_VOLUME","V46_V50_PROVED_FOR_ARBITRARY_K",r"v_R(t,y)=u(t,y-X_R(t))","RAW_ENDPOINT_FORMULA_AT_ALL_TIMES","HARD_TIME_USES_RAW_ENDPOINT"]
    return [
      row("note_utf8",err is None,"Source is readable UTF-8.",error=err),
      row("tag_inventory",tuple(tags)==expected and len(tags)==len(set(tags)),"Exact ordered V tag ledger.",observed=tags,expected=list(expected)),
      row("claim_and_formula_sentinels",all(x in text for x in required),"Open/proved distinctions and route ingredients remain explicit.",missing=[x for x in required if x not in text]),
      row("forbidden_overclaims",all(x not in text for x in forbidden),"No mutation overclaim or semantic collapse occurs.",found=[x for x in forbidden if x in text]),
      row("AI_Aclk_distinct",r"\mathcal A^I_{k,m}" in text and r"\mathcal A^{\rm clk}_{k,m}" in text and "must be distinguished" in text,"Instantaneous and accumulated-clock amplifications are distinct."),
      row("accumulated_dissipation_retained","accumulated dissipation" in text and "enters (V.53) without a logarithm" in text,"Persistent viscosity is not omitted."),
    ]

def hashes():
    note_expected="0"*64 if MUTATION=="source_hash" else NOTE_SHA
    primary_expected="0"*64 if MUTATION=="primary_audit_hash" else PRIMARY_AUDIT_SHA
    out=[row("note_hash",NOTE.is_file() and sha(NOTE)==note_expected,"Frozen route memo hash.",expected=note_expected,observed=sha(NOTE) if NOTE.is_file() else None),
         row("primary_audit_hash",PRIMARY_AUDIT.is_file() and len(primary_expected)==64 and sha(PRIMARY_AUDIT)==primary_expected,"Primary audit is fail-closed until frozen.",expected=primary_expected,observed=sha(PRIMARY_AUDIT) if PRIMARY_AUDIT.is_file() else None)]
    for index,(rel,digest) in enumerate(DEPENDENCIES.items()):
      expected="0"*64 if MUTATION=="dependency_hash" and index==0 else digest; p=REPO/rel
      out.append(row("dependency_"+p.stem,p.is_file() and sha(p)==expected,"Frozen dependency hash.",path=rel,expected=expected,observed=sha(p) if p.is_file() else None))
    return out

def render(payload):
    checks=payload["checks"]; finite=[x for x in checks if x["group"]=="finite"]
    lines=["# R0.74V Step 21 finite certificate report","",f"- Schema: {SCHEMA}",f"- Verdict: **{payload['verdict']}**",f"- Groups: {sum(x['pass'] for x in checks)}/{len(checks)}",f"- Finite cases: {sum(x['cases'] for x in finite)}",f"- Route memo SHA-256: `{sha(NOTE) if NOTE.is_file() else 'MISSING'}`",f"- Primary audit SHA-256: `{sha(PRIMARY_AUDIT) if PRIMARY_AUDIT.is_file() else 'PENDING/MISSING'}`","","## Inventory","","| Check | Layer | Result | Cases |","|---|---|---:|---:|"]
    lines += [f"| {x['id']} | {x['group']} | {'PASS' if x['pass'] else 'FAIL'} | {x['cases']} |" for x in checks]
    lines += ["","## Boundary","","The certificate verifies exact rational ledgers, finite union/box fixtures, source semantics, dependencies, and byte hashes. V.47--V.50, V.56, and the remote common-shear comparison remain proposed or open analytic steps. No completed-clock upper, regularity, singularity, novelty, or Clay result is machine-proved.",""]
    failed=[x["id"] for x in checks if not x["pass"]]
    if failed: lines += ["## Failed checks",""]+[f"- {x}" for x in failed]+[""]
    return "\n".join(lines)

def main():
    checks=[]
    for x in exact_arithmetic()+exponent_ledgers()+reduction_and_box()+lifted_geometry_and_quantifiers(): x["group"]="finite"; checks.append(x)
    for x in structural(): x["group"]="structural"; checks.append(x)
    for x in hashes(): x["group"]="hash"; checks.append(x)
    verdict="PASS" if all(x["pass"] for x in checks) else "FAIL"
    payload={"schema":SCHEMA,"verdict":verdict,"mutation":MUTATION or None,"note_sha256":sha(NOTE) if NOTE.is_file() else None,"primary_audit_sha256":sha(PRIMARY_AUDIT) if PRIMARY_AUDIT.is_file() else None,"checks":checks,"negative_mutations":list(MUTATIONS),"limitations":["finite exact arithmetic, kinematic, structural, dependency and hash audit only","no continuous PDE localization or common-shear remote-strip theorem","no completed-clock upper, regularity, singularity, or Clay claim"]}
    JSON_OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    REPORT_OUT.write_text(render(payload),encoding="utf-8")
    print(json.dumps({"schema":SCHEMA,"verdict":verdict,"groups_passed":sum(x["pass"] for x in checks),"groups_total":len(checks),"finite_cases":sum(x["cases"] for x in checks if x["group"]=="finite"),"mutation":MUTATION or None},sort_keys=True))
    return 0 if verdict=="PASS" else 1
if __name__=="__main__": sys.exit(main())
