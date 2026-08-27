# R0.72S figure QA report

Status: **PASSED**

Automatic-only run: `False`

- [x] `required_assets` — all formal assets exist
- [x] `png_final_size_600_dpi` — PNG is final size at 600 dpi
- [x] `pdf_one_page_final_size` — PDF is one page at declared final size
- [x] `svg_editable_vector` — SVG retains editable text and no raster image
- [x] `final_size_and_grayscale_qa` — QA surfaces match final size and grayscale contrast gate
- [x] `runtime_lineage` — all runtime inputs are canonical, hash-stable repository files
- [x] `source_certificate_and_build_commits` — source and certificate/package blobs bind clean declared commits
- [x] `flat_certificate_ledger` — flat SHA256SUMS exactly seals the certificate bundle
- [x] `package_source_hashes` — all package sources retain build hashes
- [x] `r072s_parameter_and_contract_consistency` — config and contract encode the certified R0.72S strata and heat collisions
- [x] `data_schema_and_size` — data table has the exact schema, minimum size, and three panels
- [x] `required_series_and_sampling_intervals` — every declared exact, leading, and persistent series covers its configured interval
- [x] `panel_a_exact_higher_stratum_spine` — A4 closure and the two A5 points match the exact incidence formulas
- [x] `panel_b_exact_a2_branches` — the A2 exact branches and leading squared law match their formulas
- [x] `panel_c_exact_a3_branches` — the A3 exact, leading, and persistent branches match their formulas
- [x] `public_assets_byte_identical` — public PDF, SVG, and PNG are byte-identical to masters
- [x] `claim_boundary_text` — figure text preserves proof, literature, and scope boundaries
- [x] `results_contract` — results record no PDE, no fit, and exact data count
- [x] `explicit_visual_inspection` — R072S_VISUAL_QA_INSPECTED=true after final-size, grayscale, and PDF inspection

Visual inspection must use the final-size, grayscale, and PDF-raster QA surfaces.
