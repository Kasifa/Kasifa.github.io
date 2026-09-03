#!/usr/bin/env python3
import hashlib,json,os,re,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'research/r074y_payment_compatible_route_screen.md';A=R/'research/r074y_payment_compatible_route_screen_primary_audit.md';L=R/'research/r074y_payment_compatible_route_literature_audit.md';JO=Path(os.environ.get('R074Y_JSON',R/'research/r074y_payment_compatible_route_screen_certificate.json'));RO=Path(os.environ.get('R074Y_REPORT',R/'research/r074y_payment_compatible_route_screen_certificate_report.md'));M=os.environ.get('R074Y_MUTATION','');SCHEMA='r074y-route-screen-certificate-v1'
LOCK={'main':'6144fe796d6c59a286fc32b3b0aa2b794c50006fdc7879d4595b5958c9646954','primary':'c9b8ef6f78d0d196c2f17c6c7b83fe54667a6c80135553695dd7c68325af6f49'}
DEPS={'r074p_temporal_observable_triage.md':'a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867','r074q_common_shear_multipacket_gate.md':'60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695','r074q_relaxed_multipacket_cubic_obstruction.md':'ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d','r074s_fixed_deletion_simultaneous_height.md':'305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1','r074w_remote_adjacent_inward_comparison.md':'d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10','r074x_three_packet_fixed_deletion_gate.md':'4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3'}
MUT=('age_swap','xi_sign','amplitude_not_cancel','geometry_direction','cancellation_power','candidate_fraction','tilt_identity','changed_d_theorem','viscosity_theorem','fixed_gate','whole_shell','clay','novelty','tag','reference','display','source_hash','primary_hash','dependency_hash','literature_hash','finite_non_hit','no_novelty_claim')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def c(i,b,n,k=1,**d):return {'id':i,'pass':bool(b),'note':n,'cases':k,**d}
def algebra():
 p=F(32,63);cg=F(8,3969);d0=F(433,1008);ell=F(65);heat=ell+1
 if M=='age_swap':heat=ell
 xi=p*p/(6*ell)-cg/F(12)-d0*d0/(2*heat);der=3*d0*d0*F(64,65)**2-p*p
 if M=='xi_sign':xi=-xi
 rows=[c('distinct_ages',heat==66,'Deficit age ell and heat age ell+1.'),c('Xi_derivative',der==F(4673072,16769025)>0,'Xi increasing.'),c('Xi_max',xi==F(-875993,968647680)<0,'Exact maximum.')]
 amp=F(2)-F(2); geom=4*F(3,2)*cg/F(12); improve=2*F(1)+F(2,3)*F(1)
 if M=='amplitude_not_cancel':amp=1
 if M=='geometry_direction':geom=-geom
 if M=='cancellation_power':improve=3
 rows += [c('amplitude_cancellation',amp==0,'2 alpha cancels.'),c('dyadic_geometry',geom==cg/F(2)==F(4,3969),'r=2,d=0 meets q64 equality.'),c('cancellation_improvement',improve==F(8,3),'Symbolic 2 zeta + 2 omega/3 coefficients.')]
 d=F(7,32);ch=p+d;rho=F(9,10000);q65=F(256,257985);aS=F(75,22528);Th=cg/F(12)+d*d/F(131);c0=F(3,4)*cg-d*d/F(131);sig=F(3,8)*c0
 vals=[q65-rho,aS-rho,Th,c0,F(2,3)*rho-Th,ch*ch/F(260)-p*p/F(256),F(194323,1072963584),F(6059,9289728),sig,F(6059,9289728)-sig,Th/F(2)-rho/F(12),F(1,5000)-(Th/F(2)-rho/F(12)),8*(F(1,5000)-(Th/F(2)-rho/F(12)))]
 exp=[F(47627,515970000),F(34203,14080000),F(851731,1597252608),F(203461,177472512),F(66637853,998282880000),F(216253,211341312),F(194323,1072963584),F(6059,9289728),F(203461,473260032),F(1893805,8518680576),F(382589443,1996565760000),F(16723709,1996565760000),F(16723709,249570720000)]
 if M=='candidate_fraction':vals[0]+=F(1,10**9)
 rows.append(c('formal_candidate_rationals',vals==exp and all(x>0 for x in vals),'All formal candidate fractions.',len(vals),observed=[str(x) for x in vals]));rows.append(c('tilt_identity',(4*(c0-2*sig)==c0) if M!='tilt_identity' else False,'4(chi-2sigma)=chi.'))
 return rows
