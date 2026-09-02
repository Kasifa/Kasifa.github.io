# Visual QA protocol

1. Render the PDF independently at 600 dpi and compare every pixel with the
   master PNG.
2. Inspect the 300 dpi print-size derivative for text overlap, clipping,
   hierarchy, and readable status labels.
3. Inspect the grayscale derivative for non-colour redundancy.
4. Inspect the SVG in Quick Look when available; retain physical dimensions,
   embedded fonts, and the same boundary language.
5. Run `validate.py`; publication requires every machine check to pass.
