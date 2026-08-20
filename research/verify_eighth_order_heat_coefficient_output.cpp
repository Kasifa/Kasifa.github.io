// Independent streaming verifier for R0.68B-2g heat coefficients and pairing.

#include <algorithm>
#include <cfloat>
#include <cmath>
#include <cstdint>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

using f128 = _Float128;

static_assert(sizeof(f128) == 16, "expected 16-byte binary128");
static_assert(FLT_RADIX == 2, "expected radix two");
static_assert(__FLT128_MANT_DIG__ == 113, "unexpected binary128 precision");

namespace {

constexpr int CHANNELS = 8008;
constexpr int STATES = 1792;
constexpr int OBSERVABLE_STATE = 3;

f128 pow2_negative(int exponent) {
    f128 value = 1;
    for (int index = 0; index < exponent; ++index) value *= (f128)0.5;
    return value;
}

const f128 UNIT = pow2_negative(113);
const f128 GUARD = (f128)1 + pow2_negative(100);

f128 absolute(f128 value) { return value < 0 ? -value : value; }

f128 gamma_bound(std::uint64_t terms) {
    const f128 numerator = (f128)(8 * terms) * UNIT;
    if (!(numerator < 1)) throw std::runtime_error("gamma overflow");
    return numerator / ((f128)1 - numerator) * GUARD;
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

Interval multiply(const Interval& left, const Interval& right) {
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

}  // namespace

int main(int argc, char** argv) {
    if (argc != 3 && argc != 4) {
        std::cerr << "usage: verifier HEAT_OUTPUT MOMENT_OUTPUT [BINARY64_REFERENCE]\n";
        return 2;
    }
    const std::string heat = argv[1];
    const std::string moment = argv[2];
    const auto coefficient_centre = read_vector<f128>(
        heat + "/heat-coefficient-centre.f128"
    );
    const auto coefficient_radius = read_vector<f128>(
        heat + "/heat-coefficient-radius.f128"
    );
    const auto moment_centre = read_vector<f128>(moment + "/centred-centre.f128");
    const auto moment_radius = read_vector<f128>(moment + "/centred-radius.f128");
    if (
        coefficient_centre.size() != CHANNELS
        || coefficient_radius.size() != CHANNELS
        || moment_centre.size() != (std::size_t)CHANNELS * STATES
        || moment_radius.size() != moment_centre.size()
    ) throw std::runtime_error("unexpected array size");

    f128 sum = 0;
    f128 absolute_sum = 0;
    f128 radius_sum = 0;
    f128 maximum_radius = 0;
    for (int channel = 0; channel < CHANNELS; ++channel) {
        if (
            !__builtin_isfinite(coefficient_centre[channel])
            || !__builtin_isfinite(coefficient_radius[channel])
            || coefficient_radius[channel] < 0
        ) throw std::runtime_error("invalid heat coefficient interval");
        maximum_radius = std::max(maximum_radius, coefficient_radius[channel]);
        const std::size_t index =
            (std::size_t)channel * STATES + OBSERVABLE_STATE;
        if (
            !__builtin_isfinite(moment_centre[index])
            || !__builtin_isfinite(moment_radius[index])
            || moment_radius[index] < 0
        ) throw std::runtime_error("invalid observable moment interval");
        const Interval product = multiply(
            {coefficient_centre[channel], coefficient_radius[channel]},
            {moment_centre[index], moment_radius[index]}
        );
        sum += product.centre;
        absolute_sum += absolute(product.centre);
        radius_sum += product.radius;
    }
    const f128 gamma = gamma_bound(CHANNELS);
    const f128 radius = (radius_sum + gamma * absolute_sum)
        / ((f128)1 - gamma) * GUARD;
    const f128 endpoint_error = gamma_bound(1)
        * (absolute(sum) + radius) * GUARD;
    const f128 lower = sum - radius - endpoint_error;
    const f128 upper = sum + radius + endpoint_error;
    if (!(upper < 0)) throw std::runtime_error("verified interval is not negative");

    f128 reference_difference = -1;
    if (argc == 4) {
        const auto reference = read_vector<double>(argv[3]);
        if (reference.size() != CHANNELS) {
            throw std::runtime_error("unexpected binary64 reference size");
        }
        reference_difference = 0;
        for (int channel = 0; channel < CHANNELS; ++channel) {
            reference_difference = std::max(
                reference_difference,
                absolute(coefficient_centre[channel] - (f128)reference[channel])
            );
        }
    }

    std::cout << "{\n"
              << "  \"status\": \"verified\",\n"
              << "  \"coefficientCount\": " << CHANNELS << ",\n"
              << "  \"allCoefficientIntervalsValid\": true,\n"
              << "  \"maximumCoefficientRadiusUpper\": " << std::scientific
              << std::setprecision(17) << as_double_upper(maximum_radius) << ",\n"
              << "  \"pairedCentre\": " << as_double(sum) << ",\n"
              << "  \"pairedRadiusUpper\": " << as_double_upper(radius) << ",\n"
              << "  \"pairedLower\": " << as_double_lower(lower) << ",\n"
              << "  \"pairedUpper\": " << as_double_upper(upper) << ",\n"
              << "  \"strictlyNegative\": true";
    if (argc == 4) {
        std::cout << ",\n  \"binary64ReferenceMaximumDifferenceUpper\": "
                  << as_double_upper(reference_difference);
    }
    std::cout << "\n}\n";
    return 0;
}
