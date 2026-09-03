#!/usr/bin/env python3
import hashlib,json,os,re,sys
from fractions import Fraction as F
from pathlib import Path
R=Path(__file__).resolve().parents[1];S=R/'research/r075c_background_shear_packing_false_positive.md';J=Path(os.getenv('R075C_JSON',R/'research/r075c_background_shear_packing_false_positive_certificate.json'));O=Path(os.getenv('R075C_REPORT',R/'research/r075c_background_shear_packing_false_positive_certificate_report.md'));M=os.getenv('R075C_MUTATION','');H='1f72f3c9d9d348f86188206690ce714df28aed661a9192c7b53bc1e5921f2f89'
D={'research/r074q_common_shear_multipacket_gate.md':'60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695','research/r074u_intrinsic_certified_residence.md':'e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99','research/r075b_bulk_clock_outer_padding_gate.md':'430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a'}
MU='cap_volume slice_area time_volume pm_rpower fraction neff heat_power heat_integral ratio b45_disproved f_proved nonzero_path source dependency tag reference display clay'.split()
def sh(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 s=S.read_text();t=re.findall(r'\\tag\{(C\.[^}]+)\}',s);refs=['C.'+x for x in re.findall(r'\(C\.([0-9]+[a-z]?)\)',s)];v=F(9,40000)-F(4279,79380000)+(F(1,10**9) if M=='fraction' else 0)
 req=['R075C_UNIVERSAL_NEFF_THRESHOLD_DISPROVED','R075C_BACKGROUND_SHEAR_DISSIPATION_PAID','R075C_TOTAL_CUBIC_PACKING_FALSE_POSITIVE','R075C_PASSIVE_DISSIPATION_OPEN','R075C_NOT_CLAY',r'X_R(t)=a_R(t)=0',r'cL^2R^3',r'CLR^2',r'R^{-1}',r'\omega L^2R^{-2}',r'N_{\rm eff}^{\rm sh}\asymp N\asymp R^{-1}',r'Ct^{-1/2}',r'\le CR.',r'C\omega LR^2B^2',r'c\omega B^3L^2R^3',r'C\omega^{1/3}L^{-1/3}\longrightarrow0','direct outer-dissipation estimate (B.45) is neither proved nor','PASSIVE DISSIPATION OPEN','NOT\\ CLAY']
 bad={'cap_volume':'CAP_L3R3','slice_area':'SLICE_L2R2','time_volume':'BLOCK_R2','pm_rpower':'PM_R_MINUS1','neff':'NEFF_CONSTANT','heat_power':'HEAT_T_MINUS1','heat_integral':'HEAT_INT_R2','ratio':'RATIO_WRONG','b45_disproved':'B45_DISPROVED','f_proved':'PASSIVE_F_PROVED','nonzero_path':'PATH_NONZERO','clay':'CLAY_SOLVED'}
 if M in bad:req.append(bad[M])
 if M=='reference':refs.append('C.99')
 op=sum(x.strip()==r'\[' for x in s.splitlines())+(M=='display');cl=sum(x.strip()==r'\]' for x in s.splitlines())
 c={'fraction':v==F(27163,158760000),'tags':len(t)==36 and len(set(t))==36 and M!='tag','refs':not(set(refs)-set(t)),'display':op==cl,'sentinels':all(x in s for x in req),'source':sh(S)==('0'*64 if M=='source' else H),'dependencies':all(sh(R/p)==h and f'`{p}` | `{h}`' in s for p,h in D.items()) and M!='dependency','controls':not any(ord(x)<32 and x not in '\t\n\r' for x in s)}
 vout='PASS' if all(c.values()) else 'FAIL';d={'schema':'r075c-v1','verdict':vout,'mutation':M or None,'checks':c,'values':{'threshold_gap':str(v)},'tags':len(t),'source_sha256':sh(S),'dependencies':D,'mutations':MU,'boundary':'universal B.44 rejected; B.45 not disproved; passive dissipation OPEN; NOT CLAY'}
 J.write_text(json.dumps(d,indent=2,sort_keys=True)+'\n');O.write_text(f'# R0.75C certificate report\n\n- Verdict: **{vout}**\n- Assertions: {sum(c.values())}/{len(c)}\n- Tags: {len(t)}\n- Mutations: {len(MU)}\n- Source: `{sh(S)}`\n\nUniversal B.44 proposal rejected; B.45 not disproved; passive dissipation OPEN. NOT CLAY.\n');print(json.dumps({'verdict':vout,'assertions':len(c),'mutation':M or None},sort_keys=True));return 0 if vout=='PASS' else 1
if __name__=='__main__':sys.exit(main())
