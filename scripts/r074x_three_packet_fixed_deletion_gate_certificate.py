#!/usr/bin/env python3
"""Finite exact/structural certificate for R0.74X; not an analytic proof."""
import hashlib,json,os,re,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];SRC=R/'research/r074x_three_packet_fixed_deletion_gate.md';AUD=R/'research/r074x_three_packet_fixed_deletion_gate_primary_audit.md';LIT=R/'research/r074x_three_packet_fixed_deletion_literature_audit.md'
JO=Path(os.environ.get('R074X_JSON',R/'research/r074x_three_packet_fixed_deletion_gate_certificate.json'));RO=Path(os.environ.get('R074X_REPORT',R/'research/r074x_three_packet_fixed_deletion_gate_certificate_report.md'))
SCHEMA='r074x-three-packet-fixed-deletion-gate-certificate-v1';M=os.environ.get('R074X_MUTATION','')
LOCK={'candidate':'4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3','audit':'834ec846c3f8629f9e7462caf4503bfa99ba6b88288da2dd525793206de9357e','literature':'f58f7a1d095ba6bd8b27c41872301fd367fe784597160fe060f9cd332c64c422'}
DEPS={'r074p_temporal_observable_triage.md':'a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867','r074q_common_shear_multipacket_gate.md':'60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695','r074q_relaxed_multipacket_cubic_obstruction.md':'ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d','r074s_fixed_deletion_simultaneous_height.md':'305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1','r074t_schedule_invariant_dwell_coercivity.md':'8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd','r074u_intrinsic_certified_residence.md':'e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99','r074v_completed_clock_upper_route.md':'031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c','r074w_remote_adjacent_inward_comparison.md':'d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10'}
MUT=('fraction','cross_sign','payment_gap','payment_normalization','inf_sup_swap','domain_drop','equal_time_forbidden','strip_to_whole','fixed_gate_proved','route_not_nogo','x52_removed','clay','novelty','tag','reference','display','source_hash','audit_hash','dependency_hash','exact_solution_removed','three_packet_removed','literature_hash','finite_non_hit','no_novelty_claim')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def ck(i,b,n,c=1,**d):return {'id':i,'pass':bool(b),'note':n,'cases':c,**d}
def exact():
 p=F(32,63);ch=F(15,16);d=ch-p;q=F(4,3969);q65=F(256,257985);a=F(49,14850);aS=F(75,22528)
 vals=[F(3667,70447104),F(100043,29804544),F(3667,70447104),F(147359,281788416)]
 calc=[((ch*F(1,2)-p)**2-d*d)/F(260)-q*(F(1,4)-1),((2*ch-p)**2-d*d)/F(264)-3*q,((ch*F(1,2)-p)**2-d*d)/F(260)-q*(F(1,4)-1),((ch*F(1,4)-p)**2-d*d)/F(260)-q*(F(1,16)-1)]
 if M=='cross_sign':calc[0]=-calc[0]
 inv=ch*p/F(66);period=F(3,22)*F(144,5)**2-q;surv=[4*q65-aS,16*q65-aS];chi=[F(3,4)*F(8,3969)-d*d/F(130),F(3,4)*F(8,3969)-d*d/F(132)]
 rate=F(40,3)*F(8,3969)-F(2,3)*aS;gap=rate-16*chi[1]
 if M=='fraction':inv+=F(1,10**9)
 if M=='payment_gap':gap=-gap
 expected={'inversion':F(5,693),'periodic':F(123450676,1091475),'survival2':F(3719797,5811886080),'survival3':F(72925813,5811886080),'chi65':F(12191,132088320),'chi66':F(15263,134120448),'payment_rate':F(3306805,134120448),'payment_gap':F(3062597,134120448),'lobe_outer':F(67,242550),'lobe_inner':F(4601,2910600),'lobe_nonadjacent':F(32609,11642400)}
 obs={'inversion':inv,'periodic':period,'survival2':surv[0],'survival3':surv[1],'chi65':chi[0],'chi66':chi[1],'payment_rate':rate,'payment_gap':gap,'lobe_outer':a-3*q,'lobe_inner':a/F(4)+3*q/F(4),'lobe_nonadjacent':9*a/F(16)+15*q/F(16)}
 rows=[ck('four_remote_cross_margins',calc==vals and all(x>0 for x in calc),'Four amplitude-weighted margins.',4,observed=[str(x) for x in calc])]
 rows += [ck(k,obs[k]==v and obs[k]>0,'Exact positive fraction.',observed=str(obs[k]),expected=str(v)) for k,v in expected.items()]
 rows.append(ck('payment_vs_16chi66',rate-16*chi[1]==F(3062597,134120448),'Payment rate exceeds 16 chi66.'))
 return rows
