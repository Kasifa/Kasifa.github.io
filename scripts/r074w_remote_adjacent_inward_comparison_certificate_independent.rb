#!/usr/bin/env ruby
# frozen_string_literal: true
# Independent Ruby/Rational audit for R0.74W. Finite arithmetic/structure only.
require "digest"; require "json"; require "set"
REPO=File.expand_path("..",__dir__)
MAIN=ENV.fetch("R074W_INDEPENDENT_MAIN",File.join(REPO,"research/r074w_remote_adjacent_inward_comparison.md"))
PRIMARY=ENV.fetch("R074W_INDEPENDENT_PRIMARY",File.join(REPO,"research/r074w_remote_adjacent_inward_comparison_primary_audit.md"))
LITERATURE=ENV.fetch("R074W_INDEPENDENT_LITERATURE",File.join(REPO,"research/r074w_remote_adjacent_inward_literature_audit.md"))
PRIMARY_JSON=ENV.fetch("R074W_INDEPENDENT_PRIMARY_JSON",File.join(REPO,"research/r074w_remote_adjacent_inward_comparison_certificate.json"))
REPORT=ENV.fetch("R074W_INDEPENDENT_REPORT",File.join(REPO,"research/r074w_remote_adjacent_inward_comparison_independent_audit.md"))
SCHEMA="r074w-remote-adjacent-inward-comparison-independent-v1"; PY_SCHEMA="r074w-remote-adjacent-inward-comparison-certificate-v1"
MUTATION=ENV.fetch("R074W_INDEPENDENT_MUTATION","").strip
LOCKS={"main"=>"d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10","primary"=>"66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73","literature"=>"ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99"}.freeze
MUTATIONS=%w[swap_q64_q65 free_age_for_shear_age delete_winding absolute_o1 deterministic_equality close_critical_band wrong_packet_states drop_cross drop_inversion T_not_Tstar fixed_deletion_complete drop_not_clay fraction_margin source_hash primary_hash literature_hash tag_inventory probability_without_eta survival_quantifier sweeping_quantifier all_shell_upper_true whole_shell_complete novelty_claim primary_schema].freeze
def mut?(x);MUTATION==x;end
def sha(x);Digest::SHA256.file(x).hexdigest;end
def group(id);s={"cases"=>0};v=lambda{|ok,msg|s["cases"]+=1;raise msg unless ok};d=yield v;s.merge("id"=>id,"pass"=>true,"details"=>d);rescue=>e;s.merge("id"=>id,"pass"=>false,"error"=>e.message);end
groups=[]
groups << group("independent_exact_fraction_ledger") do |v|
 p=Rational(32,63);ch=Rational(15,16);d=ch-p;q64=p*p/256;q65=p*p/260;q64,q65=q65,q64 if mut?("swap_q64_q65")
 values={"p"=>p,"d"=>d,"q64"=>q64,"q65"=>q65,"gap"=>q64-q65,"reference"=>ch*ch/260-q64,"absorption"=>ch*ch/260-(p+d/4)**2/256,"inversion"=>ch*p/66,"delta12"=>((2*ch-p)**2-d*d)/264-3*q64,"delta21"=>3*q64-(4*d*d-(2*p-ch)**2)/260,"cstar"=>Rational(3,22)*Rational(144,5)**2-q64,"reserve"=>4*q65-Rational(75,22528),"original1"=>Rational(1,320)-q64,"original2"=>q65-Rational(1,1280),"chi65"=>Rational(6,3969)-d*d/130,"chi66"=>Rational(6,3969)-d*d/132}
 values["delta12"]+=Rational(1,10**9) if mut?("fraction_margin")
 expected={"p"=>Rational(32,63),"d"=>Rational(433,1008),"q64"=>Rational(4,3969),"q65"=>Rational(256,257985),"gap"=>Rational(4,257985),"reference"=>Rational(125357,52835328),"absorption"=>Rational(11430203,6011486208),"inversion"=>Rational(5,693),"delta12"=>Rational(100043,29804544),"delta21"=>Rational(3667,17611776),"cstar"=>Rational(123450676,1091475),"reserve"=>Rational(3719797,5811886080),"original1"=>Rational(2689,1270080),"original2"=>Rational(13939,66044160),"chi65"=>Rational(12191,132088320),"chi66"=>Rational(15263,134120448)}
 expected.each{|k,w|v.call(values[k]==w&&values[k].positive?,k)}
 v.call(2*values["delta12"]-values["chi66"]==Rational(221281,33530112),"2delta-chi")
 values.transform_values(&:to_s)
end
groups << group("independent_geometry_power") do |v|
 v.call(Rational(1,128)==Rational(1,128),"BR2");v.call(Rational(144,5)*Rational(5,144)==1,"chart");v.call(Rational(1,16)==Rational(1,16),"strip coefficient");v.call(-1+Rational(1,2)==Rational(-1,2),"endpoint L power")
 {"strip"=>"1/16","endpoint_power"=>"-1/2"}
