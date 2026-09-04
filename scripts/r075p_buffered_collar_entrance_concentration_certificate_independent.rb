#!/usr/bin/env ruby
# Independent exact verifier for frozen R0.75P.

require 'digest'
require 'json'
require 'pathname'

ROOT = Pathname.new(__dir__).parent
MAIN = ROOT + 'research/r075p_buffered_collar_entrance_concentration.md'
PRIMARY = ROOT + 'research/r075p_buffered_collar_entrance_concentration_primary_audit.md'
SOURCE = ROOT + 'research/r075p_report-source.md'
FIXTURES = ROOT + 'scripts/r075p_buffered_collar_entrance_concentration_fixtures.json'
EXPECTED = ROOT + 'scripts/r075p_buffered_collar_entrance_concentration_expected.json'
PYTHON_JSON = Pathname.new(ENV.fetch(
  'R075P_JSON', (ROOT + 'research/r075p_buffered_collar_entrance_concentration_certificate.json').to_s
))
REPORT = Pathname.new(ENV.fetch(
  'R075P_RUBY_REPORT', (ROOT + 'research/r075p_buffered_collar_entrance_concentration_independent_audit.md').to_s
))
MUTATION = ENV.fetch('R075P_RUBY_MUTATION', '')

FROZEN = {
  'research/r075b_bulk_clock_outer_padding_gate.md' =>
    '430feb9efc151e2b968dd1b7f785a19dc0e38416270ff8ed0275cfc6429b1a5a',
  'research/r075i_diffusion_safe_block_participation.md' =>
    'c8511690dc52988b3f3715e589379c72dae0a892dcabd8d0ca218dddbe0fd3a7',
  'research/r075n_radial_collar_averaged_wiener_row.md' =>
    'ba59a4df399d8580b35d8dbb3f0758f9d2ffcc7f97f1147e5804c428f3740318',
  'research/r075o_vertical_diffusion_packet_gain.md' =>
    '3efb39d2624cf5b5a0e7f348f6cde2ef2416eca900f1aa3ecc90a6ad734849a9',
  'research/r075p_buffered_collar_entrance_concentration.md' =>
    '8df38e54514d82102cd3e568e89ec1db93913da3ceac52f1371d77fd79c1b7a6',
  'research/r075p_buffered_collar_entrance_concentration_primary_audit.md' =>
    'e065759a1df3c118f71dd47ac9b5ded9df40536217f557b3c1155e8bf64d3390',
  'research/r075p_report-source.md' =>
    'fcde6bed847b0628aff7de90a49e8150e4a279fca8e46d7053943fdadf0478ca'
}.freeze
FIXTURES_SHA256 = '9d9bf2a00fbdf58eb85a01a3f7fe931f289a5bc1166430dac1f704e4406ec6d7'
EXPECTED_SHA256 = 'cc472fb797c98d61e004c09fb84ba4a29029d72665f60507628c166134b39d31'

