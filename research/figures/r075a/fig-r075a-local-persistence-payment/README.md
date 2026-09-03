# R0.75A Figure Archive — Local Persistence/Payment Dichotomy

Reproducible journal-scale **analytic schematic** for frozen R0.75A; no PDE simulation, DNS, sampled trajectory, or empirical fit.

- **A:** exact normalized moving-strip and nested-core geometry.
- **B:** two exhaustive local-energy branches, both yielding `X >= c E_* R^3`.
- **C:** Hölder, scale-`2R` weight, and endpoint substitution give (A.1) and positive rate `64279/238140000`.
- **D:** proved local result versus open complete-clock/fixed-deletion branches; next target (A.63).

Bindings: main `f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388`; primary `c599a1dcee8a82ec1c91512d5b664b1394707fd6d69ac2ca7ba022ebf715d3f6` (PASS/0); literature `169eff2e607338ae990fb9994db3f75e11830246a36ee5cce8a7376e64302cea` (citation/framing PASS, not novelty); core commit `d15b7d8f9a3b16b63b4f324c75c9e156e9d03ff8`.

```bash
CODEX_PYTHON=/path/to/bundled/python3
R075A_DEPS_DIR=/path/to/version-pinned/dependencies
REPOSITORY=/path/to/navier-stokes-r074m
FIG=research/figures/r075a/fig-r075a-local-persistence-payment
env PYTHONPATH="$R075A_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/plot.py" --deps "$R075A_DEPS_DIR" --repository "$REPOSITORY" --render
env PYTHONPATH="$R075A_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/validate.py" --repository "$REPOSITORY" --seal
env PYTHONPATH="$R075A_DEPS_DIR" "$CODEX_PYTHON" -B "$FIG/validate.py" --repository "$REPOSITORY" --verify-only
```

The automated seal does not replace the recorded final-size, grayscale, and
PDF visual inspection in `qa-report.md`.

**ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE SIMULATION | NOT DNS | NO NOVELTY CLAIM | NOT CLAY**
