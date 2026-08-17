#!/usr/bin/env julia

"""
Track the isolated torus roots of the saturated R0.20 stationary system.

The input is a tab-separated Float64 coefficient file produced by
``positive_region_stationary_audit.py --homotopy-terms``.  Float64 homotopy
continuation generates candidates and path-count evidence.  It is not the
final exact certificate.  Candidate roots are returned to Python for exact
rational Krawczyk certification and for checks against the target-zero set.

The solve is split into atomic checkpoint batches.  Re-running the same
command with the same run directory and seed resumes completed batches.
"""

using Dates
using HomotopyContinuation
using Printf
using SHA
using Serialization
using TOML


function parse_arguments(arguments)
    values = Dict{String,String}()
    flags = Set{String}()
    index = 1
    while index <= length(arguments)
        argument = arguments[index]
        if argument in ("--volume-only", "--no-resume", "--robust")
            push!(flags, argument)
            index += 1
        elseif startswith(argument, "--")
            index == length(arguments) && error("missing value after $argument")
            values[argument] = arguments[index + 1]
            index += 2
        else
            error("unexpected positional argument: $argument")
        end
    end
    for required in ("--terms", "--run-dir")
        haskey(values, required) || error("required option $required is missing")
    end
    return (
        terms = abspath(values["--terms"]),
        run_dir = abspath(values["--run-dir"]),
        batch_size = parse(Int, get(values, "--batch-size", "256")),
        seed = parse(UInt32, get(values, "--seed", "85983270")),
        expected_mixed_volume = parse(
            Int,
            get(values, "--expected-mixed-volume", "8376"),
        ),
        max_batches = parse(Int, get(values, "--max-batches", string(typemax(Int)))),
        volume_only = "--volume-only" in flags,
        resume = !("--no-resume" in flags),
        robust = "--robust" in flags,
    )
end


function json_value(value)
    if value isa AbstractString
        escaped = replace(
            value,
            "\\" => "\\\\",
            "\"" => "\\\"",
            "\n" => "\\n",
            "\r" => "\\r",
        )
        return "\"$escaped\""
    elseif value isa Bool
        return value ? "true" : "false"
    elseif value === nothing
        return "null"
    elseif value isa AbstractFloat && !isfinite(value)
        return "null"
    end
    return string(value)
end


function emit_progress(run_dir, stage; fields...)
    record = Pair{String,Any}[
        "timestampUtc" => string(now(UTC)),
        "stage" => stage,
    ]
    append!(record, [string(key) => value for (key, value) in fields])
    line = "{" * join(
        (json_value(key) * ":" * json_value(value) for (key, value) in record),
        ",",
    ) * "}"
    mkpath(run_dir)
    open(joinpath(run_dir, "progress.ndjson"), "a") do stream
        println(stream, line)
        flush(stream)
    end
    println(stderr, line)
    flush(stderr)
end


function read_system(path)
    @var p q x
    variables = [p, q, x]
    equations = [0.0p, 0.0q, 0.0x]
    term_counts = zeros(Int, 3)
    open(path, "r") do stream
        header = readline(stream)
        header == "equation\tp\tq\tx\tcoefficient" || error("invalid term header")
        for line in eachline(stream)
            fields = split(line, '\t')
            length(fields) == 5 || error("invalid term row")
            equation = parse(Int, fields[1])
            powers = parse.(Int, fields[2:4])
            coefficient = parse(Float64, fields[5])
            isfinite(coefficient) || error("non-finite coefficient")
            coefficient == 0.0 && error("zero coefficient in numerical support")
            monomial = coefficient
            for variable_index in 1:3
                monomial *= variables[variable_index]^powers[variable_index]
            end
            equations[equation] += monomial
            term_counts[equation] += 1
        end
    end
    return System(equations; variables = variables), term_counts
end


checkpoint_path(run_dir, batch_index) = joinpath(
    run_dir,
    "checkpoints",
    @sprintf("batch-%04d.jls", batch_index),
)


function save_checkpoint(path, path_results_batch)
    mkpath(dirname(path))
    temporary = path * ".tmp"
    open(temporary, "w") do stream
        serialize(stream, path_results_batch)
        flush(stream)
    end
    mv(temporary, path; force = true)
