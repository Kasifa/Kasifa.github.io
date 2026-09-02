# R0.74P final source rebind audit

## Verdict

**PASS.**  The final mathematical source, problem freeze, finite certificate,
independent implementation, literature repair, and figure claim contract are
consistent at the hashes below.  No content blocker remains.

## Frozen bindings

| Artifact | SHA-256 |
|---|---|
| `research/r074p_problem_freeze.md` | `3f505349846dbb57d977a866a8b7a7bb98ea14cac09eed31277cabddb3920300` |
| `research/r074p_temporal_observable_triage.md` | `a3cb872735b92b32ddfa7b96bc4184d70b0287ff2ce7d3da8cadbbcc494d0867` |
| `research/r074p_temporal_clock_certificate.json` | `c65b38def48b5439f112ab145360c1abb211de5bf6f004eca103271d8d9a204b` |
| `research/r074p_temporal_clock_certificate_report.md` | `ebe8dff8c6a7d50c0471b98771b8e3c9a74fc1f69a2199b999b0d8ddd568fc4c` |
| `scripts/r074p_temporal_clock_certificate.py` | `be56854234c8467158549e84b0e306340de97eb017a5f909384099a5942cdf6c` |
| `scripts/r074p_temporal_clock_certificate_independent.rb` | `9e003997ce86c5330603c5dbfd309dd3d8293dd953a8293657bdf905b39012b6` |
| `research/r074p_primary_literature_boundary.md` | `18dfd23433cc4930c3a62f25a73f82bb6970d634bc48ebb6f5df7fd83025204e` |
| `research/r074p_gap_matrix.md` | `11462a348a817f53f8dda39aa63950470ef6ba888a5ce41bc11aa7e91cb6beae` |
| `research/r074p_report-source.md` | `d1602097fce2ae86089ff5dea678be6d5330366ca867886f51488aabf7c435d4` |

## Formal checks

- Main note: 87 displayed equation tags, all 87 unique.
- Problem freeze: 56 displayed equation tags, all 56 unique.
- Display delimiters, TeX environments, braces, and the targeted malformed
  command scan pass.
- `git diff --check` passes.
- Python certificate output is byte-identical to the frozen JSON.
- Independent Ruby reconstruction passes 52/52 checks.
- The three \(\sigma>1\) certificate rows use
  `right-endpoint-supremum`; the report states that the supremum is approached
  as \(x\uparrow1\) and is not attained for \(J\Subset I_R\).
- The figure contract shows only the decay-rate term and explicitly
  suppresses the unknown additive \(\log_{10}C\).

## Claim rebind

The final sources agree on all high-risk boundaries:

1. every window no-go is for each fixed \(\sigma>0\), nonuniform as
   \(\sigma\downarrow0\);
2. only the target component (v_{j,R}) has a two-sided (T_*) bound;
3. the full (Y_{2,R}^{\rm sf}) has a lower detection bound but no proved
   full-family upper bound;
4. suitable-weak clock stability is Version M, fixed (R), and fixed
   terminal point;
5. Lei--Ren's spatial intervals and regularity epochs are both disclosed,
   and Yu 2026 is identified as adjacent rather than identical;
6. no bounded non-hit is promoted to novelty or priority;
7. no singularity, regularity, continuation, or Clay theorem is claimed.

**NOT CLAY.**
