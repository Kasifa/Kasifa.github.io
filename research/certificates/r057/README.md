# R0.57 exact signed normal-channel aggregation certificate

## Scope

This directory archives the deterministic exact regression attached to the
R0.57 note.  The analytic note proves that the normalized fixed-output
Fourier--Leray operator

\[
 \mathfrak B_k(U,V)
 =|k|^{-1}P_k\sum_{p+q=k}(q\cdot U_p)V_q
\]

has the sharp bound

\[
 |\mathfrak B_k(U,V)|\leq\|U\|_{2,k}\|V\|_{2,k}.
\]

For every integer \(L\geq1\), the frequencies

\[
 k=e_2,\qquad p_N=(N,0,0),\qquad q_N=(-N,1,0),
 \qquad L\leq N<2L,
\]

with polarizations \(U_{p_N}=c_Ne_2\) and \(V_{q_N}=c_Ne_3\) attain
equality.  Their reality partners give a real-valued divergence-free Fourier
polynomial.  The modes lie in one dyadic shell and two shrinking antipodal
caps.  All forward normal contributions have the same phase, while each
exchanged contribution is zero.

The displayed proof in
research/signed_normal_aggregation_note.md establishes the all-index
statements.  The finite loops archived here are exact implementation
regressions, not substitutes for that proof.

The high-to-low coherence mechanism is classical and is not claimed as new.
R0.57 records its exact alignment with the R0.56 normal channel and the
resulting no-go theorem for a shell- or cap-decaying fixed-output constant.
The result does not estimate the time-integrated Duhamel operator, close a
large-data critical norm, or prove any claim about three-dimensional
Navier--Stokes regularity or singularity.

## Pinned source

The successful formal run is pinned to

    001a40b166d20c912e78fca4d565c3e2eadd3203

The audit source is
research/signed_normal_aggregation_audit.py.

## Exact run

From the repository root:

    tmp/r024-venv/bin/python research/run_with_monitor.py \
      --output research/certificates/r057/resources.csv \
      --interval 0.25 \
      -- \
      tmp/r024-venv/bin/python \
      research/signed_normal_aggregation_audit.py \
      --packet-size 200000 \
      --max-family-index 1000000 \
      --source-commit 001a40b166d20c912e78fca4d565c3e2eadd3203 \
      --progress \
      --progress-log research/certificates/r057/progress.ndjson \
      --check \
      --pretty \
      --output research/certificates/r057/signed-normal-aggregation.json

The run passed 20 checks.  It verified:

- a packet with 200,000 coherent high-frequency pairs;
- 800,002 supported modes after adding reality partners and the output pair;
- exactly 400,000 ordered pairs at the fixed output;
- 200,000 unit forward normal contributions and 200,000 zero reverse
  contributions;
- an exact squared fixed-output norm ratio of one;
- exact single-mode nonlinear energy input of 200,000;
- 1,000,000 all-index frequency, divergence, channel, and heat-exponent
  identities;
- an additional 100,000-coefficient exact signed Cauchy--Schwarz regression.

The finite-regression digests stored inside the certificate are:

    coherent packet  a4f2eacbb02611fff4583c285254af9cc377421bc2897248e5e8d59374ce5b90
    all-index family f706b138bd107593929e60ea616bcc9f828fdd293ce8c58da88b786d473b8e08

## Monitoring and retained restart

The successful scientific audit reported 5.745230 seconds of wall time.  The
independent process-tree monitor recorded 23 samples over 5.796003 seconds,
with peak CPU usage 100.0% and peak resident memory 434.328 MiB.  No GPU
process was used.

The first formal attempt was intentionally stopped after 36.657777 seconds.
Its pair-presence regression used a list and therefore scaled quadratically.
The failed run reached 434.844 MiB peak resident memory and exited after a
keyboard interrupt.  Its resource and stage logs are retained as
resources-attempt-01-failed.csv and progress-attempt-01-failed.ndjson.
Commit 001a40b166d20c912e78fca4d565c3e2eadd3203 replaced that list by a set,
leaving the mathematical algorithm unchanged and reducing the successful run
to linear expected-time membership checks.

The successful run used Python 3.12.13 with exact integers and Gaussian-integer
pairs.  It used no randomness, GPU kernel, or floating-point mathematical
decision.

## Files

- signed-normal-aggregation.json: machine-readable theorem classification,
  exact regressions, digests, checks, and provenance;
- progress.ndjson: append-only stages from the successful run;
- resources.csv: process-tree samples from the successful run;
- progress-attempt-01-failed.ndjson: retained stage log from the stopped
  quadratic implementation;
- resources-attempt-01-failed.csv: retained resource log from that attempt;
- SHA256SUMS: hashes of all archived content files.

## Literature boundary

The coherent high-to-low mechanism is prior work:

- J. Bourgain and N. Pavlović, *Ill-posedness of the Navier--Stokes equations
  in a critical space in 3D*, Journal of Functional Analysis 255 (2008),
  2233--2247, <https://arxiv.org/abs/0807.0882>.
- A. Cheskidov and M. Dai, *Norm inflation for generalized Navier--Stokes
  equations*, Indiana University Mathematics Journal 63 (2014), 869--884,
  <https://arxiv.org/abs/1212.3801>.

R0.57 does not present frequency-pair coherence or norm inflation as a new
idea.
