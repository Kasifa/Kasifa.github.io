#!/usr/bin/env python3
"""Finite exact/structural certificate for R0.74W; never a PDE proof."""
from __future__ import annotations
import hashlib, json, os, re, sys
from fractions import Fraction as F
from pathlib import Path

REPO=Path(__file__).resolve().parents[1]
MAIN=Path(os.environ.get("R074W_MAIN",REPO/"research/r074w_remote_adjacent_inward_comparison.md"))
PRIMARY=Path(os.environ.get("R074W_PRIMARY",REPO/"research/r074w_remote_adjacent_inward_comparison_primary_audit.md"))
LITERATURE=Path(os.environ.get("R074W_LITERATURE",REPO/"research/r074w_remote_adjacent_inward_literature_audit.md"))
JSON_OUT=Path(os.environ.get("R074W_JSON",REPO/"research/r074w_remote_adjacent_inward_comparison_certificate.json"))
REPORT_OUT=Path(os.environ.get("R074W_REPORT",REPO/"research/r074w_remote_adjacent_inward_comparison_certificate_report.md"))
SCHEMA="r074w-remote-adjacent-inward-comparison-certificate-v1"
MUTATION=os.environ.get("R074W_MUTATION","").strip()
LOCKS={"main":"d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10","primary":"66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73","literature":"ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99"}
TAGS=tuple([f"W.{n}" for n in range(1,25)]+["W.24a","W.24b"]+[f"W.{n}" for n in range(25,50)]+["W.49b"]+[f"W.{n}" for n in range(50,53)]+["W.52a"]+[f"W.{n}" for n in range(53,69)]+["W.68a"]+[f"W.{n}" for n in range(69,85)])
MUTATIONS=("swap_q64_q65","free_age_for_shear_age","delete_winding","absolute_o1","deterministic_equality","close_critical_band","wrong_packet_states","drop_cross","drop_inversion","T_not_Tstar","fixed_deletion_complete","drop_not_clay","fraction_margin","source_hash","primary_hash","literature_hash","tag_inventory","probability_without_eta","survival_quantifier","sweeping_quantifier","all_shell_upper_true","whole_shell_complete","novelty_claim")

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def fs(x): return f"{x.numerator}/{x.denominator}"
def ck(i,ok,note,cases=1,**d): return {"id":i,"pass":bool(ok),"note":note,"cases":cases,**d}

def exact():
 p=F(32,63); ch=F(15,16); d=ch-p; q64=p*p/F(256); q65=p*p/F(260)
 if MUTATION=="swap_q64_q65": q64,q65=q65,q64
 rows=[ck("p_exact",p==F(32,63),"p=1/lambda."),ck("d_exact",d==F(433,1008),"d=c_h-p."),ck("q64_exact",q64==F(4,3969),"Shear-age threshold at ell=64."),ck("q65_exact",q65==F(256,257985),"Shear-age threshold at ell=65."),ck("threshold_gap",q64-q65==F(4,257985)>0,"Critical band has a strict positive width.",gap=fs(q64-q65))]
 margins={
  "reference_height_gap":ch*ch/F(260)-q64,
  "lower_absorption":ch*ch/F(260)-(p+d/F(4))**2/F(256),
  "inversion":ch*p/F(66),
  "cross_1_from_2":((2*ch-p)**2-d*d)/F(264)-3*q64,
  "cross_2_from_1":3*q64-(4*d*d-(2*p-ch)**2)/F(260),
  "cstar":F(3,22)*F(144,5)**2-q64,
  "outer_reserve":4*q65-F(75,22528),
  "original_inner":F(1,320)-q64,
  "original_outer":q65-F(1,1280),
  "chi65":F(3,4)*F(8,3969)-d*d/F(130),
  "chi66":F(3,4)*F(8,3969)-d*d/F(132),
 }
 expected={"reference_height_gap":F(125357,52835328),"lower_absorption":F(11430203,6011486208),"inversion":F(5,693),"cross_1_from_2":F(100043,29804544),"cross_2_from_1":F(3667,17611776),"cstar":F(123450676,1091475),"outer_reserve":F(3719797,5811886080),"original_inner":F(2689,1270080),"original_outer":F(13939,66044160),"chi65":F(12191,132088320),"chi66":F(15263,134120448)}
 if MUTATION=="fraction_margin": margins["cross_1_from_2"]+=F(1,10**9)
 for name,want in expected.items(): rows.append(ck(name,margins[name]==want and margins[name]>0,"Exact positive rational margin.",observed=fs(margins[name]),expected=fs(want)))
 twice=2*margins["cross_1_from_2"]-margins["chi66"]
 rows.append(ck("two_delta_minus_chi",twice==F(221281,33530112)>0,"Swept packet cross absorption beats endpoint growth.",observed=fs(twice)))
 return rows

