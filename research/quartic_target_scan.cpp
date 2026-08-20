// Exploratory R0.61 scan of the complete quartic target coefficient.
//
// This program evaluates the exact path formula derived from the invariant
// shear recurrence, but uses long-double exponentials.  It is therefore a
// high-precision numerical exploration, not a proof or an exact certificate.

#include <algorithm>
#include <array>
#include <atomic>
#include <chrono>
#include <cmath>
#include <cstdint>
#include <filesystem>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <limits>
#include <sstream>
#include <stdexcept>
#include <string>
#include <thread>
#include <vector>

namespace {

using Clock = std::chrono::steady_clock;

struct KahanSum {
  long double sum = 0.0L;
  long double correction = 0.0L;

  void add(long double value) {
    const long double adjusted = value - correction;
    const long double updated = sum + adjusted;
    correction = (updated - sum) - adjusted;
    sum = updated;
  }
};

struct WorkerResult {
  KahanSum signed_sum;
  KahanSum absolute_sum;
  std::uint64_t paths = 0;
};

struct Arguments {
  int level_l = -1;
  int level_m = -1;
  int target = 0;
  unsigned int threads = std::max(1u, std::thread::hardware_concurrency());
  bool progress = false;
  std::filesystem::path output;
};

std::vector<int> rudin_shapiro(int level) {
  std::vector<int> p{1};
  std::vector<int> q{1};
  for (int step = 0; step < level; ++step) {
    std::vector<int> next_p = p;
    std::vector<int> next_q = p;
    next_p.insert(next_p.end(), q.begin(), q.end());
    for (const int value : q) next_q.push_back(-value);
    p = std::move(next_p);
    q = std::move(next_q);
  }
  return p;
}

long double factorial(int order) {
  if (order == 0 || order == 1) return 1.0L;
  if (order == 2) return 2.0L;
  if (order == 3) return 6.0L;
  throw std::logic_error("quartic scan only needs derivatives through order three");
}

long double simplex_kernel_three(
    std::array<std::int64_t, 4> integer_rates,
    std::int64_t high,
    long double terminal_time) {
  std::sort(integer_rates.begin(), integer_rates.end());
  std::array<long double, 4> nodes{};
  const long double high_squared =
      static_cast<long double>(high) * static_cast<long double>(high);
  for (std::size_t index = 0; index < nodes.size(); ++index) {
    nodes[index] = static_cast<long double>(integer_rates[index]) / high_squared;
  }

  std::array<std::array<long double, 4>, 4> divided{};
  for (int index = 0; index < 4; ++index) {
    divided[index][0] = std::exp(-terminal_time * nodes[index]);
  }
  for (int order = 1; order < 4; ++order) {
    for (int index = 0; index < 4 - order; ++index) {
      if (integer_rates[index + order] == integer_rates[index]) {
        divided[index][order] =
            std::pow(-terminal_time, order) *
            std::exp(-terminal_time * nodes[index]) / factorial(order);
      } else {
        divided[index][order] =
            (divided[index + 1][order - 1] - divided[index][order - 1]) /
            (nodes[index + order] - nodes[index]);
      }
    }
  }
  const long double kernel = -divided[0][3];
  if (!(kernel > 0.0L) || !std::isfinite(kernel)) {
    throw std::runtime_error("nonpositive or nonfinite third simplex kernel");
  }
  return kernel;
}

Arguments parse_arguments(int argc, char** argv) {
  Arguments arguments;
  for (int index = 1; index < argc; ++index) {
    const std::string option = argv[index];
    auto require_value = [&]() -> std::string {
      if (index + 1 >= argc) throw std::invalid_argument("missing value after " + option);
      return argv[++index];
    };
    if (option == "--level-l") {
      arguments.level_l = std::stoi(require_value());
    } else if (option == "--level-m") {
      arguments.level_m = std::stoi(require_value());
    } else if (option == "--target") {
      arguments.target = std::stoi(require_value());
    } else if (option == "--threads") {
      arguments.threads = static_cast<unsigned int>(std::stoul(require_value()));
    } else if (option == "--output") {
      arguments.output = require_value();
    } else if (option == "--progress") {
      arguments.progress = true;
    } else {
      throw std::invalid_argument("unknown option: " + option);
    }
  }
  if (arguments.level_l < 0 || arguments.level_m < 0) {
    throw std::invalid_argument("--level-l and --level-m are required");
  }
  if (arguments.level_l > 20 || arguments.level_m > 20) {
    throw std::invalid_argument("dyadic levels above twenty are outside this scanner");
  }
  arguments.threads = std::max(1u, arguments.threads);
  return arguments;
}

std::string encode_result(
    int level_l,
    int level_m,
    std::int64_t length,
    std::int64_t outputs,
    std::int64_t high,
    int target,
    unsigned int threads,
    const WorkerResult& total,
    long double quadratic_sum,
    long double normalized_constant,
    double wall_seconds) {
  const long double cancellation_condition =
      std::abs(total.signed_sum.sum) > 0.0L
          ? total.absolute_sum.sum / std::abs(total.signed_sum.sum)
          : std::numeric_limits<long double>::infinity();
  std::ostringstream stream;
  stream << std::setprecision(21);
  stream << "{\n"
         << "  \"schemaVersion\": \"0.1-exploratory\",\n"
         << "  \"classification\": \"long-double evaluation of the complete quartic path formula; not a proof\",\n"
         << "  \"levelL\": " << level_l << ",\n"
         << "  \"levelM\": " << level_m << ",\n"
         << "  \"L\": " << length << ",\n"
         << "  \"M\": " << outputs << ",\n"
         << "  \"H\": " << high << ",\n"
         << "  \"target\": " << target << ",\n"
         << "  \"threads\": " << threads << ",\n"
         << "  \"orderedQuarticPaths\": " << total.paths << ",\n"
         << "  \"dimensionlessQuadraticKernelSum\": " << quadratic_sum << ",\n"
         << "  \"dimensionlessQuarticKernelSum\": " << total.signed_sum.sum << ",\n"
         << "  \"absoluteQuarticKernelSum\": " << total.absolute_sum.sum << ",\n"
         << "  \"cancellationConditionNumber\": " << cancellation_condition << ",\n"
         << "  \"normalizedSignedRatio\": " << normalized_constant << ",\n"
         << "  \"normalization\": \"L^2*(G4/G2)/epsilon^2 for A=epsilon*sqrt(H)\",\n"
         << "  \"phaseRelation\": \"positive normalized ratio means G4 opposes G2\",\n"
         << "  \"terminalDimensionlessTime\": " << std::log(2.0L) / 2.0L << ",\n"
         << "  \"wallSeconds\": " << wall_seconds << "\n"
         << "}\n";
  return stream.str();
}

}  // namespace