end


function load_checkpoint(path)
    open(path, "r") do stream
        return deserialize(stream)
    end
end


function write_solutions(run_dir, result)
    finite_solutions = solutions(
        result;
        only_nonsingular = false,
        only_finite = true,
        multiple_results = false,
    )
    open(joinpath(run_dir, "finite-solutions.tsv"), "w") do stream
        println(stream, "index\tpReal\tpImag\tqReal\tqImag\txReal\txImag")
        for (index, solution_value) in enumerate(finite_solutions)
            @printf(
                stream,
                "%d\t%.17g\t%.17g\t%.17g\t%.17g\t%.17g\t%.17g\n",
                index,
                real(solution_value[1]),
                imag(solution_value[1]),
                real(solution_value[2]),
                imag(solution_value[2]),
                real(solution_value[3]),
                imag(solution_value[3]),
            )
        end
    end

    real_candidates = real_solutions(
        result;
        atol = 1.0e-8,
        rtol = 1.0e-10,
        only_nonsingular = false,
        only_finite = true,
        multiple_results = false,
    )
    positive_candidates = filter(solution_value -> all(solution_value .> 0), real_candidates)
    open(joinpath(run_dir, "positive-real-candidates.tsv"), "w") do stream
        println(stream, "index\tp\tq\tx")
        for (index, solution_value) in enumerate(positive_candidates)
            @printf(
                stream,
                "%d\t%.17g\t%.17g\t%.17g\n",
                index,
                solution_value[1],
                solution_value[2],
                solution_value[3],
            )
        end
    end
    return length(finite_solutions), length(real_candidates), length(positive_candidates)
end