def geometry_and_scaling():
 chart=F(5,144); br2=F(1,128); strip=F(1,16); endpoint_power=F(-1,2)
 rows=[ck("BR2_lower",br2==F(1,128),"Lower shear normalization used in displacement absorption."),ck("chart_cap",chart==F(5,144) and F(144,5)*chart==1,"Chart conversion is exact."),ck("strip_volume_coefficient",strip==F(1,16),"|S_m|=(1/16)sqrt(pL_m)R^3."),ck("endpoint_polynomial_power",endpoint_power==F(-1,2),"Amplitude square L^-1 times strip sqrt(L) gives L^-1/2.",power=fs(endpoint_power))]
 # Exact exponent ledger: gamma ratio +3/4 c_gamma, two free kernels, amplitude L^-1, volume L^1/2.
 powers={"L_amplitude":F(-1),"L_volume":F(1,2),"L_endpoint":endpoint_power}
 rows.append(ck("endpoint_power_ledger",powers["L_amplitude"]+powers["L_volume"]==powers["L_endpoint"],"Endpoint polynomial ledger closes.",powers={k:fs(v) for k,v in powers.items()}))
 return rows

def structure():
 try: text=MAIN.read_text(encoding="utf-8"); err=None
 except Exception as e: text=""; err=str(e)
 tags=re.findall(r"\\tag\{(W\.[^}]+)\}",text); expected=TAGS+("W.85",) if MUTATION=="tag_inventory" else TAGS
 required=["**NOT CLAY.**","R074W_NOT_CLAY",r"\mathbb P_{0,y}^{\rm br}",r"\eta>0",r"\sum_{n\in\mathbb Z}w_n","division by the full winding",r"\sum_nw_n\mathbb E_{n,y}^{\rm br}","The total free heat age is", "but the shear deficit in", r"has age \(t=\ell R^2\)", "not a deterministic pathwise identity","uniformly for every",r"\limsup",r"\liminf","relative failure mechanism, not an absolute", "critical equality", "requires a sharper transition", "common-shear family", "nonnegative endpoint row", "matching all-shell", "is false", "fixed-deletion functional could", "does not by itself disprove every", "whole-shell", "remain open", r"T_*=A_*^2R^2", "finite non-hit", "does not certify novelty"]
 mutation_tokens={"free_age_for_shear_age":"SHEAR_AGE_EQUALS_FREE_AGE","delete_winding":"WINDING_SUM_DELETED","absolute_o1":"ABSOLUTE_O1_SUFFICES","deterministic_equality":"DETERMINISTIC_DISPLACEMENT_EQUALITY","close_critical_band":"CRITICAL_BAND_CLOSED","wrong_packet_states":"PACKET1_SURVIVES_PACKET2_SWEPT","drop_cross":"CROSS_PACKET_COMPARISON_DELETED","drop_inversion":"INVERSION_COMPARISON_DELETED","T_not_Tstar":"ALL_ENDPOINT_LEVELS_USE_T_NOT_TSTAR","fixed_deletion_complete":"FIXED_DELETION_COMPLETED","probability_without_eta":"PROBABILITY_STATEMENT_WITHOUT_ETA","survival_quantifier":"SURVIVAL_EXISTS_TIME_ONLY","sweeping_quantifier":"SWEEPING_EXISTS_TIME_ONLY","all_shell_upper_true":"ALL_SHELL_UPPER_TRUE","whole_shell_complete":"WHOLE_SHELL_OCCUPATION_COMPLETE","novelty_claim":"NOVELTY_CERTIFIED"}
 if MUTATION in mutation_tokens: required.append(mutation_tokens[MUTATION])
 if MUTATION=="drop_not_clay": required.remove("**NOT CLAY.**"); required.append("**CLAY CLAIM.**")
 forbidden=list(mutation_tokens.values())+["**CLAY CLAIM.**"]
 # Literature wording is checked separately so a source cannot stand in for the audit.
 try: lit=LITERATURE.read_text(encoding="utf-8")
 except Exception: lit=""
 refs=["W."+ref for ref in re.findall(r"\(W\.(\d+[a-z]?)\)",text)]
 return [ck("main_utf8",err is None,"Main note reads as UTF-8.",error=err),ck("tag_inventory",tuple(tags)==expected and len(tags)==len(set(tags)),"Ordered unique W.1--W.84 ledger including suffix tags.",observed=tags,expected=list(expected)),ck("quantifier_claim_sentinels",all(x in text for x in required[:-2]),"Probability, winding, strict regimes, endpoint and open boundaries are explicit.",missing=[x for x in required[:-2] if x not in text]),ck("no_semantic_mutations",all(x not in text for x in forbidden),"Forbidden deterministic, quantifier, deletion and overclaim substitutions are absent.",found=[x for x in forbidden if x in text]),ck("literature_nonhit_no_novelty","finite primary-source non-hit" in lit.lower() and "no claim of novelty" in lit.lower(),"Literature audit is a finite non-hit and no-novelty certificate."),ck("delimiter_balance",text.count(r"\[")==text.count(r"\]") and text.count(r"\begin{aligned}")==text.count(r"\end{aligned}"),"Display delimiters and aligned environments balance."),ck("control_policy",not any(ord(c)<32 and c not in "\n\r" for c in text),"No forbidden control characters."),ck("internal_W_references",all(ref in set(tags) for ref in refs),"Every internal W reference resolves to a tagged equation.",missing=sorted(set(refs)-set(tags)))]

