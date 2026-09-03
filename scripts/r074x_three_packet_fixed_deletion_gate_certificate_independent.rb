#!/usr/bin/env ruby
# frozen_string_literal: true
require "digest"
require "json"
R = File.expand_path("..", __dir__)
SRC = File.join(R, "research/r074x_three_packet_fixed_deletion_gate.md")
AUD = File.join(R, "research/r074x_three_packet_fixed_deletion_gate_primary_audit.md")
LIT = File.join(R, "research/r074x_three_packet_fixed_deletion_literature_audit.md")
PJ = ENV.fetch("R074X_INDEPENDENT_JSON", File.join(R, "research/r074x_three_packet_fixed_deletion_gate_certificate.json"))
OUT = ENV.fetch("R074X_INDEPENDENT_REPORT", File.join(R, "research/r074x_three_packet_fixed_deletion_gate_independent_audit.md"))
M = ENV.fetch("R074X_INDEPENDENT_MUTATION", "")
PYSCHEMA = "r074x-three-packet-fixed-deletion-gate-certificate-v1"
MUT = %w[fraction cross_sign payment_gap payment_normalization inf_sup_swap domain_drop equal_time_forbidden strip_to_whole fixed_gate_proved route_not_nogo x52_removed clay novelty tag reference display source_hash audit_hash dependency_hash exact_solution_removed three_packet_removed literature_hash finite_non_hit no_novelty_claim primary_schema]
LOCK = {"source_hash"=>"4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3", "audit_hash"=>"834ec846c3f8629f9e7462caf4503bfa99ba6b88288da2dd525793206de9357e", "literature_hash"=>"f58f7a1d095ba6bd8b27c41872301fd367fe784597160fe060f9cd332c64c422"}
DEPS = {"r074p_temporal_observable_triage.md"=>"a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867","r074q_common_shear_multipacket_gate.md"=>"60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695","r074q_relaxed_multipacket_cubic_obstruction.md"=>"ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d","r074s_fixed_deletion_simultaneous_height.md"=>"305bf75f978c080a1790fbc42bb9bd725f56f537785ffe0fc45e3ca815aa5dc1","r074t_schedule_invariant_dwell_coercivity.md"=>"8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd","r074u_intrinsic_certified_residence.md"=>"e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99","r074v_completed_clock_upper_route.md"=>"031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c","r074w_remote_adjacent_inward_comparison.md"=>"d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10"}
def sha(p); Digest::SHA256.file(p).hexdigest; end
def grp(id)
  n=0; v=lambda{|b,msg| n+=1; raise msg unless b}; details=yield v
  {"id"=>id,"pass"=>true,"assertions"=>n,"details"=>details}
rescue => e
  {"id"=>id,"pass"=>false,"assertions"=>n,"error"=>e.message}
end
g=[]
g << grp("independent_rationals") do |v|
  p=Rational(32,63); ch=Rational(15,16); d=ch-p; q=Rational(4,3969); q65=Rational(256,257985); a=Rational(49,14850); a_s=Rational(75,22528)
  calc=[((ch/2-p)**2-d*d)/260-q*(Rational(1,4)-1),((2*ch-p)**2-d*d)/264-3*q,((ch/2-p)**2-d*d)/260-q*(Rational(1,4)-1),((ch/4-p)**2-d*d)/260-q*(Rational(1,16)-1)]
  calc[0]=-calc[0] if M=="cross_sign"
  v.call(calc==[Rational(3667,70447104),Rational(100043,29804544),Rational(3667,70447104),Rational(147359,281788416)],"cross")
  vals=[ch*p/66,Rational(3,22)*Rational(144,5)**2-q,4*q65-a_s,16*q65-a_s,Rational(6,3969)-d*d/130,Rational(6,3969)-d*d/132,a-3*q,a/4+3*q/4,9*a/16+15*q/16]
  vals[0]+=Rational(1,10**9) if M=="fraction"
  v.call(vals==[Rational(5,693),Rational(123450676,1091475),Rational(3719797,5811886080),Rational(72925813,5811886080),Rational(12191,132088320),Rational(15263,134120448),Rational(67,242550),Rational(4601,2910600),Rational(32609,11642400)],"margins")
  rate=Rational(40,3)*Rational(8,3969)-Rational(2,3)*a_s; gap=rate-16*vals[5]; gap=-gap if M=="payment_gap"
  v.call(rate==Rational(3306805,134120448)&&gap==Rational(3062597,134120448),"payment")
  {"rate"=>rate.to_s,"gap"=>gap.to_s}
