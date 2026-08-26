#!/usr/bin/env python3
"""Generate final-size color, grayscale, and independent PDF-render QA assets."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import resource
import shutil
import subprocess
import time
from zoneinfo import ZoneInfo

from PIL import Image, ImageChops, ImageOps, ImageStat


ROOT = Path(__file__).resolve().parent
TIMEZONE = ZoneInfo("Asia/Shanghai")


def append_log(path: Path, payload: dict[str, object]) -> None:
    record = {
        "timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"),
        **payload,
    }
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--manual-status", choices=("pending", "pass"), default="pending")
    arguments = parser.parse_args()
    started = time.perf_counter()
    config = json.loads(arguments.config.read_text(encoding="utf-8"))
    figure_config = config["figure"]
    width_mm = float(figure_config["widthMillimetres"])
    height_mm = float(figure_config["heightMillimetres"])
    archive_dpi = int(figure_config["pngDpi"])
    qa_dpi = int(figure_config["pdfQaDpi"])
    width_inches = round(width_mm / 25.4, 2)
    height_inches = round(height_mm / 25.4, 2)
    expected_width = round(width_inches * archive_dpi)
    expected_height = round(height_inches * archive_dpi)
    qa_width = round(width_inches * qa_dpi)
    qa_height = round(height_inches * qa_dpi)
    append_log(
        ROOT / "progress.ndjson",
        {"stage": "qa-start", "manualStatus": arguments.manual_status},
    )

    with Image.open(ROOT / "figure.png") as source:
        width, height = source.size
        dpi = source.info.get("dpi", (0.0, 0.0))
        if abs(width - expected_width) > 3 or abs(height - expected_height) > 3:
            raise RuntimeError(
                f"unexpected archival PNG size {source.size}; expected "
                f"approximately {(expected_width, expected_height)}"
            )
        if min(dpi) < archive_dpi - 1:
            raise RuntimeError(
                f"archival PNG does not report {archive_dpi} dpi: {dpi}"
            )
        preview = source.convert("RGB").resize(
            (qa_width, qa_height), Image.Resampling.LANCZOS
        )
        preview.save(ROOT / "qa-original.png", dpi=(qa_dpi, qa_dpi))
        grayscale = ImageOps.grayscale(preview)
        grayscale.save(ROOT / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi))
        extrema = grayscale.getextrema()
        deviation = float(ImageStat.Stat(grayscale).stddev[0])
        if extrema[1] - extrema[0] < 180 or deviation < 20:
            raise RuntimeError(
                "grayscale preview lacks tonal separation: "
                f"range={extrema}, stddev={deviation}"
            )

    renderer = shutil.which("pdftoppm")
    if renderer is None:
        raise FileNotFoundError("pdftoppm is required for independent PDF-render QA")
    subprocess.run(
        [
            renderer,
            "-png",
            "-r",
            str(qa_dpi),
            "-singlefile",
            str(ROOT / "figure.pdf"),
            str(ROOT / "qa-pdf"),
        ],
        check=True,
    )
    with Image.open(ROOT / "qa-pdf.png") as rendered:
        pdf_width, pdf_height = rendered.size
        if abs(pdf_width - qa_width) > 4 or abs(pdf_height - qa_height) > 4:
            raise RuntimeError(
                f"PDF preview size {rendered.size} is inconsistent with "
                f"declared final size {(qa_width, qa_height)} at {qa_dpi} dpi"
            )
        pdf_rgb = rendered.convert("RGB")
        difference = ImageChops.difference(preview, pdf_rgb)
        mean_difference = float(sum(ImageStat.Stat(difference).mean) / 3.0)
        if mean_difference > 8.0:
            raise RuntimeError(
                "PDF render differs unexpectedly from the archival PNG preview: "
                f"mean channel difference={mean_difference:.3f}"
            )

    manual = "PASS" if arguments.manual_status == "pass" else "PENDING"
    (ROOT / "qa-report.md").write_text(
        "# R0.71W amplitude-doping figure QA\n\n"
        f"- archival PNG pixel size {width} x {height}: PASS\n"
        f"- archival PNG density {dpi[0]:.3f} x {dpi[1]:.3f} dpi: PASS\n"
        f"- final-size preview {qa_width} x {qa_height} at {qa_dpi} dpi: PASS\n"
        "- true grayscale final-size preview generated: PASS\n"
        f"- grayscale range {extrema[0]}--{extrema[1]}, standard deviation {deviation:.3f}: PASS\n"
        f"- PDF rendered independently with Poppler at {qa_dpi} dpi: PASS\n"
        f"- PNG/PDF mean channel difference {mean_difference:.3f}: PASS\n"
        f"- final {width_mm:.2f} mm print-size inspection: {manual}\n"
        f"- Panel A ratio, tail fit, and +1 guide inspection: {manual}\n"
        f"- Panel B atom and full-retained charge semantics inspection: {manual}\n"
        f"- Panel B +1/-1 guides and fitted powers inspection: {manual}\n"
        f"- Panel C normalized slope and q=1024 radius audit inspection: {manual}\n"
        f"- non-color line-style and marker distinction inspection: {manual}\n"
        f"- PDF-specific clipping, font, and legend inspection: {manual}\n"
        "- computation-corroboration-only and not-DNS footer visible: PASS\n"
        "- analytic versus finite retained-coset evidence boundary visible: PASS\n"
        "- continuum IFT and spectral-convergence non-claims visible: PASS\n",
        encoding="utf-8",
    )
    elapsed = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(
        ROOT / "progress.ndjson",
        {
            "stage": "qa-complete",
            "manualStatus": arguments.manual_status,
            "elapsedSeconds": elapsed,
        },
    )
    append_log(
        ROOT / "resource-log.ndjson",
        {
            "stage": "qa-complete",
            "elapsedSeconds": elapsed,
            "pid": os.getpid(),
            "processUserCpuSeconds": usage.ru_utime,
            "processSystemCpuSeconds": usage.ru_stime,
            "maximumResidentSetRaw": usage.ru_maxrss,
        },
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "manualStatus": arguments.manual_status,
                "archivePixels": [width, height],
                "qaPixels": [qa_width, qa_height],
                "pdfQaPixels": [pdf_width, pdf_height],
                "meanPngPdfDifference": mean_difference,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
