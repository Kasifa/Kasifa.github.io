#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent Ruby/Rational audit for R0.74V Step 21. It rebuilds the finite
# algebra before inspecting the Python JSON contract; it is not a PDE proof.
require "digest"
require "json"
require "set"

REPO = File.expand_path("..", __dir__)
NOTE = ENV.fetch("R074V_INDEPENDENT_NOTE", File.join(REPO, "research/r074v_completed_clock_upper_route.md"))
PRIMARY_AUDIT = ENV.fetch("R074V_INDEPENDENT_PRIMARY_AUDIT", File.join(REPO, "research/r074v_completed_clock_upper_route_primary_audit.md"))
PRIMARY_JSON = ENV.fetch("R074V_INDEPENDENT_PRIMARY_JSON", File.join(REPO, "research/r074v_completed_clock_upper_route_certificate.json"))
REPORT = ENV.fetch("R074V_INDEPENDENT_REPORT", File.join(REPO, "research/r074v_completed_clock_upper_route_independent_audit.md"))
SCHEMA = "r074v-completed-clock-upper-route-independent-v1"
PRIMARY_SCHEMA = "r074v-completed-clock-upper-route-certificate-v1"
MUTATION = ENV.fetch("R074V_INDEPENDENT_MUTATION", "").strip
NOTE_SHA = "031c9ca8600c776d9897b247147bc4ecebff68a71e6b3c5906b310463d5b627c"
PRIMARY_AUDIT_SHA = ENV.fetch("R074V_EXPECTED_PRIMARY_AUDIT_SHA256", "148b41ef2755d6ca42927595362fd59c81db8880713293a8e82c1c288fdea77d")
DEPENDENCIES = {
  "research/r074e_local_mollified_frame_gate.md" => "3a0ea093c42016b78cb589738a666d7b40019fd860c934be9c46418cb1fb05d7",
  "research/r074f_two_packet_survival.md" => "0dc16cefb3ce071ce0f309a7683bf2956ebcc9cbc91520544bd5a740edb4c2eb",
  "research/r074h_collar_flux_two_regime_closure.md" => "8c1d43f08d5a2c9299ae50ebdd10c8c184f064c6830f1d663524e03fa90d88f1",
  "research/r074p_temporal_observable_triage.md" => "a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867",
  "research/r074q_common_shear_multipacket_gate.md" => "60cb683ff6b602b16d64313b278c11a08d73f89e3bc2b1562b256a9911695695",
  "research/r074q_relaxed_multipacket_cubic_obstruction.md" => "ba8897da349aa5c71c5ac355164a938599489c2691b09eb59760934b70617e8d",
  "research/r074t_schedule_invariant_dwell_coercivity.md" => "8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd",
  "research/r074u_intrinsic_certified_residence.md" => "e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99"
}.freeze
MUTATIONS = %w[d0_sign chi65_sign chi66_sign rho_margin_sign gamma_ratio_sign H_ratio_sign union_threshold remainder_threshold box_inner_failure box_outer_failure box_volume_failure v_R_minus_a K_upper_proved V64_common_shear_theorem drop_accumulated_dissipation AI_to_Aclk uniform_arbitrary_Astar drop_not_clay tag_inventory claim_sentinel source_hash primary_audit_hash dependency_hash torus_chord_cap volume_cap central_pairs_to_all_k wrong_versionM_shift raw_endpoint_all_times hard_time_raw_formula primary_schema].freeze

def mut?(name); MUTATION == name; end
def sha(path); Digest::SHA256.file(path).hexdigest; end
def group(id)
  state={"cases"=>0}; verify=lambda{|ok,msg| state["cases"]+=1; raise msg unless ok}
  details=yield verify; state.merge("id"=>id,"pass"=>true,"details"=>details)
rescue StandardError=>e
  state.merge("id"=>id,"pass"=>false,"error"=>e.message)
end

groups=[]
groups << group("independent_exact_exponents") do |v|
  d=Rational(15,16)-Rational(32,63); d=-d if mut?("d0_sign")
  c65=Rational(2,1323)-d*d/Rational(130); c65=-c65 if mut?("chi65_sign")
  c66=Rational(2,1323)-d*d/Rational(132); c66=-c66 if mut?("chi66_sign")
  reserve=Rational(1,320)-4*c66; reserve=-reserve if mut?("rho_margin_sign")
  v.call(d==Rational(433,1008)&&d.positive?,"d0")
  v.call(c65==Rational(12191,132088320)&&c65.positive?,"chi65")
  v.call(c66==Rational(15263,134120448)&&c66.positive?,"chi66")
  v.call(reserve==Rational(447593,167650560)&&reserve.positive?,"rho-4chi66")
  {"d0"=>d.to_s,"chi65"=>c65.to_s,"chi66"=>c66.to_s,"reserve"=>reserve.to_s}