function main()
    arguments = parse_arguments(ARGS)
    arguments.batch_size > 0 || error("batch size must be positive")
    arguments.max_batches > 0 || error("max batches must be positive")
    mkpath(arguments.run_dir)
    emit_progress(
        arguments.run_dir,
        "loading normalized saturated system";
        threads = Threads.nthreads(),
        seed = arguments.seed,
    )
    system, term_counts = read_system(arguments.terms)
    emit_progress(
        arguments.run_dir,
        "computing mixed volume";
        termCounts = join(term_counts, ","),
    )
    mixed_volume_value = mixed_volume(system)
    mixed_volume_value == arguments.expected_mixed_volume || error(
        "mixed volume $mixed_volume_value != expected $(arguments.expected_mixed_volume)",
    )
    emit_progress(
        arguments.run_dir,
        "mixed volume verified";
        mixedVolume = mixed_volume_value,
    )

    if arguments.volume_only
        summary = Dict(
            "mode" => "volume-only",
            "mixedVolume" => mixed_volume_value,
            "termCounts" => term_counts,
            "inputTermsSha256" => bytes2hex(sha256(read(arguments.terms))),
            "juliaVersion" => string(VERSION),
            "homotopyContinuationVersion" => string(
                Base.pkgversion(HomotopyContinuation),
            ),
            "threads" => Threads.nthreads(),
            "seed" => Int(arguments.seed),
        )
        open(joinpath(arguments.run_dir, "summary.toml"), "w") do stream
            TOML.print(stream, summary; sorted = true)
        end
        return
    end

    emit_progress(arguments.run_dir, "constructing polyhedral start system")
    tracker_options = arguments.robust ? TrackerOptions(
        automatic_differentiation = 3,
        max_steps = 50_000,
        min_step_size = 1.0e-60,
        terminate_cond = 1.0e16,
        parameters = :conservative,
    ) : TrackerOptions()
    endgame_options = arguments.robust ? EndgameOptions(
        max_endgame_steps = 10_000,
        max_endgame_extended_steps = 4_000,
        max_winding_number = 20,
        sing_cond = 1.0e16,
        refine_steps = 5,
    ) : EndgameOptions()
    solver, starts_iterator = HomotopyContinuation.solver_startsolutions(
        system;
        seed = arguments.seed,
        start_system = :polyhedral,
        only_torus = true,
        show_progress = true,
        tracker_options = tracker_options,
        endgame_options = endgame_options,
    )
    starts = collect(starts_iterator)
    length(starts) == mixed_volume_value || error("start path count mismatch")
    emit_progress(
        arguments.run_dir,
        "polyhedral start system completed";
        totalPaths = length(starts),
    )

    batch_count = cld(length(starts), arguments.batch_size)
    batches_to_run = min(batch_count, arguments.max_batches)
    batches = Vector{Any}()
    tracked = 0
    solve_started = time()
    for batch_index in 1:batches_to_run
        first_index = (batch_index - 1) * arguments.batch_size + 1
        last_index = min(batch_index * arguments.batch_size, length(starts))
        checkpoint = checkpoint_path(arguments.run_dir, batch_index)
        if arguments.resume && isfile(checkpoint)
            batch_results = load_checkpoint(checkpoint)
            length(batch_results) == last_index - first_index + 1 || error(
                "checkpoint path count mismatch for batch $batch_index",
            )
            status = "loaded checkpoint"
        else
            batch_result = solve(
                deepcopy(solver),
                starts[first_index:last_index];
                show_progress = false,
                threading = true,
            )
            batch_results = collect(path_results(batch_result))
            save_checkpoint(checkpoint, batch_results)
            status = "tracked and checkpointed batch"
        end
        push!(batches, batch_results)
        tracked += length(batch_results)
        elapsed = time() - solve_started
        eta = tracked == 0 ? nothing : elapsed * (length(starts) - tracked) / tracked
        partial = Result(batch_results; seed = arguments.seed, start_system = :polyhedral)
        emit_progress(
            arguments.run_dir,
            status;
            batch = batch_index,
            batches = batch_count,
            completedPaths = tracked,
            totalPaths = length(starts),
            failedPaths = nfailed(partial),
            pathsAtInfinity = nat_infinity(partial),
            etaSeconds = eta,
        )
    end

    if batches_to_run < batch_count
        pilot_summary = Dict(
            "mode" => "partial-pilot",
            "mixedVolume" => mixed_volume_value,
            "completedPaths" => tracked,
            "totalPaths" => length(starts),
            "completedBatches" => batches_to_run,
            "totalBatches" => batch_count,
            "batchSize" => arguments.batch_size,
            "elapsedSolveSeconds" => time() - solve_started,
            "threads" => Threads.nthreads(),
            "seed" => Int(arguments.seed),
            "robustOptions" => arguments.robust,
        )
        open(joinpath(arguments.run_dir, "pilot-summary.toml"), "w") do stream
            TOML.print(stream, pilot_summary; sorted = true)
        end
        emit_progress(
            arguments.run_dir,
            "partial homotopy pilot completed";
            completedPaths = tracked,
            totalPaths = length(starts),
        )
        return
    end

    all_path_results = reduce(vcat, batches)
    result = Result(
        all_path_results;
        seed = arguments.seed,
        start_system = :polyhedral,
    )
    finite_count, real_count, positive_count = write_solutions(arguments.run_dir, result)
    summary = Dict(
        "mode" => "full-solve",
        "mixedVolume" => mixed_volume_value,
        "trackedPaths" => ntracked(result),
        "failedPaths" => nfailed(result),
        "pathsAtInfinity" => nat_infinity(result),
        "finiteSolutions" => finite_count,
        "nonsingularSolutions" => nnonsingular(result),
        "singularSolutions" => nsingular(result),
        "heuristicRealSolutions" => real_count,
        "positiveRealCandidates" => positive_count,
        "termCounts" => term_counts,
        "inputTermsSha256" => bytes2hex(sha256(read(arguments.terms))),
        "juliaVersion" => string(VERSION),
        "homotopyContinuationVersion" => string(Base.pkgversion(HomotopyContinuation)),
        "threads" => Threads.nthreads(),
        "seed" => Int(arguments.seed),
        "batchSize" => arguments.batch_size,
        "batchCount" => batch_count,
        "robustOptions" => arguments.robust,
    )
    open(joinpath(arguments.run_dir, "summary.toml"), "w") do stream
        TOML.print(stream, summary; sorted = true)
    end
    emit_progress(
        arguments.run_dir,
        "homotopy solve completed";
        trackedPaths = ntracked(result),
        failedPaths = nfailed(result),
        positiveRealCandidates = positive_count,
    )
end


main()
