// R0.68B-2h guarded binary128 signature-defect and resolvent engine.

#include <algorithm>
#include <array>
#include <cfloat>
#include <cfenv>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include <omp.h>

using f128 = _Float128;

static_assert(sizeof(f128) == 16, "the certificate requires binary128");
static_assert(FLT_RADIX == 2, "the certificate requires radix two");
static_assert(__FLT128_MANT_DIG__ == 113, "unexpected binary128 precision");

namespace {

constexpr int CHANNELS = 8008;
constexpr int STATES = 1792;
constexpr int OBSERVABLE_STATE = 3;
constexpr int CLASSES = 44514;
constexpr int LSB_GROUPS = 64;
constexpr int SIGNATURE_COORDINATES = 14;
constexpr int DEGREES = 11;
constexpr std::array<int, 11> CHANNELS_BY_DEGREE = {
    1, 7, 28, 84, 210, 462, 924, 1716, 3003, 5005, 8008
};
constexpr std::array<std::int64_t, 7> CARRY_WEIGHTS = {
    64, 24137121, 904780185, 3769909270,
    3049493910, 448102641, 4826809
};

f128 pow2_negative(int exponent) {
    f128 value = 1;
    for (int index = 0; index < exponent; ++index) value *= (f128)0.5;
    return value;
}

const f128 UNIT = pow2_negative(113);
const f128 GUARD = (f128)1 + pow2_negative(100);

f128 absolute(f128 value) { return value < 0 ? -value : value; }
bool finite_value(f128 value) { return __builtin_isfinite(value); }

f128 gamma_bound(std::uint64_t terms) {
    if (terms == 0) return 0;
    const f128 numerator = (f128)(8 * terms) * UNIT;
    if (!(numerator < 1)) throw std::runtime_error("gamma bound overflow");
    return numerator / ((f128)1 - numerator) * GUARD;
}

f128 upper_sum(f128 left, f128 right) {
    const f128 rounded = left + right;
    return rounded + gamma_bound(1)
        * (absolute(left) + absolute(right)) * GUARD;
}

f128 lower_difference(f128 left, f128 right) {
    const f128 rounded = left - right;
    return rounded - gamma_bound(1)
        * (absolute(left) + absolute(right)) * GUARD;
}

f128 positive_product_upper(f128 left, f128 right) {
    if (left < 0 || right < 0) {
        throw std::runtime_error("positive product received a negative bound");
    }
    const f128 rounded = left * right;
    return rounded / ((f128)1 - gamma_bound(1)) * GUARD;
}

f128 positive_division_upper(f128 numerator, f128 denominator) {
    if (numerator < 0 || !(denominator > 0)) {
        throw std::runtime_error("invalid positive division");
    }
    const f128 rounded = numerator / denominator;
    return rounded / ((f128)1 - gamma_bound(1)) * GUARD;
}

double as_double(f128 value) { return (double)value; }

double as_double_upper(f128 value) {
    double output = (double)value;
    if ((f128)output < value) output = std::nextafter(output, INFINITY);
    return output;
}

double as_double_lower(f128 value) {
    double output = (double)value;
    if ((f128)output > value) output = std::nextafter(output, -INFINITY);
    return output;
}

template <class T>
std::vector<T> read_vector(const std::string& filename) {
    std::ifstream input(filename, std::ios::binary | std::ios::ate);
    if (!input) throw std::runtime_error("cannot open " + filename);
    const auto bytes = input.tellg();
    if (bytes < 0 || bytes % (std::streamoff)sizeof(T) != 0) {
        throw std::runtime_error("invalid byte length in " + filename);
    }
    input.seekg(0);
    std::vector<T> output((std::size_t)bytes / sizeof(T));
    input.read(reinterpret_cast<char*>(output.data()), bytes);
    if (!input) throw std::runtime_error("cannot read " + filename);
    return output;
}

struct Interval {
    f128 centre;
    f128 radius;
};

Interval interval_multiply(const Interval& left, const Interval& right) {
    const f128 centre = left.centre * right.centre;
    const f128 uncertainty =
        (absolute(left.centre) + left.radius) * right.radius
        + left.radius * absolute(right.centre);
    const f128 gamma = gamma_bound(1);
    return {
        centre,
        (uncertainty + gamma * absolute(centre))
            / ((f128)1 - gamma) * GUARD,
    };
}

std::vector<Interval> load_double_double(
    const std::string& filename,
    std::size_t expected
) {
    const auto parts = read_vector<double>(filename);
    if (parts.size() != expected * 3) {
        throw std::runtime_error("invalid double-double array in " + filename);
    }
    std::vector<Interval> output(expected);
    for (std::size_t index = 0; index < expected; ++index) {
        const f128 high = (f128)parts[3 * index];
        const f128 low = (f128)parts[3 * index + 1];
        const f128 centre = high + low;
        const f128 radius = (
            (f128)parts[3 * index + 2]
            + gamma_bound(1) * (absolute(high) + absolute(low))
        ) * GUARD;
        output[index] = {centre, radius};
    }
    return output;
}

f128 interval_upper(const Interval& value) {
    return upper_sum(value.centre, value.radius);
}

void validate_intervals(
    const std::vector<f128>& centres,
    const std::vector<f128>& radii,
    const std::string& label
) {
    if (centres.size() != radii.size()) {
        throw std::runtime_error(label + " shape mismatch");
    }
    for (std::size_t index = 0; index < centres.size(); ++index) {
        if (!finite_value(centres[index])) {
            throw std::runtime_error(label + " has non-finite centre");
        }
        if (!finite_value(radii[index]) || radii[index] < 0) {
            throw std::runtime_error(label + " has invalid radius");
        }
    }
}

struct SparseCycle {
    std::vector<std::int64_t> indptr;
    std::vector<std::int32_t> indices;
    std::vector<std::int32_t> data;
};

SparseCycle load_cycle(const std::string& directory) {
    return {
        read_vector<std::int64_t>(directory + "/absolute-cycle.indptr.i64"),
        read_vector<std::int32_t>(directory + "/absolute-cycle.indices.i32"),
        read_vector<std::int32_t>(directory + "/absolute-cycle.data.i32"),
    };
}

int degree_of_channel(int channel) {
    return (int)(std::lower_bound(
        CHANNELS_BY_DEGREE.begin(),
        CHANNELS_BY_DEGREE.end(),
        channel + 1
    ) - CHANNELS_BY_DEGREE.begin());
}

Interval pair_heat_jet(
    const std::vector<f128>& coefficient_centre,
    const std::vector<f128>& coefficient_radius,
    const std::vector<f128>& moment_centre,
    const std::vector<f128>& moment_radius
) {
    f128 sum = 0;
    f128 absolute_sum = 0;
    f128 radius_sum = 0;
    for (int channel = 0; channel < CHANNELS; ++channel) {
        const std::size_t moment_index =
            (std::size_t)channel * STATES + OBSERVABLE_STATE;
        const Interval product = interval_multiply(
            {coefficient_centre[channel], coefficient_radius[channel]},
            {moment_centre[moment_index], moment_radius[moment_index]}
        );
        sum += product.centre;
        absolute_sum += absolute(product.centre);
        radius_sum += product.radius;
    }
    const f128 gamma = gamma_bound(CHANNELS);
    return {
        sum,
        (radius_sum + gamma * absolute_sum)
            / ((f128)1 - gamma) * GUARD,
    };
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 10) {
        std::cerr << "usage: engine DEFECT_DATA MOMENT_DATA MOMENT_OUTPUT HEAT_OUTPUT OUTPUT SOURCE_COMMIT DEFECT_MANIFEST MOMENT_RADIUS_SHA256 HEAT_RADIUS_SHA256\n";
        return 2;
    }
    if (std::fegetround() != FE_TONEAREST) {
        throw std::runtime_error("the certificate requires round-to-nearest");
    }
    const std::string data_directory = argv[1];
    const std::string moment_data_directory = argv[2];
    const std::string moment_output_directory = argv[3];
    const std::string heat_output_directory = argv[4];
    const std::string output_directory = argv[5];
    const std::string source_commit = argv[6];
    const std::string defect_manifest = argv[7];
    const std::string moment_radius_hash = argv[8];
    const std::string heat_radius_hash = argv[9];
    const double started = omp_get_wtime();