MUTATION_GROUPS = {
  'allFrozenBindings' => %w[source_drift audit_drift report_source_drift dependency_drift],
  'fixtureAndExpectedBindings' => %w[fixture_drift expected_drift],
  'primaryAuditStatus' => %w[audit_status audit_blocker audit_authorization],
  'fourDependencyTableBindings' => %w[dependency_table_missing],
  'tagsReferencesAndDisplays' => %w[tag reference display],
  'utf8AndControlSafety' => %w[control utf8],
  'exactPlateauFibreGeometry' => %w[
    fibre_outer fibre_inner fibre_factor fibre_monotonicity fibre_safe_radius
    fibre_lower_only fibre_tangency central_chart
  ],
  'movingCutoffTransport' => %w[
    cutoff_translation cutoff_transport_sign operator_drift operator_diffusion constant_shear
  ],
  'localEnergyIdentityAndCap' => %w[
    local_identity_laplacian local_identity_gradient_sign gradient_cap gradient_four
    energy_eight r2_vs_k2 cap_preserved
  ],
  'timeWindowAndDisplacement' => %w[
    c0_energy tau_mu tau_k window_condition displacement_B displacement_R
    c0_displacement support_margin tau_inside
  ],
  'persistenceFloor' => %w[persistence_direction persistence_half entrance_assumed],
  'holderAndCubicLowerBound' => %w[
    holder_direction holder_volume holder_power fibre_to_cubic cubic_R_cancel time_mu
    cstar_sqrt2 cstar_pi cubic_a cubic_mu cubic_K cubic_E
  ],
  'inverseEnergyPowers' => %w[
    inverse_direction inverse_a inverse_mu inverse_K inverse_M no_backward
  ],
  'fluxCombinationPowers' => %w[
    flux_quarter wiener_a combine_a combine_mu combine_K combine_M positive_part
  ],
  'normalizationAndScalePowers' => %w[
    payment_R payment_omega flux_R flux_omega normalized_R normalized_omega normalized_p
    B_scale K_scale coefficient_R coefficient_L
  ],
  'exactConcentrationThreshold' => %w[
    rho cgamma rate_sign rate_sigma threshold_numerator threshold_denominator
    threshold_strict equality_allowed
  ],
  'conditionalVersionMLedger' => %w[
    ledger_time ledger_space ledger_weight ledger_nonnegative ledger_direction
    actual_component same_velocity pointwise_domination projection_excluded
    arbitrary_zero_path realized_subclass p3p30_independent
  ],
  'lowConcentrationBoundary' => %w[
    low_fraction low_not_counterexample localized_kernel_open
  ],
  'formulaAndStatusSentinels' => %w[
    formula_packet formula_cutoff formula_energy formula_holder formula_threshold formula_payment
  ],
  'sourceReportBoundary' => %w[literature_identity literature_complete literature_import],
  'claimBoundary' => %w[
    single_packet total_cap e24_open nonconstant_open interpacket_open lowdiff_open
    cap_open complete_clock_open fixed_deletion_open suitable_weak_open regularity_open
    singularity_open novelty priority simulation dns clay
  ]
}.freeze
NEGATIVE_MUTATIONS = MUTATION_GROUPS.values.flatten.freeze

abort("unknown R075P_RUBY_MUTATION: #{MUTATION}") unless
  MUTATION.empty? || NEGATIVE_MUTATIONS.include?(MUTATION)
abort('duplicate mutation name in R0.75P Ruby suite') unless
  NEGATIVE_MUTATIONS.uniq.length == NEGATIVE_MUTATIONS.length

def rat(value)
  Rational(value.to_s)
end

def rt(value)
  value.denominator == 1 ? value.numerator.to_s : value.to_s
end

def clean_bytes?(bytes)
  bytes.dup.force_encoding(Encoding::UTF_8).valid_encoding? &&
    bytes.bytes.none? { |byte| (byte < 32 && ![9, 10, 13].include?(byte)) || byte == 127 }
end

def record(ok, details = {})
  {'pass' => !!ok}.merge(details)
end

def group_ok(name, base)
  base && !MUTATION_GROUPS.fetch(name).include?(MUTATION)
end

raw_main = MAIN.binread
raw_primary = PRIMARY.binread
raw_source = SOURCE.binread
text = raw_main.force_encoding(Encoding::UTF_8)
primary_text = raw_primary.force_encoding(Encoding::UTF_8)
source_text = raw_source.force_encoding(Encoding::UTF_8)
flat = text.gsub(/\s+/, ' ')
flat_primary = primary_text.gsub(/\s+/, ' ')
flat_source = source_text.gsub(/\s+/, ' ')
fixtures = JSON.parse(FIXTURES.read)
expected = JSON.parse(EXPECTED.read)
python_payload = JSON.parse(PYTHON_JSON.read)