int main(int argc, char** argv) {
  try {
    const Arguments arguments = parse_arguments(argc, argv);
    const std::int64_t length = std::int64_t{1} << arguments.level_l;
    const std::int64_t outputs = std::int64_t{1} << arguments.level_m;
    const std::int64_t count = length * outputs;
    const std::int64_t high = 4 * count;
    if (high > 1'000'000'000LL) {
      throw std::invalid_argument(
          "H exceeds the int64-safe squared-rate range of this scanner");
    }
    const int target = arguments.target == 0 ? static_cast<int>(outputs) : arguments.target;
    if (target < 1 || target > outputs) {
      throw std::invalid_argument("target must lie in one through M");
    }

    const auto signs_l = rudin_shapiro(arguments.level_l);
    const auto signs_m = rudin_shapiro(arguments.level_m);
    std::vector<int> signs(static_cast<std::size_t>(count));
    for (std::int64_t block = 0; block < outputs; ++block) {
      for (std::int64_t offset = 0; offset < length; ++offset) {
        signs[static_cast<std::size_t>(block * length + offset)] =
            signs_m[static_cast<std::size_t>(block)] *
            signs_l[static_cast<std::size_t>(offset)];
      }
    }
    const auto carrier_sign = [&](std::int64_t carrier) -> int {
      return signs.at(static_cast<std::size_t>(carrier - high));
    };

    const long double terminal_time = std::log(2.0L) / 2.0L;
    KahanSum quadratic;
    const std::int64_t q_start = high + (target - 1) * length;
    const std::int64_t q_stop = q_start + length;
    for (std::int64_t q = q_start; q < q_stop; ++q) {
      const long double scaled_q = static_cast<long double>(q) / high;
      quadratic.add(
          (1.0L - std::exp(-2.0L * scaled_q * scaled_q * terminal_time)) /
          (2.0L * scaled_q * scaled_q));
    }

    const std::uint64_t tasks =
        static_cast<std::uint64_t>(length) * static_cast<std::uint64_t>(count);
    const unsigned int worker_count = static_cast<unsigned int>(
        std::min<std::uint64_t>(arguments.threads, std::max<std::uint64_t>(1, tasks)));
    std::vector<WorkerResult> workers(worker_count);
    std::vector<std::thread> threads;
    threads.reserve(worker_count);
    std::atomic<std::uint64_t> completed{0};
    const auto started = Clock::now();

    if (arguments.progress) {
      std::cerr << "[R0.61] starting quartic scan"
                << " L=" << length << " M=" << outputs << " target=" << target
                << " tasks=" << tasks << " threads=" << worker_count << '\n';
    }

    for (unsigned int worker = 0; worker < worker_count; ++worker) {
      threads.emplace_back([&, worker]() {
        WorkerResult& result = workers[worker];
        for (std::uint64_t task = worker; task < tasks; task += worker_count) {
          const std::int64_t q_index = static_cast<std::int64_t>(task / count);
          const std::int64_t a_index = static_cast<std::int64_t>(task % count);
          const std::int64_t q = q_start + q_index;
          const std::int64_t a = high + a_index;
          for (std::int64_t b = high; b < high + count; ++b) {
            const std::int64_t c = a + b - q;
            if (c < high || c >= high + count) continue;
            const int sign =
                carrier_sign(q) * carrier_sign(a) * carrier_sign(b) * carrier_sign(c);
            const std::array<std::array<std::int64_t, 3>, 3> paths{{
                {a, b, -c},
                {a, -c, b},
                {-c, a, b},
            }};
            for (const auto& path : paths) {
              const std::int64_t p1 = path[0];
              const std::int64_t p2 = path[1];
              const std::int64_t p3 = path[2];
              const std::int64_t k1 = -q + p1;
              const std::int64_t k2 = k1 + p2;
              if (k2 + p3 != 0) throw std::logic_error("quartic target path failed");
              const std::array<std::int64_t, 4> rates{{
                  q * q + p1 * p1 + p2 * p2 + p3 * p3,
                  k1 * k1 + p2 * p2 + p3 * p3,
                  k2 * k2 + p3 * p3,
                  0,
              }};
              const long double kernel =
                  simplex_kernel_three(rates, high, terminal_time);
              result.signed_sum.add(sign * kernel);
              result.absolute_sum.add(kernel);
              ++result.paths;
            }
          }
          ++completed;
        }
      });
    }

    if (arguments.progress) {
      while (completed.load() < tasks) {
        std::this_thread::sleep_for(std::chrono::seconds(1));
        const double elapsed = std::chrono::duration<double>(Clock::now() - started).count();
        const std::uint64_t done = completed.load();
        const double rate = done / std::max(1.0, elapsed);
        const double eta = rate > 0.0 ? (tasks - done) / rate : 0.0;
        std::cerr << "[R0.61 +" << std::fixed << std::setprecision(1) << elapsed
                  << "s] tasks=" << done << '/' << tasks
                  << " rate=" << rate << "/s eta=" << eta << "s\n";
      }
    }
    for (auto& thread : threads) thread.join();

    WorkerResult total;
    for (const WorkerResult& worker : workers) {
      total.signed_sum.add(worker.signed_sum.sum);
      total.absolute_sum.add(worker.absolute_sum.sum);
      total.paths += worker.paths;
    }
    const long double normalized_constant =
        static_cast<long double>(length) * length * target * target /
        (static_cast<long double>(high) * high * high) *
        total.signed_sum.sum / quadratic.sum;
    const double wall_seconds =
        std::chrono::duration<double>(Clock::now() - started).count();
    const std::string encoded = encode_result(
        arguments.level_l,
        arguments.level_m,
        length,
        outputs,
        high,
        target,
        worker_count,
        total,
        quadratic.sum,
        normalized_constant,
        wall_seconds);
    if (arguments.output.empty()) {
      std::cout << encoded;
    } else {
      std::filesystem::create_directories(arguments.output.parent_path());
      std::ofstream output(arguments.output);
      if (!output) throw std::runtime_error("cannot open output file");
      output << encoded;
    }
    return 0;
  } catch (const std::exception& error) {
    std::cerr << "quartic_target_scan: " << error.what() << '\n';
    return 1;
  }
}