def structural():
 s=SRC.read_text();tags=re.findall(r'\\tag\{(X\.\d+)\}',s);refs=['X.'+x for x in re.findall(r'\(X\.(\d+)\)',s)];want=[f'X.{i}' for i in range(1,53)];want += ['X.53'] if M=='tag' else []
 req=['exact smooth periodic unforced','k_3=k_1+2','I_R\\subset\\mathcal T_R',r'\inf_{\substack{S\subset\mathbb N',r'\sup_{t\in\mathcal D}',r'\mathcal D=\mathcal T_R',r'\mathfrak L^K_{1,R}(\mathcal T_R)','They may also be chosen equal','actual fixed-deletion gate','NOT PROVED','EQUAL-TARGET W-STRIP ROUTE: NO-GO',r'E_2^{\rm strip}+E_3^{\rm strip}','does not upper-bound the full shell clocks','payment-compatible two-coordinate proposition',r'(P_R^M)^{2/3}',r'T_*=A_*^2R^2',r'\tag{X.52}',r'\mathbf{NOT\ CLAY}']
 extra={'payment_normalization':'PAYMENT_NORMALIZED_BY_TSTAR','inf_sup_swap':'SUP_INF_DELETION','domain_drop':'TERMINAL_DOMAIN_LINK_REMOVED','equal_time_forbidden':'EQUAL_TIMES_FORBIDDEN','strip_to_whole':'X51_UPPER_BOUNDS_WHOLE_CLOCK','fixed_gate_proved':'ACTUAL_FIXED_DELETION_GATE_PROVED','route_not_nogo':'EQUAL_TARGET_ROUTE_SUCCEEDS','x52_removed':'X52_REMOVED','clay':'CLAY_SOLVED','novelty':'NOVELTY_PROVED','exact_solution_removed':'EXACT_SOLUTION_REMOVED','three_packet_removed':'THREE_PACKET_REMOVED'}
 if M in extra:req.append(extra[M])
 if M=='reference':refs.append('X.99')
 opens=sum(x.strip()==r'\[' for x in s.splitlines());closes=sum(x.strip()==r'\]' for x in s.splitlines());
 if M=='display':opens+=1
 return [ck('tags',tags==want and len(tags)==len(set(tags)),'52 ordered unique tags.',52),ck('references',not(set(refs)-set(tags)),'All X references resolve.',len(refs),missing=sorted(set(refs)-set(tags))),ck('standalone_displays',opens==closes==59,'Standalone display pairs, excluding table spacing.',opens+closes,opens=opens,closes=closes),ck('claim_quantifier_sentinels',all(x in s for x in req),'Exact solution, deletion, payment and boundary sentinels.',missing=[x for x in req if x not in s]),ck('controls',not any(ord(c)<32 and c not in '\n\r' for c in s),'No forbidden controls.')]
def hashes():
 rows=[]
 for name,p in [('candidate',SRC),('audit',AUD)]:
  w='0'*64 if M==('source_hash' if name=='candidate' else 'audit_hash') else LOCK[name];rows.append(ck(name+'_hash',sha(p)==w,'Frozen input.',observed=sha(p),expected=w))
 for i,(n,h) in enumerate(DEPS.items()):
  w='0'*64 if M=='dependency_hash' and i==0 else h;p=R/'research'/n;rows.append(ck('dep_'+n[:-3],p.is_file() and sha(p)==w,'Frozen dependency.',observed=sha(p) if p.is_file() else None,expected=w))
 lit=LIT.read_text();want='0'*64 if M=='literature_hash' else LOCK['literature'];rows.append(ck('literature_hash',sha(LIT)==want,'Frozen literature boundary.',observed=sha(LIT),expected=want));rows.append(ck('literature_boundary','finite primary-source non-hit' in lit and M!='finite_non_hit','Bounded finite non-hit only.'));rows.append(ck('literature_no_novelty','**not** evidence or proof of\nnovelty' in lit and M!='no_novelty_claim','No novelty/priority inference.'))
 return rows
def main():
 checks=[]
 for x in exact():x['group']='finite';checks.append(x)
 for x in structural():x['group']='structural';checks.append(x)
 for x in hashes():x['group']='hash';checks.append(x)
 v='PASS' if all(x['pass'] for x in checks) else 'FAIL';pay={'schema':SCHEMA,'verdict':v,'mutation':M or None,'checks':checks,'negative_mutations':list(MUT),'boundary':'FINITE EXACT ARITHMETIC/STRUCTURE ONLY'}
 JO.write_text(json.dumps(pay,indent=2,sort_keys=True)+'\n');lines=['# R0.74X certificate report','',f'- Verdict: **{v}**',f"- Checks: {sum(x['pass'] for x in checks)}/{len(checks)}",f"- Cases/assertions: {sum(x['cases'] for x in checks)}",'','**FINITE EXACT ARITHMETIC/STRUCTURE ONLY.** No analytic lemma, fixed-deletion counterexample, novelty, or Clay proof.',''];RO.write_text('\n'.join(lines))
 print(json.dumps({'verdict':v,'checks_passed':sum(x['pass'] for x in checks),'checks_total':len(checks),'cases':sum(x['cases'] for x in checks),'mutation':M or None},sort_keys=True));return 0 if v=='PASS' else 1
if __name__=='__main__':sys.exit(main())