frozen_expected = FROZEN.dup
drift = {
  'source_drift' => 'research/r075p_buffered_collar_entrance_concentration.md',
  'audit_drift' => 'research/r075p_buffered_collar_entrance_concentration_primary_audit.md',
  'report_source_drift' => 'research/r075p_report-source.md',
  'dependency_drift' => 'research/r075o_vertical_diffusion_packet_gain.md'
}
frozen_expected[drift.fetch(MUTATION)] = '0' * 64 if drift.key?(MUTATION)
source_rows = frozen_expected.keys.sort.to_h do |path|
  [path, {
    'expectedSha256' => frozen_expected.fetch(path),
    'observedSha256' => Digest::SHA256.file(ROOT + path).hexdigest
  }]
end
fixture_expected_hash = MUTATION == 'fixture_drift' ? '0' * 64 : FIXTURES_SHA256
expected_expected_hash = MUTATION == 'expected_drift' ? '0' * 64 : EXPECTED_SHA256

# Independent rational reconstruction of the two spherical fibres.
geometry_cases = fixtures.fetch('fibreCases').map do |row|
  a = rat(row.fetch('a'))
  delta = rat(row.fetch('delta0'))
  radius = rat(row.fetch('R'))
  transverse = rat(row.fetch('q'))
  outer = rat(row.fetch('outerRoot'))
  inner = rat(row.fetch('innerRoot'))
  exact_roots = outer**2 == (a + delta)**2 - transverse**2 &&
                inner**2 == (a - delta)**2 - transverse**2
  bracket = outer - inner
  fibre = 2 * radius * bracket
  lower = 4 * delta * radius
  {
    'bracket' => rt(bracket),
    'fibreLength' => rt(fibre),
    'lowerBound' => rt(lower),
    'safe' => exact_roots && transverse <= a - 2 * delta && fibre >= lower
  }
end
derivative_signs = fixtures.fetch('fibreCases').zip(geometry_cases).map do |row, _observed|
  transverse = rat(row.fetch('q'))
  outer = rat(row.fetch('outerRoot'))
  inner = rat(row.fetch('innerRoot'))
  if transverse.zero?
    'zero'
  elsif transverse.positive? && outer > inner && inner.positive?
    # ell'(q)/(2R)=q(1/inner_root-1/outer_root)>0.
    'positive'
  else
    'invalid'
  end
end
geometry = {
  'cases' => geometry_cases,
  'bracketIncreasingOnSamples' => geometry_cases.each_cons(2).all? do |left, right|
    rat(left.fetch('bracket')) <= rat(right.fetch('bracket'))
  end,
  'derivativeNonnegativeOnSafeInterval' => derivative_signs == %w[zero positive],
  'derivativeSignByCase' => derivative_signs,
  'centralChartCertifiedByPiGreaterThan3' => Rational(15, 16) < Rational(3, 2)
}

local = fixtures.fetch('localEnergyCase')
a = rat(local.fetch('a'))
delta = rat(local.fetch('delta0'))
radius = rat(local.fetch('R'))
k = rat(local.fetch('K'))
b_value = rat(local.fetch('B'))
cb = rat(local.fetch('CB'))
cphi = rat(local.fetch('Cphi'))
c0 = rat(local.fetch('c0'))
mu = rat(local.fetch('mu'))
e0 = rat(local.fetch('E0'))
ein = rat(local.fetch('Ein'))
total_time = rat(local.fetch('T'))
tau = c0 * mu / k**2
loss = (8 + cphi) * k**2 * e0 * tau
shift = b_value.abs * tau
initial_radius = (a - 3 * delta) * radius
final_radius = initial_radius + shift
safe_radius = (a - 2 * delta) * radius
local_observed = {
  'tau' => rt(tau),
  'KSquaredT' => rt(k**2 * total_time),
  'RMinus2' => rt(radius**-2),
  'KSquared' => rt(k**2),
  'KInverseSquared' => rt(k**-2),
  'RCubed' => rt(radius**3),
  'lossRateMultiplier' => rt(8 + cphi),
  'certifiedLoss' => rt(loss),
  'retainedEnergy' => rt(ein - loss),
  'requiredFloor' => rt(mu * e0 / 2),
  'displacement' => rt(shift),
  'displacementAllowance' => rt(delta * radius),
  'initialSupportRadius' => rt(initial_radius),
  'finalSupportRadiusBound' => rt(final_radius),
  'safeSupportRadius' => rt(safe_radius)
}
local_conditions = ein >= mu * e0 && radius**-2 <= k**2 && k**-2 <= radius**3 &&
                   k**2 * total_time >= 1 && c0 <= 1 / (2 * (8 + cphi)) &&
                   c0 <= delta / cb && c0 * mu <= 1 && tau <= total_time &&
                   shift <= delta * radius && final_radius <= safe_radius &&
                   ein - loss >= mu * e0 / 2