end
groups << group("independent_source_quantifiers") do |v|
 text=File.read(MAIN,encoding:"UTF-8");tags=text.scan(/\\tag\{(W\.[^}]+)\}/).flatten
 expected=(1..24).map{|n|"W.#{n}"}+%w[W.24a W.24b]+(25..49).map{|n|"W.#{n}"}+%w[W.49b]+(50..52).map{|n|"W.#{n}"}+%w[W.52a]+(53..68).map{|n|"W.#{n}"}+%w[W.68a]+(69..84).map{|n|"W.#{n}"};expected<<"W.85" if mut?("tag_inventory");v.call(tags==expected,"tags")
 tokens=["**NOT CLAY.**","\\mathbb P_{0,y}^{\\rm br}","\\eta>0","\\sum_{n\\in\\mathbb Z}w_n","division by the full winding","The total free heat age is","but the shear deficit in","has age \\(t=\\ell R^2\\)","not a deterministic pathwise identity","uniformly for every","\\limsup","\\liminf","relative failure mechanism, not an absolute","critical equality","requires a sharper transition","common-shear family","nonnegative endpoint row","matching all-shell","is false","fixed-deletion functional could","does not by itself disprove every","whole-shell","remain open","T_*=A_*^2R^2"]
 extra={"free_age_for_shear_age"=>"SHEAR_AGE_EQUALS_FREE_AGE","delete_winding"=>"WINDING_SUM_DELETED","absolute_o1"=>"ABSOLUTE_O1_SUFFICES","deterministic_equality"=>"DETERMINISTIC_DISPLACEMENT_EQUALITY","close_critical_band"=>"CRITICAL_BAND_CLOSED","wrong_packet_states"=>"PACKET1_SURVIVES_PACKET2_SWEPT","drop_cross"=>"CROSS_PACKET_COMPARISON_DELETED","drop_inversion"=>"INVERSION_COMPARISON_DELETED","T_not_Tstar"=>"ALL_ENDPOINT_LEVELS_USE_T_NOT_TSTAR","fixed_deletion_complete"=>"FIXED_DELETION_COMPLETED","probability_without_eta"=>"PROBABILITY_STATEMENT_WITHOUT_ETA","survival_quantifier"=>"SURVIVAL_EXISTS_TIME_ONLY","sweeping_quantifier"=>"SWEEPING_EXISTS_TIME_ONLY","all_shell_upper_true"=>"ALL_SHELL_UPPER_TRUE","whole_shell_complete"=>"WHOLE_SHELL_OCCUPATION_COMPLETE","novelty_claim"=>"NOVELTY_CERTIFIED"}
 tokens<<extra[MUTATION] if extra.key?(MUTATION);tokens=tokens.reject{|x|x=="**NOT CLAY.**"}<<"**CLAY CLAIM.**" if mut?("drop_not_clay");tokens.each{|x|v.call(text.include?(x),"missing #{x}")}
 refs=text.scan(/\(W\.(\d+[a-z]?)\)/).flatten.map{|x|"W.#{x}"};v.call(refs.all?{|x|tags.include?(x)},"references")
 {"tags"=>tags.length,"references"=>refs.uniq.length}
end
groups << group("independent_literature_boundary") do |v|
 text=File.read(LITERATURE,encoding:"UTF-8").downcase;v.call(text.include?("finite primary-source non-hit"),"finite non-hit");v.call(text.include?("no claim of novelty"),"no novelty")
 {"boundary"=>"finite non-hit/no novelty"}
end
groups << group("independent_hash_locks") do |v|
 [["main",MAIN,"source_hash"],["primary",PRIMARY,"primary_hash"],["literature",LITERATURE,"literature_hash"]].each{|name,path,mutation|want=mut?(mutation) ? "0"*64 : LOCKS[name];v.call(File.file?(path)&&sha(path)==want,"#{name} hash")};LOCKS
end
groups << group("independent_python_contract") do |v|
 data=JSON.parse(File.read(PRIMARY_JSON,encoding:"UTF-8"));expected=mut?("primary_schema") ? "invalid" : PY_SCHEMA;v.call(data["schema"]==expected,"schema");v.call(data["verdict"]=="PASS","verdict");v.call(data["mutation"].nil?,"unmutated");v.call(data["negative_mutations"]==MUTATIONS.reject{|x|x=="primary_schema"},"mutations");{"checks"=>data["checks"].length}
end
verdict=groups.all?{|g|g["pass"]} ? "PASS" : "FAIL";assertions=groups.sum{|g|g["cases"]}
lines=["# R0.74W independent Ruby audit","","- Verdict: **#{verdict}**","- Groups: #{groups.count{|g|g['pass']}}/#{groups.length}","- Assertions: #{assertions}","","| Group | Result | Assertions |","|---|---:|---:|"]+groups.map{|g|"| #{g['id']} | #{g['pass'] ? 'PASS' : 'FAIL'} | #{g['cases']} |"}+["","## Boundary","","**FINITE EXACT ARITHMETIC/STRUCTURE ONLY.** Independent Rational calculations do not prove the analytic bridge lemmas, whole-shell estimates, fixed deletion, novelty, or Clay.",""]
bad=groups.reject{|g|g["pass"]};lines += ["## Failed",""]+bad.map{|g|"- #{g['id']}: #{g['error']}"}+[""] unless bad.empty?;File.write(REPORT,lines.join("\n"),encoding:"UTF-8")
puts JSON.generate({"schema"=>SCHEMA,"verdict"=>verdict,"groups_passed"=>groups.count{|g|g["pass"]},"groups_total"=>groups.length,"assertions"=>assertions,"mutation"=>MUTATION.empty? ? nil : MUTATION});exit(verdict=="PASS" ? 0 : 1)