    std::cerr << "[R0.68B-2h defect] loading compressed certificate inputs\n";
    const auto class_indptr = read_vector<std::int64_t>(
        data_directory + "/class.indptr.i64"
    );
    const auto shells = read_vector<std::uint8_t>(
        data_directory + "/class.shell.u8"
    );
    const auto signatures = read_vector<std::int8_t>(
        data_directory + "/class.signature.i8"
    );
    const auto multiplicities = read_vector<std::int64_t>(
        data_directory + "/class.multiplicity.i64"
    );
    const auto states = read_vector<std::int32_t>(
        data_directory + "/state-by-lsb.i32"
    );
    if (
        class_indptr.size() != LSB_GROUPS + 1
        || shells.size() != CLASSES
        || signatures.size() != (std::size_t)CLASSES * SIGNATURE_COORDINATES
        || multiplicities.size() != CLASSES
        || states.size() != LSB_GROUPS * SIGNATURE_COORDINATES
        || class_indptr.front() != 0
        || class_indptr.back() != CLASSES
    ) throw std::runtime_error("invalid compressed signature dimensions");
    for (int group = 0; group < LSB_GROUPS; ++group) {
        if (class_indptr[group] > class_indptr[group + 1]) {
            throw std::runtime_error("nonmonotone signature indptr");
        }
    }

