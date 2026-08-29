# Visual QA protocol

1. Confirm one-page PDF dimensions are 178 by 132 mm.
2. Confirm the PNG is 4205 by 3118 pixels with 600 dpi metadata.
3. Rasterize the PDF at 180 dpi and compare its layout with the PNG master.
4. Inspect a 1100-pixel final-size preview for text collisions, clipping,
   panel-label order, legend readability, and honest logarithmic axes.
5. Inspect a grayscale rendering for curve and marker distinguishability.
6. Confirm SVG text remains vector text and no raster image is embedded.
7. Confirm every panel says or implies its finite/sampled boundary and the
   caption states the full non-claim boundary.