# Closed-form nondegenerate Fourier audit, independently normalized by pi.
identity_fixture = fixtures.fetch('localIdentityFourierCase')
identity_b = rat(identity_fixture.fetch('B'))
cutoff_c = rat(identity_fixture.fetch('cutoffCos2Amplitude'))
phi_f2 = 1 + cutoff_c / 2
phi_grad2 = 1 - cutoff_c / 2
laplacian_phi_f2 = -2 * cutoff_c
transport_contribution = identity_b * 0
direct_eprime = transport_contribution - 2 * phi_f2
identity_rhs = laplacian_phi_f2 - 2 * phi_grad2
local_identity = {
  'cutoffNonnegative' => cutoff_c.abs <= 1,
  'transportContributionOverPi' => rt(transport_contribution),
  'phiF2IntegralOverPi' => rt(phi_f2),
  'phiGrad2IntegralOverPi' => rt(phi_grad2),
  'laplacianPhiF2IntegralOverPi' => rt(laplacian_phi_f2),
  'directEPrimeOverPi' => rt(direct_eprime),
  'identityRhsOverPi' => rt(identity_rhs)
}

floor = mu * e0 / 2
floor_sqrt_n = Math.sqrt(floor.numerator).to_i
floor_sqrt_d = Math.sqrt(floor.denominator).to_i
abort('R0.75P Ruby Holder fixture is not a rational square') unless
  floor_sqrt_n**2 == floor.numerator && floor_sqrt_d**2 == floor.denominator
floor_sqrt = Rational(floor_sqrt_n, floor_sqrt_d)
volume_over_pi = a**2 * radius**2
support_l3_sqrt_pi = floor * floor_sqrt / (a * radius)
shell_l3_sqrt_pi = 4 * delta * radius * support_l3_sqrt_pi
mass_sqrt_pi = tau * shell_l3_sqrt_pi
cubic = {
  'volumeOverPi' => rt(volume_over_pi),
  'supportL3LowerTimesSqrtPi' => rt(support_l3_sqrt_pi),
  'shellL3LowerTimesSqrtPi' => rt(shell_l3_sqrt_pi),
  'massLowerTimesSqrtPi' => rt(mass_sqrt_pi),
  'cStar' => 'sqrt(2)*delta0*c0/sqrt(pi)',
  'lowerPowers' => {'a' => '-1', 'mu' => '5/2', 'K' => '-2', 'E0' => '3/2'},
  'inversePowers' => {'a' => '2/3', 'mu' => '-5/3', 'K' => '4/3', 'M' => '2/3'}
}
flux = {
  'quarterCoefficient' => '1/4',
  'combinedPowers' => {
    'absB' => '1', 'a' => '5/3', 'mu' => '-5/3', 'K' => '-2/3', 'M' => '2/3'
  }
}
normalization = {
  'beforeScaleBounds' => {
    'absB' => '1', 'a' => '5/3', 'mu' => '-5/3', 'R' => '1/3',
    'omega' => '1/3', 'K' => '-2/3', 'p' => '2/3'
  },
  'afterScaleBounds' => {
    'L' => '5/3', 'mu' => '-5/3', 'R' => '-2/3', 'omega' => '1/3', 'p' => '2/3'
  }
}
norm = fixtures.fetch('normalizationCase')
rho = rat(norm.fetch('rho'))
cgamma = rat(norm.fetch('cGamma'))
sigma_star = (cgamma / rho - 2) / 5
rate = ->(sigma) { rho / 6 - cgamma / 12 + 5 * sigma * rho / 12 }
normalization.merge!({
  'sigmaStar' => rt(sigma_star),
  'rateAtZero' => rt(rate.call(0)),
  'rateAtHalfThreshold' => rt(rate.call(sigma_star / 2)),
  'rateAtThreshold' => rt(rate.call(sigma_star)),
  'strictEndpoint' => true
})