    const auto channel_factors = load_double_double(
        data_directory + "/channel-factor-hi-lo-radius.f64",
        CHANNELS
    );
    const auto coarse_factors = load_double_double(
        data_directory + "/coarse-channel-factor-hi-lo-radius.f64",
        CHANNELS
    );
    const auto class_degree_factors = load_double_double(
        data_directory + "/class-degree-factor-hi-lo-radius.f64",
        (std::size_t)CLASSES * DEGREES
    );
    const auto derivative_values = read_vector<double>(
        data_directory + "/derivative-upper.f64"
    );
    if (derivative_values.size() != 1 || !(derivative_values[0] > 0)) {
        throw std::runtime_error("invalid derivative upper bound");
    }
    const f128 derivative_upper = (f128)derivative_values[0] * GUARD;

    const auto moment_centre = read_vector<f128>(
        moment_output_directory + "/centred-centre.f128"
    );
    const auto moment_radius = read_vector<f128>(
        moment_output_directory + "/centred-radius.f128"
    );
    if (moment_centre.size() != (std::size_t)CHANNELS * STATES) {
        throw std::runtime_error("invalid centred moment centre array");
    }
    validate_intervals(moment_centre, moment_radius, "centred moments");

    std::vector<f128> class_values(CLASSES, 0);
    for (int group = 0; group < LSB_GROUPS; ++group) {
        const auto begin = class_indptr[group];
        const auto end = class_indptr[group + 1];
        #pragma omp parallel for schedule(dynamic, 1)
        for (auto class_index = begin; class_index < end; ++class_index) {
            f128 channel_sum = 0;
            for (int channel = 0; channel < CHANNELS; ++channel) {
                f128 signed_sum = 0;
                f128 absolute_sum = 0;
                f128 radius_sum = 0;
                std::uint64_t nonzeros = 0;
                const std::size_t signature_offset =
                    (std::size_t)class_index * SIGNATURE_COORDINATES;
                for (int coordinate = 0; coordinate < SIGNATURE_COORDINATES; ++coordinate) {
                    const int sign = signatures[signature_offset + coordinate];
                    if (!sign) continue;
                    const int state = states[group * SIGNATURE_COORDINATES + coordinate];
                    const std::size_t moment_index =
                        (std::size_t)channel * STATES + state;
                    const f128 value = (f128)sign * moment_centre[moment_index];
                    signed_sum += value;
                    absolute_sum += absolute(value);
                    radius_sum += moment_radius[moment_index];
                    ++nonzeros;
                }
                const f128 gamma = gamma_bound(nonzeros);
                const f128 dot_radius = (
                    radius_sum + gamma * absolute_sum
                ) / ((f128)1 - gamma) * GUARD;
                const f128 dot_upper = upper_sum(absolute(signed_sum), dot_radius);
                const int degree = degree_of_channel(channel);
                const Interval weight = interval_multiply(
                    channel_factors[channel],
                    class_degree_factors[
                        (std::size_t)class_index * DEGREES + degree
                    ]
                );
                channel_sum += positive_product_upper(
                    dot_upper,
                    interval_upper(weight)
                );
            }
            class_values[class_index] = channel_sum
                / ((f128)1 - gamma_bound(CHANNELS)) * GUARD;
        }
        if ((group + 1) % 8 == 0) {
            std::cerr
                << "[R0.68B-2h defect +" << std::fixed << std::setprecision(2)
                << omp_get_wtime() - started << "s] signature-groups="
                << group + 1 << "/" << LSB_GROUPS << "\n";
        }
    }
    f128 observable_defect = 0;
    for (const auto value : class_values) observable_defect += value;
    observable_defect = observable_defect
        / ((f128)1 - gamma_bound(CLASSES)) * GUARD;

