# R0.74P figure QA report

Overall result: **PASS**

- Exact source rows: 147 Panel A + 5 Panel B.
- 600 dpi master dimensions: 4205 x 2363 pixels.
- PDF and SVG geometry independently checked at 178 mm x 100 mm.
- PDF re-render compared pixel-for-pixel with the archived PNG master.
- Final-size, grayscale, and independent SVG Quick Look derivatives created.
- Required PROVED / OPEN / target-component / NOT CLAY language found.

Visual inspection remains a human/agent QA step; this script does not infer readability from pixels.

## Check ledger

- PASS — `source_row_counts`
- PASS — `source_unique_ids`
- PASS — `panel_a_exact_formula_147_of_147`
- PASS — `panel_b_exact_ledger_5_of_5`
- PASS — `certificate_52_all_pass`
- PASS — `certificate_exact_inputs`
- PASS — `strong_rate_independent_ratio`
- PASS — `png_mode_rgb`
- PASS — `png_600dpi_dimensions`
- PASS — `pdf_one_page`
- PASS — `pdf_page_geometry`
- PASS — `svg_physical_geometry_and_units`
- PASS — `svg_required_boundary_language`
- PASS — `caption_required_boundary_language`
- PASS — `svg_final_size_text_minimum_5pt`
- PASS — `svg_fonts_embedded`
- PASS — `validator_dependencies_frozen`
- PASS — `independent_pdf_raster_matches_master`
- PASS — `svg_independent_quicklook`
- PASS — `required_external_bindings_present`