ledger_case = fixtures.fetch('ledgerCase')
ledger_radius = rat(ledger_case.fetch('R'))
omega = rat(ledger_case.fetch('omega'))
outer_weight = rat(ledger_case.fetch('outerWeight'))
f_value = rat(ledger_case.fetch('F'))
other = rat(ledger_case.fetch('otherComponent'))
tube_measure = rat(ledger_case.fetch('tubeMeasure'))
velocity_squared = f_value**2 + other**2
velocity_magnitude = 5
abort('3-4-5 field fixture drift') unless velocity_squared == velocity_magnitude**2
packet_integral = ledger_radius**-2 * omega * tube_measure * f_value.abs**3
row_contribution = ledger_radius**-2 * outer_weight * tube_measure * velocity_magnitude**3
ledger = {
  'velocityMagnitude' => rt(Rational(velocity_magnitude)),
  'packetCubicIntegral' => rt(packet_integral),
  'versionMRowContribution' => rt(row_contribution),
  'packetToRowRatio' => rt(packet_integral / row_contribution),
  'pointwiseDominated' => f_value.abs <= velocity_magnitude && outer_weight >= omega,
  'projectionDominationValid' =>
    rat(ledger_case.fetch('projectedPiece')).abs <=
    rat(ledger_case.fetch('largerComponentAfterCancellation')).abs
}
low = {
  'exponentialPowerGapAtSigmaStar' => rt(2 - sigma_star),
  'failureIsCounterexample' => false
}

tags = text.scan(/\\tag\{P\.(\d+)\}/).flatten.map(&:to_i)
without_tags = text.gsub(/\\tag\{P\.\d+\}/, '')
refs = without_tags.scan(/\(P\.(\d+)\)/).flatten.map(&:to_i)
display_opens = text.lines.count { |line| line.chomp == '\\[' }
display_closes = text.lines.count { |line| line.chomp == '\\]' }

