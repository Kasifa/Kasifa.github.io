#!/usr/bin/env ruby
# frozen_string_literal: true

# Independent finite verifier for R0.74S Step 15A--15B.
#
# All mathematical checks are reconstructed below with Ruby Rational and
# explicit finite enumeration.  The primary Python certificate is neither
# invoked nor imported.  Its JSON is read only after the independent checks
# finish, solely to verify agreement of labels, hashes, row inventories, and
# summary counts.

require "digest"
require "json"
require "set"

REPO = File.expand_path("..", __dir__)

HYBRID_NOTE = File.expand_path(
  ENV.fetch(
    "R074S_HYBRID_NOTE",
    File.join(REPO, "research/r074s_hybrid_flux_tail_equivalence.md")
  )
)
CROWN_NOTE = File.expand_path(
  ENV.fetch(
    "R074S_CROWN_NOTE",
    File.join(REPO, "research/r074s_terminal_crown_coercivity.md")
  )
)
PRIMARY_JSON = File.expand_path(
  ENV.fetch(
    "R074S_HYBRID_CROWN_PRIMARY_JSON",
    File.join(REPO, "research/r074s_hybrid_crown_certificate.json")
  )
)
PRIMARY_GENERATOR = File.join(REPO, "scripts/r074s_hybrid_crown_certificate.py")
PRIMARY_REPORT = File.join(REPO, "research/r074s_hybrid_crown_certificate_report.md")

HYBRID_FIELD = "research/r074s_hybrid_flux_tail_equivalence.md"
CROWN_FIELD = "research/r074s_terminal_crown_coercivity.md"
PRIMARY_FIELD = "research/r074s_hybrid_crown_certificate.json"
PRIMARY_GENERATOR_FIELD = "scripts/r074s_hybrid_crown_certificate.py"
PRIMARY_REPORT_FIELD = "research/r074s_hybrid_crown_certificate_report.md"
HYBRID_SHA256 = "2e41f89e2ed13c09f64f09ace1b7884303e9add0b874e934ba210519b8a8ba5d"
CROWN_SHA256 = "c62fc127c6d6381075653819a4672cae69f1ac4e2b7b45ee2d0b033ab770fd80"
PRIMARY_SCHEMA = "r074s-hybrid-crown-certificate-v1"
PRIMARY_GENERATOR_SHA256 = "84c1d8aac5399b71a98cefc4a8ff6a0e13835c8a19e47bd5693ac76fe2bcced4"
PRIMARY_JSON_SHA256 = "38e4d15c76b4bb9a2523173c0da816d6862f9e24fe59595d9953a7aa9516a7b8"
PRIMARY_REPORT_SHA256 = "6777bc9cbfdaf0d079407e24269822e52bb36ffda13b828bdd7440a554050d87"
EXPECTED_PRIMARY_FINITE_IDS = %w[
  joint_TV_diamond_sharp_one_fifth_three_sevenths
  best_N_one_common_deletion_set
  four_to_one_minus_one_over_p_window_factor
  common_window_start_debt_identity
  first_root_jump_and_C_kappa_L
  finite_32_child_half_open_terminal_crowns
  canonical_crown_payment_cubic_identity
  converse_Holder_equality_and_flat_threshold
  pure_defect_scaled_constants
].freeze
EXPECTED_PRIMARY_BOUNDARY = {
  "ancestor_gate_S288" => "OPEN",
  "combined_gate_S303" => "OPEN",
  "common_deletion_temporal_tail_S342" => "OPEN",
  "jump_corona_PDE_lemma_S375" => "OPEN",
  "selected_crown_nonlinear_payment_S407" => "OPEN",
  "terminal_crown_closure" => "PROVED_CONDITIONAL_ON_OPEN_S407",
  "periodic_measure_clock_fixture" => "TWO_SEPARATE_ABSTRACT_STRESS_TESTS_NOT_COUPLED_NOT_NSE",
  "navier_stokes_millennium_problem_solved" => false
}.freeze

EXPECTED_TAGS = (377..416).map { |number| "S.#{number}" }.freeze

