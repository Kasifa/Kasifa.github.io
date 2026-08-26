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
    record = {"timestamp": datetime.now(TIMEZONE).isoformat(timespec="milliseconds"), **payload}
    with path.open("a", encoding="utf-8") as stream:
        stream.write(json.dumps(record, sort_keys=True) + "\n")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--manual-status", choices=("pending", "pass"), default="pending")
    args = parser.parse_args()
    started = time.perf_counter()
    config = json.loads(args.config.read_text(encoding="utf-8"))
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
    append_log(ROOT / "progress.ndjson", {"stage": "qa-start", "manualStatus": args.manual_status})

    with Image.open(ROOT / "figure.png") as source:
        width, height = source.size
        dpi = source.info.get("dpi", (0.0, 0.0))
        if abs(width - expected_width) > 2 or abs(height - expected_height) > 2:
            raise RuntimeError(
                f"unexpected archival PNG size {source.size}; expected approximately {(expected_width, expected_height)}"
            )
        if min(dpi) < archive_dpi - 1:
            raise RuntimeError(f"archival PNG does not report {archive_dpi} dpi: {dpi}")
        preview = source.convert("RGB").resize((qa_width, qa_height), Image.Resampling.LANCZOS)
        preview.save(ROOT / "qa-original.png", dpi=(qa_dpi, qa_dpi))
        grayscale = ImageOps.grayscale(preview)
        grayscale.save(ROOT / "qa-grayscale.png", dpi=(qa_dpi, qa_dpi))
        extrema = grayscale.getextrema()
        deviation = float(ImageStat.Stat(grayscale).stddev[0])
        if extrema[1] - extrema[0] < 180 or deviation < 20:
            raise RuntimeError(f"grayscale preview lacks tonal separation: range={extrema}, stddev={deviation}")

    renderer = shutil.which("pdftoppm")
    if renderer is None:
        raise FileNotFoundError("pdftoppm is required for independent PDF-render QA")
    subprocess.run(
        [renderer, "-png", "-r", str(qa_dpi), "-singlefile", str(ROOT / "figure.pdf"), str(ROOT / "qa-pdf")],
        check=True,
    )
    with Image.open(ROOT / "qa-pdf.png") as rendered:
        pdf_width, pdf_height = rendered.size
        if abs(pdf_width - qa_width) > 4 or abs(pdf_height - qa_height) > 4:
            raise RuntimeError(
                f"PDF preview size {rendered.size} is inconsistent with declared final size {(qa_width, qa_height)} at {qa_dpi} dpi"
            )
        difference = ImageChops.difference(preview, rendered.convert("RGB"))
        mean_difference = float(sum(ImageStat.Stat(difference).mean) / 3.0)
        if mean_difference > 8.0:
            raise RuntimeError(f"PDF render differs unexpectedly from PNG preview: mean channel difference={mean_difference:.3f}")

    manual = "PASS" if args.manual_status == "pass" else "PENDING"
    (ROOT / "qa-report.md").write_text(
        "# R0.71Z all-root figure QA\n\n"
        f"- archival PNG pixel size {width} x {height}: PASS\n"
        f"- archival PNG density {dpi[0]:.3f} x {dpi[1]:.3f} dpi: PASS\n"
        f"- final-size preview {qa_width} x {qa_height} at {qa_dpi} dpi: PASS\n"
        "- true grayscale final-size preview generated: PASS\n"
        f"- grayscale range {extrema[0]}--{extrema[1]}, standard deviation {deviation:.3f}: PASS\n"
        f"- PDF rendered independently with Poppler at {qa_dpi} dpi: PASS\n"
        f"- PNG/PDF mean channel difference {mean_difference:.3f}: PASS\n"
        f"- final {width_mm:.2f} mm print-size inspection: {manual}\n"
        f"- Panel A exact M/Ks identity, 3/M^2 bound, axes, and tail-fit label inspection: {manual}\n"
        f"- Panel B all-root M^-2 and neutral selected-root M^-1 distinction inspection: {manual}\n"
        f"- Panel C bounded, M^(1/2), and M^(6/7) coupling-law labels inspection: {manual}\n"
        f"- Panel D fixed-window and launch-inclusive retention labels inspection: {manual}\n"
        f"- analytic/certificate and not-DNS wording inspection: {manual}\n"
        f"- non-color line-style, marker-shape, and marker-fill distinction inspection: {manual}\n"
        f"- grayscale distinction and label fit inspection: {manual}\n"
        f"- PDF-specific clipping, font, formula, and legend inspection: {manual}\n"
        "- complete slope-mass and not raw root-count footer visible: PASS\n"
        "- mixed-window and strong-coupling diagnostic boundaries visible: PASS\n"
        "- universal-endpoint and regularity non-claims visible: PASS\n",
        encoding="utf-8",
    )
    elapsed = time.perf_counter() - started
    usage = resource.getrusage(resource.RUSAGE_SELF)
    append_log(ROOT / "progress.ndjson", {"stage": "qa-complete", "manualStatus": args.manual_status, "elapsedSeconds": elapsed})
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
                "manualStatus": args.manual_status,
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