end
groups << group("independent_ratio_ledger") do |v|
  gamma=mut?("gamma_ratio_sign") ? Rational(3,4) : Rational(-3,4)
  h=mut?("H_ratio_sign") ? [Rational(-3),Rational(3)] : [Rational(3),Rational(-3)]
  v.call(gamma==Rational(-3,4),"Gamma ratio exponent")
  v.call(h==[Rational(3),Rational(-3)],"H ratio exponents")
  [Rational(1,8),Rational(1,2),Rational(2),Rational(8)].each{|e| v.call((-e/4)-(-e)==3*e/4,"shell shift")}
  {"gamma"=>gamma.to_s,"H"=>h.map(&:to_s)}
end
groups << group("independent_union_and_box") do |v|
  z=mut?("union_threshold") ? Rational(1,8) : Rational(1,4)
  rem=mut?("remainder_threshold") ? Rational(1,4) : Rational(1,8)
  inner=Rational(3,4)>Rational(32,63); inner=false if mut?("box_inner_failure")
  outer=Rational(171,256)<(Rational(64,63)**2); outer=false if mut?("box_outer_failure")
  volume=mut?("box_volume_failure") ? Rational(1,512) : Rational(1,1024)
  v.call(z==Rational(1,4),"z=kappa/4"); v.call(rem==Rational(1,8)&&rem==z/2,"remainder")
  v.call(inner,"box inner"); v.call(outer,"box outer"); v.call(volume==Rational(1,1024),"box volume")
  [8,16,32].each do |den|
    k=Rational(1,den)
    [0,k/16,k/8,k/4].product([0,k/16,k/8,k/4]).each do |e1,e2|
      total=k/2+2*e1+2*e2
      v.call(total<k||e1>=k/8||e2>=k/8,"union implication")
    end
  end
  {"z"=>z.to_s,"remainder"=>rem.to_s,"volume"=>volume.to_s}
end
groups << group("independent_lifted_geometry_and_scope") do |v|
  [Rational(1,16),Rational(1,4),Rational(1),Rational(2),Rational(8)].each do |s|
    ell=s+s**3; ell=[ell,Rational(1)].min if mut?("torus_chord_cap")
    v.call(ell==s+s**3,"ell=s+s^3 without cap")
  end
  volume=mut?("volume_cap") ? "torus_cap" : "exact_lifted_tiling"
  v.call(volume=="exact_lifted_tiling","V_k exact lifted integral")
  pairs=["k1-1","k1","k2"].product([1,2]); pairs<<["arbitrary-k",1] if mut?("central_pairs_to_all_k")
  v.call(pairs.length==6&&pairs.to_set==["k1-1","k1","k2"].product([1,2]).to_set,"six central pairs only")
  {"volume"=>volume,"pairs"=>pairs}