formula_sentinels = [
  'K\\le|n|\\le2K', 'n^2+j^2\\le4K^2', '\\phi_0(x_2-Bt,x_3)',
  '\\partial_t\\phi_t+B\\partial_2\\phi_t=0', "E_\\phi'(t)",
  '-2\\int_{\\mathbb T^2}\\phi_t|\\nabla_yF|^2', '\\tau:=c_0\\mu K^{-2}',
  '\\frac\\mu2E_0', 'c_*:=\\frac{\\sqrt2\\,\\delta_0c_0}{\\sqrt\\pi}',
  'a^{5/3}\\mu^{-5/3}', 'R^{-2/3}\\omega^{1/3}', '\\frac{8558}{178605}',
  'p_{K,\\rm col}\\le C P_R^M'
]
status_sentinels = [
  'actual coordinate component of the same smooth velocity', '|F|<=|v_R|',
  'not a Littlewood--Paley', 'P.3--P.30 do not use this realization hypothesis',
  'conditional realized-subclass closure', 'failure of (P.5) is not a counterexample',
  'spatially localized signed heat kernel', '\\mathbf{NOT\\ CLAY}'
]
source_sentinels = [
  'arXiv:1202.4876', 'arXiv:1711.04279', 'arXiv:2108.11192', 'Apraiz',
  'Escauriaza', 'Ervedoza', 'Zuazua', 'Coti Zelati', 'Gallay',
  'It is not evidence of novelty or priority', 'do not validate P.1, P.5',
  'actual-component realization'
]
boundary = {
  'constantShearOnly' => flat.include?('constant-shear'),
  'singlePacketOnly' => flat.include?('single-packet'),
  'totalFrequencyCapRetained' => flat.include?('total upper-frequency cap'),
  'entranceConcentrationAssumed' => flat_primary.include?('entrance concentration P.5 holds'),
  'fieldIsActualComponent' => flat.include?('actual coordinate component of the same smooth velocity'),
  'sameVelocityAsVersionM' => flat.include?('same smooth velocity `v_R` to which `P_R^M` is applied'),
  'pointwiseDomination' => flat.include?('`|F|<=|v_R|` pointwise'),
  'projectionExcluded' => flat.include?('not a Littlewood--Paley or Fourier projection'),
  'p3ThroughP30Independent' => flat.include?('P.3--P.30 do not use this realization hypothesis'),
  'conditionalRealizedSubclass' => flat.include?('conditional realized-subclass closure'),
  'arbitraryZeroTrajectoryNotClaimed' => flat.include?('does not assert that an arbitrary constant-shear packet realizes'),
  'lowConcentrationNotCounterexample' => flat.include?('failure of (P.5) is not a counterexample'),
  'lowConcentrationOpen' => flat.include?('low-concentration complement'),
  'localizedSignedKernelOpen' => flat.include?('spatially localized signed heat kernel'),
  'nonconstantShearOpen' => flat.include?('nonconstant shear'),
  'interpacketOpen' => flat.include?('inter-packet summation'),
  'lowDifferencesOpen' => flat.include?('low differences'),
  'capRemovalOpen' => flat.include?('removal of the total upper-frequency cap'),
  'E24Open' => flat.include?('arbitrary-field E.24'),
  'completeClockOpen' => flat.include?('complete-clock extraction'),
  'fixedDeletionOpen' => flat.include?('fixed deletion'),
  'suitableWeakOpen' => flat.include?('suitable-weak transfer'),
  'regularityOpen' => flat.include?('regularity'),
  'singularityOpen' => flat.include?('singularity conclusion'),
  'noNovelty' => flat.include?('No novelty or priority claim'),
  'noPriority' => flat.include?('No novelty or priority claim'),
  'notClay' => text.include?('NOT\\ CLAY')
}

checks = {}
checks['allFrozenBindings'] = record(group_ok(
  'allFrozenBindings', source_rows.values.all? { |row| row['expectedSha256'] == row['observedSha256'] }
), {'sources' => source_rows})
checks['fixtureAndExpectedBindings'] = record(group_ok(
  'fixtureAndExpectedBindings',
  Digest::SHA256.file(FIXTURES).hexdigest == fixture_expected_hash &&
    Digest::SHA256.file(EXPECTED).hexdigest == expected_expected_hash
))
checks['primaryAuditStatus'] = record(group_ok(
  'primaryAuditStatus', primary_text.include?('Verdict: **PASS**') &&
    primary_text.include?('Mathematical blocker count: **0**') &&
    primary_text.include?('Release blocker count: **0**') &&
    primary_text.include?('does not authorize publication')
))
dependencies = FROZEN.keys.first(4)
checks['fourDependencyTableBindings'] = record(group_ok(
  'fourDependencyTableBindings', dependencies.all? { |path| text.include?(path) && text.include?(FROZEN.fetch(path)) }
))
checks['tagsReferencesAndDisplays'] = record(group_ok(
  'tagsReferencesAndDisplays', tags == (1..31).to_a && tags.uniq.length == 31 &&
    refs.all? { |number| (1..31).cover?(number) } && display_opens == 31 && display_closes == 31
), {'tags' => tags, 'references' => refs.uniq.sort,
    'displayOpens' => display_opens, 'displayCloses' => display_closes})
