// Independent structural verifier for R0.68B-2f binary128 output arrays.

#include <algorithm>
#include <array>
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

static_assert(sizeof(f128) == 16, "expected 16-byte IEEE binary128");
static_assert(FLT_RADIX == 2, "expected radix-two arithmetic");
static_assert(__FLT128_MANT_DIG__ == 113, "unexpected _Float128 precision");

namespace {

constexpr std::uint64_t EXPECTED_VALUES = 14350336;

f128 absolute(f128 value) { return value < 0 ? -value : value; }

double as_double_upper(f128 value) {
    double output = (double)value;
    if ((f128)output < value) output = std::nextafter(output, INFINITY);
    return output;
}

struct Scan {
    std::uint64_t count = 0;
    std::uint64_t nonfinite = 0;
    std::uint64_t negative = 0;
    f128 maximum_absolute = 0;
};

Scan scan_file(const std::string& filename, bool radius) {
    std::ifstream input(filename, std::ios::binary);
    if (!input) throw std::runtime_error("cannot open " + filename);
    std::vector<f128> buffer(1 << 20);
    Scan scan;
    while (input) {
        input.read(
            reinterpret_cast<char*>(buffer.data()),
            (std::streamsize)(buffer.size() * sizeof(f128))
        );
        const auto bytes = input.gcount();
        if (bytes % (std::streamsize)sizeof(f128) != 0) {
            throw std::runtime_error("partial binary128 value in " + filename);
        }
        const std::size_t values = (std::size_t)bytes / sizeof(f128);
        for (std::size_t index = 0; index < values; ++index) {
            const f128 value = buffer[index];
            if (!__builtin_isfinite(value)) ++scan.nonfinite;
            if (radius && value < 0) ++scan.negative;
            if (__builtin_isfinite(value)) {
                scan.maximum_absolute = std::max(
                    scan.maximum_absolute,
                    absolute(value)
                );
            }
        }
        scan.count += values;
    }
    if (!input.eof()) throw std::runtime_error("read failure in " + filename);
    return scan;
}

}  // namespace

int main(int argc, char** argv) {
    if (argc != 2) {
        std::cerr << "usage: verifier OUTPUT_DIRECTORY\n";
        return 2;
    }
    const std::string directory = argv[1];
    const std::array<std::string, 4> names = {
        "raw-centre.f128",
        "raw-radius.f128",
        "centred-centre.f128",
        "centred-radius.f128",
    };
    std::array<Scan, 4> scans;
    for (std::size_t index = 0; index < names.size(); ++index) {
        scans[index] = scan_file(
            directory + "/" + names[index],
            index == 1 || index == 3
        );
        if (
            scans[index].count != EXPECTED_VALUES
            || scans[index].nonfinite != 0
            || scans[index].negative != 0
        ) {
            throw std::runtime_error("output validation failed for " + names[index]);
        }
    }
    std::cout << "{\n"
              << "  \"status\": \"verified\",\n"
              << "  \"valuesPerArray\": " << EXPECTED_VALUES << ",\n"
              << "  \"allValuesFinite\": true,\n"
              << "  \"allRadiiNonnegative\": true,\n"
              << "  \"rawMaximumRadiusUpper\": " << std::scientific
              << std::setprecision(17)
              << as_double_upper(scans[1].maximum_absolute) << ",\n"
              << "  \"centredMaximumRadiusUpper\": "
              << as_double_upper(scans[3].maximum_absolute) << "\n"
              << "}\n";
    return 0;
}
