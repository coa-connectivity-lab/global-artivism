# Note: Côa river line check (2026-09-30)

**Status:** open, decide in late October 2026 (before Global Artivism Month opens on 1 November).

## What was checked

The Côa river line on `img/map-movement.png`, `img/map-water.png` and `img/map-connection.png` looked wrong. It was checked against a fresh OpenStreetMap download in a QGIS project, with the website PNGs georeferenced exactly to their source rasters.

Full method, data, QGIS project and scripts: `Solo-field-illustrator-project-for-Rewilding-Portugal/global-artivism/coa-river-check/` (commit `4c9d5b0`, merged to `main`). Findings in `analysis.md`, numbers in `output/metrics.csv`.

## What was found

- **The river line is correct.** It is the OSM Côa (31 ways, 143.7 km), identical to a fresh Overpass download, and it runs from the Serra da Malcata to the Douro confluence. The PNGs draw it within 50 m, under one image pixel.
- **The rasters are not offset.** The water and connection surfaces line up best with the river at zero shift.
- **Two gaps, invisible at this scale:** 241 m at the Sabugal dam wall and 16 m where two OSM ways don't join.
- **The north arrow is wrong by 11.9°.** `render_maps.py` plots in EPSG:3035, where true north points 11.9° clockwise of "up" in this area, but draws "N" straight up. The whole map reads about 12° clockwise of a north-up web map. This is most likely why the line "looks off".
- **The Douro isn't drawn**, so the Côa ends mid-map and the strong northern corridors (Douro, Sabor/Vilariça) have no context.

`data/field-sites.geojson` is not affected. It is exported in WGS84 (EPSG:4326) and shown on a north-up Leaflet map.

## Options to decide

1. **Redraw the three maps** in EPSG:3763 (PT-TM06, north-up here): `da.rio.reproject(3763)` and `river.to_crs(3763)` in `scripts/render_maps.py`. Optionally add the Douro as a lighter line and label Sabugal and Vila Nova de Foz Côa. Figures 4, 5 and 7 of the Zenodo preprint are the same images, so update them together (see the note in `portfolio/zenodo-article/`).
2. **Keep the maps and fix only the arrow**: rotate it 11.9° clockwise.
3. **Keep as is** and add a line to the map credit: "Projection ETRS89-LAEA (EPSG:3035); grid north, about 12° from true north."
