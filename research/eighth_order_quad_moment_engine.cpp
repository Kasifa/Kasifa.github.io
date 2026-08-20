// R0.68B-2f binary128 interval engine for the degree-ten moment lift.
//
// Compile on GCC with:
//   g++ -O3 -std=gnu++20 -fopenmp eighth_order_quad_moment_engine.cpp -o engine
//
// This component encloses moments only. Heat coefficients, the signature
// defect, and the final heat sign remain separate gates.

#include <algorithm>
#include <array>
#include <cfloat>
#include <cfenv>
#include <cmath>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

#include <omp.h>

using f128 = _Float128;

static_assert(sizeof(f128) == 16, "the certificate requires 16-byte binary128");
static_assert(FLT_RADIX == 2, "the certificate requires radix-two arithmetic");
static_assert(__FLT128_MANT_DIG__ == 113, "unexpected _Float128 precision");

namespace {

constexpr int STATES = 1792;
constexpr std::array<int, 11> CHANNELS = {
    1, 7, 28, 84, 210, 462, 924, 1716, 3003, 5005, 8008
};
constexpr std::array<int, 4> LENGTHS = {1, 2, 4, 8};
constexpr std::array<int, 4> WORD = {0, 1, 0, 0};
constexpr int CYCLE_INFINITY_NORM = 123028;
constexpr int NORMAL_INFINITY_NORM = 2024341504;

f128 pow2_negative(int exponent) {
    f128 value = 1;
    for (int index = 0; index < exponent; ++index) value *= (f128)0.5;
    return value;
}

const f128 UNIT = pow2_negative(113);
const f128 ARITHMETIC_GUARD = (f128)1 + pow2_negative(100);
const f128 NORM_GUARD = (f128)1 + pow2_negative(88);

f128 absolute(f128 value) { return value < 0 ? -value : value; }

f128 square_root(f128 value) {
    if (!(value > 0)) return 0;
    f128 estimate = (f128)__builtin_sqrt((double)value);
    for (int index = 0; index < 12; ++index) {
        estimate = ((f128)0.5) * (estimate + value / estimate);
    }
    return estimate * ARITHMETIC_GUARD;
}

f128 gamma_bound(std::uint64_t terms) {
    if (terms == 0) return 0;
    // Eight roundings per fused path contribution are allowed.
    const f128 numerator = (f128)(8 * terms) * UNIT;
    if (!(numerator < 1)) throw std::runtime_error("gamma bound overflow");
    return numerator / ((f128)1 - numerator) * ARITHMETIC_GUARD;
}

f128 lower_difference(f128 left, f128 right) {
    const f128 rounded = left - right;
    const f128 subtraction_error =
        gamma_bound(1) * (absolute(left) + absolute(right))
        * ARITHMETIC_GUARD;
    return rounded - subtraction_error;
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

struct SparseCycle {
    std::vector<std::int64_t> indptr;
    std::vector<std::int32_t> indices;
    std::vector<std::int16_t> data;
};

struct SparseSubset {
    std::vector<std::int64_t> indptr;
    std::vector<std::int32_t> indices;
    std::vector<std::int8_t> data;
};

struct ChannelTerms {
    std::vector<std::int64_t> indptr;
    std::vector<std::int32_t> sources;
    std::vector<std::uint8_t> masks;
    std::vector<std::int64_t> coefficients;
};

struct CenteringTerms {
    std::vector<std::int64_t> indptr;
    std::vector<std::int32_t> sources;
    std::vector<std::int32_t> numerators;
    std::vector<std::uint8_t> exponents;
};

SparseCycle load_cycle(const std::string& directory) {
    return {
        read_vector<std::int64_t>(directory + "/cycle.indptr.i64"),
        read_vector<std::int32_t>(directory + "/cycle.indices.i32"),
        read_vector<std::int16_t>(directory + "/cycle.data"),
    };
}

SparseSubset load_subset(
    const std::string& directory,
    int bit,
    int mask
) {
    char stem[128];
    std::snprintf(stem, sizeof(stem), "/subset-b%d-m%02d", bit, mask);
    return {
        read_vector<std::int64_t>(directory + stem + ".indptr.i64"),
        read_vector<std::int32_t>(directory + stem + ".indices.i32"),
        read_vector<std::int8_t>(directory + stem + ".data"),
    };
}

ChannelTerms load_channels(const std::string& directory, int length) {
    const std::string stem = directory + "/channel-l" + std::to_string(length);
    return {
        read_vector<std::int64_t>(stem + ".indptr.i64"),
        read_vector<std::int32_t>(stem + ".sources.i32"),
        read_vector<std::uint8_t>(stem + ".masks.u8"),
        read_vector<std::int64_t>(stem + ".coefficients.i64"),
    };
}

CenteringTerms load_centering(const std::string& directory) {
    return {
        read_vector<std::int64_t>(directory + "/centering.indptr.i64"),
        read_vector<std::int32_t>(directory + "/centering.sources.i32"),
        read_vector<std::int32_t>(directory + "/centering.numerators.i32"),
        read_vector<std::uint8_t>(directory + "/centering.exponents.u8"),
    };
}

double as_double(f128 value) { return (double)value; }

double as_double_upper(f128 value) {
    double output = (double)value;
    if ((f128)output < value) output = std::nextafter(output, INFINITY);
    return output;
}

bool finite_value(f128 value) { return __builtin_isfinite(value); }

void validate_interval_vectors(
    const std::vector<f128>& centres,
    const std::vector<f128>& radii,
    const std::string& label
) {
    if (centres.size() != radii.size()) {
        throw std::runtime_error(label + " interval shape mismatch");
    }
    for (std::size_t index = 0; index < centres.size(); ++index) {
        if (!finite_value(centres[index])) {
            throw std::runtime_error(label + " has a non-finite centre");
        }
        if (!finite_value(radii[index]) || radii[index] < 0) {
            throw std::runtime_error(label + " has an invalid radius");
        }
    }
}

f128 maximum_absolute(const std::vector<f128>& values) {
    f128 output = 0;
    #pragma omp parallel
    {
        f128 local = 0;
        #pragma omp for nowait
        for (std::size_t index = 0; index < values.size(); ++index) {
            local = std::max(local, absolute(values[index]));
        }
        #pragma omp critical
        output = std::max(output, local);
    }
    return output;
}

f128 maximum_value(const std::vector<f128>& values) {
    f128 output = 0;
    #pragma omp parallel
    {
        f128 local = 0;
        #pragma omp for nowait
        for (std::size_t index = 0; index < values.size(); ++index) {
            local = std::max(local, values[index]);
        }
        #pragma omp critical
        output = std::max(output, local);
    }
    return output;
}

void digit_step(
    int channels,
    const ChannelTerms& terms,
    const std::array<SparseSubset, 64>& subsets,
    const std::vector<f128>& input_centre,
    const std::vector<f128>& input_radius,
    std::vector<f128>& output_centre,
    std::vector<f128>& output_radius
) {
    const std::size_t size = (std::size_t)channels * STATES;
    output_centre.assign(size, 0);
    output_radius.assign(size, 0);
    #pragma omp parallel for schedule(dynamic, 1)
    for (int target = 0; target < channels; ++target) {
        const auto term_begin = terms.indptr[target];
        const auto term_end = terms.indptr[target + 1];
        for (int row = 0; row < STATES; ++row) {
            f128 sum = 0;
            f128 absolute_sum = 0;
            f128 radius_sum = 0;
            std::uint64_t contributions = 0;
            for (auto record = term_begin; record < term_end; ++record) {
                const int source = terms.sources[record];
                const int mask = terms.masks[record];
                const std::int64_t coefficient = terms.coefficients[record];
                const auto& matrix = subsets[mask];
                for (
                    auto position = matrix.indptr[row];
                    position < matrix.indptr[row + 1];
                    ++position
                ) {
                    const int column = matrix.indices[position];
                    const std::int64_t weight =
                        coefficient * (std::int64_t)matrix.data[position];
                    const std::size_t source_index =
                        (std::size_t)source * STATES + column;
                    const f128 product =
                        (f128)weight * input_centre[source_index];
                    sum += product;
                    absolute_sum += absolute(product);
                    radius_sum +=
                        (f128)std::llabs(weight) * input_radius[source_index];
                    ++contributions;
                }
            }
            const f128 gamma = gamma_bound(contributions);
            const std::size_t output_index =
                (std::size_t)target * STATES + row;
            output_centre[output_index] = sum;
            output_radius[output_index] =
                ((radius_sum + gamma * absolute_sum) / ((f128)1 - gamma))
                * ARITHMETIC_GUARD;
        }
    }
}

void cycle_product(
    int channels,
    const SparseCycle& matrix,
    const std::vector<f128>& input_centre,
    const std::vector<f128>& input_radius,
    std::vector<f128>& output_centre,
    std::vector<f128>& output_radius
) {
    const std::size_t size = (std::size_t)channels * STATES;
    output_centre.assign(size, 0);
    output_radius.assign(size, 0);
    #pragma omp parallel for schedule(static)
    for (int channel = 0; channel < channels; ++channel) {
        for (int row = 0; row < STATES; ++row) {
            f128 sum = 0;
            f128 absolute_sum = 0;
            f128 radius_sum = 0;
            const auto begin = matrix.indptr[row];
            const auto end = matrix.indptr[row + 1];
            for (auto position = begin; position < end; ++position) {
                const int column = matrix.indices[position];
                const std::int64_t weight = matrix.data[position];
                const std::size_t input_index =
                    (std::size_t)channel * STATES + column;
                const f128 product = (f128)weight * input_centre[input_index];
                sum += product;
                absolute_sum += absolute(product);
                radius_sum +=
                    (f128)std::llabs(weight) * input_radius[input_index];
            }
            const f128 gamma = gamma_bound((std::uint64_t)(end - begin));
            const std::size_t output_index =
                (std::size_t)channel * STATES + row;
            output_centre[output_index] = sum;
            output_radius[output_index] =
                ((radius_sum + gamma * absolute_sum) / ((f128)1 - gamma))
                * ARITHMETIC_GUARD;
        }
    }
}

void neumann_solve(
    int channels,
    const SparseCycle& matrix,
    f128 scalar,
    const std::vector<f128>& right_hand_side,
    std::vector<f128>& solution,
    int& terms_used
) {
    const std::size_t size = (std::size_t)channels * STATES;
    std::vector<f128> term(size);
    solution.resize(size);
    #pragma omp parallel for schedule(static)
    for (std::size_t index = 0; index < size; ++index) {
        term[index] = right_hand_side[index] / scalar;
        solution[index] = term[index];
    }
    std::vector<f128> next;
    std::vector<f128> ignored_radius;
    const std::vector<f128> zero_radius(size, 0);
    terms_used = 1;
    for (; terms_used < 80; ++terms_used) {
        cycle_product(
            channels,
            matrix,
            term,
            zero_radius,
            next,
            ignored_radius
        );
        #pragma omp parallel for schedule(static)
        for (std::size_t index = 0; index < size; ++index) {
            next[index] /= scalar;
            solution[index] += next[index];
        }
        term.swap(next);
        if (maximum_absolute(term) < pow2_negative(108)) {
            ++terms_used;
            break;
        }
    }
}

std::vector<f128> residual_solution_radii(
    int degree,
    int channels,
    const SparseCycle& matrix,
    f128 scalar,
    f128 scalar_radius,
    f128 scalar_lower,
    const std::vector<f128>& right_centre,
    const std::vector<f128>& right_radius,
    const std::vector<f128>& solution
) {
    const std::size_t size = (std::size_t)channels * STATES;
    std::vector<f128> cycle_centre;
    std::vector<f128> cycle_radius;
    const std::vector<f128> zero_radius(size, 0);
    cycle_product(
        channels,
        matrix,
        solution,
        zero_radius,
        cycle_centre,
        cycle_radius
    );
    std::vector<f128> absolute_residual(size);
    #pragma omp parallel for schedule(static)
    for (std::size_t index = 0; index < size; ++index) {
        const f128 scalar_product = scalar * solution[index];
        const f128 centre =
            right_centre[index] - scalar_product + cycle_centre[index];
        const f128 absolute_addends =
            absolute(right_centre[index])
            + absolute(scalar_product)
            + absolute(cycle_centre[index]);
        const f128 gamma = gamma_bound(3);
        const f128 scalar_error =
            (
                gamma_bound(1) * absolute(scalar_product)
                + scalar_radius * absolute(solution[index])
            ) * ARITHMETIC_GUARD;
        const f128 radius =
            (
                right_radius[index]
                + scalar_error
                + cycle_radius[index]
                + gamma * absolute_addends
            ) * ARITHMETIC_GUARD;
        absolute_residual[index] =
            (absolute(centre) + radius) * ARITHMETIC_GUARD;
    }

    std::vector<f128> radii(channels);
    if (degree == 1) {
        const f128 norm_bound = square_root((f128)NORMAL_INFINITY_NORM);
        const f128 denominator = lower_difference(scalar_lower, norm_bound);
        if (!(denominator > 0)) {
            throw std::runtime_error("degree-one denominator is nonpositive");
        }
        #pragma omp parallel for schedule(static)
        for (int channel = 0; channel < channels; ++channel) {
            f128 sum = 0;
            for (int state = 0; state < STATES; ++state) {
                const f128 value =
                    absolute_residual[(std::size_t)channel * STATES + state];
                sum += value * value;
            }
            sum = (sum / ((f128)1 - gamma_bound(STATES)))
                * ARITHMETIC_GUARD;
            radii[channel] =
                square_root(sum) / denominator * NORM_GUARD;
        }
    } else {
        const f128 denominator = lower_difference(
            scalar_lower,
            (f128)CYCLE_INFINITY_NORM
        );
        if (!(denominator > 0)) {
            throw std::runtime_error("infinity denominator is nonpositive");
        }
        #pragma omp parallel for schedule(static)
        for (int channel = 0; channel < channels; ++channel) {
            f128 maximum = 0;
            for (int state = 0; state < STATES; ++state) {
                maximum = std::max(
                    maximum,
                    absolute_residual[(std::size_t)channel * STATES + state]
                );
            }
            radii[channel] = maximum / denominator * NORM_GUARD;
        }
    }
    return radii;
}

void centre_moments(
    int channels,
    const CenteringTerms& terms,
    const std::vector<f128>& input_centre,
    const std::vector<f128>& input_radius,
    std::vector<f128>& output_centre,
    std::vector<f128>& output_radius
) {
    const std::size_t size = (std::size_t)channels * STATES;
    output_centre.assign(size, 0);
    output_radius.assign(size, 0);
    #pragma omp parallel for schedule(dynamic, 1)
    for (int target = 0; target < channels; ++target) {
        const auto begin = terms.indptr[target];
        const auto end = terms.indptr[target + 1];
        const f128 gamma = gamma_bound((std::uint64_t)(end - begin));
        for (int state = 0; state < STATES; ++state) {
            f128 sum = 0;
            f128 absolute_sum = 0;
            f128 radius_sum = 0;
            for (auto record = begin; record < end; ++record) {
                const int source = terms.sources[record];
                f128 coefficient = (f128)terms.numerators[record];
                for (
                    int exponent = 0;
                    exponent < terms.exponents[record];
                    ++exponent
                ) coefficient *= (f128)0.5;
                const std::size_t input_index =
                    (std::size_t)source * STATES + state;
                const f128 product =
                    coefficient * input_centre[input_index];
                sum += product;
                absolute_sum += absolute(product);
                radius_sum +=
                    absolute(coefficient) * input_radius[input_index];
            }
            const std::size_t output_index =
                (std::size_t)target * STATES + state;
            output_centre[output_index] = sum;
            output_radius[output_index] =
                ((radius_sum + gamma * absolute_sum) / ((f128)1 - gamma))
                * ARITHMETIC_GUARD;
        }
    }
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 4 && argc != 6) {
        std::cerr << "usage: engine DATA_DIRECTORY OUTPUT_DIRECTORY MAX_DEGREE [SOURCE_COMMIT PAYLOAD_MANIFEST_SHA256]\n";
        return 2;
    }
    const std::string data_directory = argv[1];
    const std::string output_directory = argv[2];
    const int maximum_degree = std::stoi(argv[3]);
    const std::string source_commit = argc == 6 ? argv[4] : "uncommitted";
    const std::string payload_manifest_sha256 =
        argc == 6 ? argv[5] : "unrecorded";
    if (maximum_degree < 0 || maximum_degree > 10) {
        throw std::runtime_error("maximum degree must lie in [0,10]");
    }
    if (std::fegetround() != FE_TONEAREST) {
        throw std::runtime_error("the certificate requires round-to-nearest");
    }
    const double started = omp_get_wtime();
    std::cerr << "[R0.68B-2f quad] loading sparse bundle\n";
    const auto matrix = load_cycle(data_directory);
    std::array<std::array<SparseSubset, 64>, 2> subsets;
    for (int bit = 0; bit < 2; ++bit) {
        for (int mask = 0; mask < 64; ++mask) {
            subsets[bit][mask] = load_subset(data_directory, bit, mask);
        }
    }
    std::array<ChannelTerms, 4> channel_terms;
    for (int index = 0; index < 4; ++index) {
        channel_terms[index] = load_channels(data_directory, LENGTHS[index]);
    }
    const auto centering = load_centering(data_directory);
    const auto root_parts =
        read_vector<double>(data_directory + "/root-hi-lo-radius.f64");
    const auto mass_parts =
        read_vector<double>(data_directory + "/mass-hi-lo-radius.f64");
    if (root_parts.size() != 3 || mass_parts.size() != STATES * 3) {
        throw std::runtime_error("invalid root or mass bundle");
    }
    const f128 root_high = (f128)root_parts[0];
    const f128 root_low = (f128)root_parts[1];
    const f128 root = root_high + root_low;
    const f128 root_radius =
        (
            (f128)root_parts[2]
            + gamma_bound(1) * (absolute(root_high) + absolute(root_low))
        ) * ARITHMETIC_GUARD;

    std::vector<f128> old_centre(STATES);
    std::vector<f128> old_radius(STATES);
    for (int state = 0; state < STATES; ++state) {
        const f128 high = (f128)mass_parts[3 * state];
        const f128 low = (f128)mass_parts[3 * state + 1];
        old_centre[state] = high + low;
        old_radius[state] =
            (
                (f128)mass_parts[3 * state + 2]
                + gamma_bound(1) * (absolute(high) + absolute(low))
            ) * ARITHMETIC_GUARD;
    }
    validate_interval_vectors(old_centre, old_radius, "degree zero");

    struct DegreeRecord {
        int degree;
        int channels;
        int homogeneous;
        int neumann_terms;
        double maximum_centre;
        double maximum_radius;
        double elapsed;
    };
    std::vector<DegreeRecord> records;
    records.push_back({
        0, 1, 1, 0,
        as_double(maximum_absolute(old_centre)),
        as_double_upper(maximum_value(old_radius)),
        omp_get_wtime() - started,
    });
    std::cerr
        << "[R0.68B-2f quad +" << std::fixed << std::setprecision(2)
        << omp_get_wtime() - started
        << "s] degree=0 channels=1 max_radius="
        << std::scientific << records.back().maximum_radius << "\n";

    for (int degree = 1; degree <= maximum_degree; ++degree) {
        const int channels = CHANNELS[degree];
        const int old_channels = CHANNELS[degree - 1];
        const int homogeneous = channels - old_channels;
        std::vector<f128> centres((std::size_t)channels * STATES, 0);
        std::vector<f128> radii((std::size_t)channels * STATES, 0);
        std::copy(old_centre.begin(), old_centre.end(), centres.begin());
        std::copy(old_radius.begin(), old_radius.end(), radii.begin());
        std::vector<f128> next_centre;
        std::vector<f128> next_radius;
        for (int digit = 0; digit < 4; ++digit) {
            digit_step(
                channels,
                channel_terms[digit],
                subsets[WORD[digit]],
                centres,
                radii,
                next_centre,
                next_radius
            );
            centres.swap(next_centre);
            radii.swap(next_radius);
            std::cerr
                << "[R0.68B-2f quad +" << std::fixed << std::setprecision(2)
                << omp_get_wtime() - started
                << "s] degree=" << degree
                << " digit=" << digit + 1 << "/4"
                << " max_radius=" << std::scientific
                << as_double(maximum_value(radii)) << "\n";
        }

        std::vector<f128> right_centre((std::size_t)homogeneous * STATES);
        std::vector<f128> right_radius((std::size_t)homogeneous * STATES);
        const std::size_t offset = (std::size_t)old_channels * STATES;
        std::copy(
            centres.begin() + offset,
            centres.end(),
            right_centre.begin()
        );
        std::copy(
            radii.begin() + offset,
            radii.end(),
            right_radius.begin()
        );
        f128 power = 1;
        for (int index = 0; index < degree; ++index) power *= (f128)16;
        const f128 scalar = power * root;
        const f128 scalar_radius =
            (
                power * root_radius
                + gamma_bound(1) * absolute(scalar)
            ) * ARITHMETIC_GUARD;
        const f128 scalar_lower = lower_difference(scalar, scalar_radius);
        std::vector<f128> solution;
        int neumann_terms = 0;
        neumann_solve(
            homogeneous,
            matrix,
            scalar,
            right_centre,
            solution,
            neumann_terms
        );
        const auto channel_radii = residual_solution_radii(
            degree,
            homogeneous,
            matrix,
            scalar,
            scalar_radius,
            scalar_lower,
            right_centre,
            right_radius,
            solution
        );

        std::vector<f128> combined_centre((std::size_t)channels * STATES);
        std::vector<f128> combined_radius((std::size_t)channels * STATES);
        std::copy(old_centre.begin(), old_centre.end(), combined_centre.begin());
        std::copy(old_radius.begin(), old_radius.end(), combined_radius.begin());
        #pragma omp parallel for schedule(static)
        for (int channel = 0; channel < homogeneous; ++channel) {
            for (int state = 0; state < STATES; ++state) {
                const std::size_t target =
                    (std::size_t)(old_channels + channel) * STATES + state;
                const std::size_t source =
                    (std::size_t)channel * STATES + state;
                combined_centre[target] = solution[source];
                combined_radius[target] = channel_radii[channel];
            }
        }
        old_centre.swap(combined_centre);
        old_radius.swap(combined_radius);
        validate_interval_vectors(
            old_centre,
            old_radius,
            "degree " + std::to_string(degree)
        );
        records.push_back({
            degree,
            channels,
            homogeneous,
            neumann_terms,
            as_double(maximum_absolute(solution)),
            as_double_upper(maximum_value(channel_radii)),
            omp_get_wtime() - started,
        });
        std::cerr
            << "[R0.68B-2f quad +" << std::fixed << std::setprecision(2)
            << omp_get_wtime() - started
            << "s] degree=" << degree
            << " enclosed channels=" << channels
            << " neumann=" << neumann_terms
            << " max_radius=" << std::scientific
            << records.back().maximum_radius << "\n";
    }

    std::cerr
        << "[R0.68B-2f quad +" << std::fixed << std::setprecision(2)
        << omp_get_wtime() - started << "s] centering moments\n";
    std::vector<f128> centred_centre;
    std::vector<f128> centred_radius;
    centre_moments(
        CHANNELS[maximum_degree],
        centering,
        old_centre,
        old_radius,
        centred_centre,
        centred_radius
    );
    validate_interval_vectors(old_centre, old_radius, "raw moments");
    validate_interval_vectors(
        centred_centre,
        centred_radius,
        "centred moments"
    );

    write_vector(output_directory + "/raw-centre.f128", old_centre);
    write_vector(output_directory + "/raw-radius.f128", old_radius);
    write_vector(output_directory + "/centred-centre.f128", centred_centre);
    write_vector(output_directory + "/centred-radius.f128", centred_radius);

    std::ofstream summary(output_directory + "/summary.json");
    summary << "{\n";
    summary << "  \"schemaVersion\": \"1.0\",\n";
    summary << "  \"status\": \"certified-passed\",\n";
    summary << "  \"classification\": \"guarded IEEE binary128 round-to-nearest enclosure of the complete moment lift; heat and defect remain open\",\n";
    summary << "  \"checks\": {\"roundingModeIsNearest\": true, \"allCentresFinite\": true, \"allRadiiFiniteAndNonnegative\": true},\n";
    summary << "  \"provenance\": {\"sourceCommit\": \"" << source_commit
            << "\", \"payloadManifestSha256\": \""
            << payload_manifest_sha256 << "\"},\n";
    summary << "  \"maximumDegree\": " << maximum_degree << ",\n";
    summary << "  \"channelsPerState\": " << CHANNELS[maximum_degree] << ",\n";
    summary << "  \"stateDimension\": " << STATES << ",\n";
    summary << "  \"totalCoordinates\": "
            << (std::uint64_t)CHANNELS[maximum_degree] * STATES << ",\n";
    summary << "  \"cycleInfinityNorm\": " << CYCLE_INFINITY_NORM << ",\n";
    summary << "  \"normalInfinityNorm\": " << NORMAL_INFINITY_NORM << ",\n";
    summary << "  \"degrees\": [\n";
    for (std::size_t index = 0; index < records.size(); ++index) {
        const auto& record = records[index];
        summary << "    {\"degree\": " << record.degree
                << ", \"channels\": " << record.channels
                << ", \"homogeneousChannels\": " << record.homogeneous
                << ", \"neumannTerms\": " << record.neumann_terms
                << ", \"maximumAbsoluteCentre\": " << std::scientific
                << std::setprecision(17) << record.maximum_centre
                << ", \"maximumRadius\": " << record.maximum_radius
                << ", \"elapsedSeconds\": " << std::fixed
                << std::setprecision(3) << record.elapsed << "}";
        if (index + 1 != records.size()) summary << ",";
        summary << "\n";
    }
    summary << "  ],\n";
    summary << "  \"centredMaximumRadius\": " << std::scientific
            << std::setprecision(17)
            << as_double_upper(maximum_value(centred_radius)) << ",\n";
    summary << "  \"elapsedSeconds\": " << std::fixed
            << std::setprecision(3) << omp_get_wtime() - started << ",\n";
    summary << "  \"limitations\": [\"heat coefficients are not enclosed\", \"signature defect is not enclosed\", \"no final heat sign or Navier-Stokes regularity claim\"]\n";
    summary << "}\n";
    std::cerr
        << "[R0.68B-2f quad +" << std::fixed << std::setprecision(2)
        << omp_get_wtime() - started
        << "s] complete centred_max_radius=" << std::scientific
        << as_double_upper(maximum_value(centred_radius)) << "\n";
    return 0;
}