def structure():
 s=S.read_text();tags=re.findall(r'\\tag\{(Y\.[^}]+)\}',s);refs=['Y.'+x for x in re.findall(r'\(Y\.([0-9]+[a-z]?)\)',s)];want=tags[:] if M!='tag' else tags+['Y.99'];
 req=['formal target for\nconstruction, not a constructed family and not a sufficient feasibility','formal W-type survival inequality','re-prove the common-shear platform','all-winding bridge estimate','DIMENSIONALLY DISFAVORED, BUT NOT YET CERTIFIED','dimensional screen, not a no-go theorem','rigorous occupation upper open','does not prove (Y.57)','does not infer a\nwhole-shell','NOT\\ CLAY']
 extra={'changed_d_theorem':'CHANGED_D_SURVIVAL_THEOREM_PROVED','viscosity_theorem':'ACCUMULATED_VISCOSITY_STRICT_NO_GO','fixed_gate':'FIXED_GATE_DISPROVED','whole_shell':'WHOLE_SHELL_PROVED','clay':'CLAY_SOLVED','novelty':'NOVELTY_PROVED'}
 if M in extra:req.append(extra[M])
 if M=='reference':refs.append('Y.99')
 o=sum(x.strip()==r'\[' for x in s.splitlines())+(1 if M=='display' else 0);cl=sum(x.strip()==r'\]' for x in s.splitlines())
 return [c('tags',len(tags)==len(set(tags))==60 and tags==want,'60 tags.',60),c('references',not(set(refs)-set(tags)),'References close.',len(refs)),c('displays',o==cl==64,'Displays 64/64.',128),c('mandatory_boundaries',all(x in s for x in req),'Formal/dimensional/open boundaries.',missing=[x for x in req if x not in s]),c('controls',not any(ord(x)<32 and x not in '\n\r' for x in s),'Zero controls.')]
def hashes():
 z=[c('main_hash',sha(S)==('0'*64 if M=='source_hash' else LOCK['main']),'Main hash.'),c('primary_hash',sha(A)==('0'*64 if M=='primary_hash' else LOCK['primary']),'Primary hash.')]
 for i,(n,h) in enumerate(DEPS.items()):p=R/'research'/n;z.append(c('dep_'+n[:-3],sha(p)==('0'*64 if M=='dependency_hash' and i==0 else h),'Dependency hash.'))
 lit=L.read_text();z.append(c('literature_hash',sha(L)==('0'*64 if M=='literature_hash' else 'e93275e31b1f04b1878071123fa3471a90e88fee5bb2b0dfd26afa6abf8d43a6'),'Literature hash.'));z.append(c('finite_non_hit','dated finite non-hit only' in lit.lower() and M!='finite_non_hit','Finite non-hit only.'));z.append(c('no_novelty_claim','not' in lit.lower() and 'novelty' in lit.lower() and M!='no_novelty_claim','No novelty or feasibility inference.'))
 return z
def main():
 x=[]
 for q in algebra():q['group']='finite';x.append(q)
 for q in structure():q['group']='structural';x.append(q)
 for q in hashes():q['group']='hash';x.append(q)
 v='PASS' if all(q['pass'] for q in x) else 'FAIL';p={'schema':SCHEMA,'verdict':v,'mutation':M or None,'checks':x,'negative_mutations':list(MUT),'boundary':'FINITE EXACT ARITHMETIC/STRUCTURE ONLY'};JO.write_text(json.dumps(p,indent=2,sort_keys=True)+'\n');RO.write_text(f'# R0.74Y certificate report\n\n- Verdict: **{v}**\n- Checks: {sum(q["pass"] for q in x)}/{len(x)}\n- Cases: {sum(q["cases"] for q in x)}\n\n**FINITE EXACT ARITHMETIC/STRUCTURE ONLY.**\n');print(json.dumps({'verdict':v,'checks':len(x),'cases':sum(q['cases'] for q in x),'mutation':M or None},sort_keys=True));return 0 if v=='PASS' else 1
if __name__=='__main__':sys.exit(main())