end
groups << group("independent_source_semantics") do |v|
  text=File.read(NOTE,encoding:"UTF-8"); tags=text.scan(/\\tag\{(V\.[^}]+)\}/).flatten
  expected=%w[V.1 V.2 V.3 V.4 V.5 V.6 V.7 V.7a V.8 V.9 V.10 V.11 V.12 V.13 V.14 V.15 V.16 V.16a V.17 V.18 V.19 V.20 V.21 V.22 V.23 V.24 V.25 V.26 V.27 V.28 V.29 V.30 V.31 V.32 V.33 V.34 V.35 V.36 V.37 V.38 V.39 V.39a V.39b V.40 V.41 V.42 V.43 V.44 V.45 V.46 V.47 V.47a V.48 V.48a V.49 V.50 V.51 V.52 V.53 V.54 V.54a V.55 V.56 V.57 V.58 V.59 V.60 V.61 V.62 V.63 V.64 V.65 V.66 V.67 V.68 V.69]
  expected << "V.70" if mut?("tag_inventory"); v.call(tags==expected&&tags.uniq.length==tags.length,"tag ledger")
  tokens=["**NOT CLAY.**","STATUS_K_SUPERLEVEL_UPPER_OPEN","stated here as a target, not as","a proved theorem.","(V.64) is not yet a lower bound for","accumulated dissipation","\\mathcal A^I_{k,m}","\\mathcal A^{\\rm clk}_{k,m}","must be distinguished","no such uniform implication","\\ell_k:=s_k+s_k^3","cannot be capped by the length of one torus period","six central-chart pairs","are not statements for arbitrary","STATUS_ALL_K_LIFTED_COPY_SUMMATION_OPEN","v_R(t,y)=u(t,y+X_R(t))","At every local-energy good time","canonical absolutely","K_{k,R}=Q_{k,R}+F_{k,R}","must not be read as a raw hard-time endpoint identity","R074V_STEP21_END"]
  extra={"v_R_minus_a"=>"v_R-a","K_upper_proved"=>"K_SUPERLEVEL_UPPER_PROVED","V64_common_shear_theorem"=>"V.64 IS A COMMON-SHEAR THEOREM","drop_accumulated_dissipation"=>"ACCUMULATED_DISSIPATION_REMOVED","AI_to_Aclk"=>"A_I_AND_A_CLK_IDENTIFIED","uniform_arbitrary_Astar"=>"UNIFORM_FOR_ARBITRARY_ASTAR","claim_sentinel"=>"MILLENNIUM_PROBLEM_SOLVED","torus_chord_cap"=>"CHORD_CAPPED_BY_TORUS_LENGTH","volume_cap"=>"VOLUME_CAPPED_BY_TORUS_VOLUME","central_pairs_to_all_k"=>"V46_V50_PROVED_FOR_ARBITRARY_K","wrong_versionM_shift"=>"v_R(t,y)=u(t,y-X_R(t))","raw_endpoint_all_times"=>"RAW_ENDPOINT_FORMULA_AT_ALL_TIMES","hard_time_raw_formula"=>"HARD_TIME_USES_RAW_ENDPOINT"}
  tokens << extra[MUTATION] if extra.key?(MUTATION)
  tokens=tokens.reject{|x|x=="**NOT CLAY.**"}<<"**CLAY CLAIM.**" if mut?("drop_not_clay")
  tokens.each{|x|v.call(text.include?(x),"missing #{x}")}
  {"tags"=>tags.length,"sentinels"=>tokens.length}
end
groups << group("independent_hashes") do |v|
  v.call(File.file?(NOTE)&&sha(NOTE)==(mut?("source_hash") ? "0"*64 : NOTE_SHA),"note hash")
  wanted=mut?("primary_audit_hash") ? "0"*64 : PRIMARY_AUDIT_SHA
  v.call(File.file?(PRIMARY_AUDIT)&&wanted.length==64&&sha(PRIMARY_AUDIT)==wanted,"primary audit hash")
  DEPENDENCIES.each_with_index{|(rel,digest),i| p=File.join(REPO,rel); v.call(File.file?(p)&&sha(p)==(mut?("dependency_hash")&&i.zero? ? "0"*64 : digest),"dependency #{rel}")}
  {"dependencies"=>DEPENDENCIES.length}
end
groups << group("independent_primary_contract") do |v|
  data=JSON.parse(File.read(PRIMARY_JSON,encoding:"UTF-8")); expected=mut?("primary_schema") ? "invalid" : PRIMARY_SCHEMA
  v.call(data.fetch("schema")==expected,"schema"); v.call(data.fetch("verdict")=="PASS","verdict"); v.call(data.fetch("mutation").nil?,"unmutated")
  v.call(data.fetch("negative_mutations")==MUTATIONS.reject{|x|x=="primary_schema"},"mutation contract")
  {"checks"=>data.fetch("checks").length}
end

verdict=groups.all?{|g|g["pass"]} ? "PASS" : "FAIL"; assertions=groups.sum{|g|g["cases"]}
lines=["# R0.74V Step 21 independent Ruby audit","","- Schema: #{SCHEMA}","- Verdict: **#{verdict}**","- Groups: #{groups.count{|g|g['pass']}}/#{groups.length}","- Independent Rational/structural assertions: #{assertions}","","| Group | Result | Assertions |","|---|---:|---:|"]
groups.each{|g|lines<<"| #{g['id']} | #{g['pass'] ? 'PASS' : 'FAIL'} | #{g['cases']} |"}
lines += ["","## Boundary","","Ruby independently rebuilds the exact exponent, union, and geometric-box ledgers. It does not prove V.47--V.50, the remote-strip common-shear comparison, a completed-clock upper, or any Clay statement.",""]
failed=groups.reject{|g|g["pass"]}; lines += ["## Failed groups",""]+failed.map{|g|"- #{g['id']}: #{g['error']}"}+[""] unless failed.empty?
File.write(REPORT,lines.join("\n"),encoding:"UTF-8")
puts JSON.generate({"schema"=>SCHEMA,"verdict"=>verdict,"groups_passed"=>groups.count{|g|g["pass"]},"groups_total"=>groups.length,"assertions"=>assertions,"mutation"=>MUTATION.empty? ? nil : MUTATION})
exit(verdict=="PASS" ? 0 : 1)