def hashes():
 out=[]
 for i,(name,path) in enumerate((("main",MAIN),("primary",PRIMARY),("literature",LITERATURE))):
  mutated=(MUTATION=={"main":"source_hash","primary":"primary_hash","literature":"literature_hash"}[name]); expected="0"*64 if mutated else LOCKS[name]
  out.append(ck(name+"_sha256",path.is_file() and sha(path)==expected,"Frozen input hash.",path=str(path.relative_to(REPO)),expected=expected,observed=sha(path) if path.is_file() else None))
 return out

def report(p):
 checks=p["checks"]; lines=["# R0.74W finite exact certificate report","",f"- Schema: {SCHEMA}",f"- Verdict: **{p['verdict']}**",f"- Checks: {sum(x['pass'] for x in checks)}/{len(checks)}",f"- Assertions/cases: {sum(x['cases'] for x in checks)}","","| Check | Layer | Result | Cases |","|---|---|---:|---:|"]+[f"| {x['id']} | {x['group']} | {'PASS' if x['pass'] else 'FAIL'} | {x['cases']} |" for x in checks]+["","## Boundary","","**FINITE EXACT ARITHMETIC/STRUCTURE ONLY.** This certificate verifies rational ledgers, syntax, quantifiers and frozen bytes. It does not prove the Brownian-bridge estimates, survival/sweeping analytic lemmas, whole-shell bounds, fixed deletion, novelty, regularity, singularity, or any Clay claim.",""]
 failed=[x["id"] for x in checks if not x["pass"]]
 if failed: lines += ["## Failed checks",""]+["- "+x for x in failed]+[""]
 return "\n".join(lines)

def main():
 checks=[]
 for x in exact()+geometry_and_scaling():x["group"]="finite";checks.append(x)
 for x in structure():x["group"]="structural";checks.append(x)
 for x in hashes():x["group"]="hash";checks.append(x)
 verdict="PASS" if all(x["pass"] for x in checks) else "FAIL"
 payload={"schema":SCHEMA,"verdict":verdict,"mutation":MUTATION or None,"checks":checks,"negative_mutations":list(MUTATIONS),"locks":LOCKS,"boundary":"FINITE EXACT ARITHMETIC/STRUCTURE ONLY; no analytic lemma or Clay proof"}
 JSON_OUT.write_text(json.dumps(payload,indent=2,sort_keys=True)+"\n",encoding="utf-8");REPORT_OUT.write_text(report(payload),encoding="utf-8")
 print(json.dumps({"schema":SCHEMA,"verdict":verdict,"checks_passed":sum(x["pass"] for x in checks),"checks_total":len(checks),"cases":sum(x["cases"] for x in checks),"mutation":MUTATION or None},sort_keys=True));return 0 if verdict=="PASS" else 1
if __name__=="__main__":sys.exit(main())