end
g << grp("independent_structure") do |v|
  s=File.read(SRC); tags=s.scan(/\\tag\{(X\.\d+)\}/).flatten; want=(1..52).map{|i|"X.#{i}"}; want<<"X.53" if M=="tag"; v.call(tags==want,"tags")
  refs=s.scan(/\(X\.(\d+)\)/).flatten.map{|x|"X.#{x}"}; refs<<"X.99" if M=="reference"; v.call((refs-tags).empty?,"refs")
  o=s.lines.count{|x|x.strip=="\\["}; c=s.lines.count{|x|x.strip=="\\]"}; o+=1 if M=="display"; v.call(o==59&&c==59,"displays")
  req=["exact smooth periodic unforced","k_3=k_1+2","I_R\\subset\\mathcal T_R","\\inf_{\\substack{S\\subset\\mathbb N","\\sup_{t\\in\\mathcal D}","\\mathcal D=\\mathcal T_R","They may also be chosen equal","ACTUAL FIXED-DELETION GATE COUNTEREXAMPLE: NOT PROVED","EQUAL-TARGET W-STRIP ROUTE: NO-GO","E_2^{\\rm strip}+E_3^{\\rm strip}","does not upper-bound the full shell clocks","payment-compatible two-coordinate proposition","\\tag{X.52}","\\mathbf{NOT\\ CLAY}"]
  extra={"payment_normalization"=>"PAYMENT_BY_TSTAR","inf_sup_swap"=>"SUP_INF","domain_drop"=>"DOMAIN_LINK_REMOVED","equal_time_forbidden"=>"EQUAL_TIME_FORBIDDEN","strip_to_whole"=>"STRIP_UPPER_IS_WHOLE","fixed_gate_proved"=>"FIXED_GATE_PROVED","route_not_nogo"=>"ROUTE_SUCCEEDS","x52_removed"=>"X52_REMOVED","clay"=>"CLAY_SOLVED","novelty"=>"NOVELTY_PROVED","exact_solution_removed"=>"EXACT_REMOVED","three_packet_removed"=>"THREE_REMOVED"}; req<<extra[M] if extra[M]; req.each{|x|v.call(s.include?(x),"missing #{x}")}
  {"tags"=>tags.length,"refs"=>refs.length}
end
g << grp("independent_hashes") do |v|
  [[SRC,"source_hash"],[AUD,"audit_hash"]].each{|p,k|v.call(sha(p)==(M==k ? "0"*64 : LOCK[k]),k)}
  DEPS.each_with_index{|(n,h),i|v.call(sha(File.join(R,"research",n))==(M=="dependency_hash"&&i==0 ? "0"*64 : h),n)}
  {"dependencies"=>8}
end
g << grp("independent_literature") do |v|
  s=File.read(LIT);v.call(sha(LIT)==(M=="literature_hash" ? "0"*64 : LOCK["literature_hash"]),"hash");v.call(s.include?("finite primary-source non-hit")&&M!="finite_non_hit","non-hit");v.call(s.include?("**not** evidence or proof of\nnovelty")&&M!="no_novelty_claim","no novelty");{"scope"=>"bounded non-hit"}
end
g << grp("python_contract") do |v|
  d=JSON.parse(File.read(PJ)); v.call(d["schema"]==(M=="primary_schema" ? "bad" : PYSCHEMA),"schema");v.call(d["verdict"]=="PASS","verdict");v.call(d["negative_mutations"]==MUT.reject{|x|x=="primary_schema"},"mutations");{"checks"=>d["checks"].length}
end
ver=g.all?{|x|x["pass"]} ? "PASS" : "FAIL"; n=g.sum{|x|x["assertions"]}
File.write(OUT,["# R0.74X independent Ruby audit","","- Verdict: **#{ver}**","- Groups: #{g.count{|x|x['pass']}}/#{g.length}","- Assertions: #{n}","","**FINITE EXACT ARITHMETIC/STRUCTURE ONLY.** No analytic, fixed-deletion, novelty, or Clay proof.",""].join("\n"))
puts JSON.generate({"verdict"=>ver,"groups_passed"=>g.count{|x|x["pass"]},"groups_total"=>g.length,"assertions"=>n,"mutation"=>M.empty? ? nil : M}); exit(ver=="PASS" ? 0 : 1)