    std::cerr
        << "[R0.68B-2h defect +" << std::fixed << std::setprecision(2)
        << omp_get_wtime() - started << "s] coarse weighted bound\n";
    std::vector<f128> aggregated(STATES, 0);
    #pragma omp parallel
    {
        std::vector<f128> local(STATES, 0);
        #pragma omp for schedule(static)
        for (int channel = 0; channel < CHANNELS; ++channel) {
            const f128 factor = interval_upper(coarse_factors[channel]);
            const std::size_t offset = (std::size_t)channel * STATES;
            for (int state = 0; state < STATES; ++state) {
                const f128 moment_upper = upper_sum(
                    absolute(moment_centre[offset + state]),
                    moment_radius[offset + state]
                );
                local[state] += positive_product_upper(factor, moment_upper);
            }
        }
        #pragma omp critical
        for (int state = 0; state < STATES; ++state) {
            aggregated[state] += local[state];
        }
    }
    for (auto& value : aggregated) {
        value = value / ((f128)1 - gamma_bound(CHANNELS)) * GUARD;
    }

    const auto cycle = load_cycle(data_directory);
    if (
        cycle.indptr.size() != STATES + 1
        || cycle.indices.size() != cycle.data.size()
        || cycle.indptr.front() != 0
        || cycle.indptr.back() != (std::int64_t)cycle.data.size()
    ) throw std::runtime_error("invalid exact cycle data");
    for (std::size_t position = 0; position < cycle.data.size(); ++position) {
        if (
            cycle.data[position] <= 0
            || cycle.indices[position] < 0
            || cycle.indices[position] >= STATES
        ) throw std::runtime_error("invalid absolute-path cycle entry");
    }
    std::vector<f128> coarse_bounds(STATES, 0);
    #pragma omp parallel for schedule(static)
    for (int row = 0; row < STATES; ++row) {
        f128 sum = 0;
        const auto begin = cycle.indptr[row];
        const auto end = cycle.indptr[row + 1];
        for (auto position = begin; position < end; ++position) {
            sum += (f128)cycle.data[position]
                * aggregated[cycle.indices[position]];
        }
        coarse_bounds[row] = sum
            / ((f128)1 - gamma_bound((std::uint64_t)(end - begin))) * GUARD;
    }
    f128 weighted_maximum = 0;
    int weighted_state = -1;
    for (int state = 0; state < STATES; ++state) {
        const f128 weighted = positive_division_upper(
            coarse_bounds[state],
            (f128)CARRY_WEIGHTS[state % 7]
        );
        if (weighted > weighted_maximum) {
            weighted_maximum = weighted;
            weighted_state = state;
        }
    }

    const auto root_parts = read_vector<double>(
        moment_data_directory + "/root-hi-lo-radius.f64"
    );
    if (root_parts.size() != 3) throw std::runtime_error("invalid root interval");
    const f128 root_high = (f128)root_parts[0];
    const f128 root_low = (f128)root_parts[1];
    const f128 root_centre = root_high + root_low;
    const f128 root_radius = (
        (f128)root_parts[2]
        + gamma_bound(1) * (absolute(root_high) + absolute(root_low))
    ) * GUARD;
    const f128 root_lower = lower_difference(root_centre, root_radius);
    if (!(root_lower > 0)) throw std::runtime_error("root lower endpoint is nonpositive");

    const f128 contraction = pow2_negative(20);
    const f128 resolvent_ratio = positive_division_upper(contraction, root_lower);
    const f128 ratio_denominator = lower_difference((f128)1, resolvent_ratio);
    const f128 leading = positive_division_upper(observable_defect, root_lower);
    f128 tail = positive_product_upper(
        (f128)CARRY_WEIGHTS[OBSERVABLE_STATE % 7],
        weighted_maximum
    );
    tail = positive_division_upper(tail, root_lower);
    tail = positive_product_upper(tail, resolvent_ratio);
    tail = positive_division_upper(tail, ratio_denominator);
    const f128 resolvent_observable = upper_sum(leading, tail);
    const f128 derivative_correction = positive_product_upper(
        resolvent_observable,
        derivative_upper
    );