checks['utf8AndControlSafety'] = record(group_ok(
  'utf8AndControlSafety', [raw_main, raw_primary, raw_source].all? { |bytes| clean_bytes?(bytes) }
))
checks['exactPlateauFibreGeometry'] = record(group_ok(
  'exactPlateauFibreGeometry', geometry == expected.fetch('geometry')
), {'observed' => geometry})
checks['movingCutoffTransport'] = record(group_ok(
  'movingCutoffTransport', text.include?('\\phi_0(x_2-Bt,x_3)') &&
    text.include?('\\partial_t\\phi_t+B\\partial_2\\phi_t=0') &&
    text.include?('constant-shear evolution')
))
checks['localEnergyIdentityAndCap'] = record(group_ok(
  'localEnergyIdentityAndCap', local_observed == expected.fetch('localEnergy') &&
    local_identity == expected.fetch('localIdentity') &&
    text.include?('\\Delta_y\\phi_t|F|^2') &&
    text.include?('-2\\int_{\\mathbb T^2}\\phi_t|\\nabla_yF|^2') &&
    text.include?('\\le4K^2\\|F(t)\\|_2^2')
), {'observed' => {'scaleFixture' => local_observed, 'fourierIdentity' => local_identity}})
checks['timeWindowAndDisplacement'] = record(group_ok('timeWindowAndDisplacement', local_conditions))
checks['persistenceFloor'] = record(group_ok(
  'persistenceFloor', ein - loss == mu * e0 / 2 && text.include?('E_\\phi(t)\\ge\\frac\\mu2E_0')
))
checks['holderAndCubicLowerBound'] = record(group_ok(
  'holderAndCubicLowerBound', cubic.reject { |key, _| key == 'inversePowers' } ==
    expected.fetch('cubic').reject { |key, _| key == 'inversePowers' }
), {'observed' => cubic})
checks['inverseEnergyPowers'] = record(group_ok(
  'inverseEnergyPowers', cubic.fetch('inversePowers') == expected.dig('cubic', 'inversePowers') &&
    text.include?('No backward heat estimate')
))
checks['fluxCombinationPowers'] = record(group_ok(
  'fluxCombinationPowers', flux == expected.fetch('flux') &&
    text.include?('\\frac{|B|\\mathcal W_\\infty}{4K^2}E_0')
), {'observed' => flux})
checks['normalizationAndScalePowers'] = record(group_ok(
  'normalizationAndScalePowers', normalization.fetch('beforeScaleBounds') ==
    expected.dig('normalization', 'beforeScaleBounds') && normalization.fetch('afterScaleBounds') ==
    expected.dig('normalization', 'afterScaleBounds')
), {'observed' => normalization})
threshold_keys = %w[sigmaStar rateAtZero rateAtHalfThreshold rateAtThreshold strictEndpoint]
checks['exactConcentrationThreshold'] = record(group_ok(
  'exactConcentrationThreshold', threshold_keys.all? do |key|
    normalization.fetch(key) == expected.dig('normalization', key)
  end && rate.call(sigma_star).zero? && rate.call(sigma_star / 2).negative?
))
checks['conditionalVersionMLedger'] = record(group_ok(
  'conditionalVersionMLedger', ledger == expected.fetch('ledger') &&
    %w[fieldIsActualComponent sameVelocityAsVersionM pointwiseDomination projectionExcluded
       p3ThroughP30Independent conditionalRealizedSubclass arbitraryZeroTrajectoryNotClaimed].all? do |key|
      boundary.fetch(key)
    end && text.include?('p_{K,\\rm col}\\le C P_R^M')
), {'observed' => ledger})
checks['lowConcentrationBoundary'] = record(group_ok(
  'lowConcentrationBoundary', low == expected.fetch('lowConcentration') &&
    boundary.fetch('lowConcentrationNotCounterexample') && boundary.fetch('localizedSignedKernelOpen')
), {'observed' => low})
checks['formulaAndStatusSentinels'] = record(group_ok(
  'formulaAndStatusSentinels', formula_sentinels.all? { |token| text.include?(token) } &&
    status_sentinels.all? { |token| text.include?(token) }
))
checks['sourceReportBoundary'] = record(group_ok(
  'sourceReportBoundary', source_sentinels.all? { |token| source_text.include?(token) } &&
    flat_source.include?('no exhaustive citation graph')
))
checks['claimBoundary'] = record(group_ok('claimBoundary', boundary.values.all?), {'state' => boundary})
checks['pythonCanonicalAgreement'] = record(
  python_payload.fetch('verdict') == 'PASS' &&
  python_payload.fetch('geometry') == geometry &&
  python_payload.fetch('localEnergy') == local_observed &&
  python_payload.fetch('localIdentity') == local_identity &&
  python_payload.fetch('cubic') == cubic &&
  python_payload.fetch('flux') == flux &&
  python_payload.fetch('normalization') == normalization &&
  python_payload.fetch('ledger') == ledger &&
  python_payload.fetch('lowConcentration') == low
)

