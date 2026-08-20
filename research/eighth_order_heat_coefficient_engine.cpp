// R0.68B-2g guarded binary128 heat-coefficient and moment-pairing engine.

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
static_assert(__FLT128_MANT_DIG__ == 113, "unexpected _Float128 precision");

namespace {

constexpr int CHANNELS = 8008;
constexpr int STATES = 1792;
constexpr int OBSERVABLE_STATE = 3;
constexpr int BETA_COUNT = 28;
constexpr int SHUFFLES = 35;
constexpr int RATES_PER_SHUFFLE = 7;
constexpr int RATE_COUNT = SHUFFLES * RATES_PER_SHUFFLE;
constexpr int SERIES_ORDER = 64;
constexpr int ORDERS = SERIES_ORDER + 1;
constexpr std::array<int, 11> CHANNELS_BY_DEGREE = {
    1, 7, 28, 84, 210, 462, 924, 1716, 3003, 5005, 8008
};

f128 pow2_negative(int exponent) {
    f128 value = 1;
    for (int index = 0; index < exponent; ++index) value *= (f128)0.5;
    return value;
}

const f128 UNIT = pow2_negative(113);
const f128 ARITHMETIC_GUARD = (f128)1 + pow2_negative(100);

f128 absolute(f128 value) { return value < 0 ? -value : value; }
bool finite_value(f128 value) { return __builtin_isfinite(value); }

f128 gamma_bound(std::uint64_t terms) {
    if (terms == 0) return 0;
    const f128 numerator = (f128)(8 * terms) * UNIT;
    if (!(numerator < 1)) throw std::runtime_error("gamma bound overflow");
    return numerator / ((f128)1 - numerator) * ARITHMETIC_GUARD;
}

f128 upper_sum(f128 left, f128 right) {
    const f128 rounded = left + right;
    const f128 error = gamma_bound(1)
        * (absolute(left) + absolute(right)) * ARITHMETIC_GUARD;
    return rounded + error;
}

f128 lower_difference(f128 left, f128 right) {
    const f128 rounded = left - right;
    const f128 error = gamma_bound(1)
        * (absolute(left) + absolute(right)) * ARITHMETIC_GUARD;
    return rounded - error;
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

template <class T>
void write_vector(const std::string& filename, const std::vector<T>& values) {
    std::ofstream output(filename, std::ios::binary);
    if (!output) throw std::runtime_error("cannot create " + filename);
    output.write(
        reinterpret_cast<const char*>(values.data()),
        (std::streamsize)(values.size() * sizeof(T))
    );
    if (!output) throw std::runtime_error("cannot write " + filename);
}

struct Interval {
    f128 centre;
    f128 radius;
};

Interval interval_add(const Interval& left, const Interval& right) {
    const f128 centre = left.centre + right.centre;
    const f128 gamma = gamma_bound(1);
    const f128 radius = (
        left.radius + right.radius
        + gamma * (absolute(left.centre) + absolute(right.centre))
    ) / ((f128)1 - gamma) * ARITHMETIC_GUARD;
    return {centre, radius};
}

Interval interval_multiply(const Interval& left, const Interval& right) {
    const f128 centre = left.centre * right.centre;
    const f128 uncertainty =
        (absolute(left.centre) + left.radius) * right.radius
        + left.radius * absolute(right.centre);
    const f128 gamma = gamma_bound(1);
    const f128 radius = (
        uncertainty + gamma * absolute(centre)
    ) / ((f128)1 - gamma) * ARITHMETIC_GUARD;
    return {centre, radius};
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

struct RateData {
    std::vector<std::int64_t> indptr;
    std::vector<std::uint8_t> beta;
    std::vector<std::int64_t> numerator;
    std::vector<std::int64_t> denominator;
    std::vector<std::int32_t> source_by_target;
};

RateData load_rates(const std::string& directory) {
    return {
        read_vector<std::int64_t>(directory + "/rate.indptr.i64"),
        read_vector<std::uint8_t>(directory + "/rate.beta.u8"),
        read_vector<std::int64_t>(directory + "/rate.numerator.i64"),
        read_vector<std::int64_t>(directory + "/rate.denominator.i64"),
        read_vector<std::int32_t>(directory + "/beta-source-by-target.i32"),
    };
}

std::vector<Interval> rate_coefficients(const RateData& data) {
    if (
        data.beta.size() != data.numerator.size()
        || data.beta.size() != data.denominator.size()
    ) throw std::runtime_error("rate coefficient arrays disagree");
    std::vector<Interval> output(data.beta.size());
    for (std::size_t index = 0; index < output.size(); ++index) {
        if (data.denominator[index] <= 0 || data.beta[index] >= BETA_COUNT) {
            throw std::runtime_error("invalid exact heat-rate coefficient");
        }
        const f128 centre =
            (f128)data.numerator[index] / (f128)data.denominator[index];
        const f128 gamma = gamma_bound(1);
        const f128 radius = gamma * absolute(centre)
            / ((f128)1 - gamma) * ARITHMETIC_GUARD;
        output[index] = {centre, radius};
    }
    return output;
}

void multiply_rate(
    int rate,
    const RateData& data,
    const std::vector<Interval>& coefficients,
    const f128* input_centre,
    const f128* input_radius,
    std::vector<f128>& output_centre,
    std::vector<f128>& output_radius
) {
    output_centre.assign(CHANNELS, 0);
    output_radius.assign(CHANNELS, 0);
    const auto begin = data.indptr[rate];
    const auto end = data.indptr[rate + 1];
    #pragma omp parallel for schedule(static)
    for (int target = 0; target < CHANNELS; ++target) {
        f128 sum = 0;
        f128 absolute_sum = 0;
        f128 radius_sum = 0;
        std::uint64_t contributions = 0;
        for (auto position = begin; position < end; ++position) {
            const int beta = data.beta[position];
            const int source = data.source_by_target[
                (std::size_t)beta * CHANNELS + target
            ];
            if (source < 0) continue;
            const Interval product = interval_multiply(
                coefficients[position],
                {input_centre[source], input_radius[source]}
            );
            sum += product.centre;
            absolute_sum += absolute(product.centre);
            radius_sum += product.radius;
            ++contributions;
        }
        const f128 gamma = gamma_bound(contributions);
        output_centre[target] = sum;
        output_radius[target] = (
            radius_sum + gamma * absolute_sum
        ) / ((f128)1 - gamma) * ARITHMETIC_GUARD;
    }
}

std::vector<Interval> load_time_weights(const std::string& directory) {
    const auto parts = read_vector<double>(
        directory + "/time-weights-hi-lo-radius.f64"
    );
    if (parts.size() != ORDERS * 3) {
        throw std::runtime_error("invalid time-weight bundle");
    }
    std::vector<Interval> output(ORDERS);
    for (int order = 0; order < ORDERS; ++order) {
        const f128 high = (f128)parts[3 * order];
        const f128 low = (f128)parts[3 * order + 1];
        const f128 centre = high + low;
        const f128 radius = (
            (f128)parts[3 * order + 2]
            + gamma_bound(1) * (absolute(high) + absolute(low))
        ) * ARITHMETIC_GUARD;
        output[order] = {
            order % 2 ? -centre : centre,
            radius,
        };
    }
    return output;
}

Interval pair_prefix(
    int channels,
    const std::vector<f128>& coefficient_centre,
    const std::vector<f128>& coefficient_radius,
    const std::vector<f128>& moment_centre,
    const std::vector<f128>& moment_radius
) {
    f128 sum = 0;
    f128 absolute_sum = 0;
    f128 radius_sum = 0;
    for (int channel = 0; channel < channels; ++channel) {
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
    const f128 gamma = gamma_bound(channels);
    return {
        sum,
        (radius_sum + gamma * absolute_sum)
            / ((f128)1 - gamma) * ARITHMETIC_GUARD,
    };
}

f128 maximum_value(const std::vector<f128>& values) {
    return *std::max_element(values.begin(), values.end());
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 8) {
        std::cerr << "usage: engine HEAT_DATA MOMENT_OUTPUT OUTPUT SOURCE_COMMIT HEAT_MANIFEST CENTRED_CENTRE_SHA256 CENTRED_RADIUS_SHA256\n";
        return 2;
    }
    if (std::fegetround() != FE_TONEAREST) {
        throw std::runtime_error("the certificate requires round-to-nearest");
    }
    const std::string data_directory = argv[1];
    const std::string moment_directory = argv[2];
    const std::string output_directory = argv[3];
    const std::string source_commit = argv[4];
    const std::string heat_manifest = argv[5];
    const std::string moment_centre_hash = argv[6];
    const std::string moment_radius_hash = argv[7];
    const double started = omp_get_wtime();

    std::cerr << "[R0.68B-2g heat] loading exact-rate bundle\n";
    const auto rates = load_rates(data_directory);
    if (
        rates.indptr.size() != RATE_COUNT + 1
        || rates.source_by_target.size()
            != (std::size_t)BETA_COUNT * CHANNELS
    ) throw std::runtime_error("invalid heat-rate bundle dimensions");
    const auto exact_coefficients = rate_coefficients(rates);
    if (
        rates.indptr.front() != 0
        || rates.indptr.back() != (std::int64_t)rates.beta.size()
    ) throw std::runtime_error("invalid heat-rate indptr endpoints");
    for (int rate = 0; rate < RATE_COUNT; ++rate) {
        if (rates.indptr[rate] > rates.indptr[rate + 1]) {
            throw std::runtime_error("nonmonotone heat-rate indptr");
        }
    }
    for (const auto source : rates.source_by_target) {
        if (source < -1 || source >= CHANNELS) {
            throw std::runtime_error("invalid polynomial source map");
        }
    }
    const auto weights = load_time_weights(data_directory);
    for (const auto& weight : weights) {
        if (
            !finite_value(weight.centre)
            || !finite_value(weight.radius)
            || weight.radius < 0
        ) throw std::runtime_error("invalid time-weight interval");
    }
    const auto tail_values = read_vector<double>(
        data_directory + "/coefficient-tail-upper.f64"
    );
    if (tail_values.size() != 1 || !(tail_values[0] > 0)) {
        throw std::runtime_error("invalid coefficient-tail bound");
    }
    const f128 coefficient_tail =
        (f128)tail_values[0] * ARITHMETIC_GUARD;

    std::vector<f128> coefficient_centre(CHANNELS, 0);
    std::vector<f128> coefficient_radius(CHANNELS, 0);
    std::vector<f128> homogeneous_centre((std::size_t)ORDERS * CHANNELS);
    std::vector<f128> homogeneous_radius((std::size_t)ORDERS * CHANNELS);
    std::vector<f128> product_centre;
    std::vector<f128> product_radius;

    for (int shuffle = 0; shuffle < SHUFFLES; ++shuffle) {
        std::fill(homogeneous_centre.begin(), homogeneous_centre.end(), 0);
        std::fill(homogeneous_radius.begin(), homogeneous_radius.end(), 0);
        homogeneous_centre[0] = 1;
        for (int local_rate = 0; local_rate < RATES_PER_SHUFFLE; ++local_rate) {
            const int rate = shuffle * RATES_PER_SHUFFLE + local_rate;
            for (int order = 1; order < ORDERS; ++order) {
                const std::size_t previous = (std::size_t)(order - 1) * CHANNELS;
                const std::size_t current = (std::size_t)order * CHANNELS;
                multiply_rate(
                    rate,
                    rates,
                    exact_coefficients,
                    homogeneous_centre.data() + previous,
                    homogeneous_radius.data() + previous,
                    product_centre,
                    product_radius
                );
                #pragma omp parallel for schedule(static)
                for (int channel = 0; channel < CHANNELS; ++channel) {
                    const Interval updated = interval_add(
                        {
                            homogeneous_centre[current + channel],
                            homogeneous_radius[current + channel],
                        },
                        {product_centre[channel], product_radius[channel]}
                    );
                    homogeneous_centre[current + channel] = updated.centre;
                    homogeneous_radius[current + channel] = updated.radius;
                }
            }
        }
        for (int order = 0; order < ORDERS; ++order) {
            const std::size_t offset = (std::size_t)order * CHANNELS;
            #pragma omp parallel for schedule(static)
            for (int channel = 0; channel < CHANNELS; ++channel) {
                const Interval contribution = interval_multiply(
                    weights[order],
                    {
                        homogeneous_centre[offset + channel],
                        homogeneous_radius[offset + channel],
                    }
                );
                const Interval updated = interval_add(
                    {coefficient_centre[channel], coefficient_radius[channel]},
                    contribution
                );
                coefficient_centre[channel] = updated.centre;
                coefficient_radius[channel] = updated.radius;
            }
        }
        std::cerr
            << "[R0.68B-2g heat +" << std::fixed << std::setprecision(2)
            << omp_get_wtime() - started << "s] shuffle=" << shuffle + 1
            << "/" << SHUFFLES << "\n";
    }

    #pragma omp parallel for schedule(static)
    for (int channel = 0; channel < CHANNELS; ++channel) {
        coefficient_radius[channel] =
            (coefficient_radius[channel] + coefficient_tail)
            * ARITHMETIC_GUARD;
    }
    validate_intervals(
        coefficient_centre,
        coefficient_radius,
        "heat coefficients"
    );

    std::cerr
        << "[R0.68B-2g heat +" << std::fixed << std::setprecision(2)
        << omp_get_wtime() - started << "s] pairing certified moments\n";
    const auto moment_centre = read_vector<f128>(
        moment_directory + "/centred-centre.f128"
    );
    const auto moment_radius = read_vector<f128>(
        moment_directory + "/centred-radius.f128"
    );
    if (
        moment_centre.size() != (std::size_t)CHANNELS * STATES
        || moment_radius.size() != moment_centre.size()
    ) throw std::runtime_error("invalid centred-moment arrays");
    validate_intervals(moment_centre, moment_radius, "centred moments");

    std::array<Interval, 11> partial;
    for (int degree = 0; degree <= 10; ++degree) {
        partial[degree] = pair_prefix(
            CHANNELS_BY_DEGREE[degree],
            coefficient_centre,
            coefficient_radius,
            moment_centre,
            moment_radius
        );
    }
    const Interval final = partial.back();
    const f128 certified_final_upper = upper_sum(final.centre, final.radius);
    if (!(certified_final_upper < 0)) {
        throw std::runtime_error("degree-ten heat-jet interval does not have strict negative sign");
    }

    write_vector(
        output_directory + "/heat-coefficient-centre.f128",
        coefficient_centre
    );
    write_vector(
        output_directory + "/heat-coefficient-radius.f128",
        coefficient_radius
    );

    std::ofstream summary(output_directory + "/summary.json");
    if (!summary) throw std::runtime_error("cannot create summary");
    summary << "{\n";
    summary << "  \"schemaVersion\": \"1.0\",\n";
    summary << "  \"status\": \"strict-passed\",\n";
    summary << "  \"classification\": \"guarded degree-ten dominant heat-jet sign; signature defect remains open\",\n";
    summary << "  \"checks\": {\"roundingModeIsNearest\": true, \"allCoefficientIntervalsValid\": true, \"allMomentIntervalsValid\": true, \"degreeTenHeatJetIsStrictlyNegative\": true},\n";
    summary << "  \"provenance\": {\"sourceCommit\": \"" << source_commit
            << "\", \"heatPayloadManifestSha256\": \"" << heat_manifest
            << "\", \"centredMomentCentreSha256\": \""
            << moment_centre_hash << "\", \"centredMomentRadiusSha256\": \""
            << moment_radius_hash << "\"},\n";
    summary << "  \"parameters\": {\"maximumDegree\": 10, \"channels\": 8008, \"states\": 1792, \"shuffleCount\": 35, \"seriesOrder\": 64},\n";
    summary << "  \"uniformCoefficientTailUpper\": " << std::scientific
            << std::setprecision(17) << as_double_upper(coefficient_tail) << ",\n";
    summary << "  \"maximumCoefficientRadius\": "
            << as_double_upper(maximum_value(coefficient_radius)) << ",\n";
    summary << "  \"partialByDegree\": [\n";
    for (int degree = 0; degree <= 10; ++degree) {
        const f128 lower = lower_difference(
            partial[degree].centre,
            partial[degree].radius
        );
        const f128 upper = upper_sum(
            partial[degree].centre,
            partial[degree].radius
        );
        summary << "    {\"degree\": " << degree
                << ", \"centre\": " << as_double(partial[degree].centre)
                << ", \"radius\": " << as_double_upper(partial[degree].radius)
                << ", \"lower\": " << as_double_lower(lower)
                << ", \"upper\": " << as_double_upper(upper) << "}";
        if (degree != 10) summary << ",";
        summary << "\n";
    }
    const f128 final_lower = lower_difference(final.centre, final.radius);
    const f128 final_upper = certified_final_upper;
    summary << "  ],\n";
    summary << "  \"degreeTenHeatJet\": {\"centre\": "
            << as_double(final.centre) << ", \"radius\": "
            << as_double_upper(final.radius) << ", \"lower\": "
            << as_double_lower(final_lower) << ", \"upper\": "
            << as_double_upper(final_upper) << "},\n";
    summary << "  \"elapsedSeconds\": " << std::fixed << std::setprecision(3)
            << omp_get_wtime() - started << ",\n";
    summary << "  \"limitations\": [\"the signature-compressed defect is not enclosed\", \"the final dominant heat sign is not claimed\", \"no Navier-Stokes regularity claim\"]\n";
    summary << "}\n";
    std::cerr
        << "[R0.68B-2g heat +" << std::fixed << std::setprecision(2)
        << omp_get_wtime() - started << "s] complete interval=["
        << std::scientific << as_double_lower(final_lower) << ","
        << as_double_upper(final_upper) << "]\n";
    return 0;
}
