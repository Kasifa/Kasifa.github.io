# R0.74S visual QA protocol

1. Render the PDF independently at 600 dpi and compare every pixel with the master PNG.
2. Inspect the 300 dpi print-size derivative for overlap, clipping, hierarchy, and readable status labels.
3. Inspect the grayscale derivative for non-colour redundancy.
4. Inspect the SVG in Quick Look when available and verify physical dimensions and embedded fonts.
5. Check every PROVED ABSTRACT NO-GO / OPEN / NOT PDE-NSE boundary against source rows.
6. Run `validate.py`; publication requires every required machine check to pass.
