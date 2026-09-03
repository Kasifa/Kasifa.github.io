# R0.74S Step 18 — certificate QA report

## Verdict

**PASS**

The complete QA command was

    scripts/r074s_fixed_deletion_qa.sh

It was run from the repository root on Darwin arm64 with Python 3.9.6 and
Ruby 2.6.10.  The runner also repeated the producers from a different
working directory.

## Positive certificates

| Producer | Result | Exact workload |
|---|---:|---:|
| Python primary certificate | PASS, 15/15 groups | 283,157 finite rational cases |
| Ruby independent verifier | PASS, 8/8 groups | 72,144 independent assertions |

The two programs do not import or invoke one another.  The Ruby verifier
reads the final primary JSON only after independently recomputing its own
mathematics, then checks the schema, source hashes, and required primary
check identifiers.

## Reproducibility checks

The Python JSON and Markdown report were regenerated with
PYTHONHASHSEED equal to 0, 1, and 42 from /tmp.  Each pair was byte-identical
to the repository outputs:

\[
 3/3\text{ seeds PASS}.
\]

The Ruby report was regenerated from /tmp and was byte-identical to the
repository output:

\[
 1/1\text{ cross-working-directory run PASS}.
\]

## Fail-closed mutation matrix

Every intentional mutation returned a nonzero status and produced a FAIL
verdict.

| Mutation | Python | Ruby | Protected invariant |
|---|---:|---:|---|
| minimax_order | REJECTED | REJECTED | \(\sup\inf\le\inf\sup\) direction |
| layer_cake | REJECTED | REJECTED | best-\(N\) layer-cake identity |
| q_payment | REJECTED | REJECTED | one full \(B_Q\) payment in (S.483) |
| reverse_six | REJECTED | REJECTED | Step 10 coefficient six in (S.484) |
| triangle_fixed | REJECTED | REJECTED | \(\mathfrak H_N^{\rm fix}=H\) |
| triangle_separable | REJECTED | REJECTED | \((M-N)H\) separable tail |
| ledger_power | REJECTED | REJECTED | fixed-\(N\) \(2/3\)-power obstruction |
| tag_inventory | REJECTED | REJECTED | unique ordered S.476--S.493 |
| claim_boundary | REJECTED | REJECTED | OPEN / ABSTRACT / NOT CLAY labels |
| source_hash | REJECTED | REJECTED | frozen Step 18 theorem bytes |
| literature_hash | REJECTED | REJECTED | frozen primary-source audit bytes |
| dependency_hash | REJECTED | REJECTED | Step 10/15/17 inherited inputs |
| primary_schema | not applicable | REJECTED | cross-implementation result contract |

Totals:

\[
 12/12\text{ Python mutations rejected},\qquad
 13/13\text{ Ruby mutations rejected}.
\]

## Scope boundary

This QA proves that the finite arithmetic and structural certificate fail
closed under the listed perturbations.  It does not convert finite testing
into a machine proof of suitable-weak local-energy theory, dense good-time
closure, the Taylor continuum asymptotics, the open fixed-deletion gate,
regularity, or the Navier--Stokes Millennium problem.