# These are semantic anchors, not byte locks.  They make an equation mutation
# fail even when SHA checking is deliberately disabled in the mutation test.
FORMULA_SENTINELS = {
  "S.377" => [%q{\sigma_k^{\rmhyb}(\tau):=\begin{cases}}, %q{z_{k,R}^{\boldsymbol\lambda}(\tau):=F_{k,R}(\tau)-F_{k,R}(\sigma_k^{\rmhyb}(\tau))}],
  "S.378" => [%q{z_k=r_k^{\rmsh}=r_k}, %q{z_k=F_{k,R}(\tau)=[F_{k,R}(\tau)]_+}, %q{z_k=r_k=0}],
  "S.379" => [%q{0\lex_k^{\rmsel}(\tau)\lez_k(\tau)}],
  "S.380" => [%q{|U_k|+|V_k|}, %q{\le\beta_{k,R}(J_\tau)<{T_k\over6}}],
  "S.381" => [%q{z_k=T_k-U_k-V_k}, %q{r_k={T_k\over3}-V_k}],
  "S.382" => [%q{{1\over5}z_k<r_k<{3\over7}z_k}],
  "S.383" => [%q{{1\over5}z_k(\tau)\ler_k(\tau)\lez_k(\tau)}, %q{z(\tau)\in\ell^1_+}],
  "S.384" => [%q{{1\over5}\mathcalS_N(z(\tau))\le\mathcalS_N(r(\tau))\le\mathcalS_N(z(\tau))}],
  "S.385" => [%q{{1\over5}\mathfrakZ_{N,R}^{\boldsymbol\lambda}(\mathcalD)\le\mathfrakR_{N,R}^{\boldsymbol\lambda}(\mathcalD)\le\mathfrakZ_{N,R}^{\boldsymbol\lambda}(\mathcalD)}],
  "S.386" => [%q{0\lez_k(\tau)\le\int_0^4h_{k,R}(\sigma)\,d\sigma\le4^{\,1-1/p}\|h_{k,R}\|_{L^p(0,4)}}],
  "S.387" => [%q{\mathcalS_N(r(\tau))\le\mathcalS_N(z(\tau))\le4^{\,1-1/p}\mathfrakH^F_{p,N,R}}],
  "S.388" => [%q{\mathfrakH^F_{p,N_F,R}\leC_HA_R}, %q{A_R=(P_R^M)^{2/3}}],
  "S.389" => [%q{\mathfrakR_{N_F,R}^{\boldsymbol\lambda}(\mathcalT_R)\le4^{\,1-1/p}C_HA_R}],
  "S.390" => [%q{C_{\rmpay}(\boldsymbol\lambda)+6\,4^{\,1-1/p}C_H}],
  "S.391" => [%q{\mathfrakC_R^M\leC(\boldsymbol\lambda,p,N_F,C_H)\left[A_R+Y_{2,R}^{\rmsf}\right]}],
  "S.392" => [%q|\alpha\in\{{\rmcub,loc,har,dr}\}|, %q{\int_{\sigma_k^{\rmhyb}(\tau)}^\tau\dotF_{k,R}^{\alpha}(t)\,dt}],
  "S.393" => [%q{r_k^{\rmsh}=G_{k,\tau,\delta}+\left[K_{k,R}(a)-{2T_k\over3}\right]+\left[Q_{k,R}(\ell_k)-Q_{k,R}(a)\right]}],
  "S.394" => [%q{\left[\sum_{k\in\mathcalR_{\rmsh}^{\le\delta}(\tau)\setminusS}G_{k,\tau,\delta}\right]_+}, %q{+\sum_{k\notinS}\omega_{k,\tau,\delta}+C_QA_R}],
  "S.395" => [%q|\inf_{\#S\leN}\Bigg\{|, %q{+\sum_{k\notinS}\omega_{k,\tau,\delta}}],
  "S.396" => [%q{{1/6+\varepsilon\over5/6+\varepsilon}\longrightarrow{1\over5}}, %q{{1/2-\varepsilon\over7/6-\varepsilon}\longrightarrow{3\over7}}],
  "S.397" => [%q{G=F(\tau)-F(a)=3-M}, %q{\omega=K(a)-2=M-2}, %q{r=G+\omega}],
  "S.398" => [%q{b_k(\tau)=\alpha^{\rmanc}_{k,\tau}(\mathbbR\times\mathbbR^3)}, %q{0\led\alpha^{\rmanc}_{k,\tau}\le\gamma_k\mathbf1_{\widehat{\mathcalU}_{k,R}(\tau)}\,d\nu_R}],
  "S.399" => [%q{\widehat{\mathcalU}_{k,R}(\tau)=\mathop{\dot\bigcup}_{T:(T,k)\in\mathscrI_{\rmtop}}\mathcalO_{Tk}}, %q{\mathcalO_{Tk}\subsetT\cap\widehat{\mathcalU}_{k,R}(\tau)}],
  "S.400" => [%q{\mathscrC_{\rmtop}:=\sum_{(T,k)\in\mathscrI_{\rmtop}}\gamma_k\rho_T}],
  "S.401" => [%q{\sum_{S\in\mathscrR(T)}\rho_S\le{m_T\over\lambda_T}=\rho_T}],
  "S.402" => [%q{\sum_{S\in\mathscrJ_j(T)}\rho_S\le\kappa^{-j}\rho_T}, %q{\le{\kappa\over\kappa-1}\rho_T}],
  "S.403" => [%q{T=\Omega_T\mathbin{\dot\cup}\mathop{\dot\bigcup}_{0\lej\leL}\mathop{\dot\bigcup}_{S\in\mathscrJ_j(T)}\Omega_S}],
  "S.404" => [%q{C_{\kappa,L}:=1+\sum_{j=0}^{L}\kappa^{-j}}, %q{C_\kappa:=1+{\kappa\over\kappa-1}={2\kappa-1\over\kappa-1}}],
  "S.405" => [%q{a_{Sk}=q_{Sk}+a_{Sk}^{\rmpay}}, %q{\sum_{(S,T,k)\in\mathscrC_L(E_\tau)}q_{Sk}\leC_qA_R}],
  "S.406" => [%q{p_{Sk}^{\rmcrown}:={\bigl(a_{Sk}^{\rmpay}\bigr)^{3/2}\over(\gamma_k\rho_S)^{1/2}}}, %q{{\bigl(a_{Sk}^{\rmpay}\bigr)^3\over\bigl(p_{Sk}^{\rmcrown}\bigr)^2}=\gamma_k\rho_S}],
  "S.407" => [%q{\sum_{(S,T,k)\in\mathscrC_L(E_\tau)}p_{Sk}^{\rmcrown}}, %q{\leC_pP_R^M.\qquad\textbf{OPEN}}],
  "S.408" => [%q{\mathcalS_{N_b}(b(\tau))\leC_qA_R+\bigl(C_\kappa\mathscrC_{\rmtop}\bigr)^{1/3}\bigl(C_pP_R^M\bigr)^{2/3}}],
  "S.409" => [%q{\sum_i{a_i^3\overp_i^2}\ge{A^3\overP^2}}, %q|\inf_{p_i\ge0,\\\\sump_i=P}\sum_i{a_i^3\overp_i^2}={A^3\overP^2}|],
  "S.410" => [%q{b_{k_i}\geH\quad(1\lei\leM)}, %q{P_H=C_MH}, %q{A_H=(C_MH)^{2/3}}],
  "S.411" => [%q{\sum_i{a_i^3\overp_i^2}\ge{H\over8C_p^2C_M^2}}],
  "S.412" => [%q{\sumq_k\geH-C_{\rmcor}^{1/3}(C_pC_MH)^{2/3}}],
  "S.413" => [%q{\sum_{n\in\mathbbZ^3}\sum_{i=1}^M}, %q{Q_i^x+(2\pi/R)n}],
  "S.414" => [%q{\rho_v=2^{-d}\rho_0}, %q{m_v=8^{-d}m_0}, %q{\Theta(v)=4^{-d}\Theta(0)}],
  "S.415" => [%q{T={5H\over3}}, %q{b=m=H}, %q{r^x={5H\over9}}, %q{\sigma={959H\over7200}<{T\over12}}, %q{x={2641H\over3600}>{T\over6}}, %q{\beta=0}],
  "S.416" => [%q{{\mathcalS_{N_b}(b)\overA_H}\ge{H\over(C_MH)^{2/3}}=C_M^{-2/3}H^{1/3}\longrightarrow\infty}]
}.freeze

def sha256(path)
  Digest::SHA256.file(path).hexdigest
end

def rational_string(value)
  "#{value.numerator}/#{value.denominator}"
end

def check(identifier, cases, failures, details = {})
  {
    "id" => identifier,
    "pass" => failures.empty?,
    "cases" => cases,
    "failures" => failures
  }.merge(details)
end

def subsets(length, budget)
  (0..[length, budget].min).flat_map do |size|
    (0...length).to_a.combination(size).to_a
  end
end

def complement_sum(values, removed)
  removed_set = removed.to_set
  values.each_with_index.inject(Rational(0)) do |sum, (value, index)|
    removed_set.include?(index) ? sum : sum + value
  end
end

def best_n(values, budget)
  subsets(values.length, budget).map { |removed| complement_sum(values, removed) }.min
end

def compact_math(value)
  value.gsub(/\s+/, "").delete("&")
end

def equations(text)
  result = {}
  text.scan(/\\\[(.*?)\\tag\{(S\.\d+)\}(.*?)\\\]/m) do |before, tag, after|
    result[tag] = compact_math("\\[#{before}\\tag{#{tag}}#{after}\\]")
  end
  result
end

def check_joint_tv
  failures = []
  cases = 0
  [Rational(1), Rational(5, 2), Rational(11, 3)].each do |total|
    (-16..16).each do |iu|
      (-16..16).each do |iv|
        u = total * Rational(iu, 108)
        v = total * Rational(iv, 108)
        next unless u.abs + v.abs < total / 6

        z = total - u - v
        r = total / 3 - v
        cases += 1
        unless z.positive? && 5 * r - z == 2 * total / 3 + u - 4 * v &&
               3 * z - 7 * r == 2 * total / 3 - 3 * u + 4 * v &&
               5 * r > z && 7 * r < 3 * z
          failures << [rational_string(total), rational_string(u), rational_string(v)]
        end
      end
    end
  end

  previous_low = nil
  previous_high = nil
  [12, 60, 600, 6000].each do |denominator|
    epsilon = Rational(1, denominator)
    plus_v = Rational(1, 6) - epsilon
    minus_v = -Rational(1, 6) + epsilon
    low = (Rational(1, 3) - plus_v) / (1 - plus_v)
    high = (Rational(1, 3) - minus_v) / (1 - minus_v)
    cases += 1
    unless low > Rational(1, 5) && high < Rational(3, 7) &&
           (previous_low.nil? || low < previous_low) &&
           (previous_high.nil? || high > previous_high)
      failures << ["sharp", denominator]
    end
    previous_low = low
    previous_high = high
  end
  check("joint_tv_exact_diamond_and_sharp_endpoints", cases, failures)
end

def check_common_best_n
  failures = []
  cases = 0
  pairs = [[Rational(0), Rational(0)], [Rational(1), Rational(1)], [Rational(3), Rational(3)]]
  [[0, 0], [1, 0], [-1, 1], [2, -1]].each do |iu, iv|
    total = Rational(6)
    u = Rational(iu, 8)
    v = Rational(iv, 8)
    next unless u.abs + v.abs < total / 6
    z = total - u - v
    r = total / 3 - v
    pairs << [r, z]
  end

  pairs.repeated_permutation(4) do |rows|
    r_values = rows.map(&:first)
    z_values = rows.map(&:last)
    (0..3).each do |budget|
      subsets(rows.length, budget).each do |removed|
        r_sum = complement_sum(r_values, removed)
        z_sum = complement_sum(z_values, removed)
        cases += 1
        failures << ["fixed", rows, budget, removed] unless z_sum / 5 <= r_sum && r_sum <= z_sum
      end
      r_tail = best_n(r_values, budget)
      z_tail = best_n(z_values, budget)
      cases += 1
      failures << ["optimized", rows, budget] unless z_tail / 5 <= r_tail && r_tail <= z_tail
    end
  end

  # N+1 flat coordinates are the minimal same-deletion stress.
  (0..5).each do |budget|
    height = Rational(7, 3)
    vector = Array.new(budget + 1, height)
    cases += 1
    failures << ["flat", budget] unless best_n(vector, budget) == height
  end
  check("one_common_best_n_deletion_equivalence", cases, failures)
end

def check_window_holder
  failures = []
  cases = 0
  [0, 1, 2, 3].repeated_permutation(4) do |integers|
    values = integers.map { |value| Rational(value) }
    total = values.inject(Rational(0), :+)
    cases += 4
    failures << ["p1", integers] unless total == values.inject(Rational(0), :+)
    failures << ["p2", integers] unless total**2 <= 4 * values.map { |v| v**2 }.inject(Rational(0), :+)
    failures << ["p3", integers] unless total**3 <= 16 * values.map { |v| v**3 }.inject(Rational(0), :+)
    failures << ["pinf", integers] unless total <= 4 * values.max
  end
  [[1, 0], [Rational(4, 3), Rational(1, 4)], [2, Rational(1, 2)], [3, Rational(2, 3)], ["infinity", 1]].each do |p, exponent|
    cases += 1
    reciprocal = p == "infinity" ? Rational(0) : Rational(1, 1) / p
    failures << ["exponent", p] unless exponent == 1 - reciprocal
  end
  check("length_four_holder_factor", cases, failures)
end

def check_common_window_debt
  failures = []
  cases = 0
  ledger_rows = []
  [Rational(3), Rational(9, 2), Rational(7)].each do |total|
    [Rational(0), total / 2, total, 3 * total].each do |clock_a|
      [[0, 0, 0], [Rational(1, 5), -Rational(1, 7), Rational(2, 9)], [-2, Rational(3, 4), -Rational(5, 6)]].each do |triple|
        q_a, q_ell, q_tau = triple
        f_a = clock_a - q_a
        f_ell = 2 * total / 3 - q_ell
        f_tau = total - q_tau
        residual = f_tau - f_ell
        common = f_tau - f_a
        debt = clock_a - 2 * total / 3
        prefix = q_ell - q_a
        cases += 1
        failures << [total, clock_a, triple] unless residual == common + debt + prefix
        ledger_rows << [residual, common, [debt, Rational(0)].max, prefix.abs]
      end
    end
  end

  ledger_rows.first(8).repeated_permutation(3) do |rows|
    residuals = rows.map { |row| row[0] }
    commons = rows.map { |row| row[1] }
    debts = rows.map { |row| row[2] }
    q_bound = rows.map { |row| row[3] }.inject(Rational(0), :+)
    subsets(3, 2).each do |removed|
      left = complement_sum(residuals, removed)
      signed_common = complement_sum(commons, removed)
      debt_sum = complement_sum(debts, removed)
      right = [signed_common, Rational(0)].max + debt_sum + q_bound
      cases += 1
      failures << ["summed", rows, removed] unless left <= right
    end
  end

  [4, 7, 100].each do |height_integer|
    height = Rational(height_integer)
    residual = Rational(1)
    common = 3 - height
    debt = height - 2
    cases += 1
    failures << ["overshoot", height_integer] unless residual == common + debt
  end
  check("common_window_identity_same_set_and_overshoot", cases, failures)
end

def all_paths(arity, depth)
  return [[]] if depth.zero?

  all_paths(arity, depth - 1).flat_map do |prefix|
    (0...arity).map { |digit| prefix + [digit] }
  end
end

def below(prefix, leaves)
  leaves.select { |leaf| leaf.first(prefix.length) == prefix }.to_set
end

def crown_pieces(arity, depth, roots, generation_one, generation_two)
  universe = all_paths(arity, depth).to_set
  pieces = []
  top = universe.dup
  roots.each { |root| top.subtract(below(root, universe)) }
  pieces << top
  roots.each do |root|
    part = below(root, universe)
    generation_one.fetch(root).each { |child| part.subtract(below(child, universe)) }
    pieces << part
  end
  generation_one.values.flatten(1).each do |node|
    part = below(node, universe)
    generation_two.fetch(node).each { |child| part.subtract(below(child, universe)) }
    pieces << part
  end
  generation_two.values.flatten(1).each { |node| pieces << below(node, universe) }
  [universe, pieces]
end

def check_jump_and_crowns
  failures = []
  cases = 0
  [Rational(3, 2), Rational(2), Rational(5, 2), Rational(7, 3)].each do |kappa|
    (0..10).each do |depth|
      finite = 1 + (0..depth).map { |j| kappa**(-j) }.inject(Rational(0), :+)
      formula = 1 + kappa / (kappa - 1) * (1 - kappa**(-(depth + 1)))
      limit = (2 * kappa - 1) / (kappa - 1)
      cases += 2
      failures << ["geometric", kappa, depth] unless finite == formula && finite <= limit
      root_radii = [Rational(1, 2), Rational(1, 3), Rational(1, 7)]
      failures << ["roots", kappa, depth] unless root_radii.inject(Rational(0), :+) <= 1
    end
  end

  arity = 32
  roots = [[0], [11], [31]]
  generation_one = {}
  roots.each { |root| generation_one[root] = [1, 17, 30].map { |digit| root + [digit] } }
  generation_two = {}
  generation_one.values.flatten(1).each do |node|
    generation_two[node] = [2, 29].map { |digit| node + [digit] }
  end
  universe, pieces = crown_pieces(arity, 3, roots, generation_one, generation_two)
  union = pieces.inject(Set.new) { |memo, piece| memo | piece }
  multiplicity = Hash.new(0)
  pieces.each { |piece| piece.each { |leaf| multiplicity[leaf] += 1 } }
  cases += universe.length + pieces.length
  failures << ["partition_union"] unless union == universe
  failures << ["partition_disjoint"] unless multiplicity.values.all? { |count| count == 1 }
  failures << ["terminal_omission"] if pieces[0...-1].inject(Set.new) { |memo, piece| memo | piece } == universe

  # Occurrence labels are deliberately preserved.  Two geometrically equal
  # top rows and two adjacent-shell rows must contribute four times.
  occurrences = [
    ["grid0/copy0/top0", 7, Rational(1, 3), Rational(2)],
    ["grid1/copy0/top0", 7, Rational(1, 3), Rational(2)],
    ["grid0/copy0/top0", 8, Rational(1, 5), Rational(2)],
    ["grid0/copy1/top0", 8, Rational(1, 5), Rational(2)]
  ]
  top_content = occurrences.map { |_label, _shell, gamma, rho| gamma * rho }.inject(Rational(0), :+)
  collapsed_content = occurrences.map { |row| row[1] }.uniq.map do |shell|
    row = occurrences.find { |candidate| candidate[1] == shell }
    row[2] * row[3]
  end.inject(Rational(0), :+)
  cases += 2
  failures << ["occurrence_content"] unless top_content > collapsed_content
  kappa = Rational(2)
  depth = 4
  crown_content = occurrences.map do |_label, _shell, gamma, rho|
    gamma * rho * (1 + (0..depth).map { |j| kappa**(-j) }.inject(Rational(0), :+))
  end.inject(Rational(0), :+)
  failures << ["coefficient_bound"] unless crown_content <= ((2 * kappa - 1) / (kappa - 1)) * top_content
  check("jump_decay_terminal_crown_partition_and_occurrence_content", cases, failures,
        "leaves" => universe.length, "crowns" => pieces.length)
end

def check_canonical_payment
  failures = []
  cases = 0
  coefficients = [Rational(1, 3), Rational(2, 5), Rational(7, 4)]
  [Rational(1, 2), Rational(1), Rational(2)].repeated_permutation(3) do |scales|
    masses = coefficients.zip(scales).map { |coefficient, scale| coefficient * scale**2 }
    payments = coefficients.zip(scales).map { |coefficient, scale| coefficient * scale**3 }
    masses.each_with_index do |mass, index|
      cases += 1
      failures << ["cube", index, scales] unless mass**3 == payments[index]**2 * coefficients[index]
    end
    cases += 1
    failures << ["holder", scales] unless masses.inject(Rational(0), :+)**3 <=
                                             coefficients.inject(Rational(0), :+) * payments.inject(Rational(0), :+)**2
  end
  # Two equal occurrence rows need two payments.  A reused single payment
  # fails the exact Holder closure, so occurrence collapse is detectable.
  cases += 2
  failures << ["double_payment"] unless Rational(2)**3 <= Rational(2) * Rational(2)**2
  failures << ["reused_payment_not_rejected"] if Rational(2)**3 <= Rational(2) * Rational(1)**2
  check("canonical_payment_cube_holder_and_repeated_incidence", cases, failures)
end

def check_converse_holder
  failures = []
  cases = 0
  values = [Rational(1, 2), Rational(1), Rational(2), Rational(3)]
  payments = [Rational(1, 3), Rational(1), Rational(5, 2)]
  values.repeated_permutation(3) do |masses|
    payments.repeated_permutation(3) do |pays|
      mass_sum = masses.inject(Rational(0), :+)
      pay_sum = pays.inject(Rational(0), :+)
      lhs = masses.zip(pays).map { |mass, pay| mass**3 / pay**2 }.inject(Rational(0), :+)
      rhs = mass_sum**3 / pay_sum**2
      cases += 1
      failures << ["converse", masses, pays] unless lhs >= rhs
    end
  end

  [[1, 2, 5], [Rational(1, 3), Rational(7, 5), 4]].each do |raw|
    masses = raw.map { |value| Rational(value) }
    mass_sum = masses.inject(Rational(0), :+)
    pay_sum = Rational(11, 3)
    pays = masses.map { |mass| pay_sum * mass / mass_sum }
    lhs = masses.zip(pays).map { |mass, pay| mass**3 / pay**2 }.inject(Rational(0), :+)
    cases += 1
    failures << ["equality", raw] unless lhs == mass_sum**3 / pay_sum**2
  end

  [[1, Rational(1, 2), 1], [2, 1, 2], [Rational(3, 2), Rational(2, 3), Rational(5, 4)]].each do |cube_root_cm, c_q, c_p|
    c_m = cube_root_cm**3
    root_h = 2 * c_q * cube_root_cm**2 + 1
    height = root_h**3
    a_h = cube_root_cm**2 * root_h**2
    q = c_q * a_h
    paid = height - q
    p_budget = c_p * c_m * height
    lower = paid**3 / p_budget**2
    displayed = height / (8 * c_p**2 * c_m**2)
    cases += 1
    failures << ["threshold", cube_root_cm, c_q, c_p] unless q <= height / 2 && lower >= displayed
  end

  [[1, 1, 1, 4], [2, Rational(3, 2), 2, 9]].each do |d, e, c, h|
    c_cor = Rational(d)**3
    c_p = Rational(e)**3
    c_m = Rational(c)**3
    height = Rational(h)**3
    paid_cap = Rational(d) * Rational(e)**2 * Rational(c)**2 * Rational(h)**2
    cases += 1
    failures << ["tradeoff", d, e, c, h] unless paid_cap**3 == c_cor * (c_p * c_m * height)**2
  end
  check("converse_holder_equality_threshold_and_tradeoff", cases, failures)
end

def check_scaled_stresses
  failures = []
  cases = 0
  [Rational(1, 5), Rational(1), Rational(7, 3), Rational(19)].each do |height|
    scale = 5 * height / 3
    total = scale
    mass = 3 * scale / 5
    residual = scale / 3
    sigma = Rational(959, 12_000) * scale
    excess = Rational(2641, 6000) * scale
    cases += 1
    unless total == 5 * height / 3 && mass == height && residual == 5 * height / 9 &&
           sigma == 959 * height / 7200 && excess == 2641 * height / 3600 &&
           sigma < total / 12 && excess > total / 6
      failures << ["clock", height]
    end
  end
  (0..12).each do |depth|
    rho = Rational(1, 2**depth)
    mass = Rational(1, 8**depth)
    density = mass / rho
    cases += 1
    failures << ["branch", depth] unless density == Rational(1, 4**depth) &&
                                                (depth.zero? || density < Rational(1, 4**(depth - 1)))
  end
  (0..6).each do |budget|
    height = Rational(27)
    c_m = Rational(8)
    vector = Array.new(budget + 1, height)
    a_h_cube = (c_m * height)**2
    ratio_cube = best_n(vector, budget)**3 / a_h_cube
    cases += 1
    failures << ["flat", budget] unless best_n(vector, budget) == height && ratio_cube == height / c_m**2
  end
  check("periodic_branching_scaled_clock_and_flat_divergence", cases, failures)
end

def semantic_errors(hybrid, crown, enforce_hash)
  errors = []
  hybrid_equations = equations(hybrid)
  crown_equations = equations(crown)
  all_equations = hybrid_equations.merge(crown_equations)
  hybrid_tags = hybrid.scan(/\\tag\{(S\.\d+)\}/).flatten
  crown_tags = crown.scan(/\\tag\{(S\.\d+)\}/).flatten
  errors << "hybrid_hash" if enforce_hash && Digest::SHA256.hexdigest(hybrid.b) != HYBRID_SHA256
  errors << "crown_hash" if enforce_hash && Digest::SHA256.hexdigest(crown.b) != CROWN_SHA256
  errors << "tag_sequence" unless hybrid_tags == (377..397).map { |n| "S.#{n}" } &&
                                 crown_tags == (398..416).map { |n| "S.#{n}" } &&
                                 (hybrid_tags + crown_tags) == EXPECTED_TAGS
  FORMULA_SENTINELS.each do |tag, sentinels|
    source = all_equations.fetch(tag, "")
    errors << "formula_#{tag.delete('.')}" unless sentinels.all? { |sentinel| source.include?(sentinel) }
  end
  errors << "display_balance" unless hybrid.scan(/\\\[/).length == hybrid.scan(/\\\]/).length &&
                                     crown.scan(/\\\[/).length == crown.scan(/\\\]/).length
  combined = hybrid + "\n" + crown
  errors << "control_character" if combined.include?("\r") || combined.each_byte.any? { |byte| byte < 32 && ![9, 10].include?(byte) }
  errors << "trailing_whitespace" if combined.lines.any? do |line|
    content = line.sub(/\n\z/, "")
    !content.strip.empty? && content.match?(/[ \t]\z/)
  end
  forbidden = combined.match?(/(?:\bwe\b|\bour\b|攻关|主攻|研究纪律|三重审计|杀死错误想法)/i)
  errors << "prose_voice" if forbidden

  hybrid_flat = hybrid.gsub(/\s+/, " ")
  crown_flat = crown.gsub(/\s+/, " ")
  hybrid_boundaries = [
    "The common-deletion estimate (S.342), Step 10 (S.243), Q.12, and Q.1 remain open.",
    "No claim of novelty, regularity, singularity formation, or a solution of the",
    "This is a boundary statement, not a new impossibility theorem for PDE cancellation.",
    "This is an **ABSTRACT SCALAR-LEDGER WITNESS**.",
    "This too is only an **ABSTRACT CLOCK",
    "outside the same arbitrary set",
    "same deletion set controls the full time norm"
  ]
  crown_boundaries = [
    "This is an **ABSTRACT METHOD OBSTRUCTION**, not a Navier--Stokes",
    "The following is an **OPEN PDE INPUT**:",
    "They are not asserted to satisfy one common completed-clock/measure identity.",
    "The measure and clocks have not been coupled even at the completed-clock",
    "same set for the defect and high-Rayleigh parts, for all tops",
    "may not be reused for different occurrences unless it is repeated in the",
    "none is silently quotiented out.",
    "**NOT CLAY.**"
  ]
  errors << "hybrid_claim_boundaries" unless hybrid_boundaries.all? { |value| hybrid_flat.include?(value) }
  errors << "crown_claim_boundaries" unless crown_boundaries.all? { |value| crown_flat.include?(value) }
  errors.uniq
end

def structural_checks(hybrid, crown)
  errors = semantic_errors(hybrid, crown, true)
  required = ["hybrid_hash", "crown_hash", "tag_sequence", "display_balance", "control_character",
              "trailing_whitespace", "prose_voice", "hybrid_claim_boundaries", "crown_claim_boundaries"] +
             EXPECTED_TAGS.map { |tag| "formula_#{tag.delete('.')}" }
  required.map { |identifier| { "id" => identifier, "pass" => !errors.include?(identifier) } }
end

def replace_once(text, old, replacement)
  raise "mutation source missing: #{old}" unless text.include?(old)

  text.sub(old, replacement)
end

def source_mutation_checks(hybrid, crown)
  mutations = [
    ["joint_tv_threshold", :hybrid, %q{<{T_k\over6}}, %q{<{T_k\over5}}, "formula_S380"],
    ["one_fifth_ratio", :hybrid, " \\boxed{\n {1\\over5}z_k<r_k", " \\boxed{\n {1\\over4}z_k<r_k", "formula_S382"],
    ["best_n_direction", :hybrid, %q{\le\mathcal S_N(z(\tau)).}, %q{\ge\mathcal S_N(z(\tau)).}, "formula_S384"],
    ["window_exponent", :hybrid, %q{4^{\,1-1/p}\|h_{k,R}\|}, %q{4^{\,1/p}\|h_{k,R}\|}, "formula_S386"],
    ["conditional_coefficient_six", :hybrid, %q{+6\,4^{\,1-1/p}C_H}, %q{+5\,4^{\,1-1/p}C_H}, "formula_S390"],
    ["debt_sign", :hybrid, %q{+\left[K_{k,R}(a)-{2T_k\over3}\right]}, %q{-\left[K_{k,R}(a)-{2T_k\over3}\right]}, "formula_S393"],
    ["common_deletion_wording", :hybrid, "outside the same arbitrary set", "outside branchwise arbitrary sets", "hybrid_claim_boundaries"],
    ["abstract_scalar_boundary", :hybrid, "This is an **ABSTRACT SCALAR-LEDGER WITNESS**.", "This is a scalar witness.", "hybrid_claim_boundaries"],
    ["first_root_direction", :crown, %q{{m_T\over\lambda_T}=\rho_T}, %q{{m_T\over\lambda_T}\ge\rho_T}, "formula_S401"],
    ["terminal_crown_depth", :crown, %q{0\le j\le L}, %q{0\le j<L}, "formula_S403"],
    ["crown_geometric_power", :crown, %q{\kappa^{-j}}, %q{\kappa^{-2j}}, "formula_S402"],
    ["canonical_payment_power", :crown, %q|{\bigl(a_{Sk}^{\rm pay}\bigr)^{3/2}|, %q|{\bigl(a_{Sk}^{\rm pay}\bigr)^{1/2}|, "formula_S406"],
    ["open_payment_promoted", :crown, %q{\textbf{OPEN}}, %q{\textbf{PROVED}}, "formula_S407"],
    ["converse_cube", :crown, %q{{a_i^3\over p_i^2}}, %q{{a_i^2\over p_i^2}}, "formula_S409"],
    ["threshold_eight", :crown, %q{{H\over8C_p^2C_M^2}}, %q{{H\over4C_p^2C_M^2}}, "formula_S411"],
    ["periodic_copy_sum", :crown, %q{\sum_{n\in\mathbb Z^3}\sum_{i=1}^M}, %q{\sum_{i=1}^M}, "formula_S413"],
    ["pure_defect_sigma", :crown, %q{\sigma={959H\over7200}}, %q{\sigma={959H\over7000}}, "formula_S415"],
    ["uncoupled_boundary", :crown, "They are\nnot asserted to satisfy one common completed-clock/measure identity.", "They are\nasserted to satisfy one common completed-clock/measure identity.", "crown_claim_boundaries"],
    ["occurrence_payment_boundary", :crown, "may not be reused for different occurrences unless it is repeated in the", "may be reused for different occurrences without repetition in the", "crown_claim_boundaries"],
    ["open_heading", :crown, "The following is an **OPEN PDE INPUT**:", "The following is a **PROVED PDE INPUT**:", "crown_claim_boundaries"]
  ]
  rows = mutations.map do |identifier, target, old, replacement, expected_error|
    begin
      mutated_hybrid = target == :hybrid ? replace_once(hybrid, old, replacement) : hybrid.dup
      mutated_crown = target == :crown ? replace_once(crown, old, replacement) : crown.dup
      errors = semantic_errors(mutated_hybrid, mutated_crown, false)
      { "id" => identifier, "pass" => errors.include?(expected_error), "errors" => errors }
    rescue StandardError => error
      { "id" => identifier, "pass" => false, "errors" => ["#{error.class}: #{error.message}"] }
    end
  end

  duplicate = crown.sub(%q{\tag{S.416}}, %q{\tag{S.415}})
  errors = semantic_errors(hybrid, duplicate, false)
  rows << { "id" => "duplicate_final_tag", "pass" => errors.include?("tag_sequence"), "errors" => errors }
  errors = semantic_errors("#{hybrid}\r", crown, false)
  rows << { "id" => "carriage_return", "pass" => errors.include?("control_character"), "errors" => errors }
  rows
end

def primary_errors(payload)
  errors = []
  errors << "schema" unless payload["schema"] == PRIMARY_SCHEMA
  errors << "overall_pass" unless payload["overall_pass"] == true
  errors << "hybrid_path" unless payload["hybrid_note_path"] == HYBRID_FIELD
  errors << "crown_path" unless payload["crown_note_path"] == CROWN_FIELD
  errors << "hybrid_hash" unless payload["hybrid_note_sha256"] == HYBRID_SHA256
  errors << "crown_hash" unless payload["crown_note_sha256"] == CROWN_SHA256
  errors << "hybrid_hash_lock" unless payload["hybrid_note_sha256_lock_enforced"] == true
  errors << "crown_hash_lock" unless payload["crown_note_sha256_lock_enforced"] == true
  errors << "generator_field" unless payload["generator_path"] == PRIMARY_GENERATOR_FIELD
  errors << "generator_payload_hash" unless payload["generator_sha256"] == PRIMARY_GENERATOR_SHA256
  finite = payload["finite_checks"]
  errors << "finite_rows" unless finite.is_a?(Array) && finite.all? { |row| row["pass"] == true }
  if finite.is_a?(Array)
    errors << "finite_ids" unless finite.map { |row| row["id"] }.to_set == EXPECTED_PRIMARY_FINITE_IDS.to_set
  end
  %w[dependency_checks structural_checks negative_checks].each do |key|
    rows = payload[key]
    errors << key unless rows.is_a?(Array) && !rows.empty? && rows.all? { |row| row["pass"] == true }
  end
  summary = payload["summary"]
  if summary.is_a?(Hash)
    errors << "finite_summary" unless summary["finite_total"] == finite.length && summary["finite_passed"] == finite.length
    errors << "structural_summary" unless summary["structural_total"] == payload["structural_checks"].length &&
                                           summary["structural_passed"] == payload["structural_checks"].length
    errors << "negative_summary" unless summary["negative_total"] == payload["negative_checks"].length &&
                                         summary["negative_passed"] == payload["negative_checks"].length
  else
    errors << "summary"
  end
  boundary = payload["claim_boundary"]
  errors << "claim_boundary_object" unless boundary.is_a?(Hash)
  if boundary.is_a?(Hash)
    EXPECTED_PRIMARY_BOUNDARY.each do |key, expected|
      errors << "claim_boundary_#{key}" unless boundary[key] == expected
    end
  end
  errors.uniq
end

def primary_mutation_checks(payload)
  mutations = {
    "overall_false" => proc { |copy| copy["overall_pass"] = false },
    "stale_hybrid_hash" => proc { |copy| copy["hybrid_note_sha256"] = "0" * 64 },
    "drop_finite_row" => proc { |copy| copy["finite_checks"].pop },
    "flip_structural_row" => proc { |copy| copy["structural_checks"][0]["pass"] = false },
    "stale_summary" => proc { |copy| copy["summary"]["negative_total"] += 1 },
    "promote_S407" => proc { |copy| copy["claim_boundary"]["selected_crown_nonlinear_payment_S407"] = "PROVED" },
    "falsely_couple_stresses" => proc { |copy| copy["claim_boundary"]["periodic_measure_clock_fixture"] = "ABSTRACT_COUPLED_LEDGER_NOT_NSE_REALIZATION" },
    "claim_Clay" => proc { |copy| copy["claim_boundary"]["navier_stokes_millennium_problem_solved"] = true }
  }
  mutations.map do |identifier, mutate|
    copy = Marshal.load(Marshal.dump(payload))
    mutate.call(copy)
    errors = primary_errors(copy)
    { "id" => identifier, "pass" => !errors.empty?, "errors" => errors }
  end
end

required = [HYBRID_NOTE, CROWN_NOTE, PRIMARY_JSON, PRIMARY_GENERATOR, PRIMARY_REPORT]
missing = required.reject { |path| File.file?(path) }
unless missing.empty?
  warn "missing required input(s): #{missing.join(', ')}"
  exit 2
end

hybrid = File.binread(HYBRID_NOTE).force_encoding(Encoding::UTF_8)
crown = File.binread(CROWN_NOTE).force_encoding(Encoding::UTF_8)

# The primary artifact is intentionally not read before these groups finish.
independent_checks = [
  check_joint_tv,
  check_common_best_n,
  check_window_holder,
  check_common_window_debt,
  check_jump_and_crowns,
  check_canonical_payment,
  check_converse_holder,
  check_scaled_stresses
]
structure = structural_checks(hybrid, crown)
source_mutations = source_mutation_checks(hybrid, crown)

primary_payload = JSON.parse(File.binread(PRIMARY_JSON))
producer_errors = primary_errors(primary_payload)
producer_errors << "primary_generator_artifact_hash" unless sha256(PRIMARY_GENERATOR) == PRIMARY_GENERATOR_SHA256
producer_errors << "primary_json_artifact_hash" unless sha256(PRIMARY_JSON) == PRIMARY_JSON_SHA256
producer_errors << "primary_report_artifact_hash" unless sha256(PRIMARY_REPORT) == PRIMARY_REPORT_SHA256
artifact_mutations = primary_mutation_checks(primary_payload)

passed = independent_checks.all? { |row| row["pass"] } &&
         structure.all? { |row| row["pass"] } &&
         source_mutations.all? { |row| row["pass"] } &&
         producer_errors.empty? &&
         artifact_mutations.all? { |row| row["pass"] }

output = {
  "schema" => "r074s-hybrid-crown-independent-audit-v1",
  "source" => {
    "hybrid_note" => HYBRID_FIELD,
    "hybrid_note_sha256" => sha256(HYBRID_NOTE),
    "crown_note" => CROWN_FIELD,
    "crown_note_sha256" => sha256(CROWN_NOTE),
    "primary_certificate" => PRIMARY_FIELD,
    "primary_certificate_sha256" => sha256(PRIMARY_JSON),
    "primary_generator" => PRIMARY_GENERATOR_FIELD,
    "primary_generator_sha256" => sha256(PRIMARY_GENERATOR),
    "primary_report" => PRIMARY_REPORT_FIELD,
    "primary_report_sha256" => sha256(PRIMARY_REPORT)
  },
  "independent_checks" => independent_checks,
  "structural_checks" => structure,
  "source_mutations" => source_mutations,
  "primary_producer_errors" => producer_errors,
  "primary_artifact_mutations" => artifact_mutations,
  "scope" => {
    "finite_algebra_combinatorics_and_statement_integrity_only" => true,
    "machine_proves_common_deletion_tail_S342" => false,
    "machine_proves_selected_crown_payment_S407" => false,
    "machine_proves_jump_corona_lemma_S375" => false,
    "machine_proves_NSE_realization_of_abstract_stresses" => false,
    "machine_proves_regularity_or_Clay" => false
  },
  "summary" => {
    "independent_groups_passed" => independent_checks.count { |row| row["pass"] },
    "independent_groups_total" => independent_checks.length,
    "independent_finite_cases" => independent_checks.map { |row| row["cases"] }.inject(0, :+),
    "structural_passed" => structure.count { |row| row["pass"] },
    "structural_total" => structure.length,
    "source_mutations_rejected" => source_mutations.count { |row| row["pass"] },
    "source_mutations_total" => source_mutations.length,
    "artifact_mutations_rejected" => artifact_mutations.count { |row| row["pass"] },
    "artifact_mutations_total" => artifact_mutations.length
  },
  "pass" => passed
}

puts JSON.pretty_generate(output)
exit(passed ? 0 : 1)