    const auto heat_centre = read_vector<f128>(
        heat_output_directory + "/heat-coefficient-centre.f128"
    );
    const auto heat_radius = read_vector<f128>(
        heat_output_directory + "/heat-coefficient-radius.f128"
    );
    if (heat_centre.size() != CHANNELS) {
        throw std::runtime_error("invalid heat coefficient centre array");
    }
    validate_intervals(heat_centre, heat_radius, "heat coefficients");
    const Interval heat_jet = pair_heat_jet(
        heat_centre,
        heat_radius,
        moment_centre,
        moment_radius
    );
    const f128 heat_lower = lower_difference(heat_jet.centre, heat_jet.radius);
    const f128 heat_upper = upper_sum(heat_jet.centre, heat_jet.radius);
    const f128 final_lower = lower_difference(heat_lower, derivative_correction);
    const f128 final_upper = upper_sum(heat_upper, derivative_correction);
    if (!(final_upper < 0)) {
        throw std::runtime_error("corrected dominant heat interval is not negative");
    }

    std::ofstream summary(output_directory + "/summary.json");
    if (!summary) throw std::runtime_error("cannot create summary");
    summary << "{\n";
    summary << "  \"schemaVersion\": \"1.0\",\n";
    summary << "  \"status\": \"strict-passed\",\n";
    summary << "  \"classification\": \"strict corrected dominant heat sign for the fixed eighth-order construction; no all-order regularity claim\",\n";
    summary << "  \"checks\": {\"roundingModeIsNearest\": true, \"allInputIntervalsValid\": true, \"allSignatureClassesProcessed\": true, \"correctedDominantHeatIntervalIsStrictlyNegative\": true},\n";
    summary << "  \"provenance\": {\"sourceCommit\": \"" << source_commit
            << "\", \"defectPayloadManifestSha256\": \"" << defect_manifest
            << "\", \"centredMomentRadiusSha256\": \"" << moment_radius_hash
            << "\", \"heatCoefficientRadiusSha256\": \"" << heat_radius_hash
            << "\"},\n";
    summary << "  \"parameters\": {\"signatureClasses\": " << CLASSES
            << ", \"coveredFreeShifts\": 16777216, \"channels\": " << CHANNELS
            << ", \"states\": " << STATES << ", \"derivativeOrder\": 11},\n";
    summary << std::scientific << std::setprecision(17);
    summary << "  \"observableDefectUpper\": "
            << as_double_upper(observable_defect) << ",\n";
    summary << "  \"unaggregated\": {\"observableUpper\": "
            << as_double_upper(coarse_bounds[OBSERVABLE_STATE])
            << ", \"weightedMaximumUpper\": "
            << as_double_upper(weighted_maximum)
            << ", \"weightedMaximumState\": " << weighted_state << "},\n";
    summary << "  \"resolvent\": {\"rootLower\": "
            << as_double_lower(root_lower) << ", \"remainderContraction\": "
            << as_double(contraction) << ", \"ratioUpper\": "
            << as_double_upper(resolvent_ratio) << ", \"observableUpper\": "
            << as_double_upper(resolvent_observable) << "},\n";
    summary << "  \"derivativeUpper\": " << as_double_upper(derivative_upper)
            << ",\n";
    summary << "  \"heatJet\": {\"centre\": " << as_double(heat_jet.centre)
            << ", \"radiusUpper\": " << as_double_upper(heat_jet.radius)
            << ", \"lower\": " << as_double_lower(heat_lower)
            << ", \"upper\": " << as_double_upper(heat_upper) << "},\n";
    summary << "  \"derivativeCorrectionUpper\": "
            << as_double_upper(derivative_correction) << ",\n";
    summary << "  \"correctedDominantHeat\": {\"lower\": "
            << as_double_lower(final_lower) << ", \"upper\": "
            << as_double_upper(final_upper) << "},\n";
    summary << "  \"elapsedSeconds\": " << std::fixed << std::setprecision(3)
            << omp_get_wtime() - started << ",\n";
    summary << "  \"limitations\": [\"one fixed eighth-order coefficient only\", \"all Picard orders remain uncontrolled\", \"no general 3D Navier-Stokes regularity claim\"]\n";
    summary << "}\n";
    std::cerr
        << "[R0.68B-2h defect +" << std::fixed << std::setprecision(2)
        << omp_get_wtime() - started << "s] complete corrected=["
        << std::scientific << as_double_lower(final_lower) << ","
        << as_double_upper(final_upper) << "]\n";
    return 0;
}