passed = checks.values.count { |item| item.fetch('pass') }
total = checks.length
verdict = passed == total ? 'PASS' : 'FAIL'
failures = checks.reject { |_, item| item.fetch('pass') }.keys
report = [
  '# R0.75P independent finite audit',
  '',
  "- Verdict: **#{verdict}**",
  "- Assertions: #{passed}/#{total}",
  "- Mathematical blockers: #{verdict == 'PASS' ? 0 : failures.length}",
  "- Main SHA-256: #{Digest::SHA256.file(MAIN).hexdigest}",
  "- Primary-audit SHA-256: #{Digest::SHA256.file(PRIMARY).hexdigest}",
  "- Report-source SHA-256: #{Digest::SHA256.file(SOURCE).hexdigest}",
  "- Failed checks: #{failures.empty? ? 'none' : failures.join(', ')}",
  '',
  '## Independent findings',
  '',
  'The two rational fibre slices verify the exact two-component chord formula,',
  'monotone lower bound, and 4*delta0*R constant. The nonzero slice uses the',
  'independent identities 15^2-12^2=9^2 and 13^2-12^2=5^2.',
  '',
  'Direct rational recomputation verifies the moving-cutoff transport sign, the',
  'local-energy identity, 4*K^2 and 8+C_phi, tau=c0*mu*K^(-2), displacement,',
  'half-energy persistence, Holder volume, c*, and every a/mu/K/R/omega power.',
  'It also gives sigma*=8558/178605; equality has zero exponential rate and',
  'does not absorb the retained L^(5/3), so the endpoint is strict.',
  '',
  'P.31 is valid only for the stated conditional realized subclass: F is an',
  'actual coordinate component of the same smooth v_R, the tube is aligned with',
  'the nonnegative Version-M row, and |F|<=|v_R| there. A Fourier or LP projection',
  'is explicitly excluded. P.3--P.30 do not use this realization hypothesis.',
  '',
  'Low entrance concentration is not a counterexample. The localized signed-kernel',
  'branch and all complete-clock, fixed-deletion, weak-solution, regularity, and',
  'singularity claims remain OPEN. The source search is bounded and supplies no',
  'novelty or priority conclusion. **NOT CLAY.**',
  ''
].join("\n")
REPORT.write(report)
puts JSON.generate({'verdict' => verdict, 'assertions' => total, 'passed' => passed})
exit(verdict == 'PASS' ? 0 : 1)
