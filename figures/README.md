# Figure and simulation archive

This directory holds paper-ready quantitative figures and the evidence needed to regenerate them. The public site may use lighter copies, but a formal figure should always be traceable to one package here.

## Package layout

Use one directory per figure:

```text
figures/<study>/<figure-id>/
├── caption.md
├── manifest.json
├── plot.py
├── data.csv              # or .json/.npz/.h5 plus a documented schema
├── figure.pdf            # vector, preferred paper asset
├── figure.svg            # vector, preferred web/source asset
└── figure.png            # 600 dpi print raster
```

Large raw simulation states do not have to live in Git. In that case the manifest's `sourceData` records must give stable storage locations, file names, byte sizes, SHA-256 hashes, and the exact extraction command that produced the plotted table retained in the package.

## Required evidence

Every formal package records:

- the analytical question and the single claim supported by the figure;
- the simulation or audit command, parameters, solver tolerances, precision, and random seed;
- the git commit, Python/package environment, operating system, hardware, process/thread count, and wall time;
- the source-data schema, units, filters, and any normalization;
- checksums for data and exported assets;
- an English paper caption and, when used on the site, a concise Chinese explanation;
- whether the figure passed final-size, grayscale, label, legend, and scale checks.

## Process monitoring

Formal simulations must not be silent. Write machine-readable records while the job is running:

- `progress.ndjson` records a timestamp, elapsed wall time, stage, step, physical time, residual or stopping metric, CFL when applicable, divergence/conservation diagnostics, the latest checkpoint, and an estimated remaining time;
- `resources.csv` records CPU utilization, resident memory, process/thread count, and—when a GPU is used—GPU utilization, device memory, and temperature;
- checkpoint creation, numerical warnings, failed steps, restarts, and parameter changes are appended to the log rather than erased;
- each monitoring log is listed in the manifest's `data` records so its size and SHA-256 are checked with the scientific data.

During an active run, report meaningful progress to the user at stage transitions and at the declared monitoring interval. A report should distinguish a solver step from physical progress and should say explicitly when an ETA is not yet reliable.

Wrap the solver command to capture the independent resource log:

```bash
python3 research/run_with_monitor.py \
  --output figures/<study>/<figure-id>/resources.csv \
  --interval 60 -- \
  python3 research/simulation.py --config config.json
```

The wrapper follows the complete child-process tree. On a DGX/NVIDIA host it samples `nvidia-smi`; on the local Mac, unavailable GPU fields remain empty rather than being guessed. The simulation code must still write the scientific `progress.ndjson` log.

Use `manifest.template.json` as the starting point. Do not mark `qa.status` as `passed` before inspecting the actual PDF/SVG and 600 dpi PNG.

## Journal export defaults

- Single column: 85 mm wide.
- Double column: 178 mm wide.
- Default text: 8 pt at final size; never below the journal minimum.
- Vector formats: PDF and SVG.
- Raster fallback: PNG at 600 dpi; 300 dpi is allowed only for continuous-tone imagery when the target journal permits it.
- Fonts: embedded and consistent with the manuscript.
- Lines and markers must remain distinguishable in grayscale. Color is supplementary, not the sole encoding.
- Titles are neutral descriptions. Units, domain, resolution, sample size, or time interval belong in labels, subtitle, or caption.
- Avoid cropped labels, deceptive truncated axes, decorative gradients, and screenshots of interactive plots.

The shared Matplotlib defaults are in `journal.mplstyle`. Individual journals may override dimensions or fonts, but the manifest must name the journal profile used.

Set the physical canvas in the plotting source rather than relying on a screen default. For example, an 85 mm by 55 mm single-column panel starts with:

```python
import matplotlib.pyplot as plt

with plt.style.context("figures/journal.mplstyle"):
    figure, axis = plt.subplots(figsize=(85 / 25.4, 55 / 25.4))
    # Draw from the archived source data here.
    for suffix in ("pdf", "svg", "png"):
        figure.savefig(package / f"figure.{suffix}")
```

The shared 254 dpi working canvas corresponds to 10 pixels per millimetre, which prevents Matplotlib from silently shortening the vector canvas during pixel quantization. `savefig.dpi` independently fixes the archival PNG at 600 dpi.

Install the pinned research environment from `requirements-research.txt`. Before a formal figure is committed, run:

```bash
python3 research/validate_figure_package.py figures/<study>/<figure-id>
```

The command checks the manifest, provenance, expected formats, file hashes, and recorded QA decisions. It cannot replace inspecting the PDF/SVG and grayscale PNG at their final physical size.
